#include "pcmkit.h"

#include <cmath>
#include <iostream>

namespace {

int fail(int code) {
    std::cerr << "consumer check " << code << " failed\n";
    return code;
}

}  // namespace

int main() {
    float samples[] = {0.5f, -0.25f, 0.2f};
    if (pcmkit_apply_gain(samples, 3, 0.0f) != 0) {
        return fail(1);
    }
    if (std::fabs(samples[0] - 0.5f) > 1e-6f) {
        return fail(2);
    }
    if (pcmkit_apply_gain(samples, 3, 60.0f) != 0) {
        return fail(3);
    }
    if (std::fabs(samples[0] - 1.0f) > 1e-5f || std::fabs(samples[1] + 1.0f) > 1e-5f) {
        return fail(4);
    }
    if (std::fabs(samples[2] - 1.0f) > 1e-5f) {
        return fail(5);
    }
    if (pcmkit_apply_gain(nullptr, 1, 0.0f) == 0) {
        return fail(6);
    }
    if (!std::isnan(pcmkit_peak(nullptr, 1))) {
        return fail(7);
    }

    float dirty[] = {0.25f, 0.5f};
    if (pcmkit_apply_gain(dirty, 2, NAN) == 0) {
        return fail(12);
    }
    if (dirty[0] != 0.25f || dirty[1] != 0.5f) {
        return fail(13);
    }
    float non_finite[] = {0.25f, NAN};
    if (pcmkit_apply_gain(non_finite, 2, 0.0f) == 0) {
        return fail(14);
    }
    if (non_finite[0] != 0.25f) {
        return fail(15);
    }

    float quiet[] = {0.0f, 0.0f};
    if (pcmkit_normalize(quiet, 2) != 0) {
        return fail(8);
    }
    if (quiet[0] != 0.0f || quiet[1] != 0.0f) {
        return fail(9);
    }

    float hot[] = {0.25f, -0.5f};
    if (pcmkit_normalize(hot, 2) != 0) {
        return fail(10);
    }
    const float p = pcmkit_peak(hot, 2);
    if (std::fabs(p - 1.0f) > 1e-5f) {
        return fail(11);
    }
    std::cout << "ok\n";
    return 0;
}
