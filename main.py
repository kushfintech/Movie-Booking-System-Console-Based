import inquirer

from views.customer import customer_non_logged_in_menu
from views.staff import staff_non_logged_in_menu, check_staff_exists_or_not


def main_menu():
    check_staff_exists_or_not()
    while True:
        print("\nWelcome to Movie Reservation System")
        print("Choose User Type")
        menu_choices = [("I am Customer", "1"), ("I am Staff", "2"), ("Exit", "3")]
        question = [
            inquirer.List('menu',
                          message="Select an Option:",
                          choices=menu_choices,
                          carousel=True)
        ]

        answers = inquirer.prompt(question)

        choice = answers['menu']
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
