Project Overview

Goal Build an e-commerce web application with Django to promote sustainable shopping by offering products that reduce CO2 emissions such as bicycles and eco-friendly shoes The platform includes a login page with Google authentication a product list a shopping cart and an order confirmation system

Tech Stack Django Python PostgreSQL via Docker Bootstrap CDN Font Awesome CDN Kanit font Google Fonts

Environment Docker Compose with web Django and db PostgreSQL services

Abstract

Treevaq is an e-commerce platform developed to encourage sustainable consumption by focusing on selling products that help reduce carbon dioxide CO2 emissions such as bicycles and shoes made from recycled materials This project aims to enable users to purchase environmentally friendly products while tracking the amount of CO2 they reduce through their purchases Built using the Django Framework with PostgreSQL as the database the application runs in a Docker environment for easy development and deployment

The platform offers key features including Google login integration using django-allauth a shopping cart system that allows users to add adjust or remove products and an order confirmation page that displays the CO2 reduction achieved The user interface is designed with Bootstrap and Font Awesome for a modern look and enhanced usability while supporting Thai language with the Kanit font from Google Fonts

User Stories

1 User Seeking Eco-Friendly Products  
Description A user wants to browse and purchase products that reduce CO2 emissions such as bicycles or recycled shoes  
Goal Purchase environmentally friendly products and track the CO2 reduction from their orders

2 New User Registering and Logging In with Google  
Description A new user wants to register or log in using their Google account to access the platform  
Goal Securely access the system and start shopping quickly

3 User Managing Shopping Cart and Confirming Orders  
Description A user wants to add products to the cart adjust quantities remove items and confirm their purchase  
Goal Efficiently manage their order and receive a complete order confirmation

Usage Steps for User Stories

1 Browsing and Purchasing Eco-Friendly Products  
Step 1 Access the Treevaq website at localhost:8000 and log in using a Google account or register as a new user  
Step 2 After logging in the user is redirected to the homepage /index/ which displays a list of products with prices and CO2 reduction details  
Step 3 Select a product such as a bicycle or shoes and click the Add to Cart button  
Step 4 Navigate to the Cart page to review the selected products and total price  
Step 5 Click Confirm Cart to complete the purchase and view the CO2 reduction achieved

2 Registering and Logging In with Google  
Step 1 Visit localhost:8000 which automatically displays the login page  
Step 2 Click Log in with Google to use a Google account or click Register to create a new account with a username and password  
Step 3 Upon successful login the user is redirected to the homepage to begin shopping

3 Managing Shopping Cart and Confirming Orders  
Step 1 After logging in click the Cart icon in the navigation bar to access the Cart page  
Step 2 Review the list of products in the cart including product names prices quantities and total cost  
Step 3 Adjust quantities using the plus or minus buttons or click Remove to delete an item  
Step 4 Click Confirm Cart to finalize the purchase after which the cart is reset and the user receives an order confirmation

Installation and Usage

System Requirements  
Operating System Windows Linux or macOS  
Required Tools Docker and Docker Compose for running the application Git for cloning the repository A modern browser such as Google Chrome or Firefox  
Dependencies Django==4.2 django-allauth==0.58.2 django-extensions==3.2.3 psycopg2-binary==2.9.6 Pillow djangorestframework==3.15.2 gunicorn==20.1.0

Installation Steps  
1 Clone the Repository  
Open a terminal and run the following commands  
git clone https://github.com/Peerawastantitemit/dsi202_2025.git Treevaq  
cd Treevaq  

2 Verify Docker Installation  
Ensure Docker and Docker Compose are installed  
docker --version  
docker-compose --version  
If not installed download and install Docker Desktop from the official website https://www.docker.com/products/docker-desktop/  

3 Run the Application with Docker  
Confirm that the files Dockerfile docker-compose.yml entrypoint.sh and requirements.txt are present in the Treevaq directory  
Run the following command to build and start the container  
docker-compose up --build  
Wait until the container is running and the server starts at localhost:8000/  

4 Configure Google OAuth for Google Login  
Visit Google Cloud Console at https://console.developers.google.com/  
Create a new project and set up OAuth 2.0 Client IDs  
Add Authorized redirect URIs as localhost:8000/accounts/google/login/callback/  
Copy the Client ID and Client Secret then add them to Social Applications at localhost:8000/admin/  

5 Access the Application  
Open a browser and navigate to localhost:8000/ to access the login page  
Log in using a Google account or register as a new user  
The homepage will display a list of eco-friendly products  
Access the Cart page at localhost:8000/cart/  
Access the Admin page at localhost:8000/admin/  

Project Structure  
Treevaq/  
  myproject/  
    myproject/  
      settings.py  
      urls.py  
    store/  
      templates/  
        store/  
          base.html  
          index.html  
          cart.html  
        registration/  
          login.html  
          register.html  
      models.py  
      views.py  
      urls.py  
    manage.py  
  static/  
    css/  
      style.css  
  media/  
  Dockerfile  
  docker-compose.yml  
  entrypoint.sh  
  requirements.txt  

Additional Notes  
Troubleshooting  
If errors occur check the logs  
docker-compose logs web  
Ensure requirements.txt includes all necessary packages  
Future Development  
Add new models in store/models.py and run migrations to update the database  
Enhance the UI in templates/store/ by adding features like product search  

Summary

Treevaq is a platform that empowers users to shop for eco-friendly products while contributing to CO2 reduction With an intuitive design Google login integration and a comprehensive shopping cart system Treevaq effectively promotes sustainable consumption

Character Count 1080 characters