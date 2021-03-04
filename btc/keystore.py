# from .bip32 import (convert_bip32_path_to_list_of_uint32, BIP32_PRIME,
#                     is_xpub, is_xprv, BIP32Node, normalize_bip32_derivation,
#                     convert_bip32_intpath_to_strpath, is_xkey_consistent_with_key_origin_info)
#
#
# def get_pubkey_from_xpub(self, xpub: str, sequence) -> bytes:
#     node = BIP32Node.from_xkey(xpub).subkey_at_public_derivation(sequence)
#     return node.eckey.get_public_key_bytes(compressed=True)
