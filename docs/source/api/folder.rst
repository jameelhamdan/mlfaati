Folder
======

These endpoints can be used to perform operations on :code:`Folder` objects.


Create
------
.. code-block::

    POST /folder

Creates a Folder.

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
     - Name of new folder

   * - :code:`space`
     - string
     - body
     - Space ID

   * - :code:`parent`
     - string
     - body
     - Parent Folder ID (optional)


Response
^^^^^^^^
.. code-block::

    Status: 201 Created

.. code-block:: JSON

    {
        "id": 1,
        "name": "images",
        "path": [
            "images"
        ],
        "full_path": "images/",
        "created_on": "2021-01-01T00:00:00.000000Z",
        "updated_on": "2021-01-01T00:00:00.000000Z",
        "parent": null,
        "space_id": "c8f56ffd-77ed-4095-8e68-e17c8d698816"
    }


Validation failed
^^^^^^^^^^^^^^^^^

On Validation error, errors will be returned as list of strings for each field

.. code-block::

    Status: 400 Bad Request

.. code-block:: JSON

    {
        "name": [],
        "space": [],
        "parent": []
    }

**********************************

Retrieve
--------
.. code-block::

    GET /folder/{id}

Retrieve a folder by ID.

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
     - Folder ID

Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    {
        "id": 1,
        "name": "images",
        "path": [
            "images"
        ],
        "full_path": "images/",
        "created_on": "2021-01-01T00:00:00.000000Z",
        "updated_on": "2021-01-01T00:00:00.000000Z",
        "parent": null,
        "space_id": "c8f56ffd-77ed-4095-8e68-e17c8d698816"
    }


Folder not found
^^^^^^^^^^^^^^^^^

.. code-block::

    Status: 404 Not Found

.. code-block:: JSON

    {
        "detail": "Not found."
    }

Folder belongs to another user
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

    PUT or PATCH /folder/{id}

Update a Folder by id.

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
     - Folder ID

   * - :code:`name`
     - string
     - body
     - Name of new folder


Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    {
        "id": 1,
        "name": "images",
        "path": [
            "images"
        ],
        "full_path": "images/",
        "created_on": "2021-01-01T00:00:00.000000Z",
        "updated_on": "2021-01-01T00:00:00.000000Z",
        "parent": null,
        "space_id": "c8f56ffd-77ed-4095-8e68-e17c8d698816"
    }


Validation failed
^^^^^^^^^^^^^^^^^

On Validation error, errors will be returned as list of strings for each field

.. code-block::

    Status: 400 Bad Request

.. code-block:: JSON

    {
        "name": []
    }

**********************************

Delete
------
.. code-block::

    DELETE /folder/{id}

Delete a folder by ID.

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
     - Folder ID

Response
^^^^^^^^
.. code-block::

    Status: 204 No Content
