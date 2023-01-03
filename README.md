# The Fractal Flame Algorithm
![FLAM3 Houdini LazySwirl image](https://github.com/alexnardini/FLAM3/blob/main/img/JulianSwirlsKarma.jpg)

`The above image consist of 400M points and rendered with Houdini internal Karma renderer.`

## FLAM3 for SideFX Houdini

![FLAM3 logo svg](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3_HDA_intro.svg)

**[FLAM3HOUDINI website](https://www.alexnardini.net/)**

**[FLAM3HOUDINI instagram](https://www.instagram.com/alexnardini/)**

An implementation of FLAM3 inside SideFX Houdini software using CVEX programming language.
Not a real-time thing but If you have a beefy CPU (dual beefy CPU even better) it should be fun.
The code went up and down and finally settled for the most minimalistic version in favor of performance.
The language allowed me to take many shortcuts. He is dealing with execution threading, memory management, and offered me
fast, ready to use functions like **creating and sampling a cdf** and a very robust **random number generator**.

Part of the work is done inside the HDA within the Houdini environment
like attribute binding, UI building, parameters creations, their visibility conditions and much more.

**Highly inspired by Apophysis software and its workflow design**,
it is a one to one match with it.
Many Apophysis fractal Flames are available for download on the web
and you can copy all values into FLAM3 for houdini to get the same result.
**Downolad Apophysis 7x here**: [**Apophysis 7x download**](https://sourceforge.net/projects/apophysis7x/)

## Viewport live point cloud
`Imagine the possibilities using Houdini procedural paradigm to control all aspect of your Flame.`
![FLAM3 Houdini viewport](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3_Hviewport_ChaoticaMatch_H19.jpg)
![FLAM3 Houdini viewport](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3_Hviewport_H19.jpg)
`FLAM3 for Houdini generate a live point cloud of the fractal Flame being worked on.`

## Karma interactive rendering
![FLAM3 Houdini Karma](https://github.com/alexnardini/FLAM3/blob/main/img/DDragon_Karma_UI.jpg)
![FLAM3 Houdini Karma](https://github.com/alexnardini/FLAM3/blob/main/img/CosmicFlower_Karma_UI.jpg)
![FLAM3 Houdini Karma](https://github.com/alexnardini/FLAM3/blob/main/img/Medalion_Karma_UI.jpg)
`Use Karma integrated renderer to interactively render the generated fractal flames in the Houdini's viewport.`


## References
Reference A: [**Github::FLAM3 from Scott Draves and Erik Reckase**](https://github.com/scottdraves/flam3)

Reference B: [**Github::Apophysis 7x**](https://github.com/xyrus02/apophysis-7x)

Reference C: [**PDF::The Fractal Flame Algorithm publication**](https://flam3.com/flame_draves.pdf)

Reference D: [**Github::Fractorium from Matt Feemster**](https://bitbucket.org/mfeemster/fractorium/src/master/)


## Example videos
**[FLAM3HOUDINI vimeo](https://vimeo.com/alexnardini)**




