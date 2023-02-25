# Сервис YaCut


## Описание проекта

Сервис `YaCut` - это сервис укорачивания ссылок и `API` к нему

Ключевые возможности сервиса:
* генерация коротких ссылок и связь их с исходными длинными ссылками
* переадресация на исходный адрес при обращении к коротким ссылкам

Пользовательский интерфейс сервиса — одна страница с формой. Эта форма состоит из двух полей:
* обязательного для длинной исходной ссылки
* необязательного для пользовательского варианта короткой ссылки (не должен превышать 16 символов)

Если пользователь предложит вариант короткой ссылки, который уже занят, то появляется соответствующее уведомление. Существующая в базе данных ссылка должна остаться неизменной.

Если пользователь не заполнит поле со своим вариантом короткой ссылки, то сервис должен сгенерировать её автоматически. Формат для ссылки по умолчанию — шесть случайных символов, в качестве которых можно использовать:
* большие латинские буквы,
* маленькие латинские буквы,
* цифры в диапазоне от 0 до 9.

Автоматически сгенерированная короткая ссылка добавляется в базу данных, но только если в ней уже нет такого же идентификатора. В противном случае идентификатор генерируется заново.

## Установка и запуск проекта

1. Клонировать проект на компьютер
```
git clone https://github.com/sidelkin1/yacut.git
```
2. Создание виртуального окружения
```
python -m venv venv
```
3. Запуск виртуального окружения
```
. venv/bin/activate
```
4. Установить зависимости из файла `requirements.txt`
```
pip install -r requirements.txt
```
5. Создать базу данных `SQLite`
```
flask db upgrade
```
6. Запуск приложения
```
flask run
```

## API для проекта

API проекта доступен всем желающим. Сервис обслуживает только два эндпоинта:
* **/api/id/** — POST-запрос на создание новой короткой ссылки;
* **/api/id/<short_id>/** — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.

Примеры запросов к API, варианты ответов и ошибок приведены в спецификации `openapi.yml`.


## Примеры запросов

**GET** `.../api/id/{short_id}/`
*200*
```
{
  "url": "string"
}
```
*404*
```
{
  "message": "Указанный id не найден"
}
```


**POST** `.../api/id/`
```
{
  "url": "string",
  "custom_id": "string"
}
```
*201*
```
{
  "url": "string",
  "short_link": "string"
}
```
*400*
```
{
  "message": "Отсутствует тело запроса"
}
```


## Шаблон наполнения .env файла
```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```

## Техническая информация

Стек технологий: Python 3.9, Flask 2.0, SQLAlchemy 1.4, Alembic 1.7.

---
## Об авторе

[Константин Сидельников](https://github.com/sidelkin1)