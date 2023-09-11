import socket
from cryptography.fernet import Fernet

# Función para cargar la clave desde un archivo
def cargar_llave(archivo):
    return open(archivo, 'rb').read()

# Definir la dirección del servidor y el puerto al que te quieres conectar
server_address = ('127.0.0.1', 12345)

# Crear un socket de cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar al servidor
    client_socket.connect(server_address)

    # Recibir la clave del servidor
    llave = client_socket.recv(1024)

    # Crear una instancia de Fernet con la clave recibida
    fernet = Fernet(llave)

    # Leer la imagen desde el archivo y enviarla en bloques encriptados
    with open("gatito1.jpg", "rb") as image_file:
        data = image_file.read(4096)
        while data:
            data_encrypted = fernet.encrypt(data)  # Encriptar los datos
            client_socket.send(data_encrypted)
            data = image_file.read(4096)

    print("Imagen enviada al servidor correctamente")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Cerrar el socket del cliente
    client_socket.close()