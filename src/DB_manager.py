import os
from dotenv import load_dotenv

from src.working_with_databases_tables import DatabaseHandler

load_dotenv()


class DBManager:
    """Класс для управления данными в БД."""

    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

        # Получаем данные для подключения из переменных окружения
        self.db_name = 'project_db'
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.db_handler.cursor.execute("""
            SELECT c.name, COUNT(v.id) 
            FROM companies c 
            LEFT JOIN vacancies v ON c.id = v.company_id 
            GROUP BY c.id;
        """)
        return self.db_handler.cursor.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты."""
        self.db_handler.cursor.execute("""
            SELECT v.title, v.salary, c.name 
            FROM vacancies v 
            JOIN companies c ON v.company_id = c.id;
        """)
        return self.db_handler.cursor.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        self.db_handler.cursor.execute("SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;")
        return self.db_handler.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        self.db_handler.cursor.execute("""
            SELECT v.title, v.salary, c.name 
            FROM vacancies v 
            JOIN companies c ON v.company_id = c.id 
            WHERE v.salary > %s;
        """, (avg_salary,))
        return self.db_handler.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        self.db_handler.cursor.execute("""
            SELECT v.title, v.salary, c.name 
            FROM vacancies v 
            JOIN companies c ON v.company_id = c.id 
            WHERE v.title ILIKE %s;
        """, (f"%{keyword}%",))
        return self.db_handler.cursor.fetchall()
