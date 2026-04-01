# 🧩 PicoCTF Challenge: Sequences

## 🎯 Objective
Recover the original flag from a provided encrypted byte sequence.  
The encryption key is derived from a huge integer `sol`, which is the **20,000,000th term** of a given recurrence relation.

---

## 🧠 Approach Summary

### 1. Understand the Recurrence
The challenge provides the recurrence:

```
m(i) = 55692 * m(i-4) - 9549 * m(i-3) + 301 * m(i-2) + 21 * m(i-1)
```

With base cases:

```
m(0) = 1
m(1) = 2
m(2) = 3
m(3) = 4
```

Computing `m(2e7)` using simple recursion or iteration is computationally **infeasible** due to time and space constraints.

---

### 2. Use Closed-Form Expression
Using **WolframAlpha**, we paste the recurrence relation and receive a closed-form expression:

```
(1612*(-21)^i + 30685*2^(5+2i)*3^i - 1082829*13^i + 8349*17^(1+i)) / 42636
```

This allows direct computation of `m(20000000)` by substituting `i = 20000000`.

---

### 3. Evaluate the Closed-Form Expression
Due to the **extreme size** of the result (~10,000+ digits), WolframAlpha truncates the output.

✅ So, I used **SageMathCell**:  
➡️ https://sagecell.sagemath.org

Using:

```python
i = 20000000
sol = (1612*(-21)^i + 30685*2^(5+2*i)*3^i - 1082829*13^i + 8349*17^(1+i)) / 42636
sol_mod = sol % (10^10000)
```

Saved `sol_mod` as output to a file `sample.txt`.

---

### 4. Verify the Solution

A Python script:
- Reads `sol_mod` from `sample.txt`.
- Computes the **MD5 hash**.
- Compares it against a predefined `VERIFY_KEY`.

```python
import hashlib

with open("sample.txt") as f:
    sol = f.read().strip()

md5_hash = hashlib.md5(sol.encode()).hexdigest()
assert md5_hash == VERIF_KEY
```

---

### 5. Decrypt the Flag

- Compute `SHA-256(sol)` to derive the XOR key.
- XOR the encrypted bytes with this key to retrieve the original flag.

```python
import hashlib

key = hashlib.sha256(sol.encode()).digest()
decrypted = bytes([c ^ key[i % len(key)] for i, c in enumerate(encrypted_data)])
print(decrypted.decode())
```

---

## 🧰 Tools Used

- 🔍 **WolframAlpha**: For finding the closed-form of the recurrence.
- 🧮 **SageMathCell**: For evaluating large modular arithmetic.
- 🐍 **Python**: For flag verification and decryption.

---

## 📚 Key Learnings

- Large recurrence relations can often be simplified using **closed-form expressions**.
- For very large numbers, use **symbolic computation tools** like SageMath rather than attempting brute-force or recursive solutions.
- **MD5** and **SHA-256** hashes are commonly used in CTFs for validation and encryption.

---

## ✅ Status

**Successfully retrieved the flag!**

