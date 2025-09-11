def emulate():
    var = 0x9fe1a  
    if var <= 0x2710:  
        var += 0x65    
    else:
        var -= 0x65    
    return var

print(hex(emulate()), emulate())
