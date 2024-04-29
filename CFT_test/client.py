import requests


def get_access_token(username, password):
    url = "http://localhost:8000/token"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Ошибка:", response.text)
        return None


def get_salary(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "http://localhost:8000/salary"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Ошибка:", response.text)
        return None


if __name__ == "__main__":
    username = input("Введите ваше имя пользователя: ")
    password = input("Введите ваш пароль: ")

    access_token = get_access_token(username, password)
    if access_token:
        print("Токен доступа:", access_token)

        salary = get_salary(access_token)
        if salary:
            print("Зарплата:", salary)
