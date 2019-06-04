import sys

# XORCalculator
# By Tedezed
#
# python XORCalculator.py 01000100010111100011111101000111010101010101111001010011001111110100110001011100010010010100111101001111 \
# 	00110000001100010001111100110011001101000011010100110110000111110011100000111001001110100011101100111100

#binary_encrypt = '01000100010111100011111101000111010101010101111001010011001111110100110001011100010010010100111101001111'
#binary_decrypt = '01110100011011110010000001110100011000010110101101100101001000000111010001100101011100110111010001110011'
binary_encrypt = sys.argv[1]
binary_decrypt = sys.argv[2]

key_str = ''
for idx,b1 in enumerate(binary_encrypt):
	#print binary_encrypt[idx]
	#print binary_decrypt[idx]
	if binary_encrypt[idx] == '0' and binary_decrypt[idx] == '0':
		key_str += '0'
	elif binary_encrypt[idx] == '1' and binary_decrypt[idx] == '0':
		key_str += '1'
	elif binary_encrypt[idx] == '0' and binary_decrypt[idx] == '1':
		key_str += '1'
	elif binary_encrypt[idx] == '1' and binary_decrypt[idx] == '1':
		key_str += '0'
	else:
		raise 'Error XOR'

print key_str