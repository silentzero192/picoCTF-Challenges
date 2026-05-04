# weird-file CTF Writeup

---

## 📋 Challenge Information
| Detail | Value |
|--------|-------|
| **Challenge Name** | weird file |
| **Category** | Forensics |
| **Description** | What could go wrong if we let Word documents run programs? (aka "in-the-clear") |
| **Files Provided** | `weird.docm` (Microsoft Word macro-enabled document) |
| **Flag Format** | `picoCTF{...}` |

---

## 🧠 Background
This challenge tests understanding of two core concepts:
1. **Macro-Enabled Office Documents (.docm)**: Microsoft Word documents with the `.docm` extension can contain embedded VBA (Visual Basic for Applications) macros. These macros can execute arbitrary code when the document is opened, making them a common attack vector for malware.
2. **OLE and OpenXML Analysis**: `.docm` files are essentially ZIP archives containing XML and binary components. The `vbaProject.bin` file stores VBA macros in OLE (Object Linking and Embedding) format. Tools like `oletools` can extract and analyze these macros without actually opening the document in Word.

---

## 🔍 Step-by-Step Solution

### Step 1: Initial File Analysis
First, we verify the file type to confirm we're dealing with a Word document:
```bash
file weird.docm
# Output: weird.docm: Microsoft Word 2007+
```

The file is identified as a Microsoft Word 2007+ document (Office Open XML format with macros).

---

### Step 2: Basic String Extraction
We perform a quick strings check to see if anything obvious appears in plain text:
```bash
strings weird.docm | head -20
# Output:
# [Content_Types].xml
# $.g'_
# `9K>
# _rels/.rels
# jH[{
# l0/%
# word/_rels/document.xml.rels
# ?@SK
# word/document.xml
# 3<x+
# ...
```

Nothing immediately visible - the macro is embedded within the OLE structure and not directly visible via strings.

---

### Step 3: Understanding .docm Structure
`.docm` files are essentially ZIP archives containing XML and binary components:
```
weird.docm
├── [Content_Types].xml
├── _rels/
├── word/
│   ├── document.xml
│   ├── vbaProject.bin    ← Contains VBA macros (key file)
│   ├── styles.xml
│   ├── settings.xml
│   └── theme/
└── docProps/
```

The `vbaProject.bin` file is the OLE stream containing the actual VBA macro code.

---

### Step 4: Extracting Macros with oletools
`oletools` is a Python package specifically designed for analyzing OLE and OpenXML files with macros. We use the `olevba` tool to extract the VBA macros:

```bash
# Install oletools if not already installed
pip install oletools

# Run olevba to extract macros
olevba weird.docm
# Output:
# olevba 0.60.2 on Python 3.12.3 - http://decalage.info/python/oletools
# ===============================================================================
# FILE: weird.docm
# Type: OpenXML
# WARNING  For now, VBA stomping cannot be detected for files in memory
# -------------------------------------------------------------------------------
# VBA MACRO ThisDocument.cls
# in file: word/vbaProject.bin - OLE stream: 'VBA/ThisDocument'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

---

### Step 5: Analyze the Extracted Macro Code
The extracted VBA macro code:
```vb
Sub AutoOpen()
    MsgBox "Macros can run any program", 0, "Title"
    Signature
End Sub

Sub Signature()
    Selection.TypeText Text:="some text"
    Selection.TypeParagraph
End Sub

Sub runpython()
    Dim Ret_Val
    Args = """" '"""
    Ret_Val = Shell("python -c 'print(\"cGljb0NURnttNGNyMHNfcl9kNG5nM3IwdXN9\")'" & " " & Args, vbNormalFocus)
    If Ret_Val = 0 Then
        MsgBox "Couldn't run python script!", vbOKOnly
    End If
End Sub
```

| Component | Analysis |
|-----------|----------|
| `AutoOpen()` | Automatically executes when the document is opened |
| `Signature()` | Appears to be a decoy - types placeholder text |
| `runpython()` | Contains the actual payload - executes Python via `Shell()` |
| Base64 String | `cGljb0NURnttNGNyMHNfcl9kNG5nM3IwdXN9` - contains encoded flag |

The `olevba` tool also identified suspicious keywords:
```
+----------+--------------------+---------------------------------------------+
| Type     | Keyword            | Description                                 |
+----------+--------------------+---------------------------------------------+
| AutoExec | AutoOpen           | Runs when the Word document is opened       |
| Suspicious | Shell            | May run an executable file or a system      |
|          |                    | command                                     |
| Suspicious | vbNormalFocus    | May run an executable file or a system      |
|          |                    | command                                     |
| Suspicious | run              | May run an executable file or a system      |
|          |                    | command                                     |
+----------+--------------------+---------------------------------------------+
```

---

### Step 6: Decode the Flag
The `Shell` command in `runpython()` contains a base64-encoded string that would be printed when the macro executes:
```python
python -c 'print("cGljb0NURnttNGNyMHNfcl9kNG5nM3IwdXN9")'
```

We decode the base64 string:
```bash
echo "cGljb0NURnttNGNyMHNfcl9kNG5nM3IwdXN9" | base64 -d
# Output: picoCTF{m4cr0s_r_d4ng3r0us}
```

Alternatively, using Python:
```bash
python3 -c "import base64; print(base64.b64decode('cGljb0NURnttNGNyMHNfcl9kNG5nM3IwdXN9').decode())"
# Output: picoCTF{m4cr0s_r_d4ng3r0us}
```

---

## 🚩 Flag
```
picoCTF{m4cr0s_r_d4ng3r0us}
```

---

## 💡 Lessons Learned
1. **Macro Security**: Word macros can execute arbitrary code via VBA's `Shell()` function, making `.docm` files dangerous. Always be cautious when enabling macros in documents from untrusted sources.
2. **Static Analysis Tools**: Tools like `oletools` (specifically `olevba`) allow safe extraction and analysis of VBA macros without actually executing them in Word, which is essential for malware analysis and CTF challenges.
3. **Office Document Structure**: Understanding that `.docx`/`.docm` files are ZIP archives helps in manually inspecting their contents. The `vbaProject.bin` file is the key artifact for macro analysis.
4. **Defense in Depth**: Even if macros are disabled by default in modern Office, attackers often use social engineering to convince users to enable them - as demonstrated by the innocent-looking `AutoOpen()` message box.
