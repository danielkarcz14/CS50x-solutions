# Contact Management App
#### Video Demo:  <URL HERE>
#### Description:


### Introduction:

Welcome to the Contact Management App, a robust and user-friendly command-line tool designed to streamline your contact organization. Executed with the command python project.py, this application provides an efficient interface for managing your contacts with ease.

### Key Features:

#### Adding New Contacts:

Option 1 allows users to effortlessly add a new contact by providing the individual's name and phone number.
The application intelligently stores this information in list.csv. If the file doesn't exist, the app's "add_new" function dynamically creates it.
Phone numbers undergo meticulous validation using regular expressions in the is_valid function, ensuring accuracy. The is regex pattern in is valid function was obtained from this source: https://softhints.com/regex-phone-number-find-validation-python/


#### Removing Contacts:

Option 2 empowers users to remove contacts by name, phone number, or choose to delete all contacts.
Deleting all contacts prompts a warning for confirmation, ensuring users do not accidentally erase their entire contact list.


#### Searching Contacts:

Option 3 provides two search options: by name or by phone number.
A red error message notifies users if the specified name or phone number is not found.


#### Viewing All Contacts:

Option 4 allows users to view all contacts in a well-organized tabular format.
If the contact list does not exist, users are prompted to create one with the "Add new(1)" option.


#### Graceful Exit:

Option 5 enables users to gracefully close the program when they are done managing their contacts.


#### Enhancements:

The application employs a colorful terminal output using the print_colored function, enhancing the user experience.
The tabulate library is utilized to present contacts in a visually appealing tabular format.
The project incorporates error handling, ensuring smooth interactions and preventing unintended actions.


#### Usage:

Execute the app with python project.py and follow the on-screen menu to manage your contacts seamlessly. Whether adding, removing, or searching for contacts, this command-line app offers a simple yet effective solution for contact management.

This was my CS50P final project.

Thank you.