Django and Dropbox API seed project
===================================

This is a seed project I created while getting started with django and dropbox API. Feel free to use it, fork it and extend it.

HTH :)

Installation
------------

1. You'll need a Dropbox API account of course.
2. For testing add: ```http://localhost:8000/dropbox_auth_finish/``` to your OAuth redirect URIs at the dropbox developer admin for your app.
3. Fill in your dropbox API keys in the ```settings.py``` under ```DROPBOX_SETTINGS```.
4. Install dropbox sdk for python: ```pip install dropbox```.

Run
---

1. first ````python manage.py syncdb```
2. then ````python manage.py runserver```
