#ifndef HITTABLE_LIST_H
#define HITTABLE_LIST_H

#include <memory>
#include <vector>

#include "hittable.h"

/*
 * A list of a bunch of hittable objects.
 * Makes up the entire world for scene.
 */
class HittableList : public Hittable {
  public:
    std::vector<std::shared_ptr<Hittable>> objects;

    HittableList() {}
    HittableList(std::shared_ptr<Hittable> object) { add(object); }

    void clear() {
        objects.clear();
        bbox = Aabb();
    }

    void add(std::shared_ptr<Hittable> object) {
        objects.push_back(object);
        bbox = Aabb(bbox, object->bounding_box());
    }

    bool hit(const Ray& r, Interval ray_t, HitRecord& rec) const override {
        HitRecord temp_rec;
        bool hit_anything = false;
        double closest_so_far = ray_t.max;

        for (const auto& object : objects) {
            if (object->hit(r, Interval(ray_t.min, closest_so_far), temp_rec)) {
                hit_anything = true;
                closest_so_far = temp_rec.t;
                rec = temp_rec;
            }
        }

        return hit_anything;
    }

    Aabb bounding_box() const override { return bbox; }

  private:
    Aabb bbox;
};

#endif
