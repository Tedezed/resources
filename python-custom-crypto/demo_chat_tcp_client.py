import socket, random, getpass

from miarma_crypto import *

iphost = input('Introduce la IP Servidor: ')
nameuser = input('Nombre a utilizar: ')

internal_seed=input('Internal seed: ')
password_xor=getpass.getpass()

socket = socket.socket()
socket.connect((iphost, 6969))
print("INF: puedes escribir 'close' sin comillas para cerrar.")

characters_to_encode = string.ascii_letters + string.digits
init_seed = "".join(random.sample(characters_to_encode,32))
socket.send(init_seed.encode())
mc = miarma_crypto(password_xor=password_xor, internal_seed=internal_seed, seed_negotiation=init_seed)

while True:
    mensaje = input('Mensaje: ')
    datos= nameuser + ": " + mensaje
    encode_message = mc.string_dictionary_encode(datos)
    mutant = mc.mutant_str(encode_message)
    socket.send(mutant.encode())
    if mensaje == 'close':
        socket.close()

    print("Esperando mensaje...")
    datos = socket.recv(1000).decode()
    print(datos)
    try:
        normal = mc.mutant_to_normal(datos)
        decode_message = mc.string_dictionary_decode(normal)
        print(decode_message)
    except Exception as e:
        print("ERROR %s" % e)