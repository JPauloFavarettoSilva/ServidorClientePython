import socket


class ResourceClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def request_resource(self, client_id, resource, duration):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            message = f"RESERVE,{client_id},{resource},{duration}"
            s.sendall(message.encode())
            data = s.recv(1024)
            response = data.decode()

            print(f"Cliente {client_id} - resposta do servidor: {response}")

    def check_resource_status(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            message = "STATUS"
            s.sendall(message.encode())
            data = s.recv(1024)
            response = data.decode()

            print("Status dos recursos: ", response)


if __name__ == "__main__":
    client = ResourceClient("127.0.0.1", 65432)

    client.check_resource_status()

    client.request_resource(1, "impressora1", 10)

    client.check_resource_status()
