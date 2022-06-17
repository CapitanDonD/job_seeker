import os

from dotenv import load_dotenv
import requests
from itertools import count
from collections import defaultdict

from predict_salary import predict_rub_salary

load_dotenv()

SJ_KEY = os.getenv('SJ_KEY')

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


def decoded_sj_response(found_languages='Python', page=0):
    headers = {'X-Api-App-Id': SJ_KEY}
    url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'period': 30,
        'catalogues': 48,
        'town': '4',
        'keyword': found_languages,
        'page': page
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()


def table_predicted_rub_salary_sj(FOUND_LANGUAGES):
    count_used = 0
    all_average_salaries = []
    found = 0

    for page in count(0, 1):
        decoded_response = decoded_sj_response(FOUND_LANGUAGES, page=page)

        for salary in decoded_response['objects']:
            if salary['payment_from'] or salary['payment_to']:
                if salary['currency'] == 'rub':
                    salary_rub = predict_rub_salary(
                        salary['payment_from'],
                        salary['payment_to']
                    )
                    count_used += 1
                    all_average_salaries.append(salary_rub)

        if not decoded_response['more']:
            break

        found = decoded_response["total"]

    sum_salary = int(sum(all_average_salaries) / len(all_average_salaries))

    statistics = {
        'average_salary': sum_salary,
        'vacancies_found': found,
        'vacancies_processed': count_used
    }

    return statistics


def get_statistics_of_languages_sj(languages):
    statistics = defaultdict()

    for language in languages:
        statistics[language] = table_predicted_rub_salary_sj(language)

    return statistics


def main():
    print(get_statistics_of_languages_sj(LANGUAGES))


if __name__ == '__main__':
    main()