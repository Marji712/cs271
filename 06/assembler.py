import os, sys

#Get file to copy and name of copy
asmIn = input("What file do you want to read in (.asm)?")
hackOut = input("What do you want to name your output file (.hack)?")

#Copy file to new hack file
from shutil import copyfile
copyfile(asmIn, hackOut)

#dictionary for mem locations
locations = {
    "@SP": "000",
    "@LCL": "001",
    "@ARG": "010",
    "@THIS": "011",
    "@THAT": "100",
    "@SCREEN": "100000000000000",
    "@KBD": "110000000000000",
    "@R0": "000",
    "@R1": "001",
    "@R2": "010",
    "@R3": "011",
    "@R4": "100",
    "@R5": "101",
    "@R6": "110",
    "@R7": "111",
    "@R8": "1000",
    "@R9": "1001",
    "@R10": "1010",
    "@R11": "1011",
    "@R12": "1100",
    "@R13": "1101",
    "@R14": "1110",
    "@R15": "1111"
    }


#dictionary for comp bits
comp = {
    "0": "1110101010",
    "1": "1110111111",
    "-1": "1110111010",
    "D": "1110001100",
    "A": "1110110000",
    "!D": "1110001101",
    "!A": "1110110001",
    "-D": "1110001111",
    "-A": "1110110011",
    "D+1": "1110011111",
    "A+1": "1110110111",
    "D-1": "1110001110",
    "A-1": "1110110010",
    "D+A": "1110000010",
    "D-A": "1110010011",
    "A-D": "1110000111",
    "D&A": "1110000000",
    "D|A": "1110010101",
    "M": "1111110000",
    "!M": "1111110001",
    "-M": "1111110011",
    "M+1": "1111110111",
    "M-1": "1111110010",
    "D+M": "1111000010",
    "D-M": "1111010011",
    "M-D": "1111000111",
    "D&M": "1111000000",
    "D|M": "1111010101"
    }

#dictionary for dest bits
dest = {
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }

#dictionary for jump bits
jump = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }



#control program for first pass
#removes extras
#checks for labels
def firstPass():
    #use copied file, make a temp file for changes
    infile = open(hackOut)
    outfile = open('temp.tmp', "w")

    #read through each line
    currentLine = 0
    for line in infile:
        noExtras = removeExtras(line)
        if noExtras != "":
            if noExtras[0] == "(":
                label = noExtras[1:-1]
                address = "{0:b}".format(currentLine)                
                locations['@' + label] = str(address)
                noExtras = ""
            else:
                currentLine +=1
                outfile.write(noExtras + "\n")

    #close files
    infile.close()
    outfile.close()


#remove comments, blank lines, and whitespace
def removeExtras(line):
    firstChar = line[0]
    if firstChar == "/" or firstChar == "\n":
        return ""
    elif firstChar == " ":
        return removeExtras(line[1:])
    else:
        return firstChar + removeExtras(line[1:])


#control program for second pass
#translates instructions
def secondPass():
    #use copied file, make a temp file for changes
    infile = open('temp.tmp')
    outfile = open(hackOut, "w")
    
    #read through each line
    for line in infile:
        translation = instruction(line)
        outfile.write(translation + "\n")
    

    #close files
    infile.close()
    outfile.close()
    #delete temp file
    os.remove('temp.tmp')


#decide if line is an a-instruction or a c-instruction
def instruction(line):
    if line[0] == "@":
        return aInstruct(line)
    else:
        return cInstruct(line)

varCount = 1

#translate an a-instruction
def aInstruct(line):
    cleanLine = line.split('\n')
    temp = cleanLine[0]
    address = locations.get(temp)


    if address is None:
        if temp[1].isalpha():
                global varCount
                variable = temp
                address = "{0:b}".format(15 + varCount)                
                locations[variable] = str(address)
                varCount += 1
                
        else:
            cleanLine = cleanLine[0].split('@')
            temp = cleanLine[1]
            intAdd = int(temp)
            binAdd = "{0:b}".format(intAdd)                
            address = str(binAdd)

    return address.zfill(16)

def cInstruct(line):
    cleanLine = line.split('\n')
    equalSplit = cleanLine[0].split("=")
    
    if "=" in line:
        destBits = dest.get(equalSplit[0])
        compBits = comp.get(equalSplit[1])
    else:
        destBits = "000"

    if ";" in line:
        jumpSplit = cleanLine[0].split(";")
        compBits = comp.get(jumpSplit[0])
        jumpBits = jump.get(jumpSplit[1])
    else:
        jumpBits = "000"

        
    trans = compBits + destBits + jumpBits
      
    return trans




firstPass()
secondPass()


