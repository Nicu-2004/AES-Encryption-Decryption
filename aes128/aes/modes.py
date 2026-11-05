from .core import encrypt_block, decrypt_block
from .utils import pad, unpad, split_blocks

def encrypt(key, plaintext):
    out = b""
    for block in split_blocks(pad(plaintext)):
        out += encrypt_block(key, block)
    return out

def decrypt(key, ciphertext):
    out = b""
    for block in split_blocks(ciphertext):
        out += decrypt_block(key, block)
    return unpad(out)