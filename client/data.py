from client.message import Message

class Data(Message):

    """Construtor da classe de Data(Herdada da classe Message) possui um número de bloco e um campo de dados

    @param opcode: Opcode correspondente ao tipo de mensagem
    @param blck: String de Block do pacote
    @param data: Contém os dados da Messagem
    """
    def __init__(self, opcode, block, data):
        if (type(opcode) != int) and (opcode != 3):
            raise Exception("Não foi enviado um Opcode de Data")
        self.__opcode = opcode
        self.__block = block
        self.__data = data
        
    """Faz a transmissão dos Dados das Mensagens

        2 bytes | 2 bytes | n Bytes
        Opcode  | Block # | Data
    """
    def serializeMsg(self):
        serial = bytearray()
        serial.append(0)
        serial.append(self.__opcode)
        serial += self.__block
        serial += self.__data
        return serial