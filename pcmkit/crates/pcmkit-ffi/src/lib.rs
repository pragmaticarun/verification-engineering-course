//! C ABI. Panics must not cross this boundary; callers get a status code.

use std::panic::{catch_unwind, AssertUnwindSafe};

use pcmkit::{apply_gain_db, normalize_peak, peak};

const OK: i32 = 0;
const ERR: i32 = 1;

fn samples_mut(ptr: *mut f32, len: usize) -> Option<&'static mut [f32]> {
    if ptr.is_null() {
        return None;
    }
    if len > (isize::MAX as usize) / std::mem::size_of::<f32>() {
        return None;
    }
    // SAFETY: the caller promises `ptr` points at `len` initialized f32 values
    // for the duration of the call, and that the slice does not alias a
    // reference this process is using. A null pointer is rejected above.
    Some(unsafe { std::slice::from_raw_parts_mut(ptr, len) })
}

fn samples_ref(ptr: *const f32, len: usize) -> Option<&'static [f32]> {
    if ptr.is_null() {
        return None;
    }
    if len > (isize::MAX as usize) / std::mem::size_of::<f32>() {
        return None;
    }
    // SAFETY: same contract as `samples_mut`, for a shared borrow.
    Some(unsafe { std::slice::from_raw_parts(ptr, len) })
}

/// Apply a gain in dB and clamp to [-1, 1]. Returns 0 on success, 1 on bad input.
#[no_mangle]
pub extern "C" fn pcmkit_apply_gain(samples: *mut f32, len: usize, db: f32) -> i32 {
    let outcome = catch_unwind(AssertUnwindSafe(|| {
        let Some(buf) = samples_mut(samples, len) else {
            return ERR;
        };
        if apply_gain_db(buf, db).is_err() {
            return ERR;
        }
        OK
    }));
    outcome.unwrap_or(ERR)
}

/// Peak-normalize. Exact silence is left unchanged. Returns 0 on success.
#[no_mangle]
pub extern "C" fn pcmkit_normalize(samples: *mut f32, len: usize) -> i32 {
    let outcome = catch_unwind(AssertUnwindSafe(|| {
        let Some(buf) = samples_mut(samples, len) else {
            return ERR;
        };
        if normalize_peak(buf).is_err() {
            return ERR;
        }
        OK
    }));
    outcome.unwrap_or(ERR)
}

/// Peak magnitude. Returns NaN when the pointer is null.
#[no_mangle]
pub extern "C" fn pcmkit_peak(samples: *const f32, len: usize) -> f32 {
    let outcome = catch_unwind(AssertUnwindSafe(|| {
        let Some(buf) = samples_ref(samples, len) else {
            return f32::NAN;
        };
        peak(buf).unwrap_or(f32::NAN)
    }));
    outcome.unwrap_or(f32::NAN)
}
