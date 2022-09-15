from client.message import Message
from client.request import Request
from client.data import Data
from client.ack import Ack
from client.error import Error
from pypoller import poller
from socket import *

"""Enumeração dos Estado de Máquina do Cliente TFTP
Idle - Ocioso, Connect - Conectado, Rx - Recepção, Tx - Transmissão, End - Fim
"""
class ClientTFTP_States:
    Idle = 0
    Connect= 1
    Rx = 2
    Tx = 3
    End = 4

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
        self._handlers = {ClientTFTP_States.Idle: self.__handle_idle, ClientTFTP_States.Connect: self.__handle_connect, 
                      ClientTFTP_States.Rx: self.__handle_rx, ClientTFTP_States.Tx: self.__handle_tx, ClientTFTP_States.End: self.__handle_end} # tabela de handlers
        self.__state = ClientTFTP_States.Idle

        self.n = 0
        self.max_n = 0
        self.msg_size = 0
        self.mode = "NetAscii"
        self.datafile = None


    """Requisição de leitura do TFTP
    
    @param fname: Nome do Arquivo
    @param mode: contém o modo de formato, onde pode ser as Strings "netascii", "octet", or "mail"
    """
    def get(self, fname:str, mode:str):
        self.__state = ClientTFTP_States.Connect
        buffer = ""
        self.__msg = Request(buffer, fname, mode)

    """Requisição de escrita do TFTP

    @param fname: Nome do Arquivo
    @param mode: contém o modo de formato, onde pode ser as Strings "netascii", "octet", or "mail"
    """
    def put(self, fname:str, mode:str):
        self.__state = ClientTFTP_States.Connect
        buffer = ""
        self.__msg = Request(buffer, fname, mode)

    """Mudança de Estado para Ocioso

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_idle(self, msg:Message, tout:bool):
        self.__state = ClientTFTP_States.Idle
        self._msg = msg

    """Mudança de Estado para Conectando

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_connect(self, msg:Message, tout:bool):
        self.__state = ClientTFTP_States.Connect
        self._msg = msg

    """Mudança de Estado para Recepção

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_rx(self, msg:Ack, tout:bool):
        self.__state = ClientTFTP_States.Rx
        self._msg = msg
    
    """Mudança de Estado para Transmissão

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_tx(self, msg:Data, tout:bool):
        self.__state = ClientTFTP_States.Tx
        self._msg = msg

 
    """Mudança de Estado para Fim

    @param msg: Messagem utilizadas durante a troca de messagem
    @param tout: verifcação de ocorrencia do timeout
    """
    def __handle_end(self, msg:Data, tout:bool):
        self.__state = ClientTFTP_States.End
        self._msg = msg

    def handle(self):
        #recebe mensagem do socket
        data, (addr, port) = self.__socket.recvfrom(516) # 512 bytes + opcode + block
        #escrevendo no arquivo
        #maquina de Estados

    def handle_timeout(self):
        self.disable_timeout()
        self.disable()
        #maquina de estado passar para ociso