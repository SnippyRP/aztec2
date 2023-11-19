# Aztec² CPU
The Aztec² is an 8-bit homebrew computer using a load-store architecture, using a RISC-like instruction set. It has a 16-bit address bus. The circuit was originally made in [Logisim Evolution](https://github.com/logisim-evolution/logisim-evolution), and is being built in real life!

## Instruction Set

    (0000) 0: NOP (No operation, skip)
    (0001) 1: AW (Add word to register. Can also copy register values to another register) (reg = const8/reg)
    (0010) 2: LW (Load word from RAM to reg destination. This instruction takes register C as the low address, and register D as the bank.)
    (0011) 3: SW (Store the word from reg source into RAM. This instruction takes register C as the low address, and register D as the bank.)
    (0100) 4: RW (Load word from the OS ROM into the reg destination. This instruction takes register C as the low address, and register D as the bank.)
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

## Registers
Registers are places to temporarily store data on the CPU, and should not be used as a fill-in alternative to RAM. Some registers are overwritten by the CPU passivly, and are outlined here.

    (000) Register A
    (001) Register B
    (010) Register C
    (011) Register D
    (100) Flags Register
    (101) Register H
    (110) Register L
    (111) Instruction register

<br>

**General Purpose Register A (0)**
<br>
A general purpose register for computing normal operations
<br>

**General Purpose Register B (1)**
<br>
A general purpose register for computing normal operations
<br>

**General Purpose Register C (2)**
<br>
A general purpose register for computing normal operations
<br>

**General Purpose Register D (3)**
<br>
A general purpose register for computing normal operations
<br>

**Flags Register (4)**
<br>
ALU will output the flags of an arithmatic operation here. Data from here can be copied over to the general-purpose registers, and other operations can be done. This register is automatically overwritten, and should not be used in normal operations.

*USAGE*

    (MSB TO LSB)
    CARRY OUT
    BORROW OUT
    A > B
    A = B
    A < B

<br>

**High Address Register (5)**
<br>
The high end of the address BUS, made to access more RAM/ROM. Also known as the memory bank register. This register is frequently updated passivly by the CPU, and should not be used normally. Incrementing this register by 1 increases the address BUS by 255, giving a total of 65535 bytes of ROM/RAM. Combining these gives us a total of 131070 bytes of memory.
<br>

**Low Address Register (5)**
<br>
The low end of the address BUS. Incrementing this by 1 increments the address BUS by 1, AKA the LSB part. This is overwritten by the CPU on every instruction, and should not be manually used for operations.
<br>

**Instruction Register (6)**
<br>
This register is the most important part of the CPU, and is mostly used by the CPU to handle register operations and store the current executing instruction. Attempting to write to this register may brick the entire system, and a reset would be required. May be useful for some advanced diagnostic programs.

*USAGE*

    (MSB TO LSB)
    OPCODE
    ISREG
    DESTINATION REG

## Detailed Documentation

  **NOP (0)**
<br>
A placeholder operation meant to fill space. Useful for padding, delays, and cleaning up a program.

    00000000
    
<br>
 
**AW (1)**
<br>
Inserts a byte into a specified register, or copy a value from one register to another. The source/insertion byte comes directly after the instruction byte.
*CONST:*

    ; Add 48 into register B
    
    0001 0 001
    01001000
*COPY*

    ; Copy the value of register B to register A
    
    0001 1 000
    00000 001

<br>

**LW (2)**
<br>
Used to load a byte from the RAM into the specified register in the instruction. This instruction takes the value inside **register C** as the low address byte, and **register D** as the memory bank to read from. ( C+(D*255) )

    ; Load the value from RAM address 514 into register A
    
    ; Load 4 into register C
    0001 0 010
    00000100
    
    ; Load 2 into register D
    0001 0 011
    00000010
    
    ; Load the value from RAM into register A
    0010 1 000

<br>

**SW (3)**
<br>
Used to store the value in a specified register to the RAM. The reason why there is no option to directly load a constant is that it would effectivly be reading the value from program ROM into a register, before immediatly being rewritten into RAM. This instruction takes the value inside **register C** as the low address byte, and **register D** as the memory bank to read from. ( C+(D*255) )

    ; Save the value from register B into RAM address 692

    ; Load 182 into register C
    0001 0 010
    10110110

    ; Load 2 into register D
    0001 0 011
    00000010

    ;Save register B into RAM
    0011 1 001

<br>

**RW (4)**
<br>
Like LW, this instruction works the same, except that it reads the byte in ROM. The ROM can be thought of as a hard-disk, and things such as files and the OS can be stored here. This instruction takes the value inside **register C** as the low address byte, and **register D** as the memory bank to read from. ( C+(D*255) )

    ; Load ROM address 764 into register B

    ; Load 254 into register C
    0001 0 010
    11111110

    ; Load 2 into register D
    0001 0 011
    00000010

    ; Load ROM into reg B
    0100 1 001

<br>

**JNZ (5)**
<br>
Change the program counter if **destination register** != 0 or constant value else NOP. This instruction is the main part of any conditional/unconditional loop you may add. It can be used in a FOR loop, a WHILE loop, or a full unconditional loop if you set a const value to anything other than 0. This instruction takes register C as the low pointer, and register D as the high pointer.

*USING A REGISTER*

    ; Jump to byte 14 in ROM unconditionally

    ; Write 1 to register A
    0001 0 000
    00000001

    ; Write 14 to register C
    0001 0 010
    0001110

    ; Write 0 to register D
    0001 0 011
    00000000

    ; JNZ
    0101 1 000


*USING A CONSTANT*

    ; Jump to byte 28 in ROM unconditionally

    ; Write 28 to register C
    0001 0 010
    00011100

    ; Write 0 to register D
    0001 0 011
    00000000

    ; JNZ (reg not used)
    0101 1 000
    0000001

<br>

**ADD (6)**
<br>
Adds the contents of the destination register with the source register value or a constant value, and outputs the result into the destination register.

* *A conditional loop of addition can be used to create multiplication In x\*y, loop add 0 by x y times.*

*REGISTER*

    ; Add the value of register A with register B

    0110 1 000
    00000 001

*CONSTANT*

    ; Add register B and 25

    0110 0 001
    00011001

<br>

**SUB (7)**
<br>
Subtracts the contents of the destination register with the source register value or a constant value, and outputs the result into the destination register.
* Since floating-point arithmetic and signed numbers are not supported nativly, subtracting a larger number will cause the byte to roll over into 255.

*REGISTER*

    ; Subtract the value of register A with register B

    0111 1 000
    00000 001

*CONSTANT*

    ; Subtract register B and 25

    0111 0 001
    00011001

<br>

**ADC (8)**
<br>
Adds the contents of the destination register with the source register value or a constant value, and outputs the result into the destination register. As well as the two registers, it takes the value from the **flags register** and loads it into the ALU. If the *carry-in* bit is a 1, it will add 1 to the result. It has all of the same options as *ADD*.

* You can use multiple *ADC* operations to do arithmetic on numbers larger than 255, by using two or more registers and consecutivly adding the carry bit. For example, using two registers to store a 16-bit number maxes out at 65,535


*REGISTER*

    ; Add the value from register A with register B, and use the carry bit.

    1000 1 000
    00000 001

*USAGE*

    ; Add 24000 by 1000, by splitting that 16-bit number after the 8th bit.

    ; Load 192 into register A
    0001 0 000
    00011110

    ; Load 93 into register B
    0001 0 001
    01011110

    ; Add register A by 232
    1000 0 000
    11101000

    ; Add register B by 3
    1000 0 001
    00000011

    ; Now you have 25000 represented in register A and B. Bytes in register B become the MSB's, and register A is LSB's.

<br>

**SBB (9)**
<br>
The same as *ADC*, except it does subtraction, and uses the *borrow-in* bit inside of the *flags register* instead of *carry-in*. Using the same principle, you can do division, and that allows you to do more complex operations. IT subtracts the contents of the destination register with the source register value or a constant value, and outputs the result into the destination register.

    ; Subtract register A with register B, and subtract the borrow-in bit.

    1001 1 000
    00000 001

<br>

**NOR (A)**
<br>
Performs bitwise NOR operation on either the destination and source register, or the destination register and a constant value. Works best with register-register operations.

*EXAMPLE*

    10100101
    10000001
    ========
    01011010

<br>

*REGISTER*

    ; Bitwise NOR operation on register A and register B

    1010 1 000
    00000 001

<br>

**BSL (B)**
<br>
Performs logical left bit-shift operation on either the destination and source register, or the destination register and a constant value. Works best with register-register operations.

* **Shift-amount only works for the three LSB's of the byte!**

*EXAMPLE*

    10100101
    00000010
    ========
    10010100

<br>

*REGISTER*

    ; Left-shift operation on register A and register B

    1011 1 000
    00000 001

<br>

**BSR (C)**
<br>
Performs logical right bit-shift operation on either the destination and source register, or the destination register and a constant value. Works best with register-register operations.

* **Shift-amount only works for the three LSB's of the byte!**

*EXAMPLE*

    10100101
    00000011
    ========
    00010100

<br>

*REGISTER*

    ; Right-shift operation on register A and register B

    1100 1 000
    00000 001

<br>

**CMP (D)**
<br>
Compares the destination register with either the source register or a constant value, and outputs to the **flags register**. This is the main part of a conditional loop, where you can bit-shift it left to get the desired bit, then use JNZ. For example, you could perform a NOT operation using a NOR operation, then shift it left and run a *JNZ* instruction.

*CONSTANT*

    ; Compare register A with 25 and move it into register A

    1101 0 000
    00011001

    ; Copy value
    0001 1 000
    00000 100

*REGISTER*

    ; Compare register B with register C

    1101 1 001
    00000 010

<br>

**INB (E)**
<br>
Reads the input port and write the data to the destination register.

* This instruction can be used to interface with a keyboard, and to handle input to the computer.

*USAGE*

    ; Read keyboard to register B

    1110 1 001

<br>

**OUTB (F)**
<br>
Reads the destination register or constant value from ROM and writes the value to the output port for one clock pulse, **not full instruction!!** This can be used to run a terminal output, or a TTL display.

* A graphics card does not run on the output port, instead hooks directly onto the RAM, and has it's own VRAM and clock process.

*USAGE*

    ; Write register A to the output port, for a TTL display.

    1111 1 000

## Microcode
Microcode is not used by a program, but instead is used by the CPU in order to control itself. These simply toggle parts of the CPU, and are all 1-bit in length, except for the reg selections. Custom instructions can be created using more microcode.

    Reads, writes, extras, reg sel 0, reg sel 1

    READS:
        0001: READ REG
        0010: READ MEMORY
        0011: READ ROM
        0100: READ COUNTER LOW
        0101: READ COUNTER HIGH
        0110: READ ALU
        0111: READ FLAGS
        1000: READ PORT

    WRITES:
        0001: WRITE REG
        0010: WRITE MEMORY
        0011: WRITE COUNTER
        0100: LOADX
        0101: LOADY
        0110: WRITE PORT
    EXTRAS:
        01: ENABLE COUNTER
        10: EI

    REG SEL 0/1:
        000: Register definied inside of the instruction register
        001: Register decoded from current ROM reading (Assumed to be reading from RAM/ROM like second byte)
        010: Register C
        > .. and the rest of the registers after.
    
    (REG_SEL_0 means what to write too, and REG_SEL_1 is what to read from.)
    <read> <write> <extra> <sel0> <sel1>

## Assembly and Macros
Macros can be used to perform multiple instructions when programming faster. Programs written with macros will be easier to understand, but be less efficient than simply writing using assembly.

**Usage**

Machine code for the CPU can be automatically written using a version of assembly I created. This current version is a very crude python program, and I plan to expand on this later. You follow the same instructions as outlined in the instruction set.

For example, to load 60 into register A, you would write:

    aw a, 60

The code follows the same structure as writing through pure machine code. It uses \<instruction> \<destination> \<source>.
If an instruction only has one argument, it can be written like this:

    outb 87

When writing a program, you can create a comment if a line starts with a semicolon (;).

If you would like to see more example programs before writing your own, see the 'examples' directory.

**Manual Compilation**

If you would like to compile a program manually, without using the compiler, you need to simply write out the machine code bytes, as stated in the instruction set documentation. Then to insert that into the program ROM, simply convert it into hexadecimal. I like to use the website https://www.rapidtables.com/convert/number/binary-to-hex.html to convert easily. Once you have converted all your binary, list the program byte by byte into a text file. Once done, right-click the ROM and select "load image". This will bring up a file selection window. Simply select your file and choose "v2.0 raw".

**Macros**

One of the big reasons to use a compiler is the use of macros. A macro is like pasting a wall of instructions into your code with custom variables. For example, multiplication is not native to the CPU hardware. You can easily implement it by using the *mul* macro. Macros should not be treated as a stand-in for writing assembly, and can currently produce unexpected behaviour. All macros currently use base-10. Keep in mind that this is currently being worked on, and some unexpected behaviour can come from this. If you happen to write a fix, please share it with me ;-)

    ; multiply register A with register B
    mul a, b

    ; multiply register A with 6
    mul a, 6

Here are all the currently usable macros:

    goto <ln>
    goto if <reg/const> <comp> <reg/const> <ln>
    define <vname> <val>
    load <addr> <reg/const>
    store <reg> <addr> (assembly should be used if programmably interacting with memory)
    mul <reg> <reg/const>

<br>

**goto**

The *goto* macro makes the program jump unconditionally to whatever line in the program you want.

    goto 5

<br>

**gotoif**

The *gotoif* macro jumps the program to thwtaver line in the program only if the conditional is met.

* You can use '<', '==', '>', '!=' as functioning comapritors

* **This macro will overwrite a lot of the registers, so save any data you need into RAM before running!**

<br>

    gotoif 5 < 4, 0

    gotoif a == 5, 62

<br>

**define**
The *define* macro is used to define a variable. Unlike most other *good* languages, a variable cannot be changed later in the program, and can only be defined once. It can be either a register or a constant value, and can be used in both instructions and macros.
* When using a variable, it must start with a '#' in the instruction.

<br>

    define x, 5
    define y, 4

    aw a, #x
    aw b, #y

    mul a, b

    ; or do

    aw a, #x
    mul a, #y

<br>

**load**
<br>
*Load* can be used to easily load a constant address into a register. When you need to programmably use memory, it is more efficient to use regular assembly, so that has not been implemented. Same goes for *save*.

* This instruction will overwrite some registers, so be careful!

<br>

    load a, 6

<br>

**store**
<br>
*Store* can be used to easily save the value of a constant value or the value in a register to a constant RAM address. When you need to programmably use memory, it is more efficient to use regular assembly, so that has not been implemented.

* This instruction will overwrite some registers, so be careful!

<br>

    save 50, a
    save 51, 0

<br>

**mul**
<br>
*Mul* is used like any normal arithmatic instruction. It will multiply any register with either another register or a constant value, and outout into the destination register. Can also be used with variables.

* This operation will overwrite pretty much every register, along with the first few spots inside of RAM. This is like a *for* loop of repeated addition, and has to store the loop index, current number, coefficient A, and if using two registers, coefficient B.

* Using *mul* will also use up a lot of the disk, and is around 44 bytes long. It may also take up a lot of time, depending on clock rate.

<br>

    mul a, b

    ; or

    mul a, 6
