/*
 * Responsible for 2 jobs
 *
 * 1. Constructing and dispatching rays into the world
 * 2. Using the results of these rays to construct the rendered image
 */
#ifndef CAMERA_H
#define CAMERA_H

#include <algorithm>
#include <atomic>
#include <fstream>
#include <iostream>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

#include "color.h"
#include "hittable.h"
#include "material.h"
#include "rtweekend.h"
#include "vector.h"

// Display a progress bar in console
inline void progress(int completed, int total) {
    int filled_length = int(std::round(20.0 * completed / total));
    std::string bar;
    for (int i = 0; i < 20; i++)
        bar += i < filled_length ? "█" : ".";
    std::clog << "\rprogress: [" << bar << "]" << std::flush;
}

/*
 * Constructs and dispatches rays into the world
 * Uses results of rays to construct rendered img
 */
class Camera {
  public:
    double aspect_ratio = 1.0; // width / height
    int image_width = 100;     // rendered img width in px
    int samples_per_px = 100;  // count of random samples per px -- higher == higher quality pic
    int max_depth = 50;        // max number of ray bounces into scene
    int num_threads = 0;       // render threads; 0 == use all hardware threads

    void render(const Hittable& world, const std::string& file) {
        initialize();

        // rendered pixels, 3 bytes (r, g, b) each, row-major from the top left
        std::vector<unsigned char> pixels(size_t(image_width) * image_height * 3);

        // threads repeatedly claim the next unrendered row until none are left
        std::atomic<int> next_row{0};
        std::atomic<int> rows_done{0};
        std::mutex progress_mutex;

        auto worker = [&]() {
            for (int j = next_row++; j < image_height; j = next_row++) {
                for (int i = 0; i < image_width; i++) {
                    Vector pixel_color(0, 0, 0);
                    for (int sample = 0; sample < samples_per_px; sample++) {
                        Ray r = get_ray(i, j);
                        pixel_color += ray_color(r, max_depth, world);
                    }
                    write_color(&pixels[(size_t(j) * image_width + i) * 3], pixel_samples_scale * pixel_color);
                }

                int done = ++rows_done;
                std::lock_guard<std::mutex> lock(progress_mutex);
                progress(done, image_height);
            }
        };

        int n = num_threads > 0 ? num_threads : int(std::max(1u, std::thread::hardware_concurrency()));
        std::vector<std::thread> threads;
        for (int t = 0; t < n; t++)
            threads.emplace_back(worker);
        for (auto& t : threads)
            t.join();

        // binary PPM (P6): same header as P3, then raw bytes instead of text
        std::ofstream f(file, std::ios::binary);
        f << "P6\n" << image_width << ' ' << image_height << "\n255\n";
        f.write(reinterpret_cast<const char*>(pixels.data()), std::streamsize(pixels.size()));

        std::clog << "\nDone.\n";
    }

  private:
    int image_height;           // rendered img height
    double pixel_samples_scale; // color scale factor for a sum of pixel samples
    Vector center;              // point in 3D space from which all scene rays will originate
    Vector pixel00_loc;         // location of pixel 0, 0
    Vector pixel_delta_u;       // offset to pixel to the right
    Vector pixel_delta_v;       // offset to pixel below

    void initialize() {
        // calculate image height to keep aspect ratio, ensuring it's at least 1
        image_height = int(image_width / aspect_ratio);
        image_height = (image_height < 1) ? 1 : image_height;

        pixel_samples_scale = 1.0 / samples_per_px;

        center = Vector(0, 0, 0);

        // determine viewport dimensions
        double focal_length = 1.0;
        double viewport_height = 2.0;
        double viewport_width = viewport_height * (double(image_width) / image_height);

        // calculate the vectors across the horizontal and down the vertical viewport edges
        Vector viewport_u(viewport_width, 0, 0);
        Vector viewport_v(0, -viewport_height, 0);

        // calculate the horizontal and vertical delta vectors from pixel to pixel
        pixel_delta_u = viewport_u / image_width;
        pixel_delta_v = viewport_v / image_height;

        // calculate location of the upper left pixel
        Vector viewport_upper_left = center - Vector(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2;
        pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v);
    }

    // Construct a camera ray originating from the origin and directed at
    // randomly sampled point around the pixel location i, j
    Ray get_ray(int i, int j) const {
        Vector offset = sample_square();
        Vector pixel_sample = pixel00_loc + ((i + offset.x) * pixel_delta_u) + ((j + offset.y) * pixel_delta_v);

        Vector ray_origin = center;
        Vector ray_direction = pixel_sample - ray_origin;

        return Ray(ray_origin, ray_direction);
    }

    // Returns the vector to a random point in the [-.5, -.5]-[+.5, +.5] unit square
    Vector sample_square() const {
        return Vector(random_double() - 0.5, random_double() - 0.5, 0);
    }

    Vector ray_color(const Ray& r, int depth, const Hittable& world) const {
        if (depth <= 0)
            return Vector(0, 0, 0);

        HitRecord rec;

        if (world.hit(r, Interval(0.001, infinity), rec)) {
            Ray scattered;
            Vector attenuation;
            if (rec.mat->scatter(r, rec, attenuation, scattered))
                return attenuation * ray_color(scattered, depth - 1, world);
            return Vector(0, 0, 0);
        }

        Vector unit_direction = unit_vector(r.direction);
        double a = 0.5 * (unit_direction.y + 1.0);
        return (1.0 - a) * Vector(1.0, 1.0, 1.0) + a * Vector(0.5, 0.7, 1.0);
    }
};

#endif
