from ray import Ray
from vector import Vector
from material import Material

class HitRecord:
    def __init__(self):
        self.p = Vector(0,0,0)
        self.normal = Vector(0,0,0)
        self.t = 0.0
        self.mat = None
        self.front_face = False

    def set_face_normal(self, r, outward_normal):
        # set the hit record normal vector
        self.front_face = Vector.dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

    def copy(self, other):
        self.p = Vector(other.p.x, other.p.y, other.p.z)
        self.normal = Vector(other.normal.x, other.normal.y, other.normal.z)
        self.t = other.t
        self.front_face = other.front_face
        self.mat = other.mat

class Hittable:
    def __init__(self):
        pass

    def hit(self, r, ray_t, rec):
        pass




