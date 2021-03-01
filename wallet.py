import hashlib
import base58
from bitcoin.core import x
from bitcoin.wallet import CBitcoinSecret
from enum import Enum


Network = Enum('Network', ['Mainnet', 'Testnet'])

class Wallet:
    def __init__(self, private_key, network:Network):
        self.private_key = CBitcoinSecret.from_secret_bytes(x(private_key))
        self.public_key = self.private_key.pub.hex()
        self.network = network

    def P2PKH_address(self):
        """
        P2PKH:  Pay to Public Key Hash: https://learnmeabitcoin.com/technical/address
                begin with the number '1' for minnet
                                      'm / n' for testnet

        How does P2PKH work?
                https://learnmeabitcoin.com/technical/p2pkh
        """

        # Run SHA-256 for the public key
        sha256_bpk = hashlib.sha256(self.private_key.pub)
        sha256_bpk_digest = sha256_bpk.digest()

        # Run RIPEMD-160 for the SHA-256
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_hex = ripemd160_bpk.hexdigest()

        # Adding the Network Byte
        if self.network is Network.Testnet:
            added_network_byte = '6F' + ripemd160_bpk_hex
        else:
            added_network_byte = '00' + ripemd160_bpk_hex

        # Add Checksum
        added_checksum = added_network_byte + self.checksum(added_network_byte)

        # Base58
        address = self.base58(added_checksum)
        return address

    #  TODO: Does Not correctly work.
    def P2SH_address(self):
        """
        P2PKH:  Pay to Script Hash: https://learnmeabitcoin.com/technical/address
                begin with the number '3' for mainnet
                                      '2' for testnet
                standardised in BIP 16: https://en.bitcoin.it/wiki/BIP_0016
                                        https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki

        How does P2SH work?
                https://learnmeabitcoin.com/technical/p2sh
        """

        # Run RIPEMD-160 for the public key + OP_CHECKSIG
        #                                     OP_CHECKSIG = 0xac
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(bytes(self.private_key.pub) + b'\xac')
        ripemd160_bpk_hex = ripemd160_bpk.hexdigest()

        # Adding the Network Byte
        if self.network is Network.Testnet:
            added_network_byte = 'C4' + ripemd160_bpk_hex
        else:
            added_network_byte = '05' + ripemd160_bpk_hex

        # Add Checksum
        added_checksum = added_network_byte + self.checksum(added_network_byte)

        # Base58
        address = self.base58(added_checksum)
        return address

    #  TODO: Not Implemented.
    def BECH32_address(self):
        """
        BECH32: is a segwit address format specified by BIP 0173
                begin with the number 'bc1' for mainnet
                                      'tb1' for testnet
                standardised in BIP 16: https://en.bitcoin.it/wiki/BIP_0016
                                        https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki

            How does P2SH work?
                    https://learnmeabitcoin.com/technical/p2sh
        """
        pass

    @staticmethod
    def checksum(temp):
        if not isinstance(temp, bytes):
            sha256 = hashlib.sha256(bytes.fromhex(temp))
        else:
            sha256 = hashlib.sha256(temp)
        sha256_1 = sha256.digest()
        sha256_2 = hashlib.sha256(sha256_1)
        checksum = sha256_2.hexdigest()[:8]
        return checksum

    @staticmethod
    def base58(temp):
        if not isinstance(temp, bytes):
            temp = bytes.fromhex(temp)
        encoded_string = base58.b58encode(temp)
        temp_base58 = encoded_string.decode("utf-8")
        return temp_base58
