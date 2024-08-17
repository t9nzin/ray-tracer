import sys
import math
# PART 2

def progress(completed, total):
    filled_length = int(round(20 * completed / float(total)))
    bar = '█' * filled_length + '.' * (20 - filled_length)
    sys.stdout.write(f'progress: \r[{bar}]')
    sys.stdout.flush()

# PPM Image Format
class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render(self, file):
        with open(file, "w") as f:
            f.write(f"P3\n{self.width} {self.height}\n255\n")

            # render
            for j in range(self.height):
                progress(j, self.height)
                for i in range(self.width):
                    # pixel_color = Vector(i/(self.width-1), j/(self.height-1), 0)
                    pixel_center = pixel100_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
                    ray_direction = pixel_center - camera_center
                    r = Ray(camera_center, ray_direction)
                    pixel_color = ray_color(r)
                    write_color(f, pixel_color)


# PART 3

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

# color utility functions
def write_color(file, pixel_color):
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    rbyte = int(255.999 * r)
    gbyte = int(255.999 * g)
    bbyte = int(255.999 * b)

    file.write(f"{rbyte} {gbyte} {bbyte}\n")


# PART 4

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def at(self, t):
        return self.origin + t*self.direction

aspect_ratio = 16.0 / 9.0
image_width = 400

image_height = int(image_width / aspect_ratio)
image_height = 1 if image_height < 1 else image_height

focal_length = 1.0
viewport_height = 2.0
viewport_width = viewport_height * (image_width / image_height)
camera_center = Vector(0,0,0)

viewport_u = Vector(viewport_width, 0, 0)
viewport_v = Vector(0, -viewport_height, 0)

pixel_delta_u = viewport_u / image_width
pixel_delta_v = viewport_v / image_height

viewport_upper_left = camera_center - Vector(0, 0, focal_length) - viewport_u/2 - viewport_v/2
pixel100_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

# code that implements the camera
def ray_color(r):
    t = hit_sphere(Vector(0, 0, -1), 0.5, r)
    if t > 0.0:
        N = Vector.unit_vector(r.at(t) - Vector(0, 0, -1))
        return 0.5*Vector(N.x+1, N.y+1, N.z+1)

    unit_direction = Vector.unit_vector(r.direction)
    a = 0.5 * (unit_direction.y + 1.0)
    return (1.0 - a) * Vector(1.0, 1.0, 1.0) + a * Vector(0.5, 0.7, 1.0)

# PART 5

def hit_sphere(center, radius, r):
    oc = center - r.origin
    # a = Vector.dot(r.direction, r.direction)
    # b = -2.0 * Vector.dot(r.direction, oc)
    # c = Vector.dot(oc, oc) - radius * radius
    # discriminant = b*b - 4 * a * c
    a = r.direction().length_squared()
    h = Vector.dot(r.direction(), oc)
    c = oc.length_squared() - radius * radius
    discriminant = h * h - a * c

    if (discriminant < 0):
        return -1.0
    else:
        return (h - math.sqrt(discriminant)) / a


img = Image(image_width, image_height)
img.render("sky.ppm")

# PART 6

class HitRecord:
    def __init__(self, p, normal, t):
        self.p = p
        self.normal = normal
        self.t = t

class Hittable:
    def __init__(self):
        pass

    def hit(self, r, ray_tmin, ray_tmax, rec):
        pass

class Sphere(Hittable):
    def __init__(self, center, radius):
        self.center = center
        self.radius = max(0, radius)

    def hit(self, r, ray_tmin, ray_tmax, rec):
        oc = self.center - r.origin
        a = r.direction.length_squared
        h = Vector.dot(r.direction, oc)
        c = oc.length_squared - self.radius * self.radius

        discriminant = h * h - a * c
        if discriminant < 0:
            return False

        sqrtd = math.sqrt(discriminant)

        # find nearest root in acceptable range
        root = (h - sqrtd) / a
        if (root <= ray_tmin) or (ray_tmax <= root):
            return False

        rec.t = root
        rec.p = r.at(rec.t)
        rec.normal = (rec.p - self.center) / self.radius
        return True

def front_face():
    if