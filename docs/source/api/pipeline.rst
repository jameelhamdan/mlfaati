Pipeline
========

These endpoints can be used to perform operations on :code:`Pipeline` objects.


Create
------
.. code-block::

    POST /pipeline

Creates a Pipeline.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`name`
     - string
     - body
     - Name of new pipeline (also used as a prefix for file name if applicable)

   * - :code:`folder`
     - string
     - body
     - Folder ID

   * - :code:`target_type`
     - string
     - body
     - Target file types ('ALL', 'IMAGE', 'VIDEO', 'AUDIO')



Response
^^^^^^^^
.. code-block::

    Status: 201 Created

.. code-block:: JSON

    {
        "id": 2,
        "name": "test",
        "is_enabled": true,
        "target_type": "IMAGE",
        "folder_id": 3,
        "created_on": "2021-01-01T08:49:14.759510Z",
        "updated_on": "2021-01-01T08:49:14.759557Z",
        "transformations": []
    }


Validation failed
^^^^^^^^^^^^^^^^^

On Validation error, errors will be returned as list of strings for each field

.. code-block::

    Status: 400 Bad Request

.. code-block:: JSON

    {
        "name": [],
        "folder": [],
        "target_type": []
    }

**********************************

Retrieve
--------
.. code-block::

    GET /pipeline/{id}

Retrieve a pipeline by ID.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`id`
     - string
     - path
     - Pipeline ID

Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    {
        "id": 2,
        "name": "test",
        "is_enabled": true,
        "target_type": "IMAGE",
        "folder_id": 3,
        "created_on": "2021-01-01T08:49:14.759510Z",
        "updated_on": "2021-01-01T08:49:14.759557Z",
        "transformations": []
    }


Pipeline not found
^^^^^^^^^^^^^^^^^

.. code-block::

    Status: 404 Not Found

.. code-block:: JSON

    {
        "detail": "Not found."
    }

Pipeline belongs to another user
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    Status: 403 Forbidden

.. code-block:: JSON

    {
        "detail": "You do not have permission to perform this action."
    }

**********************************

Update
------
.. code-block::

    PUT or PATCH /pipeline/{id}

Update a Pipeline by id.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`id`
     - string
     - path
     - Pipeline ID

   * - :code:`is_enabled`
     - string
     - body
     - defined that the pipeline is enabled or not


Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    {
        "id": 2,
        "name": "test",
        "is_enabled": false,
        "target_type": "IMAGE",
        "folder_id": 3,
        "created_on": "2021-05-19T08:49:14.759510Z",
        "updated_on": "2021-05-19T08:49:14.759557Z",
        "transformations": []
    }


Validation failed
^^^^^^^^^^^^^^^^^

On Validation error, errors will be returned as list of strings for each field

.. code-block::

    Status: 400 Bad Request

.. code-block:: JSON

    {
        "is_enabled": []
    }

**********************************

Delete
------
.. code-block::

    DELETE /pipeline/{id}

Delete a Pipeline by ID.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`id`
     - string
     - path
     - Pipeline ID

Response
^^^^^^^^
.. code-block::

    Status: 204 No Content
