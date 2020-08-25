'''

    This script that takes a bitmap and outputs a header file that can be used
    with AVR microcontrollers 8bit. 

    usage: python bmp2image.py image.bmp
    output: output.h

'''

import sys
import struct

#Open our input file which is defined by the first commandline argument
#then dump it into a list of bytes
infile = open(sys.argv[1],"rb") #b is for binary
contents = bytearray(infile.read())
infile.close()

#Get the size of this image
data = [contents[2], contents[3], contents[4], contents[5]]
fileSize = struct.unpack("I", bytearray(data))

print("Size of file:", fileSize[0])

#Get the width of this image
data = [contents[18], contents[19], contents[20], contents[21]]
imageWidth = struct.unpack("I", bytearray(data))

print("Image width:", imageWidth[0])

#Get the height of this image

data = [contents[22], contents[23], contents[24], contents[25]]
imageHeight = struct.unpack("I", bytearray(data))

print("Image Height:", imageHeight[0])

#Get header offset amount
data = [contents[10], contents[11], contents[12], contents[13]]
offset = struct.unpack("I",bytearray(data))

print("Offset:", offset[0])

#Get number of colors. i.e. 2 from mtpaint
data = [contents[46], contents[47], contents[48], contents[49]]
colorsUsed = struct.unpack("I",bytearray(data))

print("Number of colors used:", colorsUsed[0]);

#Determine starting data for image
startOfDefinitions = offset[0]

#for i in range(offset[0], fileSize[0]):
#    print(contents[i])

verticalBanks = int(imageHeight[0]/8 - 1)
print("Total Vertical Banks for 8-bit:", verticalBanks)

totalArray = imageWidth[0] * (verticalBanks+1)
print("Total Array Length in C:",totalArray)

outputString = "/* This is generated" + '\r'
outputString += "static const unsigned char myGraphic[" + str(totalArray) + "] PROGMEM = {" + '\r\t'

buf = 0x00

bank = 1
count = 0

for z in range(fileSize[0], offset[0], -imageWidth[0]*bank*8):
    for y in range(0,imageWidth[0]):
        index = z + y
        for x in range(0,8):
            buf = (buf | (contents[index - imageWidth[0]*bank] << x))
            bank += 1
        #print("{0:#0{1}x}".format(buf,4))
        #print(hex(buf))
        outputString += "{0:#0{1}x}".format(buf,4) + ", "
        count += 1
        if count % 16 == 0:
            outputString += '\r\t'
        buf = 0x00
        bank = 1

#Remove last space and ','
outputString = outputString[:-2]
outputString += "};"

# Write the output to a file
outfile = open("output.h","w")
outfile.write(outputString)
outfile.close()

print("output.h complete!!")

