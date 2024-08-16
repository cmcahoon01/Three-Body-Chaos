from math import pi

max_x = 1000
max_y = 1000
mass_range = 3, 10
max_v = 1

max_steps = 1000

parameter_domains = {
    "a x": (0, max_x),
    "a y": (0, max_x),
    "b x": (0, max_x),
    "b y": (0, max_x),
    "a theta": (0, 2 * pi),
    "b theta": (0, 2 * pi),
    "a v": (0, max_v),
    "b v": (0, max_v),
    "a mass": mass_range,
    "b mass": mass_range,
    "c distance": (0, max_x / 2),
}

gravitational_constant = 10
