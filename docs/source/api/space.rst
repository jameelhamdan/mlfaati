Space
=====

These endpoints can be used to perform operations on :code:`Space` objects.


List Spaces
------------------
.. code-block::

    GET /space

Returns all spaces for current user.

Response
^^^^^^^^
.. code-block::

    Status: 200 OK

.. code-block:: JSON

    [
        {
            "id": "cf23e365-bcd9-4e3b-82d3-7f6f479805cd",
            "name": "jameel",
            "privacy": "PUBLIC",
            "created_on": "2021-01-01T08:24:30.356106Z",
            "updated_on": "2021-05-01T08:24:30.356161Z"
        }
    ]

