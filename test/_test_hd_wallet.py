from wallet import HDWallet


hex_seed = '67f93560761e20617de26e0cb84f7234aaf373ed2e66295c3d7397e6d7ebe882ea396d5d293808b0defd7edd2babd4c091ad942e6a9351e6d075a29d4df872af'
hd_wallet = HDWallet(hex_seed)
print('x-prv: {}'.format(hd_wallet.get_extend_private_key()))
print('x-pub: {}'.format(hd_wallet.get_extend_public_key()))
print('chain code: {}'.format(hd_wallet.get_chain_code()))
print('serialization xprv: {}\n'.format(hd_wallet.serialization_xprv()))
print('serialization xpub: {}\n'.format(hd_wallet.serialization_xpub()))

hd_wallet.Normal_Child__extended_private_key(index=3)
