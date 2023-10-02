# API сервиса YaMDb

## Описание

Групповой проект по API от Яндекс Практикума, в котором была реализован сервис, который собирает произведения и отзывы пользователей к ним.
  
## Стек

- Python
- Django
- DRF
- JWT

## Настройка проекта

- Клонируйте репозиторий

```bash
git clone
```

- Установите и активируйте виртуальное окружение

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

```bash
python -m pip install --upgrade pip
```

- Установите зависимости из файла requirements.txt

```bash
pip install -r requirements.txt
```

- Выполните миграции

```bash
python manage.py migrate
```

- Запустите проект

```bash
python manage.py runserver
```

## Примеры некоторых запросов API

Регистрация пользователя:  
``` POST /api/v1/auth/signup/ ```  
Получение JWT-токена в обмен на username и confirmation code:  
``` POST /api/v1/auth/token/ ```  
Добавление новой категории:  
``` POST /api/v1/categories/ ```  
Удаление категории:  
``` DELETE /api/v1/categories/{slug} ```  
Частичное обновление информации о произведении:  
``` PATCH /api/v1/titles/{titles_id} ```  
Получение списка всех отзывов:  
``` GET /api/v1/titles/{title_id}/reviews/ ```   
Добавление нового отзыва:  
``` POST /api/v1/titles/{title_id}/reviews/ ```    

## Полный список запросов API находится в документации по адресу http://127.0.0.1:8000/redoc/
____
Для тестирования работы приложения в терминале [Postman][1] можете воспользоваться коллекцией запросов из папки [postman_collection][2].

## Авторы

##### Чурилов Александр - [https://github.com/HopedForLuck]
##### Горбунов Александр - [https://github.com/Alexander-Gorbunov-gth]

[1]: https://www.postman.com/
[2]: ./postman_collection/
