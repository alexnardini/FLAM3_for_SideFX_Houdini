__author__ = "F stands for liFe ( made in Italy )"
__copyright__ = "© 2023 F stands for liFe"

__py_version__ = "3.11.7" # H20.5
__license__ = "GPL v3.0"
__maintainer__ = "Alessandro Nardini"

import hou
import nodesearch

from typing import Any
from typing import Type
from typing import Final
from typing import Callable
from typing import Protocol
from typing import TypeAlias
# This do not seem to work in Lop context
# from typing import TYPE_CHECKING 
# if TYPE_CHECKING:
#     from typing import TypeAlias
from platform import python_version
from datetime import datetime

import builtins

__pyside_version__: int | None = None
try:
    from PySide6 import QtWidgets, QtGui, QtCore
    __pyside_version__ = 6
except ImportError:
    try:
        from PySide2 import QtWidgets, QtGui, QtCore
        __pyside_version__ = 2
    except ImportError:
        pass
    else:
        from PySide2.QtSvg import QSvgRenderer
        from PySide2.QtGui import QPainter
else:
    from PySide6.QtSvg import QSvgRenderer
    from PySide6.QtGui import QPainter

FLAM3HUSD_NODE_TYPE_NAME_CATEGORY = 'alexnardini::Lop/FLAM3HUSD'
nodetype = hou.nodeType(FLAM3HUSD_NODE_TYPE_NAME_CATEGORY)
__version__ = nodetype.hdaModule().__version__
__status__ = nodetype.hdaModule().__status__
__range_type__: bool = nodetype.hdaModule().__range_type__  # True for closed range. False for open range
__h_version_min__: int = nodetype.hdaModule().__h_version_min__
__h_version_max__: int = nodetype.hdaModule().__h_version_max__


'''
    Tested on:  PYTHON v3.11.7  (H20.5, H21)

    Title:      SideFX Houdini FLAM3H™USD
    Author:     F stands for liFe ( made in Italy )
    date:       April 2025, Last revised February 2026 (cloned from: py_flam3usd__3_7.py)
                Source file start date: September 2023

    Name:       PY_FLAM3USD__3_11 "PYTHON" ( The ending filename digits represent the least python version needed to run this code )

    Comment:    Simple utility node to quickly setup
                fractal flames point clouds in Solaris for previews.

                This is basic and its the start of something.
                
                This code will be turned into a module from within Houdini.


    LIST OF CLASSES:
    
        f3husd_nodeNames
        f3husd_HDAsections
        
        f3husd_tabs
            PREFS
            ABOUT
            
        f3husd_pvt
        f3h_hda

        flam3husd_prm_utils
        flam3husd_scripts
        flam3husd_general_utils
        flam3husd_about_utils
        
        SvgIcon(QtWidgets.QWidget)
        pyside_master_app_names
        pyside_master_base_proto(Protocol)
        pyside_utils
        
        pyside_master
            F3HUSD_msg_panel(QtWidgets.QWidget)
        
        _NOTE:
            - Class @properties are always defined inbetween the @staticmethods and the class methods.
            - Global variables are all upper cases. Every upper case variable's name created inside any definition always start with an underscore (_)

'''


# TypeAlias
TA_PrmData: TypeAlias = int | float | str | tuple | hou.Ramp | hou.Vector3 | hou.Vector2


class f3husd_nodeNames:
    '''
    FLAM3H™ OTL contents node names used in various cases.</br>
    
    '''
    # Those node names are hard coded here.
    # If you change those node names inside the FLAM3H™USD houdini HDA network, update those global variables as well.
    # If not, some functionalities will stop working.
    DEFAULT_OUT_BBOX_REFRAME: Final = 'OUT_bbox_reframe' # prefix
    
    
class f3husd_HDAsections:
    '''
    HDA section names being used.</br>
    
    '''
    HDA_SECTION_IMG_BANNER: Final = 'FLAM3HUSD_DOC_intro.jpg'
    HDA_SECTION_SVG_LOGO: Final = 'iconSVG.svg'
    HDA_SECTION_SVG_LOGO_RED: Final = 'iconSVGR.svg'


class f3husd_tabs:
    '''
    FLAM3H™USD tabs and parameters names used throughout the code.</br>
    Additionally some miscellaneous constants used throughout the code as well.</br></br>
    
    Mainly for organizational purposes and namespace.</br></br>
    
    * Parameters names always start with the prefix: <b>PRM_</b>
    * Private parameters names always start with the prefix: <b>PVT_PRM_</b>
    * Message parameters names always start with the prefix: <b>MSG_PRM_</b>
    * Default values always start with the prefix: <b>DEFAULT_</b>
    * Message strings always start with the prefix: <b>MSG_</b>
    * Miscellaneous constants can be anything else.</b>

    '''
    
    DEFAULT_FLASH_MESSAGE_TIMER = 2 # Note that for this FLAM3H™USD OTL the flash messages only run in netowrk editors belonging to the Lop context.

    
    class PREFS:
        '''
        Everything related to the PREFS tab parameters names and miscellaneous constants.</br>
        
        '''
        PRM_F3H_PATH: Final = 'flam3hpath'
        PRM_F3H_WIDTHS: Final = 'widths_xf_viz'
        PRM_VIEWPORT_RENDERER: Final = 'rndtype'
        PRM_VIEWPORT_PT_TYPE: Final = 'vptype'
        PRM_VIEWPORT_PT_SIZE: Final = 'vpptsize'
        PRM_VIEWPORT_DARK: Final = 'setdark'
        
        PRM_KARMA_PIXEL_SAMPLES: Final = 'pxsamples'
        PRM_KARMA_F3H_SHADER_GAMMA: Final = 'f3h_gamma'
        PRM_KARMA_F3H_SHADER_HUE: Final = 'f3h_hsv_h'
        PRM_KARMA_F3H_SHADER_SATURATION: Final = 'f3h_hsv_s'
        PRM_KARMA_F3H_SHADER_VALUE: Final = 'f3h_hsv_v'
        PRM_KARMA_F3H_SHADER_EMISSION: Final = 'f3h_emission'
        PRM_KARMA_F3H_SHADER_TRANSMISSION: Final = 'f3h_transmission'

        # PREFS tab: PRIVATE SYSTEM
        PVT_PRM_FLAM3HUSD_DATA_DISABLED: Final = 'disabled'
        PVT_PRM_FLAM3HUSD_DATA_H_VALID: Final = 'h_valid' # The same paramater name as in FLAM3H™
        PVT_PRM_FLAM3HUSD_DATA_F3H_VALID: Final = 'f3h_valid'
        PVT_PRM_FLAM3HUSD_DATA_H190: Final = 'h_19_0'
        PVT_PRM_FLAM3HUSD_DATA_H205_UP: Final = 'h_20_5_up'
        # PREFS tab: PRIVATE MEM
        PVT_PRM_VIEWPORT_RENDERER_MEM: Final = 'rndtype_mem'
        PVT_PRM_VIEWPORT_PT_TYPE_MEM: Final = 'vptype_mem'
        PVT_PRM_VIEWPORT_PT_SIZE_MEM: Final = 'vpptsize_mem'
        
        MSG_PRM_ERROR: Final = 'msg_f3husd_error'
        
    class ABOUT:
        '''
        Everything related to the ABOUT tab parameters names and miscellaneous constants.</br>
        
        '''
        # MSG PRM
        MSG_PRM_ABOUT: Final = 'msg_f3husd_about'
        MSG_PRM_ABOUT_ERROR: Final = 'msg_f3husd_about_error'


class f3husd_pvt:
    '''
    All FLAM3H™USD private parameters names that are supposed to always stay private.</br>
    
    '''
    PVT_ALL: tuple[str, ...] = (f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_RENDERER_MEM,
                                f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_SIZE_MEM,
                                f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_TYPE_MEM,
                                f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_DISABLED, 
                                f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H_VALID, 
                                f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 
                                f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H190,
                                f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H205_UP
                                )
    
    
class f3husd_hda:
    '''
    Everything related to the FLAM3H™ node parameters names and miscellaneous constants being imported.</br>
    This include paths to and type of specific nodes being referenced inside FLAM3H™USD on import.</br>
    
    '''
    PRM_GLB_DENSITY = 'ptcount'
    
    # FLAM3H™ import density limit on creation
    DEFAULT_F3H_IMPORT_DENSITY_LIMIT: Final = 50000000 # 50M(millions)

    # FLAM3H™ to FLAM3H™USD - The full path will be the string inside the parameter: f3husd_tabs.PREFS.PREFS_F3H_PATH
    # plus this one
    F3H_TO_FLAM3HUSD_NODE_PATH: Final = '/TAGS/OUT_TO_FLAM3HUSD'
    # And its node type
    F3H_TO_FLAM3HUSD_NODE_TYPE_CATEGORY: Final = 'null'

    # FLAM3H™
    F3H_NODE_TYPE_NAME_CATEGORY: Final = 'alexnardini::Sop/FLAM3H'


# FLAM3H™ PRM UTILS start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################

  
class flam3husd_prm_utils:
    """
class f3h_prm_utils

@STATICMETHODS
* set(node: hou.LopNode, _prm: hou.Parm | hou.ParmTuple | str, data: TA_PrmData) -> None:
* setParms(node: hou.LopNode, parms_dict: dict) -> None:
* private_prm_set(node: hou.LopNode, _prm: str | hou.Parm, data: str | int | float) -> None:
* private_prm_deleteAllKeyframes(node: hou.LopNode, _prm: str | hou.Parm) -> None:

@METHODS

    """  
    
    @staticmethod
    def set(node: hou.LopNode, _prm: hou.Parm | hou.ParmTuple | str, data: TA_PrmData) -> None:
        """Set a single parameter using the folloing hou methods:</br>
        * <b>node.parm("name").set(val)</b>
        * <b>node.parmTuple("name").set(val)</b></br>
        
        while unlocking them and deleting their keyframes first.</br>
        
        Note:
            * In this code base, many parameter uses the raw version from the hou module to set parameters data.</br>
            * When you find some, it mean a definition prior to that code did unlock and cleared their keyframes already.</br>
        
        Args:
            node(hou.LopNode): this FLAM3H™ node.
            _prm( hou.Parm | hou.ParmTuple | str): Either a <b>hou.Parm</b>, <b>hou.ParmTuple</b> or a <b>parm name string</b>.
            data(TA_PrmData): the data to set the parameter to.
            
        Returns:
            (None):
        """ 
        prm: hou.Parm | hou.ParmTuple | None = None
        if isinstance(_prm, str):
            prm = node.parm(_prm)
            if prm is None:
                prm = node.parmTuple(_prm)
            
        elif isinstance(_prm, (hou.Parm, hou.ParmTuple)):
            prm = _prm
            
        if prm is not None:
            prm.lock(False)
            prm.deleteAllKeyframes()
            prm.set(data) # type: ignore
            
        else:
            print(f"{node.name()}: The passed in parameter is not valid:\n{_prm}")
    
    
    @staticmethod
    def setParms(node: hou.LopNode, parms_dict: dict) -> None:
        """Set a group of parameters using the hou node.setParms method.</br>
        while unlocking them and deleting their keyframes first .</br>
        
        Args:
            node(hou.LopNode): this FLAM3H™ node.
            parms_dict(dict): A dictionary specifying the parm names and their values.</br>Usually the dict is composed as [str, int | float | str]
            
        Returns:
            (None):
        """ 
        prm: hou.Parm | hou.ParmTuple | None = None
        for key in parms_dict.keys():
            prm = node.parm(key)
            if prm is None:
                prm = node.parmTuple(key)
            
            if prm is not None:
                prm.lock(False)
                prm.deleteAllKeyframes()
        
        if prm is not None:
            node.setParms(  # type: ignore
                            parms_dict
                            ) 
        else:
            print(f"{node.name()}: The passed in parameters dictionary is not valid:\n{parms_dict}")


    @staticmethod
    def private_prm_set(node: hou.LopNode, _prm: str | hou.Parm, data: TA_PrmData) -> None:
        """Set a parameter value while making sure to unlock and lock it right after.</br>
        This is being introduced to add an extra level of security so to speak to certain parameters</br>
        that are not meant to be changed by the user, so at least it will require some step before allowing them to do so.</br>
        
        Args:
            node(hou.LopNode): this FLAM3H™ node.
            prm_name(str | hou.Parm): the parameter name or the parameter hou.Parm directly.
            data(TA_PrmData): The value to set the parameter to.
            
        Returns:
            (None):
        """ 
        if isinstance(_prm, str): prm: hou.Parm | None = node.parm(_prm)
        elif isinstance(_prm, hou.Parm): prm: hou.Parm | None = _prm
        else: prm: hou.Parm | None = None
        if prm is not None:
            prm.lock(False)
            prm.deleteAllKeyframes()
            prm.set(data) # type: ignore # the set method for the hou.Parm exist but it is not recognized
            prm.lock(True)
            
        else:
            if isinstance(_prm, str):
                print(f"{node.name()}: PVT parameter not found to Set: {_prm}")
            else:
                print(f"{node.name()}: PVT parameter not found to Set.")
        
        
    @staticmethod
    def private_prm_deleteAllKeyframes(node: hou.LopNode, _prm: str | hou.Parm) -> None:
        """Delete all parameter's keyframes while making sure to unlock and lock it right after.</br>
        This is being introduced to add an extra level of security so to speak to certain parameters</br>
        that are not meant to be changed by the user, so at least it will require some step before allowing them to do so.</br>
        
        Args:
            node(hou.LopNode): this FLAM3H™ node.
            prm_name(str | hou.Parm):  the parameter name or the parameter hou.Parm directly.
            
        Returns:
            (None):
        """ 
        if isinstance(_prm, str): prm: hou.Parm | None = node.parm(_prm)
        elif isinstance(_prm, hou.Parm): prm: hou.Parm | None = _prm
        else: prm: hou.Parm | None = None
        if prm is not None and len(prm.keyframes()):
            prm.lock(False)
            prm.deleteAllKeyframes()
            prm.lock(True)
            
        elif prm is None:
            if isinstance(_prm, str):
                print(f"{node.name()}: PVT parameter not found to DeleteAllKeyFrames: {_prm}")
            else:
                print(f"{node.name()}: PVT parameter not found to DeleteAllKeyFrames.")


# FLAM3H™USD SCRIPTS start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class flam3husd_scripts:
    """
class flam3husd_scripts

@STATICMETHODS
* flam3husd_on_create_load_first_instance(node: hou.LopNode, msg: bool = True, limit: bool = True) -> bool:
* flam3husd_on_create_lock_parms(node: hou.LopNode) -> None:
* flam3husd_h_versions_build_data(__h_versions__: tuple | int, last_index: bool = False) -> str:
* flam3husd_compatible_h_versions_msg(this_h_versions: tuple, msg: bool = True, ps_cls_about: bool = False) -> str:
* flam3husd_compatible(h_version: int, this_h_versions: tuple, kwargs: dict | None, msg: bool) -> bool:
* flam3husd_compatible_range_close(kwargs: dict | None, msg: bool) -> bool:
* flam3husd_compatible_range_open(kwargs: dict | None, msg: bool) -> bool:

@METHODS
* flam3husd_compatible_type(self, range_type: bool, kwargs: dict | None = None, msg: bool = True) -> bool:
* flam3husd_is_valid_flam3h_node(self, _node: hou.LopNode | None = None) -> None:
* flam3husd_h_version_check(self) -> None:
* flam3husd_on_create_set_prefs_viewport(self, default_value_pt: float = 1) -> None:
* flam3husd_on_create_compatible_false(self) -> None:
* flam3husd_on_create(self) -> None:
* flam3husd_on_loaded_compatible_false(self) -> None:
* flam3husd_on_loaded_compatible_true(self) -> None:
* flam3husd_on_loaded(self) -> None:
* autoSetRenderer_on_create(self) -> None:
* flam3h_on_deleted(self) -> None:

    """

    __slots__ = ("_kwargs", "_node")

    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H™USD node houdini kwargs.
            
        Returns:
            (None):
        """  
        self._kwargs: dict = kwargs
        self._node = kwargs['node']
        
        
    @staticmethod
    def flam3husd_on_create_load_first_instance(node: hou.LopNode, msg: bool = True, limit: bool = True) -> bool:
        """Set the FLAM3H™ node path to the first instance if any are found to be imported into FLAM3H™USD.
        
        If multiple FLAM3H™USD nodes and more than one FLAM3H™ nodes are already present,
        always import the FLAM3H™ node that has not been imported yet; If all FLAM3H™ nodes are imported, it will import nothing.
        
        It will NOT automatically import FLAM3H™ nodes with more than f3husd_hda.DEFAULT_F3H_IMPORT_DENSITY_LIMIT point count. The users will need to import them by theirself.
        
        Args:
            node(hou.LopNode): This FLAM3H™USD node
            msg(bool): Default to True. When False it will not print messages (Status bar and Flash messages)
            limit(bool): Default to True. If False, it will not import FLAM3H™ node with a points count higher than 50M(millions) (f3husd_hda.DEFAULT_F3H_IMPORT_DENSITY_LIMIT).
            
        Returns:
            (bool): True if an instance is found and False if not.
        """
                
        # If it is a valid Houdini version
        if node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H_VALID).eval():
            
            # displayFlag
            display_flag: bool = node.isGenericFlagSet(hou.nodeFlag.Display) # type: ignore
                
            f3h_all_instances: tuple[hou.SopNode, ...] = hou.nodeType(f3husd_hda.F3H_NODE_TYPE_NAME_CATEGORY).instances()
            if f3h_all_instances:
                
                f3husd_all_instances: list[hou.LopNode] = hou.nodeType(FLAM3HUSD_NODE_TYPE_NAME_CATEGORY).instances()
                f3husd_all_instances_paths: list[str] = [f3husd.parm(f3husd_tabs.PREFS.PRM_F3H_PATH).eval() for f3husd in f3husd_all_instances if node != f3husd]
                
                # If we already have some FLAM3H™USD nodes and more than one FLAM3H™ nodes
                if len(f3husd_all_instances) > 1 and len(f3h_all_instances) > 1:
                    
                    for f3h in f3h_all_instances:
                        
                        if f3h.path() in f3husd_all_instances_paths:
                            pass
                        
                        else:
                            # If the point count of the FLAM3H™ node we want to import is not greater than f3husd_hda.DEFAULT_F3H_IMPORT_DENSITY_LIMIT
                            if limit:
                                
                                if f3h.parm(f3husd_hda.PRM_GLB_DENSITY).eval() <= f3husd_hda.DEFAULT_F3H_IMPORT_DENSITY_LIMIT:
                                    flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h.path())
                                    
                                    if display_flag:
                                        flam3husd_general_utils.util_auto_set_f3h_parameter_editor(f3h)
                                        
                                    if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                                    
                                    if msg:
                                        ...
                                        
                                    return True
                                
                                flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
                                return False
                                
                            else:
                                flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h.path())
                                return True
                            
                    flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
                    return False
                    
                else: # If we are creating the very first FLAM3H™USD instance, always import the very first FLAM3H™ node
                    
                    if f3h_all_instances:
                        
                        if f3h_all_instances[0].path() in f3husd_all_instances_paths:
                            return False
                        
                        else:
                            # If the point count of the FLAM3H™ node we want to import is not greater than f3husd_hda.DEFAULT_F3H_IMPORT_DENSITY_LIMIT
                            if limit:
                                
                                if f3h_all_instances[0].parm(f3husd_hda.PRM_GLB_DENSITY).eval() <= f3husd_hda.DEFAULT_F3H_IMPORT_DENSITY_LIMIT:
                                    flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h_all_instances[0].path())
                                    
                                    if display_flag:
                                        flam3husd_general_utils.util_auto_set_f3h_parameter_editor(f3h_all_instances[0])
                                        
                                    if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                                    
                                    if msg:
                                        ...
                                        
                                    return True
                                
                                flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
                                return False
                            
                            else:
                                flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h_all_instances[0].path())
                                
                                if display_flag:
                                    flam3husd_general_utils.util_auto_set_f3h_parameter_editor(f3h_all_instances[0])
                                    
                                if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                                    flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                                return True
                            
                    return False
            
            else: # If there are not FLAM3H™ nodes
                if msg:
                    ...
                    
                flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
                return False
            
        else:
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
            return False
        
        
    @staticmethod
    def flam3husd_on_create_lock_parms(node: hou.LopNode) -> None:
        """lock private parameters not being locked on creation by other definitions.
        
        Args:
            node(hou.LopNode): This FLAM3H™USD node
            
        Returns:
            (None):
        """
        
        for prm_name in f3husd_pvt.PVT_ALL:
            parm = node.parm(prm_name)
            if parm is not None and not parm.isLocked():
                parm.lock(True)
        
        
    @staticmethod
    def flam3husd_h_versions_build_data(__h_versions__: tuple | int, last_index: bool = False) -> str:
        """Get the houdini version number from the gloabl: __h_versions__

        Args:
            __h_versions__(tuple | int): a tuple containing all the compatible Houdini versions or an int of the desire Houdini version. When a tuple, it will be coming from the HDA's PythonModule: __h_versions__
            last_index(bool): Default to False as it will return the first in the tuple. If True, it will return the last in the tuple. This is done because some FLAM3H™USD HDA version run on multiple Houdinin versions.
            or it can be a 3 digits int

        Returns:
            (None):
        """ 
        if isinstance(__h_versions__, tuple):
            
            num_str: str | None = None
            if len(__h_versions__) > 1:
                if last_index: num_str = str(__h_versions__[-1])
                
                else:
                    num_str = str(__h_versions__[0])
                    
            elif __h_versions__:
                num_str = str(__h_versions__[0])

            if num_str is not None:
                return f"{num_str[:2]}.{num_str[-1]}"
            else:
                return f"**N/A**"
        
        elif isinstance(__h_versions__, int):
            
            if len(str(__h_versions__)) == 3:
                return f"{str(__h_versions__)[:2]}.{str(__h_versions__)[-1]}"
            
            elif len(str(__h_versions__)) == 2:
                return f"**{str(__h_versions__)}**"
            
            else:
                return f"**N/A**"
            
        else:
            return f"**N/A**"


    @staticmethod
    def flam3husd_compatible_h_versions_msg(this_h_versions: tuple, msg: bool = True, ps_cls_about: bool = False) -> str:
        """Build and fire a message letting the user know the Houdini version/s needed to run the installed FLAM3H™USD HDA version.

        Args:
            this_h_versions(tuple): a tuple containing all the Houdini version numbers. This is coming from the HDA's PythonModule: __h_versions__
            msg(bool): Default to True. When False it will not execute the: hou.ui.displayMessage
            ps_cls_about(bool): Default to False. If True, will build the message string for the pyside about panel.

        Returns:
            (str): Only the part of the message string with the allowed Houdini versions, to be used to compose the final message.
        """ 
        if len(this_h_versions) > 1:
            if __range_type__ is True: 
                
                if ps_cls_about:
                    _MSG_H_VERSIONS = f"H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions)} to H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions, True)}"
                else:
                    _MSG_H_VERSIONS = f"from H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions)} to H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions, True)}"
                    
            else:
                
                if ps_cls_about:
                    _MSG_H_VERSIONS = f"H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions)} to H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions, True)}*"
                else:
                    _MSG_H_VERSIONS = f"from H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions)} to H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions, True)} and up"
                    
        else:
            
            if __range_type__ is True:
                _MSG_H_VERSIONS = f"H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions)}"
                
            else:
                
                if ps_cls_about:
                    _MSG_H_VERSIONS = f"H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions)}*"
                else:
                    _MSG_H_VERSIONS = f"H{flam3husd_scripts.flam3husd_h_versions_build_data(this_h_versions)} and up"
    
        if msg and hou.isUIAvailable():
            hou.ui.displayMessage(f"Sorry, You need {_MSG_H_VERSIONS} to run this FLAM3H™USD version", buttons=("Got it, thank you",), severity=hou.severityType.Error, default_choice=0, close_choice=-1, help=None, title="FLAM3H™USD Houdini version check", details=None, details_label=None, details_expanded=False) # type: ignore

        return _MSG_H_VERSIONS


    @staticmethod
    def flam3husd_compatible(h_version: int, this_h_versions: tuple, kwargs: dict | None, msg: bool) -> bool:
        """This is to be run inside:
        
        * def flam3h_compatible_range_close(kwargs: dict | None, msg: bool) -> bool:
        * def flam3h_compatible_range_open(kwargs: dict | None, msg: bool) -> bool:
        
        It is for when FLAM3H™USD is allowed to run inside the current Houdini version.
        
        Args:
            h_version(int): This Houdini version.
            this_h_versions(tuple): The allowed Houdini versions this FLAM3H™USD can run with.
            kwargs(dict | None): When needed, this must be the class' self.kwargs. In the case of this definition, it will be passed in from the containing definition args. Or None
            msg(bool): When False it will not run the hou display messages.

        Returns:
            (bool): True if compatible otherwise False.
        """ 
        
        # If it is a match
        if h_version in this_h_versions:
            return True
        
        # We never know what will happen with the next major release of Houdini
        # but we allow it to run regardless for now.
        # If the current Houdini version is newer than the latest version supported by FLAM3H™USD
        # we allow it to run anyway letting the user know that something can go wrong.
        elif h_version > __h_version_max__:
            
            try:
                _H_VERSION_ALLOWED: bool =  hou.session.F3HUSD_H_VERSION_ALLOWED # type: ignore
            except AttributeError:
                _H_VERSION_ALLOWED: bool = False
            
            if _H_VERSION_ALLOWED is False:
                
                # Do not show me this Display Message window again when creating succesive instances of this HDA
                hou.session.F3HUSD_H_VERSION_ALLOWED = True # type: ignore
                    
                return True
            
            return True
        
        else:
            
            if msg: flam3husd_scripts.flam3husd_compatible_h_versions_msg(this_h_versions)
            
            if kwargs is not None:
                # Just in case I will need to do something
                ...
                
            return False


    @staticmethod
    def flam3husd_compatible_range_close(kwargs: dict | None, msg: bool) -> bool:
        """Tell if this FLAM3H™USD version is compatible with this Houdini version
        
        * range_close -> mean FLAM3H™USD will run only on Houdini versions included inside: nodetype.hdaModule().__h_versions__
        
        Args:
            kwargs(dict | None): When needed, this must be the class' self.kwargs, or None
            msg(bool): When False it will not run the hou display messages.

        Returns:
            (bool): True if compatible otherwise False.
        """ 
        h_version: int = flam3husd_general_utils.houdini_version(2)
        this_h_versions: tuple[int, ...] = nodetype.hdaModule().__h_versions__ # type: ignore # This is set inside each FLAM3H™USD HDA PythonModule module.
        
        # checks the full available range in the tuple
        if h_version < this_h_versions[0] or h_version > this_h_versions[-1]:
            
            if msg: flam3husd_scripts.flam3husd_compatible_h_versions_msg(this_h_versions)
            
            if kwargs is not None:
                # Just in case I will need to do something
                ...
            
            return False
        
        # This will probably never evaluate with the range close, but just in case.
        return flam3husd_scripts.flam3husd_compatible(h_version, this_h_versions, kwargs, msg)


    @staticmethod
    def flam3husd_compatible_range_open(kwargs: dict | None, msg: bool) -> bool:
        """Tell if this FLAM3H™USD version is compatible with this Houdini version
        
        * range_open -> mean it allow FLAM3H™USD to run on newer versions of Houdini than the versions included inside: nodetype.hdaModule().__h_versions__ before being properly fine tuned.

        Args:
            kwargs(dict | None): When needed, this must be the class' self.kwargs, or None
            msg(bool): When False it will not run the hou display messages.

        Returns:
            (bool): True if compatible otherwise False.
        """ 
        h_version: int = flam3husd_general_utils.houdini_version(2)
        this_h_versions: tuple[int, ...] = nodetype.hdaModule().__h_versions__ # type: ignore # This is set inside each FLAM3H™USD HDA PythonModule module.
        
        # Only for the latest FLAM3H™USD on the latest Houdini version (and its latest python module version), otherwise the full range is checked.
        #
        # We never know what will happen with the next major release of Houdini
        # but we allow it to run regardless for now.
        # the files: "py_flam3__3_11.py" and "py_flam3__3_7.py" checks the full available range in the tuple:
        # e.g.
        # if h_version < this_h_versions[0] or h_version > this_h_versions[-1]:
        #   ... 
        # Most likely the range will be closed again once SideFX update the vcc compiler and LLVM.
        if h_version < this_h_versions[0]:
            
            if msg: flam3husd_scripts.flam3husd_compatible_h_versions_msg(this_h_versions)
            
            if kwargs is not None:
                # Just in case I will need to do something
                ...
            
            return False
            
        return flam3husd_scripts.flam3husd_compatible(h_version, this_h_versions, kwargs, msg)


    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node
    
    
    def flam3husd_compatible_type(self, range_type: bool, kwargs: dict | None = None, msg: bool = True) -> bool:
        """Check FLAM3H™USD compatibility based on the type of range(of Houdini versions)
        
        * range_open -> mean it allow FLAM3H™USD to run on newer versions of Houdini than the versions included inside: nodetype.hdaModule().__h_versions__ before being properly fine tuned.
        * range_close -> mean FLAM3H™USD will run only on Houdini versions included inside: nodetype.hdaModule().__h_versions__

        Args:
            range_type(bool): True for closed range. False for open range. This is set inside the HDA's -> Type Properties -> Scripts -> PythonModule
            kwargs(dict | None): Default to None. When needed, this must be the class' self.kwargs
            msg(bool): Default to True. When False it will not run the hou display messages.

        Returns:
            (bool): True if compatible otherwise False.
        """ 
        if range_type:
            return self.flam3husd_compatible_range_close(kwargs, msg)
        else:
            return self.flam3husd_compatible_range_open(kwargs, msg)


    def flam3husd_is_valid_flam3h_node(self, _node: hou.LopNode | None = None) -> None:
        """Check if the imported FLAM3H™ node is valid or not
        
        Args:
            (self): 
            _node(hou.LopNode | None): Default to None and use the self.node. Otherwise it will use the provided Lop node instead.
            
        Returns:
            (None): 
        """  
        if _node is None: node: hou.LopNode = self.node
        else: node = _node
            
        f3h_path: str = node.parm(f3husd_tabs.PREFS.PRM_F3H_PATH).eval()
        
        f3h_to_f3husd_node: hou.SopNode = hou.node(f"{f3h_path}{f3husd_hda.F3H_TO_FLAM3HUSD_NODE_PATH}")
        try:
            type: hou.SopNodeType = f3h_to_f3husd_node.type()
        except AttributeError:
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
        else:
            if hou.node(f3h_path).type().nameWithCategory() == f3husd_hda.F3H_NODE_TYPE_NAME_CATEGORY and type.name() == f3husd_hda.F3H_TO_FLAM3HUSD_NODE_TYPE_CATEGORY:
                if hou.node(f3h_path).parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H_VALID).eval():
                    flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                else: flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
                
            else: flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
        

    def flam3husd_h_version_check(self) -> None:
        """Karma CPU has a bug in Houdini version 19.0.x and it crashes if it find a null primitive.
        Since the xform handls viz may generate one, this is used to hide the UI Karma handles import tab.
        
        We also want the shader with the unlit material x node to be partially usable in some versions
        and fully usable in some others.
        
        Args:
            (self): 
            
        Returns:
            (None): 
        """  

        node: hou.LopNode = self.node
        
        # Houdini 19.0
        if flam3husd_general_utils.houdini_version(2) == 190:
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H190, 1)
        else:
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H190, 0)
            
        # Houdini 20.5 UP
        if flam3husd_general_utils.houdini_version(2) >= 205:
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H205_UP, 1)
        else:
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H205_UP, 0)
    
    
    def flam3husd_on_create_set_prefs_viewport(self, default_value_pt: float = 1) -> None:
        """Initialize the necessary data for the viewport display preference's option on creation.
        This need some work as it is a little rough, I'll be back to this at some point. Good enough for now.
        
        Args:
            (self):
            default_value_pt(float): A default value to compare to for the point setting. This must always be the same as the FLAM3H™USD UI parameter's default values.
            
        Returns:
            (None):
        """
        
        node: hou.LopNode = self.node
        
        # Update dark history
        flam3husd_general_utils.util_store_all_viewers_color_scheme_onCreate() # init Dark viewers data, needed for the next definition to run
        flam3husd_general_utils(self.kwargs).colorSchemeDark(False) # type: ignore
        # Set other FLAM3H™USD instances to dark if any
        all_f3husd: tuple[hou.LopNode, ...] = node.type().instances()
        all_f3husd_vpptsize: list[float] = []
        all_f3husd_vptype: list[int] = []
        
        if len(all_f3husd) > 1:

            for f3husd in all_f3husd:
                if f3husd != node:
                    all_f3husd_vpptsize.append(f3husd.parm(f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE).eval())
                    all_f3husd_vptype.append(f3husd.parm(f3husd_tabs.PREFS.PRM_VIEWPORT_PT_TYPE).eval())
                    if f3husd.parm(f3husd_tabs.PREFS.PRM_VIEWPORT_DARK).eval():
                        flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_VIEWPORT_DARK, 1)
                        flam3husd_general_utils(self.kwargs).colorSchemeDark(False)
                        
                    # FLAM3H™USD nodes viewport preferences options are already synced
                    # so we really need only one to know them all
                    break
        else:
            flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_VIEWPORT_DARK, 1)
            flam3husd_general_utils(self.kwargs).colorSchemeDark(False) # type: ignore
    
        # If we collected some data, set
        if all_f3husd_vpptsize:
            
            parms_dict: dict = {f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE: all_f3husd_vpptsize[0], # type: ignore
                                f3husd_tabs.PREFS.PRM_VIEWPORT_PT_TYPE: all_f3husd_vptype[0]
                                }
            flam3husd_prm_utils.setParms(node, parms_dict)

            # Updated memory
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_SIZE_MEM, all_f3husd_vpptsize[0])
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_TYPE_MEM, all_f3husd_vptype[0])
            
        else:
            Pixels = hou.viewportParticleDisplay.Pixels # type: ignore
            
            for view in flam3husd_general_utils.util_getSceneViewers():
                
                # Lets make sure we check for a viewer in the Lop context
                if flam3husd_general_utils.util_is_context('Lop', view) and view.isViewingSceneGraph():
                    
                    settings: hou.GeometryViewportSettings = view.curViewport().settings()
                    size: float = settings.particlePointSize()
                    
                    if size != default_value_pt:
                        flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE, size)
                        # Updated memory
                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_SIZE_MEM, size)
                        
                    type: hou.EnumValue = settings.particleDisplayType()
                    if type == Pixels:
                        flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_VIEWPORT_PT_TYPE, 1)
                        # Updated memory
                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_TYPE_MEM, 1)
                        
                else:
                    # FLAM3H™USD shoud use its parameter default value in this case, but just to be sure
                    flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE, default_value_pt)
                    # Updated memory
                    flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_SIZE_MEM, default_value_pt)
                    
                    
    def flam3husd_on_create_compatible_false(self) -> None:
        """When FLAM3H™USD is loaded into an incompatible Houdini version this code is run on creation.
        
        _NOTE:
            This will need to be expanded at some point in time, for now it is enough to catch the versions and show the incompatibility for simple cases.
        
        Args:
            (self):
            iterators_count_zero(bool): Default to True. Set the iterators count to Zero. Set it to False to not set.
            descriptive_prm(bool): Default to True. Set the node descriptive parameter. Set it to False to not set.
            
        Returns:
            (None):
        """
        node: hou.LopNode = self.node
        
        flam3husd_prm_utils.private_prm_set(self.node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H_VALID, 0)
        __h_versions__: tuple[int, ...] = nodetype.hdaModule().__h_versions__ # type: ignore # This is set inside each FLAM3H™USD HDA PythonModule module.
        
        _MSG_H_VERSIONS = flam3husd_scripts.flam3husd_compatible_h_versions_msg(__h_versions__, False)

        _MSG_INFO = f"ERROR -> FLAM3H™USD version: {__version__}. This Houdini version is not compatible with this FLAM3H™USD version. you need {_MSG_H_VERSIONS} to run this FLAM3H™USD version"
        _MSG_ABOUT = f"This FLAM3H™USD version need {_MSG_H_VERSIONS} to work."
        
        # Set proper messages in the about tabs
        parms_dict: dict = {f3husd_tabs.PREFS.MSG_PRM_ERROR: _MSG_ABOUT, # type: ignore
                            f3husd_tabs.ABOUT.MSG_PRM_ABOUT_ERROR: _MSG_ABOUT
                            }
        flam3husd_prm_utils.setParms(node, parms_dict)
            
        # ERROR in the status bar
        if hou.isUIAvailable(): hou.ui.setStatusMessage(_MSG_INFO, hou.severityType.Error) # type: ignore


    def flam3husd_on_create(self) -> None:
        """Initialize FLAM3H™USD node on creation and all the data it need to run.
        
        Args:
            (self)
            
        Returns:
            (None):
        """
        node: hou.LopNode = self.node
        # Set initial node color
        node.setColor(hou.Color((0.165,0.165,0.165)))
        
        # Check H version and set
        self.flam3husd_h_version_check()
        # Check if we are importing a valid FLAM3H™ node on all of the other FLAM3H™USD node instances
        _flam3husd_is_valid_flam3h_node: Callable[[hou.LopNode | None], None] = self.flam3husd_is_valid_flam3h_node
        for f3husd in node.type().instances():
            if f3husd != node:
                _flam3husd_is_valid_flam3h_node(f3husd)

        
        if self.flam3husd_compatible_type(__range_type__):
            
            # Load FLAM3H node first instance if any
            self.flam3husd_on_create_load_first_instance(node)
            # Check if we are importing a valid FLAM3H™ node
            self.flam3husd_is_valid_flam3h_node()
            # Set renderer
            self.autoSetRenderer_on_create()
            # Set viewport preferences settings
            self.flam3husd_on_create_set_prefs_viewport()
            # Set about box
            flam3husd_about_utils(self.kwargs).flam3husd_about_msg()
            
            # Lock data parameters
            self.flam3husd_on_create_lock_parms(node)
            
        else:
            # Do the incompatibility things
            self.flam3husd_on_create_compatible_false()
            
            
    def flam3husd_on_loaded_compatible_false(self) -> None:
        """When FLAM3H™USD is loaded into an incompatible Houdini version on hip file load and on node copy/clone this code is run.
        
        _NOTE:
            This will need to be expanded at some point in time, for now it is enough to catch the versions and show the incompatibility for simple cases.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        # For now we set both cases the same
        if hou.hipFile.isLoadingHipFile(): #type: ignore
            self.flam3husd_on_create_compatible_false()
        else:
            self.flam3husd_on_create_compatible_false()
            
            
    def flam3husd_on_loaded_compatible_true(self) -> None:
        """If we are loading hip files with FLAM3H™USD nodes in it that were prviewsly initialized with an incompatible version of Houdini,
        restore their default settings if their iterators count is set to Zero, otherwise leave them as they are to not modify exixting settings.
        
        This definition must run inside a:
        * if hou.hipFile.isLoadingHipFile():
            ....
        
        _NOTE:
            This may be extended in the future, depending on needs.
        
        To be used inside:
        * def flam3h_on_loaded(self) -> None:
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node: hou.LopNode = self.node
        
        # This is done in case the user saved a hip file with FLAM3H™USD nodes in it
        # while using an incompatible version of Houdini so that we can restore it to functional again.
        h_valid_prm: hou.Parm = node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H_VALID)
        if not h_valid_prm.eval():
            flam3husd_prm_utils.private_prm_set(self.node, h_valid_prm, 1)
            
            # Clear messages just in case
            parms_dict: dict = {f3husd_tabs.PREFS.MSG_PRM_ERROR: '', # type: ignore
                                f3husd_tabs.ABOUT.MSG_PRM_ABOUT_ERROR: ''
                                }
            flam3husd_prm_utils.setParms(node, parms_dict)
            
            # Lock data parameters
            self.flam3husd_on_create_lock_parms(node)
        
        
    def flam3husd_on_loaded(self) -> None:
        """Initialize FLAM3H™USD node on creation and all the data it need to run.
        For now the same as the on_create script, will see later on how this will evolve.
        
        Args:
            (self)
            
        Returns:
            (None):
        """
        
        # Check H version and set
        self.flam3husd_h_version_check()
            
        if self.flam3husd_compatible_type(__range_type__):
            
            # Restore if it is needed
            self.flam3husd_on_loaded_compatible_true()
            # Set viewport preferences settings
            self.flam3husd_on_create_set_prefs_viewport()
            
            # Check if we are importing a valid FLAM3H™ node
            self.flam3husd_is_valid_flam3h_node()
            # When cloning FLAM3H™USD nodes, check if other FLAM3H™USD nodes still have a valid FLAM3H™ node imported and disable them if not.
            if not hou.hipFile.isLoadingHipFile(): #type: ignore
                
                _flam3husd_is_valid_flam3h_node: Callable[[hou.LopNode | None], None] = self.flam3husd_is_valid_flam3h_node
                for f3husd in self.node.type().instances():
                    if f3husd != self.node:
                        _flam3husd_is_valid_flam3h_node(f3husd)
                
            # Set about box
            flam3husd_about_utils(self.kwargs).flam3husd_about_msg()
            
            # Lock data parameters
            self.flam3husd_on_create_lock_parms(self.node)
            
        else:
            self.flam3husd_on_loaded_compatible_false()
        

    def autoSetRenderer_on_create(self) -> None:
        """This need more work to make it smarter...its a start
        Set the hydra renderer based on the one found in the viewers already.
        Since the renderer menu will set all the Lop viewers in one go, we assume that the are all the same type already.
        
        _NOTE:
            This need work to make it meaningful.
        
        Args:
            (self)
            
        Returns:
            (None):
        """
        
        node: hou.LopNode = self.node
        
        views = flam3husd_general_utils.util_getSceneViewers()
        renderers: list = []
        
        for v in views:
            # Store only if it is a Lop viewer
            if (flam3husd_general_utils.util_is_context('Lop', v) and v.isViewingSceneGraph()) and not hou.hipFile.isLoadingHipFile(): # type: ignore
                renderers.append(hou.SceneViewer.currentHydraRenderer(v))

        if renderers:
            
            _RND: str | None = None
            for r in renderers:
                
                _karma_cpu_name: str = flam3husd_general_utils.karma_cpu_hydra_renderer_name()
                _houdini_name: str = 'Houdini'
                
                # CPU
                #
                # Just in case lets compare everything as str.lower()
                if _karma_cpu_name.lower() in str(r).lower():
                    _RND = _karma_cpu_name
                    break
                
                # GL/VK
                #
                # Just in case lets compare everything as str.lower()
                elif _houdini_name.lower() in str(r).lower(): 
                    _RND = 'Houdini GL'
                    break
                
                # anything else
                else:
                    pass
                
            if _RND is not None:
                
                rnd_idx: int | None = flam3husd_general_utils.flam3husd_hydra_renderers_dict().get(_RND)
                lop_viewers: bool = False
                
                for v in views:
                    
                    # Set only if it is a Lop viewer
                    if flam3husd_general_utils.util_is_context('Lop', v) and v.isViewingSceneGraph():
                        
                        if lop_viewers is False: lop_viewers = True
                        
                        if rnd_idx is not None:
                            
                            flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_VIEWPORT_RENDERER, rnd_idx)
                            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_RENDERER_MEM, rnd_idx)
                            hou.SceneViewer.setHydraRenderer(v, _RND)

                            instances: tuple[hou.LopNode, ...] = node.type().instances()
                            if len(instances) > 1:
                                
                                # Sync FLAM3H™USD nodes
                                for n in instances:
                                    
                                    if n != node:
                                        
                                        flam3husd_prm_utils.set(n, f3husd_tabs.PREFS.PRM_VIEWPORT_RENDERER, rnd_idx)
                                        flam3husd_prm_utils.private_prm_set(n, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_RENDERER_MEM, rnd_idx)
                        
                    else:
                        pass
                    
                if lop_viewers and rnd_idx is not None:
                    flam3husd_general_utils.flash_message(flam3husd_general_utils.in_get_dict_key_from_value(flam3husd_general_utils.flam3husd_hydra_renderers_dict(), rnd_idx))
                        
    
    def flam3husd_on_deleted(self) -> None:
        """Cleanup the data on deletion.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node: hou.LopNode = self.node
        node_instances: tuple[hou.LopNode, ...] = node.type().instances()

        _flam3husd_is_valid_flam3h_node: Callable[[hou.LopNode | None], None] = self.flam3husd_is_valid_flam3h_node
        for f3husd in node_instances:
            if f3husd != node:
                _flam3husd_is_valid_flam3h_node(f3husd)

        if len(node_instances) == 1:
            
            # Delete the Houdini update mode data if needed
            try:
                del hou.session.HUSD_CS_STASH_DICT # type: ignore
            except AttributeError:
                pass


# FLAM3H™USD GENERAL UTILS start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################

class flam3husd_general_utils:
    """
class flam3husd_general_utils

@STATICMETHODS
* util_flam3h_node_exist_all(node: hou.LopNode) -> None:
* util_flam3h_node_exist_self(node: hou.LopNode) -> bool:
* in_get_dict_key_from_value(mydict: dict, idx: int) -> str:
* karma_cpu_hydra_renderer_name() -> str:
* houdini_version(digit: int = 1) -> int:
* util_auto_set_f3h_parameter_editor(f3h_node: hou.SopNode) -> None:
* util_getParameterEditors() -> list:
* util_getSceneViewers() -> list:
* util_is_context(context: str, viewport: hou.paneTabType) -> bool:
* util_is_context_available_viewer(context: str) -> bool:
* flash_message(msg: str | None, timer: float = FLAM3HUSD_FLASH_MESSAGE_TIMER, img: str | None] = None) -> None:
* set_status_msg(msg: str, type: str) -> None:

@METHODS
* util_flam3h_node_exist(self, f3husd_all: bool = False) -> None:
* util_flam3h_node_cycle_import(self) -> None:
* util_set_clipping_viewers(self) -> None:
* get_node_path(self, node_name: str) -> str | None:
* util_viewport_bbox_frame(self) -> None:
* util_store_all_viewers_color_scheme(self) -> None:
* colorSchemeDark(self, update_others: bool = True) -> None:
* viewportParticleDisplay(self) -> None:
* viewportParticleSize(self, reset_val: float | None = None, prm_name_size: str = PREFS_VIEWPORT_PT_SIZE) -> None:
* setHydraRenderer(self) -> None:
* reset_flam3h_shader(self) -> None:
* flam3husd_display_help(self) -> None:

    """

    __slots__ = ("_kwargs", "_node", "_bbox_reframe_path")
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H™USD node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs: dict[str, Any] = kwargs
        self._node: hou.LopNode = kwargs['node']
        self._bbox_reframe_path: str | None = self.get_node_path(f3husd_nodeNames.DEFAULT_OUT_BBOX_REFRAME)
        
        
    @staticmethod
    def util_flam3h_node_exist_self(node: hou.LopNode) -> bool:
        """Check if the currently imported node path point to a valid FLAM3H™ node.
        
        Args:
            node(hou.LopNode): this FLAM3H™USD node.
            
        Returns:
            (bool): True if the imported FLAM3H™ node exist and False if it does not.
        """ 
        current_import: str = node.parm(f3husd_tabs.PREFS.PRM_F3H_PATH).eval()
        
        f3h: hou.SopNode | None = hou.node(current_import)
            
        if f3h is None:
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
            return False
        
        else:
            if f3h is not None: # I dnt think  this is needed
                if f3h.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H_VALID).eval():
                    flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                    return True
                
                flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
                return False
            
            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
            return False
            
            
    @staticmethod
    def util_flam3h_node_exist_all(node: hou.LopNode) -> None:
        """Check if the currently imported node path point to a valid FLAM3H™ node
        for all FLAM3H™USD node instances.
        
        Args:
            node(hou.LopNode): this FLAM3H™USD node to use for its node instances collection.
            
        Returns:
            (None):
        """ 
        [flam3husd_general_utils.util_flam3h_node_exist_self(f3husd) for f3husd in node.type().instances()]


    @staticmethod
    def in_get_dict_key_from_value(mydict: dict, idx: int) -> str:
        """Get the dictionary key from the dictionary value.

        Args:
            mydict(dict): The dictionary for lookup
            idx(int): The index to retrieve its key from.

        Returns:
            (str): The key string.
        """       
        var_name: str = list(mydict.keys())[list(mydict.values()).index(idx)] 
        return var_name
    
    
    @staticmethod
    def karma_cpu_hydra_renderer_name() -> str:
        """Return the internal hydra renderer name for Karma.
        
        Args:
            (None):
            
        Returns:
            (str): [Return the internal hydra renderer name for Karma.]
        """    
        karma_name: str = 'Karma CPU'
        if flam3husd_general_utils.houdini_version(2) < 200: karma_name = 'Karma'
        return karma_name


    @staticmethod
    def flam3husd_hydra_renderers_dict() -> dict[str, int]:
        """Return a dictionary with the available renderer as the keys
        and their renderer menu parameter index as the values.
        
        Args:
            (None):
            
        Returns:
            (str): [Return the internal hydra renderer name for Karma.]
        """    
        _RND_idx: dict[str, int] = {'Houdini GL': 0,
                                    flam3husd_general_utils.karma_cpu_hydra_renderer_name(): 1
                                    }
        
        return _RND_idx


    @staticmethod
    def houdini_version(digit: int=1) -> int:
        """Retrieve the major Houdini version number currently in use.

        Args:
            digit(int): Default to 1: 19, 20. if set to 2: 190, 195, 200, 205, and so on.

        Returns:
            (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
        """ 
        return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))


    @staticmethod
    def util_auto_set_f3h_parameter_editor(f3h_node: hou.SopNode) -> None:
        """Update any pinned Parameter Editor with the currently imported FLAM3H™ node if a FLAM3H™ node Parameters was already on display.
        
        Args:
            f3h_node(hou.SopNode): The FLAM3H™ node to set the pinned parameter editor to.
            
        Returns:
            (None):
        """ 
        
        pe: list = flam3husd_general_utils.util_getParameterEditors()
        for p in pe:
            if p.currentNode() != f3h_node and p.isPin():
                p.setCurrentNode(f3h_node, False)
    
    
    @staticmethod
    def util_getParameterEditors() -> list:
        """Return a list of Parameter Editors currently open in this Houdini session.
        It will collect only the Parameter Editors with a FLAM3H node parameter on display already.
        
        Args:
            (None):
            
        Returns:
            (list): [return a list of open Parmaeter Editors with a FLAM3H™ node on display]
        """    
        parms: tuple[Any, ...] = hou.ui.paneTabs() # type: ignore
        return [p for p in parms if isinstance(p, hou.ParameterEditor) and p.currentNode().type().nameWithCategory() == f3husd_hda.F3H_NODE_TYPE_NAME_CATEGORY]


    @staticmethod
    def util_getSceneViewers() -> list:
        """Return a list of viewer currently open in this Houdini session.
        
        Args:
            (None):
            
        Returns:
            (list): [return a list of open scene viewers]
        """    
        views: tuple = hou.ui.paneTabs() # type: ignore
        return [v for v in views if isinstance(v, hou.SceneViewer)]
    

    @staticmethod
    def util_is_context(context: str, viewport: hou.SceneViewer | hou.NetworkEditor | hou.ParameterEditor) -> bool:
        """Return if we are inside a context or not.
        
        Args:
            context(str): The context we want to check if we are currently in. Options so far are: 
                * Sop: str
                * Lop: str
            viewport(hou.SceneViewer | hou.NetworkEditor | hou.ParameterEditor): Any of the available pane tab types, in my case will always be: hou.paneTabType.SceneViewer or hou.SceneViewer
            
        Returns:
            (bool): [True if we are in Solaris and False if we are not.]
        """    
        context_now: hou.NodeTypeCategory = hou.ui.findPaneTab(viewport.name()).pwd().childTypeCategory() # type: ignore
        if str(context_now.name()).lower() == context.lower():
            return True
        
        return False


    @staticmethod
    def util_is_context_available_viewer(context: str) -> bool:
        """Return if there are viewers that belong to a desired context.
        
        Args:
            context(str): The context we want to check if we are currently in. Options so far are: 
                * Sop: str
                * Lop: str
            
        Returns:
            (bool): [True if there is at least one viewer that belong to a desired context or False if not.]
        """    
        available: bool = False
        for v in flam3husd_general_utils.util_getSceneViewers():
            if flam3husd_general_utils.util_is_context(context, v):
                available = True
                break
        return available
    
    
    @staticmethod
    def util_is_context_available_viewer_data(context: str) -> tuple[bool, list[hou.SceneViewer]]:
        """Return if there are viewers that belong to a desired context and a list of all viewers.</br>
        
        This is being added as an alternative to:
        * def util_is_context_available_viewer(context: str) -> bool:
        
        It perform the same operations</br>
        but will also return all the data available instead of just getting a bool.
        
        Args:
            context(str): The context we want to check if we are currently in. Options so far are: 
                * Object: str
                * Sop: str
                * Lop: str
            
        Returns:
            (tuple[bool, list[hou.SceneViewer]]): A tuple containing a bool and a list of viewers.</br>The bool will tell us if there is at least one viewer that belong to a desired context and the list will contain all available viewers.
        """    
        available = False
        viewers: list[hou.SceneViewer] = flam3husd_general_utils.util_getSceneViewers()
        for v in viewers:
            if flam3husd_general_utils.util_is_context(context, v):
                available = True
                break
            
        return available, viewers
        
    
    @staticmethod
    def flash_message(msg: str | None, timer: float = f3husd_tabs.DEFAULT_FLASH_MESSAGE_TIMER, img: str | None = None, usd_context: str = 'Lop') -> None:
        """Cause a message to appear on the top left of the network editor.
        This will work either in Sop and Lop context as it is handy to get those messages either ways. 

        Args:
            msg(str | None): The string message to print or None.
            timer(float): Default to: FLAM3HUSD_FLASH_MESSAGE_TIMER. How long the printed message stay before it fade away.
            img(str | None): Default to none. specifies an icon or image file that should be displayed along with the text specified in the msg argument.

        Returns:
            (None):
        """  
        if hou.isUIAvailable():
            for ne in (p for p in hou.ui.paneTabs() if p.type() == hou.paneTabType.NetworkEditor): ne.flashMessage(img, msg, timer) # type: ignore
            # Force the flash message to appear in any Lop viewers available.
            # This is being done because it is more handy for the user to read the message in the Lop viewers
            # when working through the FLAM3H™USD HDA instead of the network editor that it is usually covered with parameters editor interfaces.
            lop_viewer_available, viewers = flam3husd_general_utils.util_is_context_available_viewer_data(usd_context)
            if lop_viewer_available:
                for view in (v for v in viewers if flam3husd_general_utils.util_is_context(usd_context, v) and v.isViewingSceneGraph()): view.flashMessage('', msg, timer)

        
    @staticmethod
    def set_status_msg(msg: str, type: str) -> None:
        """Print a message to the Houdini's status bar if the UI is available.

        Args:
            msg(str): The message string to print
            type(str): The type of severity message to use, Possible choises are:
            
            * MSG ( message )
            * IMP ( important message )
            * WARN ( warning )
            
            If type is mispelled, it will fall back to: hou.severityType.Message
            
        Returns:
            (None):
        """

        if hou.isUIAvailable():
            st: dict[str, hou.EnumValue] = { 'MSG': hou.severityType.Message, 'IMP': hou.severityType.ImportantMessage, 'WARN': hou.severityType.Warning }  # type: ignore
            severityType: hou.EnumValue | None = st.get(type)
            if severityType is not None:
                hou.ui.setStatusMessage(msg, st.get(type)) # type: ignore
            else:
                # If the selected severity type is not found, use the default severity type: hou.severityType.Message
                # This mostly not to make it error out if the user make a typo or such.
                hou.ui.setStatusMessage(msg, hou.severityType.Message) # type: ignore
        

    @staticmethod
    def util_store_all_viewers_color_scheme_onCreate() -> None:
        """Store dictionaries of viewers color schemes if needed on FLAM3H™USD node creation
        This version do not check from which parameter run as we need it to run regardless.
        
        Args:
            (None):
            
        Returns:
            (None):  
        """  
        # Check if the required data exist already
        try:
            hou.session.HUSD_CS_STASH_DICT # type: ignore
            _EXIST: bool = True
        except:
            _EXIST: bool = False
            
        views_scheme: list[hou.EnumValue]  = []
        views_keys: list[str] = []
        for v in flam3husd_general_utils.util_getSceneViewers():
            
            # Store only if it is a Lop viewer
            if flam3husd_general_utils.util_is_context('Lop', v) and v.isViewingSceneGraph():
            
                settings: hou.GeometryViewportSettings = v.curViewport().settings()
                _CS: hou.EnumValue = settings.colorScheme()
                if _CS != hou.viewportColorScheme.Dark: # type: ignore
                    views_scheme.append(_CS)
                    views_keys.append(v.name())
                    
        # Always store and update this data if we collected something
        if views_scheme and views_keys:
            new: dict[str, hou.viewportColorScheme] = dict(zip(views_keys, views_scheme)) # type: ignore
            if _EXIST:
                # Check if it needs an update
                if new != hou.session.HUSD_CS_STASH_DICT: #type: ignore
                    __old_to_update: dict[str, hou.viewportColorScheme] = hou.session.HUSD_CS_STASH_DICT.copy() #type: ignore
                    for key, value in new.items():
                        if value != hou.viewportColorScheme.Dark: # type: ignore
                            if key not in __old_to_update.keys(): __old_to_update[key] = value
                    hou.session.HUSD_CS_STASH_DICT: dict[str, hou.viewportColorScheme] = __old_to_update #type: ignore
            else:
                # otherwise create
                hou.session.HUSD_CS_STASH_DICT: dict[str, hou.viewportColorScheme] = new # type: ignore


    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node
    
    @property
    def bbox_reframe_path(self):
        return self._bbox_reframe_path
    
    
    def util_flam3h_node_exist(self, f3husd_all: bool = False) -> None:
        """Check if the currently imported node path point to a valid FLAM3H™ node.
        
        Option to check self or all self node instances instead is provided.
        
        Args:
            (self):
            f3husd_all(bool): Default to False. If set to True it will run for all FLAM3H™USD node instances instead.
            
        Returns:
            (None):
        """ 
        node = self.node
        if f3husd_all: self.util_flam3h_node_exist_all(node)
        else: self.util_flam3h_node_exist_self(node)
    

    def util_flam3h_node_cycle_import(self) -> None:
        """import and cycle through the available FLAM3H™ nodes one by one.
        You can [LMB] and import the next one or [SHIFT+LMB] to import the preview one.
        
        When you reach the end while using the [LMB], it will start again from the start (index 0(Zero)).
        When you reach the first while [SHIFT+LMB], it will start again from the end (last available index)
        
        Args:
            (self):
            
        Returns:
            (None):  
        """
        
        node: hou.LopNode = self.node
        # If it is a valid Houdini version
        if node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H_VALID).eval():
            
            f3h_all_instances: tuple[hou.SopNode, ...] = hou.nodeType(f3husd_hda.F3H_NODE_TYPE_NAME_CATEGORY).instances()
            if f3h_all_instances:
                
                f3h_all_instances_paths: list[str] = [f3h.path() for f3h in f3h_all_instances]
                current_import: str = node.parm(f3husd_tabs.PREFS.PRM_F3H_PATH).eval()
                    
                # If we have multiple FLAM3H™ node instances
                if len(f3h_all_instances) > 1:
                        
                    # If a valid FLAM3H™ is already imported
                    if node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                    
                        try:
                            hou.node(current_import).type()
                            
                        except AttributeError:
                            # Otherwise load one that has not being imported yet to start with 
                            flam3husd_scripts.flam3husd_on_create_load_first_instance(node, False, False)
                            if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                                # IF it could not find a new one to import
                                # import the first one
                                flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h_all_instances_paths[0])
                                self.util_auto_set_f3h_parameter_editor(hou.node(f3h_all_instances_paths[0]))
                                flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                                
                        else:
                            
                            if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                                flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                                
                            else:
                                
                                current_index: int = f3h_all_instances_paths.index(current_import)
                                
                                # Update current pinned Parameter editor if any
                                if self.kwargs['ctrl']:
                                    self.util_auto_set_f3h_parameter_editor(hou.node(current_import))
                                
                                # Import preview
                                elif self.kwargs['shift']:
                                    
                                    try:
                                        flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h_all_instances_paths[current_index - 1])
                                        self.util_auto_set_f3h_parameter_editor(hou.node(f3h_all_instances_paths[current_index - 1]))
                                        
                                    except IndexError: # just in case
                                        # start over
                                        flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h_all_instances_paths[-1])
                                        self.util_auto_set_f3h_parameter_editor(hou.node(f3h_all_instances_paths[-1]))
                                        
                                    if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                                    
                                # Import next
                                else:
                                    
                                    try:
                                        flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h_all_instances_paths[current_index + 1])
                                        self.util_auto_set_f3h_parameter_editor(hou.node(f3h_all_instances_paths[current_index + 1]))
                                        
                                    except IndexError: # just in case
                                        # start over
                                        flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h_all_instances_paths[0])
                                        self.util_auto_set_f3h_parameter_editor(hou.node(f3h_all_instances_paths[0]))
                                        
                                    if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                                
                    else:
                        
                        try:
                            hou.node(current_import).type()
                            
                        except AttributeError:
                            # Otherwise load one that has not being imported yet to start with
                            flam3husd_scripts.flam3husd_on_create_load_first_instance(node, False, False)
                            if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                                # IF it could not find a new one to import
                                # import the first one
                                flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h_all_instances_paths[0])
                                self.util_auto_set_f3h_parameter_editor(hou.node(f3h_all_instances_paths[0]))
                                flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                                
                        else:
                            
                            # Update current pinned Parameter editor if any
                            if self.kwargs['ctrl']:
                                self.util_auto_set_f3h_parameter_editor(hou.node(current_import))
                            
                            if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                                flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                                
            
                # If we have one FLAM3H™ node instance
                else:
                    
                    current_import: str = node.parm(f3husd_tabs.PREFS.PRM_F3H_PATH).eval()
                    
                    try:
                        hou.node(current_import).type()
                        
                    except AttributeError:
                        flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_F3H_PATH, f3h_all_instances_paths[0])
                        self.util_auto_set_f3h_parameter_editor(hou.node(f3h_all_instances_paths[0]))
                        if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                            
                    else:
                        
                        # Update current pinned Parameter editor if any
                        if self.kwargs['ctrl']:
                            self.util_auto_set_f3h_parameter_editor(hou.node(current_import))
                        
                        # Just in case
                        if not node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 1)
                    
            else:
                flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID, 0)
                
            # As last,
            # Check if the imported FLAM3H™ node is really a valid one or not
            if node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_F3H_VALID).eval():
                flam3husd_scripts(self.kwargs).flam3husd_is_valid_flam3h_node()
    
    
    def util_set_clipping_viewers(self) -> None:
        """Set current viewport camera clipping near/far planes
        
        Args:
            (self):
            
        Returns:
            (None):  
        """
        for view in self.util_getSceneViewers():
            
            # Only if it is a Lop viewer
            if self.util_is_context('Lop', view) and view.isViewingSceneGraph():
                
                curView: hou.GeometryViewport = view.curViewport()
                settings = curView.settings()
                settings.setHomeAutoAdjustsClip( hou.viewportHomeClipMode.Neither ) # type: ignore
                settings.setClipPlanes( (0.001, 1000) )
                settings.homeAutoAdjustClip()
                settings.clipPlanes()
    
    
    def get_node_path(self, node_name: str) -> str | None:
        """Find the full path of the bbox data null node
        inside the current FLAM3H™USD node.
        
        The Null node names prefixes to search are stored inside the global variables:
        
        * NODE_NAME_OUT_BBOX_REFRAME

        Args:
            (self):
            node_name(str): The node name to search for
            
        Returns:
           ( str | None): The full path string to the bbox null data node used by the Camera sensor mode or the Re-frame mode.
        """     
        matcher = nodesearch.Name(node_name, exact=True)
        search = matcher.nodes(self.kwargs['node'], recursive=True)
        if search:
            return search[0].path()
        else:
            # Disabling this because it is annoying it never find it on creation, need to investigate.
            # Added it to: def util_viewport_bbox_frame(self) -> None:
            # _MSG: str = f"{self.node.name()}: Camera sensor BBOX data node not found."
            # self.set_status_msg(_MSG, 'WARN')
            return None
        
        
    def util_viewport_bbox_frame(self) -> None:
        """Re-frame the current viewport based on camera sensor node's bounding box.
        
        Args:
            (self):
            
        Returns:
            (None):  
        """  
        node = self.node
        
        viewports: list = self.util_getSceneViewers()
        num_viewers: int = len(viewports)
        num_viewers_lop: int = 0
        if num_viewers:
            self.util_set_clipping_viewers()
            
            for v in viewports:
                
                # Only if it is a Lop viewer
                if self.util_is_context('Lop', v) and v.isViewingSceneGraph():
                    
                    num_viewers_lop = num_viewers_lop + 1

                    view: hou.GeometryViewport = v.curViewport()
                    if view.type() != hou.geometryViewportType.Front: # type: ignore
                        view.changeType(hou.geometryViewportType.Front) # type: ignore
                        
                    if self.bbox_reframe_path is not None:
                        node_bbox: hou.SopNode = hou.node(self.bbox_reframe_path)
                        view.frameBoundingBox(node_bbox.geometry().boundingBox())
                    else:
                        _MSG: str = f"{self.node.name()}: Camera sensor BBOX data node not found."
                        self.set_status_msg(_MSG, 'WARN')
                        
            match num_viewers_lop:
                
                case 0:
                    _MSG: str = f"No LOP viewers available."
                    self.set_status_msg(f"{node.name()}: {_MSG} You need at least one LOP viewer for the reframe to work.", 'IMP')
                    self.flash_message(f"{_MSG}")

                case 1:
                    _MSG: str = f"viewport REFRAMED (Front)"
                    self.flash_message(_MSG)
                    self.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    
                case _:
                    _MSG: str = f"viewports REFRAMED (Front)"
                    self.flash_message(_MSG)
                    self.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    
        else:
            _MSG: str = f"No viewports in the current Houdini Desktop."
            self.set_status_msg(f"{node.name()}: {_MSG} You need at least one viewport for the reframe to work.", 'IMP')
            self.flash_message(f"{_MSG}")


    def util_store_all_viewers_color_scheme(self) -> None:
        """Store dictionaries of viewers color schemes
        
        Args:
            (self):
            
        Returns:
            (None):  
        """  
        # Do this only if the parameter toggle is: f3husd_tabs.PREFS.PRM_VIEWPORT_DARK
        parm = self.kwargs.get('parm')
        _ENTER_PRM = None
        if parm is not None: _ENTER_PRM = parm.name()
        if _ENTER_PRM is not None and _ENTER_PRM == f3husd_tabs.PREFS.PRM_VIEWPORT_DARK:
            views_scheme: list[hou.EnumValue]  = []
            views_keys: list[str] = []
            for v in self.util_getSceneViewers():
                
                # Store only if it is a Lop viewer
                if self.util_is_context('Lop', v) and v.isViewingSceneGraph():
                    
                    view = v.curViewport()
                    settings = view.settings()
                    _CS = settings.colorScheme()
                    if _CS != hou.viewportColorScheme.Dark: # type: ignore
                        views_scheme.append(_CS)
                        views_keys.append(v.name())
            
            # Always store and update this data
            hou.session.HUSD_CS_STASH_DICT: dict[str, hou.EnumValue] = dict(zip(views_keys, views_scheme)) # type: ignore


    def colorSchemeDark(self, update_others: bool = True) -> None:
        """Change viewport color scheme to dark
        and remember the current color scheme so to switch back to it when unchecked.
        If the viewport color scheme is already dark, checking this option will do nothing. 
        
        Args:
            (self):
            update_others(bool): Default to True. Update also the other FLAM3H™USD nodes in the scene if any
            
        Returns:
            (None):
        """
        node: hou.LopNode = self.node
        prm = node.parm(f3husd_tabs.PREFS.PRM_VIEWPORT_DARK)
        views: list[hou.SceneViewer] = self.util_getSceneViewers()
        
        if views:
            if prm.eval():
                # Store all viewers current color schemes
                # if different than Dark
                self.util_store_all_viewers_color_scheme()
                
                dark: bool = False
                lop_viewers: bool = False
                
                for v in views:
                    
                    # Set only if it is a Lop viewer
                    if self.util_is_context('Lop', v) and v.isViewingSceneGraph():
                        
                        if lop_viewers is False: lop_viewers = True
                        
                        settings: hou.GeometryViewportSettings = v.curViewport().settings()
                        _CS: hou.EnumValue = settings.colorScheme()
                        if _CS != hou.viewportColorScheme.Dark: # type: ignore
                            settings.setColorScheme(hou.viewportColorScheme.Dark) # type: ignore
                            if dark is False: dark = True
                
                if lop_viewers:
                    
                    if dark:
                        _MSG: str = f"Dark: ON"
                        self.flash_message(_MSG)
                        self.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                    else:
                        _MSG: str = f"Dark already"
                        self.set_status_msg(f"{node.name()}: {_MSG}. Viewers are in Dark mode already", 'MSG')
                        
                else:
                    flam3husd_prm_utils.set(node, prm, 0)
                    
                    if not hou.hipFile.isLoadingHipFile(): # type: ignore
                        _MSG: str = f"No Lop viewers available."
                        self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Lop viewer to either set to Dark or restore.", 'WARN')
                        self.flash_message(f"{_MSG}")
                    
            else:
                
                try: _STASH_DICT: dict[str, hou.EnumValue] | None = hou.session.HUSD_CS_STASH_DICT # type: ignore
                except AttributeError: _STASH_DICT: dict[str, hou.EnumValue] | None = None
                
                dark = False
                lop_viewers: bool = False
                if _STASH_DICT is not None:
                    for v in views:
                        
                        # Only if it is a Sop viewer
                        if self.util_is_context('Lop', v) and v.isViewingSceneGraph():

                            if lop_viewers is False: lop_viewers = True
                            
                            key: str = v.name()
                            _STASH: hou.EnumValue | None = _STASH_DICT.get(key)
                            if _STASH is not None:
                                settings: hou.GeometryViewportSettings = v.curViewport().settings()
                                _CS: hou.EnumValue = settings.colorScheme()
                                if _CS == hou.viewportColorScheme.Dark: # type: ignore
                                    settings.setColorScheme(_STASH)
                                    if dark is False: dark = True
                                
                if dark:
                    _MSG: str = f"Dark: OFF"
                    self.flash_message(_MSG)
                    self.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    
                else:
                    
                    try:
                        
                        if hou.session.HUSD_CS_STASH_DICT: # type: ignore
                            
                            if lop_viewers is False:
                                flam3husd_prm_utils.set(node, prm, 1)
                                self.set_status_msg(f"{node.name()}: There are not Lop viewers available to restore.", 'WARN')
                                _MSG_FLASH: str = f"No Lop viewers available."
                                self.flash_message(f"{_MSG_FLASH}")
                                
                            else:
                                _MSG: str = f"No viewer in Dark mode"
                                self.set_status_msg(f"{node.name()}: {_MSG}. None of the current viewers are set to Dark.", 'MSG')
                                
                        else:
                            _MSG: str = f"Nothing to restore"
                            self.set_status_msg(f"{node.name()}: {_MSG}. None of the current viewers has been switched to Dark. They probably were already in Dark mode.", 'MSG')
                            
                    except AttributeError:
                        pass
                            
        else:
            flam3husd_prm_utils.set(node, prm, 0)
            
            if not hou.hipFile.isLoadingHipFile(): # type: ignore
                _MSG = f"No Lop viewers in the current Houdini Desktop."
                self.set_status_msg(f"{node.name()}: {_MSG} You need at least one viewer to either set to Dark or restore.", 'WARN')
                self.flash_message(f"Dark: {_MSG}")
            
            
        if update_others:
            # Update dark preference's option toggle on other FLAM3H™USD nodes instances
            all_f3husd: tuple[hou.LopNode, ...] = self.node.type().instances()
            if len(all_f3husd) > 1:
                for f3husd in all_f3husd:
                    if f3husd == node:
                        continue
                    if f3husd.parm(f3husd_tabs.PREFS.PRM_VIEWPORT_DARK).eval() != prm.eval():
                        flam3husd_prm_utils.set(f3husd, f3husd_tabs.PREFS.PRM_VIEWPORT_DARK, prm.eval())

    
    def viewportParticleDisplay(self) -> None:
        """Switch viewport particle display mode
        between Pixel and Points.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node: hou.LopNode = self.node
        
        pttype: int = node.parm(f3husd_tabs.PREFS.PRM_VIEWPORT_PT_TYPE).eval()
        pttype_mem: int = node.parm(f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_TYPE_MEM).eval()
        
        Points: hou.EnumValue = hou.viewportParticleDisplay.Points # type: ignore
        Pixels: hou.EnumValue = hou.viewportParticleDisplay.Pixels # type: ignore

        lop_viewers: bool = False

        for view in self.util_getSceneViewers():
            
            # Set only if it is a Lop viewer
            if self.util_is_context('Lop', view) and view.isViewingSceneGraph():
                
                if lop_viewers is False: lop_viewers = True
                
                settings: hou.GeometryViewportSettings = view.curViewport().settings()
                
                match pttype:
                    
                    case 0:
                        settings.particleDisplayType(Points)
                        # update memory
                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_TYPE_MEM, pttype)
                        
                    case 1:
                        settings.particleDisplayType(Pixels)
                        # update memory
                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_TYPE_MEM, pttype)
                        
                    case _:
                        pass # For now, will see if in the future new option will be added.
                        
        # Sync FLAM3H™USD nodes
        all_f3husd: tuple[hou.LopNode, ...] = node.type().instances()
              
        if lop_viewers:  
            for f3husd in all_f3husd:
                if f3husd == node:
                    continue

                if f3husd.parm(f3husd_tabs.PREFS.PRM_VIEWPORT_PT_TYPE).eval() != pttype:
                    flam3husd_prm_utils.set(f3husd, f3husd_tabs.PREFS.PRM_VIEWPORT_PT_TYPE, pttype)

                if f3husd.parm(f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_TYPE_MEM).eval() != pttype:
                    flam3husd_prm_utils.private_prm_set(f3husd, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_TYPE_MEM, pttype)

    
        else:
            if pttype != pttype_mem:
                for f3husd in all_f3husd:
                    flam3husd_prm_utils.set(f3husd, f3husd_tabs.PREFS.PRM_VIEWPORT_PT_TYPE, pttype_mem)

            
            _MSG = f"No Lop viewers available."
            self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Lop viewer for this option to work.", 'WARN')
            self.flash_message(f"{_MSG}")
            

    def viewportParticleSize(self, reset_val: float | None = None, prm_name_size: str = f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE) -> None:
        """When the viewport particle display type is set to Point
        this will change their viewport size.
        
        Args:
            (self):
            reset_val (float | None): Default to None. Can be either "None" or a float value. If "None" it will use the current parameter value, otherwise it will use the one passed in this function.
            prm_name_size(str): Default to: f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE. The name of the parameter to set.
            
        Returns:
            (None):
        """
        node: hou.LopNode = self.node
        
        Points: hou.EnumValue = hou.viewportParticleDisplay.Points # type: ignore
        ptsize: float = node.parm(prm_name_size).eval()
        ptsize_mem: float = node.parm(f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_SIZE_MEM).eval()
        
        lop_viewers: bool = False

        for view in self.util_getSceneViewers():
            
            # Set only if it is a Lop viewer
            if self.util_is_context('Lop', view) and view.isViewingSceneGraph():
            
                if lop_viewers is False: lop_viewers = True
            
                settings: hou.GeometryViewportSettings = view.curViewport().settings()
                settings.particleDisplayType(Points)
                if reset_val is None:
                    if prm_name_size == f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE:
                        settings.particlePointSize(ptsize)
                        # update memory
                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_SIZE_MEM, ptsize)
                        
                else:
                    ptsize: float = float(reset_val)
                    if prm_name_size == f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE:
                        settings.particlePointSize(ptsize)
                        
                    prm = node.parm(prm_name_size)
                    flam3husd_prm_utils.set(node, prm, ptsize)
                    if prm_name_size == f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE:
                        # update memory
                        flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_SIZE_MEM, ptsize)
        
        if prm_name_size == f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE:
            
            # Sync FLAM3H™USD nodes
            all_f3husd: tuple[hou.LopNode, ...] = node.type().instances()
            
            # Update Point Size preference's option toggle on other FLAM3H™USD nodes instances
            if prm_name_size == f3husd_tabs.PREFS.PRM_VIEWPORT_PT_SIZE and node.parm(f3husd_tabs.PREFS.PRM_VIEWPORT_PT_TYPE).evalAsInt() == 0:
                
                if lop_viewers:
                    for f3husd in all_f3husd:
                        if f3husd.parm(prm_name_size).eval() != ptsize:
                            flam3husd_prm_utils.set(f3husd, prm_name_size, ptsize)
                        if f3husd.parm(f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_SIZE_MEM).eval() != ptsize:
                            flam3husd_prm_utils.private_prm_set(f3husd, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_PT_SIZE_MEM, ptsize)

                else:
                    for f3husd in all_f3husd:
                        if f3husd.parm(prm_name_size).eval() != ptsize_mem:
                            flam3husd_prm_utils.set(f3husd, prm_name_size, ptsize_mem)

                
                    _MSG: str = f"No Lop viewers available."
                    self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Lop viewer for this option to work.", 'WARN')
                    self.flash_message(f"{_MSG}")
                    
                    
    def setHydraRenderer(self) -> None:
        """Set the selected hydre renderer in the availables Lop viewers.
        
        Args:
            (self):
            
        Returns:
            (None):  
        """  
        node: hou.LopNode = self.node
        rndtype: int = node.parm(f3husd_tabs.PREFS.PRM_VIEWPORT_RENDERER).eval()
        rndtype_mem: hou.Parm = node.parm(f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_RENDERER_MEM)
        lop_viewers: bool = False
        
        for view in self.util_getSceneViewers():
            
            # Set only if it is a Lop viewer
            if self.util_is_context('Lop', view) and view.isViewingSceneGraph():
                
                # This double check should not be necessary
                # But H19 did throw me an error in some cases so I leave it here for now
                if isinstance(view, hou.SceneViewer):
                    
                    if lop_viewers is False: lop_viewers = True
                    
                    match rndtype:
                    
                        case 0 | 1: # Only Houdini GL or Karma CPU while from Houdini 21 UP also Karma XPU (2)
                            _RND: str = self.in_get_dict_key_from_value(self.flam3husd_hydra_renderers_dict(), rndtype)
                            hou.SceneViewer.setHydraRenderer(view, _RND)
                            # update memory
                            flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_RENDERER_MEM, rndtype)
                            # fire message
                            self.flash_message(_RND)
                            
                        case _:
                            lop_viewers = False # For now, will see if in the future new options will be added.
                    
                else: pass
                
        if lop_viewers:
            for n in node.type().instances():
                if n != node:
                    # Sync FLAM3H™USD node instances
                    flam3husd_prm_utils.set(n, f3husd_tabs.PREFS.PRM_VIEWPORT_RENDERER, rndtype)
                    # Update memory
                    flam3husd_prm_utils.private_prm_set(node, f3husd_tabs.PREFS.PVT_PRM_VIEWPORT_RENDERER_MEM, rndtype)


        else:
            flam3husd_prm_utils.set(node, f3husd_tabs.PREFS.PRM_VIEWPORT_RENDERER, rndtype_mem.eval())
        
            _MSG = f"No Lop viewers available."
            self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Lop viewer for this option to work.", 'WARN')
            self.flash_message(f"{_MSG}")
                        
                    
    def reset_flam3h_shader(self) -> None:
        """Reset the OUT Render settings parameters tab.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node: hou.LopNode = self.node
        
        prms_f3h_shader_data: dict[str, float] = {  f3husd_tabs.PREFS.PRM_KARMA_F3H_SHADER_GAMMA: 1,
                                                    f3husd_tabs.PREFS.PRM_KARMA_F3H_SHADER_HUE: 1,
                                                    f3husd_tabs.PREFS.PRM_KARMA_F3H_SHADER_SATURATION: 1,
                                                    f3husd_tabs.PREFS.PRM_KARMA_F3H_SHADER_VALUE: 1,
                                                    f3husd_tabs.PREFS.PRM_KARMA_F3H_SHADER_EMISSION: 1,
                                                    f3husd_tabs.PREFS.PRM_KARMA_F3H_SHADER_TRANSMISSION: 0
                                                    }
        # Set
        flam3husd_prm_utils.setParms(node, prms_f3h_shader_data)
        
        
    def flam3husd_display_help(self) -> None:
        """Open the Houdini help browser to display the FLAM3H™USD node documentation.

        Args:
            (self):
            
        Returns:
            (None):
        """
        hou.ui.displayNodeHelp(self.node.type()) # type: ignore


# FLAM3H™USD ABOUT start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################

class flam3husd_about_utils():
    """
class flam3husd_about_utils

@STATICMETHODS
* flam3husd_about_show_info_panel(node: hou.SopNode) -> None:

@METHODS
* flam3husd_about_msg(self):

    """
    
    __slots__ = ("_kwargs", "_node")
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H™USD node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs: dict[str, Any] = kwargs
        self._node: hou.LopNode = kwargs['node']
        
        
    @staticmethod
    def flam3husd_about_show_info_panel(node: hou.SopNode) -> None:
        """Display default pyside about message panel.</br>
        
        Args:
            node(hou.SopNode): This FLAM3H™USD node. In this case will be set to: kwargs['node'] directly in the parameter callback script string.
            
        Returns:
            (None):
        """ 
        
        pyside_utils.pyside_panels_safe_launch(
                                                pyside_master.F3HUSD_msg_panel, 
                                                app_name=pyside_master_app_names.PS_CLS_ABOUT,
                                                f3husd_node=node,  
                                                links=True,
                                                auto_close_ms=4000, 
                                                fade_in_ms=400, 
                                                fade_out_ms=400
                                               )


    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def kwargs(self) ->  dict[str, Any]:
        return self._kwargs
    
    @property
    def node(self) -> hou.LopNode:
        return self._node


    def flam3husd_about_msg(self):
        """Build and set the FLAM3H™USD about message.
        
        Args:
            (self):
            
        Returns:
            (None):
        """ 
        
        nl = "\n"
        nnl = "\n\n"
        
        # year = datetime.now().strftime("%Y")
        
        flam3h_author: str = f"AUTHOR: {__author__}"
        flam3h_cvex_version: str = f"CODE: vex H{flam3husd_scripts.flam3husd_h_versions_build_data(nodetype.hdaModule().__h_versions__, True)}"
        flam3h_python_version: str = f"Python {__py_version__}"
        flam3h_houdini_version: str = f"VERSION: {__version__} - {__status__} :: ({__license__})"
        Implementation_build: str = f"{flam3h_author}\n{flam3h_houdini_version}\n{flam3h_cvex_version}, {flam3h_python_version}\n{__copyright__}"
        
        build: tuple[str, ...] = (Implementation_build, nl
                                )
        
        build_about_msg: str = "".join(build)

        flam3husd_prm_utils.set(self.node, f3husd_tabs.ABOUT.MSG_PRM_ABOUT, build_about_msg)
        
        
# PYSIDE start here (panels and such)
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class SvgIcon(QtWidgets.QWidget):
    """A QWidget for displaying an SVG image.</br></br>

    This widget wraps a QSvgRenderer to render SVG content inside a QWidget.</br>
    It safely handles invalid SVG data or incorrect types.</br>
    
    """
    def __init__(self, svg_bytes: QtCore.QByteArray, parent=None):
        super().__init__(parent)
        
        try:
            self.renderer: QSvgRenderer | None = QSvgRenderer(svg_bytes)
            if not self.renderer.isValid():
                self.renderer = None
                print("Warning: SVG data is invalid!")
                
        except TypeError:
            self.renderer = None
            print("Warning: SVG data is invalid!")

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        if parent is not None and isinstance(parent, QtWidgets.QWidget):
            self.setSizePolicy(parent.sizePolicy())
        else:
            self.setSizePolicy( QtWidgets.QSizePolicy.Preferred,
                                QtWidgets.QSizePolicy.Preferred)
            print("Warning: SVG parent is not a QWidget!")
            
    
    def paintEvent(self, event: QtGui.QPaintEvent):
        if self.renderer and self.renderer.isValid():
            painter = QPainter(self)
            self.renderer.render(painter, self.rect())
            

class pyside_master_app_names:
    """Pyside app names to use with PS_CLS being the default app name.</br>
    
    """
    PS_CLS: Final[str] = "_f3husd_ps_cls" # Default app name
    PS_CLS_ABOUT: Final[str] = "_f3husd_ps_cls_about"
    
    
class pyside_master_base_proto(Protocol):
    """the protocol to check which pyside_master classes agree with it.
    
    """ 
    def null(self) -> str: ...


class pyside_utils:
    """
class pyside_utils

@STATICMETHODS
* pyside_panels_safe_launch(ps_cls: Type[pyside_master_base_proto], 
                                    app_name: str = pyside_master_app_names.PS_CLS, 
                                    run: bool = True, 
                                    *args, 
                                    **kwargs
                                    ) -> None:

"""
    
    @staticmethod
    def pyside_panels_safe_launch(ps_cls: Type[pyside_master_base_proto], 
                                  app_name: str = pyside_master_app_names.PS_CLS, 
                                  run: bool = True, 
                                  *args, 
                                  **kwargs
                                  ) -> None:
        """Safely run a pyside panel,</br>
        additionally there is the option to only remove an already exisiting one.</br>

        Args:
            ps_cls(Type[pyside_master_base_proto]): Any of the classes that agree to the pyside_master_base_proto protocol.
            app_name(str): Default to: "_ps_cls"</br>The app name.
            run(str): Default to: True</br>When False, it will close/exit the app with the <b>varname</b>.
            args: Any args to pass to the <b>ps_cls</b> if any.</br>
            kwargs: Any kwargs to pass to the <b>ps_cls</b> if any, following a list:</br><b>parent</b>=None (usually untouched)</br><b>ps_app_name</b>=pyside_master_app_names.PS_CLS (Never to be set as it will always be set to: <b>app_name</b> internally)</br><b>f3husd_node</b>=None (This FLAM3H™ node)</br><b>app_info</b>=APP_INFO (The main info message string)</br><b>links</b>=False (When True it will display FLAM3H™ related web links)</br><b>auto_close_ms</b>=5000 (Timer in millisecond. Default to 5 seconds)</br><b>fade_in_ms</b>=None (Fade in time in millisecond. Default to 0(Zero))</br><b>fade_out_ms</b>=None (Fade ot time in millisecond. Default to 0(Zero))</br><b>splash_screen</b>=False (When True it will force the banner image to be load even if some chackes fail, just for the splash screen)</br>
            
        Returns:
            (None):
        """ 
        
        if hasattr(builtins, app_name):
            try:
                getattr(builtins, app_name).close()
                delattr(builtins, app_name) # probably not needed anymore but just in case
            except AttributeError:
                pass
            
        if __pyside_version__ is not None:
            
            if hou.isUIAvailable() and run:
                
                ps_app_name: str | None = kwargs.get("ps_app_name")
                if ps_app_name is None and app_name != pyside_master_app_names.PS_CLS:
                    kwargs["ps_app_name"] = app_name
                    
                h_version: int = flam3husd_general_utils.houdini_version(2)
                if __pyside_version__ == 6:
                    if h_version > 205:
                        setattr(builtins, app_name, ps_cls(*args, **kwargs))
                        getattr(builtins, app_name).show()
                        
                elif __pyside_version__ == 2:
                    if h_version == 205:
                        setattr(builtins, app_name, ps_cls(*args, **kwargs))
                        getattr(builtins, app_name).show()
                    
        else:
            _MSG: str = """
WARNING: This \"PySide\" and/or \"Qt\" versions are not supported just yet.
Supported and tested versions are:\n
FLAM3H™USD H20.5 - PySide2 version: 5.15.15
FLAM3H™USD H20.5 - Qt version: 5.15.2
FLAM3H™USD H21.0 - PySide6 version: 6.5.3
FLAM3H™USD H21.0 - Qt version: 6.5.3
"""
            print(f"{_MSG}\n")


class pyside_master:
    """Ideally this class will contain all pyside classes for FLAM3H™USD panels and such.</br>
    For now there is just one, its a start...
    
    """ 
    
    class F3HUSD_msg_panel(QtWidgets.QWidget):
        """A default PySide meassage panel.</br></br>

        Can be used in different scenarios to display a short message nicely.</br></br>
        
        It features auto close timer, fade in, fade out.</br>
        and allow drawing Svg files on top of banner images as well.</br></br>
        
        Everything is properly scaled to keep the right size and proportions</br>
        across different screen sizes (4K, HD, ...) and few more features.</br></br>
        
        It is a work in progress and it will likely grow in the future.</br>
        
        """

        APP_NAME: str = "FLAM3H™USD"
        
        APP_INFO: str = (
            "Nothing yet\n"
        )

        APP_COPYRIGHT: str = (
            "\n"
            f"v{__version__} indie {flam3husd_scripts.flam3husd_compatible_h_versions_msg(nodetype.hdaModule().__h_versions__, False, True)}, {__license__} - {__copyright__} ( made in Italy )"
        )
        
        # milliseconds
        FADE_IN_DURATION_MS: int = 0
        FADE_OUT_DURATION_MS: int = 0
        
        BG_COLOR: str = "#f4f6f8"
        TEXT_COLOR: str = "#2b2b2b"
        
        BASE_WINDOW_WIDTH: int = 512
        BASE_WINDOW_HEIGHT: int = 472
        BASE_DRAG_POSITION: QtCore.QPoint | None = None
        
        BASE_BANNER_HEIGHT: int = 300
        
        BASE_SVG_ICON_SIZE: int = 96
        
        IMG_PIXMAP: QtGui.QPixmap | None = None
        IMG_PIXMAP_SECTION_NAME: str = f3husd_HDAsections.HDA_SECTION_IMG_BANNER
        
        SVG_ICON: SvgIcon | None = None
        SVG_ICON_W_SECTION_NAME: str = f3husd_HDAsections.HDA_SECTION_SVG_LOGO
        SVG_ICON_R_SECTION_NAME: str = f3husd_HDAsections.HDA_SECTION_SVG_LOGO_RED
        
        NODETYPE: hou.SopNodeType = nodetype

        def __init__(   self, 
                        parent=None, 
                        f3husd_node: hou.SopNode | None = None, 
                        app_info: str = APP_INFO, 
                        ps_app_name: str = pyside_master_app_names.PS_CLS, 
                        links: bool = False, 
                        auto_close_ms: int = 5000, 
                        fade_in_ms: int | None = None, 
                        fade_out_ms: int | None = None,
                        splash_screen: bool = False, 
                     ):
            super().__init__(parent)
            
            app: QtCore.QCoreApplication | None = QtWidgets.QApplication.instance()
            if app:
                
                self.ps_app_name = ps_app_name if ps_app_name else pyside_master_app_names.PS_CLS
                
                # DPI scaling
                screen: QtGui.QScreen = app.primaryScreen()
                self.dpi_scale: float = screen.logicalDotsPerInch() / 96.0

                self.window_width: int = int(self.BASE_WINDOW_WIDTH * self.dpi_scale)
                self.window_height: int = int(self.BASE_WINDOW_HEIGHT * self.dpi_scale)
                self.banner_height: int = int(self.BASE_BANNER_HEIGHT * self.dpi_scale)
                self.svg_icon_size: int = int(self.BASE_SVG_ICON_SIZE * self.dpi_scale)
                
                self.f3husd_node: hou.SopNode | None = f3husd_node if f3husd_node is not None and f3husd_node.type().nameWithCategory() == FLAM3HUSD_NODE_TYPE_NAME_CATEGORY else None
                self.h_valid: int | None = f3husd_node.parm(f3husd_tabs.PREFS.PVT_PRM_FLAM3HUSD_DATA_H_VALID).eval() if f3husd_node is not None else None
                self.splash_screen = splash_screen
                
                # Check if the user want fade in and/or fade out (Disabled by default)
                if fade_in_ms is not None and isinstance(fade_in_ms, int | float): self.FADE_IN_DURATION_MS = int(fade_in_ms)
                if fade_out_ms is not None and isinstance(fade_out_ms, int | float): self.FADE_OUT_DURATION_MS = int(fade_out_ms)
                
                self.font_os: QtGui.QFont = app.font()

                # Add FLAM3H™ weblinks
                self.LINKS: bool = links
                # in case of a custom message, this must be a one liner ending with a newline(\n). Meant for short descriptive messages.
                # Check: APP_INFO variable for an example as it is the default message
                self.INFO = '' if self.LINKS else app_info if app_info else "\n"

                # Frameless + always on top
                self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
                self.setFixedSize(self.window_width, self.window_height)
                
                if (self.f3husd_node is not None and self.h_valid) or self.splash_screen: self._load_image_pixmap()
                self._center_window()
                self._build_ui()

                # Fade in animation
                self._start_fade_in()

                # Auto close with fade out
                if isinstance(auto_close_ms, int | float) and int(auto_close_ms) > 0:
                    fade_out_start: int = max(0, int(auto_close_ms) - self.FADE_OUT_DURATION_MS)
                    QtCore.QTimer.singleShot(fade_out_start, lambda: self._start_fade_out(self.FADE_OUT_DURATION_MS))


        # PROTOCOL
        def null(self) -> str: ...
        
            
        # LOAD BANNER IMG
        def _load_image_pixmap(self) -> None:
            try:
                section_img: hou.HDASection = self.NODETYPE.definition().sections()[self.IMG_PIXMAP_SECTION_NAME]
            except KeyError:
                print(f"Warning: Banner image: HDASection[{self.IMG_PIXMAP_SECTION_NAME}] not found!")
            else:
                # PIXMAP LOAD
                self.IMG_PIXMAP = QtGui.QPixmap()
                self.IMG_PIXMAP.loadFromData(QtCore.QByteArray(section_img.binaryContents()))
                
                
        # LOAD SVG ICON
        def _load_svg_icon(self) -> None:
            svg_icon_name: str = self.SVG_ICON_W_SECTION_NAME
            try:
                if self.h_valid or self.splash_screen:
                    section_svg: hou.HDASection = self.NODETYPE.definition().sections()[self.SVG_ICON_W_SECTION_NAME]
                else:
                    section_svg: hou.HDASection = self.NODETYPE.definition().sections()[self.SVG_ICON_R_SECTION_NAME]
                    
            except KeyError:
                svg_icon_name = self.SVG_ICON_R_SECTION_NAME
                print(f"Warning: SVG icon: HDASection[{svg_icon_name}] not found!")
                
            else:
                svg_bytes: QtCore.QByteArray = QtCore.QByteArray(section_svg.binaryContents())
                self.SVG_ICON = SvgIcon(svg_bytes, parent=self.banner_container)
                self.SVG_ICON.resize(self.svg_icon_size, self.svg_icon_size)
            
            
        # CENTER WINDOW
        def _center_window(self) -> None:
            
            try:
                main_win: QtWidgets.QWidget = hou.qt.mainWindow()
                houdini_geom: QtCore.QRect = main_win.frameGeometry()
                
                best_screen: QtGui.QScreen | None = None
                max_area: int = 0
                for screen in QtWidgets.QApplication.screens():
                    intersect: QtCore.QRect = houdini_geom.intersected(screen.availableGeometry())
                    area: int = intersect.width() * intersect.height()
                    if area > max_area:
                        max_area = area
                        best_screen = screen

                if best_screen is None:
                    best_screen = QtWidgets.QApplication.primaryScreen()

                geom: QtCore.QRect = best_screen.availableGeometry()
                x: int = geom.x() + (geom.width() - self.width()) // 2
                y: int = geom.y() + (geom.height() - self.height()) // 2
                self.move(x, y)
                
            except Exception:
                geom: QtCore.QRect = QtWidgets.QApplication.primaryScreen().availableGeometry()
                x: int = (geom.width() - self.width()) // 2
                y: int = (geom.height() - self.height()) // 2
                self.move(x, y)


        # BUILD UI
        def _build_ui(self) -> None:
            
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.BG_COLOR};
                }}
                QLabel {{
                    color: {self.TEXT_COLOR};
                }}
            """)

            main_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(int(10 * self.dpi_scale))
            main_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            # Banner
            self.banner_container: QtWidgets.QWidget = QtWidgets.QWidget()
            self.banner_container.setFixedSize(self.window_width, self.banner_height)
            self.banner_container.setStyleSheet("background: black;") # transparent
            main_layout.addWidget(self.banner_container)

            self.image_label: QtWidgets.QLabel = QtWidgets.QLabel(self.banner_container)
            self.image_label.setGeometry(0, 0, self.window_width, self.banner_height)
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)
            self._update_banner()

            # Svg
            self._load_svg_icon()
            self._position_svg_icon()

            # Init font, dn't needed but just in case!
            if self.font_os is None:
                # in my case being on windows
                self.font_os = QtGui.QFont("Segoe UI")


            # Title
            title_label: QtWidgets.QLabel = QtWidgets.QLabel(self.APP_NAME, self)
            title_label.setAlignment(QtCore.Qt.AlignCenter)
            self.font_os.setPointSize(22)
            self.font_os.setBold(True)
            title_label.setFont(self.font_os)
            main_layout.addWidget(title_label)
            
            # Info
            info_label: QtWidgets.QLabel = QtWidgets.QLabel(self.INFO, self)
            info_label.setAlignment(QtCore.Qt.AlignCenter)
            self.font_os.setPointSize(16)
            self.font_os.setBold(False)
            info_label.setFont(self.font_os)
            info_label.setWordWrap(True)
            main_layout.addWidget(info_label)
            
            # Clickable links
            if self.LINKS:
                links_label: QtWidgets.QLabel = QtWidgets.QLabel(self.INFO, self)
                links_label.setAlignment(QtCore.Qt.AlignCenter)
                self.font_os.setPointSize(10)
                self.font_os.setBold(False)
                links_label.setFont(self.font_os)
                links_label.setWordWrap(True)
                links_label.setTextFormat(QtCore.Qt.RichText)
                links_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
                links_label.setOpenExternalLinks(True)
                links_label.setText(f"""
                <html>
                    <body>
                    <a href="https://www.alexnardini.net">Website</a>
                    <a href="https://www.instagram.com/alexnardini/">Instagram</a>
                    <a href="https://www.youtube.com/@alexnardiniITALY/videos">Youtube</a>
                    <a href="https://github.com/alexnardini/FLAM3_for_SideFX_Houdini">Github</a>
                    </body>
                </html>
                """)
                main_layout.addWidget(links_label)
            
            # Copyright
            copyright_label: QtWidgets.QLabel = QtWidgets.QLabel(self.APP_COPYRIGHT, self)
            copyright_label.setAlignment(QtCore.Qt.AlignCenter)
            self.font_os.setPointSize(10)
            copyright_label.setFont(self.font_os)
            copyright_label.setWordWrap(True)
            main_layout.addWidget(copyright_label)

            main_layout.addStretch()
            
            
        def _start_fade_in(self) -> None:
            # Fade in animation
            self.setWindowOpacity(0)
            self.fade_in_anim: QtCore.QPropertyAnimation = QtCore.QPropertyAnimation(self, b"windowOpacity")
            self.fade_in_anim.setDuration(self.FADE_IN_DURATION_MS)
            self.fade_in_anim.setStartValue(0)
            self.fade_in_anim.setEndValue(1)
            self.fade_in_anim.start()
            

        # BANNER UPDATE: SCALE + CROP
        def _update_banner(self) -> None:
            if self.IMG_PIXMAP:
                try:
                    w: int = self.banner_container.width()
                    h: int = self.banner_container.height()
                    scaled: QtGui.QPixmap = self.IMG_PIXMAP.scaled(w, h, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
                    x_offset: int = (scaled.width() - w) // 2
                    y_offset: int = (scaled.height() - h) // 2
                    cropped: QtGui.QPixmap = scaled.copy(x_offset, y_offset, w, h)
                    self.image_label.setPixmap(cropped)
                    
                except Exception as e:
                    print("Failed to update banner:", e)
                    
            else:
                if (self.f3husd_node is not None and self.h_valid) or self.splash_screen:
                    self.image_label.setText("🎨")
                    font = self.font_os
                    font.setPointSize(72)
                    self.image_label.setFont(font)
                    self.image_label.setAlignment(QtCore.Qt.AlignCenter)


        # SVG POSITION
        def _position_svg_icon(self) -> None:
            if self.SVG_ICON:
                x: int = (self.banner_container.width() - self.SVG_ICON.width()) // 2
                y: int = (self.banner_container.height() - self.SVG_ICON.height()) // 2
                self.SVG_ICON.move(x, y)
                
                
        # FADE OUT ANIMATION
        def _start_fade_out(self, fade_out_duration_ms) -> None:
            self.fade_out_anim: QtCore.QPropertyAnimation = QtCore.QPropertyAnimation(self, b"windowOpacity")
            self.fade_out_anim.setDuration(fade_out_duration_ms)
            self.fade_out_anim.setStartValue(1)
            self.fade_out_anim.setEndValue(0)
            self.fade_out_anim.finished.connect(self._exit)
            self.fade_out_anim.start()
                
            
        # PYSIDE: RESIZE EVENT
        def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
            super().resizeEvent(event)
            self._position_svg_icon()
            self._update_banner()


        # PYSIDE: DRAG SUPPORT MOUSE PRESS EVENT
        def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
            if event.button() == QtCore.Qt.LeftButton:
                
                if __pyside_version__ == 6:
                    self.BASE_DRAG_POSITION = event.globalPosition().toPoint()
                elif __pyside_version__ == 2:
                    self.BASE_DRAG_POSITION = event.globalPos()


        # PYSIDE: DRAG SUPPORT MOUSE MOVE EVENT
        def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
            if event.buttons() == QtCore.Qt.LeftButton and self.BASE_DRAG_POSITION:
                
                if __pyside_version__ == 6:
                    delta = event.globalPosition().toPoint() - self.BASE_DRAG_POSITION
                elif __pyside_version__ == 2:
                    delta = event.globalPos() - self.BASE_DRAG_POSITION
                    
                self.move(self.x() + delta.x(), self.y() + delta.y())
                
                if __pyside_version__ == 6:
                    self.BASE_DRAG_POSITION = event.globalPosition().toPoint()
                elif __pyside_version__ == 2:
                    self.BASE_DRAG_POSITION = event.globalPos()
                
                
        # PYSIDE: CLOSE EVENT
        def closeEvent(self, event: QtGui.QCloseEvent) -> None:
            try:
                delattr(builtins, self.ps_app_name)
            except AttributeError:
                pass
            
            event.accept()
            

        # EXIT
        def _exit(self) -> None:
            self.close()
