Kill
====

Kill endpoint allows to shutdown aucote remotely. It shouldn't be run accidentally, so you need to 
authorize yourself during request.

This endpoint requires ``service.api.password`` to be set up in configuration. Value of this key should be SHA512 hash
of password.

URL
---

.. code::

   /api/v1/kill

Request
-------

.. code::

   curl -X POST -H 'Authorization: Bearer <password>' http://localhost:1235/api/v1/kill


Response
--------

Just after getting proper request the Aucote kill itself and close connection to the requester.

For curl, the expected response is:

.. code::

   curl: (52) Empty reply from server
