def asm2(start_value: int, start_count: int) -> int:
    acc = start_value
    count = start_count

    while acc <= 0xFB46:
        count += 1
        acc += 0x74

    return count


result = asm2(0x4, 0x21)
print(hex(result))
