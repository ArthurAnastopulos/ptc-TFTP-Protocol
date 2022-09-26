import sys
import logging as logger
from client import clientTftp

if len(sys.argv) == 0:
    print('No argument was passed, exiting test program.')
    sys.exit()

# Capture os argumentos necessários para usar o programa de teste TFTP.
try:
    IP_ = sys.argv[1]
    print('IP obtained by argument successfully') 
except Exception as Argument:
    print('Error. There is no IP passed by argument: \n', Argument)
    sys.exit()

try:
    PORT_ = int(sys.argv[2])
    print('PORT obtained by argument successfully') 
except Exception as Argument:
    print('Error. There is no PORT passed by argument: \n', Argument)
    sys.exit()

try:
    TIMEOUT_ = int(sys.argv[3])
    print('TIMEOUT obtained by argument successfully') 
except Exception as Argument:
    print('Error. There is no TIMEOUT passed by argument: \n', Argument)
    sys.exit()

try:
    FILENAME_ = sys.argv[4]
    print('FILENAME obtained by argument successfully') 
except Exception as Argument:
    print('Error. There is no FILENAME passed by argument: \n', Argument)
    sys.exit()

try:
    REQUEST_ = int(sys.argv[5])
    print('REQUEST obtained by argument successfully') 
except Exception as Argument:
    print('Error. There is no REQUEST passed by argument: \n', Argument)
    sys.exit()

MODE_ = "NetAscii"

# Inicia a classe do cliente TFTP com os argumentos obtidos. Se REQUEST_ tem seu opcode = 1 é um RRQ, ou se REQUEST_ tem seu opcode = 2 é um WRQ.
# Qualquer outra coisa é um argumento REQUEST_ inválido, então o Cliente TFTP deve lançar uma mensagem de erro se outro opcode diferente de 1 ou 2 estiver na solicitação.
CLIENT = clientTftp.ClientTFTP(IP_, PORT_, TIMEOUT_)

if REQUEST_ == 1:
    try:
        CLIENT.get(FILENAME_, MODE_)
    except Exception as Argument:
        print('Error. Error got while reading using TFTP: \n', Argument)
        sys.exit()  
elif REQUEST_ == 2:
    try:
        CLIENT.put(FILENAME_, MODE_)
    except Exception as Argument:
        print('Error. Error got while writing using TFTP: \n', Argument)
        sys.exit()
else:
    print('This is an invalid opcode for the TFTP request, the expected response is an error on both types of requests.') 
    try:
        CLIENT.get(FILENAME_, MODE_)
        CLIENT.put(FILENAME_, MODE_)
    except Exception as Argument:
        print('Error. Error got while using wrong opcode for TFTP request: \n', Argument)
        sys.exit()