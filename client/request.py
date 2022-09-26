from client.message import Message

class Request(Message):

    """Construtor da classe de Requisição(Herdada da classe Message)

    @param opcode: Opcode correspondente ao tipo de mensagem
    @param fname: Nome do Arquivo
    @param mode: contém o modo de formato, onde pode ser as Strings "netascii", "octet", or "mail" 
    """
    def __init__(self, opcode, fname:str, mode:str):
        if (type(opcode) != int) and (opcode != 1 or opcode != 2):
            raise Exception("Não foi enviado um Opcode de REQUEST")
        self.__opcode = opcode
        self.__fname = fname
        if mode.lower() == "netascii" or mode.lower() == "octet" or mode.lower() == "mail": 
            self.__mode = mode.lower()
        else:
           raise Exception("Não foi enviado um modo válido")     
        
    """Faz a transmissão dos Dados das Mensagens

        2 bytes | string   | 1 byte | string | 1 byte
        Opcode  | Filename |    0   | Mode   | 0
    """
    def serializeMsg(self):
        serial = bytearray()
        serial.append(0)
        serial.append(self.__opcode)
        
        serial += self.__fname.encode('ascii')
        serial.append(0)
        
        serial += self.__mode.encode('ascii')
        serial.append(0)
        return serial