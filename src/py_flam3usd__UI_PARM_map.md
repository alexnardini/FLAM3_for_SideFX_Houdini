```python
#   Title:      FLAM3HUSD. SideFX Houdini FLAM3USD: PYTHON MAP PRM Definitions
#   Author:     Alessandro Nardini
#   date:       March 2025, Last revised September 2025
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
</br>
</br>

#### Quick links

- **FLAM3HUSD** [**UI_ICON_map**](FLAM3HUSD__UI_ICON_map.md)

</br>

- **FLAM3H™** [**UI_ICON_map**](FLAM3H__UI_ICON_map.md)
- **FLAM3H™** [**UI_PARM_map**](py_flam3__UI_PARM_map.md)

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

# PythonModule - Houdini version: `H21 UP`
The **`flam3usd`** module is created out of the **`py_flam3usd`** file located inside the **Extra Files** section.</br>
First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule**

```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

import toolutils

# Set some HDA infos
__version__ = "0.1.80"
__status__ = "Prototype"
__h_versions__: tuple = (210,)
__range_type__: bool = False # True for closed range. False for open range

# The following are min and max Houdini version where FLAM3HUSD can run.
# The max version is always most likely the latest Houdini version released by SideFX
# unless it is a closed range due to moving into newer Houdini and FLAM3HUSD versions.
#
# The ranges can be open or close inside this definition:
# - (py_flam3usd__3_11_H21_UP) -> def flam3husd_compatible_type(self, range_type: bool, kwargs: dict | None = None, msg: bool = True) -> bool:
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
else: __module__: str = "py_flam3usd__3_11_H21_UP"

flam3usd = toolutils.createModuleFromSection("flam3usd", kwargs["type"], __module__)
```

</br>
</br>
</br>

# PythonModule - Houdini version: `H20.5`
The **`flam3usd`** module is created out of the **`py_flam3usd`** file located inside the **Extra Files** section.</br>
First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule**

```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

import toolutils

# Set some HDA infos
__version__ = "0.1.80"
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

# PythonModule - Houdini version: `H19 to H20`
The **`flam3usd`** module is created out of the **`py_flam3usd`** file located inside the **Extra Files** section.</br>
First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule**

```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

import toolutils

# Set some HDA infos
__version__ = "0.1.80"
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

# PreFirstCreate
Before the node is even created but invoked.</br>
Inside: **OTL**->**type_properties**->**Scripts**->**PreFirstCreate**

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

# OnCreated
Initialize what the tool need when you create its node in the network editor.</br>
Inside: **OTL**->**type_properties**->**Scripts**->**OnCreated**
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

# OnLoaded
When loading hip files with FLAM3HUSD nodes in it do some checks.</br>
Inside: **OTL**->**type_properties**->**Scripts**->**OnLoaded**
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

# OnDeleted
When deleting a FLAM3HUSD node.</br>
Inside: **OTL**->**type_properties**->**Scripts**->**OnDeleted**
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




# SYS Tab
# parameter name:    `sys_help`
## parameter type: `button`
- ### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).flam3husd_display_help()
```
</br>
</br>

_Here you will play with the main settings of FLAM3HUSD._

# SYS Tab
# parameter name:    `sys_reframe`
## parameter type: `button`
- ### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_viewport_bbox_frame()
```


</br>
</br>

# SYS Tab
# parameter name:    `flam3hpath`
## parameter type: `operator path`
- ### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_is_valid_flam3h_node()
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

# PREFS Tab
# parameter name:    `setdark`
## parameter type: `toggle`
- ### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).colorSchemeDark()
```

</br>
</br>

# PREFS Tab
# parameter name:    `rndtype`
## parameter type: `ordered menu`
- ### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).setHydraRenderer()
```
- ### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).setHydraRenderer()

```

</br>
</br>

# PREFS Tab
# parameter name:    `vptype`
## parameter type: `ordered menu`
- ### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleDisplay()
```

</br>
</br>

# PREFS Tab
# parameter name:    `vpptsize`
## parameter type: `float`
- ### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize()
```
- ### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(1.0)
```

</br>
</br>

# PREFS Tab
# parameter name:    `widths`
## parameter type: `float`
- ### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(1.0, 'widths')
```

</br>
</br>

# PREFS Tab
# parameter name:    `widths_xf_viz`
## parameter type: `float`
- ### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(2.0, 'widths_xf_viz')
```


</br>
</br>

# PREFS Tab
# parameter name:    `pxsamples`
## parameter type: `integer`
- ### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(128, 'pxsamples')
```

</br>
</br>

# PREFS Tab
# parameter name:    `use_f3h_shader`
## parameter type: `toggle`
- ### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).reset_flam3h_shader()
```
