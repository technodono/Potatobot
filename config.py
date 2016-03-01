import json

# helper program for calculating coordinates of boulders on the field
# TODO make this print the whole config.json file


def inches_in_feet(inches):
    return inches / 12

ballSize = inches_in_feet(10.0)
midLineX = 27
defaultEdge = ballSize / 3

boulderSeparation = inches_in_feet(45.5)
barrierSeparation = inches_in_feet(50)
defense_sep = inches_in_feet(52.5)


# make a boulder centered at x,y, returns array(8) of points which are arrays(2)
def make_boulder(x, y, edge=defaultEdge):
    b = []
    # will be an irregular "octagon", vertices at 1/3 and 2/3 on each side of a square
    # leftmost top point
    x1 = x - edge / 2
    y1 = y - edge * 2 / 3
    b.append([x1, y1])
    # rightmost top point
    x2 = x1 + edge
    y2 = y1
    b.append([x2, y2])
    # topmost right point
    x3 = x2 + edge
    y3 = y1 + edge
    b.append([x3, y3])
    # bottommost right point
    x4 = x3
    y4 = y3 + edge
    b.append([x4, y4])
    # rightmost bottom point
    x5 = x2
    y5 = y4 + edge
    b.append([x5, y5])
    # leftmost bottom point
    x6 = x1
    y6 = y5
    b.append([x6, y6])
    # bottommost left point
    x7 = x1 - edge
    y7 = y4
    b.append([x7, y7])
    # topmost left point
    x8 = x7
    y8 = y3
    b.append([x8, y8])

    return {
        'color': "thistle3",
        'label': format("boulder at %d,%d" % (x, y)),
        'points': b
    }

# make an array of point tuples in draw-order for a rectangle origin x,y width w height h
def rect(x, y, w, h):
    return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]


def make_barrier(x, y, length=4, thick=inches_in_feet(1)):
    return {
        'color': "black",
        'label': "defense divider",
        'points': rect(x, y, length, thick)
    }


config = {
    'pyfrc': {
        'robot': {
            "w": 2.4,
            "h": 2,
            "starting_x": 25,
            "starting_y": 20,
            "starting_angle": 0
        },
        "field": {
            "w": 54,
            "h": 27,
            "px_per_ft": 12,
            "objects": [
                {
                    "color": "thistle3",
                    "label": "blue alliance defenses",
                    "points": [[19.95, 4.458], [15.95, 4.458], [15.95, 26.643], [19.95, 26.643]]
                },
                {
                    "color": "light slate gray",
                    "label": "platform",
                    "points": [[16.95, 4.458], [18.95, 4.458], [18.95, 26.643], [16.95, 26.643]]
                },
                {
                    "color": "thistle3",
                    "label": "red alliance defenses",
                    "points": [[34.05, 0], [38.08, 0], [38.08, 22.643], [34.05, 22.643]]
                },
                {
                    "color": "light slate gray",
                    "label": "platform",
                    "points": [[35.05, 0], [37.08, 0], [37.08, 22.643], [35.05, 22.643]]
                },
                {
                    "color": "red",
                    "label": "red alliance secret passage",
                    "points": [[30, 27], [30, 23], [54, 23], [54, 27]]
                },

                {
                    "color": "blue",
                    "label": "blue alliance secret passage",
                    "points": [[0, 4], [0, 0], [24, 0], [24, 4]]
                },
                {
                    "color": "black",
                    "label": "centre line",
                    "points": [[27, 0], [27.1, 0], [27.1, 27], [27, 27]]
                }
            ]
        }
    }
}

objects = config['pyfrc']['field']['objects']

for i in range(6):
    boulder = make_boulder(midLineX, boulderSeparation * (i + 1))
    objects.append(boulder)

for i in range(6):
    barrier = make_barrier(15.95, 4.458 + i * defense_sep)
    objects.append(barrier)

for i in range(6):
    barrier = make_barrier(34.05, 0 + i * defense_sep)
    objects.append(barrier)

with open('sim/config.json', 'w') as f:
    json.dump(config, f, indent=2, sort_keys=True)

