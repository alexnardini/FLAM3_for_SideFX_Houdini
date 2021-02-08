# FLAM3
![alt text](https://github.com/alexnardini/FLAM3/blob/main/img/F_01_logo_gh.jpg)
## The Fractal Flame Algorithm for SideFX Houdini

[![FLAM3 for Houdini](https://github.com/alexnardini/FLAM3/blob/main/img/F_vimeo_img_preview.jpg)](https://vimeo.com/506501855 "FLAM3 for Houdini - Click to Watch!")
`Whatch "F", a little video reel of Flames created during the development of FLAM3 for SideFX Houdini.`

## Based on the original "The Fractal Flame Algorithm: FLAM3".

One variation per iterator is the default limit. However, there are currently 100+ variations to choose from ( each one with their own 3D version ), and as optional: pre blur variations ( pb ), post variations ( pv ), final flame transform ( FF ) and variation’s iterators ( VI ); not to mention motion blur, too.

#### Implementation notes:
Since we work on 3D points and not screen pixels, some changes have been made to the way we are dealing with variation’s weights. While we can simply skip to hit a pixel if rejected, we can not ignore a point as it is a real entity in the Houdini 3D world. One of the main differences introduced is to always weight the points back to their most basic function. For the same reason, Xaos is not implemented yet.
