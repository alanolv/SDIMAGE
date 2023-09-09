import socket

# Definir la dirección del servidor y el puerto en el que escucharás conexiones
server_address = ('localhost', 12345)

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
            # Recibir datos del cliente
            data = client_socket.recv(4096)
            if not data:
                break  # El cliente cerró la conexión
            with open("imagen recibida.jpg", "ab") as image_file:
                image_file.write(data)
            print("imagen recibida y guardada como: imagen recibida.jpg")
            data=data.decode('utf-8')

            # Enviar una respuesta al cliente
            #response = data
            #client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cerrar el socket del cliente
        client_socket.close()