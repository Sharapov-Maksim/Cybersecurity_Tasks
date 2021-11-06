p = 221646491259360846924446449467974137196269135310795762760598401423881532320757080865517022411802775025535426436954808071054998021163533966351277826569258309272730188460975994269145177351749921860925281281647786597284095409909392188916319636330360515308185670747545206248867358332285567253975332842485965863629
q = 273005130134403559070473518424878646663970688162147276887417662275020793562074646827725294670014418734105152077423134435580935187635681508708212033880355943595684279230918753887075618279728930945420112966991049683456226612300536913209566632835029274589202238240727516878338051142020966218922478331787711213611
#p = 3557
#q = 2579
n = p * q
fin = (p - 1) * (q - 1)  # Euler's function of n
e = 65537  # public exponent: gcd(e, fin) = 1
#e = 3

def gcd(a, b, x, y):
    if a == 0:
        return b, x, y
    d, x1, y1 = gcd(b % a, a, x, y)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y


# e*x + fin*y = gcd(e, fin) = 1
g, d, y = gcd(e, fin, 0, 1)
# e*d = 1 (mod fin)
assert ((e * d) % fin) == 1
# d - secret exponent
d = d % fin
publicKey = (e, n)
secretKey = (d, n)

print("n:   ", n)
print("fin: ", fin)
print("e:   ", e)
print("d:   ", d)
print("pk:  ", publicKey)
print("sk:  ", secretKey)

dp = d % (p-1)
dq = d % (q-1)
_, qinv, _ = gcd(q, p, 0, 1)
qinv = qinv % p
print("qinv ", qinv)
assert ((q * qinv) % p) == 1


def pad(plaintext):
    """
    Pads the given plaintext with zeroes to a multiple of 256 bytes.
    """
    padding_len = (256 - (len(plaintext) % 256)) % 256
    padding = bytes([0] * padding_len)
    return plaintext + padding




inp = open("message.txt", "rb")
inputMessage = bytearray(inp.read(256))  # 2048 bit
inputMessage = pad(inputMessage)
m = int.from_bytes(inputMessage, "big")
assert m < n
import time
start = time.time()
#m = 111111
print("Mesasge:         ", m.to_bytes(((m.bit_length() + 7) // 8), "big"))
codedmessage = (m ** e) % n  # coding message using public key

print("Coded message:   ", codedmessage.to_bytes(((codedmessage.bit_length() + 7) // 8), "big"))

# encoding with optimizations
m1 = (codedmessage ** dp) % p
m2 = (codedmessage ** dq) % q
h = 0
if m1 < m2:
    h = (qinv * ((m1 + (q//p)*p) - m2)) % p
else:
    h = (qinv * (m1 - m2)) % p
encodedmessage = (m2 + h*q) % n

print("Encoded message: ", encodedmessage.to_bytes(((encodedmessage.bit_length() + 7) // 8), "big"))

end = time.time()
print(end - start)
