import csv
from pathlib import Path


# Find the CSV next to this Python file.
CSV_FILE = Path(__file__).parent /"data"/"employees.csv"


def bonus(salary, rate=0.1, *extras, **options):
    """Calculate a percentage bonus, add extras, and apply an optional cap."""
    total = salary * rate + sum(extras)

    if "cap" in options:
        total = min(total, options["cap"])

    return total


class InvalidSalaryError(Exception):
    """Error raised when an employee salary is negative."""


class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")

        self.name = name
        self.salary = salary

    def annual_salary(self):
        # Assumption: salary from the CSV is monthly.
        return self.salary * 12

    def get_details(self):
        return f"Employee: {self.name}, Salary: {self.salary}"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        # Reuse Employee's setup and salary check.
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        return (
            f"Manager: {self.name}, Salary: {self.salary}, "
            f"Team size: {self.team_size}"
        )


def load_employees():
    """Read employee records from employees.csv."""
    with CSV_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def main():
    employees = load_employees()

    # List comprehension: names of employees earning over 50,000.
    above_50000 = [
        employee["name"]
        for employee in employees
        if int(employee["salary"]) > 50000
    ]
    print("Above 50000:", above_50000)

    # map and lambda: calculate a 10% raise for each employee.
    raised_salaries = list(
        map(
            lambda employee: (
                employee["name"],
                int(employee["salary"]) * 1.10,
            ),
            employees,
        )
    )
    print("10% raise:", raised_salaries)

    # filter and lambda: keep only employees from Chennai.
    chennai_employees = list(
        filter(
            lambda employee: employee["city"] == "Chennai",
            employees,
        )
    )
    print("Chennai:", [employee["name"] for employee in chennai_employees])

    # Example of *extras and **options, including the cap.
    print("Bonus example:", bonus(50000, 0.1, 200, 300, cap=4000))

    # Create and use Employee and Manager objects.
    employee = Employee("Rahul", 60000)
    manager = Manager("Divya", 75000, team_size=4)

    print("Annual salary:", employee.annual_salary())
    print(manager.get_details())

    # Catch the custom error. finally runs whether there is an error or not.
    try:
        Employee("Invalid Example", -500)
    except InvalidSalaryError as error:
        print(f"Error: {error}")
    finally:
        print("Transaction finished")

    # continue skips 0; break stops at the first salary above 85,000.
    salaries = [30000, 0, 45000, 60000, 75000, 90000, 52000]
    processed_salaries = []

    for salary in salaries:
        if salary == 0:
            continue

        if salary > 85000:
            break

        processed_salaries.append(salary)

    print("Loop processed before break:", processed_salaries)


if __name__ == "__main__":
    main()