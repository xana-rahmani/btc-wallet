from bitcoin import SelectParams
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress, CBitcoinAddress, P2WPKHBitcoinAddress
from bitcoin.core import x, Hash160, b2x
from bitcoin.core.script import CScript, OP_0, OP_CHECKSIG

"""
    
    https://bitcoinlib.readthedocs.io/en/latest
    https://github.com/petertodd/python-bitcoinlib/tree/master/examples
    
"""

Mainnet_private_keys = [
    '60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2',
]
Testnet_private_keys = [
    'a43987c75084a287b64161c1eb364e2409d33039eb2814aa96dc499b1cf07874',
]

def print_network(network):
    print("\n\t\t##############################\n \t\t\t   {}\n \t\t##############################\n".format(network))


print_network("Mainnet")
for prv_key in Mainnet_private_keys:
    private_key = CBitcoinSecret.from_secret_bytes(x(prv_key))
    public_key = private_key.pub

    P2PKH_address = P2PKHBitcoinAddress.from_pubkey(public_key)
    print('\tP2PKH  address: {}'.format(P2PKH_address))

    txin_redeemScript = CScript([public_key, OP_CHECKSIG])
    txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()
    txin_p2sh_address = CBitcoinAddress.from_scriptPubKey(txin_scriptPubKey)
    print('\tP2SH   address: {}'.format(txin_p2sh_address))

    BECH32_scriptPubKey = CScript([OP_0, Hash160(public_key)])
    BECH32_address = P2WPKHBitcoinAddress.from_scriptPubKey(BECH32_scriptPubKey)
    print('\tBECH32 address: {}'.format(BECH32_address))
    print(10 * "----------")

print_network("Testnet")
SelectParams('testnet')
for t_prv_key in Testnet_private_keys:
    t_private_key = CBitcoinSecret.from_secret_bytes(x(t_prv_key))
    t_public_key = t_private_key.pub

    P2PKH_address = P2PKHBitcoinAddress.from_pubkey(t_public_key)
    print('\tP2PKH  address: {}'.format(P2PKH_address))

    txin_redeemScript = CScript([t_public_key, OP_CHECKSIG])
    txin_scriptPubKey = txin_redeemScript.to_p2sh_scriptPubKey()
    txin_p2sh_address = CBitcoinAddress.from_scriptPubKey(txin_scriptPubKey)
    print('\tP2SH   address: {}'.format(txin_p2sh_address))

    BECH32_scriptPubKey = CScript([OP_0, Hash160(t_public_key)])
    BECH32_address = P2WPKHBitcoinAddress.from_scriptPubKey(BECH32_scriptPubKey)
    print('\tBECH32 address: {}'.format(BECH32_address))
    print(10 * "----------")
