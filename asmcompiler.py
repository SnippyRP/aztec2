import re
import math

# fix random instr map subtractions

opcodes = {
    "nop":"0000",
    "aw":"0001",
    "lw":"0010",
    "sw":"0011",
    "rw":"0100",
    "jnz":"0101",
    "add":"0110",
    "sub":"0111",
    "adc":"1000",
    "sbb":"1001",
    "nor":"1010",
    "bsl":"1011",
    "bsr":"1100",
    "cmp":"1101",
    "inb":"1110",
    "outb":"1111"
}

regs = {
    "a":"000",
    "b":"001",
    "c":"010",
    "d":"011",
    "flags":"100",
    "h":"101",
    "l":"110",
    "in":"111"
}

macros = {"goto","gotoif","define","load","store","mul"}

variables = {}

file = ""
for line in open("programs/mtest.txt","r").readlines():
    if not ";" in line:
        file += line

program = re.sub(",", "", file).replace("\n"," ").lower()

print(program)

instr = ""
current = None
ii = 0

tokens = program.split(" ")

def getHL(num: int):
    H = math.floor(num/256)
    L = num-(H*256)
    return H,L



print(tokens)

# initial run

instrmap = {}

tn = 0
for index,token in enumerate(tokens):
    if token in opcodes:
        if opcodes[token] in ["0000","0010","0011","0100","1110"]:
            tn += 1
        elif opcodes[token] in ["0001","1111","0110","0111","1000","1001","1010","1011","1100","1101","0101"]:
            tn += 2
        instrmap[ii] = tn
        ii += 1
    if token in macros:
        if token == "goto":
            tn += 6
        if token == "gotoif":
            if tokens[index+2] == "!=": # to invert
                tn += 19
            else:
                tn += 17
        if token == "define":
            varname = tokens[index+1]
            varitem = tokens[index+2]
            if varitem.isdigit():
                variables[varname] = varitem
            elif varitem in regs:
                variables[varname] = varitem

        if token in ["load","store"]:
            if tokens[index+1].isdigit():
                tn += 7
            else:
                tn += 5
        if token == "mul":
            if tokens[index+1].isdigit():
                tn += 42
            else:
                tn += 46
        instrmap[ii] = tn
        ii += 1

def buildArgs(start,len):
    uses = tokens[start:start+len]
    argstable = []
    num = 0
    for a in uses:
        if num >= len:
            return argstable
        if a in regs or a.isdigit() or a in ["==","<",">","!="]:
            argstable.append(a)
            num += 1
        elif a.startswith("#"): # variable
            print(variables)
            if a[1:] in variables:
                argstable.append(variables[a[1:]])
                num += 1
        else:
            pass
    return argstable

bytecount = 0

for index,token in enumerate(tokens):
    if token in opcodes:
        if opcodes[token] == "0000":
            instr += "00000000" + "\n"
            bytecount += 1
        if opcodes[token] == "0001":
            instr += opcodes[token]

            args = buildArgs(index+1,2)

            isreg = not args[1].isdigit()
            instr += str(int(isreg))
            instr += regs[args[0]] + "\n"
            if isreg:
                instr += "00000" + regs[args[1]] + "\n"
            else:
                instr += str(bin(int(args[1]))[2:]) + "\n"

            bytecount += 2

        if opcodes[token] in ["0010","0011","0100","1110"]:
            instr += opcodes[token]

            args = buildArgs(index+1,1)
            instr += "1" + regs[args[0]] + "\n"

            bytecount += 1

        if opcodes[token] in ["1111"]:
            instr += opcodes[token]

            args = buildArgs(index+1,1)

            isreg = not args[0].isdigit()
            instr += str(int(isreg))
            if isreg:
                instr += regs[args[0]] + "\n"
            else:
                instr += "000\n"
                instr += str(bin(int(args[0]))[2:]) + "\n"

            bytecount += 2

        if opcodes[token] in ["0110","0111","1000","1001","1010","1011","1100","1101"]:

            instr += opcodes[token]

            args = buildArgs(index+1,2)

            isreg = not args[1].isdigit()
            instr += str(int(isreg))
            instr += regs[args[0]] + "\n"
            if isreg:
                instr += "00000" + regs[args[1]] + "\n"
            else:
                instr += str(bin(int(args[1]))[2:]) + "\n"

            bytecount += 2
        
        if opcodes[token] in ["0101"]:
            instr += opcodes[token]

            args = buildArgs(index+1,1)
            isreg = not args[0].isdigit()
            instr += str(int(isreg))
            if isreg:
                instr += regs[args[0]] + "\n"
                bytecount += 1
            else:
                instr += "000\n"
                instr += str(bin(int(args[0]))[2:]) + "\n"
                bytecount += 2

            

    

    if token in macros:
        if token == "goto":
            args = buildArgs(index+1,1)
            if len(args) == 1:
                ins = int(args[0])
                high, low = getHL(ins)
                if high in instrmap and low in instrmap:
                    mappedh, mappedl = instrmap[high]-2, instrmap[low]-2
                    print(mappedh,mappedl)
                    # add numbers into registers and jump
                    # add low byte
                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += str(bin(mappedl)[2:]) + "\n"

                    # add high byte
                    instr += opcodes["aw"] + "0" + regs["d"] + "\n"
                    instr += str(bin(mappedh)[2:]) + "\n"

                    # unconditional jump
                    instr += opcodes["jnz"] + "0000" + "\n"
                    instr += "1" + "\n"

                    bytecount += 6
                else:
                    print("[ERROR]: No instruction '{}' found in script!".format(args[0]))

            else:
                print("[ERROR]: Macro {} received a malformed argument".format(token))

        if token == "gotoif":

            args = buildArgs(index+1,4)
            
            if len(args) == 4:
                a = args[0]
                comp = args[1]
                b = args[2]
                ins = int(args[3])
                high, low = getHL(ins)

                areg = not a.isdigit()
                breg = not b.isdigit()

                if high in instrmap and low in instrmap and comp in ["<","==",">","!="]:
                    mappedh, mappedl = instrmap[high]-2, instrmap[low]-3
                    print(mappedh, mappedl)


                    # add A and B into their respective registers
                    if areg:
                        instr += opcodes["aw"] + "1" + regs["a"] + "\n"
                        instr += regs[a] + "\n"
                    else:
                        instr += opcodes["aw"] + "0" + regs["a"] + "\n"
                        instr += str(bin(int(a))[2:]) + "\n"
                    

                    if breg:
                        instr += opcodes["aw"] + "1" + regs["b"] + "\n"
                        instr += regs[b] + "\n"
                    else:
                        instr += opcodes["aw"] + "0" + regs["b"] + "\n"
                        instr += str(bin(int(b))[2:]) + "\n"


                    # run a compare
                    instr += opcodes["cmp"] + "1" + regs["a"] + "\n"
                    instr += regs["b"] + "\n"

                    # copy flags data
                    instr += opcodes["aw"] + "1" + regs["a"] + "\n"
                    instr += regs["flags"] + "\n"

                    # bit-shift to single out bit
                    if comp == "<":
                        instr += opcodes["bsl"] + "0" + regs["a"] + "\n"
                        instr += "100" + "\n"
                    elif comp == "==":
                        instr += opcodes["bsl"] + "0" + regs["a"] + "\n"
                        instr += "11" + "\n"
                    elif comp == ">":
                        instr += opcodes["bsl"] + "0" + regs["a"] + "\n"
                        instr += "10" + "\n"
                    elif comp == "!=":
                        instr += opcodes["nor"] + "1" + regs["a"] + "\n"
                        instr += regs["a"] + "\n"

                        instr += opcodes["bsl"] + "0" + regs["a"] + "\n"
                        instr += "11" + "\n"

                    instr += opcodes["bsr"] + "0" + regs["a"] + "\n"
                    instr += "111" + "\n"

                    # add numbers into registers and jump
                    # add low byte

                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += str(bin(mappedl)[2:]) + "\n"

                    # add high byte
                    instr += opcodes["aw"] + "0" + regs["d"] + "\n"
                    instr += str(bin(mappedh)[2:]) + "\n"

                    # jump
                    instr += opcodes["jnz"] + "1000" + "\n"

                    if comp == "!=":
                        bytecount += 19
                    else:
                        bytecount += 17
                else:
                    print("[ERROR]: No instruction '{}' found in script!".format(args[0]))

            else:
                print("[ERROR]: Macro {} received a malformed argument".format(token))

        if token in ["load","store"]: # destination, source 
            args = buildArgs(index+1,2)

            if len(args) == 2:
                if token == "store":
                    ins = int(args[0])

                    src = args[1]

                    cmd = "sw"
                else:
                    ins = int(args[1])

                    src = args[0]

                    cmd = "lw"

                high, low = getHL(ins)

                instr += opcodes["aw"] + "0" + regs["d"] + "\n"
                instr += str(bin(int(high))[2:]) + "\n"

                instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                instr += str(bin(int(low))[2:]) + "\n"

                if src.isdigit():
                    instr += opcodes["aw"] + "0" + regs["a"] + "\n"
                    instr += str(bin(int(src))[2:]) + "\n"

                    instr += opcodes[cmd] + "1" + regs["a"] + "\n"
                    bytecount += 7
                else:
                    if src in regs:
                        instr += opcodes[cmd] + "1" + regs[src] + "\n"
                        bytecount += 5
                    else:
                        print("[ERRPR]: No source found for {}".format(token))
            else:
                print("[ERROR]: Macro {} received a malformed argument".format(token))

        # here we go again!
        if token == "mul":
            args = buildArgs(index+1,2)
            if len(args) == 2:
                # begin
                isreg = not args[1].isdigit()
                src = args[1]
                dest = args[0]

                instr += opcodes["aw"] + "0" + regs["d"] + "\n"
                instr += "0" + "\n"
                instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                instr += "10" + "\n"
                instr += opcodes["sw"] + "1" + regs[dest] + "\n"

                if isreg:
                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += "11" + "\n"
                    instr += opcodes["sw"] + "1" + regs[src] + "\n"
                
                instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                instr += "0" + "\n"
                instr += opcodes["aw"] + "0" + regs["a"] + "\n"
                instr += "0" + "\n"
                instr += opcodes["sw"] + "1" + regs["a"] + "\n"
                instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                instr += "1" + "\n"
                instr += opcodes["sw"] + "1" + regs["a"] + "\n"
                # loop
                instr += opcodes["aw"] + "0" + regs["d"] + "\n"
                instr += "0" + "\n"
                instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                instr += "10" + "\n"
                instr += opcodes["lw"] + "1" + regs["b"] + "\n"
                instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                instr += "1" + "\n"
                instr += opcodes["lw"] + "1" + regs["a"] + "\n"
                instr += opcodes["add"] + "1" + regs["a"] + "\n"
                instr += regs["b"] + "\n"
                instr += opcodes["sw"] + "1" + regs["a"] + "\n"

                if isreg:
                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += "11" + "\n"
                    instr += opcodes["lw"] + "1" + regs["a"] + "\n"

                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += "0" + "\n"
                    instr += opcodes["lw"] + "1" + regs["b"] + "\n"
                else:
                    instr += opcodes["aw"] + "0" + regs["a"] + "\n"
                    instr += str(bin(int(src))[2:]) + "\n"
                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += "0" + "\n"
                    instr += opcodes["lw"] + "1" + regs["b"] + "\n"
                
                instr += opcodes["add"] + "0" + regs["b"] + "\n"
                instr += "1" + "\n"
                instr += opcodes["sw"] + "1" + regs["b"] + "\n"
                instr += opcodes["sub"] + "1" + regs["a"] + "\n"
                instr += regs["b"] + "\n"

                if isreg:
                    high, low = getHL(bytecount+16)
                    #print(str(bin(int(low))[2:]))
                    instr += opcodes["aw"] + "0" + regs["d"] + "\n"
                    instr += str(bin(int(high))[2:]) + "\n"
                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += str(bin(int(low))[2:]) + "\n"
                    instr += opcodes["jnz"] + "1" + regs["a"] + "\n"
                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += "1" + "\n"
                    instr += opcodes["lw"] + "1" + regs[dest] + "\n"

                    bytecount += 36
                else:
                    high, low = getHL(bytecount+14)
                    instr += opcodes["aw"] + "0" + regs["d"] + "\n"
                    instr += str(bin(int(high))[2:]) + "\n"
                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += str(bin(int(low))[2:]) + "\n"
                    instr += opcodes["jnz"] + "1" + regs["a"] + "\n"
                    instr += opcodes["aw"] + "0" + regs["c"] + "\n"
                    instr += "1" + "\n"
                    instr += opcodes["lw"] + "1" + regs[dest] + "\n"

                    bytecount += 32


final = ""
print(instr)
for ins in instr.rstrip().split("\n"):
    final += hex(int(ins, 2))[2:] + "\n"
open("compiled.txt","w").write(final)
#print(instr)
