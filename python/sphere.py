import math
from hittable import Hittable
from vector import Vector
from hittable import HitRecord
from material import Material


class Sphere(Hittable):
    def __init__(self, center, radius, mat):
        self.center = center
        self.radius = max(0, radius)
        self.material = mat

    def hit(self, r, ray_t, rec):
        oc = self.center - r.origin
        a = r.direction.length_squared()
        h = Vector.dot(r.direction, oc)
        c = oc.length_squared() - self.radius * self.radius

        discriminant = h * h - a * c
        if discriminant < 0:
            return False

        sqrtd = math.sqrt(discriminant)

        # find nearest root in acceptable range
        root = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.material

        return True