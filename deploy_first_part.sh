#! /bin/bash

PORT=21003
MACHINE=paffenroth-23.dyn.wpi.edu
STUDENT_ADMIN_KEY_PATH=../../scripts/

# Clean up from previous runs
ssh-keygen -f "/home/rcpaffenroth/.ssh/known_hosts" -R "[paffenroth-23.dyn.wpi.edu]:21003"
rm -rf tmp

# Create a temporary directory
mkdir tmp

# copy the key to the temporary directory
cp ${STUDENT_ADMIN_KEY_PATH}/student-admin_key* tmp

# Change to the temporary directory
cd tmp

# Set the permissions of the key
chmod 600 student-admin_key*

# Create a unique key
rm -f mykey*
ssh-keygen -f mykey -t ed25519 -N "careful"

# Insert the key into the authorized_keys file on the server
# One > creates
cat mykey.pub > authorized_keys
# two >> appends
# Remove to lock down machine
#cat student-admin_key.pub >> authorized_keys

chmod 600 authorized_keys

echo "checking that the authorized_keys file is correct"
ls -l authorized_keys
cat authorized_keys

# Copy the authorized_keys file to the server
scp -i student-admin_key -P ${PORT} -o StrictHostKeyChecking=no authorized_keys student-admin@${MACHINE}:~/.ssh/

# Add the key to the ssh-agent
eval "$(ssh-agent -s)"
ssh-add mykey

# Check the key file on the server
echo "checking that the authorized_keys file is correct"
ssh -p ${PORT} -o StrictHostKeyChecking=no student-admin@${MACHINE} "cat ~/.ssh/authorized_keys"

# clone the repo
git clone https://github.com/rcpaffenroth/CS553_example

# Copy the files to the server
scp -P ${PORT} -o StrictHostKeyChecking=no -r CS553_example student-admin@${MACHINE}:~/

# check that the code in installed and start up the product
# COMMAND="ssh -p ${PORT} -o StrictHostKeyChecking=no student-admin@${MACHINE}"

# ${COMMAND} "ls CS553_example"
# ${COMMAND} "sudo apt install -qq -y python3-venv"
# ${COMMAND} "cd CS553_example && python3 -m venv venv"
# ${COMMAND} "cd CS553_example && source venv/bin/activate && pip install -r requirements.txt"
# ${COMMAND} "nohup CS553_example/venv/bin/python3 CS553_example/app.py > log.txt 2>&1 &"

# nohup ./whatever > /dev/null 2>&1 

# debugging ideas
# sudo apt-get install gh
# gh auth login
# requests.exceptions.HTTPError: 429 Client Error: Too Many Requests for url: https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta/v1/chat/completions
# log.txt
