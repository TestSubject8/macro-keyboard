#!/bin/bash
# test.sh

# manager_pidfile=/var/run/system_monitor.pid
manager_pidfile=/home/pi/.local/run/system_monitor.pid

# Add check for existence of mypidfile
if [ -f $manager_pidfile ]; then
    echo "script is already running " `cat $manager_pidfile`
    kill -9 `cat $manager_pidfile`
fi

python3 controller.py & 
controller_pid=$!

# Create a file with current PID to indicate that process is running.
echo $controller_pid > "$manager_pidfile"

wait $controller_pid

echo "Deleting pidfile"
# Ensure PID file is removed on program exit.
rm $manager_pidfile
