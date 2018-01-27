Aircharts
-----------

A Django web application which provides graphs of recent air pollution measurements from over 120 automated
monitoring sites across the UK. Site locations are detailed using Google Maps and interactive charts are created using HighCharts, a JavaScript plotting library.
Chart data is obtained through requests to the aurn-API; endpoints are specified in the readme for the GitHub repository:  https://github.com/paulos84/aurn2

Getting Started
---------------


**Prerequisites**

Python 3.4, pip, virtualenv

**1. Clone or copy repository**

**2. Set up Virtual Environment**

Create a virtual environment named aurn-venv:

    $ virtualenv aurn-venv

Activate the virtual environment:

    $ source aurn-venv/bin/activate
    (aurn-venv) $

Use *pip* to install requirements:

    (aurn-venv) $ pip install requirements.txt

Verify that packages have been installed:

    (aurn-venv) $ pip freeze
    Django==2.0
    requests==2.13.0

**3. Run migrations and management commands**

Specify database settings, run initial migrations and then enter the following management commands within the project root directory to populate the Site table and obtain recent hourly data:

    $ python manage.py addsites

    $ python manage.py collectdata

**4. Run the server**

    $ python manage.py runserver