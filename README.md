# FLASK Template - Konco Dev

flask template for easy web application project start

In this application template you will find all the usefull flask plugins already configured. check the requirements.txt for details.

The project is build using flask blueprints. Two blueprints are implemented Base and Home. The file structure is as follow

```
└── erp-bet
    ├── app
    │   ├── __init__.py # main init file
    │   ├── admin        # admin dashboard blueprint folder
    │   ├── base        # base blueprint folder
    │   ├── site      # website front blueprint folder
    ├── config.py       # the app config file containing different configuration for development, production or debug mode 
    ├── .env            # all the app environement variable are set here
    ├── .gitignore
    ├── requirements.txt
    └── run.py         # the application entry point
```
Authentification page must be implemented the project already contains the user model and authentification Wtform.

###### Base blueprint
The base blueprint contains authentication logic, the project models, different usefull tools and the project static files.
```
└── base
    ├── static             # all the app static files folder
    ├── template            # html files
    ├── __init__.py         # the blueprint initialisation
    ├── errors.py           # error pages redirections
    ├── events.py           # socket io events
    ├── forms.py            # authentication forms and validation using WTForm
    ├── mixins.py           # models classes mixins
    ├── models.py           # all the project models
    ├── orm_tools.py        # database related tools
    ├── routes.py           # main application routes
    ├── search.py           # elasticsearch indexing logic
    ├── tools.py            # different util functions and classes 
```

###### Home blueprint
The site blueprint contains the authenticated users main pages
```
└── site
    ├── template            # html files
    ├── __init__.py         # the blueprint initialisation
    ├── forms.py            # authentication forms and validation using WTForm
    ├── routes.py           # the home blueprint routes
```

# Requirement

Python 3.10, virtualenv, mysql

# Installation

The project uses Mysql for the database, make sure to create a mysql database before proceeding to the project building

````
mysql -u root

mysql> CREATE USER 'webapp_admin'@'localhost' IDENTIFIED BY 'password';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE DATABASE webapp_db;
Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON webapp_db . * TO 'webapp_admin'@'localhost';
Query OK, 0 rows affected (0.00 sec)
````
To use a different database or credentials make sure to change the SQLALCHEMY_DATABASE_URI value in the project .env file.

Before proceeding to the installation you should install virtualenv and create a new dev environment.
After that switch to your new environment and install all the project requirements

```
pip install -r requirements.txt
```

set the flask env variable
```
set FLASK_APP=run.py
```

for Windows powershell
```
$env:FLASK_APP='run.py'
```
use alembic the build the database

init : to initialize alembic migration. 
migrate: to generate the migration file. 
upgrade: to create the tables. 

```
flask db init
flask db migrate
flask db upgrade
```
Switch to the flask shell to create an admin user.
```
flask shell
```

In the flask shell import User model and db, and initialize a new user object

```
from app.base.models import User
from app import db

admin = User(email="admin@app.com", first_name="administrator", last_name="app", password="12345678")
```
Make the user admin and activate it
```
admin.is_admin = true
admin.is_active = true
```
Add the new user to the database and commit the changes
```
db.session.add(admin)
db.session.commit()
```
exit the flask shell
```
exit()
```
Run the app

```
python run.py
```

If everything went smoothly the app should be running on http://127.0.0.1:5000/
