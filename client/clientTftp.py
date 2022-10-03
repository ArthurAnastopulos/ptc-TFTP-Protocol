from enum import Enum
import sys
from client.message import Message
from client.request import Request
from client.data import Data
from client.ack import Ack
from client.error import Error
from client.pypoller import poller
from socket import *
import os
import struct

class ClientTFTP(poller.Callback):
    """Construtor do Cliente TFTP

    @param ip: String contendo o ip do Cliente
    @param port: Inteiro contendo porta do Cliente
    @param tout: Valor do Timeout
    """
    def __init__(self, ip:str, port:int, tout:float):
        self.__ip = ip
        self.__port = port
        self.__tout = tout

        self.__socket = socket(AF_INET, SOCK_DGRAM)
        poller.Callback.__init__(self, self.__socket, self.__tout)

        self.__n = 0
    
        self.__max_n = 0
        self.__msg_size = 0
        self.__mode = "NetAscii"
        self.__fname = None


    """Requisição de leitura do TFTP
    
    @param fname: Nome do Arquivo
    @param mode: contém o modo de formato, onde pode ser as Strings "netascii", "octet", or "mail"
    """
    def get(self, fname:str, mode:str):
        print("Get")
        # Envia mensagem de RRQ
        msg = Request(1, fname, mode)
        self.__mode = mode
        self.__fname = fname
        self.__n = 1

        #cria o arquivo para escrita de bytes
        self.__file = open("./" + self.__fname, "wb" )
        self.__socket.sendto(msg.serializeMsg(), (self.__ip, self.__port))

        #Instancia Poller
        self.enable()
        self.enable_timeout()
        sched = poller.Poller()

        #Despache e mudança de estado
        self.__state = self.__handle_connect
        sched.adiciona(self)
        sched.despache()

    """Requisição de escrita do TFTP

    @param fname: Nome do Arquivo
    @param mode: contém o modo de formato, onde pode ser as Strings "netascii", "octet", or "mail"
    """
    def put(self, fname:str, mode:str):
        print("Put")
        msg = Request(2, fname, mode)
        self.__mode = mode
        self.__fname = fname
        self.__n = 1

        #cria o arquivo para leitura de bytes
        self.__file = open("./" + self.__fname, "rb")
        size = os.path.getsize("./" + self.__fname)
        print("Tamanho do Arquivo: ", size)
        self.__max_n = 1 + (size/512) #Qtd de vezes q será feito a o enviado

        self.__socket.sendto(msg.serializeMsg(), (self.__ip, self.__port))

        #Instancia Poller
        self.enable()
        self.enable_timeout()
        sched = poller.Poller()

        #Despache e mudança de estado
        self.__state = self.__handle_connect
        sched.adiciona(self)
        sched.despache()

    """Mudança de Estado para Conectando

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_connect(self, msg:Message):
        print("Connect")
        #recebe mensagem do socket
        #Se for ERROR
        if( msg.getOpcode() == 5 ):
            print("Obteve Erro no Connect")
            error = Error(5, msg.getBuffer()[3])
            print(error.getErrorMsg())
            sys.exit()

        #Se Receber um DATA (Significa que é RX)
        if(msg.getOpcode() == 3 ):
            data = msg.getBuffer()[4:]
            if(len(data) < 512):
                block_n = struct.pack(">H",self.__n)
                sendMsg = Ack(4, block_n)
                self.__socket.sendto( sendMsg.serializeMsg(), (self.__ip,self.__port) )
                print("Enviado ACK para o Serivodor TFTP")
                self.__file.write(data) # do Byte 4 em diante é o Data do arquivo
                self.__state = self.__handle_end
            if(len(data) == 512):
                block_n = struct.pack(">H",self.__n)
                sendMsg = Ack(4, block_n)
                self.__socket.sendto( sendMsg.serializeMsg(), (self.__ip,self.__port) )
                self.__n += 1
                self.__file.write(data)
                self.__state = self.__handle_rx

        #Se Receber um ACK (Significa que é TX)
        if( msg.getOpcode() == 4 ):
            ack_n = msg.getBuffer()[2:4]
            ack_n = int.from_bytes(ack_n, 'big')
            if (ack_n == 0):
                sentData = self.__file.read(512)
                block_n = struct.pack(">H", self.__n)
                dataMsg = Data(3, block_n, sentData)
                self.__socket.sendto( dataMsg.serializeMsg(), (self.__ip,self.__port) )
                self.__state = self.__handle_tx


    """Mudança de Estado para Recepção

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_rx(self, msg:Message):
        print("Rx")
        #Se for ERROR
        if( msg.getOpcode() == 5 ):
            error = Error(5, msg.getBuffer()[3])
            print(error.getErrorMsg())
            sys.exit()
        

        #Recebe Msg do socket
        data = msg.getBuffer()[4:]
        data_block_m = int.from_bytes(msg.getBuffer()[2:4],"big")
        #Se len do Data == 512, continua neste estado
            #envia Ack, incrementa n
        if( (msg.getOpcode() == 3) and (len(data) == 512) ):
            block_n = struct.pack(">H",self.__n)
            sendMsg = Ack(4, block_n)
            self.__socket.sendto( sendMsg.serializeMsg(), (self.__ip,self.__port) )
            self.__n += 1
            self.__file.write(data)
            self.__state = self.__handle_rx
        elif(data_block_m != self.__n):
            block_n = struct.pack(">H",data_block_m)
            sendMsg = Ack(4, block_n)
            self.__socket.sendto( sendMsg.serializeMsg(), (self.__ip,self.__port) )
            self.__file.write(data)
            self.__state = self.__handle_rx
        elif( (msg.getOpcode() == 3) and (len(data) < 512) ):
            block_n = struct.pack(">H",self.__n)
            sendMsg = Ack(4, block_n)
            self.__socket.sendto( sendMsg.serializeMsg(), (self.__ip,self.__port) )
            self.__file.write(data)
            print("Transferencia Concluida")
            self.__file.close()
            sys.exit() 
        
    
    """Mudança de Estado para Transmissão

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_tx(self, msg:Message):
        print("Tx")
        #Recebe Msg do socket
        ack_n = msg.getBuffer()[2:4]
        ack_n = int.from_bytes(ack_n, "big")

        if( (ack_n == self.__n) and (self.__n < (self.__max_n - 1)) ):
            self.__n += 1
            sendData = self.__file.read(512)
            block_n = struct.pack(">H", self.__n)
            dataMsg = Data(3, block_n, sendData)
            self.__socket.sendto( dataMsg.serializeMsg(), (self.__ip,self.__port) )
            self.__state = self.__handle_tx
        elif( ack_n and (self.__n == (self.__max_n - 1) ) ):
            self.__n += 1
            sendData = self.__file.read(512)
            block_n = struct.pack(">H", self.__n)
            dataMsg = Data(3, block_n, sendData)
            self.__socket.sendto( dataMsg.serializeMsg(), (self.__ip,self.__port) )
            self.__state = self.__handle_end
        

    """Mudança de Estado para Fim

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_end(self, msg:Message):
        print("End")
        #Se for ERROR
        if( msg.getOpcode() == 5 ):
            error = Error(5, msg.getBuffer()[3])
            print(error.getErrorMsg())
            sys.exit()

        if( ( msg.getOpcode() == 3 ) and ( len(msg.getBuffer()[4:]) ) ):
            block_n = struct.pack(">H",self.__n)
            sendMsg = Ack(4, block_n)
            self.__socket.sendto( sendMsg.serializeMsg(), (self.__ip,self.__port) )
            self.__file.close()
            sys.exit()
        elif( (msg.getOpcode() == 4) and ( msg.getBuffer() != None) ):
            self.__n += 1
            sendData = self.__file.read(512)
            block_n = struct.pack(">H", self.__n)
            dataMsg = Data(3, block_n, sendData)
            self.__socket.sendto( dataMsg.serializeMsg(), (self.__ip,self.__port) )
            sys.exit()


    def handle(self):
        #recebe mensagem do socket
       
        data, (addr, port) = self.__socket.recvfrom(516) # 512 bytes + opcode + block
        self.__port = port  
        #transformar data em objeto mensagem
        if type(data) is bytes:
            print( "Recebido Mensagem do " + str(addr) + ":" + str(port) + " = " )
            print(data)
            recvMsg = Message(data)
        else:
            print("Mensagem recebida não esta em bytes: " + str(data) )
            print("Abortanto execução do Cliente")
            sys.exit()

        #maquina de Estados
        self.__state(recvMsg)


    def handle_timeout(self):
        print("Timeout")
        self.disable_timeout()
        self.disable()
        #maquina de estado passar para ociso
