Transformation
==============

These endpoints can be used to perform operations on :code:`Transformation` objects.


Create
------
.. code-block::

    POST /transformation

Creates a Transformation.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`pipeline`
     - string
     - body
     - Pipeline ID

   * - :code:`extra_data`
     - JSON
     - body
     - JSON of transformation config

   * - :code:`type`
     - string
     - body
     - Target file types ('COMPRESS', 'CHECKSUM', 'IMAGE_COMPRESS', 'IMAGE_CLASSIFY', 'RESIZE', 'ADJUST')


Response
^^^^^^^^
.. code-block::

    Status: 201 Created

.. code-block:: JSON

    {
        "id": 4,
        "type": "IMAGE_CLASSIFY",
        "extra_data": {},
        "created_on": "2021-01-01T09:07:09.308652Z",
        "updated_on": "2021-01-01T09:07:09.309219Z"
    }


Validation failed
^^^^^^^^^^^^^^^^^

On Validation error, errors will be returned as list of strings for each field

.. code-block::

    Status: 400 Bad Request

.. code-block:: JSON

    {
        "extra_data": [],
        "pipeline": [],
        "type": []
    }

**********************************

Retrieve
--------
.. code-block::

    GET /transformation/{id}

Retrieve a transformation by ID.

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
     - Transformation ID

Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    {
        "id": 4,
        "type": "IMAGE_CLASSIFY",
        "extra_data": {},
        "created_on": "2021-01-01T09:07:09.308652Z",
        "updated_on": "2021-01-01T09:07:09.309219Z"
    }


Transformation not found
^^^^^^^^^^^^^^^^^

.. code-block::

    Status: 404 Not Found

.. code-block:: JSON

    {
        "detail": "Not found."
    }

Transformation belongs to another user
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

    PUT or PATCH /transformation/{id}

Update a Transformation by id.

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
     - Transformation ID

   * - :code:`extra_data`
     - JSON
     - body
     - JSON of transformation config


Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    {
        "id": 4,
        "type": "IMAGE_CLASSIFY",
        "extra_data": {},
        "created_on": "2021-01-01T09:07:09.308652Z",
        "updated_on": "2021-01-01T09:07:09.309219Z"
    }


Validation failed
^^^^^^^^^^^^^^^^^

On Validation error, errors will be returned as list of strings for each field

.. code-block::

    Status: 400 Bad Request

.. code-block:: JSON

    {
        "extra_data": []
    }

**********************************

Delete
------
.. code-block::

    DELETE /transformation/{id}

Delete a Transformation by ID.

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
     - Transformation ID

Response
^^^^^^^^
.. code-block::

    Status: 204 No Content
