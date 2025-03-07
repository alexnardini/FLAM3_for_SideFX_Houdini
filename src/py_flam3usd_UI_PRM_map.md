

```python
#   Title:      FLAM3HUSD. SideFX Houdini FLAM3USD: PYTHON MAP PRM Definitions
#   Author:     Alessandro Nardini
#   date:       March 2025, Last revised March 2025
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



The file **`py_flam3usd.py`** is loaded inside the **Extra Files** section. Renamed as **`py_flam3usd`** (no extension).

First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule**:
the **`flam3usd`** module is created out of the **`py_flam3usd`** file from inside the **Extra Files** section.

```python
import toolutils
flam3usd = toolutils.createModuleFromSection("flam3usd", kwargs["type"], "py_flam3usd")
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
When deleting a FLAM3H node.
```python
kwargs["node"].hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3h_on_deleted()
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
