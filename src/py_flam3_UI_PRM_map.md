

```python
#   Title:      FLAM3H™. SideFX Houdini FLAM3: PYTHON MAP PRM Definitions
#   Author:     Alessandro Nardini
#   date:       April 2023, Last revised July 2025
#   License:    GPL
#   Copyright:  2021, © F stands for liFe ( made in Italy )
#
#   Name:       PY_FLAM3_UI_PRM_MAP
#
#   Comment:    List of all UI parameters wired with a python definition
#               and the command string they actually run and from where.
#
#               THIS IS ONLY INFORMATIVE AND FOR EASY FIND INSTEAD OF
#               NAVIGATING THE PARAMETERS INSIDE THE OTL TYPE PROPERTIES WINDOW.
```


<br>
<br>



The file **`py_flam3__(least_needed_python version).py`** are loaded inside the **Extra Files** section. Renamed as **`py_flam3__(least_needed_python version)`** (no extension).

For example the file for python 3.11 is renamed<br>
from: **py_flam3__3_11.py**<br>
to: **py_flam3__3_11**

First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule**:
the **`flam3`** module is created out of the **`py_flam3`** file from inside the **Extra Files** section.

# Houdini version:  `H21 and up`
```python
import toolutils

__module__: str = "py_flam3__3_11_H21_UP"
flam3 = toolutils.createModuleFromSection("flam3", kwargs["type"], __module__)
```

# Houdini version:  `H19 to H20.5`
```python
import toolutils

def houdini_version(digit: int=1) -> int:
    """Retrieve the major Houdini version number currently in use.

    Args:
        digit(int): Default to 1: 19, 20. if set to 2: 190, 195, 200, 205, and so on.

    Returns:
        (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
    """ 
    return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))
    
h: int = houdini_version(2)
if h < 205: __module__: str = "py_flam3__3_7"
else: __module__: str = "py_flam3__3_11"
 
flam3 = toolutils.createModuleFromSection("flam3", kwargs["type"], __module__)
```

</br>
</br>

Inside: **OTL**->**type_properties**->**Scripts**->**PreFirstCreate**: Before the node is even created but invoked.

# Houdini version:  `H21 and up`
```python
from datetime import datetime

__version__ = '1.8.70 - Production'

# We are keeping the: py_flam3__3_7 module only for the following reason:
# 
# This is is solely to detect if FLAM3H OTL for H21
# has been loaded inside a Houdini version minor than H20.5.
# Thx to this we can disable the functionalities since it is not a match.
try: hou.session.F3H_H_VERSION_H21
except: hou.session.F3H_H_VERSION_H21: bool = True
else: pass

def houdini_version(digit: int = 1) -> int:
    """Retrieve the major Houdini version number currently in use.

    Args:
        digit(int): Default to 1: 19, 20. if set to 2: 190, 195, 200, 205, and so on.

    Returns:
        (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
    """ 
    return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))

def flam3h_first_time() -> bool:
    """If the version of Houdini running is smaller than version 19 
    will pop up a message to let the user know.

    Args:
        ():

    Returns:
        (None):
    """ 
    hou_version: int = houdini_version(2)
    if hou_version < 210:
        hou.ui.displayMessage("Sorry, you need H21.0.457 and up to run this FLAM3H™ version", buttons=("Got it, thank you",), severity=hou.severityType.Error, default_choice=0, close_choice=-1, help=None, title="Houdini version check", details=None, details_label=None, details_expanded=False)
        return False
    else:
        return True

def flam3h_sys_updated_mode() -> None:
    """Store the current houdini Update mode status into the hou.session
    so FLAM3H™ can pick it up from inside the currently used python module.

    Args:
        ():

    Returns:
        (None):
    """ 
    current: hou.EnumValue = hou.updateModeSetting()
    hou.session.FLAM3H_SYS_UPDATE_MODE: hou.EnumValue = current

def flam3h_compile_first_time_msg() -> None:
    """On first time FLAM3H™ node instance creation:

    - Store the current FLAM3H™ precision mode into the hou.session so FLAM3H™ can pick it up from inside the currently used python module.
    - Additionally build a message to print into the console.

    Args:
        ():

    Returns:
        (None):
    """ 
    now: str = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
    
    h: int = houdini_version()
    __module__: str = "3.11"
    
    try:
        hou.session.FLAM3H_FIRST_INSTANCE_32BIT # type: ignore
        first_instance_32bit: bool = False
    except:
        first_instance_32bit: bool = True
    try:
        hou.session.FLAM3H_FIRST_INSTANCE_64BIT # type: ignore
        first_instance_64bit: bool = False
    except:
        first_instance_64bit: bool = True

    if first_instance_32bit:
        _MSG_INFO = f"\n-> {now}\n\nFLAM3H™ version: {__version__} - F3H Python module: {__module__}\n\nThe CVEX nodes need to cook once to compile their definitions.\nDepending on your PC configuration it can take up to 1(one) minute.\nIt is a one time compile process.\n"
        print(_MSG_INFO)
        hou.ui.setStatusMessage(_MSG_INFO, hou.severityType.Warning) # type: ignore
        
    # we skip 64bit check for now as FLAM3H™ should always be at 32bit to start with.

def flam3h_not_compatible_first_time_msg() -> None:
    """On first time FLAM3H™ node instance creation:

    - Run messages if not compatible with this Houdini version

    Args:
        ():

    Returns:
        (None):
    """ 
    now: str = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
    
    _MSG_INFO = f"\n-> FLAM3H™ version: {__version__}\n\nThis Houdini version is not compatible with this FLAM3H™ version.\nYou need H21.0.457 and up to run this FLAM3H™ version"
    print(_MSG_INFO)
    _MSG_INFO_SB = f"\n-> FLAM3H™ version: {__version__}. This Houdini version is not compatible with this FLAM3H™ version. You need H21.0.457 and up to run this FLAM3H™ version"
    hou.ui.setStatusMessage(_MSG_INFO_SB, hou.severityType.Error) # type: ignore

if flam3h_first_time():
    flam3h_sys_updated_mode()
    flam3h_compile_first_time_msg()
else:
    flam3h_not_compatible_first_time_msg()
```

# Houdini version:  `H19 to H20.5`
```python
from datetime import datetime

__version__ = '1.8.70 - Production'

# This is is solely to detect if a FLAM3H OTL for H21
# has been loaded inside this Houdini session if its version is minor than H20.5.
# If so, we are cxlearing it out.
try: hou.session.F3H_H_VERSION_H21
except: pass
else: del hou.session.F3H_H_VERSION_H21

def houdini_version(digit: int = 1) -> int:
    """Retrieve the major Houdini version number currently in use.

    Args:
        digit(int): Default to 1: 19, 20. if set to 2: 190, 195, 200, 205, 210, and so on.

    Returns:
        (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
    """ 
    return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))

def flam3h_first_time() -> bool:
    """If the version of Houdini running is smaller than version 19 
    will pop up a message to let the user know.

    Args:
        ():

    Returns:
        (None):
    """ 
    hou_version: int = houdini_version(2)
    if hou_version < 190 or hou_version > 205:
        hou.ui.displayMessage("Sorry, you need from H19 to H20.5 to run this FLAM3H™ version", buttons=("Got it, thank you",), severity=hou.severityType.Error, default_choice=0, close_choice=-1, help=None, title="Houdini version check", details=None, details_label=None, details_expanded=False)
        return False
    else:
        return True

def flam3h_sys_updated_mode() -> None:
    """Store the current houdini Update mode status into the hou.session
    so FLAM3H™ can pick it up from inside the currently used python module.

    Args:
        ():

    Returns:
        (None):
    """ 
    current: hou.EnumValue = hou.updateModeSetting()
    hou.session.FLAM3H_SYS_UPDATE_MODE: hou.EnumValue = current

def flam3h_compile_first_time_msg() -> None:
    """On first time FLAM3H™ node instance creation:

    - Store the current FLAM3H™ precision mode into the hou.session so FLAM3H™ can pick it up from inside the currently used python module.
    - Additionally build a message to print into the console.

    Args:
        ():

    Returns:
        (None):
    """ 
    now: str = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
    
    h: int = houdini_version(2)
    if h < 205: __module__: str = "3.7"
    else: __module__: str = "3.11"
    
    try:
        hou.session.FLAM3H_FIRST_INSTANCE_32BIT # type: ignore
        first_instance_32bit: bool = False
    except:
        first_instance_32bit: bool = True
    try:
        hou.session.FLAM3H_FIRST_INSTANCE_64BIT # type: ignore
        first_instance_64bit: bool = False
    except:
        first_instance_64bit: bool = True

    if first_instance_32bit:
        _MSG_INFO = f"\n-> {now}\n\nFLAM3H™ version: {__version__} - F3H Python module: {__module__}\n\nThe CVEX nodes need to cook once to compile their definitions.\nDepending on your PC configuration it can take up to 1(one) minute.\nIt is a one time compile process.\n"
        print(_MSG_INFO)
        hou.ui.setStatusMessage(_MSG_INFO, hou.severityType.Warning) # type: ignore
        
    # we skip 64bit check for now as FLAM3H™ should always be at 32bit to start with.

def flam3h_not_compatible_first_time_msg() -> None:
    """On first time FLAM3H™ node instance creation:

    - Run messages if not compatible with this Houdini version

    Args:
        ():

    Returns:
        (None):
    """ 
    now: str = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
    
    _MSG_INFO = f"\n-> FLAM3H™ version: {__version__}\n\nThis Houdini version is not compatible with this FLAM3H™ version.\nYou need from H19 to H20.5 to run this FLAM3H™ version"
    print(_MSG_INFO)
    _MSG_INFO_SB = f"\n-> FLAM3H™ version: {__version__}. This Houdini version is not compatible with this FLAM3H™ version. You need from H19 to H20.5 to run this FLAM3H™ version"
    hou.ui.setStatusMessage(_MSG_INFO_SB, hou.severityType.Error) # type: ignore

if flam3h_first_time():
    flam3h_sys_updated_mode()
    flam3h_compile_first_time_msg()
else:
    flam3h_not_compatible_first_time_msg()
```

Inside: **OTL**->**type_properties**->**Scripts**->**OnCreated**:
initialize what the tool need when you create its node in the network editor.
```python
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_create()
```

Inside: **OTL**->**type_properties**->**Scripts**->**OnLoaded**:
When loading a hip file with a FLAM3H™ node in it do some checks.
```python
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_loaded()
```

Inside: **OTL**->**type_properties**->**Scripts**->**OnDeleted**:
When deleting a FLAM3H™ node.
```python
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_deleted()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

_Parameters to define the quality of the fractal Flame algorithm solution._

# GLOBAL Tab
# parameter name:    `iter`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_change_iter_num_to_prm()
```
# GLOBAL Tab
# parameter name:    `ptcount_presets`
### Callback script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density_set()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density()
return menu
```
### Action Script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density_set_default()
```
# GLOBAL Tab
# parameter name:    `ptcount_presets_off`
### Action Script
```python
n = None
```


<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

_Tools available to enhance and speed up the workflow.<br>
I keep changing and adding functionalities, it is still a work in progress, but thus far, this most recent configuration has been successful._

# SYS Tab
# parameter name:    `sys_help`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_display_help(), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `iterlist`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_select_iterator(), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_select_iterator()
return menu
```
# SYS Tab
# parameter name:    `doff_sysdisabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("doff"), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `doff_sysenabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("doff"), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `rip_disabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("rip"), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `rip_enabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("rip"), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `f3c_chaotica`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("f3c"), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `f3c_apophysis`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("f3c"), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `xfviz_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_xf_viz_toggle(), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `xfviz_on`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_xf_viz_toggle(), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `xfviz_on_solo`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_sys_xf_viz_solo(), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `xfvizff_on_solo`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_sys_xf_ff_viz_solo(), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `sys_out_sensorviz`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle(), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `sys_out_sensorviz_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle(), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `sys_tag_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("tag"), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `sys_tag`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("tag"), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `tagsize`
### Callback Script
```python
kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `loaddef`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_default()
```
# SYS Tab
# parameter name:    `frameview`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_viewport_bbox_frame(), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `frameviewsensor`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False), kwargs['parm'].deleteAllKeyframes()
```
# SYS Tab
# parameter name:    `sys_palettepresets_disabled`
### Action Button script
```python
n = None
```
# SYS Tab
# parameter name:    `sys_palettepresets_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp_sys(False), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets_empty()
return menu
```
### Action Button Script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()
```
# SYS Tab
# parameter name:    `sys_palettepresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp_sys(False), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets()
return menu
```
### Action Button Script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()
```
# SYS Tab
# parameter name:    `sys_inpresets_disabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_sys(), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets_empty()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
```
# SYS Tab
# parameter name:    `sys_inpresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_sys(), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
```
# SYS Tab
# parameter name:    `sys_outpresets_disabled`
### Action Button script
```python
n = None
```
# SYS Tab
# parameter name:    `sys_outpresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_to_flam3h_quick('SYS'), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_XML()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

_This is where you’ll spend the majority of your time, along with the FF Tab.<br>
Here you will create your fractal Flame logic.<br>Since every parameter has the same name inside, if you have ever used Apophysis, Fractorium, or other fractal Flame editors, you will almost immediately feel at home. The logic you will operate with will be the same._

# FLAME Tab
# parameter name:    `flamefunc`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterators_count()
```
# FLAME Tab
# parameter name:    `mp_add_#` -> _only from H21 up_
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).add_iterator()
```
# FLAME Tab
# parameter name:    `note_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).destroy_data_note(), kwargs['parm'].deleteAllKeyframes()
```
# FLAME Tab
# parameter name:    `doiter_disabled_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_vactive_and_update(), kwargs['parm'].deleteAllKeyframes()
```
# FLAME Tab
# parameter name:    `doiter_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_vactive_and_update(), kwargs['parm'].deleteAllKeyframes()
```
# FLAME Tab
# parameter name:    `xfviz_off_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_mp_xf_viz(), kwargs['parm'].deleteAllKeyframes()
```
# FLAME Tab
# parameter name:    `xfviz_on_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_mp_xf_viz(), kwargs['parm'].deleteAllKeyframes()
```
# FLAME Tab
# parameter name:    `iw_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_vactive_and_update()
```
# FLAME Tab
# parameter name:    `prmpastesel_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel(), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste()
return menu
```
# FLAME Tab
# parameter name:    `xaos_#`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_ui_msg_utils(kwargs).ui_xaos_infos()
return menu
```
# FLAME Tab
# parameter name:    `alpha_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils.destroy_cachedUserData(kwargs['node'], 'iter_sel')
```
# FLAME Tab
# parameter name:    `preblurtype_#`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T_pb()
return menu
```
# FLAME Tab
# parameter name:    `pre1type_#`, `pre2type_#` and `p1type_#`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T_PP()
return menu
```
# FLAME Tab
# parameter name:    `v1type_#`, `v2type_#`, `v3type_#`, `v4type_#`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T()
return menu
```
# FLAME Tab
# parameter name:    `scl_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_affine_scale()
```
### Action Button script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_pre_affine()
```
# FLAME Tab
# parameter name:    `ang_#`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_preaffine()
```
# FLAME Tab
# parameter name:    `pscl_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_post_affine_scale()
```
### Action Button script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_post_affine()
```
# FLAME Tab
# parameter name:    `pang_#`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_postaffine()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

_Iterators like Final Flame (FF) or finalXform function like camera lenses.<br>
It allows for a great deal of creative experimentation by taking the combined result of all the iterators inside the FLAME Tab and applying further modifications to that result._

# FF Tab
# parameter name:    `doff_disabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("doff"), kwargs['parm'].deleteAllKeyframes()
```
# FF Tab
# parameter name:    `doff_enabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_private("doff"), kwargs['parm'].deleteAllKeyframes()
```
# FF Tab
# parameter name:    `xfvizff_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_xf_ff_viz(), kwargs['parm'].deleteAllKeyframes()
```
# FF Tab
# parameter name:    `xfvizff_on`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_xf_ff_viz(), kwargs['parm'].deleteAllKeyframes()
```
# FF Tab
# parameter name:    `ffnote`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).note_FF(), kwargs['parm'].deleteAllKeyframes()
```
# FF Tab
# parameter name:    `ffprmpastesel`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_FF(), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste_FF()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_FF()
```
# FF Tab
# parameter name:    `ffpre1type` and `ffp1type`, `ffp2type`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils.menu_T_PP(True)
return menu
```
# FF Tab
# parameter name:    `ffv1type`, `ffv2type`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils.menu_T(True)
return menu
```
# FF Tab
# parameter name:    `ffscl`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_FF_affine_scale()
```
### Action Button script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_pre_affine_FF()
```
# FF Tab
# parameter name:    `ffang`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_preaffine_FF()
```
# FF Tab
# parameter name:    `ffpscl`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_FF_post_affine_scale()
```
### Action Button script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_post_affine_FF()
```
# FF Tab
# parameter name:    `ffpang`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_postaffine_FF()
```

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
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_hsv()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).reset_CP(2)
```
# CP Tab
# parameter name:    `palettehsv`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_lock()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).palette_cp()
```
# CP Tab
# parameter name:    `cp_lookupsamples`
### Callback Script
```python
kwargs['parm'].deleteAllKeyframes()
```
# CP Tab
# parameter name:    `palette`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_cp(True)
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).reset_CP(3)
```
# CP Tab
# parameter name:    `palettefile`
### Callbac Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets_CP_PRESETS(), kwargs['parm'].deleteAllKeyframes()
```
# CP Tab
# parameter name:    `palettename`
### Callbac Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).cp_preset_name_set(), kwargs['parm'].deleteAllKeyframes()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).flam3h_ramp_save()
```
# CP Tab
# parameter name:    `palettepresets_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp(False), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets_empty()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()
```
# CP Tab
# parameter name:    `palettepresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp(False), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()
```

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

# MB Tab
# parameter name:    `domb`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_general_utils(kwargs).reset_MB(False)
```

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

# IN Tab
# parameter name:    `inpath`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets_IN_PRESETS(), kwargs['parm'].deleteAllKeyframes()
```
# IN Tab
# parameter name:    `inpresets_disabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h(), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets_empty()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
```
# IN Tab
# parameter name:    `inpresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h(), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
```
# IN Tab
# parameter name:    `iternumonload`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).set_iter_on_load_callback()
```
# IN Tab
# parameter name:    `useiteronload`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).use_iter_on_load_callback()
```
# IN Tab
# parameter name:    `oritername`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).use_iter_on_load_callback()
```
# IN Tab
# parameter name:    `in_f3h_affine`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_toggle_f3h_affine()
```
# IN Tab
# parameter name:    `propertiescp`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_toggle("propertiescp")
```
# IN Tab
# parameter name:    `cprendervals`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_all_stats_msg(kwargs, None, False, True), kwargs['parm'].deleteAllKeyframes()
```
# IN Tab
# parameter name:    `cprendervals_cb`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_all_stats_msg(kwargs, None, False, True), kwargs['parm'].deleteAllKeyframes()
```
# IN Tab
# parameter name:    `icon_in_infos_sensor`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_sensor_stats_msg(kwargs)
```
# IN Tab
# parameter name:    `icon_in_infos_render`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_stats_msg(kwargs)
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

_Inside here, you can export your fractal Flame into an XML format ( standard *.flame file format ) and reload it inside FLAM3H™ or inside Apophysis, Fractorium and others.<br>
The Flame file format does not support animations, but only static frames, so to speak. If you animated your fractal Flame, save the hip file from Houdini instead._

# OUT Tab
# parameter name:    `outpath`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets_OUT_PRESETS(), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `outname`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_add_iter_num_to_prm(), kwargs['parm'].deleteAllKeyframes()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_XML()
```
# OUT Tab
# parameter name:    `outpresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_to_flam3h_quick(), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_presets_copy_menu_label_callback()
```
# OUT Tab
# parameter name:    `out_in_flame_name`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_flame_name_inherit_on_load()
```
# OUT Tab
# parameter name:    `autoadditer`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_change_iter_num_to_prm()
```
# OUT Tab
# parameter name:    `outedit`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_off("outsensor"), kwargs['parm'].deleteAllKeyframes()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).reset_OUT_kwargs()
```
# OUT Tab
# parameter name:    `out_sensorviz_disabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle(), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `out_sensorviz`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle(), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
'parameter name:    `out_sensorviz_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle(), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `outres`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```
# OUT Tab
# parameter name:    `outrespresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).menu_sensor_resolution_set(False), kwargs['parm'].deleteAllKeyframes()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_sensor_resolution()
return menu
```
# OUT Tab
# parameter name:    `outcprendervals`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_all_stats_msg(kwargs, None, False, True), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `outcenter`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```
# OUT Tab
# parameter name:    `outrotate`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```
# OUT Tab
# parameter name:    `outscale`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```
# OUT Tab
# parameter name:    `outsensorupdate`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `outccdefault`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils.out_render_curves_compare_and_set_toggle(kwargs['node']), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `icon_f3h_cc_defaults_copy`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_cc_curves_stats_msg(kwargs), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `icon_f3h_cc_modified_reset`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils.out_render_curves_set_and_retrieve_defaults(kwargs['node']), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `outcurvesval`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils.out_render_curves_retrive_data(kwargs['node']), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `outcurveoverallval`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils.out_render_curves_retrive_data(kwargs['node']), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `outcurveredval`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils.out_render_curves_retrive_data(kwargs['node']), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `outcurvegreenval`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils.out_render_curves_retrive_data(kwargs['node']), kwargs['parm'].deleteAllKeyframes()
```
# OUT Tab
# parameter name:    `outcurveblueval`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils.out_render_curves_retrive_data(kwargs['node']), kwargs['parm'].deleteAllKeyframes()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


# prefs Tab
# parameter name:    `prefspaletteplus`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_palette_256_plus_check()
```
# prefs Tab
# parameter name:    `ptcount`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils.flam3h_on_loaded_set_density_menu(kwargs['node'])
```
# prefs Tab
# parameter name:    `enumeratemenu`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).menus_refresh_enum_prefs(), kwargs['parm'].deleteAllKeyframes()
```
# prefs Tab
# parameter name:    `itericons`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).refresh_iterator_vars_menu(), kwargs['parm'].deleteAllKeyframes()
```
# prefs Tab
# parameter name:    `xm`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_xaos_convert(), kwargs['parm'].deleteAllKeyframes()
```
# prefs Tab
# parameter name:    `vex_precision`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_scripts(kwargs).flam3h_check_first_node_instance_prefs_cvex_precision_msg()
```
# prefs Tab
# parameter name:    `autoxaos`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).auto_set_xaos()
```
# prefs Tab
# parameter name:    `setdark`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).colorSchemeDark(), kwargs['parm'].deleteAllKeyframes()
```
# prefs Tab
# parameter name:    `vpww`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).viewportWireWidth()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_general_utils(kwargs).viewportWireWidth(1.0)
```
# prefs Tab
# parameter name:    `vptype`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleDisplay(), kwargs['parm'].deleteAllKeyframes()
```
# prefs Tab
# parameter name:    `vpptsize`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleSize()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleSize(1.0)
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


# about Tab
# parameter name:    `flam3homepage`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('web')
```
# about Tab
# parameter name:    `flam3github`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('git')
```
# about Tab
# parameter name:    `flam3insta`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('insta')
```
# about Tab
# parameter name:    `flam3youtube`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('youtube')
```
# about Tab
# parameter name:    `tffa_pdf`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('paper')
```
# about Tab
# parameter name:    `tffa_flam3github`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('flam3git')
```
# about Tab
# parameter name:    `fract_bit`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('bitbucket')
```
# about Tab
# parameter name:    `fract_web`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('fractweb')
```
