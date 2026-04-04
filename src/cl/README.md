
# <img width="48" height="48" src="../../icons/icon_tag_oclSVG.svg" /> OpenCL
## File name: [**`cl_flam3.cl`**](cl_flam3.cl)
## Houdini version: H21 and up
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
