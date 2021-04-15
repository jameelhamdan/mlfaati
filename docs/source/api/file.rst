File
====

These endpoints can be used to perform operations on :code:`File` objects.


Upload
------
.. code-block::

    PUT or POST /file or /file/upload

Uploads a file to a specific folder.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`accept`
     - string
     - body
     - Recommended to be :code:`form-data` or similar

   * - :code:`content`
     - file
     - body
     - File that needs to be uploaded

   * - :code:`space`
     - string
     - body
     - Space ID

   * - :code:`space`
     - string
     - body
     - Folder ID (optional)


Response
^^^^^^^^
.. code-block::

    Status: 201 Created

.. code-block:: JSON

    {
        "id": "79b86337-1a91-49fe-911f-461c71b038b8",
        "parent_id": null,
        "name": "image.png",
        "content_type": "image/png",
        "content_length": 353,
        "metadata": {}
    }


Validation failed
^^^^^^^^^^^^^^^^^

On Validation error, errors will be returned as list of strings for each field

.. code-block::

    Status: 400 Bad Request

.. code-block:: JSON

    {
        "content": [],
        "space": [],
        "folder": []
    }

**********************************

Retrieve
--------
.. code-block::

    GET /file/{id}

Retrieve a file by ID.

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
     - File ID

Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    {
        "id": "79b86337-1a91-49fe-911f-461c71b038b8",
        "parent_id": null,
        "name": "image.png",
        "content_type": "image/png",
        "content_length": 353,
        "metadata": {}
    }


File not found
^^^^^^^^^^^^^^

.. code-block::

    Status: 404 Not Found

.. code-block:: JSON

    {
        "detail": "Not found."
    }

File belongs to another user
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    Status: 403 Forbidden

.. code-block:: JSON

    {
        "detail": "You do not have permission to perform this action."
    }

**********************************

Delete
------
.. code-block::

    DELETE /file/{id}

Delete a file by ID.

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
     - File ID

Response
^^^^^^^^
.. code-block::

    Status: 204 No Content
