import math
import sys
import random
from ray import Ray
from interval import Interval

infinity = float('inf')
pi = math.pi

# utility functions
def degrees_to_radians(degrees):
    return degrees * pi / 180.0

def random_double():
    return random.random()

def random_double_min_max(min, max):
    return min + (max - min) * random_double()