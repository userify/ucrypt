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

See disable_mfa.sh for an example use script, or, to install and execute:

    curl -# https://usrfy.io/install_ucrypt.sh | sudo -sE
    sudo /opt/userify-server/disable_mfa.sh


## Help

    # ucrypt.py --help

    usage: ucrypt.py [-h] [-i INFILE] [-o OUTFILE] [--keygen] [--key KEY]
                     [--base_config BASE_CONFIG]

    Decrypt/Encrypt userify files.

    optional arguments:
      -h, --help            show this help message and exit
      -i INFILE, --infile INFILE
                            input_file or - for STDIN
      -o OUTFILE, --outfile OUTFILE
                            output_file or - for STDOUT
      --keygen              generate an encryption key.
      --key KEY             provide encryption/decryption key.
      --base_config BASE_CONFIG
                            provide path to base_config.cfg.

    Data will be read from STDIN and output to STDOUT. If no key is provided, one
    will be read from base_config. (base_config file location defaults to /opt
    /userify-server/base_config.cfg.)


## Ucrypt in your own scripts

Ucrypt both compresses (with zlib) and encrypts (using libsodium) your data with secure keys. You can use this within your own programs as well.

Here's how to use ucrypt in your own scripts (after copying ucrypt.py to /usr/bin)


    # first, generate a secret key
    keyfile=$(mktemp)
    echo {\"crypto_key\": \"$(ucrypt.py --keygen)\"} > $keyfile

    # encrypt something with the secret key
    echo "bar" | ucrypt.py --base_config $keyfile -o /tmp/bar.ucrypt

    # decrypt that file with the same key (prints bar)
    ucrypt.py --base_config $keyfile -i /tmp/bar.ucrypt


Copyright 2017 Userify Corporation

