#! /bin/sh

# Install both binaries

curl -# https://raw.githubusercontent.com/userify/ucrypt/master/ucrypt.py \
    | sudo tee - > /opt/userify-server/ucrypt.py

curl -# https://raw.githubusercontent.com/userify/ucrypt/master/disable_mfa.sh \
    | sudo tee - > /opt/userify-server/disable_mfa.sh

chmod +x /opt/userify-server/disable_mfa.sh /opt/userify-server/ucrypt.py

# Execute it..
/opt/userify-server/disable_mfa.sh

