def asm3(arg1, arg2, arg3):
    """
    Python implementation of the asm3 assembly function.

    Assembly breakdown:
    - xor eax,eax           ; eax = 0x00000000
    - mov ah,[ebp+0xa]      ; ah = byte at [ebp+0xa]
    - shl ax,0x10           ; shift ax left by 16 bits (but ax is 16-bit register!)
    - sub al,[ebp+0xc]      ; al = al - byte at [ebp+0xc]
    - add ah,[ebp+0xd]      ; ah = ah + byte at [ebp+0xd]
    - xor ax,[ebp+0x10]     ; ax = ax XOR word at [ebp+0x10]
    """

    # Initial state: eax = 0
    eax = 0

    # Extract bytes from memory addresses
    # [ebp+0x8] = arg1 = 0xd73346ed
    # [ebp+0xa] is 2 bytes into arg1 (little-endian)
    byte_at_ebp_plus_0xa = (arg1 >> 16) & 0xFF  # 0x46

    # mov ah, BYTE PTR [ebp+0xa]
    # ah is the high byte of ax (bits 8-15 of eax)
    eax = (eax & 0xFFFF00FF) | (byte_at_ebp_plus_0xa << 8)
    print(f"After mov ah,[ebp+0xa]: eax = 0x{eax:08x}, ax = 0x{eax & 0xFFFF:04x}")

    # shl ax, 0x10 (shift ax left by 16 bits)
    # IMPORTANT: ax is only 16 bits, so shifting by 16 makes it 0!
    ax = (eax & 0xFFFF) << 16
    ax = ax & 0xFFFF  # Keep only lower 16 bits (ax is 16-bit register)
    eax = (eax & 0xFFFF0000) | ax
    print(f"After shl ax,0x10: eax = 0x{eax:08x}, ax = 0x{eax & 0xFFFF:04x}")

    # [ebp+0xc] is the first byte of arg2
    byte_at_ebp_plus_0xc = arg2 & 0xFF  # 0xae

    # sub al, BYTE PTR [ebp+0xc]
    # al is the low byte of ax (bits 0-7 of eax)
    al = eax & 0xFF
    al = (al - byte_at_ebp_plus_0xc) & 0xFF  # Keep 8-bit result
    eax = (eax & 0xFFFFFF00) | al
    print(f"After sub al,[ebp+0xc]: eax = 0x{eax:08x}, ax = 0x{eax & 0xFFFF:04x}")

    # [ebp+0xd] is the second byte of arg2
    byte_at_ebp_plus_0xd = (arg2 >> 8) & 0xFF  # 0x72

    # add ah, BYTE PTR [ebp+0xd]
    ah = (eax >> 8) & 0xFF
    ah = (ah + byte_at_ebp_plus_0xd) & 0xFF  # Keep 8-bit result
    eax = (eax & 0xFFFF00FF) | (ah << 8)
    print(f"After add ah,[ebp+0xd]: eax = 0x{eax:08x}, ax = 0x{eax & 0xFFFF:04x}")

    # [ebp+0x10] is the first word (2 bytes) of arg3
    word_at_ebp_plus_0x10 = arg3 & 0xFFFF  # 0xb139

    # xor ax, WORD PTR [ebp+0x10]
    ax = eax & 0xFFFF
    ax = ax ^ word_at_ebp_plus_0x10
    eax = (eax & 0xFFFF0000) | ax
    print(f"After xor ax,[ebp+0x10]: eax = 0x{eax:08x}, ax = 0x{eax & 0xFFFF:04x}")

    # Return value is in eax (but only ax is meaningful here)
    return ax


# Test with the given values
arg1 = 0xD73346ED
arg2 = 0xD48672AE
arg3 = 0xD3C8B139

print("=== Executing asm3(0xd73346ed, 0xd48672ae, 0xd3c8b139) ===")
print(f"arg1 = 0x{arg1:08x}")
print(f"arg2 = 0x{arg2:08x}")
print(f"arg3 = 0x{arg3:08x}")
print()

result = asm3(arg1, arg2, arg3)
print(f"\nFinal result: 0x{result:x}")
