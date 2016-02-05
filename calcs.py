
# helper program for calculating coordinates of boulders on the field


def inches_in_feet(inches):
    return inches / 12


def pair(point):
    return "[{0:.3f}, {1:.3f}]".format(point[0], point[1])

ballSize = inches_in_feet(10.0)
midLineX = 27
defaultEdge = ballSize / 3

boulderSeparation = inches_in_feet(45.5)
barrierSeparation = inches_in_feet(50)


# make a boulder centered at x,y
def make_boulder(x, y, boulderEdge=defaultEdge):
    b = []
    # leftmost top point
    x1 = x - boulderEdge / 2
    y1 = y
    b.append([x1, y1])
    # rightmost top point
    x2 = x1 + boulderEdge
    y2 = y1
    b.append([x2, y2])
    # topmost right point
    x3 = x2 + boulderEdge
    y3 = y2 + boulderEdge
    b.append([x3, y3])
    # bottommost right point
    x4 = x3
    y4 = y3 + boulderEdge
    b.append([x4, y4])
    # rightmost bottom point
    x5 = x4 - boulderEdge
    y5 = y4 + boulderEdge
    b.append([x5, y5])
    # leftmost bottom point
    x6 = x5 - boulderEdge
    y6 = y5
    b.append([x6, y6])
    # bottommost left point
    x7 = x6 - boulderEdge
    y7 = y6 - boulderEdge
    b.append([x7, y7])
    # topmost left point
    x8 = x7
    y8 = y7 - boulderEdge
    b.append([x8, y8])
    return b


def print_boulder(n, b):
    print(',{')
    print('"color": "purple",')
    print("\"label\": \"boulder %d\"," % n)
    print('"points": [' + pair(b[0]), pair(b[1]), pair(b[2]), pair(b[3]), pair(b[4]), pair(b[5]), pair(b[6]), pair(b[7]) + "]", sep=', ')
    print('}')


print_boulder(1, make_boulder(midLineX, boulderSeparation))
print_boulder(2, make_boulder(midLineX, boulderSeparation * 2))
print_boulder(3, make_boulder(midLineX, boulderSeparation * 3))
print_boulder(4, make_boulder(midLineX, boulderSeparation * 4))
print_boulder(5, make_boulder(midLineX, boulderSeparation * 5))
print_boulder(6, make_boulder(midLineX, boulderSeparation * 6))


# make a barrier with top left corner at x,y and thickness of thick
def print_barrier(x, y, thick):
    length = 4
    print(',{')
    print('"color": "black",')
    print("\"label\": \"defense divider\",")
    print('"points": [' + pair([x, y]), pair([x + length, y]), pair([x + length, y + thick]), pair([x, y + thick]) + ']', sep=', ')
    print('}')

defenseSeparation = inches_in_feet(52.5)
print_barrier(15.95, 4.458, 0.1)
print_barrier(15.95, 4.458 + defenseSeparation, 0.1)
print_barrier(15.95, 4.458 + defenseSeparation * 2, 0.1)
print_barrier(15.95, 4.458 + defenseSeparation * 3, 0.1)
print_barrier(15.95, 4.458 + defenseSeparation * 4, 0.1)
print_barrier(15.95, 4.458 + defenseSeparation * 5, 0.1)