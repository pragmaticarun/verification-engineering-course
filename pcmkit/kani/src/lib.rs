//! One Kani proof, excluded from the workspace so `cargo test --offline`
//! never downloads the `kani` crate.
//!
//! The input is an `i8` divided by 16, which includes values outside
//! [-1, 1] and values on both rails. It is not every `f32`.

#[cfg(kani)]
#[kani::proof]
fn clamp_unit_holds_an_i8_grid() {
    let steps: i8 = kani::any();
    let sample = f32::from(steps) / 16.0;
    let clamped = pcmkit::clamp_unit(sample);
    assert!(clamped <= 1.0);
    assert!(clamped >= -1.0);
}
