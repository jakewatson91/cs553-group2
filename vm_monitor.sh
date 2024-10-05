#!/bin/bash

# Configuration
PORT=22002
MACHINE=paffenroth-23.dyn.wpi.edu
CHECK_INTERVAL=60         # Time in seconds between checks
MAX_RETRIES=3             # Number of failed attempts before recovery is triggered
FAILED_ATTEMPTS=0

while true; do
    # Check if VM is reachable by pinging the machine 
    ping -c 1 $MACHINE > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "$(date): VM $MACHINE is up."
        FAILED_ATTEMPTS=0
    else
        ((FAILED_ATTEMPTS++))
        echo "$(date): VM $MACHINE is down. Attempt $FAILED_ATTEMPTS of $MAX_RETRIES."
    fi

    # Trigger recovery if maximum retries reached
    if [ $FAILED_ATTEMPTS -ge $MAX_RETRIES ]; then
        echo "$(date): Maximum retries reached. Initiating recovery process."
        # Call the recovery function or script
        ./recovery_script.sh
        FAILED_ATTEMPTS=0
    fi

    # Wait before the next check
    sleep $CHECK_INTERVAL
done
