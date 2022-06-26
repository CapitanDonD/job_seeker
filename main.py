from terminaltables import AsciiTable

from hhru import get_hhru_language_statistics
from sj import get_sj_language_statistics


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

SJ_TITLE = 'Superjob Moscow'
HHRU_TITLE = 'HeadHunter Moscow'


def create_table(content, title):
    template = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]

    for languages, value in content.items():
        argument_for_append = [
            languages,
            value['vacancies_found'],
            value['vacancies_processed'],
            value['average_salary']
        ]
        template.append(argument_for_append)
    table = AsciiTable(template, title)
    return table.table


def main():
    print(create_table(get_hhru_language_statistics(LANGUAGES), HHRU_TITLE))
    print(create_table(get_sj_language_statistics(LANGUAGES), SJ_TITLE))


if __name__ == '__main__':
    main()