===============================
mapistar
===============================

.. image:: https://travis-ci.org/jgirardet/mapistar.svg?branch=master
    :target: https://travis-ci.org/jgirardet/mapistar
.. image:: https://readthedocs.org/projects/mapistar/badge/?version=latest
   :target: http://mapistar.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/jgirardet/mapistar/badge.svg
   :target: https://coveralls.io/github/jgirardet/mapistar
.. image:: https://badge.fury.io/py/mapistar.svg
   :target: https://pypi.python.org/pypi/mapistar/
   :alt: Pypi package

Api pour ma gestion d'un dossier médical sous Apistar


* License : GNU General Public License v3 
* Documentation: https://mapistar.readthedocs.org/en/latest/
* Source: https://github.com/jgirardet/mapistar

Features
--------

* TODO

Usage
-----

* TODO



.. code-block:: python

    class Customer(db.Entity):
        id = PrimaryKey(int, auto=True)
        email = Required(str)

    @db_session
    def handler(email):
        c = Customer(email=email)
        # c.id is equal to None
        # because it is not assigned by the database yet
        c.flush()
        # c is saved as a table row to the database.
        # c.id has the value now
        print(c.id)

.. note::

   When :py:func:`flush` is called, the object is saved only inside the current session.
It means it will be peristed to the database after calling :py:func:`commit` manually (not necessary in most cases) or automatically before leaving the current database session.

