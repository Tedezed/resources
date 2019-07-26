# DEMO

```
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
```