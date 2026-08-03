
# <img width="48" height="48" src="../../icons/icon_tag_oclSVG.svg" /> OpenCL
## File name: [**`cl_flam3.cl`**](cl_flam3.cl)
## Houdini version: H20.5 and up
### Description:
Implementation of the algorithm using OpenCL for high performance.<br>
It run billions of iterations per second in Houdini Sop.<br>

_This file include everything_:<br>
- variations' functions
- variations' dispatch
- RNG noises
- weighted probabilities
- the chaos game
- CDF sampling
- kernels
- everything else...

<br>

To maximize performance and since the data is already on the GPU<br>
the **FF**(_finalXform_) run as a separate kernel in its own OpenCL node.<br>

<br>

## Note on the OpenCL implementation

* The OpenCL implementation used the CVEX code as its reference starting point, as a significant amount of effort had already been invested in porting the original Flam3 mathematics to FLAM3H™.

* To take advantage of GPU parallelism, most, if not all, variations have been adapted to be GPU-friendly. Where possible, they have been made branchless and include both a ground-truth implementation and a performance-oriented variant that relies exclusively on OpenCL `native_*()` functions. Many mathematical blocks have also been rewritten using lighter-weight approximations better suited to GPU execution.

* The CVEX codebase could now benefit from the knowledge gained during the development of the GPU implementation. However, it has intentionally been left unchanged to mirror the original Flam3 codebase as closely as possible and serve as the sole reference for correctness. This ensures that the GPU implementation always has a reliable ground truth against which it can be validated.

* If and when SideFX expands the capabilities of the CVEX language, I may revisit the implementation and attempt a rewrite to improve performance and, hopefully, overcome some of the current limitations of CVEX.
