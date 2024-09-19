import requests

url = "http://localhost:8000/salary"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX2RvZSIsImV4cCI6MTcxNDQwNDgyMX0.TRXRJKXLJckiOi1qApmijF4objVnwVxmUR4qUzEl9QQ"
}

response = requests.get(url, headers=headers)

print(response.json())
