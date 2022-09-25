from typing_extensions import Self
from client.message import Message

class Error(Message):

    """Construtor da classe de Error(Herdada da classe Message) usado para ser reconhecido por algum outro tipo de pacote e seu código de erro é um inteiro indicando a natureza do erro

    @param opcode: Opcode correspondente ao tipo de mensagem
    @param errorCode: Codgio do Erro
    """
    def __init__(self, opcode, errorCode:int):
        if (type(opcode) != int) and (opcode != 5):
            raise Exception("Não foi enviado um Opcode de ERROR")
        super().__init__(opcode)
        self.__errorCode =  errorCode
        if self.__errorCode == 0:
            self.__errMsg = "Not defined, see error message (if any)."
        if self.__errorCode == 1:
            self.__errMsg = "File not found."
        if self.__errorCode == 2:
            self.__errMsg = "Access violation."
        if self.__errorCode == 3:
            self.__errMsg = "Disk full or allocation exceeded."
        if self.__errorCode == 4:
            self.__errMsg = "Illegal TFTP operation."
        if self.__errorCode == 5:
            self.__errMsg = "Unknown transfer ID."
        if self.__errorCode == 6:
            self.__errMsg = "File already exists." 
        if self.__errorCode == 7:
            self.__errMsg = "No such user."                      


    def getErrorMsg(self):
        return self.__errMsg

    """Faz a transmissão dos Dados das Mensagens

       2 bytes | 2 bytes   | string | 1 byte
       Opcode  | ErrorCode | ErrMsg | 0
    """
    def serializeMsg(self):
        serial = bytearray()
        serial.append(0)
        serial.append(self.__opcode)
        serial.append(0)
        serial.append(self.__errorCode)
        serial += self.__errMsg.encode('ascii')
        serial.append(0)
        return serial
