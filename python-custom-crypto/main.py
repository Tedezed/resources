import string, random, binascii, base64, zlib

from plugin_aes import *

#characters = string.ascii_letters + string.digits + string.punctuation
#characters = string.ascii_letters + string.digits

characters = string.printable
characters_to_encode = string.ascii_letters + string.digits
depth=random.randrange(3, 7)

message = "Hola Mundo!"
key = "sxeunsofvqazcsohutwezaqcqqehklxa"
password_xor = "67438yrg4yu8g3gfy34ugr7834yurg84t67587hu786hghg76tr57g"

cipher = AESCipher(key)

def string_recurvive(characters, old_character, depth):
    if depth >= 0:
        depth = depth - 1
        for s in range(len(characters)):
            string_recurvive(characters, old_character + characters[s], depth)
    else:
        print(old_character)

#string_recurvive(characters, "", depth)

def string_dictionary(characters, characters_to_encode, depth):
    dic_translate = {}
    for c in characters:
        p =  "".join(random.sample(characters_to_encode,depth))
        dic_translate[c] = p
        dic_translate[p] = c
    dic_translate["depth"] = depth
    return dic_translate

def string_dictionary_encode(dic_translate, s_message):
    encode_message = ""
    for s in s_message:
        encode_message = encode_message + dic_translate[s]
    return encode_message

def change_to_be_hex(string_str):
    return int(string_str.encode().hex(),base=16)

def xor_two_str(str1,str2):
    a = change_to_be_hex(str1)
    b = change_to_be_hex(str2)
    return hex(a ^ b)

def xor_hex_str(hex1,str2):
    b = change_to_be_hex(str2)
    return hex(hex1 ^ b)

def int_hex_to_str(int_hex):
    return bytes.fromhex(hex(int_hex)[2:]).decode()

def hex_to_str(input_hex):
    return bytes.fromhex(input_hex[2:]).decode()

def mutant_str(encode_message, password_xor):
    to_mutant = ""
    index_pass = 0
    for s in encode_message:
        to_mutant = to_mutant + ":" + xor_two_str(s,str(password_xor[index_pass]))[2:]
        index_pass += 1
        if index_pass >= len(password_xor):
            index_pass = 0
    return base64.b64encode(zlib.compress(to_mutant[1:].encode("utf-8"))).decode()

def mutant_to_normal(muntant_input, password_xor):
    to_normal = ""
    index_pass = 0
    m_input = zlib.decompress(base64.b64decode(muntant_input + '=' * (-len(muntant_input) % 4))).decode()
    for h in m_input.split(":"):
        p1 = str(password_xor[index_pass])
        to_normal = to_normal + hex_to_str(xor_hex_str(int(h, 16),p1))
        index_pass += 1
        if index_pass >= len(password_xor):
            index_pass = 0
    return to_normal

def string_dictionary_decode(dic_translate, encode_message):
    decode_message = ""
    depth = dic_translate["depth"]
    for index in range(int(len(encode_message)/depth)):
        init_string = index*depth
        encode_character = encode_message[init_string:init_string+depth]
        decode_message = decode_message + dic_translate[encode_character]
    return decode_message

############# Demo #############

# Generate dictionary to translate
dic_translate = string_dictionary(characters, characters_to_encode, depth)
print(dic_translate)

# Encode with dictionary
encode_message = string_dictionary_encode(dic_translate, message)
print(encode_message)

# Mutant v1
#mutant = xor_two_str(encode_message, password_xor)
#not_mutant = hex_to_str(xor_two_str(hex_to_str(mutant), password_xor))
#decode_message = string_dictionary_decode(dic_translate, not_mutant)

# XOR using encode message and "password" to mutant
mutant = mutant_str(encode_message, password_xor)
print(mutant)

# Encrypted to AES
encrypted = cipher.encrypt(mutant)

# ----- Travel happily on the Internet -----
print(encrypted)
# ----- Travel happily on the Internet -----

# Decrypted to AES
decrypted = cipher.decrypt(encrypted)

# XOR using encode message and "password" to normal
normal = mutant_to_normal(decrypted, password_xor)

# Decode message using dictionary to translate
decode_message = string_dictionary_decode(dic_translate, normal)
print(decode_message)