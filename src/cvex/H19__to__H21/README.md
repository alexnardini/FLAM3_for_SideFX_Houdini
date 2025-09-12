
# CVEX Source
# File name:    `cvex_TFFAcamcull.vfl`
## Houdini version: H19 and up
### Description:
Cull points outside the camera view.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAcamhandles.vfl`
## Houdini version: H19 and up
### Description:
Transform the camera handles geometry so it is center framed and properly scaled.
It is only working if the camera type is Perspective and not Orthogonal. 

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAcompensate.vfl`
## Houdini version: H19 and up
### Description:
When using FLAM3H™ in Motion Blur mode, it will compensate the `@pscale` values
so not to loose to much of the body presence due to the layering method being used
to form the final point cloud.

<br>
<br>


# CVEX Source
# File name:    `cvex_TFFAffdata.vfl`
## Houdini version: H19 and up
### Description:
NOT USED ANYMORE. (it is now done inside the Houdini environment)<br>
Collect all FF(_finalxform_) data to be passed to the chaos game.

<br>
<br>


# CVEX Source
# File name:    `cvex_TFFAiteratorsdata.vfl`
## Houdini version: H19 and up
### Description:
NOT USED ANYMORE. (it is now done inside the Houdini environment)<br>
Collect all iterators data to be passed to the chaos game.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAmbcalc.vfl`
## Houdini version: H19 and up
### Description:
Based on FPS, Samples and Shutter Speed it will compute the necessary time increment
for the Motion Blur to build its point cloud's layers.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFApalettesimple.vfl`
## Houdini version: H19 and up
### Description:
DISMISSED. This is not being used anymore and it is part of the old legacy code used as a place holder.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAsensor.vfl`
## Houdini version: H19 and up
### Description:
All the render settings required by third-party programs such as Apophysis and Fractorium are stored together with the fractal flames when they are saved from FLAM3H™. A portion of the render parameters deal with the camera and how the fractal flame you just saved is framed. The FLAM3H™ camera sensor will precisely display the image framing.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAsensorbbox.vfl`
## Houdini version: H19 and up
### Description:
Compute camera sensor bbox data. Used also to reframe the viewport properly.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAsensorInfo.vfl`
## Houdini version: H19 and up
### Description:
Compute camera sensor bbox parametric locations for the camera sensor information messages
so they will scale proportionally with the Sensor resolution.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAuicollect.vfl`
## Houdini version: H19 and up
### Description:
UI FLAM3 viewport TAG infos collection.
Build a string to use as a TAG composed of all the current FLAM3H™ iterators and FF informations
like variations used, and many system infos.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAxaos.vfl`
## Houdini version: H19 and up
### Description:
Build all the Xaos data to be used inside the Chaos game.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAxaos_chk.vfl`
## Houdini version: H19 and up
### Description:
NOT USED ANYMORE. Simply check if Xaos is active. This is a stripped down version of: `cvex_TFFAxaos.vfl`

<br>
<br>


# CVEX Source
# File name:    `cvex_TheFractalFlameAlgorithm.vfl`
## Houdini version: H19 and up
### Description:
The Chaos game. This is where all the data is mixed, shuffled and executed based on the fractal flame logic set by the user.

<br>
<br>

# CVEX Header
# File name:    `flame.h`
## Houdini version: H19 and up
### Description:
The path to the selected variations inside the iterator (PRE, VAR, POST). This file will take care of finding the one and execute it.

<br>
<br>

# CVEX Header
# File name:    `flameff.h`
## Houdini version: H19 and up
### Description:
The path to the selected variations inside the FF (PRE, VAR, POST). This file will take care of finding the one and execute it.

<br>
<br>

# CVEX Header
# File name:    `flamepp.h`
## Houdini version: H19 and up
### Description:
DISMISSED. This file map only non parametric variations.<br>
The path to the selected variations inside the iterator (PRE, VAR, POST). This file will take care of finding the one and execute it.

<br>
<br>

# CVEX Header
# File name:    `functions.h`
## Houdini version: H19 and up
### Description:
The FLAM3 functions library used by the variations for their computation. Include also functions used in the Chaos game and for the computation of the Camera sensor infos placement along with some more of a general use case, like for example Xaos transpose.

<br>
<br>

# CVEX Header
# File name:    `genome.h`
## Houdini version: H19 and up
### Description:
Build the fractal flame genome entities. A genome is a structure that hold all the data of a flame to be executed, it is like its DNA so to speak.

<br>
<br>

# CVEX Header
# File name:    `variations.h`
## Houdini version: H19 and up
### Description:
All the variations functions are inside here.

<br>
<br>

# CVEX Header
# File name:    `xaos.h`
## Houdini version: H19 and up
### Description:
This define the path to arrive at the xaos values dictated by the choosen index at each iteration inside the chaos game.