import cartesius as c
import neural_network as nn
from graphics import *


#gera o mapa a ser simulado
map_extension = [700, 600]
MAP = c.Space(map_extension)

#cria a interface gráfica
window = GraphWin("Simulation", map_extension[0], map_extension[1])

#aquisição do número de objetos
n_obj = int(input("Insert n_obj: "))

#gera os objetos por meio de cliques na janela
pair_points = []
objects = []
cartesius_objcts = []
for i in range(n_obj):
    p1 = window.getMouse()
    p2 = window.getMouse()
    pair_points.append([p1, p2])
    print("Object ", (i+1), ": ", pair_points[i])
    rect = Rectangle(pair_points[i][0], pair_points[i][1])
    objects.append(rect)
    rect.draw(window)
    #converte os objetos do módulo graphics para o módulo cartesius
    cartesius_objcts.append([c.Point(p1.getX(), p1.getY()), c.Point(p2.getX(), p2.getY())])



    

window.getMouse()
window.close()
