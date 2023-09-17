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
            
def receive_file_size(sck: socket.socket):
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    while received_bytes < expected_bytes:
        chunk = sck.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize

def receive_file(sck: socket.socket, filename):
    filesize = receive_file_size(sck)
    with open(filename, "wb") as f:
        received_bytes = 0
        while received_bytes < filesize:
            chunk = sck.recv(1024)
            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)
                
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
 
     
with socket.create_connection(("10.10.47.4", 6190)) as conn:
    print("Conectado al servidor.")
    encrypt_file("image.png")
    print("Enviando archivo...")
    send_file(conn, "encrypted_image.png")
    print("Enviado.")
    print("Recibiendo archivo")
    receive_file(conn, "image_receive.png")
    print("Archivo recibido.")
print("Conexión cerrada.")