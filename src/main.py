import logging

from src.db_manager import DBManager

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Конфигурация базы данных
config = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Vcrsmart2025",
    "host": "localhost",
    "port": 5432,
}

db_manager = DBManager(config)
db_manager.create_database()

try:
    db_manager.connect()

    # Создание таблиц
    db_manager.create_tables()

    while True:
        print("1. Показать компании и количество вакансий")
        print("2. Показать среднюю зарплату")
        print("3. Показать вакансии по ключевому слову")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Показать все вакансии")
        option = input("Выберите опцию (или 'exit' для выхода): ")

        if option == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"Компания: {company[0]}, Количество вакансий: {company[1]}")

        elif option == "2":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif option == "3":
            keyword = input("Введите ключевое слово: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            if vacancies:
                for vacancy in vacancies:
                    title = vacancy[1]
                    salary_min = vacancy[2]
                    salary_max = vacancy[3]
                    print(
                        f"Вакансия: {title}, Минимальная зарплата: {salary_min}, Максимальная зарплата: {salary_max}"
                    )
            else:
                print("Вакансии не найдены.")

        elif option == "4":
            high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            if high_salary_vacancies:
                for vacancy in high_salary_vacancies:
                    title = vacancy[1]
                    salary_min = vacancy[2]
                    salary_max = vacancy[3]
                    print(
                        f"Вакансия: {title}, Минимальная зарплата: {salary_min}, Максимальная зарплата: {salary_max}"
                    )
            else:
                print("Вакансии с высокой зарплатой не найдены.")

        elif option == "5":
            all_vacancies = db_manager.get_all_vacancies()
            for vacancy in all_vacancies:
                print(vacancy)

        elif option.lower() == "exit":
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

finally:
    # Закрытие соединения с базой данных
    db_manager.close()
