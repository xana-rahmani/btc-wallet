from btc import seqwit_addr, constants, script
from btc.crypto import sha256, hash_160, base_58_encode

bfh = bytes.fromhex

def pubkey_to_address(txin_type: str, pubkey: str, *, net=None) -> str:
    if net is None:
        net = constants.net
    if txin_type == 'p2pkh':
        return public_key_to_p2pkh(bfh(pubkey), net=net)
    elif txin_type == 'p2wpkh':
        return public_key_to_p2wpkh(bfh(pubkey), net=net)
    elif txin_type == 'p2wpkh-p2sh':
        return public_key_to_p2wpkh_p2sh(bfh(pubkey), net=net)
    else:
        raise NotImplementedError(txin_type)


def public_key_to_p2pkh(public_key: str, net=None) -> str:
    """
    P2PKH:  Pay to Public Key Hash: https://learnmeabitcoin.com/technical/address
            begin with the number '1' for minnet
                                  'm / n' for testnet

        How does P2PKH work?
            https://learnmeabitcoin.com/technical/p2pkh
   """
    if net is None:
        net = constants.net
    h160 = hash_160(bfh(public_key))

    # Adding the Network Byte
    s = bytes([net.ADDRTYPE_P2PKH]) + h160

    # Checksum
    checksum = sha256(sha256(s))[0:4]
    s = s + checksum

    # Hash160 to Base58 Address
    address = base_58_encode(s)
    return address


def public_key_to_p2wpkh(public_key: str, net=None) -> str:
    """
    BECH32: is a segwit address format specified by BIP 0173
            begin with the number 'bc1' for mainnet
                                  'tb1' for testnet
            standardised in BIP 16: https://en.bitcoin.it/wiki/BIP_0016
                                    https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki

        How does P2SH work?
                https://learnmeabitcoin.com/technical/p2sh
    """
    if net is None:
        net = constants.net
    h160 = hash_160(bfh(public_key))
    address = seqwit_addr.encode(hrp=net.SEGWIT_HRP, witver=0, witprog=h160)
    return address


def public_key_to_p2wpkh_p2sh(public_key: str, net=None) -> str:
    if net is None:
        net = constants.net
    h160 = hash_160(bfh(public_key))
    scriptSig = script.construct_script([0, h160])

    scriptSig_hash_160 = hash_160(bfh(scriptSig))

    # Adding the Network Byte
    s = bytes([net.ADDRTYPE_P2SH]) + scriptSig_hash_160

    # Checksum
    checksum = sha256(sha256(s))[0:4]
    s = s + checksum

    # Hash160 to Base58 Address
    address = base_58_encode(s)
    return address


def p2sh():
    """
    P2SH:  Pay to Script Hash: https://learnmeabitcoin.com/technical/address
            begin with the number '3' for mainnet
                                  '2' for testnet
            standardised in BIP 16: https://en.bitcoin.it/wiki/BIP_0016
                                    https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki

    How does P2SH work?
            https://learnmeabitcoin.com/technical/p2sh
    """
    pass
