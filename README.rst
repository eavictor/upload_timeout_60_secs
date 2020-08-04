==================================================
Django ASGI file upload request 60 seconds timeout
==================================================

Django ASGI mysterious timeout when upload file request reached 60 seconds.

This is a minimum reproduce repository for reproducing the behavior.

Download request is not impact by this bug.

Python: 3.8.5

OS:

1. MacOS 10.15.6 Catalina (amd64, 2020/08/04)
2. Windows 10.0.19041.1 with latest patches installed (amd64, 2020/08/04)
3. Ubuntu 20.04 LTS with latest patches (amd64, 2020/08/04)

Site-Packages:

.. code-block:: shell

    Django==3.0.8
    daphne==2.5.0
    channels==2.4.0
    uWSGI==2.0.19.1

-------
Prepare
-------

1. Install Python 3.8.x (3.8.5)
2. Execute command

.. code-block:: shell

    sudo pip3 install -r requirements.txt

3. Create a large enough file which can take more than 60 seconds to upload. Or use something like NetLimiter to throttle upload speed.
4. Open browser and start upload

-------------
Run with WSGI
-------------

Note: request can survive over 60 seconds.

Development Server:

Be aware, `'channels'`

1. Open `settings.py`
2. Remove `'channels'` from `INSTALLED_APPS`
3. Execute `manage.py runserver` command.

.. code-block:: shell

    python3 manage.py runserver 0.0.0.0:8000

Production Server:

1. Install uWSGI
2. Write a ini config file as `uwsgi.ini`,
3. Execute `uwsgi -i uwsgi.ini` command.

.. code-block:: shell

    uwsgi -i uwsgi.ini

-------------
Run with ASGI
-------------

Note: request will timeout at 60 seconds.

Development Server:

1. Open `settings.py`
2. Add `'channels'` into `INSTALLED_APPS`
3. Make sure `CHANNEL_LAYERS` setup is correct and is enabled.
4. Make sure `ASGI_APPLICATION` setup is correct and is enabled.
5. Execute `manage.py runserver` command.

.. code-block:: shell

    python3 manage.py runserver 0.0.0.0:8000

Production Server:

1. Make sure daphne is installed (should installed with channels).
2. Add `'channels'` into `INSTALLED_APPS`
3. Make sure `CHANNEL_LAYERS` setup is correct and is enabled.
4. Make sure `ASGI_APPLICATION` setup is correct and is enabled.
5. Execute `daphne` command.

.. code-block:: shell

    daphne -b 0.0.0.0 -p 8000 upload_timeout_60_secs.asgi:application

------------------------------------
Workaround before ASGI fix comes out
------------------------------------
For request takes over 60 seconds, stay at WSGI (uWSGI) until ASGI has fix for this issue.

Run 2 servers sharing same Database, SECRET_KEY and CORS settings (if have something like react.js or vue.js)

>> 1 ASGI Server to handle WebSocket

>> 1 WSGI Server to handle http request/response

Q: What will happen I forget to disable/remove `'channels'` and run with uWSGI ?

A: At the time I test (2020/08/04), http request/response works normally.
WebSocket is not working with WSGI as expected.
You can use same repository, start both ASGI & WSGI, split these servers by FQDN and point all upload requests to WSGI.
Then everything is gonna be ok.
