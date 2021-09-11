

# output length: 256 bits
b = 1600
nrounds = 24
blockSize = 1088
capacity = b - blockSize
file = open('input.txt', 'rb')
inputMessage = file.read()
print('Input Message: ', inputMessage)
inputBits = []
for i in range(0, len(inputMessage)):
    byte = format(inputMessage[i], '08b')
    inputBits.extend([int(b) for b in byte])

# Adding padding
inputBits.append(1)
paddingNumber = blockSize - (len(inputBits) % blockSize)
for i in range(0, paddingNumber-1):
    inputBits.append(0)
inputBits.append(1)

blocksNum = len(inputBits) // blockSize

def f(state, iterations_number = 24):
    for iteration in range(0, iterations_number):


for blockId in range (0, blocksNum):
    block = inputBits[blockId * blockSize : (blockId+1) * blockSize]

