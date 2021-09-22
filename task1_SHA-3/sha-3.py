

# output length: 256 bits
b = 1600
l = 6
nrounds = 24
blockSize = 1088
capacity = b - blockSize
file = open('input.txt', 'rb')
inputMessage = bytearray(file.read())
print('Input Message: ', inputMessage.__class__)
#x = int(inputMessage[0:2], 10)
y = int.from_bytes(inputMessage[0:8], "big", signed=True)
print(bin(inputMessage[0]) + ' ' + bin(inputMessage[1])[2:])

print(bin(y))

'''
inputBits = []
for i in range(0, len(inputMessage)):
    byte = format(inputMessage[i], '08b')
    inputBits.extend([int(b) for b in byte])
'''
print(len(inputMessage)*8)
# Adding padding
paddingNumber = blockSize - (len(inputMessage)*8 % blockSize)  # count of bits to add
print(paddingNumber)
if paddingNumber == 0:
    inputMessage.join(bytes([0b10000000]))
    for i in range(1, blockSize//8 - 1):
        inputMessage.join(bytes([0b00000000]))
    inputMessage.join(bytes([0b00000001]))
elif paddingNumber == 8:
    inputMessage.join(bytes([0b10000001]))
elif paddingNumber == 16:
    inputMessage.join(bytes([0b10000000, 0b00000001]))
else:
    inputMessage.append(0b10000000)
    for i in range(1, paddingNumber // 8 - 1):
        inputMessage.append(0b00000000)
    inputMessage.append(0b00000001)

print(len(inputMessage)*8)
blocksNum = (len(inputMessage)*8) // blockSize
print(blocksNum)
print(inputMessage)

RC = []
RC.append(0x0000000000000001)
RC.append(0x0000000000008082)
RC.append(0x800000000000808A)
RC.append(0x8000000080008000)
RC.append(0x000000000000808B)
RC.append(0x0000000080000001)
RC.append(0x8000000080008081)
RC.append(0x8000000000008009)
RC.append(0x000000000000008A)
RC.append(0x0000000000000088)
RC.append(0x0000000080008009)
RC.append(0x000000008000000A)
RC.append(0x000000008000808B)
RC.append(0x800000000000008B)
RC.append(0x8000000000008089)
RC.append(0x8000000000008003)
RC.append(0x8000000000008002)
RC.append(0x8000000000000080)
RC.append(0x000000000000800A)
RC.append(0x800000008000000A)
RC.append(0x8000000080008081)
RC.append(0x8000000000008080)
RC.append(0x0000000080000001)
RC.append(0x8000000080008008)


def f(A, iterations_number = 24):
    for iteration in range(0, iterations_number):
        # step theta
        for i in range(5):
            for j in range(5):
                for k in range(2**l):
                    for n in range(5):
                        A[i][j] ^= (A[n][(j-1)%5] & (1<<k)) ^ (A[n][(j+1)%5] & (1<<((k-1)%5)))
        # step rho  ( << (t+1)(t+2)//2 )

        tmp = [[A[0][0],0,0,0,0]]
        for r in range(4):
            tmp.append([0,0,0,0,0])
        i = 1
        j = 0
        for t in range(24):
            for k in range(2**l):
                tmp[i][j] |= (((A[i][j] & (1<<((k - (t+1)*(t+2)//2) % 2**l))) >> ((k - (t+1)*(t+2)//2) % 2**l)) << k)
            iprev = i
            i = (3*i + 2*j) % 5
            j = iprev
        # step pi
        for x in range(5):
            for y in range(5):
                A[y][(2*x+3*y)%5] = tmp[x][y]
        # step chi
        for x in range(5):
            for y in range(5):
                tmp[x][y] = A[x][y] ^ (~A[(x+1)%5][y] & A[(x+2)%5][y])
        A = tmp
        # step iota
        A[0][0] ^= RC[iteration]

    return A

state = []
for blockId in range (0, blocksNum):
    blockBytes = inputMessage[blockId * (blockSize // 8) : (blockId+1) * (blockSize // 8)]
    block = []
    for start in range(0, blockSize//8, 8):
        block.append(int.from_bytes(inputMessage[start : start+8], "big", signed=False))
    for start in range(blockSize//8, b//8, 8):
        block.append(0)
    block = [block[i:i+5] for i in range(0, 25, 5)]
    if blockId != 0:
        for i in range(5):
            for j in range(5):
                state[i][j] ^= block[i][j]
    else:
        state = block
    print("Before f: ", state)
    state = f(state)
    print("After  f: ", state)

res = 0
for i in range(4):
    res |= state[0][i] << (3-i) * 64

print(res.to_bytes(32, "big").hex())




