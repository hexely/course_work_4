import json


# Функция фильтрации вакансий
def filtered_vacancies(search_query: str, filter_words: list, top_n: int):
    """ Получает, название вакансии,
        слова для фильтрации, кол-во вакансий для вывода
        :return: отсортированный список вакансий """

    lst_vac = []
    with open("vacancy.json", "r", encoding="utf8") as file:
        vac_json = json.load(file)
        for vacancy in vac_json:
            if search_query.lower() in vacancy['name'].lower():
                if len(filter_words) > 0:

                    # Информация о вакансии в строковом виде для сравнения с фильтруемыми словами
                    vac_data_str = f"{vacancy['name']},{vacancy['requirement']},{vacancy['city']},{vacancy['responsibility']}"

                    for word in filter_words:
                        if word in vac_data_str.split():
                            lst_vac.append(vacancy)
                else:
                    lst_vac.append(vacancy)
    # сортировка по зп
    lst_vac.sort(key=lambda x: x["salary"] if isinstance(x["salary"], int) else 0, reverse=True)

    return lst_vac[:top_n]
