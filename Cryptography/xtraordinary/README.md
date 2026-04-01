# 🔐 XtraORdinary (Cryptography) — PicoCTF Challenge Writeup

## 🧩 Challenge Overview

**Title**: XtraORdinary  
**Hint**: "Check out my new, never-before-seen method of encryption! I totally invented it myself. I added so many for loops that I don't even know what it does. It's extraordinarily secure!"  

Attachments provided:
- `encrypt.py`
- `output.txt`

Given the challenge name emphasizes **XOR**, and understanding the nature of XOR, we know that:
> If a value is encrypted with XOR and the same key is applied again, it will **revert** to its original state.

---

## 🔍 Initial Analysis

Upon examining the `encrypt.py` script, we find:

```python
for random_str in random_strs:
    for i in range(randint(0, pow(2, 8))):
        for j in range(randint(0, pow(2, 6))):
            for k in range(randint(0, pow(2, 4))):
                for l in range(randint(0, pow(2, 2))):
                    for m in range(randint(0, pow(2, 0))):
                        ctxt = encrypt(ctxt, random_str)
```

While this looks complex due to nested loops, it ultimately just **repeats XOR with the same key** multiple times — and since XOR is reversible, the effect of even counts cancels out.

The `random_strs` list contains repeated entries:

```python
random_strs = [
    b'my encryption method',
    b'is absolutely impenetrable',
    b'and you will never',
    b'ever',
    b'ever',
    b'ever',
    b'ever',
    b'ever',
    b'ever',
    b'break it'
]
```

Since XORing an even number of times has no effect, we only consider the unique strings that are XORed **odd** number of times. Simplifying, this leaves:

```python
random_strs = [
    b'my encryption method',
    b'is absolutely impenetrable',
    b'and you will never',
    b'ever',
    b'break it'
]
```

This reduces the number of combinations for reversing the encryption to **2^5 = 32** possibilities.

---

## 🧪 Known Plaintext Attack

We know that all PicoCTF flags start with:

```
picoCTF{
```

This gives us a **known-plaintext**. We can brute-force through the reversed layers and try to identify the **original encryption key**.

The encrypted content is:

```python
from Crypto.Util.number import long_to_bytes
ctxt = long_to_bytes(0x57657535570c1e1c612b3468106a18492140662d2f5967442a2960684d28017931617b1f3637)
```

---

## 🔁 Decryption Routine

We reverse the encryption by applying the `encrypt` function (which is also the decryption function) in the **same nested loop structure**, but attempt to isolate the XOR key.

```python
from Crypto.Util.number import long_to_bytes, bytes_to_long

ctxt=long_to_bytes(0x57657535570c1e1c612b3468106a18492140662d2f5967442a2960684d28017931617b1f3637)
key=b"picoCTF{"
random_strs = [
    b'my encryption method',
    b'is absolutely impenetrable',
    b'and you will never',
    b'ever',
    b'break it'
]

def encrypt(ptxt, key):
    ctxt = b''
    for i in range(len(ptxt)):
        a = ptxt[i]
        b = key[i % len(key)]
        ctxt += bytes([a ^ b])
    return ctxt

for _ in range(2):
  ctxt = encrypt(ctxt, random_strs[0])
  for _ in range(2):
    ctxt = encrypt(ctxt, random_strs[1])
    for _ in range(2):
      ctxt = encrypt(ctxt, random_strs[2])
      for _ in range(2):
        ctxt = encrypt(ctxt, random_strs[3])
        for _ in range(2):
          ctxt = encrypt(ctxt, random_strs[4])
          a = encrypt(ctxt, key)
          print(a)
```

We cycle through the possible decryptions and look for readable/plaintext results.

---

## 🎯 Discovery

After trying the above and analyzing the outputs, we found that one trial reveals:

```
Africa!
```

Which seems to be the actual **key** used to XOR the flag.

---

## ✅ Final Step

Update the key:

```python
key = b"Africa!"
```

Run the script again with this key, and we successfully get the **flag**!

---

## 🧰 Tools Used

- Python 3
- `Crypto.Util.number` for byte manipulation

---

## 📚 Key Learnings

- XOR is its own inverse.
- Repeated XORing with the same string can be ignored if done an even number of times.
- Known plaintext like `picoCTF{` can greatly help in XOR key recovery.
- An overcomplicated encryption function doesn't necessarily provide more security — especially with symmetric encryption like XOR.

---

## 🏁 Status

**Flag successfully recovered!**

