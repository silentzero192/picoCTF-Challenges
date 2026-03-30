# Binary Digits

## Challenge

- **Name:** Binary Digits
- **Category:** Forensics
- **Description:** `This file doesn't look like much... just a bunch of 1s and 0s. But maybe it's not just random noise. Can you recover anything meaningful from this?`

## Files

- `digits.bin`

## Analysis

The challenge file looked like plain ASCII text containing only `0` and `1`, so the first step was to check whether those bits represented actual bytes.

The file starts with:

```text
11111111 11011000 11111111 11100000 ...
```

Grouping into 8-bit chunks gives:

```text
FF D8 FF E0 ...
```

`FF D8` is the JPEG magic header, which means the binary digits are just a JPEG image encoded as text bits.

## Solve

Convert every 8 characters of `digits.bin` into one byte and write the output to an image file:

```python
from pathlib import Path

bits = Path("digits.bin").read_text().strip()
data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
Path("decoded.jpg").write_bytes(data)
```

You can also do it in a one-liner:

```bash
python3 -c 'from pathlib import Path; b=Path("digits.bin").read_text().strip(); Path("decoded.jpg").write_bytes(bytes(int(b[i:i+8],2) for i in range(0,len(b),8)))'
```

After opening `decoded.jpg`, the flag is visible in the image.

## Flag

```text
picoCTF{h1dd3n_1n_th3_b1n4ry_2c2db635}
```
