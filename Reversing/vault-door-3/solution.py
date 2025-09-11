target = "jU5t_a_sna_3lpm12g94c_u_4_m7ra41"
password = ["?"] * 32

# Loop 1: first 8 same
for i in range(0, 8):
    password[i] = target[i]

# Loop 2: reversed block
for i in range(8, 16):
    password[23 - i] = target[i]

# Loop 3: even indices reversed
for i in range(16, 32, 2):
    password[46 - i] = target[i]

# Loop 4: odds same
for i in range(17, 32, 2):
    password[i] = target[i]

flag = "picoCTF{" + "".join(password) + "}"
print(flag)
