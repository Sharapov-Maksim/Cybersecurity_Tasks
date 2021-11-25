""" Make signature of message
    :param messageFileName - file name with message to be signed
    :param secretKeyFileName - file name with secret key in such format:
        d - Integer
        n - Integer
"""
def sign(messageFileName, secretKeyFileName):
    print("Making signature...")
    # read secret key
    sec = open(secretKeyFileName, "r")
    d = int(sec.readline())
    n = int(sec.readline())
    # print("d: ", d)
    # print("n: ", n)
    sec.close()

    # The size of blocks on which the message will be divided
    # message block should be  < n  in integer representation
    size = (n.bit_length() - 1) // 8
    print("Block size: ", size)
    l = 1
    iteration = 0
    out = open("signature.txt", "w")
    with open(messageFileName, "rb") as inp:
        import time
        start = time.time()
        while l:
            # read message block
            inputMessage = bytearray(inp.read(size))  # 1024 bit
            l = len(inputMessage)
            if l == 0:
                break
            m = int.from_bytes(inputMessage, "big")
            assert m < n

            # print("Mesasge part:    ", m.to_bytes(((m.bit_length() + 7) // 8), "big"))
            signature = pow(m, d, n)  # coding message using secret key   s = m**d (mod n)
            # print("Coded message:   ", signature.to_bytes(((signature.bit_length() + 7) // 8), "big"))

            # store signature in file
            if iteration == 0:
                out.write(str(signature))
                iteration = 1
            else:
                out.write("\n" + str(signature))
        end = time.time()
        print("Signature done, elapsed time:  ", (end - start)*1000, "ms")



sign("message.txt", "secret.txt")

