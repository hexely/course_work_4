import json


class Vacancies:
    def __init__(self, name: str, platform: str, responsibility: str, url: str, city, pay: dict = None,
                 requirement: str = "Не указано",
                 value: str = "Не указано"):
        self.name = name
        self.platform = platform
        self.responsibility = responsibility
        self.url = url
        self.city = city
        self.salary = pay
        self.requirement = requirement
        self.value = value

    @staticmethod
    def get_vacancies_from_file():
        """Получение вакансий из файлов и инициализация экземпляров класса"""

        items = []

        with open("hh.json", "r", encoding="utf-8") as file_hh:
            json_hh_file = json.load(file_hh)

        for page in json_hh_file:
            for item_hh in page:
                items.append(Vacancies(
                    item_hh["name"],
                    "HeadHunter",
                    item_hh["snippet"]["responsibility"],
                    item_hh["alternate_url"],
                    item_hh["area"]["name"],
                    item_hh["salary"]["from"] if isinstance(item_hh["salary"], dict) else "Не указана",
                    item_hh["snippet"]["requirement"],
                    item_hh["salary"]['currency'] if isinstance(item_hh["salary"], dict) else "Не указана"
                ))

        with open("sj.json", "r", encoding="utf-8") as file_sj:
            json_sj_file = json.load(file_sj)
        for page in json_sj_file:
            for item_sj in page:
                items.append(Vacancies(
                    item_sj["profession"],
                    "SuperJob",
                    item_sj["candidat"],
                    item_sj["link"],
                    item_sj["town"]["title"],
                    item_sj["payment_from"],
                    item_sj["vacancyRichText"],
                    item_sj["currency"]
                ))

        return items

    def __repr__(self):
        return f"{self.name}\n" \
               f"Зарплата: От {self.salary}\n" \
               f"{self.requirement}\n" \
               f"{self.url}"

    def __ge__(self, other):
        """Сравнение зарплат"""
        return int(
            self.salary[3:]
        ) >= int(
            other.salary[3:]
        ) if isinstance(
            self.salary, str
        ) and isinstance(
            other.salary, str
        ) else "Зарплата одной из вакансий не указана"


class JSONSaver:
    """Класс для записи вакансий в файл, чтения вакансий из файлов и очистки файла"""
    @staticmethod
    def add_vacancies():
        vacancies_to_file = []
        for el in Vacancies.get_vacancies_from_file():
            vacancies_to_file.append({
                "platform": el.platform,
                "url": el.url,
                "name": el.name,
                "salary": el.salary,
                "requirement": el.requirement,
                "currency": el.value,
                "city": el.city,
                "responsibility": el.responsibility
            })

        with open("vacancy.json", "w", encoding="utf-8") as file:
            json.dump(vacancies_to_file, file)

    @staticmethod
    def get_vacancies():
        with open("vacancy.json", "r", encoding="utf-8") as file:
            template = json.load(file)
        return template

    @staticmethod
    def delete_vacancy():
        with open("vacancy.json", "w", encoding="utf-8"):
            pass
