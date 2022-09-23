from client.message import Message
from client.request import Request
from client.data import Data
from client.ack import Ack
from client.error import Error
from pypoller import poller
from socket import *
import os

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
        self.__state =  self.__handle_idle

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
        # Envia mensagem de RRQ
        msg = Request(1, fname, mode)
        self.__mode = mode
        self.__fname = fname
        self.__n = 1

        #cria o arquivo para escrita de bytes
        self.file = open("./" + self.__fname, "wb" )
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
        msg = Request(2, fname, mode)
        self.__mode = mode
        self.__fname = fname
        self.__n = 1

        #cria o arquivo para leitura de bytes
        self.file = open("./" + self.__fname, "rb")
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

    """Mudança de Estado para Ocioso

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_idle(self, msg:Message):
        self.__state = self.__handle_idle

    """Mudança de Estado para Conectando

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_connect(self, msg:Message):
        #recebe mensagem do socket
        
        #Se for ERROR
        if(msg.getopcode()==5):
            self.__state = self.__handle_idle

        #Se Receber um DATA (Significa que é RX)
        if(msg.getopcode()==3):
            self.__state = self.__handle_rx

        #Se Receber um ACK (Significa que é TX)
        if(msg.getopcode()==4):
            self__state = self.__handle_tx


    """Mudança de Estado para Recepção

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_rx(self, msg:Ack):
        #Recebe Msg do socket

        #Se len do Data == 512, continua neste estado
            #envia Ack, incrementa n
        if(len(msg)==512):  
            self.__state = self.__handle_rx
            #enviar ack
            #self.__socket.sendto(msg.)

            self.__n+=1


        #Se len do Data < 512, encerrar
        if(len(msg)< 512):
            self.__state = self.__handle_idle
        
    
    """Mudança de Estado para Transmissão

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_tx(self, msg:Data):
        #Recebe Msg do socket

        #Se houver timeout na espera da resposta, re envia data (mantem estado)
        self.__state = self.__handle_tx

        #Se receber Ack(4), e ainda tem mais q 512 de tamanho continua no estado
        if(msg.getopcode==4 & len(msg)==512):
            self.__state = self.__handle_tx

        #Se estiver sobrando  menos que 512
        if(len(msg)<512):
            self.__state = self.__handle_end
        

 
    """Mudança de Estado para Fim

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_end(self, msg:Data):
        #Se houve timeout renvia uma ultima Data (mantem o estado)
        self.__state = self.__handle_end

        #Se não encerra 
        self.__state = self.__handle_idle

    def handle(self):
        #recebe mensagem do socket
       
        data, (addr, port) = self.__socket.recvfrom(516) # 512 bytes + opcode + block
        #transformar data em objeto mensagem
        self.__state(data)
        #escrevendo no arquivo
        #maquina de Estados

    def handle_timeout(self):
        self.disable_timeout()
        self.disable()
        self.__state = self.__handle_idle
        #maquina de estado passar para ociso
