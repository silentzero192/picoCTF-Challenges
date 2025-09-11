# Challenge Name: asm1

## Challenge Description
We are given a disassembled function `asm1` and asked:
> What does `asm1(0x6fa)` return?
> Submit the flag as a hexadecimal value (starting with `0x`).

The function is written in x86 assembly and performs conditional comparisons and arithmetic before returning a value.

---

## Step-by-Step Analysis

### 1. Function prototype
The function takes one integer argument and returns an integer:

`int asm1(int x);`

### 2. Assembly breakdown
The function compares the input (x) with certain constants and executes different branches:

#### Case 1: `x <= 0x3a2`

If `x == 0x358` → return `x + 0x12`

Else → return `x - 0x12`

#### Case 2: `x > 0x3a2`

If `x == 0x6fa` → return `x - 0x12`

Else → return `x + 0x12`

### 3. Input given
We need to evaluate:

asm1(0x6fa);
`0x6fa` (1786 in decimal) is greater than `0x3a2`.

The function checks if `x == 0x6fa.`
The condition is true, so it executes:
`eax = x - 0x12`

### 4. Final calculation
`0x6fa - 0x12 = 0x6e8`
