# Работа с базами данных

## Описание
В рамках данного проекта вам необходимо получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в 
базе данных PostgreSQL и загрузить полученные данные в созданные таблицы.

## Основные шаги проекта
Получение данных: Используйте публичный API hh.ru и библиотеку requests для получения данных о работодателях и их вакансиях.
Выбор компаний: Выберите не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях через API.
Проектирование таблиц: Спроектируйте таблицы в базе данных PostgreSQL для хранения полученных данных о работодателях и их вакансиях. Для работы с базой данных используйте библиотеку psycopg2.
Заполнение таблиц: Реализуйте код, который будет заполнять созданные в базе данных PostgreSQL таблицы данными о работодателях и их вакансиях.
Создание класса DBManager: Создайте класс DBManager для работы с данными в базе данных.
Класс DBManager
Класс DBManager должен подключаться к базе данных PostgreSQL и иметь следующие методы:

get_companies_and_vacancies_count(): Этот метод получает список всех компаний и количество вакансий у каждой компании.
get_all_vacancies(): Этот метод получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
get_avg_salary(): Этот метод получает среднюю зарплату по всем вакансиям.
get_vacancies_with_higher_salary(): Этот метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
get_vacancies_with_keyword(): Этот метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например, "python".
Класс DBManager должен использовать библиотеку psycopg2 для работы с базой данных.

## Установка и использование
1. Клонируйте репозиторий: git@github.com:Anastasiya-Nikolaeva/Project_3.git

2. Установите необходимые зависимости:
pip install -r requirements.txt

3. Скачайте файл `.env.example` и добавьте в него необходимые данные.

