# 🔐 Stego RSA — Writeup

## 🧩 Challenge Information

- **Name:** Stego RSA  
- **Category:** Crypto / Steganography  
- **Difficulty:** Easy–Medium  

**Description:**  
A message has been encrypted using RSA. The public key is gone… but someone might have been careless with the private key.  

**Hint:**  
Metadata can tell you more than you expect. Hex can be turned back into a key file.

---

## 📁 Provided Files

```
flag.enc
image.jpg
```

---

## 🔍 Step 1: Analyze Image Metadata

```bash
exiftool image.jpg
```

### Key Finding

```
Comment : 2d2d2d2d2d424547494e2050524956415445204b4559...
```

The `Comment` field contains a long **hex string**.

---

## 🧠 Step 2: Identify the Hidden Data

The hex starts with:

```
2d2d2d2d2d424547494e2050524956415445204b4559
```

Decoding reveals:

```
-----BEGIN PRIVATE KEY-----
```

This indicates the hex is a **hex-encoded private key**.

---

## 🔄 Step 3: Convert Hex → Private Key

```bash
echo "<hex_data>" > key.hex
xxd -r -p key.hex > private.pem
```

---

## ⚠️ Step 4: Fix Permissions

```bash
chmod 600 private.pem
```

---

## 🔧 Step 5: Convert OpenSSH Key → PEM

Check key format:

```bash
file private.pem
```

Output:

```
OpenSSH private key
```

Convert to PEM:

```bash
ssh-keygen -p -m PEM -f private.pem
```

(Leave passphrase empty)

Verify:

```bash
file private.pem
```

```
PEM RSA private key
```

---

## 🔐 Step 6: Decrypt Ciphertext

```bash
openssl pkeyutl -decrypt -inkey private.pem -in flag.enc -out flag.txt
```

---

## 📄 Step 7: Get the Flag

```bash
cat flag.txt
```

---

## 🎉 Flag

```
picoCTF{REDACTED}
```

---

## 🧠 Key Takeaways

- Metadata can leak sensitive data (private keys)
- Hex encoding is reversible
- OpenSSH keys must be converted to PEM for OpenSSL
- Always inspect files using:
  - `exiftool`
  - `strings`
  - `file`

---

## 🧰 Tools Used

- exiftool  
- xxd  
- ssh-keygen  
- openssl  

---

## ⚡ One-Liner Solution

```bash
exiftool image.jpg | grep Comment | cut -d ':' -f2 | tr -d ' ' > key.hex
xxd -r -p key.hex > private.pem
chmod 600 private.pem
ssh-keygen -p -m PEM -f private.pem
openssl pkeyutl -decrypt -inkey private.pem -in flag.enc -out flag.txt
cat flag.txt
```
