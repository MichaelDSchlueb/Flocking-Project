import math
from random import random

from Constants import *
from Agent import Agent
from Obstacle import Obstacle
from Behaviors import Behaviors

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import numpy as np

class GuiFlockingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.stop                = True
        self.weightAvoid         = 4.0/8.0
        self.weightAlign         = 3.0/8.0
        self.weightApproach      = 1.0/8.0
        self.weightAvoidObstacle = 2.0
        self.weightFlee          = 1.0
        self.numPrey             = 100
        self.brush = QBrush(QColor(255,0,0))
        self.preyAgents = []
        self.predatorAgents = []
        self.obstacles = []
        self.flockingBehaviors   = Behaviors()
        self.showTheFeelers = False

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

    def addAnotherAgent(self, numAgents):
        self.numPrey = numAgents
        self.initialize()

    def getNumObstacles(self):
        return(len(self.obstacles))

    def getNumPredators(self):
        return(len(self.predatorAgents))

    def getNumPrey(self):
        return(len(self.preyAgents))

    def initialize(self):
        self.createPrey(self.numPrey)

    def createPrey(self, numPrey):
        width  = self.parentWidget().width()
        height = self.parentWidget().height()
        for i in range(numPrey):
            xloc = random()*width
            yloc = random()*height
            newAgent = Agent(xloc, yloc, 0, "prey")
            self.preyAgents.append(newAgent)

        return len(self.preyAgents)

    def createPredators(self, numPredators):
        width  = self.parentWidget().width()
        height = self.parentWidget().height()

        for i in range(numPredators):
            newAgent = Agent(random()*width, random()*height, 0, "predator")
            self.predatorAgents.append(newAgent)

        return len(self.predatorAgents)

    def createObstacles(self, numObstacles):
        width  = self.parentWidget().width()
        height = self.parentWidget().height()
        margin = 50

        for i in range(numObstacles):
            xloc = margin+random()*(width-2*margin)
            yloc = margin+random()*(height-2*margin)
            newAgent = Obstacle(xloc, yloc, 0, "obstacle")
            self.obstacles.append(newAgent)
        return len(self.obstacles)

    def createTestObstacle(self):
        numTestObstacles = 1
        width  = self.parentWidget().width()
        height = self.parentWidget().height()

        for i in range(numTestObstacles):
            newAgent = Obstacle(width/4, height/2, 0, "obstacle")
            self.obstacles.append(newAgent)

        return (numTestObstacles)

    def keepInFlockingArea(self, curAgent):
        width  = self.width()
        height = self.height()
        agentPos = curAgent.getPos()
        margin = 20

        if (agentPos[0] < -margin):
            agentPos[0] = width+margin
        elif (agentPos[0] > width+margin):
            agentPos[0] = -margin

        if (agentPos[1] < -margin):
            agentPos[1] = height+margin
        elif (agentPos[1] > height+margin):
            agentPos[1] = -margin

        curAgent.setPos(agentPos)

    def paintEvent(self, event):
        # Create object with center at origin
        preyPoints = [
            QPoint(-3, -5),
            QPoint( 3, -5),
            QPoint( 0,  5),
            QPoint(-3, -5)]

        predatorPoints = [
            QPoint(-4, -6),
            QPoint( 4, -6),
            QPoint( 0,  6),
            QPoint(-4, -6)]

        pos = np.array([0, 0])
        ahead = np.array([0, 0])

        x,y,r = 0, 0, 0
        redPen = QPen(QColor(255,0,0))
        blackPen = QPen(QColor(0,0,0))
        redBrush = QBrush(QColor(255,0,0))
        blackBrush = QBrush(QColor(0,0,0))

        painter = QPainter(self)
        painter.setBrush(self.brush)

        # Draw obstacles
        for curObstacle in self.obstacles:
            pos = curObstacle.getPos()
            x = pos[0]
            y = pos[1]
            r = curObstacle.getRadius()
            # topleft, bottom right, created at origin
            boundingRect = QRectF(QPointF(-r,-r), QPointF(r,r))
            painter.save()
            painter.translate(float(x),float(y))
            painter.drawEllipse(boundingRect)
            painter.restore()

        # Draw prey agents
        for curAgent in self.preyAgents:
            self.updateAgentPosition(curAgent)
            pos   = curAgent.getPos()
            ahead = curAgent.getAhead()

            # Draw agent triangle
            painter.save()
            painter.translate(float(pos[0]), float(pos[1]))
            painter.rotate(curAgent.getHeading())
            painter.setPen(blackPen)
            painter.setBrush(blackBrush)
            painter.drawPolygon(preyPoints)
            painter.restore()

            # Draw agent ahead line
            if self.showTheFeelers:
                painter.save()
                painter.translate(float(pos[0]), float(pos[1]))
                painter.setPen(redPen)
                pt1 = QPoint(0,0)
                pt2 = QPoint(curAgent.getAhead()[0] - pos[0],
                             curAgent.getAhead()[1] - pos[1])
                painter.drawLine(pt1, pt2)
                painter.restore()

        # Draw predator agents
        for curAgent in self.predatorAgents:
            self.updateAgentPosition(curAgent)
            pos = curAgent.getPos()

            painter.save()
            painter.translate(float(pos[0]), float(pos[1]))
            painter.rotate(curAgent.getHeading())
            painter.setPen(redPen)
            painter.setBrush(redBrush)
            painter.drawPolygon(predatorPoints)
            painter.restore()

        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))

    def removePredators(self):
        self.predatorAgents.clear()

    def removeObstacles(self):
        self.obstacles.clear()

    def removePrey(self):
        self.numPrey = 0
        self.preyAgents.clear()

    def setBrush(self, brush):
        self.brush = brush
        self.update()

    def setNumAgents(self, numAgents):
        width  = self.parentWidget().width()
        height = self.parentWidget().height()

        # Create prey agents here
        self.preyAgents.clear()
        for i in range(numAgents):
            newAgent = Agent(width/2, height/2, 0, "prey")
            self.preyAgents.append(newAgent)

    def setNumObstacles(self, numObstacles):
        width  = self.parentWidget().width()
        height = self.parentWidget().height()

        self.obstacles.clear()
        for i in range(self.numObstacles):
            newAgent = Obstacle(width/4, height/2, 0, "obstacle")
            self.obstacles.append(newAgent)

    def setWeightAvoid(self, val):
        self.weightAvoid = val

    def setWeightAlign(self, val):
        self.weightAlign = val

    def setWeightApproach(self, val):
        self.weightApproach = val

    def showFeelers(self, value):
        self.showTheFeelers = value

    def updateAgentPosition(self, curAgent):

        #heading = 0
        finalAcc = np.array([0, 0])

        if self.stop:
            return

        # Rule 1: Avoid Neighbors
        avoidAcc  = self.flockingBehaviors.adjustAccForNeighborAvoidance(curAgent, self.preyAgents)
        avoidAcc  = avoidAcc * self.weightAvoid

        # Rule 2: Steer towards average neighbor velocity
        alignAcc  = self.flockingBehaviors.adjustAccForNeighborVelocity(curAgent, self.preyAgents)
        alignAcc  = alignAcc * self.weightAlign

        # Rule 3: Steer towards average neighbor position
        approachAcc  = self.flockingBehaviors.adjustAccForNeighborPosition(curAgent, self.preyAgents)
        approachAcc  = approachAcc * self.weightApproach

        # Rule 4: Steer away from fixed objects
        avoidObstacleAcc = self.flockingBehaviors.adjustAccForObstacleAvoidance(curAgent, self.obstacles)
        avoidObstacleAcc = avoidObstacleAcc * self.weightAvoidObstacle

        # Rule 5: Flee Rule Move in opposite direction from predator as soon as you detect one
        fleeAcc  = self.flockingBehaviors.adjustAccForFleeing(curAgent, self.predatorAgents)
        fleeAcc  = fleeAcc * self.weightFlee

        # Calculate total acc
        finalAcc = finalAcc + avoidAcc
        finalAcc = finalAcc + alignAcc
        finalAcc = finalAcc + approachAcc
        finalAcc = finalAcc + avoidObstacleAcc
        finalAcc = finalAcc + fleeAcc

        # Update the velocity
        curAgent.addToVel(finalAcc)
        vel = curAgent.getVel()

        # Apply velocity to the position and set heading
        curAgent.addToPos(vel)
        heading = float(math.atan(vel[1]/vel[0]))
        heading = math.degrees(heading) - 90.0
        if (vel[0] < 0):
            heading += 180
        curAgent.setHeading(heading)

        # Perform wraparound if necessary
        self.keepInFlockingArea(curAgent)
        self.flockingBehaviors.adjustVelForBoundaryCondition(curAgent)

        # Reset the acceleration
        curAgent.resetAcc()


    # ----- callbacks -----

    def callback_stop(self):
        self.stop = not self.stop

    def callback_reset(self):
        pos = np.array([0, 0])

        width  = self.parentWidget().width()
        height = self.parentWidget().height()

        for obstacle in self.obstacles:
            pos = np.array([random()*width,
                            random()*height])
            obstacle.setPos(pos)

        pos = np.array([width/2, height/2]);
        for curAgent in self.preyAgents:
            curAgent.setPos(pos)
            curAgent.resetAcc()
            curAgent.resetVel()
