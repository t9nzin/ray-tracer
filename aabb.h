#ifndef AABB_H
#define AABB_H

#include "interval.h"
#include "ray.h"
#include "vector.h"

// axis-aligned bounding box, stored as one interval per axis
class Aabb {
  public:
    Interval x, y, z;

    Aabb() {} // default box is empty, since intervals are empty by default

    Aabb(const Interval& x, const Interval& y, const Interval& z) : x(x), y(y), z(z) {
        pad_to_minimums();
    }

    // treat the two points a and b as extrema for the bounding box
    Aabb(const Vector& a, const Vector& b) {
        x = (a.x <= b.x) ? Interval(a.x, b.x) : Interval(b.x, a.x);
        y = (a.y <= b.y) ? Interval(a.y, b.y) : Interval(b.y, a.y);
        z = (a.z <= b.z) ? Interval(a.z, b.z) : Interval(b.z, a.z);
        pad_to_minimums();
    }

    // box tightly enclosing both input boxes
    Aabb(const Aabb& box0, const Aabb& box1) {
        x = Interval(box0.x, box1.x);
        y = Interval(box0.y, box1.y);
        z = Interval(box0.z, box1.z);
    }

    const Interval& axis_interval(int n) const {
        if (n == 1) return y;
        if (n == 2) return z;
        return x;
    }

    // slab test: narrow ray_t by each axis' entry/exit distances
    bool hit(const Ray& r, Interval ray_t) const {
        for (int axis = 0; axis < 3; axis++) {
            const Interval& ax = axis_interval(axis);
            const double adinv = 1.0 / r.direction[axis];

            double t0 = (ax.min - r.origin[axis]) * adinv;
            double t1 = (ax.max - r.origin[axis]) * adinv;

            if (t0 < t1) {
                if (t0 > ray_t.min) ray_t.min = t0;
                if (t1 < ray_t.max) ray_t.max = t1;
            } else {
                if (t1 > ray_t.min) ray_t.min = t1;
                if (t0 < ray_t.max) ray_t.max = t0;
            }

            if (ray_t.max <= ray_t.min)
                return false;
        }
        return true;
    }

    // index of the longest axis of the bounding box
    int longest_axis() const {
        if (x.size() > y.size())
            return x.size() > z.size() ? 0 : 2;
        else
            return y.size() > z.size() ? 1 : 2;
    }

  private:
    // avoid zero-width boxes (e.g. flat objects) which break the slab test
    void pad_to_minimums() {
        double delta = 0.0001;
        if (x.size() < delta) x = x.expand(delta);
        if (y.size() < delta) y = y.expand(delta);
        if (z.size() < delta) z = z.expand(delta);
    }
};

#endif
