# Бэк для работы PythonZooBot, для работы нужно:
1. Файл с переменными окружений (.env): databaseName (Имя БД), databaseUser (пользователь БД), databasePassword (пароль БД), databaseHost (Хост БД), databasePort (Порт БД), ya_token (токен яндекса для использования YandexGPT), ya_catalog_key (ключ яндекса для использования YandexGPT)
2. Установка библиотек (есть в файле requirements.txt) - pip install -m requirements.txt
3. Запуск производится при помощи uvicorn - uvicorn PythonDjangoZoo.asgi:application --host 127.0.0.1 --port 4200
