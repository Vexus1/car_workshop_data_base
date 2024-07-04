import json
import os

import pandas as pd
from pandas import DataFrame
from sqlalchemy import orm
from datetime import datetime

from config_app import run_config_app
from conn import load_config, create_connection
from src.emulation.customer_decision_maker import CustomerDecisionMaker
from src.emulation.workshop_decision_maker import WorkshopDecisionMaker
from src.emulation.workshop_emulator import WorkshopEmulator
from src.emulation.emulation import emulate_day
from src.generators.equipment_generator import generate_equipment_table
from src.generators.personal_data_generator import PersonalDataGenerator
from src.models.base import Base

def load_json_file(file_path: str) -> (dict | Exception):
    try:
        with open(file_path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at the specified path: {file_path} \
                                 was not found. Please check if the path is correct.")
    except Exception as e:
        return e
    
def load_cvs_file(file_path: str) -> (DataFrame | Exception):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at the specified path: {file_path} \
                                 was not found. Please check if the path is correct.")
    except Exception as e:
        raise e

dates = load_json_file("data/parameters/dates.json")
employees_data = load_json_file("data/parameters/employees.json")
service_parameters = load_json_file("data/parameters/services_parts.json")
names = load_cvs_file("data/names.csv")
female_surnames = load_cvs_file("data/female_surnames.csv")
male_surnames = load_cvs_file("data/male_surnames.csv")
vehicles_info = load_cvs_file("data/brands.csv")

run_config_app()
config = load_config()
conn = create_connection(config)
Base.metadata.drop_all(conn)
Base.metadata.create_all(conn)
session = orm.sessionmaker(bind=conn)()

def create_date_range() -> list[datetime]:
    _date_range = pd.date_range(dates["start"], periods=365).to_pydatetime()
    _date_range = [d for d in _date_range if d.weekday() < 5]
    return _date_range

equipment = generate_equipment_table(service_parameters=service_parameters)
personal_data_generator = PersonalDataGenerator(
    names=names,
    female_surnames=female_surnames,
    male_surnames=male_surnames,
)

workshop_decision_maker1 = WorkshopDecisionMaker(
    manager_salary=employees_data["manager"],
    mechanics_salary=employees_data["mechanic"],
    purchase_probability=0.3,
    selling_probability=0.15,
    repair_completion_probability=0.5,
    service_parameters=service_parameters,
    employee_resignation_probability=1 / (365 * 2),
    number_of_items_in_stock=10,
    personal_data_generator=personal_data_generator,
    initial_equipment_number=10,
    vehicles_info=vehicles_info,
    stock_replenishment_fraction=3,
)

date_range = create_date_range()
workshop_emulator1 = WorkshopEmulator(
    date=date_range[0],
    decision_maker=workshop_decision_maker1,
    service_parameters=service_parameters,
    margin=0.2,
    equipment=equipment,
    personal_data_generator=personal_data_generator,
)

workshop_decision_maker2 = WorkshopDecisionMaker(
    manager_salary=employees_data["manager"],
    mechanics_salary=employees_data["mechanic"],
    purchase_probability=0.2,
    selling_probability=0.15,
    repair_completion_probability=0.4,
    service_parameters=service_parameters,
    employee_resignation_probability=1 / 365,
    number_of_items_in_stock=10,
    personal_data_generator=personal_data_generator,
    initial_equipment_number=10,
    vehicles_info=vehicles_info,
    stock_replenishment_fraction=3,
)

workshop_emulator2 = WorkshopEmulator(
    date=date_range[0],
    decision_maker=workshop_decision_maker2,
    service_parameters=service_parameters,
    margin=0.2,
    equipment=equipment,
    personal_data_generator=personal_data_generator,
)

workshop_emulators = [workshop_emulator1, workshop_emulator2]
customer_decision_maker = CustomerDecisionMaker(
    account_deactivation_probability=1/(3 * 365),
    regular_customers_per_day=0.001,
    new_customers_per_day=6,
    personal_data_generator=personal_data_generator,
)

complaints = []
transactions = []
for day_number, date in enumerate(date_range):
    emulate_day(
        date, workshop_emulators,
        customer_decision_maker, transactions, day_number
    )

workshops = [wdm.workshop for wdm in workshop_emulators]
employees = [emp for wdm in workshop_emulators for emp in wdm.employees]
services = [service for wdm in workshop_emulators for service in wdm.repairs]
vehicles = [vehicle for wdm in workshop_emulators for vehicle in wdm.vehicles]
inventory = [inv for wdm in workshop_emulators for inv in wdm.inventory]

if __name__ == "__main__":
    session.add_all(equipment)
    session.add_all(customer_decision_maker.all_customers)
    session.add_all(workshops)
    session.add_all(employees)
    session.add_all(transactions)
    session.add_all(services)
    session.add_all(vehicles)
    session.add_all(inventory)
    session.commit()
