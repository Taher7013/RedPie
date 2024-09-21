#import hashlib
#
#def crack_password(hash_to_crack, wordlist_path):
#    with open(wordlist_path, "r") as wordlist:
#        for password in wordlist:
#            password = password.strip()
#            hashed_password = hashlib.md5(password.encode()).hexdigest()
#            if hashed_password == hash_to_crack:
#                print(f"Password found: {password}")
#                return
#                print("Password not found in wordlist")