

```python
#   Title:      FLAM3H™. SideFX Houdini FLAM3: UI ICON MAP
#   Author:     F stands for liFe ( made in Italy )
#   date:       September 2025, Last revised September 2025
#   License:    GPL
#   Copyright:  (c) 2021 F stands for liFe
#
#   Name:       FLAM3H__UI_ICON_MAP
#
#   Comment:    List of all UI parameters with ICONS associated with
#               and the command string they are called from and from where.
#
#               THIS IS ONLY INFORMATIVE AND FOR EASY FIND INSTEAD OF
#               NAVIGATING THE PARAMETERS INSIDE THE OTL TYPE PROPERTIES WINDOW.
```


<br>
<br>



_Parameters to define the quality of the fractal Flame algorithm solution._

# GLOBAL Tab
# parameter name:    `icon_iter_off`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```python
opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg
```

</br>
</br>

# GLOBAL Tab
# parameter name:    `ptcount_presets_off`
### Menu icons
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```
![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]
```

</br>
</br>

# GLOBAL Tab
# parameter name:    `icon_iter`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarBlueSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg
```

</br>
</br>

# GLOBAL Tab
# parameter name:    `ptcount_presets`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density()
return menu
```

</br>
</br>

The pre-built icons menu python lists being used:

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhiteSVG.svg" />
<img width="48" height="48" src="../icons/icon_StarSwapCyanSmallSVG.svg" />
<img width="48" height="48" src="../icons/icon_optionEnabledMidSVG.svg" />
<img width="48" height="48" src="../icons/icon_optionStarRedHighSVG.svg" />
</p>

```python
MENU_DENSITY: list = [-1, '', 1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg]...', 2, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]1M', 3, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]2M', 4, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]5M', 5, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]15M', 6, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]25M', 7, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]50M', 8, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]100M', 9, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]150M', 10, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]250M', 11, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]500M', 12, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]750M', 13, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1 Billion', 14, '']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhiteXFVIZOFFSVG.svg" />
<img width="48" height="48" src="../icons/icon_StarSwapCyanSmallXFVIZOFFSVG.svg" />
<img width="48" height="48" src="../icons/icon_StarSwapCyanSmallSVG.svg" />
<img width="48" height="48" src="../icons/icon_optionEnabledMidSVG.svg" />
<img width="48" height="48" src="../icons/icon_optionStarRedHighSVG.svg" />
</p>

```python
MENU_DENSITY_XFVIZ_OFF: list = [-1, '', 1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteXFVIZOFFSVG.svg]...', 2, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZOFFSVG.svg]1M', 3, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZOFFSVG.svg]2M', 4, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZOFFSVG.svg]5M', 5, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]15M', 6, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]25M', 7, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]50M', 8, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]100M', 9, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]150M', 10, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]250M', 11, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]500M', 12, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]750M', 13, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1 Billion', 14, '']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhiteXFVIZSVG.svg" />
<img width="48" height="48" src="../icons/icon_StarSwapCyanSmallXFVIZSVG.svg" />
<img width="48" height="48" src="../icons/icon_StarSwapCyanSmallSVG.svg" />
<img width="48" height="48" src="../icons/icon_optionEnabledMidSVG.svg" />
<img width="48" height="48" src="../icons/icon_optionStarRedHighSVG.svg" />
</p>

```python
MENU_DENSITY_XFVIZ_ON: list = [-1, '', 1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteXFVIZSVG.svg]...', 2, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSVG.svg]1M', 3, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSVG.svg]2M', 4, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSVG.svg]5M', 5, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]15M', 6, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]25M', 7, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]50M', 8, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]100M', 9, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]150M', 10, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]250M', 11, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]500M', 12, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]750M', 13, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1 Billion', 14, '']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhiteXFVIZSOLOSVG.svg" />
<img width="48" height="48" src="../icons/icon_StarSwapCyanSmallXFVIZSOLOSVG.svg" />
<img width="48" height="48" src="../icons/icon_StarSwapCyanSmallSVG.svg" />
<img width="48" height="48" src="../icons/icon_optionEnabledMidSVG.svg" />
<img width="48" height="48" src="../icons/icon_optionStarRedHighSVG.svg" />
</p>

```python
MENU_DENSITY_XFVIZ_ON_SOLO: list = [-1, '', 1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteXFVIZSOLOSVG.svg]...', 2, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSOLOSVG.svg]1M', 3, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSOLOSVG.svg]2M', 4, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSOLOSVG.svg]5M', 5, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]15M', 6, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]25M', 7, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]50M', 8, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]100M', 9, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]150M', 10, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]250M', 11, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]500M', 12, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]750M', 13, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1 Billion', 14, '']
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg
```

</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>

_Tools available to enhance and speed up the workflow.<br>
I keep changing and adding functionalities, it is still a work in progress, but thus far, this most recent configuration has been successful._

# SYS Tab
# parameter name:    `sys_help`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_F_docStarSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_F_docStarSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `iterlist`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_select_iterator()
return menu
```
</br>
</br>

The pre-built icons menu python lists being used:

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarYellowOrangeSVG.svg" />
<img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteSVG.svg" />
</p>

```python
SEL_ITER_BOOKMARK_ACTIVE_AND_WEIGHT: tuple = (FLAM3H_ICON_STAR_FLAME_ITER_ACTV, FLAM3H_ICON_COPY_PASTE)
```
```python
# FLAM3H_ICON_STAR_FLAME_ITER_ACTV
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarYellowOrangeSVG.svg]'
```
```python
# FLAM3H_ICON_COPY_PASTE
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteSVG.svg]'
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledZeroIterSVG.svg" />
<img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteZeroWSVG.svg" />
</p>

```python
SEL_ITER_BOOKMARK_ACTIVE_AND_WEIGHT_ZERO: tuple = (FLAM3H_ICON_STAR_EMPTY_OPACITY, FLAM3H_ICON_COPY_PASTE_ENTRIE_ZERO)
```
```python
# FLAM3H_ICON_STAR_EMPTY_OPACITY
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]'
```
```python
# FLAM3H_ICON_COPY_PASTE_ENTRIE_ZERO
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteZeroWSVG.svg]'
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledSVG.svg" />
<img width="48" height="48" src="../icons/icon_optionDisabledSelIterSVG.svg" />
</p>

```python
SEL_ITER_BOOKMARK_OFF: tuple = (FLAM3H_ICON_STAR_EMPTY, FLAM3H_ICON_COPY_PASTE_ENTRIE_ITER_OFF_MARKED)
```
```python
# FLAM3H_ICON_STAR_EMPTY
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledSVG.svg]'
```
```python
# FLAM3H_ICON_COPY_PASTE_ENTRIE_ITER_OFF_MARKED
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledSelIterSVG.svg]'
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarBlueSVG.svg" /></p>

```python
MENU_ZERO_ITERATORS: list = [0, "![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]  ZERO ITERATORS\n -> Please, create at least one iterator or load an IN flame file first.", 1, ""]
```

</br>
</br>

# SYS Tab
# parameter name:    `doff_no_iterators`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `doff_sysdisabled`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionFFDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionFFDisabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `doff_sysenabled`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionFFEnabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionFFEnabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `rip_no_iterators`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `rip_disabled`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionRIPDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionRIPDisabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `rip_enabled`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionRIPEnabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionRIPEnabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `f3c_no_iterators`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `f3c_chaotica`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionF3CDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionF3CDisabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `f3c_apophysis`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionF3CEnabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionF3CEnabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `xfviz_no_iterators`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `xfviz_off`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_xfHandlesDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_xfHandlesDisabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `xfviz_on`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_xfHandlesEnabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_xfHandlesEnabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `xfviz_on_solo`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_xfHandlesEnabledMPIDXSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_xfHandlesEnabledMPIDXSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `xfvizff_on_solo`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_ffHandlesEnabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_ffHandlesEnabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_out_sensorviz`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_TagORedSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_TagORedSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_out_sensorviz_off`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_TagORedOffSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_TagORedOffSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_tag_disabled`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_tag_off`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_TagOBlueSVG_disabled.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_TagOBlueSVG_disabled.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_tag`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_TagOBlueSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_TagOBlueSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `tagsize`
### Menu icons
<p align="left"><img width="48" height="48" src="../icons/icon_TagOBlueMenuSmallSVG.svg" /></p>
Token: 0

```
![opdef:/alexnardini::Sop/FLAM3H?icon_TagOBlueMenuSmallSVG.svg] sml
```
<p align="left"><img width="48" height="48" src="../icons/icon_TagOBlueMenuMidSVG.svg" /></p>
Token: 1

```
![opdef:/alexnardini::Sop/FLAM3H?icon_TagOBlueMenuMidSVG.svg] Mid
```
<p align="left"><img width="48" height="48" src="../icons/icon_TagOBlueMenuBigSVG.svg" /></p>
Token: 2

```
![opdef:/alexnardini::Sop/FLAM3H?icon_TagOBlueMenuBigSVG.svg] BIG
```

</br>
</br>

# SYS Tab
# parameter name:    `loaddef`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_SierpinskyDefSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_SierpinskyDefSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `frameview`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_FrameBlueSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_FrameBlueSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `frameview`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_FrameRedSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_FrameRedSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_palettepresets_disabled`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_palettepresets_off`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets_empty()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionPRIDEDisabledSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionPRIDEDisabledSVG.svg]'
```

</br>
</br>

The pre-built icons menu python lists being used:

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledZeroIterSVG.svg" />
</p>

```python
MENU_PRESETS_EMPTY: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]  Empty     ']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarBlueSVG.svg" />
</p>

```python
MENU_PRESETS_SAVEONE: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]  Save to create this file     ']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarOrangeSVG.svg" />
</p>

```python
MENU_PRESETS_INVALID: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  Invalid file path     ']
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionPRIDEDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionPRIDEDisabledSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_palettepresets`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionCPSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionCPSVG.svg]'
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionCPSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionCPSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_inpresets_disabled`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets_empty()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_WhiteSVG_disabled.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_WhiteSVG_disabled.svg]'
```

</br>
</br>

The pre-built icons menu python lists being used:

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledZeroIterSVG.svg" />
</p>

```python
MENU_PRESETS_EMPTY: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]  Empty     ']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarBlueSVG.svg" />
</p>

```python
MENU_PRESETS_SAVEONE: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]  Save to create this file     ']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarOrangeSVG.svg" />
</p>

```python
MENU_ZERO_ITERATORS_PRESETS_INVALID: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  ZERO ITERATORS\n -> Invalid file path. Please, create at least one iterator or load a valid IN flame file first.']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarOrangeSVG.svg" />
</p>

```python
MENU_PRESETS_INVALID: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  Invalid file path     ']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarOrangeSVG.svg" />
</p>

```python
MENU_PRESETS_INVALID_CB: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  [CLIPBOARD] Invalid file path     ']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhiteSVG.svg" />
</p>

```python
MENU_IN_PRESETS_EMPTY_CB: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg]  [CLIPBOARD]     ']
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_WhiteSVG_disabled.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_WhiteSVG_disabled.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_inpresets`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionFlameINEntrieSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionFlameINEntrieSVG.svg]'
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_WhiteSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_WhiteSVG.svg
```




</br>
</br>


# SYS Tab
# parameter name:    `sys_outpresets_disabled`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg
```

</br>
</br>

# SYS Tab
# parameter name:    `sys_outpresets`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionFlameOUTEntrieSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionFlameOUTEntrieSVG.svg]'
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_WhiteStarSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_WhiteStarSVG.svg
```

</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>

_This is where you’ll spend the majority of your time, along with the FF Tab.<br>
Here you will create your fractal Flame logic.<br>Since every parameter has the same name inside, if you have ever used Apophysis, Fractorium, or other fractal Flame editors, you will almost immediately feel at home. The logic you will operate with will be the same._
# FLAME Tab
# parameter name:    `mp_add_#` -> _only from H21 up_
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_AddDelIteratorSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_AddDelIteratorSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `prmpastesel_#`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteEntrieSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteEntrieSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteZeroWSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteZeroWSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionStarBlueSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]'
```
</br>
</br>

The pre-built icons menu python lists being used:

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarOrangeSVG.svg" /></p>

```python
MENU_ITER_COPY_PASTE_DELETED_MARKED: list = [ 0, "![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  DELETED: Marked iterator's node has been deleted.\n-> Mark another iterator first.", 1, "" ]
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarOrangeSVG.svg" /></p>

```python
MENU_ITER_COPY_PASTE_REMOVED: list = [0, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  REMOVED: The marked iterator has been removed.\n-> Mark an existing iterator instead.', 1, '']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteSVG.svg" /></p>

```python
MENU_ITER_COPY_PASTE_EMPTY: list = [0, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteSVG.svg]  Please, mark an iterator first.', 1, '']
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_StarSwapRedCopyPasteSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `doiter_disabled_#`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `doiter_#`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarYellowOrangeSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarYellowOrangeSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `xfviz_off_#`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_xfHandlesDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_xfHandlesDisabledSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `xfviz_on_#`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_xfHandlesEnabledMPIDXSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_xfHandlesEnabledMPIDXSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `xfviz_on_#`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarBlueKwargsSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueKwargsSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `preblurtype_#`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T_pb()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhitePBSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhitePBSVG.svg]'
```

</br>
</br>

# FLAME Tab
# parameter name:    `pre1type_#`, `pre2type_#` and `p1type_#`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T_PP()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhitePBSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhitePBSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhitePBHSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhitePBHSVG.svg]'
```

</br>
</br>

# FLAME Tab
# parameter name:    `pre2weight_#`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteKwargsSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteKwargsSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `v1type_#`, `v2type_#`, `v3type_#`, `v4type_#`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionEnabledSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapCyanSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSVG.svg]'
```

</br>
</br>

# FLAME Tab
# parameter name:    `scl_#`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_StarSwapRedCopyPasteAffineSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteAffineSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `ang_#`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteKwargsSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteKwargsSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `pscl_#`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_StarSwapRedCopyPasteAffineSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteAffineSVG.svg
```

</br>
</br>

# FLAME Tab
# parameter name:    `pang_#`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteKwargsSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteKwargsSVG.svg
```

</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>

_Iterators like Final Flame (FF) or finalXform function like camera lenses.<br>
It allows for a great deal of creative experimentation by taking the combined result of all the iterators inside the FLAME Tab and applying further modifications to that result._

# FF Tab
# parameter name:    `doff_disabled`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionFFDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionFFDisabledSVG.svg
```

</br>
</br>

# FF Tab
# parameter name:    `doff_enabled`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionFFEnabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionFFEnabledSVG.svg
```

</br>
</br>

# FF Tab
# parameter name:    `xfvizff_off`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_xfHandlesDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_xfHandlesDisabledSVG.svg
```

</br>
</br>

# FF Tab
# parameter name:    `xfvizff_on`
### Button icon
<p align="left"><img width="80" height="80" src="../icons/icon_ffHandlesEnabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_ffHandlesEnabledSVG.svg
```

</br>
</br>

# FF Tab
# parameter name:    `ffprmpastesel`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste_FF()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteFFSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteFFSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteEntrieFFSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteEntrieFFSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteEntrieFFOffSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteEntrieFFOffSVG.svg]'
```

</br>
</br>

The pre-built icons menu python lists being used:

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedCopyPasteFFSVG.svg" /></p>

```python
MENU_FF_COPY_PASTE_EMPTY: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteFFSVG.svg]  Please, mark the FF first.', 0, '']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarBlueSVG.svg" /></p>

```python
MENU_FF_COPY_PASTE_SELECT: list = [0, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]  FF: MARKED\n-> Select a different FLAM3H™ node to paste those FF values.', 1, '']
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_StarSwapRedCopyPasteFFSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteFFSVG.svg
```

</br>
</br>

# FF Tab
# parameter name:    `ffpre1type` and `ffp1type`, `ffp2type`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T_PP(True)
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhitePBSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhitePBSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhitePBHSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhitePBHSVG.svg]'
```

</br>
</br>

# FF Tab
# parameter name:    `ffv1type`, `ffv2type`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T(True)
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledZeroIterSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionEnabledSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapRedSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedSVG.svg]'
```
<p align="left"><img width="48" height="48" src="../icons/icon_StarSwapCyanSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSVG.svg]'
```

</br>
</br>

# FF Tab
# parameter name:    `ffp2weight`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteKwargsSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteKwargsSVG.svg
```

</br>
</br>

# FF Tab
# parameter name:    `ffscl`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_StarSwapRedCopyPasteAffineFFSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteAffineFFSVG.svg
```

</br>
</br>

# FF Tab
# parameter name:    `ffang`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteKwargsSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteKwargsSVG.svg
```

</br>
</br>

# FF Tab
# parameter name:    `ffpscl`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_StarSwapRedCopyPasteAffineFFSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteAffineFFSVG.svg
```

</br>
</br>

# FF Tab
# parameter name:    `ffpang`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteKwargsSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteKwargsSVG.svg
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

_The palette colors used in a successful fractal Flame are crucial.<br>
In addition to playing with the shader parameters for each iterator, fractal Flames can be transformed into something truly unique by trying out various color schemes._

# CP Tab
# parameter name:    `hsv`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg
```

</br>
</br>

# CP Tab
# parameter name:    `palettehsv`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg
```

</br>
</br>

# CP Tab
# parameter name:    `cp_lookupsamples`
### Menu icons
<p align="left"><img width="48" height="48" src="../icons/icon_optionStarWhiteSVG.svg" /></p>
Token: 256

```
![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg]256
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionEnabledSVG.svg" /></p>
Token: 512

```
![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledSVG.svg]512
```
<p align="left"><img width="48" height="48" src="../icons/icon_optionStarRedHighSVG.svg" /></p>
Token: 1024

```
![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1024     
```

</br>
</br>

# CP Tab
# parameter name:    `palette`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteKwargsSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteKwargsSVG.svg
```

</br>
</br>

# CP Tab
# parameter name:    `palettename`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_WhiteStarSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_WhiteStarSVG.svg
```

</br>
</br>

# CP Tab
# parameter name:    `palettepresets_off`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets_empty()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionPRIDEDisabledSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionPRIDEDisabledSVG.svg]'
```

</br>
</br>

The pre-built icons menu python lists being used:

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionDisabledZeroIterSVG.svg" />
</p>

```python
MENU_PRESETS_EMPTY: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]  Empty     ']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarBlueSVG.svg" />
</p>

```python
MENU_PRESETS_SAVEONE: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]  Save to create this file     ']
```

</br>
</br>

<p align="left"><img width="48" height="48" src="../icons/icon_optionStarOrangeSVG.svg" />
</p>

```python
MENU_PRESETS_INVALID: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  Invalid file path     ']
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionPRIDEDisabledSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionPRIDEDisabledSVG.svg
```

</br>
</br>

# CP Tab
# parameter name:    `palettepresets`
### Menu icons
This menu icon set is built on demand from the py_flam3__x_x.py HDA python module (_where x_x is the python module version_).
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets()
return menu
```
Menu entries icon:</br>
_The following are icons being used on demand based on the menu python script needs._
<p align="left"><img width="48" height="48" src="../icons/icon_optionCPSVG.svg" /></p>

```python
'![opdef:/alexnardini::Sop/FLAM3H?icon_optionCPSVG.svg]'
```

</br>
</br>

### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionCPSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionCPSVG.svg
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

_Flame fractal moton blur._<br>
_When animating your fractal Flame, turning this on will compute a proper temporal motion blur._

</br>
</br>

# MB Tab
# parameter name:    `domb`
### Action icon
<p align="left"><img width="80" height="80" src="../icons/icon_optionStarWhiteSVG.svg" /></p>

```
opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

_Load *.flame files created with Apophysis, Fractorium and others.<br>
A *.flame file is an XML-formatted type of file._
