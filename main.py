from views.customer import customer_non_logged_in_menu
from views.staff import staff_non_logged_in_menu, check_staff_exists_or_not


def main_menu():
    check_staff_exists_or_not()
    while True:
        print("\nWelcome to Movie Reservation System")
        print("Choose User Type")
        print("1. Customer")
        print("2. Staff")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            customer_non_logged_in_menu()
        elif choice == "2":
            staff_non_logged_in_menu()
        elif choice == "3":
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main_menu()
