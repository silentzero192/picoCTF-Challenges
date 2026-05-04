import hashlib

def str_xor(secret, key):
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key += key[i]
        i = (i + 1) % len(key)
    return "".join(chr(ord(s) ^ ord(k)) for s, k in zip(secret, new_key))

def hash_pw(pw_str):
    return hashlib.md5(pw_str.encode()).digest()

# Read encrypted flag and correct hash
flag_enc = open("level5.flag.txt.enc", "rb").read()
correct_pw_hash = open("level5.hash.bin", "rb").read()

# Open dictionary file
with open("dictionary.txt", "r") as f:
    for line in f:
        pw = line.strip()          # VERY IMPORTANT
        if not pw:
            continue

        if hash_pw(pw) == correct_pw_hash:
            print("[+] Password found:", pw)
            flag = str_xor(flag_enc.decode(), pw)
            print("[+] FLAG:", flag)
            break
    else:
        print("[-] No password matched")
