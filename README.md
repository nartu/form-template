# Тествовое задание

## Условия

1. На вход по урлу `/get_form` POST запросом передаются данные такого вида: `f_name1=value1&f_name2=value2`

2. В БД хранятся шаблоны в json формате вида
  ```
  {
      "name": "Form template name",
      "field_name_1": "email",
      "field_name_2": "phone"
  }
```

3. Сервис возращает имена шаблонов в случае если найдены. Сначала определяется тип переданных данных, потом вычисляются совпадения.
Совпадающие шаблоны те, все поля которых пристуствуют в запросе, но в запросе полей может быть больше чем в шаблоне.

4. Если шаблон не найден, возращается кастомный. Т.е имена полей и их определённые сервисом типы. По умолчанию тип `text`, так же есть `date`, `email`, `phone`.

Подробнее
https://docs.google.com/document/d/1fMFwPBs53xzcrltEFOpEG4GWTaQ-5jvVLrNT6_hmC7I/edit


## Использование

1. Запуск `docker-compose up -d`

2. Тесты `docker exec -ti app pytest tests`

3. Примеры запросов `./examples.sh` на хосте (из докер-контейнера поставить localhost и порт 80)


## Миграция

1. Заполнить таблицу шаблонов данными из json файла, по умолчанию /app/dump_last.json `curl -XPUT http://127.0.1.20:8000/migrate`

2. Очистить таблицу шаблонов `curl -XPUT http://127.0.1.20:8000/clear_all`

3. Импортировать таблицу шаблонов в json файл, по умолчанию в /app/dump/dumb_{unix-time}.json `curl -XPOST http://127.0.1.20:8000/save_to_file`
