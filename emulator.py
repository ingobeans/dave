def binary_to_int(binary:str)->int:
    return int(binary, 2)

def int_to_binary(number:int)->str:
    return '{0:08b}'.format(number)[:8]

class Dave:
    def __init__(self):
        self.ram = ["00000000" for _ in range(32)]
        self.reg_a = "00000000"
        self.reg_b = "00000000"
        self.program_counter = 0
    def execute(self, binary:list[str], step:bool):
        try:
            print(chr(27) + "[2J", flush=True)
            while True:
                instruction = binary[self.program_counter]
                self.program_counter += 1
                opcode = instruction[:8]
                operand = instruction[8:]

                old_ram = self.ram.copy()
                old_reg_a = self.reg_a
                old_reg_b = self.reg_b
                old_program_counter = self.program_counter

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

                if old_ram != self.ram or old_reg_a != self.reg_a or old_reg_b != self.reg_b or old_program_counter != self.program_counter:
                    print(chr(27) + "[H", flush=False)
                    print("\n".join(self.ram[:8]), flush=False)
                    print(f"\n{self.reg_a=}\t{self.reg_b=}\t{self.program_counter=}", flush=False)
                    print("",flush=True)
                if step:
                    input(chr(27) + "[H")
                    print(chr(27) + "[2J", flush=True)
        except KeyboardInterrupt:
            print(chr(27) + "[H", flush=False)
            print(chr(27) + "[2J", flush=True)