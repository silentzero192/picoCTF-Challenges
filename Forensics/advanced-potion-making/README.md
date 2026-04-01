# Advanced Potion Making - Writeup (picoCTF)

### 1. Analysis

The challenge provides a file named `advanced-potion-making`. Checking the file type and hex data reveals it is a corrupted PNG file:

- **Magic Bytes:** `89 50 42 11` (Should be `89 50 4E 47`)
- **IHDR Length:** `00 12 13 14` (Should be `00 00 00 0D`)

### 2. Repairing the Header

We use a Python script to patch the corrupted signature and the IHDR chunk length to make it a valid PNG.

```python
with open('advanced-potion-making', 'rb') as f:
    data = bytearray(f.read())

# Fix PNG Signature 'NG'
data[2:4] = b'\x4e\x47'
# Fix IHDR Chunk Length to 13 bytes
data[8:12] = b'\x00\x00\x00\x0d'

with open('fixed-potion.png', 'wb') as f:
    f.write(data)
```

Use code with caution.

### 3. Visual Steganography

The repaired image fixed-potion.png appears as a solid red square. This indicates the flag is hidden in the color channels, likely using LSB (Least Significant Bit) steganography.

### 4. Extracting the Flag

We use the Pillow library to isolate the LSB of the Red channel. By checking if the red value is even or odd, we can reconstruct the hidden image.

```python
from PIL import Image

img = Image.open('fixed-potion.png')
pixels = img.load()
width, height = img.size

new_img = Image.new('RGB', (width, height))
new_pixels = new_img.load()

for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        # If LSB of Red is 1, make pixel white; else black
        val = 255 if (r & 1) else 0
        new_pixels[x, y] = (val, val, val)

new_img.save('recovered_flag.png')
```

Use code with caution.

### 5. Result

Opening recovered_flag.png reveals the flag in white text on a black background.
Flag: picoCTF{................}
