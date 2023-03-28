# The Fractal Flame Algorithm
![FLAM3 Houdini LazySwirl image](https://github.com/alexnardini/FLAM3/blob/main/img/JulianSwirlsKarma.jpg)

`The above image consist of 400M points and rendered with Houdini internal Karma renderer.`

## FLAM3 for SideFX Houdini

<p align="center">
  <img width="160" height="160" src="https://github.com/alexnardini/FLAM3/blob/main/img/LOGO_F_github.svg" />
</p>

**[FLAM3HOUDINI website](https://www.alexnardini.net/)**

**[FLAM3HOUDINI instagram](https://www.instagram.com/alexnardini/)**

An implementation of FLAM3 inside SideFX Houdini software using CVEX programming language.
Not a real-time thing but If you have a beefy CPU (dual beefy CPU even better) it should be fun.
The code went up and down and finally settled for the most minimalistic version in favor of performance.
The language allowed me to take many shortcuts. He is dealing with execution threading, memory management, and offered me
fast, ready to use functions like **creating and sampling a cdf**, a very robust **random number generator** and more.

Part of the work is done inside the HDA within the Houdini environment
like attribute binding, UI building, parameters creations, their visibility conditions, final compile and much more.

FLAM3 for SideFX Houdini generate a live point cloud of the fractal Flame being worked on, witch is the actual render.
From there to the final image it is left to the users ( aka points rendering ).

**Highly inspired by Apophysis software and its workflow design**,

Many Apophysis fractal Flames are available for download on the web
and you can load them inside FLAM3 for Houdini,
or you can use Apophysis or Fractorium for example, to author your flames and load them back into FALM3 for Houdini.

Only restrictions when authoring flames with external apps are:
the flames must use the same variations included inside FLAM3 for Houdini.
A maximum of 4 variations plus PRE_BLUR plus 2 PRE and 1 POST variations for each iterator are allowed.
( for a total of 8 vars per iterator ).
Each itertor's variations share the same parametric parameters.
This mean that if inside iterator 2 you add 3 Mobius, they will all share the same "im:abcd" and "re:abcd" parameters insde the VARS Tab.
Maybe in one of the next Houdini release SideFX will make the instantiaton of the parameter inside a multi parameter group much faster
so that we can add different one for each variation of the same type.
For FF ( FinalXForm ) you have 3 vars plus 2 POST vars available.
So be wise in your choices and pick your battles.

**Download Apophysis 7x here**: [**Apophysis 7x download**](https://sourceforge.net/projects/apophysis7x/)

**Download Fractorium here**: [**Fractorium download**](http://fractorium.com/)


## Viewport live point cloud
`Imagine the possibilities using Houdini procedural paradigm to control all aspect of your Flame.`
![FLAM3HOUDINI viewport](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3_Hviewport_ChaoticaMatch_H19.jpg)
![FLAM3HOUDINI viewport](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3_Hviewport_H19.jpg)
`FLAM3 for Houdini generate a live point cloud of the fractal Flame being worked on.`

## Load Flames files authored with Apophysis, Fractorium, etc.
Below some comparison with FLAM3 for Houdini rendering some of the Fractorium's example flame files.
Some have been modified to fit within FLAM3 for Houdini available variations. The screenshots shows
Houdini Karma interactive render on the left and Fractorium render of the same flame file on the right.
Note that those flames in Houdini have been pre generated. Intercative karma render after generation is real fast.
![Fractorium to FLAM3HOUDINI 01](https://github.com/alexnardini/FLAM3/blob/main/img/FractoriumToFLAM3HOUDINI_01.jpg)
![Fractorium to FLAM3HOUDINI 02](https://github.com/alexnardini/FLAM3/blob/main/img/FractoriumToFLAM3HOUDINI_02.jpg)
![Fractorium to FLAM3HOUDINI 03](https://github.com/alexnardini/FLAM3/blob/main/img/FractoriumToFLAM3HOUDINI_00.jpg)


## References
Reference A: [**Github::FLAM3 from Scott Draves and Erik Reckase**](https://github.com/scottdraves/flam3)

Reference B: [**Github::Fractorium from Matt Feemster**](https://bitbucket.org/mfeemster/fractorium/src/master/)

Reference C: [**Github::Apophysis 7x**](https://github.com/xyrus02/apophysis-7x)

Reference D: [**PDF::The Fractal Flame Algorithm publication**](https://flam3.com/flame_draves.pdf)


## Example videos
**[FLAM3HOUDINI vimeo](https://vimeo.com/alexnardini)**

