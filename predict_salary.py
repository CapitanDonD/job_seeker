def predict_rub_salary(salary_of=None, salary_to=None):
    if salary_of and salary_to:
        return (salary_of + salary_to)/2
    elif salary_of:
        return salary_of * 1.2
    elif salary_to:
        return salary_to * 0.8