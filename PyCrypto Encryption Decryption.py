# ---------------------------------------- DES and DES3 ----------------------------------------
from Crypto.Cipher import DES, DES3
from Crypto import Random

iv = Random.get_random_bytes(8)
ENCRYPTION_STANDARD = DES
# The size of the key is limited to have a size of 8 characters because of DES algorithm
ENCRYPTION_DECRYPTION_KEY = "KEY__8__" 
TOTAL_ROUNDS_OF_ENCRYPTION = 10000

def encrypt_data(total, data, standard):
    encrypted_data = data
    for i in range(0, total):
        object = standard.new(ENCRYPTION_DECRYPTION_KEY, DES.MODE_CFB, iv)
        encrypted_data = object.encrypt(encrypted_data)
    return encrypted_data

def decrypt_data(total, data, standard):
    decrypted_data = data
    for i in range(0, total):
        object = standard.new(ENCRYPTION_DECRYPTION_KEY, DES.MODE_CFB, iv)
        decrypted_data = object.decrypt(decrypted_data)
    return decrypted_data

TEXT_TO_ENCRYPT = 'abcdefghijklmnop'

encrypted_text = encrypt_data(TOTAL_ROUNDS_OF_ENCRYPTION, TEXT_TO_ENCRYPT, ENCRYPTION_STANDARD)
decrypted_text = decrypt_data(TOTAL_ROUNDS_OF_ENCRYPTION, encrypted_text, ENCRYPTION_STANDARD)
print(encrypted_text, decrypted_text)



# ---------------------------------------- ARC4 and ARC2 ----------------------------------------
from Crypto.Cipher import ARC4, ARC2

ENCRYPTION_DECRYPTION_KEY = "THIS_IS_THE_KEY_TO_THE_ENCRYPTION"
ENCRYPTION_STANDARD = ARC4

object1 = ENCRYPTION_STANDARD.new(ENCRYPTION_DECRYPTION_KEY)
object2 = ENCRYPTION_STANDARD.new(ENCRYPTION_DECRYPTION_KEY)
text = '9d5887d330674e1f960835aaaa146b00'

encrypted_text = object1.encrypt(text)
decrypted_text = object2.decrypt(encrypted_text)
print(decrypted_text)
