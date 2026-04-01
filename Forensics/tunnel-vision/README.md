# picoCTF Writeup: tunn3l v1s10n (Forensics)

## Description
I found this file. Recover the flag.

## Solution

### 1. Identify File Type
Using a hex editor, we see the file starts with the hex signature `42 4D` (`BM` in ASCII), confirming it is a **BMP (Bitmap)** file. However, the file is corrupted and won't open.

### 2. Fix the DIB Header Size
The DIB header size is located at offset `0x0E`. In this file, it is set to an invalid value.

*   **Offset `0x0E`**: Change `BA D0 00 00` to **`28 00 00 00`** (the standard 40-byte header size).

### 3. Adjust Image Height
After fixing the header, the image opens but shows a decoy: `notaflag{sorry}`. This means the image height is restricted, hiding the real flag in the metadata "above" the visible area.

*   **Offset `0x16`**: Change the height from `32 01 00 00` (306px) to **`32 03 00 00`** (818px).

### 4. Result
Save the file as `tunn3l_v1s10n.bmp` and open it. The real flag is revealed at the top of the expanded image.

## Flag
`picoCTF{REDACTED}`

