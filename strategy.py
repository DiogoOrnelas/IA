############################### IMPORTS ###############################

from movement import *
from action import *
from extra import *
import pathfinding

####################################### CÓDIGO PARA JOGO ################################################
    
# Primeiro passo do jogo: mapear o tabuleiro
def map():

    # Conterá as casas a serem examinadas
    goals = []

    # Preenchar com as casas de forma a que o percurso seja feito em Ss
    for y in range(6):
        if ( y % 2 ):
            for x in range(5,-1,-1):
                goals = goals + [[x,y]]
        else:
            for x in range(6):
                goals = goals + [[x,y]]

    
    goals.remove([5,5]) # Não pode entrar no curral!
    checked = []        # Guarda as casas examinadas

    # Verificar o primeiro quadrado antes de mais
    checkNeighbors() 
    checked = checked + [copy.copy(location)]

    goal = 0   # Para percorrer os goals

    # Enquanto não são encontradas todas as ovelhas e todas as paredes, percorre goals
    while (goal < len(goals)):
        if (len(sheep) < 2 or len(walls) < 6):
            while ( location != goals[goal]):                   # Para cada goal...
                if ( location not in checked ):                 # Se a casa atual não foi verificada...
                    checkNeighbors()                            # Verifica-a
                    checked = checked + [copy.copy(location)]   # Adiciona-a à lista
                    for s in sheep:                             # Para cada ovelha
                        if s in goals:                          # Vê se a sua localização está em goals
                            goals.remove(s)                     # Remove-a

                # Define o caminho a tomar para o goal
                path = pathfinding.getPath(location,goals[goal])

                if (path):                              # Se o caminho não está bloqueado dirige-se para o próximo passo
                    goToAdj(path[0])                    # [0] se a casa atual não é parte do path, [1] caso contrário
                else:                                   # Senão...
                    ev3.speaker.say("No path found.")   # O robot queixa-se
                    quit()                              # E o jogo acaba

            goal = goal + 1     # Com este goal atingido, passa ao próximo
        else:
            break

# Para verificar uma casa
def checkNeighbors():
    # Verifica todos os lados
    for i in range(4):
        canMove()
        wait(500)
        turn(-1)
        wait(1000)
    # Atualiza as restrições de pathfinding
    pathfinding.setRestrictions([5,5],walls,sheep+[[5,5]])


def checkSheeps(s):
    for i in range(4):
        if (spot()):
            sheep[s] = getFront()
            pathfinding.setRestrictions([5,5],walls,sheep+[[5,5]])
            break
        wait(500)
        turn(-1)
        wait(500)
    

def lostSheep(s):
    move()
    if (not spot):
        while(not(spot())):
            if (coinToss==0):
                move()
                checkSheeps(s)
            else:
                turn(-1)
                move()
                checkSheeps(s)


def takeSheep(s):

    pathfinding.illegal_tiles.clear()
    sheep_path = pathfinding.getPath(sheep[s],[5,5])
    pathfinding.illegal_tiles = copy.copy(sheep + [[5,5]])
    v = s+1
    print ("Illegal Tiles" + str(pathfinding.illegal_tiles))
    print ("Caminho da ovelha " , v , ": " + str(sheep_path))
    print ("Location: " + str(location))
    print ("Ovelha " , v , ": " + str(sheep[s]))
    if (sheep_path):
        moveSheepAdj(s,sheep_path[0],True)
        wait(2000)
        while( sheep_path ):
            if( moveSheepAdj(s,sheep_path[0],False) ):
                sheep_path = sheep_path[1:]
            else:
                '''move()
                ev3.speaker.beep(1)
                wait(1000)
            
                move()
                for i in range (4):
                    turn(1)
                    ev3.speaker.say("Peekaboo")
                    if(spot()):
                        sheep[s]=getFront()'''
                takeSheep(s)
                break
                '''
                if ( spot() ):
                    sheep[s] = getFront()
                    takeSheep(s)
                    break
                '''
            wait(2000)

        return
    else:
        ev3.speaker.play_file(SoundFile.FANFARE)

def moveSheepAdj(s,target,first_move):

    back_sheep = [0,0]
    
    back_sheep[1] = sheep[s][1] + (sheep[s][1] - target[1])
    back_sheep[0] = sheep[s][0] + (sheep[s][0] - target[0])

    path = pathfinding.getPath(location,back_sheep)

    if (first_move):
        followPath(path)
    else:
        if (len(path) < 3):
            followPath(path)
            print ("Location: " + str(location))
            print ("Ovelha ",s,": "+ str(sheep[s]))
            turnTo(sheep[s])
            wait(1000)
            if(not spot()):
                lostSheep(s)
            bark()
            sheep[s] = copy.copy(target)
            pathfinding.setRestrictions([5,5],walls,sheep+[[5,5]])
            return True
        else:
            if(sheepIsFacingWall(s) or isSheepOnMargin(s)):
                move()
                if(not spot()):
                    lostSheep(s)
                bark()
                newPos = getSheepNewPos(s)
                sheep[s] = ([sheep[s][0] + newPos[0],sheep[s][1] + newPos[1]])
                pathfinding.setRestrictions([5,5],walls,sheep+[[5,5]])
                path = pathfinding.getPath(location,sheep[s])
            return False

# Função de jogo
def play():
    ev3.speaker.say("Phase 1")
    pathfinding.setRestrictions([5,5],walls,sheep+[[5,5]])
    map()
    followPath(pathfinding.getPath(location,[0,0]))
    turnTo([1,0])
    ev3.speaker.say("Phase 2")
    takeSheep(0)
    takeSheep(1)
    log()
    die()