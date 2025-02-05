import hashlib
import random
import string

def generate_hash(target_prefix, student_number):
    while True:
        password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))  # Random length
        salt = str(student_number)
        value = password + salt
        hash_value = hashlib.sha256(value.encode()).hexdigest()
        
        if hash_value.startswith(target_prefix):
            return password, salt, hash_value

student_number = "101187310"
target_prefix = "c0ffee10"  # "c0ffee" + last two digits of student number "10"

password, salt, hash_value = generate_hash(target_prefix, student_number)

print(f"Password: {password}")
print(f"Salt: {salt}")
print(f"SHA256 Hash: {hash_value}")

# Save password to part1.txt
with open("part1.txt", "w") as f:
    f.write(password)
    
