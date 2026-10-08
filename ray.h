#ifndef RAY_H
#define RAY_H

#include "vector.h"

class Ray {
  public:
    Vector origin;
    Vector direction;

    Ray() {}
    Ray(const Vector& origin, const Vector& direction) : origin(origin), direction(direction) {}

    Vector at(double t) const { return origin + t * direction; }
};

#endif
