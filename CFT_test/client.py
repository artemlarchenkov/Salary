import requests

def get_access_token(username, password):
    url = "http://localhost:8000/token"
    data = {"username": username, "password": password}  # параметры в теле запроса
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Error:", response.text)
        return None

def get_salary(access_token):
    url = "http://localhost:8000/salary"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    print("Request URL:", response.request.url)
    print("Request Headers:", response.request.headers)
    print("Response:", response.text)
    return response.json()

username = input("Введите ваше имя пользователя: ")
password = input("Введите ваш пароль: ")

access_token = get_access_token(username, password)
if access_token:
    print("Токен доступа:", access_token)
    salary = get_salary(access_token)
    print("Зарплата и дата следующего повышения:", salary)
