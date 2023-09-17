# server.py
import socket
import struct

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
                
def decrypt_file(filename):
  
    key = 107
     
    fin = open(filename, 'rb')
     
    image = fin.read()
    fin.close()

    image = bytearray(image)
 
    for index, values in enumerate(image):
        image[index] = values ^ key
 
    new_filename = "decrypted_" + filename  
    fin = open(new_filename, 'wb')

    fin.write(image)
    fin.close()
    
def send_file(sck: socket.socket, filename):
    with open(filename, "rb") as f:
        data = f.read()
        sck.sendall(data)
        
with socket.create_server(("localhost", 6190)) as server:
    print("Esperando al cliente...")
    conn, address = server.accept()
    print(f"{address[0]}:{address[1]} conectado.")
    print("Recibiendo archivo...")
    receive_file(conn, "image_receive.png")
    print("Archivo recibido.")
    print("Desencriptando archivo")
    decrypt_file("image_receive.png")
    print("Archivo desencriptado")
    print("Enviando archivo desencriptado al cliente...")
    send_file(conn, "decrypted_image_receive.png")
    print("Archivo desencriptado enviado al cliente.")
print("Conexión cerrada.")
