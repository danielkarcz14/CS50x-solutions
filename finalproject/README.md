# SAVINGS.IO
#### Video Demo:  <URL HERE>
#### Description:

## Project Description
Savings.io is a web application designed to help users calculate and visualize the potential growth of their savings over time. User can edit monthly saved value (max 400€), time of savings (max 25 years), extra deposit (max 20000€), interest rate (max 15%) and lastly name their plan accordingly. The web application then allows users to save their plans, view them together in a table, and edit them as needed.

## Key Features
<b>Flexible calculator:</b> Users can input and later on edit the monthly saved amount (0 - 400€), the time of savings (1 - 25 years), extra deposits (0 - 20000€), and the interest rate (0.1 - 15%). They can also name their savings plans for easy identification. For example gold investment.

<b>Plan manager:</b> Users can save their plans and view them on a dedicated page. Each plan can be edited, deleted, or downloaded as a PDF document.

<b>User-friendly interface:</b>  The application has a clean and intuitive interface, making it easy to use for users with different levels of technical knowledge.

<b>Dynamic news feed:</b> On the homepage there are newest articles from world of finance and technology.


## Application Structure
Web application is divided into 4 pages.

- Homepage
- Create Plan
- My Plans
- Settings


## Pages Description

### Homepage
 On the homepage user is greeted with their name and under that is little text. Then there are shown 3 articles either from technology or finance topic which is selected randomly. Then there are two buttons "Create a new plan" which will redirect user to the create plan page and "Load news" which refreshes the homepage and show different 3 articles.

### Create Plan
This page is the core of the application it is where the calculator for counting the amount of money saved is. I used coumpound interest for counting. The calculator has 1 input text field: Plan's name and 4 input range fields: Monthly amount, Time of saving, Extra deposit and interest rate.

Then there is a button called "Save plan" which will redirect you to "MY PLANS" and shows you all your created plans. However if you dont fill the plan's name error message is flashed.


### My Plans
The My Plans page lists all the savings plans created by the user. Each plan is displayed in a table format with the following columns:

Plan's name: The user-assigned name of the savings plan.
Total amount saved: The projected total amount saved at the end of the specified duration.
Monthly amount: The monthly savings amount.
Date of creation: The date when the plan was created.
Action: Includes options to edit or download the plan.

In the action column there is:

Edit button which opens popup where user can edit the created plan in same way as when it was being created. Then at the bottom of the popup there are 3 buttons save changes which closes the popup, update the selected plan which updates the plan, cancel which just closes the popup without any changes being made and delete button which will delete the plan.

Download button will start generating pdf file and after 8 second downloading of PDF file starts. PDF file contains title which is the plan's name. Then bellow the title there is information about monthly amount, extra deposit, time of saving, interest rate and in bold totaly saved amount. Under that is a table with 3 columns and time of saving rows. Columns are year, growth and total amount and what you can see here is every year growth of the investment and cumulated total amount of that year. Then there is a chart representing the same what the table does but graphicly.


### Settings
Last page is settings where user can update their information provided when registering. This information is their first name, last name, username, email and password.


## Technologies Used
### Back End
Flask: A micro web framework that was taught in CS50x class.

### Database
SQLite: Also taught in CS50x class and it is a great choice for this local project since it is serveless and is simple to setup and use with Flask.

### Front End
HTML & JavaScript: For templates and enhanced user experience.
Tailwind CSS: I wanted to learn some new technologies along side this project so for styling I decied to choose Tailwind CSS because of it's popularity and easiness of use when you grab the logic behind it

## Detailed File Explanation
### HTML Files
HTML files contains templates for each page. I have base.html which contains the head and nav bar and is being used as extension for other templates.

### CSS Files
input.css & output.css: These files contain the Tailwind CSS styles.
styles.css: Custom styles mainly wrote for the input sliders in the calculator.

### script.js
This file contains main user experience features. The main one is interactive calculator where displayed total amount saved value is being changed in real time as you move the sliders. Next I wanted to train some AJAX requsts so I added them for submiting settings for and for downloading the saving plan as pdf file.

### init.py
Contains the configuration settings for the Flask application.

### auth.py
This file contains main logic for user authentification. It checks if required fields are completed, if email is correct and if password matches requrements and then if repeated password matches with the initial one. If any of those requirements are not met then corresponding error message is flashed.
Handles user authentication processes, including:


### main.py
The main backend logic is implemented here, with functions handling various aspects of the application:

<b>create_plan():</b> Manages the creation of new plans, storing them in the database, and handling errors.

<b>my_plans():</b> Handles the display, editing, and deletion of plans, as well as the creation and downloading of PDF files.

<b>settings():</b> Manages user settings updates, ensuring data validation before saving.

<b>update_flags():</b> A helper function for error checking.

<b>create_pdf():</b> Generates PDF files using the FPDF library, containing detailed information about the savings plans.

<b>calculate_result():</b> Ensures accurate calculation of the saved amounts.

<b>get_articles():</b> Fetches and displays articles from the News API for the homepage.

<b>download():</b> Sends the PDF file as a downloadable attachment.

<b>remove_file():</b> Deletes the generated PDF file if it exists.
 

