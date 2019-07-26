import string, random, binascii, base64, zlib

from plugin_aes import *

#characters = string.ascii_letters + string.digits + string.punctuation
#characters = string.ascii_letters + string.digits

class miarma_crypto():

    def __init__(self, internal_seed, seed_negotiation, password_xor):
        self.characters = string.printable
        self.characters_to_encode = string.ascii_letters + string.digits

        self.internal_seed = internal_seed
        #self.key = key
        self.password_xor = password_xor
        self.seed_negotiation = seed_negotiation

        self.end_seed = self.internal_seed + self.seed_negotiation
        random.seed(self.end_seed)
        self.depth=random.randrange(3, 7)
        #self.cipher = AESCipher(self.key)

        def string_dictionary():
            dic_translate = {}
            for c in self.characters:
                p =  "".join(random.sample(self.characters_to_encode,self.depth))
                dic_translate[c] = p
                dic_translate[p] = c
            dic_translate["depth"] = self.depth
            return dic_translate

        self.dic_translate = string_dictionary()

    def string_dictionary_encode(self, s_message):
        encode_message = ""
        for s in s_message:
            encode_message = encode_message + self.dic_translate[s]
        return encode_message

    def change_to_be_hex(self, string_str):
        return int(string_str.encode().hex(),base=16)

    def xor_two_str(self, str1, str2):
        a = self.change_to_be_hex(str1)
        b = self.change_to_be_hex(str2)
        return hex(a ^ b)

    def xor_hex_str(self, hex1, str2):
        b = self.change_to_be_hex(str2)
        return hex(hex1 ^ b)

    def int_hex_to_str(self, int_hex):
        return bytes.fromhex(hex(int_hex)[2:]).decode()

    def hex_to_str(self, input_hex):
        return bytes.fromhex(input_hex[2:]).decode()

    def mutant_str(self, encode_message):
        to_mutant = ""
        index_pass = 0
        for s in encode_message:
            to_mutant = to_mutant + ":" + self.xor_two_str(s,str(self.password_xor[index_pass]))[2:]
            index_pass += 1
            if index_pass >= len(self.password_xor):
                index_pass = 0
        return base64.b64encode(zlib.compress(to_mutant[1:].encode("utf-8"))).decode()

    def mutant_to_normal(self, muntant_input):
        to_normal = ""
        index_pass = 0
        m_input = zlib.decompress(base64.b64decode(muntant_input + '=' * (-len(muntant_input) % 4))).decode()
        for h in m_input.split(":"):
            p1 = str(self.password_xor[index_pass])
            to_normal = to_normal + self.hex_to_str(self.xor_hex_str(int(h, 16),p1))
            index_pass += 1
            if index_pass >= len(self.password_xor):
                index_pass = 0
        return to_normal

    def string_dictionary_decode(self, encode_message):
        decode_message = ""
        depth = self.dic_translate["depth"]
        for index in range(int(len(encode_message)/depth)):
            init_string = index*depth
            encode_character = encode_message[init_string:init_string+depth]
            decode_message = decode_message + self.dic_translate[encode_character]
        return decode_message

