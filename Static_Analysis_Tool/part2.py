import hashlib
import itertools
import string

def find_salt(password, target_hash):
    characters = string.ascii_lowercase
    for salt in itertools.product(characters, repeat=8):  # Generate all possible 8-char lowercase salts
        salt = ''.join(salt)
        hash_value = hashlib.sha256((password + salt).encode()).hexdigest()
        
        if hash_value == target_hash:
            return salt
    return None

password = "comp2108"
target_hash = "9f02b0fd48e9211a5a33ae3321b942896e4ebb0cb267fdfff53fa58cf8c56f24"

salt = find_salt(password, target_hash)

if salt:
    print(f"Found Salt: {salt}")
    with open("part2.txt", "w") as f:
        f.write(salt)
else:
    print("Salt not found")
