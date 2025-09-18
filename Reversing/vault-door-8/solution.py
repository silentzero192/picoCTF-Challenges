#!/usr/bin/env python3
# solve_vault8.py
expected = [
    0xF4, 0xC0, 0x97, 0xF0, 0x77, 0x97, 0xC0, 0xE4,
    0xF0, 0x77, 0xA4, 0xD0, 0xC5, 0x77, 0xF4, 0x86,
    0xD0, 0xA5, 0x45, 0x96, 0x27, 0xB5, 0x77, 0xD2,
    0xD0, 0xB4, 0xE1, 0xC1, 0xE0, 0xD0, 0xD0, 0xE0
]

def switch_bits(byte, p1, p2):
    """
    Swap the bit at p1 with the bit at p2 in the 0..7 bit positions of byte.
    p1 < p2 assumed.
    """
    mask1 = 1 << p1
    mask2 = 1 << p2
    bit1 = byte & mask1
    bit2 = byte & mask2
    rest = byte & ~(mask1 | mask2)
    shift = p2 - p1
    # move bit1 up by shift and bit2 down by shift
    result = ((bit1 << shift) | (bit2 >> shift) | rest) & 0xFF
    return result

# reverse operation sequence (reverse of the scramble's order)
reverse_ops = [(6,7), (2,5), (3,4), (0,1), (4,7), (5,6), (0,3), (1,2)]

recovered_bytes = []
for v in expected:
    x = v
    for p1, p2 in reverse_ops:
        x = switch_bits(x, p1, p2)
    recovered_bytes.append(x)

password = bytes(recovered_bytes).decode('ascii')  # ASCII printable expected
print("Flag : picoCTF{" + password + "}")
