ints = [
    1096770097,
    1952395366,
    1600270708,
    1601398833,
    1716808014,
    1734293296,
    842413104,
    1684157793,
]
bytes_out = b"".join(
    ((x >> shift) & 0xFF).to_bytes(1, "big") for x in ints for shift in (24, 16, 8, 0)
)
print(bytes_out.decode("latin1")) 
