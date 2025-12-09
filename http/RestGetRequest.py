import requests

# Указываем URL для GET-запроса
url = 'https://my-json-server.typicode.com/inetcoyote/users-api/users/2'

try:
    # Выполняем GET-запрос
    response = requests.get(url, verify=False)


    # Проверяем статус-код ответа
    if response.status_code == 200:
        # Успешный запрос
        print("Response received:")
        # Выводим полученные данные в формате JSON
        print(response.json())
    else:
        print("Failed to retrieve data:", response.status_code)

except requests.exceptions.RequestException as e:
    # Обработка ошибок, если запрос не удался
    print("An error occurred:", e)