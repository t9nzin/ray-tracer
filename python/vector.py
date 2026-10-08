import math
from rtweekend import *
import numpy

# 3 coordinates
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.components = [x, y, z]

    def __str__(self):
        return f'{self.x} {self.y} {self.z}'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __imul__(self, s):
        self.x *= s
        self.y *= s
        self.z *= s
        return self

    def __floordiv__(self, s):
        return Vector(self.x // s, self.y // s, self.z // s)

    def __ifloordiv__(self, s):
        self.x //= s
        self.y //= s
        self.z //= s
        return self

    def __truediv__(self, s):
        return Vector(self.x / s, self.y / s, self.z / s)

    def __itruediv__(self, s):
        self.x /= s
        self.y /= s
        self.z /= s
        return self

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __getitem__(self, i):
        return self.components[i]

    def __setitem__(self, i, value):
        self.components[i] = value

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def length_squared(self):
        return self.x**2 + self.y**2 + self.z**2

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def unit_vector(self):
        return self / self.length()

    def copy(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z
        self.components = other.components.copy()

    def random(self):
        return Vector(random_double(), random_double(), random_double())

    # general utility method
    @staticmethod # static methods belong to a class, not an instance, we dont require an instance to call it
    def random_min_max(min, max):
        return Vector(random_double_min_max(min, max), random_double_min_max(min, max), random_double_min_max(min, max))

    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = Vector.random_min_max(-1, 1)
            if p.length_squared() < 1:
                return p

    @staticmethod
    def random_unit_vector():
        return Vector.random_in_unit_sphere().unit_vector()

    @staticmethod
    def random_on_hemisphere(normal):
        on_unit_sphere = Vector.random_unit_vector()
        if Vector.dot(on_unit_sphere, normal) > 0.0:
            return on_unit_sphere
        else:
            return -on_unit_sphere

    @staticmethod
    def reflect(v, n):
        return v - 2 * Vector.dot(v, n) * n

    def near_zero(self):
        s = 1e-8
        return abs(self.x < s) and abs(self.y < s) and abs(self.z < s)

    @staticmethod
    def refract(uv, n, etai_over_etat):
        cos_theta = min(Vector.dot(-uv, n), 1.0)
        r_out_perp = etai_over_etat * (uv + cos_theta*n)
        r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
        return r_out_perp + r_out_parallel