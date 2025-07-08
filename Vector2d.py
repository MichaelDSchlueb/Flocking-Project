
import math

class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, vec):
        diffx = self.x - vec.getX()
        diffy = self.y - vec.getY()
        return(math.sqrt(diffx*diffx + diffy*diffy))

    def dot(self, vec):
        return (self.x*vec.getX() + self.y*vec.getY())

    def getX(self):
        return(self.x)

    def getY(self):
        return(self.y)

    def isZero(self):
        return((self.x == 0) and (self.y == 0))

    def length(self):
        xcoord = self.x
        ycoord = self.y
        return(math.sqrt(xcoord*xcoord+ycoord*ycoord))

    def normalize(self):
        len = self.length()
        self.setX(self.x/len)
        self.setY(self.y/len)

    def print(self, msg):
        print(msg, ": (", self.x, ",", self.y, ")")

    def rotate(self, thetaDeg):
        thetaRad = math.radians(thetaDeg)
        costh = math.cos(thetaRad)
        sinth = math.sin(thetaRad)
        newX = self.x*costh - self.y*sinth
        newY = self.x*sinth + self.y*costh
        self.setX(newX)
        self.setY(newY)

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def __add__(self, vec):
        return(Vector2d(self.x + vec.getX(), self.y + vec.getY()))

    def __iadd__(self, vec):
        self.x += vec.getX()
        self.y += vec.getY()
        return(self)

    def __imul__(self, factor):
        self.x *= factor
        self.y *= factor
        return(self)

    def __isub__(self, vec):
        self.x -= vec.getX()
        self.y -= vec.getY()
        return(self)
    def __itruediv__(self, den):
        self.x /= den
        self.y /= den
        return(self)

    def __mul__(self, factor):
        return(Vector2d(self.x * factor, self.y * factor))

    def __sub__(self, vec):
        return(Vector2d(self.x - vec.getX(), self.y - vec.getY()))
