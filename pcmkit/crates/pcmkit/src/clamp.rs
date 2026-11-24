//! A tiny clamp, separated so the heavy job can mutate this file alone.
//!
//! `cargo mutants` rewrites operators and rebuilds. A one-file target keeps
//! that smoke inside a few minutes. Two edits are equivalent and survive:
//! `>` versus `>=`, and `<` versus `<=`, because the equal sample already
//! returns that rail. `tools/heavy/mutants.sh` allows those two lines and
//! fails if any other mutant survives.

/// Fold a sample into [-1, 1].
///
/// Infinities compare as outside the rails, so they clamp. NaN compares false
/// against every bound, so it falls through unchanged. Callers that need to
/// reject non-finite input still have to test `is_finite` themselves.
///
/// Written as comparisons, not `f32::clamp`, so cargo-mutants can rewrite the
/// operators. `manual_clamp` is allowed for that reason.
#[allow(clippy::manual_clamp)]
pub fn clamp_unit(sample: f32) -> f32 {
    if sample > 1.0 {
        1.0
    } else if sample < -1.0 {
        -1.0
    } else {
        sample
    }
}

#[cfg(test)]
mod tests {
    use super::clamp_unit;

    #[test]
    fn outside_samples_land_on_the_rail() {
        assert_eq!(clamp_unit(2.0), 1.0);
        assert_eq!(clamp_unit(-2.0), -1.0);
        assert_eq!(clamp_unit(4.5), 1.0);
    }

    #[test]
    fn inside_samples_and_the_rails_stay() {
        assert_eq!(clamp_unit(0.25), 0.25);
        assert_eq!(clamp_unit(0.0), 0.0);
        assert_eq!(clamp_unit(1.0), 1.0);
        assert_eq!(clamp_unit(-1.0), -1.0);
        assert_eq!(clamp_unit(-0.5), -0.5);
    }

    #[test]
    fn infinities_hit_the_rail_and_nan_falls_through() {
        assert!(clamp_unit(f32::NAN).is_nan());
        assert_eq!(clamp_unit(f32::INFINITY), 1.0);
        assert_eq!(clamp_unit(f32::NEG_INFINITY), -1.0);
    }
}
