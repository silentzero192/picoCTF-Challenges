# reconstruct_flag.py
import struct

# Constants extracted from the decompiled function (64-bit values, little-endian architecture)
v3      = 0x617B2375F81EA7E1
v4_0    = 0xD269DF5B5AFC9DB9
write_at = 0xF467EDF4ED1BFED2

# Build the 23-byte array that the check() function reads.
# In the decompiled code the memory layout is: v3 (8 bytes) then v4[0] (8 bytes) then a QWORD write
# starting at (char*)v4 + 7 (i.e. at byte index 15 relative to the start of v3).
ba = bytearray(23)
ba[0:8]  = struct.pack('<Q', v3)
ba[8:16] = struct.pack('<Q', v4_0)
# write 8 bytes starting at offset 15 (8 + 7)
start = 8 + 7
data = struct.pack('<Q', write_at)
for i, b in enumerate(data):
    if start + i < len(ba):
        ba[start + i] = b

# Now emulate the exact bitwise mapping from check()
input_len = 27
# initialize per-byte bit storage; index bit 0 is LSB, bit7 is MSB
inp_bits = [[None]*8 for _ in range(input_len)]

v10 = 0
v11 = 0
for i in range(0x17):  # 0..22
    for j in range(8):  # bit 7 down to 0
        if v10 == 0:
            v10 = 1
        # secret bit mask
        secret_mask = 1 << (7 - j)
        secret_bit = 1 if (ba[i] & secret_mask) else 0
        # input bit position in that byte
        bitpos = 7 - v10
        # store the bit
        if v11 < input_len:
            if inp_bits[v11][bitpos] is None:
                inp_bits[v11][bitpos] = secret_bit
            elif inp_bits[v11][bitpos] != secret_bit:
                raise Exception("Conflict detected")
        v10 += 1
        if v10 == 8:
            v10 = 0
            v11 += 1

# Any None bits can be set arbitrarily. Choose 0 for unspecified bits for clarity.
result = bytearray()
for b in inp_bits:
    val = 0
    for bitpos in range(8):
        bit = b[bitpos] if b[bitpos] is not None else 0
        val |= (bit << bitpos)
    result.append(val)

print("length:", len(result))
print("bytes:", [hex(x) for x in result])
print("flag (as ASCII):")
print(result.decode('latin1'))
