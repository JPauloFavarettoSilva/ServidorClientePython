import threading
import socket


class ResourceServer:
    def __init__(self):
        self.resources = {"impressora1": True, "sala_reuniao1": True}
        self.lock = threading.Lock()

    def handle_request(self, client_id, resource, duration):
        with self.lock:  # Adquirir o lock (monitor)
            if self.resources.get(resource, None) is None:
                return f"Recurso {resource} não encontrado."

            if self.resources[resource]:
                self.resources[resource] = False
                print(f"Cliente {client_id} reservou {resource} por {duration} minutos")
                threading.Timer(duration * 60, self.release_resource, args=[client_id, resource]).start()
                return f"Recurso {resource} reservado por {duration} minutos."
            else:
                print(f"Cliente {client_id} - {resource} ocupado")
                return f"Recurso {resource} está ocupado."

    def release_resource(self, client_id, resource):
        with self.lock:
            self.resources[resource] = True
            print(f"Cliente {client_id} liberou {resource}")

    def start_server(self, host="127.0.0.1", port=65432):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Servidor rodando no endereço {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Conexão de {client_address}")
            client_thread = threading.Thread(target=self.client_handler, args=(client_socket,))
            client_thread.start()

    def client_handler(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break


            try:
                client_id, resource, duration = data.split(',')
                duration = int(duration)
                response = self.handle_request(client_id, resource, duration)
            except Exception as e:
                response = f"Erro na requisição: {str(e)}"

            client_socket.sendall(response.encode())

        client_socket.close()


if __name__ == "__main__":
    server = ResourceServer()
    server.start_server()