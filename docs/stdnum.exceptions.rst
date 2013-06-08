stdnum.exceptions
=================

.. automodule:: stdnum.exceptions
   :show-inheritance:
   :member-order: bysource
   :members:

   The exceptions are organised hierarchically in the following structure:

   ::

      ValidationError
       +-- InvalidFormat
       |    +-- InvalidLength
       +-- InvalidChecksum
       +-- InvalidComponent

   It is possible to change the exception messages by setting the `message`
   class property. This allows localisation and application-specific error
   messages.

   >>> raise InvalidFormat()
   Traceback (most recent call last):
       ...
   InvalidChecksum: The number has an invalid format.
   >>> InvalidFormat.message = 'UNKNOWN'
   >>> raise InvalidFormat()
   Traceback (most recent call last):
       ...
   InvalidChecksum: UNKNOWN
