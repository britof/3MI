#Cartesius
#
#added classes for simulation


import math
import graphics

class Point:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def through(self, point):
        line_through_points = Line((self.Y - point.Y),(point.X - self.X),((self.X*point.Y)-(point.X*self.Y)))
        return line_through_points

    def coordinates(self, i):
        if(i==0):
            return self.X
        if(i==1):
            return self.Y
    
    def distance_to(self, point):
        deltaX = self.X - point.X
        deltaY = self.Y - point.Y
        s = (deltaX*deltaX) + (deltaY*deltaY)
        distance = math.sqrt(s)
        return distance

class Line:

    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C
        self.show()

    def f(self, x):
        return -(self.C + (self.A*x))/self.B

    def get_x(self, y):
        return -(self.C + (self.B*y))/self.A

    def show(self):
        print(self.A, 'x + ', self.B, 'y + ', self.C, '= 0')
                                   

class Segment:
    def __init__(self, line, origin, destiny):
        self.line = line
        self.origin = origin
        self.destiny = destiny

#####################################################################################################
class Space:
    def __init__(self, extension):
        self.height = extension[0]
        self.width = extension[1]
        self.objects = []

    def insert_object(self, pointA, pointC):#todo objeto é um retângulo descrito por quatro vértices
        pointB = Point(pointA.X, pointC.Y)
        pointD = Point(pointC.X, pointA.Y)
        self.objects.append([pointA, pointB, pointC, pointD])


class SimulatedRobot:
    def __init__(self, initial_position):
        self.initial_position = initial_position
        self.points = []#pontos que indicam os feixes {self.point, point}
        self.direction = Point(initial_position.X, (initial_position.Y+4))#ponto que indica a orientação
        self.points.append(Point(initial_position.X+(4*unidade), initial_position.Y))
        for i in range(10):#dez feixes não horizontais
            x = math.cos((i+1)*15)*4#distância * cos == x
            y = math.sin((i+1)*15)*4#distância * sen == y
            p = Point(x, y)
            self.points.append(p)
        self.points.append(Point(initial_position.X-4, initial_position.X))

    def get_spacial_projection(self, rect_points):
        robot = self.initial_position
        if(robot.Y >= rect_points[0].Y and robot.Y <= rect_points[1].Y):#left/right
            if(robot.X < rect_points[2].X):
                return [rect_points[0], rect_points[1]]
            else:
                return [rect_points[3], rect_points[2]]

        elif(robot.X >= rect_points[0].X and robot.X <= rect_points[3].X):#above/below
            if(robot.Y < rect_points[0].Y):
                return [rect_points[0], rect_points[3]]
            else:
                return [rect_points[1], rect_points[2]]
            
    def measure(self, point, space):
        for i in range(len(space.objects)):#para cada objeto no espaço
            if(point.Y >= space.objects[i][0].Y and point.Y <= space.objects[i][1].Y):    #verifica se o ponto do feixe
                if(point.X >= space.objects[i][0].X and point.X <= space.objects[i][1].X):#está contido no objeto
                    line = self.initial_position.through(point)#equação que contêm o feixe
                    intercepted_face = self.get_spacial_projection(space.objects[i])#face interceptada pelo feixe
                    if(intercepted_face[0].X == intercepted_face[1].X):#se a face é vertical
                        x = intercepted_face[0].X
                        y = line.f(x)
                        intersection = Point(x, y)
                    else:#a face é horizontal
                        y = intercepted_face[0].Y
                        x = line.get_x(y)
                        intersection = Point(x, y)
                    break
        distance = self.initial_position.distance_to(intersection)
        return distance
        
    def getMeasurements(self):
        measurements = []
        for i in range(12):
            m = measure(self.points[i])
            measurements.append(m)
#####################################################################################################

class Route:
    def __init__(self):
        self.way = []

    def appendSegment(self, segment):
        self.way.append(segment)

    def nextStep(self, matched_points):
        return self.way[(matched_points-1)]

    def newRoute(self, matched_points, end):
        new_route = Segment(self.way[-1].destiny.through(end), self.way[-1].destiny, end)
        setRight(matched_points, new_route)

    def setRight(self, matched_points, wrng_segment):                                                                                                                     
        next_point = nextStep(matched_points).destiny
        right_line = wrng_segment.destiny.through(next_point)
        right_segment = Segment(right_line, wrng_segment.destiny, next_point)
        return right_segment                                    
