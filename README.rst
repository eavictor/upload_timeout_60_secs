==========================================
Django ASGI file upload 60 seconds timeout
==========================================

Django ASGI mysterious timeout when upload file request reached 60 seconds.

This is a minimum reproduce repository for reproducing the behavior.

-------
Prepare
-------

1. Install Python 3.8.x (3.8.5)
2. Execute command

.. code-block::

    sudo pip3 install -r requirements.txt

3. Create a large enough file which can take more than 60 seconds to upload. Or use something like NetLimiter to throttle upload speed.
4. Open browser and start upload

-------------
Run with WSGI
-------------

Note: request can survive over 60 seconds.

1. Open `settings.py`
2. Remove `'channels'` from `INSTALLED_APPS`
3. Remove `CHANNEL_LAYERS`
4. Remove `ASGI_APPLICATION`
5. Execute `manage.py runserver` command, or write a file called `uwsgi.ini` as in root folder, then execute production server command.

Development Server:

.. code-block::

    python3 manage.py runserver 0.0.0.0:8000

Production Server:

.. code-block::

    uwsgi -i uwsgi.ini

-------------
Run with ASGI
-------------

Note: request will timeout at 60 seconds.

1. Open `settings.py`
2. Add `'channels'` into `INSTALLED_APPS`
3. Add `CHANNEL_LAYERS`
4. Add `ASGI_APPLICATION`
5. Execute `manage.py runserver` command, or execute production server command

Development Server:

.. code-block::

    python3 manage.py runserver 0.0.0.0:8000

Production Server:

.. code-block::

    daphne -b 0.0.0.0 -p 8000 upload_timeout_60_secs.asgi:application

------------------------------------
Workaround before ASGI fix comes out
------------------------------------
For request takes over 60 seconds, stay at WSGI (uWSGI) until ASGI has fix for this issue.

Run 2 servers sharing same Database, SECRET_KEY and CORS settings (if have something like react.js or vue.js)

>> 1 ASGI Server to handle WebSocket

>> 1 WSGI Server to handle http request/response
