# Week 1 Assessment

## Setup

Create the virtual environment with `uv venv`.

Install the packages with `uv pip install --python .\.venv\Scripts\python.exe -r requirements.txt`.

Open `notebooks/analysis.ipynb` in VS Code and select the project `.venv` as its Python kernel.

## Findings

- The employee dataset contains 8 original records.
- IT has the largest headcount, with 3 employees.
- Sales and HR each have 2 employees.
- Finance has 1 employee, while Marketing has none.
- The analysis fills 2 missing salaries with the median and removes 1 duplicate row.