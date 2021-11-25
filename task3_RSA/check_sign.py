""" Check signature of message
    :param messageFileName - file name with message to be signed
    :param publicKeyFileName - file name with secret key in such format:
        e - Integer
        n - Integer
    :param signatureFileName - file name with signatures of message blocks
"""
def check(messageFileName, publicKeyFileName, signatureFileName):
    print("Checking message...")
    # read public key
    pub = open(publicKeyFileName, "r")
    e = int(pub.readline())
    n = int(pub.readline())
    # print("e: ", e)
    # print("n: ", n)
    pub.close()

    # The size of blocks on which the message was divided
    # message block should be  < n  in integer representation
    size = (n.bit_length() - 1) // 8
    print("Block size: ", size)


    messageFile = open(messageFileName, "rb")
    import time
    start = time.time()
    iscorrect = 1
    with open(signatureFileName, "r") as signatureFile:
        l = 1
        while l:
            # reading block signature
            sign = signatureFile.readline()  # 1024 bit
            l = len(sign)
            if l == 0:
                break
            s = int(sign)

            # encode block   m' = s**e (mod n)
            encoded = pow(s, e, n)

            # check if corresponding message block is correct
            realMessage = messageFile.read(size)
            messageInt = int.from_bytes(realMessage, "big")
            if encoded != messageInt:
                iscorrect = 0
                break

    end = time.time()
    print("Signature is checked, elapsed time:  ", (end - start) * 1000, "ms")

    if iscorrect:
        print("Message is correct!")
        return 0
    else:
        print("Message is not correct!")
        return 1


check("message.txt", "public.txt", "signature.txt")
