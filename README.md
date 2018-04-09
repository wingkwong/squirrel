# Django Expense Tracker

## About
A responsive web application for expense tracking and analytics powered by Django

## Installed apps:
* django 2.0.2
* django.contrib.admin
* django.contrib.auth
* django.contrib.contenttypes
* django.contrib.sessions
* django.contrib.messages
* django.contrib.staticfiles
* tracker.apps.TrackerConfig
* django_tables2
* django_filters
* bootstrap3
* crispy_forms

## Configured URLs:

* ``/tracker``
* ``/tracker/add``
* ``/tracker/update/{id}``
* ``/analytics``
* ``/analytics/{year}``
* ``/analytics/{year}/{month}``
* ``/analytics/{year}/{month}/{day}``
* ``/accounts/register``
* ``/accounts/login``
* ``/accounts/logout``
* ``/accounts/profile/{id}``
* ``/admin/``

## Templates:

Tracker:
* ``tracker/expense_form.html``
* ``tracker/from_template.html``
* ``tracker/header.html``
* ``tracker/index.html``
* ``analytics/index.html``

Accounts:
* ``registration/login.html``
* ``registration/logged_out.html``

## Features:

* Responsive 
* Expense Overview with filtering
* Expense addition
* Expense Analytics by year, month or day
* Bootstrap 3 based

## Usage
TBA

## Prerequisites

- Python >= 3.5
- pip

## Installation
1. Fork this project
2. Make Migrations
```bash
python manage.py makemigrations
```
3. Migrate
```bash
python manage.py migrate
```
4. Run
```bash
python manage.py runserver
```

## Authors

* **Wing Kam WONG** -  [@wingkwong](https://github.com/wingkwong)

## Contributor

* **Tushar Kapoor** -  [@TusharKapoor23](https://github.com/TusharKapoor23)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details