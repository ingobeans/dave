import keyboard, time, color

def binary_to_int(binary:str)->int:
    return int(binary, 2)

def int_to_binary(number:int)->str:
    if number < 0:
        number = 255
    return '{0:08b}'.format(number)[:8]

class Device:
    def __init__(self):
        pass
    def write(self, byte:str, pos:str):
        pass
    def read(self, pos)->str:
        pass
    def display(self)->str|None:
        pass

class Ram(Device):
    def __init__(self):
        self.data = ["00000000" for _ in range(16)]
    def write(self, byte:str, pos:str):
        self.data[binary_to_int(pos)] = byte
    def read(self, pos)->str:
        return self.data[binary_to_int(pos)]
    def display(self)->str|None:
        not_empty = any([not all([c == "0" for c in b]) for b in self.data])
        if not_empty:
            return "\n\t"+"\n\t".join(self.data)

class Screen(Device):
    def __init__(self):
        self.data = ["0000000000000000" for _ in range(8)]
        self.displayed_data = ["0000000000000000" for _ in range(8)]
    def write(self, byte:str, pos:str):
        x = binary_to_int(byte[1:5])
        y = 7-binary_to_int(byte[5:8])
        write = byte[0]
        if write == "1":
            self.displayed_data = self.data.copy()
            self.data = ["0000000000000000" for _ in range(8)]
        else:
            if y >= 0 and y < 8 and x >= 0 and x < 16:
                self.data[y] = self.data[y][:x] + "1" + self.data[y][x + 1:]
    def read(self, pos)->str:
        state = "00000000"
        is_a_pressed = keyboard.is_pressed("a")
        is_d_pressed = keyboard.is_pressed("d")
        if is_a_pressed:
            state = state[:6] + "1" + state[6 + 1:]
        if is_d_pressed:
            state = state[:7] + "1" + state[7 + 1:]
        return state
    def display(self)->str|None:
        return "\n\t"+"\n\t".join([text.replace("1","█").replace("0",color.blue("█")) for text in self.displayed_data])

class Dave:
    def __init__(self):
        self.devices:list[Device] = {
            0: Ram(), 
            1: Ram(),
            7: Screen()
        }
        self.reg_a = "00000000"
        self.reg_b = "00000000"
        self.program_counter = 0
    def execute(self, binary:list[str], step:bool, only_screen=True, time_per_instruction=0.0055):
        try:
            print(chr(27) + "[2J", flush=True)
            while True:
                if self.program_counter >= len(binary):
                    print("reached end of file!")
                    break
                instruction = binary[self.program_counter]
                self.program_counter += 1
                opcode = instruction[8:]
                operand = instruction[:8]

                # used for devices
                device_pos, data_pos = binary_to_int(operand[:4]), operand[4:]

                match opcode:
                    case "00000000": #nop
                        pass
                    case "00000001": #lda
                        self.reg_a = self.devices[device_pos].read(data_pos)
                    case "00000010": #ldb
                        self.reg_b = self.devices[device_pos].read(data_pos)
                    case "00000011": #sta
                        self.devices[device_pos].write(self.reg_a, data_pos)
                    case "00000100": #stb
                        self.devices[device_pos].write(self.reg_b, data_pos)
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
                        
                print(chr(27) + "[H", flush=False)
                
                if not only_screen:
                    for index, device in enumerate(self.devices):
                        display = self.devices[device].display()
                        if display:
                            print(f"device {index}: {display}", flush=False)
                    print(f"\n{self.reg_a=}\t{self.reg_b=}\t{self.program_counter=}", flush=False)
                    print("",flush=True)
                else:
                    print(f"{self.devices[7].display()}")
                    print(chr(27) + "[H", flush=True)
                if step:
                    input(chr(27) + "[H")
                    print(chr(27) + "[2J", flush=True)
                if time_per_instruction > 0:
                    time.sleep(time_per_instruction)
        except KeyboardInterrupt:
            print(chr(27) + "[H", flush=False)
            print(chr(27) + "[2J", flush=True)