import sys, emulator, re

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

    labels = {}
    index = -1
    while True:
        index += 1
        if index >= len(lines):
            break
        
        # remove comments and strip line
        line = lines[index]
        line = line.strip()
        line = re.sub(r"(#.+)","",line)
        lines[index] = line

        if not line:
            lines.remove(line)
            index -= 1
        elif line.endswith(":"):
            # find and note labels
            if line[:-1] in labels:
                print(f"label {line[:-1]} already exists!")
                quit()
            labels[line[:-1]] = index
            lines.remove(line)
            index -= 1
    
    # replace labels
    for index, line in enumerate(lines):
        for word in line.split(" "):
            if word in labels:
                lines[index] = line.replace(word,f"{labels[word]}i")

    # replace instructions with binary
    for line in lines:
        words = line.lower().split(" ")
        new = "0000000000000000"
        for word in words:
            if not word:
                continue
            if word in instructions:
                new = new[:8] + instructions[word]
            elif word.endswith("i"):
                new = '{0:08b}'.format(int(word[:-1])) + new[8:]
            elif len(word) == 8 and all([True if c == "1" or c == "0" else False for c in word]):
                new = word + new[8:]
            else:
                print(f"unknown symbol '{word}'")
                quit()
        binary.append(new)
    return binary

def assemble_and_run(asm:list[str], step=False):
    binary = assemble(asm)
    text = "\n".join(binary)
    with open("output/binary.txt","w") as f:
        f.write(text)
    with open("output/readable.txt","w",encoding="utf-8") as f:
        replaced = text.replace("1","■").replace("0","□")
        new = ""
        for t in replaced.split("\n"):
            new += t[:8] + " " + t[8:] + "\n"
        f.write(new)
    
    dave = emulator.Dave()
    dave.execute(binary, step)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("no input file specified")
        quit()
    with open(sys.argv[1],"r") as f:
        asm = f.read().split("\n")
    assemble_and_run(asm)