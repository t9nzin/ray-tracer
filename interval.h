#ifndef INTERVAL_H
#define INTERVAL_H

#include "rtweekend.h"

class Interval {
  public:
    double min, max;

    Interval() : min(+infinity), max(-infinity) {} // default interval is empty
    Interval(double min, double max) : min(min), max(max) {}

    // create the interval tightly enclosing the two input intervals
    Interval(const Interval& a, const Interval& b)
        : min(a.min <= b.min ? a.min : b.min), max(a.max >= b.max ? a.max : b.max) {}

    double size() const { return max - min; }

    bool contains(double x) const { return min <= x && x <= max; }

    bool surrounds(double x) const { return min < x && x < max; }

    double clamp(double x) const {
        if (x < min) return min;
        if (x > max) return max;
        return x;
    }

    // pad the interval by delta / 2 on each side
    Interval expand(double delta) const {
        double padding = delta / 2;
        return Interval(min - padding, max + padding);
    }

    // static instances
    static const Interval empty, universe;
};

inline const Interval Interval::empty    = Interval(+infinity, -infinity);
inline const Interval Interval::universe = Interval(-infinity, +infinity);

#endif
