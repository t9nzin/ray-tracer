#ifndef RTWEEKEND_H
#define RTWEEKEND_H

#include <cmath>
#include <limits>
#include <random>

const double infinity = std::numeric_limits<double>::infinity();
const double pi = 3.1415926535897932385;

// utility functions
inline double degrees_to_radians(double degrees) {
    return degrees * pi / 180.0;
}

// returns a random real in [0, 1)
// each thread gets its own generator so render threads don't share state
inline double random_double() {
    thread_local std::uniform_real_distribution<double> distribution(0.0, 1.0);
    thread_local std::mt19937 generator(std::random_device{}());
    return distribution(generator);
}



inline double random_double(double min, double max) {
    return min + (max - min) * random_double();
}

#endif
