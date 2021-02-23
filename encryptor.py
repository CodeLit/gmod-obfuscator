def str_xor(s1, s2):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(s1, s2)])

# somecode = 'asdfln3j34tnonfdkjnflksdfnla'
# message = 'this is my message'
# encoded = str_xor(message, somecode)
# decoded = str_xor(encoded, somecode)
# print(encoded)
# print(decoded)
