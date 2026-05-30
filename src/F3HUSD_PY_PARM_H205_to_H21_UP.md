```python
#   Title:      FLAM3H™USD. SideFX Houdini FLAM3USD: PYTHON MAP PRM Definitions
#   Author:     F stands for liFe ( made in Italy )
#   date:       March 2025, Last revised June 2026
#   License:    GPL
#   Copyright:  2023, © F stands for liFe ( made in Italy )
#
#   Name:       F3HUSD_PY_PARM_H205_to_H21_UP
#
#   Comment:    List of all the UI parameters wired with a python definition
#               and the command string they actually run and from where.
#
#               THIS IS ONLY INFORMATIVE AND FOR EASY FIND INSTEAD OF
#               NAVIGATING THE PARAMETERS INSIDE THE OTL TYPE PROPERTIES WINDOW.
```

<br>
<br>

# FLAM3H™USD -> PY_PARM_map

- #### Houdini versions:  `H20.5 to H21 UP`
- ### Contents
    - _Collection of all the python modules run by the tool inside the HDA Type properties -> Script tab_.
    - _List of all the UI parameters wired with a python definition and the command string they actually run and from where_.

- #### THIS FILE IS ONLY INFORMATIVE and part of the Documentations

</br>
</br>

- #### Quick links

    - **FLAM3H™USD** [**UI_ICON_map**](F3HUSD_UI_ICON.md)
    - **FLAM3H™USD** [**PY_PARM_map H19.0 to H20.0**](F3HUSD_PY_PARM_H19_to_H20.md)

    </br>

    - **FLAM3H™** [**UI_ICON_map H19.0 to H20.0**](F3H_UI_ICON_H19_to_H20.md)
    - **FLAM3H™** [**UI_ICON_map H20.5 to H21.0 UP**](F3H_UI_ICON_H205_to_H21_UP.md)
    - **FLAM3H™** [**PY_PARM_map H19.0 to H20.0**](F3H_PY_PARM_H19_to_H20.md)
    - **FLAM3H™** [**PY_PARM_map H20.5 to H21.0 UP**](F3H_PY_PARM_H205_to_H21_UP.md)

    </br>

    - [**FULL ICON set**](../icons/README.md)

<br>
<br>
<br>
<br>

# Contents

<br>

The needed **`py_flam3usd__x_x.py`** files are loaded inside the **Extra Files** section. Renamed as **`py_flam3usd__x_x`** (no extension).

For example the file for python 3.11 is renamed<br>
from: **py_flam3usd__3_11.py**<br>
to: **py_flam3usd__3_11**

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> PythonModule `H21 UP`

| SCRIPT | Description | 
|:---|:---|
| **PythonModule** | The **`flam3usd`** module is created out of the **`py_flam3usd`** file located inside the **Extra Files** section.</br>First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule** | 

```python

# ███████╗██╗░░░░░░█████╗░███╗░░░███╗██████╗░██╗░░██╗██╗░░░██╗░██████╗██████╗░
# ██╔════╝██║░░░░░██╔══██╗████╗░████║╚════██╗██║░░██║██║░░░██║██╔════╝██╔══██╗
# █████╗░░██║░░░░░███████║██╔████╔██║░█████╔╝███████║██║░░░██║╚█████╗░██║░░██║
# ██╔══╝░░██║░░░░░██╔══██║██║╚██╔╝██║░╚═══██╗██╔══██║██║░░░██║░╚═══██╗██║░░██║
# ██║░░░░░███████╗██║░░██║██║░╚═╝░██║██████╔╝██║░░██║╚██████╔╝██████╔╝██████╔╝
# ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═════╝░
#
#   Title:      FLAM3H™USD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe
#
#   File:       PythonModule

import toolutils

# Set some HDA infos
__v__ = 0
__version__ = "0.2.56"
__status__ = "Prototype"
# Note:
# The intgers contained into this __h_versions__ tuple must be Houdini version numbers composed of 3 digits:
# 190, 195, 200, 205, 210 and so on.
__h_versions__: tuple = (210,)
__range_type__: bool = False # True for closed range. False for open range


def is_nonempty_int_tuple(value: tuple) -> bool:
    """Check if a tuple contain only integers.</br>
    This is done to be sure the FLAM3H™ dunder data: __h_versions__ is valid.</br>
    
    Note:
        The intgers contained into this __h_versions__ tuple must be Houdini version numbers composed of 3 digits:
        - 190, 195, 200, 205, 210 and so on.

    Args:
        value(str): The tuple to check</br>

    Returns:
        (bool): True if it contain only integers and False if not (including if empty)
    """
    return (
            isinstance(value, tuple) and
            len(value) > 0 and
            all(type(x) is int and len(str(abs(x))) == 3 for x in value)
    )

# The following are min and max Houdini version where FLAM3H™ can run.
# The max version is always most likely the latest Houdini version released by SideFX
# unless it is a closed range due to moving into newer Houdini and FLAM3H™ versions.
#
# The ranges can be open or close inside this definition:
# - (py_flam3usd__3_11) -> def flam3husd_compatible_type(self, range_type: bool, kwargs: dict | None = None, msg: bool = True) -> bool:
# - (py_flam3usd__3_7)  -> def flam3husd_compatible_type(self, range_type: bool, kwargs: Union[dict, None] = None, msg: bool = True) -> bool:
__h_version_min__: int = 190
try:
    __h_version_max__: int = __h_versions__[-1]
    if not is_nonempty_int_tuple(__h_versions__):
        __h_version_min__: int = 999
        __h_version_max__: int = __h_version_min__
except:
    __h_version_min__: int = 999
    __h_version_max__: int = __h_version_min__


def houdini_version(digit: int=1) -> int:
    """Retrieve the major Houdini version number currently in use.

    Args:
        digit(int): Default to 1: 19, 20. if set to 2: 190, 195, 200, 205, and so on.

    Returns:
        (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
    """ 
    return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))
    

def py_module_vars() -> str:
    """Return a strings:</br>
    * __module_filename__ -> module filename to use

    Args:
        (None):
        
    Returns:
        (None):
    """ 
    h: int = houdini_version(2)
    if h < 205: 
        __module_filename__: str = "py_flam3usd__3_7"
    else:
        __module_filename__: str = "py_flam3usd__3_11_H21_UP"

    return __module_filename__


__module_filename__ = py_module_vars()
flam3usd = toolutils.createModuleFromSection("flam3usd", kwargs["type"], __module_filename__)
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> PythonModule `H20.5`

| SCRIPT | Description | 
|:---|:---|
| **PythonModule** | The **`flam3usd`** module is created out of the **`py_flam3usd`** file located inside the **Extra Files** section.</br>First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule*** | 


```python

# ███████╗██╗░░░░░░█████╗░███╗░░░███╗██████╗░██╗░░██╗██╗░░░██╗░██████╗██████╗░
# ██╔════╝██║░░░░░██╔══██╗████╗░████║╚════██╗██║░░██║██║░░░██║██╔════╝██╔══██╗
# █████╗░░██║░░░░░███████║██╔████╔██║░█████╔╝███████║██║░░░██║╚█████╗░██║░░██║
# ██╔══╝░░██║░░░░░██╔══██║██║╚██╔╝██║░╚═══██╗██╔══██║██║░░░██║░╚═══██╗██║░░██║
# ██║░░░░░███████╗██║░░██║██║░╚═╝░██║██████╔╝██║░░██║╚██████╔╝██████╔╝██████╔╝
# ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═════╝░
#
#   Title:      FLAM3H™USD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe
#
#   File:       PythonModule

import toolutils

# Set some HDA infos
__v__ = 0
__version__ = "0.2.52"
__status__ = "Prototype"
# Note:
# The intgers contained into this __h_versions__ tuple must be Houdini version numbers composed of 3 digits:
# 190, 195, 200, 205, 210 and so on.
__h_versions__: tuple = (205,)
__range_type__: bool = True # True for closed range. False for open range


def is_nonempty_int_tuple(value: tuple) -> bool:
    """Check if a tuple contain only integers.</br>
    This is done to be sure the FLAM3H™ dunder data: __h_versions__ is valid.</br>
    
    Note:
        The intgers contained into this __h_versions__ tuple must be Houdini version numbers composed of 3 digits:
        - 190, 195, 200, 205, 210 and so on.

    Args:
        value(str): The tuple to check</br>

    Returns:
        (bool): True if it contain only integers and False if not (including if empty)
    """
    return (
            isinstance(value, tuple) and
            len(value) > 0 and
            all(type(x) is int and len(str(abs(x))) == 3 for x in value)
    )

# The following are min and max Houdini version where FLAM3H™ can run.
# The max version is always most likely the latest Houdini version released by SideFX
# unless it is a closed range due to moving into newer Houdini and FLAM3H™ versions.
#
# The ranges can be open or close inside this definition:
# - (py_flam3usd__3_11) -> def flam3husd_compatible_type(self, range_type: bool, kwargs: dict | None = None, msg: bool = True) -> bool:
# - (py_flam3usd__3_7)  -> def flam3husd_compatible_type(self, range_type: bool, kwargs: Union[dict, None] = None, msg: bool = True) -> bool:
__h_version_min__: int = 190
try:
    __h_version_max__: int = __h_versions__[-1]
    if not is_nonempty_int_tuple(__h_versions__):
        __h_version_min__: int = 999
        __h_version_max__: int = __h_version_min__
except:
    __h_version_min__: int = 999
    __h_version_max__: int = __h_version_min__

def houdini_version(digit: int=1) -> int:
    """Retrieve the major Houdini version number currently in use.

    Args:
        digit(int): Default to 1: 19, 20. if set to 2: 190, 195, 200, 205, and so on.

    Returns:
        (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
    """ 
    return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))


def py_module_vars() -> str:
    """Return a strings:</br>
    * __module_filename__ -> module filename to use

    Args:
        (None):
        
    Returns:
        (None):
    """ 
    h: int = houdini_version(2)
    if h < 205: 
        __module_filename__: str = "py_flam3usd__3_7"
    else:
        __module_filename__: str = "py_flam3usd__3_11"

    return __module_filename__


__module_filename__ = py_module_vars()
flam3usd = toolutils.createModuleFromSection("flam3usd", kwargs["type"], __module_filename__)
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> PreFirstCreate `H20.5 to H21 UP`

| SCRIPT | Description | 
|:---|:---|
| **PreFirstCreate** | Before the node is even created but invoked.</br>Inside: **OTL**->**type_properties**->**Scripts**->**PreFirstCreate** | 

```python

# ███████╗██╗░░░░░░█████╗░███╗░░░███╗██████╗░██╗░░██╗██╗░░░██╗░██████╗██████╗░
# ██╔════╝██║░░░░░██╔══██╗████╗░████║╚════██╗██║░░██║██║░░░██║██╔════╝██╔══██╗
# █████╗░░██║░░░░░███████║██╔████╔██║░█████╔╝███████║██║░░░██║╚█████╗░██║░░██║
# ██╔══╝░░██║░░░░░██╔══██║██║╚██╔╝██║░╚═══██╗██╔══██║██║░░░██║░╚═══██╗██║░░██║
# ██║░░░░░███████╗██║░░██║██║░╚═╝░██║██████╔╝██║░░██║╚██████╔╝██████╔╝██████╔╝
# ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═════╝░
#
#   Title:      FLAM3H™USD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe
#
#   File:       PreFirstCreate

from datetime import datetime

# Get some HDA infos from the HDA module
FLAM3HUSD_NODE_TYPE_NAME_CATEGORY = 'alexnardini::Lop/FLAM3HUSD'
nodetype = hou.nodeType(FLAM3HUSD_NODE_TYPE_NAME_CATEGORY)
try:
    # This is the major version number only, for example version 1 or version 2, as integer
    __v__: int = nodetype.hdaModule().__v__
except AttributeError:
    __v__: int = 0
else:
    if not isinstance(__v__, int):
        __v__: int = 0
try:
    # this is the full version number, for example version 1.9.80 or 2.0.22, as string
    __version__: str = nodetype.hdaModule().__version__
except AttributeError:
    __version__: str = "Unknown"
else:
    if not isinstance(__version__, str):
        __version__: str = "Unknown"
try:
    # This is the status of the tool for this version, for example Prototype or Production
    __status__: str = nodetype.hdaModule().__status__
except AttributeError:
    __status__: str = "Unknown"
else:
    if not isinstance(__status__, str):
        __status__: str = "Unknown"
try:
    # This is a tuple containing all the houdini versions where this FLAM3H™ OTL is allowed to run
    __h_versions__: tuple[int, ...] = nodetype.hdaModule().__h_versions__
except AttributeError:
    __h_versions__: tuple[int, ...] = (999,)
else:
    if not nodetype.hdaModule().is_nonempty_int_tuple(__h_versions__):
        __h_versions__: tuple[int, ...] = (999,)
try:
    # This is telling us if FLAM3H™ will run only on a selected Houdini version numbers or also beyound those.
    __range_type__: bool = nodetype.hdaModule().__range_type__  # True for closed range. False for open range
except AttributeError:
    __range_type__: bool = True
else:
    if not isinstance(__range_type__, bool):
        __range_type__: bool = True
try:
    # This is the least Houdini version allowed
    __h_version_min__: int = nodetype.hdaModule().__h_version_min__
except AttributeError:
    if __h_versions__[0] != 999:
        __h_version_min__: int = __h_versions__[0]
    else:
        __h_version_min__: int = 999
else:
    if not isinstance(__h_version_min__, int):
        __h_version_min__: int = 999
try:
    # This is the max Houdini version allowed. if "__range_type__" is False, it will run beyound this version regardless
    __h_version_max__: int = nodetype.hdaModule().__h_version_max__
except AttributeError:
    if __h_versions__[0] != 999:
        __h_version_max__: int = __h_versions__[-1]
    else:
        __h_version_max__: int = 999
else:
    if not isinstance(__h_version_max__, int):
        __h_version_max__: int = 999


def flam3husd_first_time() -> bool:
    """If the version of Houdini running is not allowed for this FLAM3H™USD HDA version (different cases)
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
    
    
def flam3husd_compatible_allowed_msg() -> None:
    """If this the the first instance and an allowed version higher than the latest supported version
    display a message letting the user know.
    
    This is done to allow the splash screen to still be displayed if this is the case.
    
    Args:
        (None):
        
    Returns:
        (None):
    """ 
    
    _H_VERSION_ALLOWED = None
    try:
        _H_VERSION_ALLOWED = hou.session.F3HUSD_H_VERSION_ALLOWED # type: ignore
        
    except AttributeError:  
        pass
    
    if _H_VERSION_ALLOWED is None:
        
        if hou.isUIAvailable():
            h_version: int = nodetype.hdaModule().houdini_version(2)
            __h_versions__: tuple = nodetype.hdaModule().__h_versions__
            if h_version > __h_versions__[-1]:
                _MSG_H_VERSIONS = f"This Houdini version is: H{nodetype.hdaModule().flam3usd.flam3husd_scripts.flam3husd_h_versions_build_data(h_version)}\nThe latest Houdini version supported by this FLAM3H™USD is: H{nodetype.hdaModule().flam3usd.flam3husd_scripts.flam3husd_h_versions_build_data(__h_version_max__)}\nSome functionality may not work as intended or not work at all."
                hou.ui.displayMessage(_MSG_H_VERSIONS, buttons=("Got it, thank you",), severity=hou.severityType.ImportantMessage, default_choice=0, close_choice=-1, help=None, title="FLAM3H™USD Houdini version check", details=None, details_label=None, details_expanded=False) # type: ignore
        

def flam3husd_not_compatible_first_time_msg() -> None:
    """On first time FLAM3H™USD node instance creation:

    Run messages if not compatible with this Houdini version.
    
    Compatibility is checked inside:
    * def flam3h_first_time() -> bool:

    Args:
        ():

    Returns:
        (None):
    """ 
    
    _DUNDER: bool = __h_versions__[-1] == 999
    
    if not _DUNDER:
        _MSG_H_VERSIONS = nodetype.hdaModule().flam3usd.flam3husd_scripts.flam3husd_compatible_h_versions_msg(False)
        _MSG_INFO = f"\n-> FLAM3H™USD version: {__version__} - {__status__}\n\nThis Houdini version is not compatible with this FLAM3H™USD version.\nYou need {_MSG_H_VERSIONS} to run this FLAM3H™USD version"
                
        if hou.isUIAvailable():

            print(_MSG_INFO)

            _MSG_INFO_SB = f"-> FLAM3H™USD version: {__version__} - {__status__}. This Houdini version is not compatible with this FLAM3H™USD version. You need {_MSG_H_VERSIONS} to run this FLAM3H™USD version"
            hou.ui.setStatusMessage(_MSG_INFO_SB, hou.severityType.Error) # type: ignore

            hou.ui.displayMessage(f"Sorry, you need {_MSG_H_VERSIONS} to run this FLAM3H™USD version", buttons=("Got it, thank you",), severity=hou.severityType.Error, default_choice=0, close_choice=-1, help=None, title="FLAM3H™USD Houdini version check", details=None, details_label=None, details_expanded=False)

        else:
            print(_MSG_INFO)
            
    else:
        _MSG_INFO = f"FLAM3H™USD python module dunder's data is not valid."
                
        if hou.isUIAvailable():

            print(_MSG_INFO)

            _MSG_INFO_SB = f"-> {_MSG_INFO}"
            hou.ui.setStatusMessage(_MSG_INFO_SB, hou.severityType.Error) # type: ignore

            hou.ui.displayMessage(_MSG_INFO, buttons=("Got it, thank you",), severity=hou.severityType.Error, default_choice=0, close_choice=-1, help=None, title="FLAM3H™USD invalid dunder's data", details=None, details_label=None, details_expanded=False)

        else:
            print(_MSG_INFO)


if flam3husd_first_time():
    flam3husd_compatible_allowed_msg()
else:
    flam3husd_not_compatible_first_time_msg()
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> OnCreated `H20.5 to H21 UP`

| SCRIPT | Description | 
|:---|:---|
| **OnCreated** | Initialize what the tool need when you create its node in the network editor.</br>Inside: **OTL**->**type_properties**->**Scripts**->**OnCreated** | 

```python

# ███████╗██╗░░░░░░█████╗░███╗░░░███╗██████╗░██╗░░██╗██╗░░░██╗░██████╗██████╗░
# ██╔════╝██║░░░░░██╔══██╗████╗░████║╚════██╗██║░░██║██║░░░██║██╔════╝██╔══██╗
# █████╗░░██║░░░░░███████║██╔████╔██║░█████╔╝███████║██║░░░██║╚█████╗░██║░░██║
# ██╔══╝░░██║░░░░░██╔══██║██║╚██╔╝██║░╚═══██╗██╔══██║██║░░░██║░╚═══██╗██║░░██║
# ██║░░░░░███████╗██║░░██║██║░╚═╝░██║██████╔╝██║░░██║╚██████╔╝██████╔╝██████╔╝
# ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═════╝░
#
#   Title:      FLAM3H™USD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe
#
#   File:       OnCreated

kwargs["node"].hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_on_create()
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> OnLoaded `H20.5 to H21 UP`

| SCRIPT | Description | 
|:---|:---|
| **OnLoaded** | When loading hip files with FLAM3H™USD nodes in it do some checks.</br>Inside: **OTL**->**type_properties**->**Scripts**->**OnLoaded** | 

```python

# ███████╗██╗░░░░░░█████╗░███╗░░░███╗██████╗░██╗░░██╗██╗░░░██╗░██████╗██████╗░
# ██╔════╝██║░░░░░██╔══██╗████╗░████║╚════██╗██║░░██║██║░░░██║██╔════╝██╔══██╗
# █████╗░░██║░░░░░███████║██╔████╔██║░█████╔╝███████║██║░░░██║╚█████╗░██║░░██║
# ██╔══╝░░██║░░░░░██╔══██║██║╚██╔╝██║░╚═══██╗██╔══██║██║░░░██║░╚═══██╗██║░░██║
# ██║░░░░░███████╗██║░░██║██║░╚═╝░██║██████╔╝██║░░██║╚██████╔╝██████╔╝██████╔╝
# ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═════╝░
#
#   Title:      FLAM3H™USD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe
#
#   File:       OnLoaded

kwargs["node"].hdaModule().flam3usd.flam3husd_scripts(kwargs).flam3husd_on_loaded()
```

</br>
</br>
</br>

# <img width="48" height="48" src="../icons/icon_pythonSVG.svg" /> OnDeleted `H20.5 to H21 UP`

| SCRIPT | Description | 
|:---|:---|
| **OnLoaded** | When deleting a FLAM3H™USD node.</br>Inside: **OTL**->**type_properties**->**Scripts**->**OnDeleted** |


```python

# ███████╗██╗░░░░░░█████╗░███╗░░░███╗██████╗░██╗░░██╗██╗░░░██╗░██████╗██████╗░
# ██╔════╝██║░░░░░██╔══██╗████╗░████║╚════██╗██║░░██║██║░░░██║██╔════╝██╔══██╗
# █████╗░░██║░░░░░███████║██╔████╔██║░█████╔╝███████║██║░░░██║╚█████╗░██║░░██║
# ██╔══╝░░██║░░░░░██╔══██║██║╚██╔╝██║░╚═══██╗██╔══██║██║░░░██║░╚═══██╗██║░░██║
# ██║░░░░░███████╗██║░░██║██║░╚═╝░██║██████╔╝██║░░██║╚██████╔╝██████╔╝██████╔╝
# ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═════╝░
#
#   Title:      FLAM3H™USD. Render FLAM3H™ fractal Flames in Solaris using Karma
#   Author:     F stands for liFe ( made in Italy )
#   License:    GPL
#   Copyright:  (c) 2023 F stands for liFe
#
#   File:       OnDeleted

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

_FLAM3H™USD system utilities._

</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **SYS** | `sys_help` | `button` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_general_utils(kwargs).flam3husd_display_help(), hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **SYS** | `sys_reframe` | `button` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_viewport_bbox_frame(), hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **SYS** | `flam3hpath` | `operator path` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_scripts(kwargs).flam3husd_is_valid_flam3h_node(), kwargs['parm'].deleteAllKeyframes()
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

_Here you will play with the main settings of FLAM3H™USD._

</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `setdark` | `toggle` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_general_utils(kwargs).colorSchemeDark(), kwargs['parm'].deleteAllKeyframes(), hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `rndtype` | `ordered menu` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_general_utils(kwargs).setHydraRenderer(), kwargs['parm'].deleteAllKeyframes(), hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
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
| **PREFS** | `vptype` | `ordered menu` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_general_utils(kwargs).viewportParticleDisplay(), kwargs['parm'].deleteAllKeyframes(), hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `vpptsize` | `float` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(), kwargs['parm'].deleteAllKeyframes()
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
| **PREFS** | `widths` | `float` | `from H20.5` |

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
| **PREFS** | `xfviz` | `toggle` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `widths_xf_viz` | `float` | `from H20.5` |

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
| **PREFS** | `pxsamples_cpu` | `integer` | `from H20.5` |

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
| **PREFS** | `pxsamples_xpu` | `integer` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_actionButtonSVG.svg" /> Action Button Script
```python
node = kwargs['node']
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).viewportParticleSize(512, 'pxsamples_xpu')
node.hdaModule().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `denoiser` | `string` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
kwargs['parm'].deleteAllKeyframes(), hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **PREFS** | `use_f3h_shader` | `toggle` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
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
| **PREFS** | `tonemap` | `string` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
kwargs['parm'].deleteAllKeyframes(), hou.phm().flam3usd.flam3husd_general_utils(kwargs).util_flam3h_node_exist(True)
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

_Here you will find informations about FLAM3H™USD._

</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **ABOUT** | `icon_about_error` |  `Button` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_about_utils.flam3husd_about_show_info_panel(kwargs['node'])
```

</br>
</br>
</br>

| Tab | Parameter name | Parameter type |  Houdini version |
|:---|:---|---:|---:|
| **ABOUT** | `icon_about` |  `Button` | `from H20.5` |

- ### <img width="16" height="16" src="../icons/icon_callbackButtonSVG.svg" /> Callback Script
```python
hou.phm().flam3usd.flam3husd_about_utils.flam3husd_about_show_info_panel(kwargs['node'])
```



