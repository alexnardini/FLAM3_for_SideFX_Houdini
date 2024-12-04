
# CVEX Source
# File name:    `cvex_TFFAcamcull.vfl`
### Description:
Cull points outside the camera view.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAcamhandles.vfl`
### Description:
Transform the camera handles geometry so it is center framed and properly scaled.
It is only working if the camera type is Perspective and not Orthogonal. 

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAcompensate.vfl`
### Description:
When using FLAM3H in Motion Blur mode, it will compensate the `@pscale` values
so not to loose to much of the body presence due to the layering method being used
to form the final point cloud.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAmbcalc.vfl`
### Description:
Based on FPS, Samples and Shutter Speed it will compute the necessary time increment
for the Motion Blur to build its point cloud's layers.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFApalettesimple.vfl`
### Description:
DISMISSED. This is not being used anymore and it is part of the old legacy code used as a place holder.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAsensor.vfl`
### Description:
All the render settings required by third-party programs such as Apophysis and Fractorium are stored together with the fractal flames when they are saved from FLAM3H. A portion of the render parameters deal with the camera and how the fractal flame you just saved is framed. The FLAM3H camera sensor will precisely display the image framing.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAsensorbbox.vfl`
### Description:
Compute camera sensor bbox data. Used also to reframe the viewport properly.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAsensorInfo.vfl`
### Description:
Compute camera sensor bbox parametric locations for the camera sensor information messages
so they will scale proportionally with the Sensor resolution.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAuicollect.vfl`
### Description:
UI FLAM3 viewport TAG infos collection.
Build a string to use as a TAG composed of all the current FLAM3H iterators and FF informations
like variations used, and many system infos.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAxaos.vfl`
### Description:
Build all the Xaos data to be used inside the Chaos game.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAxaos_chk.vfl`
### Description:
Simply check if Xaos is active. This is a stripped down version of: cvex_TFFAxaos.vfl

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAxformsactive.vfl`
### Description:
Collect all iterator multi-parameter indexs and their count to drive the iterator's xforms handles generation.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAxformshandles.vfl`
### Description:
Transform each iterator handle accordingly to their PRE and POST affine values.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAxformshandlesFF.vfl`
### Description:
Transform the iterator FF handle accordingly to its PRE and POST affine values.

<br>
<br>

# CVEX Source
# File name:    `cvex_TFFAxformshandlescolor.vfl`
### Description:
Assign a unique color to each iterator xforms handle.

<br>
<br>

# CVEX Source
# File name:    `cvex_TheFractalFlameAlgorithm.vfl`
### Description:
The Chaos game. This is where all the data is mixed, shuffled and executed based on the fractal flame logic set by the user.

<br>
<br>

# CVEX Header
# File name:    `flame.h`
### Description:
The path to the selected variations inside the iterator (PRE, VAR, POST). This file will take care of finding the one and execute it.

<br>
<br>

# CVEX Header
# File name:    `flameff.h`
### Description:
The path to the selected variations inside the FF (PRE, VAR, POST). This file will take care of finding the one and execute it.

<br>
<br>

# CVEX Header
# File name:    `flamepp.h`
### Description:
DISMISSED. This file map only non parametric variations.<br>
The path to the selected variations inside the iterator (PRE, VAR, POST). This file will take care of finding the one and execute it.

<br>
<br>

# CVEX Header
# File name:    `functions.h`
### Description:
The FLAM3 functions library used by the variations for their computation. Include also functions used in the Chaos game and for the computation of the Camera sensor infos placement along with some more of a general use case, like for example Xaos transpose.

<br>
<br>

# CVEX Header
# File name:    `genome.h`
### Description:
Build the fractal flame genome entities. A genome is a structure that hold all the data of a flame to be executed, it is like its DNA so to speak.

<br>
<br>

# CVEX Header
# File name:    `variations.h`
### Description:
All the variations functions are inside here.

<br>
<br>

# CVEX Header
# File name:    `xaos.h`
### Description:
This define the path to arrive at the xaos values dictated by the choosen index at each iteration inside the chaos game.