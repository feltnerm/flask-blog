gunicorn -c gunicorn.conf --access-logfile log/gunicorn.access.log --log-file log/gunicorn.log -D app:app 
