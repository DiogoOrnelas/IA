############################### IMPORTS ###############################

# Ferramentas do EV3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, UltrasonicSensor)
from pybricks.parameters import Port, Color, Stop
from pybricks.tools import wait
from pybricks.media.ev3dev import SoundFile

############################### INICIALIZAÇÂO DE VARIÁVEIS ###############################

# Inicialização do brick
ev3 = EV3Brick()
ev3.speaker.set_volume(80)
