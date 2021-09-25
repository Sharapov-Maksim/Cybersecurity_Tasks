

# output length: 256 bits
b = 1600
l = 6
nrounds = 24
blockSize = 1088
capacity = b - blockSize
file = open('input.txt', 'rb')
inputMessage = bytearray(file.read())
y = int.from_bytes(inputMessage[0:8], "big", signed=True)


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
    inputMessage.join(bytes([l]))
    for i in range(1, blockSize//8 - 1):
        inputMessage.join(bytes([0b00000000]))
    inputMessage.join(bytes([0x80]))
elif paddingNumber == 8:
    inputMessage.join(bytes([l ^ 0x80]))
elif paddingNumber == 16:
    inputMessage.join(bytes([l, 0x80]))
else:
    inputMessage.append(l)
    for i in range(1, paddingNumber // 8 - 1):
        inputMessage.append(0b00000000)
    inputMessage.append(0x80)

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

def rot(a, shift, N = 2**l):
                          # a=  |111001|    shift = 1
    b = a << shift        #    1|110010|
    m = 1 << N            #    1|000000|
    c = b % m             #    0|110010|
    d = a >> (N - shift)  #     |000001|(11001)
    res = c | d           #     |110011|
    return res

r = [[0,36,3,41,18],
     [1,44,10,45,2],
     [62,6,43,15,61],
     [28,55,25,21,56],
     [27,20,39,8,14]]

def f(A, iterations_number = 24):
    for iteration in range(0, iterations_number):
        # step theta
        '''
        for i in range(5):
            for j in range(5):
                for k in range(2**l):
                    for n in range(5):
                        A[i][j] ^= (A[n][(j-1)%5] & (1<<k)) ^ (A[n][(j+1)%5] & (1<<((k-1)%5)))
        '''
        C = []
        for x in range(5):
            C.append(A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4])
        D = [0, 0, 0, 0, 0]
        for x in range(5):
            D[x] = C[(x-1)%5] ^ rot(C[(x+1)%5], 1)
        for x in range(5):
            for y in range(5):
                A[x][y] ^= D[x]

        # step rho + pi  ( << (t+1)(t+2)//2 )
        B = []
        for i in range(5):
            B.append([0,0,0,0,0])

        for x in range(5):
            for y in range(5):
                B[y][(2*x+3*y)%5] = rot(A[x][y], r[x][y])

        '''
        tmp = [[A[0][0],0,0,0,0]]
        for r in range(4):
            tmp.append([0,0,0,0,0])
        i = 1
        j = 0
        for t in range(24):
            tmp[i][j] = rot(A[i][j], ((t+1)*(t+2)//2) % 2**l)
            #for k in range(2**l):
            #    tmp[i][j] |= (((A[i][j] & (1<<((k - (t+1)*(t+2)//2) % 2**l))) >> ((k - (t+1)*(t+2)//2) % 2**l)) << k)
            iprev = i
            i = (3*i + 2*j) % 5
            j = iprev
        # step pi
        for x in range(5):
            for y in range(5):
                A[y][(2*x+3*y)%5] = tmp[x][y]
        '''
        # step chi
        for x in range(5):
            for y in range(5):
                A[x][y] = B[x][y] ^ ((~B[(x+1)%5][y]) & B[(x+2)%5][y])
        # step iota
        A[0][0] ^= RC[iteration]
    return A

state = []
for blockId in range (0, blocksNum):
    blockBytes = inputMessage[blockId * (blockSize // 8) : (blockId+1) * (blockSize // 8)]
    block = []
    for start in range(0, blockSize//8, 8):
        block.append(int.from_bytes(blockBytes[start : start+8], "little", signed=False))
    for start in range(blockSize//8, b//8, 8):
        block.append(0)
    #lanes = [[load64(state[8 * (x + 5 * y):8 * (x + 5 * y) + 8]) for y in range(5)] for x in range(5)]
    block = [block[i:21+i:5] for i in range(0, 5)]
    if blockId != 0:
        for i in range(5):
            for j in range(5):
                state[i][j] ^= block[i][j]
    else:
        state = block
    #print("Before f: ", state)
    state = f(state)
    #print("After  f: ", state)

res = 0
for i in range(4):
    res |= state[i][0] << i * 64

print(res.to_bytes(32, "little").hex())


