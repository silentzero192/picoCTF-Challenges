def asm4(input_string):
    """
    Python implementation of the asm4 assembly function.
    
    The function takes a string pointer as input and performs some calculations
    based on the characters in the string.
    """
    # Convert string to list of ASCII values for easier processing
    chars = [ord(c) for c in input_string] + [0]  # Add null terminator
    
    # Local variables (stack allocations)
    # [ebp-0x10]: result accumulator, initialized to 0x252
    var_10 = 0x252
    
    # [ebp-0xc]: string length counter, initialized to 0
    var_c = 0
    
    # [ebp-0x8]: loop counter for main processing
    var_8 = 0
    
    print(f"Input string: '{input_string}'")
    print(f"ASCII values: {chars[:-1]}")
    print()
    
    # First loop: Count string length
    # <+21>: jmp 0x518 (jump to +27)
    # <+27>: Check if current character is null
    print("=== Phase 1: Counting string length ===")
    while True:
        # <+27>: mov edx, [ebp-0xc]
        edx = var_c
        # <+30>: mov eax, [ebp+0x8] (string pointer)
        # <+33>: add eax, edx
        # <+35>: movzx eax, BYTE PTR [eax]
        current_char = chars[edx]
        # <+38>: test al,al
        if current_char == 0:
            break
        # <+23>: add DWORD PTR [ebp-0xc], 0x1
        var_c += 1
    
    print(f"String length found: {var_c}")
    print()
    
    # Second part: Main calculation loop
    # <+42>: mov DWORD PTR [ebp-0x8], 0x1
    var_8 = 1
    
    print("=== Phase 2: Main calculation loop ===")
    # <+49>: jmp 0x587 (jump to +138)
    while True:
        # <+138>: mov eax, [ebp-0xc]
        # <+141>: sub eax, 0x1
        # <+144>: cmp [ebp-0x8], eax
        if var_8 >= (var_c - 1):
            break
        
        # <+51>: mov edx, [ebp-0x8]
        # <+54>: mov eax, [ebp+0x8]
        # <+57>: add eax, edx
        # <+59>: movzx eax, BYTE PTR [eax]
        char_at_i = chars[var_8]
        
        # <+62>: movsx edx, al
        edx = char_at_i
        
        # <+65>: mov eax, [ebp-0x8]
        # <+68>: lea ecx, [eax-0x1]
        ecx = var_8 - 1
        
        # <+71>: mov eax, [ebp+0x8]
        # <+74>: add eax, ecx
        # <+76>: movzx eax, BYTE PTR [eax]
        char_at_i_minus_1 = chars[ecx]
        
        # <+79>: movsx eax, al
        # <+82>: sub edx, eax
        diff1 = edx - char_at_i_minus_1
        
        # <+84>: mov eax, edx
        # <+86>: mov edx, eax
        # <+88>: mov eax, [ebp-0x10]
        # <+91>: lea ebx, [edx+eax*1]
        ebx = diff1 + var_10
        
        # <+94>: mov eax, [ebp-0x8]
        # <+97>: lea edx, [eax+0x1]
        edx = var_8 + 1
        
        # <+100>: mov eax, [ebp+0x8]
        # <+103>: add eax, edx
        # <+105>: movzx eax, BYTE PTR [eax]
        char_at_i_plus_1 = chars[edx] if edx < len(chars) else 0
        
        # <+108>: movsx edx, al
        edx = char_at_i_plus_1
        
        # <+111>: mov ecx, [ebp-0x8]
        # <+114>: mov eax, [ebp+0x8]
        # <+117>: add eax, ecx
        # <+119>: movzx eax, BYTE PTR [eax]
        # <+122>: movsx eax, al
        # <+125>: sub edx, eax
        diff2 = edx - char_at_i
        
        # <+127>: mov eax, edx
        # <+129>: add eax, ebx
        # <+131>: mov [ebp-0x10], eax
        var_10 = ebx + diff2
        
        print(f"Iteration {var_8}:")
        print(f"  char[{var_8}] = '{input_string[var_8]}' (0x{char_at_i:02x})")
        print(f"  char[{var_8-1}] = '{input_string[var_8-1]}' (0x{char_at_i_minus_1:02x})")
        if edx < len(input_string):
            print(f"  char[{var_8+1}] = '{input_string[var_8+1]}' (0x{char_at_i_plus_1:02x})")
        else:
            print(f"  char[{var_8+1}] = '\\0' (0x00)")
        print(f"  diff1 (char[i] - char[i-1]) = 0x{diff1:02x}")
        print(f"  diff2 (char[i+1] - char[i]) = {diff2:02x}")
        print(f"  var_10 = 0x{var_10:x}")
        print()
        
        # <+134>: add DWORD PTR [ebp-0x8], 0x1
        var_8 += 1
    
    # <+149>: mov eax, [ebp-0x10]
    # <+157>: ret
    return var_10

# Test with the given input
input_str = "picoCTF_724a2"
result = asm4(input_str)
print(f"=== Final Result ===")
print(f"asm4('{input_str}') = 0x{result:x}")