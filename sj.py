import os

from dotenv import load_dotenv
import requests
from itertools import count
from collections import defaultdict

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


def get_sj_vacancies(sj_key, language='Python', page=0):
    headers = {'X-Api-App-Id': sj_key}
    url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'period': 30,
        'catalogues': 48,
        'town': '4',
        'keyword': language,
        'page': page
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()


def collect_sj_language_statistics(language, sj_key):
    all_average_salaries = []
    found = 0

    for page in count(0, 1):
        decoded_response = get_sj_vacancies(sj_key, language, page=page)

        for salary in decoded_response['objects']:
            if salary['payment_from'] or salary['payment_to']:
                if salary['currency'] == 'rub':
                    salary_rub = predict_rub_salary(
                        salary['payment_from'],
                        salary['payment_to']
                    )
                    all_average_salaries.append(salary_rub)

        if not decoded_response['more']:
            break

        found = decoded_response["total"]

    salary_sum = int(sum(all_average_salaries) / len(all_average_salaries))
    used_count = len(all_average_salaries)

    statistics = {
        'average_salary': salary_sum,
        'vacancies_found': found,
        'vacancies_processed': used_count
    }

    return statistics


def get_sj_language_statistics(languages):
    statistics = defaultdict()
    sj_key = os.getenv('SJ_KEY')

    for language in languages:
        statistics[language] = collect_sj_language_statistics(language, sj_key)

    return statistics


def main():
    load_dotenv()

    print(get_sj_language_statistics(LANGUAGES))


if __name__ == '__main__':
    main()