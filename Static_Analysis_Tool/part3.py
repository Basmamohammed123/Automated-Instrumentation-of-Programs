from os import urandom
from base64 import b64encode
import string


def generate_salts(count=16, length=16):
    salts = set()
    characters = string.ascii_lowercase + string.digits
    
    while len(salts) < count:
        salt = ''.join(characters[b % len(characters)] for b in urandom(length))
        salts.add(salt)
    
    return list(salts)

# Generate salts
salts = generate_salts()

# Save to file
with open("part3.txt", "w") as f:
    for salt in salts:
        f.write(salt + "\n")

# Print salts
for salt in salts:
    print(salt)
