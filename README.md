# The Fractal Flame Algorithm
![alt text](https://github.com/alexnardini/FLAM3/blob/main/img/TheCURE_hd.jpg)

`The above image consist of 400M points and rendered with Houdini internal Mantra renderer.`

https://user-images.githubusercontent.com/42110232/141430036-d6b7f2db-93a0-4c25-b9e7-d89c35bbefc9.mp4

https://user-images.githubusercontent.com/42110232/141742842-00628772-a018-4d1f-876d-899f52311c7c.mp4

https://user-images.githubusercontent.com/42110232/142930391-560d51d8-6ed5-4418-9d1e-a24bf2e37dbd.mp4

`The above Videos consist of 300M points and rendered with Houdini internal Karma renderer.`


## FLAM3 for SideFX Houdini
An implementation of FLAM3 inside SideFX Houdini software using CVEX programming language.
The code went up and down and finally settled for the most minimalistic version in favor of performance.
The language allowed me to take many shortcuts. He is dealing with execution threading, memory management, and offered me
fast, ready to use functions like **creating and sampling a cdf** and a very robust **random number generator**.

Part of the work is done inside the HDA within the Houdini environment
like attribute binding, UI building, parameters creations, their visibility conditions and much more.

`Imagine the possibilities using Houdini procedural paradigm to control all aspect of your Flame.`
![alt text](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3_Hviewport.jpg)
![alt text](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3_Hviewport_ChaoticaMatch.jpg)
`FLAM3 for Houdini generate a live point cloud of the fractal Flame being worked on.`

**Highly inspired by Apophysis software and its workflow design**,
it is a one to one match with it.
Many Apophysis fractal Flames are available for download on the web
and you can copy all values into FLAM3 for houdini to get the same result.
**Downolad Apophysis 7x here**: [**Apophysis 7x download**](https://sourceforge.net/projects/apophysis7x/)

## References
Reference A: [**Github::FLAM3 from Scott Draves and Erik Reckase**](https://github.com/scottdraves/flam3)

Reference B: [**Github::Apophysis 7x**](https://github.com/xyrus02/apophysis-7x)

Reference C: [**PDF::The Fractal Flame Algorithm publication**](https://flam3.com/flame_draves.pdf)

Reference D: [**Github::Fractorium from Matt Feemster**](https://bitbucket.org/mfeemster/fractorium/src/master/)





