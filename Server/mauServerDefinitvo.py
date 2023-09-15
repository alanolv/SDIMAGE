import socket
from cryptography.fernet import Fernet

# Dirección del servidor y puerto en el que escucharás conexiones
server_address = ('localhost', 23456)

# Crear un socket de servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket a la dirección y el puerto
server_socket.bind(server_address)

# Escuchar conexiones entrantes
server_socket.listen()

print("Esperando conexiones entrantes...")

while True:
    # Esperar una conexión entrante
    client_socket, client_address = server_socket.accept()
    print(f"Conexión entrante desde: {client_address}")

    try:
        
        # Recibir la imagen encriptada
        data = client_socket.recv(4096)
        encrypted_image = data
        print("Imagen encriptada recibida")
        
        # Recibir la clave de encriptación del cliente
        key = client_socket.recv(1024)
        print("Clave de encriptación recibida")
        
        #desencriptamos la imagen
        clave = open("clave.key","rb").read()
        fernet = Fernet(clave)
        desencriptado = fernet.decrypt(open("img.tk3","rb").read())
        
        # Guardar la imagen en el servidor
        with open("imagen_recibida.jpg", "wb") as file:
            file.write(desencriptado)
        
        print("Imagen desencriptada y guardada correctamente.")

        # Enviar un mensaje de confirmación al cliente
        confirmation_message = "Imagen recibida y desencriptada correctamente."
        client_socket.send(confirmation_message.encode())
        
        # se envia la imagen desencriptada de vuelta al cliente
        with open("imagen_recibida.jpg", "rb") as file:
            desencripted_image_data = file.read()
            client_socket.send(desencripted_image_data)
        
        print("Imagen desencriptada enviada de vuelta al cliente.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cerrar el socket del cliente
        client_socket.close()