import socket

# Definir la dirección del servidor y el puerto al que te quieres conectar
server_address = ('localhost', 12345)

# Crear un socket de cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar al servidor
    client_socket.connect(server_address)

    # Leer la imagen desde el archivo
    with open("Diagrama.jpeg", "rb") as image_file:
        image_data = image_file.read()

    # Enviar los datos de la imagen al servidor
    client_socket.sendall(image_data)

    print("Imagen enviada al servidor correctamente")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Cerrar el socket del cliente
    client_socket.close()