import math
import sys

from bitstring import BitArray

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: python decompress.py input output")
        exit(0)

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    inputBinArray = BitArray(filename=inputFile).bin

    lastIndexOf1 = inputBinArray.rindex("1")
    inputBinArray = inputBinArray[:lastIndexOf1]

    index = 0
    increment = 1
    keyDictionary = {0: ''}
    output = BitArray()

    prefixNull = False

    while True:
        key = ''
        sizeOfKey = math.ceil(math.log2(len(keyDictionary)))

        if index + sizeOfKey >= len(inputBinArray):
            if index < len(inputBinArray):
                output.append("0b" + inputBinArray[index:])
            break

        if sizeOfKey > 0:

            pos = int(inputBinArray[index: index + sizeOfKey], 2)
            if pos >= len(keyDictionary):
                if index < len(inputBinArray):
                    output.append("0b" + inputBinArray[index:])
                break

            prefix = keyDictionary[pos]
            if prefix != '':
                key = prefix
                output.append("0b" + prefix)
            else:
                if inputBinArray[index + sizeOfKey] in keyDictionary.values():
                    prefixNull = True

        if prefixNull:
            output.append("0b" + inputBinArray[(index + sizeOfKey):])
            break
        else:
            output.append("0b" + inputBinArray[index + sizeOfKey])
            key += inputBinArray[index + sizeOfKey]
            keyDictionary[len(keyDictionary)] = key

        index += sizeOfKey + 1

    print("input: " + str(len(inputBinArray)))
    # print(inputBinArray)

    print("output: " + str(len(output.bin)))
    # print(output.bin)

    output.tofile(open(outputFile, 'wb'))
