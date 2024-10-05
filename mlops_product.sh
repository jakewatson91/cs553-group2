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
mlopshost=paffenroth-23.dyn.wpi.edu
mlopsport=22002
mlopsadmin=student-admin
#mlopsadminkey=~/.ssh/${mlopsadmin}_key
mlopspers=andrew
mlopsperskey=~/.ssh/${mlopspers}
MLOPSPRODUCT=cs553-group2
githubuser=1keane
githubpasswd=`cat ~/.p-github-WPI-admin`

echo; echo "`date` - Starting..."

#-- Setup up path for GitHub clone
mkdir -p ~/git
cd ~/git
rm -rf $MLOPSPRODUCT

#-- Clone the GitHub Repo with Group 2 Product
echo ; echo "Cloning GitHub repo - $MLOPSPRODUCT"
git clone https://$githubuser:$githubpasswd@github.com/jakewatson91/$MLOPSPRODUCT

#-- Copy the product files to the server
echo ; echo "Copying proudct code to server"
scp -p -i $mlopsperskey -P $mlopsport -r $MLOPSPRODUCT $mlopsadmin@$mlopshost:

# check that the code in installed and start up the product
SSHCMD="ssh -i $MLOPSADMINKEY -p $MLOPSPORT $MLOPSADMIN@$MLOPSHOST"
#COMMAND="ssh -p ${PORT} -o StrictHostKeyChecking=no student-admin@${MACHINE}"
$SSHCMD "ls cs553-group2"

exit

# $SSHCMD "sudo apt install -qq -y python3-venv"
# $SSHCMD "cd cs553-group2 && python3 -m venv venv"
# $SSHCMD "cd cs553-group2 && source venv/bin/activate && pip install -r requirements.txt"
# $SSHCMD "nohup cs553-group2/venv/bin/python3 cs553-group2/app.py > log.txt 2>&1 &"

# nohup ./whatever > /dev/null 2>&1 

# debugging ideas
# sudo apt-get install gh
# gh auth login
# requests.exceptions.HTTPError: 429 Client Error: Too Many Requests for url: https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta/v1/chat/completions
# log.txt

