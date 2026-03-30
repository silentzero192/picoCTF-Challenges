#!/usr/bin/env python3
import sys

# --- func1 ---
def func1(n: int) -> int:
    if n > 100:
        return func2(n + 100)
    else:
        return func3(n)

# --- func2 ---
def func2(n: int) -> int:
    if n > 499:
        return func5(n + 13)
    else:
        return func4(n - 86)

# --- func3 ---
def func3(n: int) -> int:
    return func7(n)

# --- func4 ---
def func4(n: int) -> int:
    # call func1(17), ignore return, then return original n
    _ = func1(17)
    return n

# --- func5 ---
def func5(n: int) -> int:
    n = func8(n)
    return n

# --- func6 ---
def func6(n: int) -> int:
    # local vars according to assembly
    val = n
    x = 314
    y = 1932
    counter = 0
    result = 0
    while counter <= 899:
        w1 = y
        w0 = 800 * w1
        w2 = w0 // x
        w1 = (w2 * x)
        result = w0 - w1
        counter += 1
    return result

# --- func7 ---
def func7(n: int) -> int:
    if n > 100:
        return n
    else:
        return 7

# --- func8 ---
def func8(n: int) -> int:
    return n + 2

# --- main ---
def main():
    # if len(sys.argv) < 2:
    #     print(f"Usage: {sys.argv[0]} <number>")
    #     sys.exit(1)

    # n = int(sys.argv[1])
    n = 1151828495
    result = func1(n)

    # mask result to 32-bit
    result_32 = result & 0xFFFFFFFF
    print(f"picoCTF{{{result_32:08x}}}")

if __name__ == "__main__":
    main()
