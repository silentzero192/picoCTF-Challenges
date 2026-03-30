#include <stdio.h>
#include <stdint.h>

uint32_t asm3_emulate(uint32_t arg1, uint32_t arg2, uint32_t arg3)
{
    uint8_t b1_2 = (arg1 >> 16) & 0xFF; // [ebp+0xa]
    uint8_t b2_0 = arg2 & 0xFF;         // [ebp+0xc]
    uint8_t b2_1 = (arg2 >> 8) & 0xFF;  // [ebp+0xd]
    uint16_t w3_0 = arg3 & 0xFFFF;      // [ebp+0x10]

    uint32_t eax = 0;
    uint8_t ah = b1_2;
    uint16_t ax = (ah << 8) & 0xFFFF;

    // shift ax left 16 -> place into high 16 bits of eax
    eax = ((uint32_t)ax << 16) & 0xFFFFFFFF;

    uint8_t al = eax & 0xFF;
    al = (uint8_t)(al - b2_0);
    ah = (uint8_t)(((eax >> 8) & 0xFF) + b2_1);

    ax = (uint16_t)((ah << 8) | al);
    ax ^= w3_0;

    eax = (eax & 0xFFFF0000) | ax;
    return eax;
}

int main(void)
{
    uint32_t r = asm3_emulate(0xd73346ed, 0xd48672ae, 0xd3c8b139);
    printf("0x%08x\n", r); // prints 0x3300c36b
    return 0;
}
