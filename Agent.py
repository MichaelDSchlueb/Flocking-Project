import numpy as np
from random import random
from copy import copy

class Agent:
    def __init__(self, x, y, heading, type):
        self.acc = np.array([0.01, 0.01])
        self.vel = np.array([((random()*50)-25)/10.0,
                             ((random()*50)-25)/10.0])
        self.x = x
        self.y = y
        self.heading = heading # heading in degrees, 0 is straight down and angles increase clockwise
        self.type = type
        self.ahead = np.array([0, 0])
        self.avoidingObstacle = True

    def addToVel(self, vec):
        self.vel = self.vel + vec

    def addToPos(self, vec):
        self.x += vec[0]
        self.y += vec[1]

    def getAcc(self):
        return(self.acc)

    def getAhead(self):
        return(self.ahead)

    def getHeading(self):
        return(self.heading)

    def getPos(self):
        return(np.array([self.x, self.y]))

    def getType(self):
        return(self.type)

    def getVel(self):
        return(self.vel)

    def getX(self):
        return(self.x)

    def getY(self):
        return(self.y)

    def isAvoidingObstacle(self):
        return(self.avoidingObstacle)

    def isPredator(self):
        return(self.type == "predator")

    def resetAcc(self):
        self.acc = np.array([0,0])

    def resetVel(self):
        self.vel = np.array(
            [((random()*50)-25)/10.0,
             ((random()*50)-25)/10.0] )

    def setAcc(self, acc):
        self.acc = acc

    def setAhead(self, ahead):
        self.ahead = ahead

    def setAvoidingObstacle(self, avoidingObstacle):
            self.avoidingObstacle = copy(avoidingObstacle)

    def setPos(self, vec):
        self.x = vec[0]
        self.y = vec[1]

    def setHeading(self, heading):
        self.heading = heading

    def setVel(self, vec):
        self.vel = copy(vec)

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def steer(self, vec):
        self.vel = self.vel - vec

    def stop(self):
        self.vel = np.array([0, 0])
