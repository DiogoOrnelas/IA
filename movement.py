############################### IMPORTS ###############################

from brick import *
from action import spot
import copy

############################### INICIALIZAÇÂO DE VARIÁVEIS ###############################

# Inicialização dos motores e sensores
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
touch_sensor = TouchSensor(Port.S3)

# Variáveis de jogo
moves = 0           # Número de jogadas
location = [0,0]    # Coordenadas do robot (x,y)
facing = 1          # Orientação do robot { 0->NORTH 1->EAST 2->SOUTH 3->WEST }
walls = []          # Paredes encontradas
unwalls = []        # Caminhos livres encontrados
sheep = []          # Posição inicial das ovelhas

# walls = [[[5,0],[5,1]],[[5,0],[5,1]],[[5,0],[5,1]],[[5,0],[5,1]],[[5,0],[5,1]],[[5,0],[5,1]]]
# walls = [ [[0,1],[0,2]] , [[2,1],[2,2]] , [[0,4],[0,5]] , [[1,3],[2,3]] , [[3,3],[3,4]] , [[4,0],[4,1]] ]

############################### FUNÇÕES ###############################

############################### Funções que lidam com movimento
# Função de paragem
def stop():
    left_motor.stop(Stop.BRAKE)
    right_motor.stop(Stop.BRAKE)
    wait(500)

# Função de andamento
def walk(speed):
    right_motor.run(speed)
    left_motor.run(speed)

# Função de rotação
def turn(direction):
    global facing

    # Rodar na direção pedida
    left_motor.run(direction * 270)
    right_motor.run(direction * -270)
    wait(750)

    # Parar motores
    left_motor.stop()
    right_motor.stop()
    facing = (facing + direction) % 4

# Faz o robot mover-se
def move():
    global facing
    if ( canMove() ):
        walk(450)
        wait(1225)           
        if ( facing == 0 ):
            location[1] += 1
        elif( facing == 1 ):
            location[0] += 1       
        elif( facing == 2 ):
            location[1] -= 1
        else:
            location[0] -= 1  
        stop()      
        return True
    else:
        ev3.light.on(Color.RED)
        wait(1000)
        ev3.light.on(Color.GREEN)
        return False   

# Avalia se o robot está numa margem, a apontar para fora
def isOnMargin():
    return ((facing == 0) and (location[1] == 5)) or ((facing == 1) and (location[0] == 5)) or ((facing == 2) and (location[1] == 0)) or ((facing == 3) and (location[0] == 0))   

#Avalia se a Ovelha se encontra numa margem 
def isSheepOnMargin(s):
    return ((facing == 0) and (sheep[s][1] == 5)) or ((facing == 1) and (sheep[s][0] == 5)) or ((facing == 2) and (sheep[s][1] == 0)) or ((facing == 3) and (sheep[s][0] == 0))   


def followPath(path):
    while ( len ( path ) ): 
        goToAdj(path[0])
        path = path[1:]

def turnTo(target):
    axis = [[1,3],[0,2]]
    priority = 0

    while ( priority < 2):
        if location[priority] < target[priority]:
            while facing != axis[priority][0]:
                if(facing == 3 and axis[priority][0]==0):
                    turn(1)
                turn_to = axis[priority][0] - facing
                if(turn_to > 0):
                    while(turn_to > 0):
                        turn(1)
                        turn_to = turn_to - 1
                elif(turn_to < 0):
                    while(turn_to < 0):
                        turn(-1)
                        turn_to = turn_to + 1
        priority = priority + 1
   
    return True

def goToAdj(target):

    axis = [[1,3],[0,2]]
    priority = 0

    while( location != target ):
        while location[priority] != target[priority]:
            # Rodar na direção certa do eixo desejado
            if location[priority] < target[priority]:
                while facing != axis[priority][0]:
                    if(facing == 3 and axis[priority][0]==0):
                        turn(1)
                    turn_to = axis[priority][0] - facing
                    if(turn_to > 0):
                        while(turn_to > 0):
                            turn(1)
                            turn_to = turn_to - 1
                    elif(turn_to <0):
                        while(turn_to<0):
                            turn(-1)
                            turn_to = turn_to + 1
            elif location[priority] > target[priority]:
                while facing != axis[priority][1]:
                    if(facing == 0 and axis[priority][1]==3):
                        turn(-1)
                    turn_to = axis[priority][1] - facing
                    if(turn_to > 0):
                        while(turn_to > 0):
                            turn(1)
                            turn_to = turn_to - 1
                    elif(turn_to <0):
                        while(turn_to<0):
                            turn(-1)
                            turn_to = turn_to + 1
            if ( not move() ):
                return False

        priority = priority + 1
    return True

############################### Funções heurísticas

# Função para guardar a parede
def setWall(a,b):
        _a = ( copy.copy(a) )
        _b = ( copy.copy(b) )
        if ( [_a,_b] not in walls and [_b,_a] not in walls ):
            walls.append( [_a,_b][:] )

# Função para guardar a ovelha
def setSheep(c):
        _c = ( copy.copy(c) )
        if ( [_c] not in sheep):
            sheep.append( _c[:] )

# Função para guardar os caminhos livres
def setUnwall(a,b):
        _a = ( copy.copy(a) )
        _b = ( copy.copy(b) )
        if ( [_a,_b] not in unwalls and [_b,_a] not in unwalls ):
            unwalls.append( [_a,_b][:] )

# Verifica se há uma parede guardada à sua frente
def isFacingWall():
    return ([location,getFront()] in walls) or ([getFront(),location] in walls)

def sheepIsFacingWall(s):
    return ([sheep[s],getFrontSheep(s)] in walls) or ([getFrontSheep(s),sheep[s]] in walls)

def isFacingUnwall():
    return ([location,getFront()] in unwalls) or ([getFront(),location] in unwalls)

# Verificar a existência de uma possível parede não guardada
def wallCheck():
    walk(80)
    wait(1000)
    if (touch_sensor.pressed()):
        stop()
        ev3.light.on(Color.ORANGE)
        wall_found = True
        #Guardar posição da parede      
        setWall(location,getFront())
    else:
        stop()
        wall_found = False
        setUnwall(location,getFront())
    walk(-60)
    wait(1000)
    stop()
    ev3.light.on(Color.GREEN)
    return wall_found

# Devolve a coordenada em frente do robot
def getFront():
    front = [0,0]
    if (facing == 0):
        front[1] = location[1] + 1
        front[0] = location[0] 
    elif (facing == 1):
        front[1] = location[1] 
        front[0] = location[0] + 1    
    elif (facing == 2):
        front[1] = location[1] - 1
        front[0] = location[0] 
    elif (facing == 3):
        front[1] = location[1] 
        front[0] = location[0] - 1
    return front

#Indica qual o quadrado que segue após o robo ladrar para certa ovelha (Sendo que o robo deve estar a olhar na direção da ovelha)
def getFrontSheep(s):
    front = [0,0]
    if (facing == 0):
        front[1] = sheep[s][1] + 1
        front[0] = sheep[s][0] 
    elif (facing == 1):
        front[1] = sheep[s][1] 
        front[0] = sheep[s][0] + 1    
    elif (facing == 2):
        front[1] = sheep[s][1] - 1
        front[0] = sheep[s][0] 
    elif (facing == 3):
        front[1] = sheep[s][1] 
        front[0] = sheep[s][0] - 1
    return front

#Indica qual a nova posição da ovelha, após ser empurrada pelo robo contra uma parede (Partimos sempre do principio que a direita está disponível)
def getSheepNewPos(s):
    newPos = [0,0]
    if (facing == 0):
        newPos=[1,0]
    elif (facing == 1):
        newPos=[0,-1]
    elif (facing == 2):
        newPos=[-1,0]
    elif (facing == 3):
        newPos=[0,1]
    return newPos
    
# Determina se pode andar para a frente
def canMove(): 
    if ( not isFacingWall() ):
        if ( not isFacingUnwall() ):
            if (len(walls) < 6):
                if(spot() and (len(sheep) <2)): 
                    setSheep(getFront())
                return not ( isOnMargin() or wallCheck() or ( getFront() == [5,5] ) or spot() )
                
            else:
                if(spot() and (len(sheep) <2)): 
                    setSheep(getFront())
                return not ( ( getFront() == [5,5] )  or isOnMargin() or spot() )
                
        else:
            if(spot() and (len(sheep) <2)):  
                    setSheep(getFront())
            return not ( ( getFront() == [5,5] ) or isOnMargin() or spot()  )
            
    else:
        return False


# Sinal de bloqueio
def die():
    ev3.light.on(Color.RED)
    ev3.speaker.say("dead")
    raise SystemExit