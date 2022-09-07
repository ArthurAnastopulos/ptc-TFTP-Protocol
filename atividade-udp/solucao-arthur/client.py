import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5006
MESSAGE = b"Hello, World!"

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

socket_ = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
socket_.bind((UDP_IP, UDP_PORT))

while True:
    MESSAGE = input("Message: ")
    socket_.sendto(MESSAGE.encode(), (UDP_IP, 5005))
    data, addr = socket_.recvfrom(1024)
    print("received message from server: %s" % data.decode())