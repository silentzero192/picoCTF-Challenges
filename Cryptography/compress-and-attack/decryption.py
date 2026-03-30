from pwn import *
import string

sh = remote("wily-courier.picoctf.net", 59646)
charset = string.ascii_letters + "_{}"

def oracle(text):
    sh.recvuntil(b"encrypted:")
    sh.sendline(text.encode())
    sh.recvline()
    sh.recvline()
    return int(sh.recvline().decode())


known = "picoCTF{"

length = oracle(known)
# print(known, end="")

current = ""
while current != "}":
    for c in charset:
        oracle_length = oracle(known + c)
        print(f"Trying {known}{c} -> {oracle_length}")
        if oracle_length == length:
            known += c
            print(f"[+] Found so far: {known}\n")
            current = c
            print(c, end="")
            break
