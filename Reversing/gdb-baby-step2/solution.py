def main():
    var1 = 0x1e0da   
    var2 = 0x25f     
    i = 0

    while i < var2:
        var1 += i
        i += 1

    print("Final value in eax:", var1)

if __name__ == "__main__":
    main()
