# 🕵️ Flag in Flame – picoCTF Writeup

## 📌 Challenge Description

> The SOC team discovered a suspiciously large log file after a recent breach. Instead of normal logs, it contains a massive block of encoded data. Your task is to analyze it and uncover any hidden information.

**Hint:** Use Base64 to decode the data and generate the image file.

---

## 🎯 Objective

Extract the hidden flag from the provided encoded log file.

```text id="k2x7hz"
picoCTF{XXXXX}
```

---

## 🧰 Tools Used

* `base64`
* `file` / image viewer
* Python
* `Crypto.Util.number`

---

## 🔍 Step 1: Analyze the Given File

We are given a large file:

```bash id="t7v7f2"
logs.txt
```

The description suggests it contains **encoded data**, not actual logs.

---

## 🔐 Step 2: Decode Base64 Data

Use Base64 decoding:

```bash id="1xg6op"
cat logs.txt | base64 -d > output.png
```

👉 This converts the encoded data into an image file.

---

## 🖼️ Step 3: Inspect the Image

Open the generated image:

```bash id="m6w2hn"
output.png
```

The image contains a **hexadecimal number**:

```text id="7x8a2p"
0x7069636F4354467B666F72656E736963735F616E616C797369735F69735F616D617A696E675F35636363376362307D
```

---

## 🧠 Step 4: Understand the Encoding

* The value starts with `0x` → indicates a **hexadecimal integer**
* This likely represents **ASCII bytes encoded as a number**

---

## ⚙️ Step 5: Convert Hex to Bytes

Use Python with `Crypto.Util.number`:

```python id="w9p4ds"
from Crypto.Util.number import *

ct = 0x7069636F4354467B666F72656E736963735F616E616C797369735F69735F616D617A696E675F35636363376362307D
print(long_to_bytes(ct))
```

Output:

```text id="y6zv1q"
b'picoCTF{forensics_analysis_is_amazing_5ccc7cb0}'
```

---

## ✅ Final Flag

```text id="8z1j3m"
picoCTF{forensics_analysis_is_amazing_5ccc7cb0}
```

---

## 🧠 Key Takeaways

* Large “log” files may actually contain **encoded payloads**
* Base64 is commonly used for:

  * obfuscation
  * embedding binary data in text
* Images can contain **hidden textual clues**
* Hex values (`0x...`) often represent:

  * encoded ASCII data
  * integers that need conversion to bytes
* Use `long_to_bytes()` when dealing with large hex integers

---

## 🚀 TL;DR

* Decoded Base64 → got PNG
* Opened image → found hex value
* Converted hex → bytes → flag

---

💡 *Lesson:* Multi-layer encoding is common—decode step by step and always interpret the output format correctly.
