from btc.bitcoin import (public_key_to_p2pkh, public_key_to_p2wpkh, public_key_to_p2wpkh_p2sh)
from bitcoin.core import x
from bitcoin.wallet import CBitcoinSecret
from btc import constants
import hmac
import hashlib


Secp256k1_order = 'fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141'
"""
        + https://en.bitcoin.it/wiki/Secp256k1
        + order n of G and the cofactor are:
            FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141
"""


class Wallet:
    def __init__(self, private_key, network=None):
        self.private_key = private_key
        self.public_key = CBitcoinSecret.from_secret_bytes(x(private_key)).pub.hex()
        if network is None:
            constants.set_mainnet()
            self.network = constants.net
        else:
            self.network = network

    def public_key_to_address(self, txin_type: str):
        if txin_type == 'p2pkh':
            return public_key_to_p2pkh(public_key=self.public_key, net=self.network)
        elif txin_type == 'p2wpkh':
            return public_key_to_p2wpkh(public_key=self.public_key, net=self.network)
        elif txin_type == 'p2wpkh-p2sh':
            return public_key_to_p2wpkh_p2sh(public_key=self.public_key, net=self.network)
        else:
            raise NotImplementedError(txin_type)


# TODO:  Serialization
class HDWallet:
    def __init__(self, seed: hex):
        """
            Extended Keys: Private keys and public keys that you can derive children from.
            learn about Extend Key: https://learnmeabitcoin.com/technical/extended-keys
        """
        self.seed = bytes.fromhex(seed)
        self.key = b'Bitcoin seed'

        # extend_private_key (x_prv) length is 128 chr in hex :>> 128 * 4 = 512 :>> 512 / 8 == 64 byte.
        #   the first 32 bytes (64 hex) is the private key.
        #   the last  32 bytes (64 hex) is the chain code.
        self.x_prv = hmac.new(key=self.key, msg=self.seed, digestmod=hashlib.sha512).hexdigest()
        private_key, chain_code = self.x_prv[:64], self.x_prv[64:]
        public_key = CBitcoinSecret.from_secret_bytes(x(private_key)).pub.hex()
        self.x_pub = public_key + chain_code
        # The chain code is just an extra 32 bytes that we couple with the private
        # key to create what we call an extended key.
        self.chain_code = chain_code

    def get_extend_private_key(self):
        return self.x_prv

    def get_chain_code(self):
        return self.chain_code

    def get_extend_public_key(self):
        return self.x_pub

    def Normal_Child__extended_private_key(self, index):
        """
            Use an index between 0 and 2147483647.
            https://learnmeabitcoin.com/technical/hd-wallets
        """

        parent_private_key = self.x_prv[:64]
        len_parent_public_key = len(self.x_pub) - len(self.chain_code)
        parent_public_key = self.x_pub[:len_parent_public_key]
        parent_chain_code = self.chain_code

        for i in range(index):
            # TODO: '4' to change index > 2**8 to byte is correctly ??
            data = bytes.fromhex(parent_public_key) + i.to_bytes(4, byteorder='big')
            key = bytes.fromhex(parent_chain_code)
            hmac_hash = hmac.new(key=key, msg=data, digestmod=hashlib.sha512).hexdigest()
            left_32bit = hmac_hash[:64]  # 64 hex >> 32 bit
            child_chain_code = hmac_hash[64:]

            int_child_private_key = (int(parent_private_key, 16) + int(left_32bit, 16)) % int(Secp256k1_order, 16)
            child_private_key = hex(int_child_private_key)[2:]
            child_public_key = CBitcoinSecret.from_secret_bytes(x(child_private_key)).pub.hex()

            print(" #{}".format(i))
            print("\tchild_private_key: {}".format(child_private_key))
            print("\tchild_public_key : {}".format(child_public_key))
            print("\tchild_chain_code : {}".format(child_chain_code))

    # TODO
    def Hardened_Child__extended_private_key(self, index):
        """
            Use an index between 2147483647 and 4294967295.
            Indexes in this range are designated for hardened child extended keys.
        """
        pass

    # TODO
    def Normal_Child__extended_public_key(self, index):
        """
        Use an index between 0 and 2147483647. Indexes in this range are designated for normal child extended keys.
        """
        pass

    def Hardened_Child_extended_public_key(self, index):
        """
            Not possible.
        """
        pass

