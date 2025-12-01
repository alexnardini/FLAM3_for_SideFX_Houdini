```python
#   Title:      FLAM3HUSD. SideFX Houdini FLAM3USD: PYTHON MAP PRM Definitions
#   Author:     F stands for liFe ( made in Italy )
#   date:       March 2025, Last revised November 2025
#   License:    GPL
#   Copyright:  2023, © F stands for liFe ( made in Italy )
#
#   Name:       PY_FLAM3USD__UI_PARM_MAP
#
#   Comment:    List of all the UI parameters wired with a python definition
#               and the command string they actually run and from where.
#
#               THIS IS ONLY INFORMATIVE AND FOR EASY FIND INSTEAD OF
#               NAVIGATING THE PARAMETERS INSIDE THE OTL TYPE PROPERTIES WINDOW.
```
- #### THIS FILE IS ONLY INFORMATIVE and part of the Documentations
- #### Houdini versions:  `H19 to H20.5`

</br>
</br>

#### Quick links

- **FLAM3HUSD** [**UI_ICON_map**](FLAM3HUSD__UI_ICON_map.md)
- **FLAM3HUSD** [**UI_PARM_map H21 UP**](py_flam3usd__UI_PARM_map_H21_UP.md)

</br>

- **FLAM3H™** [**UI_ICON_map**](FLAM3H__UI_ICON_map.md)
- **FLAM3H™** [**UI_PARM_map H21 UP**](py_flam3__UI_PARM_map_H21_UP.md)
- **FLAM3H™** [**UI_PARM_map H19 to H20.5**](py_flam3__UI_PARM_map_H19_to_H205.md)

</br>

- [**FULL ICON set**](../icons/README.md)

<br>
<br>
<br>
<br>

# FLAM3HUSD -> UI_PARM_map
- ### Contents
    - _Collection of all the python modules run by the tool inside the HDA Type properties -> Script tab_.
    - _List of all the UI parameters wired with a python definition and the command string they actually run and from where_.

<br>
<br>
<br>
<br>

The needed **`py_flam3usd__x_x.py`** files are loaded inside the **Extra Files** section. Renamed as **`py_flam3usd__x_x`** (no extension).

For example the file for python 3.11 is renamed<br>
from: **py_flam3usd__3_11.py**<br>
to: **py_flam3usd__3_11**

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> PythonModule `H20.5`

| SCRIPT | Description | 
|:---|:---|
| **PythonModule** | The **`flam3usd`** module is created out of the **`py_flam3usd`** file located inside the **Extra Files** section.</br>First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule*** | 


```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

import toolutils

# Set some HDA infos
__version__ = "0.2.34"
__status__ = "Prototype"
__h_versions__: tuple = (205,)
__range_type__: bool = True # True for closed range. False for open range

# The following are min and max Houdini version where FLAM3HUSD can run.
# The max version is always most likely the latest Houdini version released by SideFX
# unless it is a closed range due to moving into newer Houdini and FLAM3HUSD versions.
#
# The ranges can be open or close inside this definition:
# - (py_flam3usd__3_11) -> def flam3husd_compatible_type(self, range_type: bool, kwargs: dict | None = None, msg: bool = True) -> bool:
# - (py_flam3usd__3_7)  -> def flam3husd_compatible_type(self, range_type: bool, kwargs: Union[dict, None] = None, msg: bool = True) -> bool:
__h_version_min__: int = 190
__h_version_max__: int = __h_versions__[-1]

def houdini_version(digit: int=1) -> int:
    """Retrieve the major Houdini version number currently in use.

    Args:
        digit(int): Default to 1: 19, 20. if set to 2: 190, 195, 200, 205, and so on.

    Returns:
        (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
    """ 
    return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))
    
h: int = houdini_version(2)
if h < 205: __module__: str = "py_flam3usd__3_7"
else: __module__: str = "py_flam3usd__3_11"

flam3usd = toolutils.createModuleFromSection("flam3usd", kwargs["type"], __module__)
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> PythonModule `H19 to H20`

| SCRIPT | Description | 
|:---|:---|
| **PythonModule** | The **`flam3usd`** module is created out of the **`py_flam3usd`** file located inside the **Extra Files** section.</br>First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule** | 

```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

import toolutils

# Set some HDA infos
__version__ = "0.2.34"
__status__ = "Prototype"
__h_versions__: tuple = (190, 195, 200)
__range_type__: bool = True # True for closed range. False for open range

# The following are min and max Houdini version where FLAM3HUSD can run.
# The max version is always most likely the latest Houdini version released by SideFX
# unless it is a closed range due to moving into newer Houdini and FLAM3HUSD versions.
#
# The ranges can be open or close inside this definition:
# - (py_flam3usd__3_11) -> def flam3husd_compatible_type(self, range_type: bool, kwargs: dict | None = None, msg: bool = True) -> bool:
# - (py_flam3usd__3_7)  -> def flam3husd_compatible_type(self, range_type: bool, kwargs: Union[dict, None] = None, msg: bool = True) -> bool:
__h_version_min__: int = 190
__h_version_max__: int = __h_versions__[-1]

def houdini_version(digit: int=1) -> int:
    """Retrieve the major Houdini version number currently in use.

    Args:
        digit(int): Default to 1: 19, 20. if set to 2: 190, 195, 200, 205, and so on.

    Returns:
        (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
    """ 
    return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))
    
h: int = houdini_version(2)
if h < 205: __module__: str = "py_flam3usd__3_7"
else: __module__: str = "py_flam3usd__3_11"

flam3usd = toolutils.createModuleFromSection("flam3usd", kwargs["type"], __module__)
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> PreFirstCreate `H19 to H20.5`

| SCRIPT | Description | 
|:---|:---|
| **PreFirstCreate** | Before the node is even created but invoked.</br>Inside: **OTL**->**type_properties**->**Scripts**->**PreFirstCreate** | 



```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

from datetime import datetime

# Get some HDA infos from the HDA module
FLAM3HUSD_NODE_TYPE_NAME_CATEGORY = 'alexnardini::Lop/FLAM3HUSD'
nodetype = hou.nodeType(FLAM3HUSD_NODE_TYPE_NAME_CATEGORY)
__version__ = nodetype.hdaModule().__version__
__status__ = nodetype.hdaModule().__status__
__h_versions__: tuple = nodetype.hdaModule().__h_versions__
__range_type__: bool = nodetype.hdaModule().__range_type__
__h_version_min__: int = nodetype.hdaModule().__h_version_min__


def flam3husd_first_time() -> bool:
    """If the version of Houdini running is not allowed for this FLAM3HUSD HDA version (different cases)
    will return False, otherwise will return True.

    Args:
        ():

    Returns:
        (bool): True if compatible and False if not.
    """ 
    hou_version: int = nodetype.hdaModule().houdini_version(2)

    if hou_version < __h_version_min__:
        return False
    
    elif __range_type__ is True:
        if hou_version < __h_versions__[0] or hou_version > __h_versions__[-1]:
            return False
        else:
            return True
        
    elif __range_type__ is False:
        if hou_version < __h_versions__[0]:
            return False
        else:
            return True
        
    else:
        return True


def flam3husd_not_compatible_first_time_msg() -> None:
    """On first time FLAM3HUSD node instance creation:

    Run messages if not compatible with this Houdini version.
    
    Compatibility is checked inside:
    * def flam3h_first_time() -> bool:

    Args:
        ():

    Returns:
        (None):
    """ 
    
    _MSG_H_VERSIONS = nodetype.hdaModule().flam3usd.flam3husd_scripts.flam3husd_compatible_h_versions_msg(__h_versions__, False)
    _MSG_INFO = f"\n-> FLAM3HUSD version: {__version__} - {__status__}\n\nThis Houdini version is not compatible with this FLAM3HUSD version.\nYou need {_MSG_H_VERSIONS} to run this FLAM3HUSD version"
            
    if hou.isUIAvailable():

        print(_MSG_INFO)

        _MSG_INFO_SB = f"-> FLAM3HUSD version: {__version__} - {__status__}. This Houdini version is not compatible with this FLAM3HUSD version. You need {_MSG_H_VERSIONS} to run this FLAM3HUSD version"
        hou.ui.setStatusMessage(_MSG_INFO_SB, hou.severityType.Error) # type: ignore

        hou.ui.displayMessage(f"Sorry, you need {_MSG_H_VERSIONS} to run this FLAM3HUSD version", buttons=("Got it, thank you",), severity=hou.severityType.Error, default_choice=0, close_choice=-1, help=None, title="FLAM3HUSD Houdini version check", details=None, details_label=None, details_expanded=False)

    else:
        print(_MSG_INFO)


if not flam3husd_first_time():
    flam3husd_not_compatible_first_time_msg()
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> OnCreated `H19 to H20.5`

| SCRIPT | Description | 
|:---|:---|
| **OnCreated** | Initialize what the tool need when you create its node in the network editor.</br>Inside: **OTL**->**type_properties**->**Scripts**->**OnCreated** | 

```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

kwargs["node"].hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_on_create()
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> OnLoaded `H19 to H20.5`

| SCRIPT | Description | 
|:---|:---|
| **OnLoaded** | When loading hip files with FLAM3HUSD nodes in it do some checks.</br>Inside: **OTL**->**type_properties**->**Scripts**->**OnLoaded** | 

```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

kwargs["node"].hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_on_loaded()
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> OnDeleted `H19 to H20.5`

| SCRIPT | Description | 
|:---|:---|
| **OnLoaded** | When deleting a FLAM3HUSD node.</br>Inside: **OTL**->**type_properties**->**Scripts**->**OnDeleted** | 

```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

kwargs["node"].hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_on_deleted()
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

_FLAM3HUSD system utilities._

</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **SYS** | `sys_help` | `button` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).flam3husd_display_help(), hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```
</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **SYS** | `sys_reframe` | `button` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_viewport_bbox_frame(), hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **SYS** | `flam3hpath` | `operator path` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_is_valid_flam3h_node(), kwargs['parm'].deleteAllKeyframes()
```
- ### <img width="16" height="16" src="../icons/icon_actionButtonSVG.svg" /> Action Button Script
```python
node = kwargs['node']
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_cycle_import()
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)

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

_Here you will play with the main settings of FLAM3HUSD._

</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `setdark` | `toggle` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).colorSchemeDark(), kwargs['parm'].deleteAllKeyframes(), hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `rndtype` | `ordered menu` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).setHydraRenderer(), kwargs['parm'].deleteAllKeyframes(), hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```
- ### <img width="16" height="16" src="../icons/icon_actionButtonSVG.svg" /> Action Button Script
```python
node = kwargs['node']
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).setHydraRenderer()
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `vptype` | `ordered menu` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleDisplay(), kwargs['parm'].deleteAllKeyframes(), hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `vpptsize` | `float` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize()
```
- ### <img width="16" height="16" src="../icons/icon_actionButtonSVG.svg" /> Action Button Script
```python
node = kwargs['node']
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(1.0)
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `widths` | `float` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_actionButtonSVG.svg" /> Action Button Script
```python
node = kwargs['node']
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(1.0, 'widths')
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `xfviz` | `toggle` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `widths_xf_viz` | `float` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_actionButtonSVG.svg" /> Action Button Script
```python
node = kwargs['node']
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(2.0, 'widths_xf_viz')
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `pxsamples_cpu` | `integer` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_actionButtonSVG.svg" /> Action Button Script
```python
node = kwargs['node']
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(128, 'pxsamples_cpu')
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `denoiser` | `string` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
kwargs['parm'].deleteAllKeyframes(), hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `use_f3h_shader` | `toggle` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```
- ### <img width="16" height="16" src="../icons/icon_actionButtonSVG.svg" /> Action Button Script
```python
node = kwargs['node']
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).reset_flam3h_shader()
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `tonemap` | `string` | `H19 to H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
kwargs['parm'].deleteAllKeyframes(), hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>


