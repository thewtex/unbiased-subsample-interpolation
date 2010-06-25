===================================================================
An Approach to Unbiased Subsample Interpolation For Motion Tracking
===================================================================

Abstract
========

Accurate subsample displacement estimation is a necessity in ultrasound
elastography because of the small motions that occur and application of a
derivative operation on displacements.  Many commonly used subsample estimation
techniques have a high amount of error because of bias.  In this paper we
examine an unbiased approach subsample displacement estimations that consists of
2D windowed-sinc interpolation with numerical optimization.  We find that a
Welch or Lanczos window with Nelder-Mead simplex optimization are well suited
for this purpose.  The strain signal-to-noise (SNRe) ratio is compared to other
common interpolation methods, and it is found that the SNRe is superior while
still providing reasonable computational performance.
