from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import date, datetime, timedelta
import jwt
from passlib.context import CryptContext
import jwt.exceptions

app = FastAPI()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

users_db = {
    "john_doe": {
        "password": hash_password("123"),  # хэшированный пароль
        "salary": 50000,
        "promotion_date": "2024-01-01"
    },
    "jane_smith": {
        "password": hash_password("456"),  # хэшированный пароль
        "salary": 60000,
        "promotion_date": "2024-05-01"
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    password: str

class Salary(BaseModel):
    salary: int
    next_promotion_date: datetime

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    return users_db.get(username)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(user: User):
    db_user = get_user(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

def get_current_user(token: str = Depends(authenticate_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(user: User):
    try:
        return authenticate_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/salary", response_model=Salary)
async def read_user_salary(current_user: dict = Depends(get_current_user)):
    try:
        return Salary(salary=current_user["salary"], next_promotion_date=date.fromisoformat(current_user["promotion_date"]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Hello World"}
