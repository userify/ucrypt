#! /bin/bash -e

DATAPATH=/opt/userify-server/data/
UCRYPT=ucrypt.py

if [ ! -f $UCRYPT ]; then
    echo "Please:\ncp -p ucrypt.py /usr/bin/"
    exit 1
fi

echo "Please provide the username or email address to disable MFA for."
read UNAME
UNAMEFILE="$DATAPATH/$UNAME:username"

if [ ! -f "$UNAMEFILE" ]; then
    echo "$UNAMEFILE does not exist."
    exit 1
fi

user_id="$(sudo cat $UNAMEFILE | sudo $UCRYPT -i - -o - | jq -r .user_id)"
user_filename=$DATAPATH/$user_id:user
redis_keyname=user:$DATAPATH:$user_id:user::$user_id:

echo "Reviewing current MFA status for $UNAME ..."
sudo $UCRYPT -i $user_filename | jq '.mfa'

echo "Backing up $UNAME file $user_filename .."
sudo cp $user_filename $user_filename-$(date -I).backup

echo "Disabling MFA for $UNAME ..."
sudo $UCRYPT -i $user_filename | jq -r '.mfa.enabled=false' | sudo $UCRYPT -o $user_filename

echo "Wiping old version from cache ..."
redis-cli del $redis_keyname

echo "Please verify that MFA is now disabled:"
sudo $UCRYPT -i $user_filename | jq .mfa
