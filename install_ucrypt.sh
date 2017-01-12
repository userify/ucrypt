#! /bin/bash

# RHEL/CENTOS PREREQUISITES
function rhel_prereqs {
    echo "Installing RHEL/CENT/Amazon Prerequisites"
    # not in typical RHEL repos..
    # sudo which yum 2>/dev/null && sudo yum install -q -y jq
    sudo which yum 2>/dev/null && ( \
    # Annoying behavior of RHEL: error status if 'nothing to do'
    set +e
    sudo yum install -q -y jq python-devel libffi-devel openssl-devel libxml2-devel \
        gcc gcc-c++
    set -e
    curl -# "https://bootstrap.pypa.io/get-pip.py" | sudo /usr/bin/env python
}

# DEBIAN/UBUNTU PREREQUISITES
function debian_prereqs {
    echo "Installing Debian/Ubuntu Prerequisites"
    sudo apt-get update
    sudo apt-get -qy upgrade
    sudo apt-get install -qqy build-essential python-dev libffi-dev zlib1g-dev \
    libssl-dev 
    curl -# "https://bootstrap.pypa.io/get-pip.py" | sudo -H /usr/bin/env python
}


sudo which yum 2>/dev/null && rhel_prereqs
sudo which apt-get 2>/dev/null && debian_prereqs

sudo pip install pynacl ucrypt

# Install both binaries

mkdir -p /opt/userify-server/
curl -# https://usrfy.io/disable_mfa.sh | sudo tee /opt/userify-server/disable_mfa.sh >/dev/null
chmod +x /opt/userify-server/disable_mfa.sh
echo "Install complete. Please see documentation: https://github.com/userify/ucrypt/"
