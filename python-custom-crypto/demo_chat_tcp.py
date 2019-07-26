from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
import socket, getpass

from miarma_crypto import *

def list_config(list_input):
    for (index, element) in enumerate(list_input):
        print(index, element)

print("Chat - Interfaces disponibles: ")
list_interfaces = ni.interfaces()
list_config(list_interfaces)
num_intfz = input('Introduce la interfaz a utilizar: ')
intfz = list_interfaces[int(num_intfz)]
iphost = ni.ifaddresses(intfz)[AF_INET][0]['addr']
print("La IP del Servidor es: ", iphost)
nameuser = input('Nombre a utilizar: ')

internal_seed=input('Internal seed: ')
password_xor=getpass.getpass()

server = socket.socket()
server.bind((iphost, 6969))
server.listen(7)
print("INF: puedes escribir 'close' sin comillas para cerrar.")

print("Esperando clientes...")
# Aceptamos una conexion, se bloquea hasta que alguien se conecte.
socket_cliente, datos_cliente = server.accept()

print("Esperando init seed...")
init_seed = socket_cliente.recv(1000).decode()
mc = miarma_crypto(password_xor=password_xor, internal_seed=internal_seed, seed_negotiation=init_seed)

llave = 0
while llave == 0:
    print("Esperando mensaje...")
    datos = socket_cliente.recv(1000).decode()
    print(datos)
    normal = mc.mutant_to_normal(datos)
    decode_message = mc.string_dictionary_decode(normal)
    print(decode_message)

    mensaje = input('Mensaje: ')
    datos= nameuser + ": " + mensaje
    encode_message = mc.string_dictionary_encode(datos)
    mutant = mc.mutant_str(encode_message)
    socket_cliente.send(mutant.encode())
    if mensaje == 'close':
        socket.close()