import shutil
import csv
import os
import sys
from tabulate import tabulate
import re




def main():
    # print app menu
    print_menu()

    option = get_option()
    while True:
        if option == 1:
            print(add_new())
            print_menu()
            option = get_option()
        elif option == 2:
            print(remove_contact())
            print_menu()
            option = get_option()
        elif option == 3:
            print(find_contact())
            print_menu()
            option = get_option()
        elif option == 4:
            print(see_all())
            print_menu()
            option = get_option()
        else:
            sys.exit(0)


def print_menu():
    print(print_colored("< MY CONTACTS >", 'underline'))
    print(print_colored("< 1 > | Add new", 'green'))
    print(print_colored("< 2 > | Remove", 'green'))
    print(print_colored("< 3 > | Search", 'green'))
    print(print_colored("< 4 > | See all", 'green'))
    print(print_colored("< 5 > | Exit", 'green'))


def print_colored(text, color):
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'reset': '\033[0m',
        'underline': '\033[4m'
    }
    return f"{colors[color]}{text}{colors['reset']}"


# Regular expression for phone number validation
# Source: https://softhints.com/regex-phone-number-find-validation-python/
def is_valid(phone_number):
    pattern = r"^[\+\(]?\d+(?:[- \)\(]+\d+)+$"
    match = re.match(pattern, phone_number)
    if match:
        return True
    return False


def get_option():
    # If option is not between 1-5, reprompt
    while True:
        try:
            option = int(input("Enter option number: "))
            if option > 5 or option < 1:
                raise ValueError
            return option
        except ValueError:
            continue


def get_contact_info():
    name = input("Name: ")
    tel = input("Phone number: ")
    
    return name, tel
    

def add_new():
    name, tel = get_contact_info()
    if not is_valid(tel):
        return print_colored("Invalid phone number", 'red')

    # create list.csv if it does not exist
    if not check_file_exists():
        # if list.csv does not exist, create it
        with open("list.csv", "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'phone'])
            writer.writeheader()

    
    with open("list.csv", "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'phone'])
        writer.writerow({'name': name, 'phone': tel})
        
    return print_colored("Contact added successfully", 'green')


def find_contact():
    # if list.csv does not exist, print warning message and reprompt for option
    if not check_file_exists():
        return f"Contact list does not exist create new with: {print_colored("Add new(1)", 'green')}"
    
    option = int(input("Search by name(0) by phone number(1): "))
    if option == 0:
        name = input("Name: ")
        with open("list.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] == name:
                    return (print_colored(f"{row['name']}, {row['phone']}", 'green'))
            return print_colored("Contact not found", 'red')
    elif option == 1:
        tel = input("Phone number: ")
        with open("list.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['phone'] == tel:
                    return (print_colored(f"{row['name']}, {row['phone']}", 'green'))
            return print_colored("Contact not found", 'red')


def remove_contact():
    # if list.csv does not exist, print warning message and reprompt for option
    if not check_file_exists():
        return f"Contact list does not exist create new with: {print_colored("Add new(1)", 'green')}"
    remove_option = int(input("Remove by name(0) by phone number(1) or remove all(2): "))
    if remove_option == 0:
        name = input("Name: ")
        field = 'name'
    elif remove_option == 1:
        tel = input("Phone: ")
        field = 'phone'
    elif remove_option == 2:
        warning = input("Are you sure you want to remove all contacts? y/n: ").lower()
    else:
        return print_colored("Invalid remove option", 'red')

    with open("list.csv") as file, open ("temp.csv", "w", newline='') as outfile:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(outfile, fieldnames=['name', 'phone'])
        writer.writeheader()

        for row in reader:
            if remove_option == 0 and name not in row["name"]:
                return f"Name not found"
            elif remove_option == 1 and tel not in row["phone"]:
                return f"Phone number not found"
            elif warning == 'y':
                continue
            elif row[field] != (name if remove_option == 0 else tel):
                writer.writerow({'name': row['name'], 'phone': row['phone']})
    if remove_option == 2 and warning == 'y':
        shutil.move("temp.csv", "list.csv")
        return print_colored("All contacts removed successfully", 'green')
    
    shutil.move("temp.csv", "list.csv")
    return print_colored("Contact removed successfully", 'green')
                        
        

def see_all():
    # if list.csv does not exist, print warning message and reprompt for option
    if not check_file_exists():
        return f"Contact list does not exist create new with: {print_colored("Add new(1)", 'green')}"
    contacts = []
    with open("list.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            contacts.append(row)
    return (tabulate(contacts, headers="firstrow", tablefmt="rounded_grid"))


def check_file_exists():
    file_exists = os.path.isfile("list.csv")
    return file_exists



if __name__ == "__main__":
    main()