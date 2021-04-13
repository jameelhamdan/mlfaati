.. Mlfaati documentation master file, created by
   sphinx-quickstart on Fri Feb 12 15:34:41 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
===================================

.. toctree::
   :maxdepth: 2

   self
   installation
   api/index

What is Mlfaati?
----------------

a file server/cdn/processing backend.

Application Stack
-----------------

Mlfaati is built on the Django Python framework and utilizes a PostgreSQL database.
It runs as an ASGI service behind an HTTP server.

.. list-table::
   :header-rows: 1

   * - Function
     - Component

   * - HTTP Service
     - Nginx or Apache

   * - ASGI Service
     - daphne or uvicorn

   * - Application
     - Django/Python

   * - Database
     - PostgreSQL 12.6+

   * - Background jobs
     - Celery/Redis


Contribute to Mlfaati
---------------------

If you discovered a bug or want to improve the code, please submit an issue and/or pull request via GitHub.
Before submitting a new issue, please make sure there is no issue submitted that involves the same problem.

| GitHub repository: https://github.com/kingjmk/mlfaati
| Issues: https://github.com/kingjmk/mlfaati/issues
