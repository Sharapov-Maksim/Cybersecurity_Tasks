""" Test rsa-based digital signature """
from rsa import rsa_init
from make_signature import sign
from check_sign import check

# Initialize RSA
rsa_init("public.txt", "secret.txt")

""" Small test """
print("\nSmall test")
# Make signature
sign("message.txt", "secret.txt")

# Check if message matches with signature
assert check("message.txt", "public.txt", "signature.txt") == 0


""" Big test """
print("\nBig test")
# Make signature
sign("big_message.txt", "secret.txt")

# Check if message matches with signature
assert check("big_message.txt", "public.txt", "signature.txt") == 0
