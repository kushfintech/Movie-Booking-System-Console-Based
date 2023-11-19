from typing import Optional, List

import inquirer

from models.customer_model import CustomerModel
import json

CUSTOMERS_FILE = 'Customers.dat'


def fetch_all_customers():
    try:
        with open(CUSTOMERS_FILE, 'r') as f:
            customer_data = json.load(f)
        return [CustomerModel.deserialize(customer) for customer in customer_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_all_customers(customers: List[CustomerModel]):
    with open(CUSTOMERS_FILE, 'w') as f:
        json.dump([customer.serialize() for customer in customers] or [], f)


def show_all_customers():
    customers = fetch_all_customers()
    if not customers:
        print("No Customers Found")
        return

    headers = ["ID", "Customer Name", "Email", "Address", "Country"]
    attributes = ["id", "name", "email", "address", "country"]

    column_widths = [
        max(len(header), max((len(str(getattr(customer, attr))) for customer in customers), default=0))
        for header, attr in zip(headers, attributes)
    ]

    header_row = " | ".join(header.ljust(column_widths[idx]) for idx, header in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))

    for customer in customers:
        customer_details = [str(getattr(customer, attr)) for attr in attributes]
        row = " | ".join(detail.ljust(column_widths[idx]) for idx, detail in enumerate(customer_details))
        print(row)


def create_account(name: str, email: str, password: str, address: Optional[str], country: Optional[str]):
    customers = fetch_all_customers()
    is_email_already_registered = any(customer.email == email for customer in customers)
    if is_email_already_registered:
        print("Email already exists")
    else:
        cust_id = max(customer.id for customer in customers) + 1 if customers else 1
        new_customer = CustomerModel(cust_id=cust_id, name=name, email=email, password=password, address=address,
                                     country=country)
        customers.append(new_customer)
        save_all_customers(customers)
        print("Account Created Successfully!")


def delete_account(cust_id):
    customers = fetch_all_customers()
    customers = [customer for customer in customers if customer.id != cust_id]
    save_all_customers(customers)
    return True


def update_profile(cust_id, name=None, email=None, password=None, address=None, country=None):
    customers = fetch_all_customers()
    customer = next((cust for cust in customers if cust.id == cust_id), None)
    if customer:
        if name != "":
            customer.name = name
        if email != "":
            customer.email = email
        if password != "":
            customer.password = password
        if address != "":
            customer.address = address
        if country != "":
            customer.country = country
        save_all_customers(customers)
        return True
    else:
        return False


def login_to_account(email: str, password: str):
    customers = fetch_all_customers()
    customer = next((cust for cust in customers if cust.email == email), None)
    if customer:
        if customer.password == password:
            return True
        else:
            print("Password does not matched")
            return False
    else:
        print("Account doesn't exists for this email")
        return False


def get_cust_id():
    customers = fetch_all_customers()
    customer_choices = [(f"{customer.id} - {customer.name} - {customer.email}", customer.id) for customer in
                        customers]

    customer_question = [
        inquirer.List('customer',
                      message="Select Customer",
                      choices=customer_choices,
                      carousel=True)
    ]
    selected_cust_id = inquirer.prompt(customer_question)['customer']
    return selected_cust_id


def get_customer_by_id(customer_id):
    customers = fetch_all_customers()
    customer = next((cust for cust in customers if cust.id == customer_id), None)
    if customer is not None:
        return customer
    else:
        print(f"No customer found with ID {customer_id}")
        return None


def show_customer_details_by_id(cust_id):
    customers = fetch_all_customers()

    customer = next((cust for cust in customers if str(cust.id) == cust_id), None)
    if not customer:
        print(f"No customer found with ID {cust_id}")
        return

    customer_data = {
        "ID": customer.id,
        "Customer Name": customer.name,
        "Email": customer.email,
        "Address": customer.address,
        "Country": customer.country
    }
    headers = customer_data.keys()

    column_widths = {header: max(len(header), len(str(customer_data[header]))) for header in headers}

    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    row = " | ".join(str(customer_data[header]).ljust(column_widths[header]) for header in headers)
    print(row)
