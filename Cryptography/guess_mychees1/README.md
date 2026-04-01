# 🧀 Guess My Cheese Part # 1

We were given an encrypted string and a cryptic hint:

> “Remember that cipher we devised together Squeexy? The one that incorporates your affinity for linear equations???”

This hint strongly pointed toward the **Affine Cipher**, which is a monoalphabetic substitution cipher based on a linear transformation using modular arithmetic.

---

## 🔢 Affine Cipher Overview

The encryption formula for the Affine Cipher is:
`E(x) = (a * x + b) mod 26`

Where:
- `x` is the position of the plaintext letter (`A=0`, `B=1`, ..., `Z=25`)
- `a` and `b` are the keys
- `a` must be **coprime with 26** to ensure invertibility

---

## 🔍 Initial Test

We were told to encrypt a known cheese. I chose:

- **Plaintext**: `CHEDDAR`
- **Program Output (Ciphertext)**: `GBEFFIR`

---

## 🔓 Cracking the Cipher

To recover the encryption keys, I used [dcode.fr](https://www.dcode.fr/affine-cipher), a well-known cipher analysis tool.

By providing the known pair:

- **Plaintext**: `CHEDDAR`
- **Ciphertext**: `GBEFFIR`

The tool successfully identified the **Affine Cipher keys**:

- `a = 25`
- `b = 8`

---

## 🧠 Decrypting the Main Challenge

We were then given the encrypted cheese:

- **Ciphertext**: `CIHRAEXGWA`

Using the identified key pair (`a = 25`, `b = 8`), I decrypted it (again using dcode.fr) and got:

- **Decrypted**: `GABRIELCMI`

---

## 🏁 Final Step

I submitted the decrypted text:

- ✅ **Flag Captured!**

