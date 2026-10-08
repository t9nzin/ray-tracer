#include <memory>

#include "bvh.h"
#include "camera.h"
#include "hittable_list.h"
#include "material.h"
#include "sphere.h"

const char* FILE_NAME = "test.ppm";

int main() {
    HittableList world;

    auto material_ground = std::make_shared<Lambertian>(Vector(0.8, 0.8, 0.0));
    auto material_center = std::make_shared<Lambertian>(Vector(0.1, 0.2, 0.5));
    auto material_left   = std::make_shared<Dielectric>(1.50);
    auto material_bubble = std::make_shared<Dielectric>(2.42);
    auto material_right  = std::make_shared<Metal>(Vector(0.8, 0.6, 0.2), 1.0);

    world.add(std::make_shared<Sphere>(Vector( 0.0, -100.5, -1.0), 100.0, material_ground));
    world.add(std::make_shared<Sphere>(Vector( 0.0,    0.0, -1.2),   0.5, material_center));
    world.add(std::make_shared<Sphere>(Vector(-1.0,    0.0, -1.0),   0.5, material_left));
    world.add(std::make_shared<Sphere>(Vector(-1.0,    0.0, -1.0),   0.4, material_bubble));
    world.add(std::make_shared<Sphere>(Vector( 1.0,    0.0, -1.0),   0.5, material_right));

    world = HittableList(std::make_shared<BvhNode>(world));

    Camera cam;
    cam.aspect_ratio   = 16.0 / 9.0;
    cam.image_width    = 400;
    cam.samples_per_px = 100;
    cam.max_depth      = 50;

    cam.render(world, FILE_NAME);
}
