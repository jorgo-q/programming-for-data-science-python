""" 
Drawing a circle
"""

import math
import comp614_module1 as circles


def distance(point0x, point0y, point1x, point1y):
    """
    Given the x- and y-coordinates of two points, computes and returns the 
    distance between them.
    """
    # Breaking it down to dist_x and dist_y for readability
    # This will help to make the distance formula easier to express
    dist_x = point0x - point1x 
    dist_y = point0y - point1y 
    dist = math.sqrt(dist_x**2 + dist_y**2) 
    return dist 


def midpoint(point0x, point0y, point1x, point1y):
    """
    Given the x- and y-coordinates of two points, computes and returns the
    midpoint of the line segment between them.
    """
    # Here I simplified the math formula -> (2x0 + x1 - x0) / 2 -> (x0 + x1) / 2
    x_m = (point0x + point1x)/2 
    y_m = (point0y + point1y)/2 
    return x_m, y_m 


def slope(point0x, point0y, point1x, point1y):
    """
    Given the x- and y-coordinates of two points, computes and returns the
    slope of the line segment from (point0x, point0y) to (point1x, point1y).
    """
    slope1 = (point1y - point0y) / (point1x - point0x) 
    return slope1


def perp(lineslope):
    """
    Given the slope of a line, computes and returns the slope of a line 
    perpendicular to the input slope.
    """
    return -1 / lineslope 


def intersect(slope0, point0x, point0y, slope1, point1x, point1y):
    """
    Given two lines, where each is represented by its slope and a point
    that it passes through, computes and returns the intersection point
    of the two lines. 
    """
    # Finding the x and y coordinate of the intersection point of two lines
    # Does not handle edge cases (parallel lines) as instructed in the HW
    x_i = ((slope0 * point0x) - (slope1 * point1x) + (point1y - point0y)) / (slope0 - slope1)
    y_i = slope0 * (x_i - point0x) + point0y
    return x_i, y_i


def make_circle(point0x, point0y, point1x, point1y, point2x, point2y):
    """
    Given the x- and y-coordinates of three points, computes and returns
    three real numbers: the x- and y-coordinates of the center of the circle
    that passes through all three input points, and the radius of that circle.
    """
    
    # Step 1-3: Calculates the midpoints and their perpendicular bisectors
    midpoint1 = midpoint(point0x, point0y, point1x, point1y)
    slope1 = slope(point0x, point0y, point1x, point1y)
    perp1 = perp(slope1)
    
    midpoint2 = midpoint(point1x, point1y, point2x, point2y)
    slope2 = slope(point1x, point1y, point2x, point2y)
    perp2 = perp(slope2)
    
    # Step 4: Finds the circle_center as the intercect of the two perp bisectors  
    circle_center = intersect(perp1, midpoint1[0], midpoint1[1], 
                              perp2, midpoint2[0], midpoint2[1])
    

    # Step 5: Calculates the distance from the center of the circle to point 0
    # All points (0, 1, or 2) can be used here since they're all in the circle 
    radius = distance(circle_center[0], circle_center[1], point0x, point0y) 
    
    # Returns the circle's center (x, y) and the radius
    return circle_center[0], circle_center[1], radius 

circles.start(make_circle)
