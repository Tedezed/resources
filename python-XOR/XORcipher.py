from __future__ import print_function, unicode_literals
from os import urandom
import sys

# XOR cipher
# Source: https://en.wikipedia.org/wiki/XOR_cipher
# By Tedezed
#
# python XORcipher.py create -> Crerate file output_file.bin and key_file.bin
# python XORcipher.py create -> Decrypt with key_file.bin and output_file.bin

#key_number = 3003599829466203248162261534406550074744661342684
#key_binary = '100000111000011110000100110001001100101011101101111001011101100100110111001100110101101010000001110100011111100110010000100000011010101010110010111111100111011100'

def genkey(length):
    """Generate key"""
    return urandom(length)

def xor_strings(s, t):
    """xor two strings together"""
    if isinstance(s, str):
        # Text strings contain single characters
        return b"".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, t))
    else:
        # Python 3 bytes objects contain integer values in the range 0-255
        return bytes([a ^ b for a, b in zip(s, t)])

def to_binary(input):
    return ''.join(format(ord(x), 'b') for x in input)

def bytes_to_int(bytes_input):
    result = 0
    for b in bytes_input:
        result = result * 256 + int(b)
    return result

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def write_binary(binary_file, binary_text):
    f = open(binary_file, 'w+b')
    f.write(binary_text)
    f.close()

def open_binary(binary_file_name, binary_key_name):
    with open(binary_file_name, "rb") as file:
        with open(binary_key_name, "rb") as key_file:
            fileContent = file.read()
            keyContent = key_file.read()
            print('cipherText: ', fileContent)
            print(keyContent)
            #bin_key = bin(key_number)
            #bin_key = bin_key[2:]
            #key_byte = bitstring_to_bytes(key_binary)
            #print('key:', key_byte)
            print('decrypted:', xor_strings(fileContent, keyContent).decode('utf8'))

def example_encrypt_txt_to_binary_xor():
    message = 'This is a secret message'
    print('message:', message)

    key = genkey(len(message))
    print(key)
    print('binary key:', to_binary(key))
    print('int key:', int(to_binary(key), 2))

    cipherText = xor_strings(message.encode('utf8'), key)
    print('cipherText:', cipherText)
    print('decrypted:', xor_strings(cipherText, key).decode('utf8'))

    # verify
    if xor_strings(cipherText, key).decode('utf8') == message:
        print('Unit test passed')
        write_binary('output_file.bin', cipherText)
        write_binary('key_file.bin', key)
    else:
        print('Unit test failed')

def errors():
    print('Use: create or decrypt')

if len(sys.argv) > 1:
    if sys.argv[1] == 'create':
        example_encrypt_txt_to_binary_xor()
    elif sys.argv[1] == 'decrypt':
        open_binary("output_file.bin", "key_file.bin")
    else:
        errors()
else:
    errors()
