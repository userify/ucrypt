# Userify UCRYPT

### An encryption/compression utility for Userify data files.

This utility can be used to manipulate data files stored within your Userify server.
Install into /opt/userify-server/ or your path.

Example usage:

    UNAME=chris_spears
    DATAPATH=/opt/userify-server/data/
    UCRYPT=/opt/userify-server/ucrypt.py

    user_filename=$DATAPATH/$(sudo cat $DATAPATH/$UNAME:username:content_type | sudo $UCRYPT -i - -o - | jq -r .user_id):user


To see the whole user record:

    sudo $UCRYPT -i $user_filename | jq .


See disable_mfa.sh for an example use script.
