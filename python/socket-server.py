import socket, threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("my ipv4 from ipconfig", 12))

server.listen(5)

def client_handler(client_socket):
    request = client_socket.recv(100)

    print ("[*] Received: " + request)

    client_socket.close()

while True:
    client, addr = server.accept()
    print ("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
    servert = threading.Thread(target=client_handler, args=(client,))
    servert.start()
