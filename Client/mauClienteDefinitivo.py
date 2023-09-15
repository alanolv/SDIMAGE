import socket
from cryptography.fernet import Fernet
# Generar una clave de encriptación
key = Fernet.generate_key()

# Dirección del servidor y puerto al que conectarse
server_address = ('localhost', 23456)

# Crear un socket de cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar al servidor
    client_socket.connect(server_address)
    print("Conexión establecida con el servidor.")
    
    #generamos la llave
    clave = Fernet.generate_key()
    with open("clave.key","wb") as file:
        file.write(clave)
    clave = open("clave.key","rb").read()
    
    # Enviar la clave de encriptación al servidor
    client_socket.send(key)

    # Leer la imagen a enviar
    with open("ds2.jpg", "rb") as file:
        image_data = file.read()
        
    #encriptamos la imagen
    f = Fernet(clave)
    encriptado = f.encrypt(image_data)
        
    # Encriptar la imagen
    fernet = Fernet(key)
    encrypted_image = fernet.encrypt(image_data)
    with open("img.tk3","wb") as file:
        file.write(encriptado)
    
    # Enviar la imagen encriptada al servidor
    client_socket.send(encrypted_image)
    print("Imagen encriptada enviada al servidor.")
    
    # Recibir el mensaje de confirmación del servidor
    confirmation_message = client_socket.recv(1024)
    print(confirmation_message.decode())

    # Recibir la imagen desencriptada del servidor
    desencripted_image_data = client_socket.recv(4096)
    print("Imagen desencriptada recibida del servidor.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Cerrar el socket del cliente
    client_socket.close()