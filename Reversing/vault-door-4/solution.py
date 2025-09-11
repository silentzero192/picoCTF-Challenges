# Define the array exactly as in Java
myBytes = [
    106,
    85,
    53,
    116,
    95,
    52,
    95,
    98,
    0x55,
    0x6E,
    0x43,
    0x68,
    0x5F,
    0x30,
    0x66,
    0x5F,
    0o142,
    0o131,
    0o164,
    0o63,
    0o163,
    0o137,
    0o70,
    0o146,
    ord("4"),
    ord("a"),
    ord("6"),
    ord("c"),
    ord("b"),
    ord("f"),
    ord("3"),
    ord("b"),
]

# Convert numbers to characters and join them
result = "".join(chr(x) for x in myBytes)

print("picoCTF{" + result + "}")
