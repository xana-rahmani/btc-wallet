from wallet import HDWallet


hex_seed = 'e05bdbefccf74e6cd7d2f6cceecc9bde2d156a18b93b3c0a4d5ef1032c8ad69d60c085fe9ddc8d788f1ecc65773e799c2f286880e66b6c4615c0234d08e87f92'
hd_wallet = HDWallet(hex_seed)
print('x-prv: {}'.format(hd_wallet.get_extend_private_key()))
print('x-pub: {}'.format(hd_wallet.get_extend_public_key()))
print('chain code: {}\n'.format(hd_wallet.get_chain_code()))

hd_wallet.Normal_Child__extended_private_key(index=3)
