import logging

import psycopg2


class DBManager:
    def __init__(self, db_config):
        logging.basicConfig(level=logging.DEBUG)
        # Логируем конфигурацию
        logging.debug(f"Connecting to database with config: {db_config}")
        try:
            self.connection = psycopg2.connect(**db_config)
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}")
            raise
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        create_employers_table = """
        CREATE TABLE IF NOT EXISTS employers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            vacancies_count INTEGER DEFAULT 0
        );
        """

        create_vacancies_table = """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            salary_min INTEGER,
            salary_max INTEGER,
            employer_id INTEGER REFERENCES employers(id)
        );
        """

        self.cursor.execute(create_employers_table)
        self.cursor.execute(create_vacancies_table)
        self.connection.commit()

    def insert_employer(self, name):
        self.cursor.execute(
            "INSERT INTO employers (name) VALUES (%s) RETURNING id;", (name,)
        )
        employer_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return employer_id

    def insert_vacancy(self, title, salary_min, salary_max, employer_id):
        self.cursor.execute(
            "INSERT INTO vacancies (title, salary_min, salary_max, employer_id) VALUES (%s, %s, %s, %s);",
            (title, salary_min, salary_max, employer_id),
        )
        self.connection.commit()

    def get_companies_and_vacancies_count(self):
        query = """
        SELECT e.name, COUNT(v.id) AS vacancies_count 
        FROM employers e 
        LEFT JOIN vacancies v ON e.id = v.employer_id 
        GROUP BY e.id;
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        query = """
        SELECT e.name AS company_name, v.title AS vacancy_title, v.salary_min AS min_salary,
               v.salary_max AS max_salary 
        FROM vacancies v 
        JOIN employers e ON v.employer_id = e.id;
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        query = "SELECT AVG((salary_min + salary_max) / 2) FROM vacancies;"

        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()

        query = """
          SELECT * FROM vacancies WHERE (salary_min + salary_max) / 2 > %s;
          """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        query = "SELECT * FROM vacancies WHERE title ILIKE %s;"
        self.cursor.execute(query, ("%" + keyword + "%",))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()


# Пример использования
if __name__ == "__main__":
    db_config = {
        "dbname": "headhunter",
        "user": "user",
        "password": "1234",
        "host": "localhost",
        "port": 5432,
    }

    db_manager = DBManager(db_config)
