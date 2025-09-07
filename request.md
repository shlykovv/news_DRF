# API Documentation - Django Blog Project

## Базовые настройки

**Base URL:** `http://127.0.0.1:8000/`

### Переменные окружения в Postman:

- `base_url`: `http://127.0.0.1:8000`
- `access_token`: (получается после авторизации)
- `refresh_token`: (получается после авторизации)

---

# ПРИЛОЖЕНИЕ ACCOUNTS - Управление пользователями

## 1. Регистрация пользователя

- **Метод:** `POST`
- **URL:** `{{base_url}}/api/v1/auth/register/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!",
  "first_name": "Иван",
  "last_name": "Иванов"
}
```

- **Ответ (201):**

```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "full_name": "Иван Иванов",
    "avatar": null,
    "bio": "",
    "created_at": "2025-09-07T12:00:00Z",
    "updated_at": "2025-09-07T12:00:00Z",
    "posts_count": 0,
    "comments_count": 0
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "User registered successfull"
}
```

## 2. Авторизация пользователя

- **Метод:** `POST`
- **URL:** `{{base_url}}/api/v1/auth/login/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**

```json
{
  "email": "test@example.com",
  "password": "SecurePassword123!"
}
```

- **Ответ (200):**

```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "full_name": "Иван Иванов",
    "avatar": null,
    "bio": "",
    "created_at": "2025-09-07T12:00:00Z",
    "updated_at": "2025-09-07T12:00:00Z",
    "posts_count": 0,
    "comments_count": 0
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "User login successfull"
}
```

## 3. Получить профиль пользователя

- **Метод:** `GET`
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Ответ (200):**

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Иван",
  "last_name": "Иванов",
  "full_name": "Иван Иванов",
  "avatar": null,
  "bio": "",
  "created_at": "2025-09-07T12:00:00Z",
  "updated_at": "2025-09-07T12:00:00Z",
  "posts_count": 2,
  "comments_count": 5
}
```

## 4. Обновить профиль пользователя

- **Метод:** `PUT`
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "first_name": "Иван",
  "last_name": "Петров",
  "bio": "Разработчик Python и Django"
}
```

## 5. Частичное обновление профиля

- **Метод:** `PATCH`
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "bio": "Обновленная биография пользователя"
}
```

## 6. Обновить профиль с аватаром

- **Метод:** `PUT`
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Body (form-data):**
  - `first_name`: "Иван"
  - `last_name`: "Петров"
  - `bio`: "Разработчик Python и Django"
  - `avatar`: [файл изображения]

## 7. Изменить пароль

- **Метод:** `PUT`
- **URL:** `{{base_url}}/api/v1/auth/change-password/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "old_password": "SecurePassword123!",
  "new_password": "NewSecurePassword456!",
  "new_password_confirm": "NewSecurePassword456!"
}
```

- **Ответ (200):**

```json
{
  "message": "Password changed successfull"
}
```

## 8. Обновить Access Token

- **Метод:** `POST`
- **URL:** `{{base_url}}/api/v1/auth/refresh-token/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**

```json
{
  "refresh": "{{refresh_token}}"
}
```

- **Ответ (200):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 9. Выход пользователя (Logout)

- **Метод:** `POST`
- **URL:** `{{base_url}}/api/v1/auth/logout/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "refresh_token": "{{refresh_token}}"
}
```

- **Ответ (200):**

```json
{
  "message": "Logout successfull"
}
```

## 10. Удалить профиль

- **Метод:** `DELETE`
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`

---

# ПРИЛОЖЕНИЕ MAIN - Блог (Категории и Посты)

## КАТЕГОРИИ

### 11. Получить список всех категорий

- **Метод:** `GET`
- **URL:** `{{base_url}}/categories/`
- **Headers:** `Content-Type: application/json`
- **Authorization:** не требуется
- **Ответ (200):**

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Технологии",
      "slug": "tehnologii",
      "description": "Статьи о современных технологиях",
      "posts_count": 5,
      "created_at": "2025-09-07T10:00:00Z"
    }
  ]
}
```

### 12. Создать новую категорию

- **Метод:** `POST`
- **URL:** `{{base_url}}/categories/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "name": "Веб-разработка",
  "description": "Статьи о веб-разработке и frontend/backend технологиях"
}
```

### 13. Получить категорию по slug

- **Метод:** `GET`
- **URL:** `{{base_url}}/categories/veb-razrabotka/`
- **Headers:** `Content-Type: application/json`

### 14. Обновить категорию

- **Метод:** `PUT`
- **URL:** `{{base_url}}/categories/veb-razrabotka/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "name": "Современная веб-разработка",
  "description": "Обновленное описание категории"
}
```

### 15. Удалить категорию

- **Метод:** `DELETE`
- **URL:** `{{base_url}}/categories/veb-razrabotka/`
- **Headers:** `Authorization: Bearer {{access_token}}`

### 16. Поиск категорий

- **Метод:** `GET`
- **URL:** `{{base_url}}/categories/?search=веб`
- **Headers:** `Content-Type: application/json`

### 17. Сортировка категорий

- **Метод:** `GET`
- **URL:** `{{base_url}}/categories/?ordering=-created_at`
- **Headers:** `Content-Type: application/json`

## ПОСТЫ

### 18. Получить список всех постов

- **Метод:** `GET`
- **URL:** `{{base_url}}/`
- **Headers:** `Content-Type: application/json`
- **Authorization:** не требуется (публичные посты)
- **Ответ (200):**

```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Введение в Django REST Framework",
      "slug": "vvedenie-v-django-rest-framework",
      "content": "Django REST Framework - это мощный инструмент...",
      "image": null,
      "category": "Технологии",
      "author": "test@example.com",
      "status": "PUBLISHED",
      "created_at": "2025-09-07T12:00:00Z",
      "updated_at": "2025-09-07T12:00:00Z",
      "views_count": 15,
      "comments_count": 3
    }
  ]
}
```

### 19. Создать новый пост

- **Метод:** `POST`
- **URL:** `{{base_url}}/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "title": "Руководство по Python для начинающих",
  "content": "Python - это высокоуровневый язык программирования, который отлично подходит для начинающих разработчиков. В этой статье мы рассмотрим основы языка...",
  "category": 1,
  "status": "PUBLISHED"
}
```

### 20. Создать пост с изображением

- **Метод:** `POST`
- **URL:** `{{base_url}}/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Body (form-data):**
  - `title`: "Визуализация данных в Python"
  - `content`: "В этой статье рассматриваем различные способы визуализации данных..."
  - `category`: 1
  - `status`: "PUBLISHED"
  - `image`: [файл изображения]

### 21. Создать черновик поста

- **Метод:** `POST`
- **URL:** `{{base_url}}/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "title": "Неопубликованная статья",
  "content": "Это черновик статьи, который пока не готов к публикации...",
  "category": 1,
  "status": "DRAFT"
}
```

### 22. Получить конкретный пост по slug

- **Метод:** `GET`
- **URL:** `{{base_url}}/rukovodstvo-po-python-dlya-nachinayushchih/`
- **Headers:** `Content-Type: application/json`
- **Ответ (200):**

```json
{
  "id": 2,
  "title": "Руководство по Python для начинающих",
  "slug": "rukovodstvo-po-python-dlya-nachinayushchih",
  "content": "Python - это высокоуровневый язык программирования...",
  "image": null,
  "category": 1,
  "author": 1,
  "status": "PUBLISHED",
  "created_at": "2025-09-07T14:00:00Z",
  "updated_at": "2025-09-07T14:00:00Z",
  "views_count": 1,
  "comments_count": 0,
  "author_info": {
    "id": 1,
    "username": "testuser",
    "full_name": "Иван Петров",
    "avatar": null
  },
  "category_info": {
    "id": 1,
    "name": "Технологии",
    "slug": "tehnologii"
  }
}
```

### 23. Обновить пост

- **Метод:** `PUT`
- **URL:** `{{base_url}}/rukovodstvo-po-python-dlya-nachinayushchih/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "title": "Полное руководство по Python для начинающих",
  "content": "Обновленное и расширенное содержимое статьи...",
  "category": 1,
  "status": "PUBLISHED"
}
```

### 24. Частичное обновление поста

- **Метод:** `PATCH`
- **URL:** `{{base_url}}/rukovodstvo-po-python-dlya-nachinayushchih/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (JSON):**

```json
{
  "status": "DRAFT"
}
```

### 25. Удалить пост

- **Метод:** `DELETE`
- **URL:** `{{base_url}}/rukovodstvo-po-python-dlya-nachinayushchih/`
- **Headers:** `Authorization: Bearer {{access_token}}`

## ФИЛЬТРАЦИЯ И ПОИСК ПОСТОВ

### 26. Поиск постов по заголовку или содержимому

- **Метод:** `GET`
- **URL:** `{{base_url}}/?search=Python`
- **Headers:** `Content-Type: application/json`

### 27. Фильтрация по категории

- **Метод:** `GET`
- **URL:** `{{base_url}}/?category=1`
- **Headers:** `Content-Type: application/json`

### 28. Фильтрация по автору

- **Метод:** `GET`
- **URL:** `{{base_url}}/?author=1`
- **Headers:** `Content-Type: application/json`

### 29. Фильтрация по статусу (только для авторизованных)

- **Метод:** `GET`
- **URL:** `{{base_url}}/?status=DRAFT`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`

### 30. Сортировка постов по популярности

- **Метод:** `GET`
- **URL:** `{{base_url}}/?ordering=-views_count`
- **Headers:** `Content-Type: application/json`

### 31. Сортировка постов по дате создания

- **Метод:** `GET`
- **URL:** `{{base_url}}/?ordering=-created_at`
- **Headers:** `Content-Type: application/json`

### 32. Комбинированные фильтры

- **Метод:** `GET`
- **URL:** `{{base_url}}/?category=1&status=PUBLISHED&search=Django&ordering=-created_at`
- **Headers:** `Content-Type: application/json`

## СПЕЦИАЛЬНЫЕ ЭНДПОИНТЫ

### 33. Получить мои посты

- **Метод:** `GET`
- **URL:** `{{base_url}}/my-posts/`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`

### 34. Получить популярные посты (ТОП-10)

- **Метод:** `GET`
- **URL:** `{{base_url}}/popular/`
- **Headers:** `Content-Type: application/json`
- **Ответ (200):**

```json
[
  {
    "id": 5,
    "title": "Самая популярная статья",
    "slug": "samaya-populyarnaya-statya",
    "content": "Краткое содержимое...",
    "image": null,
    "category": "Технологии",
    "author": "author@example.com",
    "status": "PUBLISHED",
    "created_at": "2025-09-06T10:00:00Z",
    "updated_at": "2025-09-06T10:00:00Z",
    "views_count": 150,
    "comments_count": 25
  }
]
```

### 35. Получить последние посты (ТОП-10)

- **Метод:** `GET`
- **URL:** `{{base_url}}/recent/`
- **Headers:** `Content-Type: application/json`

### 36. Получить посты определенной категории

- **Метод:** `GET`
- **URL:** `{{base_url}}/categories/tehnologii/posts/`
- **Headers:** `Content-Type: application/json`
- **Ответ (200):**

```json
{
  "category": {
    "id": 1,
    "name": "Технологии",
    "slug": "tehnologii",
    "description": "Статьи о современных технологиях",
    "posts_count": 8,
    "created_at": "2025-09-01T12:00:00Z"
  },
  "posts": [
    {
      "id": 1,
      "title": "Введение в Django REST Framework",
      "slug": "vvedenie-v-django-rest-framework",
      "content": "Django REST Framework - это мощный...",
      "image": null,
      "category": "Технологии",
      "author": "test@example.com",
      "status": "PUBLISHED",
      "created_at": "2025-09-07T12:00:00Z",
      "updated_at": "2025-09-07T12:00:00Z",
      "views_count": 15,
      "comments_count": 3
    }
  ]
}
```

## ПАГИНАЦИЯ

### 37. Получить первую страницу постов

- **Метод:** `GET`
- **URL:** `{{base_url}}/?page=1`
- **Headers:** `Content-Type: application/json`

### 38. Получить вторую страницу постов

- **Метод:** `GET`
- **URL:** `{{base_url}}/?page=2`
- **Headers:** `Content-Type: application/json`

### 39. Изменить размер страницы (если поддерживается)

- **Метод:** `GET`
- **URL:** `{{base_url}}/?page=1&page_size=10`
- **Headers:** `Content-Type: application/json`

---

# ТЕСТОВЫЕ СЦЕНАРИИ

## Сценарий 1: Полный цикл работы с пользователем

1. Регистрация нового пользователя
2. Авторизация пользователя
3. Получение профиля
4. Обновление профиля с аватаром
5. Изменение пароля
6. Выход из системы

## Сценарий 2: Создание и управление контентом

1. Авторизация пользователя
2. Создание новой категории
3. Создание поста в этой категории
4. Публикация поста (изменение статуса с DRAFT на PUBLISHED)
5. Просмотр поста (увеличение счетчика просмотров)
6. Редактирование поста
7. Удаление поста

## Сценарий 3: Работа с правами доступа

1. Создание поста пользователем A
2. Попытка редактирования поста пользователем B (ошибка 403)
3. Успешное редактирование поста пользователем A
4. Попытка удаления категории неавторизованным пользователем (ошибка 401)

## Сценарий 4: Поиск и фильтрация

1. Создание нескольких постов в разных категориях
2. Поиск постов по ключевому слову
3. Фильтрация по категории
4. Сортировка по популярности
5. Комбинированная фильтрация

---

# КОДЫ ОТВЕТОВ HTTP

- **200 OK** - Успешное получение/обновление данных
- **201 Created** - Успешное создание объекта
- **204 No Content** - Успешное удаление объекта
- **400 Bad Request** - Ошибки валидации данных
- **401 Unauthorized** - Требуется авторизация
- **403 Forbidden** - Недостаточно прав доступа
- **404 Not Found** - Объект не найден
- **500 Internal Server Error** - Внутренняя ошибка сервера

---

# ПРИМЕРЫ ОШИБОК

## Ошибка валидации при регистрации:

```json
{
  "email": ["This field is required."],
  "password": ["Password fields didnt match."]
}
```

## Ошибка авторизации:

```json
{
  "detail": "User not found"
}
```

## Ошибка прав доступа:

```json
{
  "detail": "You do not have permission to perform this action."
}
```

## Ошибка валидации при создании поста:

```json
{
  "title": ["This field is required."],
  "content": ["This field is required."]
}
```

---

# ИСПРАВЛЕНИЯ КОДА

В процессе анализа были обнаружены опечатки в коде:

1. `apps/main/serializers.py:19` - `CategorySerialzier` → `CategorySerializer`
2. `apps/main/models.py:31` - `constent` → `content`
3. `apps/main/views.py:101` - `get_serialzier` → `get_serializer`
4. `apps/main/views.py:102` - `raise_exceprion` → `raise_exception`
5. `apps/accounts/admin.py:9` - `search_fileds` → `search_fields`

Также отсутствуют запятые в нескольких местах в serializers.py после полей в кортежах.
