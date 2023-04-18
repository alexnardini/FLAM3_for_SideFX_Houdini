# The Fractal Flame Algorithm
![FLAM3 Intro image](https://github.com/alexnardini/FLAM3/blob/main/img/GITHUB_intro_img.jpg)

`The above image consist of 400M points and rendered with Houdini internal Karma renderer.`

## FLAM3 for SideFX Houdini v1.x
**_A huge special thanks and lots of gratitude toward my family who kept up with me for so long while I was inside the fractal Flame bubble!_**

<p align="center">
  <img width="160" height="160" src="https://github.com/alexnardini/FLAM3/blob/main/img/LOGO_F_github.svg" />
</p>

**[FLAM3HOUDINI website](https://www.alexnardini.net/)**

**[FLAM3HOUDINI instagram](https://www.instagram.com/alexnardini/)**

### Premise

One of the main mission, was to pack the entire algorithm and functionalities I desired inside a tool
using only Houdini out of the box. No HDK.
As a result, it become a somewhat conservative implementation, it has everything but with some limits as I needed to cut corners everywhere wich became a daunting process to put into balance.

There are more functionalities I'd love to add, but this v1.x is happily out as it is.

A big commitment I needed to honor was to learn how to do fractal art. 
Building a fractal art tool without knowing what a fractal artis need and feel while doing it is kind of pointless. And so I did so much fractal art with this tool while developing it that I inhevitably fell in love with the discipline.
It was important so I could shape and steer this tool in the right direction.

### Description

An implementation of FLAM3 inside SideFX Houdini software using Houdini's CVEX programming language.
Not a real-time thing but If you have a beefy CPU (dual beefy CPU even better) it should be fun.

The code went up and down and finally settled for the most minimalistic version in favor of performance.
The language allowed me to take many shortcuts. He is dealing with execution threading, memory management, and offered me
fast, ready to use functions like **creating and sampling a cdf**, a very robust **random number generator** and more.

Part of the work is done inside the HDA within the Houdini environment
like attribute binding, UI building, parameters creations, their visibility conditions, final compile and much more.

Python has been used to enhance the user experience and to add functionalities like:
copy/paste iterators data, load/save palette's libraries, load/save flame's file format, responses/automations to user actions and much more.

FLAM3 for SideFX Houdini generate a live point cloud of the fractal Flame being worked on, witch is the actual render.
From there to the final image it is left to the users ( aka points rendering ).
With Houdini integrated Karma renderer you will be able to render the generated fractal flames in nearly real time.

`Karma interactive rendering in the Houdini's viewport.`
![FLAM3HOUDINI Karma rendering viewport](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3H_Hviewport_Karma_H19.jpg)

**Highly inspired by Apophysis software and its workflow design.**

Many Apophysis fractal Flames are available for download on the web and you can load them inside FLAM3 for Houdini,
or you can use Apophysis or Fractorium to author your flames first and load them back into FLAM3 for Houdini. But also the other way around, create your flame in Houdini and render them inside other applications...you've got choises.

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

## Considerations

Fractal flames are really expensive to compute, no wonder GPUs made miracles in this field too.

Being inside Houdini has its major advantages. Only think at the possibilities you have to animate those flames using Houdini's procedural paradigm and toolsets, endless! Useless to say the ability to create a pipeline around this tool easily using Houdini's Python HOM libraries.

If you know how to create your flames the speed isnt bad at all. On a modern workstation you'll do pretty much all the fractals flames you can think of within minutes for ~HD images. ( the higher the resolution and the more points you'll need to get a cleaner image, and some flames are tougher than others ). You start with default settings and work your way up, as everything in Houdini.

Karma with the integrated Nvidia Optix denoiser is a great combo to produce your fractal images.

Almost all fractal flame images on my website and instagram use an average of 64 iterations max,
some much less and some a bit more. A few exceptions went above 128 and up to 256/512. 

Some flames require truly an high amount of iterations to resolve properly.
Below are some presets that Chaotica software ship with, ported inside FLAM3 for Houdini.
They have been choosen becasue they use variations I have implemented too and becasue they are really expensive to solve.

Those presets require hundreds of iterations to show you the proper results, some of them require thousands.

Lets start with this gnarl preset:

`Iterations needed in FLAM3 for Houdini to resolve: 1280`

`zuek ieddaka gnarl`
![Chaotica to FLAM3HOUDINI 00](https://github.com/alexnardini/FLAM3/blob/main/img/ChaoticaToFLAM3HOUDINI_00.jpg)

The next two are a bit more speedy:

`Iterations needed in FLAM3 for Houdini to resolve: 512`
`( potentially a bit less are needed for those but just in case. )`

`tatasz blue modulus`
![Chaotica to FLAM3HOUDINI 01](https://github.com/alexnardini/FLAM3/blob/main/img/ChaoticaToFLAM3HOUDINI_01.jpg)

`meckie lazyswirls`
![Chaotica to FLAM3HOUDINI 02](https://github.com/alexnardini/FLAM3/blob/main/img/ChaoticaToFLAM3HOUDINI_02.jpg)

This one is quick and beautiful:

`Iterations needed in FLAM3 for Houdini to resolve: 64`

`tatasz majestic`
![Chaotica to FLAM3HOUDINI 03](https://github.com/alexnardini/FLAM3/blob/main/img/ChaoticaToFLAM3HOUDINI_03.jpg)

End the last one:

`Iterations needed in FLAM3 for Houdini to resolve: 32`

`tatasz blurry splits`
![Chaotica to FLAM3HOUDINI 04](https://github.com/alexnardini/FLAM3/blob/main/img/ChaoticaToFLAM3HOUDINI_04.jpg)

You'll find other scenarios where your iterations number will need to rise up,
especially when relying heavily on containers and such.

However from all my tests, betweem 16 and 96 iterations will get you covered on almost all your needs. And dnt forget you can create some beautiful fractal flames with just 6 iterations, I have plenty of them on my webiste and instagram.

I could add a lot more functionalities but this project consumed me for a very long time.
Every aspects of this algorithm, once understood, look somehow simple at first but they are all a challenge on their own. It has been quite a crazy ride to pack everyhting inside this implementation.

It is time to park this project for a little bit but I really, really loved the long journey on this topic and I will now for ever love fractal flames as a whole, they are awesome!

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

