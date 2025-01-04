import sys, emulator

instructions = {
    "nop": "00000000",
    "lda": "00000001",
    "ldb": "00000010",
    "sta": "00000011",
    "stb": "00000100",
    "add": "00000101",
    "sub": "00000110",
    "mul": "00000111",
    "div": "00001000",
    "goto": "00001001",
    "giz": "00001010",
    "gnz": "00001011",
    "wra": "00001101",
    "wrb": "00001110",
    "and": "00010000",
    "or": "00010001",
    "xor": "00010010",
    "nand": "00010011",
    "nor": "00010100",
    "xnor": "00010101",
    "shr": "00010110",
    "shl": "00010111",
    "hlt": "11111111",
}

def assemble(lines:list[str])->list[str]:
    binary = []
    for line in lines:
        words = line.lower().split(" ")
        new = []
        for word in words:
            if word in instructions:
                word = instructions[word]
            elif word.endswith("i"):
                word = '{0:08b}'.format(int(word[:-1]))
            
            new.append(word)
        new.reverse()
        new = "".join(new)
        length = len(new)
        if length < 16:
            new = "0"*(16-length) + new
        binary.append(new)
    return binary

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("no input file specified")
        quit()
    with open(sys.argv[1],"r") as f:
        asm = f.read().split("\n")
    binary = assemble(asm)
    text = "\n".join(binary)
    with open("binary.txt","w") as f:
        f.write(text)
    with open("readable.txt","w",encoding="utf-8") as f:
        replaced = text.replace("1","■").replace("0","□")
        new = ""
        for t in replaced.split("\n"):
            new += t[:8] + " " + t[8:] + "\n"
        f.write(new)
    
    dave = emulator.Dave()
    dave.execute(binary, False)