# Aztec² CPU
The Aztec² is a homebrew computer using a load-store architecture, using a RISC-like instruction set.
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
