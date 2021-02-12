Installation
============

Installation can be done either as a single docker container inside a ``docker-compose.yml`` using
the docker image on dockerhub ``mlfaati:latest``

Embedded within an existing `docker-compose.yml`
################################################

.. code-block:: yaml
    :caption: ``docker-compose.yml``
    :name: your existing docker compose

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
this method requires you to provide your own ``postgres``, ``redis``, and ``nginx`` configurations,
which can be changed in ``conf.py`` or directly as environment variables as in ``.env-example``, and
nginx can be configured based on ``conf/nginx.http.conf`` or ``conf/nginx.conf`` with SSL.


using `docker-compose.yml`
##########################

or you can use the provided ``docker-compose-yml`` and run this command in order to run
all required services.

.. code-block:: shell
    :caption: ~/
    :name: ~/

    $ docker-compose up -d

