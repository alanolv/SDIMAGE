# client.py
import os
import socket
import struct
def send_file(sck: socket.socket, filename):
    filesize = os.path.getsize(filename)
    sck.sendall(struct.pack("<Q", filesize))
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)
            
def encrypt_file(filename):
   
    key = 107  
    fin = open(filename, 'rb')

    image = fin.read()
    fin.close()
        
    image = bytearray(image)
   
    for index, values in enumerate(image):
        image[index] = values ^ key
 
   
    new_filename = "encrypted_" + filename  
    fin = open(new_filename, 'wb')

    fin.write(image)
    fin.close()
    print('Archivo encriptado...')
 
     
with socket.create_connection(("localhost", 6190)) as conn:
    print("Conectado al servidor.")
    encrypt_file("image.png")
    print("Enviando archivo...")
    send_file(conn, "encrypted_image.png")
    print("Enviado.")
print("Conexión cerrada.")