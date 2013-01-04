===================================================================
An Approach to Unbiased Subsample Interpolation for Motion Tracking
===================================================================
Response to Reviewer 2 Comments
+++++++++++++++++++++++++++++++

We are grateful to the reviewer for their thoughtful and helpful comments.

Response to General Comments
----------------------------

**Comment**

This manuscript describes a new subsample interpolation method for ultrasonic motion
tracking. The paper reports original analysis and interesting results; however, a few issues need
to be addressed before it can be considered for publication. The following issues require
particular attention:

1. Include a clearer description of the method. Some illustrative examples of the method should have been provided. (Also, see below.)
#. Every other researcher reported better results with cosine interpolation than parabolic interpolation. They used various systems and system parameters. Thus, the authors’ argument about the better performance of parabolic method is not convincing. Check for errors.  
#. There are other inconsistencies, as described in additional comments.
#. If available, some in vivo results should be included.

**Response**

The authors appreciate the reviewers insightful comments.  We have endeavored to address all remarks in response to the specific commentst and as described below:

1. An additional figure was added to the work (now Figure 1) to illustrate how iterative sinc interpolation works for subsample peak interpolation and how it reduces bias relative to the parametric methods.
#. The authors checked for errors in the cosine interpolation results and are confident in the results.  These data-dependent performance of the cosine fit relative to the parabolic fit was expected given the dependence on the form and sampling of the data, which is discussed in detail within the Cespedes et al. reference.  We also think it is important to publish these contrasting quantitative results so a more thorough survey of possible algorithm behavior is available in the literature.
#. Apparent inconsistencies have been corrected or better explained.
#. Unfortunately, no in vivo results are available.

Response to Specific Comments
-----------------------------

**Comment 1**

Page 5, Lines 1-3: Mention whether these bias errors are significant for ultrasound
applications. In the reviewer’s experience, the errors are not large.

**Response 1**

While in many cases the errors are not large (Figure 2a, 2.5% strain magnitude), the range of quality images that can be created (Figure 2b, 0.5% strain magnitude).

The following comment was added:

*A reduction of subsample peak interpolation bias errors can extend the useful
range of imaged strains for a given algorithm.*

**Comment 2**

Page 7. Eqn 2.  Two comments: i) Is XCORRi,j normalized correlation?  ii) Although the reviewer can follow this, it is not clear just by looking at it how this equation produces interpolated
correlation. This is a key point of this paper and illustrated
examples would greatly help.

**Response 2**

Yes, this results in the normalized cross-correlation as remarked in the text.  The relationship with the new fix is described:

*The normalized cross-correlation values are the basis for interpolation, illustrated as the
solid circles in Fig. 1.*

**Comment 3**

Page 8, Line 14.  “False-peak error” might be more formal than “peak-hopping error.”

**Response 3**

We now use "false-peak error".

**Comment 4**

Page 8, Second paragraph.  An illustration should be provided for matching-block scaling.

**Response 4**

In the interest of space contraints and since the focus of the article is the interpolation method instead of the multi-scale algorithm, the figure was not included.

**Comment 5**

Page 9, Line 17.  Do the authors mean “collected?”

**Response 5**

Yes; "obtain" has be changed to "collect".

**Comment 6**

Page 11, Eqn 3.  Are the numerator and denominator the mean and standard deviation?

**Response 6**

Yes; a more explicit description now follows the equation.

**Comment 7**

Page 11, Lines 5-7.  “Twice the ... plots.”—Confusing sentence.

**Response 7**

The sentence now reads:

*Error bars in the the results are two times the standard error computed over 30 trials for point.*

**Comment 8**

Page 28, Fig. 3.  Two comments: i) In the reviewer’s experience, cosine interpolation is at least as fast as the parabolic interpolation.  ii) 261 vs 1 μs is a huge difference in computational complexity.  iii)  The “no interpolation” image looks nearly as good as the other images, at least visually!

**Response 8**

Performance depends on implementation, but the cosine interpolation should be slower than the parabolic interpolation based only on computational complexity.  The parabolic interpolation consists only of a few simple additions, multiplications, and divisions.  The cosine interpolation has arccos and arctan computations, which are significantly more computationally complex mathematical operations.

The quantification in the table should remind a reader that even though sinc interpolation may be feasible, the parameteric methods are certainly faster.

There was a major error during a last-minute reformat of the figure before submission -- a) had been replaced with d).  The error has been corrected, and the visual improvement from sinc interpolation is now apparent.
