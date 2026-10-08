#ifndef SPHERE_H
#define SPHERE_H

#include <cmath>
#include <memory>

#include "hittable.h"
#include "vector.h"

class Sphere : public Hittable {
  public:
    Sphere(const Vector& center, double radius, std::shared_ptr<Material> mat)
        : center(center), radius(std::fmax(0, radius)), mat(mat) {
        Vector rvec(this->radius, this->radius, this->radius);
        bbox = Aabb(center - rvec, center + rvec);
    }

    bool hit(const Ray& r, Interval ray_t, HitRecord& rec) const override {
        Vector oc = center - r.origin;
        double a = r.direction.length_squared();
        double h = dot(r.direction, oc);
        double c = oc.length_squared() - radius * radius;

        double discriminant = h * h - a * c;
        if (discriminant < 0)
            return false;

        double sqrtd = std::sqrt(discriminant);

        // find nearest root in acceptable range
        double root = (h - sqrtd) / a;
        if (!ray_t.surrounds(root)) {
            root = (h + sqrtd) / a;
            if (!ray_t.surrounds(root))
                return false;
        }

        rec.t = root;
        rec.p = r.at(rec.t);
        Vector outward_normal = (rec.p - center) / radius;
        rec.set_face_normal(r, outward_normal);
        rec.mat = mat.get();

        return true;
    }

    Aabb bounding_box() const override { return bbox; }

  private:
    Vector center;
    double radius;
    std::shared_ptr<Material> mat;
    Aabb bbox;
};

#endif
