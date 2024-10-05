#!/bin/bash

#--
#-- CS/DS 553 MLOps
#--
#-- Install and start the product
#--    Extract from GitHub
#--    Copy to VM
#--    Create virtual environment
#--    Add required dependencies
#--

#-- Initialize
MLOPSHOST=paffenroth-23.dyn.wpi.edu
MLOPSPORT=22002
MLOPSADMIN=student-admin
#MLOPSADMINKEY=~/.ssh/${MLOPSADMIN}_key
MLOPSPERS=andrew
MLOPSPERSKEY=~/.ssh/${MLOPSPERS}
MLOPSPRODUCT=cs553-group2

echo; echo "`date` - Starting..."

#-- Setup up path for GitHub clone
mkdir -p ~/git
cd ~/git
rm -rf $MLOPSPRODUCT

#-- Clone the GitHub Repo with Group 2 Product
echo ; echo "`date` - Cloning GitHub repo - $MLOPSPRODUCT"
git clone git@github.com:jakewatson91/cs553-group2

#-- Copy the product files to the server
echo ; echo "`date` - Copying proudct code to server"
scp -p -i $MLOPSPERSKEY -P $MLOPSPORT -r $MLOPSPRODUCT $MLOPSADMIN@$MLOPSHOST:

#-- check that the code in installed and start up the product
echo ; echo "`date` - Verifying product exists on server"
SSHCMD="ssh -i $MLOPSPERSKEY -p $MLOPSPORT $MLOPSADMIN@$MLOPSHOST"
$SSHCMD "ls -lad cs553-group2"

#-- Install the Python virtual environment application
echo ; echo "`date` - Installing Pything virtual environment application"
$SSHCMD "sudo apt install -qq -y python3-venv"

#-- Create and activate the Python virtual environment
echo ; echo "`date` - Create and activate the Python virtual environment, install required packages"
$SSHCMD "cd cs553-group2 && python3 -m venv venv"
$SSHCMD "cd cs553-group2 && source venv/bin/activate && pip install -r requirements.txt"

#-- Start the product and use nohup to keep up even if terminal windows close
echo ; echo "`date` - Start the product"
# $SSHCMD "nohup cs553-group2/venv/bin/python3 CS553_example/app.py > log.txt 2>&1 &"


# debugging ideas
# sudo apt-get install gh
# requests.exceptions.HTTPError: 429 Client Error: Too Many Requests for url: https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta/v1/chat/completions
