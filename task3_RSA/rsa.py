""" RSA initialization: set public and secret keys """
def rsa_init(publicFileName, secretFileName):
    print("Initializing rsa...")
    # Choosing 2 prime numbers p and q:
    p = 604424354465196281578544170172516377491513712443224792637274658347440736801958602247528489203210233452194556480402322929292105483955112388824995578322577395734883251144371410139198325854452545849312385073763544513769636523659914401960387533632577510604647281699762952873830087985457147770237082350921
    q = 899284973317613602866022377802431491438733114656833986256209267731293981780927220619771010231794286681104658280072645513892027246919727680816246681493053271364918476487460629906444052808847224382461481805049314875632613250827173866201827000796045982243648949063524704178185987094109926965067856414119
    # n = pq  - used as the modulus
    n = p * q
    fin = (p - 1) * (q - 1)  # Euler's function of n
    e = 65537  # public exponent: gcd(e, fin) = 1

    # Extended Euclidean algorithm
    def gcd(a, b, x, y):
        if a == 0:
            return b, x, y
        d, x1, y1 = gcd(b % a, a, x, y)
        x = y1 - (b // a) * x1
        y = x1
        return d, x, y

    # e*x + fin*y = gcd(e, fin) = 1
    g, d, _ = gcd(e, fin, 0, 1)  # d == x
    assert g == 1  # gcd == 1
    assert ((e * d) % fin) == 1  # e*d = 1 (mod fin)
    # d - secret exponent
    d = d % fin

    # now public and secret keys are generated
    publicKey = (e, n)
    secretKey = (d, n)

    print("n:   ", n)
    print("fin: ", fin)
    print("e:   ", e)
    print("d:   ", d)
    print("pk:  ", publicKey)
    print("sk:  ", secretKey)

    # store keys to files
    pub = open(publicFileName, "w")
    sec = open(secretFileName, "w")
    pub.writelines([str(e) + '\n', str(n)])
    sec.writelines([str(d) + '\n', str(n)])


rsa_init("public.txt", "secret.txt")
