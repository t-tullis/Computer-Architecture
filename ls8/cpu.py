"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [00000000] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0xF4
        self.branchtable = {}
        self.branchtable[0b00000001] = self.handleHLT
        self.branchtable[0b10000010] = self.handleLDI
        self.branchtable[0b01000111] = self.handlePRN
        self.branchtable[0b01000101] = self.handleStackPush
        self.branchtable[0b01000110] = self.handleStackPop

    def load(self):
        """Load a program into memory."""

        address = 0

        lines = None
        try:
            lines = open(sys.argv[1]).readlines()
        except FileNotFoundError:
            print(f"{sys.argv[1]} Not Found.")
            sys.exit(2)

        for line in lines:
            if line[0].startswith('0') or line[0].startswith('1'):
                self.ram[address] = int(line[:8], 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        ADD = 0b10100000
        SUB = 0b10100001
        MUL = 0b10100010
        DIV = 0b10100011
        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == DIV:
            if not self.reg[reg_b]:
                print("Error: You are not allowed to divide a number by 0.")
                sys.exit()
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def handleHLT(self):
        print('Process Ending.')
        sys.exit()

    def handleLDI(self, operand_1, operand_2):
        self.reg[operand_1] = operand_2

    def handlePRN(self, operand_1):
        print(self.reg[operand_1])

    def handleStackPush(self, operand_1):
        self.sp -= 1
        reg_value = self.reg[operand_1]
        self.ram[self.sp] = reg_value

    def handleStackPop(self, operand_1):
        ram_value = self.ram[self.sp]
        self.reg[operand_1] = ram_value
        self.sp += 1

    def run(self):
        """Run the CPU."""
        on = True

        while on:
            IR = self.ram[self.pc]

            # get next two MDR's from the next two MAR's stored in ram incase instructions need it
            operand_1 = self.ram_read(self.pc + 1)
            operand_2 = self.ram_read(self.pc + 2)

            operand_count = (IR & 0b11000000) >> 6
            alu_number = (IR & 0b00100000) >> 5
            if alu_number:
                self.alu(IR, operand_1, operand_2)
            elif operand_count == 2:
                self.branchtable[IR](operand_1, operand_2)
            elif operand_count == 1:
                self.branchtable[IR](operand_1)
            elif operand_count == 0:
                self.branchtable[IR]()
            else:
                self.handleHLT()
            self.pc += 1
            self.pc += operand_count
