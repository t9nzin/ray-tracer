from rtweekend import *
from vector import Vector

class Material:
    def __init__(self):
        pass

    def scatter(self, r_in, rec, attenuation, scattered):
        return False

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec, attenuation, scattered):
        scatter_direction = rec.normal + Vector.random_unit_vector()

        # catch degenerate scatter direction
        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered.origin = rec.p
        scattered.direction = scatter_direction
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return True

class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, r_in, rec, attenuation, scattered):
        reflected = Vector.reflect(r_in.direction, rec.normal)
        reflected = Vector.unit_vector(reflected) + (self.fuzz * Vector.random_unit_vector())
        scattered.origin = rec.p
        scattered.direction = reflected
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return Vector.dot(scattered.direction, rec.normal) > 0

class Dielectric(Material):
    def __init__(self, refraction_index):
        self.refraction_index = refraction_index

    def scatter(self, r_in, rec, attenuation, scattered):
        attenuation.x = 1.0
        attenuation.y = 1.0
        attenuation.z = 1.0

        ri = (1.0 / self.refraction_index) if rec.front_face else self.refraction_index

        unit_direction = Vector.unit_vector(r_in.direction)
        # refracted = Vector.refract(unit_direction, rec.normal, ri)
        cos_theta = min(Vector.dot(-unit_direction, rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = ri * sin_theta > 1.0
        if cannot_refract or (self.reflectance(cos_theta, ri) > random_double()):
            direction = Vector.reflect(unit_direction, rec.normal)
        else:
            direction = Vector.refract(unit_direction, rec.normal, ri)

        scattered.origin = rec.p
        scattered.direction = direction

        return True

    @staticmethod
    def reflectance(cosine, refraction_index):
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1 - r0) * math.pow((1-cosine), 5)