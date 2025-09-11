```python
#   Title:      FLAM3HUSD. SideFX Houdini FLAM3USD: PYTHON MAP PRM Definitions
#   Author:     Alessandro Nardini
#   date:       March 2025, Last revised April 2025
#   License:    GPL
#   Copyright:  2023, © F stands for liFe ( made in Italy )
#
#   Name:       PY_FLAM3USD__UI_PRM_MAP
#
#   Comment:    List of all UI parameters wired with a python definition
#               and the command string they actually run and from where.
#
#               THIS IS ONLY INFORMATIVE AND FOR EASY FIND INSTEAD OF
#               NAVIGATING THE PARAMETERS INSIDE THE OTL TYPE PROPERTIES WINDOW.
```

<br>
<br>

The file **`py_flam3usd__x_x.py`** are loaded inside the **Extra Files** section. Renamed as **`py_flam3usd__x_x`** (no extension).

For example the file for python 3.11 is renamed<br>
from: **py_flam3usd__3_11.py**<br>
to: **py_flam3usd__3_11**

</br>
</br>
</br>

# PythonModule Houdini version `H21 and up`
The **`flam3usd`** module is created out of the **`py_flam3usd`** file from inside the **Extra Files** section.</br>
First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule**

```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

import toolutils

# Set some HDA infos
__version__ = "0.1.63"
__status__ = "Prototype"

__module__: str = "py_flam3usd__3_11_H21_UP"
flam3usd = toolutils.createModuleFromSection("flam3usd", kwargs["type"], __module__)
```

</br>
</br>
</br>

# PythonModule Houdini version `H19 to H20.5`
The **`flam3usd`** module is created out of the **`py_flam3usd`** file from inside the **Extra Files** section.</br>
First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule**

```python
#   Title:      FLAM3HUSD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe

import toolutils

# Set some HDA infos
__version__ = "0.1.60"
__status__ = "Prototype"

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

_Preferences parameters._

# Prefs Tab
# parameter name:    `sys_help`
## type: `button`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).flam3husd_display_help()
```

</br>
</br>

# Prefs Tab
# parameter name:    `flam3hpath`
## type: `operator path`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_is_valid_flam3h_node()
```

</br>
</br>

# Prefs Tab
# parameter name:    `setdark`
## type: `toggle`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).colorSchemeDark()
```

</br>
</br>

# Prefs Tab
# parameter name:    `rndtype`
## type: `ordered menu`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).setHydraRenderer()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).setHydraRenderer()

```

</br>
</br>

# Prefs Tab
# parameter name:    `vptype`
## type: `ordered menu`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleDisplay()
```

</br>
</br>

# Prefs Tab
# parameter name:    `vpptsize`
## type: `float`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(1.0)
```

</br>
</br>

# Prefs Tab
# parameter name:    `widths`
## type: `float`
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(1.0, 'widths')
```

</br>
</br>

# Prefs Tab
# parameter name:    `pxsamples`
## type: `integer`
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(128, 'pxsamples')
```

</br>
</br>

# Prefs Tab
# parameter name:    `use_f3h_shader`
## type: `toggle`
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).reset_flam3h_shader()

```
