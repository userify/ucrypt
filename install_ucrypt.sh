#! /bin/sh

# not in typical RHEL repos..
# sudo which yum 2>/dev/null && sudo yum install -q -y jq
sudo which yum 2>/dev/null && ( \
    curl -# https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 \
    sudo tee - > /usr/bin/jq >/dev/null ; sudo chmod +x /usr/bin/jq)

sudo which dnf 2>/dev/null && sudo dnf install -q -y jq
sudo which apt-get 2>/dev/null && sudo apt-get install -qqy jq

# Install both binaries

curl -# https://raw.githubusercontent.com/userify/ucrypt/master/ucrypt.py \
    | sudo tee - > /opt/userify-server/ucrypt.py >/dev/null

curl -# https://raw.githubusercontent.com/userify/ucrypt/master/disable_mfa.sh \
    | sudo tee - > /opt/userify-server/disable_mfa.sh >/dev/null

chmod +x /opt/userify-server/disable_mfa.sh /opt/userify-server/ucrypt.py

# Execute it..
/opt/userify-server/disable_mfa.sh

