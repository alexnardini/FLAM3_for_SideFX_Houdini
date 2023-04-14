# The Fractal Flame Algorithm
![FLAM3 Houdini LazySwirl image](https://github.com/alexnardini/FLAM3/blob/main/img/JulianSwirlsKarma.jpg)

`The above image consist of 400M points and rendered with Houdini internal Karma renderer.`

## FLAM3 for SideFX Houdini

<p align="center">
  <img width="160" height="160" src="https://github.com/alexnardini/FLAM3/blob/main/img/LOGO_F_github.svg" />
</p>

**_I really want to make a special honorable mention to Matt Feemster, the Developer of Fractorium._**

**_His c++ code is beyound awesome, clean and packed with useful comments all over the place._**
**_In the last months its been crucial for me to refine and complete this implementation._**

**_Fractorium is really impressive._**


**_Matt, if you will ever read this, thank you!_**

**[FLAM3HOUDINI website](https://www.alexnardini.net/)**

**[FLAM3HOUDINI instagram](https://www.instagram.com/alexnardini/)**

`Compact UI Tabs to acces all functionalities in one unified interface.`
![FLAM3HOUDINI UI Tabs](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3H_UI_Tabs.jpg)

An implementation of FLAM3 inside SideFX Houdini software using CVEX programming language.
Not a real-time thing but If you have a beefy CPU (dual beefy CPU even better) it should be fun.
The code went up and down and finally settled for the most minimalistic version in favor of performance.
The language allowed me to take many shortcuts. He is dealing with execution threading, memory management, and offered me
fast, ready to use functions like **creating and sampling a cdf**, a very robust **random number generator** and more.

Part of the work is done inside the HDA within the Houdini environment
like attribute binding, UI building, parameters creations, their visibility conditions, final compile and much more.

Python has been used to enhance the user experience and to add functionalities like:
copy/paste iterators data, load/save palette's libraries, load flame files authored with other applications, save flame files to load inside other applications and much more.

FLAM3 for SideFX Houdini generate a live point cloud of the fractal Flame being worked on, witch is the actual render.
From there to the final image it is left to the users ( aka points rendering ).
With Houdini integrated Karma renderer you will be able to render the generated fractal flames in nearly real time.

**Highly inspired by Apophysis software and its workflow design.**

Many Apophysis fractal Flames are available for download on the web and you can load them inside FLAM3 for Houdini,
or you can use Apophysis or Fractorium to author your flames first and load them back into FLAM3 for Houdini.

**Download Apophysis 7x here**: [**Apophysis 7x download**](https://sourceforge.net/projects/apophysis7x/)

**Download Fractorium here**: [**Fractorium download**](http://fractorium.com/)


## Viewport live point cloud
`Imagine the possibilities using Houdini procedural paradigm to control all aspect of your Flame.`
![FLAM3HOUDINI viewport](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3H_Hviewport_01_H19.jpg)
![FLAM3HOUDINI viewport](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3H_Hviewport_02_H19.jpg)
`FLAM3 for Houdini generate a live point cloud of the fractal Flame being worked on.`



## Load Flames files authored with Apophysis, Fractorium, etc.
Following some images showing FLAM3 for Houdini rendering some of the Fractorium's example flame files.
Some have been modified to fit within FLAM3 for Houdini available variations. The screenshots shows
Houdini Karma interactive on the left and Fractorium with the same flame file on the right.

`Chocolate Scaffold in Too Many Dimensions by plangkye. Source: Fractorium`
![Fractorium to FLAM3HOUDINI 01](https://github.com/alexnardini/FLAM3/blob/main/img/FractoriumToFLAM3HOUDINI_03.jpg)
`Mountain by tatasz. Source: Fractorium`
![Fractorium to FLAM3HOUDINI 01](https://github.com/alexnardini/FLAM3/blob/main/img/FractoriumToFLAM3HOUDINI_01.jpg)
`Bipolar by tatasz. Source: Fractorium`
![Fractorium to FLAM3HOUDINI 02](https://github.com/alexnardini/FLAM3/blob/main/img/FractoriumToFLAM3HOUDINI_02.jpg)
`Flipped disk. Source: Fractorium`
![Fractorium to FLAM3HOUDINI 03](https://github.com/alexnardini/FLAM3/blob/main/img/FractoriumToFLAM3HOUDINI_00.jpg)


## List of all available variations/plugins:
_Note that all the followings, are also available as PRE__ _and/or POST__ _variations._

_`arch` `auger` `bent` `bent2` `bipolar` `blade` `blob` `blur` `boarders` `bubble` `butterfly` `bwraps` `cell` `conic` `cos` `cosh` `cosine` `cot` `coth` `cpow` `crop` `cross` `csc` `csch` `curl` `curve` `cylinder` `diamond` `disc` `disc2` `edisc` `elliptic` `escher` `ex` `exp` `exponential` `eyefish` `fan` `fan2` `fisheye` `flower` `flux` `foci` `gaussian_blur` `glynnia` `handkerchief` `heart` `hemisphere` `horseshoe` `hyperbolic` `julia` `juliaN` `juliascope` `lazysusan` `linear` `log` `loonie` `mobius` `modulus` `ngon` `noise` `oscope` `parabola` `pdj` `perspective` `pie` `point_symmetry` `polar` `polar2` `polynomial` `popcorn` `popcorn2` `power` `pre_blur` `radialblur` `rays` `rectangles` `rings` `rings2` `scry` `sec` `secant2` `sech` `separation` `sin` `sinh` `sinusoidal` `spherical` `spiral` `split` `splits` `square` `stripes` `supershape` `swirl` `tan` `tangent` `tanh` `twintrian` `unpolar` `waves` `waves2` `wedge` `wedgejulia` `wedgesph` `whorl`_

## Example flame files.
Some of the example flame files I'm using as a proof of correctness and shipped with this implementation are created/authored by some incredible fractal artists using a variety of open source / free apps like Apophysis and Fractorium among the most popular.

Please be sure to check out their gallery:

[tatasz](https://www.deviantart.com/tatasz/gallery), 
[plangkye](https://www.deviantart.com/plangkye/gallery), 
[Pillemaster](https://www.deviantart.com/pillemaster/gallery), 
[Triptychaos](https://www.deviantart.com/triptychaos/gallery), 
[TyranWave](https://www.deviantart.com/tyrantwave/gallery), 
[Zy0rg](https://www.deviantart.com/zy0rg/gallery)


## References
Reference A: [**Github::FLAM3 from Scott Draves and Erik Reckase**](https://github.com/scottdraves/flam3)

Reference B: [**Github::Fractorium from Matt Feemster**](https://bitbucket.org/mfeemster/fractorium/src/master/)

Reference C: [**Github::Apophysis 7x**](https://github.com/xyrus02/apophysis-7x)

Reference D: [**PDF::The Fractal Flame Algorithm publication**](https://flam3.com/flame_draves.pdf)


## Example videos
**[FLAM3HOUDINI vimeo](https://vimeo.com/alexnardini)**

