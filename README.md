# Userify UCRYPT

### An encryption/compression utility for data files.

This is a command-line tool and Python library to compress and decrypt/encrypt files with NaCl and gzip.

This utility can be used in your own scripts to securely encrypt or decrypt files. It can be also used to manipulate data files stored within your Userify server and includes some demonstration scripts.

Obligatory disclaimer if you're using this on Userify data files..

## ! FOR OBVIOUS REASONS, BACKUP YOUR DATA DIRECTORY FIRST !

Additional warnings: BACKUP BACKUP! By using these tools, you take full responsibility for their use. These tools have minimal safeguards and are intended for emergency use only. We will be unable to help you if you, for example, re-encrypt files with a different or unknown key. This is deliberately *very strong* encryption and you can paint yourself into a corner if you are not careful. (Reading the data, however, is interesting and shouldn't cause any problems, but still, please backup your `/opt/userify-server/data` and `/opt/userify-server/base_config.cfg` on a regular basis.)


## INSTALLATION

    sudo pip install pynacl
    curl -# https://usrfy.io/ucrypt.py | sudo tee /usr/bin/ucrypt.py >/dev/null
    sudo chmod +x /usr/bin/ucrypt.py


## Help

    # ucrypt.py --help

    usage: ucrypt.py [-h] [-i INFILE] [-o OUTFILE] [--keygen] [--key KEY]
                     [--keyfile BASE_CONFIG]

    Decrypt/Encrypt files with NaCl.

    optional arguments:
      -h, --help            show this help message and exit
      -i INFILE, --infile INFILE
                            input_file or - for STDIN
      -o OUTFILE, --outfile OUTFILE
                            output_file or - for STDOUT
      --keygen              generate an encryption key.
      --key KEY             provide encryption/decryption key.
      --keyfile KEYFILE     provide path to keyfile

    Data will be read from STDIN and output to STDOUT. If no key is provided, one
    will be read from keyfile. (keyfile file location defaults to /opt
    /userify-server/base_config.cfg.)



## Ucrypt in your own scripts

Ucrypt both compresses (with zlib) and strongly encrypts (using libsodium) your data with secure keys. You can use this within your own programs as well. A very big thank you to the developers of libsodium, NaCl, and X25519.

Ucrypt is released under the MIT license so please feel free to use in your own programs, both commercial and personal.



## Ucrypt in your Python scripts

Example Python usage:

    >>> from ucrypt import Ucrypt
    >>> hexkey = Ucrypt().keygen()
    >>> ucrypt = Ucrypt(hexkey)
    >>> print (ucrypt.decrypt(ucrypt.encrypt("foo")))
    foo


## Ucrypt in your shell scripts

Here's how to use ucrypt in your own scripts (after copying ucrypt.py to /usr/bin)

    # first, generate a secret key
    ucrypt.py --keygen --keyfile mykey

    # encrypt something with the secret key
    echo "bar" | ucrypt.py --keyfile mykey -o /tmp/bar.ucrypt

    # decrypt that file with the same key (prints bar)
    ucrypt.py --keyfile mykey -i /tmp/bar.ucrypt


### Example usage (with Userify server)

    UNAME=chris_spears
    DATAPATH=/opt/userify-server/data/

    user_filename=$DATAPATH/$(sudo cat $DATAPATH/$UNAME:username | sudo ucrypt.py -i - -o - | jq -r .user_id):user


To see the whole user record:

    sudo ucrypt.py -i $user_filename | jq .

See disable_mfa.sh for an example use script, or, to install and execute:

    curl -# https://usrfy.io/install_ucrypt.sh | sudo -sE
    sudo /opt/userify-server/disable_mfa.sh



Copyright 2017 Userify Corporation

