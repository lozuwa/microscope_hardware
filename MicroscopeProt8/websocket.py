import socket

#host = "192.168.3.213"
host = "192.168.3.213"
port = 50007
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
print("Binded port")

if __name__ == "__main__":
    while 1:
        client, address = s.accept()
        print("Accepted new client ", client, address)
        data = client.recv(size)
        print(data)
        #if data:
        #   client.send(data)
