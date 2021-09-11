from turtle import Turtle, Screen, color
import time
import turtle

TURTLE_SIZE = 20  #tamaño del jugador
WORLD_SIZE = 100  #cuadrado de 100 x 100
angleMap = {'N':90,'E':0,'S':270,'W':180}  #Map para traducir direcciones en angulos de turtle
colorList = ["red", 'blue', 'yellow', 'green', 'orange', 'black']

#players es una lista donde cada elemento es una terna de [x,y,dir]
#la coordenada (0,0) está en el centro de la pantalla, por lo que x e y van de -WORLD_SIZE/2 hasta WORLD_SIZE/2
#si las coordenadas a dibujar son de 0 a WORLD_SIZE, se deberá hacer la transformación correspondiente.
#screen es la pantalla donde se dibuja
def updateWorld (players, screen):
    screen.clear()    #Se puede comentar para ver la traza de cada tortuga
    i = 0
    for p in players:
        #creo a la tortuga pepe
        pepe = Turtle(shape="turtle", visible=False)
        pepe.color (colorList[i])

        #para dibujar la tortuga en una pos inicial, se inicia oculta y se mueve a la pos deseada, luego se muestra
        pepe.speed(0)
        pepe.penup()
        pepe.goto((p[0]/(WORLD_SIZE/2))*(screen.window_width()/2-TURTLE_SIZE/2), (p[1]/(WORLD_SIZE/2))*(screen.window_height()/2-TURTLE_SIZE/2))
        pepe.tiltangle(angleMap.get(p[2]))
        pepe.showturtle()

        i = (i+1) % 6 #no acepta mas de 6 colores distintos, se puede extender la lista


#ejemplo de uso

screen = Screen()
screen.setup(1000,1000)
players = [[5,7,'N'],[20,30,'S'],[-40,3,'E'],[40,-10,'W']]  #ver que las coordenadas van de -50 a 50 en este caso.
#llamo a la función que dibuja la posición inicial de cada jugador
updateWorld (players, screen)

#ejemplo de uso donde en cada iteración cada jugador avanza en su dirección inicial
for x in range(500):
    time.sleep(0.1)
    players[0][1] = players[0][1] + 0.5
    players[1][1] = players[1][1] - 0.5
    players[2][0] = players[2][0] + 0.5
    players[3][0] = players[3][0] - 0.5
    print(players)
    updateWorld (players, screen)
