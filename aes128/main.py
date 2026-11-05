from aes.modes import encrypt, decrypt
import base64

key = bytes.fromhex(input("key (32 hex): "))
mode = input("e/d: ")

if mode == "e":
    text = input("text: ").encode()
    ct = encrypt(key, text)
    print("hex:   ", ct.hex())
    print("base64:", base64.b64encode(ct).decode())
else:
    ct = bytes.fromhex(input("ciphertext hex: "))
    print(decrypt(key, ct).decode())