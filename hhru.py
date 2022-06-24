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


def getting_hhru_languages_vacancies(language='Python', page=0):
    url = 'https://api.hh.ru/vacancies'


    params = {
        'period': 30,
        'area': '1',
        'specialization': '1.221',
        'text': language,
        'page': page
    }
    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()


def collect_hhru_statistics(language):
    all_average_salaries = []
    found = 0

    for page in count(0, 1):
        decoded_response = getting_hhru_languages_vacancies(language, page=page)
        found = decoded_response['found']

        for salary in decoded_response['items']:
            if salary['salary'] and salary['salary']['currency'] == 'RUR':
                all_average_salaries.append(
                    predict_rub_salary(
                        salary['salary']['from'],
                        salary['salary']['to']
                    )
                )

        if page >= decoded_response['pages']-1:
            break

    salary_sum = int(sum(all_average_salaries) / len(all_average_salaries))
    count_used = len(all_average_salaries)

    statistics = {
        'average_salary': salary_sum,
        'vacancies_found': found,
        'vacancies_processed': count_used
    }

    return statistics


def get_hhru_language_statistics(languages):
    statistics = defaultdict()

    for language in languages:
        statistics[language] = collect_hhru_statistics(language)

    return statistics


def main():
    print(get_hhru_language_statistics(LANGUAGES))


if __name__ == '__main__':
    main()