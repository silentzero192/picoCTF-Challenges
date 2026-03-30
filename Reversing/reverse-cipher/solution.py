def reverse_transform(s: str) -> str:
    # convert to mutable list of character codes
    out_bytes = list(s.encode("latin1"))  # keep raw bytes
    orig = [0] * len(out_bytes)

    # indices 0–7 unchanged
    for i in range(0, 8):
        orig[i] = out_bytes[i]

    # indices 8–22 transformed
    for j in range(8, 23):
        if j % 2 == 0:   # even index -> was +5 during encoding
            orig[j] = (out_bytes[j] - 5) % 256
        else:            # odd index -> was -2 during encoding
            orig[j] = (out_bytes[j] + 2) % 256

    # last byte (23) unchanged
    orig[23] = out_bytes[23]

    return bytes(orig).decode("latin1")


if __name__ == "__main__":
    given = "picoCTF{w1{1wq85jc=2i0<}"
    flag = reverse_transform(given)
    print("Recovered flag:", flag)
