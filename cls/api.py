import requests
import os
import json
import time
from abc import ABC, abstractmethod


class JobSite(ABC):
    """Абстрактный класс для работы с API"""
    @classmethod
    @abstractmethod
    def get_vacancies(cls, page=0):
        """Получает название вакансии и количество.
           :return: JSON"""
        pass

    @staticmethod
    @abstractmethod
    def save_vacancies():
        """Сохранение результата в файл JSON"""
        pass


class HeadHunterAPI(JobSite):
    """Класс для работы с API сайта HeadHunter"""
    url_vacancies = 'https://api.hh.ru/vacancies'
    headers = {}

    @classmethod
    def get_vacancies(cls, page=0):
        params = {'page': page, 'per_page': 100}
        response = requests.get(cls.url_vacancies, headers=cls.headers, params=params)
        if response.status_code != 200:
            raise Exception("cервер не отвечает")
        else:
            return response.json()

    @staticmethod
    def save_vacancies():
        with open('hh.json', 'w', encoding="utf8") as f:

            vac_list = []
            json.dump(vac_list, f, indent=4, ensure_ascii=False)

        for page in range(10):

            # Преобразуем текст ответа запроса в справочник Python
            json_page = HeadHunterAPI.get_vacancies(page)

            # Дозапись вакансий в json файл оказалась не лучшей идеей
            with open('hh.json', 'r', encoding="utf8") as f:
                temporary = json.load(f)
                temporary.append(json_page['items'])

            with open("hh.json", "w", encoding="utf8") as file:
                json.dump(temporary, file, indent=4, ensure_ascii=False)

            # Проверка на последнюю страницу, если вакансий меньше 2000
            if (json_page['pages'] - page) <= 1:
                break

            # Подсказали что задержка нужна, что-бы не было проблем с сервером и капчей
            time.sleep(0.25)


class SuperJobAPI(JobSite):
    """Класс для работы с API сайта SuperJob"""
    url_vacancies = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': os.getenv('SUPERJOB_KEY'),
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
            }

    @classmethod
    def get_vacancies(cls, page=0):
        params = {'page': page, 'per_page': 100, 'not_archive': True}
        response = requests.get(cls.url_vacancies, headers=cls.headers, params=params)
        if response.status_code != 200:
            raise Exception("cервер не отвечает")
        else:
            return response.json()

    @staticmethod
    def save_vacancies():
        with open('sj.json', 'w', encoding="utf8") as f:
            vac_list = []
            json.dump(vac_list, f, indent=4, ensure_ascii=False)

        for page in range(10):

            # Преобразуем текст ответа запроса в справочник Python
            json_page = SuperJobAPI.get_vacancies(page)

            # Дозапись вакансий в json файл оказалась не лучшей идеей
            with open('sj.json', 'r', encoding="utf8") as file:
                temporary = json.load(file)
                temporary.append(json_page['objects'])

            with open("sj.json", "w", encoding="utf8") as file:
                json.dump(temporary, file, indent=4, ensure_ascii=False)

            # Проверка на последнюю страницу, если вакансий меньше 2000
            if (json_page['total'] - page) <= 1:
                break

            # Подсказали что задержка нужна, что-бы не было проблем с сервером и капчей
            time.sleep(0.25)
