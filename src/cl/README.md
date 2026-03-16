
# <img width="48" height="48" src="../../icons/icon_optionOCLSVG.svg" /> OpenCL
## File name: [**`cl_flam3.cl`**](cl_flam3.cl)
## Houdini version: H21 and up
### Description:
Implementation of the algorithm using OpenCL for high performance.<br>
It run billions of iterations per second in Houdini Sop.<br>

_This file include everything_:<br>
- the variations functions,
- the RNG noises, 
- variation dispatch,
- weighted probabilities,
- the chaos game,
- CDF sampling,
- kernels,
- and everything else...

<br>

In this implementation, the **FF**(_finalXform_) run as a separate kernel in its own OpenCL node<br>
to maximize performance since the data is already on the GPU.
