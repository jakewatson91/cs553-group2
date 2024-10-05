#!/bin/bash

# Configuration
PORT=22002
MACHINE=paffenroth-23.dyn.wpi.edu
CHECK_INTERVAL=60         # Time in seconds between checks
MAX_RETRIES=3             # Number of failed attempts before recovery is triggered
FAILED_ATTEMPTS=0

# Paths to your recovery scripts
FIRST_PART="/Users/jakewatson/Desktop/cs553/cs553-group2/case-study-1/deploy_first_part.sh"
SECOND_PART="/Users/jakewatson/Desktop/cs553/cs553-group2/case-study-1/path/to/deploy_second_part.sh"

# Function to trigger the recovery process
function recover_vm() {
    echo "$(date): Starting recovery process."

    # Execute the first part of the recovery
    if [ -f "$FIRST_PART" ]; then
        echo "$(date): Running the first part of the recovery."
        bash "$FIRST_PART"
        if [ $? -eq 0 ]; then
            echo "$(date): First part completed successfully."
        else
            echo "$(date): First part failed."
        fi
    else
        echo "$(date): First part recovery script not found!"
    fi

    # Execute the second part of the recovery
    if [ -f "$SECOND_PART" ]; then
        echo "$(date): Running the second part of the recovery."
        bash "$SECOND_PART"
        if [ $? -eq 0 ]; then
            echo "$(date): Second part completed successfully."
        else
            echo "$(date): Second part failed."
        fi
    else
        echo "$(date): Second part recovery script not found!"
    fi

    echo "$(date): Recovery process finished."
}

# Main monitoring loop
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
        recover_vm  # Run the recovery function
        FAILED_ATTEMPTS=0  # Reset the failed attempts counter after recovery
    fi

    # Wait before the next check
    sleep $CHECK_INTERVAL
done
