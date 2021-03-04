from wallet import Wallet
from btc import constants



Mainnet_private_keys = [
    '60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2',
]

Testnet_private_keys = [
    'a43987c75084a287b64161c1eb364e2409d33039eb2814aa96dc499b1cf07874',
]

def print_network(network):
    print("\n\t\t##############################\n \t\t\t\t   {}\n \t\t##############################\n".format(network))


print_network("Mainnet")
constants.set_mainnet()
for prv_key in Mainnet_private_keys:
    wallet = Wallet(private_key=prv_key, network=constants.net)
    print('private key: {}'.format(wallet.private_key))
    print('public  key: {}'.format(wallet.public_key))
    print('\tP2PKH  address: {}'.format(wallet.public_key_to_address(txin_type='p2pkh')))
    print('\tP2WPKH address: {}'.format(wallet.public_key_to_address(txin_type='p2wpkh')))
    print('\tP2WPKH-P2SH address: {}'.format(wallet.public_key_to_address(txin_type='p2wpkh-p2sh')))
    print(10*"----------")


print_network("Testnet")
constants.set_testnet()
for t_prv_key in Testnet_private_keys:
    wallet = Wallet(private_key=t_prv_key, network=constants.net)
    print('private key: {}'.format(wallet.private_key))
    print('public  key: {}'.format(wallet.public_key))
    print('\tP2PKH  address: {}'.format(wallet.public_key_to_address(txin_type='p2pkh')))
    print('\tP2WPKH address: {}'.format(wallet.public_key_to_address(txin_type='p2wpkh')))
    print('\tP2WPKH-P2SH address: {}'.format(wallet.public_key_to_address(txin_type='p2wpkh-p2sh')))
    print(10*"----------")
