from Crypto.Cipher import DES, DES3
from Crypto import Random

iv = Random.get_random_bytes(8)
key = "KEY__8__"
des1 = DES.new(key, DES.MODE_CFB, iv)
des2 = DES.new(key, DES.MODE_CFB, iv)

text = 'abcdefghijklmnop'
encrypted_text = des1.encrypt(text)
decrypted_text = des2.decrypt(encrypted_text)

print(encrypted_text, decrypted_text)