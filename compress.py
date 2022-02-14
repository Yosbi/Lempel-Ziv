import math
import sys

from bitstring import BitArray

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: python compress.py input output")
        exit(0)

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    inputBinArray = BitArray(filename=inputFile).bin
    index = 0
    increment = 0
    keyDictionary = {'': 0}
    output = BitArray()

    while True:
        if index + increment > len(inputBinArray):
            if len(inputBinArray[index:]) > 0:
                sizeOfKey = math.ceil(math.log2(len(keyDictionary)))
                for j in range(sizeOfKey):
                    output.append('0b0')
                for b in inputBinArray[index:]:
                    output.append(bin(int(b, 2)))
            output.append('0b1')
            break

        candidateKey = inputBinArray[index: index + increment]

        if candidateKey in keyDictionary:
            increment += 1
        else:
            sizeOfKey = math.ceil(math.log2(len(keyDictionary)))

            if len(output) > 0:
                if len(candidateKey) == 1:
                    for i in range(sizeOfKey):
                        output.append('0b0')
                else:
                    storedKey = bin(keyDictionary[inputBinArray[index: index + (increment - 1)]])[2:]

                    for j in range((sizeOfKey - len(storedKey))):
                        output.append('0b0')
                    output.append(bin(int(storedKey, 2)))

            output.append("0b" + candidateKey[len(candidateKey) - 1:])

            keyDictionary[candidateKey] = len(keyDictionary)
            index += increment
            increment = 1

    print("input: " + str(len(inputBinArray)))
    #print(inputBinArray)
    print("output: " + str(len(output.bin)))
    #print(output.bin)

    output.tofile(open(outputFile, 'wb'))
