from cls.api import HeadHunterAPI, SuperJobAPI
from cls.vacan import Vacancies, JSONSaver
from utils import filtered_vacancies
from datetime import datetime
import os
import json

print("Загрузка информации о вакансиях ... ")
HeadHunterAPI.save_vacancies()
SuperJobAPI.save_vacancies()
Vacancies.get_vacancies_from_file()
JSONSaver.add_vacancies()


# Функции взаимодействия с пользователем
def user_interaction():

    search_query = input("Введите название вакансии: ")

    # Если не корректно введено кол-во вакансий, то ставит 10
    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    except ValueError:
        top_n = 10

    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered = filtered_vacancies(search_query, filter_words, top_n)

    for vacancy in filtered:
        print(f"{vacancy['name']} {vacancy['url']} , зарплата - {vacancy['salary']}, "
              f"требования: {vacancy['requirement']}, обязанности: {vacancy['responsibility']}")

    # Если вакансии не найдены
    if not filtered:
        print("Нет вакансий, соответствующих заданным критериям.")
        # Удаляем лишние файлы
        JSONSaver.delete_vacancy()
        os.remove("hh.json")
        os.remove("sj.json")
        os.remove("vacancy.json")
        quit()

    # Предложение сохранить файл
    while True:
        save_vac_search = input('Сохранить результаты поиска? Y/N ').lower()
        if save_vac_search == 'y':
            # Запись в файл по названию профессии и дате
            with open(f"{search_query}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.json", "w", encoding='utf8') as f:
                json.dump(filtered, f, indent=4, ensure_ascii=False)
                break
        elif save_vac_search == 'n':
            break
        else:
            continue

    # Удаляем лишние файлы
    JSONSaver.delete_vacancy()
    os.remove("hh.json")
    os.remove("sj.json")
    os.remove("vacancy.json")


if __name__ == "__main__":
    user_interaction()
