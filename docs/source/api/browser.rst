File Browser
============

These endpoints can be used to browse all files and folders in a particular space.


List Space Folders
------------------
.. code-block::

    GET /browser/{space}/folders

This endpoints returns all folders in Root directory.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`space`
     - string
     - path
     - Space ID or name

   * - :code:`by`
     - string
     - query parameter
     - Specify list by space name or id, must be provided as :code:`name` or :code:`id`

Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    [
        {
            "id": 1,
            "name": "images",
            "path": [
                "images"
            ],
            "full_path": "images/",
            "created_on": "2021-01-01T00:00:00.000000Z",
            "updated_on": "2021-01-01T00:00:00.000000Z"
        }
    ]


List Space Folder's Sub Folders
-------------------------------
.. code-block::

    GET /browser/{space}/folders/{folder}

This endpoints returns all folders in specified directory.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`space`
     - string
     - path
     - Space ID or name

   * - :code:`folder`
     - string
     - path
     - Folder ID

   * - :code:`by`
     - string
     - query parameter
     - Specify list by space name or id, must be provided as :code:`name` or :code:`id`

Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    [
        {
            "id": 2,
            "name": "avatars",
            "path": [
                "images/avatars"
            ],
            "full_path": "images/avatars",
            "created_on": "2021-01-01T00:00:00.000000Z",
            "updated_on": "2021-01-01T00:00:00.000000Z"
        }
    ]

List Space Files
----------------
.. code-block::

    GET /browser/{space}/files

This endpoints returns all files in Root directory.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`space`
     - string
     - path
     - Space ID or name

   * - :code:`by`
     - string
     - query parameter
     - Specify list by space name or id, must be provided as :code:`name` or :code:`id`

Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    [
        {
            "id": "bb6c5cda-c7e4-4402-b23b-169414541052",
            "parent_id": null,
            "name": "image.png",
            "content_type": "image/png",
            "content_length": 215167,
            "metadata": {}
        }
    ]


List Space Folder's Files
-------------------------
.. code-block::

    GET /browser/{space}/files/{folder}

This endpoints returns all files in specified directory.

Parameters
^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - In
     - Description

   * - :code:`space`
     - string
     - path
     - Space ID or name

   * - :code:`folder`
     - string
     - path
     - Folder ID

   * - :code:`by`
     - string
     - query parameter
     - Specify list by space name or id, must be provided as :code:`name` or :code:`id`

Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    [
        {
            "id": "18482e22-e95d-4902-b1e6-d6ee8f7a6b89",
            "parent_id": null,
            "name": "profile.png",
            "content_type": "image/png",
            "content_length": 165167,
            "metadata": {}
        }
    ]
