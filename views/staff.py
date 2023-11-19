from controllers.staff import (fetch_all_staffs, create_account, login_to_account, view_all_staffs, delete_account, get_staff_id,
                               update_profile)
from views.movie import manage_movie_menu
from views.sessions import manage_sessions_menu
from views.customer import manage_customer_menu
from views.reservation import manage_reservation_menu


def check_staff_exists_or_not():
    staffs = fetch_all_staffs()
    if not staffs:
        print("Please create first staff to start managing this system!")
        name = input("Enter Full Name: ")
        email = input("Enter Email Address: ")
        password = input("Enter New Password: ")
        c_password = input("Enter New Password Again: ")
        address = input("Enter Your Address(Optional): ")
        country = input("Enter Your Country Name(Optional): ")
        if password == c_password:
            create_account(name=name, email=email, password=password, address=address, country=country)
        else:
            print("Both password does not matched")


def staff_non_logged_in_menu():
    while True:
        print("\n MRS>Staffs")
        print("1. Login")
        print("2. Back")
        choice = input("Enter choice: ")
        if choice == "1":
            email = input("Enter your email address: ")
            password = input("Enter your password: ")
            result = login_to_account(email=email, password=password)
            if result:
                staff_logged_in_menu()
        elif choice == "2":
            return
        else:
            print("Invalid choice, please try again.")


def manage_staff_menu():
    while True:
        print("\n MRS>Manage Staffs")
        print("1. View Staffs")
        print("2. Add Staff")
        print("3. Update Staff")
        print("4. Remove Staff")
        print("5. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_all_staffs()
        elif choice == "2":
            name = input("Enter Staff Full Name: ")
            email = input("Enter Staff Email Address: ")
            password = input("Enter New Password: ")
            c_password = input("Enter Staff New Password Again: ")
            address = input("Enter Staff Living Address(Optional): ")
            country = input("Enter Staff Country Name(Optional): ")
            if password == c_password:
                create_account(name=name, email=email, password=password, address=address, country=country)
            else:
                print("Both password does not matched")
        elif choice == "3":
            staff_id = get_staff_id()
            if staff_id:
                name = input("Enter Staff Full Name: ")
                email = input("Enter Staff Email Address: ")
                address = input("Enter Staff Living Address(Optional): ")
                country = input("Enter Staff Country Name(Optional): ")
                success = update_profile(staff_id=staff_id, name=name, email=email, address=address, country=country,
                                         password=None)
                if success:
                    print(f"Staff with Id: {staff_id} updated successfully!")
        elif choice == "4":
            staff_id = get_staff_id()
            if staff_id:
                success = delete_account(staff_id)
                if success:
                    print(f"Staff with Id: {staff_id} deleted successfully!")
        elif choice == "5":
            break
        else:
            print("Invalid choice, please try again.")


def staff_logged_in_menu():
    while True:
        print("\n MRS>Staffs>Menu")
        print("1. Staffs")
        print("2. Customers")
        print("3. Movies")
        print("4. Movie Shows")
        print("5. Reservations")
        print("6. Back")
        choice = input("Enter choice: ")
        if choice == "1":
            manage_staff_menu()
        elif choice == "2":
            manage_customer_menu()
        elif choice == "3":
            manage_movie_menu()
        elif choice == "4":
            manage_sessions_menu()
        elif choice == "5":
            manage_reservation_menu()
        elif choice == "6":
            return
        else:
            print("Invalid choice, please try again.")

