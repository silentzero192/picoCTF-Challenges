# 🕵️ Secret of Polyglot – picoCTF Writeup

## 📌 Challenge Description

> Files can always be changed in a secret way. Can you find the flag?
> **Hint:** Look at the details of the file.

---

## 🎯 Objective

Analyze the given file and uncover the hidden flag in the format:

```
picoCTF{XXXXX}
```

---

## 🧰 Tools Used

* `file`
* `strings`
* `binwalk`
* `cat`

---

## 🔍 Step 1: File Identification

Check the file type:

```bash
file flag2of2-final.png
```

Output:

```
PNG image data
```

At first glance, the file appears to be a normal PNG image.

---

## ⚠️ Step 2: Suspicious Content Detection

Run `strings` to inspect embedded readable data:

```bash
strings flag2of2-final.png
```

Key finding:

```
%PDF-1.4
```

👉 This indicates that the file contains **PDF data inside a PNG**.

---

## 🧠 Step 3: Understanding the Trick

This is a **polyglot file**, meaning:

* It is valid as **both a PNG image and a PDF document**
* PNG files end at the `IEND` chunk
* Any data after `IEND` can be used to hide additional content

---

## ⚙️ Step 4: Extract Hidden Data

Use `binwalk` to analyze embedded structures:

```bash
binwalk flag2of2-final.png
```

Output:

```
914  PDF document
1149 Zlib compressed data
```

Extract the hidden content:

```bash
binwalk -e flag2of2-final.png
```

This creates a directory:

```
_flag2of2-final.png.extracted
```

---

## 📦 Step 5: Analyze Extracted Files

Navigate to extracted folder:

```bash
cd _flag2of2-final.png.extracted
ls
```

Open the extracted data:

```bash
cat 47D
```

Output:

```
(1n_pn9_&_pdf_90974127})Tj
```

👉 This is text from a **PDF stream**, containing part of the flag.

---

## 🖼️ Step 6: Extract First Part from Image

Viewing the PNG image reveals:

```
picoCTF{f1u3n7_
```

---

## 🔗 Step 7: Combine the Flag

| Source       | Extracted Data           |
| ------------ | ------------------------ |
| PNG Image    | `picoCTF{f1u3n7_`        |
| Embedded PDF | `1n_pn9_&_pdf_90974127}` |

---

## ✅ Final Flag

```
picoCTF{f1u3n7_1n_pn9_&_pdf_90974127}
```

---

## 🧠 Key Takeaways

* Always inspect files beyond their extension
* Use `strings` to detect hidden file signatures
* Look for indicators like:

  * `%PDF` inside non-PDF files
  * Extra data after expected file endings
* `binwalk` is essential for extracting embedded data
* Polyglot files are a common forensic challenge technique

---

## 🚀 TL;DR

* File looked like PNG → actually PNG + PDF
* Used `strings` → found `%PDF`
* Used `binwalk` → extracted hidden data
* Combined image + extracted text → got flag

---

💡 *Lesson:* Never trust file extensions—always analyze the raw data.
