from Crypto.Hash import SHA256, SHA224, SHA384, SHA512, SHA
from Crypto.Hash import MD2, MD4, MD5

STRING_TO_HASH = 'abc'.encode('utf-8')

# ---------------------------------------- Hashing ----------------------------------------
# Hash functions comparison
# Hash      function	Hash output size (bits)	Secure?
# MD2       128	        No
# MD4	    128	        No
# MD5	    128	        No
# SHA-1	    160	        No
# SHA-256	256	        Yes

sha = SHA.new(STRING_TO_HASH).hexdigest()
sha224 = SHA224.new(STRING_TO_HASH).hexdigest()
sha256 = SHA256.new(STRING_TO_HASH).hexdigest()
sha384 = SHA384.new(STRING_TO_HASH).hexdigest()
sha512 = SHA512.new(STRING_TO_HASH).hexdigest()

md2 = MD2.new(STRING_TO_HASH).hexdigest()
md4 = MD4.new(STRING_TO_HASH).hexdigest()
md5 = MD5.new(STRING_TO_HASH).hexdigest()

print(md2)
print(md4)
print(md5)

# function to check whether the authentication is true or false
def check_password(clear_password, password_hash):
    return SHA256.new(clear_password).hexdigest() == password_hash
