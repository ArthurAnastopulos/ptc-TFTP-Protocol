from msilib.schema import Class
from urllib.request import Request
from client.message import Message

class Request(Message):

    """Construtor da classe de Requisição(Herdada da classe Message)

    @param buffer: buffer contendo os dados da messagem
    @param fname: Nome do Arquivo
    @param mode: contém o modo de formato, onde pode ser as Strings "netascii", "octet", or "mail" 
    """
    def __init__(self, buffer:str, fname:str, mode:str):
        super().__init__(buffer)
        self.__fname = fname
        self.__mode = mode
        
    """Faz a transmissão dos Dados das Mensagens

    """
    def serializeMsg(self):
        return super().serialize()