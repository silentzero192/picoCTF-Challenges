#!/usr/bin/env python3
"""
AES-ABC Decryption - PicoCTF Challenge

The encryption works as:
1. Plaintext -> AES-ECB -> ciphertext blocks (c1, c2, ..., cn)
2. Prepend random IV: blocks = [IV, c1, c2, ..., cn]  
3. Addition Block Chaining: blocks[i+1] = (blocks[i] + blocks[i+1]) % UMAX

We reverse the ABC to get back ECB ciphertext.
Since AES-ECB produces identical output for identical input blocks,
the image structure (flag) will be visible in the output PPM.
No key needed!
"""

import math

BLOCK_SIZE = 16
UMAX = int(math.pow(256, BLOCK_SIZE))


def to_bytes(n):
    s = hex(n)
    s_n = s[2:]
    if 'L' in s_n:
        s_n = s_n.replace('L', '')
    if len(s_n) % 2 != 0:
        s_n = '0' + s_n
    decoded = bytes.fromhex(s_n)

    pad = len(decoded) % BLOCK_SIZE
    if pad != 0:
        decoded = b'\x00' * (BLOCK_SIZE - pad) + decoded
    return decoded


def remove_line(s):
    idx = s.index(b'\n')
    return s[:idx + 1], s[idx + 1:]


def parse_header_ppm(data):
    header = b""
    for i in range(3):
        header_i, data = remove_line(data)
        header += header_i
    return header, data


if __name__ == "__main__":
    with open('body.enc.ppm', 'rb') as f:
        data = f.read()

    header, encrypted_body = parse_header_ppm(data)
    print(f"Header: {header}")
    print(f"Encrypted body length: {len(encrypted_body)} bytes")

    # Split into 16-byte blocks
    blocks = [
        encrypted_body[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]
        for i in range(len(encrypted_body) // BLOCK_SIZE)
    ]
    print(f"Number of blocks: {len(blocks)}")

    # Reverse the Addition Block Chaining
    # During encryption: blocks[i+1] = (blocks[i] + blocks[i+1]) % UMAX
    # To reverse: original[i+1] = (blocks[i+1] - blocks[i]) % UMAX
    # Process from last block to first
    for i in range(len(blocks) - 1, 0, -1):
        prev_blk = int(blocks[i - 1].hex(), 16)
        curr_blk = int(blocks[i].hex(), 16)
        n_orig_blk = (curr_blk - prev_blk) % UMAX
        blocks[i] = to_bytes(n_orig_blk)

    # Remove IV (first block) - it was prepended during encryption
    ecb_ct = b''.join(blocks[1:])

    # Write as PPM - the ECB penguin effect will reveal the flag
    with open('flag_decrypted.ppm', 'wb') as fw:
        fw.write(header)
        fw.write(ecb_ct)

    print("Decrypted file saved as flag_decrypted.ppm")
    print("Open it to see the flag!")
