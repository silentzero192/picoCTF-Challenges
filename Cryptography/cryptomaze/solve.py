from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


INITIAL_STATE = [
    0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0,
    1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1,
    0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1,
    1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1,
]
TAPS = [63, 61, 60, 58]
CIPHERTEXT_HEX = (
    "8f0e6d0f5b0dc1db201948b9e0cebd8f"
    "65f3dbc3c00ee080eeede2138a5175fd"
    "38338e7e04fbddef0c6260a4eb758417"
)


def lfsr_bits(state, taps, count):
    state = state[:]
    for _ in range(count):
        yield state[0]
        feedback = 0
        for tap in taps:
            feedback ^= state[tap]
        state = state[1:] + [feedback]


def bits_to_bytes(bits):
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value.to_bytes(len(bits) // 8, "big")


def main():
    key = bits_to_bytes(list(lfsr_bits(INITIAL_STATE, TAPS, 128)))
    ciphertext = bytes.fromhex(CIPHERTEXT_HEX)
    plaintext = unpad(AES.new(key, AES.MODE_ECB).decrypt(ciphertext), AES.block_size)

    print(f"AES key: {key.hex()}")
    print(f"Flag: {plaintext.decode()}")


if __name__ == "__main__":
    main()
