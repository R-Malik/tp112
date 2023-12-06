### MODULES ####################################################################
import math
################################################################################

'''
Vector class contains helper methods related to vector operations needed
to determine the shortest distance between a line segment (a piece of the
scribble) and a point (the center of the circular-modelled player).
'''

class Vector():
    # returns a vector (x, y) from two points p, q in R2
    def fromPoints(p, q):
        x0, y0 = p
        x1, y1 = q
        return (x1-x0, y1-y0)

    # returns sum of two vectors in R2
    def add(u, v):
        x0, y0 = u
        x1, y1 = v
        return (x0+x1, y0+y1)

    # returns a linearly scaled vector in R2 by given constant
    def scale(v, k):
        x0, y0 = v
        return (x0*k, y0*k)

    # returns dot product of two vectors in R2
    def dot(u, v):
        x0, y0 = u
        x1, y1 = v
        return x0*x1 + y0*y1

    # returns a unit vector from a vector in R2
    def unitize(v):
        x0, y0 = v
        norm = Vector.magnitude(v)
        # check for divide by zero error
        if norm != 0:
            return (x0/norm, y0/norm)
        else:
            return (x0, y0)

    # returns norm or magnitude of vector in R2
    def magnitude(v):
        x0, y0 = v
        return math.sqrt(x0**2 + y0**2)

    # returns distance between two points in R2
    def distance(p, q):
        # create a vector first, then use magnitude method
        v = Vector.fromPoints(p, q)
        return Vector.magnitude(v)

'''
distanceFromPointToSegment function takes a point (player center), start point
of a line segment, AND end point of a line segment. It outputs a tuple of the
shortest distance between the player center AND the line segment and the point
on the line segment that is closest.
'''

def distanceFromPointToSegment(point, start, end):
    # creates vector for line segment
    segmentVector = Vector.fromPoints(start, end)
    # creates point vector from start of line segment to player
    pointVector = Vector.fromPoints(start, point)
    segmentMagnitude = Vector.magnitude(segmentVector)
    if segmentMagnitude == 0:
        segmentMagnitude = 1 # checks for divide by zero error later
    segmentUnitVector = Vector.unitize(segmentVector)

    # scale player point vector by the length of the segment
    pointVectorScaled = Vector.scale(pointVector, 1.0/segmentMagnitude)
    # gets dot product of segment unit vector and adjusted point vector
    scaleFactor = Vector.dot(segmentUnitVector, pointVectorScaled)

    # checks that the dot product is in range from parallel to perpendicular
    if scaleFactor < 0.0:
        scaleFactor = 0.0
    elif scaleFactor > 1.0:
        scaleFactor = 1.0

    # distance from closest point to point vector is the shortest distance
    closestPoint = Vector.scale(segmentVector, scaleFactor)
    dist = Vector.distance(closestPoint, pointVector)
    # add to start vector to get closest point along segment
    closestPoint = Vector.add(closestPoint, start)

    return (dist, closestPoint) # return is tuple