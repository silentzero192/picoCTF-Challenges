# 🕵️ Hidden in Plain Sight – picoCTF Writeup

## 📌 Challenge Description

> You’re given a seemingly ordinary JPG image. Something is tucked away out of sight inside the file. Your task is to discover the hidden payload and extract the flag.
> **Hint:** Read the metadata.

---

## 🎯 Objective

Find the hidden flag inside the image file in the format:

```text
picoCTF{XXXXX}
```

---

## 🧰 Tools Used

* `file`
* `exiftool`
* `base64`
* `steghide`

---

## 🔍 Step 1: Inspect the File

Check basic file information:

```bash
file img.jpg
```

Output:

```text
JPEG image data ... comment: "c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9"
```

👉 The **comment field** looks suspicious (Base64 encoded).

---

## 🔎 Step 2: Extract Metadata

Use `exiftool`:

```bash
exiftool img.jpg
```

Relevant field:

```text
Comment : c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9
```

---

## 🔐 Step 3: Decode the Hidden Data

### First Base64 decode:

```bash
echo "c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9" | base64 -d
```

Output:

```text
steghide:cEF6endvcmQ=
```

---

### Second Base64 decode:

```bash
echo "cEF6endvcmQ=" | base64 -d
```

Output:

```text
pAzzword
```

---

## 🧠 Step 4: Understand the Clue

The decoded string follows this format:

```text
steghide:<password>
```

👉 This tells us:

* Tool to use → `steghide`
* Password → `pAzzword`

---

## ⚙️ Step 5: Extract Hidden Payload

Run:

```bash
steghide extract -sf img.jpg
```

Enter password:

```text
pAzzword
```

Output:

```text
wrote extracted data to "flag.txt"
```

---

## 📦 Step 6: Retrieve the Flag

```bash
cat flag.txt
```

Output:

```text
picoCTF{h1dd3n_1n_1m4g3_92f08d7c}
```

---

## ✅ Final Flag

```text
picoCTF{h1dd3n_1n_1m4g3_92f08d7c}
```

---

## 🧠 Key Takeaways

* Always inspect **metadata** using `exiftool`
* Encoded strings (Base64) often hide:

  * passwords
  * instructions
* `steghide` is commonly used for:

  * hiding files inside images
  * extracting hidden payloads with a password
* Not everything decoded is the flag—sometimes it's a **key to unlock it**

---

## 🚀 TL;DR

* Found Base64 string in metadata
* Decoded → got `steghide` + password
* Used `steghide extract`
* Retrieved flag from hidden file

---

💡 *Lesson:* Metadata often contains the key—not the flag itself.
