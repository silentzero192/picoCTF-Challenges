#!/usr/bin/env python3
import sys


def func2(x: int) -> int:
    return x + 3


def func1(n: int) -> int:
    acc = 0
    while n != 0:
        if n & 1:
            acc = func2(acc)
        n >>= 1
    return acc


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <number>")
        sys.exit(1)

    n = int(sys.argv[1])
    result = func1(n)

    # mask to 32-bit unsigned and format as 8-digit lowercase hex
    hex32 = result & 0xFFFFFFFF
    flag = f"picoCTF{{{hex32:08x}}}"
    print(flag)


if __name__ == "__main__":
    main()
