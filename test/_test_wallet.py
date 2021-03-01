from bitcoin import SelectParams
from wallet import Wallet
from wallet import Network


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
    wallet = Wallet(private_key=prv_key, network=Network.Mainnet)
    print('private key: {}'.format(wallet.private_key))
    print('public key: {}'.format(wallet.public_key))
    print('\tP2PKH address: {}'.format(wallet.P2PKH_address()))
    print('\tP2SH  address: {}'.format(wallet.P2SH_address()))
    print(10*"----------")


print_network("Testnet")
SelectParams('testnet')
for t_prv_key in Testnet_private_keys:
    wallet = Wallet(private_key=t_prv_key, network=Network.Testnet)
    print('private key: {}'.format(wallet.private_key))
    print('public key: {}'.format(wallet.public_key))
    print('\tP2PKH address: {}'.format(wallet.P2PKH_address()))
    print('\tP2SH  address: {}'.format(wallet.P2SH_address()))
    print(10*"----------")
