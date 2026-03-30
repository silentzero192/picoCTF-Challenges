# AES-ABC

**Platform:** picoCTF  
**Category:** Crypto  
**Difficulty:** Medium  
**Time spent:** ~10 minutes  

---

## 1) Goal

Decrypt an encrypted PPM image (`body.enc.ppm`) that was encrypted using a custom "Addition Block Chaining" (ABC) scheme layered on top of AES-ECB. The flag is hidden visually inside the image.

---

## 2) Key Clues

- **Challenge description:** *"AES-ECB is bad, so I rolled my own cipher block chaining mechanism - Addition Block Chaining!"* — hints that the weakness lies in ECB, not the custom chaining.
- **Source code provided:** `aes-abc.py` reveals the full encryption logic.
- **PPM image format:** An uncompressed image format — pixel patterns are preserved through ECB encryption.
- **No key provided:** The AES key is imported from a separate file we don't have, meaning the solution must bypass AES decryption entirely.

---

## 3) Plan

- Read `aes-abc.py` to understand the encryption pipeline: AES-ECB → Addition Block Chaining.
- Realize that reversing only the ABC layer (which uses simple modular addition) recovers AES-ECB ciphertext — no key needed.
- Exploit the **ECB penguin effect**: identical plaintext blocks produce identical ciphertext blocks, so the image structure (and flag text) remain visible.
- Write the recovered ECB ciphertext back as a PPM file and view it.

---

## 4) Steps

**Step 1 — Analyze the source code**  
- **Action:** Read `aes-abc.py` to understand the encryption flow.  
- **Result:** The encryption does:
  1. `plaintext → AES-ECB → ciphertext blocks (c1, c2, ..., cn)`
  2. Prepend a random IV: `blocks = [IV, c1, c2, ..., cn]`
  3. Apply ABC: `blocks[i+1] = (blocks[i] + blocks[i+1]) % 2^128`
- **Decision:** The ABC is reversible without the key — just subtract each previous block.

**Step 2 — Write the decryption script**  
- **Action:** Created `solve.py` that:
  1. Parses the PPM header (3 lines: magic number, dimensions, max color value)
  2. Splits the encrypted body into 16-byte blocks
  3. Reverses ABC from last block to first: `original[i] = (blocks[i] - blocks[i-1]) % 2^128`
  4. Strips the IV (first block)
  5. Writes the result back with the original PPM header
- **Result:** Successfully produced `flag_decrypted.ppm`.

**Step 3 — View the decrypted image**  
- **Action:** Converted PPM to PNG and opened the image.  
- **Result:** The flag text is clearly visible through the ECB penguin effect — identical background pixels form uniform blocks, while the flag text stands out as different block patterns.

---

## 5) Solution Summary

The "Addition Block Chaining" is a post-processing layer applied **after** AES-ECB encryption. Since it only uses modular addition (`(prev + curr) % 2^128`), it's trivially reversible by subtracting each previous block from the current one — no AES key required. Once the ABC layer is stripped, we're left with raw AES-ECB ciphertext. Because ECB mode encrypts each block independently, identical plaintext blocks (e.g., background pixels) produce identical ciphertext blocks. This preserves the image structure, making the flag text visually readable in the output — the classic **ECB penguin** vulnerability.

---

## 6) Flag

```
picoCTF{d0nt_r0ll_yoUr_0wN_aES}
```

---

## 7) Lessons Learned

- **AES-ECB leaks patterns:** Identical plaintext blocks always produce identical ciphertext blocks, making it unsuitable for structured data like images.
- **Custom crypto is often weaker than standard modes:** The "Addition Block Chaining" added no real security — it was trivially reversible without the key.
- **Not every crypto challenge requires brute-forcing or finding the key:** Sometimes the vulnerability is in the mode of operation, not the cipher itself.
- **PPM is a great format for ECB demos:** Its uncompressed nature perfectly preserves block-level patterns.

---

## 8) Personal Cheat Sheet

| Command / Tool | Purpose |
|---|---|
| `python3 solve.py` | Reverse ABC chaining and output decrypted PPM |
| `convert file.ppm file.png` | Convert PPM to PNG (ImageMagick) |
| `PIL / Pillow` | Alternative PPM → PNG conversion in Python |
| **ECB penguin pattern** | When you see ECB + image/structured data → patterns leak through, no key needed |
| **Modular arithmetic reversal** | `(a + b) % n` reversed by `(result - a) % n` |
