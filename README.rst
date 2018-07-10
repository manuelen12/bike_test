Project Name
============

project to rent cars

Requirement
--------
	- postgresql
	- Python3.6
	- Django 1.11

How to Install
--------
	if you want to use the local enviroment use:
		pip install -r requirements/local.txt
	to make unitary test use 
		pip install -r requirements/test.txt
	the next step is run the migration
		./manage.py migration
	to finih load the fixture
		./manage.py loaddata rental/rents/fixture/price_by_frecuency.json

How to Use
--------
	to run the project like api use:
		./manage.py runserver
	then you can intro in the documentation since the url http://localhost:8000
	to run the unitary test use:
		./manage.py test


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html


Main Application
----------------
the Main class is in the folder 
    rental/rents/v0/api.py with the class Controller this extend from my Base Class (rental/common/utils.py) , utils.py are the tools that i would use in all the project  

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest
  the unit test are in rentals/rents/tests

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



