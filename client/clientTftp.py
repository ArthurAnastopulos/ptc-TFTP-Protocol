from client.message import Message
from client.request import Request
from client.data import Data
from client.ack import Ack
from client.error import Error

"""Enumeração dos Estado de Máquina do Cliente TFTP
Idle - Ocioso, Connect - Conectado, Rx - Recepção, Tx - Transmissão, End - Fim
"""
class ClientTFTP_States:
    Idle = 0
    Connect= 1
    Rx = 2
    Tx = 3
    End = 4

class ClientTFTP:
    """Construtor do Cliente TFTP

    @param ip: String contendo o ip do Cliente
    @param port: Inteiro contendo porta do Cliente
    @param tout: Valor do Timeout
    """
    def __init__(self, ip:str, port:int, tout:float):
        self.__ip = ip
        self.__port = port
        self.__tout = tout
        self.__state = ClientTFTP_States.Idle
    
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
