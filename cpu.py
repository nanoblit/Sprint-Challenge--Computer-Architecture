"""CPU functionality."""

import sys

hlt = 0b00000001
ldi = 0b10000010
prn = 0b01000111
add = 0b10100000
mul = 0b10100010
push = 0b01000101
pop = 0b01000110
call = 0b01010000
ret = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.registers = [0] * 8

        self.branchtable = {
           hlt : self.handle_hlt,
           ldi : self.handle_ldi,
           prn : self.handle_prn,
           add : self.handle_add,
           mul : self.handle_mul,
           push : self.handle_push,
           pop : self.handle_pop,
           call : self.handle_call,
           ret : self.handle_ret
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        program = []

        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if len(num) == 0:
                        continue
                    value = int(num, 2)
                    program.append(value)

        except FileNotFoundError:
            print(f"{filename} not found")
            sys.exit(2)

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_hlt(self, operand_a, operand_b):
        sys.exit(0)

    def handle_ldi(self, operand_a, operand_b):
        self.registers[operand_a] = operand_b

    def handle_prn(self, operand_a, operand_b):
        print(self.registers[operand_a])

    def handle_add(self, operand_a, operand_b):
        self.registers[operand_a] +=  self.registers[operand_b]

    def handle_mul(self, operand_a, operand_b):
        self.registers[operand_a] *=  self.registers[operand_b]

    def handle_push(self, operand_a, operand_b):
        reg = operand_a
        val = self.registers[reg]
        # move stack pointer
        self.registers[7] -= 1
        # set value in sp position in ram to val 
        self.ram[self.registers[7]] = val

    def handle_pop(self, operand_a, operand_b):
        reg = operand_a
        val = self.ram[self.registers[7]]
        # set value in given register to val from stack
        self.registers[reg] = val
        # move stack pointer
        self.registers[7] += 1 

    def handle_call(self, operand_a, operand_b):
        # move stack pointer
        self.registers[7] -= 1
        # set top value in stack to the position to return
        self.ram[self.registers[7]] = self.pc + 2
        # set pc to the position stored in register
        self.pc = self.registers[operand_a]

    def handle_ret(self, operand_a, operand_b):
        # store top value from the stack in pc
        self.pc = self.ram[self.registers[7]] 
        # move stack pointer
        self.registers[7] += 1

    def run(self):
        """Run the CPU."""

        self.registers[7] = 0xF3

        while True:
            ir = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            ops_to_skip = 0
            if ir != call and ir != ret:
                ops_to_skip = (ir >> 6) + 1

            self.branchtable[ir](operand_a, operand_b)
            
            self.pc += ops_to_skip
