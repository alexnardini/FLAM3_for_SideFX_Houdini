# FLAM3 for SideFX Houdini
![alt text](https://github.com/alexnardini/FLAM3/blob/main/img/Stripes_01.jpg)

`The above image consit of 400M points and rendered with Houdini internal Mantra renderer.`


## The Fractal Flame Algorithm for SideFX Houdini

An implementation of FLAM3 inside SideFX Houdini software using CVEX programming language.
The code went up and down and finally settled for the most minimalistic version in favor of performance.
The language allowed me to take many shortcuts. He is dealing with execution threading, and offered me
many, fast, ready to use functions like **creating and sampling a cdf** and a very robust and super fast
**random number generator**.

Part of the work is done inside the HDA witin the Houdini environment
like attribute binding, UI building and binding, parameters creations and their visibility conditions.

`Imagine the possibilities of Houdini procedural paradigm to control all aspect of your Flame?`
![alt text](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3_Hviewport.jpg)
`FLAM3 for Houdini generate a live point cloud of the fractal Flame being worked on.`

Higly inspired by Apophysis and its workflow design,
it is a one to one match with it if used within the same limits.
Many Apophysis fractal Flames are available for download on the web
and you can copy all values into FLAM3 for houdini to get the same result.
Downolad Apophysis 7x here: [Apophysis 7x download](https://sourceforge.net/projects/apophysis7x/)

## Future additions ?

Some nice addition to this would be:

- **Xaos**

- **Ability to load and save ".flame" file format. (stripping out whats allowed)**

- **Ability to dublicate iterators ( probably easy to add with a python call back script)**

- **All python addition to improve and make the workflow more enjoable.**
  
- **Copy paste parameters groups from one iterator to the other.**
  
- **Adding Triangle's handle to drive the affine coefficient would be nice, too.**
  
- **Color ramps presets.**

- **More variations even tho using CVEX performace wil need to be safe guarded.**

With time I may get to those, other wise help your self.
Everything has been compiled in favor of execution speed and to make it feel a compact tool.

Hope you enjoy, I had a blast and still having a blast using it.

**For more images that illustrate the development progress:**
[FLAM3 for Houdini web page](https://alexnardini.net/flame-home/)


**Watch a video created with an early version of the tool:**
[F :: the video](https://vimeo.com/506501855)

**Watch the making of here:**
[F :: making of](https://vimeo.com/511517064)




