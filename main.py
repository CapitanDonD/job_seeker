import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


TEMPLATE_TABLE = [
    ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
]

LANGUAGES_FOR_FILL = {
    'Python': '',
    'Java': '',
    'JavaScript': '',
    'PHP': '',
    'Ruby': '',
    'C++': '',
    'TypeScript': '',
    'C#': ''
}


def predict_rub_salary(of, to):
    if of and to:
        return (of + to)/2
    elif of:
        return of * 1.2
    else:
        return to * 0.8


def predict_rub_salary_hhru(found_languages, template):
    all_average_salaries = []
    url = 'https://api.hh.ru/vacancies'

    for vacancies in found_languages:
        params = {
            'period': 30,
            'area': '1',
            'specialization': '1.221',
            'text': f'{vacancies}',
            'per_page': 100,
        }
        response = requests.get(url, params=params)
        vacancies_processed = 0

        for i in range(0, response.json()['pages']):
            params = {
                'period': 30,
                'page': i,
                'area': '1',
                'specialization': '1.221',
                'text': f'{vacancies}',
                'per_page': 100,
            }
            response = requests.get(url, params=params)
            for salary in response.json()['items']:
                if salary['salary'] and salary['salary']['currency'] == 'RUR':
                    all_average_salaries.append(predict_rub_salary(salary['salary']['from'], salary['salary']['to']))
                    vacancies_processed = vacancies_processed + 1

            found_languages[vacancies] = {
                "average_salary": int(sum(all_average_salaries) / len(all_average_salaries)),
                "vacancies_found": response.json()['found'],
                'vacancies_processed': vacancies_processed
            }
    title_hhru = 'HeadHunter Moscow'

    for languages, value in found_languages.items():
        argument_for_append = [languages,  value['vacancies_found'], value['vacancies_processed'], value['average_salary']]
        template.append(argument_for_append)
    table = AsciiTable(template, title_hhru)
    return table.table


def predict_rub_salary_sj(found_languages, template):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    all_average_salaries = []
    headers = {'X-Api-App-Id': f'{os.getenv("SECRET_KEY")}'}
    title = 'SuperJob Moscow'

    for vacancies in found_languages:
        for i in range(0, 6):
            vacancies_processed = 0
            params = {
                'period': 30,
                'catalogues': 48,
                'page': i,
                'count': 100,
                'town': '4',
                'keyword': f'{vacancies}'
            }
            response = requests.get(url, headers=headers, params=params)

            for salary in response.json()['objects']:
                if salary['payment_from'] or salary['payment_to'] !=0 or None:
                    if salary['currency'] == 'rub':
                        all_average_salaries.append(predict_rub_salary(salary['payment_from'], salary['payment_to']))
                        vacancies_processed += 1

            found_languages[vacancies] = {
                "average_salary": int(sum(all_average_salaries) / len(all_average_salaries)),
                "vacancies_found": response.json()['total'],
                'vacancies_processed': vacancies_processed
            }

    for languages, value in found_languages.items():
        argument_for_append = [languages,  value['vacancies_found'], value['vacancies_processed'], value['average_salary']]
        template.append(argument_for_append)
    table = AsciiTable(template, title)
    return table.table

if __name__ == '__main__':

    load_dotenv()

    print(predict_rub_salary_sj(LANGUAGES_FOR_FILL, TEMPLATE_TABLE))
    print(predict_rub_salary_hhru(LANGUAGES_FOR_FILL, TEMPLATE_TABLE))