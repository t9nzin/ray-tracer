#ifndef BVH_H
#define BVH_H

#include <algorithm>
#include <memory>
#include <vector>

#include "aabb.h"
#include "hittable.h"
#include "hittable_list.h"

/*
 * Bounding volume hierarchy: a binary tree of bounding boxes.
 * A ray that misses a node's box skips everything beneath it, so hit
 * tests cost roughly O(log n) instead of O(n) per ray.
 */
class BvhNode : public Hittable {
  public:
    // note: copies the list's objects, so the original list can be modified freely
    BvhNode(HittableList list) : BvhNode(list.objects, 0, list.objects.size()) {}

    BvhNode(std::vector<std::shared_ptr<Hittable>>& objects, size_t start, size_t end) {
        // build the bounding box of the span of source objects
        for (size_t i = start; i < end; i++)
            bbox = Aabb(bbox, objects[i]->bounding_box());

        // split along the axis where the objects are most spread out
        int axis = bbox.longest_axis();
        auto comparator = [axis](const std::shared_ptr<Hittable>& a, const std::shared_ptr<Hittable>& b) {
            return a->bounding_box().axis_interval(axis).min < b->bounding_box().axis_interval(axis).min;
        };

        size_t object_span = end - start;

        if (object_span == 1) {
            left = right = objects[start];
        } else if (object_span == 2) {
            left = objects[start];
            right = objects[start + 1];
        } else {
            std::sort(objects.begin() + start, objects.begin() + end, comparator);

            size_t mid = start + object_span / 2;
            left = std::make_shared<BvhNode>(objects, start, mid);
            right = std::make_shared<BvhNode>(objects, mid, end);
        }
    }

    bool hit(const Ray& r, Interval ray_t, HitRecord& rec) const override {
        if (!bbox.hit(r, ray_t))
            return false;

        bool hit_left = left->hit(r, ray_t, rec);
        // only accept a right hit if it's closer than the left one
        bool hit_right = right->hit(r, Interval(ray_t.min, hit_left ? rec.t : ray_t.max), rec);

        return hit_left || hit_right;
    }

    Aabb bounding_box() const override { return bbox; }

  private:
    std::shared_ptr<Hittable> left;
    std::shared_ptr<Hittable> right;
    Aabb bbox;
};

#endif
