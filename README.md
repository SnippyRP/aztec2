# Aztec² CPU
The Aztec² is an 8-bit homebrew computer using a load-store architecture, using a RISC-like instruction set. It has a 16-bit address bus.
## Instruction Set

    (0000) 0: NOP (No operation, skip)
    (0001) 1: AW (Add word to register. Can also copy register values to another register) (reg = const8/reg)
    (0010) 2: LW (Load word from RAM to reg destination. This instruction takes register C as the low address, and register D as the bank.)
    (0011) 3: SW (Store the word from reg source into RAM. This instruction takes register C as the low address, and register D as the bank.)
    (0100) 4: PW (Load word from the OS ROM into the reg destination. This instruction takes register C as the low address, and register D as the bank.)
    (0101) 5: JNZ (Change the program counter if register != 0 else NOP. This instruction takes register C as the low pointer, and register D as the high pointer.)

    (0110) 6: ADD  (Add reg source with the secondary register and output that to the reg source)
    (0111) 7: SUB  (Subtract reg source with the secondary register and output that to the reg source)
    (1000) 8: ADC^ (Add reg source with the secondary register, add carry bit and output that to the reg source)
    (1001) 9: SBB^ (Subtract reg source with the secondary register, subtract borrow bit and output that to the reg source)
    (1010) A: NOR  (Perform NOR bitwise operation on reg source with secondary register, then output into reg source)
    (1011) B: AND  (Perform AND bitwise operation on reg source with secondary register, then output into reg source)
    (1100) C: OR   (Perform OR bitwise operation on reg source with secondary register, then output into reg source)
    (1101) D: CMP  (Compare destination reg with source register, output to flags register)

    (1110) E: INB  (Write the contents of the input port to the register destination)
    (1111) F: OUTB (Output the contents of the destination register to the out port)

    All instructions are destinatiom, source
    <instr> <isreg> <destination>; <source reg/const8>
## Detailed Documentation


  **NOP (0)**
  <br>
A placeholder operation meant to fill space. Useful for padding, delays, and cleaning up code.

    00000000
    
 <br>
 
**AW (1)**
<br>
Inserts a byte into a specified register, or copy a value from one register to another. The source/insertion byte comes directly after the instruction byte.
*CONST:*

    ; Add 0x48 into register B
    
    0001 0 001
    01001000
*COPY*

    ; Copy the value of register B to register A
    
    0001 1 000
    00000 001

<br>

**LW (2)**
<br>
Used to load a byte from the RAM into the specified register in the instruction. This instruction takes the value inside **register C** as the low address byte, and **register D** as the memory bank to read from. (C+(D*255))

    ; Load the value from RAM address 0x514 into register A
    
    ; Load 0x4 into register C
    0001 0 010
    00000100
    
    ; Load 0x2 into register D
    0001 0 011
    00000010
    
    ; Load the value from RAM into register A
    0010 0 000
