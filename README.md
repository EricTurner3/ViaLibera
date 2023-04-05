# ViaLibera
A free, open-source vehicle management web application, written in Python


## Powered by
* [Django Argon Dashboard](https://github.com/app-generator/django-argon-dashboard) template


## Setup Instructions (forked from the template's [readme](https://github.com/app-generator/django-argon-dashboard/blob/master/README.md))
> 👉 Download the code  

```bash
$ git clone https://github.com/EricTurner3/ViaLibera.git
$ cd ViaLibera
```
> 👉 Install modules via `VENV`  
```bash
# Linux
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
```ps
# Windows
PS > python -m venv env
PS > . .\env\Scripts\Activate.ps1
PS > pip install -r requirements.txt
```

> 👉 Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

> 👉 Create the Superuser

```bash
$ python manage.py createsuperuser
```

> 👉 Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                            
   |    |-- settings.py                  # Project Configuration  
   |    |-- urls.py                      # Project Routing
   |
   |-- home/
   |    |-- views.py                     # APP Views 
   |    |-- urls.py                      # APP Routing
   |    |-- models.py                    # APP Models 
   |    |-- tests.py                     # Tests  
   |    |-- templates/                   # Theme Customisation 
   |         |-- includes                # 
   |              |-- custom-footer.py   # Custom Footer      
   |     
   |-- requirements.txt                  # Project Dependencies
   |
   |-- env.sample                        # ENV Configuration (default values)
   |-- manage.py                         # Start the app - Django default start script
   |
   |-- ************************************************************************
```
