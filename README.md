# Обмен валют 

REST API для описания валют и обменных курсов.   
Позволяет просматривать и редактировать списки валют и обменных курсов, и совершать расчёт конвертации произвольных сумм из одной валюты в другую.  


## Запуск проекта
### Через виртуальное окружение
1. Склонировать репозиторий https://github.com/ratmeow/currency_exchanger.git
2. Выполнить `python -m venv venv`
3. Установить зависимости `pip install -r requirements.txt`
4. Запустите скрипт, выполнив `python main.py` в терминале.

* Backend будет доступен по адресу http://127.0.0.1:8080
* Описание эндпоинтов доступно на http://127.0.0.1:8080/docs

### Через docker
1. Склонировать репозиторий https://github.com/ratmeow/currency_exchanger.git
2. Выполнить `docker-compose up -d`

* Backend будет доступен на http://127.0.0.1:8080
* Frontend будет доступен на http://127.0.0.1:3000

## Тестирование
1. Установить переменные среды в режим тестирования `export TEST_MODE=True`
2. Перейти в папку с тестами `cd tests`
3. Выполнить `pytest currency.py` или `pytest exchange_rates.py`

## Примечание
* При первом запуске проекта создается файл БД и заполняется начальными данными
* Начальные данные можно изменить, отредактировав `data/schema.sql`
* Также создается файл `package.log`, который будет содержать логи приложения

## Preview
![Описание изображения](docs/page.png)

## Стек 

* Python 3.10
* fastapi
* SQLite