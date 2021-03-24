# CurrencyConverter
Pet Project

Сервер: HTTPServer

Установка и запуск через docker-compose:
1. Клонировать проект
2. В папке проекта в терминале вызвать docker-compose up

Сервис доступен по адресу 127.0.0.1:9000

## Доступные запросы:

GET '/'
127.0.0.1:9000/?currency=&amount=

currency = [usd, eur]
Тип валюты

amount = любое число
Количество валюты

### Возвращаемое значение

JSON:
{
  given_currency: "string",
  given_amount: "number",
  conversion_currency: "string",
  conversion_amount: "number"
}

Пример выполнения:
http://127.0.0.1:9000/?currency=usd&amount=30
Response: {"given_currency": "usd", "given_amount": 30.0, "conversion_currency": "RUB", "conversion_amount": 2282.406}
  
