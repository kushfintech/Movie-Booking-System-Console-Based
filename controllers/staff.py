from typing import Optional, List

import inquirer

from models.staff_model import StaffModel
import json

STAFF_FILE = 'Staffs.dat'

def fetch_all_staffs():
    try:
        with open(STAFF_FILE, 'r') as f:
            staff_data = json.load(f)
        return [StaffModel.deserialize(staff) for staff in staff_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_staffs(staffs: List[StaffModel]):
    with open(STAFF_FILE, 'w') as f:
        json.dump([staff.serialize() for staff in staffs] or [], f)


def view_all_staffs():
    staffs = fetch_all_staffs()
    if not staffs:
        print("No Staffs Found")
        return

    headers = ["ID", "Staff Name", "Email", "Password", "Address", "Country"]
    attributes = ["staff_id", "name", "email", "password", "address", "country"]

    column_widths = [
        max(len(header), max((len(str(getattr(staff, attr))) for staff in staffs), default=0))
        for header, attr in zip(headers, attributes)
    ]

    header_row = " | ".join(header.ljust(column_widths[idx]) for idx, header in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))

    for staff in staffs:
        staff_details = [str(getattr(staff, attr)) for attr in attributes]
        staff_details[attributes.index("password")] = '*' * len(staff_details[attributes.index("password")])
        row = " | ".join(detail.ljust(column_widths[idx]) for idx, detail in enumerate(staff_details))
        print(row)


def create_account(name: str, email: str, password: str, address: Optional[str], country: Optional[str]):
    staffs = fetch_all_staffs()
    is_email_already_registered = any(staff.email == email for staff in staffs)
    if is_email_already_registered:
        print("This Email already exists")
    else:
        staff_id = max(staff.staff_id for staff in staffs) + 1 if staffs else 1
        new_staff = StaffModel(staff_id=staff_id, name=name, email=email, password=password, address=address,
                               country=country)
        staffs.append(new_staff)
        save_staffs(staffs)
        print("Account Created Successfully!")


def delete_account(staff_id):
    staffs = fetch_all_staffs()
    staffs = [staff for staff in staffs if staff.staff_id != staff_id]
    save_staffs(staffs)


def update_profile(staff_id, name=None, email=None, password=None, address=None, country=None):
    staffs = fetch_all_staffs()
    staff = next((staff for staff in staffs if staff.staff_id == staff_id), None)
    if staff:
        if name != "" and not None:
            staff.name = name
        if email != "" and not None:
            staff.email = email
        if address != "" and not None:
            staff.address = address
        if country != "" and not None:
            staff.country = country
        save_staffs(staffs)
        return True
    else:
        return False


def login_to_account(email: str, password: str):
    staffs = fetch_all_staffs()
    staff = next((staff for staff in staffs if staff.email == email), None)
    if staff:
        if staff.password == password:
            print(f"Welcome " + staff.name)
            return True
        else:
            print("Password did not matched")
            return False
    else:
        print("Account do not exists for this email")
        return False


def get_staff_id():
    staffs = fetch_all_staffs()
    staff_choices = [(f"{staff.staff_id} - {staff.name} - {staff.email}", staff.staff_id) for staff in staffs]

    staff_question = [
        inquirer.List('staff',
                      message="Select staff",
                      choices=staff_choices,
                      carousel=True)
    ]
    selected_staff_id = inquirer.prompt(staff_question)['staff']
    return selected_staff_id
