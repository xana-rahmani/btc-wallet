import hashlib
from typing import Union


def hash_160(x: bytes) -> bytes:
    return ripemd(sha256(x))

def sha256(x: Union[bytes, str]) -> bytes:
    x = to_bytes(x, 'utf8')
    return bytes(hashlib.sha256(x).digest())

def ripemd(x):
    try:
        md = hashlib.new('ripemd160')
        md.update(x)
        return md.digest()
    except BaseException:
        from . import ripemd
        md = ripemd.new(x)
        return md.digest()

def to_bytes(something, encoding='utf8') -> bytes:
    """
    cast string to bytes() like object, but for python2 support it's bytearray copy
    """
    if isinstance(something, bytes):
        return something
    if isinstance(something, str):
        return something.encode(encoding)
    elif isinstance(something, bytearray):
        return bytes(something)
    else:
        raise TypeError("Not a string or bytes like object")

def base_58_encode(v: bytes) -> str:
    __b58chars = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    long_value = 0
    power_of_base = 1
    for c in v[::-1]:
        # naive but slow variant:   long_value += (256**i) * c
        long_value += power_of_base * c
        power_of_base <<= 8
    result = bytearray()
    while long_value >= 58:
        div, mod = divmod(long_value, 58)
        result.append(__b58chars[mod])
        long_value = div
    result.append(__b58chars[long_value])
    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in v:
        if c == 0x00:
            nPad += 1
        else:
            break
    result.extend([__b58chars[0]] * nPad)
    result.reverse()
    return result.decode('ascii')
