# FLAM3 for SideFX Houdini
![alt text](https://github.com/alexnardini/FLAM3/blob/main/img/Stripes_01.jpg)


## The Fractal Flame Algorithm for SideFX Houdini

An implementation of FLAM3 inside SideFX Houdini software using CVEX programming language.
The code went up and down during the past months and finally settled
for the most minimalistic version in favor of performace.

![alt text](https://github.com/alexnardini/FLAM3/blob/main/img/FLAM3_Hviewport.jpg)
FLAM3 for Houdini generate a point cloud of the fractal Flame being worked on, witch is the actual render.


## Future additions

Some nice addition to this would be:

- Xaos

- Ability to load and save ".flame" file format. (stripping out whats allowed)

- Ability to dublicate iterators ( probably easy to add with a python call back script)

- All python addition to improve and make the workflow more enjoable.
  Ability to copy paste parameters from one iterator to the other and simlar things nice to have.
  
- Adding the Triangle handles to drive the affine coefficient would be nice, too.
  
- Color ramps presets.

- More variations even tho using CVEX performace wil need to be safe guarded.

Everything has been compiled, moslty in favor of execution speed
and to make it feel more of a compact tool.

To compile the .vfl files, open a Houdini shell and go to the vfl files location
and use the Houdini vcc compiler provided. Type `vcc -h` to get help.

So, with time I may get to those, other wise help your self.
Hope you enjoy, I had a blast and still having a blast using it!



