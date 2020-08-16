# Application Summary
The goal of this application is to apply skills of full stack web development that uses Python Django framework. CRUD implementaion to provide support of create, view, update and delete. This application works on local environment.
# Software Requirements
This application runs on local environment.
All required software to run this application is already made available in Vagrantfile provided by Udacity. Hence separately no installation is required.
Application:
1. [Python - 3.6+](https://www.python.org/download/releases/3.0/)
4. [Git](https://git-scm.com/download/win)
# How to run the project
A. Download(Optional):
1. [Git](https://git-scm.com/download/win)
2. [Pycharm](https://www.jetbrains.com/pycharm/download/#section=mac)

B. Installation(If not installed):
1. Git(To clone the project)
2. Virtualenv
3. Packages

C. Run
1. Open gitbash terminal
2. Create new directory or you can use existing one. For creating directory use mkdir 'DirectoryName' on gitbash terminal/cmd.
3. Goto the directory where you want to keep your files.
4. ```git clone project_url``` use this command to clone the project.
5. ```pip install virtualenv``` install virtualenv
6. ```virtualenv mypython``` create environment.
7. ```source mypython/bin/activate``` to start the environment.
8. ```pip install -r requirements.txt``` install all required packages.
9. After completing step 8th, ```python manage.py makemigrations``` to create database schema and tables.
10. ```python manage.py migrate``` to migrate according to new db structure.
11. ```python manage.py runserver``` this will run your server
12. Now open browser and type 'https://localhost:8000/' in URL bar to see homepage.

# Navigation in application
1. 'https://localhost:8000/' or 'https://localhost:5000/home/' to view the homepage.
2. 'https://localhost:8000/login/' to login as user or manager.
3. 'https://localhost:5000/register/ to register as user or manager.
4. 'https://localhost:8000/orders/ to view orders that were placed by the user are approved/rejected/on pending or not..
5. 'https://localhost:8000/cart/ to view items that were added to cart.
6. 'https://localhost:8000/checkout/ to place the order.
7. 'https://localhost:8000/profile/ to view profile for both user/manager.
8. 'https://localhost:8000/orders_status/ or Incoming orders on navigation bar, to accept or reject the order handled by manager only. (Required login)
9. 'https://localhost:8000/orders_history/' to view all orders that were accepted or reject(Only available for manager).
10. 'https://localhost:8000/product_create/' to add new product(Only for manager)
11. 'https://localhost:8000/add_address/' to add new shipping address(Only for user)
12. 'https://localhost:8000/add_category/' to add product category(Only for manager)
13. 'https://localhost:8000/update_category/' to update product category(Only for manager)
14. 'https://localhost:8000/update_product/product_id/' to update product details(Only for manager)
15. 'https://localhost:8000/update_product/product_id/' to update product details(Only for manager)
16. 'https://localhost:8000/update_profile/' to update profile details.
# JSON Endpoints
Will add soon.
# Troubleshoot
A. Create superuser to handle the reset password feature as of now. In future I will add reset feature with email as recovery method.
```python manange.py createsuperuser``` Required fields - First Name, Last Name, Email, Password, Confirm Password. 

B. If DB got deleted, if you run into problem and then create again.
paste code below to get the python3 compatiable modules and packages.
1. sudo apt-get -qqy install python3 python3-pip
2. sudo pip3 install --upgrade pip


C. If python3 manage.py gives error that might be for dos and unix format difference. To over come install
1. run sudo apt-get install dos2unix on gitbash terminal/cmd
2. run dos2unix manage.py on gitbash terminal/cmd

D. Unreachable issue may be caused due to trying to access using ```https://``` 

# Note
This project was done as part of the Dphi Web Development Assigned for the Web Development Role. This project was done by me only. 
