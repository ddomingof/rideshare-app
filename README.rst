CarPool
=======
A Django-based web application to facilitate sharing commutes in a company.

What information is stored?
---------------------------
This web application displays only emails as personal information.

Getting Started
---------------
1. Install the requirements

.. code-block:: sh

    $ python -m pip install -r requirements.txt

2. Set up the database

.. code-block:: sh

    $ python manage.py makemigrations ui
    $ python manage.py migrate

3. Start the app

.. code-block:: sh

    $ python manage.py runserver

Getting Started with Docker
---------------------------
This web application comes with a ``Dockerfile`` and ``docker-compose.yml``. It can be run with:

.. code-block:: sh

    $ docker-compose up

Cron Job
--------
Periodically run this command to remove expired commutes

.. code-block:: sh

    $ python manage.py delete_expired
