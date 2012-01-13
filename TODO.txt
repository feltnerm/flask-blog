TODO
====
__in order of *priority*__

CHECK OUT https://github.com/laoqiu/pypress
specifically helpers.py and markdown support


Database
-------
- Set up a persistent database for testing and development purposes.
- Create / teardown test database
- Backup/dump database

Templates
---------
- Whiteboard a template inheritance structure:
  layout.html (Pieces that are on ALL pages)
  |
  ----> base.html (Pieces specific to the layout of a certain blueprint)
        |
        ---------> new.html (An agnostic piece)
                   edit.html
                   ...

- Form autofill (edit.html)
- Keep creating and testing
- CSS/Style
- Javascript/Ajax

Forms
-----
- Form autofill (edit.html)
- Validation
-- Ensure unique slug title is generated or forced

Views
-----
- API that returns JSON
- Archives view
- Pagination on blog Entries

Configuration
-------------
- Compartmentalize generate_app()

Logging
-------
- Set up logbook

Email
------
- Email on new entry?

Error Handling
--------------
- Exception catching
- 403, 404, etc...configure error pages/conditions

Fabfile
-------
- pychecker
- pep8
- tabnanny
- determine method to push to server