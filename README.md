# Simple Stock

Author: soldiers-son

POS.py Version: 1.0

Python: 3.11+

Platform: Windows / Linux / Mac

Dependencies: tkinter, customtkinter

----------------------------------------------------
0. Acknowledgments
----------------------------------------------------

Thank you to the open source community, whose 
work makes this project possible.

----------------------------------------------------
1. Introduction
----------------------------------------------------

A simple GUI application designed to manage a farm inventory and allows users to create accounts, log in, and access various features such as data logging, task management, and farm supply tracking.

----------------------------------------------------
2. Features
----------------------------------------------------
-GUI design: The application uses Tkinter & Custontkinter to create a simple GUI with buttons, labels, and entry forms.

-Login/Registration: Users can create an account or log in using their username and password. The application uses a JSON file to store the current user's session information, allowing users to log in and stay logged in between runs.

<img src="/sImple_stock/media/Login.png">

-Data Logging: There are three types of data that can be logged: plant, harvest, and task. Each type has its own entry form with fields for the item name, quantity, and date/time.

<img src="/sImple_stock/media/HarvestLogEntry.png">

-Farm Inventory: The application allows users to manage farm supplies, including tools, farm supplies, and animal supplies. Each supply has its own entry form with fields for the item name, quantity and price.

<img src="/sImple_stock/media/AnimalSupplyEntry.png">

-Task Management: Users can log tasks completed on the farm, with fields for the task description, date/time, and quantity (if applicable).

-View Data: Users can view logged data in various forms, including tables and charts via menubar items.
<img src="/sImple_stock/media/AnimalSupply.png">


----------------------------------------------------
3. Requirements
----------------------------------------------------

-Python: 3.11+

-customtkinter

----------------------------------------------------
4. Installation
----------------------------------------------------
1. Clone or download this repository.
2. Place the project folder on your desktop or 
   desired directory.
3. Install Python and required dependencies.
4. Run the application:

   Windows:
   > python main.py

   Linux/Mac:
   $ python3 main.py

----------------------------------------------------
5. Dependencies
----------------------------------------------------
Open file in terminal and run:

   >pip install REQUIREMENTS.txt

----------------------------------------------------
6. Usage
----------------------------------------------------
1. Getting Started
   
-Create an Account: To start, click on "Create User" and follow the prompts to create a new account.

-Log In: Once your account is created, log in by entering your username and password.

-Main Menu: You will be taken to the main menu, where you can access various features such as Data Logging, Farm Inventory, and Task Management.

3. Data Logging
   
-Plant Log: To log new plants, click on "Plant" and enter the plant name and quantity.

-Harvest Log: To log harvested items, click on "Harvest" and enter the item name and quantity.

-Task Log: To log completed tasks, click on "Task" and enter the task completed.

4. Farm Inventory

-Tools: To manage your farm tools, click on "Tool Supply" and enter the tool name and quantity.

-Farm Supplies: To manage your farm supplies, click on "Farm Supply" and enter the supply name and quantity.

-Animal Supplies: To manage your animal supplies, click on "Animal Supply" and enter the supply name, quantity, and price.

4. View Data and Inventory

-Click on "View Data" in the menu bar, and select the data entries you wish to view(Plant, Harvest, Tasks)

-Click on "View Inv" to view your farm inventory(Tools, Farm Supplies, Animal Supplies)

----------------------------------------------------
7. Future Goals
----------------------------------------------------

Planned expansions include:

-Expaned data visualization and management

-User Task assignment with todo notifications

----------------------------------------------------
8. Contributing
----------------------------------------------------

Suggestions and improvements are welcome. 
Fork the repo, make your changes, and submit a PR.

----------------------------------------------------
9. License
----------------------------------------------------

This project is open source under the MIT License.

----------------------------------------------------
10. Contact
----------------------------------------------------

Author: soldiers-son

GitHub: (https://github.com/soldiers-son?tab=repositories)

Email: (soldiers.son1618@gmail.com)
