# Документація для back-end застосунку "group-project-photoapp"

## 1. Підстава для розроблення

Застосунок розроблено відповідно до технічного завдання компанії GoIT "Технічне завдання на створення застосунку “PhotoShare” (REST API)". Застосунок являється екзаменаційною роботою з курсу "Python Web", ставить завданням закріплення отриманих під час навчання знань та відпрацювання командної роботи і роботи з GitHub.

## 2. Доступ до застосунку

Python-скрипт застосунку доступний в репозиторії [GitHub](https://github.com/AleksandrRevuka/group_project_photoapp/tree/develop). Розгортання (deploy) застосунку виконано по адресу [http://api.photoa.pp.ua:8000/docs#/](http://api.photoa.pp.ua:8000/docs#/).

## 3. Розробники

Застосунок розроблено наступними розробниками:
- Олександр Ревука (Team Lead);
- Олександр Шевченко (Scrum Master);
- Артем Іваніна (Python Developer);
- Євген Кулик (Python Developer). 
Перевірку та допуск командного проєкту до захисту виконано ментором GoIT Данилом Сологубом.

## 4. Програмна основа

Мова програмування - Python. Застосунок реалізований на фреймворку FastAPI. В якості бази даних використано PostgreSQL. Для взаємодії з базою даних, використано бібліотеку SQLAlchemy.

## 5. Використані зовнішні програмні пакети

- uvicorn;
- jinja2
- passlib;
- python-jose;
- libgravatar;
- logging;
- pydantic;
- fastapi-mail;
- redis;
- fastapi-limiter;
- cloudinary;
- asyncpg;
- python-multipart;
- psycopg2-binary;
- psycopg2;
- alembic;
- qrcode;
- pytest-cov;
- coverage;
- fastapi-filter.

## 6. Endpoints, доступні в Swagger-документації

### 6.1. "auth":

#### 6.1.1. "Signup":

Параметри, що приймає endpoint: "username": "string", "email": "string", "password": "string".
Функціональність: реєстрація юзера. Під час першої реєстрації юзер автоматично позначається як Адміністратор. Під час реєстрації виконується підтвердження електронної пошти через надісланий лист.

#### 6.1.2. "Login":

Параметри, що приймає endpoint: "username": "string", "password": "string".
Функціональність: аутентифікація зареєстрованого юзера.

#### 6.1.3. "User Logout":

Параметри, що приймає endpoint: відсутні.
Функціональність: вихід з режиму аутентифікованого юзера.

#### 6.1.4. "Refresh Token":

Параметри, що приймає endpoint: відсутні.
Функціональність: оновлення access token.

#### 6.1.5. "Confirmed Email":

Параметри, що приймає endpoint: "token": "string".
Функціональність: оновлення access token.

#### 6.1.6. "Request Email":

Параметри, що приймає endpoint: "email": "string".
Функціональність: надсилання електронного листа на пошту користувача для підтвердження авторизації.

#### 6.1.7. "Forgot Password":

Параметри, що приймає endpoint: "email": "string".
Функціональність: надсилання електронного листа на пошту користувача для скидання паролю.

#### 6.1.8. "Reset Password":

Параметри, що приймає endpoint: "new_password": "string", "token": "string".
Функціональність: аутентифікація зареєстрованого юзера.

### 6.2. "user":

#### 6.2.1. "Read User Me":

Параметри, що приймає endpoint: відсутні.
Функціональність: надає інформацію про поточного користувача.

#### 6.2.2. "Edit My Profile":

Параметри, що приймає endpoint: "name": "string", file.
Функціональність: зміна аватару.

#### 6.2.3. "All Users":

Параметри, що приймає endpoint: "skip": "integer", "limit": "integer".
Функціональність: вивід всіх користувачів, що є в базі даних.

#### 6.2.4. "User Profile":

Параметри, що приймає endpoint: "username": "string".
Функціональність: вивід профільної інформації користувача.

#### 6.2.5. "Ban User":

Параметри, що приймає endpoint: "username": "string".
Функціональність: блокування користувача.

#### 6.2.6. "Activate User":

Параметри, що приймає endpoint: "username": "string".
Функціональність: розблокування користувача.

#### 6.2.7. "Change Role":

Параметри, що приймає endpoint: "username": "string", "role": "string".
Функціональність: зміна ролі (user/moderator/admin) користувача.

### 6.3. "comments":

#### 6.3.1. "Create Comment":

Параметри, що приймає endpoint: "picture_id": "integer", "text": "string".
Функціональність: створення коментаря до зображення.

#### 6.3.2. "Update Comment":

Параметри, що приймає endpoint: "comment_id": "integer", "text": "string".
Функціональність: зміна ролі (user/moderator/admin) користувача.

#### 6.3.3. "Delete Comment":

Параметри, що приймає endpoint: "comment_id": "integer".
Функціональність: видалення коментаря до зображення.

#### 6.3.4. "Comments Of User":

Параметри, що приймає endpoint: "comment_id": "integer", "skip": "integer", "limit": "integer".
Функціональність: вивід всіх коментарів до певного зображення.

#### 6.4.4. "Comments Of User":

Параметри, що приймає endpoint: "user_id": "integer", "skip": "integer", "limit": "integer".
Функціональність: вивід всіх коментарів до певного зображення.

### 6.4. "tags":

#### 6.4.1. "Gat Tags":

Параметри, що приймає endpoint: "picture_id": "integer", "text": "string".
Функціональність: вивід всіх тегів, що є в базі даних.

#### 6.4.2. "Gat Tag":

Параметри, що приймає endpoint: "tag_id": "integer".
Функціональність: вивід тегу за його id.

#### 6.4.3. "Update Tag":

Параметри, що приймає endpoint: "tag_id": "integer".
Функціональність: редагування певного тегу.

#### 6.4.4. "Delete Tag":

Параметри, що приймає endpoint: "tag_id": "integer".
Функціональність: видалення певного тегу.

#### 6.4.5. "Tags Of Picture":

Параметри, що приймає endpoint: "picture_id": "integer".
Функціональність: вивід тегів до певного зображення.

### 6.5. "pictures":

#### 6.5.1. "Upload Picture To Cloudinary":

Параметри, що приймає endpoint: "name": "string", "description": "string", "width": "integer", "height": "integer", "crop": "string", "gravity": "string", "angle": "integer", file.
Функціональність: завантаження зображення на хмарний сервіс "Cloudinary".

#### 6.5.2. "Update Name Of Picture":

Параметри, що приймає endpoint: "id": "integer", "name": "string".
Функціональність: зміна назви певного зображення.

#### 6.5.3. "Update Description Of Picture":

Параметри, що приймає endpoint: "id": "integer", "description": "string".
Функціональність: зміна опису певного зображення.

#### 6.5.4. "Get All Pictures":

Параметри, що приймає endpoint: "skip": "integer", "limit": "integer".
Функціональність: вивід всього переліку зображень.

#### 6.5.5. "Get Picture By Id":

Параметри, що приймає endpoint: "id": "integer".
Функціональність: вивід певного зображення.

#### 6.5.6. "Get All Pictures Of User":

Параметри, що приймає endpoint: "user_id": "integer", "skip": "integer", "limit": "integer".
Функціональність: вивід всіх зображень певного користувача.

#### 6.5.7. "Delete Picture":

Параметри, що приймає endpoint: "picture_id": "integer".
Функціональність: видалення певного зображення.

#### 6.5.8. "Get Qrcode On Transformed Picture":

Параметри, що приймає endpoint: "picture_id": "integer".
Функціональність: генерування qrcode-посилання певного зображення.

### 6.6. "rating":

#### 6.6.1. "Create Picture Rating":

Параметри, що приймає endpoint: "picture_id": "integer", "rating": "integer".
Функціональність: задання рейтингу зображення.

#### 6.6.2. "Picture Ratings":

Параметри, що приймає endpoint: "picture_id": "integer".
Функціональність: вивід середнього значення рейтингу певного зображення.

#### 6.6.3. "Remove Photo Rating":

Параметри, що приймає endpoint: "picture_id": "integer", "user_id": "integer".
Функціональність: вивід середнього значення рейтингу певного зображення.

### 6.7. "search_filter":

#### 6.7.1. "Search Users":

Параметри, що приймає endpoint: "username": "query", "username_ilike": "query", "username_like": "query".
Функціональність: пошук користувача по імені/частині імені.

### 6.8. "healthchecker":

#### 6.8.1. "Healthchecker":

Параметри, що приймає endpoint: відсутні.
Функціональність: перевірка стану застосунку.
