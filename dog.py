#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random

# Código para representar o cão pastor

class dog:
    loc = [0,0]
    front = [0,1]
    facing = 1      # 0->NORTH 1->EAST 2->SOUTH 3->WEST
    
    ev3 = EV3Brick()
    
    left_motor = Motor(Port.A)
    right_motor = Motor(Port.D)
    spin_motor = Motor(Port.B)
    distance_sensor = UltrasonicSensor(Port.S2)
    touch_sensor = TouchSensor(Port.S3)
    
    # Inicializador; start é a posição inicial; start_facing é a direção inicial

    def __init__(self,start,start_facing):
    
        self.loc = start
        self.facing = start_facing

        self.ev3.speaker.set_volume(80)
    
    def setFront(self):
        if(self.facing == 0):
            self.front[1] = self.loc[1] + 1
            self.front[0] = self.loc[0] 
        elif(self.facing == 1):
            self.front[1] = self.loc[1] 
            self.front[0] = self.loc[0] + 1    
        elif(self.facing == 2):
            self.front[1] = self.loc[1] - 1
            self.front[0] = self.loc[0] 
        else:
            self.front[1] = self.loc[1] 
            self.front[0] = self.loc[0] - 1

    # Verifica se está frente a frente a uma parede

    def isFacingWall(self,b):
        return ((self.loc,self.front) in b.walls) or ((self.front,self.loc) in b.walls)

    # Verifica se está numa margem

    def isOnMargin(self):
        is_on_margin = True
        # CANTOS
        if (self.loc == [0,0]):
            if (self.facing == 2 ):
                self.turn(-1)
            elif (self.facing ==3):
                self.turn(1)
        elif (self.loc == [5,0]):
            if (self.facing ==1):
                self.turn(-1)
            elif(self.facing ==2):
                self.turn(1)
        elif (self.loc == [0,5]):
            if(self.facing ==3):
                self.turn(-1)
            elif(self.facing ==0):
                self.turn(1)
        elif (self.loc == [5,5]):
            if (self.facing ==0):
                self.turn(-1)
            elif (self.facing ==1):
                self.turn(1)
        # MARGENS
        elif (self.loc[0]==0):
            if (self.facing ==3):
                self.turn(1)
        elif (self.loc[0]==5):
            if (self.facing ==1):
                self.turn(1)
        elif (self.loc[1]==0):
            if (self.facing ==2):
                self.turn(1)
        elif (self.loc[1]==5):
            if (self.facing ==0):
                self.turn(1)
        else:
            is_on_margin = False
        return is_on_margin

    # Função de movimento

    def move(self,b):
        if( (self.front == [5,5]) or self.wall_check(b) or self.spot() ):
            ev3.light.on(Color.RED)
            wait(1000)
            ev3.light.on(Color.GREEN)
            return False
        else:
            left_motor.run(450)
            right_motor.run(450)
            wait(1000)           
            if(self.facing ==0):
                self.loc[1] += 1
            elif(self.facing == 1):
                self.loc[0] += 1       
            elif(self.facing == 2):
                self.loc[1] -= 1
            else:
                self.loc[0] -= 1  
            self.stop()            
            self.setFacing()
            print (self.loc)
            print (self.front)
            return True

    # Função de rotação
    def turn(self, direction):
        #Rodar para direction
        left_motor.run(direction * 115)
        right_motor.run(direction * -115)
        wait(1600)
        self.stop()
        if self.facing ==0 and direction ==-1:
            self.facing =3         
        elif self.facing==3 and direction ==1:
            self.facing =0
        else:
            self.facing = self.facing + direction
        self.setFacing()
        
    #função de paragem
    def stop(self):
        left_motor.stop()
        right_motor.stop()
        wait(1000)

    # Função de berro
    def bark(self):
        #Berrar, assustando as ovelhas
        ev3.speaker.play_file(SoundFile.DOG_BARK_2)

    # Função de toque
    # Alcance de toque é 150
    def touch(self):
        #Rodar o motor mais pequeno, com o chicote
        spin_motor.run(-80)
        wait(1000)
        spin_motor.run(80)
        wait(1000)
        spin_motor.stop()
        self.setFacing()
    
    # Função de deteção de ovelhas
    # Caso dete um objeto a 260 de distância, devolve True 
    def spot(self):   
        return distance_sensor.distance()<160

    def wall_check(self,b):
        right_motor.run(80)
        left_motor.run(80)
        wait(1000)
        if (touch_sensor.pressed()):
            self.stop()
            ev3.light.on(Color.ORANGE)
            wall_found = True
            #Guardar posição da parede
            self.setFront()        
            b.setWall(self.loc,self.front)
        else:
            self.stop()
            wall_found = False

        right_motor.run(-60)
        left_motor.run(-60)
        wait(1000)
        self.stop()
        ev3.light.on(Color.GREEN)
        return wall_found

