############################### IMPORTS ###############################

from brick import *

# Inicialização dos motores e sensores

spin_motor = Motor(Port.B)
distance_sensor = UltrasonicSensor(Port.S2)

############################### FUNÇÕES ###############################

# Função de berro
def bark():
    # Berrar, assustando as ovelhas
    ev3.speaker.play_file(SoundFile.DOG_BARK_2)

# Função de toque
def touch():
    # Alcance de toque é 150
    # Rodar o motor mais pequeno, com o chicote
    spin_motor.run(-80)
    wait(1000)
    spin_motor.run(80)
    wait(1000)
    spin_motor.stop()

# Função de deteção de ovelhas
def spot():   
    # Caso dete um objeto a 260 de distância, devolve True
    if (distance_sensor.distance() < 160):
        ev3.speaker.play_file(SoundFile.DOG_SNIFF)
    return distance_sensor.distance() < 160
