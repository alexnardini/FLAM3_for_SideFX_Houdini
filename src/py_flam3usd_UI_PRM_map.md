

```python
#   Title:      FLAM3HUSD. SideFX Houdini FLAM3USD: PYTHON MAP PRM Definitions
#   Author:     Alessandro Nardini
#   date:       March 2025, Last revised April 2025
#
#   Name:       PY_FLAM3USD_UI_PRM_MAP
#
#   Comment:    List of all UI parameters wired with a python definition
#               and the command string they actually run and from where.
#
#               THIS IS ONLY INFORMATIVE AND FOR EASY FIND INSTEAD OF
#               NAVIGATING THE PARAMETERS INSIDE THE OTL TYPE PROPERTIES WINDOW.
```


<br>
<br>



The file **`py_flam3usd__(least_needed_python version).py`** are loaded inside the **Extra Files** section. Renamed as **`py_flam3usd__(least_needed_python version)`** (no extension).

For example the file for python 3.11 is renamed<br>
from: **py_flam3usd__3_11.py**<br>
to: **py_flam3usd__3_11**

First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule**:
the **`flam3usd`** module is created out of the **`py_flam3usd`** file from inside the **Extra Files** section.

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
if h < 205: __module__: str = "py_flam3usd__3_7"
else: __module__: str = "py_flam3usd__3_11"

flam3usd = toolutils.createModuleFromSection("flam3usd", kwargs["type"], __module__)
```

Inside: **OTL**->**type_properties**->**Scripts**->**OnCreated**:
initialize what the tool need when you create its node in the network editor.
```python
kwargs["node"].hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_on_create()
```

Inside: **OTL**->**type_properties**->**Scripts**->**OnLoaded**:
When loading a hip file with a FLAM3HUSD node in it do some checks.
```python
kwargs["node"].hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_on_loaded()
```

Inside: **OTL**->**type_properties**->**Scripts**->**OnDeleted**:
When deleting a FLAM3HUSD node.
```python
kwargs["node"].hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_on_deleted()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

_Preferences parameters._

# Prefs Tab
# parameter name:    `sys_help`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).flam3husd_display_help()
```
# Prefs Tab
# parameter name:    `flam3hpath`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_is_valid_flam3h_node()
```
# Prefs Tab
# parameter name:    `setdark`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).colorSchemeDark()
```
# Prefs Tab
# parameter name:    `rndtype`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).setHydraRenderer()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).setHydraRenderer()
```
# Prefs Tab
# parameter name:    `vptype`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleDisplay()
```
# Prefs Tab
# parameter name:    `vpptsize`
### Callback Script
```python
hou.pwd().hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(1.0)
```
# Prefs Tab
# parameter name:    `widths`
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(1.0, 'widths')
```
# Prefs Tab
# parameter name:    `pxsamples`
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(128, 'pxsamples')
```
# Prefs Tab
# parameter name:    `use_f3h_shader`
### Action Button script
```python
kwargs['node'].hdaModule().flam3usd.flam3husd_general_utils(kwargs).reset_flam3h_shader()
```
