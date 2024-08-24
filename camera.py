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

"""
Display a progress bar in console
"""
def progress(completed, total):
    filled_length = int(round(20 * completed / float(total)))
    bar = '█' * filled_length + '.' * (20 - filled_length)
    sys.stdout.write(f'progress: \r[{bar}]')
    sys.stdout.flush()

"""
Constructs and dispatches rays into the world
Uses results of rays to construct rendered img
"""
class Camera:
    def __init__(self, aspect_ratio=1.0, image_width=100, samples_per_px=100, max_depth=50):
        self.aspect_ratio = aspect_ratio # width / height
        self.image_width = image_width # rendered img width in px
        self.samples_per_px = samples_per_px # count of random samples per px
        # samples_per_px = number of rays shot per pixel -- higher == higher quality pic
        self.max_depth = max_depth # max number of ray bounces into scene
        # point in 3D space from which all scene rays will originate
        self.center = Vector(0, 0, 0)

    def initialize(self):
        # calculate image height to keep aspect ratio
        self.image_height = int(self.image_width / self.aspect_ratio)
        # ensure image height is at least 1
        self.image_height = 1 if self.image_height < 1 else self.image_height
        self.pixel_samples_scale = 1.0 / self.samples_per_px

        self.center = Vector(0,0,0)

        # determine viewport dimensions
        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (self.image_width / self.image_height)

        # calculate the vectors across the horizontal and down the vertical viewport edges
        viewport_u = Vector(viewport_width, 0, 0)
        viewport_v = Vector(0, -viewport_height, 0)

        # calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # calculate location of the upper left pixel
        viewport_upper_left = self.center - Vector(0, 0,focal_length) - viewport_u / 2 - viewport_v / 2
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

    """
    Construct a camera ray originating from the origin and directed at
    randomly sampled point around the pixel location i, j
    """
    def get_ray(self, i , j):
        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x) * self.pixel_delta_u) + ((j + offset.y) * self.pixel_delta_v)

        ray_origin = self.center
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)

    """
    Returns the vector to a random point in the [-.5, -.5]-[+.5, +.5] unit square
    """
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
            return Vector(0,0,0)

        unit_direction = Vector.unit_vector(r.direction)
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * Vector(1.0, 1.0, 1.0) + a * Vector(0.5, 0.7, 1.0)
