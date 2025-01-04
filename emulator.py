def binary_to_int(binary:str)->int:
    return int(binary, 2)

def int_to_binary(number:int)->str:
    return '{0:07b}'.format(number)

class Dave:
    def __init__(self):
        self.ram = ["00000000" for _ in range(32)]
        self.reg_a = "00000000"
        self.reg_b = "00000000"
        self.program_counter = 0
    def execute(self, binary:list[str]):
        while True:
            instruction = binary[self.program_counter]
            self.program_counter += 1
            opcode = instruction[:8]
            operand = instruction[8:]
            match opcode:
                case "00000000": #nop
                    pass
                case "00000001": #lda
                    self.reg_a = self.ram[binary_to_int(operand)]
                case "00000010": #ldb
                    self.reg_b = self.ram[binary_to_int(operand)]
                case "00000011": #sta
                    self.ram[binary_to_int(operand)] = self.reg_a
                case "00000100": #stb
                    self.ram[binary_to_int(operand)] = self.reg_b
                case "00000101": #add
                    self.reg_a = int_to_binary(binary_to_int(self.reg_a) + binary_to_int(self.reg_b))
                case "00000110": #sub
                    self.reg_a = int_to_binary(binary_to_int(self.reg_a) - binary_to_int(self.reg_b))
                case "00000111": #mul
                    self.reg_a = int_to_binary(binary_to_int(self.reg_a) * binary_to_int(self.reg_b))
                case "00001000": #div
                    self.reg_a = int_to_binary(binary_to_int(self.reg_a) / binary_to_int(self.reg_b))
                case "00001001": #goto
                    self.program_counter = binary_to_int(operand)
                case "00001010": #giz
                    if self.reg_a == "00000000":
                        self.program_counter = binary_to_int(operand)
                case "00001011": #gnz
                    if self.reg_a != "00000000":
                        self.program_counter = binary_to_int(operand)
                case "00001101": #wra
                    self.reg_a = operand
                case "00001110": #wrb
                    self.reg_b = operand
                case "00010000": #and
                    self.reg_a = int_to_binary(binary_to_int(self.reg_a) & binary_to_int(self.reg_b))
                case "00010001": #or
                    self.reg_a = int_to_binary(binary_to_int(self.reg_a) | binary_to_int(self.reg_b))
                case "00010010": #xor
                    self.reg_a = int_to_binary(binary_to_int(self.reg_a) ^ binary_to_int(self.reg_b))
                case "00010011": #nand
                    raise NotImplementedError
                case "00010100": #nor
                    raise NotImplementedError
                case "00010101": #xnor
                    raise NotImplementedError
                case "00010110": #shr
                    self.reg_a = self.reg_a[7] + self.reg_a[:7]
                case "00010111": #shl
                    self.reg_a = self.reg_a[1:8] + self.reg_a[0]
                case "11111111": #hlt
                    print("done!")
                    break
                case _:
                    print(f"instruction {opcode} doesnt exist")
                    quit()
