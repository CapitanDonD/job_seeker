import requests

from collections import defaultdict
from itertools import count

from predict_salary import predict_rub_salary


LANGUAGES = [
    'Python',
    'Java',
    'JavaScript',
    'PHP',
    'Ruby',
    'C++',
    'TypeScript',
    'C#'
]


def decoded_hhru_response(found_languages='Python', page=0):
    url = 'https://api.hh.ru/vacancies'


    params = {
        'period': 30,
        'area': '1',
        'specialization': '1.221',
        'text': found_languages,
        'page': page
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def table_predicted_rub_salary_hhru(found_languages):
    all_average_salaries = []
    found = 0

    for page in count(0, 1):
        decoded_response = decoded_hhru_response(found_languages, page=page)
        found = decoded_response['found']

        for salary in decoded_response['items']:
            if salary['salary'] and salary['salary']['currency'] == 'RUR':
                all_average_salaries.append(
                    predict_rub_salary(salary['salary']['from'],
                                       salary['salary']['to']
                                       )
                )

        if page >= decoded_response['pages']-1:
            break

    statistics = {
        'average_salary': int(sum(all_average_salaries) / len(all_average_salaries)),
        'vacancies_found': found,
        'vacancies_processed': len(all_average_salaries)
    }

    return statistics


def get_statistics_of_languages_hhru(languages):
    statistics = defaultdict()

    for language in languages:
        statistics[language] = table_predicted_rub_salary_hhru(language)

    return statistics


def main():
    print(get_statistics_of_languages_hhru(LANGUAGES))


if __name__ == '__main__':
    main()