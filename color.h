#ifndef COLOR_H
#define COLOR_H

#include <cmath>

#include "interval.h"
#include "vector.h"

inline double linear_to_gamma(double linear_component) {
    if (linear_component > 0)
        return std::sqrt(linear_component);

    return 0;
}

// write the pixel's 3 bytes (r, g, b) into out
inline void write_color(unsigned char* out, const Vector& pixel_color) {
    double r = pixel_color.x;
    double g = pixel_color.y;
    double b = pixel_color.z;

    // apply a linear to gamma transform for gamma 2
    r = linear_to_gamma(r);
    g = linear_to_gamma(g);
    b = linear_to_gamma(b);

    // translate [0, 1] component values to the byte range [0, 255]
    static const Interval intensity(0.000, 0.999);
    int rbyte = int(256 * intensity.clamp(r));
    int gbyte = int(256 * intensity.clamp(g));
    int bbyte = int(256 * intensity.clamp(b));

    out[0] = (unsigned char)rbyte;
    out[1] = (unsigned char)gbyte;
    out[2] = (unsigned char)bbyte;
}

#endif
