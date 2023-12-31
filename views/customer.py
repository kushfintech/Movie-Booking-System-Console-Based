import inquirer

from controllers.customer import login_to_account, create_account, show_all_customers, delete_account, update_profile, \
    get_cust_id, show_customer_details_by_id
from controllers.movie import view_all_movies, show_movie_details_by_name, select_movie
from controllers.movie_session import select_show_date, select_show_time, display_seats_for_session


def customer_non_logged_in_menu():
    while True:
        menu_choices = [("Login", "1"), ("Register", "2"), ("Back", "3")]
        question = [
            inquirer.List('menu',
                          message="Select an Option:",
                          choices=menu_choices,
                          carousel=True)
        ]
        answers = inquirer.prompt(question)
        choice = answers['menu']

        if choice == "1":
            email = input("Enter your email address: ")
            password = input("Enter your password: ")
            result = login_to_account(email=email, password=password)
            if result:
                customer_logged_in_menu()
        elif choice == "2":
            name = input("Enter Your Full Name: ")
            email = input("Enter Your Email Address: ")
            password = input("Enter New Password: ")
            c_password = input("Enter Your New Password Again: ")
            address = input("Enter Your Living Address(Optional): ")
            country = input("Enter Your Country Name(Optional): ")
            if password == c_password:
                create_account(name=name, email=email, password=password, address=address, country=country)
            else:
                print("Both password does not matched")
        elif choice == "3":
            break
        else:
            print("Invalid choice, please try again.")


def movie_action_menu():
    while True:
        print("\n Choose Option below")
        menu_choices = [("Select Movie", "1"), ("Back", "2")]
        question = [
            inquirer.List('menu',
                          message="Select an Option:",
                          choices=menu_choices,
                          carousel=True)
        ]
        answers = inquirer.prompt(question)
        choice = answers['menu']
        if choice == "1":
            movie = select_movie()
            if movie:
                print("Check Seat Availability")
                show_date = select_show_date(movie_id=movie.movie_id)
                if show_date:
                    show_time = select_show_time(movie_id=movie.movie_id, show_date_str=show_date)
                    display_seats_for_session(movie.movie_id, show_date, show_time)
        elif choice == "2":
            return
        else:
            print("Invalid choice, please try again.")


def customer_logged_in_menu():
    while True:
        print("\n MRS>Customers")
        menu_choices = [("View Movies", "1"), ("Search Movies", "2"), ("Back", "3")]
        question = [
            inquirer.List('menu',
                          message="Select an Option:",
                          choices=menu_choices,
                          carousel=True)
        ]
        answers = inquirer.prompt(question)
        choice = answers['menu']
        if choice == "1":
            view_all_movies()
            movie_action_menu()

        elif choice == "2":
            while True:
                print("Search Movies")
                movie_title = input("Enter movie name to search or C to Cancel: ")
                if movie_title:
                    if movie_title.lower() == "c":
                        break
                    else:
                        show_movie_details_by_name(movie_title)
                        movie_action_menu()

        elif choice == "3":
            break
        else:
            print("Invalid choice, please try again.")


def manage_customer_menu():
    while True:
        print("\n MRS>Manage Customers")
        menu_choices = [("View Customer", "1"), ("Search Customer", "2"), ("Add Customer", "3"),
                        ("Update Customer", "4"), ("Remove Customer", "5"), ("Back", "6")]
        question = [
            inquirer.List('menu',
                          message="Select an Option:",
                          choices=menu_choices,
                          carousel=True)
        ]
        answers = inquirer.prompt(question)
        choice = answers['menu']
        if choice == "1":
            show_all_customers()
        if choice == "2":
            while True:
                print("Search Customer")
                cust_id = input("Enter customer id to search and C to Cancel: ")
                if cust_id:
                    if cust_id.lower() == "c":
                        break
                    else:
                        show_customer_details_by_id(cust_id)
        elif choice == "3":
            name = input("Enter Customer Full Name: ")
            email = input("Enter Customer Email Address: ")
            password = input("Enter New Password: ")
            c_password = input("Enter Customer New Password Again: ")
            address = input("Enter Customer Address(Optional): ")
            country = input("Enter Customer Country Name(Optional): ")
            if password == c_password:
                create_account(name=name, email=email, password=password, address=address, country=country)
            else:
                print("New password and confirm password must be same")
        elif choice == "4":
            cust_id = get_cust_id()
            if cust_id:
                name = input("Enter Customer Full Name: ")
                email = input("Enter Customer Email Address: ")
                address = input("Enter Customer Living Address(Optional): ")
                country = input("Enter Customer Country Name(Optional): ")
                success = update_profile(cust_id=cust_id, name=name, email=email, address=address, country=country)
                if success:
                    print(f"Customer for Id: {cust_id} updated!")
        elif choice == "5":
            cust_id = get_cust_id()
            if cust_id:
                success = delete_account(cust_id)
                if success:
                    print(f"Customer for Id: {cust_id} deleted!")
        elif choice == "6":
            break
        else:
            print("Bad Choice!, Try again.")
