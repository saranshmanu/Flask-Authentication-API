from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

text = 'DATA_TO_BE_SIGNED'

random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
print(key, key.publickey())

hash = SHA256.new(text).digest()
signature = key.sign(hash, '')
print(signature)


hash = SHA256.new(text).digest()
print(key.verify(hash, signature))