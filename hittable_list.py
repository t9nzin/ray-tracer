from hittable import Hittable
from hittable import HitRecord
from interval import Interval

class HittableList(Hittable):
    def __init__(self, object = None):
        self.objects = []
        if object:
            self.add(object)

    def clear(self):
        self.objects.clear()

    def add(self, object):
        self.objects.append(object)

    def hit(self, r, ray_t, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = ray_t.max

        for object in self.objects:
            if object.hit(r, Interval(ray_t.min, closest_so_far), temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.copy(temp_rec)

        return hit_anything


