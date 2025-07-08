
from Agent import Agent
from random import random


class Obstacle(Agent):
    def __init__(self, x, y, heading, type):
        super().__init__(x, y, heading, type)
        self.radius = 30+(random()*20-10)

    def getRadius(self):
        return(self.radius)
