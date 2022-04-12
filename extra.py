############################### IMPORTS ###############################

from movement import moves, location, facing, walls, unwalls, sheep
import random

############################### FUNÇÕES ###############################

# O brick guarda o output de print num ficheiro "main.py.err.log" por default
# Esta função utiliza isso a proveito de guardar as ações do robot num formato mais legível
def log():
    global facing
    print("LOC: ",location, " | FACING: ",facing)
    print("WALLS: ", str(walls))
    print("UNWALLS: ", str(unwalls))
    print("SHEEP: ", str(sheep))
    print()


# Para chances de 50/50, devolve 0 ou 1
def coinToss():
    return random.randrange(2)

