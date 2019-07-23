"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # hold 256 bytes of memory
        self.ram = [0] * 256
        #8 general-purpose registers.
        self.register = [0] * 8
        #Program Counter
        self.pc = 0
    

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
    
    # should accept the address to read and return the value stored there.
    def ram_read(self,MAR):
        return self.ram[MAR]
    
    #  should accept a value to write, and the address to write it to.
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

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

    def run(self):
        """Run the CPU."""
        running = True 

        #Instructions
        
        #Halt the CPU (and exit the emulator).
        HLT = 0b00000001
        #Set the value of a register to an integer.
        LDI = 0b10000010
        #Print to the console the decimal integer value that is stored in the given register.
        PRN = 0b01000111

        while running:

            IR = self.ram[self.pc]

            # get next two MDR's from the next two MAR's stored in ram incase instructions need it
            #Argument 1
            operand_a = self.ram_read(self.pc + 1)
            #Argument2
            operand_b = self.ram_read(self.pc + 2)

            #If Insturction Register == HLT exit the emulator, turning true to false and move to next instruction
            if IR == HLT:
                running = False
                self.pc += 1

            #Else if Instruction Register == LDI Set the value of a register[operand_a] to a operand_b/integer. 
            elif IR == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
            
            #Else if Instruction Register == PRN print to the console the decimal integer value of  register[operand_a]
            elif IR == PRN:
                print(self.register[operand_a])
                self.pc += 2

            else:
                print(f"Command {IR} Not Found")
        


