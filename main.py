import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable



FOUND_LANGUAGES = {
    'Python': '',
    'Java': '',
    'JavaScript': '',
    'PHP': '',
    'Ruby': '',
    'C++': '',
    'TypeScript': '',
    'C#': ''
}


def files_the_environment():
    key = os.getenv('SJ_KEY')
    return key


def creating_table(content, title):
    template = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for languages, value in content.items():
        argument_for_append = [languages,  value['vacancies_found'], value['vacancies_processed'], value['average_salary']]
        template.append(argument_for_append)
    table = AsciiTable(template, title)
    return table.table


def predict_rub_salary(of, to):
    if of and to:
        return (of + to)/2
    elif of:
        return of * 1.2
    else:
        return to * 0.8


def predict_rub_salary_hhru():
    all_average_salaries = []
    url = 'https://api.hh.ru/vacancies'
    title_hhru = 'HeadHunter Moscow'

    for vacancies in FOUND_LANGUAGES:
        params = {
            'period': 30,
            'area': '1',
            'specialization': '1.221',
            'text': f'{vacancies}',
            'per_page': 100,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
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
            decoded_response = response.json()
            for salary in decoded_response['items']:
                if salary['salary'] and salary['salary']['currency'] == 'RUR':
                    all_average_salaries.append(predict_rub_salary(salary['salary']['from'], salary['salary']['to']))
                    vacancies_processed = vacancies_processed + 1

            FOUND_LANGUAGES[vacancies] = {
                "average_salary": int(sum(all_average_salaries) / len(all_average_salaries)),
                "vacancies_found": decoded_response['found'],
                'vacancies_processed': vacancies_processed
            }
    return creating_table(FOUND_LANGUAGES, title_hhru)




def predict_rub_salary_sj():
    url = 'https://api.superjob.ru/2.0/vacancies/'
    all_average_salaries = []
    headers = {'X-Api-App-Id': f'{files_the_environment()}'}
    title_sj = 'SuperJob Moscow'

    for vacancies in FOUND_LANGUAGES:
        for number_of_page in range(0, 6):
            vacancies_processed = 0
            params = {
                'period': 30,
                'catalogues': 48,
                'page': number_of_page,
                'count': 100,
                'town': '4',
                'keyword': f'{vacancies}'
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            decoded_response = response.json()

            for salary in decoded_response['objects']:
                if salary['payment_from'] or salary['payment_to'] !=0 or None:
                    if salary['currency'] == 'rub':
                        all_average_salaries.append(predict_rub_salary(salary['payment_from'], salary['payment_to']))
                        vacancies_processed += 1

            FOUND_LANGUAGES[vacancies] = {
                "average_salary": int(sum(all_average_salaries) / len(all_average_salaries)),
                "vacancies_found": decoded_response['total'],
                'vacancies_processed': vacancies_processed
            }

    return creating_table(FOUND_LANGUAGES, title_sj)

if __name__ == '__main__':

    load_dotenv()

    print(predict_rub_salary_sj())
    print(predict_rub_salary_hhru())