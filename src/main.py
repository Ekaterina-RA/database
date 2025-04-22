from src.DBManager import DBManager


def user_interface(user_manager: DBManager):
    while True:
        print("1. Показать компании и количество вакансий")
        print("2. Показать среднюю зарплату")
        print("3. Показать вакансии с зарплатой выше средней")
        print("4. Показать вакансии по ключевому слову")

        choice = input("Выберите опцию (или 'exit' для выхода): ")

        if choice == "1":
            companies = user_manager.get_companies_and_vacancies_count()
            if companies:
                for company in companies:
                    print(f"Компания: {company[0]}, Вакансий: {company[1]}")
            else:
                print("Нет доступных компаний.")

        elif choice == "2":
            avg_salary = user_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == "3":
            higher_salary_vacancies = user_manager.get_vacancies_with_higher_salary()
            if higher_salary_vacancies:
                for vacancy in higher_salary_vacancies:
                    print(vacancy)
            else:
                print("Нет вакансий с зарплатой выше средней.")

        elif choice == "4":
            keyword = input("Введите ключевое слово: ")
            keyword_vacancies = user_manager.get_vacancies_with_keyword(keyword)
            if keyword_vacancies:
                for vacancy in keyword_vacancies:
                    print(vacancy)
            else:
                print(f"Нет вакансий по ключевому слову '{keyword}'.")

        elif choice.lower() == "exit":
            break


# Пример использования
if __name__ == "__main__":
    db_config = {
        "dbname": "headhunter",
        "user": "user",
        "password": "1234",
        "host": "localhost",
        "port": 5432,
    }

    user_manager = DBManager(db_config)
    try:
        user_interface(user_manager)
    finally:
        user_manager.close()
