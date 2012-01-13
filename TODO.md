TODO  
====

__in order of *priority*__

Inspiration:  
[Flask-Boilerplate](https://github.com/swaroopch/flask-boilerplate)  
[PyPress](https://github.com/laoqiu/pypress). Specifically: helpers.py and markdown support

Error Handling
--------------

* Exception catching
* 403, 404, etc...configure error pages/conditions

Logging
---------

* Set up logbook

Forms
-----

* Form autofill (edit.html)
* Validation
** Ensure unique slug title is generated or forced

Templates
---------

* Whiteboard a template inheritance structure:

<pre>
layout.html (Pieces that are on ALL pages)
|
----> base.html (Pieces specific to the layout of a certain blueprint)
      |
      ---------> new.html (An agnostic piece)
                 edit.html
                 ...
</pre>
* Form autofill (edit.html)
* Keep creating and testing
* CSS/Style
* Javascript/Ajax

Database
-------
* Set up a persistent database for testing and development purposes.
* Create / teardown test database
* Backup/dump database

Views
-----
* API that returns JSON
* Archives view
* Pagination on blog Entries

Configuration
-------------
* Compartmentalize generate_app()

Email
------
* Email on new entry?

Fabfile
-------
* pychecker
* pep8
* tabnanny
* determine method to push to server