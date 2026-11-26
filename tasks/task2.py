import csv
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


FOLDER = Path(__file__).resolve().parent.parent
EMPLOYEES_FILE = FOLDER / "data" / "employees.csv"

def process_employees():
    
    with EMPLOYEES_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        employees = list(csv.DictReader(file))

   
    with (FOLDER / "employees.json").open("w", encoding="utf-8") as file:
        json.dump(employees, file, indent=2)

   
    high_earners = [
        employee for employee in employees
        if int(employee["salary"]) > 50000
    ]

    
    with (FOLDER / "high_earners.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=employees[0].keys())
        writer.writeheader()
        writer.writerows(high_earners)

    print(f"Rows read: {len(employees)} | High earners: {len(high_earners)}")


def get_users():
    
    load_dotenv(FOLDER / ".env")
    api_key = os.getenv("API_KEY")  

    url = "https://jsonplaceholder.typicode.com/users"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        users = response.json()
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return
    except requests.exceptions.ConnectionError:
        print("Could not connect to the API.")
        return
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")
        return

    
    for user in users[:3]:
        print(f"{user.get('id')} - {user.get('name')} - {user.get('email')}")

    
    selected_users = [
        {
            "id": user.get("id"),
            "name": user.get("name"),
            "city": user.get("address", {}).get("city"),
        }
        for user in users
    ]

    with (FOLDER / "users.json").open("w", encoding="utf-8") as file:
        json.dump(selected_users, file, indent=2)

    
    try:
        missing_response = requests.get(f"{url}/9999", timeout=5)
        if missing_response.status_code == 404:
            print("/users/9999 -> 404 Not found")
        else:
            missing_response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Request timed out while checking /users/9999.")
    except requests.exceptions.ConnectionError:
        print("Could not connect while checking /users/9999.")
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error for /users/9999: {error}")


if __name__ == "__main__":
    process_employees()
    get_users()