# 🌱 PicoCTF: Seeds and Feeds

> **Category:** Reversing
> **Description:**
> "There is something on my shop network running at `nc mercury.picoctf.net 59953`, but I can't tell what it is. Can you?"
> **Hint:** *What language does a CNC machine use?*

---

## 🔎 Overview

This challenge provided a network service that, when connected to via `nc`, outputs a series of instructions resembling **G-code**. G-code is the programming language used to control CNC machines, describing tool paths and shapes.

---

## 🛠️ Solution Steps

1.  **Connect to the Service**
    First, I connected to the challenge server:
    ```bash
    nc mercury.picoctf.net 59953
    ```
    The output was a long list of commands starting with G0, G1, X, and Y coordinates, which are standard G-code instructions.

2.  **Save the Output**
    Redirected the output into a file for further inspection:
    ```bash
    nc mercury.picoctf.net 59953 > flag.gcode
    ```

3.  **Visualize the G-code**
    Since G-code represents paths and shapes, I uploaded the file into an online G-code visualizer (e.g., [ncviewer.com](http://ncviewer.com)).

4.  **Extract the Flag**
    The visualization revealed the flag drawn as a shape in the plotted output.
