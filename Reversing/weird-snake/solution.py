input_list = [
    4,
    54,
    41,
    0,
    112,
    32,
    25,
    49,
    33,
    3,
    0,
    0,
    57,
    32,
    108,
    23,
    48,
    4,
    9,
    70,
    7,
    110,
    36,
    8,
    108,
    7,
    49,
    10,
    4,
    86,
    43,
    105,
    114,
    91,
    0,
    71,
    106,
    124,
    93,
    78,
]


def decryption(key_str):
    key_list = [ord(c) for c in key_str]

    # extend key to match length
    while len(key_list) < len(input_list):
        key_list.extend(key_list)

    # xor decode
    result = [a ^ b for a, b in zip(input_list, key_list)]
    flag = "".join(map(chr, result))

    return flag


# key_str = "tJo_3"
# print(decryption(key_str))
# ouput = p|F_CTS^~0tJV_czkVus$KW_s{e[e_#33 }
# It prints just the gibbrish characters, as we know intials of flag which are
# 'picoCT{' we will me xor this with ciphertext which gives us the key.

# key_str = "picoCTF{"
# print(decryption(key_str))
# output = t_Jo3t_JQjcozt*l@mj)D:bsnReGm2c()(
# So, our key will be 't_Jo3'

key_str = "t_Jo3"
print(decryption(key_str))
# This gives us the final flag.