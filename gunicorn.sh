
if ps ax | grep -v grep | grep gunicorn > /dev/null
then
    echo "Stopping gunicorn workers..."
    killall gunicorn
fi
echo "Starting gunicorn workers..."
gunicorn -c gunicorn.conf --access-logfile log/gunicorn.access.log --log-file log/gunicorn.log -D app:app 
echo "gunicorns are flying!"
