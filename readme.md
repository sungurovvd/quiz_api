# quiz
---
###
Проект - тестовое задание, выполненное с использованием фреймворка Flask.
## Инструкции по запуску
 - клонируйте репозиторий
 - создайте файл .env и заполните его необходимыми для БД переменными окружения
> По умолчанию:  

    DB_HOST=db 
    DB_PORT=5432
    DB_USER=root
    DB_PASSWORD=admin
    DB_NAME=quiz_db 
    
 - запустите контейнер с БД Postgres следующей командой:  
    docker-compose up -d --build 

---
## Примеры запросов к API
URL для запросов GET и POST:
>http://localhost:5000/questions

GET запрос возвращает случайный вопрос из уже сохраненных в бд

POST запрос вида:
    {"questions_num": 2} 

Сохранит полученные с API https://jservice.io вопросы  
(текст вопроса, ответ, дата создания)
И вернет последний сохраненный в БД, до добавления новых, вопрос