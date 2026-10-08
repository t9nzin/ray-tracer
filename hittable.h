#ifndef HITTABLE_H
#define HITTABLE_H

#include <memory>

#include "aabb.h"
#include "interval.h"
#include "ray.h"
#include "vector.h"

class Material;

class HitRecord {
  public:
    Vector p;
    Vector normal;
    double t = 0.0;
    // non-owning: the scene owns materials. a shared_ptr here would mean an atomic
    // refcount update on every hit, which threads contend on heavily
    const Material* mat = nullptr;
    bool front_face = false;

    // set the hit record normal vector
    // NOTE: outward_normal is assumed to have unit length
    void set_face_normal(const Ray& r, const Vector& outward_normal) {
        front_face = dot(r.direction, outward_normal) < 0;
        normal = front_face ? outward_normal : -outward_normal;
    }
};

class Hittable {
  public:
    virtual ~Hittable() = default;

    virtual bool hit(const Ray& r, Interval ray_t, HitRecord& rec) const = 0;

    virtual Aabb bounding_box() const = 0;
};

#endif
