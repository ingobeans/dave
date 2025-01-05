import sys, color, assembler, re

class BlockToken:
    def __init__(self):
        self.subtokens = []
    def append(self, token):
        self.subtokens.append(token)
    def __str__(self):
        return " {" + " ".join([token.__str__() for token in self.subtokens]) + "}" if self.subtokens else ""
    def __repr__(self):
        return self.__str__()

class GenericToken(BlockToken):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def __str__(self):
        return color.yellow(self.name) + (" {" + " ".join([token.__str__() for token in self.subtokens]) + "}" if self.subtokens else "")

class NumberToken(BlockToken):
    def __init__(self, value):
        super().__init__()
        self.value = value
    def __str__(self):
        return color.cyan(self.value)

class LetToken(BlockToken):
    def __init__(self, variable_name):
        super().__init__()
        self.variable_name = variable_name
    def __str__(self):
        return color.purple(f"let {self.variable_name}")

class SetToken(LetToken):
    def __init__(self, variable_name, expression):
        super().__init__(variable_name)
        self.expression = expression
    def __str__(self):
        return color.red(f"{self.variable_name.name} = {self.expression}")

class IfToken(BlockToken):
    def __init__(self, lhs, rhs, comparer, block):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.comparer = comparer
        self.block = block
    def __str__(self):
        return color.green(f"if {self.lhs} {self.comparer} {self.rhs}") + color.green(str(self.block))

class VariableToken(GenericToken):
    def __str__(self):
        return color.green(self.name)

class EqualsToken(BlockToken):
    def __str__(self):
        return color.yellow("==")
    
class NotEqualsToken(BlockToken):
    def __str__(self):
        return color.yellow("!=")

def tokenize(code:str, depth=0, token_amount:int=None)->list[GenericToken]:
    code = re.sub(r"(\/\/.+)","",code)
    code = code.replace("\n"," ")
    code = code.replace("{","{ ")
    code = code.replace("}"," }")
    words = code.split(" ")
    words = [word for word in words if len(word) != 0]
    tokens = BlockToken()
    index = 0
    
    while True:
        if index >= len(words):
            break
        if token_amount:
            if len(tokens.subtokens) >= token_amount:
                break
        word = words[index]
        index += 1
        match word:
            case "let":
                tokens.append(LetToken(words[index]))
                index += 1
            case "if":
                block, add_index = tokenize(" ".join(words[index:]),depth+1,4)
                token = IfToken(block.subtokens[0], block.subtokens[2], block.subtokens[1], block.subtokens[3])
                tokens.append(token)
                index += add_index
            case "=":
                block, add_index = tokenize(" ".join(words[index:]),depth+1,1)
                var = tokens.subtokens.pop()
                tokens.append(SetToken(var, block.subtokens[0]))
                index += add_index
            case "==":
                tokens.append(EqualsToken())
            case "!=":
                tokens.append(NotEqualsToken())
            case "{":
                block, add_index = tokenize(" ".join(words[index:]),depth+1)
                index += add_index
                tokens.append(block)
            case "}":
                return tokens, index
            case _:
                if word.isnumeric():
                    tokens.append(NumberToken(int(word)))
                elif word.isalnum():
                    tokens.append(VariableToken(word))
                else:
                    print(color.red(f"unknown keyword {word}"))
                    quit()
    return tokens, index

def tokens_to_asm(token_block:BlockToken, sections:list[list], variables={}, reg_a=0, reg_b=0, pointer_counter=0)->list[str]:
    sections.append([])
    current_section_index = len(sections) - 1
    for index, token in enumerate(token_block.subtokens):
        if type(token) == BlockToken:
            reg_a, reg_b = tokens_to_asm(token, sections, variables, reg_a, reg_b)
        elif type(token) == VariableToken:
            if not token.name in variables:
                print(f"undefined variable {token}")
            if index == len(token_block.subtokens) - 1:
                sections[current_section_index].append(f"lda {variables[token.name]}i")
        elif type(token) == LetToken:
            variables[token.variable_name] = max(list(variables.values()))+1 if variables else 1
        elif type(token) == NumberToken:
            if reg_a != token.value:
                sections[current_section_index].append(f"wra {token.value}i")
            if index == len(token_block.subtokens) - 1:
                reg_a = token.value
        elif type(token) == SetToken:
            data = []
            reg_a, reg_b = tokens_to_asm(token.expression, data, variables, reg_a, reg_b, pointer_counter)
            asm = data[0]
            sections[current_section_index] += asm
            sections[current_section_index].append(f"sta {variables[token.variable_name.name]}i")
        elif type(token) == IfToken:
            data = []
            reg_a,reg_b = tokens_to_asm(token.lhs,data,variables,reg_a,reg_b, pointer_counter)
            reg_a,reg_b = tokens_to_asm(token.rhs,data,variables,reg_a,reg_b, pointer_counter)
            reg_a,reg_b = tokens_to_asm(token.block,data,variables,reg_a,reg_b, pointer_counter)
            data[1] += ["sta 0i","ldb 0i"]
            data[2] += [f"goto {pointer_counter}&"]
            sections[current_section_index] += data[1]
            sections[current_section_index] += data[0]
            if type(token.comparer) == EqualsToken:
                sections[current_section_index] += ["xor",f"giz {len(sections)}$", f"pointer {pointer_counter}"]
            elif type(token.comparer) == NotEqualsToken:
                sections[current_section_index] += ["xor",f"gnz {len(sections)}$", f"pointer {pointer_counter}"]
            sections.append(data[2])
            pointer_counter += 1
            reg_a,reg_b = None, None
        else:
            print(token)
    return reg_a, reg_b

def compile(token_block:BlockToken)->list[str]:
    class Instruction:
        def __init__(self, text, source):
            self.text = text
            self.source = source
        def __str__(self):
            return self.text+f"({self.source})"
        def __repr__(self):
            return self.__str__()
    sections = []
    variables = {}
    tokens_to_asm(token_block, sections, variables)
    asm:list[Instruction] = []

    for i in sections[0]:
        asm.append(Instruction(i,0))
    print(asm)
    asm.append(Instruction("hlt",0))
    for index, section in enumerate(sections[1:]):
        for i in section:
            asm.append(Instruction(i,index+1))
    index = -1
    pointers = {}
    section_jumps = {}
    while True:
        index += 1
        if index >= len(asm):
            break
        instruction = asm[index].text
        parts = instruction.split(" ")
        if parts[0] == "pointer":
            pointers[int(parts[1])] = index
            asm.remove(asm[index])
        elif len(parts) > 1 and parts[1].endswith("&"):
            new = pointers[int(parts[1][:-1])]
            asm[index] = Instruction(parts[0] + " " + str(new) + "i",asm[index].source)
        elif len(parts) > 1 and parts[1].endswith("$"):
            new = int(parts[1][:-1])
            section_jumps[index] = new
    
    for jump in section_jumps:
        dest = section_jumps[jump]
        count = 0
        for line in asm:
            if line.source == dest:
                break
            count += 1
        parts = asm[jump].text.split(" ")
        text = f"{parts[0]} {count}i"
        source = asm[jump].source
        asm[jump] = Instruction(text,source)
    print(asm)
    text = []
    for i in asm:
        text.append(i.text)
    return text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("no input file specified")
        quit()
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()
    tokens, _ = tokenize(code)
    print(tokens)
    asm = compile(tokens)
    with open("output/asm.txt","w") as f:
        f.write("\n".join(asm))
    assembler.assemble_and_run(asm)