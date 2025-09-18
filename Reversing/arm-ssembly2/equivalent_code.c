#include <stdio.h>
#include <stdlib.h>

unsigned int func1(unsigned int n)
{
    unsigned int acc = 0;
    unsigned int cnt = 0;

    while (cnt < n)
    {
        acc += 3;
        cnt += 1;
    }

    return acc;
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        fprintf(stderr, "usage: %s <number>\n", argv[0]);
        return 1;
    }

    int v = atoi(argv[1]);
    unsigned int result = func1((unsigned int)v);

    // print result in hex
    printf("Result: 0x%X\n", result);

    return 0;
}
