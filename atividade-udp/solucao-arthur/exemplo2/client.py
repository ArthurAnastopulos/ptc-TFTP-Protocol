from pypoller import poller
import sys,time
import os
import socket

class CallbackRX(poller.Callback):
  
   def __init__(self, tout):
      poller.Callback.__init__(self, None, tout)
 
   def envia(self):
      data, addr = socket_.recvfrom(1024)
      print("received message from server: %s" % data.decode())
      self.enable_timeout()
      self.reload_timeout()

   def handle_timeout(self):
      print("timeout")
      self.disable_timeout()        
  

class CallbackTX(poller.Callback):
  
   def __init__(self, cb):
      poller.Callback.__init__(self, sys.stdin, 0)
      self.disable_timeout()
      self.cb = cb
 
   def handle(self):
      MESSAGE = sys.stdin.readline()
      socket_.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
      self.cb.envia()
 
    
      
####################################  

UDP_IP = "127.0.0.1"
UDP_PORT = 5555
MESSAGE = b"Hello, World!"

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

socket_ = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP

# instancia um callback
cb_rx = CallbackRX(5)
cb_tx = CallbackTX(cb_rx)


# cria o poller (event loop)
sched = poller.Poller()
 
# registra o callback no poller
sched.adiciona(cb_tx)
sched.adiciona(cb_rx)

# entrega o controle pro loop de eventos
sched.despache()

# while True:
#     MESSAGE = input("Message: ")
#     socket_.sendto(MESSAGE.encode(), (UDP_IP, 5005))
#     data, addr = socket_.recvfrom(1024)
#     print("received message from server: %s" % data.decode())