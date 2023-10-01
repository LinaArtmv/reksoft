# Веб-приложение на Python

## Технологии

- [Python 3.10](https://www.python.org/downloads/)


## Запуск проекта в docker-контенерах:

```sudo docker compose build```
```sudo docker compose up```
```http://localhost:8001/resources/```

## Наполнение БД тестовыми данными:
```sudo docker exec -i reksoft-db-1 psql -U linaart -d reksoft < data.txt```

## Пример POST-запроса на адрес /resources/: 
```
{
    "name": "Э103",
    "current_speed": 60,
    "type_id": 2
}
```
Пример ответа:
```
{
    "id": 1,
    "name": "Э103",
    "current_speed": "60",
    "type": "Экскаватор",
    "over_speed": "50"
}
```

## Пример GET-запроса на адреса /resources/ и /resources/?type=1/
```
[
    {
        "id": 2,
        "name": "Э104",
        "current_speed": "0",
        "type": "Экскаватор",
        "over_speed": "-100"
    },
    {
        "id": 1,
        "name": "Э104",
        "current_speed": "85",
        "type": "Экскаватор",
        "over_speed": "113"
    }
]
```

## Пример GET-запроса на адрес /resource/1/:
```
{
    "id": 1,
    "name": "Э104",
    "current_speed": "85",
    "type": "Экскаватор",
    "over_speed": "40"
}
```

## Пример PUT-запроса на адрес /resource/1/:
```
{
    "name": "Э103",
    "current_speed": 60,
    "type_id": 2
}
```

## Пример DELETE-запроса на адрес /resource/1/:
```
'Успешное удаление'
```

## Пример POST-запроса на адрес /types/: 
```
{
    "name": "Самосвал",
    "max_speed": 40
}
```

Пример ответа:
```
{
    "id": 1,
    "name": "Самосвал",
    "max_speed": "80"
}
```

## Пример GET-запроса на адрес /types/
```
[
    {
        "id": 2,
        "name": "Экскаватор",
        "max_speed": "40"
    },
    {
        "id": 1,
        "name": "Самосвал",
        "max_speed": "80"
    }
]
```

## Пример GET-запроса на адрес /type/1/:
```
{
    "id": 1,
    "name": "Самосвал",
    "max_speed": "80"
}
```

## Пример PUT-запроса на адрес /type/1/:
```
{
    "name": "Экскаватор",
    "max_speed": 60
}
```

## Пример DELETE-запроса на адрес /type/1/:
```
'Успешное удаление'
```

## Пример DELETE-запроса на адрес /delete/:
```
{
    "resources": [1, 2],
    "types": [1, 2]
}
```
Пример ответа:
```
'Успешное удаление'
```
