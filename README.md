# Squirrel
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fwingkwong%2Fsquirrel.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fwingkwong%2Fsquirrel?ref=badge_shield)


![](https://preview.ibb.co/b7GTNS/image.png)

## About
A responsive web application for expense tracking and analytics platform powered by Django

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
* tracker.templatetags.month_labels
* social_django

## Configured URLs:

* ``/``
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
* ``/dashboard``
* ``/auth/``
* ``/admin/``

## Templates:

Landing:
* ``landing/index.html``

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
* Google OAuth2

## Prerequisites

- Python >= 3.5
- pip

## Setup Your Environment
1. Fork this project
2. Install from the given requirements file.
```bash
pip install -r requirements.txt
```
3. Make Migrations
```bash
python manage.py makemigrations
```
4. Migrate
```bash
python manage.py migrate
```
5. Run
```bash
python manage.py runserver
```

## Setup Your Google OAuth
1. Go to Google Developers Console(https://console.developers.google.com/apis/library?project=_) and create a new project
2. Go to credentials tab
3. Create Credentials and choose OAuth Client ID
4. Select Web Application and enter any name in 'Product name shown to users' under OAuth Consent Screen tab
5. Set `http://127.0.0.1:8000/auth/complete/google-oauth2/` in Authorized redirect URIs
6. Under APIs and services tab, click on Google+ API and then click Enable
7. Copy the Client ID and Client Secret Under settings.py
```bash
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='' # ClientKey
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=''# SecretKey
```

## Authors

* **Wing Kam WONG** -  [@wingkwong](https://github.com/wingkwong)

## Contributor

* **Tushar Kapoor** -  [@TusharKapoor23](https://github.com/TusharKapoor23)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fwingkwong%2Fsquirrel.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fwingkwong%2Fsquirrel?ref=badge_large)