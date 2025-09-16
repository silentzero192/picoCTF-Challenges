input_list = [
    4, 54, 41, 0, 112, 32, 25, 49, 33, 3,
    0, 0, 57, 32, 108, 23, 48, 4, 9, 70,
    7, 110, 36, 8, 108, 7, 49, 10, 4, 86,
    43, 105, 114, 91, 0, 71, 106, 124, 93, 78
]

# Build the key string step by step
key_str = "J"
key_str = key_str + "_"
key_str = key_str + "o"
key_str = key_str + "3"
key_str = "t" + key_str   # prepend 't'

# Convert key_str into a list of character ordinals
key_list = [ord(char) for char in key_str]

# Repeat key_list until it matches input_list length
while len(key_list) < len(input_list):
    key_list.extend(key_list)

# XOR each input byte with key byte
result = [a ^ b for a, b in zip(input_list, key_list)]

# Convert result back to string
result_text = "".join(map(chr, result))
