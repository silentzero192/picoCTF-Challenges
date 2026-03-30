# 🕵️ RED, RED, RED – picoCTF Writeup

## 📌 Challenge Description

> RED, RED, RED, RED
> **Hint:** The picture seems pure, but is it though? Red? Ged? Bed? Aed? Check whatever Facebook is called now.

---

## 🎯 Objective

Find the hidden flag inside the given PNG image.

```text
picoCTF{XXXXX}
```

---

## 🧰 Tools Used

* `strings`
* `exiftool`
* `zsteg`
* `base64`

---

## 🔍 Step 1: Initial File Analysis

Check strings inside the image:

```bash
strings red.png
```

We find a **poem embedded inside the file**:

```text
Crimson heart, vibrant and bold,
Hearts flutter at your sight.
Evenings glow softly red,
Cherries burst with sweet life.
Kisses linger with your warmth.
Love deep as merlot.
Scarlet leaves falling softly,
Bold in every stroke.
```

---

## 🔎 Step 2: Inspect Metadata

```bash
exiftool red.png
```

We confirm the poem is stored in metadata under:

```text
Poem : <same text>
```

---

## 🧠 Step 3: Hidden Clue (Acrostic)

Take the **first letter of each line**:

| Line     | Letter |
| -------- | ------ |
| Crimson  | C      |
| Hearts   | H      |
| Evenings | E      |
| Cherries | C      |
| Kisses   | K      |
| Love     | L      |
| Scarlet  | S      |
| Bold     | B      |

👉 This spells:

```text
CHECKLSB
```

---

## 💡 Step 4: Interpret the Hint

* “CHECK LSB” → Use **Least Significant Bit steganography**
* Hint: *“Check whatever Facebook is called now”* → **Meta**

  * Suggests looking deeper / hidden layers inside the image

---

## ⚙️ Step 5: Extract Hidden Data

Use `zsteg`:

```bash
zsteg red.png
```

Important output:

```text
b1,rgba,lsb,xy .. text: "cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==..."
```

👉 This is **Base64 encoded data** (repeated multiple times)

---

## 🔐 Step 6: Decode the Payload

```bash
echo "<base64_string>" | base64 -d
```

Output:

```text
picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}
```

(The string repeats multiple times, but the flag is the same)

---

## ✅ Final Flag

```text
picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}
```

---

## 🧠 Key Takeaways

* Metadata can contain **hidden clues**, not just data
* Acrostics (first-letter patterns) are common in CTFs
* LSB steganography is widely used for hiding payloads in images
* `zsteg` is extremely effective for PNG stego challenges
* Encoded outputs (Base64) often need an additional decoding step

---

## 🚀 TL;DR

* Found poem in metadata
* Extracted first letters → `CHECKLSB`
* Used `zsteg` → found Base64 string
* Decoded → got flag

---

💡 *Lesson:* Always look for patterns in text—sometimes the file tells you exactly how to solve it.

