===================================================================
An Approach to Unbiased Subsample Interpolation For Motion Tracking
===================================================================
Matthew M. McCormick\ :sup:`1,2` and Tomy Varghese\ :sup:`1,2`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. highlights::

  :sup:`1`\ Department of Biomedical Engineering

  University of Wisconsin-Madison

  Room 2130 Engineering Centers Building

  1550 Engineering Drive

  Madison, WI 53706-1609

------------------

.. highlights::

  :sup:`2`\ Department of Medical Physics

  University of Wisconsin-Madison

  1111 Highland Ave, Rm 1005

  1550 Engineering Drive

  Madison, WI 53705-2275

-------------------

Correspondence can be sent to matt@mmmccormick.com.


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


----------------

**Key Words**: Subsample interpolation, strain imaging, motion tracking, sinc
reconstruction.

----------------

1. Introduction
===============

Digital images present challenges in ultrasound motion tracking.  The sampling
rates are barely sufficient to satisfy the Shannon-Nyquist sampling criterion.
For example, a sampling rate of 40 MHz on the Siemens S2000 scanner is very
close to the 20 MHz Nyquist frequency with its 18L6 transducer that purports to
respond to frequencies up to 18 MHz.  In the lateral direction, where resolution
is determined by transducer element spacing, sampling requirements are reduced.
However, the sampling rate is usually an order of magnitude smaller in this
direction.  Furthermore, noise is introduced into the post-deformation signal.
These conditions are a concern when trying to perform ultrasounds strain imaging
where displacement estimates need a precision on the order of micrometers; the
sample spacing in axial direction is only 19 μm with a for a 40 MHz sampling
rate.  Cespedes et al. [Cespedes1995]_ examined the theoretical values for time
delay estimation using cross correlation with parameters from a typical
ultrasound system.  He found the standard deviation due to time quantization was 5.7
ns, which is much larger than the Cramer-Rao Lower Bound (CRLB) for the continuous
case, 0.024 ns.

This subsample delay estimation problem has been studied extensively in 1D in
the sonar and radar fields, where the use of cross-correlation as a similarity
statistic is dominant.  If the signal is approximately narrowband,
quadrature subsample delay techniques can be used [Maskell2002]_. (Tomy: do you
know of other references to use here, possibly something by Kanai?).
Maskell and Woods described a technique where the shift between signals is not
determined by comparing them directly but by comparisons with shifted versions of
a reference signal [Maskell1999]_.  The total delay is then determined to be the difference
between the two delays to the reference signal.

A number of techniques used the fact that phase of the analytic signal's
cross-correlation in the vicinity of the signal shift will have a slope
equivalent to the nominal centroid frequency and zero crossing at the shift
[MarpleJr1999,Pesavento1999]_.  Marple discusses the theory behind this method,
and the scaling that must occur at the DC and Nyquist frenquencies during
calculation that should take place when dealing with discrete signals.
Grennberg and Sandell described a fast subsample delay estimator calculated with
the cross correlation of the delayed signal with the Hilbert transform of the
original signal using an arcsin [Grennberg1994]_.  Other authors used a similar
approach by taking the cross-correlation of base-band analytic signals from both
the original and shifted signal [Pesavento1999,Fromageau2003]_.  The root is
then found with an iterative modified Newton method.  This approach only works
for narrowband signals with small time delays.  For larger time delays,
strategies have to be employed to prevent phase aliasing.  However, if these
approaches can be used, they are advantagous because they are very precise with
minimal computation that can be performed in a single step.  This approach only
works for narrowband signals with small time delays.  In medical ultrasound, the
signal normally only oscillates in the axial direction, so these methods can
only be used to calculate axial displacements.  However, if unconventional
beaming forming strategies are used, phase can also be tracked in the lateral
direction [Basarab2009]_.  Alternatively, a synthetic oscillatory signal can be
generate by taking the inverse Fourier transform of half the transformed signal
[Chen2004]_.  Instead of the more prevalent cross-correlation/Fourier methods,
Viola and Walker have worked on a sum-of-squared error/cubic spline method
[Viola2005,Viola2008]_.  After a cubic spline fit, the problem reduces to
finding the roots of a polynomial whose order is proportional to the number
samples in the fit.

As studied by in [Viola2005]_, a more brute force to determining a more precise
signal shift is to resample the image through interpolation before performing
cross-correlation.  Use of a matched filter during resample may improve the
result [Lai1999].  Instead of resampling and recalculation of the
cross-correlation, curve fitting can be applied.  For example, a parabola
[Boucher1981,Jacovitti1993,Foster1990,Moddemeijer1991,Lai1999]_ or cosine fit
[deJong1990]_ can be used in 1D or an ellipsoid in 2D [Giunta1999]_.  These
methods are computationally efficient and easy to implement, but they suffer
from bias because the underlying signal may not conform to the shape chosen.
[Zahiri-Azar2008,Geiman2000,Jacovitti1993,Moddemeijer1991,Cespedes1995]_.

Curve fitting bias can be avoided by instead using signal reconstruction with
sinc interpolation, which is the maximum likelihood estimator for interpolation
[Cespedes1995,Boucher1981]_.  Cespedes et al. examined the use of 1D sinc
reconstruction to locate the cross-correlation peak, and found that it
significantly out-performs parabolic or cosine interpolation.  Reconstruction is
computationally expensive compared to curve fitting methods, and an optimization
method must be utilized to find the peak location.  Cespedes used a binary
search method to decrease computation times [Cespedes1995]_.

It has also been demonstrated that 2D displacement vector estimates generate
better results than two-pass 1D displacement estimation
[Konofagou1998,Chen2004,Geiman2000,Zahiri-Azar2008]_.  Sumi described an
iterative 2D phase tracking technique [Sumi1999]_, and Ebbini described a similar technique
that iteratively searches for the location where the gradient vectors of the 2D
complex cross correlation are orthogonal, which exists along the zero-phase
contour [Ebbini2006]_.

In this paper, we propose the use of a 2D sinc reconstruction method coupled
with traditional numerical optimization techniques for subsample ultrasound
displacement estimation.  Since parabolic methods remain the most popular method
referenced in the literature and to follow the analysis of Cespedes, we compare
the new method again parabolic and cosine curve fitting.  Performance is
evaluated as the elastographic signal-to-noise ratio (*SNRe*) in phantoms and
simulations.  We examine the optimal sinc-filtering window length and type, and
the computational performance of the Nelder-Mead simplex and a regular step
gradient descent optimizer.

2. Methods
==========

2.1 Subsample interpolation algorithm
-------------------------------------

In the article by Cespedes et al., a binary search algorithm improved the time
required to localize the subsample 1D cross-correlation peak.  The approach
involves probing the sampled cross-correlation with sinc interpolation.  We
framed this process as a multi-parameter, single-valued cost function numerical
optimization problem.  We applied traditional numerical optimization methods that
have quicker convergence properties than a binary search and can be applied to
multiple parameters.  The cost function to be maximized is the cross-correlation
function.  The parameters to be optimized are the axial and lateral
displacements.

We obtained subsample displacements values with 2D sinc interpolation
[Meijering1999,Yoo2002]_.  The sinc kernel, :math:`K(t)` is given by

.. math:: K(t) =  w(t) sinc(t) = w(t) \frac{\sin(\pi t)}{\pi t} \;\;\;\;\; (Eq.\; 1)

where w(t) is the window function.  We examined the window
functions shown in Table 2.0 [Meijering1999,Yoo2002]_,  Here *m* is the window
radius; the window is non-zero from *-m* to *m*.

Table 2.0 - Sinc window functions
---------------------------------

============= =======================
 Window Name   Expression
------------- -----------------------
 Blackman      :math:`0.42 + 0.50 \cos(\frac{\pi x}{m}) + 0.08 \cos(\frac{2 \pi x}{m})`
 Cosine        :math:`\cos(\frac{\pi x}{2 m})`
 Hamming       :math:`0.54 + 0.46 \cos(\frac{\pi x}{m})`
 Lanczos       :math:`sinc( \frac{\pi x}{m})`
 Welch         :math:`1 - \frac{x^2}{m^2}`
============= =======================

An interpolated normalized cross-correlation value, :math:`XCORR(x,y)` was calculated with
the sampled correlation values across the radius, and the window,

.. math:: XCORR(x,y) = \sum_{i=\lfloor x \rfloor + 1 - m}^{\lfloor x \rfloor + m} \sum_{j=\lfloor y \rfloor + 1 - m}^{\lfloor y \rfloor + m} XCORR_{i,j} K(x-i) K(y-j) \;\;\;\;\; (Eq.\; 2)

In this article, two simple optimization methods were examined, a regular-step
gradient descent and Nelder-Mead simplex (amoeba) optimization.  In the
regular-step gradient descent method, parameters are advanced along the
direction of the negative of the gradient, which is calculated with the finite
difference method.  The step length is reduced by half
when the sign of the gradient changes [Ibanez2005]_.  The well-known Nelder-Mead
simplex optimization advances a three-point simplex over the optimization space.

We set the initial condition to be the sampled maximum of the normalized
cross-correlation.  The parameter space was the displacement in the axial and
lateral directions defined in fractional samples.  We proceeded with
optimization until reaching convergence defined with a minimum step length with
the regular-step gradient descent method and a parameter tolerance with the
Nelder-Mead simplex method.

2.2  Motion tracking algorithm
------------------------------

The proposed subsample interpolation algorithm was used within a block-matching
motion tracking context.  Normalized cross-correlation was used as a similarity
metric when comparing the matching blocks in the pre-deformation image to the
image content in the post-deformation image search region.  A multi-level
tracking approach was used to improve search region initialization at the lowest
level of the multi-level image pyramid.  A three-level pyramid
was utilized where the highest level was decimated by a factor of three in the
axial direction and a factor of two in the lateral direction, and the middle level
was decimated by a factor of 2 in the axial direction only.  Before decimation,
the data was filtered with a discrete Gaussian with variance :math:`(f/2)^2` where *f*
is the decimation factor [Lindeberg1994]_.  Matching-block sizes varied linearly
from the top to bottom level with axial length of 1.3mm and lateral width of
4.0mm at the top level to an axial length of 0.5mm and lateral width of 2.2mm at
the bottom level.  There was no block overlap.

To remove peak-hopping tracking errors, displacements with strains greater than
15% magnitude were replaced with linearly interpolated values from outside the
faulty region.  To improve correlation, matching-blocks at lower levels were
compressed according to the strain estimated at the previous level
[Chaturvedi1998,Brusseau2008]_.  The
matching block was scaled by a factor of :math:`1+\varepsilon_d`, where :math:`\varepsilon_d`
is the strain in direction *d*, at its center and resampled using sinc interpolation
with a Lanczos window and radius four.

In order to demonstrate that proposed method is effective in finding the
subsample peak in situations other than normalized cross-correlation of
ultrasound images, we also examined interpolation after regularization with a
Bayesian regularization method [McCormick2011]_.  Where noted in the results, two iterations of
the regularization method where applied to the normalized cross-correlation.
The parameter of the algorithm, the strain regularization sigma (SRS) was 0.15
in the axial direction and 0.075 in the lateral direction.

The effectiveness of the algorithm was tested on both tissue-mimicking phantom
and simulated ultrasound images.

2.3 Tissue-mimicking phantom
----------------------------

We collected ultrasound radio-frequency (RF) data on a tissue-mimicking (TM)
phantom with a clinical ultrasound scanner, the Siemens S2000 (Siemens
Ultrasound, Mountain View, CA, USA).  The Siemens VFX9-4 linear array transducer
acquired RF data at 40MHz with an excitation frequency of 8.9 MHz and a depth of
5.5 cm.

A 95×95×95 mm, uniform oil-gelatin phantom was placed in a rigid, low-friction basin
and imaged from the top.  Uni-axial, uniform, uncontrained compression was
applied by placing the surface of the tranducer in an acrylic plate.  Slip
boundary conditions were maintained at the interface of the phantom and plate by
ensuring adequate oil was present for lubrication.  Precise deformations in the
directions intended were achieved by a motion with three linear degrees of
freedom, and two rotational degrees of freedom.  A reference image was
collection along with post-deformation images at 0.5%, 1.0%, 3.0%, 5.0%, and
7.0% strain magnitude.  The position of the transducer was rotated and translated to
obtain an uncorrelated scattering field, and the set of deformed images were
re-collected.  This process was repeated to obtain 30 independent trials at each
strain magnitude.

2.4 Ultrasound and mechanics simulation
---------------------------------------

Computer simulations were performed intended to model the ultrasound and
mechanical behavior of the clinical system and TM phantom.  A phantom was
generated by simulating randomly positioned acoustic scatterers over a
40×40×10mm volume.  A transducer was modeled with a Gaussian spectrum having a
center frequency of 8.0 MHz and a 40% fractional bandwidth, 128 element linear
array with 0.15mm lateral by 10mm elevational element dimensions, and 0.2 mm
element pitch [Li1999]_.  Focusing occured at a 20mm depth.

Displacements were applied to the scatterers assuming uni-axial compression of
an incompressible material, i.e. strains were opposite in sign and half the
magnitude of the axial directions.  The same set of strains applied to the TM
phantom were generated.  Axial displacements started from zero at the the
transducer surface to a negative value at the bottom of the simulated phantom,
and lateral displacements transitioned from negative to positive values across
the phantom with zero lateral displacement at the centerline.  New sets of
randomly distributed scatterers were used to create 30 independent scattering
fields.

2.5 Experimental protocol
-------------------------

Following the analysis by Cespedes et al., we evaluated the effectiveness of the
subsample interpolation method using the elastographic signal-to-noise ratio
(*SNRe*).

.. math:: SNR_e [dB] = 20 \log10 \; ( \frac {m_\varepsilon} {s_\varepsilon} ) \;\;\;\;\; (Eq.\; 3)

*SNRe* was evaluated over the strain magnitude examined for both the TM phantom
and simulation, in the axial and lateral directions, and with and without
regularization.  Twice the standard error calculated for the 30 trials examined
in each experiment was displayed in resulting plots.  We compare sinc
interpolation with numerical optimization via Nelder-Mead simplex or regular
step gradient descent with parabolic interpolation, cosine interpolation, and no
interpolation.

The *SNRe* was also used to evaluate the parameters of the algorithm.  With a
window radius of four samples, we compare the Blackman, Cosine, Hamming,
Lanczos, and Welch windows types.  The effect of window length is examined along
with the convergence tolerance.

Given a convergence tolerance of 1e-5 samples, we inserted time probes in our
code to measure the average time required for convergence in an image on an
Intel Core i7 Processor at 2.8 GHz.  We also measured the effect of the initial
simplex offset on the number of iterations required for convergence when using the
Nelder-Mead optimization method.

3. Results
==========



