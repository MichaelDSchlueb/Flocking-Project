import math
from copy import copy
import Utils as utils
import Constants as consts
import numpy as np

class Behaviors:
    def __init__(self):
        pass

    #
    # You may see erratic movements with your agents as they enounter obstacles
    # and predators. Use this method to put an upper limit on their return values.
    # N.B. You may have to modify the MAX_SPEED constant for you implementation.
    #
    def limitSpeed(self, velocity):
        speed = utils.length(velocity)
        if speed > consts.MAX_SPEED:
            return utils.normalize(velocity) * consts.MAX_SPEED
        return velocity

    #
    # For collisions, you'll need to detect whether the look ahead line intersects
    # an obstacle (i.e., a circle). Instead of calculating the intersection of the actual
    # look-ahead line with a circle, approximate by testing 3 points: the base of the line,
    # the half-way point of the line, and the end of the line.
    #
    def lineIntersectsCircle(self, aheadNone, ahead, aheadHalf, obstacle):

        # Make the obstacle radius a bit bigger so as to
        # give the code enough time to calculate intersections
        # before they've already happened for a few frames.
        obstacleFactor = 1.2
        obstacleRadius = obstacleFactor * obstacle.getRadius()

        distNone = (utils.distance(obstacle.getPos(), aheadNone) <= obstacleRadius)
        distHalf = (utils.distance(obstacle.getPos(), aheadHalf) <= obstacleRadius)
        dist     = (utils.distance(obstacle.getPos(), ahead)     <= obstacleRadius)

        return (distNone or dist or distHalf)

    #
    # Need to recalculate the ahead vector so that the boundary
    # case won't draw one from one edge of the drawing area to
    # the other.
    #
    def adjustVelForBoundaryCondition(self, curAgent):
        ahead = np.array([0, 0])
        agentPos = curAgent.getPos()
        agentVel = curAgent.getVel()

        agentVel = utils.normalize(agentVel)
        agentVel *= consts.MAX_SEE_AHEAD
        ahead = agentPos + agentVel
        curAgent.setAhead(ahead)




    #                                                                #
    # ---------------- Modify the following methods ---------------- #
    #                                                                #



    #
    # Flee rule similar to avoidance rule but not dependent upon
    # distance to predator.  Flee as fast as you can. This method should return
    # the difference between the agent's current direction and the desired direction.
    # The steering force (i.e., the value that this method will return) should be the
    # difference between the desired direction and the current agent's velocity. The desired
    # direction is found as the average of all differences of the current agent's position and the
    # predator's position normalized.
    #
    def adjustAccForFleeing(self, curAgent, predatorAgents):
        newForce = np.array([0, 0])
        desiredDir = np.array([0,0])
        posDiff = np.array([0,0])
        predatorsInSim = 0
        avg = np.array([0,0])
        curAgentPos = curAgent.getPos()
        for pred in predatorAgents:
            #what would happen if the predator was in the range for the bird to see it?
            predPos =   pred.getPos()
            posDiff[0] += (curAgentPos[0] - predPos[0])
            posDiff[1] += (curAgentPos[1] - predPos[1])
            predatorsInSim += 1
        if predatorsInSim > 0:
            #avg[0] = posDiff[0]/predatorsInSim
            #avg[1] = posDiff[1]/predatorsInSim
        #if avg[0] != 0 and avg[1] != 0:
            desiredDir = posDiff
            newForce = utils.normalize(desiredDir * consts.DESIRED_SPEED) - utils.normalize(curAgent.getVel())
            newForce = utils.normalize(newForce)
        return(newForce)

    #
    # If a nearest neighbor's distance is withing MIN_AVOID_DIST, calculate the current agent's
    # position vector minus the nearest neighbor's position e
    #
    def adjustAccForNeighborAvoidance(self, curAgent, preyAgents):
        newForce = np.array([0, 0])
        posDiff = np.array([0,0])
        desiredDir = np.array([0,0])
        preyPos = np.array([0,0])
        curAgentPos = curAgent.getPos()
        neighbor = 0
        for prey in preyAgents:
            if prey == curAgent:
                continue
            preyPos = prey.getPos()
            dist = utils.distance(curAgentPos,preyPos)
            if dist <= consts.MAX_SEE_AHEAD and dist >= 0:
                posDiff[0] += (curAgentPos[0] - preyPos[0]) 
                posDiff[1] += (curAgentPos[1] - curAgentPos[1])
                neighbor += 1
        if neighbor > 0:
            desiredDir = utils.normalize(posDiff)
            newForce = desiredDir * consts.DESIRED_SPEED - utils.normalize(curAgent.getVel())
            newForce = self.limitSpeed(newForce)
        return(newForce)

    #
    # Find the average position from the current agent's nearest neighbors. This method should
    # return the difference from the current agent's position and its neighbors' average position.
    #
    def adjustAccForNeighborPosition(self, curAgent, preyAgents):
        #Only to the neighbors, so apply the step from earlier
        newForce = np.array([0, 0])
        agentPos = curAgent.getPos()
        preyPos = np.array([0,0])
        desiredDir = np.array([0,0])
        neighbor = np.array([0,0])
        preyLength = 0
        avg = np.array([0,0])
        for prey in preyAgents:
            if prey == curAgent:
                continue
            preyPos = prey.getPos()
            dist = utils.distance(agentPos, preyPos)
            if dist <= consts.MAX_SEE_AHEAD and dist >= 0:
                neighbor[0] += preyPos[0]
                neighbor[1] += preyPos[1]
                preyLength += 1
        if preyLength > 0:
            desiredDir = utils.average(neighbor, preyLength)
            desiredDir = utils.normalize(avg)
            desiredDir = desiredDir - curAgent.getPos()
            newForce = utils.normalize(desiredDir)
        return(newForce)

    #
    # Calculate the difference in velocity from the current agent with that
    # of the average velocty of neighboring agents. The difference will be what
    # should be returned from this method.
    #
    def adjustAccForNeighborVelocity(self, curAgent, preyAgents):
        newForce = np.array([0, 0])
        curVel = curAgent.getVel()
        desiredVel = np.array([0,0])
        neighbors = 0
        for prey in preyAgents:
           neighborVel = prey.getVel()
           if prey == curAgent:
                continue
           if utils.distance(curVel, neighborVel) <= consts.MAX_SEE_AHEAD:
                desiredVel[0] += neighborVel[0]
                desiredVel[1] += neighborVel[1]
                neighbors += 1
        if neighbors > 0:
            desiredVel = utils.average(desiredVel, neighbors)
            newForce[0] = desiredVel[0] - curVel[0]
            newForce[1] = desiredVel[1] - curVel[1]
            newForce = utils.normalize(newForce)
        return(newForce)

    #
    # This method checks all of the obstacles to see if any intersect the
    # current path of the current agent using the "ahead" vector. The "ahead"
    # vector is just the sum of the current agent's position vector and the
    # current agent's velocity vector. To see how to calculate this collision,
    # read the comment on the lineIntersectsCircle() method. Once you find an
    # obstacle that will be collided with, this method should return the difference
    # of the most threatening obstacle's force and the current agent's velocity vector.
    # The former is the vector equal to the difference of the most threatening obstacle
    # and the ahead vector.
    #
    def adjustAccForObstacleAvoidance(self, curAgent, obstacles):
        newForce = np.array([0, 0])
        ahead = curAgent.getAhead()
        start = curAgent.getPos()
        end = ahead
        desiredDir = np.array([0,0])
        aheadHalf = (end + start)/2
        if not obstacles:
            return newForce
        for obstacle in obstacles:
            dist = utils.distance(obstacle.getPos(), curAgent.getPos())
            radius = obstacle.getRadius() * consts.RADIUS_EXPAND
            if dist <= radius:
                return utils.normalize(curAgent.getPos() - obstacle.getPos())* consts.MAX_AVOID_FORCE
            
            if self.lineIntersectsCircle(start, ahead, aheadHalf, obstacle):
                desiredDir = utils.normalize(curAgent.getPos() - obstacle.getPos()) * consts.DESIRED_SPEED
                newForce = curAgent.getVel() - desiredDir
                newForce = utils.normalize(newForce)              
        return(newForce)
