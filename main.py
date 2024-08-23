from color import write_color
from hittable import HitRecord
from hittable_list import HittableList
from sphere import Sphere
from rtweekend import *
from camera import *
from material import *

# TODO:
# [] BUG: updating . attributes for cam class doesn't work

FILE = "test.ppm"

def main():
    world = HittableList()

    material_ground = Lambertian(Vector(0.8, 0.8, 0.0))
    material_center = Lambertian(Vector(0.1, 0.2, 0.5))
    material_left = Dielectric(1.50) #Metal(Vector(0.8, 0.8, 0.8), 0.3)
    material_bubble = Dielectric(2.42)
    material_right = Metal(Vector(0.8, 0.6, 0.2), 1.0)

    world.add(Sphere(Vector(0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Vector(0.0, 0.0, -1.2), 0.5, material_center))
    world.add(Sphere(Vector(-1.0, 0.0, -1.0), 0.5, material_left))
    world.add(Sphere(Vector(-1.0, 0.0, -1.0), 0.4, material_bubble))
    world.add(Sphere(Vector(1.0, 0.0, -1.0), 0.5, material_right))

    # world.add(Sphere(Vector(0, 0, -1), 0.5))
    # world.add(Sphere(Vector(0, -100.5, -1), 100))

    cam = Camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_px = 100
    cam.max_depth = 50

    cam.vfov = 20
    cam.look_from = Vector(-2, 2, 1)
    cam.look_at = Vector(0,0, -1)
    cam.vup = Vector(0, 1, 0)

    cam.render(world, FILE)

main()