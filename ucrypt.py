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
import os

__doc__ = "See https://github.com/userify/ucrypt"
__version__ = "1.0.3"

def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

class Ucrypt:

    """
    Example Python usage:

    >>> from ucrypt import Ucrypt
    >>> hexkey = Ucrypt().keygen()
    >>> ucrypt = Ucrypt(hexkey)
    >>> print (ucrypt.decrypt(ucrypt.encrypt("foo")))
    foo

    """

    def __init__(self, hexkey=""):
        if hexkey:
            self.secretbox = nacl.secret.SecretBox(hexkey,
                    encoder=nacl.encoding.HexEncoder)

    def keygen(self):
        hexkey = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        self.secretbox = nacl.secret.SecretBox(hexkey)
        return (self.secretbox.encode(encoder=nacl.encoding.HexEncoder))

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


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Compress and decrypt/encrypt files with NaCl and gzip.",
        epilog="\n".join(("Data will be read from STDIN and output to STDOUT.",
        "If no key is provided, one will be read from keyfile.",
        "(keyfile file location defaults to /opt/userify-server/base_config.cfg.)",
        "If both keygen and keyfile arguments are created, a keyfile will be securely created.")))
    parser.add_argument("-i", "--infile", help="input_file or - for STDIN", action="store")
    parser.add_argument("-o", "--outfile", help="output_file or - for STDOUT", action="store")
    parser.add_argument("--keygen", help="generate an encryption key.", action="store_true")
    parser.add_argument("--key", help="provide encryption/decryption key.", action="store")
    parser.add_argument("--keyfile", help="provide path to keyfile.", action="store")
    args = parser.parse_args()

    bc_fn = "/opt/userify-server/base_config.cfg"

    if args.keygen:
        hexkey = Ucrypt().keygen()
        keyfile = args.keyfile.strip()
        if keyfile and keyfile != bc_fn:
            # securely write file.
            open(keyfile, "w").close()
            uid = os.getuid()
            gid = os.getgid()
            os.chown(keyfile, uid, gid)
            os.chmod(keyfile, 0o660)
            open(keyfile, "a").write(
                '{"crypto_key": "%s"}' % hexkey)
        else:
            print(hexkey)
        sys.exit(0)

    hexkey = args.key
    if args.keyfile:
        bc_fn = args.keyfile

    if not hexkey:
        if os.path.isfile(bc_fn):
            try:
                keyfile = open(bc_fn).read()
            except Exception, e:
                parser.print_help()
                print(e)
                sys.exit(1)
            try:
                # try to parse.
                hexkey = loads(keyfile)["crypto_key"]
            except:
                # ok, just a string..
                hexkey = keyfile.strip()
        else:
            die(bc_fn + " does not exist and no key was provided.\n" +
                "Do you need to generate a key? Try:\n\n   %s --help" % sys.argv[0])
            sys.exit(1)

    cryptbox = Ucrypt(hexkey)

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

if __name__ == "__main__":
    main()
