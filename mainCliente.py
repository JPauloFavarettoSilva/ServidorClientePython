import socket

class ResourceClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def request_resource(self, client_id, resource, duration):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            message = f"{client_id},{resource},{duration}"
            s.sendall(message.encode())
            data = s.recv(1024)
            response = data.decode()

            print(f"Cliente {client_id} - resposta do servidor: {response}")

if __name__ == "__main__":
    client = ResourceClient("127.0.0.1", 65432)
    client.request_resource(1, "impressora1", 10)
    client.request_resource(2, "sala_reuniao1", 30)
    client.request_resource(3, "impressora1", 5)