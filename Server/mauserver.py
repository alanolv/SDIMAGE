import socket
from cryptography.fernet import Fernet

# Funciones para encriptar
def crear_llave():
    return Fernet.generate_key()

def guardar_llave(llave, archivo):
    with open(archivo, 'wb') as archivo_llave:
        archivo_llave.write(llave)

def cargar_llave(archivo):
    return open(archivo, 'rb').read()

def encriptar(data, llave):
    fernet = Fernet(llave)
    return fernet.encrypt(data)

def desencriptar(data, llave):
    fernet = Fernet(llave)
    return fernet.decrypt(data)

# Definir la dirección del servidor y el puerto en el que escucharás conexiones
server_address = ("148.220.215.254", 12345)

# Crear un socket de servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket a la dirección y el puerto
server_socket.bind(server_address)

# Escuchar conexiones entrantes
server_socket.listen(5)  # Acepta hasta 5 conexiones pendientes

print("Esperando conexiones entrantes...")

while True:
    # Esperar una conexión entrante
    client_socket, client_address = server_socket.accept()
    print(f"Conexión entrante desde: {client_address}")

    try:
        while True:
            # Generar y enviar la clave al cliente
            llave = crear_llave()
            guardar_llave(llave, 'secret.key')
            client_socket.send(llave)

            # Recibir datos del cliente
            with open("Diagrama.jpg", "ab") as image_file:
                data = client_socket.recv(4096)
                while data:
                    image_file.write(data)
                    data = client_socket.recv(4096)
                print("Imagen recibida y guardada como: imagen_encriptada.jpg")
            
            if not data:
                break  # El cliente cerró la conexión
            
            # Desencriptar la imagen
            llave = cargar_llave('secret.key')
            with open('imagen_encriptada.jpg', 'rb') as file:
                encriptar_data = file.read()
            desencriptar_data = desencriptar(encriptar_data, llave)

            # Guardar la imagen desencriptada
            with open('imagen_desencriptada.jpg', 'wb') as file:
                file.write(desencriptar_data)

            print("Imagen recibida y desencriptada.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cerrar el socket del cliente
        client_socket.close()