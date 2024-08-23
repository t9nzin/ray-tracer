"""
Responsible for 2 jobs

1. Constructing and dispatching rays into the world
2. Using the results of these rays to construct the rendered image
"""

from rtweekend import *
from hittable import *
from color import *
from vector import *
from material import *

def progress(completed, total):
    filled_length = int(round(20 * completed / float(total)))
    bar = '█' * filled_length + '.' * (20 - filled_length)
    sys.stdout.write(f'progress: \r[{bar}]')
    sys.stdout.flush()

class Camera:
    def __init__(self, aspect_ratio=1.0, image_width=100, samples_per_px=10, max_depth=50, vfov=20, look_from=Vector(-2,2,1), look_at=Vector(0, 0, -1), vup=Vector(0, 1, 0)):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_px = samples_per_px
        self.max_depth = max_depth
        self.center = Vector(0, 0, 0)
        self.vfov = vfov
        self.look_from = look_from
        self.look_at = look_at
        self.vup = vup

    def initialize(self):
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = 1 if self.image_height < 1 else self.image_height
        self.pixel_samples_scale = 1.0 / self.samples_per_px

        self.center = self.look_from

        # determine viewport dimensions
        focal_length = (self.look_from - self.look_at).length()
        theta = degrees_to_radians(self.vfov)
        h = math.tan(theta/2)
        viewport_height = 2 * h * focal_length
        viewport_width = viewport_height * (self.image_width / self.image_height)

        # calculate u, v, w unit basis vectors
        w = Vector.unit_vector(self.look_from - self.look_at)
        u = Vector.unit_vector(Vector.cross(self.vup, w))
        v = Vector.cross(w,u)

        # calculate the vectors across the horizontal and down the vertical viewport edges
        viewport_u = viewport_width * u #Vector(viewport_width, 0, 0)
        viewport_v = viewport_height * -v #Vector(0, -viewport_height, 0)

        # calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # calculate location of the upper left pixel
        #viewport_upper_left = self.center - Vector(0, 0,focal_length) - viewport_u / 2 - viewport_v / 2
        viewport_upper_left = self.center - (focal_length * w) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + 0.5 * (
                    self.pixel_delta_u + self.pixel_delta_v)

    def render(self, world, file):
        self.initialize()

        with open(file, "w") as f:
            f.write(f"P3\n{self.image_width} {self.image_height}\n255\n")

            for j in range(self.image_height):
                progress(j, self.image_height)
                for i in range(self.image_width):
                    pixel_color = Vector(0,0,0)
                    for sample in range(self.samples_per_px):
                        r = self.get_ray(i, j)
                        pixel_color += self.ray_color(r, self.max_depth, world)

                    write_color(f, self.pixel_samples_scale * pixel_color)

    def get_ray(self, i , j):
        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x) * self.pixel_delta_u) + ((j + offset.y) * self.pixel_delta_v)

        ray_origin = self.center
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)

    def sample_square(self):
        return Vector(random_double() - 0.5, random_double() - 0.5, 0)

    def ray_color(self, r, depth, world):
        if depth <= 0:
            return Vector(0, 0, 0)

        # rec.mat is None
        rec = HitRecord() # created an hit record object

        if world.hit(r, Interval(0.001, infinity), rec):
            scattered = Ray(None, None)
            attenuation = Vector(0,0,0)
            if rec.mat.scatter(r, rec, attenuation, scattered):
                return attenuation * self.ray_color(scattered, depth - 1, world)
            # direction = rec.normal + Vector.random_unit_vector()
            # return 0.5 * self.ray_color(Ray(rec.p, direction), depth - 1, world)
            return Vector(0,0,0)

        unit_direction = Vector.unit_vector(r.direction)
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * Vector(1.0, 1.0, 1.0) + a * Vector(0.5, 0.7, 1.0)
