#!/bin/bash

#--
#-- CS/DS 553 MLOps
#--
#-- Poll the host/container given to our group to discover if it has been
#--    restarted/wiped
#-- If it has been restarted, update host with
#--    Users, SSH public keys, and startup scripts
#--
#-- Assumptions:
#--    1) If my personal SSH key has access, system is stable
#--    2) If system has been rebooted, that means it has been wiped
#--    3) If system has been wiped, it has been restored to the original
#--       state that it was in when presented to the class on 2024-09-16
#--       This includes:
#--       a) A user account "student-admin"
#--       b) That account has sudo permission
#--       c) A public key is stored in /home/student-admin/.ssh/authorized_keys
#--

#-- Initialize
MLOPSHOST=paffenroth-23.dyn.wpi.edu
MLOPSPORT=22002
MLOPSADMIN=student-admin 
MLOPSADMINKEY=~/.ssh/${MLOPSADMIN}_key
MLOPSPERS=andrew #--change to specific key name to run 
MLOPSPERSKEY=~/.ssh/$MLOPSPERS

echo; echo "`date` - Starting..."

#-- Try to access host using my personal SSH key
testhost=`ssh -i $MLOPSPERSKEY -p $MLOPSPORT $MLOPSHOST hostname 2> /dev/null`
testhost=`ssh -i $MLOPSPERSKEY -p $MLOPSPORT $MLOPSHOST "ls /foobar" 2> /dev/null`

#-- If access failed, my personal SSH key no longer has access
if [ "$?" != 0 ]; then

   #--
   #-- The system has been wiped/restored.
   #--

   #-- Create authorized_keys file with the group's public keys to access student-admin account
   cat << EOF > /tmp/authorized_keys
#-- Default User
`cat ~/.ssh/student-admin_key.pub`

#-- Andrew Keane
`cat ~/.ssh/andrew.pub`

#-- Jake Watson
`cat ~/.ssh/jakewatson.pub`

#-- Deep Suchak
`cat ~/.ssh/deepsuchak.pub`
EOF

   #-- Restrict permissions to user read only
   chmod 600 /tmp/authorized_keys

   #-- Put the group's public keys into default user's authorized_keys
   echo "Update the default user's authorized_keys with group's user's public keys"
   SCPCMD="scp -p -i $MLOPSADMINKEY -P $MLOPSPORT"
   $SCPCMD /tmp/authorized_keys $MLOPSADMIN@$MLOPSHOST:.ssh/authorized_keys

   #-- Loop for all users in group
   #for username in andrew jakewatson deepsuchak ; do
   for username in andrew jakewatson ; do

      echo ; echo "`date` - Working on user $username..."

      #-- Create accounts for group's users
      echo "Create account and directories"
      SSHCMD="ssh -i $MLOPSADMINKEY -p $MLOPSPORT $MLOPSADMIN@$MLOPSHOST"
      $SSHCMD "sudo adduser $username < /dev/null > /dev/null 2>&1"

      #-- Create directories for user's private SSH keys
      $SSHCMD "sudo mkdir /home/$username/.ssh"

      #-- Temporarily change owner to student admin account
      $SSHCMD "sudo chown -R student-admin:student-admin /home/$username"

      #-- Put SSH public keys in place for user's access their owh accounts
      echo "Push public key"
      $SCPCMD ~/.ssh/$username.pub $MLOPSADMIN@$MLOPSHOST:/home/$username/.ssh/authorized_keys

      #-- Restrict permission to make SSH keys usable
      $SSHCMD "sudo chmod 700 /home/$username/{,.ssh}"
      $SSHCMD "sudo chmod 600 /home/$username/.ssh/authorized_keys"

      #-- Set ownership to correct users
      $SSHCMD "sudo chown -R $username:$username /home/$username"

   done

   #-- Add Andrew (but not Jake or Deep because I don't trust them) to the sudo group
   #echo ; echo "`date` - Add group users to sudo group"
   #$SSHCMD "sudo usermod -aG sudo andrew"

fi

echo ; echo "`date` - Complete"
