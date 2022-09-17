from client.message import Message

class Ack(Message):

    """Construtor da classe de Ack(Herdada da classe Message) usado para ser reconhecido pelos pacotes DATA e ERROR

    @param opcode: Opcode correspondente ao tipo de mensagem
    @param blck: String de Block do pacote
    @param data: Contém os dados da Messagem
    """
    def __init__(self, opcode, block):
        if (type(opcode) != int) and (opcode != 4):
            raise Exception("Não foi enviado um Opcode de ACK")
        super().__init__(opcode)
        self.__block = block

    """Faz a transmissão dos Dados das Mensagens

        2 bytes | 2 bytes
        Opcode  | Block #
    """
    def serializeMsg(self):
        serial = bytearray()
        serial.append(0) #Opcode é composto por 2 bytes portanto: 0 + Opcode, neste caso 04
        serial.append(self.__opcode)
        serial += self.__block
        return serial