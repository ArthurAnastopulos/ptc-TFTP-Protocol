import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

socket_ = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
socket_.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = socket_.recvfrom(1024)
    MESSAGE = "received message: " + data.decode()
    print(MESSAGE)
    socket_.sendto("Server message recived".encode(), (UDP_IP, 5006))