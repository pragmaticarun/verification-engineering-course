#ifndef PCMKIT_H
#define PCMKIT_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Returns 0 on success, 1 when the pointer is null or a sample is non-finite. */
int pcmkit_apply_gain(float *samples, size_t len, float db);

/* Peak-normalize to 1.0. Silence stays silence. Returns 0 on success. */
int pcmkit_normalize(float *samples, size_t len);

/* Peak magnitude, or NaN when `samples` is null. */
float pcmkit_peak(const float *samples, size_t len);

#ifdef __cplusplus
}
#endif

#endif
