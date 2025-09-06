# FLAM3H™ indie


<p align="center">
  <img width="160" height="160" src="./img/LOGO_F_github.svg" />
</p>

## License
- Software: [GNU GPL v3.0](LICENSE)
- Documentation: [CC BY-SA 4.0](LICENSE.docs)

## Platforms
_One code base, multiple platforms._
- **Win**, **Mac**, **Linux**

## Houdini versions
_The following are Houdini versions where FLAM3H™ is fully functional, tested and supported._
- **H19** to **H20.5**
- **H21**

</br>
</br>

## Release history
Below is a list of all the **FLAM3H™** (_and_ **FLAM3HUSD**) releases and the updates that went into each.</br>
They are all available in this Github repository.

</br>
</br>

### [<ins>From v1.8.80</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.80) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**



<br>
<br>




### [<ins>From v1.8.79</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.79) ###

- **Fix**: When a FLAM3H™ HDA is installed inside an incompatible Houdini version its node will now properly trigger an error message instead of a non related warning message.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.77</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.77) ###

- **New H21 ONLY**: Added FLAM3H™ and FLAM3HUSD descriptive infos to the new H21 node info window. 
- **Fix**: Improved handling of incompatible Houdini versions.



<br>
<br>




### [<ins>From v1.8.75</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.75) ###

#### FLAM3H™ ####

- **New H21 ONLY**: Added FLAM3H™ for **H21** (_initial release_).
- **New H21 ONLY**: New iterators' control icon to add or delete iterators while still updating their xaos string correctly.
- **New**: When an iterator is in SOLO mode, changing the iterator focus using the SYS tab' select iterator mini menu will also set the selected iterator to be in SOLO mode, allowing you to easily review them one by one automatically.
- **New**: The whole user interface will now be disabled and zero points will be generated when a FLAM3H OTL is installed in the incorrect Houdini version. The user will also get an error message informing them of the appropriate Houdini version to use.
- **Fix**: CP Save action button -> [SHIFT+LMB] file chooser had the wrong default file extension to start with, it is now fxed.
- **Fix**: Improved some status bar messages about copying PRE or POST affine values and when resetting them.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**

</br>
</br>

_Some of the small fixes/improvements include_:

- **Fix H21 ONLY**: The variations menus had varying lengths based on the selected variation's name, it is now of a fixed length as it used to be in preview versions of Houdini.
- Copy/paste menus (_iterators and FF_) now delete their keyframes every time they are executed (_they should not be allowed to be animated_).
- Variation "**_Pt_symmetry_**" has been renamed to: "**_Point sym_**".



<br>
<br>




### [<ins>From v1.8.68</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.68) ###

- **New**: Added a H21 note inside the HDA Documentaion->Limitations' chapter.
- **New**: CP and OUT tabs save action button: [SHIFT+LMB] will now open a file chooser if not a valid filepath is present already, otherwise it will open the file explorer to the file location.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.67</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.67) ###

_Renamed some files in this Github repository and updated some additional licenses informations_.

#### FLAM3H™ ####

- **Updated HDA documentation.**

#### FLAM3HUSD v0.1.59 - Prototype ####

- **New**: Added documentation license chapter to match the one added inside FLAM3H™.
- **Updated HDA documentation and some parameters tooltips.**



<br>
<br>




### [<ins>From v1.8.66</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.66) ###

- **New**: Added FLAM3H™ documentation license chapter.
- **New**: When opening a file chooser with [SHIFT+LMB] from either the CP or IN tabs, it will now start at the currently loaded file directory location if any.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.64</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.64) ###

- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.63</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.63) ###

- **New**: "XML_last_loaded" changes checks against the currently loaded Flame file preset on disk are now scattered into more places across the UI functionalities.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.61</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.61) ###

- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.60</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.60) ###

- **Fix**: When saving flames with empty iterator FF name (only in a rare case in H19.x), the iterator FF name was not being built properly. it is now fixed.
- **Fix**: When saving flames with empty iterator's names (only in a rare case in H19.x), the iterator names were not being built properly. it is now fixed.
- **Fix**: When saving flames with inactive iterators while some with a name different from their default name, the iterator number was not being counted properly. it is now fixed.
- **Fix**: Loading Flame presets with only spaces characters as their iterator's names would fail to build a proper name inside FLAM3H™ (_leaving the iterator's names empty_). It is now fixed.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.57</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.57) ###

- **Fix**: Loading hip files with FLAM3H™ nodes in it from a fresh Houdini session did not initialize the xform handles viz viewport wire width value. it is now fixed.
- **Fix**: copy/paste iterator menu's all entrie from another FLAM3H™ node now has the parents dots in its label also in H20.5.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.55</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.55) ###

- **Fix**: The HDA documentation now goes more in-depth on some of the topics that are important for the editing and understanding of fractal Flames.
- **Fix**: Improved some tooltips and their formatting layout.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.52</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.52) ###

- **New**: The OUT Tab file contents menu action button is now also able to save the currently selected OUT Flame preset into the Clipboard.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.50</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.50) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.47</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.47) ###

- **New**: The OUT Tab file contents menu will now print a quick info recap of the flame preset being selected to the status bar and as a flash message. Infos like: iterators/xforms count, if it is using a finalXform(FF), palette colors count and its HSV values if used.
- **Fix**: Some parameters (mostly icon buttons) should not be allowed to be animated/keyframed as they are mainly a frontend interface to control their backend toggle. It is now fixed.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.45</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.45) ###

_This release complete a very, very long polyshing period of all that was done in FLAM3H™ up to todays date_.

- **New**: Added a new chapter to the OUT Tab documentation: `Anatomy of a XML flame file format`.
- **Fix**: Affine scale parameter now clear/delete its keyframes everytime is evaluated. It can not be animated.
- **Fix**: Final cvex compiled file size: ~1kb smaller.
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.42</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.42) ###

- **Fix**: When in camera sensor mode, toggling off the "edit render properties" toggle was not restoring the viewport settings prior to entering the camera sensor mode, it is now fixed.
- **Recompiled all cvex code using the latest stable Houdini version: vcc compiler: v20.5.654**
- **Updated HDA documentation.**



<br>
<br>




### [<ins>From v1.8.40</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.40) ###

- **New**: Added action script button to reset the Motion Blur parms to their default values.
- **Updated HDA documentation and some parameters tooltips.**



<br>
<br>




### [<ins>From v1.8.39</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.39) ###

- **Fix**: The Xaos Ui display info message had a typo in one of its keyword arguments causing an error when trying to display it.



<br>
<br>




### [<ins>From v1.8.38</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.38) ###

- **Fix**: Changing an iterator's name and then Undoing to the preview name was not updating the SYS tab select iterator menu entries list, it is now fixed.



<br>
<br>




### [<ins>From v1.8.36</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.36) ###

- Copy/Paste data menus are now fully evaluated only when their tab is visible improving the UI performance a little.



<br>
<br>




### [<ins>From v1.8.35</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.35) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**



<br>
<br>



### [<ins>From v1.8.33</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.33) ###

- **Improved print messages when parametric variation's XML keys are missing.**
- **Small fixes/improvements as part of an ongoing polishing pass.**



<br>
<br>



### [<ins>From v1.8.31</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.31) ###

- **Fix**: Silenced a warning message on Flame load for the XML key: color_speed as it is specific to Fractorium.



<br>
<br>



### [<ins>From v1.8.30</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.30) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**



<br>
<br>




### [<ins>From v1.8.28</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.28) ###

- **New**: You can now paste only the palette data from a Flame preset stored into the clipboard.
- **New**: When all iterators are inactive or 0(_Zero_) Weight, FLAM3H™ wont generate any points.
- **Updated HDA documentation.**



<br>
<br>



### [<ins>From v1.8.25</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.25) ###

- **New**: Iterator's names are now automatically set when they are at their default name, otherwise they will be kept as is.
- **New**: When saving Flames out with disabled iterators, FLAM3H™ will discard them and rename the active one based of their new multi parameter index if they have a default iterator name.
- **Small fixes/improvements as part of an ongoing polishing pass.**



<br>
<br>



### [<ins>From v1.8.22</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.22) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**



<br>
<br>



### [<ins>From v1.8.20</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.20) ###

_This is a migration release to a newer python version, for now to: python **3.11** as of: **Houdini 20.5.x**._<br>
_No much changes yet but it is a start and it will be the way forward._

- **New**: Started migrating to a newer python version, for now to: **python 3.11** (as of **Houdini 20.5** which is the latest available).
- **New**: FLAM3H™ will now use the appropriate python module version based on the Houdini version being run. 
- **New**: The new updated python module is for **python version 3.11** and it will be used only when run within **Houdini 20.5.x**. 
- **New**: All the older Houdini versions up until **Houdini 19.x.x** will use the FLAM3H™ python module for **python version 3.7**.
- **New**: On first node instance creation, FLAM3H™ will print informations about the python module version being used.



<br>
<br>



### [<ins>From v1.8.15</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.15) ###

- **New**: Improved variation's XML key names searches. 



<br>
<br>



### [<ins>From v1.8.14</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.14) ###

- **New**: Motion blur XML keys are now checked and corrected if needed on Flame load. 



<br>
<br>




### [<ins>From v1.8.13</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.13) ###

#### FLAM3H™ ####

- **Small fixes/improvements as part of an ongoing polishing pass.**

#### FLAM3HUSD v0.1.53 - Prototype ####

- **Small fixes/improvements as part of an ongoing polishing pass.**



<br>
<br>



### [<ins>From v1.8.12</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.12) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**



<br>
<br>



### [<ins>From v1.8.10</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.10) ###

- **New**: If they are missing from the loaded XML data on Flame load, set the OUT renderer settings to its defaults.
- **Small fixes/improvements as part of an ongoing polishing pass.**



<br>
<br>



### [<ins>From v1.8.08</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.08) ###

- **Fix**: RIP(Remove Invalid Points), F3C(Flame3 compatibility) and Motion blur were being always activated and set to its default values on flame load even when the loaded Flame did not use them at all, it is now fixed. A regression from versions: [**v1.8.07**](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.07)



<br>
<br>



### [<ins>From v1.8.07</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.07) ###

- **New**: Improved IN XML data correction.
- **Fix**: when loading a Flame from the clipboard and while not using the enumerated menus, the prefix [CLIPBOARD] was not being added to the selected IN preset menu labels.
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>



### [<ins>From v1.8.00</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.8.00) ###

- **New**: Added an info message to each of the FLAM3H™ HDA sub-network nodes and updated some parameter's tooltips.
- **Updated HDA documentation.**


<br>
<br>



### [<ins>From v1.7.98</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.98) ###

#### FLAM3H™ ####

- **Fix**: When in viewport Dark mode, adding new Sop viewers to the current Houdini desktop and creating a new FLAM3H™ node right after was not updating the available viewers data, loosing track of the old Sop viewers stashed Color Scheme and cam data. it is now fixed.
- **Small fixes/improvements as part of an ongoing polishing pass.**

#### FLAM3HUSD v0.1.52 - Beta ####

- **Fix**: When in viewport Dark mode, adding new Lop viewers to the current Houdini desktop and creating a new FLAM3HUSD node right after was not updating the available viewers data, loosing track of the old Lop viewers stashed Color Scheme and cam  data. it is now fixed.
- **Small fixes/improvements as part of an ongoing polishing pass.**

<br>
<br>



### [<ins>From v1.7.94</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.94) ###

- **Python code improvements.**
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>



### [<ins>From v1.7.90</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.90) ###

- **Updated HDA documentation.**


<br>
<br>



### [<ins>From v1.7.88</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.88) ###

- **Fix**: IN infos stats heading parameter is now controlled by the FLAM3H™ python module.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>



### [<ins>From v1.7.85</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.85) ###

- **Fix**: Paste a flame render properties from the clipboard was not working anymore (a regression from preview versions).


<br>
<br>



### [<ins>From v1.7.84</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.84) ###

- **Fix**: After fixing some more rounding errors in other variations, the new Elliptic implemented in v1.7.83 now produce the correct result at 64bit as in: [Improved Elliptic](https://mathr.co.uk/blog/2017-11-01_a_more_accurate_elliptic_variation.html)


<br>
<br>



### [<ins>From v1.7.83</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.83) ###

- **Fix**: Added an improved Elliptic version which helps with rounding errors.


<br>
<br>



### [<ins>From v1.7.82</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.82) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>



### [<ins>From v1.7.80</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.80) ###

- **Fix**: CP palette save action button did not have the new icon name properly wired. (a regression from preview version)
- **Fix**: Updated variation DISC2 precalc inside its HDA compiled parametric wrangle core.
- **Fix**: Final cvex compiled file size: ~2kb smaller.


<br>
<br>



### [<ins>From v1.7.77</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.77) ###

- **New**: When entering the Camera Sensor Viz mode while in viewport xforms handles VIZ mode, the xforms handles will be hidden and the camera sensor frame outline will be of color Yellow if not in solo mode and of color Red if in solo mode.
- **New**: Added a new intro image to the HDA Documentation.
- **New**: Added a new illustration to the HDA Documentation for the Camera Sensor VIZ outline.
- **New**: New icon for the copy/paste data for when the marked iterator is active.
- **New**: New icon for the copy/paste data for when the marked FF is active.
- **Fix**: Renamed all the HDA's extra files icons to be prefixed with: "**`icon_`**"
- **Fix**: Renamed all the HDA's extra files geometry to be prefixed with: "**`geo_`**"
- **Fix**: Renamed the main python module file to have the minimum python version to run with baked into the file name.
- **Fix**: Updated python module creation to use the new main python module file name.
- **Fix**: Final cvex compiled file size: ~15kb smaller.
- **Updated HDA documentation.**


<br>
<br>



### [<ins>From v1.7.60</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.60) ###

- **New**: The camera sensor viz now have an outline.
- **New**: If entering the camera sensor viz while in xform handles viz, the camera sensor viz outline will be red to signal it.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>



### [<ins>From v1.7.55</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.55) ###

- **New**: New bookmark icon for the sys tab select iterator menu entrie for when an iterator is OFF and marked. Now in line with the others.
- **New**: New copy/paste menu entries icons. Now when the marked iterator is OFF or when is zero weight uses the same icons as the sys tab select iterator menu's bookmark icons. Now in line with the others.
- **New**: New FF menu copy/paste icon when the marked FF is OFF. Now in line with the others.
- **Updated HDA documentation.**


<br>
<br>



### [<ins>From v1.7.51</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.51) ###

- **New**: When copy/paste affine values between iterators/FLAM3H™ nodes, if they are at their defaults the post affine will be automatically turned OFF.
- **New**: When copy/paste affine values between FF/FLAM3H™ nodes, if they are at their defaults the post affine will be automatically turned OFF.
- **New**: FLAM3H™ will now check if the iterators/FF post affine are at their default values on hip file load and turn the post affine OFF if so.
- **Updated HDA documentation.**


<br>
<br>



### [<ins>From v1.7.47</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.47) ###

- **Fix**: When resetting an iterator to its defaults it will now properly reset all its parametric variation's parameters (PRE, VAR and POST).
- **Fix**: When resetting an FF(finalXform) to its defaults it will now properly reset all its parametric variation's parameters (PRE, VAR and POST).


<br>
<br>



### [<ins>From v1.7.45</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.45) ###

- **Fix**: Density parameter and its preset menu are now cleared from any keyframes every time they are set.
- **Fix**: Removed prints to the console if an invalid file path is entered inside the CP, IN and OUT tabs as the menu presets message is more than enough and just more elegant by itself.
- **Fix**: Density can now be animated only from the preferences tab density parameter.
- **Fix**: When FLAM3H™ reset the color correction curves data/parameters it will now also delete their keyframes.
- **Fix**: When FLAM3H™ reset the affine values (PRE or POST) it will now also delete their keyframes.
- **Fix**: When FLAM3H™ copy data between the affine (from PRE to POST and viceversa) it will now also delete their keyframes before copying.
- **Fix**: When copy/paste data between iterators/FF FLAM3H™ will now delete all keyframes before copying the values.
- **Fix**: When swapping an iterator PRE variations it will now be able to swap also if they have keyframes and/or expressions.
- **Fix**: When swapping the FF POST variations it will now be able to swap also if they have keyframes and/or expressions.
- **Fix**: XML xf_color_speed's key is now officially a @property of: class out_flame_xforms_data(out_flame_utils):


<br>
<br>


### [<ins>From v1.7.35</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.35) ###

#### FLAM3H™ ####

- **Small fixes/improvements as part of an ongoing polishing pass.**

#### FLAM3HUSD v0.1.50 - Beta ####

- **Fix**: Fixed a potential error on hip file load.


<br>
<br>


### [<ins>From v1.7.33</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.33) ###

- **Fix**: Removed two parameters from the FLAM3H™ UI IN tab renderer settings folder and now using only one controlled by the python's FLAM3H™ module.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.7.30</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.30) ###

- **Fix**: Added some parachutes if something goes wrong while loading the Palette data.
- **Fix**: Removed an error message in the descriptive parameter if something goes wrong when loading the Palette data and used a print() to console instead, its cleaner.
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.7.27</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.27) ###

- **Fix**: When activating the OUT options "Flame name inherit on Load" toggle, if the current FLAM3H™ iterations number was different from the one stored into the loaded IN Preset name it was not updating it.
- **Fix**: Improvements of the json palette presets loading into FLAM3H.
- **Fix**: Improvements of the palette conversion from hex to rgb on Flame Load.
- **Fix**: Suppressed a flash message about the Render properties being copied on Flame Load.
- **Fix**: Suppressed a window messsage in case of invalid hex values from a loaded Flame preset palette data.
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.7.22</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.22) ###

- **New**: Added the OUT tab option toggle: "Flame name inherit on Load". Cause the OUT Flame name parameter to automatically be set to the name of the loaded flame preset. It is OFF by default.
- **Fix**: Switching Flame files was triggering a message about the node user data updates if the new file loaded preset was the same name as the one currnetly loaded before switching.
- **Fix**: When a valid Flame file was already loaded, loading an invalid Flame file right after was triggering a message about the node user data updates.
- **Fix**: When resetting to the default Sierpiński triangle the OUT flame name's iteration number was not being updated.
- **Fix**: When the iterators count is set to 0(Zero) the OUT flame name's iteration number was not being updated.
- **Fix**: The IN tab option: "copy render properties on Load" is now ON by default.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.7.12</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.12) ###

#### FLAM3H™ ####

- **New**: Copy/paste of the Sensor and Render settings data now work also when a Flame preset has been loaded from the clipboard.
- **New**: In case of hand made modifications to the loaded XML Flame preset file, some of the FLAM3H™ UI toggles will now also force an updated of the IN Flame stats infos.
- **Fix**: Suppressed some flash messages firing on hip file load.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**

#### FLAM3HUSD v0.1.48 - Beta ####

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.7.07</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.07) ###

#### FLAM3H™ ####

- **Fix**: Reinforced context aware options and messages.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**

#### FLAM3HUSD v0.1.45 - Beta ####

- **Fix**: Reinforced context aware options and messages.
- **Fix**: New icons.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.7.04</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.04) ###

#### FLAM3H™ ####

- **Fix**: Better messages for contex aware functionalities.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**

#### FLAM3HUSD v0.1.40 - Beta ####

- **Fix**: This is now officially and internally marked as: Beta
- **Fix**: Less invasive on_create actions.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.7.01</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.01) ###

- **Fix**: Fixed a rare Xaos bug on Flame load introduced with the preview version: [**v1.7.00**](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.00) - It was sometime setting the first xaos value on the first iterator to '0'(Zero) when all Xaos values were supposed to be '1'(One).


<br>
<br>


### [<ins>From v1.7.00</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.7.00) ###

#### FLAM3H™ ####

- **New**: Xaos command string: typo checking, auto-corrections and undos. Retrieve from history can now retrieve single and multiple entries instead of the entire Xaos string for the selected iterator.
- **New**: Xaos command string: you can now type a single floating point value to fill all entries with it (before you could only type integers).
- **Updated HDA documentation.**

#### FLAM3HUSD v0.1.37</ins> ####

- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.6.97</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.97) ###

#### FLAM3H™ ####

- **Fix**: Post affine xform handle viz offset segment is now properly cast as: **polyline** instead of **poly**.
- **Fix**: Post affine xform handle viz offset segment is now properly positioned in the same plane as the main handle.
- **Fix**: First node instance was not cooking/compiling if no Sop viewers were present in the current desktop.
- **Fix**: Corrected some context checking and messages.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**

#### FLAM3HUSD v0.1.35 ####

- **New**: With Houdini versions higher than 19.0.x you can now import and render the xforms handles viz using Karma.
- **New**: Addded checking for the validity of the imported FLAM3H™ node.
- **Fix**: Reinforced viewers context checks.
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.6.91</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.91) ###

_This update is all about FLAM3HUSD._

#### FLAM3HUSD v0.1.25 ####

- **New**: Added validity check for the imported FLAM3H™ node.
- **New**: Added action button to reset the Widths parameter to its default value.
- **New**: Added action button to reset houdini GL viewport point size parameter to its default value.
- **New**: Added action button to reset FLAM3H™ shader parameters to their default values.
- **New**: Added action button to reset Karma pixel samples parameter to its default value.
- **New**: Added: **py_flam3usd_UI_PRM_map.md** mark down file to this repository.
- **Fix**: Improved USD hierarchy build.
- **Fix**: Improved UI and UX.
- **Fix**: FLAM3USD Corrected about box code python version used (always display the least needed).
- **Small fixes/improvements**


<br>
<br>


### [<ins>From v1.6.90</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.90) ###

#### FLAM3H™ ####

- **New**: Camera Sensor viz and xforms handles viz now check each available viewer's type before performing any operations. If any of the viewers is in **Lop** context it will be ignored.
- **Fix**: Xforms handles viz wire settings will now only affect viewers belonging to the **Sop** context. 
- **Fix**: Viewport preferences point type will now only affect viewers belonging to the **Sop** context. 
- **Fix**: Viewport preferences point size will now only affect viewers belonging to the **Sop** context. 
- **Fix**: Dark mode will now only affect viewers belonging to the **Sop** context. 


#### FLAM3HUSD v0.1.15 ####

- **Fix**: Python code has been structured the same as the big brother FLAM3H™ so to facilitate future updates.
- **Fix**: Viewport preferences point type will now only affect viewers belonging to the **Lop** context. 
- **Fix**: Viewport preferences point size will now only affect viewers belonging to the **Lop** context. 
- **Fix**: Dark mode will now only affect viewers belonging to the **Lop** context. 
- **Fix**: Set hydra renderer menu will now only set viewers belonging to the **Lop** context.
- **Fix**: FLAM3HUSD documentation ICON is now properly displayed.


<br>
<br>


### [<ins>From v1.6.84</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.84) ###

#### FLAM3H™ ####

- **New**: FLAM3H™ will now check if the user is in Solaris/LOP context or not prior to activate the Camera Sensor mode.
- **Fix**: Motion blur viz was not working. (a regression from preview version: v1.6.82)
- **Updated HDA documentation.**

#### FLAM3HUSD v0.1.0 ####

_This simple utility node got an upgrade._

- **New**: New import location from within the selected FLAM3H™ node. This will prevent the xform handles viz and the camera sensor bbox geometries to show up in Solaris/Lop.
- **New**: New materialX shader for Karma CPU. Simple and will allow to perform Gamma and HSV corrections on the fly.
- **Fix**: Revisited UI a little.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.82</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.82) ###

- **Fix**: _Motion Blur_ is now initialized directly within the main function making it ~30% faster to compute when active.


<br>
<br>


### [<ins>From v1.6.81</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.81) ###

- **Fix**: Enumerated presets menus now start to count from **1**.


<br>
<br>


### [<ins>From v1.6.80</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.80) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.6.78</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.78) ###

- **Fix**: New Dark mode method, it is more accurate and scale better to new modes like for example the DarkGrey mode introduced in H20.x. It now also print more targeted status bar messages.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.77</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.77) ###

- **Fix**: Missing variations text message lines now ends with a comma(**,**) unless it is the last line in the message which will end with a dot(**.**).
- **Fix**: Smaller compiled file size, almost 40kb saved.


<br>
<br>


### [<ins>From v1.6.76</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.76) ###

- **Fix**: Xoas.h had a missing return statement even tho it was still able to correctly return the proper idx but for the sake of correctness it has been fixed.
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.6.75</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.75) ###

- **Fix**: Output path check messages now understand if they run from the IN or the OUT tab. Before was always from the OUT tab.
- **Fix**: Loading a hip file with multiple FLAM3H™ nodes and a marked iterator was not recognizing the marked iterator as the other nodes init script was clearing out that data. It is now fixed.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.71</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.71) ###

- **New**: Viewport xforms handles VIZ geo is now pre-cooked every time a Flame preset is loaded.
- **New**: Density menu entries now have xforms handles VIZ indicators to signal which mode is ON.
- **Fix**: Fixed camera sensor toggle not being properly call when cloning a FLAM3H™ node. (_a regression from preview versions_)
- **Fix**: Corrected back-up "OUT_PATH" menu cache variable's name.
- **Fix**: OUT menu presets was not properly updating when saving a Flame out.
- **Fix**: Cloning a FLAM3H™ node with Zero iterators was erroring out in checking the opacities. It is now fixed.
- **Fix**: Fixed a rare case where the XML color correction curves can be an empty key.
- **Fix**: Tool responsiveness and first node instance creation time are a tiny bit better.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.65</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.65) ###

_This release is a tentative: **Final** as of **H20.5.x**:_

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.63</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.63) ###

- **New**: When the xforms handles VIZ mode is ON, the density presets menu entries will display a small red handle to indicate the density values the xforms handles VIZ mode will keep being active.
- **Fix**: When in xforms handles VIZ mode, if the density value is raised above 5M(_millions_) points, the related UI icons will be disabled as well.
- **Fix**: Updated xforms handles VIZ icons parameters tooltips.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.60</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.60) ###

- **Fix**: First node instance creation time is now twice as fast.
- **Fix**: The overall responsiveness of the tool while editing feel a bit faster.
- **Fix**: Fixed FLAM3H™ warning messages' node not being updated in the preview version/release.
- **Fix**: Viewport xforms handles VIZ are a bit faster.
- **Fix**: Viewport TAG is a bit faster.
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.6.50</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.50) ###

- **New**: ~**5%** faster (_All iterators,FF and parametrics variations parameters data are now pre-computed_).
- **New**: A new way of query parametric parameters values made the tool more responsive and a bit more interactive while editing.
- **New**: New viewport xforms handles VIZ implementation. It is now many times faster.
- **New**: Viewport xforms handles VIZ now turn dashed when an iterator(_or FF_) POST affine is activated.
- **New**: Viewport xforms handles VIZ now allow each iterator to be viz in SOLO mode (_only display the selected iterator's viewport handle_).
- **New**: Viewport xforms handles VIZ now allow the FF to be viz in SOLO mode (_only display the FF viewport handle_).
- **New**: Added the viewport' preferences tab option: **wire width** to control the curve thickness of the viewport xforms handles VIZ.
- **New**: When an iterator(_or FF_) POST affine is activated, an extra knot in the viewport handle VIZ is created to represent its post affine' pivot/offset.
- **New**: Viewport xforms handles VIZ will be visible up to a density value of 5M(millions) max and they will be hidden beyound that.
- **New**: When entering the viewport handles VIZ mode, FLAM3H™ will now store all viewport wire widths data and restore everything upon exiting the mode assuming no other FLAM3H™ node in the scene has the mode ON.
- **New**: Added the ability to copy/paste sections of an affine between PRE and POST affine and viceversa, for example only the **X** and **Y** or only the **O** or only the **Rot** value.
- **Fix**: The viewport xforms handle knot geometry had an overlapping primitive. it is now fixed.
- **Fix**: FLAM3H™ now handle some of the checks to a new one-off cvex node instead of querying the incoming FLAM3H™ point cloud.
- **Fix**: If more than 20 iterators are created while Xaos is active(_current limit with Xaos_), FLAM3H™ now won't generate any points.
- **Fix**: Loading a hip file with a FLAM3H™ node from a fresh houdini session was causing a python's **AttributeError** when attempting to reset to the default Sierpinski triangle. It is now fixed.
- **Fix**: Fixed viewport TAG not being able to read and display some data.
- **Fix**: Re-built viewport TAG using pre-stored data. It is now many times faster.
- **Fix**: Fixed FF variations: "BLOB" and "SUPERSHAPE" having their arguments in the wrong order inside: "flameff.h" file.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.10</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.10) ###

_This is the last update of 2024, after a very long time of development and unit test (**years**) it is now considered in good shape ;D_

- **New**: Global tab -> Density menu action button icon can now set also lower tier presets: 300k, 200k, 100k points.
- **Fix**: Compiled "cvex_TheFractalFlameAlgorithm.vex" file size is now ~14kb smaller.
- **Fix**: Fixed a very, very small difference in the MODULUS variation between FLAM3H™ and the official one.
- **Fix**: It can be slightly faster, depend on how the processed Flame is constructed. 
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.09</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.09) ###

- **New**: New SYS tab "viewport handles VIZ" icon.
- **Fix**: Improved a little the Global tab.
- **Fix**: When entering the Sensor viz mode, the viewport handles viz icon will now switch to a disabled empty star.


<br>
<br>


### [<ins>From v1.6.06</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.06) ###

- **New**: Added viewport handles VIZ icons to the SYS Utils' tab; Much more handy!
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.05</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.05) ###

- **Fix**: Some xforms handles compiled cvex files size are now smaller(~40% smaller).
- **Fix**: The xforms handles geo transformations are a bit faster.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.6.02</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.02) ###

- **Fix**: iterators viewport xforms handles geo transformations is now many, many times faster.


<br>
<br>


### [<ins>From v1.6.01</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.01) ###

- **Fix**: viewport xforms handles knots now have a non-uniform scale, indipendent from each other allowing for a better scale computation during shear/stretching.



<br>
<br>


### [<ins>From v1.6.00</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.6.00) ###

- **New**: Added the ability to preview the xforms handles in the viewport. You can toggle it ON or OFF in the preferences options under: general tab. These handles are not editable and serve only a VIZ purpose. They will be helpful to better grasp how the affine values (PRE and POST affine) are acting over each iterator/FF of the fractal Flame. They are meant to be a VIZ of manipulators as found in other fractal flame editors out there. (_it is a work in progress_)
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**

_Some of those small fixes/improvements include_:

- **Fix**: When an iterator Xaos string is invalid, the FLAM3H™ compile block node warning message was reporting the wrong iterator number. It is now fixed.
- **Fix**: When a negative value was left inside an iterator Xaos string, the FLAM3H™ compile block node warning message was reporting the wrong iterator number. It is now fixed.
- **Fix**: When there are ZERO iterators, the FLAM3H™ compile block node warning message will now properly state: ZERO iterator and not the iterator number 1 warning message like before.
- **Fix**: Corrected some python definition doc-strings. - (_an ongoing effort_).
- **Fix**: Improved and updated some parameter's tooltips. 


<br>
<br>


### [<ins>From v1.5.98</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.98) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.97</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.97) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.5.96</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.96) ###

- **New**: Added ArchViz High Quality palette libraries.
- **New**: Added Portraits High Quality palette library.
- **New**: Added MultiVibrant Super High Quality (1024 color keys) palette library.
- **New**: It is now possible to copy the selected palette preset name (if any) into the palette name string parameter field.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.95</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.95) ###

- **New**: Added 3(three) new High Quality palette libraries with one derived from Super Heros characters with 50s colors.
- **Small fixes/improvements as part of an ongoing polishing pass.**

_Some of those fixes/improvements include_:

- **Fix**: When the OUT "add iterations to Flame name" toggle is OFF, it will still auto-correct the Flame name if any.
- **Fix**: The Palette name parameter now run an auto-correction string to behave the same way as the OUT Flame name string parameter.
- **Fix**: Updated and corrected all python definitions doc-strings - (_an ongoing effort_).
- **Fix**: Updated and corrected all python definitions type-hints  - (_an ongoing effort_).


<br>
<br>


### [<ins>From v1.5.93</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.93) ###

- **New**: Added 2(two) new High Quality palette libraries.
- **Fix**: CP and IN tab presets file path data initialization has been updated.
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.5.90</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.90) ###

- **Fix**: Optimized density menu presets' bookmark icons (about half the file size) making the menu a bit faster to build when you click on it.
- **Fix**: Density presets menu's bookmark icons are now right aligned giving more sense of scale/progression while reinforcing the feeling of a boundary between the menu labels.
- **Fix**: When there are ZERO iterators, the density preset menu now only possess an empty icon without the three dots label (...) giving more a sense of being empty.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.88</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.88) ###

- **New**: New global tab layout and its new density menu workflow; much lighter and pleasant to the eyes and takes up less UI space. You can still set a custom density value from inside the preferences tab.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.85</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.85) ###

- **Fix**: Remap "pre_gaussian_blur" on Flame load is now fully automatic and its IN option's toggle has been removed.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.84</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.84) ###

- **New**: The density presets menu entries now have new bookmark icons to identify the different ranges.
- **Fix**: The CP palette lookup samples menu entries are now only from 256 to 1024 samples.
- **Fix**: Revisited the IN presets menu labels when there are ZERO ITERATORS.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.82</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.82) ###

- **Fix**: Fixed a not defined index variable that casued an error when resetting an iterator to its defaults (bug introduced in one of the preview versions).


<br>
<br>


### [<ins>From v1.5.81</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.81) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.80</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.80) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.78</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.78) ###

- **Fix**: improved copy/paste edge case handling. Now that case is being run once until it need to update again, having less impact on the UI performance.


<br>
<br>


### [<ins>From v1.5.77</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.77) ###

- **New**: Allow to reload an hip file with marked iterator or FF and pick up from there.
- **Fix**: Fixed a rare bug causing a wrong message in the copy/paste iterator mechanism.
- **Fix**: Fixed edge case so we don't have marked iterators in multiple FLAM3H™ node's "select iterator" mini-menus.


<br>
<br>


### [<ins>From v1.5.74</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.74) ###

- **Fix**: More Presets menus update/refresh sneaked into toggles and other places.
- **Fix**: Grouped many toggle resets and wrapped all of them into list comprehensions.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.72</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.72) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.70</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.70) ###

- **Fix**: Forced the Preset menus to be updated and refreshed from few other places, like for example inside the reframe Viewport SYS icon definition.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.68</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.68) ###

- **Fix**: Undos now work again. They work flawlessly in H20.5
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.66</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.66) ###

- **New**: The OUT Flame preset Palette 256+ option is now one and global inside the preferences tab. It will Enable/Disable this feature for the OUT Flame preset save option. Since this implementation has been crafted to be used in tandem with Fractorium, there are no reasons to toggle this option OFF as Fractorium can handle Flame presets with more than 256 color keys.
- **New**: When the preferences **palette 256+** toggle is ON(it is by default) the text **[256+]** at the end of the SYS tab will appear, and when OFF it will disappear.
- **New**: The CP palette is now always saved with its **palette 256+** option ON as there are no reasons to limit it for just the palette preset data.
- **New**: The CP options tab has been removed. The option **palette hsv** was not really needed for the CP palette save as the HSV values are saved along with the palette data and used on load if found.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.64</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.64) ###

- **Fix**: During a Flame preset load it will now checks against multiple color correction curves data defaults.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.62</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.62) ###

- **Updated/Corrected HDA documentation.**


<br>
<br>


### [<ins>From v1.5.60</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.60) ###

- **New**: From the OUT render color correction curves folder, you can now copy only the cc curves from the loaded IN Flame preset.
- **Fix**: The OUT color correction curves folder content is now properly setup internally for its default values and the folder name font won't be **bold** anymore when at default.
- **Fix**: The OUT color correction curves folder tip icon's parameters (Blue stars) now have proper labels that show up when the mouse is hovered over.
- **Fix**: When loading Flame presets in, FLAM3H™ now make better decisions about what palette lookup sample value to choose.
- **Fix**: The affine's Scale parameter ranges are now between 0.975 and 1.025 to allow for more precise and small value changes when modified using the slider.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.56</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.56) ###

- **Fix**: def get_ramp_keys_count(...) will now return a minimun of 128 color keys on save (before it could have been 64 but in some cases it was not enough)
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.55</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.55) ###

- **Fix**: When loading hip files with older version of FLAM3H™ their color correction curves values were nulls resulting in a black image when saving the Flame out and load it in Fractorium and others. It will now set them to their default values on load if needed.
- **Fix**: When saving out a palette with more than 256 color keys, will now always store the lookup sample value if greater than the number of the color keys, otherwise store the nearest lookup sample value that is greater than the number of color keys in the palette.
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.5.54</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.54) ###

- **Fix**: Only the color correction curves different from their default values will be listed inside the IN infos render properties.
- **Fix**: In infos CC detection was not using the preset_id index to compare color correction curves values.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.53c</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.53c) ###

- **Fix**: IN tab Infos now shows if a loaded Flame preset uses color correction curves values different from default. Below the Palette count info line the text: *CC* will appear if so.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.53b</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.53b) ###

- **Fix**: The OUT render color correction curves folder was missing an header's toggle to signal when a color correction was Active(ON) or at its default values(OFF).
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.53</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.53) ###

- **Fix**: When the IN option toggle "copy render properties on Load" was ON, it was not copying the data into the OUT render properties. It is now fixed.


<br>
<br>


### [<ins>From v1.5.52</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.52) ###

- **New**: FLAM3H™ can now handle Fractorium color correction curves when the flame preset you are loading have it. If not, default values (no color correction) will be used instead. When saving the flame out from FLAM3H, the stored color correction curves will be saved back into the flame preset file so that the original color correction done in Fractorium won't be lost anymore.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.50</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.50) ###

- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.45</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.45) ###

- **New**: Added menu label for when an IN flame from the clipboard is loaded but an invalid file path is being entered in the IN file path parameter.
- **New**: When activating the OUT option: palette 256+ toggle FLAM3H™ will let the user knows if the current palette posses enough colors and give some infos.
- **New**: When adding more than 256 color keys to the palette, if the OUT options toggle: palette 256+ is ON, FLAM3H™ will let the user know. Same when from more than 256 color keys we go back to 256 or less.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.42</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.42) ###

- **Updated HDA documentation.**: Added the use of badges to signal some parameters' types and their scope. It make easier and clear to spot what you are looking for and to gather a quick understanding of it at glance.
- **Updated HDA documentation.**: Added a Badges section to the documentation.


<br>
<br>


### [<ins>From v1.5.41</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.41) ###

- **Fix**: When loading a flame preset from the clipboard while a valid locked flame library was already loaded, deleting the file path string will leave the text: "-> LOCKED" inside the Flame stats. It will now be removed.
- **Fix**: When a flame preset from the clipboard is loaded, trying to load an invalid flame file would toggle the isValidPreset check OFF causing the clipboard flame stats to disappear. It is now fixed.



<br>
<br>


### [<ins>From v1.5.39</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.39) ###

- **New**: The palette action button is now multipurpose allowing you to also only remove and clear all keyframes/expressions if any are present in both the Palette and the HSV Palette.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.37</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.37) ###

- **Fix**: Loading Palette presets is now much, much faster.
- **Fix**: Splitted some large Palette lib files into smaller sets per file.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.35</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.35) ###

- **Fix**: Fixed a bug that prevented the HDA definition to being matched in H20.5, throwing an error and making impossible to edit, update and save the tool anylonger.


<br>
<br>


### [<ins>From v1.5.33</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.33) ###

- **New**: You can now copy only the Render Properties of a Flame preset from the Clipboard. This is being added because it is handy to tweak the render settings let say in Fractorium and just copy and paste them from the clipboard into FLAM3H™ without the need to load the copied Flame preset fully, but just to updated the Render Properties.
- **New**: Now you can create presets files with their LOCK state in the file name even if they do not exist yet on dirve and the LOCK will be active only after you save the first preset in it. (May that be from the CP or OUT tabs)
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.30b</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.30b) ###

- **Fix**: Removed os.path.getsize() and used os.path.exists() instead so not to cause more checks if the file exist or not.


<br>
<br>


### [<ins>From v1.5.30</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.30) ###

- **Fix**: Improved output paths checks for the CP and OUT tabs and their messaging system.
- **Fix**: Reduced the amount of messages print to the console.
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.5.26</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.26) ###

- **Fix**: Fixed wrangle cores: "Reload CVEX" button's tooltips.
- **Fix**: Fixed a missing backslash in the generation of the output paths from the CP and OUT tabs. (introduced in one of the preview updates)
- **Fix**: Fixed issues with loading invalid Palette or Flame files that causes FLAM3H™ to error our or even overwrite an invalid file without consent when Saving out a preset. (introduced in one of the preview updates)
- **Small fixes/improvements as part of an ongoing polishing pass.**


<br>
<br>


### [<ins>From v1.5.22</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.22) ###

- **New**: Created Markdown [readme file](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/blob/main/src/py/README.md) inside the src/py/ files.
- **New**: Created Markdown [readme file](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/blob/main/src/cvex/README.md) readme file inside the src/cvex/ files.
- **Fix**: A bit better data formatting on OUT Flame save for FLAM3 compatibility messages and warnings.


<br>
<br>


### [<ins>From v1.5.20</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.20) ###

- **Fix**: The main IN Load Flame preset definition: def in_to_flam3h(self) -> None: has been splitted into separate functions, each with its own purpose. Much cleaner and easier to move around and update in the future.
- **Fix**: Rewritten: def out_flam3_compatibility_check_and_msg(self) -> bool: for a better data formatting (long overdue) on OUT Flame save for FLAM3 compatibility messages and warnings.
- **Small fixes/improvements as part of an ongoing polishing pass.**

<br>
<br>


### [<ins>From v1.5.17</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.17) ###

- **Fix**: Loading a Flame preset with 0(Zero) iterators was causing an error. It is now fixed (_All Flames have at least 1(one) iterator but just in case_).
- **Fix**: Loading a Flame preset without any Palette data was causing an error. It is now fixed (_All Flames have a Palette XML data, but just in case_).


<br>
<br>


### [<ins>From v1.5.15</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.15) ###

- **New**: When in sensor mode and Zero iterators, the viewport sensor logo will switch to a blue version of itself to keep consistent with the logo displayed in the viewport.
- **New**: Added warning for when a valid xaos command string is missing in any of the available iterators (_it is a rare case and it will probably never happen from H20 up_).
- **Fix**: Since the all inactive iterators or all iterators Weights set to Zero cases are now being handled from inside the CVEX code, a new definition has been created (def iterator_vactive_and_update(self) -> None:) that simplify the process of checking and handling those cases.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.10</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.10) ###

- **New**: Added a "Special Thanks" section to the About Tab message.
- **New**: Added Fractorium bitbucket repository inside the About Tab's web links.
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.06</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.06) ###

- **Fix**: The CP and OUT tabs automated file parameters now should work also with network paths.


<br>
<br>


### [<ins>From v1.5.05</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.05) ###

- **New**: When loading hip files with FLAM3H™ nodes inside, it will now check their iterator's opacity and if any is 0(Zero) it will turn the Remove Invalid Point(RIP) toggle ON.
- **Fix**: The OUT tab sensor resolutions presets menu is now pre-built.
- **Fix**: Updated: [../src/py/py_flam3_UI_PRM_map.md](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/blob/main/src/py/py_flam3_UI_PRM_map.md)
- **Small fixes/improvements as part of an ongoing polishing pass.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.5.00b</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.00b) ###

- **Fix**: Fixed an error occurring when resetting the Sensor Viz properties while being in the Sensor Viz mode.


<br>
<br>


### [<ins>From v1.5.00</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.5.00) ###

- **New**: When entering the Sensor Viz mode, FLAM3H™ will now store all viewers data and restore them all on exit to their preview state.
- **New**: Added status bar messages when copy/paste affine values between pre and post affine within the same iterator and/or FF.
- **New**: The preferences xaos and viewport display menus now have a bookmark icon to mark the default option.
- **New**: Added new icon for the FF tab copy/paste FF data.
- **New**: Added new icon for the wrangle-core nodes: Reload CVEX button.
- **New**: Added new icon for the file nodes: Reload Geometry file button.
- **New**: Added new icon for the copy Flame preset render properties inside the IN and OUT tabs.
- **New**: The file: [../src/py/py_flam3_UI_PRM_map.md](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/blob/main/src/py/py_flam3_UI_PRM_map.md) has been converted into a native GitHub markdown file. Nicer to update and review in **GitHub**, **VSCode** and similar.
- **New**: The file: [../icons/README.md](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/tree/main/icons#readme) has been created as a native GitHub markdown file for easy review and find. Nicer to update and review in **GitHub**, **VSCode** and similar.
- **Fix**: Loading a palette preset whitout a valid F3H plaette json file already loaded causes the palette to revert to its default colors. It is now fixed (a regression from one of the preview updates).
- **Fix**: The SYS tab icon reframe viewport will now reframe all available viewers, and not only the current one.
- **Fix**: Fixed an annoying but harmless error status bar message about the sensor bbox node path not being found on creation.
- **Fix**: Updated all python classes doc-strings definitions lists.
- **Fix**: The preferences tab is now a collapsible folder, so the toggle 'display prefs' has been removed as it is no longer needed. Much more elegant now.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.95</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.95) ###

- **New**: Added an affine Scale parameter to the PRE and POST affine tabs for iterator and FF (FLAME and FF tabs). This was long overdue.
- **Fix**: When entering the Sensor Viz mode, FLAM3H™ will now check if at least one Viewport is available and if there is more than one, it will handle them all (to be continued...).
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.94</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.94) ###

- **New**: When typing an invalid file path inside the CP, IN or OUT presets file parameter, the menu labels will say so.
- **New**: When an existing directory path is present inside the CP or OUT presets file parameter but the file do not exist yet, the menu labels will say so.
- **Fix**: All the presets menus are now forced to be rebuilt here and there to keep them up to date without over-loading them during their generation. As an example, when you load a preset (CP or IN) they will be forced to be rebuilt. When you type in or update the loaded file strings, they will be forced to be rebuilt and from few other places as to make the process transparent and efficient. This make it possible to have the menus pickup manually hand made changes by the user to the already loaded files.
- **Fix**: It happened that over time a loaded valid file became an invalid file path (for some mysterious reasons) so I enforced a file check in all presets menus to force a data re-cache if the loaded file become invalid.
- **Fix**: Improved build of all menus presets.
- **Fix**: When resetting to the default Sierpinski triangle, the SYS tab select iterator mini-menu was not updating. It is now fixed.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.88</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.88) ###

- **New**: When there are 0(Zero) iterators, clicking the IN tab load Flame preset icon will now change the focus to the IN tab if not already.
- **Fix**: When a Flame preset only had F3H affine style in the post affine, the reload Flame with F3H affine style toggle inside the IN tab was not working. It is now fixed.
- **Fix**: When a Flame preset only had F3H affine style in the FF(finalXform), the reload Flame with F3H affine style toggle inside the IN tab was not working. It is now fixed.
- **Fix**: Fixed a rare bug that caused Houdini to crash when all active iterator's Weights were set to 0(Zero) after an undo action.


<br>
<br>


### [<ins>From v1.4.84</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.84) ###

- **Fix**: Faster menus build when prefs tab "iterator menus bookmark icons" toggle is ON.
- **Fix**: Palette ramp parameter now delete its parameter's keyframes when reset or when loading a new palette or flame preset.


<br>
<br>


### [<ins>From v1.4.80</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.80) ###

- **New**: Added a preferences tab section for the UI options.
- **Fix**: Fixed prefs UI tab staying visible when display prefs was toggled OFF.
- **Fix**: prefs viewport point size parameter now delete its parameter's keyframes when reset.
- **Fix**: Updated menu_copypaste_FF method.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.77</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.77) ###

- **Fix**: Added undos support to the SYS tab Select Iterator mini-menu.
- **Fix**: Improved copy/paste iterator menu build.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.75</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.75) ###

_This update focus is mainly to improve the UI performance_:

- **New**: The iterator's variation menus are now without dynamic bookmark icons as default and pre built. You can still activate the dynamic bookmark icons in the preference's tab if you desire.
- **New**: When loading a Flame from the clipboard while a valid flame file was already loaded, the selected menu label will now be prefixed with: [CLIPBOARD]
- **Fix**: When using the iterator bookmark icons, it is now a bit faster as it is using a pre built menu static data to start with.
- **Fix**: Faster build of the CP presets menus.
- **Fix**: Faster build of the IN presets menus.
- **Fix**: Faster build of the OUT preset menu.
- **Fix**: Faster build of the Select Iterator mini-menu.
- **Fix**: Faster build of the density presets menu.
- **Fix**: Global density presets now delete its parameter's keyframes when is set from a menu preset or from a reset.
- **Fix**: CP HSV parameter now delete its parameter's keyframes when reset.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.65c</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.65c) ###

- **Fix**: Fixed palette HSV not being updated on Flame load if the loaded json preset posses the HSV values different from defaults.
- **Fix**: Removed some duplicate definitions calls to palette_cp(), probably some left over from preview versions.


<br>
<br>


### [<ins>From v1.4.65b</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.65b) ###

_Updated py_flam3 version number_:

- **New**: Added the ability to SAVE Flame presets using F3H affine style format (uses the Rotation angle parameter without transforming the affine by it first).
- **New**: Added the ability to LOAD Flame presets using F3H affine style format (uses the Rotation angle parameter without transforming the affine by it first).
- **New**: F3H affine style export only when the Rotation parameter is different from Zero.
- **New**: Added flash message with the updated Flame name when switching the OUT tab's option "auto add iter num to Flame name" toggle ON or OFF.
- **New**: Added xform values validity check and corrections on Flame load to possibly avoid errors.
- **New**: Post affine are now being exported only when they are different from their ident values or the Rot angle is different from Zero.
- **New**: When an iterator is Disabled or Zero weight and it is marked for being copied, the copy/paste mini menu section's bookmark icons are now more transparent.
- **New**: When the FF is Disabled and it is marked for being copied, the FF copy/paste mini menu section's bookmark icons are now more transparent.
- **New**: When an iterator shader's opacity is 0(Zero), the SYS iterator selection mini-menu labels will have a: [ZERO opacity] text added after the menu label number/count.
- **Fix**: If something goes wrong while loading a CP palette preset it will now set only one RED color key and not error out anymore.
- **Fix**: If something goes wrong while loading a CP palette preset it will fire a proper error message.
- **Fix**: smaller bug fixes.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.48</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.48) ###

- **Fix**: When deleting a FLAM3H™ node with its FF marked for being copied, it willl now clear that data and ask to mark the FF again instead of warning you about the node being deleted.
- **Fix**: When deleting a FLAM3H™ node with its FF marked for being copied, it will now print to the status bar and fire a flash message as well.
- **Fix**: Wrong tooltip for the youtube video tutorial web link.
- **Fix**: improved the open web browser mechanism.


<br>
<br>


### [<ins>From v1.4.44</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.44) ###

- **New**: Added new bookmark icon for the copy/paste delete case info message.
- **New**: Added Youtube video tutorials web link button to the about tab.
- **New**: Added new high tier menu entrie icon.
- **Fix**: Revisited some tooltips inside the About tab web links section.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.38</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.38) ###

- **Fix**: When selecting an iterator using the SYS tab Select Iterator mini-menu, if it was a floating pane was erroring out.
- **Fix**: When selecting an iterator using the SYS tab Select Iterator mini-menu, if it was a Network Editor's Parameter Dialog was erroring out.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.35</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.35) ###

- **New**: The IN Preset render properties can now be copied also in sections: SENSOR and RENDER.
- **Fix**: Fixed a rare bug due to loading a Flame preset with Zero weights iterators, causing Houdini to crash.
- **Fix**: Revisited some status bar messages priority.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.31</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.31) ###

- **Updated HDA documentation and About tab -> web links section.**


<br>
<br>


### [<ins>From v1.4.30</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.30) ###

_More small things:_

- **Fix**: When selecting an iterator from the mini-menu Select Iterator parameter, the flash message will now include also if the selected iterator to focus on is Marked for being copied.
- **Fix**: When the CP, IN and OUT files are empty or invalid the menu bookmark icon will now be more transparent to signal the absence of data, much more elegant.
- **Fix**: More readable flash messages when an iterator is Marked for being copied.
- **Fix**: When loading a Flame from the clipboard, the confirmation status bar message was not removing the iterations number baked into the preset name. It is now fixed.
- **Fix**: 
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.23</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.23) ###

- **Fix**: When marking an iterator for being copied, that data was destroyed once the user created a new FLAM3H™ node right after. It is now fixed.
- **Fix**: Updated def flam3h_paste_reset_hou_session_data(self) -> None:
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.15</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.15) ###

- **Fix**: Added OUT_PALETTE_256_PLUS to: def reset_OUT_options(self) -> None:
- **Fix**: OUT_USE_FRACTORIUM_PRM_NAMES now default to: 1
- **Fix**: Fixed some mixed up messages inside: def reset_CP(self, mode=0) -> None:
- **Fix**: Fixed a status bar message after loading a Flame preset.
- **Fix**: When copy/paste the main section it will not copy the ON/OFF(Enable/Disable) iterator parameter anymore.
- **Fix**: The default value for the OUT tab option's parameter: "use Fractorium parametric prm names" is now ON(Active).
- **Fix**: Removed quotes from the IN tab options parameter's name: "remap 'pre_gaussian_blur'"
- **Fix**: When selecting the focus of an iterator through the SYS mini-menu "Select iterator" the flash message will now print also if it is Disabled.
- **Fix**: Improved some parameter's tooltips.
- **Fix**: Cleaned and improved palette plus([256+]) messages python definition.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.05b</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.05b) ###

- **Fix**: Updated documentation with the correct and new bookmark icon when a variation's weight is set to 0.0 ( ZERO ).


<br>
<br>


### [<ins>From v1.4.05</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.05) ###

- **New**: New bookmark icon for non active variations.
- **Fix**: When loading a Flame, the Descriptive parameter will now display the Flame name without the iterations number baked into its name string.
- **Fix**: When loading a Flame, the Status bar message will now print the Flame name without the iterations number baked into its name string.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.4.01</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.01) ###

- **Fix**: When copy the OUT preset flame name it will now print the copied name with a flash message or give a warning message in the status bar otherwise.


### [<ins>From v1.4.00</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.4.00) ###

- **New**: The OUT file contents action script button is now a multi-purpose button.
- **New**: You can now copy an existing preset Flame name from the selected OUT file into the Flame name string field. 
- **Fix**: OUT tab option "auto add iter num to Flame name" will remove the iter num from the Flame name when toggled OFF.
- **Fix**: FLAM3H™ node is now created with the "xaos div" preferences option set to: ON.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.96</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.96) ###

- **Fix**: When the IN tab's "force iterations on load" toggle was ON, changing the iterations number was not updating the IN tab "iterations on Load" value. It is now fixed.
- **Fix**: Flame preset info "Name" is now just below the "Software" info without an extra empty line as spacer.
- **Fix**: Changed the IN tab's IN infos -> "flame lib file: LOCKED" string to just: "-> LOCKED"
- **Fix**: Fixed an empty extra space inside the generated XML plugin key on Save caused by the way the "pre_blur" variation name was added to the processed list.
- **Fix**: Fixed some wrong python type hints.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.90</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.90) ###

- **New**: The CP Palette, IN Flame and OUT Flame preset's menus entries can now be enumerated. It's handy and easier to remember a preset you liked while trying out others.
- **New**: Added a preference's option to turn the presets menus enumeration ON/OFF.
- **New**: Added the option to override the iterations number coming from the Flame preset name.
- **Fix**: Updated list of definition's declarations inside each class's doc string for easy find and search.
- **Fix**: Changing the IN prefs -> "iterations on Load" value was not updating the OUT Flame preset name if any. It is now fixed.
- **Fix**: When turning ON the "force iterations on Load" toggle the OUT Flame preset name if any was not updating. It is now fixed. 
- **Fix**: Fixed issue to undo a copy/paste iterator's section action in H20.5.
- **Fix**: Fixed issue to undo a copy/paste FF's section action in H20.5.
- **Fix**: When truning ON the "auto add iter num to Flame name" toggle the OUT Flame preset name if any was not updating. It is now fixed. 
- **Fix**: Fixed a typo error in the onDeleted python script.
- **Fix**: Fixed few typos in some parameter's tooltip doc string.
- **Fix**: Improved some parameter's tooltips.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.77</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.77) ###

- **New**: added a new camera sensor's screenshot examples for the app Fractorium to the documentation.
- **Fix**: improved some parameter's tool tips.
- **Fix**: corrected some python classes @property declaration's names and usage.
- **Fix**: a marked iterator in one of the FLAM3H™ nodes caused an error in the mini-menu Select iterator parameter when reloading the same hip file from a fresh Houdini session. It is fixed now.
- **Fix**: the mini-menu Select Iterator parameter was not able to catch up after multiple undos of marked iterators. It is now fixed.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.70</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.70) ###

- **New**: You can now save and load Flames with more than 256 palette colors. An option to enable saving with this spec has been added to the OUT: Options tab.
- **New**: You can now save and load Palette with more than 256 palette colors. An option to enable saving with this spec has been added to the CP: Options tab.
- **New**: When you are adding more than 256 colors keys to the palette either by editing it or by loading a Flame or Palette preset with that many colors, a message in the CP tab UI will show up as: "[256+]"
- **New**: Added info flash message when changing iterator number focus through the SYS tab mini-menu: Select iterator.
- **Fix**: Loading a Palette preset will now automatically set the palette lookup samples to use for if the color kesy are more than 256.
- **Fix**: Kept only the python module: lxml elementTree.
- **Fix**: The IN render preset infos are now split into: CAMERA SENSOR and RENDER SEITTINGS infos to match what's inside the OUT tab Render Properties options.
- **Fix**: fixed few more typos.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.62</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.62) ###

- **Fix**: XML key -> "Color Speed" is now always exported on save.
- **Fix**: CP Palette lookup sample menu's "256" entry has now a bookmark icon to identify it as the default value that should be used.
- **Fix**: Turned for loops into proper list comprehension form inside: def paste_from_list(...) and def paste_from_list_affine(...)
- **Fix**: The "flam3 compatibility" toggle inside the Preferences Tab is now hidded and only the one inside the SYS Tab has been kept.
- **Fix**: PRE and POST variation type menu's bookmark icon now use the same icon as the pre_blur to symbolize their type.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.56</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.56) ###

- **Fix**: Toggle parameter references are now properly rewired as they got erased in the preview version.


<br>
<br>


### [<ins>From v1.3.54</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.54) ###

- **Fix**: Fixed the iterator disabled tooltip.


<br>
<br>


### [<ins>From v1.3.53</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.53) ###

- **New**: When loading a Flame with more variations number than allowed it will now print the one that are in excess and skipped from being loaded.
- **Fix**: Fixed the active iterator and FF buttons sliding one slot when clicked, introduced in the preview version.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.50</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.50) ###

- **New**: Added a button in each affine's tab to copy and paste from/to the pre or post affine values in the same iterator.
- **New**: Added a button in each FF affine's tab to copy and paste from/to the FF pre or FF post affine values.
- **Fix**: Updated the about box FLAM3H™ website's icon to match the one used in the website homepage.
- **Fix**: The iterator active buttons have been swapped with a geometry data prm's action button to save one parameter.
- **Fix**: Fixed a few typo in some of the UI folder names.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.45</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.45) ###

- **Fix**: When using the mini-menu in the SYS tab to quickly change focus to a desired iterator multi-parameter tab number, it will now bring you back to the FLAME Tab if the focus were somewhere else.
- **Fix**: version number in the HDA about tab is now correct.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.44</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.44) ###

- **New**: Added a mini-menu in the SYS tab to quickly change focus to a desired multi-parameter tab number.
- **New**: the SYS Tag size menu is now turned into a mini-menu to save a bit of space.
- **Fix**: When "use iter on Load" value is greater than the global iteration value it wont force a re-cook when switched ON.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.40</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.40) ###

- **New**: Added reset action script button the the preferences tab viewport particle size parameter.
- **New**: Flash messages are now printed into multiple network editors instead of only inside the main one.
- **Fix**: The about FLAM3H™ tab is now set to be initially open instead of closed/collapsed.
- **Python code cleanup.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.37</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.37) ###

- **New**: Added option inside the CP tab to keep the HSV values untouched after loading a palette preset.
- **Fix**: When saving a Flame out with "use Fractorium paramtetric prm names" option ON the exported ColorSpeed value was wrong resulting in different colors when loaded inside Fractorium. It is now fixed.
- **Python code cleanup.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.35</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.35) ###

- **Fix**: When in camera sensor mode, the camera cull option will now be turned off.
- **Fix**: When loading a flame file without the expected root tag, it would not show the proper Flame name in the IN menu presets label list. It is now fixed.
- **Python code cleanup.**


<br>
<br>


### [<ins>From v1.3.33</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.33) ###

- **New**: Camera sensor icons now changes when the update sensor option is either ON or OFF. It change in the UI and in the viewport too.
- **New**: Added higher tier bookmark icon to the CP lookup samples menu entries.
- **New**: Added the option to reset an iterator to its default values.
- **New**: Added the option to reset an FF iterator to its default values.
- **New**: New FF iterator disabled icon.
- **Fix**: When using the IN remap pre_gaussian_blur action button while a flame preset from the clipboard was already loaded, the status bar msg was printing alos the bookmark icon path. it is now fixed.
- **Fix**: When loading a json file that is not a FLAM3H™ valid palette file, it will now prevent you to save a palette so to not override its content
- **Fix**: When create a new palette file, saving a palette was not updating the menu entries, it is now fixed.
- **Fix**: Cleaned up CP tab.
- **Python code cleanup.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.20</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.20) ###

- **New**: All of the variations that Fractorium lacks will now be classified as: "Unknown" during Flame load and listed inside the Flame preset's stats/info tab. Note that this will scan the Flame XML key's "plugins" and not through the available xforms.
- **New**: Added info icon to the IN Tab -> IN Info folder's header. (purely cosmetic)
- **Fix**: When loading a flame or a palette file and then saving the hip file somewhere else, Houdini would add the $HIP variable at the beginning of the filepath, causing the same file path to become invalid and throwing an error. It is now fixed.
- **Fix**: Fixed a case where the flame's plugins key could be populated with an empty var name string resulting in an error during flame's load.
- **Fix**: Moved variable cast PFF (GEM.PFF) inside the FF section where it belong inside: "TheFractalFlameAlgorithm.vfl" .
- **Fix**: Improved all the reset's pre_affine methods as they now use dictionaries instead.
- **Fix**: Fixed IN Tab render properties folder's heading typo.
- **Fix**: Variation name "linear3d" is now automatically re-mapped into "linear".
- **Python code cleanup.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.3.07 (last Studio commenrcial license available)</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.3.07) ###

- **New**: Sensor bbox node is now compiled as a native CVEX node.
- **New**: About Tab folders title headers now have an icon to start with (purely cosmetic).
- **New**: When no flame file is loaded and we load a flame from the clipboard, the menu labe will now say: "Clipboard".
- **New**: New IN preset menu label bookmark icon when a flame from the clipboard is loaded.
- **New**: New SYS HDA documentation icon. It now uses the blue star as it stand for: "help/informations/tips".
- **New**: Added the blue star icon to the copy/paste info menu label messages as it stand for: "help/informations/tips".
- **New**: New parameter's option icon.
- **New**: New parameter's kwargs options icon.
- **New**: New Pre_blur bookmark icon when its value is above 0.
- **New**: New Pre_blur bookmark icon when its value is above 1.
- **New**: You can now paste the entire iterator also from the copy/paste mini menu, CTRL+LMB on the icon is also still available.
- **New**: You can now paste the entire FF also from the copy/paste mini menu, CTRL+LMB on the icon is also still available.
- **Fix**: Loading an invalid flame file from the SHIFT + LMB file dialog while a valid flame file was already loaded caused to invalidate it. It is now fixed.
- **Fix**: Updated Iterator's active icon. It has a nicer contrast now.
- **Fix**: Fixed a bug that prevented loading flames from the clipboard if a valid flame file wasnt loaded already. (introduced in some of the preview updates)
- **Fix**: The TFFAsensor CVEX node is now independent and do not need a transform node anymore to complete the sensor orientation.
- **Fix**: The reframe viewport bounding box is now compiled as a native CVEX node.
- **Fix**: When creating a new FLAM3H™ node while something else has the displayflag ON, it wont send a load default message to the flash message anymore.
- **Fix**: Instead of importing the whole Numpy module, FLAM3H™ is now importing only the needed methods.
- **Fix**: Better copy/paste menu labels messages format.
- **Fix**: Improved action buttons tooltips.
- **Fix**: Improved sensor's bbox build method.
- **Fix**: Default palette ramps values are now embedded into their own Class's @staticmethods.
- **Fix**: Copy/paste the same iterator/FF section after an Undo was not working. It is now fixed.
- **Fix**: The SYS IN presets menu parameter was trying to load a flame preset when selecting the "Empty" menu label. It is now fixed.
- **Fix**: All the copy/paste menu label's messages now ends their sentences with a dot(".").
- **Fix**: Improved flash messages on flame save.
- **Fix**: Missing FF PRE variations were searched and compared against the POST dictionary instead of the PRE dictionary. It is now fixed.
- **Fix**: Revisited some general messages and its frequency.
- **Fix**: More targeted messages on flame load when not a valid flame file or preset.
- **Fix**: Check for Chaotica flame presets on flame load (from SHIFT + LMB file dialog as well ) and on load from the clipboard too.
- **Python code cleanup.**
- **Updated HDA documentation.**

### FLAM3H™ USD</ins> ###
- **New**: The HDA node has a new icon that make more sense and in line with the FLAM3H™ HDA icons library.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.2.75</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.2.75) ###

- **New**: Camera sensor infos are now turned into their own CVEX native node, much cleaner.
- **New**: Camera sensor TAG logos transformations are now turned into their own CVEX native nodes. 
- **New**: A new and very small class: _xml() has been added dedicated to compute menu entries for the IN presets menu parameters quicker.
- **New**: New FF Enabled state icon.
- **New**: The density mini menu entrie labels from 500k to 1 Billion now have a red star bookmark icon to signal the higher band of those values. 
- **Fix**: FF variation disabled state bookmark icon now matches the one used inside the iterator's variations as it is more readable.
- **Fix**: The IN and SYS Tab menus IN presets parameters are now a bit more lightweight to compute and populate based on the loaded XML file.
- **Fix**: The CP and SYS Tab menus CP presets parameters are now a bit more lightweight to compute and populate based on the loaded JSON file.
- **Fix**: The CP Tab is now at its default values since the start.
- **Fix**: When in camera sensor viz mode the RIP option will now be disabled as it is not needed and wont affect anything turning it ON or OFF.
- **Fix**: the flame private definition __get_name() in class: _xml_tree() is now a public def: get_name() and run directly from its parent class: _xml_tree()
- **Fix**: FF pre and post Affine X,Y not being reset on SHIFT + LMB. It is now fixed.
- **Fix**: Auto set xaos now use a SET and GET definition for each of its different data types, making it a little faster.
- **Fix**: Added better tooltips to some of the parameters that were left out from preview revisions.
- **Fix**: When in ZERO iterator count mode, the SYS Diabled star icon is more transparent, making it look more cleaner.
- **Improved Python code.**
- **Updated HDA documentation.**

### FLAM3H™ USD</ins> ###
- **Fix**: improved a the python code of this basic HDA for quickly rendering FLAM3H™ Flames in Solaris.


<br>
<br>


### [<ins>From v1.2.60</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.2.60) ###

- **New**: Added check for chaotica XML style files, wich are not supported but now it wont error out if the user try to load them anyway.
- **New**: Added few more flash messages for IN/OUT flame actions and few others.
- **New**: Added RIP option to the viewport TAG.
- **New**: New iterator's active icon.
- **New**: New pre_blur's bookmark icon.
- **New**: New Reframe viewport flame icons.


<br>
<br>


### [<ins>From v1.2.55</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.2.55) ###

- **New**: Added flash messages. Those are really nice, especially when marking/unmarking iterators or FF for being copied. You can disable them from the preferences tab otions.
- **New**: New IN and OUT menu presets bookmark icons.
- **Fix**: Fixed bookmark icon for the CP menu label selected Palette preset when not loaded.
- **Fix**: Fixed bookmark icon for the IN menu label selected Flame preset when not loaded.
- **Fix**: Python Tag Icons path gloabal variable for the IN Flame loaded preset is now pointing to the correct one.
- **Fix**: IN copy render properties icon when a flame has been loaded from the clipboard is now pointing to the correct one.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.2.50</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.2.50) ###

- **New**: The selected variation name in each of their menu parameter now posses a bookmark icon next to its label to display its state based on its weight.
- **New**: The IN presets menu parameter now posses a bookmark icon next to the currently selected flame preset label. The bookmark icon will change once the flame preset is being loaded.
- **New**: The CP presets menu parameter now posses a bookmark icon next to the currently selected palette preset label. The bookmark icon will change once the palette preset is being loaded.
- **New**: The iterator and FF copy/paste mini menu labels now have an icon.
- **New**: When copy/paste iterator or FF data between different FLAM3H™ nodes the menu labels now show the source FLAM3H™ node parent name.
- **New**: Added a visual feedback to recognize if the user made any modification to the currently loaded palette preset and if so the bookmark icon will change.
- **New**: The SYS CP preset icon and the CP Tab preset icon are now multipurpose and change their icon based on their state.
- **Fix**: When loading a hip file with a FLAM3H™ node in Camera Sesnor mode and its display flag ON, it will restore the proper Camera Sensor viewport on load. However seem to silently fail on Houdini versions prior to H20.0.590.
- **Fix**: When loading a palette preset from the clipboard, the SYS CP menu presets was reverting back to a value of 0 instead of keeping the last loaded preset index. It is fixed now.
- **Fix**: When in camera sensor mode, clicking frame sensor view SYS tab icon was not properly restoring the front viewport type if needed. It is fixed now.
- **Fix**: Fixed SYS CP menu preset OFF state not being updated on hip file load.
- **Fix**: When cloning a FLAM3H™ node with Camera Sensor mode ON, the new node will now be created with the mode OFF.
- **Fix**: Improved CP palette preset name string checking.
- **Fix**: Improved some tooltip and better formatted their text.
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.2.37</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.2.37) ###

- **New**: New palette lookup method. When using up to 256 color palette keys it is many times faster in sampling it.
- **New**: Added F3C toggle option to the SYS tab.
- **New**: Added a palette lookup samples parameter to sample the palette using different sample's count. The default for a typical fractal flame is always 256.
- **New**: Added palette lookup samples XML key to the python XML code so that it get saved with the flame preset and loaded back.
- **New**: New HDA documentation banner image.
- **Fix**: Fixed a regression that made appending new palette presets to the same file not working.
- **Fix**: Fixed filepath variables not being expanded when loading a flame or palette file from the SHIFT + Click dialog window resulting in a silent failed load.
- **Fix**: SYS Tab RIP option has a new icon for its enable state.
- **Fix**: When Motion Blur was ON, the alpha value could have exeeded the value of 1. It is now clamped.
- **Fix**: IN Flame preset stats info: "Variation used" are now capitalized.
- **Fix**: IN Flame preset stats info: "Missing variations" are now capitalized.
- **Fix**: Improved SYS tab icons tooltips.
- **Fix**: Small cosmetic touches here and there.
- **Improved Python code.**
- **Updated HDA documentation.**


<br>
<br>


### [<ins>From v1.2.25</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.2.25) ###

- **New**: New UX multipurpose icons ( best with a 4k display and the Houdini's Global UI scale set to: 1.75 or higher ).
- **New**: You can now SHIFT + LMB to the SYS IN_LOAD Flame icon to open a file dialog to choose a flame file to load.
- **New**: You can now SHIFT + LMB to the SYS CP_LOAD Palette icon to open a file dialog to choose a palette json file to load.
- **New**: You can now copy/paste a color palette into and from the clipboard.
- **New**: Iterator's active toggle is now a multipurpose icon.
- **New**: FF's has now a multipurpose icon for the active toggle.
- **New**: When in camera sensor mode the SYS camera framing icon is now using the sensor framing data.
- **New**: Under H20, the preference's Dark toggle option can now recognize the new background theme color: DarkGrey.
- **New**: New SYS Doc icon.
- **Fix**: The OUT SYS menu preset is now updated accordinlgy with the OUT menu preset.
- **Fix**: The IN SYS menu presets are now updated accordingly with the IN menu presets.
- **Fix**: When the sum of the color palette's HSV values was equal to 3 was considerade a default value even tho it could have been: { 0.9, 1.0, 1.1 } . This is now fixed.
- **Fix**: Preference's option CVEX precision has been hidden as the 64bit cvex mode is slow and almost never needed.
- **Fix**: About plugins variation's names are now capitalized and grouped by each 5, with a comma added at then of each line for correctness.
- **Improved Python code.**
- **Updated HDA documentation.** 


<br>
<br>


### [<ins>From v1.1.90</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.1.90) ###

- **New**: In load option "remap pre_gaussian_blur" now has a multi-functional action button to automatically set its toggle and reload the flame preset.
- **New**: In load option "remap pre_gaussian_blur" now capable to function also when re-loading a flame from the clipboard.
- **New**: In load option "copy render properties on Load" now has an action button to automatically set its toggle and reload the flame preset.
- **New**: Added SYS Tab icon to re-frame your viewport to a close to zero world frame of your flame. This is being added because it occasionally happens that the camera viewport frames the current Flame really small due to some of its points ending up being really far away from the zero world position.
- **Fix**: FF pre_gaussin_blur variation was not being properly loaded from a flame file, it is fixed now.
- **Fix**: FinalXform XML key "name" is now properly written as first to match the iterator's key order.
- **Fix**: Menu copy paste entries now omit the prefix "iter" to make it cleaner to read.
- **Fix**: Flame render properties "Size" is now renamed to "Resolution".
- **Improved Python code.**
- **Updated HDA documentation.** 


<br>
<br>


### [<ins>From v1.1.80</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.1.80) ###

- **New**: The viewport TAG infos now display if a flame is using the preference's option flam3 compatibility (F3C) toggle.
- **New**: If a negative value or a non digit character is left inside the xaos string ( ex: after an Undo action ), FLAM3H™ will rise appropriate warnings.
- **Fix**: All the FLAM3H™ custom UI parameter's data is now properly grouped into their own preference's tab folder.
- **Fix**: Negative xaos values are not allowed anymore. If a negative xaos value is entered, FLAM3H™ will reset it to a value of 1.0.
- **Fix**: the viewport TAG infos now use the incoming SYS array attribute to determine the active FLAM3H™ options.
- **Improved Python code.**: Camera sensor viz mode methods and its boundig box data now rely only on the data node name.
- **Improved Python code.**: Python type hints and its houdini node class types are now properly casted.
- **Improved Python code.**: numpy arrays are now directly converted into lists. 
- **Updated HDA documentation.** 


<br>
<br>


### [<ins>From v1.1.70</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.1.70) ###

- **New**: When entering the Camera Sensor viz mode, FLAM3H™ will now guarantee there will only be one Camera sensor viz mode active at any given time. This is to prevent concurrent stashed cameras to be restored and saved at the same time causing a jump in the current viewport.
- **Fix**: All the Houdini's status bar message are now execute if the Houdini's UI is available.
- **Fix**: All the display message windows are now displayed if the Houdini's UI is available.
- **Fix**: Removed tkinter import module and used legacy hou.ui module clipboard methods instead.
- **Fix**: Reset OUT render properties button now reset the quality parameter properly on SHIFT + LMB.
- **Fix**: Better tooltips text formatting where is possible. ( Action Button tooltips do not support formatting style chars )
- **Improved Python code.**: for 32bit or 64bit mode checks and other small improvements.
- **Updated HDA documentation.** 


<br>
<br>


### [<ins>From v1.1.62</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.1.62) ###

- **New**: Added an OUT save option to save a flame using variation parameter's names that Fractorium uses. This is only useful if you use Mobius or Oscilloscope ( oscope ) parametric variations and want to load the flame inside Fractorium as it uses diferent paramtric paramter's names for these.
- **New**: Added Sensor viz update toggle. ON by default. Every change to the sensor parameters will update the sensor viewport viz. Turn this OFF to disable any sensor viewport's updates.
- **Fix**: Copy/save a flame to the clipboard is now omitting the "flames" root tag. This now make it possible to paste the flame also inside Chaotica. Fractorium and Apophysis were just fine before but to conform more with the rest.
- **Fix**: When loading the default Sierpinsky triangle preset, if a valid palette json file was already loaded and it was a locked file lib the palette msg will not clear anylonger.
- **Fix**: When loading a flame from the clipboard, the status bar message will now print the correct flame preset name.
- **Fix**: Parameter's menu presets now uses their own python method instead of one for all. This should help a tiny bit in speeding up the UI.
- **Updated HDA documentation.** 


<br>
<br>


### [<ins>From v1.1.55</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.1.55) ###

- **New**: Ability to copy/paste flames from/to the clipboard. This is great when exchanging flames between different third-party application, FLAM3H™ and vice-versa.
- **New**: When loading a flame from the clipboard, its render properties will be automatically copied into the OUT tab render properties. This is done so not to loose those properties in case we copy another flame into the clipboard right after.
- **New**: Now you can load flame files without a valid _flames_ root tag as when you copy them to the clipboard from Apophysis or Fractorium.
- **New**: Added copy IN flame preset render properties button also to the OUT render properties tab as it is handy to also have it there.
- **Fix**: Loading flame files is now a bit faster.
- **Fix**: FLAM3H™ is now smarter about what's the content of the *.flame file you load is and will perform additional validity checks to be a bit more robust so to speak.
- **Fix**: Tag size presets are now working for the error messages too.
- **Fix**: OUT save option's tab is now of type: collapsible.
- **Fix**: The OUT Camera sensor Brightness, Scale and Rotate values are now properly cast as float instead of int.
- **Fix**: When the OUT sensor mode is ON, copying the IN flame preset render properties into the OUT render properties will now reset the camera sensor framing within the Houdini's current viewport.
- **Fix**: Updated HDA documentation to include the new features.


<br>
<br>


### [<ins>From v1.1.45</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.1.45) ###

- **New**: Recompiled everything using the latest H20.x vcc compiler. I could not spot any differences but for peace of mind.
- **New**: When in OUT Camera sensor mode, the SYS tab Tag icon will now turn red to allow to exit the mode also when inside a different tab other than the OUT tab.
- **New**: Added FLAM3H™ info messages to the Camera sensor mode: Zero iterators message and Xaos crossing the number of iterators allowed message.
- **New**: Added check for first node instance creation for the CVEX 64bit compile version.
- **New**: the HDA node now live inside its own tab menu call: FLAM3H.
- **Fix**: When in OUT Camera sensor mode, turning "edit render properties" toggle OFF will now properly restore the viewport you had prior to entering the Camera sensor mode.
- **Fix**: The OUT Camera sensor parameters are now capable to be set with values higher than their defaults limits.
- **Fix**: Fixed a bug that caused the copy/paste iterator and FF menus to display a deleted marked node message when loading a new hipe file.
- **Fix**: Improved Global density and OUT sensor resolution menu parameters pyhton methods.
- **Fix**: Improved FLAM3H™ on creation 32bit or 64bit CVEX compile checking methods.
- **Fix**: Fixed a bug that prevented to copy/paste an iterator's Weight and Active toggle value before copying something else first.
- **Fix**: Updated documentation and its vcc compiler version tag number.


<br>
<br>


### [<ins>From v1.1.33</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.1.33) ###

- **New**: Tested and working on the latest version of Houdini: H20
- **New**: New OUT Tab Render properties Camera sensor viz. All the render settings required by third-party programs such as Apophysis and Fractorium are stored together with the fractal flames when they are saved out from FLAM3H. A portion of the render parameters deal with the camera and how the fractal flame you just saved is framed. The FLAM3H™ camera sensor will precisely display the image framing.
- **New**: New copy/paste iterators and FF methods. It now also use FLAM3H™ node user data to better keep track of the marking actions.
- **New**: Added visual node's note when marking iterators and FF. This seemed like a simple feature to add but ended up requiring to add/change a big portion of the code.
- **New**: The Out Render properties tab has been split into two tabs: "_OUT Camera sensor_" and "_OUT Render settings_".
- **New**: The OUT Render properties reset button is now a muti-funtional button to reset different sections of the OUT Render properties.
- **New**: Affine values can now be reset in full, or only the different components using a combination of SHIFT, CTRL, ALT keys when clicking the reset button icon.
- **New**: Added SYS Tab viewport tag button icon that change based of the Tag being ON or OFF.
- **New**: Renamed FLAM3H™ hou.session data. Now this data have more proper names. If you are sourcing this new HDA version from an already running Houdini session, it may require you to restart Houdini fresh before or it may cause some clashes.
- **Fix**: Fixed a bug that caused to mess up some of the hou.session data needed for the copy/paste iterators methods when marking an iterator and then loading a flame file right after.
- **Fix**: Updated and improved documentation.
- **Fix**: Improved python code.


<br>
<br>


### [<ins>From v1.1.23</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.1.23) ###

- **New**: Xaos command string now allow you to type a number and the xaos will be generated with all weights set to that number.
- **Fix**: In some cases, deleting the very last iterator could messup the FLAM3H™ multiparameter index data.
- **Fix**: Fixed an error message when saving flames out even tho they were correctly saved.
- **Fix**: Small python code improvements.


<br>
<br>


### [<ins>From v1.1.22</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.1.22) ###

_This update improves upon nearly everything, focusing mostly on the  workflow and user experience that was already in place. For example the method for the copy/paste iterator's data has been completely rebuilt to integrate with the Xaos method. Now that Xaos is completely automated, they employ their own techniques to handle Undo's actions. Additionally, it addresses a tonne of minor issues that were overlooked in preview releases._

- **New**: Added F3C preference option ( flam3 compatibility ) to the XML ( IN/OUT ).
- **New**: Added RIP sys option ( Remove Invalid Points ) to the XML ( IN/OUT ).
- **New**: Palette are now saved with their HSV values if used.
- **New**: If you type a non numeric character in any of the xaos string weights, FLAM3H™ will Undo to what you had before instead of resetting all weights to a value of 1.0.
- **New**: Now is possible to swap the order of an iterator PRE variations or the order of the FF POST variations with one click.
- **New**: All Flame presets lib files now use the HSV values on load to be more vibrant in the viewport without modifying their original palette. Use the new Flame library presets files shipped with this release.
- **New**: If an OUT Flame name has been given, loading a new flame preset will update the Flame name iteration number string on Load if “_auto add iter num to Flame name_” option is ON.
- **New**: FLAM3H™ will now prevent you to deactivate all iterators. It will always keep the last one Active if it come to that. Houdini was crashing when all iterators were being deactivated.
- **New**: FLAM3H™ will now prevent you to set all iterators Weights to Zero. It will always keep the last iterator weight above Zero if it come to that. Houdini was crashing when all iterator’s weights were set to Zero.
- **New**: Added CVEX node compile status bar messages on first time node creation.
- **New**: Added FLAM3H™ documentation icon to the SYS tab.
- **New**: FLAM3H™ now print to the Houdini’s status bar instead of the console for most of its messages. Much more elegant.
- **New**: When iterators count is Zero the SYS Palette and SYS OUT icons will dim down.
- **New**: Added About Tab to the documentation topics.
- **New**: Added list of parametric variations and their parameter's names relative to their Houdini parameters to the OTL documentation for reference.
- **New**: "PALETTE JSON file load" is now a bit smarter about what JSON file you load in, and it check if it is a valid FLAM3H™ palette file. Due to this, preview palette libraries wont work anymore, sorry. Use the new palette libraries shipped with this release or rename the old json file presets keys yourself according to the new format.
- **New**: FLAM3H™ is a bit smarter when you create its node, automatically configuring its viewport display settings based on other FLAM3H™ node's settings already in the scene.
- **New**: Fixed a rare bug that prevented to properly add the iteration number string to the Flame name when "auto add iter num to Flame name" OUT Tab's option was ON.
- **New**: Now "auto set xaos" is handling and updating the copy/paste iterator's data as well. Becasue of this, it became the only available mode ( you can not turn it OFF anymore as there are no longer need to do it. The toggle has been hidden from the UI.)
- **New**: Added new icons.
- **Fix**: Improved COPY/PASTE iterator's data methods, its debug messages and fixed some bugs. Now the marked iterator is tracked down until its deletion if it come to that. A custom Undo mechanism has been implemented so to never really loose track of the marked iterator.
- **Fix**: Improved COPY/PASTE FF's data method, its debug messages and fixed some bugs. A custom Undo mechanism has been implemented so to never really loose track of the marked FF.
- **Fix**: Improved flam3 compatibility warning messages on flame OUT. Now it print out the affected iterator’s numbers and the name of the variations that are duplicates.
- **Fix**: Removed CP option “reset HSV on Load” as not needed anymore.
- **Fix**: Loading a Flame preset will now always set the “auto set xaos” preference option ON.
- **Fix**: IN load stats info name field is not all capital anymore but spelled correctly.
- **Fix**: Fixed extra empty line in the Locked lib file message for CP and OUT presets.
- **Fix**: Fixed IN preset infos Tab showing up when a non flame file was loaded.
- **Fix**: When iterators count is Zero the SYS IN and IN flame presets menu parameters will now display a more appropriate message.
- **Fix**: UI sub tabs names now use their parent tab’s name as a prefix.
- **Fix**: SYS tab icons are now properly left aligned in Houdini 19.5 too.
- **Fix**: Wrangle core nodes "Reload CVEX" button is now properly wired, and it work.
- **Fix**: Updated OTL documentation.
- **Fix**: Improved and finally better organized python code ( long overdue and still in a wip state ).
- **Fix**: Added doc strings to almost all python definitions.



<br>
<br>


### [<ins>From v1.0.28</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.0.28) ###

_Will update once H20 release._ 

- **New**: Updated documentation.
- **New**: Added documentation sub topics. Much more clear and easier to find what you are looking for.
- **New**: Re written most of the documentation in a much more clear and elegant form.
- **New**: Added a new node icon to reflect the new logo design.
- **New**: Included a very first release of FLAM3HUSD OTL. A simple **lop** node to make it easier to render FLAM3H™ fractal flames in Solaris for previews. It offers the very fundamental functionalities to setup your fractal flame point cloud to start rendering with Karma within a few clicks.
- **New**: Added a houdini desktop config file. This is the Houdini UI layout that worked best while doing fractal art with FLAM3H.
- **Fix**: Python: FLAM3H™ xaos history data is now protected so to speak.


<br>
<br>


### [<ins>From v1.0.25</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.0.25) ###

- **New**: FLAM3H™ OTL documentation: Added a much, much more comprehensive documentation.
- **New**: FLAM3H™ OTL documentation: Added new banner image.
- **New**: FLAM3H™ OTL documentation: Added new help card icon.
- **New**: FLAM3H™ OTL documentation: Added "intro" section.
- **New**: FLAM3H™ OTL documentation: Added "rendering tips" section.
- **New**: FLAM3H™ OTL documentation: Added "cvex how to" section.
- **New**: FLAM3H™ OTL documentation: Added "author" section.
- **New**: FLAM3H™ OTL documentation: Added a new colored Xaos paths diagram/image.
- **New**: FLAM3H™ OTL documentation: Added weblinks to an handful of Apophysis tutorials to follow as a starter.
- **New**: FLAM3H™ node: Added "Reload Cvex" icon button to each wrangleCore node.
- **New**: FLAM3H™ Github: Added "icons" folder to the Github repository.
- **New**: FLAM3H™ Github: Added updated images to the main README.md file/page.

- **Fix**: FLAM3H™ OTL documentation: Fixed some typos.
- **Fix**: FLAM3H™ XML custom data: Motion blur shutter time value now export properly into the XML.
- **Fix**: FLAM3H™ XML custom data: Improved "flam3h motion blur" XML key's names.


<br>
<br>


### [<ins>From v1.0.23</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.0.23) ###

- **New**: Added "auto set xaos" preference option. ( ON by default ). Now Xaos is automatically set and taken care of by the tool. This was the the very last feature so to speak in my bucket list.
- **New**: The viewport Tag icon will now turn to a red when "auto set xaos" preferences option is OFF.
- **New**: Added "auto space xaos weights" option to make the xaos string more readable. ( OFF by default )
- **New**: Added "auto add iter num" to Flame preset name inside the OUT Tab.
- **New**: When "auto add iter num" is ON, changing the iterations number will updated the Flame name string if any.
- **New**: FLAM3 for Houdini now export the ramp HSV values into the XML and set them on load if it find them. This is useful because when saving out Flames their ramp's colors will be clamped, defeating the whole purpose of increasing the Value in HS"V" to achieve high dynamic ranges in your render when you load the saved Flame back in.
- **New**: FLAM3 for Houdini now export Motion Blur settings into the XML and set them on load. This do not make much sense since you can not export animation data into the XML at the moment, but maybe handy to have for the future.
- **New**: Added Button to reset density to its default.
- **Fix**: when switching between xaos modes with "auto set xaos" ON, there were some wrong shuffling of xaos weights due to the use of "conservative xaos" during conversions.
- **Fix**: when switching between xaos modes with "auto set xaos" ON, the xaos history wasnt being updated accordingly.
- **Fix**: the iterator's xaos string parameter has been renamed from: "varnote_#" to: "xaos_#" ( long overdue ). This will force old scenes to reset their xaos to a default values value of 1, sorry! You can save out your Flames first into a flame file library before upgrading to this verion.
- **Fix**: improved auto correction of output paths.
- **Fix**: IN Tab "use iterations on load" is a bit smarter.
- **Fix**: when iterators count is ZERO, the SYS OUT flame mini menu will show the proper message.
- **Fix**: when iterators count is ZERO, you wont be able to save out to a flame file from the SYS OUT flame icon.
- **Fix**: when iterators count is ZERO, trying to load a palette from the SYS load palette icon wont error anymore.
- **Fix**: pyhton code cleanup and improvements.


<br>
<br>


### [<ins>From v1.0.15</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.0.15) ###

- New: added density presets.
- New: added CP palette file presets menu to the SYS Tab.
- New: added IN flame file presets menu to the SYS Tab.
- New: added OUT flame file contents menu to the SYS Tab.
- New: added auto correction of the output paths you enter in the CP and OUT Tabs. It will happen on the fly as soon as you hit enter.
- New: updated OTL documentation with new parameters/menus entries and additional helpful informations.
- New: OTL documentation now have a proper section's agenda at the very top for quick access to informations. ( in progress )
- Fixed: pre_blur and mobius in the same iterator causing a mismatch of value when loading a flame.
- Fixed: Mismatch of variations when loading flames in some cases.
- Fixed: Saving out a palette to a filepath not existing yet was erroring out. 
- Fixed: Post affine checkboxes now uses the header_toggle builtin tag, much more cleaner.
- Fixed: When iterator's count is ZERO the density value will now reset back to default (500k).
- Fixed: When iterator's count is ZERO, the node descriptive message will now clear up.
- Fixed: When selecting a non valid file location in the IN flame file parameter the infos and IN render properties Tabs will now hide.
- Fixed: Loading an hip file with a FLAM3H™ node in it with a JSON, IN or OUT file path no longer valid will now properly hide unnecessary Tabs and print out messages accordingly.
- Fixed: Palette and IN presets now kept when loading back a hip file with those menus set.
- Fixed: Force update about tab on load to pick up changes made on the moment.
- Fixed: Little IN Tab UI redesign.
- Fixed: Little python code improvements.
- Fixed: The IN Tab parameter option "Use Fractorium color speed" has been hidden.


<br>
<br>


### [<ins>From v1.0.00</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v1.0.0) ###

- **New**: ability to save in a flame file format.
- **New**: render properties settings on flame save to control the renderer of the saved flame file inside an host application ( Fractorium ideal, Apophysis as well. ).
- **New**: render properties copy/paste from the IN flame file to the OUT flame file.
- **New**: auto correction of filename for palette and flame file on save.
- **New**: auto generated filename for palette and flame save if none specified.
- **New**: auto generated preset name for palette and flame presets if none specified.
- **New**: removed SM Tab ( symmetry ) and added a point_symetry variation. Much more powerful and versatile.
- **New**: removed TM Tab ( global transformations ). It was useful
                 but you can do the same animating all the affine's Rot parameters and I saved a bit inside the chaos game.
- **New**: added 1 finalxform pre variation slot.
- **New**: save flame files with conservative xaos data output ( to match all the other applications as well )
- **New**: ability to save out a flame using either the source palette or the color corrected one.
- **New**: new palette data format much, much lighter. You can now create libraries of hundreds of them resulting in a very small file size.
                ( the preview palette's implementation didn't scale well for this purpose considering every flame always have 256 colors/keys )
- **New**: a bit faster, when multiple variations are used inside each iterator can be ~5% faster.
- **New**: simple but effective way to lock/protect a palette or flame library file you created from being overwritten accidentally by the tool.
- **New**: Added a set of palette libraries using the new data format and translated from the one available in Fractorium.
- **New**: button to reset pre and post affine if needed.
- **New**: button to reset the palette ramp.
- **New**: added button to update/reload the current IN flame preset to the SYS Tab ( always accessible )
- **New**: Multi functional save button for the Palette and Flame OUT file.
- **New**: quick, simple and intuitive way to write, append or overwrite a palette or flame inside each one library.
- **New**: added more web links inside the about tab.
- **New**: asset definition name has changed from "::sop/FLAME" to "::sop/FLAM3H".
                 As a result, Houdini will see this as a brand new plugin/asset.
                 This has been done to prevent old presets ( if any ) to clash and `sabotage` the asset with the new updates of this version.
- **New**: added information's buttons to display parts of parameter's documentation only available inside the OTL help otherwise ( blue F icons ).
- **Fixed**: corrected pre variations behavior.
- **Fixed**: iterator's Weight not being set on flame load when its value was Zero.
- **Fixed**: "xaos: " command string is now smarter about what you type in.
- **Fixed**: iterations on flame load not always using its default values.
- **Fixed**: pre_blur variation not always being set on flame load.
- **Fixed**: out of bounds palette's color values are now taken care of.
- **Fixed**: Auger variation.
- **Fixed**: Fan variation.
- **Fixed**: iterators are now created with a default name.
- **Fixed**: the "xaos:" keyword is now present as a default inside each iterator.
- **Fixed**: improved OTL documentation.
- **Fixed**: parameters tooltips now showing more descriptive and generous descriptions.


<br>
<br>


### [<ins>From v0.9.5.2</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.5.2) ###

- **New**: Added Crop variation.
- **New**: Added Unpolar variation.
- **New**: Added Glynnia variation.
- **New**: Added more example files from Devianart.
- **Fixed**: flame files created with older versions of Apophysis
  didn’t load due to missing key names in the file.
  Now it work and the missing keys are set to a default value.
- **Fixed**: palette colors from flame load are now more vibrant.
- **Fixed**: Palette HSV values now default to: (1, 1, 1) making possible to hue backward.
- **Fixed**: Juliascope variation distance parameter not being set on flame load.


<br>
<br>


### [<ins>From v0.9.5</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.5) ###

- **New**: Able to Load flame files ( “IN” Tab )
- **New**: Added flame files examples library to load them in.
- **New**: Auto set iterations count on flames load.
- **New**: Flame file loaded preset’s Stats/infos.
- **New**: Stats can display used variations.
- **New**: Stats can display missing variations.
- **New**: iterator shader’s values in line with Apophysis.
- **New**: Added both flam3 compatible and non compatible versions to the following variations:
                 cos, cosh, cot, coth, csc, csch, sec, sech, sin, sinh, tan and tanh. 
                 You can switch between the two versions from preferences->flam3 compatibility checkbox.
- **New**: Both iterator’s pre vars are now capable of parametrics.
- **New**: about box infos.
- **Fixed**: Modulus.
- **Fixed**: Edisc.
- **Fixed**: Curve.
- **Fixed**: Auger.
- **Fixed**: Exp.
- **Fixed**: Heart.
- **Fixed**: Polynomial.
- **Fixed**: Waves.
- **Fixed**: Sech.
- **Fixed**: Csc.
- **Fixed**: wedge, wedge_julia, wedge_sph. They had their parameters order mixed up.


<br>
<br>


### [<ins>From v0.9.3d</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.3d) ###

- Iterator and FF notes are now saved along with the copy/paste msg string.
- When setting the iterator count to ZERO also the FF tab parameters will reset to their default values.
- When setting the iterator count to ZERO the load default preset icon stay accessible.
- HSV back to being applied from inside the cvex code to keep interactivity while changing the ramp colors.
- Some parameter's name have been renamed to keep consistency.


<br>
<br>


### [<ins>From v0.9.3c</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.3c) ###

- Added extra ramp to preview HSV values. ( not editable - viz only )
- HSV is now applied directly to the ramp instead of happening inside the TFFApalettesimple cvex code.
- Added the preference option to set the Houdini viewport scheme to Dark.
   It will remember the color scheme you had if not dark and revert back to it when unchecked. 
-  Added the preference option to set the viewport particle display to either Points or Pixels.
- cvex code improvements there and there.
- python code improvements there and there.


<br>
<br>


### [<ins>From v0.9.3</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.3) ###

- More robust copy/paste method.
- Ability to copy and paste iterators between different FLAM3 nodes.
- Ability to copy and paste Final Flame transforms between different FLAM3 nodes.
- Ability to copy and paste single sections of an iterator or of a Final Flame transform.
   ex.: only shader values, only pre affine or post affine, only pre-variations or post-variations and so on, also between different FLAM3 nodes.
- Smarter copy and paste UI menus so that they can show useful messages and piece of data
   about what it is that you are copying and from where.
-  All copy and paste modes now support Animation: Keyframes and Expressions channels.
- Ability to clear/delete the stored data.


<br>
<br>


### [<ins>From v0.9.2b</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.2b) ###

- Improved copy/paste of iterator' s values.
   Now you can copy/paste iterators between different FLAM3 nodes.
   The note parms will be set to tell you from witch FLAM3 node
   and iterator number the values are coming from when pasted.
- Removed the "Presets" file previously embedded in the asset.
- Load default preset now handled with python. Much more cleaner.
- Cleaner initial python setup, now using FLAM3 sub-module from section everywhere.


<br>
<br>


### [<ins>From v0.9.2</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.2) ###

- You can now copy iterator's values from one to another.
- Updated Final Flame transform's parameters names.
- Better python setup. It is now going through the toolutils Houdini python module.
- Color palette menu library now update as soon as you load a palette library json file.
- Added an icon under SYS tab to load back the default Sierpinsky triangle preset.
- Fixed TAG viewport display not showing PRE variations and Final Flame POST variations.


<br>
<br>


### [<ins>From v0.9.1c</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.1c) ###

- Added the ability to use Xaos in either **TO** or **FROM** mode.
  `You can find the option inside the preferences tab.`
- Updated OTL Help/Documentation a bit.
- Little code cleanup there and there.


<br>
<br>


### [<ins>From v0.9.1</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.1) ###

- Fixed XAOS.
  Due to a Houdini bug I needed to redo the Xaos implementation. Now is correct.
- The new Xaos is ~10/15% faster than the preview one.
   Read the HDA help/documentation for more infos.
- Added 1 pre variation witch support parametric vars too, for a total of 3 pre variations each iterator.
- Added one post variation for the Final Flame transform for a total of 2 Final Post vars.
- Fixed ring2 variation parametrics parameters not being wired properly.
- Quickly added the ability to save and load palette based on the code found here:
   **[SideFX Forum ramp manager]( https://www.sidefx.com/forum/topic/81130/)**
   This is a placeholder as it will change/grow in the future.
- Little code cleanup there and there.


<br>
<br>


### [<ins>From v0.9.0c</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.0c) ###

- More code cleanup.
- Shortened local var's names and attrib's names.
- Genome's data collection now slightly faster.
- Flames with many iterators should see a little speed increase of up to ~3%.
- Compiled file size ~10kb smaller.
- `TFFAvactive.vfl` has been renamed to `TFFAxaos.vfl` as well its host wrangle core node.


<br>
<br>


### [<ins>From v0.9.0b</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.0b) ###

- Code cleanup everywhere.
- Compiled file size ~10kb smaller.
- DISC2 variation is ~18% faster.
- Slightly faster.
- Fixed a small bug in the camera handles.


<br>
<br>


### [<ins>From v0.9.0</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.9.0) ###

- Added pre variations. ( non parametrics for now )
- XAOS now has a better sampling.
- Compiled the few remaining wrangles into CVEX so now the tool is self contained.
- Swapped VOPs nodes for the new wrangle core node. Feel more solid and modern in a way.
- UI got a little lifting.
- Code optimizations.


<br>
<br>


### [<ins>From v0.8.9b</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.8.9b) ###

- Fixed a bug introduced with the preview release where the Alpha value was coming out wrong if XAOS was used.
- XAOS now has its own field. You can still use it as an extra description note if you like so.
- Slightly faster.


<br>
<br>


### [<ins>From v0.8.8</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.8.8) ###

- XAOS is now automatically active only when used. ( before it was always active)
- As a result of the above, when not using XAOS it will be ~15/20% faster.
- Variation's functions are now living in their own header file.


<br>
<br>


### [<ins>From v0.8.7</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.8.7) ###

- Added a first try of XAOS. Read the HDA documentation to learn how to use it within the tool UI.


<br>
<br>


### [<ins>From v0.8.6</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.8.6) ###

- Color speed can now be a negative value too.
- Added color opacity, this allow to build simple but proper fractal flame containers.


<br>
<br>


### [<ins>From v0.8.5</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.8.5) ###

- A bit faster ( ~5% on average. H19.x version being the faster )
- Improved HDA help/documentation.
- Added rotation parameter inside post affine as well.
- Final Flame post variation now has its own set of parameters and Tab for parametric variations.
- Please, use the new provided Presets files. They have more examples and are rebuilt using this version new UI.
- Removed symmetry global pivot parameter.
- Removed TMG translation parameter.
- Code clean up and improvements.


<br>
<br>


### [<ins>From v0.8.0</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.8.0) ###

- Added rotation parameter inside iterators affine tab. This help when editing the fractal flame.
- The rotation will take the values of *X, Y, O* and apply a rotation. Note that the resulting affine coefficients are not updated in the UI but passed directly internally to the algorithm so that if you are copying values from Apophysis, then the rotation must be set to ZERO to match or you will apply a double transformation otherwise.
- Attribute @pscale now default to a value of 0.001.
- Now if an iterators weight is set to ZERO it will be considered disabled.
- Little code cleanup there and there.


<br>
<br>


### [<ins>From v0.7.9</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.7.9) ###

- ~10/20% faster (depending on hardware).
- Conformed UI with new H19 parameters look.
- This is a Houdini 19.x only version. SideFX have made some big updates to the vcc compiler and the results shows!


<br>
<br>


### [<ins>From v0.7.8b</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.7.8b) ###

- Added POST Variation to Final Flame transform.
- ~40% faster first node instance creation time.
- ~5% faster overall.
- Added new presets file


<br>
<br>


### [<ins>From v0.7.7c3</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.7.7c3) ###

- Removed some leftover variables from variation.h and fixed an else statement inside genome.h


<br>
<br>


### [<ins>From v0.7.7c2</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.7.7c2) ###

- Fixed Final Flame transform POST affine not being used.


<br>
<br>


### [<ins>From v0.7.7c</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.7.7c) ###

- Color mode now in line with Apophysis and the other ( uses Color Location and Blend Speed).
   To test it out I replicated a preset from Chaotica software inside Houdini.
   This was one of Chaotica's preset I loved the most and kept it as my milestone. Gloriously rendered with Mantra.
   Added new presets file to play with, include the Chaotica's match preset as well.


<br>
<br>


### [<ins>From v0.7.6</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.7.6) ###

- Affine coefficients now have the same layout as Apophysis software. Improved genomeParametricBuild() function. New Presets file, override the old one ( back it up first ) as the UI layout as changed. Overall is ~10% faster.


<br>
<br>


### [<ins>From v0.7.5d</ins>](https://github.com/alexnardini/FLAM3_for_SideFX_Houdini/releases/tag/v0.7.5d) ###

- Fixed POST affine and faster first node instance creation time


<br>
<br>


..._plus many more from when I first started and this project was not on GitHub yet_.
