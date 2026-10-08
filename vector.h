#ifndef VECTOR_H
#define VECTOR_H

#include <cmath>
#include <iostream>

#include "rtweekend.h"

// 3 coordinates
class Vector {
  public:
    double x, y, z;

    Vector() : x(0), y(0), z(0) {}
    Vector(double x, double y, double z) : x(x), y(y), z(z) {}

    Vector operator-() const { return Vector(-x, -y, -z); }

    double operator[](int i) const { return i == 0 ? x : (i == 1 ? y : z); }
    double& operator[](int i) { return i == 0 ? x : (i == 1 ? y : z); }

    Vector& operator+=(const Vector& v) {
        x += v.x;
        y += v.y;
        z += v.z;
        return *this;
    }

    Vector& operator*=(double s) {
        x *= s;
        y *= s;
        z *= s;
        return *this;
    }

    Vector& operator/=(double s) { return *this *= 1 / s; }

    double length() const { return std::sqrt(length_squared()); }

    double length_squared() const { return x * x + y * y + z * z; }

    // return true if the vector is close to zero in all dimensions
    bool near_zero() const {
        double s = 1e-8;
        return std::fabs(x) < s && std::fabs(y) < s && std::fabs(z) < s;
    }

    // general utility methods
    static Vector random() {
        return Vector(random_double(), random_double(), random_double());
    }

    static Vector random(double min, double max) {
        return Vector(random_double(min, max), random_double(min, max), random_double(min, max));
    }
};

// vector utility functions

inline std::ostream& operator<<(std::ostream& out, const Vector& v) {
    return out << v.x << ' ' << v.y << ' ' << v.z;
}

inline Vector operator+(const Vector& u, const Vector& v) {
    return Vector(u.x + v.x, u.y + v.y, u.z + v.z);
}

inline Vector operator-(const Vector& u, const Vector& v) {
    return Vector(u.x - v.x, u.y - v.y, u.z - v.z);
}

inline Vector operator*(const Vector& u, const Vector& v) {
    return Vector(u.x * v.x, u.y * v.y, u.z * v.z);
}

inline Vector operator*(double t, const Vector& v) {
    return Vector(t * v.x, t * v.y, t * v.z);
}

inline Vector operator*(const Vector& v, double t) {
    return t * v;
}

inline Vector operator/(const Vector& v, double t) {
    return (1 / t) * v;
}

inline double dot(const Vector& u, const Vector& v) {
    return u.x * v.x + u.y * v.y + u.z * v.z;
}

inline Vector cross(const Vector& u, const Vector& v) {
    return Vector(u.y * v.z - u.z * v.y,
                  u.z * v.x - u.x * v.z,
                  u.x * v.y - u.y * v.x);
}

inline Vector unit_vector(const Vector& v) {
    return v / v.length();
}

inline Vector random_in_unit_sphere() {
    while (true) {
        Vector p = Vector::random(-1, 1);
        if (p.length_squared() < 1)
            return p;
    }
}

// uniformly distributed point on the unit sphere, generated directly
// (uniform z and azimuth) rather than by rejection sampling + normalizing
inline Vector random_unit_vector() {
    double z = random_double(-1, 1);
    double phi = 2 * pi * random_double();
    double r = std::sqrt(1 - z * z);
    return Vector(r * std::cos(phi), r * std::sin(phi), z);
}

inline Vector random_on_hemisphere(const Vector& normal) {
    Vector on_unit_sphere = random_unit_vector();
    if (dot(on_unit_sphere, normal) > 0.0)
        return on_unit_sphere;
    else
        return -on_unit_sphere;
}

inline Vector reflect(const Vector& v, const Vector& n) {
    return v - 2 * dot(v, n) * n;
}

inline Vector refract(const Vector& uv, const Vector& n, double etai_over_etat) {
    double cos_theta = std::fmin(dot(-uv, n), 1.0);
    Vector r_out_perp = etai_over_etat * (uv + cos_theta * n);
    Vector r_out_parallel = -std::sqrt(std::fabs(1.0 - r_out_perp.length_squared())) * n;
    return r_out_perp + r_out_parallel;
}

#endif
