from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

TASK_FOLDER = Path(__file__).resolve().parent
WEEK1_FOLDER = TASK_FOLDER.parent

DATA_FOLDER = WEEK1_FOLDER / "data"
EMPLOYEES_CSV = DATA_FOLDER / "employees.csv"
DEPARTMENTS_CSV = DATA_FOLDER / "departments.csv"
FIGURES_FOLDER = WEEK1_FOLDER / "figures"

FIGURES_FOLDER.mkdir(parents=True, exist_ok=True)

def numpy_examples():
    
    marks = np.array([
        [82, 76, 90],
        [68, 88, 79],
        [95, 91, 84],
        [73, 80, 87],
    ])

    print("Marks shape:", marks.shape)
    print("Student averages:", marks.mean(axis=1))
    print("Subject averages:", marks.mean(axis=0))

   
    marks_with_grace = marks + 5
    print("Marks with grace marks:\n", marks_with_grace)

   
    weights = np.array([0.5, 0.3, 0.2])
    weighted_scores = np.dot(marks_with_grace, weights)
    print("Weighted scores:", weighted_scores)


def make_department_file():
    
    departments = pd.DataFrame({
        "department": ["Sales", "HR", "IT", "Finance", "Marketing"],
        "head": ["Arun", "Priya", "Rahul", "Karthik", "Unassigned"],
        "budget": [100000, 80000, 200000, 120000, 50000],
    })
    departments.to_csv(DEPARTMENTS_CSV, index=False)


def load_and_clean_employees():
    employees = pd.read_csv(EMPLOYEES_CSV)

    
    employees.loc[[1, 4], "salary"] = np.nan
    employees = pd.concat([employees, employees.iloc[[0]]], ignore_index=True)

    employees["salary"] = pd.to_numeric(employees["salary"], errors="coerce")
    employees["id"] = pd.to_numeric(employees["id"], errors="coerce").astype("Int64")

    print("\nDataFrame info:")
    employees.info()
    print("\nSalary and ID description:")
    print(employees[["salary", "id"]].describe())

    print("\nUsing loc (first three named columns):")
    print(employees.loc[:2, ["name", "department", "salary"]])

    print("\nUsing iloc (first three rows and columns):")
    print(employees.iloc[:3, :3])

    print("\nFiltering salary above 50000:")
    print(employees[employees["salary"] > 50000][["name", "salary"]])

   
    employees = employees.drop_duplicates()
    median_salary = employees["salary"].median()
    employees["salary"] = employees["salary"].fillna(median_salary)

   
    employees["salary"] = employees["salary"].round().astype(int)
    employees["department"] = employees["department"].astype("category")

    print("\nCleaned data types:")
    print(employees.dtypes)

    return employees


def summarize_and_merge(employees):
    summary = employees.groupby("department", observed=False).agg(
        headcount=("id", "count"),
        average_salary=("salary", "mean"),
        maximum_salary=("salary", "max"),
    ).reset_index()

    print("\nHeadcount:")
    for _, row in summary.iterrows():
        print(f"{row['department']}: {row['headcount']}")

    departments = pd.read_csv(DEPARTMENTS_CSV)

    
    inner_join = pd.merge(summary, departments, on="department", how="inner")
    print("\nInner join:")
    print(inner_join)

    
    left_join = pd.merge(summary, departments, on="department", how="left")
    print("\nLeft join:")
    print(left_join)

    
    outer_join = pd.merge(summary, departments, on="department", how="outer")
    print("\nOuter join:")
    print(outer_join)

    no_employee_departments = outer_join.loc[
        outer_join["headcount"].isna(), "department"
    ].tolist()
    print("Departments with no employees:", no_employee_departments)

    return summary


def save_chart(fig, filename, insight):
    
    fig.text(0.5, 0.01, insight, ha="center", wrap=True, fontsize=9)
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    fig.savefig(FIGURES_FOLDER / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    plt.show()
    print(f"{filename} insight: {insight}")


def make_charts(employees, summary):
   # BAR CHART
    fig, ax = plt.subplots()
    ax.bar(summary["department"].astype(str), summary["average_salary"],
           color="steelblue", label="Average salary")
    ax.set_title("Average Employee Salary by Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average salary (salary units)")
    ax.legend()
    plt.show()
    save_chart(
        fig,
        "bar_average_salary.png",
        "IT has the highest average salary among departments with employees."
    )

    # HISTOGRAM
    fig, ax = plt.subplots()
    ax.hist(employees["salary"], bins=5, color="darkorange",
            edgecolor="black", label="Employees")
    ax.set_title("Distribution of Employee Salaries")
    ax.set_xlabel("Salary (salary units)")
    ax.set_ylabel("Number of employees (people)")
    ax.legend()
    save_chart(
        fig,
        "histogram_salaries.png",
        "The histogram shows how employee salaries are distributed across five ranges."
    )

    # SCATTER PLOT
    fig, ax = plt.subplots()
    ax.scatter(employees["id"], employees["salary"],
               color="seagreen", label="Employees")
    ax.set_title("Employee Salary by ID")
    ax.set_xlabel("Employee ID (identifier)")
    ax.set_ylabel("Salary (salary units)")
    ax.legend()
    plt.show()
    save_chart(
        fig,
        "scatter_salary_by_id.png",
        "Employee salaries vary across IDs, so ID does not represent a salary trend."
    )

    # LINE CHART
    sorted_salaries = employees["salary"].sort_values().reset_index(drop=True)
    fig, ax = plt.subplots()
    ax.plot(sorted_salaries.index + 1, sorted_salaries,
            marker="o", color="purple", label="Sorted salary")
    ax.set_title("Employee Salaries Sorted from Lowest to Highest")
    ax.set_xlabel("Employee rank (lowest to highest)")
    ax.set_ylabel("Salary (salary units)")
    ax.legend()
    plt.show()
    save_chart(
        fig,
        "line_sorted_salaries.png",
        "Sorted salaries rise steadily from the lowest employee salary to the highest."
    )


def main():
    numpy_examples()
    make_department_file()
    employees = load_and_clean_employees()
    summary = summarize_and_merge(employees)
    make_charts(employees, summary)


if __name__ == "__main__":
    main()