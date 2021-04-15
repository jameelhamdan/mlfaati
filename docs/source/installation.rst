Installation
============

Installation can be done either as a single docker container inside a :code:`docker-compose.yml` using
the docker image on dockerhub :code:`mlfaati:latest`

Embedded within an existing :code:`docker-compose.yml`
------------------------------------------------------

.. code-block:: yaml

    mlfaati_web:
      image: "mlfaati:latest"
      command: bash -c "./scripts/release.sh && daphne -b 0.0.0.0 -p 8000 app.server:application"
      env_file: .mlfaati_env
      volumes:
        - static_volume:/usr/src/app/.static
        - media_volume:/usr/src/app/media
        - logs_app:/var/log/app
        # Use this to custom settings without rebuilding image
        - ./mlfaati/conf.py:/var/log/app/settings/conf.py
        # Use this to install extra dependencies without rebuilding image
        - ./mlfaati/requirements-extra.txt:/var/log/app/requirements-extra.txt


*Note*:
this method requires you to provide your own :code:`postgres`, :code:`redis`, and :code:`nginx` configurations,
which can be changed in :code:`conf.py` or directly as environment variables as in :code:`.env-example`, and
nginx can be configured based on :code:`conf/nginx.http.conf` or :code:`conf/nginx.conf` with HTTPS.


using :code:`docker-compose.yml`
--------------------------------

or you can use the provided :code:`docker-compose-yml` and run this command in order to run
all required services.

.. code-block:: shell

    $ docker-compose up -d



Post Installation
-----------------

After installation you will need to create a user, this can be done using django command
from inside a running docker container:

.. code-block:: shell

    $ docker exec -it <container_name> /bin/bash
    $ python manage.py createsuperuser

and enter all the necessary information when prompted.
