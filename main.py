from src.vacancy_api_handler import HeadHunter
from src.working_with_databases_tables import DatabaseHandler


def main():
    # Список работодателей
    employers = [
        {"name": "Яндекс", "hh_id": 1740},
        {"name": "Т-банк", "hh_id": 78638},
        {"name": "Сбер. IT", "hh_id": 3529},
        {"name": "МТС", "hh_id": 3776},
        {"name": "Роснефть", "hh_id": 239363},
        {"name": "Газпром", "hh_id": 5778059},
        {"name": "Ростелеком", "hh_id": 2748},
        {"name": "Лаборатория Касперского", "hh_id": 1057},
        {"name": "Ozon", "hh_id": 1057},
        {"name": "Все Инструменты.ру", "hh_id": 208707},
    ]

    # Инициализация классов
    db_handler = DatabaseHandler()
    db_handler.create_database()  # Создаем базу данных, если она не существует
    db_handler.connect()
    db_handler.create_tables()

    hh_api = HeadHunter()

    # Заполнение базы данных
    for employer in employers:
        # Вставка компании
        company_id = db_handler.insert_company(employer["name"], employer["hh_id"])
        if company_id is None:
            print(f"Failed to insert company: {employer['name']}")
            continue  # Пропустить, если кодировка неверная или компания уже существует

        # Получаем вакансии для текущего работодателя
        vacancies = hh_api.get_vacancies_by_employer(employer["hh_id"])

        for vacancy in vacancies:
            if vacancy is None:
                continue

            # Получаем информацию о зарплате
            salary_info = vacancy.get("salary")
            salary = (
                salary_info.get("from") if salary_info else None
            )  # Получаем зарплату, если она указана

            # Вставка вакансии в базу данных
            vacancy_id = db_handler.insert_vacancy(
                vacancy["name"],
                vacancy.get("description", ""),
                vacancy.get("url", ""),
                company_id,
                salary,
            )
            if vacancy_id is None:
                print(
                    f"Failed to insert vacancy: {vacancy['name']} for company id: {company_id}"
                )

    # Сохраняем изменения в базе данных
    db_handler.connection.commit()

    # Примеры использования методов DBManager
    print("Количество вакансий у каждой компании:")
    db_handler.cursor.execute(
        """
        SELECT e.name, COUNT(v.id)
        FROM employers e
        LEFT JOIN vacancies v ON e.id = v.employer_id
        GROUP BY e.id;
    """
    )
    companies_and_vacancies_count = db_handler.cursor.fetchall()
    for company, count in companies_and_vacancies_count:
        print(f"{company}: {count} вакансий")

    print("\nВсе вакансии:")
    db_handler.cursor.execute(
        """
        SELECT v.title, v.salary, e.name
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.id;
    """
    )
    all_vacancies = db_handler.cursor.fetchall()
    for title, salary, company in all_vacancies:
        print(f"Вакансия: {title}, Зарплата: {salary}, Компания: {company}")

    # Закрытие соединения с БД
    db_handler.close()


if __name__ == "__main__":
    main()
