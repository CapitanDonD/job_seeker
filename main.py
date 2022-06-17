from terminaltables import AsciiTable

from hhru_code import get_statistics_of_languages_hhru
from sj_code import get_statistics_of_languages_sj

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

TITLE_SJ = 'Superjob Moscow'
TITLE_HHRU = 'HeadHunter Moscow'


def creating_table(content, title):
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
    print(creating_table(get_statistics_of_languages_hhru(LANGUAGES), TITLE_HHRU))
    print(creating_table(get_statistics_of_languages_sj(LANGUAGES), TITLE_SJ))


if __name__ == '__main__':
    main()