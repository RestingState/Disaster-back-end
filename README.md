# stellarly-back-end
To build this project


1 - > virtualenv venv


2 - > activate environment

     for Windows: 
source env/bin/activate

     for Linux:
       source venv/bin/activate
       
       
3 - > install the requirements

    pip install -r requirements.txt
    
    
4 -> run 

    Run app.py
    

Environment variables for db:   
     STELLARLY_USER  - postgres username(default = 'postgres') 
     STELLARLY_PASSWORD - postgres password 
     STELLARLY_SERVER - postgres server name(default = 'localhost') 
 
 
Description:

API - package used for storing data about some libs, where there is information about planets, etc.

Database - package where there is a script for PostgreSQL

Models - package to store our models

Rest - package to store restful application
