#! /usr/bin/python

from __future__ import print_function
import sys
from json import loads, dumps, load, dump
import nacl.utils
import nacl.public
import nacl.encoding
import nacl.secret
import nacl.exceptions
import os.path
import argparse # python 2.7 & later
import zlib

__doc__ = "See https://github.com/userify/ucrypt"

def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

class CryptoBox:

    def __init__(self, hexkey):
        # set up secretbox and decrypt
        self.secretbox = nacl.secret.SecretBox(hexkey,
                encoder=nacl.encoding.HexEncoder)

    def decrypt(self, data=""):
        try:
            decrypted = self.secretbox.decrypt(data)
        except nacl.exceptions.CryptoError, e:
            die(e.message)
        try:
            return loads(decrypted)
        except ValueError:
            return decrypted
        except:
            raise

    def encrypt(self, data=""):
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        return self.secretbox.encrypt(data, nonce)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Decrypt/Encrypt userify files.",
        epilog="Data will be read from STDIN and output to STDOUT.\n" +
        "If no key is provided, one will be read from base_config.\n" +
        "(base_config file location defaults to /opt/userify-server/base_config.cfg.)")
    parser.add_argument("-i", "--infile", help="input_file or - for STDIN", action="store")
    parser.add_argument("-o", "--outfile", help="output_file or - for STDOUT", action="store")
    parser.add_argument("--keygen", help="generate an encryption key.", action="store_true")
    parser.add_argument("--key", help="provide encryption/decryption key.", action="store")
    parser.add_argument("--base_config", help="provide path to base_config.cfg.", action="store")
    args = parser.parse_args()

    if args.base_config:
        bc_fn = args.base_config
    else:
        bc_fn = "/opt/userify-server/base_config.cfg"

    if args.keygen:
        # generate secretkey
        hexkey = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        secretbox = nacl.secret.SecretBox(hexkey)
        print(secretbox.encode(encoder=nacl.encoding.HexEncoder))
        sys.exit(0)

    hexkey = args.key
    if not hexkey:
        if os.path.isfile(bc_fn):
            base_config = load(open(bc_fn))
            hexkey = base_config["crypto_key"]
        else:
            die(bc_fn + " does not exist and no key was provided.\n" +
                "Do you need to generate a key? Try:\n\n   %s --help" % sys.argv[0])
            sys.exit(1)

    cryptbox = CryptoBox(hexkey)

    if not args.infile or args.infile.strip() == "-":
	inobj = sys.stdin
    else:
        inobj = open(args.infile)
    indata = inobj.read().strip()

    if not args.outfile or args.outfile.strip() == "-":
	outobj = sys.stdout
    else:
        outobj = open(args.outfile, "w")

    if indata.startswith("X25519:"):
        indata = indata[len("X25519:"):]
        decrypted = cryptbox.decrypt(indata)
        decrypted = cryptbox.decrypt(indata)
        if not decrypted:
            outobj.write("")
            sys.exit(0)
        decrypted = zlib.decompress(decrypted)
        if decrypted.lstrip().startswith("{"):
            try:
                dump(outobj, decrypted, sort_keys=True,
                    ensure_ascii=True,
                    indent=2,
                    separators=(',', ': '))
            except:
                outobj.write(decrypted)
        else:
            outobj.write(decrypted)
    else:
        outobj.write("X25519:" + cryptbox.encrypt(zlib.compress(indata)))
