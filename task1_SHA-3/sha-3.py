# output length: 256 bits
b = 1600
l = 6
nrounds = 24
blockSize = 1088
capacity = b - blockSize
file = open('big_input.txt', 'rb')
inputMessage = bytearray(file.read())
print("Size of input: " + str(len(inputMessage)) + " Bytes")

# Adding padding
paddingNumber = blockSize - (len(inputMessage)*8 % blockSize)  # count of bits to add
if paddingNumber == 0:
    inputMessage.append(l)
    for i in range(1, blockSize//8 - 1):
        inputMessage.append(0b00000000)
    inputMessage.append(0x80)
elif paddingNumber == 8:
    inputMessage.append(l ^ 0x80)
elif paddingNumber == 16:
    inputMessage.append(l)
    inputMessage.append(0x80)
else:
    inputMessage.append(l)
    for i in range(1, paddingNumber // 8 - 1):
        inputMessage.append(0b00000000)
    inputMessage.append(0x80)

blocksNum = (len(inputMessage)*8) // blockSize
# Round constants
RC = [0 for i in range(24)]
RC[0]  = 0x0000000000000001
RC[1]  = 0x0000000000008082
RC[2]  = 0x800000000000808A
RC[3]  = 0x8000000080008000
RC[4]  = 0x000000000000808B
RC[5]  = 0x0000000080000001
RC[6]  = 0x8000000080008081
RC[7]  = 0x8000000000008009
RC[8]  = 0x000000000000008A
RC[9]  = 0x0000000000000088
RC[10] = 0x0000000080008009
RC[11] = 0x000000008000000A
RC[12] = 0x000000008000808B
RC[13] = 0x800000000000008B
RC[14] = 0x8000000000008089
RC[15] = 0x8000000000008003
RC[16] = 0x8000000000008002
RC[17] = 0x8000000000000080
RC[18] = 0x000000000000800A
RC[19] = 0x800000008000000A
RC[20] = 0x8000000080008081
RC[21] = 0x8000000000008080
RC[22] = 0x0000000080000001
RC[23] = 0x8000000080008008

# Rotation offsets
r = [[0,36,3,41,18],
     [1,44,10,45,2],
     [62,6,43,15,61],
     [28,55,25,21,56],
     [27,20,39,8,14]]

def rot(a, shift, N = 64):
                          # a=  |111001|    shift = 1
    b = a << shift        #    1|110010|
    m = 1 << N            #    1|000000|
    c = b % m             #    0|110010|
    d = a >> (N - shift)  #     |000001|(11001)
    res = c | d           #     |110011|
    return res


def f(A, iterations_number = 24):
    for iteration in range(0, iterations_number):
        # step theta
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
    block = [block[i:21+i:5] for i in range(0, 5)]
    if blockId != 0:
        for i in range(5):
            for j in range(5):
                state[i][j] ^= block[i][j]
    else:
        state = block
    state = f(state)

res = 0
for i in range(4):
    res |= state[i][0] << (i * 64)
print("Result:")
print(res.to_bytes(32, "little").hex())


