from __future__ import division
from __future__ import annotations

__author__ = "F stands for liFe ( made in Italy )"
__copyright__ = "Copyright 2021, © F stands for liFe"

__license__ = "GPL"
__version__ = "1.8.33"
__maintainer__ = "Alessandro Nardini"
__status__ = "Production"

import os
import json
import colorsys
import lxml.etree as lxmlET
import hou
import nodesearch

from platform import python_version
from platform import system as platform_system
from typing import Callable
from typing import KeysView
from typing import TypeVar
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import TypeAlias
from itertools import count as iter_count
from itertools import islice as iter_islice
from textwrap import wrap
from datetime import datetime
from math import sin
from math import cos
from copy import copy
from re import sub as re_sub
from re import search as re_search
from numpy import pad as np_pad
from numpy import resize as np_resize
from numpy import transpose as np_transpose
from numpy import searchsorted as np_searchsorted
from webbrowser import open as www_open
from inspect import cleandoc as i_cleandoc


'''
    Tested on:  PYTHON v3.11.7  (H20.5)

    Title:      FLAM3H. SideFX Houdini FLAM3: PYTHON
    Author:     Alessandro Nardini
    date:       April 2025, Last revised April 2025 (cloned from: py_flam3__3_7.py)

    Name:       PY_FLAM3__3_11 "PYTHON" ( The ending filename digits represent the least python version needed to run this code )

    Comment:    Python classes and definitions for:
                - General UX
                - Menus builder
                - Copy/Paste iterator's data
                - Load/Save flame files
                - Load/Save palettes
                - Fully automated UX Xaos
                - Tool's user experience
                - and more...
                
                This code will be turned into a module from within Houdini.

                _NOTE:
                    Some definitions run directly from inside the FLAM3H parameters.
                    Please check the file: ../py_flam3_UI_PRM_map.py
                    to see if any of the definition you are curious about is being used inside any of the FLAM3H parameters directly.
                    The file include a list/map of all the definitions used directly inside FLAM3H and categorized as:
                        
                        - callback script
                        - menu script
                        - action button script

                INTERACTIVE Section:
                    The interactive python side for this tool is not done;
                    If you select a FLAM3H node and press the "enter" key over a viewer nothing will happen.
                    It is something nice to try to implement at some point but as of now, it is not a deal breaker at all
                    and the current implementation of the UX is far more than enough to enjoy the fractal art workflow.

                DOC-STRINGS
                    To distinguish class @staticmethods from the class @methods, the class @methods doc-string Args list always start with the argument: (self):
                    This make it easier to distinguish them when typing their name while checking their infos like for example in VSCode. 


                LIST OF CLASSES:

                    flam3h_iterator_prm_names
                    flam3h_iterator_prm_names_collections
                    flam3h_varsPRM
                    flam3h_iterator
                    flam3h_varsPRM_FF
                    flam3h_iterator_FF
                    flam3h_scripts
                    flam3h_general_utils
                    flam3h_iterator_utils
                    flam3h_palette_utils
                    flam3h_about_utils
                    flam3h_ui_msg_utils

                    flam3h_varsPRM_APO
                    _xml
                    _xml_tree
                    in_flame(_xml_tree)
                    in_flame_iter_data(in_flame)
                    in_flame_utils

                    out_flame_utils
                    out_flame_render_properties(out_flame_utils)
                    out_flame_xforms_data(out_flame_utils)

                    _NOTE:
                        - Class @properties are always defined inbetween the @staticmethods and the class methods.
                        - Global variables are all upper cases. Every upper case variable's name created inside any definition always start with an underscore (_)

'''


T = TypeVar('T')

TA_TypeVarCollection: TypeAlias = str | list | tuple | KeysView
TA_XformVarKeys: TypeAlias = str | list[str] | tuple[str] | dict[str, int] | dict[str, tuple] | KeysView | None
TA_TypeMaker: TypeAlias = list | float | hou.Vector2 | hou.Vector3 | hou.Vector4
TA_F3H_Init: TypeAlias = tuple[str | None, bool, int, str, bool, bool]
TA_MNode: TypeAlias = hou.SopNode | None
TA_M: TypeAlias = int | None


CHARACTERS_ALLOWED = "_-().:"
CHARACTERS_ALLOWED_OUT_AUTO_ADD_ITER_NUM = "_-+!?().: "
CHARACTERS_ALLOWED_XFORM_VAL = "0123456789.-e"

# Default globals
FLAM3H_DEFAULT_GLB_DENSITY: int = 500000
FLAM3H_DEFAULT_GLB_ITERATIONS: int = 10
# On IN Flame preset load set the iteration number to use to this value.
# This setting will be overwritten if the IN Tab "force iterations on Load" option is turned ON.
# All of the above settings will be overwritten if the iteration number to use is baked into the Flame preset's name.
FLAM3H_DEFAULT_IN_ITERATIONS_ON_LOAD: int = 64
FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV = '::'

# Node user data (nodeinfo)
FLAM3H_USER_DATA_PRX = "nodeinfo"
FLAM3H_USER_DATA_ITER = "Marked iterator"
FLAM3H_USER_DATA_FF = "Marked FF"
FLAM3H_USER_DATA_XF_VIZ = "XF VIZ"
# Node user data
FLAM3H_USER_DATA_XML_LAST = 'XML_last_loaded'

# Main tab in the UI
FLAM3H_ITERATORS_TAB = "f_flam3h"

# Default affine values
AFFINE_DEFAULTS: dict[str, hou.Vector2 | float] = {"affine_x": hou.Vector2((1.0, 0.0)), "affine_y": hou.Vector2((0.0, 1.0)), "affine_o": hou.Vector2((0.0, 0.0)), "angle": float(0.0)} # X, Y, O, ANGLE
AFFINE_IDENT: list = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

# FF parametric parameter's prefixes
# FF posses two sets of parametric variations parameters, one for the VAR named "VARS" and one for the PRE and POST, named "PP: VARS"
PRX_FF_PRM = 'ff'
PRX_FF_PRM_POST = 'fp1'

# vars names identifiers for parametrics and dependants
DPT = '*'
PRM = '...'

# copy/paste set note sections names
SEC_ALL = '.ALL'
SEC_MAIN = '.main'
SEC_XAOS = '.xaos'
SEC_SHADER = '.shader'
SEC_PREVARS = '.PRE'
SEC_VARS = '.VAR'
SEC_POSTVARS = '.POST'
SEC_PREAFFINE = '.pre affine'
SEC_POSTAFFINE = '.post affine'

# Saving flames out will always use the standard PALETTE_COUNT_256
# but saving palette out will downsample if possible to save some data but with an allowed MAX of 256...for now.
# def get_ramp_keys_count(ramp: hou.Ramp) -> str: -> need to be reworked to allow more than 256. Same goes to the OUT flame palette.
PALETTE_COUNT_64 = '64' # not used
PALETTE_COUNT_128 = '128'
PALETTE_COUNT_256 = '256'
PALETTE_COUNT_512 = '512' # not used
PALETTE_COUNT_1024 = '1024'
PALETTE_OUT_MENU_OPTIONS_ALL: tuple = (16, 32, 64, 128, 256, 512, 1024) # not used
PALETTE_OUT_MENU_OPTIONS_PLUS: tuple = (256, 512, 1024)
PALETTE_PLUS_MSG = '[256+]'
# The following will always be used for now
# even tho we check for the XML palette format on load.
PALETTE_FORMAT = 'RGB'

# Automated CP or OUT names
AUTO_NAME_CP = 'Palette'
AUTO_NAME_OUT = 'Flame'

# Parameters at hand
GLB_DENSITY = 'ptcount'
GLB_DENSITY_PRESETS = 'ptcount_presets'
GLB_ITERATIONS = 'iter'
SYS_SELECT_ITERATOR = 'iterlist'
SYS_XF_VIZ_OFF = 'xfviz_off'
SYS_XF_VIZ_ON = 'xfviz_on'
SYS_TAG_SIZE = 'tagsize'
SYS_FRAME_VIEW_SENSOR = 'frameviewsensor'
FLAME_ITERATORS_COUNT = 'flamefunc'
CP_PALETTE_LIB_PATH = 'palettefile'
CP_PALETTE_OUT_PRESET_NAME = 'palettename'
CP_PALETTE_PRESETS = 'palettepresets'
CP_PALETTE_PRESETS_OFF = 'palettepresets_off'
CP_SYS_PALETTE_PRESETS = 'sys_palettepresets'
CP_SYS_PALETTE_PRESETS_OFF = 'sys_palettepresets_off'
CP_RAMP_LOOKUP_SAMPLES = 'cp_lookupsamples'
CP_RAMP_SRC_NAME = 'palette'
CP_RAMP_TMP_NAME = 'palettetmp'
CP_RAMP_HSV_NAME = 'palettehsv'
CP_PALETTE_256_PLUS = 'cppaletteplus'
CP_RAMP_SAVE_HSV = 'savehsv'
CP_RAMP_HSV_KEEP_ON_LOAD = 'keephsv'
CP_RAMP_HSV_VAL_NAME = 'hsv'
# CP SYSTEM PRIVATE
CP_PVT_ISVALID_FILE = 'cpisvalidfile'
CP_PVT_ISVALID_PRESET = 'cpisvalidpreset'

MB_DO = 'domb'
MB_FPS = 'fps'
MB_SAMPLES = 'mbsamples'
MB_SHUTTER = 'shutter'
MB_VIZ = 'vizmb'
IN_CLIPBOARD_LABEL_MSG = '[CLIPBOARD]'
IN_HSV_LABEL_MSG = '[HSV]'
IN_PATH = 'inpath'
IN_PRESETS = 'inpresets'
IN_PRESETS_OFF = "inpresets_disabled"
IN_SYS_PRESETS = 'sys_inpresets'
IN_SYS_PRESETS_OFF = 'sys_inpresets_disabled'
IN_USE_ITER_ON_LOAD = 'useiteronload'
IN_OVERRIDE_ITER_FLAME_NAME = 'oritername'
IN_ITER_NUM_ON_LOAD = 'iternumonload'
IN_FLAM3H_AFFINE_STYLE = 'in_f3h_affine'
IN_COPY_RENDER_PROPERTIES_ON_LOAD = 'propertiescp'
# IN SYSTEM PRIVATE
IN_PVT_ISVALID_FILE = 'inisvalidfile'
IN_PVT_ISVALID_PRESET = 'inisvalidpreset'
IN_PVT_CLIPBOARD_TOGGLE = 'inclipboard'

OUT_PATH = 'outpath'
OUT_PRESETS = 'outpresets'
OUT_SYS_PRESETS = 'sys_outpresets'
OUT_FLAME_PRESET_NAME = 'outname'
OUT_AUTO_ADD_ITER_NUM = 'autoadditer'
OUT_UPDATE_SENSOR = 'outsensorupdate'
OUT_HSV_PALETTE_DO = 'outpalette'
OUT_FLAM3H_AFFINE_STYLE = 'out_f3h_affine'
OUT_IN_FLAME_NAME_AUTO_FILL = 'out_in_flame_name'
OUT_USE_FRACTORIUM_PRM_NAMES = 'outfractoriumprm'
OUT_PALETTE_FILE_EXT = '.json'
OUT_FLAM3_FILE_EXT = '.flame'
OUT_RENDER_PROPERTIES_EDIT = 'outedit'
OUT_RENDER_PROPERTIES_SENSOR = 'outsensor'
OUT_RENDER_PROPERTIES_SENSOR_ENTER = 'out_sensorviz_disabled'
OUT_RENDER_PROPERTIES_RES_PRESETS_MENU = 'outrespresets'
# Curves
OUT_TOGGLE_CC_DEFAULTS_MSG = 'outccdefault'
OUT_LABEL_CC_DEFAULTS_MSG = 'label_outccdefault'
OUT_RENDER_PROPERTIES_CURVES = 'outcurvesval'
OUT_RENDER_PROPERTIES_CURVE_OVERALL = 'outcurveoverallval'
OUT_RENDER_PROPERTIES_CURVE_RED = 'outcurveredval'
OUT_RENDER_PROPERTIES_CURVE_GREEN = 'outcurvegreenval'
OUT_RENDER_PROPERTIES_CURVE_BLUE = 'outcurveblueval'
# OUT SYSTEM PRIVATE
OUT_PVT_ISVALID_FILE = 'outisvalidfile'

# NODE NAMES
# Those Null node names are hard coded here and represent the nodes name's prefix.
# If you change those Null node names inside the FLAM3H houdini HDA network, update those global variables as well.
# If not, the camera sensor mode wont be able to properly frame itself in the current viewport.
OUT_BBOX_NODE_NAME_SENSOR = 'OUT_bbox_sensor' # prefix
OUT_BBOX_NODE_NAME_REFRAME = 'OUT_bbox_reframe' # prefix
# PREFS XF VIZ NODE NAME TO COOK
PREFS_XFVIZ_NODE_NAME = 'XFVIZ_GL'
# XAOS
TFFA_XAOS = '_TFFAxaos'

PREFS_PALETTE_256_PLUS = 'paletteplus'
PREFS_FLASH_MSG = 'flashmsg'
PREFS_ITERATOR_BOOKMARK_ICONS = 'itericons'
PREFS_ENUMERATE_MENU = 'enumeratemenu'
PREFS_CVEX_PRECISION = 'vex_precision'
PREFS_XAOS_MODE = 'xm'
PREFS_CAMERA_HANDLE = 'camhandle'
PREFS_CAMERA = 'fcam'
PREFS_CAMERA_CULL = 'camcull'
PREFS_CAMERA_CULL_AMOUNT = 'cullamount'
PREFS_VIEWPORT_DARK = 'setdark'
PREFS_VIEWPORT_WIRE_WIDTH = 'vpww'
PREFS_VIEWPORT_PT_TYPE = 'vptype'
PREFS_VIEWPORT_PT_SIZE = 'vpptsize'
# PRIVATE PREFS SYSTEM
PREFS_PVT_DOFF = 'doff'
PREFS_PVT_RIP = 'rip'
PREFS_PVT_F3C = 'f3c'
PREFS_PVT_TAG = 'tag'
PREFS_PVT_XAOS_AUTO_SPACE = 'xaosdiv'
PREFS_PVT_AUTO_PATH_CORRECTION = 'autopath'
PREFS_PVT_XF_VIZ = 'vizhandles'
PREFS_PVT_XF_VIZ_SOLO = 'vizhandles_solo'
PREFS_PVT_XF_VIZ_SOLO_MP_IDX = 'vizhandles_solo_mpidx'
PREFS_PVT_XF_FF_VIZ_SOLO = 'vizhandlesff_solo'
# PRIVATE PREFS TEMP PARMS
PREFS_PVT_INT_0 = 'tmp_int_0'
PREFS_PVT_INT_1 = 'tmp_int_1'
PREFS_PVT_FLOAT_0 = 'tmp_float_0'
PREFS_PVT_FLOAT_1 = 'tmp_float_1'
# PREFS SYSTEM PRIVATE: self prm names for user data
FLAM3H_DATA_PRM_XAOS_MP_MEM = 'flam3h_data_mpmem'
FLAM3H_DATA_PRM_XAOS_PREV = 'flam3h_data_xaos'
FLAM3H_DATA_PRM_MPIDX = 'flam3h_data_mpidx'
# Flame stats locked message string
MSG_FLAMESTATS_LOCK = '-> LOCKED'
# Flame stats message parameters
MSG_IN_STATS_HEADING = 'flamestats_heading'
MSG_IN_STATS_HEADING_DEFAULT = 'IN flame preset infos'
MSG_IN_SETTINGS_HEADING = 'flamerender_heading'
MSG_IN_SETTINGS_HEADING_DEFAULT = 'IN flame preset renderer settings'
MSG_IN_FLAMESTATS = 'flamestats_msg'
MSG_IN_FLAMESENSOR = 'flamesensor_msg'
MSG_IN_FLAMERENDER = 'flamerender_msg'
MSG_DESCRIPTIVE_PRM = 'descriptive_msg'
# Presets PRM and MSG
MSG_PALETTE = 'palettemsg'
MSG_PALETTE_MSG = 'Palette lib file: LOCKED'
MSG_OUT = 'outmsg'
MSG_OUT_MSG = 'Flame lib file: LOCKED'
# Message About Tab parameters
MSG_FLAM3H_ABOUT = 'flam3about_msg'
MSG_FLAM3H_PLUGINS = 'flam3plugins_msg'
MSG_FLAM3H_WEB = 'flam3h_heading_web'
MSG_FLAM3H_GIT = 'flam3h_heading_git'
MSG_FLAM3H_INSTA = 'flam3h_heading_insta'
MSG_FLAM3H_YOUTUBE = 'flam3h_heading_youtube'
MSG_FLAM3_PDF = 'flam3_heading_pdf'
MSG_FLAM3_GIT = 'flam3_heading_git'
MSG_FRACT_BITBUCKET = 'fract_heading_bit'
MSG_FRACT_WEB = 'fract_heading_web'
# Message Mark iterators
MARK_ITER_MSG = "Please, mark an iterator first"
MARK_ITER_MSG_STATUS_BAR = f"{MARK_ITER_MSG} to copy parameter's values from."
MARK_FF_MSG = "Please, mark the FF first"
MARK_FF_MSG_STATUS_BAR = f"{MARK_FF_MSG} to copy parameter's values from."
# File lock prefix
FLAM3H_LIB_LOCK = 'F3H_LOCK'
# PALETTE JSON data keys
CP_JSON_KEY_NAME_HEX = 'f3h_hex'
CP_JSON_KEY_NAME_HSV = 'f3h_hsv'
# Flash messages timer
FLAM3H_FLASH_MESSAGE_TIMER: float = 2


class flam3h_iterator_prm_names:

    '''
    Mostly, handy to have all those packed into one class
    for easy access everywhere is needed and better readability.
    
    The parameter names for the FF(finalXform) are the same but with a string prefix: 'ff'
    The FF parametric parameter names are as well the same but with a string prefix: 'ff_'
    Main, Xaos and Shader parameters are not included in the FF but only: PRE, VAR, POST, pre affine and post affine.
    
    Note:
        The following definitions:
        
        * flam3h_iterator_utils.iterator_keep_last_vactive(self) -> None:
        * flam3h_iterator_utils.iterator_keep_last_vactive_STAR(self) -> None:
        * flam3h_iterator_utils.iterator_keep_last_weight(self) -> None:
        * flam3h_iterator_utils.iterator_vactive_and_update(self) -> None:
        * flam3h_iterator_utils.menu_select_iterator_data(self) -> list:
        * flam3h_iterator_utils.menu_select_iterator(self) -> list:
        * flam3h_iterator_utils.menu_copypaste(self) -> list:
        * flam3h_iterator_utils.menu_copypaste_FF(self) -> list:
        * flam3h_iterator_utils.iterator_affine_scale(self) -> None:
        * flam3h_iterator_utils.iterator_post_affine_scale(self) -> None:
        * flam3h_iterator_utils.iterator_FF_affine_scale(self) -> None:
        * flam3h_iterator_utils.iterator_FF_post_affine_scale(self) -> None:
        .
        are not using this class
        but have Houdini parameter's names hard coded inside in an attempt to try to speed up a tiny, tiny bit.
            
        If you update/change the following values and the FLAM3H HDA parameter's names,
        please update inside the above mentioned definitions as well.
    
    '''
    
    __slots__ = ("main_xf_viz", "main_mpmem", "main_note", "main_prmpastesel", "main_selmem", "main_vactive", "main_weight", 
                 "xaos", 
                 "shader_color", "shader_speed", "shader_alpha", 
                 "prevar_blur", "prevar_weight_blur", "prevar_type_1", "prevar_type_2", "prevar_weight_1", "prevar_weight_2", 
                 "var_type_1", "var_type_2", "var_type_3", "var_type_4", "var_weight_1", "var_weight_2", "var_weight_3", "var_weight_4", 
                 "postvar_type_1", "postvar_type_2", "postvar_weight_1", "postvar_weight_2", 
                 "preaffine_scale", "preaffine_x", "preaffine_y", "preaffine_o", "preaffine_ang", 
                 "postaffine_do", "postaffine_scale", "postaffine_x", "postaffine_y", "postaffine_o", "postaffine_ang")
    
    def __init__(self) -> None:
        """
        Args:
            (self):
            
        Returns:
            (None):
        """  
        # ITERATOR
        #
        # Main
        self.main_xf_viz: str = 'xfviz'
        self.main_mpmem: str = 'mpmem' # auto set xaos: custom data
        self.main_note: str = 'note'
        self.main_prmpastesel: str = 'prmpastesel'
        self.main_selmem: str = 'selmem' # custom data
        self.main_vactive: str = 'vactive'
        self.main_weight: str = 'iw'
        # Xaos
        self.xaos: str = 'xaos'
        # Shader
        self.shader_color: str = 'clr'
        self.shader_speed: str = 'clrspeed'
        self.shader_alpha: str = 'alpha'
        # PRE 
        self.prevar_blur: str = 'preblurtype' # this can be omitted as it is always zero
        self.prevar_weight_blur: str = 'preblurweight'
        self.prevar_type_1: str = 'pre1type'
        self.prevar_type_2: str = 'pre2type'
        self.prevar_weight_1: str = 'pre1weight'
        self.prevar_weight_2: str = 'pre2weight'
        # VAR
        self.var_type_1: str = 'v1type'
        self.var_type_2: str = 'v2type'
        self.var_type_3: str = 'v3type'
        self.var_type_4: str = 'v4type'
        self.var_weight_1: str = 'v1weight'
        self.var_weight_2: str = 'v2weight'
        self.var_weight_3: str = 'v3weight'
        self.var_weight_4: str = 'v4weight'
        # POST
        self.postvar_type_1: str = 'p1type'
        self.postvar_type_2: str = 'p2type'
        self.postvar_weight_1: str = 'p1weight'
        self.postvar_weight_2: str = 'p2weight'
        # pre affine
        self.preaffine_scale: str = 'scl' # this do not really need to be stored/copied as it modify the pre affine only.
        self.preaffine_x: str = 'x'
        self.preaffine_y: str = 'y'
        self.preaffine_o: str = 'o'
        self.preaffine_ang: str = 'ang'
        # post affine
        self.postaffine_do: str = 'dopost'
        self.postaffine_scale: str = 'pscl' # this do not really need to be stored/copied as it modify the post affine only.
        self.postaffine_x: str = 'px'
        self.postaffine_y: str = 'py'
        self.postaffine_o: str = 'po'
        self.postaffine_ang: str = 'pang'
    
    
class flam3h_iterator_prm_names_collections(flam3h_iterator_prm_names):
    """
    Args:
        flam3h_iterator_prm_names ([class]): [inherit properties methods from the flam3h_iterator_prm_names class]
    """    
    
    '''
    Mostly, handy to have all those packed into one class.
    They are split into tuple parameters (vector, vector2, vector4...) and not (int, float, string..)
    
    The parametric's parameter names for the FF(finalXform) are the same but with a string prefix: 'ff_' ( f"{PRX_FF_PRM}_{...}" )
    The FF PRE and POST parametric parameter names are as well the same but with a string prefix: 'fp1_' ( f"{PRX_FF_PRM_POST}_{...}" )
    
    If you add new parametric variations add their base parameter's names here accordingly (tuple or not tuple).
    
    '''
    
    __slots__ = ("_prm_iterator_tuple", "_prm_iterator", "_prm_iterator_vars_all", "_prm_FF_tuple", "_prm_FF", "_prm_FF_vars_all", 
                 "_prm_parametrics_tuple", "_prm_parametrics")
    
    def __init__(self) -> None:
        """
        Args:
            (self):
            
        Returns:
            (None):
        """  
        super().__init__()
        
        self._prm_iterator_tuple: tuple = (self.preaffine_x, self.preaffine_y, self.preaffine_o, self.postaffine_x, self.postaffine_y, self.postaffine_o)
        self._prm_iterator: tuple = (self.main_note, self.main_weight, self.xaos, self.shader_color, self.shader_speed, self.shader_alpha, self.prevar_blur, self.prevar_weight_blur, self.prevar_type_1, self.prevar_weight_1, self.prevar_type_2, self.prevar_weight_2, self.var_type_1, self.var_weight_1, self.var_type_2, self.var_weight_2, self.var_type_3, self.var_weight_3, self.var_type_4, self.var_weight_4, self.postvar_type_1, self.postvar_weight_1, self.preaffine_scale, self.preaffine_ang, self.postaffine_do, self.postaffine_scale, self.postaffine_ang)
        self._prm_iterator_vars_all: tuple = (self.prevar_blur, self.prevar_weight_blur, self.prevar_type_1, self.prevar_weight_1, self.prevar_type_2, self.prevar_weight_2, self.var_type_1, self.var_weight_1, self.var_type_2, self.var_weight_2, self.var_type_3, self.var_weight_3, self.var_type_4, self.var_weight_4, self.postvar_type_1, self.postvar_weight_1)
        self._prm_FF_tuple: tuple = (self.preaffine_x, self.preaffine_y, self.preaffine_o, self.postaffine_x, self.postaffine_y, self.postaffine_o)
        self._prm_FF: tuple = (self.main_note, self.prevar_type_1, self.prevar_weight_1, self.var_type_1, self.var_weight_1, self.var_type_2, self.var_weight_2, self.postvar_type_1, self.postvar_weight_1, self.postvar_type_2, self.postvar_weight_2, self.preaffine_scale, self.preaffine_ang, self.postaffine_do, self.postaffine_scale, self.postaffine_ang)
        self._prm_FF_vars_all: tuple = (self.prevar_type_1, self.prevar_weight_1, self.var_type_1, self.var_weight_1, self.var_type_2, self.var_weight_2, self.postvar_type_1, self.postvar_weight_1, self.postvar_type_2, self.postvar_weight_2)
        # Hard coded as this may be the only case with need those parameters.
        # Those are the houdini parametric variations parameters base names.
        self._prm_parametrics_tuple: tuple = ("curlc", "ngon", "pdjw", "blob", "julian", "juliascope", "fan2", "rectangles", "pie", "disc2", "supershape", "supershapen", "flower", "conic", "parabola", "bent2xy", "cpow", "lazysusanxyz", "lazysusan", "modulusXYZ", "oscope", "popcorn2xyz", "separationxyz", "separationinsidexyz", "splitxyz", "splitsxyz", "stripes", "wedge", "wedgejulia", "wedgesph", "whorl", "waves2scalexyz", "waves2freqxyz", "auger", "mobiusre", "mobiusim", "curvexyzlenght", "curvexyzamp", "persp", "bwraps", "bwrapstwist", "polynomialpow", "polynomiallc", "polynomialsc", "cropltrb", "cropaz", "ptsym")
        self._prm_parametrics: tuple = ("rings2val", "radialblur", "bipolarshift", "cellsize", "escherbeta", "popcorn2c", "fluxspread")
        
    
    # CLASS: PROPERTIES
    ##########################################
    ##########################################
    
    @property
    def prm_iterator_tuple(self):
        return self._prm_iterator_tuple
    
    @property
    def prm_iterator(self):
        return self._prm_iterator
    
    @property
    def prm_iterator_vars_all(self):
        return self._prm_iterator_vars_all
    
    @property
    def prm_FF_tuple(self):
        return self._prm_FF_tuple
    
    @property
    def prm_FF(self):
        return self._prm_FF
    
    @property
    def prm_FF_vars_all(self):
        return self._prm_FF_vars_all
    
    @property
    def prm_parametrics_tuple(self):
        return self._prm_parametrics_tuple
    
    @property
    def prm_parametrics(self):
        return self._prm_parametrics


class flam3h_varsPRM:
    """
class flam3h_varsPRM

@STATICMETHODS
* __populate_keys_and_values(keys: list, values: list, item: int | str, id: int) -> None:
* __populate_linear_list(linear: list, item: str, id: int, spacer: bool = True) -> None:

@METHODS
* vars_all(self) -> list:
* menu_vars_all(self) -> list:
* menu_vars_no_PRM(self) -> list:
* build_menu_vars_all_linear(self) -> list:
* build_menu_vars_indexes(self) -> dict[int, int]:

    """ 
    
    __slots__ = ("varsPRM",)
    
    def __init__(self) -> None:
        """
        Args:
            (self):
            
        Returns:
            (None):
        """  
        # Collect all variations and their parametric parameters properly ordered as per flame*.h files
        # Those names are what it will appear inside each variation's menu.
        self.varsPRM: tuple = ( ("Linear", 0), 
                                ("Sinusoidal", 0), 
                                ("Spherical", 0), 
                                ("Swirl", 0), 
                                ("Horseshoe", 0), 
                                ("Polar", 0), 
                                ("Handkerchief", 0), 
                                ("Heart", 0), 
                                ("Disc", 0), 
                                ("Spiral", 0), 
                                ("Hyperbolic", 0), 
                                ("Diamond", 0), 
                                ("Ex", 0), 
                                ("Julia", 0), 
                                ("Bent", 0), 
                                (f"Waves{DPT}", 0), 
                                ("Fisheye", 0), 
                                (f"Popcorn{DPT}", 0), 
                                ("Exponential", 0), 
                                ("Power", 0), 
                                ("Cosine", 0), 
                                (f"Rings{DPT}", 0), 
                                (f"Fan{DPT}", 0), 
                                ("Bubble", 0), 
                                ("Cylinder", 0), 
                                ("Eyefish", 0), 
                                ("Blur", 0), 
                                (f"Curl{PRM}", ("curlc_", 1), 1), 
                                (f"Ngon{PRM}", ("ngon_", 1), 1), 
                                (f"Pdj{PRM}", ("pdjw_", 1), 1), 
                                (f"Blob{PRM}", ("blob_", 1), 1), 
                                (f"JuliaN{PRM}", ("julian_", 1), 1), 
                                (f"Juliascope{PRM}", ("juliascope_", 1), 1), 
                                ("Gaussian_blur", 0), 
                                (f"Fan2{PRM}", ("fan2_", 1), 1), 
                                (f"Rings2{PRM}", ("rings2val_", 0), 1), 
                                (f"Rectangles{PRM}", ("rectangles_", 1), 1), 
                                (f"Radialblur{PRM}", ("radialblur_", 0), 1), 
                                (f"Pie{PRM}", ("pie_", 1), 1), 
                                ("Arch", 0), 
                                ("Tangent", 0), 
                                ("Square", 0), 
                                ("Rays", 0), 
                                ("Blade", 0), 
                                ("Secant2", 0), 
                                ("Twintrian", 0), 
                                ("Cross", 0), 
                                (f"Disc2{PRM}", ("disc2_", 1), 1), 
                                (f"Supershape{PRM}", ("supershape_", 1), ("supershapen_", 1), 1), 
                                (f"Flower{PRM}", ("flower_", 1), 1), 
                                (f"Conic{PRM}", ("conic_", 1), 1), 
                                (f"Parabola{PRM}", ("parabola_", 1), 1), 
                                (f"Bent2{PRM}", ("bent2xy_", 1), 1), 
                                (f"Bipolar{PRM}", ("bipolarshift_", 0), 1),
                                ("Boarders", 0),
                                ("Butterfly", 0), 
                                (f"Cell{PRM}", ("cellsize_", 0), 1), 
                                (f"Cpow{PRM}", ("cpow_", 1), 1), 
                                ("Edisc", 0), 
                                ("Elliptic", 0), 
                                ("Noise", 0), 
                                (f"Escher{PRM}", ("escherbeta_", 0), 1), 
                                ("Foci", 0), 
                                (f"Lazysusan{PRM}", ("lazysusanxyz_", 1), ("lazysusan_", 1), 1), 
                                ("Loonie", 0), 
                                ("Pre blur", 0), 
                                (f"Modulus{PRM}", ("modulusXYZ_", 1), 1), 
                                (f"Oscope{PRM}", ("oscope_", 1), 1), 
                                ("Polar2", 0), 
                                (f"Popcorn2{PRM}", ("popcorn2xyz_", 1), ("popcorn2c_", 0), 1), 
                                ("Scry", 0), 
                                (f"Separation{PRM}", ("separationxyz_", 1), ("separationinsidexyz_", 1), 1), 
                                (f"Split{PRM}", ("splitxyz_", 1), 1), 
                                (f"Splits{PRM}", ("splitsxyz_", 1), 1), 
                                (f"Stripes{PRM}", ("stripes_", 1), 1), 
                                (f"Wedge{PRM}", ("wedge_", 1), 1), 
                                (f"Wedgejulia{PRM}", ("wedgejulia_", 1), 1), 
                                (f"Wedgesph{PRM}", ("wedgesph_", 1), 1), 
                                (f"Whorl{PRM}", ("whorl_", 1), 1), 
                                (f"Waves2{PRM}", ("waves2scalexyz_", 1), ("waves2freqxyz_", 1), 1), 
                                ("Exp", 0), 
                                ("Log", 0), 
                                ("Sin", 0), 
                                ("Cos", 0), 
                                ("Tan", 0), 
                                ("Sec", 0), 
                                ("Csc", 0), 
                                ("Cot", 0), 
                                ("Sinh", 0), 
                                ("Cosh", 0), 
                                ("Tanh", 0), 
                                ("Sech", 0), 
                                ("Csch", 0), 
                                ("Coth", 0), 
                                (f"Auger{PRM}", ("auger_", 1), 1), 
                                (f"Flux{PRM}", ("fluxspread_", 0), 1), 
                                (f"Mobius{PRM}", ("mobiusre_", 1), ("mobiusim_", 1), 1),
                                (f"Curve{PRM}", ("curvexyzlenght_", 1), ("curvexyzamp_", 1), 1), 
                                (f"Perspective{PRM}", ("persp_", 1), 1), 
                                (f"Bwraps{PRM}", ("bwraps_", 1), ("bwrapstwist_", 1), 1), 
                                ("Hemisphere", 0), 
                                (f"Polynomial{PRM}", ("polynomialpow_", 1), ("polynomiallc_", 1), ("polynomialsc_", 1), 1),
                                (f"Crop{PRM}", ("cropltrb_", 1), ("cropaz_", 1), 1),
                                ("Unpolar", 0), 
                                ("Glynnia", 0),
                                (f"Pt_symmetry{PRM}", ("ptsym_", 1), 1)
                                )
            
    
    @staticmethod
    def __populate_keys_and_values(keys: list, values: list, item: int | str, id: int) -> None:
        """ Populate the keys and values lists. This is to be used inside a loop.
        Specifically designed to be used in a list comprehension inside: def build_menu_vars_indexes(self) -> dict[int, int]:
        
        Args:
            keys(str): the keys empty list to populate
            values(str): the values empty list to populate
            item(str): The current loop iteration item
            id(int): The current loop iteration index
            
        Returns:
            (None):
        """
        try:
            int(item)
        except:
            values.append(id)
        else:
            keys.append(item)
            
            
    @staticmethod
    def __populate_linear_list(linear: list, item: str, id: int, spacer: bool = True) -> None:
        """ Populate linear list. This is to be used inside a loop.
        Specifically designed to be used in a list comprehension inside: def build_menu_vars_all_linear(self) -> list:
        
        Args:
            linear(list): the empty list to populate
            item(str): The current loop iteration item
            id(int): The current loop iteration index
            spacer(bool): Default to: True. Add a spacer to the ent of the item to conform with the desired menu label length
            
        Returns:
            (None):
        """
        linear.append(id)
        if spacer: linear.append(f"{item}          ") # 10 times \s
        else: linear.append(item)
    
    
    def vars_all(self) -> list:
        """Build a list of all the variation names properly ordered as per flame*.h files
        
        Args:
            (self):
            
        Returns:
            (list): return a list of all the variation names properly ordered as per flame*.h files
        """

        return list(map(lambda x: x[0], self.varsPRM))
    
    
    def menu_vars_all(self) -> list:
        """This is used to generate the following list: MENU_VARS_ALL
        
        Args:
            (self):
            
        Returns:
            (list): return an enumerated variations menu list with "linear" being the first one for convenience
        """

        vars_no_lin: list = list(enumerate(self.vars_all()))[1:]
        vars_no_lin.remove((65, 'Pre blur')) # remove "pre blur" as it is hard coded into the chaos game.
        vars_sorted: list = sorted(vars_no_lin, key=lambda var: var[1])
        return list(enumerate(['Linear'])) + vars_sorted
    
    
    def menu_vars_no_PRM(self) -> list:
        """Build a list of all the variation names properly ordered as per flame*.h files without the parametric variations in it.
        
        Args:
            (self):
            
        Returns:
            (list): return a list of all the variation names properly ordered as per flame*.h files without the parametric variations in it.
        """   
        return list(map(lambda x: x, filter(lambda x: x[1][-3:]!=PRM, self.menu_vars_all())))
    
    
    def build_menu_vars_all_linear(self) -> list:
        """This is used to generate the following list: MENU_VARS_ALL_SIMPLE
        
        Args:
            (self):
            
        Returns:
            (list): return an linearly composed list with the var index followed by the var name as if it was a Houdini valid menu data
        """  
        linear: list = []
        [self.__populate_linear_list(linear, item, id) for id, item in self.menu_vars_all()]
        return linear
    
    
    def build_menu_vars_indexes(self) -> dict[int, int]:
        """This is used to generate the following dict: MENU_VARS_INDEXES
        
        Args:
            (self):
            
        Returns:
            (dict): a dictionary for the variation indexes used by the menu_T_ICONS definitions
        """   
        keys: list = []
        values: list = []
        [self.__populate_keys_and_values(keys, values, item, id) for id, item in enumerate(self.build_menu_vars_all_linear())]
        return dict(zip(keys, values))


class flam3h_iterator(flam3h_iterator_prm_names):
    """
    Args:
        flam3h_iterator_prm_names ([class]): [inherit properties methods from the flam3h_iterator_prm_names class]
    """   
    
    __slots__ = ("_sec_main", "_sec_xaos", "_sec_shader", "_sec_prevarsT", "_sec_prevarsW", "_sec_varsT", "_sec_varsW", "_sec_postvarsT", "_sec_postvarsW", "_sec_preAffine", "_sec_postAffine", 
                 "_allT", "_allMisc")

    def __init__(self) -> None:
        """
        Args:
            (self):
            
        Returns:
            (None):
        """  
        super().__init__()
        
        # SECTIONS method lists
        #
        # (*T)Types have no signature and always to be used with: pastePRM_T_from_list() for now.
        
        # sec_main = ( (f"{n.main_vactive}_", 0), (f"{n.main_weight}_", 0) )
        
        self._sec_main: tuple = ( (f"{self.main_weight}_", 0),) # When copy/paste the main section it will not copy the ON/OFF(vactive) iterator parameter anymore.
        self._sec_xaos: tuple = ( (f"{self.xaos}_", 0),)
        self._sec_shader: tuple = ( (f"{self.shader_color}_", 0), (f"{self.shader_speed}_", 0), (f"{self.shader_alpha}_", 0) )
        self._sec_prevarsT: tuple = ( f"{self.prevar_type_1}_", f"{self.prevar_type_2}_" ) # preblur is omitted as it is always ZERO
        self._sec_prevarsW: tuple = ( (f"{self.prevar_weight_blur}_", 0), (f"{self.prevar_weight_1}_", 0), (f"{self.prevar_weight_2}_", 0) )
        self._sec_varsT: tuple = ( f"{self.var_type_1}_", f"{self.var_type_2}_", f"{self.var_type_3}_", f"{self.var_type_4}_" )
        self._sec_varsW: tuple = ( (f"{self.var_weight_1}_", 0), (f"{self.var_weight_2}_", 0), (f"{self.var_weight_3}_", 0), (f"{self.var_weight_4}_", 0) )
        self._sec_postvarsT: tuple = ( f"{self.postvar_type_1}_",)
        self._sec_postvarsW: tuple = ( (f"{self.postvar_weight_1}_", 0),)
        self._sec_preAffine: tuple = ( (f"{self.preaffine_x}_", 1), (f"{self.preaffine_y}_", 1), (f"{self.preaffine_o}_", 1), (f"{self.preaffine_ang}_", 0) )
        self._sec_postAffine: tuple = ( (f"{self.postaffine_do}_", 0), (f"{self.postaffine_x}_", 1), (f"{self.postaffine_y}_", 1), (f"{self.postaffine_o}_", 1), (f"{self.postaffine_ang}_", 0) )
        
        # ALL method lists
        self._allT: tuple = self._sec_prevarsT + self._sec_varsT + self._sec_postvarsT
        self._allMisc: tuple = self._sec_main + self._sec_shader + self._sec_prevarsW + self._sec_varsW + self._sec_postvarsW + self._sec_preAffine + self._sec_postAffine


    # CLASS: PROPERTIES
    ##########################################
    ##########################################
    
    @property
    def sec_main(self):
        return self._sec_main
    
    @property
    def sec_xaos(self):
        return self._sec_xaos
    
    @property
    def sec_shader(self):
        return self._sec_shader
    
    @property
    def sec_prevarsT(self):
        return self._sec_prevarsT
    
    @property
    def sec_prevarsW(self):
        return self._sec_prevarsW
    
    @property
    def sec_varsT(self):
        return self._sec_varsT
    
    @property
    def sec_varsW(self):
        return self._sec_varsW
    
    @property
    def sec_postvarsT(self):
        return self._sec_postvarsT
    
    @property
    def sec_postvarsW(self):
        return self._sec_postvarsW
    
    @property
    def sec_preAffine(self):
        return self._sec_preAffine
    
    @property
    def sec_postAffine(self):
        return self._sec_postAffine
    
    @property
    def allT(self):
        return self._allT
    
    @property
    def allMisc(self):
        return self._allMisc


class flam3h_varsPRM_FF(flam3h_varsPRM):
    """
    Args:
        flam3h_varsPRM ([class]): [inherit properties methods from the flam3h_varsPRM class]
    """    
    
    __slots__ = ("prx",)
    
    def __init__(self, prx: str) -> None:
        """
        Args:
            prx (str): The variation's name prefix. This can be any of:
            * PRX_FF_PRM -> ff
            * PRX_FF_PRM_POST -> fp1

        Returns:
            (None):
        """       
        
        super().__init__()
        
        # The FF posses two sets of parameteric parameters; 
        # One for the VAR variations and one for the PRE and POST variations.
        # This prefix will help us pick either one or the other. 
        self.prx = prx

    def varsPRM_FF(self) -> tuple:

        px: str = self.prx
        vPRM: tuple = self.varsPRM
        varsPRM_FF: tuple = ( vPRM[0], 
                              vPRM[1], 
                              vPRM[2], 
                              vPRM[3], 
                              vPRM[4], 
                              vPRM[5], 
                              vPRM[6], 
                              vPRM[7], 
                              vPRM[8], 
                              vPRM[9], 
                              vPRM[10], 
                              vPRM[11], 
                              vPRM[12], 
                              vPRM[13], 
                              vPRM[14], 
                              vPRM[15], 
                              vPRM[16], 
                              vPRM[17], 
                              vPRM[18], 
                              vPRM[19], 
                              vPRM[20], 
                              vPRM[21], 
                              vPRM[22], 
                              vPRM[23], 
                              vPRM[24], 
                              vPRM[25], 
                              vPRM[26], 
                              (vPRM[27][0], (f"{px}_{vPRM[27][1][0][:-1]}", 1), 1), 
                              (vPRM[28][0], (f"{px}_{vPRM[28][1][0][:-1]}", 1), 1), 
                              (vPRM[29][0], (f"{px}_{vPRM[29][1][0][:-1]}", 1), 1), 
                              (vPRM[30][0], (f"{px}_{vPRM[30][1][0][:-1]}", 1), 1), 
                              (vPRM[31][0], (f"{px}_{vPRM[31][1][0][:-1]}", 1), 1), 
                              (vPRM[32][0], (f"{px}_{vPRM[32][1][0][:-1]}", 1), 1), 
                              (vPRM[33][0], 0), 
                              (vPRM[34][0], (f"{px}_{vPRM[34][1][0][:-1]}", 1), 1), 
                              (vPRM[35][0], (f"{px}_{vPRM[35][1][0][:-1]}", 0), 1), 
                              (vPRM[36][0], (f"{px}_{vPRM[36][1][0][:-1]}", 1), 1), 
                              (vPRM[37][0], (f"{px}_{vPRM[37][1][0][:-1]}", 1), 1), 
                              (vPRM[38][0], (f"{px}_{vPRM[38][1][0][:-1]}", 1), 1), 
                              (vPRM[39][0], 0), 
                              (vPRM[40][0], 0), 
                              (vPRM[41][0], 0), 
                              (vPRM[42][0], 0), 
                              (vPRM[43][0], 0), 
                              (vPRM[44][0], 0), 
                              (vPRM[45][0], 0), 
                              (vPRM[46][0], 0), 
                              (vPRM[47][0], (f"{px}_{vPRM[47][1][0][:-1]}", 1), 1), 
                              (vPRM[48][0], (f"{px}_{vPRM[48][1][0][:-1]}", 1), (f"{px}_{vPRM[48][2][0][:-1]}", 1), 1), 
                              (vPRM[49][0], (f"{px}_{vPRM[49][1][0][:-1]}", 1), 1), 
                              (vPRM[50][0], (f"{px}_{vPRM[50][1][0][:-1]}", 1), 1), 
                              (vPRM[51][0], (f"{px}_{vPRM[51][1][0][:-1]}", 1), 1), 
                              (vPRM[52][0], (f"{px}_{vPRM[52][1][0][:-1]}", 1), 1), 
                              (vPRM[53][0], (f"{px}_{vPRM[53][1][0][:-1]}", 0), 1),
                              (vPRM[54][0], 0),
                              (vPRM[55][0], 0), 
                              (vPRM[56][0], (f"{px}_{vPRM[56][1][0][:-1]}", 0), 1), 
                              (vPRM[57][0], (f"{px}_{vPRM[57][1][0][:-1]}", 1), 1), 
                              (vPRM[58][0], 0), 
                              (vPRM[59][0], 0), 
                              (vPRM[60][0], 0), 
                              (vPRM[61][0], (f"{px}_{vPRM[61][1][0][:-1]}", 0), 1), 
                              (vPRM[62][0], 0), 
                              (vPRM[63][0], (f"{px}_{vPRM[63][1][0][:-1]}", 1), (f"{px}_{vPRM[63][2][0][:-1]}", 1), 1), 
                              (vPRM[64][0], 0), 
                              (vPRM[65][0], 0), 
                              (vPRM[66][0], (f"{px}_{vPRM[66][1][0][:-1]}", 1), 1), 
                              (vPRM[67][0], (f"{px}_{vPRM[67][1][0][:-1]}", 1), 1), 
                              (vPRM[68][0], 0), 
                              (vPRM[69][0], (f"{px}_{vPRM[69][1][0][:-1]}", 1), (f"{px}_{vPRM[69][2][0][:-1]}", 0), 1), 
                              (vPRM[70][0], 0), 
                              (vPRM[71][0], (f"{px}_{vPRM[71][1][0][:-1]}", 1), (f"{px}_{vPRM[71][2][0][:-1]}", 1), 1), 
                              (vPRM[72][0], (f"{px}_{vPRM[72][1][0][:-1]}", 1), 1), 
                              (vPRM[73][0], (f"{px}_{vPRM[73][1][0][:-1]}", 1), 1), 
                              (vPRM[74][0], (f"{px}_{vPRM[74][1][0][:-1]}", 1), 1), 
                              (vPRM[75][0], (f"{px}_{vPRM[75][1][0][:-1]}", 1), 1), 
                              (vPRM[76][0], (f"{px}_{vPRM[76][1][0][:-1]}", 1), 1), 
                              (vPRM[77][0], (f"{px}_{vPRM[77][1][0][:-1]}", 1), 1), 
                              (vPRM[78][0], (f"{px}_{vPRM[78][1][0][:-1]}", 1), 1), 
                              (vPRM[79][0], (f"{px}_{vPRM[79][1][0][:-1]}", 1), (f"{px}_{vPRM[79][2][0][:-1]}", 1), 1), 
                              (vPRM[80][0], 0), 
                              (vPRM[81][0], 0), 
                              (vPRM[82][0], 0), 
                              (vPRM[83][0], 0), 
                              (vPRM[84][0], 0), 
                              (vPRM[85][0], 0), 
                              (vPRM[86][0], 0), 
                              (vPRM[87][0], 0), 
                              (vPRM[88][0], 0), 
                              (vPRM[89][0], 0), 
                              (vPRM[90][0], 0), 
                              (vPRM[91][0], 0), 
                              (vPRM[92][0], 0), 
                              (vPRM[93][0], 0), 
                              (vPRM[94][0], (f"{px}_{vPRM[94][1][0][:-1]}", 1), 1), 
                              (vPRM[95][0], (f"{px}_{vPRM[95][1][0][:-1]}", 0), 1), 
                              (vPRM[96][0], (f"{px}_{vPRM[96][1][0][:-1]}", 1), (f"{px}_{vPRM[96][2][0][:-1]}", 1), 1),
                              (vPRM[97][0], (f"{px}_{vPRM[97][1][0][:-1]}", 1), (f"{px}_{vPRM[97][2][0][:-1]}", 1), 1), 
                              (vPRM[98][0], (f"{px}_{vPRM[98][1][0][:-1]}", 1), 1), 
                              (vPRM[99][0], (f"{px}_{vPRM[99][1][0][:-1]}", 1), (f"{px}_{vPRM[99][2][0][:-1]}", 1), 1), 
                              (vPRM[100][0], 0), 
                              (vPRM[101][0], (f"{px}_{vPRM[101][1][0][:-1]}", 1), (f"{px}_{vPRM[101][2][0][:-1]}", 1), (f"{px}_{vPRM[101][3][0][:-1]}", 1), 1),
                              (vPRM[102][0], (f"{px}_{vPRM[102][1][0][:-1]}", 1), (f"{px}_{vPRM[102][2][0][:-1]}", 1), 1), 
                              (vPRM[103][0], 0),
                              (vPRM[104][0], 0), 
                              (vPRM[105][0], (f"{px}_{vPRM[105][1][0][:-1]}", 1), 1)
                              )
        
        return varsPRM_FF


class flam3h_iterator_FF(flam3h_iterator_prm_names):
    """
    Args:
        flam3h_iterator_prm_names ([class]): [inherit properties methods from the flam3h_iterator_prm_names class]
    """    
    
    """
        Note that every parameters inside the FF have the same name as the iterator parameters 
        plus the string "ff" added at the beginning of their names. parametric variation's parameters have the string  "ff_" instead.
        If you create new parameters inside the FF, or change the parameters names inside the FLAM3H iterator,
        please be sure to follow the same nameing convetion so to keep the flam3h_varsPRM: class as the only source for their names.
    """
    
    __slots__ = ("_sec_prevarsT_FF", "_sec_prevarsW_FF", "_sec_varsT_FF", "_sec_varsW_FF", "_sec_postvarsT_FF", "_sec_postvarsW_FF", "_sec_preAffine_FF", "_sec_postAffine_FF", 
                 "_allMisc_FF")
    
    def __init__(self) -> None:
        """
        Args:
            (self):
            
        Returns:
            (None):
        """  
        super().__init__()
        
        # SECTIONS method lists
        #
        # (*T)Types have no signature and always to be used with: pastePRM_T_from_list()
        self._sec_prevarsT_FF: tuple = ( f"{PRX_FF_PRM}{self.prevar_type_1}",)
        self._sec_prevarsW_FF: tuple = ( (f"{PRX_FF_PRM}{self.prevar_weight_1}", 0),)
        self._sec_varsT_FF: tuple = ( f"{PRX_FF_PRM}{self.var_type_1}", f"{PRX_FF_PRM}{self.var_type_2}" )
        self._sec_varsW_FF: tuple = ( (f"{PRX_FF_PRM}{self.var_weight_1}", 0), (f"{PRX_FF_PRM}{self.var_weight_2}", 0) )
        self._sec_postvarsT_FF: tuple = ( f"{PRX_FF_PRM}{self.postvar_type_1}", f"{PRX_FF_PRM}{self.postvar_type_2}" )
        self._sec_postvarsW_FF: tuple = ( (f"{PRX_FF_PRM}{self.postvar_weight_1}", 0), (f"{PRX_FF_PRM}{self.postvar_weight_2}", 0) )
        self._sec_preAffine_FF: tuple = ( (f"{PRX_FF_PRM}{self.preaffine_x}", 1), (f"{PRX_FF_PRM}{self.preaffine_y}", 1), (f"{PRX_FF_PRM}{self.preaffine_o}", 1), (f"{PRX_FF_PRM}{self.preaffine_ang}", 0) )
        self._sec_postAffine_FF: tuple = ( (f"{PRX_FF_PRM}{self.postaffine_do}", 0), (f"{PRX_FF_PRM}{self.postaffine_x}", 1), (f"{PRX_FF_PRM}{self.postaffine_y}", 1), (f"{PRX_FF_PRM}{self.postaffine_o}", 1), (f"{PRX_FF_PRM}{self.postaffine_ang}", 0) )
        
        # ALL method lists
        # allT_FF list is omitted here because FF PRE VARS, FF VARS and FF POST VARS have their own unique parametric parameters
        # so I need to handle them one by one inside: def prm_paste_FF(kwargs).prm_paste_FF() and prm_paste_FF(kwargs).def prm_paste_sel_FF()
        self._allMisc_FF: tuple = self._sec_varsW_FF + self._sec_prevarsW_FF + self._sec_postvarsW_FF + self._sec_preAffine_FF + self._sec_postAffine_FF


    # CLASS: PROPERTIES
    ##########################################
    ##########################################
    
    @property
    def sec_prevarsT_FF(self):
        return self._sec_prevarsT_FF
    
    @property
    def sec_prevarsW_FF(self):
        return self._sec_prevarsW_FF
    
    @property
    def sec_varsT_FF(self):
        return self._sec_varsT_FF
    
    @property
    def sec_varsW_FF(self):
        return self._sec_varsW_FF
    
    @property
    def sec_postvarsT_FF(self):
        return self._sec_postvarsT_FF
    
    @property
    def sec_postvarsW_FF(self):
        return self._sec_postvarsW_FF
    
    @property
    def sec_preAffine_FF(self):
        return self._sec_preAffine_FF
    
    @property
    def sec_postAffine_FF(self):
        return self._sec_postAffine_FF
    
    @property
    def allMisc_FF(self):
        return self._allMisc_FF


# FLAM3H SCRIPTS start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class flam3h_scripts:
    """
class flam3h_scripts

@STATICMETHODS
* flam3h_on_create_lock_parms(node: hou.SopNode) -> None:
* set_first_instance_global_var(cvex_precision: int) -> None:
* flam3h_check_first_node_instance_msg_status_bar_display_flag(node: hou.SopNode, cvex_precision: int, _MSG_INFO: str, _MSG_DONE: str, sys_updated_mode: hou.EnumValue) -> None:
* flam3h_check_first_node_instance_msg_status_bar_no_display_flag(node: hou.SopNode, cvex_precision: int, _MSG_INFO: str, _MSG_DONE: str, sys_updated_mode: hou.EnumValue) -> None:
* flam3h_set_first_instance_global_var(cvex_precision: int, first_instance_32bit: bool, first_instance_64bit: bool) -> None:
* is_post_affine_default_on_load(node: hou.SopNode) -> None:

@METHODS
* flam3h_check_first_node_instance_msg(self, FIRST_TIME_MSG: bool = True) -> None:
* flam3h_check_first_node_instance_prefs_cvex_precision_msg(self) -> None:
* flam3h_on_create_set_houdini_session_data(self) -> None:
* flam3h_on_create_set_prefs_viewport(self, default_value_pt: float = 1, default_value_ww: float = 3) -> None:
* flam3h_on_create_init_viewportWireWidth(self) -> None:
* flam3h_presets_cache_filepath_on_load(self) -> None:
* flam3h_on_create(self) -> None:
* flam3h_on_loaded(self) -> None:
* flam3h_on_deleted(self) -> None:

    """    
    
    __slots__ = ("_kwargs", "_node")
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """  
        self._kwargs: dict = kwargs
        self._node = kwargs['node']


    @staticmethod
    def flam3h_on_create_lock_parms(node: hou.SopNode) -> None:
        """lock private parameters not being locked on creation by other definitions.
        
        Args:
            node(hou.SopNode): This FLAM3H node
            
        Returns:
            (None):
        """
        prm_names: tuple = (CP_PVT_ISVALID_FILE, 
                            CP_PVT_ISVALID_PRESET, 
                            IN_PVT_ISVALID_FILE, 
                            IN_PVT_ISVALID_PRESET, 
                            IN_PVT_CLIPBOARD_TOGGLE, 
                            OUT_PVT_ISVALID_FILE, 
                            PREFS_PVT_F3C, 
                            PREFS_PVT_XAOS_AUTO_SPACE,
                            PREFS_PVT_INT_0,
                            PREFS_PVT_INT_1,
                            PREFS_PVT_FLOAT_0,
                            PREFS_PVT_FLOAT_1
                            )
        
        [node.parm(prm_name).lock(True) for prm_name in prm_names]
        
        
        # The following are FLAM3H UI utility parameters
        # hence they do not have a global variable and only hard coded here.
        disabler_prm_names: tuple = ("cpdisable",
                                     "hide_palette",
                                     "indisable",
                                     "outdisable",
                                     "prefsdisable",
                                     "aboutdisable"
                                     )
        
        [node.parm(prm_name).lock(True) for prm_name in disabler_prm_names]


    @staticmethod
    def set_first_instance_global_var(cvex_precision: int) -> None:
        """Set the hou.session variable to hold the cvex precision being used on first instance node creation time.

        Args:
            cvex_precision(int): 32bit or 64bit - This is the cvex precision preference's option parameter
            
        Returns:
            (None):
        """  
        if cvex_precision == 32:
            hou.session.FLAM3H_FIRST_INSTANCE_32BIT: bool = False # type: ignore
        elif cvex_precision == 64:
            hou.session.FLAM3H_FIRST_INSTANCE_64BIT: bool = False # type: ignore


    @staticmethod
    def flam3h_check_first_node_instance_msg_status_bar_display_flag(node: hou.SopNode, cvex_precision: int, _MSG_INFO: str, _MSG_DONE: str, sys_updated_mode: hou.EnumValue) -> None:
        """This is temporary until I dnt have time to find a better solution
        to advice the user about the first node compile time without having any leftover
        messages in the Houdini status bar.
        
        This definition will cook and updated the FLAM3H node on creation based on its CVEX precision preference's setting
        if its display flag is True.

        Args:
            node(hou.SopNode): This FLAM3H node
            cvex_precision(int): 32bit or 64bit - This is the cvex precision preference's option parameter
            _MSG_INFO(str): The message to print in the status bar
            _MSG_DONE(str): The message to print in the hou window 
            sys_updated_mode(hou.EnumValue): houdini updated mode before dropping a FLAM3H node for the first time ( stored from the preFirstCreate script )
            
        Returns:
            (None):
        """
        flam3h_general_utils.set_status_msg(_MSG_INFO, 'WARN')
        if hou.isUIAvailable():
            
            # If there are not any Sop viewer lets cook it since this is the first node instance of FLAM3H
            if flam3h_general_utils.util_is_context_available_viewer('Sop') is False: node.cook(force=True)
            
            if hou.ui.displayMessage(_MSG_DONE, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title = "FLAM3H: CVEX 32bit compile", details=None, details_label=None, details_expanded=False) == 0: # type: ignore
                flam3h_scripts.set_first_instance_global_var(cvex_precision)
                hou.setUpdateMode(sys_updated_mode) # type: ignore
                # Print to the Houdini console
                print(f"\nFLAM3H CVEX nodes compile: DONE\n")
                
            flam3h_general_utils.set_status_msg(_MSG_DONE, 'IMP')
        else:
            flam3h_scripts.set_first_instance_global_var(cvex_precision)
            hou.setUpdateMode(sys_updated_mode) # type: ignore


    @staticmethod
    def flam3h_check_first_node_instance_msg_status_bar_no_display_flag(node: hou.SopNode, cvex_precision: int, _MSG_INFO: str, _MSG_DONE: str, sys_updated_mode: hou.EnumValue) -> None:
        """This is temporary until I dnt have time to find a better solution
        to advice the user about the first node compile time without having any leftover
        messages in the Houdini status bar.
        
        This definition will cook and updated the FLAM3H node on creation based on its CVEX precision preference's setting
        if its display flag is False.

        Args:
            node(hou.SopNode): This FLAM3H node
            cvex_precision(int): 32bit or 64bit - This is the cvex precision preference's option parameter
            _MSG_INFO(str): The message to print in the status bar
            _MSG_DONE(str): The message to print in the hou window 
            sys_updated_mode(hou.EnumValue): houdini updated mode before dropping a FLAM3H node for the first time ( stored from the preFirstCreate script )
            
        Returns:
            (None):
        """
        # m = nodesearch.State("Display", True)
        # _display_node = m.nodes(node.parent(), recursive=False)[0]
        flam3h_general_utils.set_status_msg(_MSG_INFO, 'WARN')
        node.cook(force=True)
        flam3h_scripts.set_first_instance_global_var(cvex_precision)

        hou.setUpdateMode(sys_updated_mode) # type: ignore
        flam3h_general_utils.set_status_msg(_MSG_DONE, 'IMP')
        print(f"\nFLAM3H CVEX node compile: DONE\n")
        
        
    @staticmethod
    def flam3h_set_first_instance_global_var(cvex_precision: int, first_instance_32bit: bool, first_instance_64bit: bool) -> None:
        """Set the hou.session variable to hold the cvex precision being used during the Houdini session.

        Args:
            cvex_precision(int): 32bit or 64bit - This is the cvex precision preference's option parameter
            first_instance_32bit(bool): 32bit or 64bit - Was this FLAM3H node instance created with this cvex precision ?
            first_instance_64bit(bool): 32bit or 64bit - Was this FLAM3H node instance created with this cvex precision ?
            
        Returns:
            (None):
        """  
        if cvex_precision == 32 and first_instance_32bit is True:
            hou.session.FLAM3H_FIRST_INSTANCE_32BIT: bool = False # type: ignore
        elif cvex_precision == 64 and first_instance_64bit is True:
            hou.session.FLAM3H_FIRST_INSTANCE_64BIT: bool = False # type: ignore


    @staticmethod
    def is_post_affine_default_on_load(node: hou.SopNode) -> None:
        """Turn iterators/FF post affine OFF if they are active and default values.

        Args:
            node(hou.SopNode): This FLAm3H node.
            
        Returns:
            (None):
        """  

        # Iterators
        iter_num: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        prm_list_post_affine: tuple = flam3h_iterator().sec_postAffine
        keyframes: list = [[item for sublist in k for item in sublist] for k in [[[1 if len(p.keyframes()) else 0 for p in node.parmTuple(f"{prm_list_post_affine[1:][idx][0]}{id + 1}")] if prm_list_post_affine[1:][idx][1] else [1 if len(node.parm(f"{prm_list_post_affine[1:][idx][0]}{id + 1}").keyframes()) else 0] for idx in range(len(prm_list_post_affine[1:]))] for id in range(iter_num)]]
        collect: list = [[node.parmTuple(f"{prm_list_post_affine[1:][idx][0]}{id + 1}").eval() if prm_list_post_affine[1:][idx][1] else node.parm(f"{prm_list_post_affine[1:][idx][0]}{id + 1}").eval() for idx in range(len(prm_list_post_affine[1:]))] for id in range(iter_num)]
        [node.setParms({f"{prm_list_post_affine[0][0]}{id + 1}": 0}) if node.parm(f"{prm_list_post_affine[0][0]}{id + 1}").eval() and 1 not in keyframes[id] and affine == [(1.0, 0.0), (0.0, 1.0), (0.0, 0.0), 0.0] else ... for id, affine in enumerate(collect)] # type: ignore
        
        # FF
        prm_list_post_affine_FF: tuple = flam3h_iterator_FF().sec_postAffine_FF
        keyframes: list = [item for sublist in [[1 if len(p.keyframes()) else 0 for p in node.parmTuple(f"{prm_list_post_affine_FF[1:][idx][0]}")] if prm_list_post_affine_FF[1:][idx][1] else [1 if len(node.parm(f"{prm_list_post_affine_FF[1:][idx][0]}").keyframes()) else 0] for idx in range(len(prm_list_post_affine_FF[1:]))] for item in sublist]
        collect: list = [node.parmTuple(f"{prm_list_post_affine_FF[1:][idx][0]}").eval() if prm_list_post_affine_FF[1:][idx][1] else node.parm(f"{prm_list_post_affine_FF[1:][idx][0]}").eval() for idx in range(len(prm_list_post_affine_FF[1:]))]
        if node.parm(f"{prm_list_post_affine_FF[0][0]}").eval() and 1 not in keyframes and collect == [(1.0, 0.0), (0.0, 1.0), (0.0, 0.0), 0.0]:
            node.setParms({f"{prm_list_post_affine_FF[0][0]}": 0}) # type: ignore


    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node


    def flam3h_check_first_node_instance_msg(self, FIRST_TIME_MSG: bool = True) -> None:
        """This is temporary until I dnt have time to find a better solution
        to advice the user about the first node compile time without having any leftover
        messages in the Houdini status bar.
        
        This definition will cook and updated the FLAM3H node on creation based on its CVEX precision preference's setting
        and based on its display flag status ( Tru or False ).
        
        It will also restore the houdini session update mode if not set already on AutoUpdate.

        Args:
            (self):
            FIRST_TIME_MSG(int): False for onLoaded and True for onCreated
            
        Returns:
            (None):
        """
        
        try:
            hou.session.FLAM3H_FIRST_INSTANCE_32BIT # type: ignore
        except:
            first_instance_32bit: bool = True
        else:
            first_instance_32bit: bool = False
            
        try:
            hou.session.FLAM3H_FIRST_INSTANCE_64BIT # type: ignore
        except:
            first_instance_64bit: bool = True
        else:
            first_instance_64bit: bool = False
            
        node = self.node
        cvex_precision: int = int( node.parm(PREFS_CVEX_PRECISION).eval() )
                
        if FIRST_TIME_MSG is True and ( first_instance_32bit is True or first_instance_64bit is True ): # type: ignore
            
            h: int = flam3h_general_utils.houdini_version(2)
            if h < 205: __module__: str = "3.7"
            else: __module__: str = "3.11"
            
            if cvex_precision == 32 and first_instance_32bit is True:
                
                hou.setUpdateMode(hou.updateMode.AutoUpdate) # type: ignore
                sys_updated_mode: hou.EnumValue = hou.session.FLAM3H_SYS_UPDATE_MODE # type: ignore
                
                _MSG_INFO = f"FLAM3H v{__version__}  first instance -> Compiling FLAM3H CVEX nodes. Depending on your PC configuration it can take up to 1(one) minute. It is a one time compile process."
                _MSG_DONE = f"FLAM3H CVEX nodes compile: DONE \nversion: {__version__} - {__status__}\nF3H Python module: {__module__}"
            
                if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
                    self.flam3h_check_first_node_instance_msg_status_bar_display_flag(node, cvex_precision, _MSG_INFO, _MSG_DONE, sys_updated_mode) # type: ignore
                else:
                    self.flam3h_check_first_node_instance_msg_status_bar_no_display_flag(node, cvex_precision,_MSG_INFO, _MSG_DONE, sys_updated_mode) # type: ignore
                    
                    
            elif cvex_precision == 64 and first_instance_64bit is True:

                hou.setUpdateMode(hou.updateMode.AutoUpdate) # type: ignore
                sys_updated_mode: hou.EnumValue = hou.session.FLAM3H_SYS_UPDATE_MODE # type: ignore
                
                _MSG_INFO = f"FLAM3H v{__version__} 64-bit  first instance -> Compiling FLAM3H CVEX 64-bit nodes. Depending on your PC configuration it can take up to 1(one) minute. It is a one time compile process."
                _MSG_DONE = f"FLAM3H CVEX 64-bit nodes compile: DONE\nversion: {__version__} - {__status__}\nF3H Python module: {__module__}"
                
                if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
                    self.flam3h_check_first_node_instance_msg_status_bar_display_flag(node, cvex_precision, _MSG_INFO, _MSG_DONE, sys_updated_mode) # type: ignore
                else:
                    self.flam3h_check_first_node_instance_msg_status_bar_no_display_flag(node, cvex_precision,_MSG_INFO, _MSG_DONE, sys_updated_mode) # type: ignore
                    
            else:
                pass
                
        else:
            self.flam3h_set_first_instance_global_var(cvex_precision, first_instance_32bit, first_instance_64bit)


    def flam3h_check_first_node_instance_prefs_cvex_precision_msg(self) -> None:
        """When changing CVEX precison modes in the preference's tab,
        this definition will let the user node of the compilie time if a mode is selected for the first time in the current houdini's session.

        Args:
            (self):
            
        Returns:
            (None):
        """
        
        try:
            hou.session.FLAM3H_FIRST_INSTANCE_32BIT # type: ignore
        except:
            first_instance_32bit: bool = True
        else:
            first_instance_32bit: bool = False
            
        try:
            hou.session.FLAM3H_FIRST_INSTANCE_64BIT # type: ignore
        except:
            first_instance_64bit: bool = True
        else:
            first_instance_64bit: bool = False
                
        if first_instance_32bit is True or first_instance_64bit is True: # type: ignore
            
            h: int = flam3h_general_utils.houdini_version(2)
            if h < 205: __module__: str = "3.7"
            else: __module__: str = "3.11"

            node = self.node
            cvex_precision: int = int( node.parm(PREFS_CVEX_PRECISION).eval() )
            
            sys_updated_mode = hou.updateModeSetting() # type: ignore
            hou.setUpdateMode(hou.updateMode.AutoUpdate) # type: ignore
            
            if cvex_precision == 32:
                _MSG_INFO = f" FLAM3H v{__version__}  first instance -> Compiling FLAM3H CVEX node. Depending on your PC configuration it can take up to 1(one) minute. It is a one time compile process."
                _MSG_DONE = f"FLAM3H CVEX node compile: DONE \nversion: {__version__} - {__status__}\nF3H Python module: {__module__}"
            else:
                _MSG_INFO = f" FLAM3H v{__version__} 64-bit  first instance -> Compiling FLAM3H CVEX 64-bit node. Depending on your PC configuration it can take up to 1(one) minute. It is a one time compile process."
                _MSG_DONE = f"FLAM3H CVEX 64-bit node compile: DONE\nversion: {__version__} - {__status__}\nF3H Python module: {__module__}"
            
            density: int = node.parm(GLB_DENSITY).eval()
            if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
                flam3h_general_utils.set_status_msg(_MSG_INFO, 'WARN')
                node.setParms({GLB_DENSITY: 1})
                node.cook(force=True)
                if hou.isUIAvailable():
                    if hou.ui.displayMessage(_MSG_DONE, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title = "FLAM3H: CVEX 64bit compile", details=None, details_label=None, details_expanded=False) == 0: # type: ignore
                        # node.cook(force=True)
                        self.flam3h_set_first_instance_global_var(cvex_precision, first_instance_32bit, first_instance_64bit)

                        node.setParms({GLB_DENSITY: density})
                        hou.setUpdateMode(sys_updated_mode) # type: ignore
                        flam3h_general_utils.set_status_msg(_MSG_DONE, 'IMP')
                else:
                    self.flam3h_set_first_instance_global_var(cvex_precision, first_instance_32bit, first_instance_64bit)

                    node.setParms({GLB_DENSITY: density})
                    hou.setUpdateMode(sys_updated_mode) # type: ignore
            else:
                # m = nodesearch.State("Display", True)
                # _display_node = m.nodes(node.parent(), recursive=False)[0]
                flam3h_general_utils.set_status_msg(_MSG_INFO, 'WARN')
                node.setParms({GLB_DENSITY: 1})
                node.cook(force=True)
                self.flam3h_set_first_instance_global_var(cvex_precision, first_instance_32bit, first_instance_64bit)

                node.setParms({GLB_DENSITY: density})
                hou.setUpdateMode(sys_updated_mode) # type: ignore
                flam3h_general_utils.set_status_msg(_MSG_DONE, 'IMP')


    def flam3h_on_create_set_houdini_session_data(self) -> None:
        """Initialize the necessary data for the copy/paste iterator and FF methods on creation.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        node = self.node
        node_instances: tuple = self.node.type().instances()
        
        # FLAM3H node and MultiParameter id for iterators
        # This is to make sure the hou.session's data is at least initialized.
        flam3h_iterator_utils.flam3h_init_hou_session_iterator_data(node)

        # If an iterator was copied from a node that has been deleted
        try: hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
        except:
            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = None # type: ignore
            # If we deleted all FLAM3H nodes and we then create a new one,
            # Lets initialize back to himself.
            if len(node_instances) == 1:
                hou.session.FLAM3H_MARKED_ITERATOR_NODE: TA_MNode = node # type: ignore

        # FLAM3H node for FF.
        # This is to make sure the hou.session's data is at least initialized.
        flam3h_iterator_utils.flam3h_init_hou_session_ff_data(node)

        # If the FF was copied from a node that has been deleted
        try: hou.session.FLAM3H_MARKED_FF_NODE.type() # type: ignore
        except:
            hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = None # type: ignore
            # If we deleted all FLAM3H nodes and we then create a new one,
            # Lets initialize back to himself.
            if len(node_instances) == 1:
                hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = node # type: ignore


    def flam3h_on_create_set_prefs_viewport(self, default_value_pt: float = 1, default_value_ww: float = 3) -> None:
        """Initialize the necessary data for the viewport display preference's option on creation.
        This need some work as it is a little rough, I'll be back to this at some point. Good enough for now.
        
        Args:
            (self):
            default_value_pt(float): A default value to compare to for the point setting. This must always be the same as the FLAM3H UI parameter's default values.
            default_value_ww(float): A default value to compare to for the wire width setting. This must always be the same as the FLAM3H UI parameter's default values.
            
        Returns:
            (None):
        """
        
        node = self.node
        
        # viewers
        viewers: list = flam3h_general_utils.util_getSceneViewers()
        
        # Update dark history
        flam3h_general_utils.util_store_all_viewers_color_scheme_onCreate() # init Dark viewers data, needed for the next definition to run
        flam3h_general_utils(self.kwargs).colorSchemeDark(False) # type: ignore
        # Set other FLAM3H instances to dark if any
        all_f3h: tuple = node.type().instances()
        all_f3h_vpptsize: list = []
        all_f3h_vptype: list = []
        all_f3h_ww: list = []
        
        if len(all_f3h) > 1:

            for f3h in all_f3h:
                if f3h != node:
                    all_f3h_vpptsize.append(f3h.parm(PREFS_VIEWPORT_PT_SIZE).eval())
                    all_f3h_vptype.append(f3h.parm(PREFS_VIEWPORT_PT_TYPE).eval())
                    all_f3h_ww.append(f3h.parm(PREFS_VIEWPORT_WIRE_WIDTH).eval())
                    if f3h.parm(PREFS_VIEWPORT_DARK).eval():
                        node.setParms({PREFS_VIEWPORT_DARK: 1})
                        flam3h_general_utils(self.kwargs).colorSchemeDark(False)
                        
                    # FLAM3H nodes viewport preferences options are already synced
                    # so we really need only one to know them all
                    break
        else:
            node.setParms({PREFS_VIEWPORT_DARK: 1})
            flam3h_general_utils(self.kwargs).colorSchemeDark(False) # type: ignore
        
        # If we collected some data, set
        if all_f3h_vpptsize:
            node.setParms({PREFS_VIEWPORT_PT_SIZE: all_f3h_vpptsize[0]})
            node.setParms({PREFS_VIEWPORT_PT_TYPE: all_f3h_vptype[0]})
            
        else:
            Pixels = hou.viewportParticleDisplay.Pixels # type: ignore
            
            for v in viewers:
                
                # Lets make sure we check for a viewer in the Sop context
                if flam3h_general_utils.util_is_context('Sop', v):
                    
                    settings: hou.GeometryViewportSettings = v.curViewport().settings()
                    size: float = settings.particlePointSize()
                    
                    if size != default_value_pt:
                        node.setParms({PREFS_VIEWPORT_PT_SIZE: size})
                        
                    type: hou.EnumValue = settings.particleDisplayType()
                    if type == Pixels:
                        node.setParms({PREFS_VIEWPORT_PT_TYPE: 1})
                        
                else:
                    # FLAM3H shoud use its parameter default value in this case, but just to be sure
                    node.setParms({PREFS_VIEWPORT_PT_SIZE: default_value_pt})
                    
        # If we collected some data, set
        if all_f3h_ww:
            node.setParms({PREFS_VIEWPORT_WIRE_WIDTH: all_f3h_ww[0]})
            
        else:
            
            for v in viewers:
                
                # Lets make sure we check for a viewer in the Sop context
                if flam3h_general_utils.util_is_context('Sop', v):
                    
                    settings: hou.GeometryViewportSettings = v.curViewport().settings()
                    size: float = settings.wireWidth()
                    
                    if size != default_value_ww:
                        node.setParms({PREFS_VIEWPORT_WIRE_WIDTH: size})
    
    
    def flam3h_on_create_init_viewportWireWidth(self) -> None:
        """Initialize FLAM3H viewport wire width.
        We set it ot 3 for now as it looks nice.
        This will affect the viewport wireframe width as it is a global setting.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        if flam3h_general_utils(self.kwargs).util_other_xf_viz() is False:
            hou.session.FLAM3H_VIEWPORT_WIRE_WIDTH: float = 3 # type: ignore
        else:
            try: hou.session.FLAM3H_VIEWPORT_WIRE_WIDTH # type: ignore
            except: hou.session.FLAM3H_VIEWPORT_WIRE_WIDTH: float = 3 # type: ignore
    
    
    def flam3h_presets_cache_filepath_on_load(self) -> None:
        """Initialize presets cached data to be up to date.
        
        Here I could use userData instead of a cachedUserData but can happen that between one houdini session
        and the next one the user may make some modification to the stored file, like moving it into another location or deleting it
        so this way we make sure to always be up to date.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        
        cp_is_valid: int = node.parm(CP_PVT_ISVALID_FILE).eval()
        in_is_valid: int = node.parm(IN_PVT_ISVALID_FILE).eval()
        out_is_valid: int = node.parm(OUT_PVT_ISVALID_FILE).eval()
        
        if cp_is_valid:
            cp_path: str = os.path.expandvars(node.parm(CP_PALETTE_LIB_PATH).eval())
            cp_path_checked: str | bool = out_flame_utils.out_check_outpath(node,  cp_path, OUT_PALETTE_FILE_EXT, AUTO_NAME_CP)
            if cp_path_checked is not False and os.path.isfile(cp_path_checked): node.setCachedUserData('cp_presets_filepath', cp_path_checked)
                
        if in_is_valid:
            xml: str = os.path.expandvars(node.parm(IN_PATH).eval())
            xml_checked: str | bool = out_flame_utils.out_check_outpath(node,  xml, OUT_FLAM3_FILE_EXT, AUTO_NAME_OUT, False, False)
            if xml_checked is not False and os.path.isfile(xml_checked): node.setCachedUserData('in_presets_filepath', xml_checked)
            
        if out_is_valid:
            xml: str = os.path.expandvars(node.parm(OUT_PATH).eval())
            xml_checked: str | bool = out_flame_utils.out_check_outpath(node,  xml, OUT_FLAM3_FILE_EXT, AUTO_NAME_OUT)
            if xml_checked is not False and os.path.isfile(xml_checked): node.setCachedUserData('out_presets_filepath', xml_checked)


    def flam3h_on_create(self) -> None:
        """Initialize FLAM3H node on creation and all the data it need to run.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        node.setColor(hou.Color((0.9,0.9,0.9)))
        
        flam3h_iterator_utils(self.kwargs).flam3h_default()
        self.flam3h_check_first_node_instance_msg()
        
        # Set about tab infos
        flam3h_about_utils(self.kwargs).flam3h_about_msg()
        flam3h_about_utils(self.kwargs).flam3h_about_plugins_msg()
        flam3h_about_utils(self.kwargs).flam3h_about_web_msg()
        
        self.flam3h_on_create_set_houdini_session_data()
        self.flam3h_on_create_set_prefs_viewport()
        self.flam3h_on_create_init_viewportWireWidth()
        
        # Remove any comment and user data from the node
        flam3h_iterator_utils.del_comment_and_user_data_iterator(node)
        flam3h_iterator_utils.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)
        # This is already destroyed inside: flam3h_iterator_utils(self.kwargs).flam3h_default()
        # But I keep it for now in case a make some changes later on
        flam3h_iterator_utils.destroy_userData(node, FLAM3H_USER_DATA_XML_LAST)
        
        # OUT render curves reset and set
        out_flame_utils.out_render_curves_set_and_retrieve_defaults(node)
        
        # Clear menu caches
        # This is needed to help to updates the menus from time to time so to pick up sneaky changes to the loaded files
        # (ex. the user perform hand made modifications like renaming a Preset and such).
        flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node, True)
        
        # lock private parameters not being locked on creation by other definitions.
        self.flam3h_on_create_lock_parms(node)


    # def flam3h_on_loaded_set_density_menu(self) -> None:
    #     """This is for backward compatibility when the point count parameter was still exposed.
    #     It will set the density presets menu to the closest point count value
        
    #     The density values dictionary entries match whats inside: def menu_global_density_set(self) -> None:
    #     and also the entries inside the global menu: MENU_DENSITY
        
    #     Any changes to the entries on one of those need to be made also on the others.
        
    #     Returns:
    #         (None):
    #     """
    #     node = self.node
    #     density = node.parm(GLB_DENSITY).eval()
    #     density_values: dict = { 500000: 1, 1000000: 2, 2000000: 3, 5000000: 4, 15000000: 5, 25000000: 6, 50000000: 7, 100000000: 8, 150000000: 9, 250000000: 10, 500000000: 11, 750000000: 12, 1000000000: 13 }
    #     density_new = min(density_values.keys(), key=lambda x:abs(x-density))
    #     node.setParms({GLB_DENSITY_PRESETS: density_values.get(density_new)})
    #     node.setParms({GLB_DENSITY: density_new})


    def flam3h_on_loaded(self) -> None:
        """Initialize FLAM3H node on hip file load and all the data it need to run.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        node = self.node
        
        # Force updated of the mini-menu iterator selection
        flam3h_iterator_utils.destroy_cachedUserData(node, 'iter_sel')
        flam3h_iterator_utils.destroy_cachedUserData(node, 'edge_case_01')
        # CP and IN PRESETS filepaths (cache data)
        self.flam3h_presets_cache_filepath_on_load()
        # Turn iterators/FF post affine OFF if they are default values
        self.is_post_affine_default_on_load(node)
        
        # init xaos
        flam3h_iterator_utils(self.kwargs).auto_set_xaos()
        
        if hou.hipFile.isLoadingHipFile(): #type: ignore
            
            # set density menu
            flam3h_iterator_utils.flam3h_on_loaded_set_density_menu(node)
            
            # This is important so loading a hip file with a FLAM3H node inside
            # it wont block the houdini session until user input.
            self.flam3h_check_first_node_instance_msg(False)
            
            # Update FLAM3H viewport preferences
            self.flam3h_on_create_set_prefs_viewport()
            
            # init CP PRESETS: mode (int): ZERO: To be used to prevent to load a preset when loading back a hip file.
            flam3h_general_utils(self.kwargs).flam3h_init_presets_CP_PRESETS(0)
            # init IN PRESETS: mode (int): ZERO: To be used to prevent to load a preset when loading back a hip file.
            flam3h_general_utils(self.kwargs).flam3h_init_presets_IN_PRESETS(0)
            # init OUT PRESETS
            flam3h_general_utils(self.kwargs).flam3h_init_presets_OUT_PRESETS()
            # init RIP: Remove Invalid Points
            flam3h_iterator_utils.flam3h_on_load_opacity_zero(node)
            
            # Set color correction curves to their defaults if there is need to do it (ex: hip files with older version of FLAM3H)
            out_flame_utils.out_render_curves_set_defaults_on_load(node)
            
            # update about tab just in case
            flam3h_about_utils(self.kwargs).flam3h_about_msg()
            flam3h_about_utils(self.kwargs).flam3h_about_plugins_msg()
            flam3h_about_utils(self.kwargs).flam3h_about_web_msg()
            
            # CAMERA SENSOR
            #
            # If a FLAM3H node is in camera sensor mode and its display flag ON, update the viewport to actually be in camera sensor mode.
            # This work with multiple FLAM3H node becasue there can only be one FLAM3H node in camera sensor mode at any given time.
            if node.isGenericFlagSet(hou.nodeFlag.Display) and node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval(): # type: ignore
                flam3h_general_utils(self.kwargs).util_set_clipping_viewers()
                flam3h_general_utils(self.kwargs).util_set_front_viewer()
            else:
                # Otherwise just turn the camera sensor mode OFF.
                if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                    node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                    # Clear stashed cams data
                    flam3h_general_utils.util_clear_stashed_cam_data()
            
            # The following is a workaround to keep the correct preset inside the IN Tab when the hip file was saved
            # as it always get reset to ZERO on load for some reason. The preset inside the SYS Tab is correct after load.
            # Need to investigate why. the IN_SYS_PRESETS menu parameter is set inside:
            # 
            #   - in_flame_utils(self.kwargs).in_to_flam3h()
            #   - in_flame_utils(self.kwargs).in_to_flam3h_sys()
            #
            node.setParms({IN_PRESETS: node.parm(IN_SYS_PRESETS).eval()})
            node.setParms({IN_PRESETS_OFF: node.parm(IN_SYS_PRESETS_OFF).eval()})
            
            
            # Same goes for the palette preset entrie, and some time goes also out of range
            # so we store the selection first inside a mem menu parameter on Load inside:
            #
            #   - flam3h_palette_utils(self.kwargs).json_to_flam3h_ramp_SET_PRESET_DATA()
            #   - flam3h_palette_utils(self.kwargs).json_to_flam3h_ramp_sys()
            #
            # and on Save inside:
            #
            #   - flam3h_palette_utils(self.kwargs).flam3h_ramp_save()
            #
            node.setParms({CP_PALETTE_PRESETS: node.parm(CP_SYS_PALETTE_PRESETS).eval()})
            node.setParms({CP_PALETTE_PRESETS_OFF: node.parm(CP_SYS_PALETTE_PRESETS_OFF).eval()})
            
            # init/clear copy/paste iterator's data and prm
            # This was causing some issues and got updated.
            flam3h_iterator_utils(self.kwargs).flam3h_paste_reset_hou_session_data(True)
            # If in the loaded hip file there are data stored into the nodes, lets set the copy/paste data from them.
            # This will allow to re-load an hip file with marked iterator or FF and pick up from there, which is nice.
            flam3h_iterator_utils.flam3h_init_hou_session_restore_from_user_data(node)
            
        else:
            # CAMERA SENSOR
            # If camera sensor is ON
            if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                # lets turn it OFF.
                node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                # Restore anc clear stashed cams data
                flam3h_general_utils.util_set_stashed_cam()
                flam3h_general_utils(self.kwargs).flam3h_other_sensor_viz_off(node)
                
            # Reset memory mpidx prm data
            flam3h_iterator_utils.iterator_mpidx_mem_set(node, 0)
            # init RIP: Remove Invalid Points: ALL
            flam3h_iterator_utils.flam3h_on_load_opacity_zero(node, True)
            
            # Clear menu caches
            # This is needed to help to updates the menus from time to time so to pick up sneaky changes to the loaded files
            # (ex. the user perform hand made modifications like renaming a Preset and such).
            flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node, True)
            flam3h_iterator_utils(self.kwargs).update_xml_last_loaded()
            
            # Clear any comment and user data from the node
            if flam3h_iterator_utils.exist_user_data(node):
                flam3h_iterator_utils.del_comment_and_user_data_iterator(node)
            if flam3h_iterator_utils.exist_user_data(node, FLAM3H_USER_DATA_FF):
                flam3h_iterator_utils.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)


    def flam3h_on_deleted(self) -> None:
        """Cleanup the data on deletion.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        node_instances: tuple = node.type().instances()
        
        if len(node_instances) == 1:
            
            # Init the Copy/Paste data to defaults
            try: hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
            except:
                try:
                    if hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX is not None:  # type: ignore
                        hou.session.FLAM3H_MARKED_ITERATOR_NODE: TA_MNode = None # type: ignore
                except: pass
                
            try: hou.session.FLAM3H_MARKED_FF_NODE.type() # type: ignore
            except:
                try:
                    if hou.session.FLAM3H_MARKED_FF_CHECK is not None:  # type: ignore
                        hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = None # type: ignore
                except: pass
                
            # Delete the Houdini update mode data if needed
            try: del hou.session.FLAM3H_SYS_UPDATE_MODE # type: ignore
            except: pass
            
            # Restore and delete the xforms handles VIZ data if needed
            flam3h_general_utils.util_xf_viz_set_stashed_wire_width()
            flam3h_general_utils.util_clear_xf_viz_stashed_wire_width_data()
            
            # Delete all data related to the Camera sensor viz
            flam3h_general_utils.util_clear_stashed_cam_data()
            
        else:
            # Clear menu caches
            # This is needed to help to updates the menus from time to time so to pick up sneaky changes to the loaded files
            # (ex. the user perform hand made modifications like renaming a Preset and such).
            flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node, True)
            flam3h_iterator_utils(self.kwargs).update_xml_last_loaded()
            
            # If we are deleting a FLAM3H node in xforms handles VIZ mode
            # check if others FLAM3H node are in xfomrs handles VIZ mode as well
            # and if not, restore the H viewports wire widths data
            if flam3h_general_utils(self.kwargs).util_other_xf_viz() is False:
                flam3h_general_utils.util_xf_viz_set_stashed_wire_width()
                flam3h_general_utils.util_clear_xf_viz_stashed_wire_width_data()
            
            # If we are deleting a FLAM3H node in camera Sensor Viz mode,
            # restore the viewers to their preview states and clear all the stashed cams data
            if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                flam3h_general_utils.util_set_stashed_cam()
                flam3h_general_utils.util_clear_stashed_cam_data()
            
            if hou.session.FLAM3H_MARKED_FF_CHECK: # type: ignore
                from_FLAM3H_NODE: TA_MNode = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
                
                if node == from_FLAM3H_NODE and node_instances:
                    hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = None # type: ignore
                    hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = node_instances[0] # type: ignore
                    
                    _MSG: str = f"The FLAM3H node you just deleted had its FF marked for being copied. Please, mark a FF first to copy parameters from."
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                    flam3h_general_utils.flash_message(node, f"FF marked node: DELETED")


# FLAM3H GENERAL UTILS start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class flam3h_general_utils:
    """
class flam3h_general_utils

@STATICMETHODS
* private_prm_set(node: hou.SopNode, prm_name: str, data: str | int | float) -> None:
* private_prm_deleteAllKeyframes(node: hou.SopNode, prm_name: str) -> None:
* flash_message(node: hou.SopNode, msg: str | None, timer: float=FLAM3H_FLASH_MESSAGE_TIMER, img: str | None = None) -> None:
* remove_locked_from_flame_stats(node) -> None:
* houdini_version(digit: int=1) -> int:
* clamp(x, val_max: int | float = 255) -> float:
* reset_density(node: hou.SopNode) -> None:
* my_system() -> str:
* set_status_msg(msg: str, type: str) -> None:
* isLOCK(filepath: str | bool) -> bool:
* util_open_file_explorer(filepath_name: str) -> None:
* util_getSceneViewers() -> list:
* util_getNetworkEditors() -> list:
* util_is_context(context: str, viewport: hou.paneTabType | hou.SceneViewer) -> bool:
* util_is_context_available_viewer(context: str) -> bool:
* util_is_context_available_network_editor(context: str) -> bool:
* util_clear_stashed_cam_data() -> None:
* util_set_stashed_cam() -> None:
* util_clear_xf_viz_stashed_wire_width_data() -> None:
* util_xf_viz_set_stashed_wire_width() -> None:
* util_xf_viz_force_cook(node: hou.SopNode, kwargs: dict) -> None:
* util_store_all_viewers_color_scheme_onCreate(self) -> None:

@METHODS
* menus_refresh_enum_prefs(self) -> None:
* get_node_path(self, node_name: str) -> str | None:
* util_set_clipping_viewers(self) -> None:
* util_store_all_viewers(self) -> None:
* util_set_front_viewer(self, update: bool=True) -> bool:
* util_set_front_viewer_all(self, node: hou.SopNode, update_sensor: bool, _SYS_FRAME_VIEW_SENSOR_prm: bool, update: bool = True) -> bool:
* util_store_all_viewers_xf_viz(self) -> None:
* util_other_xf_viz(self) -> bool:
* util_viewport_bbox_frame(self) -> None:
* flam3h_other_sensor_viz_off(self, node: hou.SopNode) -> None:
* flam3h_outsensor_toggle(self, prm_name: str=OUT_RENDER_PROPERTIES_SENSOR) -> None:
* flam3h_xf_viz_toggle(self, prm_name: str = PREFS_PVT_XF_VIZ) -> None:
* flam3h_toggle_sys_xf_viz_solo(self) -> None:
* flam3h_toggle_sys_xf_ff_viz_solo(self) -> None:
* flam3h_toggle_mp_xf_viz(self) -> None:
* flam3h_toggle_xf_ff_viz(self) -> None:
* flam3h_toggle(self, prm_name: str) -> None:
* flam3h_toggle_private(self, prm_name: str) -> None:
* flam3h_toggle_private_FF(self, prm_name: str = PREFS_PVT_DOFF) -> None:
* flam3h_toggle_off(self, prm_name: str) -> None:
* flam3h_init_presets_CP_PRESETS(self, mode: int = 1, destroy_menus: bool = True, json_file: bool | None = None, f3h_json_file: bool | None = None, json_path_checked: str | bool | None = None) -> None:
* flam3h_init_presets_IN_PRESETS(self, mode: int = 1) -> None:
* flam3h_init_presets_OUT_PRESETS(self, destroy_menus: bool = True) -> None:
* flam3h_display_help(self) -> None:
* util_store_all_viewers_color_scheme(self) -> None:
* colorSchemeDark(self, update_others: bool = True) -> None:
* viewportParticleDisplay(self) -> None:
* viewportParticleSize(self, reset_val: float | None = None) -> None:
* viewportWireWidth(self, reset_val: float | None = None) -> None:
* reset_SYS(self, density: int, iter: int, mode: int) -> None:
* reset_MB(self) -> None:
* reset_PREFS(self, mode: int = 0) -> None:
    """    
    
    __slots__ = ("_kwargs", "_node", "_bbox_sensor_path", "_bbox_reframe_path")
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs: dict = kwargs
        self._node = kwargs['node']
        # Why am I doing the following ? Because with time FLAM3H grew and evolved and I was tiered to keep updating an hard coded node path,
        # hence I added the following so I can always find the nodes even if I place them in different locations from time to time.
        self._bbox_sensor_path: str | None = self.get_node_path(OUT_BBOX_NODE_NAME_SENSOR)
        self._bbox_reframe_path: str | None = self.get_node_path(OUT_BBOX_NODE_NAME_REFRAME)


    @staticmethod
    def private_prm_set(node: hou.SopNode, _prm: str | hou.Parm, data: str | int | float) -> None:
        """Set a parameter value while making sure to unlock and lock it right after.
        This is being introduced to add an extra level of security so to speak to certain parameters
        that are not meant to be changed by the user, so at least it will require some step before allowing them to do so.
        
        Args:
            node(hou.SopNode): this FLAM3H node.
            prm_name(str | hou.Parm): the parameter name or the parameter hou.Parm directly.
            data(str | int | float): The value to set the parameter to.
            
        Returns:
            (None):
        """ 
        if isinstance(_prm, str): prm: hou.Parm = node.parm(_prm)
        elif isinstance(_prm, hou.Parm): prm: hou.Parm = _prm
        prm.lock(False)
        prm.set(data) # type: ignore # the set method for the hou.Parm exist but it is not recognized
        prm.lock(True)
        
        
    @staticmethod
    def private_prm_deleteAllKeyframes(node: hou.SopNode, _prm: str | hou.Parm) -> None:
        """Delete all parameter's keyframes while making sure to unlock and lock it right after.
        This is being introduced to add an extra level of security so to speak to certain parameters
        that are not meant to be changed by the user, so at least it will require some step before allowing them to do so.
        
        Args:
            node(hou.SopNode): this FLAM3H node.
            prm_name(str | hou.Parm):  the parameter name or the parameter hou.Parm directly.
            
        Returns:
            (None):
        """ 
        if isinstance(_prm, str): prm: hou.Parm = node.parm(_prm)
        elif isinstance(_prm, hou.Parm): prm: hou.Parm = _prm
        prm.lock(False)
        prm.deleteAllKeyframes()
        prm.lock(True)


    @staticmethod
    def flash_message(node: hou.SopNode, msg: str | None, timer: float=FLAM3H_FLASH_MESSAGE_TIMER, img: str | None = None) -> None:
        """Cause a message to appear on the top left of the network editor.
        This will work either in Sop and Lop context as it is handy to get those messages either ways. 

        Args:
            node(hou.SopNode): the current FLAM3H node.
            msg(str | None): The string message to print or None.
            timer(float): Default to: FLAM3H_FLASH_MESSAGE_TIMER. How long the printed message stay before it fade away.
            img(str | None): Default to none. specifies an icon or image file that should be displayed along with the text specified in the msg argument.

        Returns:
            (None):
        """  
        if hou.isUIAvailable() and node.parm(PREFS_FLASH_MSG).eval():
            [ne.flashMessage(img, msg, timer) for ne in [p for p in hou.ui.paneTabs() if p.type() == hou.paneTabType.NetworkEditor]] # type: ignore
        

    @staticmethod
    def remove_locked_from_flame_stats(node) -> None:
        """When loading a flame preset from the clipboard while a valid locked flame library is loaded,
        deleting the path string will leave the text: -> LOCKED inside the stats.
        This definition will remove it.

        Args:
            node (hou.SopNode): This FLAM3H node
            
        Returns:
            (None):
        """  
        stats: str = node.parm(MSG_IN_FLAMESTATS).eval()
        lines: list = stats.splitlines()
        if lines[0] == MSG_FLAMESTATS_LOCK: lines[0] = ''
        node.setParms({MSG_IN_FLAMESTATS: "\n".join(lines)})


    @staticmethod
    def houdini_version(digit: int=1) -> int:
        """Retrieve the major Houdini version number currently in use.

        Args:
            digit(int): Default to 1: H_19, H_20. if set to 2: H_190, H_195, H_200, H_205, and so on.

        Returns:
            (int): By default it will retrieve major Houdini version number. ex: 19, 20 but not: 195, 205
        """  
        return int(''.join(str(x) for x in hou.applicationVersion()[:digit]))


    @staticmethod  
    def clamp(x, val_max: int | float = 255) -> float:
        """clamp a value to be between Zero and 255.

        Args:
            x(int | float): the value to clamp.
            val_max(int | float): Default to: 255. Max value to clamp to.

        Returns:
            float: value clamped between Zero and 255.
        """
        return float(max(0, min(x, val_max)))


    @staticmethod
    def reset_density(node: hou.SopNode) -> None:
        """Reset/set density to its default.

        Args:
            (None):

        Returns:
            (None):
        """  
        node.parm(GLB_DENSITY).deleteAllKeyframes()
        node.parm(GLB_DENSITY_PRESETS).deleteAllKeyframes()
        node.setParms({GLB_DENSITY: FLAM3H_DEFAULT_GLB_DENSITY}) # type: ignore
        node.setParms({GLB_DENSITY_PRESETS: 1}) # type: ignore


    @staticmethod
    def my_system() -> str:
        """Return the OS we are on.

        Args:
            (None):
            
        Returns:
            (str): Possible outcomes are: 
            * WIN (windows)
            * LNX (linux)
            * MAC
            * JAVA
            * UNKNW
        """
        sys: str = platform_system()
        sys_options: dict[str, str] = {'Windows': 'WIN', 'Linux': 'LNX', 'Darwin': 'MAC', 'Java': 'JAVA'}
        mysys: str | None = sys_options.get(sys)
        if mysys is not None: return mysys
        else: return 'UNKNW'


    @staticmethod
    def set_status_msg(msg: str, type: str) -> None:
        """Print a message to the Houdini's status bar if the UI is available.

        Args:
            msg(str): The message string to print
            type(str): The type of severity message to use, Possible choises are: MSG ( message ), IMP ( important message ), WARN ( warning ).
            
        Returns:
            (None):
        """

        if hou.isUIAvailable():
            st: dict[str, hou.EnumValue] = { 'MSG': hou.severityType.Message, 'IMP': hou.severityType.ImportantMessage, 'WARN': hou.severityType.Warning }  # type: ignore
            hou.ui.setStatusMessage(msg, st.get(type)) # type: ignore


    @staticmethod
    def isLOCK(filepath: str | bool) -> bool:
        """Check if the loaded lib file ( Palette or flame XML ) is locked.

        Args:
            filepath(str | bool): the full lib file path.

        Returns:
            (bool): True if locked. False if not.
        """
        if filepath is not False:
            if os.path.exists(filepath) and os.path.split(str(filepath))[-1].startswith(FLAM3H_LIB_LOCK):
                return True
            else:
                return False
        else:
            return False


    @staticmethod
    def util_open_file_explorer(filepath_name: str) -> None:
        """Open the file explorer to the currently loaded file location.

        Args:
            filepath_name(str): The currently loaded file name full path.
            
        Returns:
            (None):
        """
        # If it is an exisiting valid file path
        if os.path.isfile(filepath_name):
            hou.ui.showInFileBrowser(filepath_name) # type: ignore
            
        # If the parent directory exist
        else:
            dir = os.path.dirname(filepath_name)
            if os.path.isdir(dir):
                hou.ui.showInFileBrowser(dir) # type: ignore


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
    def util_getNetworkEditors() -> list:
        """Return a list of NetworkEditors currently open in this Houdini session.
        
        Args:
            (None):
            
        Returns:
            (list): [return a list of open scene viewers]
        """    
        views: tuple = hou.ui.paneTabs() # type: ignore
        return [v for v in views if isinstance(v, hou.NetworkEditor)]
    
    
    @staticmethod
    def util_is_context(context: str, viewport: hou.paneTabType | hou.SceneViewer) -> bool:
        """Return if we are inside a context or not.
        
        Args:
            context(str): The context we want to check if we are currently in. Options so far are: 
                * Sop: str
                * Lop: str
            viewport(hou.paneTabType): Any of the available pane tab types, in my case will always be: hou.paneTabType.SceneViewer or hou.SceneViewer
            
        Returns:
            (bool): [True if we are in desired context or False if we are not.]
        """    
        context_now: hou.NodeTypeCategory = hou.ui.findPaneTab(viewport.name()).pwd().childTypeCategory() # type: ignore
        if str(context_now.name()).lower() == context.lower(): return True
        else: return False


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
        available = False
        for v in flam3h_general_utils.util_getSceneViewers():
            if flam3h_general_utils.util_is_context(context, v):
                available = True
                break
        return available
    
    
    @staticmethod
    def util_is_context_available_network_editor(context: str) -> bool:
        """Return if there are network editors that belong to a desired context.
        
        Args:
            context(str): The context we want to check if we are currently in. Options so far are: 
                * Sop: str
                * Lop: str
            
        Returns:
            (bool): [True if there is at least one NetworkEditor that belong to a desired context or False if not.]
        """    
        available = False
        for v in flam3h_general_utils.util_getNetworkEditors():
            if flam3h_general_utils.util_is_context(context, v):
                available = True
                break
        return available
    

    @staticmethod
    def util_clear_stashed_cam_data() -> None:
        """Clear the stored stashed cam/cams data.

        Args:
            (None):
            
        Returns:
            (None):
        """
        try: del hou.session.FLAM3H_SENSOR_CAM_STASH # type: ignore
        except: pass
        try: del hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE # type: ignore
        except: pass
        try: del hou.session.FLAM3H_SENSOR_CAM_STASH_COUNT # type: ignore
        except: pass
        try: del hou.session.FLAM3H_SENSOR_CAM_STASH_DICT # type: ignore
        except: pass
        try: del hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE_DICT # type: ignore
        except: pass


    @staticmethod
    def util_set_stashed_cam() -> None:
        """Set/Load the stored stashed camera if a stashed camera data is available.
        It will also restore multiple stashed cameras if multiple viewers were open when entering the Sensor Viz mode.

        Args:
            (None):
            
        Returns:
            (None):
        """
        desktop: hou.Desktop = hou.ui.curDesktop() # type: ignore
        viewport: hou.SceneViewer = desktop.paneTabOfType(hou.paneTabType.SceneViewer) # type: ignore
        
        try: _CAMS: int | None = hou.session.FLAM3H_SENSOR_CAM_STASH_COUNT # type: ignore
        except: _CAMS: int | None = None
        
        if _CAMS is None:
            
            if viewport is not None and viewport.isCurrentTab() and flam3h_general_utils.util_is_context('Sop', viewport):
                
                view: hou.GeometryViewport = viewport.curViewport()
                
                try: _CAM_STASHED: hou.GeometryViewportCamera | None = hou.session.FLAM3H_SENSOR_CAM_STASH # type: ignore
                except: _CAM_STASHED: hou.GeometryViewportCamera | None = None
                    
                if _CAM_STASHED is not None:
                    
                    if _CAM_STASHED.isPerspective():
                        view.changeType(hou.geometryViewportType.Perspective) # type: ignore
                        view.setDefaultCamera(_CAM_STASHED) # type: ignore
                        
                    elif _CAM_STASHED.isOrthographic:
                        
                        try: _CAM_STASHED_TYPE: hou.geometryViewportType | None = hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE # type: ignore
                        except: _CAM_STASHED_TYPE: hou.geometryViewportType | None = None
                            
                        if _CAM_STASHED_TYPE is not None:
                            view.changeType(_CAM_STASHED_TYPE) # type: ignore
                            view_obj = view.defaultCamera()
                            view_obj.setOrthoWidth(_CAM_STASHED.orthoWidth())
                            view_obj.setTranslation(_CAM_STASHED.translation())
                            
        else:
            try: _STASH_DICT: dict[str, hou.GeometryViewportCamera] | None = hou.session.FLAM3H_SENSOR_CAM_STASH_DICT # type: ignore
            except: _STASH_DICT: dict[str, hou.GeometryViewportCamera] | None = None
            try: _TYPE_DICT: dict[str, hou.geometryViewportType] | None = hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE_DICT # type: ignore
            except: _TYPE_DICT: dict[str, hou.geometryViewportType] | None = None
                
            if _STASH_DICT is not None and _TYPE_DICT is not None:
                
                for v in flam3h_general_utils.util_getSceneViewers():
                    
                    # Restore only if it is a Sop viewer
                    if flam3h_general_utils.util_is_context('Sop', v):
                        
                        view: hou.GeometryViewport = v.curViewport()
                        key: str = v.name()
                        _STASH: hou.GeometryViewportCamera | None = _STASH_DICT.get(key)
                        if _STASH is not None:
                            if _STASH.isPerspective():
                                view.changeType(hou.geometryViewportType.Perspective) # type: ignore
                                view.setDefaultCamera(_STASH) # type: ignore
                                
                            elif _STASH.isOrthographic:
                                _TYPE: hou.geometryViewportType | None = _TYPE_DICT.get(key)
                                if _TYPE is not None:
                                    view.changeType(_TYPE) # type: ignore
                                    view_obj = view.defaultCamera()
                                    view_obj.setOrthoWidth(_STASH.orthoWidth())
                                    view_obj.setTranslation(_STASH.translation())
        
                                
    @staticmethod
    def util_clear_xf_viz_stashed_wire_width_data() -> None:
        """Clear the stored stashed cam/cams data.

        Args:
            (None):
            
        Returns:
            (None):
        """
        try: del hou.session.H_XF_VIZ_WIRE_WIDTH_STASH_DICT # type: ignore
        except: pass
    
    
    @staticmethod
    def util_xf_viz_set_stashed_wire_width() -> None:
        """Set/Load the stored stashed cameras viewport wire widths.

        Args:
            (None):
            
        Returns:
            (None):
        """
        
        # This stashed dict is already without any Lop viewers. They have been filtered inside:
        #   * flam3h_general_utils.util_store_all_viewers_xf_viz(self) -> None:
        try: _STASH_DICT: dict[str, float] | None = hou.session.H_XF_VIZ_WIRE_WIDTH_STASH_DICT # type: ignore
        except: _STASH_DICT: dict[str, float] | None = None
        
        if _STASH_DICT is not None:
            for v in flam3h_general_utils.util_getSceneViewers():
                view: hou.GeometryViewport = v.curViewport()
                key: str = v.name()
                # Since all the viewers inside this stashed dict are sure not to be a Lop viewer
                # we do not need to check and we can just proceed.
                _STASH: float | None = _STASH_DICT.get(key)
                if _STASH is not None:
                    settings: hou.GeometryViewportSettings = view.settings()
                    settings.wireWidth(_STASH)


    @staticmethod
    def util_xf_viz_force_cook(node: hou.SopNode, kwargs: dict) -> None:
        """Force viewport xforms handles VIZ to cook when the mode is OFF
        to have the geometry ready when the user turn the mode ON.
        
        If not success, it will pass silently and throw a warning message.

        Args:
            node(hou.SopNode): This FLAM3H node
            kwargs:(dict): this FLAM3H node kwargs
            
        Returns:
            (None):
        """   
        if not node.parm(PREFS_PVT_XF_VIZ).eval():
            # BUILD XFVIZ
            try: hou.node(flam3h_general_utils(kwargs).get_node_path(PREFS_XFVIZ_NODE_NAME)).cook(force=True)
            except: 
                flam3h_general_utils.set_status_msg(f"{node.name()}: XF VIZ node not found.", 'WARN')
                pass


    @staticmethod
    def util_store_all_viewers_color_scheme_onCreate() -> None:
        """Store dictionaries of viewers color schemes if needed on FLAM3H node creation
        This version do not check from which parameter run as we need it to run regardless.
        
        It will check the currently stored color schemes data and update it if there is a need to do so.
        
        Args:
            node(hou.SopNode): This FLAM3H node
            
        Returns:
            (None):  
        """  
        # Check if the required data exist already
        try:
            hou.session.H_CS_STASH_DICT # type: ignore
        except:
            _EXIST: bool = False
        else:
            _EXIST: bool = True
            
        # build a new one
        views_scheme: list[hou.viewportColorScheme]  = []
        views_keys: list[str] = []
        
        for v in flam3h_general_utils.util_getSceneViewers():
            
            # Store only if it is a Sop viewer
            if flam3h_general_utils.util_is_context('Sop', v):
                
                view: hou.GeometryViewport = v.curViewport()
                settings: hou.GeometryViewportSettings = view.settings()
                _CS: hou.viewportColorScheme = settings.colorScheme()
                if _CS != hou.viewportColorScheme.Dark: # type: ignore
                    views_scheme.append(_CS)
                    views_keys.append(v.name())
        
        # Always store and update this data if we collected something
        if views_scheme and views_keys:
            new: dict[str, hou.viewportColorScheme] = dict(zip(views_keys, views_scheme)) # type: ignore
            if _EXIST:
                # Check if it needs an update
                if new != hou.session.H_CS_STASH_DICT: #type: ignore
                    __old_to_update: dict[str, hou.viewportColorScheme] = hou.session.H_CS_STASH_DICT.copy() #type: ignore
                    for key, value in new.items():
                        if value != hou.viewportColorScheme.Dark: # type: ignore
                            if key not in __old_to_update.keys(): __old_to_update[key] = value
                    hou.session.H_CS_STASH_DICT: dict[str, hou.viewportColorScheme] = __old_to_update #type: ignore
            else:
                # otherwise create
                hou.session.H_CS_STASH_DICT: dict[str, hou.viewportColorScheme] = new # type: ignore


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
    def bbox_sensor_path(self):
        return self._bbox_sensor_path
    
    @property
    def bbox_reframe_path(self):
        return self._bbox_reframe_path


    def menus_refresh_enum_prefs(self) -> None:
        """Refresh and force presets menus names to update
        after the preference's option "enumerate presets menu" has been toggled ON or OFF
        and also from inside other places, following a list:
        * def util_set_front_viewer(self, update: bool = True) -> bool:
        * def util_viewport_bbox_frame(self) -> None:
        * def flam3h_outsensor_toggle(self, prm_name: str=OUT_RENDER_PROPERTIES_SENSOR) -> None:
        * def flam3h_toggle(self, prm_name: str) -> None:
        * def flam3h_toggle_off(self, prm_name: str) -> None:
                                                            
        Args:
            (self):
            
        Returns:
            (None):                            
        """ 
        node = self.node
        # Clear menu caches
        flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node)
        flam3h_iterator_utils(self.kwargs).update_xml_last_loaded()
        
        prm_menus: tuple = (node.parm(CP_PALETTE_PRESETS),
                            node.parm(CP_PALETTE_PRESETS_OFF),
                            node.parm(CP_SYS_PALETTE_PRESETS),
                            node.parm(CP_SYS_PALETTE_PRESETS_OFF),
                            node.parm(IN_PRESETS),
                            node.parm(IN_PRESETS_OFF),
                            node.parm(IN_SYS_PRESETS),
                            node.parm(IN_SYS_PRESETS_OFF),
                            node.parm(OUT_PRESETS),
                            node.parm(OUT_SYS_PRESETS)
                        )
        # This is probably light weight enough to be run all together
        # However in the future will be better to split this to run per type with checks (CP, IN and OUT)
        [prm.set(prm.eval()) for prm in prm_menus]


    def get_node_path(self, node_name: str) -> str | None:
        """Find the full path of the bbox data null node
        inside the current FLAM3H node.
        
        The Null node names prefixes to search are stored inside the global variables:
        
        * OUT_BBOX_NODE_NAME_SENSOR
        * OUT_BBOX_NODE_NAME_REFRAME

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
            _MSG: str = f"{self.node.name()}: Camera sensor BBOX data node not found."
            self.set_status_msg(_MSG, 'WARN')
            return None


    def util_set_clipping_viewers(self) -> None:
        """Set current viewport camera clipping near/far planes
        
        Args:
            (self):
            
        Returns:
            (None):  
        """
        for view in self.util_getSceneViewers():
            # It is handy to set the clipping planes also on LOP viewers
            # so there is no check to know if we are setting a SOP or LOP viewer
            curView: hou.GeometryViewport = view.curViewport()
            settings = curView.settings()
            settings.setHomeAutoAdjustsClip( hou.viewportHomeClipMode.Neither ) # type: ignore
            settings.setClipPlanes( (0.001, 1000) )
            settings.homeAutoAdjustClip()
            settings.clipPlanes()


    def util_store_all_viewers(self) -> None:
        """Store dictionaries of viewers cameras and their types
        
        Args:
            (self):
            
        Returns:
            (None):  
        """  
        # Do this only once; when we enter the sensor viz
        try: parm = self.kwargs['parm']
        except: parm = None
        _ENTER_PRM = None
        if parm is not None: _ENTER_PRM = parm.name()
        if _ENTER_PRM is not None and _ENTER_PRM == OUT_RENDER_PROPERTIES_SENSOR_ENTER:
            views_cam: list[hou.GeometryViewportCamera]  = []
            views_keys: list[str] = []
            views_type: list[hou.geometryViewportType] = []
            for v in self.util_getSceneViewers():
                # Store only if it is a Sop viewer
                if self.util_is_context('Sop', v):
                    view: hou.GeometryViewport = v.curViewport()
                    views_cam.append(view.defaultCamera().stash())
                    views_keys.append(v.name())
                    views_type.append(view.type())
                
            # Store everything into the hou.session so we can retrieve them later but keep them if they exist already
            # as it mean another FLAM3H node was already im camera sensor mode and we likely want to restore what was already stored.
            try: hou.session.FLAM3H_SENSOR_CAM_STASH_COUNT # type: ignore
            except: hou.session.FLAM3H_SENSOR_CAM_STASH_COUNT: int = len(views_cam) # type: ignore
            try: hou.session.FLAM3H_SENSOR_CAM_STASH_DICT # type: ignore
            except: hou.session.FLAM3H_SENSOR_CAM_STASH_DICT: dict[str, hou.GeometryViewportCamera] = dict(zip(views_keys, views_cam)) # type: ignore
            try: hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE_DICT # type: ignore
            except: hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE_DICT: dict[str, hou.geometryViewportType] = dict(zip(views_keys, views_type)) # type: ignore
            

    def util_set_front_viewer(self, update: bool = True) -> bool:
        """Set front view when entering the camera sensor mode.
        This include storing and restoring the current viewport prior to entering the camera sensor mode if there is only one and is: viewport.isCurrentTab().
        Otherwise it will set them all if multiple viewports are present and restore them all on exit.
        
        This definition is multipurpose, it is run from multiple parameters:
        * When run from the SYS prm: _SYS_FRAME_VIEW_SENSOR_prm it will also print a flash message.
        * When run from the OUT Sensor prms, it will re frame the sensor based of if update sensor prm is ON or OFF.
        * When run while loading a hip file it will test the necessary condition to see if it can work ort not.
        
        Maybe it would be better to split all those purposes into their own definition for each...but good for now.
        
        _NOTE:
            This definition is also run inside the following definitions:
            
            * def flam3h_outsensor_toggle(self, prm_name: str=OUT_RENDER_PROPERTIES_SENSOR) -> None:
            * def iterators_count(self) -> None:
            * def util_viewport_bbox_frame(self) -> None:
            * def in_copy_render_all_stats_msg(kwargs: dict,  apo_data: in_flame_iter_data | None=None, clipboard: bool=False) -> None:
            * def in_copy_sensor_stats_msg(kwargs: dict) -> None:
            * def in_copy_render_stats_msg(kwargs: dict) -> None:
            * def menu_sensor_resolution_set(self, update=True) -> None:
            * def reset_OUT_kwargs(self) -> None:
            * def reset_OUT(self, mode=0) -> None:
            * def flam3h_on_loaded(self) -> None:

        Args:
            (self):
            update(bool): Defaults to True. Updated the viewport camera sensor or not(False)
            
        Returns:
            (bool): True if the Sensor Viz is being activated. False if not.
        """     
        node = self.node
        if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
            
            desktop: hou.Desktop = hou.ui.curDesktop() # type: ignore
            viewport: hou.SceneViewer = desktop.paneTabOfType(hou.paneTabType.SceneViewer) # type: ignore
            
            # check if there are more than one viewport available
            viewports: list = self.util_getSceneViewers()
            
            # Get some data for down the line condition checks
            update_sensor: int = self.node.parm(OUT_UPDATE_SENSOR).eval()
            _SYS_FRAME_VIEW_SENSOR_prm = False
            try:
                if self.kwargs['parm'].name() == SYS_FRAME_VIEW_SENSOR:
                    _SYS_FRAME_VIEW_SENSOR_prm =True
                    # Refresh menu caches
                    self.menus_refresh_enum_prefs()
            except: pass
            
            # If the viewport is: viewport.isCurrentTab()
            if viewport is not None and len(viewports) == 1 and viewport.isCurrentTab():
                
                # Set only if it is a Sop viewer
                if self.util_is_context('Sop', viewport):
                    
                    view: hou.GeometryViewport = viewport.curViewport()
                    
                    # Do this only once; when we enter the sensor viz
                    try: parm = self.kwargs['parm']
                    except: parm = None
                    _ENTER_PRM = None
                    if parm is not None: _ENTER_PRM = parm.name()
                    if _ENTER_PRM is not None and _ENTER_PRM == OUT_RENDER_PROPERTIES_SENSOR_ENTER:
                        try: _CAM_STASHED: hou.GeometryViewportCamera | None = hou.session.FLAM3H_SENSOR_CAM_STASH # type: ignore
                        except: _CAM_STASHED: hou.GeometryViewportCamera | None = None
                            
                        if _CAM_STASHED is None:
                            cam = view.defaultCamera()
                            hou.session.FLAM3H_SENSOR_CAM_STASH: hou.GeometryViewportCamera = cam.stash() # type: ignore
                            hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE: hou.geometryViewportType = view.type() # type: ignore
                    
                    if view.type() != hou.geometryViewportType.Front: # type: ignore
                        view.changeType(hou.geometryViewportType.Front) # type: ignore
                        
                    if update:
                        if self.bbox_sensor_path is not None:
                            node_bbox: hou.SopNode = hou.node(self.bbox_sensor_path)
                            if hou.hipFile.isLoadingHipFile(): # type: ignore
                                # This fail on "isLoadingHipFile" under H19.x, H19.5.x and H20.0.506
                                # but work on H20.0.590 and up, hence the try/except block
                                try: view.frameBoundingBox(node_bbox.geometry().boundingBox())
                                except:
                                    node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                                    self.util_clear_stashed_cam_data()
                                    return False
                            else:
                                view.frameBoundingBox(node_bbox.geometry().boundingBox())

                            if _SYS_FRAME_VIEW_SENSOR_prm:
                                self.flash_message(node, f"sensor REFRAMED")
                                
                            return True

                    else:
                        # update_sensor = self.node.parm(OUT_UPDATE_SENSOR).eval()
                        if update_sensor or _SYS_FRAME_VIEW_SENSOR_prm:
                            if self.bbox_sensor_path is not None:
                                node_bbox: hou.SopNode = hou.node(self.bbox_sensor_path)
                                if hou.hipFile.isLoadingHipFile(): # type: ignore
                                    # This fail on "isLoadingHipFile" under H19.x, H19.5.x and H20.0.506
                                    # but work on H20.0.590 and up, hence the try/except block
                                    try: view.frameBoundingBox(node_bbox.geometry().boundingBox())
                                    except:
                                        node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                                        self.util_clear_stashed_cam_data()
                                        return False
                                else:
                                    view.frameBoundingBox(node_bbox.geometry().boundingBox())
                                    
                                    if _SYS_FRAME_VIEW_SENSOR_prm:
                                        self.flash_message(node, f"sensor REFRAMED")
                                        
                                return True
                            
                    return False
                
                else:
                    # If we were activating the Camera Sensor mode
                    if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                        # Revert it back to OFF and fire a message
                        node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                        _MSG: str = f"No Sop viewers available."
                        self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Sop viewer for the Camera Sensor to work.", 'WARN')
                        self.flash_message(node, f"{_MSG}")
                        
                    return False
                    
            else:
                self.util_store_all_viewers()
                if self.util_set_front_viewer_all(node, bool(update_sensor), _SYS_FRAME_VIEW_SENSOR_prm, update):
                    return True
                else:
                    # Or just exit the Sensor Viz mode
                    self.flam3h_other_sensor_viz_off(self.node)
                    self.node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                    self.util_clear_stashed_cam_data()
                    return False
                
        return False


    def util_set_front_viewer_all(self, node: hou.SopNode, update_sensor: bool, _SYS_FRAME_VIEW_SENSOR_prm: bool, update: bool = True) -> bool:
        """This is a fall back if the: util_set_front_viewer(...) can not run succesfully.
        It will activate the Sensor Viz in all available viewports with the ability of storing and restoring a stashed camera for each.

        Args:
            (self):
            node(hou.SopNode): FLAM3H node
            update_sensor(bool): Is the force sensor update toggle ON or OFF ?
            _SYS_FRAME_VIEW_SENSOR_prm(bool): Is this being run from the SYS tab reframe viewport icon ?
            update(bool): Is the updated Sensor Viz toggle ON or OFF ?
            
        Returns:
            (bool): True if the Sensor Viz is being activated. False if not.
        """ 
        if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
            
            viewports: list = self.util_getSceneViewers()
            if len(viewports):
                
                lop_viewports: list = []
                # Set them all without storing any stashed camera data 
                self.util_set_clipping_viewers()
                for v in viewports:
                    
                    # Set only if it is a Sop viewer
                    if self.util_is_context('Sop', v):
                        
                        view: hou.GeometryViewport = v.curViewport()
                        if view.type() != hou.geometryViewportType.Front: # type: ignore
                            view.changeType(hou.geometryViewportType.Front) # type: ignore
                        if update:
                            if self.bbox_sensor_path is not None:
                                node_bbox: hou.SopNode = hou.node(self.bbox_sensor_path)
                                if hou.hipFile.isLoadingHipFile(): # type: ignore
                                    # This fail on "isLoadingHipFile" under H19.x, H19.5.x and H20.0.506
                                    # but work on H20.0.590 and up, hence the try/except block
                                    try: view.frameBoundingBox(node_bbox.geometry().boundingBox())
                                    except:
                                        node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0}) # type: ignore
                                        self.util_clear_stashed_cam_data()
                                        return False
                                else:
                                    view.frameBoundingBox(node_bbox.geometry().boundingBox())

                                if _SYS_FRAME_VIEW_SENSOR_prm:
                                    self.flash_message(self.node, f"sensor REFRAMED")
                                    
                        else:
                            if update_sensor or _SYS_FRAME_VIEW_SENSOR_prm:
                                if self.bbox_sensor_path is not None:
                                    node_bbox: hou.SopNode = hou.node(self.bbox_sensor_path)
                                    if hou.hipFile.isLoadingHipFile(): # type: ignore
                                        # This fail on "isLoadingHipFile" under H19.x, H19.5.x and H20.0.506
                                        # but work on H20.0.590 and up, hence the try/except block
                                        try: view.frameBoundingBox(node_bbox.geometry().boundingBox())
                                        except:
                                            self.node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                                            self.util_clear_stashed_cam_data()
                                            return False
                                    else:
                                        view.frameBoundingBox(node_bbox.geometry().boundingBox())
                                        
                                        if _SYS_FRAME_VIEW_SENSOR_prm:
                                            self.flash_message(self.node, f"sensor REFRAMED")
                                            
                    else:
                        # Count how many Lop viewports are present
                        lop_viewports.append(True)
                        
                # If all the viewports are Lop viewports
                if len(lop_viewports) == len(viewports):
                    
                    # If we were activating the Camera Sensor mode
                    if self.node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                        # Revert it back to OFF and fire a message
                        self.node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                        _MSG: str = f"No Sop viewers available."
                        self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Sop viewer for the Sensor Viz to work.", 'WARN')
                        self.flash_message(node, f"{_MSG}")
                        
                    return False
                
                else: return True
            
            else:
                # Exit the Sensor Viz mode
                self.flam3h_other_sensor_viz_off(self.node)
                self.node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                self.util_clear_stashed_cam_data()
                
                _MSG: str = f"No Sop viewers available."
                self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Sop viewer for the Sensor Viz to work.", 'WARN')
                self.flash_message(node, f"{_MSG}")
                return False
            
        return False
    
    
    def util_store_all_viewers_xf_viz(self) -> None:
        """Store dictionaries of viewers cameras and their wire width value
        
        Args:
            (self):
            
        Returns:
            (None):  
        """  
        # Do this only once; when we activate the xforms handles VIZ
        try: parm = self.kwargs['parm']
        except: parm = None
        _ENTER_PRM = None
        if parm is not None: _ENTER_PRM = parm.name()
        if _ENTER_PRM is not None and _ENTER_PRM == SYS_XF_VIZ_OFF:
            views_widths: list[float]  = []
            views_keys: list[str] = []
            for v in self.util_getSceneViewers():
                # Store only if it is a Sop viewer
                if self.util_is_context('Sop', v):
                    
                    view: hou.GeometryViewport = v.curViewport()
                    settings: hou.GeometryViewportSettings = view.settings()
                    views_widths.append(settings.wireWidth())
                    views_keys.append(v.name())
            
            # Store everything into the hou.session so we can retrieve them later but keep them if they exist already
            # as it mean another FLAM3H node had already its viewport xforms handles VIZ ON and we likely want to restore what was already stored.
            try: hou.session.H_XF_VIZ_WIRE_WIDTH_STASH_DICT # type: ignore
            except: hou.session.H_XF_VIZ_WIRE_WIDTH_STASH_DICT: dict[str, float] = dict(zip(views_keys, views_widths)) # type: ignore
            
    
    def util_other_xf_viz(self) -> bool:
        """Check if there are other FLAM3H nodes with the xforms handles VIZ ON.
        
        Args:
            (self):
            
        Returns:
            (bool): True if there are other FLAM3H nodes with the xforms handles VIZ ON or False
        """ 
        node = self.node
        if [1 for f3h in node.type().instances() if f3h != node and f3h.parm(PREFS_PVT_XF_VIZ).eval()]: return True
        else: return False


    def util_viewport_bbox_frame(self) -> None:
        """Re-frame the current viewport based on camera sensor node's bounding box.
        
        Args:
            (self):
            
        Returns:
            (None):  
        """  
        node = self.node
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval() and not node.parm(OUT_UPDATE_SENSOR).eval():
            # This condition probably will never evaluate to True as when in Sensor Viz mode
            # a new reframe icon will be displayed with the proper definition, but its good to make this icon multipurpose anyway.
            self.util_set_clipping_viewers()
            self.util_set_front_viewer()
        
        else:
            viewports: list = self.util_getSceneViewers()
            if len(viewports):
                self.util_set_clipping_viewers()
                for v in viewports:
                    view: hou.GeometryViewport = v.curViewport()
                    if self.bbox_reframe_path is not None:
                        node_bbox: hou.SopNode = hou.node(self.bbox_reframe_path)
                        view.frameBoundingBox(node_bbox.geometry().boundingBox())
                        _MSG: str = f"Viewport REFRAMED"
                        self.flash_message(node, _MSG)
                        self.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
            else:
                _MSG: str = f"No viewports in the current Houdini Desktop."
                self.set_status_msg(f"{node.name()}: {_MSG} You need at least one viewport for the reframe to work.", 'IMP')
                self.flash_message(node, f"Sensor Viz: {_MSG}")


    def flam3h_other_sensor_viz_off(self, node: hou.SopNode) -> None:
        """When activating the Camera sensor viz, check if there is another FLAM3H in camera sensor mode
        and turn it Off if so. this way we guarantee there can be only one FLAM3H node in Camera sensor viz mode at any given time.

        Args:
            (self):
            node(hou.SopNode): This FLAM3H node

        Returns:
            (None):
        """
        all_f3h: tuple = node.type().instances()
        if len(all_f3h) > 1:
            for f3h in all_f3h:
                if f3h != node:
                    if f3h.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                        f3h.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                        # If another FLAM3H node is in Camera Sensor mode, clear up its data.
                        # after restoring the viewport prior to entering the Camera sensor mode
                        self.util_set_stashed_cam()
                        self.util_clear_stashed_cam_data()
                        break


    def flam3h_outsensor_toggle(self, prm_name: str=OUT_RENDER_PROPERTIES_SENSOR) -> None:
        """If a toggle is OFF it will switch ON, and viceversa.

        Args:
            (self):
            prm_name(str): Defaults to OUT_RENDER_PROPERTIES_SENSOR. Toggle parameter name to use.
            
        Returns:
            (None):
        """
        
        node = self.node
        prm = node.parm(prm_name)
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm.eval():
            prm.set(0)
            # Restore the viewport prior to entering the Camera sensor mode
            self.util_set_stashed_cam()
            self.util_clear_stashed_cam_data()

            _MSG: str = f"Sensor viz: OFF"
            self.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
            self.flash_message(node, _MSG)
            
        else:
            prm.set(1)
            # If the current FLAM3H node is displayed ( its displayFlag is On )
            if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
                # Check if any other FLAM3H node is in Camera Sensor viz mode
                self.flam3h_other_sensor_viz_off(node)
                # Set this FLAM3H node to enter the camera sensor viz mode
                self.util_set_clipping_viewers()
                if self.util_set_front_viewer():
                    _MSG: str = f"Sensor viz: ON"
                    self.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                    self.flash_message(node, _MSG)
            else:
                # IF displayFlag is OFF, turn the outsensor toggle OFF, too.
                prm.set(0)
                _MSG: str = f"This node display flag is OFF. Please use a FLAM3H node that is currently displayed to enter the Camera sensor viz."
                self.set_status_msg(f"{node.name()}: {str(prm.name()).upper()} -> {_MSG}", 'WARN')
                self.flash_message(node, f"{_MSG[:30]}")


    def flam3h_xf_viz_toggle(self, prm_name: str = PREFS_PVT_XF_VIZ) -> None:
        """If a toggle is OFF it will switch ON, and viceversa.

        Args:
            (self):
            prm(str): Defaults to PREFS_PVT_XF_VIZ. Toggle parameter name to use.

        Returns:
            (None):  
        """
        node = self.node
        prm = node.parm(prm_name)
        f3h_xf_viz_others: bool = self.util_other_xf_viz()
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm.eval():
            flam3h_general_utils.private_prm_set(node, prm, 0)
            
            if f3h_xf_viz_others is False:
                # Restore the viewport wire width prior to entering the xforms handles VIZ
                # only if there not other FLAM3H node in xforms handles VIZ mode.
                self.util_xf_viz_set_stashed_wire_width()
                self.util_clear_xf_viz_stashed_wire_width_data()
                
            _MSG: str = f"OFF"
            self.set_status_msg(f"{node.name()}: {str(prm.name()).upper()}: {_MSG}", 'MSG')
            self.flash_message(node, f"XF VIZ: {_MSG}")
            
        else:
            
            # There must be at least one viewport
            if self.util_is_context_available_viewer('Sop'):
            
                if f3h_xf_viz_others is False:
                    self.util_store_all_viewers_xf_viz()
                    
                # Retrieve the value we shoud be set to
                try: w: float | None = hou.session.FLAM3H_VIEWPORT_WIRE_WIDTH # type: ignore
                except: w = None
                if w is not None: self.viewportWireWidth(w)
                
                flam3h_general_utils.private_prm_set(node, prm, 1)
                
                _MSG: str = f"ON"
                self.set_status_msg(f"{node.name()}: {str(prm.name()).upper()}: {_MSG}", 'IMP')
                self.flash_message(node, f"XF VIZ: {_MSG}")
                
            else:
                flam3h_general_utils.private_prm_set(node, prm, 0)
                _MSG: str = f"No Sop viewers available."
                self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Sop viewer for the xforms handles VIZ to work.", 'WARN')
                self.flash_message(node, f"{_MSG}")
                
    
    def flam3h_all_mp_xf_viz_check(self) -> bool:
        """Check if any multiparameter have its xf_viz ON.

        Args:
            (self):

        Returns:
            (None):  
        """ 
        node = self.node
        iter_num: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        all_mp_xf_viz: list = [node.parm(f"{flam3h_iterator_prm_names().main_xf_viz}_{str(mp_idx + 1)}").eval() for mp_idx in range(iter_num)]
        if max(all_mp_xf_viz) == 1: return True
        else: return False
        
        
    def flam3h_toggle_sys_xf_viz_solo(self) -> None:
        """When in xform VIZ SOLO mode, this will turn it off and go back to viz them all.
        Specifically built for the SYS -> "xfviz_on_solo" icon parameter.

        Args:
            (self):

        Returns:
            (None):  
        """
        node = self.node
        iter_num: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        prm = node.parm(PREFS_PVT_XF_VIZ_SOLO)
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm.eval():
            self.private_prm_set(node, PREFS_PVT_XF_VIZ_SOLO, 0)
            [node.setParms({f"{flam3h_iterator_prm_names().main_xf_viz}_{str(mp_idx + 1)}": 0}) for mp_idx in range(iter_num)]
            flam3h_iterator_utils.destroy_userData(node, f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}")
            
            _MSG: str = f"{node.name()}: {str(prm.name()).upper()}: OFF"
            self.set_status_msg(_MSG, 'MSG')
            self.flash_message(node, f"XF VIZ: ALL")
            
        else:
            
            _MSG: str = f"{node.name()}: {str(prm.name()).upper()}: ON"
            self.set_status_msg(_MSG, 'IMP')
            
            
    def flam3h_toggle_sys_xf_ff_viz_solo(self) -> None:
        """When in xform VIZ SOLO mode, this will turn it off and go back to viz them all.
        Specifically built for the SYS -> "xfvizff_on_solo" icon parameter.

        Args:
            (self):

        Returns:
            (None):  
        """
        node = self.node
        prm_FF = node.parm(PREFS_PVT_XF_FF_VIZ_SOLO)
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm_FF.eval():
            self.private_prm_set(node, PREFS_PVT_XF_FF_VIZ_SOLO, 0)
            flam3h_iterator_utils.destroy_userData(node, f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}")
            
            _MSG: str = f"{node.name()}: {str(prm_FF.name()).upper()}: OFF"
            self.set_status_msg(_MSG, 'MSG')
            self.flash_message(node, f"XF VIZ: ALL")
            
        else:
            
            _MSG: str = f"{node.name()}: {str(prm_FF.name()).upper()}: ON"
            self.set_status_msg(_MSG, 'IMP')
                
                
    def flam3h_toggle_mp_xf_viz(self) -> None:
        """If a toggle is OFF it will switch ON, and viceversa.
        Specifically built for the XF VIZ multiparameter icons.
        

        Args:
            (self):

        Returns:
            (None):  
        """    
        
        # with hou.undos.disabler(): # type: ignore
        
        node: hou.SopNode = self.node
        iter_num: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        
        mp_idx: int = self.kwargs['script_multiparm_index']
        prm_mp = node.parm(f"{flam3h_iterator_prm_names().main_xf_viz}_{mp_idx}")
        
        data_name = f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}"
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm_mp.eval():
            prm_mp.set(0)
            self.private_prm_set(node, PREFS_PVT_XF_VIZ_SOLO, 0)
            flam3h_iterator_utils.destroy_userData(node, f"{data_name}")
            
            _MSG: str = f"{node.name()}: VIZHANDLES_SOLO: OFF"
            self.set_status_msg(_MSG, 'MSG')
            self.flash_message(node, f"XF VIZ: ALL")
            
        else:
            [node.setParms({f"{flam3h_iterator_prm_names().main_xf_viz}_{str(mp_idx + 1)}": 0}) for mp_idx in range(iter_num)] # type: ignore
            prm_mp.set(1)
            self.private_prm_set(node, PREFS_PVT_XF_VIZ_SOLO, 1)
            self.private_prm_set(node, PREFS_PVT_XF_VIZ_SOLO_MP_IDX, int(mp_idx))
            self.private_prm_set(node, PREFS_PVT_XF_FF_VIZ_SOLO, 0)
            node.setUserData(f"{data_name}", mp_idx)
                
            _MSG: str = f"{node.name()}: {str(prm_mp.name()).upper()}: ON"
            self.set_status_msg(_MSG, 'IMP')
            self.flash_message(node, f"XF VIZ: {mp_idx}")
            
            
    def flam3h_toggle_xf_ff_viz(self) -> None:
        """If a toggle is OFF it will switch ON, and viceversa.
        Specifically built for the XF FF VIZ icons.
        

        Args:
            (self):

        Returns:
            (None):  
        """    
        
        # with hou.undos.disabler(): # type: ignore
        
        node: hou.SopNode = self.node
        iter_num: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        
        # mp_idx = self.kwargs['script_multiparm_index']
        prm_mp = node.parm(PREFS_PVT_XF_FF_VIZ_SOLO)
        data_name = f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}"
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm_mp.eval():
            self.private_prm_set(node, PREFS_PVT_XF_FF_VIZ_SOLO, 0)
            flam3h_iterator_utils.destroy_userData(node, f"{data_name}")
            
            _MSG: str = f"{node.name()}: VIZHANDLESFF_SOLO: OFF"
            self.set_status_msg(_MSG, 'MSG')
            self.flash_message(node, f"XF VIZ: ALL")
            
        else:
            [node.setParms({f"{flam3h_iterator_prm_names().main_xf_viz}_{str(mp_idx + 1)}": 0}) for mp_idx in range(iter_num)] # type: ignore
            self.private_prm_set(node, PREFS_PVT_XF_FF_VIZ_SOLO, 1)
            self.private_prm_set(node, PREFS_PVT_XF_VIZ_SOLO, 0)
            node.setUserData(f"{data_name}", "FF")
                
            _MSG: str = f"{node.name()}: {str(prm_mp.name()).upper()}: ON"
            self.set_status_msg(_MSG, 'IMP')
            self.flash_message(node, f"XF VIZ: FF")
                
            
    def flam3h_toggle(self, prm_name: str) -> None:
        """If a toggle is OFF it will switch ON, and viceversa.

        Args:
            (self):
            prm_name(str): Toggle parameter name to use.

        Returns:
            (None):  
        """
        node = self.node
        prm = node.parm(prm_name)
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm.eval():
            prm.set(0)
            _MSG: str = f"{node.name()}: {str(prm.name()).upper()}: OFF"
            self.set_status_msg(_MSG, 'MSG')
            
        else:
            prm.set(1)
            _MSG: str = f"{node.name()}: {str(prm.name()).upper()}: ON"
            self.set_status_msg(_MSG, 'IMP')
            
            
    def flam3h_toggle_private(self, prm_name: str) -> None:
        """If a toggle is OFF it will switch ON, and viceversa,
        and make sure to unlock and lock the parameter.

        Args:
            (self):
            prm_name(str): Toggle parameter name to use.

        Returns:
            (None):  
        """
        node = self.node
        prm = node.parm(prm_name)
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm.eval():
            self.private_prm_set(node, prm, 0)
            _MSG: str = f"{node.name()}: {str(prm.name()).upper()}: OFF"
            self.set_status_msg(_MSG, 'MSG')
            
        else:
            self.private_prm_set(node, prm, 1)
            _MSG: str = f"{node.name()}: {str(prm.name()).upper()}: ON"
            self.set_status_msg(_MSG, 'IMP')
            
            
    def flam3h_toggle_private_FF(self, prm_name: str = PREFS_PVT_DOFF) -> None:
        """If a toggle is OFF it will switch ON, and viceversa,
        and make sure to unlock and lock the parameter.
        Specifically built for the FF toggles ON/OFF

        Args:
            (self):
            prm_name(str): Toggle parameter name to use.

        Returns:
            (None):  
        """
        node = self.node
        prm = node.parm(prm_name)
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm.eval():
            self.private_prm_set(node, prm, 0)
            
            if node.parm(PREFS_PVT_XF_FF_VIZ_SOLO).eval():
                self.private_prm_set(node, PREFS_PVT_XF_FF_VIZ_SOLO, 0)
                data_name = f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}"
                flam3h_iterator_utils.destroy_userData(node, f"{data_name}")
                
            _MSG: str = f"{node.name()}: {str(prm.name()).upper()}: OFF"
            self.set_status_msg(_MSG, 'MSG')
            
        else:
            self.private_prm_set(node, prm, 1)
            _MSG: str = f"{node.name()}: {str(prm.name()).upper()}: ON"
            self.set_status_msg(_MSG, 'IMP')
            

    def flam3h_toggle_off(self, prm_name: str) -> None:
        """If a toggle is ON it will switch it OFF.

        Args:
            (self):
            prm_name(str): Toggle parameter name to use

        Returns:
            (None):  
        """      
        prm = self.node.parm(prm_name)  
        
        # Refresh menu caches
        self.menus_refresh_enum_prefs()
        
        if prm.eval():
            prm.set(0)
            # If the passed toggle's name argument is the camera sensor: 'outsensor'
            # restore the viewport prior to entering the Camera sensor mode and clearup all related data
            if prm == OUT_RENDER_PROPERTIES_SENSOR:
                self.util_set_stashed_cam()
                self.util_clear_stashed_cam_data()
                
                
    def flam3h_init_presets_CP_PRESETS(self, mode: int = 1, destroy_menus: bool = True, json_file: bool | None = None, f3h_json_file: bool | None = None, json_path_checked: str | bool | None = None) -> None:
        """Initialize parameter's menu presets for the CP tab.
        
        Here I could use userData instead of a cachedUserData but can happen that between one houdini session
        and the next one the user may make some modification to the stored file, like moving it into another location or deleting it
        so this way we make sure to always be up to date.
        
        _NOTE:
            This definition differ from the IN and OUT file init presets definitions,
            because it deal with the Loading and Saving data initializations in one place.
        
        Args:
            (self):
            mode(int): Default to: 1. This is to be used to prevent to load a left over preset when loading back a hip file.
            destroy(bool): Default to True. Destroy menu presets cached data. True or False.
            json_file(bool | None): Default to None. Is it a json file ?
            f3h_json_file(bool | None): Default to None. Is it a F3H palette json file ?
            
        Returns:
            (None):
        """    
        node = self.node
        # Clear menu cache
        if destroy_menus:
            flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node)
            flam3h_iterator_utils(self.kwargs).update_xml_last_loaded()
        
        # Retrieve the filepath from the history (preview valid F3H json file path used)
        cp_presets_filepath_history: str | None = node.cachedUserData('cp_presets_filepath')
        
        prm = node.parm(CP_PALETTE_PRESETS)
        prm_off = node.parm(CP_PALETTE_PRESETS_OFF)

        if json_path_checked is None:
            json_path: str = os.path.expandvars(node.parm(CP_PALETTE_LIB_PATH).eval())
            json_path_checked = out_flame_utils.out_check_outpath(node,  json_path, OUT_PALETTE_FILE_EXT, AUTO_NAME_CP)
        
        if cp_presets_filepath_history is not None and node.parm(CP_PVT_ISVALID_FILE).eval() and os.path.isfile(cp_presets_filepath_history) and cp_presets_filepath_history == json_path_checked:
            pass
        else:
            prm.set('-1')
            prm_off.set('-1')

        if json_path_checked is not False:
            assert isinstance(json_path_checked, str)
            
            # Set the CP filepath parameter to this checked and corrected filepath
            node.setParms({CP_PALETTE_LIB_PATH: json_path_checked})
            
            # Here we are checking the file path in the file path parameter field if asked to do so(args: "json_file" and "f3h_json_file" are None)
            if json_file is None and f3h_json_file is None: json_file, f3h_json_file = flam3h_palette_utils.isJSON_F3H(node, json_path)
            if json_file and f3h_json_file:
                
                # CP is valid file
                self.private_prm_set(node, CP_PVT_ISVALID_FILE, 1)
                # We store the file path only when we know it is a valid F3H json file path
                node.setCachedUserData('cp_presets_filepath', json_path_checked)
                
                # Only set when NOT on an: onLoaded python script
                if mode:
                    prm.set('0')
                    prm_off.set('0')
                    # Mark this as not a loaded preset
                    self.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
                    # check if the selected palette file is locked
                    if self.isLOCK(json_path_checked):
                        flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, MSG_PALETTE_MSG)
                        # Lets print to the status bar as well
                        _MSG: str = f"Palette: {MSG_PALETTE_MSG}"
                        flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG} -> {json_path_checked}", 'WARN')
                    else:
                        flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, "")
                
            else:
                # Here we are checking the corrected file path
                json_file, f3h_json_file = flam3h_palette_utils.isJSON_F3H(node, json_path_checked)
                if json_file and f3h_json_file:
                    
                    # Only set when NOT on an: onLoaded python script
                    if mode and json_path_checked != cp_presets_filepath_history:
                        
                        # CP is valid file
                        self.private_prm_set(node, CP_PVT_ISVALID_FILE, 1)
                        # We store the file path only when we know it is a valid F3H json file path
                        node.setCachedUserData('cp_presets_filepath', json_path_checked)
                        
                        prm.set('0')
                        prm_off.set('0')
                        # Mark this as not a loaded preset
                        self.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
                        # check if the selected palette file is locked
                        if self.isLOCK(json_path_checked):
                            flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, MSG_PALETTE_MSG)
                            # Lets print to the status bar as well
                            _MSG: str = f"Palette: {MSG_PALETTE_MSG}"
                            flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG} -> {json_path_checked}", 'WARN')
                        else:
                            flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, "")
                            
                else:
                    prm.set('-1')
                    prm_off.set('-1')
                    # CP not a valid file
                    self.private_prm_set(node, CP_PVT_ISVALID_FILE, 0)
                    flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, "")
                    # Mark this as not a loaded preset
                    self.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
                    # Clear cached data
                    flam3h_iterator_utils.destroy_cachedUserData(node, 'cp_presets_filepath')

        else:
            # CP not a valid file
            self.private_prm_set(node, CP_PVT_ISVALID_FILE, 0)
            flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, "")
            # Mark this as not a loaded preset
            self.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
            # Clear cached data
            flam3h_iterator_utils.destroy_cachedUserData(node, 'cp_presets_filepath')
            
            # We do not want to print if the file path parameter is empty
            # This became redundant since I added file checks during the presets menus build process but I leave it here for now.
            if not json_path:
                self.set_status_msg('', 'MSG')


    def flam3h_init_presets_IN_PRESETS(self, mode: int = 1) -> None:
        """Initialize parameter's menu presets for the IN tab.
        
        Here I could use userData instead of a cachedUserData but can happen that between one houdini session
        and the next one the user may make some modification to the stored file, like moving it into another location or deleting it
        so this way we make sure to always be up to date.
        
        Args:
            (self):
            mode(int): Default to: 1. This is to be used to prevent to load a left over preset when loading back a hip file.
            
        Returns:
            (None):
        """    
        node = self.node
        # Clear menu caches
        flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node)
        flam3h_iterator_utils(self.kwargs).update_xml_last_loaded()
        # Retrieve the filepath from the history (preview valid F3H json file path used)
        in_presets_filepath_history: str | None = node.cachedUserData('in_presets_filepath')
        
        is_valid: int = node.parm(IN_PVT_ISVALID_FILE).eval()
        clipboard: int = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()
        prm = node.parm(IN_PRESETS)
        prm_off = node.parm(IN_PRESETS_OFF)
        
        xml: str = os.path.expandvars(node.parm(IN_PATH).eval())
        xml_checked: str | bool = out_flame_utils.out_check_outpath(node,  xml, OUT_FLAM3_FILE_EXT, AUTO_NAME_OUT, False, False)
        
        if in_presets_filepath_history is not None and is_valid and os.path.isfile(in_presets_filepath_history) and in_presets_filepath_history == xml_checked:
            pass
        else:
            prm.set('-1')
            prm_off.set('-1')
        
        if xml_checked is not False:
            assert isinstance(xml_checked, str)
            
            # Set the CP filepath parameter to this checked and corrected filepath
            node.setParms({IN_PATH: xml_checked})
            
            # We are using the class: _xml_tree becasue we really need to carefully validate the loaded flame file.
            # This is important as all the toggles we are setting here will be used to speed up the population of the menu presets.
            # apo = _xml_tree(xml)
            if not _xml_tree(xml_checked).isvalidtree:
                
                if clipboard:
                    self.remove_locked_from_flame_stats(node)
                    self.private_prm_set(node, IN_PVT_ISVALID_FILE, 0)
                    
                else:
                    [self.private_prm_set(node, prm_name, 0) for prm_name in (IN_PVT_ISVALID_FILE, IN_PVT_ISVALID_PRESET, IN_PVT_CLIPBOARD_TOGGLE)]
                    [prm.set("") for prm in (node.parm(MSG_IN_FLAMESTATS), node.parm(MSG_IN_FLAMERENDER), node.parm(MSG_IN_FLAMESENSOR), node.parm(MSG_DESCRIPTIVE_PRM))]
                        
                # If it is not a chaotica xml file do print out from here,
                # other wise we are printing out from:
                # class: _xml_tree(...) @staticmethod -> xmlfile_root_chk(...)
                if not in_flame_utils.in_to_flam3h_is_CHAOS(xml):
                    _MSG: str = "IN: Nothing to load"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    flam3h_general_utils.flash_message(node, _MSG)
            else:
                # Only set when NOT on an: onLoaded python script
                if mode and xml_checked != in_presets_filepath_history:
                    
                    # IN is valid file
                    self.private_prm_set(node, IN_PVT_ISVALID_FILE, 1)
                    # We store the file path only when we know it is a valid Flame file path
                    node.setCachedUserData('in_presets_filepath', xml_checked)
                    
                    prm.set('0')
                    prm_off.set('0')
                    
                    # the IN_PVT_ISVALID_PRESET is set inside the following: in_flame_utils(self.kwargs).in_to_flam3h()
                    in_flame_utils(self.kwargs).in_to_flam3h()
                    
                # Only set when NOT on an: onLoaded python script
                elif mode and not is_valid:
                        
                    # IN is valid file
                    self.private_prm_set(node, IN_PVT_ISVALID_FILE, 1)
                    # We store the file path only when we know it is a valid Flame file path
                    node.setCachedUserData('in_presets_filepath', xml_checked)
                    
                    prm.set('0')
                    prm_off.set('0')
                    
                    # the IN_PVT_ISVALID_PRESET is set inside the following: in_flame_utils(self.kwargs).in_to_flam3h()
                    in_flame_utils(self.kwargs).in_to_flam3h()
                    
        else:
            # If there is not a flame preset loaded from the clipboard
            if not clipboard:
                [self.private_prm_set(node, prm_name, 0) for prm_name in (IN_PVT_ISVALID_FILE, IN_PVT_ISVALID_PRESET, IN_PVT_CLIPBOARD_TOGGLE)]
                [prm.set("") for prm in (node.parm(MSG_IN_FLAMESTATS), node.parm(MSG_IN_FLAMERENDER), node.parm(MSG_IN_FLAMESENSOR), node.parm(MSG_DESCRIPTIVE_PRM))]
                
                # We do not want to print if the file path parameter is empty
                # This became redundant since I added file checks during the presets menus build process but I leave it here for now.
                # if xml:
                #     print(f'{node.name()}.IN: please select a valid file location.')
            else:
                self.remove_locked_from_flame_stats(node)
                # Otherwise just mark the absence of a valid file and leave everything else untouched
                self.private_prm_set(node, IN_PVT_ISVALID_FILE, 0)


    def flam3h_init_presets_OUT_PRESETS(self, destroy_menus: bool = True) -> None:
        """Initialize parameter's menu presets for the OUT tab.
        
        _NOTE:
            This need a little update at some point.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        node = self.node
        # Clear menu caches
        if destroy_menus:
            flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node)
            flam3h_iterator_utils(self.kwargs).update_xml_last_loaded()
        # Retrieve the filepath from the history (preview valid F3H json file path used)
        out_presets_filepath_history: str | None = node.cachedUserData('out_presets_filepath')
        
        is_valid: int = node.parm(OUT_PVT_ISVALID_FILE).eval()
        prm = node.parm(OUT_PRESETS)
        prm_sys = node.parm(OUT_SYS_PRESETS)
        
        xml: str = os.path.expandvars(node.parm(OUT_PATH).eval())
        xml_checked: str | bool = out_flame_utils.out_check_outpath(node, xml, OUT_FLAM3_FILE_EXT, AUTO_NAME_OUT)
        
        if out_presets_filepath_history is not None and is_valid and os.path.isfile(out_presets_filepath_history) and out_presets_filepath_history == xml_checked:
            pass
        else:
            prm.set('-1')
            prm_sys.set('-1')
        
        if xml_checked is not False:
            assert isinstance(xml_checked, str)
            
            # Set the IN filepath parameter to this checked and corrected filepath
            node.setParms({OUT_PATH: xml_checked})
            
            apo = _xml_tree(xml_checked) #type: ignore
            if apo.isvalidtree:
                
                if xml_checked != out_presets_filepath_history:
                    
                    # We store the file path only when we know it is a valid Flame file path
                    node.setCachedUserData('out_presets_filepath', xml_checked)
                    
                    prm.set(f'{len(apo.name)-1}')
                    prm_sys.set(f'{len(apo.name)-1}')
                    # check if the selected Flame file is locked
                    if self.isLOCK(xml_checked):
                        node.setParms({MSG_OUT: MSG_OUT_MSG})
                        # Lets print to the status bar as well
                        _MSG: str = f"OUT: {MSG_OUT_MSG}"
                        flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG} -> {xml_checked}", 'WARN')
                    else:
                        node.setParms({MSG_OUT: ''})
                        
                    flam3h_general_utils.private_prm_set(node, OUT_PVT_ISVALID_FILE, 1)
                
            else:
                flam3h_iterator_utils.destroy_cachedUserData(node, 'out_presets_filepath')
                
                prm.set('-1')
                prm_sys.set('-1')
                node.setParms({MSG_OUT: ''})
                flam3h_general_utils.private_prm_set(node, OUT_PVT_ISVALID_FILE, 0)
                
        else:
            flam3h_iterator_utils.destroy_cachedUserData(node, 'out_presets_filepath')
            
            node.setParms({MSG_OUT: ''})
            flam3h_general_utils.private_prm_set(node, OUT_PVT_ISVALID_FILE, 0)
            # We do not want to print if the file path parameter is empty
            # This became redundant since I added file checks during the presets menus build process but I leave it here for now.
            # if xml:
            #     print(f'{node.name()}.OUT: please select a valid file location.')


    def flam3h_display_help(self) -> None:
        """Open the Houdini help browser to display the FLAM3H node documentation.

        Args:
            (self):
            
        Returns:
            (None):
        """
        hou.ui.displayNodeHelp(self.node.type()) # type: ignore


    def util_store_all_viewers_color_scheme(self) -> None:
        """Store dictionaries of viewers color schemes
        
        Args:
            (self):
            
        Returns:
            (None):  
        """  
        # Do this only if the parameter toggle is: PREFS_VIEWPORT_DARK
        try: parm = self.kwargs['parm']
        except: parm = None
        _ENTER_PRM = None
        if parm is not None: _ENTER_PRM = parm.name()
        if _ENTER_PRM is not None and _ENTER_PRM == PREFS_VIEWPORT_DARK:
            views_scheme: list[hou.viewportColorScheme]  = []
            views_keys: list[str] = []
            for v in self.util_getSceneViewers():
                
                # Store only if it is a Sop viewer
                if flam3h_general_utils.util_is_context('Sop', v):
                    
                    view: hou.GeometryViewport = v.curViewport()
                    settings: hou.GeometryViewportSettings = view.settings()
                    _CS: hou.viewportColorScheme = settings.colorScheme()
                    if _CS != hou.viewportColorScheme.Dark: # type: ignore
                        views_scheme.append(_CS)
                        views_keys.append(v.name())
            
            # Always store and update this data
            hou.session.H_CS_STASH_DICT: dict[str, hou.viewportColorScheme] = dict(zip(views_keys, views_scheme)) # type: ignore


    def colorSchemeDark(self, update_others: bool = True) -> None:
        """Change viewport color scheme to dark
        and remember the current color scheme so to switch back to it when unchecked.
        If the viewport color scheme is already dark, checking this option will do nothing. 
        
        Args:
            (self):
            update_others(bool): Default to True. Update also the other FLAM3H nodes in the scene if any
            
        Returns:
            (None):
        """
        node = self.node
        prm = node.parm(PREFS_VIEWPORT_DARK)
        views: list = self.util_getSceneViewers()
        
        if views:
            if prm.eval():
                # Store all viewers current color schemes
                # if different than Dark
                self.util_store_all_viewers_color_scheme()
                
                dark: bool = False
                sop_view: bool = False
                
                for v in views:
                    
                    # Set only if it is a Sop viewer
                    if flam3h_general_utils.util_is_context('Sop', v):
                        
                        if sop_view is False: sop_view = True
                        
                        settings: hou.GeometryViewportSettings = v.curViewport().settings()
                        _CS: hou.viewportColorScheme = settings.colorScheme()
                        if _CS != hou.viewportColorScheme.Dark: # type: ignore
                            settings.setColorScheme(hou.viewportColorScheme.Dark) # type: ignore
                            dark = True
                
                if sop_view:
                    
                    if dark:   
                        _MSG: str = f"Dark: ON"
                        self.flash_message(node, _MSG)
                        self.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                    else:
                        _MSG: str = f"Dark already"
                        self.set_status_msg(f"{node.name()}: {_MSG}. Viewers are in Dark mode already", 'MSG')
                        
                else:
                    prm.set(0)
                    
                    if not hou.hipFile.isLoadingHipFile(): # type: ignore
                        _MSG: str = f"No Sop viewers available."
                        self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Sop viewer to either set to Dark or restore.", 'WARN')
                        self.flash_message(node, f"{_MSG}")
                    
            else:
                
                try: _STASH_DICT: dict[str, hou.EnumValue] | None = hou.session.H_CS_STASH_DICT # type: ignore
                except: _STASH_DICT: dict[str, hou.EnumValue] | None = None
                    
                dark = False
                if _STASH_DICT is not None:
                    for v in views:
                        # Here we are not checking if the viewer belong to Sop or Lop
                        # because the stashed dict has already the viewers filtered on creation inside: flam3h_general_utils.util_store_all_viewers_color_scheme()
                        key: str = v.name()
                        _STASH: hou.EnumValue | None = _STASH_DICT.get(key)
                        if _STASH is not None:
                            settings: hou.GeometryViewportSettings = v.curViewport().settings()
                            _CS: hou.viewportColorScheme = settings.colorScheme()
                            if _CS == hou.viewportColorScheme.Dark: # type: ignore
                                settings.setColorScheme(_STASH)
                                dark = True
                                
                if dark:
                    _MSG: str = f"Dark: OFF"
                    self.flash_message(node, _MSG)
                    self.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    
                else:
                    
                    try:
                        
                        if hou.session.H_CS_STASH_DICT: # type: ignore
                            _MSG = f"No viewer in Dark mode"
                            self.set_status_msg(f"{node.name()}: {_MSG}. None of the current viewers are set to Dark.", 'MSG')
                        else:
                            _MSG = f"Nothing to restore"
                            self.set_status_msg(f"{node.name()}: {_MSG}. None of the current viewers has been switched to Dark. They probably were already in Dark mode.", 'MSG')
                            
                    except AttributeError:
                        pass
                            
        else:
            prm.set(0)
            
            if not hou.hipFile.isLoadingHipFile(): # type: ignore
                _MSG: str = f"No Sop viewers available."
                self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Sop viewer to either set to Dark or restore.", 'WARN')
                self.flash_message(node, f"{_MSG}")
            
        if update_others:
            # Update dark preference's option toggle on other FLAM3H nodes instances
            all_f3h: tuple = self.node.type().instances()
            if len(all_f3h) > 1:
                [f3h.setParms({PREFS_VIEWPORT_DARK: prm.eval()}) for f3h in all_f3h if f3h != node if f3h.parm(PREFS_VIEWPORT_DARK).eval() != prm.eval()]
        

    def viewportParticleDisplay(self) -> None:
        """Switch viewport particle display mode
        between Pixel and Points.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        pttype: int = node.parm(PREFS_VIEWPORT_PT_TYPE).evalAsInt()

        Points: hou.EnumValue = hou.viewportParticleDisplay.Points # type: ignore
        Pixels: hou.EnumValue = hou.viewportParticleDisplay.Pixels # type: ignore

        for view in self.util_getSceneViewers():
            
            # Set only if it is a Sop viewer
            if self.util_is_context('Sop', view):
            
                settings: hou.GeometryViewportSettings = view.curViewport().settings()
                if pttype == 0:
                    settings.particleDisplayType(Points)
                    self.viewportParticleSize()
                elif pttype == 1:
                    settings.particleDisplayType(Pixels)
                
        # Update Point Display type preference's option toggle on other FLAM3H nodes instances
        all_f3h: tuple = self.node.type().instances()
        if len(all_f3h) > 1:
            [f3h.parm(PREFS_VIEWPORT_PT_TYPE).deleteAllKeyframes() for f3h in node.type().instances()]
            [f3h.setParms({PREFS_VIEWPORT_PT_TYPE: pttype}) for f3h in all_f3h if f3h != node if f3h.parm(PREFS_VIEWPORT_PT_TYPE).eval() != pttype]
            
        # This here for now because I still need to update the instances
        if self.util_is_context_available_viewer('Sop') is False:
            _MSG: str = f"No Sop viewers available."
            self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Sop viewer for this option to work.", 'WARN')
            self.flash_message(node, f"{_MSG}")
    
    
    def viewportParticleSize(self, reset_val: float | None = None) -> None:
        """When the viewport particle display type is set to Point
        this will change their viewport size.
        
        Args:
            (self):
            reset_val (float | None): Default to None. Can be either "None" or a float value. If "None" it will use the current parameter value, otherwise it will use the one passed in this function.
            
        Returns:
            (None):
        """
        node = self.node
        Points: hou.EnumValue = hou.viewportParticleDisplay.Points # type: ignore
        ptsize: float = node.parm(PREFS_VIEWPORT_PT_SIZE).evalAsFloat()

        for view in self.util_getSceneViewers():
            
            # Set only if it is a Sop viewer
            if self.util_is_context('Sop', view):
            
                settings: hou.GeometryViewportSettings = view.curViewport().settings()
                settings.particleDisplayType(Points)
                if reset_val is None:
                    settings.particlePointSize(ptsize)
                else:
                    ptsize = float(reset_val)
                    settings.particlePointSize(ptsize)
                    prm = node.parm(self.kwargs['parmtuple'].name())
                    prm.deleteAllKeyframes()
                    prm.set(ptsize)
            
        # Update Point Size preference's option toggle on other FLAM3H nodes instances
        if node.parm(PREFS_VIEWPORT_PT_TYPE).evalAsInt() == 0:
            [f3h.parm(PREFS_VIEWPORT_PT_SIZE).deleteAllKeyframes() for f3h in node.type().instances()]
            [f3h.setParms({PREFS_VIEWPORT_PT_SIZE: ptsize}) for f3h in node.type().instances() if f3h.parm(PREFS_VIEWPORT_PT_SIZE).eval() != ptsize]

        # This here for now because I still need to update the instances
        if self.util_is_context_available_viewer('Sop') is False:
            _MSG: str = f"No Sop viewers available."
            self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Sop viewer for this option to work.", 'WARN')
            self.flash_message(node, f"{_MSG}")
            

    def viewportWireWidth(self, reset_val: float | None = None) -> None:
        """When the viewport handle VIZ is ON
        this will change their viewport setting wire width value.
        
        Args:
            (self):
            reset_val (float | None): Default to None. Can be either "None" or a float value. If "None" it will use the current parameter value, otherwise it will use the one passed in this function.
            
        Returns:
            (None):
        """
        node = self.node
        width: float = node.parm(PREFS_VIEWPORT_WIRE_WIDTH).evalAsFloat()

        for view in self.util_getSceneViewers():
            
            # Set only if it is a Sop viewer
            if self.util_is_context('Sop', view):
                
                settings: hou.GeometryViewportSettings = view.curViewport().settings()
                if reset_val is None:
                    settings.wireWidth(width)
                else:
                    width = float(reset_val)
                    settings.wireWidth(width)
                    prm = node.parm(PREFS_VIEWPORT_WIRE_WIDTH)
                    prm.deleteAllKeyframes()
                    prm.set(width)
            
        # Updated FLAM3H wire width custom value
        hou.session.FLAM3H_VIEWPORT_WIRE_WIDTH: float = width # type: ignore
        
        # Update wire width preference's option toggle on other FLAM3H nodes instances
        [f3h.parm(PREFS_VIEWPORT_WIRE_WIDTH).deleteAllKeyframes() for f3h in node.type().instances()]
        [f3h.setParms({PREFS_VIEWPORT_WIRE_WIDTH: width}) for f3h in node.type().instances() if f3h.parm(PREFS_VIEWPORT_WIRE_WIDTH).eval() != width]
    
        # This here for now because I still need to update the instances
        if self.util_is_context_available_viewer('Sop') is False:
            _MSG: str = f"No Sop viewers available."
            self.set_status_msg(f"{node.name()}: {_MSG} You need at least one Sop viewer for this option to work.", 'WARN')
            self.flash_message(node, f"{_MSG}")
            
    
    def reset_SYS(self, density: int, iter: int, mode: int) -> None:
        """Reset the FLAM3H SYS Tab parameters.
        
        Args:
            (self):
            density(int): Numper of points to use
            iter(int): Number of iterations
            mode(int): 0: skip "doff" 1: reset "doff"
            
        Returns:
            (None):
        """    
        node = self.node
        node.setParms({GLB_DENSITY: density})
        node.setParms({GLB_DENSITY_PRESETS: 1})
        node.setParms({GLB_ITERATIONS: iter})
        
        if mode:
            self.private_prm_set(node, PREFS_PVT_DOFF, 0)
            
        node.setParms({SYS_TAG_SIZE: 0})
        self.private_prm_set(node, PREFS_PVT_TAG, 0)
        self.private_prm_set(node, PREFS_PVT_RIP, 0)
        

    def reset_MB(self) -> None:
        """Reset the FLAM3H MB Tab parameters.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        _MB: dict[str, int | float] = {MB_DO: 0,
                                             MB_FPS: 24,
                                             MB_SAMPLES: 16,
                                             MB_SHUTTER: 0.5,
                                             MB_VIZ: 0}
        [node.setParms({key: value}) for key, value in _MB.items()]


    def reset_PREFS(self, mode: int = 0) -> None:
        """Reset the FLAM3H PREFS Tab parameters.

        Args:
            (self):
            mode(int): Defaults to 0. If set to 1, it will activate the flam3 compatibility option.
            
        Returns:
            (None):
        """
        node = self.node
        node.setParms({PREFS_XAOS_MODE: 0})
        node.setParms({PREFS_CAMERA_HANDLE: 0})
        node.setParms({PREFS_CAMERA_CULL: 0})
        node.setParms({PREFS_CAMERA: ""})
        node.setParms({PREFS_CAMERA_CULL_AMOUNT: 0.99})
        
        # XF VIZ SOLO OFF (but leave the xforms handles VIZ ON)
        self.private_prm_set(node, PREFS_PVT_XF_VIZ_SOLO, 0)
        self.private_prm_set(node, PREFS_PVT_XF_FF_VIZ_SOLO, 0)
        flam3h_iterator_utils.destroy_userData(node, f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}")
        
        if mode:
            self.private_prm_set(node, PREFS_PVT_F3C, 1)


# FLAM3H ITERATOR start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################

# ICONS menu copy/paste bookmarks
FLAM3H_ICON_COPY_PASTE = '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteSVG.svg]'
FLAM3H_ICON_COPY_PASTE_ENTRIE = '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteEntrieSVG.svg]'
FLAM3H_ICON_COPY_PASTE_ENTRIE_ZERO = '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteZeroWSVG.svg]'
FLAM3H_ICON_COPY_PASTE_INFO = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]'
FLAM3H_ICON_COPY_PASTE_INFO_ORANGE = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]'
FLAM3H_ICON_COPY_PASTE_FF = '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteFFSVG.svg]'
FLAM3H_ICON_COPY_PASTE_FF_ENTRIE = '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteEntrieFFSVG.svg]'
FLAM3H_ICON_COPY_PASTE_FF_ENTRIE_OFF = '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteEntrieFFOffSVG.svg]'
# ICONS menu select/iterator
FLAM3H_ICON_COPY_PASTE_ENTRIE_ITER_OFF_MARKED = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledSelIterSVG.svg]'

# ICONS menu vars and palette bookmarks
FLAM3H_ICON_STAR_EMPTY = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledSVG.svg]'
FLAM3H_ICON_STAR_EMPTY_OPACITY = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]'
FLAM3H_ICON_STAR_FLAME_LOAD = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionFlameINEntrieSVG.svg]'
FLAM3H_ICON_STAR_FLAME_LOAD_CB = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg]'
FLAM3H_ICON_STAR_FLAME_LOAD_EMPTY = '![opdef:/alexnardini::Sop/FLAM3H?icon_WhiteSVG_disabled.svg]'
FLAM3H_ICON_STAR_FLAME_SAVE = '![opdef:/alexnardini::Sop/FLAM3H?icon_WhiteStarSVG.svg]'
FLAM3H_ICON_STAR_FLAME_SAVE_ENTRIE = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionFlameOUTEntrieSVG.svg]'
FLAM3H_ICON_STAR_PALETTE_LOAD = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionCPSVG.svg]'
FLAM3H_ICON_STAR_PALETTE_LOAD_EMPTY = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionPRIDEDisabledSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_ACTV = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_ACTV_OVER_ONE = '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_ACTV_NEGATIVE = '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhitePBSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV_OVER_ONE = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhitePBHSVG.svg]'
FLAM3H_ICON_STAR_FLAME_ITER_ACTV = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarYellowOrangeSVG.svg]'
# High tier menu entrie
FLAM3H_ICON_STAR_HIGH_TIER = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]'
# Menu select iterator - Prep icons (unmarked, marked)
SEL_ITER_BOOKMARK_ACTIVE_AND_WEIGHT: tuple = (FLAM3H_ICON_STAR_FLAME_ITER_ACTV, FLAM3H_ICON_COPY_PASTE)
SEL_ITER_BOOKMARK_ACTIVE_AND_WEIGHT_ZERO: tuple = (FLAM3H_ICON_STAR_EMPTY_OPACITY, FLAM3H_ICON_COPY_PASTE_ENTRIE_ZERO)
SEL_ITER_BOOKMARK_OFF: tuple = (FLAM3H_ICON_STAR_EMPTY, FLAM3H_ICON_COPY_PASTE_ENTRIE_ITER_OFF_MARKED)

# The following are pre built to speed up the generations of the menus.
MENU_ZERO_ITERATORS: list = [0, "![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]  ZERO ITERATORS\n -> Please, create at least one iterator or load an IN flame file first.", 1, ""]
MENU_VARS_ALL: list = [(0, 'Linear'), (39, 'Arch'), (94, 'Auger...'), (14, 'Bent'), (52, 'Bent2...'), (53, 'Bipolar...'), (43, 'Blade'), (30, 'Blob...'), (26, 'Blur'), (54, 'Boarders'), (23, 'Bubble'), (55, 'Butterfly'), (99, 'Bwraps...'), (56, 'Cell...'), (50, 'Conic...'), (83, 'Cos'), (89, 'Cosh'), (20, 'Cosine'), (87, 'Cot'), (93, 'Coth'), (57, 'Cpow...'), (102, 'Crop...'), (46, 'Cross'), (86, 'Csc'), (92, 'Csch'), (27, 'Curl...'), (97, 'Curve...'), (24, 'Cylinder'), (11, 'Diamond'), (8, 'Disc'), (47, 'Disc2...'), (58, 'Edisc'), (59, 'Elliptic'), (61, 'Escher...'), (12, 'Ex'), (80, 'Exp'), (18, 'Exponential'), (25, 'Eyefish'), (22, 'Fan*'), (34, 'Fan2...'), (16, 'Fisheye'), (49, 'Flower...'), (95, 'Flux...'), (62, 'Foci'), (33, 'Gaussian_blur'), (104, 'Glynnia'), (6, 'Handkerchief'), (7, 'Heart'), (100, 'Hemisphere'), (4, 'Horseshoe'), (10, 'Hyperbolic'), (13, 'Julia'), (31, 'JuliaN...'), (32, 'Juliascope...'), (63, 'Lazysusan...'), (81, 'Log'), (64, 'Loonie'), (96, 'Mobius...'), (66, 'Modulus...'), (28, 'Ngon...'), (60, 'Noise'), (67, 'Oscope...'), (51, 'Parabola...'), (29, 'Pdj...'), (98, 'Perspective...'), (38, 'Pie...'), (5, 'Polar'), (68, 'Polar2'), (101, 'Polynomial...'), (17, 'Popcorn*'), (69, 'Popcorn2...'), (19, 'Power'), (105, 'Pt_symmetry...'), (37, 'Radialblur...'), (42, 'Rays'), (36, 'Rectangles...'), (21, 'Rings*'), (35, 'Rings2...'), (70, 'Scry'), (85, 'Sec'), (44, 'Secant2'), (91, 'Sech'), (71, 'Separation...'), (82, 'Sin'), (88, 'Sinh'), (1, 'Sinusoidal'), (2, 'Spherical'), (9, 'Spiral'), (72, 'Split...'), (73, 'Splits...'), (41, 'Square'), (74, 'Stripes...'), (48, 'Supershape...'), (3, 'Swirl'), (84, 'Tan'), (40, 'Tangent'), (90, 'Tanh'), (45, 'Twintrian'), (103, 'Unpolar'), (15, 'Waves*'), (79, 'Waves2...'), (75, 'Wedge...'), (76, 'Wedgejulia...'), (77, 'Wedgesph...'), (78, 'Whorl...')]
MENU_VARS_ALL_SIMPLE: list = [0, 'Linear          ', 39, 'Arch          ', 94, 'Auger...          ', 14, 'Bent          ', 52, 'Bent2...          ', 53, 'Bipolar...          ', 43, 'Blade          ', 30, 'Blob...          ', 26, 'Blur          ', 54, 'Boarders          ', 23, 'Bubble          ', 55, 'Butterfly          ', 99, 'Bwraps...          ', 56, 'Cell...          ', 50, 'Conic...          ', 83, 'Cos          ', 89, 'Cosh          ', 20, 'Cosine          ', 87, 'Cot          ', 93, 'Coth          ', 57, 'Cpow...          ', 102, 'Crop...          ', 46, 'Cross          ', 86, 'Csc          ', 92, 'Csch          ', 27, 'Curl...          ', 97, 'Curve...          ', 24, 'Cylinder          ', 11, 'Diamond          ', 8, 'Disc          ', 47, 'Disc2...          ', 58, 'Edisc          ', 59, 'Elliptic          ', 61, 'Escher...          ', 12, 'Ex          ', 80, 'Exp          ', 18, 'Exponential          ', 25, 'Eyefish          ', 22, 'Fan*          ', 34, 'Fan2...          ', 16, 'Fisheye          ', 49, 'Flower...          ', 95, 'Flux...          ', 62, 'Foci          ', 33, 'Gaussian_blur          ', 104, 'Glynnia          ', 6, 'Handkerchief          ', 7, 'Heart          ', 100, 'Hemisphere          ', 4, 'Horseshoe          ', 10, 'Hyperbolic          ', 13, 'Julia          ', 31, 'JuliaN...          ', 32, 'Juliascope...          ', 63, 'Lazysusan...          ', 81, 'Log          ', 64, 'Loonie          ', 96, 'Mobius...          ', 66, 'Modulus...          ', 28, 'Ngon...          ', 60, 'Noise          ', 67, 'Oscope...          ', 51, 'Parabola...          ', 29, 'Pdj...          ', 98, 'Perspective...          ', 38, 'Pie...          ', 5, 'Polar          ', 68, 'Polar2          ', 101, 'Polynomial...          ', 17, 'Popcorn*          ', 69, 'Popcorn2...          ', 19, 'Power          ', 105, 'Pt_symmetry...          ', 37, 'Radialblur...          ', 42, 'Rays          ', 36, 'Rectangles...          ', 21, 'Rings*          ', 35, 'Rings2...          ', 70, 'Scry          ', 85, 'Sec          ', 44, 'Secant2          ', 91, 'Sech          ', 71, 'Separation...          ', 82, 'Sin          ', 88, 'Sinh          ', 1, 'Sinusoidal          ', 2, 'Spherical          ', 9, 'Spiral          ', 72, 'Split...          ', 73, 'Splits...          ', 41, 'Square          ', 74, 'Stripes...          ', 48, 'Supershape...          ', 3, 'Swirl          ', 84, 'Tan          ', 40, 'Tangent          ', 90, 'Tanh          ', 45, 'Twintrian          ', 103, 'Unpolar          ', 15, 'Waves*          ', 79, 'Waves2...          ', 75, 'Wedge...          ', 76, 'Wedgejulia...          ', 77, 'Wedgesph...          ', 78, 'Whorl...          ']
MENU_DENSITY: list = [-1, '', 1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg]...', 2, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]1M', 3, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]2M', 4, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]5M', 5, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]15M', 6, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]25M', 7, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]50M', 8, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]100M', 9, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]150M', 10, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]250M', 11, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]500M', 12, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]750M', 13, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1 Billion', 14, '']
MENU_DENSITY_XFVIZ_OFF: list = [-1, '', 1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteXFVIZOFFSVG.svg]...', 2, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZOFFSVG.svg]1M', 3, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZOFFSVG.svg]2M', 4, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZOFFSVG.svg]5M', 5, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]15M', 6, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]25M', 7, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]50M', 8, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]100M', 9, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]150M', 10, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]250M', 11, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]500M', 12, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]750M', 13, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1 Billion', 14, '']
MENU_DENSITY_XFVIZ_ON: list = [-1, '', 1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteXFVIZSVG.svg]...', 2, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSVG.svg]1M', 3, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSVG.svg]2M', 4, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSVG.svg]5M', 5, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]15M', 6, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]25M', 7, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]50M', 8, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]100M', 9, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]150M', 10, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]250M', 11, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]500M', 12, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]750M', 13, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1 Billion', 14, '']
MENU_DENSITY_XFVIZ_ON_SOLO: list = [-1, '', 1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteXFVIZSOLOSVG.svg]...', 2, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSOLOSVG.svg]1M', 3, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSOLOSVG.svg]2M', 4, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallXFVIZSOLOSVG.svg]5M', 5, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapCyanSmallSVG.svg]15M', 6, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]25M', 7, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]50M', 8, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]100M', 9, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]150M', 10, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledMidSVG.svg]250M', 11, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]500M', 12, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]750M', 13, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1 Billion', 14, '']
# This is now handled from inside Houdini # MENU_DENSITY_OFF: list = [0, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]...', 1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]1 Billion']
MENU_PRESETS_EMPTY: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]  Empty     ']
MENU_PRESETS_EMPTY_HIDDEN: list = [-1, '  Empty     ']
MENU_PRESETS_SAVEONE: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]  Save to create this file     ']
MENU_ZERO_ITERATORS_PRESETS_INVALID: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  ZERO ITERATORS\n -> Invalid file path. Please, create at least one iterator or load a valid IN flame file first.']
MENU_PRESETS_INVALID: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  Invalid file path     ']
MENU_PRESETS_INVALID_CB: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  [CLIPBOARD] Invalid file path     ']
MENU_IN_PRESETS_EMPTY_CB: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg]  [CLIPBOARD]     ']
MENU_ITER_COPY_PASTE_EMPTY: list = [0, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteSVG.svg]  Please, mark an iterator first.', 1, '']
MENU_ITER_COPY_PASTE_REMOVED: list = [0, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  REMOVED: The marked iterator has been removed.\n-> Mark an existing iterator instead.', 1, '']
MENU_ITER_COPY_PASTE_DELETED_MARKED: list = [ 0, "![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]  DELETED: Marked iterator's node has been deleted.\n-> Mark another iterator first.", 1, "" ]
MENU_FF_COPY_PASTE_EMPTY: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_StarSwapRedCopyPasteFFSVG.svg]  Please, mark the FF first.', 0, '']
MENU_FF_COPY_PASTE_SELECT: list = [0, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]  FF: MARKED\n-> Select a different FLAM3H node to paste those FF values.', 1, '']

# flam3h_varsPRM().build_menu_vars_indexes() for: MENU_VARS_ALL_SIMPLE
MENU_VARS_INDEXES: dict[int, int] = {   0: 1, 
                                        39: 3, 
                                        94: 5, 
                                        14: 7, 
                                        52: 9, 
                                        53: 11, 
                                        43: 13, 
                                        30: 15, 
                                        26: 17, 
                                        54: 19, 
                                        23: 21, 
                                        55: 23, 
                                        99: 25, 
                                        56: 27, 
                                        50: 29, 
                                        83: 31, 
                                        89: 33, 
                                        20: 35, 
                                        87: 37, 
                                        93: 39, 
                                        57: 41, 
                                        102: 43, 
                                        46: 45, 
                                        86: 47, 
                                        92: 49, 
                                        27: 51, 
                                        97: 53, 
                                        24: 55, 
                                        11: 57, 
                                        8: 59, 
                                        47: 61, 
                                        58: 63, 
                                        59: 65, 
                                        61: 67, 
                                        12: 69, 
                                        80: 71, 
                                        18: 73, 
                                        25: 75, 
                                        22: 77, 
                                        34: 79, 
                                        16: 81, 
                                        49: 83, 
                                        95: 85, 
                                        62: 87, 
                                        33: 89, 
                                        104: 91, 
                                        6: 93, 
                                        7: 95, 
                                        100: 97, 
                                        4: 99, 
                                        10: 101, 
                                        13: 103, 
                                        31: 105, 
                                        32: 107, 
                                        63: 109, 
                                        81: 111, 
                                        64: 113, 
                                        96: 115, 
                                        66: 117, 
                                        28: 119, 
                                        60: 121, 
                                        67: 123, 
                                        51: 125, 
                                        29: 127, 
                                        98: 129, 
                                        38: 131, 
                                        5: 133, 
                                        68: 135, 
                                        101: 137, 
                                        17: 139, 
                                        69: 141, 
                                        19: 143, 
                                        105: 145, 
                                        37: 147, 
                                        42: 149, 
                                        36: 151, 
                                        21: 153, 
                                        35: 155, 
                                        70: 157, 
                                        85: 159, 
                                        44: 161, 
                                        91: 163, 
                                        71: 165, 
                                        82: 167, 
                                        88: 169, 
                                        1: 171, 
                                        2: 173, 
                                        9: 175, 
                                        72: 177, 
                                        73: 179, 
                                        41: 181, 
                                        74: 183, 
                                        48: 185, 
                                        3: 187, 
                                        84: 189, 
                                        40: 191, 
                                        90: 193, 
                                        45: 195, 
                                        103: 197, 
                                        15: 199, 
                                        79: 201, 
                                        75: 203, 
                                        76: 205, 
                                        77: 207, 
                                        78: 209
                                        }


class flam3h_iterator_utils:
    """
class flam3h_iterator_utils

@STATICMETHODS
* flam3h_iterator_is_default_name(name: str, regex: str = "^[^\d\s()]+(?: [^\d\s()]+)*[\d]+") -> bool:
* flam3h_on_loaded_set_density_menu(node: hou.SopNode) -> None:
* sierpinski_settings(node: hou.SopNode) -> None:
* get_user_data(node: hou.SopNode, data_name: str = FLAM3H_USER_DATA_ITER) -> int | bool:
* exist_user_data(node: hou.SopNode, data: str = FLAM3H_USER_DATA_ITER) -> bool:
* set_comment_and_user_data_iterator(node: hou.SopNode, value: str, data: str = FLAM3H_USER_DATA_ITER) -> None:
* del_comment_and_user_data_iterator(node: hou.SopNode, data: str = FLAM3H_USER_DATA_ITER) -> None:
* flam3h_init_hou_session_iterator_data(node: hou.SopNode) -> None:
* flam3h_init_hou_session_ff_data(node: hou.SopNode) -> None:
* flam3h_init_hou_session_restore_from_user_data(node: hou.SopNode) -> None:
* iterator_mpidx_mem_set(node, data: int) -> None:
* paste_from_prm(prm_from: hou.Parm, prm_to: hou.Parm, pvt: bool = False) -> None:
* paste_from_list(node: hou.SopNode, flam3node: hou.SopNode | None, prm_list: tuple, id: str, id_from: str) -> None:
* is_iterator_affine_default(node: hou.SopNode, from_FLAM3H_NODE: hou.SopNode, prm_list_affine: tuple, id: str, id_from: str, post: bool = False) -> bool:
* is_FF_affine_default(node: hou.SopNode, from_FLAM3H_NODE: hou.SopNode, prm_list_affine: tuple, post: bool = False) -> bool:
* paste_from_list_affine(node: hou.SopNode, prm_list_affine_to: tuple, prm_list_affine_from: tuple, id: str) -> None:
* pastePRM_T_from_list(node: hou.SopNode, flam3node: hou.SopNode | None, prmT_list: tuple, varsPRM: tuple, id: str, id_from: str) -> None:
* paste_save_note(_note: str) -> str:
* paste_set_note(node: hou.SopNode, flam3node: hou.SopNode | None, int_mode: int, str_section: str, id: str, id_from: str) -> None:
* auto_set_xaos_data_get_MP_MEM(node: hou.SopNode) -> list | None:
* auto_set_xaos_data_get_XAOS_PREV(node: hou.SopNode) -> list | None:
* auto_set_xaos_data_set_MP_MEM(node: hou.SopNode, data: list | tuple) -> None:
* auto_set_xaos_data_set_XAOS_PREV(node: hou.SopNode, data: list | tuple) -> None:
* flam3h_on_load_opacity_zero(node: hou.SopNode, f3h_all: bool = False) -> None:
* destroy_cachedUserData(node, data: str, must_exist: bool = False) -> None:
* destroy_cachedUserData_all_f3h(node, data_name: str) -> None:
* destroy_userData(node, data: str, must_exist: bool = False) -> None:
* force_menu_var_update_FF(node: hou.SopNode) -> None:
* menu_T_get_type_icon(w: float) -> str:
* menu_T_PP_get_type_icon(w: float) -> str:

@METHODS
* iterator_affine_scale(self) -> None:
* iterator_post_affine_scale(self) -> None:
* iterator_FF_affine_scale(self) -> None:
* iterator_FF_post_affine_scale(self) -> None:
* destroy_all_menus_data(self, node: hou.SopNode, f3h_all: bool = False) -> None:
* update_xml_last_loaded(self) -> None:
* refresh_iterator_vars_menu(self) -> None:
* destroy_data_note(self) -> None:
* note_FF(self) -> None:
* menu_T_get_var_data(self) -> tuple[int, float]:
* menu_T_FF_get_var_data(self) -> tuple[int, float]:
* menu_T_data(self) -> tuple[int, str]:
* menu_T_PP_data(self) -> tuple[int, str]:
* menu_T_FF_data(self) -> tuple[int, str]:
* menu_T_PP_FF_data(self) -> tuple[int, str]:
* menu_T_pb_data(self) -> str:
* menu_T_ICON(self, FF: bool = False) -> list:
* menu_T_PP_ICON(self, FF: bool = False) -> list:
* menu_T_simple(self, FF: bool = False) -> list:
* menu_T(self, FF: bool = False) -> list:
* menu_T_pb(self) -> list:
* menu_select_iterator_data(self) -> list:
* menu_select_iterator(self) -> list:
* prm_select_iterator(self) -> None:
* flam3h_paste_reset_hou_session_data(self, hipLoad: bool = False) -> None:
* __menu_global_density(self) -> list:
* menu_global_density(self) -> list:
* menu_global_density_set(self) -> None:
* menu_global_density_set_default(self) -> None:
* menu_copypaste(self) -> list:
* menu_copypaste_FF(self) -> list:
* prm_paste_update_for_undo(self, node: hou.SopNode) -> tuple[hou.SopNode | None, int | None, bool]:
* prm_paste_update_for_undo_ff(self, node: hou.SopNode) -> tuple[hou.SopNode | None, int | None, bool]:
* prm_paste_CTRL(self, id: int) -> None:
* prm_paste_SHIFT(self, id: int) -> None:
* prm_paste_CLICK(self, id: int) -> None:
* prm_paste(self) -> None:
* prm_paste_FF_CTRL(self) -> None:
* prm_paste_FF_SHIFT(self) -> None:
* prm_paste_FF_CLICK(self) -> None:
* prm_paste_FF(self) -> None:
* prm_paste_sel_iter_sel_force_update(self, node: hou.SopNode) -> None:
* prm_paste_sel(self) -> None:
* prm_paste_sel_pre_affine(self) -> None:
* prm_paste_sel_post_affine(self) -> None:
* prm_paste_sel_pre_affine_FF(self) -> None:
* prm_paste_sel_post_affine_FF(self) -> None:
* prm_paste_sel_FF(self) -> None:
* flam3h_xaos_convert(self) -> None:
* reset_preaffine(self) -> None:
* reset_postaffine(self) -> None:
* reset_preaffine_FF(self) -> None:
* reset_postaffine_FF(self) -> None:
* swap_iter_pre_vars(self) -> None:
* swap_FF_post_vars(self) -> None:
* flam3h_default(self) -> None:
* flam3h_reset_iterator(self) -> None:
* flam3h_reset_FF(self) -> None:
* auto_set_xaos(self) -> None:
* iterators_count(self) -> None:
* __iterator_keep_last_vactive(self) -> None:
* __iterator_keep_last_vactive_STAR(self) -> None:
* __iterator_keep_last_weight(self) -> None:
* iterator_vactive_and_update(self) -> None:
    """    
    
    __slots__ = ("_kwargs", "_node")
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs: dict = kwargs
        self._node = kwargs['node']
        
        
    @staticmethod
    def flam3h_iterator_is_default_name(name: str, regex: str = "^[^\d\s()]+(?: [^\d\s()]+)*[\d]+") -> bool:
        """Check if an iterator name is a default name or not.
        
        Args:
            name(str): current iterator name to check.
            regex(str): The regex expresion to use to. Default to one build for the current iterators default name.
        
        Returns:
            (bool): True if the iterator name is a default name and False if not.
        """
        x = re_search(regex, name)
        return True if x is not None and x.group() == name else False


    @staticmethod
    def flam3h_on_loaded_set_density_menu(node: hou.SopNode) -> None:
        """This is for backward compatibility when the point count parameter was still exposed.
        It will set the density presets menu based on the currently set density value.
        
        The density values dictionary entries match whats inside: def menu_global_density_set(self) -> None:
        and also the entries inside the global menu: MENU_DENSITY
        
        Any changes to the entries on one of those need to be made also on the others.
        
        Args:
            node(hou.SopNode): current hou.SopNode to set
        
        Returns:
            (None):
        """
        density: int = node.parm(GLB_DENSITY).eval()
        # node.parm(GLB_DENSITY).deleteAllKeyframes() # This is commented out for now to allow to anim the density only from here
        node.parm(GLB_DENSITY_PRESETS).deleteAllKeyframes()
        density_values: dict[int, int] = { 500000: 1, 1000000: 2, 2000000: 3, 5000000: 4, 15000000: 5, 25000000: 6, 50000000: 7, 100000000: 8, 150000000: 9, 250000000: 10, 500000000: 11, 750000000: 12, 1000000000: 13 }
        density_idx: int | None = density_values.get(density)
        if density_idx is not None:
            node.setParms({GLB_DENSITY_PRESETS: density_idx}) #type: ignore
        else:
             node.setParms({GLB_DENSITY_PRESETS: -1}) #type: ignore


    @staticmethod
    def sierpinski_settings(node: hou.SopNode) -> None:
        """Set all the parameter to build a sierpinski triangle.

        Args:
            node(hou.SopNode): current hou.SopNode to set
            
        Returns:
            (None):
        """
        # iterator prm names
        n = flam3h_iterator_prm_names()

        # iter 1
        #
        # shader
        node.setParms({f"{n.shader_color}_1": 0}) # type: ignore
        node.setParms({f"{n.shader_speed}_1": -0.5}) # type: ignore
        # vars
        node.setParms({f"{n.prevar_type_1}_1": 0}) # type: ignore
        node.setParms({f"{n.prevar_type_2}_1": 0}) # type: ignore
        node.setParms({f"{n.var_type_1}_1": 0}) # type: ignore
        node.setParms({f"{n.var_type_2}_1": 0}) # type: ignore
        node.setParms({f"{n.var_type_3}_1": 0}) # type: ignore
        node.setParms({f"{n.var_type_4}_1": 0}) # type: ignore
        node.setParms({f"{n.postvar_type_1}_1": 0}) # type: ignore
        # pre affine
        node.setParms({f"{n.preaffine_x}_1": hou.Vector2((0.5, 0.0))}) # type: ignore
        node.setParms({f"{n.preaffine_y}_1": hou.Vector2((0.0, 0.5))}) # type: ignore
        node.setParms({f"{n.preaffine_o}_1": hou.Vector2((0.0, 0.51225))}) # type: ignore

        # iter 2
        #
        # shader
        node.setParms({f"{n.shader_color}_2": 0.5}) # type: ignore
        node.setParms({f"{n.shader_speed}_2": -0.5}) # type: ignore
        # vars
        node.setParms({f"{n.prevar_type_1}_2": 0}) # type: ignore
        node.setParms({f"{n.prevar_type_2}_2": 0}) # type: ignore
        node.setParms({f"{n.var_type_1}_2": 0}) # type: ignore
        node.setParms({f"{n.var_type_2}_2": 0}) # type: ignore
        node.setParms({f"{n.var_type_3}_2": 0}) # type: ignore
        node.setParms({f"{n.var_type_4}_2": 0}) # type: ignore
        node.setParms({f"{n.postvar_type_1}_2": 0}) # type: ignore
        # pre affine
        node.setParms({f"{n.preaffine_x}_2": hou.Vector2((0.5, 0.0))}) # type: ignore
        node.setParms({f"{n.preaffine_y}_2": hou.Vector2((0.0, 0.5))}) # type: ignore
        node.setParms({f"{n.preaffine_o}_2": hou.Vector2((-0.29575, 0.0))}) # type: ignore

        # iter 3
        #
        # shader
        node.setParms({f"{n.shader_color}_3": 1.0}) # type: ignore
        node.setParms({f"{n.shader_speed}_3": -0.5}) # type: ignore
        # vars
        node.setParms({f"{n.prevar_type_1}_3": 0}) # type: ignore
        node.setParms({f"{n.prevar_type_2}_3": 0}) # type: ignore
        node.setParms({f"{n.var_type_1}_3": 0}) # type: ignore
        node.setParms({f"{n.var_type_2}_3": 0}) # type: ignore
        node.setParms({f"{n.var_type_3}_3": 0}) # type: ignore
        node.setParms({f"{n.var_type_4}_3": 0}) # type: ignore
        node.setParms({f"{n.postvar_type_1}_3": 0}) # type: ignore
        # pre affine
        node.setParms({f"{n.preaffine_x}_3": hou.Vector2((0.5, 0.0))}) # type: ignore
        node.setParms({f"{n.preaffine_y}_3": hou.Vector2((0.0, 0.5))}) # type: ignore
        node.setParms({f"{n.preaffine_o}_3": hou.Vector2((0.29575, 0.0))}) # type: ignore


    @staticmethod
    def get_user_data(node: hou.SopNode, data_name: str = FLAM3H_USER_DATA_ITER) -> int | bool:
        """Get the node user data associated to the copy/paste data.
        
        Args:
            node(hou.SopNode): [current hou.SopNode to set]
            data(str): Default to: FLAM3H_USER_DATA_ITER. The name of the data we want to get. 
            
        Returns:
            (int | bool): Return the requested user data or False if it does not exist.
        """   
        
        name: str = f"{FLAM3H_USER_DATA_PRX}_{data_name}"
        data: int | None = node.userData(f"{name}")
        if data is not None:
            return data
        else:
            return False


    @staticmethod
    def exist_user_data(node: hou.SopNode, data: str = FLAM3H_USER_DATA_ITER) -> bool:
        """Confirm the node user data associated to the copy/paste data Exist.
        
        Args:
            node(hou.SopNode): [current hou.SopNode to set]
            data(str): Default to: FLAM3H_USER_DATA_ITER. The name of the data we want to get. For FF it wil be: " FLAM3H_USER_DATA_FF "
            
        Returns:
            (bool): Return True if the requested user data exist or False if it does not.
        """   
        data_name: str = f"{FLAM3H_USER_DATA_PRX}_{data}"
        if node.userData(f"{data_name}") is None:
            return False
        else:
            return True


    @staticmethod
    def set_comment_and_user_data_iterator(node: hou.SopNode, value: str, data: str = FLAM3H_USER_DATA_ITER) -> None:
        """Set the node comment associated to the copy/paste data. It can be for an iterator number or for the FF.
        
        Args:
            node(hou.SopNode): FLAM3H node to set
            value(str): The value to set this user data to.
            data(str): Default to: FLAM3H_USER_DATA_ITER. The name of the data we want to set the comment for. 

        Returns:
            (None):
        """   
        
        data_name: str = f"{FLAM3H_USER_DATA_PRX}_{data}"
        data_iter_name: str = f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_ITER}"
        data_FF_name: str = f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_FF}"
        
        if data_name == data_iter_name:
            
            if node.userData(f"{data_FF_name}") is None:
                if node.userData(f"{data_name}") is None:
                    with hou.undos.group(f"FLAM3H SET user data None"): # type: ignore
                        node.setUserData(f"{data_name}", value)
                        node.setComment(node.userData(f"{data_name}"))
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore
                    
            else:
                if node.userData(f"{data_name}") is None:
                    with hou.undos.group(f"FLAM3H SET user data"): # type: ignore
                        node.setUserData(f"{data_name}", value)
                        node.setComment(f"{value}, FF")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore
                    
        elif data_name == data_FF_name:
            if node.userData(f"{data_iter_name}") is None:
                if node.userData(f"{data_name}") is None:
                    with hou.undos.group(f"FLAM3H SET FF user data None"): # type: ignore
                        node.setUserData(f"{data_name}", value)
                        node.setComment("FF")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore
            
            else:
                if node.userData(f"{data_name}") is None:
                    with hou.undos.group(f"FLAM3H SET FF user data"): # type: ignore
                        data_iter = node.userData(f"{data_iter_name}")
                        node.setUserData(f"{data_name}", value)
                        node.setComment(f"{str(data_iter)}, FF")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore

        
    @staticmethod
    def del_comment_and_user_data_iterator(node: hou.SopNode, data: str = FLAM3H_USER_DATA_ITER) -> None:
        """Delete the node comment associated to the copy/paste data. It can be for an iterator number or for the FF.
        
        Args:
            node(hou.SopNode): FLAM3H node to set
            data(str): Default to: FLAM3H_USER_DATA_ITER. The name of the data we want to delete the comment for. 
            
        Returns:
            (None):
        """   
        
        data_name: str = f"{FLAM3H_USER_DATA_PRX}_{data}"
        data_iter_name: str = f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_ITER}"
        data_FF_name: str = f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_FF}"
        
        if data_name == data_iter_name:
            if node.userData(f"{data_FF_name}") is None:
                if node.userData(f"{data_name}") is not None:
                    with hou.undos.group(f"FLAM3H DEL user data iter None"): # type: ignore
                        flam3h_iterator_utils.destroy_userData(node, f"{data_name}")
                        node.setComment("")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, False) # type: ignore
                    
            else:
                if node.userData(f"{data_name}") is not None:
                    with hou.undos.group(f"FLAM3H DEL user data iter"): # type: ignore
                        flam3h_iterator_utils.destroy_userData(node, f"{data_name}")
                        # node.setComment("")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, False) # type: ignore
                        node.setComment("FF")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore
                    
        elif data_name == data_FF_name:
            
            if node.userData(f"{data_iter_name}") is None:
                if node.userData(f"{data_name}") is not None:
                    with hou.undos.group(f"FLAM3H DEL FF user data None"): # type: ignore
                        flam3h_iterator_utils.destroy_userData(node, f"{data_name}")
                        node.setComment("")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, False) # type: ignore
                    
            else:
                if node.userData(f"{data_name}") is not None:
                    with hou.undos.group(f"FLAM3H DEL FF user data"): # type: ignore
                        data_iter = node.userData(f"{data_iter_name}")
                        flam3h_iterator_utils.destroy_userData(node, f"{data_name}")
                        # node.setComment("")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, False) # type: ignore
                        node.setComment(f"{str(data_iter)}")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore


    @staticmethod            
    def flam3h_init_hou_session_iterator_data(node: hou.SopNode) -> None:
        """Initialize the copy/paste data need by FLAM3H iterators and stored into the current hou.session.
        
        Args:
            node(hou.SopNode): FLAM3H node to set
            
        Returns:
            (None):
        """   
        
        # The following try/except blocks are not really needed
        # becasue FLAM3H node will create and initialize those on creation
        # but just in case this data is deleted somehow.
        try: hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
        except: hou.session.FLAM3H_MARKED_ITERATOR_NODE: TA_MNode = node # type: ignore
        try: hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
        except: hou.session.FLAM3H_MARKED_ITERATOR_NODE: TA_MNode = None # type: ignore
        try: hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
        except: hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = None # type: ignore


    @staticmethod
    def flam3h_init_hou_session_ff_data(node: hou.SopNode) -> None:
        """Initialize the copy/paste data need by FLAM3H FF and stored into the current hou.session.
        
        Args:
            node(hou.SopNode): FLAM3H node to set
            
        Returns:
            (None):
        """   
        
        # The following try/except blocks are not really needed
        # becasue FLAM3H node will create and initialize those on creation
        # but just in case this data is deleted somehow.
        try: hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
        except: hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = node # type: ignore
        try: hou.session.FLAM3H_MARKED_FF_NODE.type() # type: ignore
        except: hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = None # type: ignore
        try: hou.session.FLAM3H_MARKED_FF_CHECK # type: ignore
        except: hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = None # type: ignore
        
        
    @staticmethod
    def flam3h_init_hou_session_restore_from_user_data(node: hou.SopNode) -> None:
        """If in the loaded hip file there are data stored into the nodes, lets set the copy/paste data to those.
        This will allow to re-load an hip file with marked iterator or FF and pick up from there, which is nice
        
        Args:
            node(hou.SopNode): FLAM3H node to set
            
        Returns:
            (None):
        """   
        
        # Iterator
        if flam3h_iterator_utils.exist_user_data(node):
            hou.session.FLAM3H_MARKED_ITERATOR_NODE: TA_MNode = node # type: ignore
            data = flam3h_iterator_utils.get_user_data(node)
            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = data # type: ignore
            flam3h_iterator_utils.iterator_mpidx_mem_set(node, int(data)) # type: ignore
        else:
            # If this node do not posses the copy/paste data, lets first check if the data and its node exist (other FLAM3H node)
            # before clearing it out
            try: 
                hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
            except:
                hou.session.FLAM3H_MARKED_ITERATOR_NODE: TA_MNode = None # type: ignore
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = None # type: ignore
            
        # FF
        if flam3h_iterator_utils.exist_user_data(node, FLAM3H_USER_DATA_FF):
            hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = node # type: ignore
            hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = 1 # type: ignore
        else:
            # If this node do not posses the copy/paste data, lets first check if the data and its node exist (other FLAM3H node)
            # before clearing it out
            try: 
                hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                hou.session.FLAM3H_MARKED_FF_CHECK # type: ignore
            except:
                hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = None # type: ignore
                hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = None # type: ignore


    @staticmethod
    def iterator_mpidx_mem_set(node, data: int) -> None:
        """Work as an history space to store the marked iterator info in it.
        
        Args:
            node(hou.SopNode): FLAM3H node to set
            data(int): Marked iterator number and info. The possible option are:
                * from 1 to n for the number of the marked iterator.
                * 0 to signal no iterator has been marked.
                * -1 if a marked iterator has been deleted.
            
        Returns:
            (None):
        """   
        flam3h_general_utils.private_prm_set(node, FLAM3H_DATA_PRM_MPIDX, data)


    @staticmethod
    def paste_from_prm(prm_from: hou.Parm, prm_to: hou.Parm, pvt: bool = False) -> None:
        """Paste value for a single parameter, including keyframes and expressions if any.
        
        Args:
            prm_from(hou.Parm): The parameter to copy the data from
            prm_to(hou.Parm): The parameter to copy the dato into
            pvt(bool): Default to False. is it a private parameter or not ?
            
        Returns:
            (None):
        """   
        if pvt: prm_to.lock(False) 
        prm_to.deleteAllKeyframes()
        if len(prm_from.keyframes()):
            [prm_to.setKeyframe(k) for k in prm_from.keyframes()]
        else:
            prm_to.set(prm_from.eval()) # type: ignore
        if pvt: prm_to.lock(True)


    @staticmethod
    def paste_from_list(node: hou.SopNode, flam3node: hou.SopNode | None, prm_list: tuple, id: str, id_from: str) -> None:
        """Paste value for a parameter, including keyframes and expressions if any,
        between different multiparameter indexes.
        
        Args:
            node(hou.SopNode): FLAM3H node to set
            flam3node(hou.SopNode | None): hou.SopNode to copy values from
            prm_list(tuple): parameters list to query and set
            id(str): current multiparamter index
            id_from(str): multiparameter index to copy from
            
        Returns:
            (None):
        """    
        
        if flam3node is not None:
            
            for prm in prm_list:
                # if a tuple
                if prm[1]:
                    prm_from = flam3node.parmTuple(f"{prm[0]}{id_from}")
                    prm_to = node.parmTuple(f"{prm[0]}{id}")
                    prm_to.deleteAllKeyframes()
                    [[prm_to[prm_idx].setKeyframe(k) for k in p.keyframes()] if len(p.keyframes()) else prm_to[prm_idx].set(p.eval()) for prm_idx, p in enumerate(prm_from)]
                    
                    # prm_idx = 0
                    # for p in prm_from:
                    #     if len(p.keyframes()):
                    #         [prm_to[prm_idx].setKeyframe(k) for k in p.keyframes()]
                    #     else:
                    #         prm_to[prm_idx].set(p.eval())
                    #     prm_idx += 1
                    
                else:
                    prm_from = flam3node.parm(f"{prm[0]}{id_from}")
                    prm_to = node.parm(f"{prm[0]}{id}")
                    prm_to.deleteAllKeyframes()
                    if len(prm_from.keyframes()):
                        [prm_to.setKeyframe(k) for k in prm_from.keyframes()]
                    else:
                        prm_to.set(prm_from.eval())
        else:
            _MSG: str = f"{node.name()} -> The FLAM3H node you are trying to copy data from do not exist"
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            
    
    @staticmethod
    def is_iterator_affine_default(node: hou.SopNode, from_FLAM3H_NODE: hou.SopNode, prm_list_affine: tuple, id: str, id_from: str, post: bool = False) -> bool:
        """To be used with the copy/paste methods. Check if an iterator Affine (PRE or POST) are at default values. 
        If they are default values and they are the post affine, it will turn the post affine toggle OFF for both this iterator (id) and the from iterator (id_from)
        even if they are between two different FLAM3H nodes (node and from_FLAM3H_NODE)
        
        Args:
            node(hou.SopNode): This FLAM3H node
            from_FLAM3H_NODE(hou.SopNode, None): hou.SopNode to copy values from
            prm_list_affine(tuple): parameters list to query. This expect either: flam3h_iterator().sec_preAffine or flam3h_iterator().sec_postAffine
            id(str): current multiparamter index
            id_from(str): multiparameter index to copy from
            post(bool): Default to False. Is it a post affine ?  True for declaring it as post affine.
            
        Returns:
            (bool): True if the affine are default values and False if they are not.
        """   
        if post:
            keyframes: list = [item for sublist in [[1 if len(p.keyframes()) else 0 for p in node.parmTuple(f"{prm_list_affine[1:][idx][0]}{id}")] if prm_list_affine[1:][idx][1] else [1 if len(node.parm(f"{prm_list_affine[1:][idx][0]}{id}").keyframes()) else 0] for idx in range(len(prm_list_affine[1:]))] for item in sublist]
            collect: list = [node.parmTuple(f"{prm_list_affine[1:][idx][0]}{id}").eval() if prm_list_affine[1:][idx][1] else node.parm(f"{prm_list_affine[1:][idx][0]}{id}").eval() for idx in range(len(prm_list_affine[1:]))]
            if 1 not in keyframes and collect == [(1.0, 0.0), (0.0, 1.0), (0.0, 0.0), 0.0]:
                node.setParms({f"{prm_list_affine[0][0]}{id}": 0}) # type: ignore
                from_FLAM3H_NODE.setParms({f"{prm_list_affine[0][0]}{id_from}": 0}) # type: ignore
                return True
            else:
                return False

        else:
            keyframes: list = [item for sublist in [[1 if len(p.keyframes()) else 0 for p in node.parmTuple(f"{prm_list_affine[idx][0]}{id}")] if prm_list_affine[idx][1] else [1 if len(node.parm(f"{prm_list_affine[idx][0]}{id}").keyframes()) else 0] for idx in range(len(prm_list_affine))] for item in sublist]
            collect: list = [node.parmTuple(f"{prm_list_affine[idx][0]}{id}").eval() if prm_list_affine[idx][1] else node.parm(f"{prm_list_affine[idx][0]}{id}").eval() for idx in range(len(prm_list_affine))]
            if 1 not in keyframes and collect == [(1.0, 0.0), (0.0, 1.0), (0.0, 0.0), 0.0]:
                return True
            else:
                return False
            
            
    @staticmethod
    def is_FF_affine_default(node: hou.SopNode, from_FLAM3H_NODE: hou.SopNode, prm_list_affine: tuple, post: bool = False) -> bool:
        """To be used with the copy/paste methods. Check if the FF Affine (PRE or POST) are at default values. 
        If they are default values and they are the post affine, it will turn the post affine toggle OFF for both this iterator (id) and the from iterator (id_from)
        even if they are between two different FLAM3H nodes (node and from_FLAM3H_NODE)
        
        Args:
            node(hou.SopNode): This FLAM3H node
            flam3node(hou.SopNode, None): hou.SopNode to copy values from
            prm_list_affine(tuple): parameters list to query. This expect either: flam3h_iterator_FF().sec_preAffine_FF or flam3h_iterator_FF().sec_postAffine_FF
            post(bool): Default to False. Is it a post affine ?  True for declaring it as post affine.
            
        Returns:
            (bool): True if the affine are default values and False if they are not.
        """   
        if post:
            keyframes: list = [item for sublist in [[1 if len(p.keyframes()) else 0 for p in node.parmTuple(f"{prm_list_affine[1:][idx][0]}")] if prm_list_affine[1:][idx][1] else [1 if len(node.parm(f"{prm_list_affine[1:][idx][0]}").keyframes()) else 0] for idx in range(len(prm_list_affine[1:]))] for item in sublist]
            collect: list = [node.parmTuple(f"{prm_list_affine[1:][idx][0]}").eval() if prm_list_affine[1:][idx][1] else node.parm(f"{prm_list_affine[1:][idx][0]}").eval() for idx in range(len(prm_list_affine[1:]))]
            if 1 not in keyframes and collect == [(1.0, 0.0), (0.0, 1.0), (0.0, 0.0), 0.0]:
                node.setParms({f"{prm_list_affine[0][0]}": 0}) # type: ignore
                from_FLAM3H_NODE.setParms({f"{prm_list_affine[0][0]}": 0}) # type: ignore
                return True
            else:
                return False

        else:
            keyframes: list = [item for sublist in [[1 if len(p.keyframes()) else 0 for p in node.parmTuple(f"{prm_list_affine[1:][idx][0]}")] if prm_list_affine[1:][idx][1] else [1 if len(node.parm(f"{prm_list_affine[1:][idx][0]}").keyframes()) else 0] for idx in range(len(prm_list_affine[1:]))] for item in sublist]
            collect: list = [node.parmTuple(f"{prm_list_affine[idx][0]}").eval() if prm_list_affine[idx][1] else node.parm(f"{prm_list_affine[idx][0]}").eval() for idx in range(len(prm_list_affine))]
            if 1 not in keyframes and collect == [(1.0, 0.0), (0.0, 1.0), (0.0, 0.0), 0.0]:
                return True
            else:
                return False
    
    
    @staticmethod
    def paste_from_list_affine(node: hou.SopNode, prm_list_affine_to: tuple, prm_list_affine_from: tuple, id: str) -> None:
        """Paste value from the post affine into the pre affine and viceversa ( just swap  )
        
        Args:
            node(hou.SopNode): FLAM3H node to set
            prm_list_affine_to(tuple): parameters list to query and set for the either the PRE or POST affine
            prm_list_affine_from(tuple): parameters list to query and set for the either the PRE or POST affine
            id(str): current multiparamter index
            
        Returns:
            (None):
        """    
        
        for idx, prm in enumerate(prm_list_affine_to):
            # if a tuple
            if prm[1]:
                prm_from = node.parmTuple(f"{prm[0]}{id}")
                prm_to = node.parmTuple(f"{prm_list_affine_from[idx][0]}{id}")
                prm_to.deleteAllKeyframes()
                [[prm_to[prm_idx].setKeyframe(k) for k in p.keyframes()] if len(p.keyframes()) else prm_to[prm_idx].set(p.eval()) for prm_idx, p in enumerate(prm_from)]
                
                # prm_idx = 0
                # for p in prm_from:
                #     if len(p.keyframes()):
                #         [prm_to[prm_idx].setKeyframe(k) for k in p.keyframes()]
                #     else:
                #         prm_to[prm_idx].set(p.eval())
                #     prm_idx += 1
                
            else:
                prm_from = node.parm(f"{prm[0]}{id}")
                prm_to = node.parm(f"{prm_list_affine_from[idx][0]}{id}")
                prm_to.deleteAllKeyframes()
                if len(prm_from.keyframes()):
                    [prm_to.setKeyframe(k) for k in prm_from.keyframes()]
                else:
                    prm_to.set(prm_from.eval())
                    
                     
    @staticmethod
    def pastePRM_T_from_list(node: hou.SopNode, flam3node: hou.SopNode | None, prmT_list: tuple, varsPRM: tuple, id: str, id_from: str) -> None:
        """Paste variation parameter values
        between different multiparameter indexes.
        In case of a parametric variation, it will paste its parameters using:
        * flam3h_iterator_utils.paste_from_list() definition.
         
        Args:
            node(hou.SopNode): FLAM3H node to set
            flam3node(hou.SopNode | None): hou.SopNode to copy values from
            prmT_list(tuple): variations list - types
            varsPRM(tuple): variation's parmaters list
            id(str): current multiparamter index
            id_from(str): multiparameter index to copy from
            
        Returns:
            (None):
        """    
        for prm in prmT_list:
            if flam3node is not None:
                prm_from = flam3node.parm(f"{prm}{id_from}")
                prm_to = node.parm(f"{prm}{id}")
                prm_to.deleteAllKeyframes()
                flam3h_iterator_utils.paste_from_prm(prm_from, prm_to)
                # Check if this var is a parametric or not
                v_type: int = int(prm_from.eval())
                if(varsPRM[v_type][-1]):  
                    flam3h_iterator_utils.paste_from_list(node, flam3node, varsPRM[v_type][1:-1], id, id_from)
                    

    @staticmethod
    def paste_save_note(_note: str) -> str:
        """When copy/paste parameter values between different multiparameter indexes,
        this will save the current note and place it into parenthesis as a form of backup.
        
        _NOTE:
            This need an upgrade/improvements at some point.
        
        Args:
            _note(str): current note in the parameter

        Returns:
            (str): simple new note append
        """

        search_iter: str = "iter."
        search_FF: str = ".FF"

        if _note.find("(") or _note.find(")") == -1:
            _note_split: list = _note.split()
            if len(_note_split) > 1 and (search_iter in _note_split[-1].rpartition(search_iter) or search_FF in _note_split[-1].rpartition(search_FF)):
                note: str = f"({' '.join(_note_split[0:-1])}) "
            elif len(_note.split(".")) > 1 and ("iter" in _note.split(".") or "FF" in _note.split(".")):
                note: str = ""
            else:
                note: str = f"({_note}) "
        else:
            note: str = f"({_note[_note.find('(') + 1:_note.find(')')]}) "
        return note


    @staticmethod
    def paste_set_note(node: hou.SopNode, flam3node: hou.SopNode | None, int_mode: int, str_section: str, id: str, id_from: str) -> None:
        """After a copy/paste, it will set the note parameter with a string indicating what has been pasted ( when copy/paste iterator's sections )
        
        _NOTE:
            This need an upgrade/improvements at some point.
        
        Args:
            node (hou.SopNode): FLAM3H node to set
            flam3node(hou.SopNode | None): hou.SopNode to copy values from
            int_mode(int): int(0) copy/paste iterator into the same node. int(1) copy/paste FF between different nodes. int(2) copy/paste FF sections between different nodes
            str_section(str): section name string to be copied, this is only for msg print info
            id(str): current multiparamter index
            id_from(str): multiparameter index to copy from
            
        Returns:
            (None):
        """ 
        
        n = flam3h_iterator_prm_names()
        node_name = str(flam3node)
        _current_note_FF: str = node.parm("ffnote").eval()

        if int_mode == 0:
            _current_note = node.parm(f"note_{id}").eval()
            # If on the same FLAM3H node
            if node == flam3node:
                if len(_current_note) == 0:
                    node.setParms({f"{n.main_note}_{id}": f"iter.{id_from}{str_section}"}) # type: ignore
                else:
                    node.setParms({f"{n.main_note}_{id}": f"{flam3h_iterator_utils.paste_save_note(_current_note)}iter.{id_from}{str_section}"}) # type: ignore
                _MSG: str = f"{node.name()}.iter.{id}{str_section} -> Copied values from: iter.{id_from}{str_section}"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            else:
                if len(_current_note) == 0:
                    node.setParms({f"{n.main_note}_{id}": f"{node_name}.iter.{id_from}{str_section}"}) # type: ignore
                else:
                    node.setParms({f"{n.main_note}_{id}": f"{flam3h_iterator_utils.paste_save_note(_current_note)}{node_name}.iter.{id_from}{str_section}"}) # type: ignore
                _MSG: str = f"{node.name()}.iter.{id}{str_section} -> Copied values from: {node_name}.iter.{id_from}{str_section}"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
        elif int_mode == 1:
            if node != flam3node:
                if len(_current_note_FF) == 0:
                    node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{node_name}.FF"}) # type: ignore
                else:
                    node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{flam3h_iterator_utils.paste_save_note(_current_note_FF)}{node_name}.FF"}) # type: ignore
                _MSG: str = f"{node.name()} -> Copied FF from: {node_name}.FF"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
        elif int_mode == 2:
            if node != flam3node:
                if len(_current_note_FF) == 0:
                    node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{node_name}.FF{str_section}"}) # type: ignore
                else:
                    node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{flam3h_iterator_utils.paste_save_note(_current_note_FF)}{node_name}.FF{str_section}"}) # type: ignore
                _MSG: str = f"{node.name()}.FF{str_section} -> Copied from: {node_name}.FF{str_section}"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')


    @staticmethod
    def auto_set_xaos_data_get_MP_MEM(node: hou.SopNode) -> list | None:
        """Retrieve the desire data from FLAM3H data srting parameters
    and reconvert it back to usable types.

        Args:
            node(hou.SopNode): FLAM3H node 

        Returns:
            (list | None): A valid data type of the same data retrieved to be used inside: auto_set_xaos()
        """
        get_prm: str = node.parm(FLAM3H_DATA_PRM_XAOS_MP_MEM).eval()
        if get_prm:
            return [int(x) for x in get_prm.split(' ')]
        else:
            return None
        
        
    @staticmethod
    def auto_set_xaos_data_get_XAOS_PREV(node: hou.SopNode) -> list | None:
        """Retrieve the desire data from FLAM3H data srting parameters
    and reconvert it back to usable types.

        Args:
            node(hou.SopNode): FLAM3H node

        Returns:
            (list | None): A valid data type of the same data retrieved to be used inside: auto_set_xaos()
        """
        get_prm: str = node.parm(FLAM3H_DATA_PRM_XAOS_PREV).eval()
        if get_prm:
            return [x.split(' ') for x in get_prm.split(':')]
        else:
            return None
        

    @staticmethod
    def auto_set_xaos_data_set_MP_MEM(node: hou.SopNode, data: list | tuple) -> None:
        """Set the data_name data into FLAM3H data parameters.
        Note that all the data will be of type: string.

        _NOTE:
            This parameter has been swapped for a label message parameter so the lock/unlock is not necessary anymore.
            However, is not causing any problem and I leave it here for now.

        Args:
            data (list | tuple): The actual data to set.

        Returns:
            (None):
        """
        data_to_prm: str = ' '.join([str(x) for x in data])
        flam3h_general_utils.private_prm_set(node, FLAM3H_DATA_PRM_XAOS_MP_MEM, data_to_prm)
                

    @staticmethod
    def auto_set_xaos_data_set_XAOS_PREV(node: hou.SopNode, data: list | tuple) -> None:
        """Set the data_name data into FLAM3H data parameters.
    Note that all the data will be of type: string.

        Args:
            node(hou.SopNode): The FLAM3H node
            data(list | tuple): The actual data to set. A tuple can only come from: out_flame_utils.out_xf_xaos_from(self, mode=0) -> tuple:

        Returns:
            (None):
        """
        # to prm from: flam3_xaos_convert()
        if isinstance(data, tuple):
            data_to_prm: str = ':'.join(data)
            # set
            flam3h_general_utils.private_prm_set(node, FLAM3H_DATA_PRM_XAOS_PREV, data_to_prm)
            
        else:
            data_to_prm: str = ':'.join([' '.join(xaos) for xaos in data])
            # set
            flam3h_general_utils.private_prm_set(node, FLAM3H_DATA_PRM_XAOS_PREV, data_to_prm)
            
            
    @staticmethod
    def flam3h_on_load_opacity_zero(node: hou.SopNode, f3h_all: bool = False) -> None:
        """Check each iterator's shader opacity and if any of them is 0(Zero) activate the Remove Invalid Option(RIP)

        Args:
            node(hou.SopNode): The current FLAM3H node being loaded in the hip file.
            f3h_all(bool): Default to False. Perform this check and correct if needed for all FLAM3H nodes in the scene.

        Returns:
            (None):
        """  
        iter_count: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        if iter_count:
            lambda_min_opacity: Callable[[], float] = lambda: min([node.parm(f'{flam3h_iterator_prm_names().shader_alpha}_{idx + 1}').eval() for idx in range(iter_count)])
            if f3h_all: [flam3h_general_utils.private_prm_set(f3h, PREFS_PVT_RIP, 1) if lambda_min_opacity() == 0 else ... for f3h in node.type().instances()]
            else:
                if lambda_min_opacity() == 0: flam3h_general_utils.private_prm_set(node, PREFS_PVT_RIP, 1)


    @staticmethod
    def destroy_cachedUserData(node, data: str, must_exist: bool = False) -> None:
        """Destroy cached user data.
        This is to be run also as a callback script inside parms that are responsible to update some menus,
        For now inside: Iterator shader's opacity -> calback script
        
        So far the cached user data names being used are:
        
        * iter_sel
        * iter_sel_a
        * iter_sel_w
        * iter_sel_o
        * iter_sel_id
        * edge_case_01
        * cp_presets_menu
        * cp_presets_menu_idx
        * cp_presets_menu_off
        * cp_presets_menu_off_idx
        * cp_presets_filepath
        * in_presets_menu
        * in_presets_menu_idx
        * in_presets_menu_off
        * in_presets_menu_off_idx
        * in_presets_filepath
        * out_presets_menu
        * out_presets_filepath
        * vars_menu_all_simple
            
        Args:
            node(hou.SopNode): FLAM3H node
            data(str): the name of the data to destroy
            must_exist(bool): Default to False. Destroy data will run silently if the data name do not exist. Set it to True to get an error.

        Returns:
            (None):
        """
        if not must_exist:
            try: node.destroyCachedUserData(data)
            except: pass
        else: node.destroyCachedUserData(data)
        
        
    @staticmethod
    def destroy_cachedUserData_all_f3h(node, data_name: str) -> None:
        """Destroy cached user data an all FLAM3H node in the current Houdini session.

        Args:
            node(hou.SopNode): The current FLAM3H node being loaded in the hip file.
            data_name(str): The name of the data to destroy.

        Returns:
            (None):
        """  
        for f3h in node.type().instances():
            assert isinstance(f3h, hou.SopNode)
            data = f3h.cachedUserData(data_name)
            if data is not None: flam3h_iterator_utils.destroy_cachedUserData(f3h, data_name)
            
            
    @staticmethod
    def destroy_userData(node, data: str, must_exist: bool = False) -> None:
        """Destroy user data.
        
        So far the user data names being used are:
        
        * nodeinfo_Marked iterator -> f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_ITER}
        * nodeinfo_Marked FF -> f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_FF}
        * nodeinfo_XF VIZ -> f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}
        * XML_last_loaded -> f"{FLAM3H_USER_DATA_XML_LAST}"

        Args:
            node(hou.SopNode): This FLAM3H node
            data(str): The name of the data to retrieve
            must_exist(bool): Default to: False. When True it will throw an error if the data do not exist, other will it will silently pass.
            
            
        Returns:
            (None):
        """
        if not must_exist:
            try: node.destroyUserData(data)
            except: pass
        else: node.destroyUserData(data)
        
        
    @staticmethod
    def force_menu_var_update_FF(node: hou.SopNode) -> None:
        """Refresh/Force the iterator FF variation's menus to update.

        Args:
            (node): the FLAM3H node
            
        Returns:
            (None):
        """  
        n = flam3h_iterator_prm_names()
        prm_names: tuple = (f"{PRX_FF_PRM}{n.prevar_type_1}", 
                            f"{PRX_FF_PRM}{n.var_type_1}",
                            f"{PRX_FF_PRM}{n.var_type_2}",
                            f"{PRX_FF_PRM}{n.postvar_type_1}",
                            f"{PRX_FF_PRM}{n.postvar_type_2}")
        [node.parm(name).pressButton() for name in prm_names] 


    @staticmethod
    def menu_T_get_type_icon(w: float) -> str:
        """Return the proper bookmark icon to use in the menu label for the selected variation and weight.
        This is to be used for the VAR section in the iterator (FLAME and FF tabs) 

        Args:
            w(float): the variation weight to derive the proper bookmark icon to use.
            
        Returns:
            (str): The full path of the bookmark icon to use in the menu based on this variation weight value.
        """
        if w > 0:
            if w > 1:
                return FLAM3H_ICON_STAR_FLAME_VAR_ACTV_OVER_ONE
            else:
                return FLAM3H_ICON_STAR_FLAME_VAR_ACTV
        elif w < 0:
            return FLAM3H_ICON_STAR_FLAME_VAR_ACTV_NEGATIVE
            
        return FLAM3H_ICON_STAR_EMPTY_OPACITY
    
    
    @staticmethod
    def menu_T_PP_get_type_icon(w: float) -> str:
        """Return the proper bookmark icon to use in the menu label for the selected PRE or POST variation and weight.
        This is to be used for the PRE and POST sections in the iterator (FLAME and FF tabs) 

        Args:
            w(float): the variation weight to derive the proper bookmark icon to use.
            
        Returns:
            (str): The full path of the bookmark icon to use in the menu based on this variation weight value.
        """
        if w > 0:
            if w > 1:
                return FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV_OVER_ONE
            else:
                return FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV
            
        return FLAM3H_ICON_STAR_EMPTY_OPACITY


    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def kwargs(self):
        return self._kwargs
        
    @property
    def node(self):
        return self._node
    
    
    def iterator_affine_scale(self) -> None:
        """Scale the affine X and Y of an amount.
        The default value is: 1 whitch mean 100% and so no scale.
        Once changed it will scale the affine values and reset itself back to being: 1
        For example if you type a value of: 1.2, it will scale the affine up by 20%.
        It is an initial test, and it may or may not change/improve with time.

        Args:
            (self):

        Returns:
            (None):
        """  
        idx: int = self.kwargs['script_multiparm_index']
        scl: float = hou.parm(f"scl_{idx}").eval()
        x: tuple = hou.parmTuple(f"x_{idx}").eval()
        y: tuple = hou.parmTuple(f"y_{idx}").eval()
        m2 = hou.Matrix2((x, y))
        m2_scl = hou.Matrix2(((scl, 0), (0, scl)))
        m2_new: tuple = (m2 * m2_scl).asTupleOfTuples()
        self.node.setParms({f"x_{idx}": hou.Vector2((m2_new[0]))})
        self.node.setParms({f"y_{idx}": hou.Vector2((m2_new[1]))})
        # Reset to no-scale value (1 being 100%)
        self.node.setParms({f"scl_{idx}": 1})
        
        
    def iterator_post_affine_scale(self) -> None:
        """Scale the affine X and Y of an amount.
        The default value is: 1 whitch mean 100% and so no scale.
        Once changed it will scale the affine values and reset itself back to being: 1
        For example if you type a value of: 1.2, it will scale the affine up by 20%.
        The best way to use it is to click in the numeric field and use the mouse wheel to scale up and down.
        Holding [SHIFT] will scale with an increment of: 0.01
        
        It is an initial test, and it may or may not change/improve with time.

        Args:
            (self):
            
        Returns:
            (None):
        """  
        idx: int = self.kwargs['script_multiparm_index']
        scl: float = hou.parm(f"pscl_{idx}").eval()
        x: tuple = hou.parmTuple(f"px_{idx}").eval()
        y: tuple = hou.parmTuple(f"py_{idx}").eval()
        m2 = hou.Matrix2((x, y))
        m2_scl = hou.Matrix2(((scl, 0), (0, scl)))
        m2_new: tuple = (m2 * m2_scl).asTupleOfTuples()
        self.node.setParms({f"px_{idx}": hou.Vector2((m2_new[0]))})
        self.node.setParms({f"py_{idx}": hou.Vector2((m2_new[1]))})
        # Reset to no-scale value (1 being 100%)
        self.node.setParms({f"pscl_{idx}": 1})
        
        
    def iterator_FF_affine_scale(self) -> None:
        """Scale the affine X and Y of an amount.
        The default value is: 1 whitch mean 100% and so no scale.
        Once changed it will scale the affine values and reset itself back to being: 1
        For example if you type a value of: 1.2, it will scale the affine up by 20%.
        It is an initial test, and it may or may not change/improve with time.

        Args:
            (self):
            
        Returns:
            (None):
        """  
        scl: float = hou.parm("ffscl").eval()
        x: tuple = hou.parmTuple("ffx").eval()
        y: tuple = hou.parmTuple("ffy").eval()
        m2 = hou.Matrix2((x, y))
        m2_scl = hou.Matrix2(((scl, 0), (0, scl)))
        m2_new: tuple = (m2 * m2_scl).asTupleOfTuples()
        self.node.setParms({"ffx": hou.Vector2((m2_new[0]))})
        self.node.setParms({"ffy": hou.Vector2((m2_new[1]))})
        # Reset to no-scale value (1 being 100%)
        self.node.setParms({"ffscl": 1})
        
        
    def iterator_FF_post_affine_scale(self) -> None:
        """Scale the affine X and Y of an amount.
        The default value is: 1 whitch mean 100% and so no scale.
        Once changed it will scale the affine values and reset itself back to being: 1
        For example if you type a value of: 1.2, it will scale the affine up by 20%.
        It is an initial test, and it may or may not change/improve with time.

        Args:
            (self):
            
        Returns:
            (None):
        """  
        scl: float = hou.parm("ffpscl").eval()
        x: tuple = hou.parmTuple("ffpx").eval()
        y: tuple = hou.parmTuple("ffpy").eval()
        m2 = hou.Matrix2((x, y))
        m2_scl = hou.Matrix2(((scl, 0), (0, scl)))
        m2_new: tuple = (m2 * m2_scl).asTupleOfTuples()
        self.node.setParms({"ffpx": hou.Vector2((m2_new[0]))})
        self.node.setParms({"ffpy": hou.Vector2((m2_new[1]))})
        # Reset to no-scale value (1 being 100%)
        self.node.setParms({"ffpscl": 1})

        
    def destroy_all_menus_data(self, node: hou.SopNode, f3h_all: bool = False) -> None:
        """Force all presets menus to update.
        This is being added so we can force the presets menus to be rebuilt
        everywhere we need to help keep them up to date in case the user
        make any hand made modifications to the loaded files.

        Args:
            (self):
            node(hou.SopNode): The FLAM3H node.
            f3h_all(bool): Perform this for all FLAM3H nodes in the scene.
            xml_last(bool): Default to: True. Update the "XML_last_loaded" node user data and its In Flame stats.
            
        Returns:
            (None):
        """  
        if f3h_all:
            f3h_instances: tuple = node.type().instances()
            [self.destroy_cachedUserData(f3h, 'cp_presets_menu') for f3h in f3h_instances]
            [self.destroy_cachedUserData(f3h, 'cp_presets_menu_off') for f3h in f3h_instances]
            [self.destroy_cachedUserData(f3h, 'in_presets_menu') for f3h in f3h_instances]
            [self.destroy_cachedUserData(f3h, 'in_presets_menu_off') for f3h in f3h_instances]
            [self.destroy_cachedUserData(f3h, 'out_presets_menu') for f3h in f3h_instances]
        else:
            self.destroy_cachedUserData(node, 'cp_presets_menu')
            self.destroy_cachedUserData(node, 'cp_presets_menu_off')
            self.destroy_cachedUserData(node, 'in_presets_menu')
            self.destroy_cachedUserData(node, 'in_presets_menu_off')
            self.destroy_cachedUserData(node, 'out_presets_menu')
            

    def update_xml_last_loaded(self) -> None:
        """Force node user data "XML_last_loaded" to update.
        It will update only if: xml and xml_isFile and xml == xml_history and inisvalidfile and inisvalidpreset and not clipboard

        Args:
            (self):
            
        Returns:
            (None):
        """  
            
        node = self.node
        
        # Updated the "XML_last_loaded" user data if there is a need to do so:
        inisvalidfile: int = node.parm(IN_PVT_ISVALID_FILE).eval()
        inisvalidpreset: int = node.parm(IN_PVT_ISVALID_PRESET).eval()
        clipboard: int = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()
        xml: str = os.path.expandvars(node.parm(IN_PATH).eval())
        xml_isFile: bool = os.path.isfile(xml)
        xml_history: str | None = node.cachedUserData('in_presets_filepath')
        # Only if a valid preset has been loaded from a disk file ( not clipboard )
        if xml and xml_isFile and xml == xml_history and inisvalidfile and inisvalidpreset and not clipboard:
            
            # Build the apo data
            preset_id: int = int(node.parm(IN_PRESETS).eval())
            apo_data = in_flame_iter_data(node, xml, preset_id)
            if apo_data.isvalidtree:
                
                old_data: str | None = node.userData(FLAM3H_USER_DATA_XML_LAST)
                now_data = lxmlET.tostring(apo_data.flame[preset_id], encoding="unicode") # type: ignore
                now_data_isvalid = _xml_tree(now_data).isvalidtree
                if old_data is not None and old_data != now_data and now_data_isvalid:
                
                    # Update user data
                    node.setUserData(FLAM3H_USER_DATA_XML_LAST, now_data) # type: ignore
                    # Update flame stats
                    node.setParms({MSG_IN_FLAMESTATS: in_flame_utils(self.kwargs).in_load_stats_msg(preset_id, apo_data, bool(clipboard))})
                    node.setParms({MSG_IN_FLAMESENSOR: in_flame_utils.in_load_sensor_stats_msg(preset_id, apo_data)})
                    node.setParms({MSG_IN_FLAMERENDER: in_flame_utils.in_load_render_stats_msg(preset_id, apo_data)})

                    _MSG_ALL = f"\"XML_last_loaded\" user data: Updated\n\nThe currently loaded IN Preset: \"{apo_data.name[preset_id]}\"\nhas been modified on disk. Reload the preset to update.\n\n-> Meanwhile,\nthe IN flame preset infos have been updated\nas well as its render properties infos."
                    _MSG_UI = f"The currently loaded IN Preset: \"{apo_data.name[preset_id]}\"\nhas been modified on disk."
                    hou.ui.displayMessage(_MSG_UI, buttons=("Got it, thank you",), severity=hou.severityType.ImportantMessage, default_choice=0, close_choice=-1, help=None, title="FLAM3H: IN flame file modified", details=_MSG_ALL, details_label=None, details_expanded=False) # type: ignore
                        
                else:
                    if old_data is None:
                        _MSG: str = f"\"XML_last_loaded\" user data: Corrupted"
                        print(f"\n-> {datetime.now().strftime('%b-%d-%Y %H:%M:%S')}\n{node.name()}: {_MSG}")
                    elif not now_data_isvalid:
                        _MSG: str = f"\"XML loaded preset\" data: Corrupted"
                        print(f"\n-> {datetime.now().strftime('%b-%d-%Y %H:%M:%S')}\n{node.name()}: {_MSG}")
            
            else:
                # Fire messages
                _MSG: str = f"\"XML_last_loaded\" user data: Failed"
                print(f"{node.name()}: {_MSG}.\n")


    def refresh_iterator_vars_menu(self) -> None:
        """Refresh the iterator (FLAME and FF tabs) menus
        to update to the new menu style mode.

        Args:
            (self):
            
        Returns:
            (None):
        """  
        node = self.node
        
        # Reset/Set density
        flam3h_general_utils.reset_density(node)
        
        if not self.node.parm(PREFS_ITERATOR_BOOKMARK_ICONS).eval():
            
            # Reset memory mpidx prm data
            flam3h_iterator_utils.iterator_mpidx_mem_set(node, 0)
            
            # Remove any comment and user data from the node
            if self.exist_user_data(node):
                self.destroy_cachedUserData(node, 'iter_sel')
                self.del_comment_and_user_data_iterator(node)
            if self.exist_user_data(node, FLAM3H_USER_DATA_FF):
                self.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)
            
            # This is the only way I found to update the FLAME tab multiparameter's menus, for now...
            node.type().definition().updateFromNode(node)
            node.matchCurrentDefinition()
            
            _MSG: str = "Iterator var menus: SIMPLE"
            flam3h_general_utils.flash_message(node, f"{_MSG}")
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
            
        else:
            self.destroy_cachedUserData(node, 'vars_menu_all_simple')
            
            # For some reasons the FF menus do not update so we force them to
            self.force_menu_var_update_FF(node)
            
            _MSG: str = "Iterator var menus: ICONS"
            flam3h_general_utils.flash_message(node, f"{_MSG}")
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
            
        # Change focus back to the FLAME's Tab
        node.parmTuple(FLAM3H_ITERATORS_TAB).set((0,))
        

    def destroy_data_note(self) -> None:
        """Update mini-menu iterator selection when we modify this parameter.
        and provide a default name if no string in a FLAME tab iterator note parameter is left.

        Args:
            (self):
            
        Returns:
            (None):
        """  
        node = self.node
        self.destroy_cachedUserData(node, 'iter_sel')
        prm = self.kwargs['parm']
        idx: int = self.kwargs['script_multiparm_index']
        if not prm.eval():
            prm.set(f"iterator_{idx}")
            
            
    def note_FF(self) -> None:
        """Provide a default name if no string in the FF tab note parameter is left.

        Args:
            (self):
            
        Returns:
            (None):
        """  
        prm = self.kwargs['parm']
        if not prm.eval():
            prm.set(f"iterator_FF")
            
        
    def menu_T_get_var_data(self) -> tuple[int, float]:
        """Get this menu variation type idx and its weight value.
        
        Args:
            (self):

        Returns:
            (tuple[int, float]): int: variation idx.    float: weight value
        """  
        _TYPE: int = self.kwargs['parm'].eval()
        idx: int = self.kwargs['script_multiparm_index']
        prm_weight_name: str = f"{str(self.kwargs['parm'].name()).split('type')[0]}weight_{idx}"
        return _TYPE, self.node.parm(prm_weight_name).eval()
    
    
    def menu_T_FF_get_var_data(self) -> tuple[int, float]:
        """Get this FF menu variation type idx and its weight value.
        
        Args:
            (self):

        Returns:
            (tuple[int, float]): int: variation idx.    float: weight value
        """  
        _TYPE: int = self.kwargs['parm'].eval()
        prm_weight_name: str = f"{ str(self.kwargs['parm'].name()).split('type')[0]}weight"
        return _TYPE, self.node.parm(prm_weight_name).eval()

    
    def menu_T_data(self) -> tuple[int, str]:
        """Rerturn the selected variation index and the correct bookmark icon to use
        based on its weight value.
        
        Args:
            (self):
            
        Returns:
            (tuple[int, str]): int: variation idx.    str: icon
        """
        _TYPE, w = self.menu_T_get_var_data()
        return _TYPE, self.menu_T_get_type_icon(w)


    def menu_T_PP_data(self) -> tuple[int, str]:
        """Rerturn the selected variation index and the correct bookmark icon to use
        based on its weight value.
        
        Args:
            (self):

        Returns:
            (tuple[int, str]): int: variation idx.    str: icon
        """
        _TYPE, w = self.menu_T_get_var_data()
        return _TYPE, self.menu_T_PP_get_type_icon(w)
    
    
    def menu_T_FF_data(self) -> tuple[int, str]:
        """Rerturn the selected FF variation index and the correct bookmark icon to use
        based on its weight value.
        
        Args:
            (self):

        Returns:
            (tuple[int, str]): int: variation idx.    str: icon
        """
        _TYPE, w = self.menu_T_FF_get_var_data()
        return _TYPE, self.menu_T_get_type_icon(w)
    
    
    def menu_T_PP_FF_data(self) -> tuple[int, str]:
        """Rerturn the selected FF variation index and the correct bookmark icon to use
        based on its weight value.
        
        Args:
            (self):

        Returns:
            (tuple[int, str]): int: variation idx.    str: icon
        """
        _TYPE, w = self.menu_T_FF_get_var_data()
        return _TYPE, self.menu_T_PP_get_type_icon(w)
    
    
    def menu_T_pb_data(self) -> str:
        """Rerturn the bookmark icon to use for the Pre blur variation
        based on its weight value.
        
        Args:
            (self):

        Returns:
            (tuple[int, str]): int: variation idx.    str: icon
        """
        idx: int = self.kwargs['script_multiparm_index']
        prm_weight_name: str = f"{flam3h_iterator_prm_names().prevar_weight_blur}_{idx}"

        w: float = self.node.parm(prm_weight_name).eval()

        if w > 0:
            if w > 1:
                return FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV_OVER_ONE
            else:
                return FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV
            
        return FLAM3H_ICON_STAR_EMPTY_OPACITY
    
    
    def menu_T_ICON(self, FF: bool = False) -> list:
        """Populate variation names parameter menu list and add proper bookmark icons based on their weights.
        Differentiate iterators and FF
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.
            
        Args:
            (self):

        Returns:
            (list): return menu list
        """
        menu: list = copy(MENU_VARS_ALL_SIMPLE)
        _TYPE, _ICON = (self.menu_T_data, self.menu_T_FF_data)[FF]()
        var: int | None = MENU_VARS_INDEXES.get(_TYPE)
        assert var is not None # I can assert this becasue I tested all of them myself ;)
        menu[var] = f"{_ICON} {menu[var][:13]}     " # 5 times \s

        return menu


    def menu_T_PP_ICON(self, FF: bool = False) -> list:
        """Populate variation names parameter menu list and add proper bookmark icons based on their weights.
        Differentiate iterators and FF
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.
            
        Args:
            (self):

        Returns:
            (list): return menu list
        """
        menu: list = copy(MENU_VARS_ALL_SIMPLE)
        _TYPE, _ICON = (self.menu_T_PP_data, self.menu_T_PP_FF_data)[FF]()
        var: int | None = MENU_VARS_INDEXES.get(_TYPE)
        assert var is not None # I can assert this becasue I tested all of them myself ;)
        menu[var] = f"{_ICON} {menu[var][:13]}     " # 5 times \s
            
        return menu
    
    
    def menu_T_simple(self, FF: bool = False) -> list:
        """Populate variation names parameter menu list.
        
        Args:
            (self):
            FF(bool): Default to False. If true it will signal we are looking to deal with data for the FF. In this specific definition the arg: FF is present only for consistency.
            
        Returns:
            (list): return menu list
        """
        self.node.setCachedUserData('vars_menu_all_simple', MENU_VARS_ALL_SIMPLE)
        return MENU_VARS_ALL_SIMPLE
    
    
    def menu_T(self, FF: bool = False) -> list:
        """Populate variation names parameter menu list.
        Differentiate iterators and FF
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.

        Args:
            (self):
            FF(bool): Default to: False. If True it will signal we are looking to deal with data for the FF.
            
        Returns:
            (list): return menu list
        """
        node = self.node
        
        # This data get created inside: menu_T_simple(self, FF: bool = False) -> list:
        # This data get destroyed inside: refresh_iterator_vars_menu(self) -> None:
        data: list | None = node.cachedUserData('vars_menu_all_simple')
        if data is not None:
            return data
        else:
            _ICONS_TOGGLE: int = node.parm(PREFS_ITERATOR_BOOKMARK_ICONS).eval()
            return (self.menu_T_simple, self.menu_T_ICON)[_ICONS_TOGGLE](FF)

    
    def menu_T_PP(self, FF: bool = False) -> list:
        """Populate variation names parameter menu list.
        Differentiate iterators and FF
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.
            
        Args:
            (self):
            FF(bool): Default to: False. If True it will signal we are looking to deal with data for the FF.

        Returns:
            (list): return menu list
        """
        node = self.node
        # This data get created inside: menu_T_simple(self, FF: bool = False) -> list:
        # This data get destroyed inside: refresh_iterator_vars_menu(self) -> None:
        data: list | None = node.cachedUserData('vars_menu_all_simple')
        if data is not None:
            return data
        else:
            _ICONS_TOGGLE: int = node.parm(PREFS_ITERATOR_BOOKMARK_ICONS).eval()
            return (self.menu_T_simple, self.menu_T_PP_ICON)[_ICONS_TOGGLE](FF)
    
    
    def menu_T_pb(self) -> list:
        """Populate variation name parameter menu list for Pre blur variation
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.
            
        Args:
            (self):

        Returns:
            (list): return menu list
        """
        _ICON = self.menu_T_pb_data()
        return [ 0,  f"{_ICON} Pre blur                   "] # 19 times \s


    def menu_select_iterator_data(self) -> list:
        """Build a menu of iterators using their states as bookmark icon

        Args:
            (self):

        Returns:
            (list): return menu list
        """
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            node = self.node
            menu: list = []

            iter_count: int = node.parm(FLAME_ITERATORS_COUNT).eval()
            if iter_count:
                
                note: list = [node.parm(f'note_{idx + 1}').eval() for idx in range(iter_count)]
                
                active: list = [node.parm(f'vactive_{idx + 1}').eval() for idx in range(iter_count)]
                weight: list = [node.parm(f'iw_{idx + 1}').eval() for idx in range(iter_count)]
                shader_opacity: list = [node.parm(f'alpha_{idx + 1}').eval() for idx in range(iter_count)]
                node.setCachedUserData('iter_sel_a', active)
                node.setCachedUserData('iter_sel_w', weight)
                node.setCachedUserData('iter_sel_o', shader_opacity)
                
                # This definition probably can be made more light-weight for this particular case
                from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)
                # Store the most updated version of this data
                node.setCachedUserData('iter_sel_id', mp_id_from)
                
                # append an empty line to reset to after selection (Null value).
                menu.append(0)
                menu.append("")
                
                for i in range(iter_count):
                    
                    idx: int = i + 1
                    menu.append(idx)

                    _OPACITY_MSG: str = ""
                    if shader_opacity[i] == 0: _OPACITY_MSG = "[ZERO opacity] "
                    
                    _ICON_IDX: int = 0
                    if node == from_FLAM3H_NODE and mp_id_from == idx: _ICON_IDX = 1 # Marked
                    
                    if active[i] and weight[i] > 0:
                        menu.append(f"{SEL_ITER_BOOKMARK_ACTIVE_AND_WEIGHT[_ICON_IDX]}  {idx}:  {_OPACITY_MSG}{note[i]}")
                            
                    elif active[i] and weight[i] == 0:
                        menu.append(f"{SEL_ITER_BOOKMARK_ACTIVE_AND_WEIGHT_ZERO[_ICON_IDX]}  {idx}:  {_OPACITY_MSG}{note[i]}")

                    else:
                        menu.append(f"{SEL_ITER_BOOKMARK_OFF[_ICON_IDX]}  {idx}:  {_OPACITY_MSG}{note[i]}")
                            
            else:
                menu = MENU_ZERO_ITERATORS
                    
            node.setCachedUserData('iter_sel', menu)
            return menu
    
    
    def menu_select_iterator(self) -> list:
        """Cache or rebuild the menu on demand.

        Args:
            (self):
            
        Returns:
            (list): return menu list
        """
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            node = self.node
            
            mem_id: int = node.parm(FLAM3H_DATA_PRM_MPIDX).eval()
            if node.cachedUserData('iter_sel_id') != mem_id and mem_id:
                self.destroy_cachedUserData(node, 'iter_sel')

            # For undos: compare old data_* against current data_*
            # Another piece for the undos to work is inside: def prm_paste_update_for_undo(self, node: hou.SopNode)
            iter_count: int = node.parm(FLAME_ITERATORS_COUNT).eval()
            data_awo_now: list = [[node.parm(f'vactive_{idx + 1}').eval() for idx in range(iter_count)], [node.parm(f'iw_{idx + 1}').eval() for idx in range(iter_count)], [node.parm(f'alpha_{idx + 1}').eval() for idx in range(iter_count)]]
            [self.destroy_cachedUserData(node, 'iter_sel') if node.cachedUserData('iter_sel') is not None and data != data_awo_now[idx] else ... for idx, data in ((0, node.cachedUserData('iter_sel_a')), (1, node.cachedUserData('iter_sel_w')), (2, node.cachedUserData('iter_sel_o')))]
            
            menu: list | None = node.cachedUserData('iter_sel')
            if menu is not None:
                return menu
            else:
                return self.menu_select_iterator_data()
        
    
    def prm_select_iterator(self) -> None:
        """Change multi-parameter index focus based on the selected iterator number from: def menu_select_iterator(self) -> list:
        
        _NOTE:
            Need to investigate more how to control the Network Editor's Parameter Dialog displayed when pressing the "p" key.
            For now, it will just do nothing and let the user know.

        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        iter_count: int = node.parm(FLAME_ITERATORS_COUNT).eval()

        if iter_count:
            
            # This definition probably can be made more light-weight for this particular case
            from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)
            
            prm = node.parm(FLAME_ITERATORS_COUNT)
            preset_id = node.parm(SYS_SELECT_ITERATOR).eval()
            
            try:
                # We first try to set them all with this
                hou.ui.setMultiParmTabInEditors(prm, preset_id-1) # type: ignore
            except:
                _CHECK = False
            else:
                _CHECK = True

            if _CHECK:
                
                # Change focus back to the FLAME's Tab
                node.parmTuple(FLAM3H_ITERATORS_TAB).set((0,))
                
                _MSG: str = f"iterator: {preset_id}"
                active: int = node.parm(f"{flam3h_iterator_prm_names().main_vactive}_{preset_id}").eval()
                weight: float = node.parm(f"{flam3h_iterator_prm_names().main_weight}_{preset_id}").eval()
                
                if node == from_FLAM3H_NODE and mp_id_from == preset_id:
                    if active and weight > 0: flam3h_general_utils.flash_message(node, f"{_MSG} (Marked)")
                    elif active and weight == 0: flam3h_general_utils.flash_message(node, f"{_MSG} (Zero Weight and Marked)")
                    else: flam3h_general_utils.flash_message(node, f"{_MSG} (Disabled and Marked)")
                    
                else:
                    if active and weight > 0: flam3h_general_utils.flash_message(node, _MSG)
                    elif active and weight == 0: flam3h_general_utils.flash_message(node, f"{_MSG} (Zero Weight)")
                    else: flam3h_general_utils.flash_message(node, f"{_MSG} (Disabled)")
                
            else:
                # If we can not set them all, lets see different cases one by one
                
                paneTab_uc = hou.ui.paneTabUnderCursor() # type: ignore

                if paneTab_uc is not None:

                    if paneTab_uc.type() == hou.paneTabType.Parm: # type: ignore
                        
                        paneTab_uc.setMultiParmTab(prm.name(), preset_id-1)
                        
                        # Change focus back to the FLAME's Tab
                        node.parmTuple(FLAM3H_ITERATORS_TAB).set((0,))
                        
                        _MSG: str = f"iterator: {preset_id}"
                        active: int = node.parm(f"{flam3h_iterator_prm_names().main_vactive}_{preset_id}").eval()
                        
                        if node == from_FLAM3H_NODE and mp_id_from == preset_id:
                            if active: flam3h_general_utils.flash_message(node, f"{_MSG} (Marked)")
                            else: flam3h_general_utils.flash_message(node, f"{_MSG} (Disabled and Marked)")
                                
                        else:
                            if active: flam3h_general_utils.flash_message(node, _MSG)
                            else: flam3h_general_utils.flash_message(node, f"{_MSG} (Disabled)")
                        
                        
                    elif paneTab_uc.type() == hou.paneTabType.NetworkEditor: # type: ignore
                        
                        # Need to investigate more how to control the floating Parameter Dialog displayed when pressing the "p" key
                        
                        #
                        if hou.isUIAvailable():
                            _MSG: str = "This feature is not working over the Network Editor's Parameter Dialog displayed when pressing the \"p\" key.\nPlease, open a Parameter Editor in its own pane tab or floating panel for this feature to work."
                            hou.ui.displayMessage(_MSG, buttons=("Got it, thank you",), severity=hou.severityType.ImportantMessage, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Select Iterator mini-menu", details=None, details_label=None, details_expanded=False) # type: ignore
                        
                        _MSG: str = "Selection do not work over Network Editors"
                        flam3h_general_utils.flash_message(node, f"{_MSG}")
                        flam3h_general_utils.set_status_msg(f"{node.name()}: Iterator's {_MSG.lower()}.", 'IMP')
                        
                    else:
                        _MSG: str = "Ops! That did not work!"
                        flam3h_general_utils.flash_message(node, f"{_MSG}")
                        flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG} The pane under the cursor must be a valid Parameter Editor pane or floating panel.", 'WARN')
                    
                else:
                    _MSG: str = "Ops! That did not work!"
                    flam3h_general_utils.flash_message(node, f"{_MSG}")
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG} The pane under the cursor must be a valid Parameter Editor pane or floating panel.", 'WARN')
        
        # reset selection to null value
        node.setParms({SYS_SELECT_ITERATOR: 0})
        
        # Force select-iterator menu update in case an iterator is marked on this FLAM3H node
        self.prm_paste_sel_iter_sel_force_update(node)
    
    
    def flam3h_paste_reset_hou_session_data(self, hipLoad: bool = False) -> None:
        """init/clear copy/paste iterator's data and prm
        
        Args:
            (self):
            hipLoad(bool): Default to False. To use when loading a hip file.
            
        Returns:
            (None):
        """
        node = self.node
        
        try:
            hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
        except:
            from_FLAM3HNODE = None
        else:
            from_FLAM3HNODE: TA_MNode = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
        
        if from_FLAM3HNODE is not None and node == from_FLAM3HNODE:  # type: ignore
            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = None # type: ignore
            # Reset internal mpidx memory to a None value
            if node.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt() != 0:
                self.iterator_mpidx_mem_set(node, 0)
            if hipLoad:
                # This is needed on hip file load to allow: def flam3h_init_hou_session_restore_from_user_data(node: hou.SopNode) -> None:
                # to rewire the FF copy/paste data properly on load, if any is present in the loaded FLAM3H nodes.
                if not self.exist_user_data(node, FLAM3H_USER_DATA_FF):
                    hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = node # type: ignore
                    hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = None # type: ignore
            else:
                hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = node # type: ignore
                hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = None # type: ignore
            # Remove any comment and user data from the node
            self.del_comment_and_user_data_iterator(node)
            self.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)
            
            
    def __menu_global_density(self) -> list:
        """ NOT USED ANYMORE
        
        Build density menu parameter with a list of options.
        This is obsolete now and replaced with: def menu_global_density(self) -> None
        
        Args:
            (self):

        Returns:
            (list): return menu list
        """
        iterators: int = self.node.parm(FLAME_ITERATORS_COUNT).eval()
        menu: list = []
        menuitems: tuple = ()
        if iterators:
            menuitems: tuple = ( "", "1M", "2M", "5M", "15M", "25M", "50M", "100M", "150M", "250M", f"{FLAM3H_ICON_STAR_HIGH_TIER}500M", f"{FLAM3H_ICON_STAR_HIGH_TIER}750M", f"{FLAM3H_ICON_STAR_HIGH_TIER}1 Billion", "" )
        else:
            menuitems: tuple = ("Please, add at least one iterator", "")
        for i, item in enumerate(menuitems):
            menu.append(i)
            menu.append(item)
    
        return menu
    
    
    def menu_global_density(self) -> list:
        """Return a pre built static menu data.
        It will use a different menu if the user is in xfomrs handles VIZ mode(ON or SOLO).

        Args:
            (self):

        Returns:
            (list): return menu list
        """
        node = self.node
        if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval(): return MENU_DENSITY
        elif node.parm(PREFS_PVT_XF_VIZ).eval():
            if node.parm(PREFS_PVT_XF_VIZ_SOLO).eval() or node.parm(PREFS_PVT_XF_FF_VIZ_SOLO).eval(): return MENU_DENSITY_XFVIZ_ON_SOLO
            else: return MENU_DENSITY_XFVIZ_ON
        else: return MENU_DENSITY_XFVIZ_OFF
    
    
    def menu_global_density_set(self) -> None:
        """Set density menu parameter based on user choice.
        
        Args:
            (self):
            
        Returns:
            (None):
        """       
        node = self.node
        ptcount: int = node.parm(GLB_DENSITY).eval()
        sel: int = self.kwargs['parm'].evalAsInt()
        vals: dict[int, int] = { 1: 500000, 2: 1000000, 3: 2000000, 4: 5000000, 5: 15000000, 6: 25000000, 7: 50000000, 8: 100000000, 9: 150000000, 10: 250000000, 11: 500000000, 12: 750000000, 13: 1000000000}
        vals_name: dict[int, str] = { 1: "Default: 500K points", 2: "1 Millions points", 3: "2 Millions points", 4: "5 Millions points", 5: "15 Millions points", 6: "25 Millions points", 7: "50 Millions points", 8: "100 Millions points", 9: "150 Millions points", 10: "250 Millions points", 11: "500 Millions points", 12: "750 Millions points", 13: "1 Billions points"}
        
        val_get: int | None = vals.get(sel)
        if val_get is not None and ptcount != val_get:
            
            node.parm(GLB_DENSITY).deleteAllKeyframes()
            node.parm(GLB_DENSITY_PRESETS).deleteAllKeyframes()
            node.setParms({GLB_DENSITY: val_get})
            
            _MSG: str = f"{node.name()} -> SET Density: {vals_name.get(sel)}"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')


    def menu_global_density_set_default(self) -> None:
        """Revert density parameter to its default value.
        Additionally give the ability to also set lower tier density presets: 300k, 200k, 100k.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        kwargs: dict = self.kwargs
        
        glb_density: int = node.parm(GLB_DENSITY).eval()
        
        # Clear keyframes
        node.parm(GLB_DENSITY).deleteAllKeyframes()
        node.parm(GLB_DENSITY_PRESETS).deleteAllKeyframes()
        
        if kwargs['shift']:
            if glb_density != 300000:
                node.setParms({GLB_DENSITY: 300000})
                node.setParms({GLB_DENSITY_PRESETS: -1})
                flam3h_general_utils.flash_message(node, 'Density: 300k')
                _MSG: str = f"{node.name()} -> SET Density: 300K points"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            else:
                _MSG: str = f"{node.name()}: Density already at: 300k points"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        elif kwargs['ctrl']:
            if glb_density != 200000:
                node.setParms({GLB_DENSITY: 200000})
                node.setParms({GLB_DENSITY_PRESETS: -1})
                flam3h_general_utils.flash_message(node, 'Density: 200k')
                _MSG: str = f"{node.name()} -> SET Density: 200K points"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            else:
                _MSG: str = f"{node.name()}: Density already at: 200k points"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        elif kwargs['alt']:
            if glb_density != 100000:
                node.setParms({GLB_DENSITY: 100000})
                node.setParms({GLB_DENSITY_PRESETS: -1})
                flam3h_general_utils.flash_message(node, 'Density: 100k')
                _MSG: str = f"{node.name()} -> SET Density: 100K points"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            else:
                _MSG: str = f"{node.name()}: Density already at: 100k points"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            
        else:
            # Default 500k
            if glb_density != FLAM3H_DEFAULT_GLB_DENSITY:
                # Reset/Set density
                flam3h_general_utils.reset_density(node)
                _MSG: str = f"{node.name()} -> SET default density preset: 500K points"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            else:
                _MSG: str = f"{node.name()}: Density already at its default value."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
    
    
    def menu_copypaste(self) -> list:
        """
        Build copy/paste parameter menu entries and eventually update its data if needed.
        This menu, together with: def menu_copypaste_FF(self) -> list: , are the only two menus not being cached for reuse.
        It is important not to play the cache/destroy data mechanism on those two because we need them to always evaluate to help us update other data as well.
        They are our sentinels and always vigilant.
        
        Args:
            (self):

        Returns:
            (list): return menu list
        """    
        menu: list= []
        
        node = self.node
        id: int = self.kwargs['script_multiparm_index']
        idx: str = str(id)
        
        if self.exist_user_data(node):
            node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore
        
        # Update data for copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)
        
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            if mp_id_from is not None:
                assert from_FLAM3H_NODE is not None
                
                idx_from: str = str(mp_id_from)
                
                prm_selmem = node.parm(f"selmem_{idx}")
                if prm_selmem.eval() > 0:
                    node.setParms({f"prmpastesel_{idx}": 0})
                    prm_selmem.set(0)
                    
                # Menu entrie sections bookmark icon
                active: int = from_FLAM3H_NODE.parm(f"vactive_{idx_from}").eval()
                weight: float = from_FLAM3H_NODE.parm(f"iw_{idx_from}").eval()
                if active and weight > 0: _ICON = FLAM3H_ICON_COPY_PASTE_ENTRIE
                elif active and weight == 0: _ICON = FLAM3H_ICON_COPY_PASTE_ENTRIE_ZERO
                else: _ICON = FLAM3H_ICON_COPY_PASTE_ENTRIE_ITER_OFF_MARKED
                
                # Build menu
                if node == from_FLAM3H_NODE and id == mp_id_from:
                    menu: list = [ 0, f"{FLAM3H_ICON_COPY_PASTE_INFO}  {idx}: MARKED\n-> Select a different iterator number or a different FLAM3H node to paste its values.", 1,"" ]
                elif node == from_FLAM3H_NODE:
                    path: str = f"{_ICON}  {idx_from}"
                    menu: list = [ 0, "", 1, f"{FLAM3H_ICON_COPY_PASTE}  All (no xaos:)", 2, f"{path}", 3, f"{path}:  xaos:", 4, f"{path}:  shader", 5, f"{path}:  PRE", 6, f"{path}:  VAR", 7, f"{path}:  POST", 8, f"{path}:  pre affine", 9, f"{path}:  post affine", 10, "" ]
                else:
                    assert from_FLAM3H_NODE is not None
                    path: str = f"{_ICON}  .../{from_FLAM3H_NODE.parent()}/{from_FLAM3H_NODE.name()}.iter.{idx_from}"
                    menu: list = [ 0, "", 1, f"{FLAM3H_ICON_COPY_PASTE}  All (no xaos:)", 2, f"{path}", 3, f"{path}:  xaos:", 4, f"{path}:  shader", 5, f"{path}:  PRE", 6, f"{path}:  VAR", 7, f"{path}:  POST", 8, f"{path}:  pre affine", 9, f"{path}:  post affine", 10, "" ]
                
                return menu
            
            else:
                if isDELETED: return MENU_ITER_COPY_PASTE_DELETED_MARKED
                else:
                    if from_FLAM3H_NODE is not None:
                        assert from_FLAM3H_NODE is not None
                        _FLAM3H_DATA_PRM_MPIDX = node.parm(FLAM3H_DATA_PRM_MPIDX).eval()
                        __FLAM3H_DATA_PRM_MPIDX = from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).eval()
                        if node == from_FLAM3H_NODE and _FLAM3H_DATA_PRM_MPIDX == -1:
                            menu: list = MENU_ITER_COPY_PASTE_REMOVED
                        elif node != from_FLAM3H_NODE and __FLAM3H_DATA_PRM_MPIDX == -1:
                            path: str = f".../{from_FLAM3H_NODE.parent()}/{from_FLAM3H_NODE.name()}"
                            menu: list = [ 0, f"{FLAM3H_ICON_COPY_PASTE_INFO_ORANGE}  REMOVED: The marked iterator has been removed from node: {path}\n-> Mark an existing iterator instead.", 1, "" ]
                        else:
                            menu: list = MENU_ITER_COPY_PASTE_EMPTY
                        return menu
                    
                    else: return MENU_ITER_COPY_PASTE_EMPTY

    
    def menu_copypaste_FF(self) -> list:
        """
        Build copy/paste FF parameter menu entries and eventually update its data if needed.
        This menu, together with: def menu_copypaste(self) -> list: , are the only two menus not being cached for reuse.
        It is important not to play the cache/destroy data mechanism on those two because we need them to always evaluate to help us update other data as well.
        They are our sentinels and always vigilant.
        
        Args:
            (self):

        Returns:
            (list): return menu list
        """    
        node = self.node
        
        # This is to make sure the hou.session's data is at least initialized.
        self.flam3h_init_hou_session_ff_data(node)
        
        # Update data for FF copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, from_FLAM3H_NODE_FF_CHECK, isDELETED = self.prm_paste_update_for_undo_ff(node)

        if from_FLAM3H_NODE_FF_CHECK is not None:

            flam3node_FF: TA_MNode = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
            
            # This undo's disabler is needed to make the undo work. They work best in H20.5
            with hou.undos.disabler(): # type: ignore
            
                if node == flam3node_FF: return MENU_FF_COPY_PASTE_SELECT
                else:
                    assert isinstance(flam3node_FF, hou.SopNode)
                    # Menu entrie sections bookmark icon
                    active: int = flam3node_FF.parm(PREFS_PVT_DOFF).eval()
                    _ICON: str = (FLAM3H_ICON_COPY_PASTE_FF_ENTRIE_OFF, FLAM3H_ICON_COPY_PASTE_FF_ENTRIE)[active]
                    
                    prm_selmem = node.parm(f"{PRX_FF_PRM}selmem")
                    if prm_selmem.eval() > 0:
                        node.setParms({f"{PRX_FF_PRM}prmpastesel": 0})
                        prm_selmem.set(0)
                    
                    path: str = f"{_ICON}  .../{flam3node_FF.parent()}/{flam3node_FF.name()}.FF"
                    return [ 0, "", 1, f"{FLAM3H_ICON_COPY_PASTE_FF}  All", 2, f"{path}:  PRE", 3, f"{path}:  VAR", 4, f"{path}:  POST", 5, f"{path}:  pre affine", 6, f"{path}:  post affine", 7, "" ]
        
        else:
            return MENU_FF_COPY_PASTE_EMPTY
        
        
    def prm_paste_update_for_undo(self, node: hou.SopNode) -> tuple[hou.SopNode | None, int | None, bool]:
        """Updated data for copy/paste iterator's methods in case of Undos.
        It will make sure that the houdini.session data about the iterator index
        will always be up to date.
        
        It is for: hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX -> UNDO, so to speak -> prm: FLAM3H_DATA_PRM_MPIDX

        Args:
            (self):
            node(hou.SopNode): the current FLAM3H node

        Returns:
            (tuple[hou.SopNode | None, int | None, bool]): 
            
            * from_FLAM3H_NODE -> is the node we are copying the data from. 
            * mp_id_from -> Multiparameter index. Is the iterator number we are copying from inside "from_FLAM3H_NODE".
            * isDELETED -> will tell us if "from_FLAM3H_NODE" still exist.
        """
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            isDELETED: bool = False
            _FLAM3H_DATA_PRM_MPIDX: int = node.parm(FLAM3H_DATA_PRM_MPIDX).eval()
                
            try:
                from_FLAM3H_NODE: TA_MNode = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore 
                assert from_FLAM3H_NODE is not None
                __FLAM3H_DATA_PRM_MPIDX = from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).eval()
            except:
                from_FLAM3H_NODE = None
                __FLAM3H_DATA_PRM_MPIDX = 0
                
            try:
                hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                mp_id_from: TA_M = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
                
                if node == from_FLAM3H_NODE:
                    if _FLAM3H_DATA_PRM_MPIDX > 0:
                        if mp_id_from != _FLAM3H_DATA_PRM_MPIDX:
                            mp_id_from = _FLAM3H_DATA_PRM_MPIDX
                            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = mp_id_from # type: ignore
                            self.del_comment_and_user_data_iterator(node)
                            self.set_comment_and_user_data_iterator(node, str(mp_id_from))
                            self.destroy_cachedUserData(node, 'iter_sel')
                    else:
                        if _FLAM3H_DATA_PRM_MPIDX == -1:
                            mp_id_from = None
                            self.del_comment_and_user_data_iterator(node)
                            self.destroy_cachedUserData(node, 'iter_sel')
                else:
                    if __FLAM3H_DATA_PRM_MPIDX > 0:
                        if mp_id_from != __FLAM3H_DATA_PRM_MPIDX:
                            mp_id_from = __FLAM3H_DATA_PRM_MPIDX
                            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = mp_id_from # type: ignore
                            assert from_FLAM3H_NODE is not None
                            self.del_comment_and_user_data_iterator(from_FLAM3H_NODE)
                            self.set_comment_and_user_data_iterator(from_FLAM3H_NODE, str(mp_id_from))
                            self.destroy_cachedUserData(node, 'iter_sel')
                        else:
                            # This is for an edge case so we dnt have marked iterators in multiple node's "select iterator" mini-menus
                            data: bool | None = node.cachedUserData('edge_case_01')
                            if _FLAM3H_DATA_PRM_MPIDX == 0 and hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX is not None and data is None: # type: ignore
                                self.destroy_cachedUserData(node, 'iter_sel')
                                # This so we dnt fall back into this case again and again.
                                node.setCachedUserData('edge_case_01', True)
                    else:
                        if __FLAM3H_DATA_PRM_MPIDX == -1:
                            mp_id_from = None
                            assert from_FLAM3H_NODE is not None
                            self.del_comment_and_user_data_iterator(from_FLAM3H_NODE)
                            self.destroy_cachedUserData(node, 'iter_sel')
                        # This is for an edge case so we dnt have marked iterators in multiple node's "select iterator" mini-menus
                        elif _FLAM3H_DATA_PRM_MPIDX == 0 and hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX is None: # type: ignore
                            try:
                                hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                            except:
                                pass
                            else:
                                self.destroy_cachedUserData(node, 'iter_sel')
                                # This so we dnt fall back into this case again and again.
                                hou.session.FLAM3H_MARKED_ITERATOR_NODE: TA_MNode = None # type: ignore
                            
            except:
                mp_id_from = None
                self.destroy_cachedUserData(node, 'iter_sel')
                # This to avoid a wrong copy/paste info message
                try:
                    # If we really deleted a node with a marked iterator
                    if hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX is not None: # type: ignore
                        isDELETED = True
                except:
                    # otherwise leave things as they are
                    pass
            
            # It happened sometime that the hou.undoGroup() break and it doesnt group operation anylonger, especially after multiple Undos.
            # The following will try to pick up the pieces and put them together to keep the copy/paste iterators data going smooth.
            #
            if mp_id_from is not None and from_FLAM3H_NODE is not None:
                # Mark, mark another node, Undo
                if node == from_FLAM3H_NODE and self.exist_user_data(from_FLAM3H_NODE) is False:
                    for f3h in node.type().instances():
                        if f3h != node and self.exist_user_data(f3h):
                            from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_ITERATOR_NODE = f3h # type: ignore
                            mp_id_from = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = self.get_user_data(f3h) # type: ignore
                            self.iterator_mpidx_mem_set(f3h, int(self.get_user_data(f3h)))
                            # Always on ourself since we dnt care about others FLAM3H nodes SYS tab's Select Iterator mini-menus
                            self.destroy_cachedUserData(node, 'iter_sel')
                            break
                # Mark, mark another node, Undo, Redo
                elif node != from_FLAM3H_NODE and self.exist_user_data(node):
                    from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_ITERATOR_NODE = node # type: ignore
                    mp_id_from = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = self.get_user_data(node) # type: ignore
                    self.iterator_mpidx_mem_set(node, int(self.get_user_data(node)))
                    self.destroy_cachedUserData(node, 'iter_sel')

            # Mark, Clear, Mark, Undo
            elif mp_id_from is None and from_FLAM3H_NODE is not None:
                if node == from_FLAM3H_NODE and self.exist_user_data(from_FLAM3H_NODE):
                    mp_id_from = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = self.get_user_data(from_FLAM3H_NODE) # type: ignore
                    self.iterator_mpidx_mem_set(from_FLAM3H_NODE, int(self.get_user_data(from_FLAM3H_NODE)))
                    self.destroy_cachedUserData(node, 'iter_sel')


            if isDELETED is False:
                if mp_id_from is not None and from_FLAM3H_NODE is not None:
                    if not self.exist_user_data(from_FLAM3H_NODE):
                        mp_id_from = None
                        self.destroy_cachedUserData(node, 'iter_sel')
            
            return from_FLAM3H_NODE, mp_id_from, isDELETED


    def prm_paste_update_for_undo_ff(self, node: hou.SopNode) -> tuple[hou.SopNode | None, int | None, bool]:
        """Updated data for copy/paste iterator's methods in case of Undos.
        It will make sure that the houdini.session data about the iterator index
        will always be up to date.
        
        It is for: hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX -> UNDO, so to speak -> prm: FLAM3H_DATA_PRM_MPIDX

        Args:
            (self):
            node(hou.SopNode): the current FLAM3H node

        Returns:
            (tuple[hou.SopNode | None, int | None, bool]): 
            
            * from_FLAM3H_NODE -> is the node we are copying the data from. 
            * from_FLAM3H_NODE_FF_CHECK -> Is the FF being marked or not".
            * isDELETED -> will tell us if "from_FLAM3H_NODE" still exist.
        """     
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            from_FLAM3H_NODE: TA_MNode = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
            from_FLAM3H_NODE_FF_CHECK: TA_M = hou.session.FLAM3H_MARKED_FF_CHECK # type: ignore
            
            isDELETED = False
            try:
                assert isinstance(from_FLAM3H_NODE, hou.SopNode)
                from_FLAM3H_NODE.type()
            except:
                from_FLAM3H_NODE_FF_CHECK = None
                from_FLAM3H_NODE = None
                isDELETED = True

            # It happened sometime that the hou.undoGroup() break and it doesnt group operation anylonger, especially after multiple Undos.
            # The following will try to pick up the pieces and put them together to keep the copy/paste FF data going smooth.
            #
            # -> def menu_copypaste_FF(self) -> list:
            if from_FLAM3H_NODE_FF_CHECK is not None and from_FLAM3H_NODE is not None:
                # Mark, mark another node, Undos
                if node == from_FLAM3H_NODE and self.exist_user_data(from_FLAM3H_NODE, FLAM3H_USER_DATA_FF) is False:
                    for f3h in node.type().instances():
                        if f3h != node and self.exist_user_data(f3h, FLAM3H_USER_DATA_FF):
                            from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_FF_NODE = f3h # type: ignore
                            from_FLAM3H_NODE_FF_CHECK = hou.session.FLAM3H_MARKED_FF_CHECK = 1  # type: ignore
                            break
                # Mark, mark another node, Undo, Redos
                elif node != from_FLAM3H_NODE and self.exist_user_data(node, FLAM3H_USER_DATA_FF):
                    from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_FF_NODE = node # type: ignore
                    from_FLAM3H_NODE_FF_CHECK = hou.session.FLAM3H_MARKED_FF_CHECK = 1  # type: ignore
            # Mark, unmark, Undos
            elif from_FLAM3H_NODE_FF_CHECK is None and from_FLAM3H_NODE is not None:
                if node == from_FLAM3H_NODE and self.exist_user_data(from_FLAM3H_NODE, FLAM3H_USER_DATA_FF):
                    from_FLAM3H_NODE_FF_CHECK = hou.session.FLAM3H_MARKED_FF_CHECK = 1  # type: ignore

            if isDELETED is False:
                if from_FLAM3H_NODE_FF_CHECK is not None and from_FLAM3H_NODE is not None:
                    if not self.exist_user_data(from_FLAM3H_NODE, FLAM3H_USER_DATA_FF):
                        from_FLAM3H_NODE_FF_CHECK = None
                        
            return from_FLAM3H_NODE, from_FLAM3H_NODE_FF_CHECK, isDELETED


    def prm_paste_CTRL(self, id: int) -> None:
        """Everything about paste iterator's data.

        Args:
            (self):
            id(int): current multi parameter index

        Returns:
            (None):
        """    
        node = self.node
        # Update data for copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)
                
        if mp_id_from is not None:
            
            idx: str = str(id)
            idx_from: str = str(mp_id_from)
            
            if node == from_FLAM3H_NODE and id == mp_id_from:
                _MSG: str = f"{node.name()}: This iterator is marked: {idx_from} -> Select a different iterator number or a different FLAM3H node to paste its values."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"This iterator is Marked")
            else:
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator().allT, flam3h_varsPRM().varsPRM, idx, idx_from)
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator().allMisc, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_ALL, idx, idx_from)

        else:
            if isDELETED:
                _MSG_DEL: str = "Marked iterator's node has been deleted"
                _MSG: str = f"{node.name()}: {_MSG_DEL} -> {MARK_ITER_MSG_STATUS_BAR}"
                flam3h_general_utils.set_status_msg(_MSG, 'WARN') 
                flam3h_general_utils.flash_message(node, _MSG_DEL)
                
            else:
                _MSG_REM: str = "Marked iterator has been removed"
                if node == from_FLAM3H_NODE:
                    _FLAM3H_DATA_PRM_MPIDX = node.parm(FLAM3H_DATA_PRM_MPIDX).eval()
                    if _FLAM3H_DATA_PRM_MPIDX == -1:
                        _MSG: str = f"{node.name()} -> {_MSG_REM} -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, _MSG_REM)
                    else:
                        _MSG: str = f"{node.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, MARK_ITER_MSG)
                        
                elif node != from_FLAM3H_NODE:
                    assert from_FLAM3H_NODE is not None
                    __FLAM3H_DATA_PRM_MPIDX = from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).eval()
                    
                    if __FLAM3H_DATA_PRM_MPIDX == -1:
                        _MSG: str = f"{node.name()} -> {_MSG_REM} from node: {from_FLAM3H_NODE.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, _MSG_REM)
                    else:
                        _MSG: str = f"{node.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, MARK_ITER_MSG)
                        
                else:
                    _MSG: str = f"{node.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                    flam3h_general_utils.flash_message(node, MARK_ITER_MSG)


    def prm_paste_SHIFT(self, id: int) -> None:
        """Everything about unmarking iterators from being copied.

        Args:
            (self):
            id(int): current multi parameter index

        Returns:
            (None):
        """   
        node = self.node
        # Update data for copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)

        if node == from_FLAM3H_NODE: # type: ignore
            
            _MSG_UNMARKED = "This iterator is Unmarked already"
            assert from_FLAM3H_NODE is not None
            
            if mp_id_from is not None:
                _MSG: str = f"{node.name()}: iterator UNMARKED: {str(mp_id_from)}" # type: ignore
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = None # type: ignore
                self.iterator_mpidx_mem_set(node, 0)
                self.del_comment_and_user_data_iterator(node)
                
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                flam3h_general_utils.flash_message(node, f"UNMARKED")
                
            else:
                if from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).eval() == -1:
                    _MSG: str = f"{node.name()}: {_MSG_UNMARKED}:  {str(id)}   Unmarked removed iterator -> {str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}" # type: ignore
                else:
                    _MSG: str = f"{node.name()}: {_MSG_UNMARKED} -> {str(id)}"
                    
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = None # type: ignore
                self.iterator_mpidx_mem_set(node, 0)
                self.del_comment_and_user_data_iterator(node)
                
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        else:
            if isDELETED:
                _MSG_DEL: str = "Marked iterator's node has been deleted"
                _MSG: str = f"{node.name()}: {_MSG_DEL}. Mark a new iterator first."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, _MSG_DEL)
                
            else:
                assert from_FLAM3H_NODE is not None
                __FLAM3H_DATA_PRM_MPIDX = from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).eval()
                
                if __FLAM3H_DATA_PRM_MPIDX == -1:
                    _MSG: str = f"{node.name()}: {_MSG_UNMARKED} -> The marked iterator has been removed from node: {from_FLAM3H_NODE.name()} ->  Mark an existing iterator instead." # type: ignore
                    flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                else:
                    _MSG: str = f"{node.name()}: {_MSG_UNMARKED} -> The marked iterator is from node: {from_FLAM3H_NODE.name()}.iterator.{str(mp_id_from)}" # type: ignore
                    flam3h_general_utils.set_status_msg(_MSG, 'IMP')
        

    def prm_paste_CLICK(self, id: int) -> None:
        """Everything about marking iterators for being copied.

        Args:
            (self):
            id(int): current multi parameter index

        Returns:
            (None):
        """
        node = self.node
        # Update data for copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)
                
        if self.exist_user_data(node):
            if node.isGenericFlagSet(hou.nodeFlag.DisplayComment) is False: # type: ignore
                node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore

        if node == hou.session.FLAM3H_MARKED_ITERATOR_NODE: # type: ignore
            
            if hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX != id: # type: ignore
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = id # type: ignore
                hou.session.FLAM3H_MARKED_ITERATOR_NODE: TA_MNode = self.node # type: ignore
                self.iterator_mpidx_mem_set(node, id)
                self.del_comment_and_user_data_iterator(node)
                self.set_comment_and_user_data_iterator(node, str(id))
                
                _MSG: str = f"{self.node.name()}: iterator MARKED:  {str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}" # type: ignore
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                flam3h_general_utils.flash_message(node, f"{str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}: MARKED") # type: ignore
                
            else:
                self.iterator_mpidx_mem_set(node, id)
                self.del_comment_and_user_data_iterator(node)
                self.set_comment_and_user_data_iterator(node, str(id))
                
                _MSG: str = f"{self.node.name()}: This iterator is already Marked." # type: ignore
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                
        else:
            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = id # type: ignore
            hou.session.FLAM3H_MARKED_ITERATOR_NODE: TA_MNode = self.node # type: ignore
            self.iterator_mpidx_mem_set(node, id)
            self.del_comment_and_user_data_iterator(node)
            self.set_comment_and_user_data_iterator(node, str(id))
            
            # Reset the other node mp_idx data
            if from_FLAM3H_NODE is not None:
                self.iterator_mpidx_mem_set(from_FLAM3H_NODE, 0)
                self.del_comment_and_user_data_iterator(from_FLAM3H_NODE)
                
            _MSG: str = f"{self.node.name()}: iterator MARKED:  {str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}" # type: ignore
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"{str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}: MARKED") # type: ignore


    def prm_paste(self) -> None:
        """Paste the entire iterator's data.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        
        node = self.node
        # Clear menu cache
        self.destroy_cachedUserData(node, 'iter_sel')
        
        id: int = self.kwargs['script_multiparm_index']
        
        # This is to make sure the hou.session's data is at least initialized.
        self.flam3h_init_hou_session_iterator_data(node)
        
        # Adding ability to reset the current iterator to its default values. 
        if self.kwargs["ctrl"]:
            with hou.undos.group(f"FLAM3H reset iterator {id}"): # type: ignore
                self.flam3h_reset_iterator()
                _MSG: str = f"{node.name()}: Iterator {id} -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        elif self.kwargs["shift"]:
            with hou.undos.group(f"FLAM3H unmark iterator SHIFT {id}"): # type: ignore
                self.destroy_cachedUserData_all_f3h(node, 'edge_case_01')
                self.prm_paste_SHIFT(id)
                     
        elif self.kwargs["alt"]:
            with hou.undos.group(f"FLAM3H paste iterator data CTRL {id}"): # type: ignore
                self.prm_paste_CTRL(id)
        
        else:
            if self.exist_user_data(node) and int(self.get_user_data(node)) == id and id == hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX and node == hou.session.FLAM3H_MARKED_ITERATOR_NODE: # type: ignore
                with hou.undos.group(f"FLAM3H unmark iterator CLICK {id}"): # type: ignore
                    self.destroy_cachedUserData_all_f3h(node, 'edge_case_01')
                    self.prm_paste_SHIFT(id)
            else:
                with hou.undos.group(f"FLAM3H mark iterator CLICK {id}"): # type: ignore
                    self.destroy_cachedUserData_all_f3h(node, 'edge_case_01')
                    self.prm_paste_CLICK(id)
    
    
    def prm_paste_FF_CTRL(self) -> None:
        """Everything about paste FF's data.

        Args:
            (self):
            
        Returns:
            (None):
        """    
        node = self.node
        # Update data for FF copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, from_FLAM3H_NODE_FF_CHECK, isDELETED = self.prm_paste_update_for_undo_ff(node)
            
        if from_FLAM3H_NODE_FF_CHECK is not None:
            
            if node == from_FLAM3H_NODE:
                _MSG: str = f"{node.name()}: This FF is marked. Select a different FLAM3H node's FF to paste its values."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"Select a different FLAM3H node's FF")
            else:
                f3h_iter_FF = flam3h_iterator_FF()
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_prevarsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), "", "")
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_varsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM).varsPRM_FF(), "", "")
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_postvarsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), "", "")
                self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.allMisc_FF, "", "")
                self.paste_set_note(node, from_FLAM3H_NODE, 1, SEC_ALL, "", "")

        else:
            if isDELETED:
                _MSG: str = f"{node.name()}: Marked FF's node has been deleted -> {MARK_FF_MSG_STATUS_BAR}"
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"Marked FF's node has been deleted")
            else:
                _MSG: str = f"{node.name()} -> {MARK_FF_MSG_STATUS_BAR}"
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, MARK_FF_MSG)
    
    
    def prm_paste_FF_SHIFT(self) -> None:
        """Everything about unmarking FF from being copied.

        Args:
            (self):
            
        Returns:
            (None):
        """  
        node = self.node
        # Update data for FF copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, from_FLAM3H_NODE_FF_CHECK, isDELETED = self.prm_paste_update_for_undo_ff(node)
            
        if from_FLAM3H_NODE_FF_CHECK is not None: # type: ignore
            if node == from_FLAM3H_NODE:
                assert from_FLAM3H_NODE is not None
                _MSG: str = f"{node.name()}: FF UNMARKED: {from_FLAM3H_NODE.name()}.FF" # type: ignore
                hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = None # type: ignore
                hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = node # type: ignore
                
                self.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)
                
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                flam3h_general_utils.flash_message(node, f"FF UNMARKED")
            else:
                _MSG: str = f"{node.name()}: This FF is Unmarked already. The marked FF is from node: {str(hou.session.FLAM3H_MARKED_FF_NODE)}.FF" # type: ignore
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
        else:
            if isDELETED:
                _MSG: str = f"{node.name()}: Marked FF's node has been deleted. Mark a new FF first."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            else:
                _MSG: str = f"{node.name()}: This FF is Unmarked already"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')


    def prm_paste_FF_CLICK(self) -> None:
        """Everything about marking FF for being copied.

        Args:
            (self):
            
        Returns:
            (None):
        """ 
        node = self.node
        # Update data for FF copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, from_FLAM3H_NODE_FF_CHECK, isDELETED = self.prm_paste_update_for_undo_ff(node)
        
        if self.exist_user_data(node, FLAM3H_USER_DATA_FF):
            if node.isGenericFlagSet(hou.nodeFlag.DisplayComment) is False: # type: ignore
                node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore
            
        if from_FLAM3H_NODE_FF_CHECK and node == from_FLAM3H_NODE:
            _MSG: str = f"{self.node.name()}: This FF is already Marked." # type: ignore
            flam3h_general_utils.set_status_msg(_MSG, 'MSG')

        else:
            # Remove the FF data and comment from the other node
            if from_FLAM3H_NODE is not None:
                
                self.del_comment_and_user_data_iterator(from_FLAM3H_NODE, FLAM3H_USER_DATA_FF)
                
            hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = 1 # type: ignore
            hou.session.FLAM3H_MARKED_FF_NODE: TA_MNode = self.node # type: ignore
            
            self.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)
            self.set_comment_and_user_data_iterator(node, "Yes", FLAM3H_USER_DATA_FF)
            
            _MSG: str = f"{self.node.name()}: FF MARKED" # type: ignore
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"FF MARKED")


    def prm_paste_FF(self) -> None:
        """Paste the entire FF data.
        
        Args:
            (self):
            
        Returns:
            (None):
        """   
        
        node = self.node
        # This is to make sure the hou.session's data is at least initialized.
        self.flam3h_init_hou_session_ff_data(node)
        
        # Adding ability to reset the FF to its default values. 
        if self.kwargs["ctrl"]:
            with hou.undos.group(f"FLAM3H FF RESET"): # type: ignore
                self.flam3h_reset_FF()
                _MSG: str = f"{node.name()}: FF RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                
        elif self.kwargs["shift"]:
            with hou.undos.group(f"FLAM3H unmark FF SHIFT"): # type: ignore
                self.prm_paste_FF_SHIFT()

        elif self.kwargs["alt"]:
            with hou.undos.group(f"FLAM3H paste FF data CTRL"): # type: ignore
                self.prm_paste_FF_CTRL()
        
        else:
            if self.exist_user_data(node, FLAM3H_USER_DATA_FF) and hou.session.FLAM3H_MARKED_FF_CHECK is not None and node == hou.session.FLAM3H_MARKED_FF_NODE: # type: ignore
                with hou.undos.group(f"FLAM3H unmark FF CLICK"): # type: ignore
                    self.prm_paste_FF_SHIFT()
            else:
                with hou.undos.group(f"FLAM3H mark FF CLICK"): # type: ignore
                    self.prm_paste_FF_CLICK()


    def prm_paste_sel_iter_sel_force_update(self, node: hou.SopNode) -> None:
        """Force select-iterator menu update in case an iterator is marked on this FLAM3H node.
        This is being added to deal with a mismatch during undos.
        
        Args:
            (self):
            node(hou.SopNode): This FLAM3H node

        Returns:
            (None):
        """   
        try:
            if hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX is not None and hou.session.FLAM3H_MARKED_ITERATOR_NODE == node: # type: ignore
                self.destroy_cachedUserData(node, 'iter_sel')
                self.destroy_cachedUserData_all_f3h(node, 'edge_case_01')
        except:
            pass


    def prm_paste_sel(self) -> None:
        """Paste only sections of an iterator.
        
        Args:
            (self):

        Returns:
            (None):
        """    

        node = self.node
        
        # Marked iterator ( not needed but just in case lets "try" so to speak )
        try: mp_id_from: TA_M = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
        except: mp_id_from = None

        if mp_id_from is not None:

            # current iterator
            id: int = self.kwargs['script_multiparm_index']
            idx = str(id)
            idx_from = str(mp_id_from)
            
            # prm names
            n = flam3h_iterator_prm_names()

            # Marked iterator node
            from_FLAM3H_NODE: TA_MNode = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
            assert isinstance(from_FLAM3H_NODE, hou.SopNode)
            
            # Get user selection of paste methods
            paste_sel: int = node.parm(f"{n.main_prmpastesel}_{idx}").eval()
            node.setParms({f"{n.main_selmem}_{idx}": paste_sel})

            f3h_iter = flam3h_iterator()
            varsPRM = flam3h_varsPRM().varsPRM
            
            match paste_sel:
                
                # set ALL
                case 1:
                    self.prm_paste_CTRL(id)
                # set MAIN
                case 2:
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_main, idx, idx_from)
                    self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_MAIN, idx, idx_from)
                # set XML_XF_XAOS
                case 3:
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_xaos, idx, idx_from)
                    self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_XAOS, idx, idx_from)
                # set SHADER 
                case 4:
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_shader, idx, idx_from)
                    self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_SHADER, idx, idx_from)
                # set PRE VARS
                case 5:
                    self.pastePRM_T_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_prevarsT, varsPRM, idx, idx_from)
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_prevarsW, idx, idx_from)
                    self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_PREVARS, idx, idx_from)
                # set VARS
                case 6:
                    self.pastePRM_T_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_varsT, varsPRM, idx, idx_from)
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_varsW, idx, idx_from)
                    self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_VARS, idx, idx_from)
                # set POST VARS
                case 7:
                    self.pastePRM_T_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_postvarsT, varsPRM, idx, idx_from)
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_postvarsW, idx, idx_from)
                    self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_POSTVARS, idx, idx_from)
                # set PRE AFFINE
                case 8:
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_preAffine, idx, idx_from)
                    if not self.is_iterator_affine_default(node, from_FLAM3H_NODE, f3h_iter.sec_preAffine, idx, idx_from):
                        self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_PREAFFINE, idx, idx_from)
                # set POST AFFINE
                case 9:
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter.sec_postAffine, idx, idx_from)
                    if not self.is_iterator_affine_default(node, from_FLAM3H_NODE, f3h_iter.sec_postAffine, idx, idx_from, True):
                        self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_POSTAFFINE, idx, idx_from)
                        
        
            node.setParms({f"{n.main_prmpastesel}_{idx}": 0})
            node.setParms({f"{n.main_selmem}_{idx}": paste_sel})
            
            # Force select-iterator menu update in case an iterator is marked on this FLAM3H node
            self.prm_paste_sel_iter_sel_force_update(node)
            
        else:
            _MSG: str = f"{node.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            

    def prm_paste_sel_pre_affine(self) -> None:
        """Copy/Paste POST affine inside the PRE affine.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        # current iterator
        id: int = self.kwargs['script_multiparm_index']
        idx = str(id)
        kwargs: dict = self.kwargs
        
        f3h_iter = flam3h_iterator()
        if kwargs['shift']:
            self.paste_from_list_affine(self.node, f3h_iter.sec_postAffine[1:-2], f3h_iter.sec_preAffine[:-2], idx)
            _MSG: str = f"iterator.{id} - POST affine X and Y copied into the PRE affine."
        elif kwargs['ctrl']:
            self.paste_from_list_affine(self.node, f3h_iter.sec_postAffine[3:-1], f3h_iter.sec_preAffine[2:-1], idx)
            _MSG: str = f"iterator.{id} - POST affine Offset copied into the PRE affine."
        elif kwargs['alt']:
            self.paste_from_list_affine(self.node, f3h_iter.sec_postAffine[4:], f3h_iter.sec_preAffine[3:], idx)
            _MSG: str = f"iterator.{id} - POST affine Rotation angle copied into the PRE affine."
        else:
            self.paste_from_list_affine(self.node, f3h_iter.sec_postAffine[1:], f3h_iter.sec_preAffine, idx)
            _MSG: str = f"iterator.{id} - POST affine values copied into the PRE affine."
        flam3h_general_utils.set_status_msg(f"{self.node.name()}: {_MSG}", 'IMP')
        
        
    def prm_paste_sel_post_affine(self) -> None:
        """Copy/Paste PRE affine inside the POST affine.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        # current iterator
        id: int = self.kwargs['script_multiparm_index']
        idx = str(id)
        kwargs: dict = self.kwargs
        
        f3h_iter = flam3h_iterator()
        if kwargs['shift']:
            self.paste_from_list_affine(self.node, f3h_iter.sec_preAffine[:-2], f3h_iter.sec_postAffine[1:-2], idx)
            _MSG: str = f"iterator.{id} - PRE affine X and Y copied into the POST affine."
        elif kwargs['ctrl']:
            self.paste_from_list_affine(self.node, f3h_iter.sec_preAffine[2:-1], f3h_iter.sec_postAffine[3:-1], idx)
            _MSG: str = f"iterator.{id} - PRE affine Offset copied into the POST affine."
        elif kwargs['alt']:
            self.paste_from_list_affine(self.node, f3h_iter.sec_preAffine[3:], f3h_iter.sec_postAffine[4:], idx)
            _MSG: str = f"iterator.{id} - PRE affine Rotation angle copied into the POST affine."
        else:
            self.paste_from_list_affine(self.node, f3h_iter.sec_preAffine, f3h_iter.sec_postAffine[1:], idx)
            _MSG: str = f"iterator.{id} - PRE affine values copied into the POST affine."
        flam3h_general_utils.set_status_msg(f"{self.node.name()}: {_MSG}", 'IMP')
        
        
    def prm_paste_sel_pre_affine_FF(self) -> None:
        """Paste only either the FF POST affine.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        kwargs: dict = self.kwargs
        
        f3h_iter_FF = flam3h_iterator_FF()
        if kwargs['shift']:
            self.paste_from_list_affine(self.node, f3h_iter_FF.sec_postAffine_FF[1:-2], f3h_iter_FF.sec_preAffine_FF[:-2], "")
            _MSG: str = f"iterator.{id} - FF POST affine X and Y copied into the FF PRE affine."
        elif kwargs['ctrl']:
            self.paste_from_list_affine(self.node, f3h_iter_FF.sec_postAffine_FF[3:-1], f3h_iter_FF.sec_preAffine_FF[2:-1], "")
            _MSG: str = f"iterator.{id} - FF POST affine Offset copied into the FF PRE affine."
        elif kwargs['alt']:
            self.paste_from_list_affine(self.node, f3h_iter_FF.sec_postAffine_FF[4:], f3h_iter_FF.sec_preAffine_FF[3:], "")
            _MSG: str = f"iterator.{id} - FF POST affine Rotation angle copied into the FF PRE affine."
        else:
            self.paste_from_list_affine(self.node, f3h_iter_FF.sec_postAffine_FF[1:], f3h_iter_FF.sec_preAffine_FF, "")
            _MSG: str = f"iterator.{id} - FF POST affine values copied into the FF PRE affine."
        flam3h_general_utils.set_status_msg(f"{self.node.name()}: {_MSG}", 'IMP')
        
        
    def prm_paste_sel_post_affine_FF(self) -> None:
        """Paste only either the FF PRE affine.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        kwargs: dict = self.kwargs
        
        f3h_iter_FF = flam3h_iterator_FF()
        if kwargs['shift']:
            self.paste_from_list_affine(self.node, f3h_iter_FF.sec_preAffine_FF[:-2], f3h_iter_FF.sec_postAffine_FF[1:-2], "")
            _MSG: str = f"iterator.{id} - FF PRE affine X and Y copied into the FF POST affine."
        elif kwargs['ctrl']:
            self.paste_from_list_affine(self.node, f3h_iter_FF.sec_preAffine_FF[2:-1], f3h_iter_FF.sec_postAffine_FF[3:-1], "")
            _MSG: str = f"iterator.{id} - FF PRE affine Offset copied into the FF POST affine."
        elif kwargs['alt']:
            self.paste_from_list_affine(self.node, f3h_iter_FF.sec_preAffine_FF[3:], f3h_iter_FF.sec_postAffine_FF[4:], "")
            _MSG: str = f"iterator.{id} - FF PRE affine Rotation angle copied into the FF POST affine."
        else:
            self.paste_from_list_affine(self.node, f3h_iter_FF.sec_preAffine_FF, f3h_iter_FF.sec_postAffine_FF[1:], "")
            _MSG: str = f"iterator.{id} - FF PRE affine values copied into the FF POST affine."
        flam3h_general_utils.set_status_msg(f"{self.node.name()}: {_MSG}", 'IMP')
            
            
    def prm_paste_sel_FF(self) -> None:
        """Paste only sections of a FF.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        
        node = self.node

        # Marked FF check ( not needed but just in case lets "try" so to speak )
        try: from_FLAM3H_NODE_FF_CHECK: TA_M = hou.session.FLAM3H_MARKED_FF_CHECK # type: ignore
        except: from_FLAM3H_NODE_FF_CHECK = None
            
        if from_FLAM3H_NODE_FF_CHECK is not None:
            
            # Marked FF node
            from_FLAM3H_NODE: TA_MNode = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
            assert isinstance(from_FLAM3H_NODE, hou.SopNode)
            
            # Get user selection of paste methods
            paste_sel_FF: int = node.parm(f"{PRX_FF_PRM}{flam3h_iterator_prm_names().main_prmpastesel}").eval()
            node.setParms({f"{PRX_FF_PRM}{flam3h_iterator_prm_names().main_selmem}": paste_sel_FF})
            
            f3h_iter_FF = flam3h_iterator_FF()
            
            match paste_sel_FF:
                
                # set FF ALL
                case 1:
                    self.prm_paste_FF_CTRL()
                # set FF PRE VARS
                case 2:
                    self.pastePRM_T_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_prevarsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), "", "")
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_prevarsW_FF, "", "")
                    self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_PREVARS, "", "")
                # set FF VARS
                case 3:
                    self.pastePRM_T_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_varsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM).varsPRM_FF(), "", "")
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_varsW_FF, "", "")
                    self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_VARS, "", "")
                # set FF POST VARS
                case 4:
                    self.pastePRM_T_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_postvarsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), "", "")
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_postvarsW_FF, "", "")
                    self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_POSTVARS, "", "")
                # set FF PRE AFFINE
                case 5:
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_preAffine_FF, "", "")
                    if not self.is_FF_affine_default(node, from_FLAM3H_NODE, f3h_iter_FF.sec_preAffine_FF):
                        self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_PREAFFINE, "", "")
                # set FF POST AFFINE
                case 6:
                    self.paste_from_list(node, from_FLAM3H_NODE, f3h_iter_FF.sec_postAffine_FF, "", "")
                    if not self.is_FF_affine_default(node, from_FLAM3H_NODE, f3h_iter_FF.sec_postAffine_FF, True):
                        self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_POSTAFFINE, "", "")

            node.setParms({f"{PRX_FF_PRM}{flam3h_iterator_prm_names().main_prmpastesel}": 0})
                    
        else:
            _MSG: str = f"{node.name()} -> {MARK_FF_MSG_STATUS_BAR}"
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            

    def flam3h_xaos_convert(self) -> None:
        """Here I am using a class function call from: out_flame_utils.out_xf_xaos_from()
        down below inside the save XML/FLAME file section of this file.
        The class function: out_flame_utils.out_xf_xaos_from(0) convert xaos from TO to FROM and back in one call.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        autodiv: int = node.parm(PREFS_PVT_XAOS_AUTO_SPACE).eval()
        div_xaos: str = 'xaos:'
        div_weight: str = ':'
        if autodiv:
            div_xaos = 'xaos :'
            div_weight = ' :'
        
        # Get xaos
        f3d = out_flame_utils(self.kwargs)
        # Convert xaos
        xaos_new = f3d.out_xf_xaos_from(0)
        # update CachedUserData: flam3h_xaos_iterators_prev
        self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_new)
        prm_xaos = flam3h_iterator_prm_names().xaos
        [node.setParms({f"{prm_xaos}_{str(idx + 1)}": div_xaos + div_weight.join(xaos_new[idx].split())}) if xaos_new[idx] else node.setParms({f"{prm_xaos}_{str(idx + 1)}": div_xaos}) for idx in range(f3d.iter_count)]

        # for idx in range(f3d.iter_count):
        #     if xaos_new[idx]:
        #         xs = div_xaos + div_weight.join(xaos_new[idx].split())
        #         node.setParms({f"{prm_xaos}_{str(idx + 1)}": xs})
        #     else:
        #         # I dnt think this is needed anymore but i leave it here.
        #         node.setParms({f"{prm_xaos}_{str(idx + 1)}": div_xaos})

        # Get preference xaos mode and print to Houdini's status bar
        if f3d.xm:
            _MSG: str = f"{node.name()}: XAOS Mode: FROM"
        else:
            _MSG: str = f"{node.name()}: XAOS Mode: TO"
        flam3h_general_utils.set_status_msg(_MSG, 'IMP')


    def reset_preaffine(self) -> None:
        """Reset an iterator pre affine values to their defaults.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        n = flam3h_iterator_prm_names()
        id: int = self.kwargs['script_multiparm_index']
        idx = str(id)
        check = True
        
        current: dict = { "affine_x": node.parmTuple(f"{n.preaffine_x}_{idx}"), "affine_y": node.parmTuple(f"{n.preaffine_y}_{idx}"), "affine_o": node.parmTuple(f"{n.preaffine_o}_{idx}"), "angle": node.parm(f"{n.preaffine_ang}_{idx}") }
        
        if self.kwargs["shift"]:
            current["affine_x"].deleteAllKeyframes()
            current["affine_y"].deleteAllKeyframes()
            for key in list(AFFINE_DEFAULTS.keys())[:1]:
                if current[key].eval() != AFFINE_DEFAULTS.get(key):
                    check = False
                    # pre affine
                    current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                    current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                    # Print to Houdini's status bar
                    _MSG: str = f"{node.name()}: Iterator.{idx} PRE Affine X, Y -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    break
            if check:
                _MSG: str = f"{node.name()}: Iterator.{idx} PRE Affine X, Y -> already at their default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        elif self.kwargs["ctrl"]:
            current["affine_o"].deleteAllKeyframes()
            if current["affine_o"].eval() != AFFINE_DEFAULTS.get("affine_o"):
                check = False
                current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                # Print to Houdini's status bar
                _MSG: str = f"{node.name()}: Iterator.{idx} PRE Affine O -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            if check:
                _MSG: str = f"{node.name()}: Iterator.{idx} PRE Affine O -> already at its default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        elif self.kwargs["alt"]:
            current["angle"].deleteAllKeyframes()
            if current["angle"].eval() != AFFINE_DEFAULTS.get("angle"):
                check = False
                current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                # Print to Houdini's status bar
                _MSG: str = f"{node.name()}: Iterator.{idx} PRE Affine Rotation Angle -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            if check:
                _MSG: str = f"{node.name()}: Iterator.{idx} PRE Affine Rotation Angle -> already at its default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            
        else:
            [prm.deleteAllKeyframes() for prm in current.values()]
            for key in list(AFFINE_DEFAULTS.keys()):
                if current[key].eval() != AFFINE_DEFAULTS[key]:
                    check = False
                    # pre affine
                    current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                    current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                    current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                    current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                    # Print to Houdini's status bar
                    _MSG: str = f"{node.name()}: Iterator.{idx} PRE Affine -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    break
            if check:
                _MSG: str = f"{node.name()}: Iterator.{idx} PRE Affine -> already at their default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')


    def reset_postaffine(self) -> None:
        """Reset an iterator post affine values to their defaults.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        n = flam3h_iterator_prm_names()
        id: int = self.kwargs['script_multiparm_index']
        idx = str(id)
        
        if node.parm(f"{n.postaffine_do}_{idx}").eval(): # This can be omitted as the post affine tab wont be accessible if this toggle is off.
                
            check: bool = True
            current: dict = { "affine_x": node.parmTuple(f"{n.postaffine_x}_{idx}"), "affine_y": node.parmTuple(f"{n.postaffine_y}_{idx}"), "affine_o": node.parmTuple(f"{n.postaffine_o}_{idx}"), "angle": node.parm(f"{n.postaffine_ang}_{idx}") }
            
            if self.kwargs["shift"]:
                current["affine_x"].deleteAllKeyframes()
                current["affine_y"].deleteAllKeyframes()
                for key in list(AFFINE_DEFAULTS.keys())[:1]:
                    if current[key].eval() != AFFINE_DEFAULTS[key]:
                        check = False
                        # pre affine
                        current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                        current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                        # Print to Houdini's status bar
                        _MSG: str = f"{node.name()}: Iterator.{idx} POST Affine X, Y -> RESET"
                        flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                        break
                if check:
                    _MSG: str = f"{node.name()}: Iterator.{idx} POST Affine X, Y -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    
            elif self.kwargs["ctrl"]:
                current["affine_o"].deleteAllKeyframes()
                if current["affine_o"].eval() != AFFINE_DEFAULTS.get("affine_o"):
                    check = False
                    current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                    # Print to Houdini's status bar
                    _MSG: str = f"{node.name()}: Iterator.{idx} POST Affine O -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                if check:
                    _MSG: str = f"{node.name()}: Iterator.{idx} POST Affine O -> already at its default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    
            elif self.kwargs["alt"]:
                current["angle"].deleteAllKeyframes()
                if current["angle"].eval() != AFFINE_DEFAULTS.get("angle"):
                    check = False
                    # post affine
                    current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                    # Print to Houdini's status bar
                    _MSG: str = f"{node.name()}: Iterator.{idx} POST Affine Rotation Angle -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                if check:
                    _MSG: str = f"{node.name()}: Iterator.{idx} POST Affine Rotation Angle -> already at its default value."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
            else:
                [prm.deleteAllKeyframes() for prm in current.values()]
                for key in list(AFFINE_DEFAULTS.keys()):
                    if current[key].eval() != AFFINE_DEFAULTS[key]:
                        check = False
                        # post affine
                        current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                        current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                        current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                        current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                        # Print to Houdini's status bar
                        _MSG: str = f"{node.name()}: Iterator.{idx} POST Affine -> RESET"
                        flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                        break
                if check:
                    _MSG: str = f"{node.name()}: Iterator.{idx} POST Affine -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
        
        
    def reset_preaffine_FF(self) -> None:
        """Reset FF pre affine values to their defaults.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        n = flam3h_iterator_prm_names()
        check: bool = True
        
        current: dict = { "affine_x": node.parmTuple(f"{PRX_FF_PRM}{n.preaffine_x}"), "affine_y": node.parmTuple(f"{PRX_FF_PRM}{n.preaffine_y}"), "affine_o": node.parmTuple(f"{PRX_FF_PRM}{n.preaffine_o}"), "angle": node.parm(f"{PRX_FF_PRM}{n.preaffine_ang}") }

        if self.kwargs["shift"]:
            current["affine_x"].deleteAllKeyframes()
            current["affine_y"].deleteAllKeyframes()
            for key in list(AFFINE_DEFAULTS.keys())[:1]:
                if current[key].eval() != AFFINE_DEFAULTS[key]:
                    check = False
                    # pre affine
                    current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                    current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                    # Print to Houdini's status bar
                    _MSG: str = f"{node.name()}: FF PRE Affine X, Y -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    break
            if check:
                _MSG: str = f"{node.name()}: FF PRE Affine X, Y -> already at their default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')

        elif self.kwargs["ctrl"]:
            current["affine_o"].deleteAllKeyframes()
            if current["affine_o"].eval() != AFFINE_DEFAULTS.get("affine_o"):
                check = False
                current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                # Print to Houdini's status bar
                _MSG: str = f"{node.name()}: FF PRE Affine O -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            if check:
                _MSG: str = f"{node.name()}: FF PRE Affine O -> already at its default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        elif self.kwargs["alt"]:
            current["angle"].deleteAllKeyframes()
            if current["angle"].eval() != AFFINE_DEFAULTS.get("angle"):
                check = False
                current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                # Print to Houdini's status bar
                _MSG: str = f"{node.name()}: FF PRE Affine Rotation Angle -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            if check:
                _MSG: str = f"{node.name()}: Iterator.{str(id)} FF PRE Affine Rotation Angle -> already at its default value."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        else:
            [prm.deleteAllKeyframes() for prm in current.values()]
            for key in list(AFFINE_DEFAULTS.keys()):
                if current[key].eval() != AFFINE_DEFAULTS[key]:
                    check = False
                    # pre affine
                    current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                    current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                    current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                    current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                    # Print to Houdini's status bar
                    _MSG: str = f"{node.name()}: FF PRE Affine -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    break
            if check:
                _MSG: str = f"{node.name()}: FF PRE Affine -> already at their default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')


    def reset_postaffine_FF(self) -> None:
        """Reset FF post affine values to their defaults.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        n = flam3h_iterator_prm_names()
        
        if node.parm(f"{PRX_FF_PRM}{n.postaffine_do}").eval(): # This can be omitted as the post affine tab wont be accessible if this toggle is off.
                
            check: bool = True
            current: dict = { "affine_x": node.parmTuple(f"{PRX_FF_PRM}{n.postaffine_x}"), "affine_y": node.parmTuple(f"{PRX_FF_PRM}{n.postaffine_y}"), "affine_o": node.parmTuple(f"{PRX_FF_PRM}{n.postaffine_o}"), "angle": node.parm(f"{PRX_FF_PRM}{n.postaffine_ang}") }
            
            if self.kwargs["shift"]:
                current["affine_x"].deleteAllKeyframes()
                current["affine_y"].deleteAllKeyframes()
                for key in list(AFFINE_DEFAULTS.keys())[:1]:
                    if current[key].eval() != AFFINE_DEFAULTS[key]:
                        check = False
                        # pre affine
                        current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                        current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                        # Print to Houdini's status bar
                        _MSG: str = f"{node.name()}: FF POST Affine X, Y -> RESET"
                        flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                        break
                if check:
                    _MSG: str = f"{node.name()}: FF POST Affine X, Y -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    
            elif self.kwargs["ctrl"]:
                current["affine_o"].deleteAllKeyframes()
                if current["affine_o"].eval() != AFFINE_DEFAULTS.get("affine_o"):
                    check = False
                    current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                    # Print to Houdini's status bar
                    _MSG: str = f"{node.name()}: FF POST Affine O -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                if check:
                    _MSG: str = f"{node.name()}: FF POST Affine O -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
            elif self.kwargs["alt"]:
                current["angle"].deleteAllKeyframes()
                if current["angle"].eval() != AFFINE_DEFAULTS.get("angle"):
                    check = False
                    # post affine
                    current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                    # Print to Houdini's status bar
                    _MSG: str = f"{node.name()}: FF POST Affine Rotation Angle -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                if check:
                    _MSG: str = f"{node.name()}: FF POST Affine Rotation Angle -> already at their default value."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')

            else:
                [prm.deleteAllKeyframes() for prm in current.values()]
                for key in list(AFFINE_DEFAULTS.keys()):
                    if current[key].eval() != AFFINE_DEFAULTS[key]:
                        check = False
                        # post affine
                        current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                        current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                        current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                        current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                        # Print to Houdini's status bar
                        _MSG: str = f"{node.name()}: FF POST Affine -> RESET"
                        flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                        break
                if check:
                    _MSG: str = f"{node.name()}: FF POST Affine -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')


    def swap_iter_pre_vars(self) -> None:
        """Swap the selected iterator PRE vars order or swap only their names.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        node = self.node
        id: int = self.kwargs['script_multiparm_index']
        idx: str = str(id)
        _MSG: str = f"{node.name()}.iterator.{idx} PRE variations -> SWAP"
        
        # Get prm names
        pvT: tuple = flam3h_iterator().sec_prevarsT
        pvW: tuple = flam3h_iterator().sec_prevarsW[1:]
        
        # Get prm
        pvT_prm: tuple = (node.parm(f"{pvT[0]}{idx}"), node.parm(f"{pvT[1]}{idx}"))
        pvW_prm: tuple = (node.parm(f"{pvW[0][0]}{idx}"), node.parm(f"{pvW[1][0]}{idx}"))
        # get tmp prm
        __pvT_prm: tuple = (node.parm(PREFS_PVT_INT_0), node.parm(PREFS_PVT_INT_1))
        __pvW_prm: tuple = (node.parm(PREFS_PVT_FLOAT_0), node.parm(PREFS_PVT_FLOAT_1))
        
        # Only types
        if self.kwargs["ctrl"]:
            
            # COPY TYPES into tmp
            self.paste_from_prm(pvT_prm[0], __pvT_prm[0], True)
            self.paste_from_prm(pvT_prm[1], __pvT_prm[1], True)
            # SWAP TYPES from tmp
            self.paste_from_prm(__pvT_prm[0], pvT_prm[1])
            self.paste_from_prm(__pvT_prm[1], pvT_prm[0])
            
            # Clear tmp prms so in case of keyframes or expression they wont evaluate
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvT_prm[0])
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvT_prm[1])
            flam3h_general_utils.private_prm_set(node, __pvT_prm[0], 0)
            flam3h_general_utils.private_prm_set(node, __pvT_prm[1], 0)
            
            flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            
        # Types and their weights
        else:
            
            # COPY TYPES into tmp
            self.paste_from_prm(pvT_prm[0], __pvT_prm[0], True)
            self.paste_from_prm(pvT_prm[1], __pvT_prm[1], True)
            # SWAP TYPES from tmp
            self.paste_from_prm(__pvT_prm[0], pvT_prm[1])
            self.paste_from_prm(__pvT_prm[1], pvT_prm[0])
            
            # Clear tmp prms so in case of keyframes or expression they wont evaluate
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvT_prm[0])
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvT_prm[1])
            flam3h_general_utils.private_prm_set(node, __pvT_prm[0], 0)
            flam3h_general_utils.private_prm_set(node, __pvT_prm[1], 0)


            # COPY WEIGHTS into tmp
            self.paste_from_prm(pvW_prm[0], __pvW_prm[0], True)
            self.paste_from_prm(pvW_prm[1], __pvW_prm[1], True)
            
            # SWAP WEIGHTS from tmp
            self.paste_from_prm(__pvW_prm[0], pvW_prm[1])
            self.paste_from_prm(__pvW_prm[1], pvW_prm[0])
            
            # Clear tmp prms so in case of keyframes or expression they wont evaluate
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvW_prm[0])
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvW_prm[1])
            flam3h_general_utils.private_prm_set(node, __pvW_prm[0], 0)
            flam3h_general_utils.private_prm_set(node, __pvW_prm[1], 0)
            
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                
                
    def swap_FF_post_vars(self) -> None:
        """Swap the FF iterator POST vars order or swap only their names.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        node = self.node
        _MSG: str = f"{node.name()}: FF POST variations -> SWAP"
        
        # Get prm names
        pvT: tuple = flam3h_iterator_FF().sec_postvarsT_FF
        pvW: tuple = flam3h_iterator_FF().sec_postvarsW_FF
        
        # Get prm
        pvT_prm: tuple = (node.parm(f"{pvT[0]}"), node.parm(f"{pvT[1]}"))
        pvW_prm: tuple = (node.parm(f"{pvW[0][0]}"), node.parm(f"{pvW[1][0]}"))
        # get tmp prm
        __pvT_prm: tuple = (node.parm(PREFS_PVT_INT_0), node.parm(PREFS_PVT_INT_1))
        __pvW_prm: tuple = (node.parm(PREFS_PVT_FLOAT_0), node.parm(PREFS_PVT_FLOAT_1))
        
        # Only types
        if self.kwargs["ctrl"]:
            
            # Copy types into tmp
            self.paste_from_prm(pvT_prm[0], __pvT_prm[0], True)
            self.paste_from_prm(pvT_prm[1], __pvT_prm[1], True)
            # Swap types from tmp
            self.paste_from_prm(__pvT_prm[0], pvT_prm[1])
            self.paste_from_prm(__pvT_prm[1], pvT_prm[0])
            # Clear tmp prm so in case of keyframes or expression it doesnt evaluate
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvT_prm[0])
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvT_prm[1])
            
            flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            
        # Types and their weights
        else:
            
            # Copy types into tmp
            self.paste_from_prm(pvT_prm[0], __pvT_prm[0], True)
            self.paste_from_prm(pvT_prm[1], __pvT_prm[1], True)
            # Swap types from tmp
            self.paste_from_prm(__pvT_prm[0], pvT_prm[1])
            self.paste_from_prm(__pvT_prm[1], pvT_prm[0])
            # Clear tmp prm so in case of keyframes or expression it doesnt evaluate
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvT_prm[0])
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvT_prm[1])

            # Copy weights into tmp
            self.paste_from_prm(pvW_prm[0], __pvW_prm[0], True)
            self.paste_from_prm(pvW_prm[1], __pvW_prm[1], True)
            # Swap types from tmp
            self.paste_from_prm(__pvW_prm[0], pvW_prm[1])
            self.paste_from_prm(__pvW_prm[1], pvW_prm[0])
            # Clear tmp prm so in case of keyframes or expression it doesnt evaluate
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvW_prm[0])
            flam3h_general_utils.private_prm_deleteAllKeyframes(node, __pvW_prm[1])
            
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')


    def flam3h_default(self) -> None:
        """Default Flame preset and FLAM3H settings parameters vaules on creation.
        This is used to reset back FLAM3H node entire parameter template.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        node = self.node
        # Clear menu cache
        self.destroy_cachedUserData(node, 'iter_sel')
        self.destroy_cachedUserData(node, 'edge_case_01')
        self.destroy_all_menus_data(node, False)
        self.update_xml_last_loaded()
        # Iterators reset
        in_flame_utils(self.kwargs).in_to_flam3h_reset_iterators_parms(node, 3)
        # update xaos
        self.auto_set_xaos()
        # resets Tab contexts
        self.flam3h_reset_FF()
        flam3h_general_utils(self.kwargs).reset_SYS(1, FLAM3H_DEFAULT_GLB_ITERATIONS, 1)
        flam3h_palette_utils(self.kwargs).reset_CP()
        flam3h_general_utils(self.kwargs).reset_MB()
        in_flame_utils(self.kwargs).reset_IN()
        out_flame_utils(self.kwargs).reset_OUT(1) # dnt clear the MSG_OUT if any
        flam3h_general_utils(self.kwargs).reset_PREFS()
        # Reset/Set density
        flam3h_general_utils.reset_density(node)
        # Updated the OUT preset name if needed
        out_flame_utils(self.kwargs).out_auto_change_iter_num_to_prm()
        # Sierpiński triangle settings
        self.sierpinski_settings(node)
        # OUT render curves reset and set
        out_flame_utils.out_render_curves_set_and_retrieve_defaults(node)
        # init/clear copy/paste iterator's data and prm if needed.
        self.flam3h_paste_reset_hou_session_data()
        # BUILD XFVIZ
        flam3h_general_utils.util_xf_viz_force_cook(node, self.kwargs)
        
        # Destroy data
        flam3h_iterator_utils.destroy_userData(node, FLAM3H_USER_DATA_XML_LAST)
        
        # Print if the node has its display flag ON
        if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
            # Print to Houdini's status bar
            _MSG: str = f"{node.name()}: LOAD Flame preset: \"Sierpiński triangle\" -> Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Sierpiński triangle::10")
            
            
    def flam3h_reset_iterator(self) -> None:
        """Reset selected iterator to its default parameter's values.
        Include parametrics too.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        id: int = self.kwargs['script_multiparm_index']
        idx: str = str(id)
        
        # prm names
        n = flam3h_iterator_prm_names_collections()

        # Delete all keyframes
        [node.parmTuple(f"{prm_name}_{idx}").deleteAllKeyframes() for prm_name in n.prm_iterator_tuple]
        [node.parm(f"{prm_name}_{idx}").deleteAllKeyframes() for prm_name in n.prm_iterator]
        # Delete all keyframes parametrics.
        [node.parmTuple(f"{prm_name}_{idx}").deleteAllKeyframes() for prm_name in n.prm_parametrics_tuple]
        [node.parm(f"{prm_name}_{idx}").deleteAllKeyframes() for prm_name in n.prm_parametrics]
        # Revert to defaults
        [node.parmTuple(f"{prm_name}_{idx}").revertToDefaults() for prm_name in n.prm_parametrics_tuple]
        [node.parm(f"{prm_name}_{idx}").revertToDefaults() for prm_name in n.prm_parametrics]
        
        # iter idx
        #
        # iter main
        node.setParms({f"{n.main_note}_{idx}": f"iterator_{idx}"}) # type: ignore
        node.setParms({f"{n.main_weight}_{idx}": 0.5}) # type: ignore
        #
        # We leave xaos untouched becasue its handy to keep it and just reset it in a second step if desired
        #
        # iter shader
        node.setParms({f"{n.shader_color}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.shader_speed}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.shader_alpha}_{idx}": 1.0}) # type: ignore
        # iter vars
        [node.setParms({f"{prm}_{idx}": 1}) if prm == n.var_weight_1 
            else node.setParms({f"{prm}_{idx}": 0})
                for prm in n.prm_iterator_vars_all]
        
        # Iterator Affines
        affines_dict: dict[str, hou.Vector2 | float | None] = {f"{n.preaffine_x}_{idx}": AFFINE_DEFAULTS.get("affine_x"),
                                                                    f"{n.preaffine_y}_{idx}": AFFINE_DEFAULTS.get("affine_y"),
                                                                    f"{n.preaffine_o}_{idx}": AFFINE_DEFAULTS.get("affine_o"),
                                                                    f"{n.preaffine_ang}_{idx}": AFFINE_DEFAULTS.get("angle"),
                                                                    f"{n.postaffine_do}_{idx}": 0,
                                                                    f"{n.postaffine_x}_{idx}": AFFINE_DEFAULTS.get("affine_x"),
                                                                    f"{n.postaffine_y}_{idx}": AFFINE_DEFAULTS.get("affine_y"),
                                                                    f"{n.postaffine_o}_{idx}": AFFINE_DEFAULTS.get("affine_o"),
                                                                    f"{n.postaffine_ang}_{idx}": AFFINE_DEFAULTS.get("angle")
                                                                    }
        
        # Iterator Affines Set
        [node.setParms({key: value}) for key, value in affines_dict.items()]
    
    
    def flam3h_reset_FF(self) -> None:
        """Reset the FLAM3H FF Tab parameters.
        Include parametrics too (PRE, VAR and POST)
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node

        # prm names
        n = flam3h_iterator_prm_names_collections()
        
        # Delete all keyframes
        [node.parmTuple(f"{PRX_FF_PRM}{prm_name}").deleteAllKeyframes() for prm_name in n.prm_FF_tuple]
        [node.parm(f"{PRX_FF_PRM}{prm_name}").deleteAllKeyframes() for prm_name in n.prm_FF]
        # Delete all keyframes parametrics (PRE and POST)
        [node.parmTuple(f"{PRX_FF_PRM}_{prm_name}").deleteAllKeyframes() for prm_name in n.prm_parametrics_tuple]
        [node.parm(f"{PRX_FF_PRM}_{prm_name}").deleteAllKeyframes() for prm_name in n.prm_parametrics]
        [node.parmTuple(f"{PRX_FF_PRM_POST}_{prm_name}").deleteAllKeyframes() for prm_name in n.prm_parametrics_tuple]
        [node.parm(f"{PRX_FF_PRM_POST}_{prm_name}").deleteAllKeyframes() for prm_name in n.prm_parametrics]
        # Revert to defaults
        [node.parmTuple(f"{PRX_FF_PRM}_{prm_name}").revertToDefaults() for prm_name in n.prm_parametrics_tuple]
        [node.parm(f"{PRX_FF_PRM}_{prm_name}").revertToDefaults() for prm_name in n.prm_parametrics]
        [node.parmTuple(f"{PRX_FF_PRM_POST}_{prm_name}").revertToDefaults() for prm_name in n.prm_parametrics_tuple]
        [node.parm(f"{PRX_FF_PRM_POST}_{prm_name}").revertToDefaults() for prm_name in n.prm_parametrics]

        # FF note
        node.setParms({f"{PRX_FF_PRM}{n.main_note}": "iterator_FF"})
        # FF vars
        [node.setParms({f"{PRX_FF_PRM}{prm}": 1}) if prm == n.var_weight_1 
                    else node.setParms({f"{PRX_FF_PRM}{prm}": 0})
                        for prm in n.prm_FF_vars_all]
        # FF Affines
        affines_dict: dict[str, hou.Vector2 | float | None] = {f"{PRX_FF_PRM}{n.preaffine_x}": AFFINE_DEFAULTS.get("affine_x"),
                                                                    f"{PRX_FF_PRM}{n.preaffine_y}": AFFINE_DEFAULTS.get("affine_y"),
                                                                    f"{PRX_FF_PRM}{n.preaffine_o}": AFFINE_DEFAULTS.get("affine_o"),
                                                                    f"{PRX_FF_PRM}{n.preaffine_ang}": AFFINE_DEFAULTS.get("angle"),
                                                                    f"{PRX_FF_PRM}{n.postaffine_do}": 0,
                                                                    f"{PRX_FF_PRM}{n.postaffine_x}": AFFINE_DEFAULTS.get("affine_x"),
                                                                    f"{PRX_FF_PRM}{n.postaffine_y}": AFFINE_DEFAULTS.get("affine_y"),
                                                                    f"{PRX_FF_PRM}{n.postaffine_o}": AFFINE_DEFAULTS.get("affine_o"),
                                                                    f"{PRX_FF_PRM}{n.postaffine_ang}": AFFINE_DEFAULTS.get("angle")
                                                                    }
        # FF Affines Set
        [node.setParms({key: value}) for key, value in affines_dict.items()]
        

    def auto_set_xaos(self) -> None:
        """Set iterator's xaos values every time an iterator is added or removed.
        It will also update the data for the xform handles VIZ SOLO mode if Active.

        Args:
            (self):
            
        Returns:
            (None):
        """
        
        node = self.node
        iter_count: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        # AUTO DIV XAOS
        autodiv: int = node.parm(PREFS_PVT_XAOS_AUTO_SPACE).eval()
        div_xaos: str = 'xaos:'
        div_weight: str = ':'
        if autodiv:
            div_xaos = 'xaos :'
            div_weight = ' :'
        
        # PRM DATA
        prm_mpidx = node.parm(FLAM3H_DATA_PRM_MPIDX)
        # PRM XF VIZ
        prm_xfviz = node.parm(PREFS_PVT_XF_VIZ)
        prm_xfviz_solo = node.parm(PREFS_PVT_XF_VIZ_SOLO)
        prm_xfviz_solo_mp_idx = node.parm(PREFS_PVT_XF_VIZ_SOLO_MP_IDX)
        data_name = f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}"
        
        # unlock
        [prm.lock(False) for prm in (prm_mpidx, prm_xfviz, prm_xfviz_solo, prm_xfviz_solo_mp_idx)]
        
        # init indexes
        idx_del_inbetween: int | None = None
        idx_add_inbetween: int | None = None
        
        mpmem: list = []
        mpmem_hou_get: list = []
        xaos_str_hou_get: list = []
        
        # get mpmem parms now
        mp_mem_name: str = flam3h_iterator_prm_names().main_mpmem
        [mpmem.append(int(node.parm(f"{mp_mem_name}_{str(mp_idx + 1)}").eval())) for mp_idx in range(iter_count)]
        
        # get mpmem from CachedUserData
        __mpmem_hou_get: list | None = self.auto_set_xaos_data_get_MP_MEM(node)
        if __mpmem_hou_get is None:
            mpmem_hou_get = mpmem
        else:
            mpmem_hou_get = list(__mpmem_hou_get)
        
        # collect all xaos
        val: list = out_flame_utils.out_xaos_collect(node, iter_count, flam3h_iterator_prm_names().xaos)
        # fill missing weights if any
        fill_all_xaos: list = [np_pad(item, (0, iter_count-len(item)), 'constant', constant_values=1).tolist() for item in val]
        
        # convert all xaos into array of strings
        xaos_str: list = [[str(item) for item in xaos] for xaos in fill_all_xaos]
            
        # get xaos from CachedUserData
        __xaos_str_hou_get: list | None = self.auto_set_xaos_data_get_XAOS_PREV(node)
        if __xaos_str_hou_get is None:
            xaos_str_hou_get = xaos_str
        else:
            xaos_str_hou_get = list(__xaos_str_hou_get)
            
        # DEL: INBETWEEN get index: try
        s_current: set = set(mpmem)
        s_history: set = set(mpmem_hou_get)
        _idx = list(set(s_history - s_current))
        if _idx: idx_del_inbetween = int(_idx[0]) - 1
        # ADD: INBETWEEN get index : try
        for mp in range(iter_count-1):
            if mpmem[mp] == mpmem[mp + 1]:
                idx_add_inbetween = mp
                break
        
        # DEL -> ONLY LAST ITERATOR
        if idx_del_inbetween is not None and idx_del_inbetween == iter_count:
            
            # Clear menu cache
            self.destroy_cachedUserData(node, 'iter_sel')

            # update CachedUserData: flam3h_xaos_iterators_prev
            self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_str)
            
            # NEED TO DOUBLE CHECK HERE
            # Update copy/paste iterator's index if there is a need to do so
            flam3h_node_mp_id: TA_M = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
            
            if flam3h_node_mp_id is not None:
                # Check if the node still exist
                try:
                    hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                except:
                    flam3h_node_mp_id = None
                    flam3h_node = None
                else:
                    flam3h_node: TA_MNode = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
                    
                # If the node exist
                if flam3h_node_mp_id is not None and node == flam3h_node:
                        
                    if (idx_del_inbetween + 1) == flam3h_node_mp_id: # just in case..
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = None # type: ignore
                        # set
                        prm_mpidx.set(-1)
                        self.del_comment_and_user_data_iterator(node)
                        # Let us know
                        _MSG: str = f"{node.name()}: The iterator you just removed was marked for being copied -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        
                    else:
                        pass
                    
            # XF VIZ
            if prm_xfviz.eval() and prm_xfviz_solo.eval():
                
                xf_viz_mp_idx: int = prm_xfviz_solo_mp_idx.eval()
                if (idx_del_inbetween + 1) == xf_viz_mp_idx:
                    prm_xfviz_solo.set(0)
                    self.destroy_userData(node, f"{data_name}")
                    
                    _MSG: str = f"{node.name()}: The iterator you just removed had its XF VIZ: ON. Reverted to display the xforms handles VIZ all together."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                    
        # DEL
        elif idx_del_inbetween is not None and idx_del_inbetween < iter_count:
            
            # Clear menu cache
            self.destroy_cachedUserData(node, 'iter_sel')

            xaos_str: list = xaos_str_hou_get
            del xaos_str[idx_del_inbetween]
            for x in xaos_str:
                del x[idx_del_inbetween]

            # update CachedUserData: flam3h_xaos_iterators_prev
            self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_str)
            
            # Update copy/paste iterator's index if there is a need to do so
            flam3h_node_mp_id: TA_M = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
            if flam3h_node_mp_id is not None:
                # Check if the node still exist
                try:
                    hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                except:
                    flam3h_node_mp_id = None
                    flam3h_node = None
                else:
                    flam3h_node: TA_MNode = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
                    
                # If the node exist and if it is the selected one
                if flam3h_node_mp_id is not None and node == flam3h_node:
                        
                    if (idx_del_inbetween + 1) < flam3h_node_mp_id:
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = flam3h_node_mp_id - 1 # type: ignore
                        # set
                        idx_new: int = prm_mpidx.eval() - 1
                        prm_mpidx.set(idx_new)
                        self.del_comment_and_user_data_iterator(node)
                        self.set_comment_and_user_data_iterator(node, str(idx_new))

                    elif (idx_del_inbetween + 1) == flam3h_node_mp_id:
                        
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = None # type: ignore
                        # set
                        prm_mpidx.set(-1)
                        self.del_comment_and_user_data_iterator(node)
                        # Let us know
                        _MSG: str = f"{node.name()}: The iterator you just removed was marked for being copied -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        
                    else:
                        pass
                    
            # XF VIZ
            if prm_xfviz.eval() and prm_xfviz_solo.eval():
                
                xf_viz_mp_idx: int = prm_xfviz_solo_mp_idx.eval()
                if (idx_del_inbetween + 1) < xf_viz_mp_idx:
                    prm_xfviz_solo_mp_idx.set(xf_viz_mp_idx - 1)
                    node.setUserData(f"{data_name}", str(xf_viz_mp_idx - 1))
                elif (idx_del_inbetween + 1) == xf_viz_mp_idx:
                    prm_xfviz_solo.set(0)
                    self.destroy_userData(node, f"{data_name}")
                    _MSG: str = f"{node.name()}: The iterator you just removed had its XF VIZ: ON. Reverted to display the xforms handles VIZ all together."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')

        # otherwise ADD
        # If it is true that an iterator has been added in between ( 'idx_add_inbetween' not 'None' ) lets add the new weight at index
        elif idx_add_inbetween is not None:
            
            # Clear menu cache
            self.destroy_cachedUserData(node, 'iter_sel')

            for xidx, x in enumerate(xaos_str):
                if xidx != idx_add_inbetween:
                    x.insert(idx_add_inbetween, '1.0')
                    # x already had the new iterator weight added to the end of it
                    # so lets remove the last element as it is not longer needed
                    del x[-1]
                    
            # update CachedUserData: flam3h_xaos_iterators_prev
            self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_str)
            
            # Update copy/paste iterator's index if there is a need to do so
            flam3h_node_mp_id: TA_M = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
            
            if flam3h_node_mp_id is not None:
                # Check if the node still exist
                try:
                    hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                except:
                    flam3h_node_mp_id = None
                    flam3h_node = None
                else:
                    flam3h_node: TA_MNode = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
                    
                # If the node exist and if it is the selected one
                if flam3h_node_mp_id is not None and node == flam3h_node:
                        
                    if (idx_add_inbetween + 1) <= flam3h_node_mp_id:
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = flam3h_node_mp_id + 1 # type: ignore
                        # set
                        idx_new: int = prm_mpidx.eval() + 1
                        prm_mpidx.set(idx_new)
                        self.del_comment_and_user_data_iterator(node)
                        self.set_comment_and_user_data_iterator(node, str(idx_new))
                        
                    else:
                        pass
                    
            # XF VIZ
            if prm_xfviz.eval() and prm_xfviz_solo.eval():
                
                xf_viz_mp_idx = prm_xfviz_solo_mp_idx.eval()
                if (idx_add_inbetween + 1) <= xf_viz_mp_idx:
                    prm_xfviz_solo_mp_idx.set(xf_viz_mp_idx + 1)
                    node.setUserData(f"{data_name}", str(xf_viz_mp_idx + 1))
        
        else:
            # update CachedUserData: flam3h_xaos_iterators_prev
            self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_str)
            
        # set all multi parms xaos strings parms
        xaos_str_round_floats: list = [div_weight.join(x) for x in out_flame_utils.out_util_round_floats(xaos_str)]
        prm_xaos_name: str = flam3h_iterator_prm_names().xaos
        [node.parm(f"{prm_xaos_name}_{str(mp_idx + 1)}").deleteAllKeyframes() for mp_idx in range(iter_count)]
        [node.setParms({f"{prm_xaos_name}_{str(mp_idx + 1)}": (div_xaos + xaos)}) for mp_idx, xaos in enumerate(xaos_str_round_floats)] # type: ignore
        
        # reset iterator's mpmem prm
        [node.setParms({f"{mp_mem_name}_{str(mp_idx + 1)}": str(mp_idx + 1)}) for mp_idx in range(iter_count)] # type: ignore
        # update flam3h_xaos_mpmem
        __mpmem_hou: list = [int(node.parm(f"{mp_mem_name}_{str(mp_idx + 1)}").eval()) for mp_idx in range(iter_count)]
        # export mpmem into CachedUserData
        self.auto_set_xaos_data_set_MP_MEM(node, __mpmem_hou)
        
        # Update iterator's names if there is a need ( If they have a default name )
        mp_note_name: str = flam3h_iterator_prm_names().main_note
        [node.setParms({f"{mp_note_name}_{str(mp_idx + 1)}": f"iterator_{mp_idx + 1}"}) for mp_idx in range(iter_count) if self.flam3h_iterator_is_default_name(str(node.parm(f"{mp_note_name}_{str(mp_idx + 1)}").eval()).strip())] # type: ignore
        
        # lock
        [prm.lock(True) for prm in (prm_mpidx, prm_xfviz, prm_xfviz_solo, prm_xfviz_solo_mp_idx)]


    def iterators_count(self) -> None:
        """Every time an iterator is added or remove
        this will run and execute based on iterator's number: Zero or more then Zero.

        Args:
            (self):
            
        Returns:
            (None):
        """

        _MSG_str = "Iterators count set to Zero. Add at least one iterator or load a valid IN flame file"

        node = self.node
        # Clear menu cache
        self.destroy_cachedUserData(node, 'iter_sel')
        
        iterators_count: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        
        if not iterators_count:
            
            self.destroy_cachedUserData(node, 'edge_case_01')
            
            # delete channel references
            [p.deleteAllKeyframes() for p in node.parms() if not p.isLocked()]
                
            # GLOBAL
            # Reset/Set density
            flam3h_general_utils.reset_density(node)
            # Iterations
            node.setParms({GLB_ITERATIONS: FLAM3H_DEFAULT_GLB_ITERATIONS}) # type: ignore
            # FF vars
            self.flam3h_reset_FF()
            # MB
            flam3h_general_utils(self.kwargs).reset_MB()
            # SYS, IN and PREFS
            [prm.set(0) for prm in (node.parm(PREFS_CAMERA_HANDLE), node.parm(PREFS_CAMERA_CULL))]
            [flam3h_general_utils.private_prm_set(node, prm_name, 0) for prm_name in (IN_PVT_ISVALID_PRESET, IN_PVT_CLIPBOARD_TOGGLE)]
            [flam3h_general_utils.private_prm_set(node, prm_name, 0) for prm_name in (PREFS_PVT_DOFF, PREFS_PVT_RIP, PREFS_PVT_XF_VIZ_SOLO, PREFS_PVT_XF_FF_VIZ_SOLO)]
            flam3h_iterator_utils.destroy_userData(node, f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}")
            # descriptive message parameter
            node.setParms({MSG_DESCRIPTIVE_PRM: ""}) # type: ignore
            
            # init/clear copy/paste iterator's data and prm
            self.flam3h_paste_reset_hou_session_data()
            
            # Destroy data
            self.destroy_userData(node, FLAM3H_USER_DATA_XML_LAST)
            
            # Updated the OUT flame name if any
            out_flame_utils(self.kwargs).out_auto_change_iter_num_to_prm()
            
            # OUT render curves reset and set
            out_flame_utils.out_render_curves_set_and_retrieve_defaults(node)
            
            # Reset IN Folder settings heading
            node.setParms({MSG_IN_STATS_HEADING: ''}) # type: ignore
            node.setParms({MSG_IN_SETTINGS_HEADING: ''}) # type: ignore
            
            # Force this node to cook to get a warning message show up upstream.
            hou.node(flam3h_general_utils(self.kwargs).get_node_path(TFFA_XAOS)).cook(force=True)
            
            # Print to Houdini's status bar
            _MSG: str = f"{node.name()}: {_MSG_str}"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Iterators count ZERO")
            
        else:
            
            # set xaos and updated presets menus every time an iterator is added or removed
            self.auto_set_xaos()
            self.destroy_all_menus_data(node, False)
            self.update_xml_last_loaded()
            
            # Clear status bar msg if needed
            if  _MSG_str in hou.ui.statusMessage()[0]: # type: ignore
                flam3h_general_utils.set_status_msg('', 'MSG')
                
        # If OUT Camera sensor viz mode is ON.
        if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
            # We can avoid to set the clipping planes as they are already set
            flam3h_general_utils(self.kwargs).util_set_front_viewer()


    def __iterator_keep_last_vactive(self) -> None:
        """ NOT USED ANYMORE
                Since this case is now being addressed directly in the CVEX code,
                it is not necessary anymore to revert the last iterator to being active anymore.
        
        While it is possible to delete all iterators,
        we must always have at least one active iterator, if at least one iterator is present and its weight above Zero.
        This will prevent the last active iterator to being disabled.
        
        _NOTE:
            The parameters names are hard coded here to try to speed up even if a tiny bit.
            If class flam3h_iterator_prm_names: is updated, need to be updated here too.
            
        Args:
            (self):
            
        Returns:
            (None):
        """    
        
        node = self.node
        # Clear menu cache
        self.destroy_cachedUserData(node, 'iter_sel')
        
        iter_num: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        
        # The following will collect the active iterator bool value if and only if the iterator is active and its weight is above zero.
        # What it is going to happen is that by the time we try to disable the last active iterator, it wont collect anything becasue
        # by the time we click to disable the last iterator they will all be disabled for a moment, just right before we switch this last one back to being enabled.
        # Hence the case we are interested in is when the va: list variable is empty, thats how we know we tried to switch the last active iterator OFF.
        va: list = [int(node.parm(f"vactive_{str(mp_idx + 1)}").eval()) 
                    for mp_idx in range(iter_num) 
                        if node.parm(f"vactive_{str(mp_idx + 1)}").eval() 
                        and node.parm(f"iw_{str(mp_idx + 1)}").eval() > 0]

        # If this va: list variable is empty, mean we switched the last active irterator to OFF so lets do something about it.
        if not va:
            id: int = self.kwargs['script_multiparm_index']
            node.setParms({f"vactive_{str(id)}": 1})
            _MSG: str = f"{node.name()}: iterator {str(id)} reverted back to being Active. There must always be at least one active iterator."
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"iterator {str(id)} -> back to being Active")


    def __iterator_keep_last_vactive_STAR(self) -> None:
        """ NOT USED ANYMORE
                Since this case is now being addressed directly in the CVEX code,
                it is not necessary anymore to revert the last iterator to being active anymore.
        
        This is the actual definition that run in a callback script.
        It will prevent the lasct active iterator to be turned OFF.
        
        _NOTE:
            The parameters names is hard coded here to try to speed up even if a tiny bit.
            If class flam3h_iterator_prm_names: is updated, need to be updated here too.
            
        Args:
            (self):
            
        Returns:
            (None):
        """
        id: int = self.kwargs['script_multiparm_index']
        vactive_prm_name: str = f"vactive_{str(id)}"
        flam3h_general_utils(self.kwargs).flam3h_toggle(vactive_prm_name)
        self.__iterator_keep_last_vactive()


    def __iterator_keep_last_weight(self) -> None:
        """ NOT USED ANYMORE
                Since this case is now being addressed directly in the CVEX code,
                it is not necessary anymore to revert the value to a non-zero value anymore.
        
        While it is possible to delete all iterators,
        we must always have at least one iterator's weight above Zero, if at least one iterator is present or active.
        This will prevent to set the last active iterator's Weight to be Zero.
        
        _NOTE:
            The parameters names is hard coded here to try to speed up even if a tiny bit.
            If class flam3h_iterator_prm_names: is updated, need to be updated here too.
            
        Args:
            (self):
            
        Returns:
            (None):
        """  
        node = self.node
        # Clear menu cache
        self.destroy_cachedUserData(node, 'iter_sel')
        
        iter_num: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        _W: list = [int(node.parm(f"iw_{str(mp_idx + 1)}").eval()) 
                    for mp_idx in range(iter_num) 
                        if node.parm(f"iw_{str(mp_idx + 1)}").eval() == 0 
                        and int(node.parm(f"vactive_{str(mp_idx + 1)}").eval())]
        
        vactive_iters: list = [int(node.parm(f"vactive_{str(mp_idx + 1)}").eval()) 
                                for mp_idx in range(iter_num) 
                                    if node.parm(f"vactive_{str(mp_idx + 1)}").eval()]
        
        if len(_W) == len(vactive_iters):
            min_weight: float = 0.00000001
            id: int = self.kwargs['script_multiparm_index']
            node.setParms({f"iw_{str(id)}": min_weight})
            _MSG: str = f"{node.name()}: iterator {str(id)}'s Weight reverted back to a value of: {min_weight} instead of Zero. There must always be at least one active iterator's weight above Zero."
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"iterator {str(id)} Weight: back to being NON-ZERO")
            
            
    def iterator_vactive_and_update(self) -> None:
        """Force menu updates and toggle ON/OFF if the correct parameter is being used.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        node = self.node
        # Clear menu cache
        self.destroy_cachedUserData(node, 'iter_sel')
        
        # Do toggle ON/OFF if the correct parameter is being used
        if 'doiter_' in self.kwargs['parm'].name():
            id: int = self.kwargs['script_multiparm_index']
            vactive_prm_name: str = f"vactive_{str(id)}"
            flam3h_general_utils(self.kwargs).flam3h_toggle(vactive_prm_name)


# FLAM3H PALETTE start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class flam3h_palette_utils:
    """
class flam3h_palette_utils

@STATICMETHODS
* build_ramp_palette_default(ramp_parm: hou.Parm) -> None:
* build_ramp_palette_temp(ramp_tmp_parm: hou.Parm) -> None:
* build_ramp_palette_error() -> tuple[list, list, list]:
* delete_ramp_all_keyframes(ramp_parm: hou.Parm) -> None:
* get_ramp_keys_count(ramp: hou.Ramp) -> str:
* isJSON_F3H_get_first_preset(filepath: str | bool) -> str | bool:
* isJSON_F3H(node: hou.SopNode, filepath: str | bool,  msg: bool = True, parm_path_name: str = CP_PALETTE_LIB_PATH) -> tuple[bool, bool]:
* isJSON_F3H_on_preset_load(node: hou.SopNode, filepath: str | bool,  msg: bool = True, parm_path_name: str = CP_PALETTE_LIB_PATH) -> tuple[bool, bool]:
* rgb_to_hex(rgb: tuple) -> str:
* hex_to_rgb(hex: str) -> tuple:
* find_nearest_idx(array: list | tuple, value: int | float) -> int | float:
* json_to_flam3h_palette_plus_MSG(node: hou.SopNode, HEXs: list, mode: bool = False, palette_plus_msg: bool = False) -> None:
* json_to_flam3h_palette_plus_preset_MSG(node: hou.SopNode, _MSG: str) -> None:
* json_to_flam3h_get_preset_name_and_id(node: hou.SopNode) -> tuple[str, int]:
* menu_cp_presets_loop(node: hou.SopNode, menu: list, i: int, item: str) -> None:
* menu_cp_presets_loop_enum(node: hou.SopNode, menu: list, i: int, item: str) -> None:
* menu_cp_presets_empty_loop(node: hou.SopNode, menu: list, i: int, item: str) -> None:
* menu_cp_presets_empty_loop_enum(node: hou.SopNode, menu: list, i: int, item: str) -> None:

@METHODS
* cp_preset_name_set(self) -> None:
* menu_cp_presets_data(self) -> list:
* menu_cp_presets(self) -> list:
* menu_cp_presets_empty_data(self) -> list:
* menu_cp_presets_empty(self) -> list:
* flam3h_ramp_save_JSON_DATA(self) -> tuple[dict, str]:
* flam3h_ramp_save(self) -> None:
* json_to_flam3h_ramp_initialize(self, rgb_from_XML_PALETTE: list) -> tuple[hou.Ramp, int, bool]:
* json_to_flam3h_ramp_set_HSV(self, node, hsv_check: bool, hsv_vals: list) -> None:
* json_to_flam3h_ramp_SET_PRESET_DATA(self, node: hou.SopNode) -> None:
* json_to_flam3h_ramp_sys(self, use_kwargs: bool = True) -> None:
* json_to_flam3h_ramp_SHIFT(self, node: hou.SopNode) -> None:
* json_to_flam3h_ramp_CTRL(self, node: hou.SopNode) -> None:
* json_to_flam3h_ramp_ALT(self, node: hou.SopNode) -> None:
* json_to_flam3h_ramp(self, use_kwargs: bool = True) -> None:
* palette_cp(self, palette_plus_msg: bool = False) -> None:
* palette_cp_to_tmp(self) -> None:
* palette_hsv(self) -> None:
* palette_lock(self) -> None:
* reset_CP_LOCK_MSG(self) -> None:
* reset_CP_TMP(self) -> None:
* reset_CP_options(self) -> None:
* reset_CP_run_0(self) -> None:
* reset_CP_run_2(self) -> None:
* reset_CP_run_3(self) -> None:
* reset_CP(self, mode: int=0) -> None:
* reset_CP_palette_action(self) -> None:
    """
    
    __slots__ = ("_kwargs", "_node", "_palette_plus_do")
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs: dict = kwargs
        self._node = kwargs['node']
        self._palette_plus_do: int = self._node.parm(CP_PALETTE_256_PLUS).eval()
        
        
    @staticmethod
    def build_ramp_palette_default(ramp_parm: hou.Parm) -> None:
        """Build a ramp data with default value for the FLAM3H main palette and set it.
        
        Args:
            ramp_parm(hou.Parm): The ramp parameter to set the default data to. Note this is a hou.Parm and not a hou.Ramp

        Returns:
            (None):
        """
        cp_def_bases: list = [hou.rampBasis.Linear] * 4 # type: ignore
        cp_def_keys: list = [0.0, 0.25, 0.5, 0.75, 1.0]
        cp_def_values: list[tuple] = [(0.2, 0.05, 1), (0.1, 0.85 , 1), (0.05, 1, 0.1), (0.95, 1, 0.1), (1, 0.05, 0.05)]
        ramp_parm.set(hou.Ramp(cp_def_bases, cp_def_keys, cp_def_values)) # type: ignore
        
        
    @staticmethod
    def build_ramp_palette_temp(ramp_tmp_parm: hou.Parm) -> None:
        """Build a ramp data with default value for the FLAM3H temp palette and set it.
        
        Args:
            ramp_tmp_parm(hou.Parm): The ramp parameter to set the default data to. Note this is a hou.Parm and not a hou.Ramp
            
        Returns:
            (None):
        """
        cp_tmp_bases: list = [hou.rampBasis.Linear] * 2  # type: ignore
        cp_tmp_keys: list = [0.0, 1.0]
        cp_tmp_values: list[tuple] = [(0.9989989989989989987654, 0, 0), (0.9989989989989989987654, 0 , 0)]
        ramp_tmp_parm.set(hou.Ramp(cp_tmp_bases, cp_tmp_keys, cp_tmp_values)) # type: ignore
        
        
    @staticmethod
    def build_ramp_palette_error() -> tuple[list, list, list]:
        """Build a ramp data with value the signify an error has accurred.
        
        Args:
            (None):

        Returns:
            (tuple): BASEs, POSs, COLORs for the ramp to be build.
        """
        return [hou.rampBasis.Linear], [0], [(1,0,0)] # type: ignore
    
    
    @staticmethod
    def delete_ramp_all_keyframes(ramp_parm: hou.Parm) -> None:
        """Delete all ramp keyframes for all its positon and color keys values.
        
        Args:
            ramp_parm(hou.Parm): The ramp parameter to clear from all its keyframes if any. Note this is a hou.Parm and not a hou.Ramp

        Returns:
            (None):
        """
        posList: KeysView = ramp_parm.evalAsRamp().keys()
        [hou.parm(f"{ramp_parm.path()}{str(i + 1)}pos").deleteAllKeyframes() for i in range(0, len(posList))]
        [hou.parmTuple(f"{ramp_parm.path()}{str(i + 1)}c").deleteAllKeyframes() for i in range(0, len(posList))]

        
    @staticmethod 
    def get_ramp_keys_count(ramp: hou.Ramp) -> str:
        """Based on how many color keys are present in the provided ramp,
        select a palette colors/keys count preset to use for better resample it.
        
        _NOTE:
            This need to be revised and smartened up a little as there may be cases where it will fail
            to sample the palette enough to collect the proper colors based on their location and proxymity to each other in the ramp.

        Args:
            ramp(hou.Ramp): The current ramp being considered.

        Returns:
            (str): a palette colors/keys count string preset.
        """
        keys_count: int = len(ramp.keys())
        if keys_count <= 128:
            return PALETTE_COUNT_128
        elif keys_count <= 256:
            return PALETTE_COUNT_256
        else:
            # This message when the CP options: palette 256+ toggle is OFF
            _MSG: str = f'{str(hou.pwd())}: Colors: {str(keys_count)}: to many colors and will default back to the standard 256 color keys for this palette.'
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            print(f"{_MSG}\n")
            return PALETTE_COUNT_256
        
        
    @staticmethod
    def isJSON_F3H_get_first_preset(filepath: str | bool) -> str | bool:
        """Try to get the first palette preset of a JSON FLAM3H palette file.

        Args:
            filepath(str | bool): The JSON FLAM3H Palette file path

        Returns:
            (str | bool): The preset name, or False if not.
        """
        try:
            with open(filepath, 'r') as r:
                preset_name: str = list(json.load(r).keys())[0]
            return preset_name
        except: return False


    @staticmethod
    def isJSON_F3H(node: hou.SopNode, filepath: str | bool,  msg: bool = True, parm_path_name: str = CP_PALETTE_LIB_PATH) -> tuple[bool, bool]:
        """Check if the loaded palette lib file is a valid FLAM3H palette json file.

        Args:
            node(hou.SopNode): current FLAM3H node
            filepath(str | bool): Palette lib full file path.
            msg(bool): Default to True, print out messages to the Houdini's status bar. Set it to False to not print out messages.
            parm_path_name(str): Default to global: CP_PALETTE_LIB_PATH. The actual Houdini's palette file parameter name.

        Returns:
            (bool): True if valid. False if not valid.
        """      
        if filepath is not False:
            
            preset: str | bool = flam3h_palette_utils.isJSON_F3H_get_first_preset(filepath)
            if preset is not False:
                
                # If we made it this far, mean we loaded a valid JSON file,
                # lets now check if the preset is actually a F3H Palette preset.
                with open(filepath, 'r') as r:
                    data: dict = json.load(r)[preset]
                    
                # This is the moment of the truth ;)
                try: hex_values = data[CP_JSON_KEY_NAME_HEX]
                except:
                    if msg:
                        _MSG: str = f"{node.name()}: Palette JSON load -> Although the JSON file you loaded is legitimate, it does not contain any valid FLAM3H Palette data."
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, f"CP LOAD: Not a valid FLAM3H JSON palette file")
                    del data
                    return True, False
                
                # Validate the file path setting it
                node.setParms({parm_path_name: filepath}) #type: ignore
                sm: tuple = hou.ui.statusMessage() # type: ignore
                if sm[0] and msg:
                    flam3h_general_utils.set_status_msg('', 'MSG')
                del data
                return True, True
            else:
                # The following is clearing up status messages it should have not
                # flam3h_general_utils.set_status_msg('', 'MSG')
                return False, False
        
        else:
            flam3h_general_utils.set_status_msg('', 'MSG')
            return False, False
        
        
    @staticmethod
    def isJSON_F3H_on_preset_load(node: hou.SopNode, filepath: str | bool,  msg: bool = True, parm_path_name: str = CP_PALETTE_LIB_PATH) -> tuple[bool, bool]:
        """This the same as: def isJSON_F3H(...) but wit a few condition to try to speedup things a little.

        Args:
            node(hou.SopNode): current FLAM3H node
            filepath(str | bool): Palette lib full file path.
            msg(bool): Default to True, print out messages to the Houdini's status bar. Set it to False to not print out messages.
            parm_path_name(str): Default to global: CP_PALETTE_LIB_PATH. The actual Houdini's palette file parameter name.

        Returns:
            (tuple[bool, bool]): True if valid. False if not valid.
        """      
        if not node.parm(CP_PVT_ISVALID_PRESET).eval():
            return flam3h_palette_utils.isJSON_F3H(node, filepath, msg, parm_path_name)
            
        elif node.parm(CP_PVT_ISVALID_FILE).eval() and node.parm(CP_PVT_ISVALID_PRESET).eval():
            # If a preset has been loaded already, we assume it mean the loaded lib file is valid.
            # This is risky but it make things faster
            return True, True
        
        else:
            flam3h_general_utils.set_status_msg('', 'MSG')
            return False, False
        
        
    @staticmethod
    def rgb_to_hex(rgb: tuple) -> str:
        """Convert a RGB color values into HEX color values.

        Args:
            rgb(tuple): the RGB color value to convert.

        Returns:
            (str): HEX color value
        """
        hex: str = ''.join(['{:02X}'.format(int(round(x))) for x in [flam3h_general_utils.clamp(255*x) for x in rgb]])
        return hex


    @staticmethod
    def hex_to_rgb(hex: str) -> tuple:
        """Convert a HEX color value into RGB color value.

        Args:
            rgb(str): the HEX color value to convert.

        Returns:
            (tuple): RGB color value
        """   
        return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
    
    
    @staticmethod
    def find_nearest_idx(array: list | tuple, value: int | float) -> int | float:
        """Given a value, find the closest value in the array that is bigger than the value passed in.
        
        Args:
            array(list, tuple): the array of values to search into.
            value:(int, float): The value to use to find its closest and bigger value into the array.

        Returns:
            (int | float): the closest value in the array that is bigger than the value passed in. Can be either an integer or a float
        """   
        idx: int = np_searchsorted(array, value, side="left").tolist()
        return array[idx]
    
    
    @staticmethod
    def json_to_flam3h_palette_plus_MSG(node: hou.SopNode, HEXs: list, mode: bool = False, palette_plus_msg: bool = False) -> None:
        """Given a value, find the closest value in the array that is bigger than the value passed in.
        I am using a manual f-string build here. Probably dynamically build a list would be better but if i'll need to add more strings i'll look into it.
        
        Args:
            node(hou.SopNode): The current FLAM3H node.
            HEXs(list): The array/list of hex colors.
                         In case of: palette_cp(self) definition -> this argument will be the number of the (source)palette color keys 
                                                                    and it is used only to check if we need to update the palette message while editing it.
            mode(bool): (default to False) For now True only to use inside: palette_cp(self) -> None:

        Returns:
            (None):
        """  
        palette_msg: str = node.parm(MSG_PALETTE).eval()
        if len(HEXs) > 256:
            if PALETTE_PLUS_MSG in palette_msg:
                pass
            else:
                node.setParms({MSG_PALETTE: f"{PALETTE_PLUS_MSG.strip()} {palette_msg.strip()}"}) # type: ignore
                
                if palette_plus_msg and node.parm(PREFS_PALETTE_256_PLUS).eval():
                    _MSG: str = f"OUT Palette 256+: ON"
                    flam3h_general_utils.flash_message(node, PALETTE_PLUS_MSG)
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
        else:
            if PALETTE_PLUS_MSG in palette_msg:
                node.setParms({MSG_PALETTE: f"{palette_msg[len(PALETTE_PLUS_MSG.strip()):]}"}) # type: ignore
                
                if palette_plus_msg and node.parm(PREFS_PALETTE_256_PLUS).eval():
                    _MSG: str = f"OUT Palette 256+: OFF"
                    flam3h_general_utils.flash_message(node, f"{PALETTE_PLUS_MSG} OFF")
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                
            else:
                if not mode: pass
                else:
                    # I do not remember why I am doing this else statement
                    # ...I leave it here for now as there must be a reason for this to exist ;)
                    #
                    # I think it was because from inside the palette_cp(self) definition we are constantly checking
                    # if the current number of color keys are greater than 256 and adjust the palette msg on the fly.
                    flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, palette_msg)
                
    
    @staticmethod 
    def json_to_flam3h_palette_plus_preset_MSG(node: hou.SopNode, _MSG: str) -> None:
        """Check is the plaette plus str "[256+]" is displayed already and add a custom string message(_MSG) to it.
        This is used inside: flam3h_init_presets_CP_PRESETS(self, mode=1) and its run everytime we load a palette file while the presets menu is being initialized.
        
        Args:
            node(hou.SopNode): The current FLAM3H node.
            _MSG(str): The message to add
            
        Returns:
            (None):
        """  
        
        palette_msg: str = node.parm(MSG_PALETTE).eval()
        if PALETTE_PLUS_MSG in palette_msg:
            node.setParms({MSG_PALETTE: f"{PALETTE_PLUS_MSG.strip()} {_MSG.strip()}"}) # type: ignore
        else:
            node.setParms({MSG_PALETTE: f"{_MSG}"}) # type: ignore


    @staticmethod
    def json_to_flam3h_get_preset_name_and_id(node: hou.SopNode) -> tuple[str, int]:
        """Get the selected palette preset name string and its preset_id(index)

        Args:
            node(hou.SopNode): The FLAM3H node
        
        Returns:
            tuple[str, int]: The selected palette preset name string stripped from the icon and enumeration index and the preset_id(index)
        """
        
        # get current preset name
        if node.parm(CP_PVT_ISVALID_PRESET).eval():
            preset_id: int = int(node.parm(CP_PALETTE_PRESETS).eval())
            menu_label: str = str(node.parm(CP_PALETTE_PRESETS).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_PALETTE_LOAD)[-1].strip()
        else:
            preset_id: int = int(node.parm(CP_PALETTE_PRESETS_OFF).eval())
            menu_label: str = str(node.parm(CP_PALETTE_PRESETS_OFF).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_PALETTE_LOAD_EMPTY)[-1].strip()
        
        # Remove the enumeration menu index string from the preset name.
        #
        # We are using "str.lstrip()" because the preset name has been "str.strip()" already on save from inside: self.flam3h_ramp_save_JSON_DATA()
        # and there are only the leading white spaces left from the menu enumaration index number string to remove.
        if node.parm(PREFS_ENUMERATE_MENU).eval(): return ':'.join(menu_label.split(':')[1:]).lstrip(), preset_id
        else: return menu_label, preset_id
        
            
    @staticmethod
    def menu_cp_presets_loop(node: hou.SopNode, menu: list, i: int, item: str) -> None:
        """This is spcifically to be run inside a list comprehension.

        Args:
            node(hou.SopNode): This FLAM3H node.
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            
            # ICON tag
            if i == int(node.parm(CP_PALETTE_PRESETS).eval()):
                node.setCachedUserData('cp_presets_menu_idx', str(i))
                menu.append(f"{FLAM3H_ICON_STAR_PALETTE_LOAD}  {item}     ") # 5 ending \s to be able to read the full label
            else:
                menu.append(f"{item}")
            
            
    @staticmethod
    def menu_cp_presets_loop_enum(node: hou.SopNode, menu: list, i: int, item: str) -> None:
        """This is spcifically to be run inside a list comprehension.

        Args:
            node(hou.SopNode): This FLAM3H node.
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            enum_label: str = str(i + 1) # start count from 1
            
            # ICON tag
            if i == int(node.parm(CP_PALETTE_PRESETS).eval()):
                node.setCachedUserData('cp_presets_menu_idx', str(i))
                menu.append(f"{FLAM3H_ICON_STAR_PALETTE_LOAD}  {enum_label}:  {item}     ") # 5 ending \s to be able to read the full label
            else:
                menu.append(f"{enum_label}:  {item}")
            
            
    @staticmethod
    def menu_cp_presets_empty_loop(node: hou.SopNode, menu: list, i: int, item: str) -> None:
        """This is spcifically to be run inside a list comprehension.

        Args:
            node(hou.SopNode): This FLAM3H node.
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            
            # ICON tag
            if i == int(node.parm(CP_PALETTE_PRESETS_OFF).eval()):
                node.setCachedUserData('cp_presets_menu_off_idx', str(i))
                menu.append(f"{FLAM3H_ICON_STAR_PALETTE_LOAD_EMPTY}  {item}     ") # 5 ending \s to be able to read the full label
            else:
                menu.append(f"{item}")
            
            
    @staticmethod
    def menu_cp_presets_empty_loop_enum(node: hou.SopNode, menu: list, i: int, item: str) -> None:
        """This is spcifically to be run inside a list comprehension.

        Args:
            node(hou.SopNode): This FLAM3H node.
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            enum_label = str(i + 1) # start count from 1
            
            # ICON tag
            if i == int(node.parm(CP_PALETTE_PRESETS_OFF).eval()):
                node.setCachedUserData('cp_presets_menu_off_idx', str(i))
                menu.append(f"{FLAM3H_ICON_STAR_PALETTE_LOAD_EMPTY}  {enum_label}:  {item}     ") # 5 ending \s to be able to read the full label
            else:
                menu.append(f"{enum_label}:  {item}")


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
    def palette_plus_do(self):
        return self._palette_plus_do
    
    
    def cp_preset_name_set(self) -> None:
        """Set the CP Palette preset name parameter after its string is being checked and corrected

        Args:
            (self):

        Returns:
            (None):
        """
        node = self.node
        preset_name: str = node.parm(CP_PALETTE_OUT_PRESET_NAME).eval()
        preset_name_checked: str = out_flame_utils.out_auto_add_iter_num(0, preset_name, 1, False)
        node.setParms({CP_PALETTE_OUT_PRESET_NAME: preset_name_checked})


    def menu_cp_presets_data(self) -> list:
        """Build the palette preset parameter menu entries based on the loaded json palette lib file.
        When a palette preset is currently loaded. This will use the color star icon to signal wich preset is being loaded.

        Args:
            (self):
            
        Returns:
            (list): return menu
        """
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            node = self.node
            filepath: str = os.path.expandvars(node.parm(CP_PALETTE_LIB_PATH).eval())
            
            if os.path.exists(filepath) and node.parm(CP_PVT_ISVALID_FILE).eval() and self.node.parm(CP_PVT_ISVALID_PRESET).eval():
                    
                with open(filepath) as f:
                    menuitems: KeysView = json.load(f).keys()
                    
                menu: list = []
                [self.menu_cp_presets_loop_enum(node, menu, i, item) if node.parm(PREFS_ENUMERATE_MENU).eval() else self.menu_cp_presets_loop(node, menu, i, item) for i, item in enumerate(menuitems)]
                node.setCachedUserData('cp_presets_menu', menu)
                return menu
            
            flam3h_iterator_utils.destroy_cachedUserData(node, 'cp_presets_menu')
            head_tail: tuple = os.path.split(filepath)
            if filepath and os.path.isdir(head_tail[0]) and not os.path.isfile(filepath):
                return MENU_PRESETS_SAVEONE
            elif filepath and not os.path.isfile(filepath):
                return MENU_PRESETS_INVALID
            else:
                return MENU_PRESETS_EMPTY
    
    
    def menu_cp_presets(self) -> list:
        """Rerturn either a cached menu data or rebuild that data on the fly if needed.

        Args:
            (self):
            
        Returns:
            (list): return menu
        """
        # self.node.updateParmStates() 
        if self.kwargs['parm'].isHidden():
            return MENU_PRESETS_EMPTY_HIDDEN
        else:
            # This undo's disabler is needed to make the undo work. They work best in H20.5
            with hou.undos.disabler(): # type: ignore
                
                node = self.node
                data: list | None = node.cachedUserData('cp_presets_menu')
                data_idx: str | None = node.cachedUserData('cp_presets_menu_idx')
                preset_idx: str = node.parm(CP_PALETTE_PRESETS).eval()
                
                # Double check 
                json: str = os.path.expandvars(node.parm(CP_PALETTE_LIB_PATH).eval())
                is_valid: bool = os.path.isfile(json)
                if json and not is_valid:
                    flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_FILE, 0)
                    flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
                    data = None
                elif json and is_valid:
                    # This caused some pain becasue it is forcing us not to tell the truth sometime
                    # but its quick and we added double checks for each file types (Palette or Flame) inside each menus empty presets (CP, IN and OUT)
                    flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_FILE, 1)
                    
                if data is not None and data_idx == preset_idx:
                    return data
                else:
                    return self.menu_cp_presets_data()
    

    def menu_cp_presets_empty_data(self) -> list:
        """Build the palette preset parameter menu entries based on the loaded json palette lib file.
        When no palette preset has been loaded. This will use the empty star icon to signal wich preset is being selected but not loaded.

        This definition exist only becasue if I change the icon dynamically inside: def menu_cp_presets(self) -> list:
        Houdini will not update them until I dnt execute a "next" selection in the menu parameter.

        Args:
            (self):
            
        Returns:
            (list): return menu
        """
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            node = self.node
            filepath: str = os.path.expandvars(self.node.parm(CP_PALETTE_LIB_PATH).eval())

            if self.isJSON_F3H(node, filepath, False)[-1] and node.parm(CP_PVT_ISVALID_FILE).eval() and not node.parm(CP_PVT_ISVALID_PRESET).eval():
                    
                with open(filepath) as f:
                    menuitems: KeysView = json.load(f).keys()
                    
                menu: list = []
                [self.menu_cp_presets_empty_loop_enum(node, menu, i, item) if node.parm(PREFS_ENUMERATE_MENU).eval() else self.menu_cp_presets_empty_loop(node, menu, i, item) for i, item in enumerate(menuitems)]
                node.setCachedUserData('cp_presets_menu_off', menu)
                return menu
                
            flam3h_iterator_utils.destroy_cachedUserData(node, 'cp_presets_menu_off')
            head_tail: tuple = os.path.split(filepath)
            if filepath and os.path.isdir(head_tail[0]) and not os.path.isfile(filepath):
                return MENU_PRESETS_SAVEONE
            if filepath and not os.path.isfile(filepath):
                return MENU_PRESETS_INVALID
            else:
                return MENU_PRESETS_EMPTY
    
    
    def menu_cp_presets_empty(self) -> list:
        """Rerturn either a cached menu data or rebuild that data on the fly if needed.

        Args:
            (self):
            
        Returns:
            (list): return menu
        """
        # self.node.updateParmStates() 
        if self.kwargs['parm'].isHidden():
            return MENU_PRESETS_EMPTY_HIDDEN
        else:
            # This undo's disabler is needed to make the undo work. They work best in H20.5
            with hou.undos.disabler(): # type: ignore
                
                node = self.node
                data: list | None = node.cachedUserData('cp_presets_menu_off')
                data_idx: str | None = node.cachedUserData('cp_presets_menu_off_idx')
                preset_idx: str = node.parm(CP_PALETTE_PRESETS_OFF).eval()
                
                # Double check 
                json: str = os.path.expandvars(node.parm(CP_PALETTE_LIB_PATH).eval())
                is_valid: bool = os.path.isfile(json)
                if json and not is_valid:
                    flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_FILE, 0)
                    flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
                    data = None
                elif json and is_valid:
                    # This caused some pain becasue it is forcing us not to tell the truth sometime
                    # but its quick and we added double checks for each file types (Palette or Flame) inside each menus empty presets (CP, IN and OUT)
                    flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_FILE, 1)
                    
                if data is not None and data_idx == preset_idx:
                    return data
                else:
                    return self.menu_cp_presets_empty_data()


    def flam3h_ramp_save_JSON_DATA(self) -> tuple[dict, str]:
        """Build palette data to save out into a *.json file

        Args:
            (self):

        Returns:
            (tuple[dict, str]): (dict): Raw json data dictionary. (str): indented json data as string
        """
        node = self.node
        # get user's preset name or build an automated one
        presetname: str = str(node.parm(CP_PALETTE_OUT_PRESET_NAME).eval()).strip()
        if not presetname:
            presetname: str = datetime.now().strftime("Palette_%b-%d-%Y_%H%M%S")

        # Update HSV ramp before getting it
        self.palette_cp()

        hsv_vals_prm: tuple = node.parmTuple(CP_RAMP_HSV_VAL_NAME).eval()
        if node.parm(CP_RAMP_SAVE_HSV).eval():
            palette: hou.Ramp = node.parm(CP_RAMP_HSV_NAME).evalAsRamp()
            hsv_vals_prm = (1.0, 1.0, 1.0)
        else:
            palette: hou.Ramp = node.parm(CP_RAMP_SRC_NAME).evalAsRamp()
            
        keys_count: str = out_flame_utils(self.kwargs).out_palette_keys_count(self.palette_plus_do, len(palette.keys()), 1, False)
        POSs: list = list(iter_islice(iter_count(0, 1.0/(int(keys_count)-1)), int(keys_count)))
        HEXs: list = [self.rgb_to_hex(palette.lookup(p)) for p in POSs]
        
        if hsv_vals_prm[0] == hsv_vals_prm[1] == hsv_vals_prm[2] == 1:
            json_dict: dict[str, dict[str, str]] = { presetname: {CP_JSON_KEY_NAME_HEX: ''.join(HEXs),  } }
        else:
            hsv_vals: str = ' '.join([str(x) for x in hsv_vals_prm])
            json_dict: dict[str, dict[str, str]] = { presetname: {CP_JSON_KEY_NAME_HEX: ''.join(HEXs), CP_JSON_KEY_NAME_HSV: hsv_vals} }
            
        # OUTPUT DATA
        return json_dict, json.dumps(json_dict, indent=4)


    def flam3h_ramp_save(self) -> None:
        """Save the current color palette into a json file.
        This wil also save the HSV values along with it.
        
        There is also the option to save the HSV palette instead but be cautious
        as when saving the HSV palette, its colors will be clamped. [0-255]
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        node = self.node
        # Force this data to be rebuilt
        flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node)
        flam3h_iterator_utils(self.kwargs).update_xml_last_loaded()
        
        # ALT - Copy palette to the clipboard
        if self.kwargs['alt']:
            
            json_dict, json_data = self.flam3h_ramp_save_JSON_DATA()
            hou.ui.copyTextToClipboard(json_data) # type: ignore
            # Clear up palette preset name if any
            node.setParms({CP_PALETTE_OUT_PRESET_NAME: ''})
            # Satus message
            _MSG: str = f"{node.name()}: SAVE Palette Clipboard. Palette copied to the clipboard -> Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"CP SAVED to the Clipboard")
        
        # Save palette into a file
        else:
            palettepath: str = node.parm(CP_PALETTE_LIB_PATH).eval()
            out_path_checked: str | bool = out_flame_utils.out_check_outpath(node, palettepath, OUT_PALETTE_FILE_EXT, AUTO_NAME_CP)

            if out_path_checked is not False:
                assert isinstance(out_path_checked, str)
                
                # SHIFT - Open a file explorer to the file location
                if self.kwargs['shift']:
                    flam3h_general_utils.util_open_file_explorer(out_path_checked)
                    
                else:
                    
                    if flam3h_general_utils.isLOCK(out_path_checked):
                        ui_text = f"This Palette library is Locked."
                        ALL_msg = f"This Palette library is Locked and you can not modify this file.\n\nTo Lock a Palete lib file just rename it using:\n\"{FLAM3H_LIB_LOCK}\" as the start of the filename.\n\nOnce you are happy with a palette library you built, you can rename the file to start with: \"{FLAM3H_LIB_LOCK}\"\nto prevent any further modifications to it. For example if you have a lib file call: \"my_rainbows_colors.json\"\nyou can rename it to: \"{FLAM3H_LIB_LOCK}_my_rainbows_colors.json\" to keep it safe."
                        _MSG: str = f"{node.name()}: PALETTE library file -> is LOCKED"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, f"This Palette file is LOCKED")
                        if hou.isUIAvailable():
                            hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.ImportantMessage, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Palette Lock", details=ALL_msg, details_label=None, details_expanded=False) # type: ignore
                        
                        # Clear up status bar msg
                        flam3h_general_utils.set_status_msg('', 'MSG')
                        
                    else:
                        _isNEW: bool = False
                        # F3H palette json file checks
                        json_file, f3h_json_file = self.isJSON_F3H(node, out_path_checked, False)
                        
                        # build palette data to save
                        json_dict, json_data = self.flam3h_ramp_save_JSON_DATA()

                        if self.kwargs["ctrl"]:
                            
                            if not os.path.exists(out_path_checked):
                                with open(out_path_checked,'w') as w:
                                    w.write(json_data)
                                    
                            elif json_file and f3h_json_file:
                                os.remove(out_path_checked)
                                with open(out_path_checked,'w') as w:
                                    w.write(json_data)
                                    
                            else:
                                _MSG: str = f"{node.name()}: Palette JSON SAVE: Although the JSON file you loaded is legitimate, it does not contain any valid FLAM3H Palette data."
                                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                                flam3h_general_utils.flash_message(node, f"CP SAVE: Not a valid FLAM3H JSON palette file")
                                
                        else:
                            # if the file exist and is a valid JSON file
                            if json_file and f3h_json_file:
                                
                                with open(out_path_checked,'r') as r:
                                    prevdata = json.load(r)
                                    
                                newdata: dict = json_dict
                                prevdata.update(newdata)
                                data: dict | str = json.dumps(prevdata, indent = 4)
                                assert isinstance(data, str)
                                with open(out_path_checked, 'w') as w:
                                    w.write(data)
                                    
                            # Otherwise mean it is either not a F3H json file, empty or not exist,
                            # just create one with the current ramp in it
                            #
                            # Note that we already checked for a proper file extension with:
                            # def out_flame_utils.out_check_outpath(...)
                            # so to not override something else by accident
                            else:
                                # If the file do not exist, lets create it and save the palette in it
                                if not os.path.isfile(out_path_checked):
                                    with open(out_path_checked,'w') as w:
                                        w.write(json_data)
                                    # Mark as a new file
                                    _isNEW = True

                        # We do this again so we can read the newly created file if any 
                        json_file, f3h_json_file = self.isJSON_F3H(node, out_path_checked, False)
                        if json_file and f3h_json_file:
                            
                            # Set some parameters
                            with open(out_path_checked) as f:
                                data: dict | str = json.load(f)
                            
                            # Set all CP preset menus parameter index
                            assert isinstance(data, dict)
                            [prm.set(str(len(data.keys())-1)) for prm in (node.parm(CP_PALETTE_PRESETS), node.parm(CP_PALETTE_PRESETS_OFF), node.parm(CP_SYS_PALETTE_PRESETS), node.parm(CP_SYS_PALETTE_PRESETS_OFF))]
                            # Clearup the Palette name if any were given
                            node.setParms({CP_PALETTE_OUT_PRESET_NAME: ''})
                            # Mark this as a valid file and as the currently loaded preset as it is the preset we just saved
                            flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_FILE, 1)
                            flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 1)
                            # Make sure to update the tmp ramp with the just saved one
                            self.palette_cp_to_tmp()
                            del data
                            
                            # Set the file path to the corrected one
                            node.setParms({CP_PALETTE_LIB_PATH: out_path_checked})
                            
                            # Something odd in how the messages are running, need to investigate why
                            _MSG: str = f"Palette SAVED"
                            if _isNEW and flam3h_palette_utils.isJSON_F3H(node, out_path_checked):
                                flam3h_general_utils(self.kwargs).flam3h_init_presets_CP_PRESETS(1, True, json_file, f3h_json_file, out_path_checked)
                                # Mark this as a valid file and as the currently loaded preset as it is the first ever preset we just saved into this file
                                flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_FILE, 1)
                                flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 1)
                                if flam3h_general_utils.isLOCK(out_path_checked):
                                    flam3h_general_utils.flash_message(node, f"{_MSG} and LOCKED")
                                else:
                                    flam3h_general_utils.flash_message(node, _MSG)
                            else:
                                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                                flam3h_general_utils.flash_message(node, _MSG)
                            
                        else:
                            # Just in case lets set those
                            flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_FILE, 0)
                            flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
                            
                            if json_file:
                                # If it is a legitimate JSON file
                                _MSG: str = f"{node.name()}: Palette JSON SAVE: Although the JSON file you loaded is legitimate, it does not contain any valid F3H Palette data."
                                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                                flam3h_general_utils.flash_message(node, f"CP SAVE: Not a valid F3H JSON palette file")
                            else:
                                # If it is any other file
                                _MSG: str = f"{node.name()}: Palette JSON SAVE: CP file not a valid PALETTE F3H file."
                                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                                flam3h_general_utils.flash_message(node, f"CP SAVE: Not a valid F3H JSON palette file")
                        
            else:
                _MSG: str = f"{node.name()}: SAVE Palette: Select a valid output file or a valid filename to create first."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"CP: Select a valid output file")


    def json_to_flam3h_ramp_initialize(self, rgb_from_XML_PALETTE: list) -> tuple[hou.Ramp, int, bool]:
        """It will check the passed list of colors for validity and build a Houdini ramp parameter's values from it.
        If not valid, or only one coclor is included, it will output one RED color and mark this palette as an Error.

        Args:
            (self):
            rgb_from_XML_PALETTE(list): a list of colors collected from the palette json file preset (from file or from Clipboard)
            
        Returns:
            (tuple[hou.Ramp, int, bool]): Return a tuple containing: a houdini Ramp parameter, number of keys and True or False if the operation succeded or not. If False, it will build an error Ramp instead.
        """  
        _CHECK: bool = True
        if rgb_from_XML_PALETTE:
            
            try:
                POSs: list = list(iter_islice(iter_count(0, 1.0/(len(rgb_from_XML_PALETTE)-1)), len(rgb_from_XML_PALETTE)))
                BASEs: list = [hou.rampBasis.Linear] * len(rgb_from_XML_PALETTE) # type: ignore
            except:
                # If something goes wrong...set one RED key only
                BASEs, POSs, rgb_from_XML_PALETTE = self.build_ramp_palette_error()
                _CHECK = False
                
        else:
            BASEs, POSs, rgb_from_XML_PALETTE = self.build_ramp_palette_error()
            _CHECK = False
            
        # Set lookup samples to the default value of: 256
        self.node.setParms({CP_RAMP_LOOKUP_SAMPLES: 256})
        return hou.Ramp(BASEs, POSs, rgb_from_XML_PALETTE), len(POSs), _CHECK


    def json_to_flam3h_ramp_set_HSV(self, node, hsv_check: bool, hsv_vals: list) -> None:
        """Set the HSV values to either the one comeing from the loaded palette preset or to default values.

        Args:
            (self):
            node(hou.SopNode): The current FLAM3H node.
            hsv_check(bool): True if the loaded palette preset posses its own HSV values or False if not.
            hsv_vals(list): If hsv_check is True, this will hold the values to be used to set the HSV parameter's values.

        Returns:
            (None):
        """
        keep_hsv: int = node.parm(CP_RAMP_HSV_KEEP_ON_LOAD).eval()
        if not keep_hsv:
            if hsv_check:
                node.setParms({CP_RAMP_HSV_VAL_NAME: hou.Vector3(hsv_vals)})
            else:
                # This is for backward compatibility ( when the hsv data wasn't being exported yet )
                node.setParms({CP_RAMP_HSV_VAL_NAME: hou.Vector3((1, 1, 1))})


    def json_to_flam3h_ramp_SET_PRESET_DATA(self, node: hou.SopNode) -> None:
        """From the loaded palette preset data finally set the palette.

        Args:
            (self):
            node(hou.SopNode): This FLAM3H node.
            
        Returns:
            (None):
        """
        node = self.node
        
        iterators_num: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        if iterators_num:
            
            filepath: str = os.path.expandvars(node.parm(CP_PALETTE_LIB_PATH).eval())
            if self.isJSON_F3H_on_preset_load(node, filepath, False)[-1]:
                
                # get ramps parm
                rmp_src = node.parm(CP_RAMP_SRC_NAME)
                rmp_hsv = node.parm(CP_RAMP_HSV_NAME)
                # get current preset name and preset_id(index)
                preset, preset_id = self.json_to_flam3h_get_preset_name_and_id(node)
                
                # 'hsv_check' is for backward compatibility
                with open(filepath, 'r') as r:
                    data: dict = json.load(r)[preset]
                    
                try:
                    hsv_vals: list = [float(x) for x in data[CP_JSON_KEY_NAME_HSV].split(' ')]
                    hsv_check: bool = True
                except:
                    hsv_vals: list = []
                    hsv_check: bool = False
                
                # Get usable color values
                HEXs: list = [hex for hex in wrap(data[CP_JSON_KEY_NAME_HEX], 6)]
                try:
                    RGBs: list = [list(map(abs, self.hex_to_rgb(hex))) for hex in HEXs]
                except:
                    rgb_from_XML_PALETTE: list = []
                else:
                    rgb_from_XML_PALETTE: list = [(RGBs[idx][0]/(255 + 0.0), RGBs[idx][1]/(255 + 0.0), RGBs[idx][2]/(255 + 0.0)) for idx in range(len(HEXs))]
                
                del data
                
                # Initialize and SET new ramp first
                _RAMP, _COUNT, _CHECK = self.json_to_flam3h_ramp_initialize(rgb_from_XML_PALETTE)
                rmp_src.set(_RAMP) # Load the new palette colors
                # Make sure we update the HSV palette
                rmp_hsv.set(_RAMP) # Load the new palette colors
                self.json_to_flam3h_ramp_set_HSV(node, hsv_check, hsv_vals) # Set HSV values
                self.palette_hsv() # Apply HSV values if any
                # Update palette tmp
                self.palette_cp_to_tmp()
                # Update/Set palette MSG
                flam3h_palette_utils.json_to_flam3h_palette_plus_MSG(node, HEXs)
                
                # Set palette lookup samples
                # Note we are setting the function type to: Flame(0) so we always clamp at the minimun of 256 lookup samples
                keys: str = out_flame_utils(self.kwargs).out_palette_keys_count(self.palette_plus_do, _COUNT, 0, False)
                node.setParms({CP_RAMP_LOOKUP_SAMPLES: int(keys)}) # type: ignore
                # Store selection into all preset menu just in case ;)
                [prm.set(str(preset_id)) for prm in (node.parm(CP_SYS_PALETTE_PRESETS), node.parm(CP_SYS_PALETTE_PRESETS_OFF), node.parm(CP_PALETTE_PRESETS), node.parm(CP_PALETTE_PRESETS_OFF))]
                
                # Force this data to be rebuilt - This need to be reworked as it is slowing things down on H20.5
                # This is needed to help to updates the menus from time to time so to pick up sneaky changes to the loaded files
                # (ex. the user perform hand made modifications like renaming a Preset and such).
                flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node, False)
                flam3h_iterator_utils(self.kwargs).update_xml_last_loaded()
                
                if _CHECK:
                    flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 1)
                    _MSG: str = f"{node.name()}: LOAD Palette preset: \"{preset}\" -> Completed"
                    flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                    flam3h_general_utils.flash_message(node, f"CP LOADED")
                else:
                    flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
                    _MSG: str = f"{node.name()}: PALETTE: ERROR on preset: \"{preset}\". Invalid HEX values."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                    flam3h_general_utils.flash_message(node, f"CP ERROR")
            
            else:
                _MSG: str = f"{node.name()}: PALETTE: Nothing to load"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                flam3h_general_utils.flash_message(node, f"CP: Nothing to load")


    def json_to_flam3h_ramp_sys(self, use_kwargs: bool = True) -> None:
        """Load the selected palette preset from the provided json file
        using the SYS load palette button.

        Args:
            (self):
            use_kwargs(bool): Default to: True. Use the houdini kwargs arguments or not. This is being done as when this definition run from a menu parameter the kwargs arguments are not available. 
        
        Returns:
            (None):
        """
        
        if use_kwargs:
            self.json_to_flam3h_ramp(use_kwargs)
            
        else:
            node = self.node
            if node.parm(CP_PVT_ISVALID_PRESET).eval():
                preset_id: str = node.parm(CP_SYS_PALETTE_PRESETS).eval()
                node.setParms({CP_SYS_PALETTE_PRESETS_OFF: preset_id})
            else:
                preset_id: str = node.parm(CP_SYS_PALETTE_PRESETS_OFF).eval()
                node.setParms({CP_SYS_PALETTE_PRESETS: preset_id})
                
            node.setParms({CP_PALETTE_PRESETS: preset_id})
            node.setParms({CP_PALETTE_PRESETS_OFF: preset_id}) 
            self.json_to_flam3h_ramp(use_kwargs)


    def json_to_flam3h_ramp_SHIFT(self, node: hou.SopNode) -> None:
        """When kwargs['shift'] -> Open a file chooser to select palette json file to load.

        Args:
            (self):
            node(hou.SopNode): This FLAM3H node.
        
        Returns:
            (None):
        """
        filepath: str = hou.ui.selectFile(start_directory=None, title="FLAM3H: Load a palette *.json file", collapse_sequences=False, file_type=hou.fileType.Any, pattern="*.json", default_value=None, multiple_select=False, image_chooser=None, chooser_mode=hou.fileChooserMode.Read, width=0, height=0)  # type: ignore
        filepath_expandvars: str = os.path.expandvars(filepath)
        dir: str = os.path.dirname(filepath_expandvars)
        if os.path.isdir(dir):
            node.setParms({CP_PALETTE_LIB_PATH: filepath_expandvars}) # type: ignore
            # The following definition use the default arg's value so it can set the proper ramp message if needed.
            flam3h_general_utils(self.kwargs).flam3h_init_presets_CP_PRESETS()

            
    def json_to_flam3h_ramp_CTRL(self, node: hou.SopNode) -> None:
        """When kwargs['ctrl'] -> Copy the preset name into the Palette name parameter.

        Args:
            (self):
            node(hou.SopNode): This FLAM3H node.
        
        Returns:
            (None):
        """
        
        filepath: str = os.path.expandvars(node.parm(CP_PALETTE_LIB_PATH).eval())
        if self.isJSON_F3H_on_preset_load(node, filepath, False)[-1]:
            
            # get current preset name and preset_id(index)
            preset, preset_id = self.json_to_flam3h_get_preset_name_and_id(node)
            # SET the Palette name to the preset name
            if preset:
                node.setParms({CP_PALETTE_OUT_PRESET_NAME: preset}) # type: ignore
                flam3h_general_utils.flash_message(node, preset)
            
            
    def json_to_flam3h_ramp_ALT(self, node: hou.SopNode) -> None:
        """When kwargs['alt'] -> Load palette data from the clipboard.

        Args:
            (self):
            node(hou.SopNode): This FLAM3H node.
        
        Returns:
            (None):
        """
        
        palette: str = hou.ui.getTextFromClipboard() # type: ignore
        try:
            data: dict | None = json.loads(palette)
        except:
            data: dict | None = None
        
        # If it is a valid json data
        if data is not None:
            
            try:
                preset: str | None = list(data.keys())[0]
                del data
            except: preset: str | None = None
                
            if preset is not None:
                
                data: dict | None = json.loads(palette)[preset]
                try:
                    assert data is not None
                    # Check if it is a valid FLAM3H JSON data. This is the moment of the truth ;)
                    hex_values: str = data[CP_JSON_KEY_NAME_HEX]
                except:
                    isJSON_F3H: bool = False
                    _MSG: str = f"{node.name()}: PALETTE JSON load -> Although the JSON file you loaded is legitimate, it does not contain any valid FLAM3H Palette data."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                else:
                    isJSON_F3H: bool = True
                    
                # If it is a valid FLAM3H Palette JSON data
                if isJSON_F3H:
                    assert data is not None
                    
                    # get ramps parm
                    rmp_src = node.parm(CP_RAMP_SRC_NAME)
                    rmp_hsv = node.parm(CP_RAMP_HSV_NAME)

                    try:
                        hsv_vals: list = [float(x) for x in data[CP_JSON_KEY_NAME_HSV].split(' ')]
                    except:
                        hsv_vals: list = []
                        hsv_check: bool = False
                    else:
                        hsv_check: bool = True
                    
                    # Get usable color values
                    HEXs: list = [hex for hex in wrap(data[CP_JSON_KEY_NAME_HEX], 6)]
                    try:
                        RGBs: list = [list(map(abs, self.hex_to_rgb(hex))) for hex in HEXs]
                    except:
                        rgb_from_XML_PALETTE: list = []
                    else:
                        rgb_from_XML_PALETTE: list = [(RGBs[idx][0]/(255 + 0.0), RGBs[idx][1]/(255 + 0.0), RGBs[idx][2]/(255 + 0.0)) for idx in range(len(HEXs))]
                        
                    del data
                    
                    # Initialize and SET new ramp.
                    _RAMP, _COUNT, _CHECK = self.json_to_flam3h_ramp_initialize(rgb_from_XML_PALETTE)
                    rmp_src.set(_RAMP)
                    # Make sure we update the HSV palette
                    rmp_hsv.set(_RAMP) # Load the new palette colors
                    self.json_to_flam3h_ramp_set_HSV(node, hsv_check, hsv_vals) # Set HSV values
                    self.palette_hsv()# Apply HSV values if any
                    # Update palette tmp
                    self.reset_CP_TMP()
                    # Update/Set palette MSG
                    flam3h_palette_utils.json_to_flam3h_palette_plus_MSG(node, HEXs)
                    
                    # Set palette lookup samples
                    # Note we are setting the function type to: Flame so we always clamp at the minimun of 256 lookup samples
                    keys: str = out_flame_utils(self.kwargs).out_palette_keys_count(self.palette_plus_do, _COUNT, 0, False)
                    node.setParms({CP_RAMP_LOOKUP_SAMPLES: int(keys)}) # type: ignore
                    
                    # Mark this as not a loaded preset since it is coming from the Clipboard
                    flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
                    
                    if _CHECK:
                        _MSG: str = f"{node.name()}: PALETTE Clipboard: LOAD Palette preset: \"{preset}\" -> Completed"
                        flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                        flam3h_general_utils.flash_message(node, f"CP LOADED from the Clipboard")
                    else:
                        _MSG: str = f"{node.name()}: PALETTE Clipboard: ERROR on preset: \"{preset}\". Invalid HEX values."
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, f"CP ERROR from the Clipboard")
                    
            else:
                _MSG: str = f"{node.name()}: PALETTE Clipboard: The data from the clipboard is not a valid F3H Palette data (JSON or XML)."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"CP Clipboard: Nothing to load")
                
        else:
            # Check if a full Flame preset is stored into the clipboard instead
            # and if so load its palette in.
            _FLAM3H_INIT_DATA: tuple = in_flame_utils(self.kwargs).in_to_flam3h_init_data(node)
            xml, clipboard, preset_id, flame_name_clipboard, attempt_from_clipboard, chaos = _FLAM3H_INIT_DATA

            if xml is not None and clipboard:
                apo_data = in_flame_iter_data(node, xml, preset_id)
                in_flame_utils(self.kwargs).in_to_flam3h_set_palette(node, apo_data, _FLAM3H_INIT_DATA, True)
                _MSG: str = f"{node.name()}: PALETTE Clipboard: LOAD Palette data from Flame preset: \"{_FLAM3H_INIT_DATA[3]}\" -> Completed"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                flam3h_general_utils.flash_message(node, f"CP LOADED from the Clipboard")
            else:
                _MSG: str = f"{node.name()}: Palette Clipboard: The data from the clipboard is not a valid F3H Palette data (JSON or XML)."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"CP Clipboard: Nothing to load")
                         

    def json_to_flam3h_ramp(self, use_kwargs: bool = True) -> None:
        """Load the selected palette preset from the provided json file
        
        Args:
            (self):
            use_kwargs(bool): Default to True. Use the houdini kwargs arguments or not. Defaults to True. This is being done as when this definition run from a menu parameter the kwargs arguments are not available. 

        Returns:
            (None):
        """
        
        node = self.node
        
        # KWARGS
        if use_kwargs:
                
            # SHIFT - If we are selecting a palette json file to load
            if self.kwargs['shift']:
                self.json_to_flam3h_ramp_SHIFT(node)

            # CTRL - If we are just copying the preset name into the Palette name parameter
            elif self.kwargs['ctrl']:
                self.json_to_flam3h_ramp_CTRL(node)
                
            # ALT - If we are loading a palette from the clipboard
            elif self.kwargs['alt']:
                self.json_to_flam3h_ramp_ALT(node)

            # LMB - Load the currently selected palette preset
            else:
                self.json_to_flam3h_ramp_SET_PRESET_DATA(node)

        # NO KWARGS - LMB - Load the currently selected palette preset
        #
        # This is used from the preset menus parameter, since kwargs are not available from here.
        else:
            self.json_to_flam3h_ramp_SET_PRESET_DATA(node)


    def palette_cp(self, palette_plus_msg: bool = False) -> None:
        """Force the HSV palette colors/keys to match the source palette colors/keys.
        
        Args:
            (self):
            palette_plus_msg(bool): Default to False. Coordinate messages about palette 256+ when the preferences option: "palette 256+" is ON
            
        Returns:
            (None):
        """    
        node = self.node
        rmpsrc: hou.Ramp = node.parm(CP_RAMP_SRC_NAME).evalAsRamp()
        rmphsv = node.parm(CP_RAMP_HSV_NAME)
        rmphsv.set(rmpsrc)
        # Apply HSV if any
        #
        # self.palette_hsv is running also inside self.palette_lock()
        # becasue it used to get call also from other Houdini parameter's callback scripts.
        # Need to come back and make changes...
        self.palette_hsv()
        
        if node.parm(CP_PVT_ISVALID_FILE).eval():
            rmptmp: hou.Ramp = node.parm(CP_RAMP_TMP_NAME).evalAsRamp()
            if rmpsrc.keys() != rmptmp.keys() or rmpsrc.values() != rmptmp.values():
                # Mark this as not a loaded palette preset
                flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
            else:
                # Mark this as a loaded palette preset since they match
                flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 1)

        # Update/Set palette MSG
        flam3h_palette_utils.json_to_flam3h_palette_plus_MSG(node, rmpsrc.keys(), True, palette_plus_msg)    


    def palette_cp_to_tmp(self) -> None:
        """Make a copy of the source palette into the temp palette.
        This is used when loading a palette preset to check if the user made modifications to the loaded palette.

        Args:
            (self):
            
        Returns:
            (None):
        """    
        node = self.node
        rmpsrc: hou.Ramp = node.parm(CP_RAMP_SRC_NAME).evalAsRamp()
        rmptmp = node.parm(CP_RAMP_TMP_NAME)
        rmptmp.set(rmpsrc)


    def palette_hsv(self) -> None:
        """Apply a HSV to the paltte colors/keys.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        node = self.node
        hsvprm_vals: tuple = node.parmTuple(CP_RAMP_HSV_VAL_NAME).eval()
        if hsvprm_vals[0] != 1 or hsvprm_vals[1] != 1 or hsvprm_vals[2] != 1:
            
            # Apply color correction
            rmpsrc: hou.Ramp = node.parm(CP_RAMP_SRC_NAME).evalAsRamp()
            _RGBs: list = [colorsys.hsv_to_rgb( item[0] + hsvprm_vals[0], item[1] * hsvprm_vals[1], item[2] * hsvprm_vals[2] ) for item in list(map(lambda x: colorsys.rgb_to_hsv(x[0], x[1], x[2]), rmpsrc.values()))]
            # Set the ramp
            rmphsv = node.parm(CP_RAMP_HSV_NAME)
            rmphsv.set(hou.Ramp(rmpsrc.basis(), rmpsrc.keys(), _RGBs))


    def palette_lock(self) -> None:
        """Lock the HSV palette color/keys from being modified.
        This is also used to updated the palette HSV to keep it up to date with the source palette.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        self.palette_cp()
        # self.palette_hsv is running also inside self.palette_cp()
        # becasue it get call also from other Houdini parameter's callback scripts.
        # Need to come back and make changes...
        self.palette_hsv()


    def reset_CP_LOCK_MSG(self) -> None:
        """Clearup the palette lib LOCK message if there is a need to do so.
        
        With the add of the palette [256+] feature,
        this definition will probably need an updated. Will come back to investigate on this...

        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        filepath: str = node.parm(CP_PALETTE_LIB_PATH).eval()
        if self.isJSON_F3H(node, filepath, False)[0]:
            if flam3h_general_utils.isLOCK(filepath) is False:
                node.setParms({MSG_PALETTE: ''})
        else:
            node.setParms({MSG_PALETTE: ''})


    def reset_CP_TMP(self) -> None:
        """Reset the TEMP palette to its defaults.

        Args:
            (self):
            
        Returns:
            (None):
        """
        # CP->tmp ramp RESET
        ramp_tmp_parm = self.node.parm(CP_RAMP_TMP_NAME)
        self.delete_ramp_all_keyframes(ramp_tmp_parm)
        # Build TMP ramp
        self.build_ramp_palette_temp(ramp_tmp_parm)
        
        
    def reset_CP_options(self) -> None:
        """Reset the CP tab options toggles to their defaults.

        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        node.setParms({CP_RAMP_LOOKUP_SAMPLES: 256})
        node.setParms({CP_RAMP_SAVE_HSV: 0})
        self.reset_CP_LOCK_MSG()


    def reset_CP_run_0(self) -> None:
        """Reset the CP tab to its defaults.

        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        # CP
        node.setParms({CP_RAMP_HSV_VAL_NAME: hou.Vector3((1.0, 1.0, 1.0))})
        # CP->ramp
        rmp_src = node.parm(CP_RAMP_SRC_NAME)
        # Reset ramps
        #
        # SRC
        self.build_ramp_palette_default(rmp_src)
        self.delete_ramp_all_keyframes(rmp_src)
        # HSV
        self.palette_cp()
        rmp_hsv = node.parm(CP_RAMP_HSV_NAME)
        self.delete_ramp_all_keyframes(rmp_hsv)
        # Reset CP options tab
        self.reset_CP_options()
        # CP->tmp ramp RESET
        self.reset_CP_TMP()
        # Mark this as not a loaded preset
        flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
        
        
    def reset_CP_run_1(self) -> None:
        """Delete all ramps keyframes (Palette and HSV Palette)

        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        # CP->ramp
        rmp_scr = node.parm(CP_RAMP_SRC_NAME)
        rmp_hsv = node.parm(CP_RAMP_HSV_NAME)
        # Reset ramps
        self.delete_ramp_all_keyframes(rmp_scr)
        self.delete_ramp_all_keyframes(rmp_hsv)
        # Messages
        _MSG: str = f"CP Keyframes: DELETED"
        flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
        flam3h_general_utils.flash_message(node, _MSG)

        
    def reset_CP_run_2(self) -> None:
        """Reset the CP tab HSV values to their defaults.

        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        hsv_prm = node.parmTuple(CP_RAMP_HSV_VAL_NAME)
        _hsv: tuple = hsv_prm.eval()
        if _hsv[0] == _hsv[1] == _hsv[2] == 1:
            hsv_prm.deleteAllKeyframes()
            _MSG: str = f"CP HSV: already at its default values."
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
            flam3h_general_utils.flash_message(node, _MSG)
        else:
            hsv_prm.deleteAllKeyframes()
            hsv_prm.set(hou.Vector3((1.0, 1.0, 1.0)))
            # Print out to Houdini's status bar
            _MSG: str = f"CP HSV: RESET"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
            flam3h_general_utils.flash_message(node, _MSG)
            
        # CP->tmp ramp RESET
        self.reset_CP_TMP()
        # # Update palette py
        self.palette_cp()
        # Mark this as not a loaded preset
        flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)


    def reset_CP_run_3(self) -> None:
        """Reset the CP tab Palette ramp to its defaults ( and the HSV palette too ).

        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        rmp_src = node.parm(CP_RAMP_SRC_NAME)
        # Build ramp
        #
        # SRC
        self.build_ramp_palette_default(rmp_src)
        self.delete_ramp_all_keyframes(rmp_src)
        # HSV
        self.palette_cp()
        rmp_hsv = node.parm(CP_RAMP_HSV_NAME)
        self.delete_ramp_all_keyframes(rmp_hsv)
        
        # CP->tmp ramp RESET
        self.reset_CP_TMP()
        # Mark this as not a loaded preset
        flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
        # Set lookup samples to the default value of: 256
        node.setParms({CP_RAMP_LOOKUP_SAMPLES: 256})
        
        # Print out to Houdini's status bar
        _MSG: str = f"CP: RESET"
        flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
        flam3h_general_utils.flash_message(node, _MSG)
        
    
    def reset_CP(self, mode: int=0) -> None:
        """Run the desired reset_CP(...) definition.

        Args:
            (self):
            mode(int): definition idx to run

        Returns:
            (None):
        """
        func_list: dict[int, Callable[[], None]] = {0: self.reset_CP_run_0, 1: self.reset_CP_run_1, 2: self.reset_CP_run_2, 3: self.reset_CP_run_3}
        run: Callable[[], None] | None = func_list.get(mode)
        if run is not None: run()
        else: flam3h_general_utils.set_status_msg(f"{self.node.name()}: reset_CP(...) python definition have nothing to run with the passed \"mode\" value: {mode}", 'WARN')
        
        
    def reset_CP_palette_action(self) -> None:
        """Run the desired reset_CP(...) from the Palette action button.

        Args:
            (self):
            
        Returns:
            (None):
        """
        if self.kwargs['ctrl']: self.reset_CP(1)
        else: self.reset_CP(3)


# FLAM3H ABOUT start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class flam3h_about_utils():
    """
class flam3h_about_utils

@METHODS
* flam3h_about_msg(self) -> None:
* flam3h_about_plugins_msg(self) -> None:
* flam3h_about_web_msg(self) -> None:
* flam3h_about_web_homepage(self) -> None:
* flam3h_about_web_github(self) -> None:
* flam3h_about_web_instagram(self) -> None:
* flam3h_about_web_youtube(self) -> None:
* flam3h_about_web_flam3_paper(self) -> None:
* flam3h_about_web_flam3_github(self) -> None:
* flam3h_web_run(self, key: str) -> None:
    """
    
    __slots__ = ("_kwargs", "_node")
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs: dict = kwargs
        self._node = kwargs['node']
        

    # CLASS: PROPERTIES
    ##########################################
    ##########################################
        
    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node
        

    def flam3h_about_msg(self) -> None:
        """Build and set the FLAM3H about message.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        
        nl: str = "\n"
        nnl: str = "\n\n"
            
        # year = datetime.now().strftime("%Y")
        
        flam3h_author: str = f"AUTHOR: {__author__}"
        flam3h_cvex_version: str = f"CODE: cvex H19.x.x"
        hou_version : int = flam3h_general_utils.houdini_version()
        if hou_version >= 19: flam3h_cvex_version = f"CODE: cvex H{str(hou_version)}.x.x"
        flam3h_python_version: str = f"py 3.11.7"
        flam3h_houdini_version: str = f"VERSION: {__version__} - {__status__} :: ({__license__})"
        Implementation_build: str = f"{flam3h_author}\n{flam3h_houdini_version}\n{flam3h_cvex_version}, {flam3h_python_version}\n{__copyright__}"
        
        code_references: str = """CODE REFERENCES
Flam3 :: (GPL)
Apophysis :: (GPL)
Fractorium :: (GPL)"""

        special_thanks: str = """SPECIAL THANKS
Praveen Brijwal"""

        example_flames: str = """EXAMPLE FLAMES
C-91, Gabor Timar, Golubaja, Pillemaster,
Plangkye, Tatasz, Triptychaos, TyrantWave,
Zy0rg, Seph, Lucy, b33rheart, Neonrauschen."""
        
        h_version: str = '.'.join(str(x) for x in hou.applicationVersion())
        Houdini_version: str = f"HOST\nSideFX Houdini {h_version}"
        Python_version: str = f"Python: {python_version()}"
        license_type: str = str(hou.licenseCategory()).split(".")[-1]
        Houdini_license: str = f"License: {license_type}"
        User: str = f"User: {hou.userName()}"
        PC_name: str = f"Machine name: {hou.machineName()}"
        Platform: str = f"Platform: {hou.applicationPlatformInfo()}"
        
        build: tuple = (Implementation_build, nnl,
                        code_references, nnl,
                        special_thanks, nnl,
                        example_flames, nnl,
                        Houdini_version, nl,
                        Houdini_license, nl,
                        Python_version, nl,
                        User, nl,
                        PC_name, nl,
                        Platform
                        )
        
        self.node.setParms({MSG_FLAM3H_ABOUT: "".join(build)})


    def flam3h_about_plugins_msg(self) -> None:
        """Build and set the FLAM3H about plugins message.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        vars_sorted: list = [var.capitalize() for var in sorted(VARS_FLAM3_DICT_IDX.keys()) if var not in ("linear3d",)]
        n: int = 5
        vars_sorted_grp: list = [vars_sorted[i:i + n] for i in range(0, len(vars_sorted), n)]
        vars_txt: str = "".join( [", ".join(grp) + "." if idx == (len(vars_sorted_grp)-1) else ", ".join(grp) + ",\n" for idx, grp in enumerate(vars_sorted_grp)] )
        vars_txt_MSG: str = f"They are also available as PRE and POST.\n\nNumber of plugins/variations: {len(vars_sorted)}\n\n{vars_txt}"
        self.node.setParms({MSG_FLAM3H_PLUGINS: vars_txt_MSG})
        
        
    def flam3h_about_web_msg(self) -> None:
        """Build and set the FLAM3H about web heading's msgs.
        
        Args:
            (self):
            
        Returns:
            (None):
        """    
        
        node = self.node
        
        # values
        _FLAM3HWEB_MSG: str = 'FLAM3H web'
        _FLAM3HGIT_MSG: str = 'FLAM3H github'
        _FLAM3HINSTA_MSG: str = 'FLAM3H instagram'
        _FLAM3HYOUTUBE_MSG: str = 'FLAM3H video tutorials'
        _FLAM3PDF_MSG: str = 'The Fractal Flame Algorithm pdf'
        _FLAM3GIT_MSG: str = 'The Fractal Flame Algorithm github'
        _FRACTBITBUCKETGIT_MSG: str = 'Fractorium bitbucket'
        _FRACTWEB_MSG: str = 'Fractorium web'
        
        # {prm_name: value, ...}
        about_web: dict[str, str] = { MSG_FLAM3H_WEB: _FLAM3HWEB_MSG,
                                      MSG_FLAM3H_GIT: _FLAM3HGIT_MSG,
                                      MSG_FLAM3H_INSTA: _FLAM3HINSTA_MSG,
                                      MSG_FLAM3H_YOUTUBE: _FLAM3HYOUTUBE_MSG,
                                      MSG_FLAM3_PDF: _FLAM3PDF_MSG,
                                      MSG_FLAM3_GIT: _FLAM3GIT_MSG,
                                      MSG_FRACT_BITBUCKET: _FRACTBITBUCKETGIT_MSG,
                                      MSG_FRACT_WEB: _FRACTWEB_MSG
                                    }
        
        [node.setParms({key: value}) for key, value in about_web.items()]
        

    def flam3h_about_web_homepage(self) -> None:
        """Open a web browser to the FLAM3H homepage.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        page: str = "https://www.alexnardini.net/"
        www_open(page)
        

    def flam3h_about_web_github(self) -> None:
        """Open a web browser to the FLAM3H github repository.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        page: str = "https://github.com/alexnardini/FLAM3_for_SideFX_Houdini"
        www_open(page)
        

    def flam3h_about_web_instagram(self) -> None:
        """Open a web browser to the FLAM3H instagram account.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        page: str = "https://www.instagram.com/alexnardini/"
        www_open(page)
    
    
    def flam3h_about_web_youtube(self) -> None:
        """Open a web browser to the FLAM3H youtube video tutorials.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        page: str = "https://www.youtube.com/@alexnardiniITALY/videos"
        www_open(page)


    def flam3h_about_web_flam3_paper(self) -> None:
        """Open a web browser to the original "the fractal flame algorithm" publication/paper pdf.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        page: str = "https://flam3.com/flame_draves.pdf"
        www_open(page)
        

    def flam3h_about_web_flam3_github(self) -> None:
        """Open a web browser to the original FLAM3 github repository.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        page: str = "https://github.com/scottdraves/flam3"
        www_open(page)
        
        
    def flam3h_about_web_bitbucket(self) -> None:
        """Open a web browser to the Fractorium Bitbucket repository.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        page: str = "https://bitbucket.org/mfeemster/fractorium/src/master/"
        www_open(page)
        
        
    def flam3h_about_web_fractorium(self) -> None:
        """Open a web browser to the Fractorium Bitbucket repository.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        page: str = "http://fractorium.com/"
        www_open(page)
        
        
    def flam3h_web_run(self, key: str) -> None:
        """Select the appropriate web open definition to run.

        Args:
            (self):
            key(str): The key value that define whitch web definition to run.

        Returns:
            (None):
        """
        
        web: dict[str, Callable[[], None]] = {'web': self.flam3h_about_web_homepage,
                                              'git': self.flam3h_about_web_github,
                                              'insta': self.flam3h_about_web_instagram,
                                              'youtube': self.flam3h_about_web_youtube,
                                              'paper': self.flam3h_about_web_flam3_paper,
                                              'flam3git': self.flam3h_about_web_flam3_github,
                                              'bitbucket': self.flam3h_about_web_bitbucket,
                                              'fractweb': self.flam3h_about_web_fractorium,
                                            }
        
        run: Callable[[], None] | None = web.get(key)
        if run is not None: run()


# FLAM3H UI MESSAGES start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class flam3h_ui_msg_utils():
    """
class flam3h_ui_msg_utils

@METHODS
* ui_xaos_infos(self) -> None:
* ui_OUT_presets_name_infos(self) -> None:
* __ui_active_iterator_infos(self) -> None:
    """
    
    __slots__ = ("_kwargs", "_node")
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs: dict = kwargs
        self._node = kwargs['node']


    # CLASS: PROPERTIES
    ##########################################
    ##########################################
        
    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node
        

    def ui_xaos_infos(self) -> None:
        """Open a message window with informations/tips about setting Xaos.

        Args:
            (self):
            
        Returns:
            (None):
        """
        
        ALL_msg = """The default mode is \"xaos TO\".\nYou can change it to use \"xaos FROM\" mode instead in the preferences tab.

Xaos is fully automatic,
however below are some general rules on how it work:


XAOS USAGE:

To set XAOS for a flame with 4 iterators,
use the " xaos: " keyword followed by each iterator weights values separated by a colon:
\" xaos:1:2:3:4 \" ( xaos keyword can be uppercase too if you prefer. )

If no set,
FLAM3H will assume all XAOS values are 1.0, the equivalent of: \" xaos:1:1:1:1 \"

If you set only iterator 1 and iterator 2,
FLAM3H will always fill in the rest with a value of 1.0. \" xaos:0:0 \" will be interpreted as \" xaos:0:0:1:1 \"

When turning iterators ON and OFF and removing or adding them,
FLAM3H will internally remove and reformat XAOS values
to account for missing iterators. In short, it is fully automatic.


XAOS COMMAND OPTIONS:

If you type a non-numeric character in any of the xaos's weights,
FLAM3H will undo to what you had before.

If you dnt use the “ xaos: ” keywork at the beginning,
FLAM3H will undo to what you had before.

If you type a number,
the entire xaos string will be reset to all weights set to that number.

If you type a negative number, it will be reset to a value of: 1"""
        
        node = self.node

        if self.kwargs["ctrl"]:
            if hou.isUIAvailable():
                hou.ui.displayMessage(ALL_msg, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3H: XAOS usage infos", details=None, details_label=None, details_expanded=False) # type: ignore

        else:
            # current node
            autodiv = node.parm(PREFS_PVT_XAOS_AUTO_SPACE).eval()
            if autodiv:
                flam3h_general_utils.private_prm_set(node, PREFS_PVT_XAOS_AUTO_SPACE, 0)
                flam3h_iterator_utils(self.kwargs).auto_set_xaos()
                
                _MSG: str = f"{node.name()}: Xaos weights auto space: OFF"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
            else:
                flam3h_general_utils.private_prm_set(node, PREFS_PVT_XAOS_AUTO_SPACE, 1)
                flam3h_iterator_utils(self.kwargs).auto_set_xaos()
                
                _MSG: str = f"{node.name()}: Xaos weights auto space: ON"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')

            
    def ui_OUT_presets_name_infos(self) -> None:
        """Open a message window with informations/tips about setting Flame names in the OUT tab.

        Args:
            (self):
            
        Returns:
            (None):
        """

        
        ALL_msg = """ The iteration number you want your fractal flame to use when you load it back into FLAM3H
can be baked into the preset name you choose for it. 

For instance,
the Flame preset “My_Awesome_GrandJulia” will be loaded with 64 iterations by default.
However, if the iteration number is added to the preset name after a double colon,
as in “My_Awesome_GrandJulia::16,” it will override all settings
and load the preset with 16 as the iteration numbers.

Therefore,
do some tests before saving it,
and choose the ideal iteration number to incorporate into the preset name.

If you like,
you can manually edit the created XML/Flame file
and change the flame → “name” key afterwards.
    
"""
        if hou.isUIAvailable():
            hou.ui.displayMessage(ALL_msg, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Presets name infos", details=None, details_label=None, details_expanded=False) # type: ignore


    def __ui_active_iterator_infos(self) -> None:
        """ NOT USED ANYMORE:
        Open a message window with informations/tips turning iterators ON or OFF and their consequences.

        Args:
            (self):
            
        Returns:
            (None):
        """
        
        ALL_msg = """If an xform/iterator is disabled,
it wont be included when saving the Flame out into a flame file.

In case you still want to include the inactive iterator into the file,
set its Weight to 0(Zero) instead."""
        if hou.isUIAvailable():
            hou.ui.displayMessage(ALL_msg, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Active iterator infos", details=None, details_label=None, details_expanded=False) # type: ignore


# LOAD XML FLAME FILES start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


# It happen that Houdini sometime round value to many, many decimals.
# I am limiting this to max 8 decimals on export so not to have the xml file explode with trailing floats...
# Increase this if for some reason you need more precision.
ROUND_DECIMAL_COUNT: int = 8

# XML
XML_FLAME_NAME = 'flame'
XML_FLAME_VERSION = 'version'
XML_FLAME_PLUGINS = 'plugins'
XML_FLAME_NEW_LINEAR = 'new_linear'
XML_XF = 'xform'
XML_XF_WEIGHT = 'weight'
XML_XF_NAME = 'name'
XML_XF_PB = 'pre_blur'
XML_FF = 'finalxform'

XML_PRE_AFFINE = 'coefs'
# OUT custom to FLAM3H only
XML_FLAM3H_PRE_AFFINE = 'f3h_coefs'
XML_FLAM3H_PRE_AFFINE_ANGLE = 'f3h_coefs_angle'

XML_POST_AFFINE = 'post'
# OUT custom to FLAM3H only
XML_FLAM3H_POST_AFFINE = 'f3h_post'
XML_FLAM3H_POST_AFFINE_ANGLE = 'f3h_post_angle'

XML_XF_XAOS = 'chaos'
XML_PALETTE = 'palette'
XML_PALETTE_COUNT = 'count'
XML_PALETTE_FORMAT = 'format'
XML_XF_COLOR = 'color'
XML_XF_VAR_COLOR = 'var_color'
XML_XF_SYMMETRY = 'symmetry'
XML_XF_COLOR_SPEED = 'color_speed'
XML_XF_OPACITY = 'opacity'
# OUT SYS custom to FLAM3H only
OUT_XML_FLAM3H_SYS_RIP = 'flam3h_rip'
OUT_XML_FLAM3H_HSV = 'flam3h_hsv'
OUT_XML_FLMA3H_MB_FPS = 'flam3h_mb_fps'
OUT_XML_FLMA3H_MB_SAMPLES = 'flam3h_mb_samples'
OUT_XML_FLMA3H_MB_SHUTTER = 'flam3h_mb_shutter'
OUT_XML_FLAM3H_CP_SAMPLES = 'flam3h_cp_samples'
OUT_XML_FLAM3H_PREFS_F3C = 'flam3h_f3c'
# OUT XML render key data names
OUT_XML_VERSION = 'version'
OUT_XML_FLAME_SIZE = 'size'
OUT_XML_FLAME_RESOLUTION = 'resolution' # This is not used by the Flame format but only a one off for the IN Infos Flame stats UI
OUT_XML_FLAME_CENTER = 'center'
OUT_XML_FLAME_ROTATE = 'rotate'
OUT_XML_FLAME_SCALE = 'scale'
OUT_XML_FLAME_BG = 'background'
OUT_XML_FLAME_SUPERSAMPLE = 'supersample'
OUT_XML_FLAME_FILTER = 'filter'
OUT_XML_FLAME_QUALITY = 'quality'
OUT_XML_FLAME_BRIGHTNESS = 'brightness'
OUT_XML_FLAME_GAMMA = 'gamma'
OUT_XML_FLAME_GAMMA_THRESHOLD = 'gamma_threshold'
OUT_XML_FLAME_VIBRANCY = 'vibrancy'
OUT_XML_FLAME_POWER = 'highlight_power'
OUT_XML_FLAME_K2 = 'logscale_k2'
OUT_XML_FLAME_RADIUS = 'estimator_radius'
OUT_XML_FLAME_ESTIMATOR_MINIMUM = 'estimator_minimum'
OUT_XML_FLAME_ESTIMATOR_CURVE = 'estimator_curve'
OUT_XML_FLAME_PALETTE_MODE = 'palette_mode'
OUT_XML_FLAME_INTERPOLATION = 'interpolation'
OUT_XML_FLAME_INTERPOLATION_TYPE = 'interpolation_type'
# OUT XML Curves
OUT_XML_FLAME_RENDER_CURVES = 'curves'
OUT_XML_FLAME_RENDER_CURVES_DEFAULT = '0 0 1 0.25 0.25 1 0.5 0.5 1 0.75 0.75 1 0 0 1 0.25 0.25 1 0.5 0.5 1 0.75 0.75 1 0 0 1 0.25 0.25 1 0.5 0.5 1 0.75 0.75 1 0 0 1 0.25 0.25 1 0.5 0.5 1 0.75 0.75 1'
OUT_XML_FLAME_RENDER_CURVES_DEFAULT_B = '0 0 1 0.25 0.25 1 0.75 0.75 1 1 1 1 0 0 1 0.25 0.25 1 0.75 0.75 1 1 1 1 0 0 1 0.25 0.25 1 0.75 0.75 1 1 1 1 0 0 1 0.25 0.25 1 0.75 0.75 1 1 1 1'
OUT_XML_FLAME_RENDER_CURVES_DEFAULT_C = '0 0 1 0.25 0.25 1 1 1 1 0.75 0.75 1 0 0 1 0.25 0.25 1 1 1 1 0.75 0.75 1 0 0 1 0.25 0.25 1 1 1 1 0.75 0.75 1 0 0 1 0.25 0.25 1 1 1 1 0.75 0.75 1'
OUT_XML_FLAME_RENDER_CURVES_DEFAULT_ALL: tuple = (OUT_XML_FLAME_RENDER_CURVES_DEFAULT, OUT_XML_FLAME_RENDER_CURVES_DEFAULT_B, OUT_XML_FLAME_RENDER_CURVES_DEFAULT_C) # I'll do a better solution another day for this
OUT_XML_FLAME_RENDER_CURVE_OVERALL = 'overall_curve'
OUT_XML_FLAME_RENDER_CURVE_RED = 'red_curve'
OUT_XML_FLAME_RENDER_CURVE_GREEN = 'green_curve'
OUT_XML_FLAME_RENDER_CURVE_BLUE = 'blue_curve'
OUT_XML_FLAME_RENDER_CURVE_DEFAULT = '0 0 0.25 0.25 0.5 0.5 0.75 0.75 1 1'
OUT_XML_FLAME_RENDER_CURVE_DEFAULT_B = '0 0 0.25 0.25 0.75 0.75 1 1'
OUT_XML_FLAME_RENDER_CURVE_DEFAULT_C = '0 0 0.25 0.25 1 1 0.75 0.75' # This order is odd but I have some flames coming in with this so...
OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL: tuple = (OUT_XML_FLAME_RENDER_CURVE_DEFAULT, OUT_XML_FLAME_RENDER_CURVE_DEFAULT_B, OUT_XML_FLAME_RENDER_CURVE_DEFAULT_C) # I'll do a better solution another day for this
# XML OUT render key data prm names HOUDINI
# for now make sense to expose those, I may add more in the future if needed
# Note that those are the FLAM3H UI parameter's names for the OUT Render properties tab.
OUT_XML_RENDER_HOUDINI_DICT: dict[str, str] = { XML_XF_NAME: OUT_FLAME_PRESET_NAME,
                                                OUT_XML_FLAME_SIZE: 'outres',
                                                OUT_XML_FLAME_CENTER: 'outcenter',
                                                OUT_XML_FLAME_ROTATE: 'outrotate',
                                                OUT_XML_FLAME_SCALE: 'outscale',
                                                OUT_XML_FLAME_QUALITY: 'outquality',
                                                OUT_XML_FLAME_BRIGHTNESS: 'outbrightness',
                                                OUT_XML_FLAME_GAMMA: 'outgamma',
                                                OUT_XML_FLAME_POWER: 'outhighlight',
                                                OUT_XML_FLAME_K2: 'outk2',
                                                OUT_XML_FLAME_VIBRANCY: 'outvibrancy',
                                                OUT_XML_FLAME_RENDER_CURVES: 'outcurves',
                                                OUT_XML_FLAME_RENDER_CURVE_OVERALL: 'outcurveoverall',
                                                OUT_XML_FLAME_RENDER_CURVE_RED: 'outcurvered',
                                                OUT_XML_FLAME_RENDER_CURVE_GREEN: 'outcurvegreen',
                                                OUT_XML_FLAME_RENDER_CURVE_BLUE: 'outcurveblue'
                                                }

# For now we force to assume a valid flame's XML file must have this tree.root name.
XML_VALID_FLAMES_ROOT_TAG = 'flames'
# and this for a valid chaotica file ( not supported )
XML_VALID_CHAOS_ROOT_TAG = 'ifs'

# Since we get the folowing keys in a separate action, we exclude them for later variation's names searches to help speed up a little.
XML_XF_KEY_EXCLUDE = ("weight", "color", "var_color", "symmetry", "color_speed", "name", "animate", "pre_blur", "coefs", "f3h_coefs", "f3h_coefs_angle", "post", "f3h_post", "f3h_post_angle", "chaos", "opacity")

# This has been fixed and now radial_blur variation matches all the other apps
# but I leave it here just in case other variation will need it.
XML_XF_PRM_EXCEPTION = ("None",)

# REGEX_ALL = "(?s:.*?)"
REGEX_PALETTE_LIB_LOCK = f"^(?:{FLAM3H_LIB_LOCK})"
REGEX_PRE = "^(?:pre_)"
REGEX_POST = "^(?:post_)"

V_PRX_PRE = "pre_"
V_PRX_POST = "post_"

# Set global limits for the number of allowed variations to be used for each variation type:
# PRE, VAR and POST for iterator and FF.
MAX_ITER_VARS: int = 4
MAX_ITER_VARS_PRE: int = 2
MAX_ITER_VARS_POST: int = 1
MAX_FF_VARS: int = 2
MAX_FF_VARS_PRE: int = 1
MAX_FF_VARS_POST: int = 2

# XML Flame key's "version" to identify the authoring software
# of the loaded Flame preset.
XML_APP_NAME_FLAM3H = 'FLAM3H'
XML_APP_NAME_FRACTORIUM = 'EMBER'
# XML_APP_NAME_APO = 'Apophysis'

# This is used as a faster idx lookup table.
# From the XML's xforms, each variations look itself up inside here to get the corresponding FLAM3H var idx it is mapped to.
# The key names matter and must match the variation's names as known by other apps ( in my case: Apophysis and Fratorium )
#
# _NOTE:
#       Variation name "linear3d" has been added to this dict as it is often used in old Flames and we are remapping it to "linear" on load.

VARS_FLAM3_DICT_IDX: dict[str, int] = { "linear": 0, 
                                        "linear3d": 0, 
                                        "sinusoidal": 1,
                                        "spherical": 2,
                                        "swirl": 3,
                                        "horseshoe": 4,
                                        "polar": 5,
                                        "handkerchief": 6,
                                        "heart": 7,
                                        "disc": 8,
                                        "spiral": 9,
                                        "hyperbolic": 10,
                                        "diamond": 11,
                                        "ex": 12,
                                        "julia": 13,
                                        "bent": 14,
                                        "waves": 15,
                                        "fisheye": 16,
                                        "popcorn": 17,
                                        "exponential": 18,
                                        "power": 19,
                                        "cosine": 20,
                                        "rings": 21,
                                        "fan": 22,
                                        "bubble": 23,
                                        "cylinder": 24,
                                        "eyefish": 25,
                                        "blur": 26,
                                        "curl": 27,
                                        "ngon": 28,
                                        "pdj": 29,
                                        "blob": 30,
                                        "julian": 31,
                                        "juliascope": 32,
                                        "gaussian_blur": 33,
                                        "fan2": 34,
                                        "rings2": 35,
                                        "rectangles": 36,
                                        "radial_blur": 37,
                                        "pie": 38,
                                        "arch": 39,
                                        "tangent": 40,
                                        "square": 41,
                                        "rays": 42,
                                        "blade": 43,
                                        "secant2": 44,
                                        "twintrian": 45,
                                        "cross": 46,
                                        "disc2": 47,
                                        "super_shape": 48,
                                        "flower": 49,
                                        "conic": 50,
                                        "parabola": 51,
                                        "bent2": 52,
                                        "bipolar": 53,
                                        "boarders": 54,
                                        "butterfly": 55,
                                        "cell": 56,
                                        "cpow": 57,
                                        "edisc": 58,
                                        "elliptic": 59,
                                        "noise": 60,
                                        "escher": 61,
                                        "foci": 62,
                                        "lazysusan": 63,
                                        "loonie": 64,
                                        "pre_blur": 65,
                                        "modulus": 66,
                                        "oscilloscope": 67,
                                        "polar2": 68,
                                        "popcorn2": 69,
                                        "scry": 70,
                                        "separation": 71,
                                        "split": 72,
                                        "splits": 73,
                                        "stripes": 74,
                                        "wedge": 75,
                                        "wedge_julia": 76,
                                        "wedge_sph": 77,
                                        "whorl": 78,
                                        "waves2": 79,
                                        "exp": 80,
                                        "log": 81,
                                        "sin": 82,
                                        "cos": 83,
                                        "tan": 84,
                                        "sec": 85,
                                        "csc": 86,
                                        "cot": 87,
                                        "sinh": 88,
                                        "cosh": 89,
                                        "tanh": 90,
                                        "sech": 91,
                                        "csch": 92,
                                        "coth": 93,
                                        "auger": 94,
                                        "flux": 95,
                                        "mobius": 96,
                                        "curve": 97,
                                        "perspective": 98,
                                        "bwraps": 99,
                                        "hemisphere": 100,
                                        "polynomial": 101,
                                        "crop": 102,
                                        "unpolar": 103,
                                        "glynnia": 104, 
                                        "point_symmetry": 105
                                        }

# This dictionary for a faster look up table, Fractorium has so many variations!
# We are using this to check for missing variations coming from the loaded flame file
# as Fractorium seem to have them all ;) and it is the app I am now comparing against for this data.
#
# All of the variations that Fractorium has but FLAM3H does not are known as: Missing variations.
# FLAM3H was designed to work in tandem with Fractorium,
# and it makes an effort to learn as much as it can about everything that Fractorium is capable of, in this case, about all the variations he posses.
# All of the variations that Fractorium lacks will be categorized as: Unknown variations.
#
# If you want an Unknown variation to be recognized by FLAM3H, add it here inside the corresponding dictionary letter entrie based on its name.

VARS_FRACTORIUM_DICT: dict[str, tuple] = {  "a": ("arch", "arcsech", "arcsech2", "arcsinh", "arctanh", "asteria", "auger"),
                                            "b": ( "barycentroid", "bcircle", "bcollide", "bent", "bent2", "bipolar", "bisplit", "blade", "blade3d", "blob", "blob2", "blob3d", "block", "blocky", "blur", "blur_circle", "blur_heart", "blur_linear", "blur_pixelize", "blur_square", "blur_zoom", "blur3d", "bmod", "boarders", "boarders2", "bswirl", "btransform", "bubble", "bubble2", "bubblet3d", "butterfly", "bwraps", "bwraps_rand"),
                                            "c": ( "cardioid", "cell", "checks", "circleblur", "circlecrop", "circlecrop2", "circlelinear", "circlerand", "circlesplit", "circletrans1", "circlize", "circlize2", "circus", "collideoscope", "concentric", "conic", "cos", "cos_wrap", "cosh", "coshq", "cosine", "cosq", "cot", "coth", "coth_spiral", "cothq", "cotq", "cpow", "cpow2", "cpow3", "crackle", "crackle2", "crescents", "crob", "crop", "cropn", "cross", "csc", "csch", "cschq", "cscq", "cubic3d", "cubic_lattice3d", "curl", "curl3d", "curl_sp", "curvature", "curve", "cylinder", "cylinder2"),
                                            "d": ("delta_a", "depth", "depth_blur", "depth_blur2", "depth_gaussian", "depth_gaussian2", "depth_ngon", "depth_ngon2", "depth_sine", "depth_sine2", "diamond", "disc", "disc2", "disc3d", "dragonfire", "dust","d_spherical"),
                                            "e": ("eclipse", "ecollide", "edisc", "ejulia", "elliptic", "emod", "emotion", "ennepers", "epispiral", "epush", "erf", "erotate", "escale", "escher", "estiq", "eswirl", "ex", "excinis", "exp", "exp2", "expo", "exponential", "extrude", "eyefish"),
                                            "f": ("falloff", "falloff2", "falloff3", "fan", "fan2", "farblur", "fdisc", "fibonacci", "fibonacci2", "fisheye", "flatten", "flip_circle", "flip_x", "flip_y", "flower", "flower_db", "flux", "foci", "foci3d", "foci_p", "fourth", "funnel"),
                                            "g": ("gamma", "gaussian", "gaussian_blur", "gdoffs", "glynnia", "glynnia2", "glynnsim1", "glynnsim2", "glynnsim3", "glynnsim4", "glynnsim5", "gnarly", "gridout"),
                                            "h": ("handkerchief", "heart", "heat", "helicoid", "helix", "hemisphere", "henon", "hexaplay3d", "hexcrop", "hexes", "hexnix3d", "hex_modulus", "hex_rand", "hex_truchet", "ho", "hole", "horseshoe", "hyperbolic", "hypercrop", "hypershift", "hypershift2", "hypertile", "hypertile1", "hypertile2", "hypertile3d", "hypertile3d1", "hypertile3d2"),
                                            "i": ("idisc", "inkdrop", "interference2"),
                                            "j": ("jac_cn", "jac_dn", "jac_sn", "julia", "julia3d", "julia3dq", "julia3dz", "juliac", "julian", "julian2", "julian3dx", "julianab", "juliaq", "juliascope"), 
                                            "k": ("kaleidoscope",),
                                            "l": ("lazyjess", "lazysusan", "lazy_travis", "lens", "line", "linear", "linear_t", "linear_t3d", "linear_xz", "linear_yz", "linear3d", "lissajous", "log", "log_db", "loq", "loonie", "loonie2", "loonie3", "loonie3d", "lozi"),
                                            "m": ("mask", "mcarpet", "mirror_x", "mirror_y", "mirror_z", "mobiq", "mobius", "mobius_strip", "mobiusn", "modulus", "modulusx", "modulusy", "murl", "murl2"),
                                            "n": ("nblur", "ngon", "noise", "npolar"),
                                            "o": ("octagon", "octapol", "ortho", "oscilloscope", "oscilloscope2", "ovoid", "ovoid3d"),
                                            "p": ("panorama1", "panorama2", "parabola", "pdj", "perspective", "petal", "phoenix_julia", "pie", "pie3d", "pixel_flow", "poincare", "poincare2", "poincare3d", "point_symmetry", "polar", "polar2", "polynomial", "popcorn", "popcorn2", "popcorn23d", "pow_block", "power", "pressure_wave", "projective", "prose3d", "psphere", "pulse"),
                                            "q": ("q_ode",),
                                            "r": ("radial_blur", "radial_gaussian", "rand_cubes", "rational3", "rays", "rays1", "rays2", "rays3", "rblur", "rectangles", "rings", "rings2", "ripple", "rippled", "rotate", "rotate_x", "rotate_y", "rotate_z", "roundspher", "roundspher3d"),
                                            "s": ("scry", "scry2", "scry3d", "sec", "secant2", "sech", "sechq", "secq", "separation", "shift", "shred_rad", "shred_lin", "sigmoid", "sin", "sineblur", "sinh", "sinhq", "sinq", "sintrange", "sinus_grid", "sinusoidal", "sinusoidal3d", "smartshape", "smartcrop", "spher", "sphereblur", "spherical", "spherical3d", "sphericaln", "spherivoid", "sphyp3d", "spiral", "spiral_wing", "spirograph", "split", "split_brdr", "splits", "splits3d", "square", "squares", "square3d", "squarize", "squirrel", "squish", "sschecks", "starblur", "starblur2", "stripes", "stwin", "super_shape", "super_shape3d","svf", "swirl", "swirl3", "swirl3r", "synth"),
                                            "t": ("tan", "tancos", "tangent", "tanh", "tanhq", "tanh_spiral", "tanq", "target", "target0", "target2", "taurus", "tile_hlp", "tile_log", "trade", "truchet", "truchet_fill", "truchet_hex_fill", "truchet_hex_crop", "truchet_glyph", "truchet_inv", "truchet_knot", "twintrian", "twoface"),
                                            "u": ("unicorngaloshen", "unpolar"),
                                            "v": ("vibration", "vibration2", "vignette", "voron"),
                                            "w": ("w", "waffle", "waves", "waves2", "waves22", "waves23", "waves23d", "waves2b", "waves2_radial", "waves3", "waves4", "waves42", "wavesn", "wdisc", "wedge", "wedge_julia", "wedge_sph", "whorl"),
                                            "x": ("x", "xerf", "xheart", "xtrb"),
                                            "y": ("y",),
                                            "z": ("z", "zblur", "zcone", "zscale","ztranslate")
                                            }


class flam3h_varsPRM_APO:
    
    '''
    The following parameters matches the Apophysis/Fractorium parameter's names,
    so no need to regex for now as the strings names are matching already.
    
    There are a few exceptions so far witch I handled simply for now, but it work.
    
    They are grouped as follow and based on the FLAM3H node parametric parameters:
    
    for generic variation:
    ("variation name", bool: (parametric or not parametric)),
    
    for parametric variation:
    ("variation name", (prm_1, ..., prm_4), (prm_1, ..., prm_4), bool: (parametric or not parametric)),
    
    -> (prm_1, ..., prm_4) accept a max of 4 entries (hou.Vector4) and based on the number of parameters
    they are then automatically converted to the expeted v_type using the function: 
    in_flame_utils.in_util_typemaker(data: list) -> TA_TypeMaker:
    
    The (("variation_name") entrie, is not used here and only for reference.
    '''
    
    __slots__ = ("varsPRM", "varsPRM_FRACTORIUM_EXCEPTIONS")
    
    def __init__(self) -> None:
        
        self.varsPRM: tuple = ( ("linear", 0), 
                                ("sinusoidal", 0), 
                                ("spherical", 0), 
                                ("swirl", 0), 
                                ("horseshoe", 0), 
                                ("polar", 0), 
                                ("handkerchief", 0), 
                                ("heart", 0), 
                                ("disc", 0), 
                                ("spiral", 0), 
                                ("hyperbolic", 0), 
                                ("diamond", 0), 
                                ("ex", 0), 
                                ("julia", 0), 
                                ("bent", 0), 
                                ("waves", 0), 
                                ("fisheye", 0), 
                                ("popcorn", 0), 
                                ("exponential", 0), 
                                ("power", 0), 
                                ("cosine", 0), 
                                ("rings", 0), 
                                ("fan", 0), 
                                ("bubble", 0), 
                                ("cylinder", 0), 
                                ("eyefish", 0), 
                                ("blur", 0), 
                                ("curl", ("curl_c1", "curl_c2"), 1), 
                                ("ngon", ("ngon_power", "ngon_sides", "ngon_corners", "ngon_circle"), 1), 
                                ("pdj", ("pdj_a", "pdj_b", "pdj_c", "pdj_d"), 1), 
                                ("blob", ("blob_low", "blob_high", "blob_waves"), 1), 
                                ("juliaN", ("julian_power", "julian_dist"), 1), 
                                ("juliascope", ("juliascope_power", "juliascope_dist"), 1), 
                                ("gaussian_blur", 0), 
                                ("fan2", ("fan2_x", "fan2_y"), 1), 
                                ("rings2", ("rings2_val",), 1), 
                                ("rectangles", ("rectangles_x", "rectangles_y"), 1), 
                                ("radial_blur", ("radial_blur_angle",), 1), 
                                ("pie", ("pie_slices", "pie_thickness", "pie_rotation"), 1), 
                                ("arch", 0), 
                                ("tangent", 0), 
                                ("square", 0), 
                                ("rays", 0), 
                                ("blade", 0), 
                                ("secant2", 0), 
                                ("twintrian", 0), 
                                ("cross", 0), 
                                ("disc2", ("disc2_rot", "disc2_twist"), 1), 
                                ("supershape", ("super_shape_m", "super_shape_rnd", "super_shape_holes"), ("super_shape_n1", "super_shape_n2", "super_shape_n3"), 1), 
                                ("flower", ("flower_petals", "flower_holes"), 1), 
                                ("conic", ("conic_eccentricity", "conic_holes"), 1), 
                                ("parabola", ("parabola_height", "parabola_width"), 1), 
                                ("bent2", ("bent2_x", "bent2_y"), 1), 
                                ("bipolar", ("bipolar_shift",), 1),
                                ("boarders", 0),
                                ("butterfly", 0), 
                                ("cell", ("cell_size",), 1), 
                                ("cpow", ("cpow_power", "cpow_r", "cpow_i"), 1), 
                                ("edisc", 0), 
                                ("elliptic", 0), 
                                ("noise", 0), 
                                ("escher", ("escher_beta",), 1), 
                                ("foci", 0), 
                                ("lazysusan", ("lazysusan_x", "lazysusan_y"), ("lazysusan_spin", "lazysusan_twist", "lazysusan_space"), 1), 
                                ("loonie", 0), 
                                ("pre blur", 0), 
                                ("modulus", ("modulus_x", "modulus_y"), 1), 
                                ("oscilloscope", ("oscope_frequency", "oscope_amplitude", "oscope_damping", "oscope_separation"), 1), 
                                ("polar2", 0), 
                                ("popcorn2", ("popcorn2_x", "popcorn2_y"), ("popcorn2_c",), 1), 
                                ("scry", 0), 
                                ("separation", ("separation_x", "separation_y"), ("separation_xinside", "separation_yinside"), 1), 
                                ("split", ("split_xsize", "split_ysize"), 1), 
                                ("splits", ("splits_x", "splits_y"), 1), 
                                ("stripes", ("stripes_space", "stripes_warp"), 1), 
                                ("wedge", ("wedge_swirl", "wedge_angle", "wedge_hole", "wedge_count",), 1), 
                                ("wedge_julia", ("wedge_julia_power", "wedge_julia_angle", "wedge_julia_dist", "wedge_julia_count"), 1), 
                                ("wedge_sph", ("wedge_sph_swirl", "wedge_sph_angle", "wedge_sph_hole", "wedge_sph_count"), 1), 
                                ("whorl", ("whorl_inside", "whorl_outside"), 1), 
                                ("waves2", ("waves2_scalex", "waves2_scaley"), ("waves2_freqx", "waves2_freqy"), 1), 
                                ("exp", 0), 
                                ("log", 0), 
                                ("sin", 0), 
                                ("cos", 0), 
                                ("tan", 0), 
                                ("sec", 0), 
                                ("csc", 0), 
                                ("cot", 0), 
                                ("sinh", 0), 
                                ("cosh", 0), 
                                ("tanh", 0), 
                                ("sech", 0), 
                                ("csch", 0), 
                                ("coth", 0), 
                                ("auger", ("auger_freq", "auger_scale", "auger_sym", "auger_weight"), 1), 
                                ("flux", ("flux_spread",), 1), 
                                ("mobius", ("Re_A", "Re_B", "Re_C", "Re_D"), ("Im_A", "Im_B", "Im_C", "Im_D"), 1),
                                ("curve", ("curve_xlength", "curve_ylength"), ("curve_xamp", "curve_yamp"), 1), 
                                ("persp", ("perspective_angle", "perspective_dist"), 1), 
                                ("bwraps", ("bwraps_cellsize", "bwraps_space", "bwraps_gain"), ("bwraps_inner_twist", "bwraps_outer_twist"), 1), 
                                ("hemisphere", 0), 
                                ("polynomial", ("polynomial_powx", "polynomial_powy"), ("polynomial_lcx", "polynomial_lcy"), ("polynomial_scx", "polynomial_scy"), 1),
                                ("crop", ("crop_left", "crop_top", "crop_right", "crop_bottom"), ("crop_scatter_area", "crop_zero"), 1), 
                                ("unpolar", 0), 
                                ("glynnia", 0), 
                                ("point_symmetry", ("point_symmetry_order", "point_symmetry_centre_x", "point_symmetry_centre_y"), 1)
                            )


        # EXCEPTIONS: so I dnt go into regex...
        # Update this and def in_prm_name_exceptions() if you add/find more
        self.varsPRM_FRACTORIUM_EXCEPTIONS: dict[int, tuple] = {67: ("oscilloscope", ("oscilloscope_frequency", "oscilloscope_amplitude", "oscilloscope_damping", "oscilloscope_separation"), 1),
                                                                96: ("Mobius", ("Mobius_Re_A", "Mobius_Re_B", "Mobius_Re_C", "Mobius_Re_D"), ("Mobius_Im_A", "Mobius_Im_B", "Mobius_Im_C", "Mobius_Im_D"), 1)
                                                                }


# This is used inside: __get_name_list_str(...)
# to set what default single value should be used in case something goes wrong during the processed string value cleanup/correction
XML_TO_F3H_DEFAULT_VALS: dict[str, str] = { XML_XF_WEIGHT: '0.5', 
                                            XML_XF_COLOR: '0', 
                                            XML_XF_COLOR_SPEED: '0', 
                                            XML_XF_SYMMETRY: '0', 
                                            XML_XF_OPACITY: '1', 
                                            OUT_XML_FLAM3H_HSV: '1', 
                                            OUT_XML_FLAME_SIZE: '1024'
                                            }


# This is used inside: def xf_list_cleanup(...) and def xf_list_cleanup_str(...)
# to gather a proper default list of values in case the one from the XML is empty.
XML_TO_F3H_LIST_DEFAULT_VALS: dict[str, str] = {OUT_XML_FLAME_SIZE: '1024 1024', 
                                                OUT_XML_FLAME_CENTER: '0 0', 
                                                OUT_XML_FLAM3H_HSV: '1 1 1'
                                                }


# FLAM3H XML TREE start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class _xml:
    """
class _xml

@METHODS
* get_name(self, key: str = XML_XF_NAME) -> tuple:

    """    
    
    __slots__ = ("_xml", "_tree")
    
    def __init__(self, xmlfile: str) -> None:
        """This Class is only to try to speedup the python menu UI evaulation.
        Here I assume that if the parameter IN_PVT_ISVALID_FILE is 1,
        than we can proceed without worries about actually checking and iterate through the flame file for its validity.
        It is a mere attempt to speedup but it should help a little bit ;)
        as we are not evaluating the _xml_tree() class witch is more heavy and sophisticated, something we do not need for this purpose.
        This is a very lightweight way to gather the Flames names.
        
        A parameter to the IN Tab has been added: IN_PVT_ISVALID_PRESET
        This parameter will tell us if a preset is currently loaded or not.
        
        Before we only had: IN_PVT_ISVALID_FILE
        so we were forced to read and evaluate the entire _xml_tree() class.

        Args:
            xmlfile (str): The XML full file path name to evaluate
        """     
        self._xml = xmlfile
        self._tree = lxmlET.parse(xmlfile) # type: ignore


    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def xml(self):
        return self._xml
    
    @property
    def tree(self):
        return self._tree
        
        
    def get_name(self, key: str = XML_XF_NAME) -> tuple:
        """Collect all Flame presets name from the XML Flame file.
        
        This is being added as a quick and cheap way to do so making some assumption ahead of time.
        Read this class __init__ doc string to know more.

        Args:
            (self):
            key(str): Defaults to XML_XF_NAME. The XML Flame's name key.

        Returns:
            (tuple): Flame presets names.
        """     
        if os.path.isfile(self.xml):   
            root = self.tree.getroot()
            if XML_VALID_FLAMES_ROOT_TAG in root.tag.lower():
                return tuple( [str(name.get(key)).strip() if name.get(key) is not None else [] for name in root] )
            else:
                newroot = lxmlET.Element(XML_VALID_FLAMES_ROOT_TAG) # type: ignore
                newroot.insert(0, root)
                return tuple( [str(name.get(key)).strip() if name.get(key) is not None else [] for name in newroot] )
        else:
            # inside a try/except block because it happened that when Houdini is busy like for example computing the flame while it is in camera sensor mode,
            # this failed on me once and it could not evaluate the hou.pwd() properly.
            try:
                # For safety, lets turn off those toggles
                flam3h_general_utils.private_prm_set(hou.pwd(), IN_PVT_ISVALID_FILE, 0)
                flam3h_general_utils.private_prm_set(hou.pwd(), IN_PVT_ISVALID_PRESET, 0)
                return ()
            except:
                _MSG: str = ("\nFLAM3H -> warning: Could not evaluate the current hou.SopNode. Class _xml(...).get_name(...)\n")
                print(f"{_MSG}\n")
                flam3h_general_utils.set_status_msg(f"{_MSG}", 'WARN')
                return ()


class _xml_tree:
    """
class _xml_tree

@STATICMETHODS
* xmlfile_root_chk(xmlfile: str | None, clipboard: bool = False) -> str | None:
* xmlfile_isvalidtree_chk(xmlfile: str) -> bool:

@METHODS
* get_name(self, key: str = XML_XF_NAME) -> tuple:
* __get_name_val_str(self, key: str, _DEFAULT: str = '0') -> tuple:
* __get_name_curve_val_str(self, key: str, _DEFAULT: str = '0') -> tuple:
* __get_name_list_str(self, key: str) -> tuple:
* __get_flame(self, key: str = XML_FLAME_NAME) -> tuple | None:
* __get_flame_count(self, flames: list) -> int:

"""

    __slots__ = ("_xmlfile", "_xmlfile_data", "_xmlfile_data_clipboard", "_isvalidtree", "_tree", "_name", "_plugins", "_sw_version")
    
    def __init__(self, xmlfile: str) -> None:
        """
        Args:
            (self):
            xmlfile (str): xmlfile (str): [xml *.flame file v_type to load]
        """
        self._xmlfile: str = xmlfile
        self._xmlfile_data: str | None = self.xmlfile_root_chk(self._xmlfile)
        self._xmlfile_data_clipboard: str | None = self.xmlfile_root_chk(self._xmlfile, True)
        self._isvalidtree: bool = self.xmlfile_isvalidtree_chk(self._xmlfile)
        if self._xmlfile_data_clipboard is not None:
            self._tree = lxmlET.ElementTree(lxmlET.fromstring(self._xmlfile_data_clipboard)) # type: ignore
            self._isvalidtree = True
        elif self._xmlfile_data is not None:
            self._tree = lxmlET.ElementTree(lxmlET.fromstring(self._xmlfile_data)) # type: ignore
            self._isvalidtree = True
        else:
            if self._isvalidtree:
                self._tree = lxmlET.parse(xmlfile) # type: ignore
                
        # This not private as its cheaper to have it evaluate from this parent class.
        self._name: tuple = self.get_name()
        self._plugins: tuple = self.get_name(XML_FLAME_PLUGINS)
        self._sw_version: tuple = self.get_name(XML_FLAME_VERSION) # type: ignore


    @staticmethod
    def xmlfile_root_chk(xmlfile: str | None, clipboard: bool = False) -> str | None:
        """When loading a Flame files, it can contain many flame presets in it.
        When multiple flame presets are present into the file, they will all be grouped under a root with a name.
        However, when you save a flame into the clipboard ( from FLAM3H but also from Apophysis, Fractorium and other)
        the saved Flame wont be grouped under a root, but it will be rootless.
        
        This definition will check if the loaded preset (from a file or from the Clipboard) lives under a root or not
        and perform the necessary operation to be loaded inside FLAM3H either ways.

        Args:
            xmlfile(str | None): The flame file full path string we are trying to load.
            clipboard(bool): Default to False. True if the flame preset is being loaded from the clipboard and False if not.
            
        Returns:
            (str | None): A new flame preset data valid to be loaded in.
        """
        try:
            if clipboard:
                if xmlfile is not None:
                    tree = lxmlET.ElementTree(lxmlET.fromstring(xmlfile)) # type: ignore
                else:
                    tree = lxmlET.parse(xmlfile) # type: ignore
            else:
                tree = lxmlET.parse(xmlfile) # type: ignore
                
            root = tree.getroot()
            root_tag = root.tag.lower()
            if XML_VALID_FLAMES_ROOT_TAG not in root_tag:
                newroot = lxmlET.Element(XML_VALID_FLAMES_ROOT_TAG) # type: ignore
                newroot.insert(0, root)
                # If there are flames, proceed
                if tuple([f for f in newroot.iter(XML_FLAME_NAME)]):
                    out_flame_utils._out_pretty_print(newroot)
                    return lxmlET.tostring(newroot, encoding="unicode") # type: ignore
                else:
                    if XML_VALID_CHAOS_ROOT_TAG in root_tag:
                        # let us know
                        _MSG: str = "IN: Chaotica XML not supported"
                        flam3h_general_utils.set_status_msg(f"{hou.pwd().name()}: {_MSG}", 'WARN')
                        flam3h_general_utils.flash_message(hou.pwd(), _MSG)
                    return None
            else:
                # If there are flames, proceed
                if tuple([f for f in root.iter(XML_FLAME_NAME)]):
                    out_flame_utils._out_pretty_print(root)
                    return lxmlET.tostring(root, encoding="unicode") # type: ignore
                else:
                    return None
        except: return None


    @staticmethod
    def xmlfile_isvalidtree_chk(xmlfile: str) -> bool:
        """When loading a Flame files, this definition will check their data
        and tell us if what we are trying to load is actually a valid flame data to be loaded.

        Args:
            xmlfile(str): The flame file full path string we are trying to load.
            
        Returns:
            (bool): True if it is a valid flame preset data or False if Not
        """
        try:
            tree = lxmlET.parse(xmlfile) # type: ignore
            if isinstance(tree, lxmlET.ElementTree): # type: ignore
                root = tree.getroot()
                if XML_VALID_FLAMES_ROOT_TAG in root.tag.lower():
                    # If there are flames, proceed
                    if tuple([f for f in root.iter(XML_FLAME_NAME)]):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except: return False


    # CLASS: PROPERTIES
    ##########################################
    ##########################################
    
    @property
    def xmlfile(self):
        return self._xmlfile
    
    @property
    def xmlfile_data(self):
        return self._xmlfile_data
    
    @property
    def tree(self):
        return self._tree
    
    @property
    def isvalidtree(self):
        return self._isvalidtree
    
    @property
    def name(self):
        return self._name
    
    @property
    def plugins(self):
        return self._plugins
    
    @property
    def sw_version(self):
        return self._sw_version
    

    # This not private as its cheaper to have it evaluate from this parent class.
    def get_name(self, key: str = XML_XF_NAME) -> tuple:
        """Collect all Flame presets name from the XML Flame file.

        Args:
            (self):
            key(str): Defaults to XML_XF_NAME. The XML Flame's name key.

        Returns:
            (tuple): Flame presets names packed into a tuple.
        """
        if self.isvalidtree:
            root = self.tree.getroot()
            if key == XML_XF_NAME: return tuple( [str(name.get(key)).strip() if name.get(key) is not None and len(name.get(key)) else '[]' for name in root] )
            else: return tuple( [str(name.get(key)).strip() if name.get(key) is not None and len(name.get(key)) else [] for name in root] )
        else:
            return () 
        
        
    def __get_name_val_str(self, key: str, _DEFAULT: str = '0') -> tuple:
        """Collect all Flame presets single value from the XML Flame file and return all of them packed into a tuple.
        It will also scan each string value for invalid characters and try to remove them returning a cleaned up string value.

        Args:
            (self):
            key(str): Defaults to XML_XF_NAME. The XML Flame's name key.
            _DEFAULT(str): If something goes wrong, use this default value instead.

        Returns:
            (tuple): Flame presets single string values packed into a tuple.
        """      
        if self.isvalidtree:
            root = self.tree.getroot()
            return tuple( [str(in_flame.xf_val_cleanup_str(name.get(key), _DEFAULT, key).strip()) if name.get(key) is not None else [] for name in root] )
        else:
            return () 
        
        
    def __get_name_curve_val_str(self, key: str, _DEFAULT: str = '0') -> tuple:
        """Collect all Flame presets multi color correction curve values from the XML Flame file and return all of them packed into a tuple.
        It will also scan each string value for invalid characters and try to remove them returning a cleaned up string value.

        Args:
            (self):
            key(str): Defaults to XML_XF_NAME. The XML Flame's name key.
            _DEFAULT(str): If something goes wrong, use this default value instead.

        Returns:
            (tuple): Flame presets multi color correction curve values packed into a tuple.
        """      
        if self.isvalidtree:
            root = self.tree.getroot()
            return tuple( [str(in_flame.xf_val_cleanup_split_str(name.get(key), _DEFAULT, key).strip()) if name.get(key) is not None and name.get(key) != '' else [] for name in root] )
        else:
            return () 
        
        
    def __get_name_list_str(self, key: str) -> tuple:
        """Collect all Flame presets list values from the XML Flame file.
        Some examples of values to use this definition with are: size, center... (all key name that hold multiple string values in it)

        Args:
            (self):
            key(str): The XML Flame's key name.

        Returns:
            (tuple): Return all values packed into a tuple.
        """
        if self.isvalidtree:
            
            _d: str | None = XML_TO_F3H_DEFAULT_VALS.get(key)
            if _d is not None: _default: str = _d
            else: _default: str = '0'
            
            root = self.tree.getroot()
            return tuple( [str(in_flame.xf_list_cleanup_str(str(name.get(key)).strip().split(), _default, key)) if name.get(key) is not None else [] for name in root] )
        else:
            return () 
        
        
    def __get_flame(self, key: str = XML_FLAME_NAME) -> tuple | None:
        """Collect the actual Flame presets object data from the XML file.

        Args:
            (self):
            key (str): Defaults to XML_FLAME_NAME. The XML Flame's flame key.

        Returns:
            (tuple | None): Flames objects data or None if not found.
        """
        if self.isvalidtree:
            root = self.tree.getroot()
            return tuple( [f for f in root.iter(key)] )
        else:
            return None


    def __get_flame_count(self, flames: list) -> int:
        """Get the number of Flame presets inside the XML file.

        Args:
            (self):
            flames(list): Flames objects data.

        Returns:
            (int): Number of Flames.
        """
        if self.isvalidtree:
            return len(flames)
        return 0


# FLAM3H IN FLAME start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class in_flame(_xml_tree):
    """
class in_flame

@STATICMETHODS
* xf_val_cleanup_split_str(val: str, default_val: str = '0', key_name: str | None = None) -> str:
* xf_val_cleanup_str(val: str, default_val: str = '0', key_name: str | None = None) -> str:
* xf_list_cleanup(vals: list, default_val: str = '0', key_name: str | None = None) -> list:
* xf_list_cleanup_str(vals: list, default_val: str = '0', key_name: str | None = None) -> str:
* affine_coupling(affine: list, key: str = '', mp_idx: int | None = None, type: int = 0) -> list:
* check_all_iterator_weights(node: hou.SopNode, keyvalues: list) -> None:

@METHODS
* __is_valid_idx(self, idx: int) -> int:
* __get_xforms(self, idx: int, key: str) -> tuple | None:
* __get_xaos(self, xforms: tuple | None, key: str = XML_XF_XAOS) -> tuple | None:
* __get_affine(self, xforms: tuple | None, key: str, type: int = 0) -> tuple | None:
* __get_keyvalue(self, xforms: tuple | None, key: str, msg: bool = True) -> tuple | None:
* __get_palette(self, idx: int, key: str = XML_PALETTE) -> tuple[hou.Ramp, int, str] | None:
* __get_palette_flam3h_hsv(self, idx: int) -> TA_TypeMaker | bool:
* __get_mb_flam3h_mb(self, idx: int, key: str = '') -> int | float | bool | None:
* __get_cp_flam3h_samples(self, idx: int, palette: tuple[hou.Ramp, int, str] | None = None) -> int | bool:
* __get_flam3h_toggle(self, toggle: bool) -> int | None:

    Args:
        _xml_tree ([class]): [inherit properties methods from the _xml_tree class]
    """  

    __slots__ = ("_node", "_flame", "_flame_count", 
                 "_out_size", "_out_center", "_out_rotate", "_out_scale", "_out_quality", "_out_brightness", "_out_gamma", "_out_highlight_power", "_out_logscale_k2", "_out_vibrancy", 
                 "_out_curves", "_out_curve_overall", "_out_curve_red", "_out_curve_green", "_out_curve_blue", 
                 "_flam3h_sys_rip", "_flam3h_hsv", 
                 "_flam3h_mb", "_flam3h_mb_samples", "_flam3h_mb_shutter", "_flam3h_cp_samples", 
                 "_flam3h_prefs_f3c")

    def __init__(self, node: hou.SopNode, xmlfile: str) -> None:
        """
        Args:
            (self):
            node(hou.SopNode): This FLAM3H node
            xmlfile (str): xml *.flame v_type file to load
        """
        super().__init__(xmlfile)
        
        self._node = node
        self._flame: tuple | None = self._xml_tree__get_flame() # type: ignore
        self._flame_count: int = self._xml_tree__get_flame_count(self._flame) # type: ignore
        
        # render properties
        self._out_size: tuple = self._xml_tree__get_name_list_str(OUT_XML_FLAME_SIZE) # type: ignore
        self._out_center: tuple = self._xml_tree__get_name_list_str(OUT_XML_FLAME_CENTER) # type: ignore
        self._out_rotate: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAME_ROTATE, '0') # type: ignore
        self._out_scale: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAME_SCALE, '0') # type: ignore
        self._out_quality: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAME_QUALITY, '1000') # type: ignore
        self._out_brightness: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAME_BRIGHTNESS, '3') # type: ignore
        self._out_gamma: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAME_GAMMA, '2.5') # type: ignore
        self._out_highlight_power: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAME_POWER, '5') # type: ignore
        self._out_logscale_k2: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAME_K2, '0') # type: ignore
        self._out_vibrancy: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAME_VIBRANCY, '0.3333') # type: ignore
        
        # render curves
        self._out_curves: tuple = self._xml_tree__get_name_curve_val_str(OUT_XML_FLAME_RENDER_CURVES, OUT_XML_FLAME_RENDER_CURVES_DEFAULT) # type: ignore
        self._out_curve_overall: tuple = self._xml_tree__get_name_curve_val_str(OUT_XML_FLAME_RENDER_CURVE_OVERALL, OUT_XML_FLAME_RENDER_CURVE_DEFAULT) # type: ignore
        self._out_curve_red: tuple = self._xml_tree__get_name_curve_val_str(OUT_XML_FLAME_RENDER_CURVE_RED, OUT_XML_FLAME_RENDER_CURVE_DEFAULT) # type: ignore
        self._out_curve_green: tuple = self._xml_tree__get_name_curve_val_str(OUT_XML_FLAME_RENDER_CURVE_GREEN, OUT_XML_FLAME_RENDER_CURVE_DEFAULT) # type: ignore
        self._out_curve_blue: tuple = self._xml_tree__get_name_curve_val_str(OUT_XML_FLAME_RENDER_CURVE_BLUE, OUT_XML_FLAME_RENDER_CURVE_DEFAULT) # type: ignore
        
        # custom to FLAM3H only
        self._flam3h_sys_rip: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAM3H_SYS_RIP) # type: ignore # This xml key must be present to be set otherwise leave it untouched
        self._flam3h_hsv: tuple = self._xml_tree__get_name_list_str(OUT_XML_FLAM3H_HSV) # type: ignore
        
        # just check any of the MB val and if exist mean there is MB data to be set.
        # this will act as bool and if true, it will hold our OUT_XML_FLMA3H_MB_FPS value ( as string )
        self._flam3h_mb: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLMA3H_MB_FPS) # type: ignore # This xml key must be present to be set otherwise leave it untouched
        self._flam3h_mb_samples: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLMA3H_MB_SAMPLES, '16') # type: ignore
        self._flam3h_mb_shutter: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLMA3H_MB_SHUTTER, '0.5') # type: ignore
        self._flam3h_cp_samples: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAM3H_CP_SAMPLES, '256') # type: ignore
        
        self._flam3h_prefs_f3c: tuple = self._xml_tree__get_name_val_str(OUT_XML_FLAM3H_PREFS_F3C) # type: ignore # This xml key must be present to be set otherwise leave it untouched
        

    @staticmethod
    def xf_val_cleanup_split_str(val: str, default_val: str = '0', key_name: str | None = None) -> str:
        """ Attempt to remove invalid characters from the passed value.
        This is specifically for the XML curves data.
        It will split each knots value and check for invalid chars and if the result is a valid float. If not it will return a '0' string by default.
        In the end it will re-join everything for output.
        
        Args:
            val(str): value from the xml
            default_val(str): Default to: '0'. If something goes wrong use this as the returned value.
            key_name(str | None): Default to None. If not None, it will print out the key_name if not a value.

        Returns:
            (str): value cleaned up from invalid characters
        """  
        new = []
        knots: list = val.strip().split(' ')
        for idx, k in enumerate(knots):
            try:
                float(k)
            except ValueError:
                clean: list = [letter for letter in k if letter in CHARACTERS_ALLOWED_XFORM_VAL]
                new_val: str = ''.join(clean)
                try:
                    float(new_val)
                except ValueError:
                    new.append(default_val)
                    if key_name is not None: print(f"Warning:\nIN xml key: {key_name}[{idx}] -> NOT A VALUE\n")
                else:
                    new.append(new_val)
                    if key_name is not None: print(f"Warning:\nIN xml key: {key_name}[{idx}] -> NOT A VALUE (Corrected)\n")
            else:
                new.append(k)
                
        return ' '.join(new)


    @staticmethod
    def xf_val_cleanup_str(val: str, default_val: str = '0', key_name: str | None = None) -> str:
        """ Attempt to remove invalid characters from the passed value.
        
        Args:
            val(str): value from the xml
            default_val(str): Default to: '0'. If something goes wrong use this as the returned value.
            key_name(str | None): Default to None. If not None, it will print out the key_name if not a value. Specifically added for: in_flame_utils.in_v_parametric_var_collect(...)  but it ended up being used in other places as well.

        Returns:
            (str): value cleaned up from invalid characters
        """  
        try:
            float(val)
        except ValueError:
            clean: list = [letter for letter in val if letter in CHARACTERS_ALLOWED_XFORM_VAL]
            new_val: str = ''.join(clean)
            try:
                float(new_val)
            except ValueError:
                if key_name is not None: print(f"Warning:\nIN xml key: {key_name} -> NOT A VALUE\n")
                return default_val
            else:
                if key_name is not None: print(f"Warning:\nIN xml key: {key_name} -> NOT A VALUE (Corrected)\n")
                return new_val
        else:
            return val


    @staticmethod
    def xf_list_cleanup(vals: list, default_val: str = '0', key_name: str | None = None) -> list:
        """Attempt to remove invalid characters from the list values and return a list.
        
        Args:
            vals(list): values from the xml
            default_val(str): Default to: '0'. If something goes wrong use this as the returned value.
            key_name(str | None): Default to None. If not None, it will print out the key_name if not a value.

        Returns:
            (list): a list of affine values cleaned up from invalid characters
        """  
        new = []
        if not vals and key_name is not None:
            _d: str | None = XML_TO_F3H_LIST_DEFAULT_VALS.get(key_name)
            if _d is not None: vals = str(_d).split()
        for idx, val in enumerate(vals):
            try:
                float(val)
            except ValueError:
                clean: list = [letter for letter in val if letter in CHARACTERS_ALLOWED_XFORM_VAL]
                new_val: str = ''.join(clean)
                try:
                    float(new_val)
                except ValueError:
                    new.append(default_val)
                    if key_name is not None: print(f"Warning:\nIN xml key: {key_name}[{idx}] -> NOT A VALUE\n")
                else:
                    new.append(new_val)
                    if key_name is not None: print(f"Warning:\nIN xml key: {key_name}[{idx}] -> NOT A VALUE (Corrected)\n")
            else:
                new.append(val)
                
        return new
    
    
    @staticmethod
    def xf_list_cleanup_str(vals: list, default_val: str = '0', key_name: str | None = None) -> str:
        """ Attempt to remove invalid characters from the list values and return a spaced joined string of the list.
        
        Args:
            vals(list): values from the xml
            default_val(str): Default to: '0'. If something goesw wrong use this as the returned value.
            key_name(str | None): Default to None. If not None, it will print out the key_name if not a value.

        Returns:
            (str): a string of spaced joined affine values cleaned up from invalid characters
        """  
        new = []
        if not vals and key_name is not None:
            new_vals: str | None = XML_TO_F3H_LIST_DEFAULT_VALS.get(key_name)
            if new_vals is not None: vals = str(new_vals).split(' ')
        for idx, val in enumerate(vals):
            try:
                float(val)
            except ValueError:
                clean: list = [letter for letter in val if letter in CHARACTERS_ALLOWED_XFORM_VAL]
                new_val = ''.join(clean)
                try:
                    float(new_val)
                except ValueError:
                    new.append(default_val)
                    if key_name is not None: print(f"Warning:\nIN xml key: {key_name}[{idx}] -> NOT A VALUE\n")
                else:
                    new.append(new_val)
                    if key_name is not None: print(f"Warning:\nIN xml key: {key_name}[{idx}] -> NOT A VALUE (Corrected)\n")
            else:
                new.append(val)
                    
        return ' '.join(new)


    @staticmethod
    def affine_coupling(affine: list, key: str = '', mp_idx: int | None = None, type: int = 0) -> list:
        """ Build proper affine values composed of hou.Vector2 tuples.
        It will also check the affine passed in and provide an alternative defaults affine values if not correct and print out messages to inform the user about different cases.
        
        Args:
            vals(list): values from the xml
            key(str): The type of affine to build: XML_PRE_AFFINE, XML_POST_AFFINE, XML_FLAM3H_PRE_AFFINE, XML_FLAM3H_POST_AFFINE
            mp_idx(int | None=None): [multi parameter index, for messaging purpose only]
            type(int): Is it an iterator or an FF ?

        Returns:
            (list): a list of hou.Vector2: ((X.x, X.y), (Y.x, Y.y), (O.x, O.y)) ready to be used to set affine parms, or an empty list if something is wrong
        """      
        affine_count: int = len(affine)
        if affine_count == 6: return [hou.Vector2((tuple(affine[i:i + 2]))) for i in (0, 2, 4)]
        
        else:
            print(datetime.now().strftime('%b-%d-%Y %H:%M:%S'))
            
            sel: dict[str, str] = {XML_PRE_AFFINE: f"Pre affine", XML_POST_AFFINE: f"Post affine", XML_FLAM3H_PRE_AFFINE: f"F3H Pre affine", XML_FLAM3H_POST_AFFINE: f"F3H Post affine"}
            sel_key: str | None = sel.get(key)
            
            # Is it an iterator or an FF or None ?
            if mp_idx is not None:
                if type == 0: iter_type: int | str | None = mp_idx
                elif type == 1: iter_type: int | str | None = 'FF'
                else: iter_type: int | str | None = None
            
            if key in [XML_PRE_AFFINE, XML_POST_AFFINE]:
                if affine_count == 0:
                    if iter_type is not None: _MSG: str = f"\t{sel_key} on iterator {iter_type}, have no affine values. Expeted are: 6\n\t:Reverted back to default affine values."
                    else:_MSG: str = f"\t{sel_key} have {affine_count} values. Expeted are: 6\n\t:Reverted back to default affine values."
                    print(f"{_MSG}\n")
                    return [hou.Vector2((tuple( AFFINE_IDENT[i:i + 2] ))) for i in (0, 2, 4)]
                else:
                    if iter_type is not None: _MSG: str = f"\t{sel_key} on iterator {iter_type}, have {affine_count} values. Expeted are: 6\n\t:Using 0.0(Zeros) for missing affine values."
                    else:_MSG: str = f"\t{sel_key} have {affine_count} values. Expeted are: 6\n\t:Using 0.0(Zeros) for missing affine values."
                    print(f"{_MSG}\n")
                    return [hou.Vector2((tuple( np_pad(affine, (0, 6-min(6, affine_count)), 'constant', constant_values=0).tolist()[i:i + 2] ))) for i in (0, 2, 4)]
            
            if sel_key is not None:
                if iter_type is not None:
                    _MSG: str = f"\t{sel_key} on iterator {iter_type}, have {affine_count} values. Expeted are: 6\n\t:Skipped"
                    print(f"{_MSG}\n")
                else:
                    _MSG: str = f"\t{sel_key} have {affine_count} values. Expeted are: 6\n\t:Skipped"
                    print(f"{_MSG}\n")
                    
            return []
    
    
    @staticmethod
    def check_all_iterator_weights(node: hou.SopNode, keyvalues: list) -> None:
        """If all iterators have their weights set to: 0.0(ZERO), let the user know.
        
        Args:
            node(hou.SopNode): Current FLAM3H node we are loading a Flame preset from.
            kevalues(list): list of all iterators key values, in this case all iterator's weights values.

        Returns:
           (None):
        """   
        if min(keyvalues) == max(keyvalues) == 0:
            # Since this case is now being addressed directly in the CVEX code,
            # it is not necessary anymore to revert the value to a non-zero value anymore, but I leave the message here for the user to know anyway.
            # min_weight = 0.00000001
            # keyvalues[0] = min_weight
            _MSG: str = f"Warning:\n{node.name()}:\nThe loaded Flame preset have all iterators Weight set to: 0.0(Zero).\n"
            print(f"{_MSG}")
    
    
    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def node(self):
        return self._node
    
    # @property # This is now stored from inside: class _xml_tree:
    # def name(self):
    #     return self._name

    @property
    def flame(self):
        return self._flame

    @property
    def flame_count(self):
        return self._flame_count
    
    @property
    def out_size(self):
        return self._out_size
    
    @property
    def out_center(self):
        return self._out_center
    
    @property
    def out_rotate(self):
        return self._out_rotate
    
    @property
    def out_scale(self):
        return self._out_scale
    
    @property
    def out_quality(self):
        return self._out_quality

    @property
    def out_brightness(self):
        return self._out_brightness
    
    @property
    def out_gamma(self):
        return self._out_gamma
    
    @property
    def out_highlight_power(self):
        return self._out_highlight_power
    
    @property
    def out_vibrancy(self):
        return self._out_vibrancy
    
    # render curves
    
    @property
    def out_curves(self):
        return self._out_curves
    
    @property
    def out_curve_overall(self):
        return self._out_curve_overall
    
    @property
    def out_curve_red(self):
        return self._out_curve_red
    
    @property
    def out_curve_green(self):
        return self._out_curve_green
    
    @property
    def out_curve_blue(self):
        return self._out_curve_blue
    
    # custom to FLAM3H only

    @property
    def flam3h_hsv(self):
        return self._flam3h_hsv
    
    @property
    def flam3h_mb(self): # motion blur fps ( frames per second )
        return self._flam3h_mb
    
    @property
    def flam3h_mb_samples(self):
        return self._flam3h_mb_samples
    
    @property
    def flam3h_mb_shutter(self):
        return self._flam3h_mb_shutter
    
    @property
    def flam3h_cp_samples(self):
        return self._flam3h_cp_samples
    
    @property
    def flam3h_prefs_f3c(self): # flam3 compatibility preferences option
        return self._flam3h_prefs_f3c
    
    @property
    def flame3h_sys_rip(self):
        return self._flam3h_sys_rip
    

    def __is_valid_idx(self, idx: int) -> int:
        """Make sure the fractal flame's idx passed in will always be valid and never out of range.

        Args:
            (self):
            idx(int): flame idx out of all flames included in the loaded flame file

        Returns:
            (int): clamped idx value just in case the user pass an invalid idx to this function
        """     
        return 0 if idx < 0 else 0 if self.flame_count == 1 else self.flame_count-1 if idx > self.flame_count-1 else idx


    def __get_xforms(self, idx: int, key: str) -> tuple | None:
        """Get choosen fractal flame's xforms collected inside a dict each.
        every xform in xforms is a dict coming directly from the parsed XML file.

        Args:
            (self):
            idx(int): flame idx out of all flames included in the loaded flame file
            key(str): use "xform" for transforms and "finalxform" for final flame transform

        Returns:
            (tuple): a tuple of all xforms inside the selected flame or None
        """
        if  self.isvalidtree:
            assert self.flame is not None
            xforms: list = [xf.attrib for xf in self.flame[idx].iter(key)]
            if xforms: return tuple( [dict( zip( [str(x).lower() for x in xf.keys()], xf.values() ) ) for xf in xforms] )
                
                # xforms_lower = []
                # for xf in xforms:
                #     k = [str(x).lower() for x in xf.keys()]
                #     kv = zip(k, xf.values())
                #     xforms_lower.append(dict(kv))
                
            else: return None
            
        else: return None
    
    
    def __get_xaos(self, xforms: tuple | None, key: str = XML_XF_XAOS) -> tuple | None:
        """
        Args:
            (self):
            xforms(list): list of all xforms contained inside this flame
            key(str): the flame XML xaos tag name.

        Returns:
            (tuple | None): either a list of xaos strings or None
        """
        if  self.isvalidtree and xforms is not None:

            xaos: list = [f"xaos:{':'.join(self.xf_list_cleanup(str(xf.get(key)).split(), '1', key))}" if xf.get(key) is not None else [] for xf in xforms]
            if not max(list(map(lambda x: len(x), xaos))): return None
            else: return tuple(xaos)
        
        else:
            return None


    def __get_affine(self, xforms: tuple | None, key: str, type: int = 0) -> tuple | None:
        """
        Args:
            (self):
            xforms(list): list of all xforms contained inside this flame
            key(str): affine xml tag name. Either 'coefs' for pre affine or 'post' for post affine
            type(int): Only used by the self.affine_coupling(...) definition. It is either an iterator: 0 or an FF: 1

        Returns:
            (tuple | None): Either a list of list of tuples ((X.x, X.y), (Y.x, Y.y), (O.x, O.y)) or None
        """   
        if  self.isvalidtree and xforms is not None:
            coefs: list = [tuple(self.affine_coupling([float(x) for x in self.xf_list_cleanup(str(xf.get(key)).split(), '0', key)], key, int(idx + 1), type)) if xf.get(key) is not None else [] for idx, xf in enumerate(xforms)]
            if max(list(map(lambda x: len(x), coefs))): return tuple(coefs)
            else: return None
            
        else:
            return None


    def __get_keyvalue(self, xforms: tuple | None, key: str, msg: bool = True) -> tuple | None:
        """
        Args:
            (self):
            xforms(tuple | None): list of all xforms contained inside this Flame or None if something went wrong.
            key(str): xml tag names. For shader: 'color', 'symmetry'->(color_speed), 'opacity'

        Returns:
            (tuple | None): description
        """
        if self.isvalidtree and xforms is not None:
            
            vars_keys_pre: list | None = None
            if key == XML_XF_PB: vars_keys_pre = in_flame_utils.in_get_xforms_var_keys(xforms, in_flame_utils.in_util_make_PRE(VARS_FLAM3_DICT_IDX.keys()), XML_XF_KEY_EXCLUDE)
            
            keyvalues = []
            for idx, xform in enumerate(xforms):
                
                if xform.get(key) is not None:

                    if key in XML_XF_NAME:
                        keyvalues.append(xform.get(key))
                        continue
                    
                    else:
                        if key in XML_XF_OPACITY: default_val = '1'
                        else: default_val = '0'
                        keyvalues.append(float(self.xf_val_cleanup_str(xform.get(key), default_val, key)))
                        continue
                    
                else:
                    # Fractorium used to remap "pre_blur" to "pre_gaussian_blur" when you loaded a Flame in and it seem to be fixed in the latest version.
                    # However, if a Flame xform uses a "pre_gaussian_blur" as the first in the list 
                    # mean that every time you save the Flame from Fractorium and load it back in FLAM3H you loose a PRE variation's slot.
                    #
                    # Lets remap "pre_gaussian_blur" back to "pre_blur" when we load a flame back in FLAM3H if it is the first one in the list.
                    
                    # I could hard-code the name into the function: def in_vars_keys_remove_pgb(...), but this way I keep this dict global for all purposes.
                    pgb_name: str | list[str] | None = in_flame_utils.in_util_make_PRE(in_flame_utils.in_get_dict_key_from_value(VARS_FLAM3_DICT_IDX, 33))
                    pgb_val: str | None = xform.get(pgb_name)
                    if pgb_val is not None and vars_keys_pre is not None: # This double check because also other keys not related to "pre_blur" can fall into this block otherwise
                        if vars_keys_pre[idx] and pgb_name in vars_keys_pre[idx][0]:
                            keyvalues.append(float(self.xf_val_cleanup_str(pgb_val, '0', str(pgb_name))))
                        else:
                            keyvalues.append([])

                        continue
                    
                    else:
                        default_val: str | None = XML_TO_F3H_DEFAULT_VALS.get(key)
                        if default_val is not None:
                            keyvalues.append(float(default_val))
                            if msg: print(f"Warning: iterator.{idx+1}\nIN xml key: {key} -> NOT FOUND, default value used.\n")
                        else:
                            keyvalues.append([])
                            
                        continue
            
            # CHECKS
            if key in XML_XF_WEIGHT:
                # Let the user know
                in_flame.check_all_iterator_weights(self.node, keyvalues)
                
            return tuple(keyvalues)
        
        else:
            return None

        
    def __get_palette(self, idx: int, key: str = XML_PALETTE) -> tuple[hou.Ramp, int, str] | None:
        """
        Args:
            (self):
            idx(int): flame idx out of all flames included in the loaded flame file
            key(str): the flame XML palette tag name. Default to: XML_PALETTE

        Returns:
            (tuple[hou.Ramp, int, str] | None): return a tu-ple with an already made hou.Ramp, number of keys, format or None if something went wrong.
        """     
           
        if self.isvalidtree:
            assert self.flame is not None
            try: palette_attrib: dict | None = self.flame[idx].find(key).attrib
            except: palette_attrib: dict | None = None

            if palette_attrib is not None:
                
                # _HEX = []
                # for line in palette_hex.splitlines():
                #     cleandoc = i_cleandoc(line)
                #     if(len(cleandoc) > 1):
                #         [_HEX.append(hex) for hex in wrap(cleandoc, 6)]
                
                palette_hex: str = self.flame[idx].find(key).text
                all_lines: list[str] = [line.replace(" ", "") for line in palette_hex.splitlines()]
                HEXs: list = [hex for line in all_lines for hex in wrap(i_cleandoc(line), 6) if len(i_cleandoc(line)) > 1]
                try:
                    RGBs: list = [list(map(abs, flam3h_palette_utils.hex_to_rgb(hex))) for hex in HEXs]
                except:
                    _PALETTE: bool = False
                else:
                    _PALETTE: bool = True
                
                if _PALETTE:
                    rgb_from_XML_PALETTE: list = [(RGBs[idx][0]/(255 + 0.0), RGBs[idx][1]/(255 + 0.0), RGBs[idx][2]/(255 + 0.0)) for idx in range(len(HEXs))]
                    format: str | None = dict(palette_attrib).get(XML_PALETTE_FORMAT)
                    ramp_keys_count: int = len(rgb_from_XML_PALETTE)
                    POSs: list = list(iter_islice(iter_count(0, 1.0/(ramp_keys_count-1)), (ramp_keys_count)))
                    BASESs: list = [hou.rampBasis.Linear] * (ramp_keys_count) # type: ignore
                    return hou.Ramp(BASESs, POSs, rgb_from_XML_PALETTE), ramp_keys_count, str(format)
                
                else:
                    return None

            else:
                return None
        else:
            return None
    
    
    # custom to FLAM3H only
    def __get_palette_flam3h_hsv(self, idx: int) -> TA_TypeMaker | bool:
        """
        Args:
            (self):
            idx(int): flame idx out of all flames included in the loaded flame file

        Returns:
            (TA_TypeMaker | bool): [a hou.Vector type of HSV vals or False] Since we know the HSV is made out of 3 floats, it will always rreturn a: hou.Vector3
        """   
        if self.isvalidtree:
            palette_hsv_xml_list: str | list = self.flam3h_hsv[idx]
            if isinstance(palette_hsv_xml_list, str):
                palette_hsv_xml_s: list = palette_hsv_xml_list.split()
                if len(palette_hsv_xml_s) != 3: palette_hsv_xml_s: list = np_pad(palette_hsv_xml_s, (0, 3-min(3, len(palette_hsv_xml_s))), 'constant', constant_values=1).tolist()
                return in_flame_utils.in_util_typemaker(list(map(lambda x: float(x), palette_hsv_xml_s )))
            else:
                return False
        else:
            return False
    
    
    # custom to FLAM3H only
    def __get_mb_flam3h_mb(self, idx: int, key: str = '') -> int | float | bool:
        """
        Args:
            (self):
            idx(int): flame idx out of all flames included in the loaded flame file
            key(str): the flame XML motion blur tag name you are interested to get:
            
            OUT_XML_FLMA3H_MB_FPS -> flam3h_mb_fps
            OUT_XML_FLMA3H_MB_SAMPLES -> flam3h_mb_samples
            OUT_XML_FLMA3H_MB_SHUTTER -> flam3h_mb_shutter

        Returns:
            (int | float | bool | None): FLAM3H motion blur parameter's values.
        """   
        if self.isvalidtree:
            mb_do: str | list = self.flam3h_mb[idx]
            if isinstance(mb_do, str):
                if key == OUT_XML_FLMA3H_MB_FPS:
                    try:
                        int(mb_do)
                    except:
                        return False
                    else:
                        return int(mb_do)
                elif key == OUT_XML_FLMA3H_MB_SAMPLES:
                    mp_samples: str | list = self.flam3h_mb_samples[idx]
                    if isinstance(mp_samples, list):
                        print(f"Warning:\nIN xml key: {OUT_XML_FLMA3H_MB_SAMPLES} -> NOT FOUND, default value used.\n")
                        return int(16) # default
                    else:
                        return int(mp_samples)
                elif key == OUT_XML_FLMA3H_MB_SHUTTER:
                    mb_shutter: str | list = self.flam3h_mb_shutter[idx]
                    if isinstance(mb_shutter, list):
                        print(f"Warning:\nIN xml key: {OUT_XML_FLMA3H_MB_SHUTTER} -> NOT FOUND, default value used.\n")
                        return float(0.5) # default
                    else:
                        return float(mb_shutter)
                else:
                    return False
            else:
                return False
        else:
            return False
        
        
    # custom to FLAM3H only
    def __get_cp_flam3h_samples(self, idx: int, palette: tuple[hou.Ramp, int, str] | None = None) -> int | bool:
        """
        Args:
            self:
            idx(int): flame idx out of all flames included in the loaded flame file
                      palette(tuple[hou.Ramp, int, str]): The loaded Flame palette data if any[palette hou ramp parm, colors count, format], otherwise: None

        Returns:
            (int | bool): FLAM3H palette lookup samples parameter values.
        """   
        if self.isvalidtree:
            cp_samples_key: str | list = self.flam3h_cp_samples[idx]
            if isinstance(cp_samples_key, str):
                samples: int = int(cp_samples_key)
                if samples in PALETTE_OUT_MENU_OPTIONS_PLUS: # just make sure the lookup samples count is one of the valid options.
                    return samples
                else:
                    # else return the default value
                    return 256
            else:
                if palette is not None:
                    count: int = palette[1]
                    if count > 0: return int(flam3h_palette_utils.find_nearest_idx(PALETTE_OUT_MENU_OPTIONS_PLUS, count))
                    # else return the default value
                    else: return 256
                else:
                    # else return the default value
                    return 256
        else:
            return False
        
        
    # custom to FLAM3H only
    def __get_flam3h_toggle(self, toggle: bool) -> int | None:
        """Get FLAM3H toggle parameter value: ON or OFF ( 1 or 0 )

        Args:
            toggle(bool): Get value from a toggle (Either ON or OFF - 1 or 0)

        Returns:
            (int | None): This flame toggle or None if not found
        """

        if self.isvalidtree:
            # f3c = self._flam3h_prefs_f3c[idx]
            # self._flam3h_prefs_f3c[idx] can also be an empty list, hence the double check
            if toggle is not None and toggle:
                try:
                    int(toggle)
                except:
                    return None
                else:
                    return int(toggle)
            else:
                return None
        else:
            return None


# FLAM3H IN FLAME ITER DATA start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class in_flame_iter_data(in_flame):
    """
    Args:
        in_flame ([class]): [inherit properties methods from the in_flame class]
    """  
    
    __slots__ = ("_idx", "_xforms", "_xf_name", "_weight", "_pre_blur", "_xaos", 
                 "_coefs", "_f3h_coefs", "_f3h_coefs_angle", "_post", "_f3h_post", "_f3h_post_angle", 
                 "_finalxform", "_finalxform_coefs", "_finalxform_f3h_coefs", "_finalxform_f3h_coefs_angle", "_finalxform_post", "_finalxform_f3h_post", "_finalxform_f3h_post_angle", "_finalxform_name", 
                 "_palette", "_color", "_color_speed", "_symmetry", "_opacity", 
                 "_sys_flam3h_rip", "_cp_flam3h_hsv", "_mb_flam3h_mb_fps", "_mb_flam3h_mb_samples", "_mb_flam3h_mb_shutter", "_cp_flam3h_cp_samples", "_prefs_flam3h_f3c")
    
    def __init__(self, node: hou.SopNode, xmlfile: str, idx: int=0) -> None:
        """
        Args:
            (self):
            node(hou.SopNode): This FLAM3H node.
            xmlfile (str): xmlfile (str): xml flame v_type file to load
            idx (int, optional): flame idx out of all flames included in the loaded flame file]. Defaults to 0.
        """
        super().__init__(node, xmlfile)
        
        self._idx: int = self._in_flame__is_valid_idx(idx) # type: ignore
        self._xforms: tuple | None = self._in_flame__get_xforms(self._idx, XML_XF) # type: ignore
        self._xf_name: tuple | None = self._in_flame__get_keyvalue(self._xforms, XML_XF_NAME) # type: ignore
        self._weight: tuple | None = self._in_flame__get_keyvalue(self._xforms, XML_XF_WEIGHT) # type: ignore
        self._pre_blur: tuple | None = self._in_flame__get_keyvalue(self._xforms, XML_XF_PB) # type: ignore
        self._xaos: tuple | None  = self._in_flame__get_xaos(self._xforms) # type: ignore
        
        self._coefs: tuple | None = self._in_flame__get_affine(self._xforms, XML_PRE_AFFINE) # type: ignore
        self._f3h_coefs: tuple | None = self._in_flame__get_affine(self._xforms, XML_FLAM3H_PRE_AFFINE) # type: ignore
        self._f3h_coefs_angle: tuple | None = self._in_flame__get_keyvalue(self._xforms, XML_FLAM3H_PRE_AFFINE_ANGLE) # type: ignore
        self._post: tuple | None  = self._in_flame__get_affine(self._xforms, XML_POST_AFFINE) # type: ignore
        self._f3h_post: tuple | None  = self._in_flame__get_affine(self._xforms, XML_FLAM3H_POST_AFFINE) # type: ignore
        self._f3h_post_angle: tuple | None = self._in_flame__get_keyvalue(self._xforms, XML_FLAM3H_POST_AFFINE_ANGLE) # type: ignore
        
        self._finalxform: tuple | None = self._in_flame__get_xforms(self._idx, XML_FF) # type: ignore
        self._finalxform_coefs: tuple | None = self._in_flame__get_affine(self._finalxform, XML_PRE_AFFINE, 1) # type: ignore
        self._finalxform_f3h_coefs: tuple | None = self._in_flame__get_affine(self._finalxform, XML_FLAM3H_PRE_AFFINE, 1) # type: ignore
        self._finalxform_f3h_coefs_angle: tuple | None = self._in_flame__get_keyvalue(self._finalxform, XML_FLAM3H_PRE_AFFINE_ANGLE) # type: ignore
        self._finalxform_post: tuple | None  = self._in_flame__get_affine(self._finalxform, XML_POST_AFFINE, 1) # type: ignore
        self._finalxform_f3h_post: tuple | None = self._in_flame__get_affine(self._finalxform, XML_FLAM3H_POST_AFFINE, 1) # type: ignore
        self._finalxform_f3h_post_angle: tuple | None = self._in_flame__get_keyvalue(self._finalxform, XML_FLAM3H_POST_AFFINE_ANGLE) # type: ignore
        self._finalxform_name: tuple | None = self._in_flame__get_keyvalue(self._finalxform, XML_XF_NAME) # type: ignore
        
        self._palette: tuple[hou.Ramp, int, str] | None = self._in_flame__get_palette(self._idx) # type: ignore
        self._color: tuple | None = self._in_flame__get_keyvalue(self._xforms, XML_XF_COLOR) # type: ignore
        self._color_speed: tuple | None = self._in_flame__get_keyvalue(self._xforms, XML_XF_COLOR_SPEED, False) # type: ignore # Color speed is only used by Fractorium so we silent its warning message when missing
        self._symmetry: tuple | None = self._in_flame__get_keyvalue(self._xforms, XML_XF_SYMMETRY) # type: ignore
        self._opacity: tuple | None = self._in_flame__get_keyvalue(self._xforms, XML_XF_OPACITY) # type: ignore
        
        # custom to FLAM3H only
        self._sys_flam3h_rip: int | None = self._in_flame__get_flam3h_toggle(self._flam3h_sys_rip[self._idx]) # type: ignore
        self._cp_flam3h_hsv: TA_TypeMaker | bool = self._in_flame__get_palette_flam3h_hsv(self._idx) # type: ignore
        self._mb_flam3h_mb_fps: int | float | bool = self._in_flame__get_mb_flam3h_mb(self._idx, OUT_XML_FLMA3H_MB_FPS) # type: ignore
        self._mb_flam3h_mb_samples: int | float | bool = self._in_flame__get_mb_flam3h_mb(self._idx, OUT_XML_FLMA3H_MB_SAMPLES) # type: ignore
        self._mb_flam3h_mb_shutter: int | float | bool = self._in_flame__get_mb_flam3h_mb(self._idx, OUT_XML_FLMA3H_MB_SHUTTER) # type: ignore
        self._cp_flam3h_cp_samples: int | bool = self._in_flame__get_cp_flam3h_samples(self._idx, self.palette) # type: ignore
        self._prefs_flam3h_f3c: int | None = self._in_flame__get_flam3h_toggle(self._flam3h_prefs_f3c[self._idx]) # type: ignore


    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def idx(self):
        return self._idx

    @property
    def xforms(self):
        return self._xforms
    
    @property
    def xf_name(self):
        return self._xf_name
    
    @property
    def finalxform(self):
        return self._finalxform
    
    @property
    def finalxform_name(self):
        return self._finalxform_name
    
    @property
    def weight(self):
        return self._weight
    
    @property
    def pre_blur(self):
        return self._pre_blur
         
    @property
    def xaos(self):
        return self._xaos
 
    @property
    def coefs(self):
        return self._coefs
    
    @property
    def f3h_coefs(self):
        return self._f3h_coefs
    
    @property
    def f3h_coefs_angle(self):
        return self._f3h_coefs_angle
        
    @property
    def post(self):
        return self._post
    
    @property
    def f3h_post(self):
        return self._f3h_post
    
    @property
    def f3h_post_angle(self):
        return self._f3h_post_angle
    
    @property
    def finalxform_coefs(self):
        return self._finalxform_coefs
    
    @property
    def finalxform_f3h_coefs(self):
        return self._finalxform_f3h_coefs
    
    @property
    def finalxform_f3h_coefs_angle(self):
        return self._finalxform_f3h_coefs_angle
        
    @property
    def finalxform_post(self):
        return self._finalxform_post
    
    @property
    def finalxform_f3h_post(self):
        return self._finalxform_f3h_post
    
    @property
    def finalxform_f3h_post_angle(self):
        return self._finalxform_f3h_post_angle
    
    @property
    def palette(self):
        return self._palette
    
    @property
    def color(self):
        return self._color
    
    @property
    def color_speed(self):
        return self._color_speed
    
    @property
    def symmetry(self):
        return self._symmetry
    
    @property
    def opacity(self):
        return self._opacity
    
    # custom to FLAM3H only
    
    @property
    def cp_flam3h_hsv(self):
        return self._cp_flam3h_hsv
    
    @property
    def mb_flam3h_fps(self):
        return self._mb_flam3h_mb_fps
    
    @property
    def mb_flam3h_samples(self):
        return self._mb_flam3h_mb_samples
    
    @property
    def mb_flam3h_shutter(self):
        return self._mb_flam3h_mb_shutter
    
    @property
    def cp_flam3h_samples(self):
        return self._cp_flam3h_cp_samples
    
    @property
    def prefs_flam3h_f3c(self):
        return self._prefs_flam3h_f3c
    
    @property
    def sys_flam3h_rip(self):
        return self._sys_flam3h_rip
    
    
# FLAM3H IN FLAME UTILS start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class in_flame_utils:
    """
class in_flame_utils

@STATICMETHODS
* in_util_key_name_isalnum(key_name: str) -> str:
* in_util_make_NULL(name: T) -> T:
* in_util_make_VAR(name: TA_TypeVarCollection) -> str | list[str] | None:
* in_util_make_PRE(name: TA_TypeVarCollection) -> str | list[str] | None:
* in_util_make_POST(name: TA_TypeVarCollection) -> str | list[str] | None:
* in_load_stats_unknown_vars(preset_id: int, apo_data: in_flame_iter_data) -> list:
* in_to_flam3h_is_CHAOS(xml: str) -> bool:
* in_to_flam3h_clipboard_is_CHAOS() -> bool:
* in_get_xforms_var_keys( xforms: tuple | None, 
                        vars: TA_XformVarKeys, 
                        exclude_keys: tuple
                        ) -> list[str] | None:
* in_vars_keys_remove_pgb(vars: list | None, pgb_name: str) -> list | None:              
* in_util_removeprefix(var_name: str, prefix: str) -> str:
* in_get_xforms_var_keys_PP(xforms: tuple | None, 
                          vars: dict, 
                          prx: str, 
                          exclude_keys: tuple
                          ) -> list[str] | None:
* in_util_typemaker(data: list) -> TA_TypeMaker:
* in_get_idx_by_key(key: str) -> int | None:
* in_util_flam3h_prx_mode(mode: int) -> tuple[str, str]:
* in_set_affine(mode: int, 
              node: hou.SopNode, 
              prx: str, 
              apo_data: in_flame_iter_data, 
              flam3h_prm_names: flam3h_iterator_prm_names, 
              mp_idx: int
              ) -> None:
* in_set_data(mode: int, 
              node: hou.SopNode, 
              prx: str, 
              apo_data: tuple | list | None, 
              prm_name: str, 
              mp_idx: int
              ) -> None:
* in_prm_name_exceptions(v_type: int, app: str, apo_prm: tuple) -> tuple:
* in_get_dict_key_from_value(mydict: dict, idx: int) -> str:
* in_v_parametric_var_collect(node: hou.SopNode, 
                            mode: int, 
                            apo_prm: tuple, 
                            xform: dict, 
                            mp_idx: int, 
                            v_type: int, 
                            func: Callable) -> TA_TypeMaker:
* in_v_parametric(app: str, 
                mode: int, 
                node: hou.SopNode, 
                mp_idx: int, 
                t_idx: int, 
                xform: dict, 
                v_type: int, 
                v_weight: float, 
                var_prm: tuple, 
                apo_prm: tuple
                ) -> None:
* in_v_parametric_PRE(app: str, 
                    mode: int, 
                    node: hou.SopNode, 
                    mp_idx: int, 
                    t_idx: int, 
                    xform: dict, 
                    v_type: int, 
                    v_weight: float, 
                    var_prm: tuple, 
                    apo_prm: tuple
                    ) -> None:
* in_v_parametric_POST(app: str, 
                     mode: int, 
                     node: hou.SopNode, 
                     mp_idx: int, 
                     t_idx: int, 
                     xform: dict, 
                     v_type: int, 
                     v_weight: float, 
                     var_prm: tuple, 
                     apo_prm: tuple
                     ) -> None:
* in_v_parametric_PRE_FF(app: str, 
                       node: hou.SopNode, 
                       t_idx: int, 
                       xform: dict, 
                       v_type: int, 
                       v_weight: float, 
                       var_prm: tuple, 
                       apo_prm: tuple
                       ) -> None:
* in_v_parametric_POST_FF(app: str, 
                        node: hou.SopNode, 
                        t_idx: int, 
                        xform: dict, 
                        v_type: int, 
                        v_weight: float, 
                        var_prm: tuple, 
                        apo_prm: tuple
                        ) -> None:
* in_v_generic(mode: int, 
             node: hou.SopNode, 
             mp_idx: int, 
             t_idx: int, 
             v_type: int, 
             v_weight: float
             ) -> None:
* in_v_generic_PRE(mode: int, 
                 node: hou.SopNode, 
                 mp_idx: int, 
                 t_idx: int, 
                 v_type: int, 
                 v_weight: float
                 ) -> None:
* in_v_generic_POST(mode: int, 
                  node: hou.SopNode, 
                  mp_idx: int, 
                  t_idx: int, 
                  v_type: int, 
                  v_weight: float
                  ) -> None:
* in_v_generic_PRE_FF(node: hou.SopNode, 
                    t_idx: int, 
                    v_type: int, 
                    v_weight: float
                    ) -> None:
* in_v_generic_POST_FF(node: hou.SopNode, 
                     t_idx: int, 
                     v_type: int, 
                     v_weight: float
                     ) -> None:
* in_v_pre_blur(mode: int, 
              node: hou.SopNode, 
              mp_idx: int, 
              pb_weights: tuple
              ) -> None:
* in_util_check_negative_weight(node: hou.SopNode, w: float, v_type: int, mode: int, mp_idx: int, func: Callable) -> float:
* in_get_xforms_data_and_flam3h_vars_limit(mode: int, apo_data: in_flame_iter_data) -> tuple[tuple, int]:
* in_get_preset_name_iternum(menu_label: str) -> int | None:
* in_util_join_vars_grp(groups: list) -> str:
* in_util_vars_flatten_unique_sorted(VARS_list: list[str] | list[list[str]], func: Callable, capitalize: bool = False) -> list[str]:
* in_presets_in_isvalid_file_menu_label(node: hou.SopNode, preset_id: int) -> str:
* in_set_iter_on_load(node: hou.SopNode, preset_id: int, clipboard: bool, flame_name_clipboard: str) -> int:
* in_load_sensor_stats_msg(preset_id: int, apo_data: in_flame_iter_data) -> str:
* in_load_render_stats_msg(preset_id: int, apo_data: in_flame_iter_data) -> str:
* in_copy_sensor(node: hou.SopNode, f3r: in_flame_iter_data, preset_id: int) -> None:
* in_copy_render(node: hou.SopNode, f3r: in_flame_iter_data, preset_id: int) -> None:
* in_copy_render_cc_curves(node: hou.SopNode, f3r: in_flame_iter_data, preset_id: int) -> None:
* in_copy_render_all_stats_msg(kwargs: dict,  apo_data: in_flame_iter_data | None = None, clipboard: bool = False, flash_message: bool = False) -> None:
* in_copy_sensor_stats_msg(kwargs: dict) -> None:
* in_copy_render_stats_msg(kwargs: dict) -> None:
* in_copy_cc_curves_stats_msg(kwargs: dict) -> None:
* in_util_vars_dict_type_maker(vars_dict: dict, func: Callable) -> dict:
* in_xml_key_val(xform: dict, key_name: str, default_val: float = 0) -> float:
* menu_in_presets_loop(node: hou.SopNode, menu: list, i: int, item: str, in_idx: int, is_clipboard: int) -> None:
* menu_in_presets_loop_enum(node: hou.SopNode, menu: list, i: int, item: str, in_idx: int, is_clipboard: int) -> None:
* menu_in_presets_empty_loop(node: hou.SopNode, menu: list, i: int, item: str) -> None:
* menu_in_presets_empty_loop_enum(node: hou.SopNode, menu: list, i: int, item: str) -> None:

@METHODS
* in_flam3h_set_iterators(self, 
                          mode: int, 
                          node: hou.SopNode, 
                          apo_data: in_flame_iter_data, 
                          preset_id: int, 
                          ) -> None:
* in_load_stats_msg(self, preset_id: int, apo_data: in_flame_iter_data, clipboard: bool) -> str:
* menu_in_presets_data(self) -> list:
* menu_in_presets(self) -> list:
* menu_in_presets_empty_data(self) -> list:
* menu_in_presets_empty(self) -> list:
* set_iter_on_load_callback(self) -> None:
* use_iter_on_load_callback(self) -> None:
* in_to_flam3h_toggle(self, prm: str) -> None:
* in_to_flam3h_toggle_f3h_affine(self) -> None:
* in_to_flam3h_reset_user_data(self) -> None:
* in_to_flam3h_reset_iterators_parms(self, node: hou.SopNode, in_flame_iter_count: int) -> None:
* in_to_flam3h_resets(self, node: hou.SopNode, _FLAM3H_INIT_DATA: str | None, bool, int, str, bool, bool) -> None:
* in_to_flam3h_set_iterators(self, node: hou.SopNode, apo_data: in_flame_iter_data, _FLAM3H_INIT_DATA: TA_F3H_Init) -> None:
* in_to_flam3h_set_motion_blur(self, node: hou.SopNode, apo_data: in_flame_iter_data) -> None:
* in_to_flam3h_set_palette(self, node: hou.SopNode, apo_data: in_flame_iter_data, _FLAM3H_INIT_DATA: TA_F3H_Init) -> None:
* in_to_flam3h_stats_and_properties(self, node: hou.SopNode, apo_data: in_flame_iter_data, _FLAM3H_INIT_DATA: TA_F3H_Init, copy_only: bool = False) -> None:
* in_to_flam3h_toggles_and_msg(self, node: hou.SopNode, apo_data: in_flame_iter_data, _FLAM3H_INIT_DATA: TA_F3H_Init) -> None:
* in_to_flam3h_init_data_ALT(self) -> TA_F3H_Init:
* in_to_flam3h_init_data_SHIFT(self, node: hou.SopNode) -> TA_F3H_Init:
* in_to_flam3h_init_data(self, node: hou.SopNode) -> TA_F3H_Init:
* in_to_flam3h_sys(self) -> None:
* in_to_flam3h(self) -> None:
* in_to_flam3h_render_properties_only(self) -> None:
* reset_IN(self, mode: int = 0) -> None:

    """
    
    __slots__ = ("_kwargs", "_node")
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs: dict = kwargs
        self._node = kwargs['node']
        
        
    @staticmethod
    def in_util_key_name_isalnum(key_name: str) -> str:
        """Check and correct the passed in string for invalid characters.

        Args:
            name(str): The string to check and correct.

        Returns:
            (str): the corrected string.
        """  
        return ''.join(letter for letter in key_name.strip() if letter.isalnum())
    
    
    @staticmethod
    def in_util_make_NULL(name: T) -> T:
        """This definition is used as a place holder.

        Args:
            name(T): name or names to convert.

        Returns:
            (T): The untouched name's value passed in as argument.
        """       
        return name


    @staticmethod
    def in_util_make_VAR(name: TA_TypeVarCollection) -> str | list[str] | None:
        """Convert a PRE or POST variation name into a variation name.

        Args:
            name(TA_TypeVarCollection): name or names to convert.

        Returns:
            (str | list[str] | None): A converted str, list[str] of variation's names.
        """
        if type(name) is str:
            if name.startswith(V_PRX_PRE):
                return re_sub(REGEX_PRE, '', name)
            elif name.startswith(V_PRX_POST):
                return re_sub(REGEX_POST, '', name)
            else:
                return name
        elif type(name) is list or tuple:
            _names: list = [re_sub(REGEX_PRE, '', x) for x in name if x.startswith(V_PRX_PRE) is True]
            if not _names:
                _names = [re_sub(REGEX_POST, '', x) for x in name if x.startswith(V_PRX_POST) is True]
            if not _names:
                return None
            else:
                return _names
        else:
            return None


    @staticmethod
    def in_util_make_PRE(name: TA_TypeVarCollection) -> str | list[str] | None:
        """Convert a variation name into a variation PRE variation name.

        Args:
            name(TA_TypeVarCollection): name or names to convert.

        Returns:
            (str | list | None): A converted str, list[str] of variation's names.
        """  
        if type(name) is str:
            if not (name.startswith(V_PRX_PRE) and name.startswith(V_PRX_POST)):
                return V_PRX_PRE + name
        elif type(name) is list or tuple:
            return [V_PRX_PRE + x for x in name if x.startswith(V_PRX_PRE) is False and x.startswith(V_PRX_POST) is False]
        else:
            return None


    @staticmethod
    def in_util_make_POST(name: TA_TypeVarCollection) -> str | list[str] | None:
        """Convert a variation name into a variation POST variation name.

        Args:
            name(TA_TypeVarCollection): name or names to convert.

        Returns:
            (str | list[str] | None): A converted str, list[str] of variation's names.
        """  
        if type(name) is str:
            if not (name.startswith(V_PRX_PRE) and name.startswith(V_PRX_POST)):
                return V_PRX_POST + name
        elif type(name) is list or tuple:
            return [V_PRX_POST + x for x in name if x.startswith(V_PRX_PRE) is False and x.startswith(V_PRX_POST) is False]
        else:
            return None


    @staticmethod
    def in_load_stats_unknown_vars(preset_id: int, apo_data: in_flame_iter_data) -> list:
        """Find all the variations that Fractorium lacks if any.
        Those variations will be classified as: Unknown

        Args:
            preset_id(int): The loaded flame preset idx
            apo_data(in_flame_iter_data): The loaded flame preset data from the xml

        Returns:
            (list): List of sorted uinknown variations if any
        """
        if apo_data.plugins[preset_id]:
            plugins: list = [p.strip() for p in str(apo_data.plugins[preset_id]).split() if p]
        else:
            plugins: list = []
        
        unknown = []
        if plugins:
            for var in plugins:
                if str(var).startswith(V_PRX_PRE):
                    name: str = str(in_flame_utils.in_util_make_VAR(var)).lower()
                    if name not in VARS_FRACTORIUM_DICT[name[0]]:
                        unknown.append(var.capitalize())
                elif str(var).startswith(V_PRX_POST):
                    name: str = str(in_flame_utils.in_util_make_VAR(var)).lower()
                    if name not in VARS_FRACTORIUM_DICT[name[0]]:
                        unknown.append(var.capitalize())
                else:
                    if str(var).lower() not in VARS_FRACTORIUM_DICT[str(var)[0].lower()]:
                        unknown.append(var.capitalize())

        return sorted(unknown, key=lambda var: var)


    @staticmethod
    def in_to_flam3h_is_CHAOS(xml: str) -> bool:
        """Load a flame preset from a file and tell us if it is a Chaotica flame preset or not.

        Args:
            xml(str): the xml file to load from.

        Returns:
            (bool): attempt_to_load_from_clipboard ( bool ): Is it a Chaotica's flame preset ? True or False.
        """ 
        try: tree = lxmlET.parse(xml) # type: ignore
        except: tree = None
              
        if tree is not None:
            if XML_VALID_CHAOS_ROOT_TAG in tree.getroot().tag.lower():
                return True
            else:
                return False
        else:
            return False


    @staticmethod
    def in_to_flam3h_clipboard_is_CHAOS() -> bool:
        """Load a flame preset from the clipboard and tell us if it is a Chaotica flame preset or not.

        Args:
            (None):
            
        Returns:
            (bool): attempt_to_load_from_clipboard ( bool ): Is it a Chaotica's flame preset ? True or False.
        """     
        xml: str = hou.ui.getTextFromClipboard() # type: ignore
        try: tree = lxmlET.ElementTree(lxmlET.fromstring(xml)) # type: ignore
        except: tree = None
        
        if tree is not None:
            if XML_VALID_CHAOS_ROOT_TAG in tree.getroot().tag.lower():
                return True
            else:
                return False
        else:
            return False


    @staticmethod
    def in_get_xforms_var_keys( xforms: tuple | None, 
                                vars: TA_XformVarKeys, 
                                exclude_keys: tuple
                                ) -> list | None:
        """Return a list of all the variation names included in all xforms compared against the available FLAM3H variations.
        This is used to find variation names and PRE and POST variation names based on the provided vars argument.
        
        Use this with everything but not PRE and POST dictionary lookup, use def in_get_xforms_var_keys_PP() instead
        
        Args:
            xforms(tuple | None): list of all xforms contained inside this flame. This can be iterator's xforms or FF xform
            vars(TA_XformVarKeys): list of variations to look for inside each xfomrs, usually: VARS_FLAM3_DICT_IDX.keys()
            exclude_keys(tuple): keys to exclude from teh search to speedup a little

        Returns:
            (list | None): return a list of variation's names in each xform,  or None
        """    
        if xforms is not None:
            if type(vars) is dict:
                return [list(map(lambda x: x, filter(lambda x: x in vars.get(x[0]), filter(lambda x: x not in exclude_keys, xf.keys())))) for xf in xforms] # type: ignore
            else:
                return [list(map(lambda x: x, filter(lambda x: x in vars, filter(lambda x: x not in exclude_keys, xf.keys())))) for xf in xforms] # type: ignore
        else:
            return None
        
        
    @staticmethod
    def in_vars_keys_remove_pgb(vars: list | None, pgb_name: str) -> list | None:
        """Remove "pre_gaussian_blur" variation if it is the first one in the list as we are remapping it to "pre_blur" on load.
        Args:
            vars(list | None): per iterator list of variations used, ideally always the PRE variations are passed here
            pgb_name(str): The name of the "pre_gaussian_blur" variation to check against.

        Returns:
            (list | None): A new list containing all iterator list of used variations without the "pre_gaussian_blur" if it was the first one in the list. 
        """
        if vars is not None:
            [vars[idx].pop(0) for idx, iter in enumerate(vars) if iter and iter[0] == pgb_name]
            return vars
        else:
            return None
    
        
    @staticmethod
    def in_util_removeprefix(var_name: str, prefix: str) -> str:
        """Remove any prefix, if a prefix is present, from a variation name.
        * ex: from: pre_linear to: linear
        * ex: from post_mobius to: mobius
    
        Args:
            var_name(str): the variation name to remove the prefix from
            prefix(str): the prefix to check

        Returns:
            (str): a variation name without the prefix, or the original variation name if it did not have any prefix. 
        """
        if var_name.startswith(prefix):
            return var_name[len(prefix):]
        else:
            return var_name[:]
        
        
    @staticmethod 
    def in_get_xforms_var_keys_PP(  xforms: tuple | None, 
                                    vars: dict, 
                                    prx: str, 
                                    exclude_keys: tuple
                                    ) -> list | None:
        """find a PRE or POST variation inside the currently processed xform/iterator. All xforms are passed in.

        Args:
            xforms(tuple | None): All the xforms of this flame. This can be iterator's xforms or FF xform.
            vars(dict): the variations we are searching for
            prx(str): the current type of the variation expressed as a prefix: "pre" or "post"
            exclude_keys(tuple): exclude those keys inside the current xform/iterator from the search to speed up a little

        Returns:
            (list | None): return a list of variations found using the prefix criteria
        """  
        if xforms is not None:
            return [list(map(lambda x: x, filter(lambda x: x in vars.get(in_flame_utils.in_util_removeprefix(x, prx)[0]), filter(lambda x: x.startswith(prx), filter(lambda x: x not in exclude_keys, xf.keys()))))) for xf in xforms] # type: ignore
        else:
            return None
        
        
    @staticmethod
    def in_util_typemaker(data: list) -> TA_TypeMaker:
        """Based on how many element in the passed list return the proper type of data.
        
        Args:
            data(list): [a list of floats containinig the current parameter values to be converted into hou types]

        Returns:
            (TA_TypeMaker): Based on how many element in the passed list return the proper type of data
        """
        len_data: int = len(data)
        
        match len_data:
            
            case 1:
                return float(data[0])
            case 2:
                return hou.Vector2((data))
            case 3:
                return hou.Vector3((data))
            case 4:
                return hou.Vector4((data))
            case _:
                return data
        
        
    @staticmethod  
    def in_get_idx_by_key(key: str) -> int | None:
        """Return the variation idx based on its name from the variation's dictionary.
        
        Args:
            key(str): variation name we are processing

        Returns:
            (int | None): return variation idx from the tuple look up table
        """
        try: idx = VARS_FLAM3_DICT_IDX.get(key)
        except: return None
        return idx
        
        
    @staticmethod
    def in_util_flam3h_prx_mode(mode: int) -> tuple[str, str]:
        """Set a prefix based on modes ( iterator, FF, FF PRE/POST )
        Args:
            mode(int): 0 for iterator and 1 for FF

        Returns:
            (tuple[str, str]): return parameter prefixes based on mode: Iterator, FF, FF POST
        """
        
        match mode:
            
            case 1: # FF
                prx = PRX_FF_PRM
                prx_prm = f"{PRX_FF_PRM}_"
                
            case 2: # FF PRE/POST
                prx = PRX_FF_PRM
                prx_prm = f"{PRX_FF_PRM_POST}_"
                
            case _: # Iterator
                prx: str = ""
                prx_prm: str = ""
                
        return prx, prx_prm
    
    
    @staticmethod
    def in_set_affine(mode: int, 
                      node: hou.SopNode, 
                      prx: str, 
                      apo_data: in_flame_iter_data, 
                      flam3h_prm_names: flam3h_iterator_prm_names, 
                      mp_idx: int
                      ) -> None:
        """Set the affine values based on the loaded flame preset affine values for an iterator or the FF.
        Added the ability to set parameters based also on the F3H affine style format if included in the loaded Flame preset.
        
        Args:
            mode(int): 0 for iterator. 1 for FF
            node(hou.SopNode): Current FLAM3H node
            prx(str): parameter name prefix
            apo_data(in_flame_iter_data): Apophysis XML data collection from: class[in_flame_iter_data]
            flam3h_prm_names(flam3h_iterator_prm_names): Class of FLAM3H iterator parameter's names
            mp_idx(int): Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
        """
        idx: str = str(mp_idx + 1)
        pre_affine: tuple = (flam3h_prm_names.preaffine_x, flam3h_prm_names.preaffine_y, flam3h_prm_names.preaffine_o)
        post_affine: tuple = (flam3h_prm_names.postaffine_x, flam3h_prm_names.postaffine_y, flam3h_prm_names.postaffine_o)
        f3h_affine: int = node.parm(IN_FLAM3H_AFFINE_STYLE).eval()
        
        if mode:
            
            if f3h_affine and apo_data.finalxform_f3h_coefs is not None and apo_data.finalxform_f3h_coefs[mp_idx]:
                [node.setParms({f"{prx}{pre_affine[id]}": apo_data.finalxform_f3h_coefs[mp_idx][id]}) for id in range(3)] # type: ignore
                node.setParms({f"{prx}{flam3h_prm_names.preaffine_ang}": apo_data.finalxform_f3h_coefs_angle[mp_idx]}) # type: ignore
            else:
                if apo_data.finalxform_coefs is not None:
                    # The affine XML key: "coefs" must always be present in the XML file.
                    [node.setParms({f"{prx}{pre_affine[id]}": apo_data.finalxform_coefs[mp_idx][id]}) for id in range(3)] # type: ignore
                else:
                    # If not present, we set all the pre affine values for this iterator to a value of: 0(Zero)
                    # Doing so it wont error out on load and it will act as a warning sign.
                    print(f"Warning: iterator.FF\nIN xml key: {XML_PRE_AFFINE} -> NOT FOUND, zero values used.\n")
                    [node.setParms({f"{prx}{pre_affine[id]}": [hou.Vector2((tuple( [0, 0, 0, 0, 0, 0][i:i + 2] ))) for i in (0, 2, 4)][id]}) for id in range(3)] # type: ignore
                
            if apo_data.finalxform_post is not None:
                node.setParms({f"{prx}{flam3h_prm_names.postaffine_do}": 1}) # type: ignore
                if f3h_affine and apo_data.finalxform_f3h_post is not None and apo_data.finalxform_f3h_post[mp_idx]:
                    [node.setParms({f"{prx}{post_affine[id]}": apo_data.finalxform_f3h_post[mp_idx][id]}) for id in range(3)] # type: ignore
                    node.setParms({f"{prx}{flam3h_prm_names.postaffine_ang}": apo_data.finalxform_f3h_post_angle[mp_idx]}) # type: ignore
                else:
                    [node.setParms({f"{prx}{post_affine[id]}": apo_data.finalxform_post[mp_idx][id]}) for id in range(3)] # type: ignore
                
        else:
            
            if f3h_affine and apo_data.f3h_coefs is not None and apo_data.f3h_coefs[mp_idx]:
                [node.setParms({f"{prx}{pre_affine[id]}_{idx}": apo_data.f3h_coefs[mp_idx][id]}) for id in range(3)] # type: ignore
                node.setParms({f"{prx}{flam3h_prm_names.preaffine_ang}_{idx}": apo_data.f3h_coefs_angle[mp_idx]}) # type: ignore
            else:
                if apo_data.coefs is not None and apo_data.coefs[mp_idx]:
                    # The affine XML key: "coefs" must always be present in the XML file.
                    [node.setParms({f"{prx}{pre_affine[id]}_{idx}": apo_data.coefs[mp_idx][id]}) for id in range(3)] # type: ignore
                else:
                    # If not present, we set all the pre affine values for this iterator to a value of: 0(Zero)
                    # Doing so it wont error out on load and it will act as a warning sign.
                    print(f"Warning: iterator.{mp_idx+1}\nIN xml key: {XML_PRE_AFFINE} -> NOT FOUND, zero values used.\n")
                    [node.setParms({f"{prx}{pre_affine[id]}_{idx}": [hou.Vector2((tuple( [0, 0, 0, 0, 0, 0][i:i + 2] ))) for i in (0, 2, 4)][id]}) for id in range(3)] # type: ignore
                
            if apo_data.post is not None and apo_data.post[mp_idx]:
                node.setParms({f"{prx}{flam3h_prm_names.postaffine_do}_{idx}": 1}) # type: ignore
                if f3h_affine and apo_data.f3h_post is not None and apo_data.f3h_post[mp_idx]:
                    [node.setParms({f"{prx}{post_affine[id]}_{idx}": apo_data.f3h_post[mp_idx][id]}) for id in range(3)] # type: ignore
                    node.setParms({f"{prx}{flam3h_prm_names.postaffine_ang}_{idx}": apo_data.f3h_post_angle[mp_idx]}) # type: ignore
                else:
                    [node.setParms({f"{prx}{post_affine[id]}_{idx}": apo_data.post[mp_idx][id]}) for id in range(3)] # type: ignore


    @staticmethod
    def in_set_data(mode: int, 
                    node: hou.SopNode, 
                    prx: str, 
                    apo_data: tuple | list | None, 
                    prm_name: str, 
                    mp_idx: int
                    ) -> None:
        """Set single parameter data value from the loaded flame preset.
        An example of the parameter you will set using this function are:
        
        * main_note
        * main_weight
        * shader_speed
        * shader_color
        * shader_alpha
        * xaos
        
        Args:
            mode(int): 0 for iterator. 1 for FF
            node(hou.SopNode): Current FLAM3H node
            prx(str): parameter name prefix
            apo_data(in_flame_iter_data): Apophysis XML data collection from: class[in_flame_iter_data
            prm_name(str): parameter name for the current data we want to set
            mp_idx(int): Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
        
        Returns:
            (None):
        """
        if mode: pass
        else:
            if apo_data is not None:
                n = flam3h_iterator_prm_names()
                if prm_name not in [n.shader_alpha, n.main_weight]:
                    if apo_data[mp_idx]:
                        node.setParms({f"{prx}{prm_name}_{str(mp_idx + 1)}": apo_data[mp_idx]}) # type: ignore
                else:
                    node.setParms({f"{prx}{prm_name}_{str(mp_idx + 1)}": apo_data[mp_idx]}) # type: ignore
           
           
    @staticmethod  
    def in_prm_name_exceptions(v_type: int, app: str, apo_prm: tuple) -> tuple:
        """Some software have variation names and parameters names different from FLAM3H and Apophysis.
        This will take care of those special cases.
        It will swap the current variation dictionary item with the one the posses the corret names.

        Args:
            v_type(int): The current variation we are processing
            app(str): The software used to generate the loaded flame preset.
            apo_prm(tuple): If no exception is found, return the original variation and parameter's names.

        Returns:
            (tuple): If an exception is confirmed, return the parameter expected parameter's name.
        """
        if app.startswith(XML_APP_NAME_FRACTORIUM):
            check: tuple | None = flam3h_varsPRM_APO().varsPRM_FRACTORIUM_EXCEPTIONS.get(v_type)
            if check is not None:
                return check
            else:
                return apo_prm
        else:
            return apo_prm
        
        
    @staticmethod
    def in_get_dict_key_from_value(mydict: dict, idx: int) -> str:
        """Get the dictionary key from the dictionary value.
        Used to get the current variation string name from its index from the global dict: VARS_FLAM3_DICT_IDX

        Args:
            mydict(dict): The dictionary for lookup
            idx(int): The variation index to retrieve its string name from.

        Returns:
            (str): The variation string name.
        """       
        var_name: str = list(mydict.keys())[list(mydict.values()).index(idx)] 
        return var_name
    
    
    @staticmethod
    def in_v_parametric_var_collect(node: hou.SopNode, 
                                    mode: int, 
                                    apo_prm: tuple, 
                                    xform: dict, 
                                    mp_idx: int, 
                                    v_type: int, 
                                    func: Callable) -> TA_TypeMaker:
        """Every parametric variation posses a certain number of parameters to control its behavior.
        In FLAM3H, those parameters have been grouped into a single data type.
        For example the Curl variation posses two parametric parameters: c1, c2
        Those two parameters have been packed into a vector2 data type: vector2[c1, c2].
        This has been done to help with performance as querying many, many different parameters did end up being costly,
        especially considering having many iterators each with parametric variations at the same time.
        
        Args:
            node(hou.SopNode): Current FLAM3H node
            mode(int): 0 for iterator. 1 for FF
            apo_prm(tuple): tuple of APO variation parametric parameters names: flam3h_varsPRM_APO().varsPRM[v_type]
            xform(dict): current xform we are processing to the relative key names and values for the iterator
            mp_idx(int): for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
            v_type(int): the current variation type index
            func(Callable): function to change variation name between var, pre_var and post_var
        
        Returns:
            (TA_TypeMaker): Expected data type of the collected parametric variation's parameters values.
        """   
        
        iter_type: str = f"{mp_idx + 1}"
        if mode: iter_type = 'FF'

        VAR: list = []
        for names in apo_prm[1:-1]:
            var_prm_vals: list = []
            for n in [x.lower() for x in names]:
                # If one of the FLAM3H parameter is not in the xform, skip it and set it to ZERO for now.
                n: str = func(n)
                if xform.get(n) is not None:
                    var_prm_vals.append(float(in_flame.xf_val_cleanup_str(str(xform.get(n)), '0', n)))
                else:
                    # If a variation parameter FLAM3H has is not found, set it to ZERO. Print its name to let us know if not inside XML_XF_PRM_EXCEPTION
                    if n not in XML_XF_PRM_EXCEPTION:
                        var_prm_vals.append(float(0))
                        print(f"Warning: iterator.{iter_type}\n{node.name()}: PARAMETER NOT FOUND\n-> Variation: {func(in_flame_utils.in_get_dict_key_from_value(VARS_FLAM3_DICT_IDX, v_type))}\n-> Missing parameter: {n}\n")
                        
            VAR.append(in_flame_utils.in_util_typemaker(var_prm_vals))

        return VAR


    @staticmethod
    def in_v_parametric(app: str, 
                        mode: int, 
                        node: hou.SopNode, 
                        mp_idx: int, 
                        t_idx: int, 
                        xform: dict, 
                        v_type: int, 
                        v_weight: float, 
                        var_prm: tuple, 
                        apo_prm: tuple
                        ) -> None:
        """Set a FLAM3H parametric variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        This include setting the variation type, its weight and its parametric parameters for an iterator or the FF.
        
        Args:
            app(str): What software were used to generate this flame preset
            mode(int): 0 for iterator. 1 for FF
            node(hou.SopNode): Current FLAM3H node
            mp_idx(int): for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
            t_idx(int): current variation number idx to use with: flam3h_iterator().sec_varsT, flam3h_iterator().sec_varsW
            xform(dict): current xform we are processing to the relative key names and values for the iterator
            v_type(int): the current variation type index
            v_weight(float): the current variation weight
            var_prm(tuple): tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM().varsPRM[v_type]
            apo_prm(tuple): tuple of APO variation parametric parameters names: flam3h_varsPRM_APO().varsPRM[v_type]
            
        Returns:
            (None):
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)

        VAR: TA_TypeMaker = in_flame_utils.in_v_parametric_var_collect( node, 
                                                                        mode, 
                                                                        apo_prm, 
                                                                        xform, 
                                                                        mp_idx, 
                                                                        v_type, 
                                                                        in_flame_utils.in_util_make_NULL)

        mpidx: str = str(mp_idx + 1)
        [node.setParms({f"{prx_prm}{prm[0][:-1]}": VAR[idx]}) if mode else node.setParms({f"{prx_prm}{prm[0]}{mpidx}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        
        f3h_iter = flam3h_iterator()
        if mode:
            node.setParms({f"{prx}{f3h_iter.sec_varsT[t_idx][:-1]}": v_type}) # type: ignore
            node.setParms({f"{prx}{f3h_iter.sec_varsW[t_idx][0][:-1]}": v_weight}) # type: ignore
        else:
            node.setParms({f"{prx}{f3h_iter.sec_varsT[t_idx]}{mpidx}": v_type}) # type: ignore
            node.setParms({f"{prx}{f3h_iter.sec_varsW[t_idx][0]}{mpidx}": v_weight}) # type: ignore
            
            
    @staticmethod
    def in_v_parametric_PRE(app: str, 
                            mode: int, 
                            node: hou.SopNode, 
                            mp_idx: int, 
                            t_idx: int, 
                            xform: dict, 
                            v_type: int, 
                            v_weight: float, 
                            var_prm: tuple, 
                            apo_prm: tuple
                            ) -> None:
        """Set a FLAM3H parametric PRE variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        This include setting the variation type, its weight and its parametric parameters.
        
        Args:
            app(str): What software were used to generate this flame preset
            mode(int): 0 for iterator. 1 for FF
            node(hou.SopNode): Current FLAM3H node
            mp_idx(int): for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
            t_idx(int): current variation number idx to use with: flam3h_iterator().sec_prevarsT, flam3h_iterator().sec_prevarsW
            xform(dict): current xform we are processing to the relative key names and values for the iterator
            v_type(int): the current variation type index
            v_weight(float): the current variation weight
            var_prm(tuple): tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM().varsPRM[v_type]
            apo_prm(tuple): tuple of APO variation parametric parameters names: flam3h_varsPRM_APO().varsPRM[v_type]
            
        Returns:
            (None):
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)
        
        VAR: TA_TypeMaker = in_flame_utils.in_v_parametric_var_collect( node, 
                                                                        mode, 
                                                                        apo_prm, 
                                                                        xform, 
                                                                        mp_idx, 
                                                                        v_type, 
                                                                        in_flame_utils.in_util_make_PRE)
        
        mpidx: str = str(mp_idx + 1)
        [node.setParms({f"{prx_prm}{prm[0]}{mpidx}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        # Only on pre variations with parametric so:
        node.setParms({f"{prx}{flam3h_iterator().sec_prevarsT[t_idx]}{mpidx}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3h_iterator().sec_prevarsW[1:][t_idx][0]}{mpidx}": v_weight}) # type: ignore 


    @staticmethod
    def in_v_parametric_POST(app: str, 
                             mode: int, 
                             node: hou.SopNode, 
                             mp_idx: int, 
                             t_idx: int, 
                             xform: dict, 
                             v_type: int, 
                             v_weight: float, 
                             var_prm: tuple, 
                             apo_prm: tuple
                             ) -> None:
        """Set a FLAM3H parametric POST variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        This include setting the variation type, its weight and its parametric parameters.
        
        Args:
            app(str): What software were used to generate this flame preset
            mode(int): 0 for iterator. 1 for FF
            node(hou.SopNode): Current FLAM3H node
            mp_idx(int): for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
            t_idx(int): current variation number idx to use with: flam3h_iterator().sec_postvarsT, flam3h_iterator().sec_postvarsW
            xform(dict): current xform we are processing to the relative key names and values for the iterator
            v_type(int): the current variation type index
            v_weight(float): the current variation weight
            var_prm(tuple): tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM().varsPRM[v_type]
            apo_prm(tuple): tuple of APO variation parametric parameters names: flam3h_varsPRM_APO().varsPRM[v_type]
            
        Returns:
            (None):
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)

        VAR: TA_TypeMaker = in_flame_utils.in_v_parametric_var_collect( node, 
                                                                        mode, 
                                                                        apo_prm, 
                                                                        xform, 
                                                                        mp_idx, 
                                                                        v_type, 
                                                                        in_flame_utils.in_util_make_POST)
        
        mpidx: str = str(mp_idx + 1)
        [node.setParms({f"{prx_prm}{prm[0]}{mpidx}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        # Only on post variation with parametric so:
        node.setParms({f"{prx}{flam3h_iterator().sec_postvarsT[t_idx]}{mpidx}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3h_iterator().sec_postvarsW[t_idx][0]}{mpidx}": v_weight}) # type: ignore
    
    
    @staticmethod    
    def in_v_parametric_PRE_FF(app: str, 
                               node: hou.SopNode, 
                               t_idx: int, 
                               xform: dict, 
                               v_type: int, 
                               v_weight: float, 
                               var_prm: tuple, 
                               apo_prm: tuple
                               ) -> None:
        """Set a FLAM3H parametric FF PRE variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        This include setting the variation type, its weight and its parametric parameters.
        
        Args:
            app(str): What software were used to generate this flame preset
            node(hou.SopNode): Current FLAM3H houdini node
            t_idx(int): current variation number idx to use with: flam3h_iterator().sec_prevarsT_FF, flam3h_iterator().sec_prevarsW_FF
            xform(dict): current xform we are processing to the relative key names and values for the iterator
            v_type(int): the current variation type index
            v_weight(float): the current variation weight
            var_prm(tuple): tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM().varsPRM[v_type]
            apo_prm(tuple): tuple of APO variation parametric parameters names: flam3h_varsPRM_APO().varsPRM[v_type]
            
        Returns:
            (None):
        """
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)

        VAR: TA_TypeMaker = in_flame_utils.in_v_parametric_var_collect( node, 
                                                                        1, 
                                                                        apo_prm, 
                                                                        xform, 
                                                                        0, 
                                                                        v_type, 
                                                                        in_flame_utils.in_util_make_PRE)
            
        [node.setParms({f"{PRX_FF_PRM_POST}_{prm[0][0:-1]}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        # Only on post variation with parametric so:
        node.setParms({f"{flam3h_iterator_FF().sec_prevarsT_FF[t_idx]}": v_type}) # type: ignore
        node.setParms({f"{flam3h_iterator_FF().sec_prevarsW_FF[t_idx][0]}": v_weight}) # type: ignore


    @staticmethod
    def in_v_parametric_POST_FF(app: str, 
                                node: hou.SopNode, 
                                t_idx: int, 
                                xform: dict, 
                                v_type: int, 
                                v_weight: float, 
                                var_prm: tuple, 
                                apo_prm: tuple
                                ) -> None:
        """Set a FLAM3H parametric FF POST variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        This include setting the variation type, its weight and its parametric parameters.
        
        Args:
            app(str): What software were used to generate this flame preset
            node(hou.SopNode): Current FLAM3H node
            t_idx(int): current variation number idx to use with: flam3h_iterator().sec_postvarsT_FF, flam3h_iterator().sec_postvarsW_FF
            xform(dict): current xform we are processing to the relative key names and values for the iterator
            v_type(int): the current variation type index
            v_weight(float): the current variation weight
            var_prm(tuple): tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM().varsPRM[v_type]
            apo_prm(tuple): tuple of APO variation parametric parameters names: flam3h_varsPRM_APO().varsPRM[v_type]
            
        Returns:
            (None):
        """
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)

        VAR: TA_TypeMaker = in_flame_utils.in_v_parametric_var_collect( node, 
                                                                        1, 
                                                                        apo_prm, 
                                                                        xform, 
                                                                        0, 
                                                                        v_type, 
                                                                        in_flame_utils.in_util_make_POST)
            
        [node.setParms({f"{PRX_FF_PRM_POST}_{prm[0][0:-1]}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        # Only on post variation with parametric so:
        node.setParms({f"{flam3h_iterator_FF().sec_postvarsT_FF[t_idx]}": v_type}) # type: ignore
        node.setParms({f"{flam3h_iterator_FF().sec_postvarsW_FF[t_idx][0]}": v_weight}) # type: ignore


    @staticmethod
    def in_v_generic(mode: int, 
                     node: hou.SopNode, 
                     mp_idx: int, 
                     t_idx: int, 
                     v_type: int, 
                     v_weight: float
                     ) -> None:
        """Set a FLAM3H variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        
        Args:
            mode(int): 0 for iterator. 1 for FF
            node(hou.SopNode): Current FLAM3H node
            mp_idx(int): Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
            t_idx(int): Current variation number idx to use with: flam3h_iterator().sec_prevarsT, flam3h_iterator().sec_prevarsW
            v_type(int): Current variation type index
            v_weight(float): Current variation weight
            
        Returns:
            (None):
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        f3h_iter = flam3h_iterator()
        if mode:
            node.setParms({f"{prx}{f3h_iter.sec_varsT[t_idx][:-1]}": v_type}) # type: ignore
            node.setParms({f"{prx}{f3h_iter.sec_varsW[t_idx][0][:-1]}": v_weight}) # type: ignore
        else:
            idx = str(mp_idx + 1)
            node.setParms({f"{prx}{f3h_iter.sec_varsT[t_idx]}{idx}": v_type}) # type: ignore
            node.setParms({f"{prx}{f3h_iter.sec_varsW[t_idx][0]}{idx}":v_weight}) # type: ignore


    @staticmethod
    def in_v_generic_PRE(mode: int, 
                         node: hou.SopNode, 
                         mp_idx: int, 
                         t_idx: int, 
                         v_type: int, 
                         v_weight: float
                         ) -> None:
        """Set a FLAM3H PRE variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        
        Args:
            mode(int): 0 for iterator. 1 for FF
            node(hou.SopNode): Current FLAM3H node
            mp_idx(int): Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
            t_idx(int): Current variation number idx to use with: flam3h_iterator().sec_prevarsT, flam3h_iterator().sec_prevarsW
            v_type(int): Current variation type index
            v_weight(float): Current variation weight
            
        Returns:
            (None):
        """
        idx: str = str(mp_idx + 1)
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        node.setParms({f"{prx}{flam3h_iterator().sec_prevarsT[t_idx]}{idx}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3h_iterator().sec_prevarsW[1:][t_idx][0]}{idx}":v_weight}) # type: ignore


    @staticmethod
    def in_v_generic_POST(mode: int, 
                          node: hou.SopNode, 
                          mp_idx: int, 
                          t_idx: int, 
                          v_type: int, 
                          v_weight: float
                          ) -> None:
        """Set a FLAM3H POST variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        
        Args:
            mode(int): [0 for iterator. 1 for FF
            node(hou.SopNode): Current FLAM3H node
            mp_idx(int): Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
            t_idx(int): Current variation number idx to use with: flam3h_iterator().sec_prevarsT, flam3h_iterator().sec_prevarsW
            v_type(int): Current variation type index
            v_weight(float): Current variation weight
            
        Returns:
            (None):
        """
        idx: str = str(mp_idx + 1)
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        node.setParms({f"{prx}{flam3h_iterator().sec_postvarsT[t_idx]}{idx}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3h_iterator().sec_postvarsW[t_idx][0]}{idx}":v_weight}) # type: ignore


    @staticmethod
    def in_v_generic_PRE_FF(node: hou.SopNode, 
                            t_idx: int, 
                            v_type: int, 
                            v_weight: float
                            ) -> None:
        """Set a FLAM3H FF PRE variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        
        Args:
            node(hou.SopNode): Current FLAM3H node
            t_idx(int): Current variation number idx to use with: flam3h_iterator().sec_prevarsT, flam3h_iterator().sec_prevarsW
            v_type(int): Current variation type index
            v_weight(float): Current variation weight
            
        Returns:
            (None):
        """
        node.setParms({f"{flam3h_iterator_FF().sec_prevarsT_FF[t_idx]}": v_type}) # type: ignore
        node.setParms({f"{flam3h_iterator_FF().sec_prevarsW_FF[t_idx][0]}":v_weight}) # type: ignore


    @staticmethod
    def in_v_generic_POST_FF(node: hou.SopNode, 
                             t_idx: int, 
                             v_type: int, 
                             v_weight: float
                             ) -> None:
        """Set a FLAM3H FF POST variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        
        Args:
            node(hou.SopNode): Current FLAM3H node
            t_idx(int): Current variation number idx to use with: flam3h_iterator().sec_prevarsT, flam3h_iterator().sec_prevarsW
            v_type(int): Current variation type index
            v_weight(float): Current variation weight
            
        Returns:
            (None):
        """
        node.setParms({f"{flam3h_iterator_FF().sec_postvarsT_FF[t_idx]}": v_type}) # type: ignore
        node.setParms({f"{flam3h_iterator_FF().sec_postvarsW_FF[t_idx][0]}":v_weight}) # type: ignore


    @staticmethod
    def in_v_pre_blur(mode: int, 
                      node: hou.SopNode, 
                      mp_idx: int, 
                      pb_weights: tuple
                      ) -> None:
        """Set a FLAM3H pre_blur variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        
        Args:
            mode(int): 0 for iterator. 1 for FF
            node(hou.SopNode): Current FLAM3H node
            mp_idx(int): Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
            pb_weights(tuple): all iterators pre_blur weight values
        
        Returns:
            (None):
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        if mode: pass
        else:
            if pb_weights[mp_idx]:
                node.setParms({f"{prx}{flam3h_iterator_prm_names().prevar_weight_blur}_{str(mp_idx + 1)}": pb_weights[mp_idx]}) # type: ignore


    @staticmethod
    def in_util_check_negative_weight(node: hou.SopNode, w: float, v_type: int, mode: int, mp_idx: int, func: Callable) -> float:
        """FLAM3H do not allow negative variation's weights for the PRE and POST variations.
        This function will turn a negative weight into its absoulute value instead.

        Args:
            node(hou.SopNode): FLAM3H node
            w(float): The variation weight to check.
            v_type_name(str): The name of the variation to print out if it turn out to have its weight with a negative value.
            mode(int): 0 for iterator. 1 for FF
            mp_idx(int): for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)
            func(Callable): function to change variation name between var, pre_var and post_var
            
        Returns:
            (float): If the passed in weight value is negative, return its absolute value. Only for PRE and POST variations.
        """
        if w < 0:
            iter_type: str = f"{mp_idx + 1}"
            if mode: iter_type = 'FF'
            print(f"Warning: iterator.{iter_type}\n{node.name()}: NEGATIVE VALUE not allowed in PRE or POST\n-> Variation: {func(in_flame_utils.in_get_dict_key_from_value(VARS_FLAM3_DICT_IDX, v_type))}: {w}\n-> Using its absolute value instead: {abs(w)}\n")
            return abs(w)
        else: return w


    @staticmethod
    def in_get_xforms_data_and_flam3h_vars_limit(mode: int, apo_data: in_flame_iter_data) -> tuple[tuple, int]:
        """Get all the xforms data based on mode ( iterator or FF ),
        and get all the allowed variations to be used based on mode ( iterator or FF ).

        Args:
            mode(int): iterator or FF
            apo_data(in_flame_iter_data): Flames data from the flame file loaded in: class: in_flame_iter_data()

        Returns:
            (tuple[tuple, int]): Return a tuple containing either the iterator's xforms or the FF xform and max variation limit allowed.
        """
        xf: tuple | None = None
        _MAX_VARS: int = 0
        if mode:
            _MAX_VARS = MAX_FF_VARS
            xf = apo_data.finalxform
        else:
            _MAX_VARS = MAX_ITER_VARS
            xf = apo_data.xforms
        assert xf is not None
        return xf, _MAX_VARS


    @staticmethod
    def in_get_preset_name_iternum(menu_label: str) -> int | None:
        """Get the iteration number from the loaded Flame preset if any.

        Args:
            preset_name(str): The Flame preset name.

        Returns:
            (int | None): The iteration number or none.
        """
        splt: tuple = menu_label.rpartition(FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV)
        if len([item for item in splt if item]) > 1:
            try:
                int(splt[-1])
            except:
                return None
            else:
                return int(splt[-1])
        else:
            return None


    @staticmethod
    def in_util_join_vars_grp(groups: list) -> str:
        """When formatting a message to print out we use groups as if they were each line of the meesage and join them.
        This function will avoid to have an extra empty line at the very end.

        Args:
            groups(list): The groups to join

        Returns:
            (str): The final message without the extra empty line at the end.
        """     
        vars: list = [", ".join(grp) + ",\n" if id < len(groups)-1 else ", ".join(grp) + "." for id, grp in enumerate(groups)]   
        return ''.join(vars)


    @staticmethod
    def in_util_vars_flatten_unique_sorted(VARS_list: list[str] | list[list[str]], func: Callable, capitalize: bool = False) -> list[str]:
        """Return a flattened list of unique and sorted items without duplicates.

        Args:
            VARS_list(list[str] | list[list[str]]): The data to flatten, remove duplicates and sort.
            func(Callable): Function to turn variation names from VAR to PRE or POST or none based on the function provided.
            capitalize(bool): (default to: False) capitalize the variation's names if any are found.

        Returns:
            (list[str]): Return a flattened list of unique and sorted items without duplicates.
        """
        flatten: list = [item for sublist in VARS_list for item in sublist]
        result: list = []
        [result.append(x) for x in flatten if x not in result]
        sort: list = sorted(result, key=lambda var: var)
        if not capitalize:
            return [str(func(x)) for x in sort if x]
        else:
            return [str(func(x)).capitalize() for x in sort if x]
    
    
    @staticmethod
    def in_presets_in_isvalid_file_menu_label(node: hou.SopNode, preset_id: int) -> str:
        """The IN presets menu parameters are 2, one for when a flame preset is loaded and one when not
        plus when a it can also be that a preset from the clipboard has been loaded, introducing a new bookmark icon.
        Those need to be queried separately, this definition will query the currently visible one and account for the clipboard case as well.

        Args:
            node(hou.SopNode): This FLAM3H node
            preset_id(int): the menu preset selction index to use to retrive its menu label string

        Returns:
            (str): The selected menu preset menu label string
        """

        toggle_PREFS_ENUMERATE_MENU: int = node.parm(PREFS_ENUMERATE_MENU).eval()
        
        if node.parm(IN_PVT_ISVALID_PRESET).eval():
            
            if node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval():
                menu_label: str = str(node.parm(IN_PRESETS).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_FLAME_LOAD_CB)[-1].strip()
                # We are using "str.lstrip()" because the preset name has been "str.strip()" already in the above line.
                # and there are only the leading white spaces left from the menu enumaration index number string to remove.
                if toggle_PREFS_ENUMERATE_MENU: return ':'.join(str(menu_label).split(':')[1:]).lstrip()
                else: return menu_label
            else:
                menu_label: str = str(node.parm(IN_PRESETS).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_FLAME_LOAD)[-1].strip()
                # We are using "str.lstrip()" because the preset name has been "str.strip()" already in the above line.
                # and there are only the leading white spaces left from the menu enumaration index number string to remove.
                if toggle_PREFS_ENUMERATE_MENU: return ':'.join(str(menu_label).split(':')[1:]).lstrip()
                else: return menu_label
        else:
            menu_label: str = str(node.parm(IN_PRESETS_OFF).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_FLAME_LOAD_EMPTY)[-1].strip()
            # We are using "str.lstrip()" because the preset name has been "str.strip()" already in the above line.
            # and there are only the leading white spaces left from the menu enumaration index number string to remove.
            if toggle_PREFS_ENUMERATE_MENU: return ':'.join(str(menu_label).split(':')[1:]).lstrip()
            else: return menu_label
    
    
    @staticmethod
    def in_set_iter_on_load(node: hou.SopNode, preset_id: int, clipboard: bool, flame_name_clipboard: str) -> int:
        """When loading a FLame preset, set the FLAM3H iteration number
        to the value backed into the Flame preset name we just loaded.

        Args:
            node(hou.SopNode): FLAM3H houdini node
            preset_id(int): The Flame preset we loaded
            clipboard(bool): Are we loading from a file or from the clipboard ? This data is computed inside: def in_flame_utils.in_to_flam3h_init_data(self, node: hou.SopNode)
            flame_name_clipboard(str): If we are laoding from the clipboard, use this preset name instead

        Returns:
            (int): The iteration number to set. If none is found, use the default value of 64 to load this Flame preset.
        """
        iter_on_load: int = node.parm(IN_ITER_NUM_ON_LOAD).eval()
        use_iter_on_load: int = node.parm(IN_USE_ITER_ON_LOAD).eval()
        
        if clipboard: preset_name = flame_name_clipboard
        else:
            # Get the correct menu parameter's preset menu label
            preset_name: str = in_flame_utils.in_presets_in_isvalid_file_menu_label(node, preset_id)
        
        iter_on_load_preset: int | None = in_flame_utils.in_get_preset_name_iternum(preset_name)
        if iter_on_load_preset is not None:
            # override iterations from the Flame preset name
            if use_iter_on_load and node.parm(IN_OVERRIDE_ITER_FLAME_NAME).eval():
                return node.parm(IN_ITER_NUM_ON_LOAD).eval()
            else:
                node.setParms({IN_ITER_NUM_ON_LOAD: iter_on_load_preset}) # type: ignore
                node.setParms({IN_USE_ITER_ON_LOAD: 0}) # type: ignore
                return iter_on_load_preset
        else:
            if not use_iter_on_load:
                node.setParms({IN_ITER_NUM_ON_LOAD: FLAM3H_DEFAULT_IN_ITERATIONS_ON_LOAD}) # type: ignore
                return FLAM3H_DEFAULT_IN_ITERATIONS_ON_LOAD
            
        return iter_on_load 


    @staticmethod
    def in_load_sensor_stats_msg(preset_id: int, apo_data: in_flame_iter_data) -> str:
        """Collect and write a summuary of the loaded IN Flame file preset render properties.

        Args:
            preset_id(int): The loaded XML Flame preset id to gather the data from.
            apo_data(in_flame_iter_data): The XML Flame file data

        Returns:
            (str): A string to be used to set the IN Render properties data parameter message.
        """
        # spacers
        nl: str = "\n"
        nnl: str = "\n\n"
        
        na: str = 'n/a'
        
        size: str = f"{OUT_XML_FLAME_RESOLUTION.capitalize()}: {na}"
        if apo_data.out_size[preset_id]:
            size = f"{OUT_XML_FLAME_RESOLUTION.capitalize()}: {apo_data.out_size[preset_id]}"
            
        center: str = f"{OUT_XML_FLAME_CENTER.capitalize()}: {na}"
        if apo_data.out_center[preset_id]:
            center = f"{OUT_XML_FLAME_CENTER.capitalize()}: {apo_data.out_center[preset_id]}"
            
        rotate: str = f"{OUT_XML_FLAME_ROTATE.capitalize()}: {na}"
        if apo_data.out_rotate[preset_id]:
            rotate = f"{OUT_XML_FLAME_ROTATE.capitalize()}: {apo_data.out_rotate[preset_id]}"

        scale: str = f"{OUT_XML_FLAME_SCALE.capitalize()}: {na}"
        if apo_data.out_scale[preset_id]:
            scale = f"{OUT_XML_FLAME_SCALE.capitalize()}: {apo_data.out_scale[preset_id]}"
        
        build: tuple = (size, nl,
                        center, nl,
                        rotate, nl,
                        scale, nl,
                        )
        
        return "".join(build)

    
    @staticmethod
    def in_load_render_stats_msg(preset_id: int, apo_data: in_flame_iter_data) -> str:
        """Collect and write a summuary of the loaded IN Flame file preset render properties.

        Args:
            preset_id(int): The loaded XML Flame preset id to gather the data from.
            apo_data(in_flame_iter_data): The XML Flame file data

        Returns:
            (str): A string to be used to set the IN Render properties data parameter message.
        """
        # spacers
        nl: str = "\n"
        nnl: str = "\n\n"
        na: str = 'n/a'
        
        quality: str = f"{OUT_XML_FLAME_QUALITY.capitalize()}: {na}"
        if apo_data.out_quality[preset_id]:
            quality = f"{OUT_XML_FLAME_QUALITY.capitalize()}: {apo_data.out_quality[preset_id]}"

        brightness: str = f"{OUT_XML_FLAME_BRIGHTNESS.capitalize()}: {na}"
        if apo_data.out_brightness[preset_id]:
            brightness = f"{OUT_XML_FLAME_BRIGHTNESS.capitalize()}: {apo_data.out_brightness[preset_id]}"
            
        gamma: str = f"{OUT_XML_FLAME_GAMMA.capitalize()}: {na}"
        if apo_data.out_gamma[preset_id]:
            gamma = f"{OUT_XML_FLAME_GAMMA.capitalize()}: {apo_data.out_gamma[preset_id]}"
            
        highlight: str = f"{' '.join(OUT_XML_FLAME_POWER.split('_')).capitalize()}: {na}"
        if apo_data.out_highlight_power[preset_id]:
            highlight = f"{' '.join(OUT_XML_FLAME_POWER.split('_')).capitalize()}: {apo_data.out_highlight_power[preset_id]}"
            
        log_k2: str = f"{' '.join(OUT_XML_FLAME_K2.split('_')).capitalize()}: {na}"
        if apo_data._out_logscale_k2[preset_id]:
            log_k2 = f"{' '.join(OUT_XML_FLAME_K2.split('_')).capitalize()}: {apo_data._out_logscale_k2[preset_id]}"
            
        vibrancy: str = f"{OUT_XML_FLAME_VIBRANCY.capitalize()}: {na}"
        if apo_data.out_vibrancy[preset_id]:
            vibrancy = f"{OUT_XML_FLAME_VIBRANCY.capitalize()}: {apo_data.out_vibrancy[preset_id]}"
        
        cc_curves: list = []
        if apo_data.out_curve_overall[preset_id] and apo_data.out_curve_overall[preset_id] not in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL: cc_curves.append('Overall')
        if apo_data.out_curve_red[preset_id] and apo_data.out_curve_red[preset_id] not in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL: cc_curves.append('Red')
        if apo_data.out_curve_green[preset_id] and apo_data.out_curve_green[preset_id] not in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL: cc_curves.append('Green')
        if apo_data.out_curve_blue[preset_id] and apo_data.out_curve_blue[preset_id] not in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL: cc_curves.append('Blue')
        if not cc_curves: cc = f"COLOR CORRECTION: Default (OFF)\nThe loaded preset CC Curves are default values."
        else: cc = f"COLOR CORRECTION:\n{', '.join(cc_curves)}"
        
        build: tuple = (quality, nl,
                        brightness, nl,
                        gamma, nl,
                        highlight, nl,
                        log_k2, nl,
                        vibrancy, nnl,
                        cc
                        )
        
        return "".join(build)
    
    
    @staticmethod
    def in_copy_sensor(node: hou.SopNode, f3r: in_flame_iter_data, preset_id: int) -> None:
        """Copy the loaded IN Flame preset sensor XML data into the FLAM3H OUT sensor data.

        Args:
            node(hou.SopNode): FLAM3H node.
            f3r(in_flame_iter_data): The XML Flame file data to get the loaded preset data from.
            preset_id(int): the preset index we are loading 
            
        Returns:
            (None):
        """  
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE): hou.Vector2((int(f3r.out_size[preset_id].split()[0]), int(f3r.out_size[preset_id].split()[1])))}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE): hou.Vector2((int(1024), int(1024)))}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_SIZE} -> NOT FOUND, default value used.\n")
            
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER): hou.Vector2((float(f3r.out_center[preset_id].split()[0]), float(f3r.out_center[preset_id].split()[1])))}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER): hou.Vector2((float(0), float(0)))}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_CENTER} -> NOT FOUND, default value used.\n")
            
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE): float(f3r.out_rotate[preset_id])}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE): float(0)}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_ROTATE} -> NOT FOUND, default value used.\n")
            
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE): float(f3r.out_scale[preset_id])}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE): float(400)}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_SCALE} -> NOT FOUND, default value used.\n")
    
    
    @staticmethod
    def in_copy_render(node: hou.SopNode, f3r: in_flame_iter_data, preset_id: int) -> None:
        """Copy the loaded IN Flame preset render XML data into the FLAM3H OUT render data.

        Args:
            node(hou.SopNode): FLAM3H node.
            f3r(in_flame_iter_data): The XML Flame file data to get the loaded preset data from.
            preset_id(int): the preset index we are loading 
            
        Returns:
            (None):
        """  
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY): int(f3r.out_quality[preset_id])}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY): int(1000)}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_QUALITY} -> NOT FOUND, default value used.\n")
            
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS): float(f3r.out_brightness[preset_id])}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS): float(3)}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_BRIGHTNESS} -> NOT FOUND, default value used.\n")
            
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA): float(f3r.out_gamma[preset_id])}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA): float(2.5)}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_GAMMA} -> NOT FOUND, default value used.\n")
            
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER): float(f3r.out_highlight_power[preset_id])}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER): float(5.0)}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_POWER} -> NOT FOUND, default value used.\n")
            
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2): float(f3r._out_logscale_k2[preset_id])}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2): float(0)}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_K2} -> NOT FOUND, default value used.\n")
            
        try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY): float(f3r.out_vibrancy[preset_id])}) # type: ignore
        except: # If missing set it to its default
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY): float(0.3333)}) # type: ignore
            print(f"Warning:\nIN xml key: {OUT_XML_FLAME_VIBRANCY} -> NOT FOUND, default value used.\n")
    
    
    @staticmethod
    def in_copy_render_cc_curves(node: hou.SopNode, f3r: in_flame_iter_data, preset_id: int) -> None:
        """Copy the loaded IN Flame preset color correction XML data into the FLAM3H render color correction curves data.
        It will check if each is one of the defaults settings first. 

        Args:
            node(hou.SopNode): FLAM3H node.
            f3r(in_flame_iter_data): The XML Flame file data to get the loaded preset data from.
            preset_id(int): the preset index we are loading 
            
        Returns:
            (None):
        """     
        # render curves
        if f3r.out_curves[preset_id] in OUT_XML_FLAME_RENDER_CURVES_DEFAULT_ALL:
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVES): OUT_XML_FLAME_RENDER_CURVES_DEFAULT}) # type: ignore
        else:
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVES): f3r.out_curves[preset_id]}) # type: ignore
            except: # If missing set it to its default
                node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVES): OUT_XML_FLAME_RENDER_CURVES_DEFAULT}) # type: ignore
                # Not all third-party applications export these keys so we avoid printing as it can be annoying.
                # print(f"Warning:\nIN xml key: {OUT_XML_FLAME_RENDER_CURVES} -> NOT FOUND, default value used.\n")
                
        if f3r.out_curve_overall[preset_id] in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL:
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_OVERALL): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
        else:
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_OVERALL): f3r.out_curve_overall[preset_id]}) # type: ignore
            except: # If missing set it to its default
                node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_OVERALL): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
                # Not all third-party applications export these keys so we avoid printing as it can be annoying.
                # print(f"Warning:\nIN xml key: {OUT_XML_FLAME_RENDER_CURVE_OVERALL} -> NOT FOUND, default value used.\n")
                
        if f3r.out_curve_red[preset_id] in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL:
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_RED): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
        else:
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_RED): f3r.out_curve_red[preset_id]}) # type: ignore
            except: # If missing set it to its default
                node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_RED): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
                # Not all third-party applications export these keys so we avoid printing as it can be annoying.
                # print(f"Warning:\nIN xml key: {OUT_XML_FLAME_RENDER_CURVE_RED} -> NOT FOUND, default value used.\n")
                
        if f3r.out_curve_green[preset_id] in  OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL:
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_GREEN): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
        else:
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_GREEN): f3r.out_curve_green[preset_id]}) # type: ignore
            except: # If missing set it to its default
                node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_GREEN): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
                # Not all third-party applications export these keys so we avoid printing as it can be annoying.
                # print(f"Warning:\nIN xml key: {OUT_XML_FLAME_RENDER_CURVE_GREEN} -> NOT FOUND, default value used.\n")
                
        if f3r.out_curve_blue[preset_id] in  OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL:
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_BLUE): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
        else:
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_BLUE): f3r.out_curve_blue[preset_id]}) # type: ignore
            except: # If missing set it to its default
                node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_BLUE): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
                # Not all third-party applications export these keys so we avoid printing as it can be annoying.
                # print(f"Warning:\nIN xml key: {OUT_XML_FLAME_RENDER_CURVE_BLUE} -> NOT FOUND, default value used.\n")
    
    
    @staticmethod
    def in_copy_render_all_stats_msg(kwargs: dict,  apo_data: in_flame_iter_data | None = None, clipboard: bool = False, flash_message: bool = False) -> None:
        """Copy the loaded IN Flame preset ALL properties into the OUT Flame render properties to be written out. 

        Args:
            kwargs(hou.SopNode): houdini kwargs.
            apo_data(in_flame_iter_data | None): Default to None. All the XML data from the loaded Flame preset.
            clipboard(bool): True: load from clipboard. False: load from disk file ( load from the node stored data ).
            flash_message(bool): Default to False. If True it will fire a flash message.
            
        Returns:
            (None):
        """       
        node = kwargs['node']
        
        inisvalidpreset: int = node.parm(IN_PVT_ISVALID_PRESET).eval()
        
        # If "clipboard" is True mean the incoming Flame preset from the Clipboard has been checked/validated already
        # so no needs to double check here any more...just use it as is.
        if apo_data is not None and clipboard: f3r = apo_data
        else:
            # Otherwise just use the stored data
            data: str | None = node.userData(FLAM3H_USER_DATA_XML_LAST)
            if data is not None: f3r = in_flame_iter_data(node, data) # ELSE load from the stored data instead
            else: f3r = None
        # We are checking only for the XML Flame preset validity
        # becasue we want to copy the data when loading from the clipboard
        # Hence we skip the checking of the toggles
        if f3r is not None and f3r.isvalidtree:
            
            # sensor data
            in_flame_utils.in_copy_sensor(node, f3r, 0)
            # render data
            in_flame_utils.in_copy_render(node, f3r, 0)
            # render curves data
            in_flame_utils.in_copy_render_cc_curves(node, f3r, 0)
            
            # OUT render curves ui parm set
            out_flame_utils.out_render_curves_retrive_data(node)
            # Check if the CC curves are at their default values or not and set the toggle
            # I could have done this inside the above: in_flame_utils.in_copy_render_cc_curves(node, f3r, preset_id)
            # but since this one is run also from a callback script, i'm doing the checks twice anyway
            out_flame_utils.out_render_curves_compare_and_set_toggle(node)
            
            # Set folder heading
            if clipboard:
                node.setParms({MSG_IN_STATS_HEADING: f"{MSG_IN_STATS_HEADING_DEFAULT} {IN_CLIPBOARD_LABEL_MSG}"}) # type: ignore
                node.setParms({MSG_IN_SETTINGS_HEADING: f"{MSG_IN_SETTINGS_HEADING_DEFAULT} {IN_CLIPBOARD_LABEL_MSG}"}) # type: ignore
            else:
                node.setParms({MSG_IN_STATS_HEADING: f"{MSG_IN_STATS_HEADING_DEFAULT}"}) # type: ignore
                node.setParms({MSG_IN_SETTINGS_HEADING: f"{MSG_IN_SETTINGS_HEADING_DEFAULT}"}) # type: ignore
            
            node.setParms({OUT_RENDER_PROPERTIES_EDIT: 1}) # type: ignore
            
            if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                flam3h_general_utils(kwargs).util_set_clipping_viewers()
                flam3h_general_utils(kwargs).util_set_front_viewer()
            
            if clipboard: _MSG: str = f"IN ALL settings Clipboard: COPIED"
            else: _MSG: str = f"IN ALL settings: COPIED"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
            if flash_message: flam3h_general_utils.flash_message(node, _MSG)
            
        else:
            # The actual toggle is needed here
            clipboard = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()
            if inisvalidpreset and not clipboard:
                _MSG: str = f"IN: Data corrupted"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}.", 'WARN')
                flam3h_general_utils.flash_message(node, _MSG)
            elif inisvalidpreset and clipboard:
                _MSG: str = f"IN Clipboard: Data corrupted"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}.", 'WARN')
                flam3h_general_utils.flash_message(node, _MSG)


    @staticmethod
    def in_copy_sensor_stats_msg(kwargs: dict) -> None:
        """Copy the loaded IN Flame preset SENSOR properties into the OUT Flame render properties to be written out. 

        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """
        node = kwargs['node']
        
        inisvalidpreset: int = node.parm(IN_PVT_ISVALID_PRESET).eval()
        clipboard: int = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()

        # Here we are checking those toggles
        # because when a Flame preset has been loaded already and we want to make sure it is still valid
        if inisvalidpreset or clipboard:
            
            data: str | None = node.userData(FLAM3H_USER_DATA_XML_LAST)
            if data is not None: f3r: in_flame_iter_data | None = in_flame_iter_data(node, data)
            else: f3r: in_flame_iter_data | None = None
            if f3r is not None and f3r.isvalidtree:
            
                # sensor data
                in_flame_utils.in_copy_sensor(node, f3r, 0)
                
                node.setParms({OUT_RENDER_PROPERTIES_EDIT: 1}) # type: ignore
                
                if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                    flam3h_general_utils(kwargs).util_set_clipping_viewers()
                    flam3h_general_utils(kwargs).util_set_front_viewer()
                    
                _MSG: str = f"IN SENSOR settings: COPIED"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                flam3h_general_utils.flash_message(node, _MSG)
                
            else:
                if inisvalidpreset and not clipboard:
                    _MSG: str = f"IN: Data corrupted"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}.", 'WARN')
                    flam3h_general_utils.flash_message(node, _MSG)
                elif inisvalidpreset and clipboard:
                    _MSG: str = f"IN Clipboard: Data corrupted"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}.", 'WARN')
                    flam3h_general_utils.flash_message(node, _MSG)
            
        else:
            _MSG: str = f"Load a valid IN Preset first"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
            flam3h_general_utils.flash_message(node, _MSG)
        

    @staticmethod
    def in_copy_render_stats_msg(kwargs: dict) -> None:
        """Copy the loaded IN Flame preset RENDER properties into the OUT Flame render properties to be written out. 

        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """
        node = kwargs['node']
        
        inisvalidpreset: int = node.parm(IN_PVT_ISVALID_PRESET).eval()
        clipboard: int = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()
        
        # Here we are checking those toggles
        # because the a Flame preset has been loaded already and we want to make sure it is still valid
        if inisvalidpreset or clipboard:
            
            data: str | None = node.userData(FLAM3H_USER_DATA_XML_LAST)
            if data is not None: f3r: in_flame_iter_data | None = in_flame_iter_data(node, data) # ELSE load from the stored data instead
            else: f3r: in_flame_iter_data | None = None
            if f3r is not None and f3r.isvalidtree:
                
                # render data
                in_flame_utils.in_copy_render(node, f3r, 0)
                # render curves data
                in_flame_utils.in_copy_render_cc_curves(node, f3r, 0)

                # OUT render curves ui parm set
                out_flame_utils.out_render_curves_retrive_data(node)
                # Check if the CC curves are at their default values or not and set the toggle
                # I could have done this inside the above: in_flame_utils.in_copy_render_cc_curves(node, f3r, preset_id)
                # but since this one is run also from a callback script, i'm doing the checks twice anyway
                out_flame_utils.out_render_curves_compare_and_set_toggle(node)
                
                node.setParms({OUT_RENDER_PROPERTIES_EDIT: 1}) # type: ignore
                
                # This is not needed for just the RENDER properties, but it casue no harm, so...
                if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                    flam3h_general_utils(kwargs).util_set_clipping_viewers()
                    flam3h_general_utils(kwargs).util_set_front_viewer()
                    
                _MSG: str = f"IN RENDER settings: COPIED"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                flam3h_general_utils.flash_message(node, _MSG)
                
            else:
                if inisvalidpreset and not clipboard:
                    _MSG: str = f"IN: Data corrupted"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}.", 'WARN')
                    flam3h_general_utils.flash_message(node, _MSG)
                elif inisvalidpreset and clipboard:
                    _MSG: str = f"IN Clipboard: Data corrupted"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}.", 'WARN')
                    flam3h_general_utils.flash_message(node, _MSG)
            
        else:
            _MSG: str = f"Load a valid IN Preset first"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
            flam3h_general_utils.flash_message(node, _MSG)
            
            
    @staticmethod
    def in_copy_cc_curves_stats_msg(kwargs: dict) -> None:
        """Copy the loaded IN Flame preset CC CURVES data into the OUT Flame render color correction curves properties to be written out. 

        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """
        node = kwargs['node']

        inisvalidpreset: int = node.parm(IN_PVT_ISVALID_PRESET).eval()
        clipboard: int = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()
        
        # Here we are checking those toggles
        # because the a Flame preset has been loaded already and we want to make sure it is still valid
        if inisvalidpreset or clipboard:
            
            data: str | None = node.userData(FLAM3H_USER_DATA_XML_LAST)
            if data is not None: f3r: in_flame_iter_data | None = in_flame_iter_data(node, data)
            else: f3r: in_flame_iter_data | None = None
            if f3r is not None and f3r.isvalidtree:
                
                # render curves data
                in_flame_utils.in_copy_render_cc_curves(node, f3r, 0)
                
                cc_o: str = node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_OVERALL)).eval()
                cc_r: str = node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_RED)).eval()
                cc_g: str = node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_GREEN)).eval()
                cc_b: str = node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_BLUE)).eval()
                if cc_o.strip() in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL and cc_r.strip() in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL and cc_g.strip() in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL and cc_b.strip() in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL:
                    node.setParms({OUT_LABEL_CC_DEFAULTS_MSG: 'Defaults'})
                    node.setParms({OUT_TOGGLE_CC_DEFAULTS_MSG: 0})
                    _MSG: str = f"IN CC Curves:"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG} the loaded IN Flame preset CC Curves are default values. COPY SKIPPED", 'IMP')
                    flam3h_general_utils.flash_message(node, f"{_MSG} Defaults. COPY SKIPPED")
                else:
                    # OUT render curves ui parm set
                    out_flame_utils.out_render_curves_retrive_data(node)
                    # Check if the CC curves are at their default values or not and set the toggle
                    # I could have done this inside the above: in_flame_utils.in_copy_render_cc_curves(node, f3r, preset_id)
                    # but since this one is run also from a callback script, i'm doing the checks twice anyway
                    out_flame_utils.out_render_curves_compare_and_set_toggle(node)
                    
                    # menu_label = in_flame_utils.in_presets_in_isvalid_file_menu_label(node, 0)
                    _MSG: str = f"IN CC Curves: COPIED"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG} from the IN Flame preset: {out_flame_utils.out_remove_iter_num(f3r.name[0])}", 'IMP')
                    flam3h_general_utils.flash_message(node, _MSG)
                    
            else:
                if inisvalidpreset and not clipboard:
                    _MSG: str = f"IN: Data corrupted"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}.", 'WARN')
                    flam3h_general_utils.flash_message(node, _MSG)
                elif inisvalidpreset and clipboard:
                    _MSG: str = f"IN Clipboard: Data corrupted"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}.", 'WARN')
                    flam3h_general_utils.flash_message(node, _MSG)
            
        else:
            _MSG: str = f"Load a valid IN Preset first"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG} to copy color correction curves data from.", 'WARN')
            flam3h_general_utils.flash_message(node, _MSG)


    @staticmethod
    def in_util_vars_dict_type_maker(vars_dict: dict, func: Callable) -> dict:
        """Convert a dictionary of variation names into either PRE, VAR or POST variations names in one go.
        This is used mainly with this dictionary: VARS_FRACTORIUM_DICT 

        Args:
            vars_dict(dict): The dictionary to convert.
            func(Callable):  The function to conert the variation name. Can be any of: in_flame_utils.in_util_make_PRE, in_flame_utils.in_util_make_VAR, in_flame_utils.in_util_make_POST, in_flame_utils.in_util_make_NULL
            
        Returns:
            (dict): A new dictionary equal to the one passed in but with all variation names converted based on the passed Callable func.
        """   
        return dict(map(lambda item: (item[0], func(item[1])), vars_dict.items()))


    @staticmethod
    def in_xml_key_val(xform: dict, key_name: str, default_val: float = 0) -> float:
        """Check for the queried XML key name value if it is an actual value.
        if not will return a default value instead.

        Args:
            xform(dict): The current xform dictionary.
            key_name(str):  The XMK key name to querie
            default_val(float): If anything goes wrong, return this value instead
            
        Returns:
            (float): Either the queried key name value or a default value.
        """   
        key_val: str | None = xform.get(key_name)
        assert key_val is not None # I can assert this becasue the passed key_name has been collected already from an xform
        try:
            float(key_val)
        except ValueError:
            clean = [letter for letter in key_val if letter in CHARACTERS_ALLOWED_XFORM_VAL]
            new_val: str = ''.join(clean)
            try:
                float(new_val)
            except ValueError:
                if key_name is not None: print(f"Warning:\nIN xml key: {key_name} -> NOT A VALUE\n")
                return default_val
            else:
                if key_name is not None: print(f"Warning:\nIN xml key: {key_name} -> NOT A VALUE (Corrected)\n")
                return float(new_val)
        else:
            return float(key_val)


    @staticmethod
    def menu_in_presets_loop(node: hou.SopNode, menu: list, i: int, item: str, in_idx: int, is_clipboard: int) -> None:
        """This is spcifically to be run inside a list comprehension.

        Args:
            node(hou.SopNode): This FLAM3H node.
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.
            in_idx(int): The currently selected IN preset index.
            is_clipboard(int): IN Clipboard toggle.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            
            # 5 ending \s to be able to read the full label
            labels: tuple = (f"{FLAM3H_ICON_STAR_FLAME_LOAD}  {item}     ", 
                             f"{FLAM3H_ICON_STAR_FLAME_LOAD_CB}  {IN_CLIPBOARD_LABEL_MSG} {item}     ")
            # ICON bookmarks
            #
            # If a flame preset from a file is loaded
            if i == in_idx:
                node.setCachedUserData('in_presets_menu_idx', str(i))
                menu.append(labels[is_clipboard])
                
            else:
                menu.append(f"{item}")
            
            
    @staticmethod
    def menu_in_presets_loop_enum(node: hou.SopNode, menu: list, i: int, item: str, in_idx: int, is_clipboard: int) -> None:
        """This is spcifically to be run inside a list comprehension.

        Args:
            node(hou.SopNode): This FLAM3H node.
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.
            in_idx(int): The currently selected IN preset index.
            is_clipboard(int): IN Clipboard toggle.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            enum_label: str = str(i + 1) # start count from 1
            
            # 5 ending \s to be able to read the full label
            labels: tuple = (f"{FLAM3H_ICON_STAR_FLAME_LOAD}  {enum_label}:  {item}     ", 
                             f"{FLAM3H_ICON_STAR_FLAME_LOAD_CB}  {enum_label}:  {IN_CLIPBOARD_LABEL_MSG} {item}     ")
            # ICON bookmarks
            #
            # If a flame preset from a file is loaded
            if i == in_idx:
                node.setCachedUserData('in_presets_menu_idx', str(i))
                menu.append(labels[is_clipboard])
                
            else:
                menu.append(f"{enum_label}:  {item}")
            
            
    @staticmethod
    def menu_in_presets_empty_loop(node: hou.SopNode, menu: list, i: int, item: str) -> None:
        """This is spcifically to be run inside a list comprehension.

        Args:
            node(hou.SopNode): This FLAM3H node.
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            
            in_idx: int = int(node.parm(IN_PRESETS_OFF).eval())
            clipboard: int = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()
            # ICON bookmarks
            #
            # If a flame preset from a file is loaded
            if i == in_idx and not clipboard:
                node.setCachedUserData('in_presets_menu_off_idx', str(i))
                menu.append(f"{FLAM3H_ICON_STAR_FLAME_LOAD_EMPTY}  {item}     ") # 5 ending \s to be able to read the full label

            else:
                menu.append(f"{item}")
            
            
    @staticmethod
    def menu_in_presets_empty_loop_enum(node: hou.SopNode, menu: list, i: int, item: str) -> None:
        """This is spcifically to be run inside a list comprehension.

        Args:
            node(hou.SopNode): This FLAM3H node.
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            enum_label: str = str(i + 1) # start count from 1
            
            in_idx: int = int(node.parm(IN_PRESETS_OFF).eval())
            clipboard: int = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()
            # ICON bookmarks
            #
            # If a flame preset from a file is loaded
            if i == in_idx and not clipboard:
                node.setCachedUserData('in_presets_menu_off_idx', str(i))
                menu.append(f"{FLAM3H_ICON_STAR_FLAME_LOAD_EMPTY}  {enum_label}:  {item}     ") # 5 ending \s to be able to read the full label

            else:
                menu.append(f"{enum_label}:  {item}")


    # CLASS: PROPERTIES
    ##########################################
    ##########################################


    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node


    def in_copy_section_render_stats_msg(self) -> None:
        """Copy either the SENSOR or the RENDER settings from the loaded flame preset
        into the OUT tab properties.

        Args:
            (self):
            
        Returns:
            (None):
        """
        kwargs: dict = self.kwargs
        if kwargs["ctrl"]:
            self.in_copy_render_stats_msg(kwargs)
        else:
            self.in_copy_sensor_stats_msg(kwargs)
    
    
    def in_flam3h_set_iterators(self, 
                                mode: int, 
                                node: hou.SopNode, 
                                apo_data: in_flame_iter_data, 
                                preset_id: int, 
                                ) -> None:
        """Set the FLAM3H iterators/FF parameters based on collected XML data from the flame file loaded.
        
    The collection of XML data happen inside: class: in_flame_iter_data()

        Args:
            (self):
            mode(int): iterator or FF
            node(hou.SopNode): FLAM3H node
            apo_data(in_flame_iter_data): Flames data from the flame file loaded in: class: in_flame_iter_data()
            preset_id(int): the flame preset we are loading out of all the presets included in the flame file
            exclude_keys(tuple): exclude those keys inside the current xform/iterator from the search to speed up a little
            
        Returns:
            (None):
        """ 
        
        # timenow = datetime.now().strftime('%b-%d-%Y %H:%M:%S')
        
        # I could hard-code the name into the function: def in_vars_keys_remove_pgb(...), but this way I keep this dict global for all purposes.
        pgb_name: str | list[str] | None = self.in_util_make_PRE(self.in_get_dict_key_from_value(VARS_FLAM3_DICT_IDX, 33))
        assert isinstance(pgb_name, str)
        
        xforms, _MAX_VARS_MODE = self.in_get_xforms_data_and_flam3h_vars_limit(mode, apo_data)
        
        __EXCLUDE__: tuple = copy(XML_XF_KEY_EXCLUDE)
        vars_keys: list | None = self.in_get_xforms_var_keys(xforms, VARS_FLAM3_DICT_IDX.keys(), __EXCLUDE__)
        if vars_keys is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys for item in sublist])
        assert vars_keys is not None # This can be asserted because this definition is run after this Flame preset has been checked for its validity.
        vars_keys_pre_pgb: list | None = self.in_get_xforms_var_keys(xforms, self.in_util_make_PRE(VARS_FLAM3_DICT_IDX.keys()), __EXCLUDE__)
        vars_keys_pre: list | None = self.in_vars_keys_remove_pgb(vars_keys_pre_pgb, pgb_name)
        if vars_keys_pre is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys_pre for item in sublist])
        assert vars_keys_pre is not None # This can be asserted because this definition is run after this Flame preset has been checked for its validity.
        vars_keys_post: list | None = self.in_get_xforms_var_keys(xforms, self.in_util_make_POST(VARS_FLAM3_DICT_IDX.keys()), __EXCLUDE__)
        assert vars_keys_post is not None # This can be asserted because this definition is run after this Flame preset has been checked for its validity.
        
        app: str = apo_data.sw_version[preset_id]
        var_prm: tuple = flam3h_varsPRM().varsPRM
        apo_prm: tuple = flam3h_varsPRM_APO().varsPRM
        n: flam3h_iterator_prm_names = flam3h_iterator_prm_names()
        prx, prx_prm = self.in_util_flam3h_prx_mode(mode)
        
        # Set variations ( iterator and FF )
        for mp_idx, xform in enumerate(xforms):
            
            iterator_vars_skipped: list = []
            FF_vars_skipped: list = []
            
            # Collect iterator or FF vars in excess  
            if len(vars_keys[mp_idx]) > _MAX_VARS_MODE:
                if mode: FF_vars_skipped.append(f"\n\t\tFF VAR -> {', '.join(vars_keys[mp_idx][_MAX_VARS_MODE:])}")
                else: iterator_vars_skipped.append(f"\n\t\tVAR -> {', '.join(vars_keys[mp_idx][_MAX_VARS_MODE:])}")
            
            # in case of an iterator only the first 4. In case of an FF only the first 2
            for t_idx, key_name in enumerate(vars_keys[mp_idx][:_MAX_VARS_MODE]):
                v_type: int | None = self.in_get_idx_by_key(key_name)
                if v_type is not None:
                    v_weight: float = self.in_xml_key_val(xform, key_name)
                    if apo_prm[v_type][-1]:
                        self.in_v_parametric(app, 
                                             mode, 
                                             node, 
                                             mp_idx, 
                                             t_idx, 
                                             xform, 
                                             v_type, 
                                             v_weight, 
                                             var_prm[v_type], 
                                             apo_prm[v_type]
                                             )
                    else:
                        self.in_v_generic(mode, node, mp_idx, t_idx, v_type, v_weight)
                else:
                    # if this variation is not found, set it to Linear and its weight to ZERO
                    # Note that if the missing variation will is int the first slot inside any of the available types (PRE, VAR or POST)
                    # it will be set to its respective default value becasue the multi param parameters are reverted baco to their defaults on Flame load.
                    self.in_v_generic(mode, node, mp_idx, t_idx, 0, 0)
                    
            # Set pre blur if found
            assert apo_data.pre_blur is not None
            self.in_v_pre_blur(mode, node, mp_idx, apo_data.pre_blur)
                    
            if mode:
                assert apo_data.finalxform_name is not None
                # Set finalxform name first if any
                if apo_data.finalxform_name[0]:
                    node.setParms({f"{prx}{n.main_note}": apo_data.finalxform_name[0]}) # type: ignore
                    
                # Collect FF PRE vars in excess  
                if len(vars_keys_pre[mp_idx]) > MAX_FF_VARS_PRE:
                    if FF_vars_skipped: FF_vars_skipped.insert(0, f"\n\t\tFF PRE -> {', '.join(vars_keys_pre[mp_idx][MAX_FF_VARS_PRE:])}")
                    else: FF_vars_skipped.append(f"\n\t\tFF PRE -> {', '.join(vars_keys_pre[mp_idx][MAX_FF_VARS_PRE:])}")
                    
                # FF PRE vars ( only the first one in "vars_keys_pre[mp_idx]" will be kept )
                if vars_keys_pre[mp_idx]: # type: ignore
                    for t_idx, key_name in enumerate(vars_keys_pre[mp_idx][:MAX_FF_VARS_PRE]):
                        v_type: int | None = self.in_get_idx_by_key(self.in_util_make_VAR(key_name)) # type: ignore
                        if v_type is not None:
                            w: float = self.in_xml_key_val(xform, key_name)
                            v_weight: float = self.in_util_check_negative_weight(node, w, v_type, mode, mp_idx, self.in_util_make_PRE) # type: ignore
                            if apo_prm[v_type][-1]:
                                self.in_v_parametric_PRE_FF(app, 
                                                            node, 
                                                            t_idx, 
                                                            xform, 
                                                            v_type, 
                                                            v_weight, 
                                                            var_prm[v_type], 
                                                            apo_prm[v_type]
                                                            )
                            else: self.in_v_generic_PRE_FF(node, t_idx, v_type, v_weight)
                         
                # Collect FF POST vars in excess       
                if len(vars_keys_post[mp_idx]) > MAX_FF_VARS_POST:
                    FF_vars_skipped.append(f"\n\t\tFF POST -> {', '.join(vars_keys_post[mp_idx][MAX_FF_VARS_POST:])}")
                
                # FF POST vars ( only the first two in "vars_keys_post[mp_idx]" will be kept )
                if vars_keys_post[mp_idx]: # type: ignore
                    for t_idx, key_name in enumerate(vars_keys_post[mp_idx][:MAX_FF_VARS_POST]):
                        v_type: int | None = self.in_get_idx_by_key(self.in_util_make_VAR(key_name)) # type: ignore
                        if v_type is not None:
                            w: float = self.in_xml_key_val(xform, key_name)
                            v_weight: float = self.in_util_check_negative_weight(node, w, v_type, mode, mp_idx, self.in_util_make_POST) # type: ignore
                            if apo_prm[v_type][-1]:
                                self.in_v_parametric_POST_FF(app, 
                                                             node, 
                                                             t_idx, 
                                                             xform, 
                                                             v_type, 
                                                             v_weight, 
                                                             var_prm[v_type], 
                                                             apo_prm[v_type]
                                                             )
                            else: self.in_v_generic_POST_FF(node, t_idx, v_type, v_weight)
                
                # Print all skipped FF vars if any
                if FF_vars_skipped:
                    build: str = f"Warning:\n{self.node}.FF\n\tThe following variations are in excess and skipped:{''.join(FF_vars_skipped)}\n"
                    print(build)
                
            else:
                
                # Collect iterator PRE vars in excess
                if len(vars_keys_pre[mp_idx]) > MAX_ITER_VARS_PRE:
                    if iterator_vars_skipped:
                        iterator_vars_skipped.insert(0, f"\n\t\tPRE -> {', '.join(vars_keys_pre[mp_idx][MAX_ITER_VARS_PRE:])}")
                    else:
                        iterator_vars_skipped.append(f"\n\t\tPRE -> {', '.join(vars_keys_pre[mp_idx][MAX_ITER_VARS_PRE:])}")

                # PRE vars in this iterator ( only the first two in "vars_keys_pre[mp_idx]" will be kept )
                if vars_keys_pre[mp_idx]: # type: ignore
                    for t_idx, key_name in enumerate(vars_keys_pre[mp_idx][:MAX_ITER_VARS_PRE]):
                        
                        v_type: int | None = self.in_get_idx_by_key(self.in_util_make_VAR(key_name)) # type: ignore
                        if v_type is not None:
                            w: float = self.in_xml_key_val(xform, key_name)
                            v_weight: float = self.in_util_check_negative_weight(node, w, v_type, mode, mp_idx, self.in_util_make_PRE) # type: ignore
                            if apo_prm[v_type][-1]:
                                self.in_v_parametric_PRE(app, 
                                                         mode, 
                                                         node, 
                                                         mp_idx, 
                                                         t_idx, 
                                                         xform, 
                                                         v_type, 
                                                         v_weight, 
                                                         var_prm[v_type], 
                                                         apo_prm[v_type]
                                                         )
                            else: self.in_v_generic_PRE(mode, node, mp_idx, t_idx, v_type, v_weight)
                
                # Collect iterator POST vars in excess
                if len(vars_keys_post[mp_idx]) > MAX_ITER_VARS_POST:
                    iterator_vars_skipped.append(f"\n\t\tPOST -> {', '.join(vars_keys_post[mp_idx][MAX_ITER_VARS_POST:])}")

                # POST vars in this iterator ( only the first one in "vars_keys_post[mp_idx]" will be kept )
                if vars_keys_post[mp_idx]: # type: ignore
                    for t_idx, key_name in enumerate(vars_keys_post[mp_idx][:MAX_ITER_VARS_POST]):
                        v_type: int | None = self.in_get_idx_by_key(self.in_util_make_VAR(key_name)) # type: ignore
                        if v_type is not None:
                            w: float = self.in_xml_key_val(xform, key_name)
                            v_weight: float = self.in_util_check_negative_weight(node, w, v_type, mode, mp_idx, self.in_util_make_POST) # type: ignore
                            if apo_prm[v_type][-1]:
                                self.in_v_parametric_POST(app, 
                                                          mode, 
                                                          node, 
                                                          mp_idx, 
                                                          t_idx, 
                                                          xform, 
                                                          v_type, 
                                                          v_weight, 
                                                          var_prm[v_type], 
                                                          apo_prm[v_type]
                                                          )
                            else: self.in_v_generic_POST(mode, node, mp_idx, t_idx, v_type, v_weight)
                       
                # Print all skipped iterators vars if any
                if iterator_vars_skipped:
                    build: str = f"Warning:\n{self.node}.iterator.{mp_idx + 1}\n\tThe following variations are in excess and skipped:{''.join(iterator_vars_skipped)}\n"
                    print(build)
                                
                # Activate iterator
                node.setParms({f"{n.main_vactive}_{str(mp_idx + 1)}": 1}) # type: ignore
                # Set the rest of the iterator(FLAME or FF) parameters
                apo_data_set: dict[str, tuple | None] = {n.main_note: apo_data.xf_name, 
                                                         n.main_weight: apo_data.weight,
                                                         n.xaos: apo_data.xaos,
                                                         n.shader_color: apo_data.color,
                                                         n.shader_speed: apo_data.symmetry,
                                                         n.shader_alpha: apo_data.opacity
                                                         }
                [self.in_set_data(mode, node, prx, value, key, mp_idx) for key, value in apo_data_set.items()]
            
            # Set Affine ( PRE, POST and F3H_PRE, F3H_POST) for this iterator or FF
            self.in_set_affine(mode, node, prx, apo_data, n, mp_idx)
            

    def in_load_stats_msg(self, preset_id: int, apo_data: in_flame_iter_data, clipboard: bool) -> str:
        """Build a message with all the informations about the Flame preset we just loaded.

        Args:
            (self):
            preset_id(int): The loaded XML Flame preset
            apo_data(in_flame_iter_data): The XML Flame file data to get the loaded preset data from.
            clipboard(bool): Is the cuurently loaded Flame preset coming from the Clipboard? True or False.

        Returns:
            (str): A string to be used to set the IN Flame info data parameter message.
        """     
        
        node = self.node  
        # spacers
        nl: str = "\n"
        nnl: str = "\n\n"
        
        # I could hard-code the name into the function: def in_vars_keys_remove_pgb(...), but this way I keep this dict global for all purposes.
        pgb_name: str | list[str] | None = self.in_util_make_PRE(self.in_get_dict_key_from_value(VARS_FLAM3_DICT_IDX, 33))
        assert isinstance(pgb_name, str)
        
        # checks
        pb_bool = opacity_bool = post_bool = xaos_bool = palette_bool = ff_bool = ff_post_bool = flam3h_mb_bool = False
        if apo_data.pre_blur is not None:
            for item in apo_data.pre_blur:
                if item:
                    pb_bool = True
                    break
        
        if apo_data.opacity is not None:
            if min(apo_data.opacity) == 0.0: opacity_bool = True
        if apo_data.post is not None: post_bool = True
        if apo_data.xaos is not None: xaos_bool = True
        if apo_data.palette is not None: palette_bool = True
        if apo_data.finalxform is not None: ff_bool = True
        if apo_data.finalxform_post is not None: ff_post_bool = True
        # custom to FLAM3H only
        if apo_data.mb_flam3h_fps is not False: flam3h_mb_bool = True
        
        # checks msgs
        opacity_bool_msg = post_bool_msg = xaos_bool_msg = ff_post_bool_msg = "NO"
        if opacity_bool: opacity_bool_msg = "YES"
        if post_bool: post_bool_msg = "YES"
        if xaos_bool: xaos_bool_msg = "YES"
        if ff_post_bool: ff_post_bool_msg = "YES"
        
        # build msgs
        sw: str = f"Software: {apo_data.sw_version[preset_id]}"
        name: str = f"Name: {apo_data.name[preset_id]}"
        assert apo_data.xforms is not None
        iter_count: str = f"Iterators count: {str(len(apo_data.xforms))}"
        post: str = f"Post affine: {post_bool_msg}"
        opacity: str = f"Opacity: {opacity_bool_msg}"
        xaos: str = f"Xaos: {xaos_bool_msg}"
        
        # CC - build data
        cc_overall: str | list = apo_data.out_curve_overall[preset_id]
        if not apo_data.out_curve_overall[preset_id]: cc_overall = OUT_XML_FLAME_RENDER_CURVE_DEFAULT
        cc_red: str | list = apo_data.out_curve_red[preset_id]
        if not apo_data.out_curve_red[preset_id]: cc_red = OUT_XML_FLAME_RENDER_CURVE_DEFAULT
        cc_green: str | list = apo_data.out_curve_green[preset_id]
        if not apo_data.out_curve_green[preset_id]: cc_green = OUT_XML_FLAME_RENDER_CURVE_DEFAULT
        cc_blue: str | list = apo_data.out_curve_blue[preset_id]
        if not apo_data.out_curve_green[preset_id]: cc_blue = OUT_XML_FLAME_RENDER_CURVE_DEFAULT
        # CC - check - The following are now guarantee to be of type: str
        assert isinstance(cc_overall, str)
        assert isinstance(cc_red, str)
        assert isinstance(cc_green, str)
        assert isinstance(cc_blue, str)
        # Compare
        if cc_overall.strip() in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL and cc_red.strip() in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL and cc_green.strip() in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL and cc_blue.strip() in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL:
            cc: str = ''
        else:
            cc: str = 'CC'
        
        # MB (Motion blur)
        if flam3h_mb_bool:
            if cc: mb: str = f", MB{nnl}" # not that elegant, but...
            else: mb: str = f"MB{nnl}"
        else: mb: str = nnl
        
        if ff_bool: ff_msg: str = f"FF: YES\nFF Post affine: {ff_post_bool_msg}"
        else: ff_msg: str = f"FF: NO\n"
        
        if palette_bool and apo_data.palette is not None:
            if apo_data.cp_flam3h_hsv is not False: palette_count_format = f"Palette count: {apo_data.palette[1]}, format: {apo_data.palette[2]} {IN_HSV_LABEL_MSG}" # custom to FLAM3H only
            else: palette_count_format: str = f"Palette count: {apo_data.palette[1]}, format: {apo_data.palette[2]}"
        else: palette_count_format: str = f"Palette not found."
        
        # ITERATOR COLLECT
        __EXCLUDE__: tuple = copy(XML_XF_KEY_EXCLUDE)
        vars_keys: list | None = self.in_get_xforms_var_keys(apo_data.xforms, VARS_FLAM3_DICT_IDX.keys(), __EXCLUDE__)
        if vars_keys is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys for item in sublist])
        vars_keys_PRE_pgb:list | None = self.in_get_xforms_var_keys(apo_data.xforms, self.in_util_make_PRE(VARS_FLAM3_DICT_IDX.keys()), __EXCLUDE__)
        vars_keys_PRE: list | None = self.in_vars_keys_remove_pgb(vars_keys_PRE_pgb, pgb_name)
        if vars_keys_PRE is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys_PRE for item in sublist])
        vars_keys_POST: list | None = self.in_get_xforms_var_keys(apo_data.xforms, self.in_util_make_POST(VARS_FLAM3_DICT_IDX.keys()), __EXCLUDE__)
        
        # FF COLLECT
        vars_keys_FF = vars_keys_PRE_FF = vars_keys_POST_FF = []
        if ff_bool:
            __EXCLUDE__ = copy(XML_XF_KEY_EXCLUDE)
            vars_keys_FF: list | None = self.in_get_xforms_var_keys(apo_data.finalxform, VARS_FLAM3_DICT_IDX.keys(), __EXCLUDE__)
            if vars_keys_FF is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys_FF for item in sublist])
            vars_keys_PRE_FF: list | None = self.in_get_xforms_var_keys(apo_data.finalxform, self.in_util_make_PRE(VARS_FLAM3_DICT_IDX.keys()), __EXCLUDE__)
            if vars_keys_PRE_FF is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys_PRE_FF for item in sublist])
            vars_keys_POST_FF: list | None = self.in_get_xforms_var_keys(apo_data.finalxform, self.in_util_make_POST(VARS_FLAM3_DICT_IDX.keys()), __EXCLUDE__)
        
        vars_all = vars_keys_PRE + vars_keys + vars_keys_POST + vars_keys_PRE_FF + vars_keys_FF + vars_keys_POST_FF # type: ignore
        if pb_bool: vars_all += [["pre_blur"]]
        result_sorted: list = self.in_util_vars_flatten_unique_sorted(vars_all, self.in_util_make_NULL, True) # type: ignore
        
        n: int = 5
        vars_used_heading: str = "Variations used:"
        result_grp: list = [result_sorted[i:i + n] for i in range(0, len(result_sorted), n)]  
        vars_used_msg: str = f"{vars_used_heading} {int(len(result_sorted))}\n{self.in_util_join_vars_grp(result_grp)}"
        
        # Build and set descriptive parameter msg
        if clipboard: preset_name: str = apo_data.name[0]
        else: preset_name: str = apo_data.name[preset_id]   # Get the correct menu parameter's preset menu label
                                                            # The apo_data.name[idx] is used for the descriptive parameter
                                                            # so to not print the icon path into the name.
        
        descriptive_prm: tuple = ( f"sw: {apo_data.sw_version[preset_id]}\n", f"{out_flame_utils.out_remove_iter_num(preset_name)}",)
        node.setParms({MSG_DESCRIPTIVE_PRM: "".join(descriptive_prm)}) # type: ignore
        
        # Build ITERATOR MISSING
        __EXCLUDE__ = copy(XML_XF_KEY_EXCLUDE)
        vars_keys_from_fractorium: list | None = self.in_get_xforms_var_keys(apo_data.xforms, VARS_FRACTORIUM_DICT, __EXCLUDE__)
        if vars_keys_from_fractorium is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys_from_fractorium for item in sublist])
        vars_keys_from_fractorium_pre_pgb: list | None = self.in_get_xforms_var_keys_PP(apo_data.xforms, VARS_FRACTORIUM_DICT_PRE, V_PRX_PRE, __EXCLUDE__)
        vars_keys_from_fractorium_pre: list | None = self.in_vars_keys_remove_pgb(vars_keys_from_fractorium_pre_pgb, pgb_name)
        if vars_keys_from_fractorium_pre is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys_from_fractorium_pre for item in sublist])
        vars_keys_from_fractorium_post: list | None = self.in_get_xforms_var_keys_PP(apo_data.xforms, VARS_FRACTORIUM_DICT_POST, V_PRX_POST, __EXCLUDE__)
        
        # BUILD FF MISSING
        vars_keys_from_fractorium_FF = vars_keys_from_fractorium_pre_FF = vars_keys_from_fractorium_post_FF = []
        if ff_bool:
            __EXCLUDE__ = copy(XML_XF_KEY_EXCLUDE)
            vars_keys_from_fractorium_FF: list | None = self.in_get_xforms_var_keys(apo_data.finalxform, VARS_FRACTORIUM_DICT, __EXCLUDE__)
            if vars_keys_from_fractorium_FF is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys_from_fractorium_FF for item in sublist])
            vars_keys_from_fractorium_pre_FF: list | None = self.in_get_xforms_var_keys_PP(apo_data.finalxform, VARS_FRACTORIUM_DICT_PRE, V_PRX_PRE, __EXCLUDE__)
            if vars_keys_from_fractorium_pre_FF is not None: __EXCLUDE__ += tuple([item for sublist in vars_keys_from_fractorium_pre_FF for item in sublist])
            vars_keys_from_fractorium_post_FF: list | None = self.in_get_xforms_var_keys_PP(apo_data.finalxform, VARS_FRACTORIUM_DICT_POST, V_PRX_POST, __EXCLUDE__)
        
        vars_keys_from_fractorium_all: list = vars_keys_from_fractorium + vars_keys_from_fractorium_pre + vars_keys_from_fractorium_post + vars_keys_from_fractorium_pre_FF + vars_keys_from_fractorium_FF + vars_keys_from_fractorium_post_FF # type: ignore
        result_sorted_fractorium: list = self.in_util_vars_flatten_unique_sorted(vars_keys_from_fractorium_all, self.in_util_make_NULL, True)
        
        # Build MISSING: Compare, keep and build
        vars_missing: list = [x for x in result_sorted_fractorium if x not in result_sorted]
        result_grp_fractorium: list = [vars_missing[i:i + n] for i in range(0, len(vars_missing), n)]  
        if vars_missing: vars_missing_msg = f"{nnl}MISSING:\n{self.in_util_join_vars_grp(result_grp_fractorium)}"
        else: vars_missing_msg: str = ""
        
        # Build UNKNOWN
        vars_unknown: list = in_flame_utils.in_load_stats_unknown_vars(preset_id, apo_data)
        if vars_unknown: vars_unknown_msg: str = f"{nnl}UNKNOWN:\n{self.in_util_join_vars_grp( [vars_unknown[i:i + n] for i in range(0, len(vars_unknown), n)] )}"
        else: vars_unknown_msg: str = ''
        
        # Check if the loaded Flame file is locked.
        in_path: str = os.path.expandvars(node.parm(IN_PATH).eval())
        in_path_checked: str | bool = out_flame_utils.out_check_outpath(node, in_path, OUT_FLAM3_FILE_EXT, AUTO_NAME_OUT)
        if flam3h_general_utils.isLOCK(in_path_checked): flame_lib_locked = MSG_FLAMESTATS_LOCK
        else: flame_lib_locked = ''
        
        # If the Flame use a 256+ palette, update the CP palette MSG
        if apo_data.palette is not None and apo_data.palette[1] > 256:
            palette_msg: str = node.parm(MSG_PALETTE).eval()
            if PALETTE_PLUS_MSG in palette_msg: pass
            else: node.setParms({MSG_PALETTE: f"{PALETTE_PLUS_MSG.strip()} {palette_msg.strip()}"})
        
        # build full stats msg
        build: tuple = (flame_lib_locked, nl,
                        sw, nl,
                        name, nnl,
                        palette_count_format, nl,
                        cc, mb,
                        iter_count, nl,
                        post, nl,
                        opacity, nl,
                        xaos, nl,
                        ff_msg, nnl,
                        vars_used_msg,
                        vars_missing_msg,
                        vars_unknown_msg )

        return "".join(build)


    def menu_in_presets_data(self) -> list:
        """Populate the IN menu parameters with entries based on the loaded IN XML Flame file.
        When a flame preset is loaded. This will use the blue star icon to signal wich preset is currently loaded.

        _NOTE:
            If you change the icon gobal variable name inside here,
            remember to updated with the same global variable names inside: in_flame_utils.in_presets_in_isvalid_file_menu_label(...)

        Args:
            (self):

        Returns:
            (list): the actual menu
        """
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            node = self.node
            xml: str = os.path.expandvars(node.parm(IN_PATH).eval())

            if _xml_tree(xml).isvalidtree and node.parm(IN_PVT_ISVALID_FILE).eval() and node.parm(IN_PVT_ISVALID_PRESET).eval():
                
                in_idx: int = int(node.parm(IN_PRESETS).eval())
                is_clipboard: int = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()
                
                menu: list = []
                [self.menu_in_presets_loop_enum(node, menu, i, item, in_idx, is_clipboard) if node.parm(PREFS_ENUMERATE_MENU).eval() else self.menu_in_presets_loop(node, menu, i, item, in_idx, is_clipboard) for i, item in enumerate(_xml(xml).get_name())]
                node.setCachedUserData('in_presets_menu', menu)
                return menu
            
            flam3h_iterator_utils.destroy_cachedUserData(node, 'in_presets_menu')
            if xml and not os.path.isfile(xml):
                return MENU_PRESETS_INVALID
            else:
                return MENU_PRESETS_EMPTY

            
    def menu_in_presets(self) -> list:
        """Rerturn either a cached menu data or rebuild that data on the fly if needed.

        Args:
            (self):
            
        Returns:
            (list): Return a menu
        """
        # self.node.updateParmStates() 
        if self.kwargs['parm'].isHidden():
            return MENU_PRESETS_EMPTY_HIDDEN
        else:
            # This undo's disabler is needed to make the undo work. They work best in H20.5
            with hou.undos.disabler(): # type: ignore
                
                node = self.node
                data: list | None = node.cachedUserData('in_presets_menu')
                data_idx: str | None = node.cachedUserData('in_presets_menu_idx')
                preset_idx: str = node.parm(IN_PRESETS).eval()
                
                # Double check 
                xml: str = os.path.expandvars(node.parm(IN_PATH).eval())
                is_valid: bool = os.path.isfile(xml)
                if xml and not is_valid:
                    flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_FILE, 0)
                    if not node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval(): flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_PRESET, 0)
                    data = None
                elif xml and is_valid:
                    # This caused some pain becasue it is forcing us not to tell the truth sometime
                    # but its quick and we added double checks for each file types (Palette or Flame) inside each menus empty presets (CP, IN and OUT)
                    flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_FILE, 1)
                    
                if data is not None and data_idx == preset_idx:
                    return data
                else:
                    return self.menu_in_presets_data()
        

    def menu_in_presets_empty_data(self) -> list:
        """Populate the IN menu parameters with entries based on the loaded IN XML Flame file.
        When no flame preset has been loaded. This will use the empty star icon to signal wich preset is being selected but not loaded.

        This definition exist only becasue if I change the icon dynamically inside: def menu_in_presets(self) -> list:
        Houdini will mix them up sometime, giving inconsistent results until I perform a new selection from the menu labels list.

        _NOTE:
            If you change the icon gobal variable name inside here,
            remember to updated with the same global variable names inside: in_flame_utils.in_presets_in_isvalid_file_menu_label(...)

        Args:
            (self):

        Returns:
            (list): the actual menu
        """
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            node = self.node
            xml: str = os.path.expandvars(node.parm(IN_PATH).eval())

            if _xml_tree(xml).isvalidtree and node.parm(IN_PVT_ISVALID_FILE).eval() and not node.parm(IN_PVT_ISVALID_PRESET).eval():
                    
                menu: list = []
                [self.menu_in_presets_empty_loop_enum(node, menu, i, item) if node.parm(PREFS_ENUMERATE_MENU).eval() else self.menu_in_presets_empty_loop(node, menu, i, item) for i, item in enumerate(_xml(xml).get_name())]
                node.setCachedUserData('in_presets_menu_off', menu)
                return menu
                
            else:
                if node.parm(IN_PVT_ISVALID_PRESET).eval() and node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval():
                    if xml and not os.path.isfile(xml): return MENU_PRESETS_INVALID_CB
                    else: return MENU_IN_PRESETS_EMPTY_CB
                        
            flam3h_iterator_utils.destroy_cachedUserData(node, 'in_presets_menu_off')
            if node.parm(FLAME_ITERATORS_COUNT).eval():
                if xml and not os.path.isfile(xml):
                    return MENU_PRESETS_INVALID
                else:
                    return MENU_PRESETS_EMPTY
            else:
                if xml and not os.path.isfile(xml):
                    return MENU_ZERO_ITERATORS_PRESETS_INVALID
                else:
                    return MENU_ZERO_ITERATORS

            
    def menu_in_presets_empty(self) -> list:
        """Rerturn either a cached menu data or rebuild that data on the fly if needed.

        Args:
            (self):
            
        Returns:
            (list): Return a menu
        """
        # self.node.updateParmStates() 
        if self.kwargs['parm'].isHidden():
            return MENU_PRESETS_EMPTY_HIDDEN
        else:
            # This undo's disabler is needed to make the undo work. They work best in H20.5
            with hou.undos.disabler(): # type: ignore
                
                node = self.node
                data: list | None = node.cachedUserData('in_presets_menu_off')
                data_idx: str | None = node.cachedUserData('in_presets_menu_off_idx')
                preset_idx: str = node.parm(IN_PRESETS_OFF).eval()
                
                # Double check 
                xml: str = os.path.expandvars(node.parm(IN_PATH).eval())
                is_valid: bool = os.path.isfile(xml)
                if xml and not is_valid:
                    flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_FILE, 0)
                    if not node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval(): flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_PRESET, 0)
                    data = None
                elif xml and is_valid:
                    # This caused some pain becasue it is forcing us not to tell the truth sometime
                    # but its quick and we added double checks for each file types (Palette or Flame) inside each menus empty presets (CP, IN and OUT)
                    flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_FILE, 1)
                    
                if data is not None and data_idx == preset_idx:
                    return data
                else:
                    return self.menu_in_presets_empty_data()
        
        
    def set_iter_on_load_callback(self) -> None:
        """Set the iteration number based on the "iteration on load" number.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        iter_on_load: int = self.node.parm(IN_ITER_NUM_ON_LOAD).eval()
        self.node.setParms({GLB_ITERATIONS: iter_on_load})
        # update Flame preset name if any
        out_flame_utils(self.kwargs).out_auto_change_iter_num_to_prm()
        
        
    def use_iter_on_load_callback(self) -> None:
        """When the IN tab "force iterations on Load" option is turned ON it will set the initial iteration number wisely.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        useiteronload: int = node.parm(IN_USE_ITER_ON_LOAD).eval()
        if useiteronload:
            iternumonload: int = node.parm(IN_ITER_NUM_ON_LOAD).eval()
            iter: int = node.parm(GLB_ITERATIONS).eval()
            if iternumonload == iter:
                pass
            elif iternumonload > iter:
                # node.setParms({GLB_ITERATIONS: iter})
                node.setParms({IN_ITER_NUM_ON_LOAD: iter})
            else:
                node.setParms({GLB_ITERATIONS: iternumonload})
                # update Flame preset name if any
                out_flame_utils(self.kwargs).out_auto_change_iter_num_to_prm()


    def in_to_flam3h_toggle(self, prm: str) -> None:
        """Given a FLAM3H parameter name, toggle it ON or OFF and reload the currently selected flame preset right after.

        Args:
            prm(str): The strin parameter name (toggle parameter) we desire to switch either ON or OFF before reloading the selected flame preset.
            
        Returns:
            (None)
        """
        xml: str = self.node.parm(IN_PATH).eval()
        # Here we could take a shortcut and use: if node.parm(IN_PVT_ISVALID_FILE).eval(): instead,
        # but for now we keep it safe and use the class: _xml_tree(..) instead.
        if _xml_tree(xml).isvalidtree:
            flam3h_general_utils(self.kwargs).flam3h_toggle(prm)
            self.in_to_flam3h()
        else:
            _MSG: str = f"{self.node.name()}: {prm.upper()}: No valid flame file to load the flame from, load a valid flame file first."
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            

    def in_to_flam3h_toggle_f3h_affine(self) -> None:
        """When loading a flame preset that use F3H affine style, this function will reload it
        and switch the "F3H affine style" toggle ON/OFF on the fly.
        
        If no F3H affine style are present in the currently selected flame preset, nothing will happen and a status bar warning message will let the user know about it.
        
        Args:
            (self):
            
        Returns:
            (None):
        """ 
        node = self.node
        xml, clipboard, preset_id, flame_name_clipboard, load_from_clipboard, chaos = self.in_to_flam3h_init_data(node)
        
        # Here we are forced to use the class: _xml_tree(...) becasue a Flame can come from the clipboard
        # and we need to carefully validate it before proceding.
        if xml is not None and _xml_tree(xml).isvalidtree:
            
            apo_data = in_flame_iter_data(node, xml, preset_id)
            if apo_data.f3h_coefs is not None or apo_data.f3h_post is not None or apo_data.finalxform_f3h_coefs is not None or apo_data.finalxform_f3h_post:
                flam3h_general_utils(self.kwargs).flam3h_toggle(IN_FLAM3H_AFFINE_STYLE)
                self.in_to_flam3h()
                
            else:
                if clipboard:
                    _MSG: str = f"{node.name()}: Reload of preset: \"{out_flame_utils.out_remove_iter_num(flame_name_clipboard)}\" from Clipboard -> SKIPPED. The flame preset stored into the Clipboard do not have F3H affine style."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                else:
                    # Get the correct menu parameter's preset menu label
                    preset_name = in_flame_utils.in_presets_in_isvalid_file_menu_label(node, preset_id)
                        
                    _MSG: str = f"{node.name()}: Reload of preset: \"{out_flame_utils.out_remove_iter_num(preset_name)}\" -> SKIPPED. The currently selected flame preset do not have F3H affine style."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                
        else:
            if load_from_clipboard:
                _MSG: str = f"{node.name()}: No valid flame preset to load from the Clipboard, copy a valid flame to the Clipboard first or load from a valid flame file instead."
            else:
                if chaos:
                    _MSG: str = f"IN: Chaotica XML not supported"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    flam3h_general_utils.flash_message(node, _MSG)
                else:
                    _MSG: str = f"{node.name()}: No valid flame file to load the flame from, load a valid flame file first."
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            

    def in_to_flam3h_reset_user_data(self) -> None:
        """Every time we load a flame preset, this definition will reset all FLAM3H data
        so not to clash or cause conflict with the new data generated by the new loaded flame preset.

        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        
        # lets initialize those to default values in case their data no longer exist.
        flam3h_iterator_utils.flam3h_init_hou_session_iterator_data(node)
        flam3h_iterator_utils.flam3h_init_hou_session_ff_data(node)
        
        # Reset iterator user data if needed
        from_FLAM3H_NODE: TA_MNode = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
        if from_FLAM3H_NODE is not None and node == from_FLAM3H_NODE:
            if flam3h_iterator_utils.exist_user_data(from_FLAM3H_NODE):
                flam3h_iterator_utils.del_comment_and_user_data_iterator(from_FLAM3H_NODE)
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX: TA_M = None # type: ignore
        
        # Reset mp idx flam3h mem parameter
        if node.parm(FLAM3H_DATA_PRM_MPIDX).eval() != 0:
            flam3h_iterator_utils.iterator_mpidx_mem_set(node, 0)
        
        # Reset FF user data if needed
        from_FLAM3H_NODE: TA_MNode = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
        if from_FLAM3H_NODE is not None and node == from_FLAM3H_NODE:
            if flam3h_iterator_utils.exist_user_data(from_FLAM3H_NODE, FLAM3H_USER_DATA_FF):
                flam3h_iterator_utils.del_comment_and_user_data_iterator(from_FLAM3H_NODE, FLAM3H_USER_DATA_FF)
                hou.session.FLAM3H_MARKED_FF_CHECK: TA_M = None # type: ignore


    def in_to_flam3h_reset_iterators_parms(self, node: hou.SopNode, in_flame_iter_count: int) -> None:
        """Prior to this, I was setting the iterator's count to zero and then back to the requested count to reset all their values.
        It was not the fastest solution and this is actually making it more performant overall.

        Args:
            (self):
            node(hou.SopNode): This FLAM3H node
            in_flame_iter_count(int): IN flame iterator's count ( number of xforms )

        Returns:
            (None):
        """
        # iterators
        flam3h_iter_count: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        
        if in_flame_iter_count > flam3h_iter_count:
            [p.deleteAllKeyframes() for p in node.parms() if not p.isLocked()]
            [p.revertToDefaults() for p in node.parms() if p.isMultiParmInstance()]
            node.setParms({FLAME_ITERATORS_COUNT:  in_flame_iter_count}) # type: ignore
            
        elif in_flame_iter_count == flam3h_iter_count:
            [p.deleteAllKeyframes() for p in node.parms() if not p.isLocked()]
            [p.revertToDefaults() for p in node.parms() if p.isMultiParmInstance()]
            
        else:
            node.setParms({FLAME_ITERATORS_COUNT: in_flame_iter_count}) # type: ignore
            [p.deleteAllKeyframes() for p in node.parms() if not p.isLocked()]
            [p.revertToDefaults() for p in node.parms() if p.isMultiParmInstance()]


    def in_to_flam3h_resets(self, node: hou.SopNode, _FLAM3H_INIT_DATA: TA_F3H_Init) -> None:
        """Reset the FLAM3H UI parameters to welcome the new one from the XML Flame preset we are loading.
        
        Args:
            (self):
            node(hou.SopNode): FLAM3H node to load the flame file/preset into.
            _FLAM3H_INIT_DATA(TA_F3H_Init): tuple(  xml, 
                                                    clipboard, 
                                                    preset_id, 
                                                    clipboard_flame_name, 
                                                    attempt_to_load_from_clipboard, 
                                                    chaos
                                                    )
                                                
                                                    * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                                    * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                    * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                    * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                    * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                    * chaos ( bool ): Is it a chaotica XML file type ? True or False.

        Returns:
            (None):
        """
        xml, clipboard, preset_id, flame_name_clipboard, attempt_from_clipboard, chaos = _FLAM3H_INIT_DATA
        
        iter_on_load: int = in_flame_utils.in_set_iter_on_load(node, preset_id, clipboard, flame_name_clipboard)
        flam3h_general_utils(self.kwargs).reset_SYS(1, iter_on_load, 0)
        flam3h_general_utils(self.kwargs).reset_MB()
        flam3h_general_utils(self.kwargs).reset_PREFS()


    def in_to_flam3h_set_iterators(self, node: hou.SopNode, apo_data: in_flame_iter_data, _FLAM3H_INIT_DATA: TA_F3H_Init) -> None:
        """Set the iterators data (FLAME or FF tab) into FLAM3H from the loaded XML Flame preset.
        
        Args:
            (self):
            node(hou.SopNode): FLAM3H node to load the flame file/preset into.
            apo_data(in_flame_iter_data): All the XML data from the loaded Flame preset.
            _FLAM3H_INIT_DATA(TA_F3H_Init): tuple(  xml, 
                                                    clipboard, 
                                                    preset_id, 
                                                    clipboard_flame_name, 
                                                    attempt_to_load_from_clipboard, 
                                                    chaos
                                                    )
                                                    
                                                    * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                                    * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                    * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                    * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                    * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                    * chaos ( bool ): Is it a chaotica XML file type ? True or False.

        Returns:
            (None):
        """
        xml, clipboard, preset_id, flame_name_clipboard, attempt_from_clipboard, chaos = _FLAM3H_INIT_DATA
        
        # ITERATOR
        ####################################################
        # prepare iterators
        assert apo_data.xforms is not None
        self.in_to_flam3h_reset_iterators_parms( node, len(apo_data.xforms) )
        
        # RIP: if there are ZERO opacities, always turn RIP toggle ON
        if apo_data.opacity is not None and min(apo_data.opacity) == 0.0:
            flam3h_general_utils.private_prm_set(node, PREFS_PVT_RIP, 1)
        else:
            # Otherwise set RIP toggle accordingly from the XML data if any
            if apo_data.sys_flam3h_rip is not None:
                flam3h_general_utils.private_prm_set(node, PREFS_PVT_DOFF, apo_data.sys_flam3h_rip)

        # Set iterators
        self.in_flam3h_set_iterators(0, node, apo_data, preset_id)
        
        # FF
        ####################################################
        if apo_data.finalxform is not None:
            flam3h_iterator_utils(self.kwargs).flam3h_reset_FF()
            flam3h_general_utils.private_prm_set(node, PREFS_PVT_DOFF, 1)
            # Set FF
            self.in_flam3h_set_iterators(1, node, apo_data, preset_id)
        else:
            flam3h_iterator_utils(self.kwargs).flam3h_reset_FF()
            flam3h_general_utils.private_prm_set(node, PREFS_PVT_DOFF, 0)


    def in_to_flam3h_set_motion_blur(self, node: hou.SopNode, apo_data: in_flame_iter_data) -> None:
        """Set the Motion Blur data into FLAM3H from the loaded XML Flame preset.
        
        Args:
            (self):
            node(hou.SopNode): FLAM3H node to load the flame file/preset into.
            apo_data(in_flame_iter_data): All the XML data from the loaded Flame preset.

        Returns:
            (None):
        """ 
        if apo_data.mb_flam3h_fps is not False:
            node.setParms({MB_DO: 1}) # type: ignore
            node.setParms({MB_FPS: apo_data.mb_flam3h_fps}) # type: ignore
            node.setParms({MB_SAMPLES: apo_data.mb_flam3h_samples}) # type: ignore
            node.setParms({MB_SHUTTER: apo_data.mb_flam3h_shutter}) # type: ignore
        else:
            flam3h_general_utils(self.kwargs).reset_MB()
            

    def in_to_flam3h_set_palette(self, node: hou.SopNode, apo_data: in_flame_iter_data, _FLAM3H_INIT_DATA: TA_F3H_Init, flashmessage: bool = False) -> None:
        """Set the Palette data into FLAM3H from the loaded XML Flame preset.
        
        Args:
            (self):
            node(hou.SopNode): FLAM3H node to load the flame file/preset into.
            apo_data(in_flame_iter_data): All the XML data from the loaded Flame preset.
            _FLAM3H_INIT_DATA(TA_F3H_Init): tuple(  xml, 
                                                    clipboard, 
                                                    preset_id, 
                                                    clipboard_flame_name, 
                                                    attempt_to_load_from_clipboard, 
                                                    chaos
                                                    )

                                                    * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                                    * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                    * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                    * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                    * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                    * chaos ( bool ): Is it a chaotica XML file type ? True or False.
            flashmessage(bool): Default to False. if True, it will fire a flash and status message instead of a print message to the console. To be used when loading Palette data from the clipboard from a Flame preset.

        Returns:
            (None):
        """ 
        xml, clipboard, preset_id, flame_name_clipboard, attempt_from_clipboard, chaos = _FLAM3H_INIT_DATA
        
        if apo_data.palette is not None:
            
            # if CP HSV vals
            if apo_data.cp_flam3h_hsv is not False: node.setParms({CP_RAMP_HSV_VAL_NAME: apo_data.cp_flam3h_hsv}) # type: ignore
            else: node.setParms({CP_RAMP_HSV_VAL_NAME: hou.Vector3((1.0, 1.0, 1.0))}) # type: ignore
            
            # Set XML palette data
            ramp_parm = node.parm(CP_RAMP_SRC_NAME)
            # Reset ramps to default
            flam3h_palette_utils.build_ramp_palette_default(ramp_parm)
            flam3h_palette_utils.delete_ramp_all_keyframes(ramp_parm)
            flam3h_palette_utils.delete_ramp_all_keyframes(node.parm(CP_RAMP_HSV_NAME))
            ramp_parm.set(apo_data.palette[0])
            flam3h_palette_utils(self.kwargs).palette_cp()
            # Set palette lookup samples
            node.setParms({CP_RAMP_LOOKUP_SAMPLES: apo_data.cp_flam3h_samples}) # type: ignore
            # Mark this as not a loaded palette preset
            flam3h_general_utils.private_prm_set(node, CP_PVT_ISVALID_PRESET, 0)
            # reset tmp ramp palette
            flam3h_palette_utils(self.kwargs).reset_CP_TMP()
            
        else:
            ramp_parm = node.parm(CP_RAMP_SRC_NAME)
            _BASEs, _POSs, _COLORs = flam3h_palette_utils.build_ramp_palette_error()
            ramp_parm.set(hou.Ramp(_BASEs, _POSs, _COLORs))
            
            if flashmessage:
                _MSG = f"CP ERROR from the Clipboard"
                flam3h_general_utils.flash_message(node, _MSG)
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}. The loaded Palette data has invalid HEX values.", "WARN")
            else:
                if attempt_from_clipboard: _MSG: str = "\nFlame IN Clipboard: The loaded Flame preset's Palette has invalid HEX values."
                else: _MSG: str = "\nFlame IN: The loaded Flame preset's Palette has invalid HEX values."
                # A print() is being used here becasue otherwise
                # it will be cleared out by other status bar messages down the line when loading a Flame preset
                print(f"Warning:\n{node.name()}: {_MSG}\n")
            
            
    def in_to_flam3h_stats_and_properties(self, node: hou.SopNode, apo_data: in_flame_iter_data, _FLAM3H_INIT_DATA: TA_F3H_Init, copy_only: bool = False) -> None:
        """Set all the loaded Flame preset stats/infos and copy its render properties if needed into the OUT tab.
        
        Args:
            (self):
            node(hou.SopNode): FLAM3H node to load the flame file/preset into.
            apo_data(in_flame_iter_data): All the XML data from the loaded Flame preset.
            _FLAM3H_INIT_DATA(TA_F3H_Init): tuple(  xml, 
                                                    clipboard, 
                                                    preset_id, 
                                                    clipboard_flame_name, 
                                                    attempt_to_load_from_clipboard, 
                                                    chaos
                                                    )
                                                    
                                                    * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                                    * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                    * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                    * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                    * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                    * chaos ( bool ): Is it a chaotica XML file type ? True or False.
                                                                                                
            copy_only (bool): This is used to distinguish a Flame preset coming in from the Clipboard only for the Render Properties copy/paste. Default to: False

        Returns:
            (None):
        """ 
        xml, clipboard, preset_id, flame_name_clipboard, attempt_from_clipboard, chaos = _FLAM3H_INIT_DATA
        
        # This for when we are loading a Flame preset in full
        if copy_only is False:
            # Update flame stats
            node.setParms({MSG_IN_FLAMESTATS: self.in_load_stats_msg(preset_id, apo_data, clipboard)}) # type: ignore
            node.setParms({MSG_IN_FLAMESENSOR: self.in_load_sensor_stats_msg(preset_id, apo_data)}) # type: ignore
            node.setParms({MSG_IN_FLAMERENDER: self.in_load_render_stats_msg(preset_id, apo_data)}) # type: ignore
            
            # if we are loading from the clipboard, always copy the render settings on load
            if clipboard: self.in_copy_render_all_stats_msg(self.kwargs, apo_data, clipboard)
            else:
                # If not from clipboard
                # Update SYS inpresets parameters
                node.setParms({IN_SYS_PRESETS: str(preset_id)}) # type: ignore
                node.setParms({IN_SYS_PRESETS_OFF: str(preset_id)}) # type: ignore
                
                # if "copy render properties on Load" is checked
                if node.parm(IN_COPY_RENDER_PROPERTIES_ON_LOAD).eval():
                    self.in_copy_render_all_stats_msg(self.kwargs, apo_data, clipboard)
                    
        # And this when we are loading a Flame preset from the Clipboard to only copy its Render properties
        else:
            # if we are loading from the clipboard (in this case we always are), copy all the Render Properties
            if clipboard: self.in_copy_render_all_stats_msg(self.kwargs, apo_data, clipboard)
            

    def in_to_flam3h_toggles_and_msg(self, node: hou.SopNode, apo_data: in_flame_iter_data, _FLAM3H_INIT_DATA: TA_F3H_Init) -> None:
        """Set all the toggles about file and preset validity.
        
        Args:
            (self):
            node(hou.SopNode): FLAM3H node to load the flame file/preset into.
            apo_data(in_flame_iter_data): All the XML data from the loaded Flame preset.
            _FLAM3H_INIT_DATA(TA_F3H_Init): tuple(  xml, 
                                                    clipboard, 
                                                    preset_id, 
                                                    clipboard_flame_name, 
                                                    attempt_to_load_from_clipboard, 
                                                    chaos
                                                    )
                                                    
                                                    * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                                    * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                    * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                    * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                    * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                    * chaos ( bool ): Is it a chaotica XML file type ? True or False.

        Returns:
            (None):
        """ 
        
        xml, clipboard, preset_id, flame_name_clipboard, attempt_from_clipboard, chaos = _FLAM3H_INIT_DATA
        
        if clipboard:
            # If it is a valid preset from the clipboard, set the "valid preset" and "clipboard" toggles
            # but do not change the "is valid file" toggle as we dnt know if a valid file is already loaded.
            flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_PRESET, 1)
            flam3h_general_utils.private_prm_set(node, IN_PVT_CLIPBOARD_TOGGLE, 1)
            
            preset_name: str = flame_name_clipboard
            _MSG: str = f"{node.name()}: LOAD Flame preset from Clipboard: \"{out_flame_utils.out_remove_iter_num(preset_name)}\" -> Completed"
        else:
            # Otherwise mean the preset is coming from a file,
            # set all of them and uncheck the clipboard toggle just in case.
            flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_FILE, 1)
            flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_PRESET, 1)
            flam3h_general_utils.private_prm_set(node, IN_PVT_CLIPBOARD_TOGGLE, 0)
            
            # Get the correct menu parameter's preset menu label
            preset_name: str = apo_data.name[preset_id]
            _MSG: str = f"{node.name()}: LOAD Flame preset: \"{out_flame_utils.out_remove_iter_num(preset_name)}\" -> Completed"
            
        flam3h_general_utils.set_status_msg(_MSG, 'IMP')
        flam3h_general_utils.flash_message(node, f"{preset_name}")


    def in_to_flam3h_init_data_ALT(self) -> TA_F3H_Init:
        """Load a flame preset from the clipboard.
        This definition will be used inside: 
        * def in_to_flam3h_init_data(self, node: hou.SopNode) -> TA_F3H_Init:
        
        It will also output some data to be used inside: def in_to_flam3h(self) -> None:

        Args:
            (self):

        Returns:
            (TA_F3H_Init): tuple(xml, 
                                 clipboard, 
                                 preset_id, 
                                 clipboard_flame_name, 
                                 attempt_to_load_from_clipboard, 
                                 chaos
                                 )

                                 * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                 * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                 * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                 * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                 * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                 * chaos ( bool ): Is it a chaotica XML file type ? True or False.
        """     
        xml: str = hou.ui.getTextFromClipboard() # type: ignore
        try: tree = lxmlET.ElementTree(lxmlET.fromstring(xml)) # type: ignore
        except: tree = None
        if tree is not None:
            assert xml is not None
            if tuple([f for f in tree.getroot().iter(XML_FLAME_NAME)]):
                flame_name_clipboard: str = _xml_tree(xml).name[0]
                return xml, True, 0, flame_name_clipboard, True, False
            else:
                if self.in_to_flam3h_is_CHAOS(xml):
                    return None, False, 0, '', True, True
                else:
                    return None, False, 0, '', True, False
        else:
            return None, False, 0, '', True, False


    def in_to_flam3h_init_data_SHIFT(self, node: hou.SopNode) -> TA_F3H_Init:
        """Load a flame file from a file dialog.
        This definition will be used inside: 
        * def in_to_flam3h_init_data(self, node: hou.SopNode) -> TA_F3H_Init:
        
        It will also output some data to be used inside: def in_to_flam3h(self) -> None:

        Args:
            (self):
            node(hou.SopNode): FLAM3H node to load the flame file/preset into.

        Returns:
            (TA_F3H_Init): tuple(xml, 
                                 clipboard, 
                                 preset_id, 
                                 clipboard_flame_name, 
                                 attempt_to_load_from_clipboard, 
                                 chaos
                                 )

                                 * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                 * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                 * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                 * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                 * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                 * chaos ( bool ): Is it a chaotica XML file type ? True or False.
        """
        
        flameFile = hou.ui.selectFile(start_directory=None, title="FLAM3H: Load a *.flame file", collapse_sequences=False, file_type=hou.fileType.Any, pattern="*.flame", default_value=None, multiple_select=False, image_chooser=None, chooser_mode=hou.fileChooserMode.Read, width=0, height=0)  # type: ignore
        flameFile_expandvars: str = os.path.expandvars(flameFile)
        
        dir: str = os.path.dirname(flameFile_expandvars)
        if os.path.isdir(dir):
            
            if _xml_tree(flameFile_expandvars).isvalidtree:
                
                node.setParms({IN_PATH: flameFile_expandvars}) # type: ignore
                # Since this goes directly into: self.in_to_flam3h() definition only
                # its argument is set to 0 so not to create a loop of loading processes
                # becasue inside the following definition there is another call to: self.in_to_flam3h()
                flam3h_general_utils(self.kwargs).flam3h_init_presets_IN_PRESETS(0)
                
                # Set menu parameters index to the first entry
                [prm.set('0') for prm in (node.parm(IN_PRESETS), node.parm(IN_PRESETS_OFF), node.parm(IN_SYS_PRESETS), node.parm(IN_SYS_PRESETS_OFF))]
                
                return flameFile_expandvars, False, 0, '', False, False
            
            else:
                if self.in_to_flam3h_is_CHAOS(flameFile_expandvars):
                    return None, False, 0, '', False, True
                else:
                    return None, False, 0, '', False, False
            
        else:
            return None, False, 0, '', False, False
        
        
    def in_to_flam3h_init_data_CTRL(self) -> TA_F3H_Init:
        """Load nothing, as the kwargs['ctrl'] is not mapped to anything yet so this is a place holder.
        This definition will be used inside: 
        * def in_to_flam3h_init_data(self, node: hou.SopNode) -> TA_F3H_Init:
        
        It will also output some data to be used inside: def in_to_flam3h(self) -> None:

        Args:
            (self):

        Returns:
            (TA_F3H_Init): tuple(xml, 
                                 clipboard, 
                                 preset_id, 
                                 clipboard_flame_name, 
                                 attempt_to_load_from_clipboard, 
                                 chaos
                                 )

                                 * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                 * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                 * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                 * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                 * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                 * chaos ( bool ): Is it a chaotica XML file type ? True or False.
    """
        return None, False, 0, '', False, False
    
    
    def in_to_flam3h_init_data_LMB(self, node: hou.SopNode) -> TA_F3H_Init:
        """Load a flame preset with a mouse click, no kwargs.
        This definition will be used inside:
        * def in_to_flam3h_init_data(self, node: hou.SopNode) -> TA_F3H_Init:
        
        It will also output some data to be used inside: def in_to_flam3h(self) -> None:

        Args:
            (self):
            node(hou.SopNode): FLAM3H node to load the flame file/preset into.

        Returns:
            (TA_F3H_Init): tuple(xml, 
                                 clipboard, 
                                 preset_id, 
                                 clipboard_flame_name, 
                                 attempt_to_load_from_clipboard, 
                                 chaos
                                 )

                                 * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                 * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                 * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                 * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                 * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                 * chaos ( bool ): Is it a chaotica XML file type ? True or False.
    """
        xml: str = os.path.expandvars(node.parm(IN_PATH).eval())
        
        # Get the correct menu parameter's preset idx
        if node.parm(IN_PVT_ISVALID_PRESET).eval():
            preset_id: str = node.parm(IN_PRESETS).eval()
            # Update
            node.setParms({IN_PRESETS_OFF: preset_id}) # type: ignore
        else:
            preset_id: str = node.parm(IN_PRESETS_OFF).eval()
            # Update
            node.setParms({IN_PRESETS: preset_id}) # type: ignore
            
        return xml, False, int(preset_id), '', False, False


    def in_to_flam3h_init_data(self, node: hou.SopNode) -> TA_F3H_Init:
        """Check if we are able to load a flame from a selected file or to parse a flame from the clipboard
        and provide some output data to work with if any of those cases are true.
        
        Args:
            (self):
            node(hou.SopNode): FLAM3H node to load the flame file/preset into.

        Returns:
            (TA_F3H_Init): tuple(xml, 
                                 clipboard, 
                                 preset_id, 
                                 clipboard_flame_name, 
                                 attempt_to_load_from_clipboard, 
                                 chaos
                                 )

                                 * xml ( str | None ): either a flame preset from a flame file or from the Clipboard.
                                 * clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                 * preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                 * clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                 * attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                 * chaos ( bool ): Is it a chaotica XML file type ? True or False.
        """ 
        # The following try/except block is in place to avoid a 'KeyError' when
        # loading a flame preset from the menu parameter entries instead of clicking the Action Button's icon.
        
        try:
            self.kwargs['alt']
        except:
            _K: bool = False
        else:
            _K: bool = True

        # if kwargs
        if _K:
            # ALT - If we are loading a flame from the clipboard
            if self.kwargs['alt']:
                return self.in_to_flam3h_init_data_ALT()
                
            # SHIFT - If we are selecting a flame file to load
            elif self.kwargs['shift']:
                return self.in_to_flam3h_init_data_SHIFT(node)
            
            # CTRL - not mapped yet...
            elif self.kwargs['ctrl']:
                return self.in_to_flam3h_init_data_CTRL()
            
            else:
                return self.in_to_flam3h_init_data_LMB(node)
            
        # otherwise if just a mouse click
        else:
            return self.in_to_flam3h_init_data_LMB(node)


    '''
        The following function is just a shortcut to set and load
        a new preset from the IN Tab IN_PRESETS parameter,
        It works like a hook to then set and evaluate it from the SYS Tab.
    '''
    def in_to_flam3h_sys(self) -> None:
        """Load a Flame preset into FLAM3H from the SYS Tab Flame load icon.
        This will set all FLAM3H node parameters based on values from the loaded XML Flame preset.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        xml: str = node.parm(IN_PATH).eval()

        if xml and node.parm(IN_PVT_ISVALID_FILE).eval():
            if node.parm(IN_PVT_ISVALID_PRESET).eval():
                preset_id: str = node.parm(IN_SYS_PRESETS).eval()
                # Update other PRESETS menu parameters
                [prm.set(preset_id) for prm in (node.parm(IN_SYS_PRESETS_OFF), node.parm(IN_PRESETS), node.parm(IN_PRESETS_OFF))]
            else:
                preset_id: str = node.parm(IN_SYS_PRESETS_OFF).eval()
                # Update other PRESETS menu parameters
                [prm.set(preset_id) for prm in (node.parm(IN_SYS_PRESETS), node.parm(IN_PRESETS), node.parm(IN_PRESETS_OFF))]
        
            self.in_to_flam3h()


    '''
        The following is the actual load preset/flame function to be used.
    '''
    def in_to_flam3h(self) -> None:
        """Load a Flame preset into FLAM3H.
        This will set all FLAM3H node parameters based on values from the loaded XML Flame preset.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        
        _FLAM3H_INIT_DATA: tuple = self.in_to_flam3h_init_data(node)
        xml, clipboard, preset_id, flame_name_clipboard, attempt_from_clipboard, chaos = _FLAM3H_INIT_DATA

        if xml is not None and _xml_tree(xml).isvalidtree:

            # IN flame preset data
            apo_data = in_flame_iter_data(node, xml, preset_id)
            # If there are xforms/iterators
            if apo_data.xforms is not None:
                
                # Store into the FLAM3H node data storage
                node.setUserData(FLAM3H_USER_DATA_XML_LAST, lxmlET.tostring(apo_data.flame[preset_id], encoding="unicode")) # type: ignore
                # Transfer the data from the stored XML into FLAM3H
                self.in_to_flam3h_resets(node, _FLAM3H_INIT_DATA)
                self.in_to_flam3h_set_iterators(node, apo_data, _FLAM3H_INIT_DATA)
                self.in_to_flam3h_set_motion_blur(node, apo_data)
                self.in_to_flam3h_set_palette(node, apo_data, _FLAM3H_INIT_DATA)                
                self.in_to_flam3h_stats_and_properties(node, apo_data, _FLAM3H_INIT_DATA)
                self.in_to_flam3h_reset_user_data()
                self.in_to_flam3h_toggles_and_msg(node, apo_data, _FLAM3H_INIT_DATA)
                # Updates
                flam3h_iterator_utils(self.kwargs).auto_set_xaos()
                out_flame_utils(self.kwargs).out_auto_change_iter_num_to_prm(apo_data.name[preset_id])
                flam3h_iterator_utils.destroy_cachedUserData(node, 'iter_sel')
                flam3h_iterator_utils.destroy_cachedUserData(node, 'edge_case_01')
                # This is needed to help to updates the menus from time to time so to pick up sneaky changes to the loaded files
                # (ex. the user perform hand made modifications like renaming a Preset and such).
                flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node, False)
                
                # F3C ( the if statement is for backward compatibility )
                if apo_data.prefs_flam3h_f3c is not None: flam3h_general_utils.private_prm_set(node, PREFS_PVT_F3C, apo_data.prefs_flam3h_f3c)
                # Reset/Set density
                flam3h_general_utils.reset_density(node)
                
                # XF VIZ SOLO OFF (but leave the xforms handles VIZ ON)
                flam3h_general_utils.private_prm_set(node, PREFS_PVT_XF_VIZ_SOLO, 0)
                flam3h_iterator_utils.destroy_userData(node, f"{FLAM3H_USER_DATA_PRX}_{FLAM3H_USER_DATA_XF_VIZ}")
                # BUILD XFVIZ if needed
                flam3h_general_utils.util_xf_viz_force_cook(node, self.kwargs)
                
                # As a backup plan. Most likely not needed by why not
                data: str | None = node.userData(FLAM3H_USER_DATA_XML_LAST)
                if data is None or not _xml_tree(data).isvalidtree:
                    out_flame_utils(self.kwargs).out_userData_XML_last_loaded(FLAM3H_USER_DATA_XML_LAST, apo_data.name[preset_id])
                
            else:
                if attempt_from_clipboard: _MSG: str = "Flame IN Clipboard: The loaded Flame preset have 0(Zero) xforms/iterators. SKIPPED"
                else: _MSG: str = "Flame IN: The loaded Flame preset have 0(Zero) xforms/iterators. SKIPPED"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
            
        else:
            
            # If there is an already loaded file set in the parameter
            in_xml: str = os.path.expandvars(node.parm(IN_PATH).eval())
            
            # If we loaded a Chaotica XML style preset from the Clipboard 
            if self.in_to_flam3h_clipboard_is_CHAOS():
                _MSG: str = "IN Clipboard: Chaotica XML not supported"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
                flam3h_general_utils.flash_message(node, _MSG)

            # If we are trying to load from the Clipboard
            elif attempt_from_clipboard:
                _MSG: str = "IN Clipboard: Nothing to load"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                flam3h_general_utils.flash_message(node, _MSG)
                
            else:
                
                # If we did try to load a chaotica XML style file
                if chaos:
                    _MSG: str = f"IN: Chaotica XML not supported"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
                    flam3h_general_utils.flash_message(node, _MSG)
                
                # If there was already a valid flame file
                elif _xml_tree(in_xml).isvalidtree:
                    pass
                    
                # If there was already a preset loaded from the clipboard
                elif node.parm(IN_PVT_ISVALID_PRESET).eval() and node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval():
                    
                    flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_FILE, 0)
                        
                    _MSG: str = "IN: Nothing to load"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                    flam3h_general_utils.flash_message(node, _MSG)
                     
                # Anything else   
                else:
                    [flam3h_general_utils.private_prm_set(node, prm_name, 0) for prm_name in (IN_PVT_ISVALID_FILE, IN_PVT_ISVALID_PRESET, IN_PVT_CLIPBOARD_TOGGLE)]
                    # clear info msgs
                    [prm.set("") for prm in (node.parm(MSG_IN_FLAMESTATS), node.parm(MSG_IN_FLAMERENDER), node.parm(MSG_DESCRIPTIVE_PRM))]
                    # If iterator's count is 0(Zero), change focus back to the IN's Tab
                    # And let the user know it should load a flame file first
                    if node.parm(FLAME_ITERATORS_COUNT).eval() == 0:
                        _MSG: str = "IN: Load an IN flame file first"
                        node.parmTuple(FLAM3H_ITERATORS_TAB).set((1,))
                    else: _MSG: str = "IN: Nothing to load"

                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                    flam3h_general_utils.flash_message(node, _MSG)
                    
                    
    def in_to_flam3h_render_properties_only(self) -> None:
        """Load a Flame preset render properties into FLAM3H.
        This will set all FLAM3H node parameters based on values from the loaded XML Flame preset.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        
        _FLAM3H_INIT_DATA: tuple = self.in_to_flam3h_init_data(node)
        xml, clipboard, preset_id, flame_name_clipboard, attempt_from_clipboard, chaos = _FLAM3H_INIT_DATA

        if xml is not None and _xml_tree(xml).isvalidtree:

            # IN flame preset data
            apo_data = in_flame_iter_data(node, xml, preset_id)
            
            # Transfer the data from the stored XML Render Properties from the Clipboard into FLAM3H               
            self.in_to_flam3h_stats_and_properties(node, apo_data, _FLAM3H_INIT_DATA, True)
            flam3h_general_utils.flash_message(self.node, f"ALL settings Clipboard: COPIED")
            
        else:
            
            # If we loaded a Chaotica XML style preset from the Clipboard 
            if self.in_to_flam3h_clipboard_is_CHAOS():
                _MSG: str = "Render Properties Clipboard: Chaotica XML not supported"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
                flam3h_general_utils.flash_message(node, _MSG)
                
            else:
                _MSG: str = "Render Properties Clipboard: Nothing to load"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}. Copy a Flame into the clipboard first to copy its render properties into here.", 'IMP')
                flam3h_general_utils.flash_message(node, _MSG)


    def reset_IN(self, mode: int = 0) -> None:
        """Reset the FLAM3H IN Tab parameters.

        Args:
            (self):
            mode(int): Defaults to 0. 1 will reset the remainder of the parameters.
            
        Returns:
            (None):
        """
        node = self.node
        
        flam3h_general_utils.private_prm_set(node, IN_PVT_ISVALID_PRESET, 0)
        flam3h_general_utils.private_prm_set(node, IN_PVT_CLIPBOARD_TOGGLE, 0)
        [prm.set("") for prm in (node.parm(MSG_IN_FLAMESTATS), node.parm(MSG_IN_FLAMERENDER), node.parm(MSG_IN_FLAMESENSOR), node.parm(MSG_DESCRIPTIVE_PRM),  node.parm(MSG_IN_STATS_HEADING), node.parm(MSG_IN_SETTINGS_HEADING))]
        
        if mode:
            # This is not being used anymore but I leave it here just in case
            node.setParms({IN_PATH: ""})
            node.setParms({IN_PRESETS: str(-1)})
            node.setParms({IN_PRESETS_OFF: str(-1)})
            node.setParms({IN_ITER_NUM_ON_LOAD: 64})
            node.setParms({IN_USE_ITER_ON_LOAD: 0})
            node.setParms({IN_COPY_RENDER_PROPERTIES_ON_LOAD: 1})


# CONVERT FRACTORIUM's VAR DICT start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
# Turn Fractorium variation names dictionary into PRE and POST variation names dictionary
VARS_FRACTORIUM_DICT_PRE: dict[str, tuple]  = in_flame_utils.in_util_vars_dict_type_maker(VARS_FRACTORIUM_DICT, in_flame_utils.in_util_make_PRE)
VARS_FRACTORIUM_DICT_POST: dict[str, tuple] = in_flame_utils.in_util_vars_dict_type_maker(VARS_FRACTORIUM_DICT, in_flame_utils.in_util_make_POST)


# SAVE XML FILES start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################

# this has been pre-built to work with: menu_sensor_resolution_set(self, update=True) -> None:
MENU_OUT_SENSOR_RESOLUTIONS: list = [0, '', 1, '640x480', 2, 'HDTV 720', 3, 'HDTV 1080', 4, 'HDTV 2160 (4K)', 5, '', 6, 'NTSC', 7, 'NTSC D1', 8, 'PAL', 9, 'PAL 16:9 (1 to 1)', 10, '', 11, 'Full Ap 4K', 12, 'Full Ap 2K', 13, 'Acad 4K', 14, 'Acad 2K', 15, 'Scope 4K', 16, 'Scope 2K', 17, 'Vista 2K', 18, '', 19, '256^2', 20, '512^2', 21, '1024^2', 22, '2048^2', 23, '4096^2', 24, '']


class out_flame_utils:
    """
class out_flame_utils

@STATICMETHODS
* out_render_curves_set_data_defaults(node: hou.SopNode) -> None:
* out_render_curves_retrive_data(node: hou.SopNode) -> None:
* out_render_curves_set_and_retrieve_defaults(node: hou.SopNode) -> None:
* out_render_curves_compare(node: hou.SopNode, mode: bool = False) -> bool:
* out_render_curves_compare_and_set_toggle(node: hou.SopNode) -> None:
* out_render_curves_set_defaults_on_load(node: hou.SopNode):
* out_auto_add_iter_num(iter_num: int, name: str, autoadd: int, flame: bool = True) -> str:
* out_auto_change_iter_num(iter_num: int, flame_name: str, autoadd: int) -> str:
* out_remove_iter_num(flame_name: str) -> str:
* out_flame_default_name(node: hou.SopNode, autoadd: int) -> str:
* out_util_round_float(val: float) -> str:
* out_util_round_floats(val_list: list[list[str]] | tuple[list]) -> list[str] | list[list[str]] | tuple[str]:
* out_util_check_duplicate_var_section(vars: list) -> bool:
* __out_util_iterators_vars_duplicate(vars: list) -> list:
* out_util_vars_duplicate(vars: list) -> list:
* out_check_build_file(file_split: tuple[str, str] | list[str], file_name: str, file_ext: str) -> str:
* out_check_outpath_messages(node: hou.SopNode, infile: str, file_new: str, file_ext: str, prx: str) -> None:
* out_check_outpath(node: hou.SopNode, infile: str, file_ext: str, prx: str, out: bool = True, auto_name: bool = True) -> str | bool:
* out_affine_rot(affine: list[tuple[str] | list[str]], angleDeg: float) -> list[list[str] | tuple[str]]:
* out_xaos_cleanup(xaos: list[str] | list[list[str], tuple[str]]) -> list[list[str]]:
* out_xaos_collect(node: hou.SopNode, iter_count: int, prm: str) -> list[list[str]]:
* out_xaos_collect_vactive(node: hou.SopNode, fill: list, prm: str) -> list[list[str]]:
* _out_pretty_print(current: lxmlET.Element, parent: lxmlET.Element | None = None, index: int = -1, depth: int = 0) -> None: #type: ignore
* _out_pretty_print(current, parent=None, index: int=-1, depth: int=0) -> None:
* menu_out_presets_loop(menu: list, i: int, item: str) -> None:
* menu_out_presets_loop_enum(menu: list, i: int, item: str) -> None:
* out_collect_var_section_names(node: hou.SopNode, var_section: str = "VAR") -> list[str] | None:
* out_collect_var_section_names_dict(node: hou.SopNode, mode: int = False, var_section = "VAR") -> dict[str | list[str], bool]:
* out_buil_xf_names(f3d: out_flame_xforms_data) -> tuple:

@METHODS
* out_palette_256_plus_check(self) -> None:
* out_presets_get_selected_menu_label(self) -> str | None:
* out_presets_copy_menu_label_callback(self) -> None:
* out_palette_keys_count(self, palette_plus: int, keys: int, type: int, _MSG = True) -> str:
* menu_sensor_resolution(self) -> list:
* menu_sensor_resolution_set(self, update=True) -> None:
* reset_OUT_sensor(self) -> None:
* reset_OUT_render(self) -> None:
* reset_OUT_kwargs(self) -> None:
* reset_OUT_options(self) -> None:
* reset_OUT(self, mode=0) -> None:
* out_xf_xaos_to(self) -> tuple:
* out_xf_xaos_from(self, mode=0) -> tuple:
* menu_out_contents_presets_data(self) -> list:
* menu_out_contents_presets(self) -> list:
* out_auto_add_iter_data(self) -> tuple[int, str, int]:
* out_auto_add_iter_num_to_prm(self) -> None:
* out_auto_change_iter_num_to_prm(self, name: str | None = None) -> None:
* out_flame_name_inherit_on_load(self) -> None:
* out_flame_properties_build(self, f3r: out_flame_render_properties) -> dict:
* out_flam3_compatibility_check_and_msg(self) -> bool:                                
* out_populate_xform_vars_XML(self, 
                            varsPRM: tuple, 
                            TYPES_tuple: tuple, 
                            WEIGHTS_tuple: tuple, 
                            XFORM: lxmlET.Element, # type: ignore
                            MP_IDX: str, 
                            FUNC: Callable) -> list[str]:
* out_build_XML(self, flame: lxmlET.Element) -> bool:
* out_userData_XML_last_loaded(self, data_name: str = FLAM3H_USER_DATA_XML_LAST, flame_name: str | None = None) -> None:
* out_new_XML(self, outpath: str) -> None:
* out_new_XML_clipboard(self) -> None:
* out_append_XML(self, apo_data: in_flame, out_path: str) -> None:
* out_XML(self) -> None:
* __out_flame_data(self, prm_name: str = '') -> str:
* __out_flame_name(self, prm_name: str | None = OUT_XML_RENDER_HOUDINI_DICT.get(XML_XF_NAME)) -> str:
* __out_xf_data(self, prm_name: str) -> tuple:
* __out_xf_data_color_speed(self, prm_name: str=flam3h_iterator_prm_names().shader_speed) -> tuple:
* __out_xf_name(self) -> tuple:
* __out_finalxf_name(self) -> str:
* __out_xf_pre_blur(self) -> tuple:
* __out_xf_xaos(self) -> tuple:
* __out_xf_preaffine(self) -> tuple[tuple, tuple, tuple]:
* __out_xf_postaffine(self) -> tuple[tuple, tuple, tuple]:
* __out_finalxf_preaffine(self) -> tuple[str, str, str]:
* __out_finalxf_postaffine(self) -> tuple[str, str, str]:
* __out_palette_hex(self) -> str:
* __out_flame_data_flam3h_hsv(self, prm_name = CP_RAMP_HSV_VAL_NAME) -> str | bool:
* __out_flame_data_flam3h_mb_val(self, prm_name: str = '') -> str | bool:
* __out_flame_data_flam3h_toggle(self, toggle: bool) -> str:
* __out_flame_palette_lookup_samples(self) -> str | bool:
    """

    __slots__ = ("_kwargs", "_node", 
                 "_flam3h_iter_prm_names", "_flam3h_iter", "_flam3h_iter_FF", "_flam3h_do_FF", 
                 "_iter_count", "_palette", "_palette_hsv_do", "_palette_plus_do", "_f3h_affine", "_xm", 
                 "_flam3h_rip", "_flam3h_mb_do", "_flam3h_f3c", "_flam3h_cp_lookup_samples")

    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """ 
        self._kwargs: dict = kwargs
        self._node = kwargs['node']
        
        self._flam3h_iter_prm_names = flam3h_iterator_prm_names()
        self._flam3h_iter = flam3h_iterator()
        self._flam3h_iter_FF = flam3h_iterator_FF()
        self._flam3h_do_FF: int = self._node.parm(PREFS_PVT_DOFF).eval()
        
        self._iter_count: int = self._node.parm(FLAME_ITERATORS_COUNT).eval()
        self._palette: hou.Ramp = self._node.parm(CP_RAMP_SRC_NAME).evalAsRamp()
        self._palette_hsv_do: int = self._node.parm(OUT_HSV_PALETTE_DO).eval()
        self._palette_plus_do: int = self._node.parm(PREFS_PALETTE_256_PLUS).eval()
        if self._palette_hsv_do:
            # Update hsv ramp before storing it.
            flam3h_palette_utils(self.kwargs).palette_cp()
            self._palette: hou.Ramp = self._node.parm(CP_RAMP_HSV_NAME).evalAsRamp()
        self._f3h_affine: int = self._node.parm(OUT_FLAM3H_AFFINE_STYLE).eval()
        self._xm: int = self._node.parm(PREFS_XAOS_MODE).eval()
        
        # custom to FLAM3H only
        self._flam3h_rip: int = self._node.parm(PREFS_PVT_RIP).eval()
        self._flam3h_mb_do: int = self._node.parm(MB_DO).eval()
        self._flam3h_f3c: int = self._node.parm(PREFS_PVT_F3C).eval()
        self._flam3h_cp_lookup_samples: int = self._node.parm(CP_RAMP_LOOKUP_SAMPLES).evalAsInt()
        
    
    @staticmethod
    def out_render_curves_set_data_defaults(node: hou.SopNode) -> None:
        """Set the defaults values into the color correction curves data parameters.

        Args:
            node(hou.SopNode): This FLAM3H node

        Returns:
            (None):
        """
        # render curves
        node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVES): OUT_XML_FLAME_RENDER_CURVES_DEFAULT}) # type: ignore
        node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_OVERALL): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
        node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_RED): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
        node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_GREEN): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
        node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_BLUE): OUT_XML_FLAME_RENDER_CURVE_DEFAULT}) # type: ignore
        
        
    @staticmethod
    def out_render_curves_retrive_data(node: hou.SopNode) -> None:
        """Retrieve the data from color correction curves data parameters
        and copy it into the corresponding color correction curves UI parameters.

        Args:
            node(hou.SopNode): This FLAM3H node

        Returns:
            (None):
        """
        # render curves data
        prm_data: dict[str, hou.Parm] = {'prm_curves': node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVES)), # type: ignore
                                         'prm_curve_overall': node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_OVERALL)), # type: ignore
                                         'prm_curve_red': node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_RED)), # type: ignore
                                         'prm_curve_green': node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_GREEN)), # type: ignore
                                         'prm_curve_blue': node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_BLUE)), # type: ignore
                                        }
        
        # render curves parms
        prm_ui: dict[str, hou.Parm] = { 'prm_curves': node.parm(OUT_RENDER_PROPERTIES_CURVES), # type: ignore
                                        'prm_curve_overall': node.parm(OUT_RENDER_PROPERTIES_CURVE_OVERALL), # type: ignore
                                        'prm_curve_red': node.parm(OUT_RENDER_PROPERTIES_CURVE_RED), # type: ignore
                                        'prm_curve_green': node.parm(OUT_RENDER_PROPERTIES_CURVE_GREEN), # type: ignore
                                        'prm_curve_blue': node.parm(OUT_RENDER_PROPERTIES_CURVE_BLUE) # type: ignore
                                        }
        
        # Unlock, Set and Lock again
        [prm.lock(False) for prm in prm_ui.values()]
        [prm.deleteAllKeyframes() for prm in prm_ui.values()]
        [prm_ui.get(key).set(prm_data.get(key).eval()) for key in prm_ui.keys()] # type: ignore
        [prm.lock(True) for prm in prm_ui.values()]
        
        
    @staticmethod
    def out_render_curves_set_and_retrieve_defaults(node: hou.SopNode) -> None:
        """Set the defaults values into the color correction curves data parameters
        and copy it into the correcsponding color correction curves UI parameters.

        Args:
            node(hou.SopNode): This FLAM3H node

        Returns:
            (None):
        """
        out_flame_utils.out_render_curves_set_data_defaults(node)
        out_flame_utils.out_render_curves_retrive_data(node)
        node.setParms({OUT_LABEL_CC_DEFAULTS_MSG: 'Defaults'}) # type: ignore
        node.setParms({OUT_TOGGLE_CC_DEFAULTS_MSG: 0}) # type: ignore
    
    
    @staticmethod
    def out_render_curves_compare(node: hou.SopNode, mode: bool = False) -> bool:
        """Compare the current UI CC curves with the CC CURVES DATA.
        Two modes:  (mode: False) will compare if they are default values(return: True) or not(return: False)
                    (mode: True) will compare the UI data with the CC CURVES DATA and check if they are identical(return: True) or not(return: False)

        Args:
            node(hou.SopNode): this FLAM3H node
            mode(bool): Default to False.
                * (mode: False) will compare if they are default values( return: True) or not(return: False)
                * (mode: True) will compare the UI data with the CC CURVES DATA and check if they are identical(return: True) or not(return: False)

        Returns:
            (bool): True or Flase
        """
        cc_o: str = str(node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_OVERALL)).eval()).strip()
        cc_r: str = str(node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_RED)).eval()).strip()
        cc_g: str = str(node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_GREEN)).eval()).strip()
        cc_b: str = str(node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_BLUE)).eval()).strip()
        if not mode:
            if cc_o in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL and cc_r in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL and cc_g in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL and cc_b in OUT_XML_FLAME_RENDER_CURVE_DEFAULT_ALL: return True
            else: return False
        else:
            cc_o_ui: str = str(node.parm(OUT_RENDER_PROPERTIES_CURVE_OVERALL).eval()).strip()
            cc_r_ui: str = str(node.parm(OUT_RENDER_PROPERTIES_CURVE_RED).eval()).strip()
            cc_g_ui: str = str(node.parm(OUT_RENDER_PROPERTIES_CURVE_GREEN).eval()).strip()
            cc_b_ui: str = str(node.parm(OUT_RENDER_PROPERTIES_CURVE_BLUE).eval()).strip()
            if cc_o != cc_o_ui or cc_r != cc_r_ui or cc_g != cc_g_ui or cc_b != cc_b_ui: return False
            else: return True
    
    
    @staticmethod
    def out_render_curves_compare_and_set_toggle(node: hou.SopNode) -> None:
        """Check if the color correction curves data parameters are at their default values
        and set the UI heading label parameter accordingly.

        Args:
            node(hou.SopNode): This FLAM3H node

        Returns:
            (None):
        """
        if out_flame_utils.out_render_curves_compare(node):
            node.setParms({OUT_LABEL_CC_DEFAULTS_MSG: 'Defaults'}) # type: ignore
            node.setParms({OUT_TOGGLE_CC_DEFAULTS_MSG: 0}) # type: ignore
        else:
            node.setParms({OUT_LABEL_CC_DEFAULTS_MSG: 'Modified: Click to Reset'}) # type: ignore
            node.setParms({OUT_TOGGLE_CC_DEFAULTS_MSG: 1}) # type: ignore
    
    
    @staticmethod
    def out_render_curves_set_defaults_on_load(node: hou.SopNode):
        """This is for backward compatibility when loading hip files with older version of FLAM3H nodes.
        it will set proper color correction curves default values if needed.

        Args:
            node(hou.SopNode): This FLAM3H node

        Returns:
            (None):
        """
        # render curves data
        prm_curves_data: hou.Parm = node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVES))
        prm_data: dict[str, hou.Parm] = {'prm_curve_overall': node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_OVERALL)), # type: ignore
                                         'prm_curve_red': node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_RED)), # type: ignore
                                         'prm_curve_green': node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_GREEN)), # type: ignore
                                         'prm_curve_blue': node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_BLUE)), # type: ignore
                                         }
        
        # render curves parms
        prm_curves_ui: hou.Parm = node.parm(OUT_RENDER_PROPERTIES_CURVES) # type: ignore
        prm_ui: dict[str, hou.Parm] = { 'prm_curve_overall': node.parm(OUT_RENDER_PROPERTIES_CURVE_OVERALL), # type: ignore
                                        'prm_curve_red': node.parm(OUT_RENDER_PROPERTIES_CURVE_RED), # type: ignore
                                        'prm_curve_green': node.parm(OUT_RENDER_PROPERTIES_CURVE_GREEN), # type: ignore
                                        'prm_curve_blue': node.parm(OUT_RENDER_PROPERTIES_CURVE_BLUE) # type: ignore
                                        }
        
        # Set the prm data defaults first
        prm_curves_ui.lock(False)
        if len(prm_curves_data.eval()) == 1:
            prm_curves_ui.set(OUT_XML_FLAME_RENDER_CURVES_DEFAULT) # type: ignore
            # Update CC label and toggle to their defaults
            node.setParms({OUT_LABEL_CC_DEFAULTS_MSG: 'Defaults'}) # type: ignore
            node.setParms({OUT_TOGGLE_CC_DEFAULTS_MSG: 0}) # type: ignore
        prm_curves_ui.lock(True)
        [prm_data.get(key).set(OUT_XML_FLAME_RENDER_CURVE_DEFAULT) if len(prm_data.get(key).eval()) == 1 else ... for key in prm_ui.keys()] # type: ignore

        # Set the prm ui defaults
        [prm.lock(False) for prm in prm_ui.values()]
        [prm_ui.get(key).set(OUT_XML_FLAME_RENDER_CURVE_DEFAULT) if len(prm_data.get(key).eval()) == 1 else ... for key in prm_data.keys()] # type: ignore
        [prm.lock(True) for prm in prm_ui.values()]
    
    
    @staticmethod
    def out_auto_add_iter_num(iter_num: int, name: str, autoadd: int, flame: bool = True) -> str:
        """It will check and correct the passed Flame name and add the iteration number to it if needed.
        Additionally, when the "flame" arg is set to False, it will just autocorrect the passed name, to be used for example for the Palette name.

        Args:
            iter_num(int): the current iteration's number
            flame_name(str): The Flame name to check and correct
            autoadd(int): Auto add iter num toggle value (This toggle will eventually be removed from FLAM3H at some point)
            flame(bool): Default to True(Flame). Use False for Palette

        Returns:
            (str): A new name with either the iterations number added to it if needed or corrected or both.
        """

        name = name.strip()
        
        if name:
            
            splt: list | str = ':'
            # Prep an automated Flame/Palette name if no name is provided
            if flame: name_new: str = datetime.now().strftime("Flame_%b-%d-%Y_%H%M%S")
            else: name_new: str = datetime.now().strftime("Palette_%b-%d-%Y_%H%M%S")
            
            rp: list = name.split(splt)
            rp[:] = [item for item in rp if item]
            # Lets make some name checks first
            #
            # if it start with a special character
            if not name[0].isalnum():
                rp = name_new.split(splt)
                rp[:] = [item for item in rp if item]
            # if it end with special character
            elif not name[-1].isalnum():
                
                rp = name.split(splt)
                if len(rp) == 1 and len(rp[0]):
                    item_cleaned: str =''.join(letter for letter in rp[0].strip() if letter.isalnum() or letter in CHARACTERS_ALLOWED_OUT_AUTO_ADD_ITER_NUM)
                    rp = [item_cleaned]
                    
                elif len(rp) > 1:
                    name_new: str = ' '.join(rp[:-1])
                    rp = name_new.split(splt)
                    rp[:] = [item for item in rp if item]
                    
                else:
                    rp = name_new.split(splt)
                    rp[:] = [item for item in rp if item]
            
            is_int: bool = True
            try:
                # if the name is a number, I want to still add the iteration num to it
                # and not evaluate this as integer, even if it is an integer.
                if rp[-1] != name:
                    int(rp[-1].strip())
                else:
                    is_int: bool = False
            except:
                is_int: bool = False
                
            if is_int is False:
                rp_clean: list = [''.join(letter for letter in item.strip() if letter.isalnum() or letter in CHARACTERS_ALLOWED_OUT_AUTO_ADD_ITER_NUM) for item in rp]
                if flame:
                    if autoadd: name_new: str = ' '.join(rp_clean) + FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV + str(iter_num)
                    else: name_new: str = ' '.join(rp_clean)
                    
                else: name_new: str = ' '.join(rp_clean)
                return name_new.strip()
            
            else:
                splt = name.split(":")
                if len(splt) > 1:
                    if flame: 
                        if autoadd: return ''.join([item.strip() for item in splt[:-1]]) + FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV + str(iter_num)
                        else: return ''.join([item.strip() for item in splt[:-1]])
                        
                    else: return ''.join([item.strip() for item in splt[:-1]])
                    
                else:
                    return name
                
        else:
            return name

    
    @staticmethod 
    def out_auto_change_iter_num(iter_num: int, flame_name: str, autoadd: int) -> str:
        """It will check the passed Flame name 
        and update the iteration number when changing iterations.
        If no iteration number is present in the passed Flame name
        it will add it to the end of the Flame name.

        Args:
            iter_num(int): the current iteration's number
            flame_name(str): The Flame name to check
            autoadd(int): Auto add iter num toggle value

        Returns:
            (str): A new Flame name with the iter num updated/added if needed.
        """
        if autoadd:
            
            flame_name = flame_name.strip()
            if flame_name:
                
                flame_name = out_flame_utils.out_auto_add_iter_num(iter_num, flame_name, autoadd)
                rp: tuple = flame_name.rpartition(FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV)

                is_int: bool = False
                try:
                    if rp[-1] != flame_name:
                        int(rp[-1])
                        is_int = True
                    else:
                        pass
                except: pass
                
                if is_int:
                    flame_name_changed: str = ''.join(rp[:-1]) + str(iter_num)
                    return flame_name_changed
                else:
                    return flame_name
            else:
                return flame_name
        else:
            return flame_name
        
        
    @staticmethod 
    def out_remove_iter_num(flame_name: str) -> str:
        """Remove the iterations number from the Flame name if any.

        Args:
            flame_name(str): The Flame name to check

        Returns:
            (str): A new Flame name without the iter num if any.
        """
            
        flame_name = flame_name.strip()
        
        if flame_name:
            
            rp: tuple = flame_name.rpartition(FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV)

            is_int: bool = False
            try:
                if rp[-1] != flame_name:
                    int(rp[-1])
                    is_int = True
                else:
                    pass
            except: pass
            
            if is_int:
                return ''.join(rp[:-2])
            else:
                return flame_name
        else:
            return flame_name
        
        
    @staticmethod
    def out_flame_default_name(node: hou.SopNode, autoadd: int) -> str:
        """Create a default name to be used for the output Flame file path.

        Args:
            node(hou.SopNode): Current FLAM3H houdini node
            autoadd(int): Autoadd ON/OFF value. If ON, it will auto add the iteration number to the filename, otherwise not.

        Returns:
            (str): Return a default name composed of today's date and time.
        """
        flame_name: str = datetime.now().strftime("Flame_%b-%d-%Y_%H%M%S")
        iter_num: int = node.parm(GLB_ITERATIONS).eval()
        return out_flame_utils.out_auto_add_iter_num(iter_num, flame_name, autoadd)
    
    
    @staticmethod
    def out_util_round_float(val: float) -> str:
        """remove floating Zeros if it is an integer value ( ex: from '1.0' to '1' )

        Args:
            val(float): The value to remove the floating zeros from

        Returns:
            (str): A value without the floating zeros
        """
        if float(val).is_integer():
            return str(int(float(val)))
        else:
            return str(round(float(val), ROUND_DECIMAL_COUNT))
        
        
    @staticmethod
    def out_util_round_floats(val_list: list[list[str]] | tuple[list]) -> list[str] | list[list[str]] | tuple[str]:
        """remove floating Zeros if it is an integer value ( ex: from '1.0' to '1' ) in a list or tuple of values 

        Args:
            val_list(list[list[str]] | tuple[list]): A collection of values to rounds

        Returns:
            (list[str] | list[list[str]] | tuple[str]): A list/tuple of list[str]/tuple[str] with the rounded values if any
        """    
        return [[str(int(float(i))) if float(i).is_integer() else str(round(float(i), ROUND_DECIMAL_COUNT)) for i in item] for item in val_list]
        
        
    @staticmethod  
    def out_util_check_duplicate_var_section(vars: list) -> bool:
        """Check if any of the iterator sections (PRE, VAR or POST, same for FF) is using a variation multiple times.

        Args:
            vars(list): a section list of used variations

        Returns:
            (bool): True if there are duplicates and False if not.
        """
        result: list = []
        [result.append(x) for x in vars if x not in result]
        if(len(vars) != len(result)):
            return True
        return False
    
    
    @staticmethod
    def __out_util_iterators_vars_duplicate(vars: list) -> list:
        """ NOT USED ANYMORE
        Collect duplicate variation's names per each iterator.

        Args:
            vars(list): List of all variation's list names

        Returns:
            (list): duplicate variation's names per each iterator
        """
        duplicate: list = []
        for iterator in vars:
            v: list = []
            d: list = []
            for var in iterator:
                if var not in v:
                    v.append(var)
                else:
                    if var not in d:
                        d.append(var)
            duplicate.append(d)
        
        return in_flame_utils.in_util_vars_flatten_unique_sorted(duplicate, in_flame_utils.in_util_make_NULL)
    
    
    @staticmethod
    def out_util_vars_duplicate(vars: list) -> list:
        """Collect duplicate variation's names in an iterator.

        Args:
            vars(list): List of all variation's list names

        Returns:
            (list): duplicate variation's names per each iterator
        """
        v: list = []
        d: list = []
        for var in vars:
            if var not in v:
                v.append(var)
            else:
                if var not in d:
                    d.append(var)
        
        return d
    

    @staticmethod
    def out_check_build_file(file_split: tuple[str, str] | list[str], file_name: str, file_ext: str) -> str:
        """Used in conjuction with: def out_check_outpath()
        help to make spelling auto corrections to the provided output file path.

        Args:
            file_split(tuple[str, str] | list[str]): Returns tuple "(head, tail)" where "tail" is everything after the final slash. Either part may be empty
            file_name(str): The input filename to be checked
            file_ext(str): the desired filename extension

        Returns:
            (str): A corrected file path
        """    
        # This code is very old and need some revision ;D
        build_f: str = "/".join(file_split) + file_ext
        build_f_s: list = os.path.split(build_f)[0].split("/")
        build_f_s[:] = [item for item in build_f_s if item]
        # Clean location directories. ( maybe not needed but whatever )
        build_f_s_cleaned: list = [''.join(letter for letter in item if letter.isalnum() or letter in CHARACTERS_ALLOWED) for item in build_f_s]
        # append cleaned file_name
        build_f_s_cleaned.append(''.join(letter for letter in file_name if letter.isalnum() or letter in CHARACTERS_ALLOWED))
        # the file_ext start with a dot so its added as last
        return "/".join(build_f_s_cleaned) + file_ext
    
    
    @staticmethod
    def out_check_outpath_messages(node: hou.SopNode, infile: str, file_new: str, file_ext: str, prx: str) -> None:
        """Print out some messages in the console and in the status bar.

        Args:
            node(hou.SopNode): This FLAM3H node.
            infile(str): THe file path to check.
            file_new(str): The new generated file full path
            file_ext(str): Provide an extension to tell this function if it is a Flame file or a palette file. 
            prx(str): A prefix for an automated file name to be provided for the XML Flame file or a Palette flame file. 'Palette' or 'Flame' (AUTO_NAME_CP: str or AUTO_NAME_OUT: str)

        Returns:
            (None):
        """  
        # Print out proper msg based on file extension
        if OUT_FLAM3_FILE_EXT == file_ext:
            if os.path.isfile(infile) and os.path.exists(infile):
                _MSG: str = f"OUT: You selected an OUT file that is not a {prx} file type."
                print(f"{node.name()}.{_MSG}\n")
                flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG}", 'WARN')
            else:
                if os.path.isdir(os.path.split(file_new)[0]) and not os.path.exists(file_new):
                    if flam3h_general_utils.isLOCK(os.path.split(file_new)[1]):
                        _MSG: str = 'OUT: Flame lib file: LOCKED'
                        flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG}: {file_new}", 'IMP')
                    else:
                        _MSG: str = 'OUT: Save to create this file'
                        flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG}: {file_new}", 'IMP')
        elif OUT_PALETTE_FILE_EXT == file_ext:
            if os.path.isfile(infile) and os.path.exists(infile):
                _MSG: str = f"Palette: You selected an OUT file that is not a {prx} file type."
                print(f"{node.name()}.{_MSG}\n")
                flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG}", 'WARN')
            else:
                if os.path.isdir(os.path.split(file_new)[0]) and not os.path.exists(file_new):
                    if flam3h_general_utils.isLOCK(os.path.split(file_new)[1]):
                        _MSG: str = 'Palette: Flame lib file: LOCKED'
                        flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG}: {file_new}", 'IMP')
                    else:
                        _MSG: str = 'Palette: Save to create this file'
                        flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG}: {file_new}", 'IMP')


    @staticmethod
    def out_check_outpath(node: hou.SopNode, infile: str, file_ext: str, prx: str, out: bool = True, auto_name: bool = True) -> str | bool:
        """Check for the validity of the provided output file path and correct it if needed.
        
        _NOTE:
            This definition was very old and I am improving it.

        Args:
            node(hou.SopNode): Current FLAM3H node.
            infile(str): THe file path to check.
            file_ext(str): Provide an extension to tell this function if it is a Flame file or a palette file. 
            prx(str): A prefix for an automated file name to be provided for the XML Flame file or a Palette flame file. 'Palette' or 'Flame' (AUTO_NAME_CP: str or AUTO_NAME_OUT: str)
            out(int): Default to True. Which Flame tab are we running this from? False for IN tab, True for OUT tab.
            auto_name(bool): Default to: True. When checking the output path you some time do not want to generate a filename and extension, like for example inside the IN file string parameter.
        
        Returns:
            str | bool: Either a corrected/valid file path or False if not valid.
        """
        
        file: str = os.path.expandvars(infile)
        
        # If the input file is valid, just use it as it is
        if prx == AUTO_NAME_CP and flam3h_palette_utils.isJSON_F3H(node, file, False)[-1]: return file
        elif prx == AUTO_NAME_OUT and _xml_tree(file).isvalidtree: return file

        # Otherwise lets be sure to build a proper output path and file name.
        # This will need some more work to make it more sophisticated and remove the unnecessary eventually.
        file_s: list = [''.join(x.split(' ')) for x in os.path.split(file)]
        
        # This toggle should be removed from FLAM3H at some point
        autopath: int = node.parm(PREFS_PVT_AUTO_PATH_CORRECTION).eval()
        if autopath:
            
            # Just in case lets check is a valid location
            if os.path.isdir(file_s[0]) or os.path.isdir(os.path.split(file)[0]):
                
                file_new = ''
                
                if auto_name: new_name: str = datetime.now().strftime(f"{prx}_%b-%d-%Y_%H%M%S")
                else: new_name = ''
                
                filename_s = os.path.splitext(file_s[-1].strip())
                
                if filename_s[-1] == file_ext:
                    # This code is very old and need some revision ;D
                    build_f_s: list = file.split("/")
                    build_f_s[:] = [item for item in build_f_s if item]
                    build_f_s[-1] = ''.join(letter for letter in build_f_s[-1] if letter.isalnum() or letter in CHARACTERS_ALLOWED)
                    file_new: str = "/".join(build_f_s)
                
                elif not filename_s[-1] and filename_s[0]:
                    
                    # this is done in case only the extension is left in the prm field
                    if file_s[-1] in file_ext and file_s[-1][0] == ".":
                        if auto_name: file_new: str = out_flame_utils.out_check_build_file(file_s, new_name, file_ext)
                        else: file_new: str = out_flame_utils.out_check_build_file(file_s, new_name, '')
                        
                    else:
                        
                        if not file_s[-1][0].isalnum():
                            if auto_name: file_new: str = out_flame_utils.out_check_build_file(file_s, new_name, file_ext)
                            else: file_new: str = out_flame_utils.out_check_build_file(file_s, new_name, '')
                            
                        else:
                            file_new: str = out_flame_utils.out_check_build_file(file_s, file_s[-1], file_ext)
                            
                    # Print out proper msg based on file extension
                    out_flame_utils.out_check_outpath_messages(node, file, file_new, file_ext, prx)
                    
                elif not filename_s[-1] and not filename_s[0]:
                    if auto_name: file_new: str = out_flame_utils.out_check_build_file(file_s, new_name, file_ext)
                    else: file_new: str = out_flame_utils.out_check_build_file(file_s, new_name, '')
                
                # this as last for now
                #
                # If there is a file extension and it match part or all of the file_ext string.
                #
                # This will execute only if the string match at the beginning of the file extension
                # otherwise the above if/elif statements would have executed already.
                elif len(filename_s) > 1 and filename_s[-1] in file_ext:
                    file_new: str = out_flame_utils.out_check_build_file(file_s, filename_s[0], file_ext)

                else:
                    if not os.path.exists(file):
                        file_new: str = out_flame_utils.out_check_build_file(file_s, filename_s[0], file_ext)
                
                if file_new:
                    # This is really a patch instead of rewriting this entire definition...
                    # Will allow network paths to work as well.
                    file_dir_out: str = os.path.split(file)[0]
                    # Lets check if the original output path is a valid location
                    if os.path.isdir(file_dir_out):
                        if f"{file_dir_out}"[-1] == '/': out_file = f"{file_dir_out}{os.path.split(file_new)[-1]}"
                        else: out_file = f"{file_dir_out}/{os.path.split(file_new)[-1]}"
                    # Otherwise lets check if the generated output path is a valid location
                    elif os.path.isdir(os.path.split(file_new)[0]): out_file = file_new
                    # Otherwise get the expanded and corrected infile location and append the new filename to it
                    else:
                        if f"{file_s[0]}"[-1] == '/': out_file = f"{file_s[0]}{os.path.split(file_new)[-1]}"
                        else: out_file = f"{file_s[0]}/{os.path.split(file_new)[-1]}"
                    
                    out_flame_utils.out_check_outpath_messages(node, file, file_new, file_ext, prx)
                    return out_file
                        
                else: return False

            else:
                if file:
                    if OUT_FLAM3_FILE_EXT == file_ext:
                        if out: _MSG: str = f"OUT: Select a valid OUT flame directory location."
                        else: _MSG: str = f"IN: Select a valid IN flame file path."
                        flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG}", 'WARN')
                else:
                    # If the path string is empty we do not want to print out
                    flam3h_general_utils.set_status_msg('', 'MSG')
                return False
            
        # The following else statement is not really needed anymore
        # but until I do not remove the hidden toggle I leave it here.
        else:
            # just check if the user input is a valid location
            if os.path.isdir(file_s[0]) or os.path.isdir(os.path.split(file)[0]):
                return infile
            else:
                if file:
                    if OUT_FLAM3_FILE_EXT == file_ext:
                        if out: _MSG: str = f"OUT: Select a valid OUT flame directory location."
                        else: _MSG: str = f"IN: Select a valid IN flame file path."
                        flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG}", 'WARN')
                    elif OUT_PALETTE_FILE_EXT == file_ext:
                        _MSG: str = f"PALETTE: Select a valid OUT directory location."
                        flam3h_general_utils.set_status_msg(f"{node.name()}.{_MSG}", 'WARN')
                else:
                    # If the path string is empty we do not want to print out
                    flam3h_general_utils.set_status_msg('', 'MSG')
                return False
            
 
    @staticmethod
    def out_affine_rot(affine: list[tuple[str] | list[str]], angleDeg: float) -> list[list[str] | tuple[str]]:
        """Every affine has an Angle parameter wich rotate the affine values internally.
        When we save out an iterator that use the angle parameter, we need to transform the affine by this angle
        and export the resulting values out so we can get the same result once we load it back.

        Args:
            affine( list[tuple[str] | list[str]]): X, Y, O afffine component
            angleDeg(float): a float value that represent the angle in degrees ( The iterator.affine's angle parameter )

        Returns:
            (list[list[str] | tuple[str]]): A new affine list of tuples ( (X), (Y), (O) ) rotated by the angle amount.
        """
        if angleDeg != 0.0:      
            angleRad = hou.hmath.degToRad(angleDeg) # type: ignore
            m2 = hou.Matrix2((affine[0], affine[1]))
            rot = hou.Matrix2(((cos(angleRad), -(sin(angleRad))), (sin(angleRad), cos(angleRad))))
            new: tuple = (m2 * rot).asTupleOfTuples()
            return [new[0], new[1], affine[2]]
        else:
            return affine


    @staticmethod
    def out_xaos_cleanup(xaos: list[str] | list[list[str]] | tuple[str]) -> list[list[str]]:
        """Remove all inactive iterators from each xaos weight list.

        Args:
            xaos (list[str] | list[list[str], tuple[str]]): All iterators xaos values.

        Returns:
           (list[list[str]]): an iterator Xaos cleaned up from the inactive iterator's values
        """
        xaos_cleaned: list = []
        for x in xaos:
            invert = x[::-1]
            trace: int = 0
            for idx in range(len(x)): # for idx, item in enumerate(x):
                _idx: int = idx-trace
                if invert[_idx] == '1':
                    invert.pop(_idx) # type: ignore
                    trace = trace + 1
                else:
                    break
            xaos_cleaned.append(invert[::-1])
        return xaos_cleaned
    

    @staticmethod
    def out_xaos_collect(node: hou.SopNode, iter_count: int, prm: str) -> list[list[str]]:
        """Collect all xaos command string weights.
        Provide also a form of Undo in the case we enter non numeric characters instead.
        
        XAOS COMMAND OPTIONS:

        * If you type a non-numeric character in any of the xaos's weights,
        FLAM3H will undo to what you had before.

        * If you dnt use the “ xaos: ” keywork at the beginning,
        FLAM3H will undo to what you had before.

        * If you type a number,
        the entire xaos string will be reset to all weights set to that number.

        * If you type a negative number, it will be reset to a value of: 1

        Args:
            node(hou.SopNode): FLAM3H node
            iter_count(int): Iterator's count
            prm(str): xaos varnote parameter

        Returns:
            (list[list[str]]): A list of xaos list[str] of values
        """   

        val: list = []
        val_prev: list | None = flam3h_iterator_utils.auto_set_xaos_data_get_XAOS_PREV(node)
        
        for iter in range(iter_count):
            
            # Get this iterator Xoas command string
            iter_xaos: str = node.parm(f"{prm}_{iter + 1}").eval()
            
            # If the xaos string is not empty
            if iter_xaos:
                
                strip: list[str] = iter_xaos.split(':')
                
                # if the first element of the strip is: "xaos"
                if strip[0].lower().replace(" ", "") == 'xaos':
                    
                    try:
                        _xaos: list = strip[1:iter_count + 1]
                        
                        if _xaos[0] and val_prev is not None and len(val_prev) == iter_count:
                            _xaos_strip: list = [str(float((in_flame.xf_val_cleanup_str(str(x), val_prev[iter][idx])))) if float(in_flame.xf_val_cleanup_str(str(x), val_prev[iter][idx])) >= 0 else '1' for idx, x in enumerate(_xaos)]
                        else:
                            # Otherwise use the safer version.
                            # This is used every time we add or remove an iterator or when loading Flames with different iterator's count than what we currently have.
                            _xaos_strip: list = [str(float(str(x).strip())) if float(str(x).strip()) >= 0 else '1' for x in _xaos if x]
                            
                        val.append([float(x.strip()) for x in _xaos_strip])
                        
                    except:
                        
                        if val_prev is not None:
                            val.append(val_prev[iter])
                        else:
                            # Otherwise reset to all values of 1
                            val.append([])
                            
                # If the split fail to validate and it just start with the word: 'xaos'
                elif iter_xaos.lower().replace(" ", "").startswith('xaos'):
                    
                    if val_prev is not None:
                        # retrive from the history instead ( Undo )
                        val.append(val_prev[iter])
                    else:
                        # Otherwise reset to all values of 1
                        val.append([])
                        
                else:

                    isNUM: bool = False
                    iter_xaos_clean: str = in_flame.xf_val_cleanup_str(iter_xaos, '@') # default_val here is set to an invalid char to make it fail on purpose if needed
                    
                    try:
                        if isinstance(float(iter_xaos_clean), float):
                            isNUM = True
                    except: pass
                    
                    # If a number is typed, fill all xaos weights with that number.
                    if isNUM:
                        v: list = [str((float(iter_xaos_clean))) if float(iter_xaos_clean) >= 0 else '1' for x in range(iter_count)]
                        val.append(v)
                    else:
                        # if we entered an invalid string,
                        # retrive from the history instead ( Undo )
                        if val_prev is not None:
                            val.append(val_prev[iter])
                        else:
                            # Otherwise reset to all values of 1
                            val.append([])
                            
            else:
                # Otherwise reset to all values of 1
                val.append([])
                
        return val


    @staticmethod
    def out_xaos_collect_vactive(node: hou.SopNode, fill: list, prm: str) -> list[list[str]]:
        """Check for any NO-active iterators and account for those.

        Args:
            node(hou.SopNode): FLAM3H node.
            fill(list): List representing all xaos weights.
            prm(str): iterator vactive parameter.

        Returns:
            (list[list[str]]): return a list of list[str] with the NO-active iterators taken into consideration.
        """    
        xaos_no_vactive: list = []
        for x in fill:
            collect: list = [str(item) for idx, item in enumerate(x) if node.parm(f"{prm}_{idx + 1}").eval()]
            if collect:
                xaos_no_vactive.append(collect)
            else:
                xaos_no_vactive.append([])
        return xaos_no_vactive


    @staticmethod
    def _out_pretty_print(current: lxmlET.Element, parent: lxmlET.Element | None = None, index: int = -1, depth: int = 0) -> None: #type: ignore
        """Reformat the XML data in a pretty way.

        Args:
            current(lxmlET._Element): The Flame XML root we want to reformat.
            parent(lxmlET.Element | None): Default to None.
            index(int): _description_. Defaults to -1.
            depth(int): _description_. Defaults to 0.
        """
        [out_flame_utils._out_pretty_print(node, current, i, depth + 1) for i, node in enumerate(current)]
        if parent is not None:
            if index == 0:
                parent.text = '\n' + ('  ' * depth)
            else:
                parent[index - 1].tail = '\n' + ('  ' * depth)
            if index == len(parent) - 1:
                current.tail = '\n' + ('  ' * (depth - 1))
                
                
    @staticmethod
    def menu_out_presets_loop(menu: list, i: int, item: str) -> None:
        """This is specifically to be run inside a list comprehension.

        Args:
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            menu.append(f"{FLAM3H_ICON_STAR_FLAME_SAVE_ENTRIE}  {item}     ")


    @staticmethod
    def menu_out_presets_loop_enum(menu: list, i: int, item: str) -> None:
        """This is specifically to be run inside a list comprehension.

        Args:
            menu(list): the menu list to populate.
            i(int): The outer loop index/iteration.
            item(str): The outer loop item at index/iteration.

        Returns:
            (None):
        """  
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            menu.append(str(i)) # This menu is a string parameter so I do believe this is the correct way
            enum_label: str = str(i + 1) # start count from 1
            menu.append(f"{FLAM3H_ICON_STAR_FLAME_SAVE_ENTRIE}  {enum_label}:  {item}     ")
        
    
    @staticmethod
    def out_collect_var_section_names(node: hou.SopNode, var_section: str = "VAR") -> list[str] | None:
        """Collect all the variation's names inside any of the available iterator's sections (PRE, VAR, POST)
        
        Args:
            node(hou.SopNode): This FLAM3H node
            var_section(str): Default to: 'VAR'. Desired variation's section to query, Can be one of: 'PRE', 'VAR' or 'POST' keynames.

        Returns:
            (list[str] | None): List of used variations in this iterator/xform section
        """
        # Build var parameter's sections
        f3h_iter = flam3h_iterator()
        prm_sections_T: dict[str, tuple] = {'VAR': f3h_iter.sec_varsT, 'PRE': f3h_iter.sec_prevarsT, 'POST': f3h_iter.sec_postvarsT}
        prm_sections_W: dict[str, tuple] = {'VAR': f3h_iter.sec_varsW, 'PRE': f3h_iter.sec_prevarsW[1:], 'POST': f3h_iter.sec_postvarsW}
        
        # Get correct parameter's names based on the desired var section
        T_tuple: tuple | None = prm_sections_T.get(var_section)
        W_tuple: tuple | None = prm_sections_W.get(var_section)
        
        if T_tuple is not None and W_tuple is not None:
            names: list = []
            for iter in range(node.parm(FLAME_ITERATORS_COUNT).eval()):
                _MP_IDX: str = str(int(iter + 1))
                for idx, prm in enumerate(W_tuple):
                    prm_w: float = node.parm(f"{prm[0]}{_MP_IDX}").eval()
                    if prm_w != 0:
                        v_type: int = node.parm(f"{T_tuple[idx]}{_MP_IDX}").eval()
                        names.append(in_flame_utils.in_get_dict_key_from_value(VARS_FLAM3_DICT_IDX, v_type))
                    
            return names
        else:
            return None
        
    
    @staticmethod
    def out_collect_var_section_names_dict(node: hou.SopNode, mode: int = False, var_section = "VAR") -> dict[str, list[str]] | bool:
        """Collect all the variation's names inside any of the available sections (PRE, VAR, POST)
        They will be built inside a dict with the keys representing the irterator number and the value the used variations collected inside a list.
        For the FF, the dictionary key will always be 'FF'
        
        
        Args:
            node(hou.SopNode): FLAM3H node
            mode(bool): Default to: 'False'. False for iterators and True for FF.
            var_section(str): Default to: 'VAR'. Desired variation's section to query, Can be one of: 'PRE', 'VAR' or 'POST' keynames.

        Returns:
            (dict[str, list[str]] | bool): A dictionary of used variations in this iterator/xform/FF or False if none in the desired section (VAR, PRE, POST)
        """
        # Build var parameter's sections
        if not mode:
            # Iterator
            f3h_iter = flam3h_iterator()
            prm_sections_T: dict[str, tuple] = {'VAR': f3h_iter.sec_varsT, 'PRE': f3h_iter.sec_prevarsT, 'POST': f3h_iter.sec_postvarsT}
            prm_sections_W: dict[str, tuple] = {'VAR': f3h_iter.sec_varsW, 'PRE': f3h_iter.sec_prevarsW[1:], 'POST': f3h_iter.sec_postvarsW}
        else:
            # FF
            f3h_iter_FF = flam3h_iterator_FF()
            prm_sections_T: dict[str, tuple] = {'VAR': f3h_iter_FF.sec_varsT_FF, 'PRE': f3h_iter_FF.sec_prevarsT_FF, 'POST': f3h_iter_FF.sec_postvarsT_FF}
            prm_sections_W: dict[str, tuple] = {'VAR': f3h_iter_FF.sec_varsW_FF, 'PRE': f3h_iter_FF.sec_prevarsW_FF, 'POST': f3h_iter_FF.sec_postvarsW_FF}
        
        # Get correct parameter's names based on the desired var section and mode
        T_tuple: tuple | None = prm_sections_T.get(var_section)
        W_tuple: tuple | None = prm_sections_W.get(var_section)
        
        # Just double checking
        if T_tuple is not None and W_tuple is not None:

            names_idx: dict[str, list[str]] = {}
            
            if mode:
                # FF
                if node.parm(PREFS_PVT_DOFF).eval():
                    
                    _MP_IDX = 'FF'
                    names_collect_values: list = []
                    for idx, prm in enumerate(W_tuple):
                        prm_w: float = node.parm(f"{prm[0]}").eval()
                        if prm_w != 0:
                            v_type: int = node.parm(f"{T_tuple[idx]}").eval()
                            var_name: str = in_flame_utils.in_get_dict_key_from_value(VARS_FLAM3_DICT_IDX, v_type)
                            names_collect_values.append(var_name)
                        
                    if names_collect_values:   
                        names_idx[_MP_IDX] = names_collect_values
                        
                    if not names_idx: return False
                    else: return names_idx
                    
                else: return False
                
            else:
                # iterators
                for iter in range(node.parm(FLAME_ITERATORS_COUNT).eval()):
                    _MP_IDX = str(int(iter + 1))
                    names_collect_values: list = []
                    for idx, prm in enumerate(W_tuple):
                        prm_w: float = node.parm(f"{prm[0]}{_MP_IDX}").eval()
                        if prm_w != 0:
                            v_type: int = node.parm(f"{T_tuple[idx]}{_MP_IDX}").eval()
                            var_name: str = in_flame_utils.in_get_dict_key_from_value(VARS_FLAM3_DICT_IDX, v_type)
                            names_collect_values.append(var_name)
                        
                    if names_collect_values:   
                        names_idx[_MP_IDX] = names_collect_values

                if not names_idx: return False
                else: return names_idx
        else:
            return False
        
        
    @staticmethod
    def out_buil_xf_names(f3d: out_flame_xforms_data) -> tuple:
        """Build the XML Flame iterator's names to account for inactive ierators if any.
        If all are active or if an iterator has a custom name nothing will be changed.

        Args:
            (self):
            f3d(out_flame_xforms_data): Class to pull the data from.

        Returns:
            (bool): A tuple of either the corrected names or the untouched ones.
        """
        
        new_names: list = []
        if '0' in f3d.xf_vactive:
            iter_idx = 1
            for mp_idx in range(f3d.iter_count):
                if int(f3d.xf_vactive[mp_idx]):
                    if flam3h_iterator_utils.flam3h_iterator_is_default_name(f3d.xf_name[mp_idx]):
                        new_names.append(f"iterator_{iter_idx}")
                        iter_idx = iter_idx + 1
                    else:
                        new_names.append(f3d.xf_name[mp_idx])
                else:
                    new_names.append('OFF')
                    
            return tuple(new_names)
        
        else:
            return tuple( [f"iterator_{mp_idx + 1}" if flam3h_iterator_utils.flam3h_iterator_is_default_name(f3d.xf_name[mp_idx]) else f3d.xf_name[mp_idx] for mp_idx in range(f3d.iter_count)] ) # type: ignore


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
    def flam3h_iter_prm_names(self):
        return self._flam3h_iter_prm_names
    
    @property
    def flam3h_iter(self):
        return self._flam3h_iter
    
    @property
    def flam3h_iter_FF(self):
        return self._flam3h_iter_FF
    
    @property
    def flam3h_do_FF(self):
        return self._flam3h_do_FF

    @property
    def iter_count(self):
        return self._iter_count

    @property
    def palette(self):
        return self._palette
    
    @property
    def palette_hsv_do(self):
        return self._palette_hsv_do
    
    @property
    def palette_plus_do(self):
        return self._palette_plus_do
    
    @property
    def f3h_affine(self):
        return self._f3h_affine
    
    @property
    def xm(self):
        return self._xm
    
    # custom to FLAM3H only
    
    @property
    def flam3h_mb_do(self):
        return self._flam3h_mb_do
    
    @property
    def flam3h_f3c(self):
        return self._flam3h_f3c
    
    @property
    def flam3h_rip(self):
        return self._flam3h_rip
    
    @property
    def flam3h_cp_lookup_samples(self):
        return self._flam3h_cp_lookup_samples


    def out_palette_256_plus_check(self) -> None:
        """When activating the PREFS option: palette 256+ toggle,
        let the user knows if the current palette posses enough colors and give some infos.

        Args:
            (self):

        Returns:
            (None):
        """
        node = self.node
        prm_prefs_256_plus = self.kwargs['parm']
        rmp_src: hou.Ramp = node.parm(CP_RAMP_SRC_NAME).evalAsRamp()
        if prm_prefs_256_plus.eval():
            if len(rmp_src.keys()) <= 256:
                _MSG: str = f"PALETTE 256+ ACTIVE but the CP palette do not have more than 256 color keys."
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG} The Flame will be saved with a Palette sampled at 256 color keys, which is the standard for fractal flames.", 'IMP')
            else:
                _MSG: str = f"OUT palette 256+: ON"
                flam3h_general_utils.flash_message(node, _MSG)
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
        else:
            _MSG: str = f"OUT palette 256+: OFF"
            flam3h_general_utils.flash_message(node, _MSG)
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')


    def out_presets_get_selected_menu_label(self) -> str | None:
        """Get the currently selected OUT preset menu label string.

        Args:
            (self):

        Returns:
            (str | None): The selected menu preset menu label string if any or None
        """
        node = self.node

        if node.parm(OUT_PVT_ISVALID_FILE).eval():
            toggle_PREFS_ENUMERATE_MENU: int = node.parm(PREFS_ENUMERATE_MENU).eval()
            preset_id: int = int(node.parm(OUT_PRESETS).eval())
            menu_label: str = str(node.parm(OUT_PRESETS).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_FLAME_SAVE_ENTRIE)[-1].strip()

            if toggle_PREFS_ENUMERATE_MENU:
                # We are using "str.lstrip()" because the preset name has been "str.strip()" already in the above line.
                # and there are only the leading white spaces left from the menu enumaration index number string to remove.
                flame_name: str = ':'.join(str(menu_label).split(':')[1:]).lstrip()
            else:
                flame_name: str = menu_label
                
            return flame_name
        
        else:
            return None
    
    
    def out_presets_copy_menu_label_callback(self) -> None:
        """Get the currently selected OUT preset menu label string and copy it into the OUT Flame name string field.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        node = self.node
        kwargs: dict = self.kwargs
        
        if kwargs['ctrl']:
            flam3h_ui_msg_utils(kwargs).ui_OUT_presets_name_infos()
        else:
            if node.parm(OUT_PVT_ISVALID_FILE).eval():
                menu_label: str | None = self.out_presets_get_selected_menu_label()
                if menu_label is not None:
                    flame_name: str = self.out_remove_iter_num(menu_label)
                    iter_num: int = node.parm(GLB_ITERATIONS).eval()
                    autoadd: int = node.parm(OUT_AUTO_ADD_ITER_NUM).eval()
                    flame_name_new: str = self.out_auto_add_iter_num(iter_num, flame_name, autoadd)
                    node.setParms({OUT_FLAME_PRESET_NAME: flame_name_new})
                    
                    _MSG: str = f"{node.name()}: COPY Flame name: {flame_name_new}"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    flam3h_general_utils.flash_message(node, f"{flame_name_new}")
                    
                else:
                    _MSG: str = f"{node.name()}: COPY Flame name: Select an existing preset name. There are no presets to copy the name from."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            else:
                _MSG: str = f"Load a valid OUT flame file first"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG} to COPY its Flame preset names into the Flame name string parameter.", 'WARN')
                flam3h_general_utils.flash_message(node, f"{_MSG}")
                
                
    def out_palette_keys_count(self, palette_plus: int, keys: int, type: int, _MSG = True) -> str:
        """This is used to find the number of colors we want to export when saving out a Flame file.
        We need to always export as many colors to include the current color keys count in the palette based on a predefined set of value:
        So for example, if the current palette posses 270 color keys, we will export using the closest but greater menu entry whitch is: 512 (the smaller being: 256).
        The minimum will always be clamped at: 256

        Args:
            (self):
            palette_plus(bool): "save palette 256+" toggle parameter value.
            keys(int): number of color keys in the palette.
            type(int): 0 for a Flame and 1 for a Palette.
            _MSG:(bool): Print a warning message or not. Default to: True

        Returns:
            (str): number of color to export
        """  

        if palette_plus:
            if keys <= 1024:
                if keys <= 256:
                    if not type:
                        # For a Flame
                        return PALETTE_COUNT_256
                    else:
                        # For a palette
                        return flam3h_palette_utils.get_ramp_keys_count(self.palette)
                else:
                    return str(flam3h_palette_utils.find_nearest_idx(PALETTE_OUT_MENU_OPTIONS_PLUS, keys))
            else:
                # Otherwise clamp to 1024 color keys
                if _MSG:
                    print(f"Warning:\n{self.node.name()}: the palette exceed the allowed amount of color keys and it has been clamped at: 1024\n")
                return PALETTE_COUNT_1024
        else:
            # Otherwise always export the Flame with 256 color palette
            return PALETTE_COUNT_256


    def __menu_sensor_resolution(self) -> list:
        """ NOT USED ANYMORE
        and it has been prefixed with two underscores (__)
        as the menu is now pre computed inside: MENU_SENSOR_RESOLUTIONS
        I leave it here for future needs to re-generate the menu with new entries.
        
        Build sensor resolution menu parameter with a list of options.
        
        Args:
            (self):
            
        Returns:
            (list): Return a menu
        """

        outedit = self.node.parm(OUT_RENDER_PROPERTIES_EDIT).eval()
        menu: list = []
        menuitems: tuple = ()
        if outedit:
            menuitems: tuple = ("", "640x480", "HDTV 720", "HDTV 1080", "HDTV 2160 (4K)", # 1 2 3 4
                                "", "NTSC", "NTSC D1", "PAL", "PAL 16:9 (1 to 1)", # 6 7 8 9
                                "", "Full Ap 4K", "Full Ap 2K", "Acad 4K", "Acad 2K", "Scope 4K", "Scope 2K", "Vista 2K", # 11 12 13 14 15 16 17
                                "", "256^2", "512^2", "1024^2", "2048^2", "4096^2", ""  ) # 19 20 21 22 23
        else:
            menuitems: tuple = ( "",)
            
        for i, item in enumerate(menuitems):
            menu.append(i)
            menu.append(item)
        return menu
    
    
    def menu_sensor_resolution(self) -> list:
        """ Pre computed menu: MENU_SENSOR_RESOLUTIONS
        The old sensor resolution menu definition has been renamed to: def __menu_sensor_resolution(self) -> list: (just above)
        
        Output sensor resolution menu parameter with a list of options.
        
        Args:
            (self):
            
        Returns:
            (list): Return a menu
        """
        return MENU_OUT_SENSOR_RESOLUTIONS


    def menu_sensor_resolution_set(self, update: bool=True) -> None:
        """Set sensor resolution parameter based on user choice.
        
        Args:
            (self):
            update(bool): True or False if we want to update the OUT Sensor front viewer
            
        Returns:
            (None):
        """
        node = self.node
        sel: int = int(node.parm(OUT_RENDER_PROPERTIES_RES_PRESETS_MENU).eval())
        res: dict[int, tuple | None] = {-1: None, 1: (640, 480), 2: (1280, 720), 3: (1920, 1080), 4: (3840, 2160), # 1 2 3 4
                                        -1: None, 6: (640, 486), 7: (720, 486), 8: (768, 586), 9: (1024, 576), # 6 7 8 9
                                        -1: None, 11: (4096, 3112), 12: (2048, 1556), 13: (3656, 2664), 14: (1828, 1332), 15: (3656, 3112), 16: (1828, 1556), 17: (3072, 2048), # 11 12 13 14 15 16 17
                                        -1: None, 19: (256, 256), 20: (512, 512), 21: (1024, 1024), 22: (2048, 2048), 23: (4096, 4096), # 19 20 21 22 23
                                        -1: None 
                                        }
 
        if res.get(sel) is not None:
            node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE): hou.Vector2(res.get(sel))}) # type: ignore

            if update:
                flam3h_general_utils(self.kwargs).util_set_front_viewer()
            else:
                update_sensor: int = node.parm(OUT_UPDATE_SENSOR).eval()
                if update_sensor:
                    flam3h_general_utils(self.kwargs).util_set_front_viewer()
        
        # reset to null value so we can set the same preset again
        node.setParms({OUT_RENDER_PROPERTIES_RES_PRESETS_MENU: "0"}) # type: ignore


    def reset_OUT_sensor(self) -> None:
        """Reset the OUT Camera sensor settings parameters tab.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        node = self.node
        
        prms_out_sensor_data: dict[str | None, hou.Vector2 | float] = { OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE): hou.Vector2((1024, 1024)),    # tuple
                                                                        OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER): hou.Vector2((0, 0)),  # tuple
                                                                        OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE): 0,
                                                                        OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE): 400
                                                                        }
        
        # Clear and set
        [node.parmTuple(key).deleteAllKeyframes() if isinstance(node.parmTuple(key).eval(), tuple) else node.parm(key).deleteAllKeyframes() for key in prms_out_sensor_data.keys()]
        [node.setParms({key: value}) for key, value in prms_out_sensor_data.items()]

        
    def reset_OUT_render(self) -> None:
        """Reset the OUT Render settings parameters tab.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        
        prms_out_render_data: dict[str | None, int | float] = { OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY): 1000,
                                                                OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS): 3,
                                                                OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA): 2.5,
                                                                OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER): 5,
                                                                OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2): 0,
                                                                OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY): 0.3333
                                                                }
        
        # Clear and set
        [node.parm(key).deleteAllKeyframes() for key in prms_out_render_data.keys()]
        [node.setParms({key: value}) for key, value in prms_out_render_data.items()]


    def reset_OUT_kwargs(self) -> None:
        """Build a multifunctional reset OUT render properties method.
        IT will allow to reset the entire tab or either only the Sensor or Render settings tab.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        
        kwargs: dict = self.kwargs
            
        if kwargs['shift']:
            # Reset only the Camera Sensor
            self.reset_OUT_sensor()
            flam3h_general_utils.flash_message(self.node, f"OUT Camera sensor: RESET")
            
        elif kwargs['ctrl']:
            # Reset only the Render settings
            self.reset_OUT_render()
            flam3h_general_utils.flash_message(self.node, f"OUT Render settings: RESET")
            
        elif kwargs['alt']:
            # Copy only the Render Properties of a Flame preset from the Clipboard
            in_flame_utils(self.kwargs).in_to_flam3h_render_properties_only()
            
        else:
            # Reset all render properties
            self.reset_OUT_sensor()
            self.reset_OUT_render()
            self.out_render_curves_set_and_retrieve_defaults(kwargs['node'])
            flam3h_general_utils.flash_message(self.node, f"OUT Render properties: RESET")
        
        if self.node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
            flam3h_general_utils(self.kwargs).util_set_front_viewer()


    def reset_OUT_options(self) -> None:
        """Reset the OUT save options tab parameters.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        node.setParms({OUT_HSV_PALETTE_DO: 0})
        node.setParms({OUT_FLAM3H_AFFINE_STYLE: 1})
        node.setParms({OUT_USE_FRACTORIUM_PRM_NAMES: 1})
        node.setParms({OUT_AUTO_ADD_ITER_NUM: 1})


    def reset_OUT(self, mode: int=0) -> None:
        """Reset the OUT flame render properties to their default.

        Args:
            mode(int): Defaults to 0. 1 will reset the remainder of the parameters.

        Returns:
            (None):
        """
        node = self.node

        self.reset_OUT_options()
        self.reset_OUT_sensor()
        self.reset_OUT_render()
        
        # If we are in sensor viz and we reset, make sure the sensor is framed properly.
        if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
            flam3h_general_utils(self.kwargs).util_set_clipping_viewers()
            flam3h_general_utils(self.kwargs).util_set_front_viewer()
            
        # I do not think this is used anymore but I leave it here 
        # until I make a cleanup pass of this code.
        if mode == 0:
            node.setParms({MSG_OUT: ''})
            node.setParms({OUT_RENDER_PROPERTIES_EDIT: 0})
            node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
        
        # I do not think this is used anymore but I leave it here 
        # until I make a cleanup pass of this code.
        if mode == 2:
            node.setParms({OUT_PATH: ""})
            node.setParms({OUT_HSV_PALETTE_DO: 0})
            node.setParms({OUT_PRESETS: str(-1)})
            node.setParms({OUT_SYS_PRESETS: str(-1)})
            node.setParms({OUT_FLAME_PRESET_NAME: ""})


    def out_xf_xaos_to(self) -> tuple:
        """Export in a tuple[str] the xaos TO values to write out.
        
        Args:
            (self):

        Returns:
            (tuple): the xaos TO values to write out.
        """
        val: list = self.out_xaos_collect(self.node, self.iter_count, self.flam3h_iter_prm_names.xaos)
        fill: list = [np_pad(item, (0,self.iter_count-len(item)), 'constant', constant_values=1).tolist() for item in val]
        xaos_vactive: list = self.out_xaos_collect_vactive(self.node, fill, self.flam3h_iter_prm_names.main_vactive)
        return tuple([" ".join(x) for x in self.out_xaos_cleanup(self.out_util_round_floats(xaos_vactive))])


    def out_xf_xaos_from(self, mode: int=0) -> tuple:
        """Export in a tuple[str] the xaos FROM values to write out.
        
        Args:
            mode(int): mode=1 is for writing out flame file while the default mode=0 is for converting between xaos modes only
            
        Returns:
            (tuple): the xaos FROM values transposed into xaos TO values to write out.
        """
        val: list = self.out_xaos_collect(self.node, self.iter_count, self.flam3h_iter_prm_names.xaos)
        fill: list = [np_pad(item, (0,self.iter_count-len(item)), 'constant', constant_values=1) for item in val]
        t: list = np_transpose(np_resize(fill, (self.iter_count, self.iter_count)).tolist()).tolist()
        if mode:
            xaos_vactive: list = self.out_xaos_collect_vactive(self.node, t, self.flam3h_iter_prm_names.main_vactive)
            return tuple([" ".join(x) for x in self.out_xaos_cleanup(self.out_util_round_floats(xaos_vactive))])
        else:
            return tuple([" ".join(x) for x in self.out_util_round_floats(t)])


    def menu_out_contents_presets_data(self) -> list:
        """Populate OUT parameter menu items for the SYS and OUT tab.
        
        Args:
            (self):

        Returns:
            (list): Return a menu
        """
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            node = self.node
            xml: str = os.path.expandvars(node.parm(OUT_PATH).eval())
            
            # For the OUT Tab menu presets we are forced to use the class: _xml_tree(...)
            # Instead of the lightweight version class: _xml(...)
            apo = _xml_tree(xml)
            
            if apo.isvalidtree:
                    
                menu: list = []
                [self.menu_out_presets_loop_enum(menu, i, item) if node.parm(PREFS_ENUMERATE_MENU).eval() else self.menu_out_presets_loop(menu, i, item) for i, item in enumerate(apo.name)]
                node.setCachedUserData('out_presets_menu', menu)
                return menu
            
            else:
                flam3h_iterator_utils.destroy_cachedUserData(node, 'out_presets_menu')
                head_tail: tuple = os.path.split(xml)
                if xml and os.path.isdir(head_tail[0]) and not os.path.isfile(xml):
                    return MENU_PRESETS_SAVEONE
                elif xml and not os.path.isfile(xml):
                    return MENU_PRESETS_INVALID
                else:
                    return MENU_PRESETS_EMPTY
        
        
    def menu_out_contents_presets(self) -> list:
        """Rerturn either a cached menu data or rebuild that data on the fly if needed.

        Args:
            (self):

        Returns:
            list: Return a menu
        """
        # This undo's disabler is needed to make the undo work. They work best in H20.5
        with hou.undos.disabler(): # type: ignore
            
            node = self.node
            data: list | None = node.cachedUserData('out_presets_menu')
            
            # Double check
            xml: str = os.path.expandvars(node.parm(OUT_PATH).eval())
            is_valid: bool = os.path.isfile(xml)
            if xml and not is_valid:
                flam3h_general_utils.private_prm_set(node, OUT_PVT_ISVALID_FILE, 0)
                data = None
            elif xml and is_valid:
                # This caused some pain becasue it is forcing us not to tell the truth sometime
                # but its quick and we added double checks for each file types (Palette or Flame) inside each menus empty presets (CP, IN and OUT)
                flam3h_general_utils.private_prm_set(node, OUT_PVT_ISVALID_FILE, 1)
                
            if data is not None:
                return data
            else:
                return self.menu_out_contents_presets_data()

    
    def out_auto_add_iter_data(self) -> tuple[int, str, int]:
        """Collect data needed by:
        
        def out_auto_add_iter_num_to_prm()
        
        def out_auto_change_iter_num_to_prm()
        
        Args:
            (self):

        Returns:
            (tuple[int, str, int]): A tuple with the needed data
        """
        node = self.node
        iter_num: int = node.parm(GLB_ITERATIONS).eval()
        flame_name: str = str(node.parm(OUT_FLAME_PRESET_NAME).eval()).strip()
        autoadd: int = node.parm(OUT_AUTO_ADD_ITER_NUM).eval()
        return iter_num, flame_name, autoadd


    def out_auto_add_iter_num_to_prm(self) -> None:
        """Add the iteration number string to the OUT Flame name after you type a name string in.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        iter_num, flame_name, autoadd = self.out_auto_add_iter_data()
        flame_name_new: str = self.out_auto_add_iter_num(iter_num, flame_name, autoadd)
        node.setParms({OUT_FLAME_PRESET_NAME: flame_name_new}) #type: ignore


    def out_auto_change_iter_num_to_prm(self, name: str | None = None) -> None:
        """Change the iteration number string to the OUT Flame name when you change FLAM3H iterations.
        
        Args:
            (self):
            name(str | None): Default to None (nothing happen). Handy to automatically set the out preset name when an IN preset name is loaded.
            
        Returns:
            (None):
        """      
        node = self.node
        iter_num, flame_name, autoadd = self.out_auto_add_iter_data()
        in_flame_name_auto_file: int = node.parm(OUT_IN_FLAME_NAME_AUTO_FILL).eval()
        if name is not None and in_flame_name_auto_file: flame_name = name
        
        if flame_name:
            
            if autoadd:
                flame_name_new: str = self.out_auto_change_iter_num(iter_num, flame_name, autoadd)
                node.setParms({OUT_FLAME_PRESET_NAME: flame_name_new}) #type: ignore
                
                # Update "iter num on load" if "force iterations on Load" toggle is ON 
                if node.parm(IN_USE_ITER_ON_LOAD).eval():
                    node.setParms({IN_ITER_NUM_ON_LOAD: iter_num})
            else:
                flame_name_new: str = self.out_remove_iter_num(flame_name)
                node.setParms({OUT_FLAME_PRESET_NAME: flame_name_new}) #type: ignore
                
            # Flash message if needed.
            # I need to come back on this and see exactly when firing the flash message, for now is not bad.
            if flame_name_new:
                flam3h_general_utils.flash_message(node, f"{flame_name_new}")
                
                
    def out_flame_name_inherit_on_load(self) -> None:
        """When this option is toggled ON, cause the Flame name parameter to be set to the currently loaded Flame preset name.
        
        Args:
            (self):
            
        Returns:
            (None):
        """  
        if self.kwargs['parm'].eval():
            
            node = self.node
            inisvalidfile: int = node.parm(IN_PVT_ISVALID_FILE).eval()
            inisvalidpreset: int = node.parm(IN_PVT_ISVALID_PRESET).eval()
            clipboard: int = node.parm(IN_PVT_CLIPBOARD_TOGGLE).eval()
            xml: str = os.path.expandvars(node.parm(IN_PATH).eval())
            xml_isFile: bool = os.path.isfile(xml)
            # Only if a valid preset has been loaded from a disk file ( not clipboard )
            if xml and xml_isFile and inisvalidfile and inisvalidpreset and not clipboard:
                # Build the apo data
                preset_id: int = int(node.parm(IN_PRESETS).eval())
                apo_data = in_flame_iter_data(node, xml, preset_id)
                if apo_data.isvalidtree:
                    node.setParms({OUT_FLAME_PRESET_NAME: apo_data.name[preset_id]}) #type: ignore
                    # Updated the Flame name iter num if exist and if needed
                    self.out_auto_change_iter_num_to_prm()
            elif inisvalidpreset and clipboard:
                data: str | None = node.userData(FLAM3H_USER_DATA_XML_LAST)
                if data is not None:
                    apo_data = in_flame_iter_data(node, data, 0)
                    if apo_data.isvalidtree:
                        node.setParms({OUT_FLAME_PRESET_NAME: apo_data.name[0]}) #type: ignore
                        # Updated the Flame name iter num if exist and if needed
                        self.out_auto_change_iter_num_to_prm()
                

    def out_flame_properties_build(self, f3r: out_flame_render_properties) -> dict:
        """Return a dictionary with all the flame properties to be written out.
        
        _NOTE:
            Any of these properties will not be included into the exported XML flame file if they are: False

        Args:
            (self):
            f3r(out_flame_render_properties): Flame render properties class

        Returns:
            (dict): a dictionary with all the flame properties to written out
        """   
        # If "use Fractorium parametric prm names" OUT option is ON, lets append the EMBER name to the app name
        # so that we can pick up the proper parametric parameter names if we load it back in Houdini.
        if self.node.parm(OUT_USE_FRACTORIUM_PRM_NAMES).eval(): _XML_APP_NAME = f"{XML_APP_NAME_FRACTORIUM}-{XML_APP_NAME_FLAM3H}"
        else: _XML_APP_NAME = XML_APP_NAME_FLAM3H
        
        return {OUT_XML_VERSION: f'{_XML_APP_NAME}-{flam3h_general_utils.my_system()}-{__version__}',
                XML_XF_NAME: f3r.flame_name,
                OUT_XML_FLAM3H_SYS_RIP: f3r.flam3h_sys_rip, # custom to FLAM3H only
                OUT_XML_FLAM3H_HSV: f3r.flam3h_cp_hsv, # custom to FLAM3H only
                OUT_XML_FLMA3H_MB_FPS: f3r.flam3h_mb_fps, # custom to FLAM3H only
                OUT_XML_FLMA3H_MB_SAMPLES: f3r.flam3h_mb_samples, # custom to FLAM3H only
                OUT_XML_FLMA3H_MB_SHUTTER: f3r.flam3h_mb_shutter, # custom to FLAM3H only
                OUT_XML_FLAM3H_CP_SAMPLES: f3r.flam3h_cp_samples, # custom to FLAM3H only
                OUT_XML_FLAM3H_PREFS_F3C: f3r.flam3h_prefs_f3c, # custom to FLAM3H only
                OUT_XML_FLAME_SIZE: f3r.flame_size, 
                OUT_XML_FLAME_CENTER: f3r.flame_center,
                OUT_XML_FLAME_SCALE: f3r.flame_scale,
                OUT_XML_FLAME_ROTATE: f3r.flame_rotate,
                OUT_XML_FLAME_BG: '0 0 0',
                OUT_XML_FLAME_SUPERSAMPLE: '2',
                OUT_XML_FLAME_FILTER: '0.5',
                OUT_XML_FLAME_QUALITY: f3r.flame_quality,
                OUT_XML_FLAME_BRIGHTNESS: f3r.flame_brightness,
                OUT_XML_FLAME_GAMMA: f3r.flame_gamma,
                OUT_XML_FLAME_GAMMA_THRESHOLD: '0.0423093658828749',
                OUT_XML_FLAME_K2: f3r.flame_k2,
                OUT_XML_FLAME_VIBRANCY: f3r.flame_vibrancy,
                OUT_XML_FLAME_POWER: f3r.flame_highlight,
                OUT_XML_FLAME_RADIUS: '9',
                OUT_XML_FLAME_ESTIMATOR_MINIMUM: '0',
                OUT_XML_FLAME_ESTIMATOR_CURVE: '0.4',
                OUT_XML_FLAME_PALETTE_MODE: 'linear',
                OUT_XML_FLAME_INTERPOLATION: 'linear',
                OUT_XML_FLAME_INTERPOLATION_TYPE: 'log'
                }
        

    def out_flam3_compatibility_check_and_msg(self) -> bool:
        """Check if the Flame we want to write out is compatible with the FLAM3 flame format.
        If not, print out details to let us know what is wrong with it.

        Args:
            (self):
            
        Returns:
            (bool): Return True if the Flame is valid or False if not.
        """
        node = self.node
        
        # Here we are adding POST VARS and FF PRE VARS even tho they are only one slot,
        # just in case in the future I add more.
        bool_VARS_PRE = bool_VARS = bool_VARS_POST = bool_VARS_PRE_FF = bool_VARS_FF = bool_VARS_POST_FF = False
        
        # Iterators: duplicates check
        #############################################################################
        iter_PRE: dict[str, list[str]] | bool = self.out_collect_var_section_names_dict(node, 0, 'PRE')
        iter_VAR: dict[str, list[str]] | bool = self.out_collect_var_section_names_dict(node, 0, 'VAR')
        
        iter_count: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        
        iter_VAR_dup: dict[str, list | str] = {}
        if iter_VAR is not False:
            assert isinstance(iter_VAR, dict)
            for iter in range(iter_count):
                key: str = str(iter + 1)
                vars: list[str] | None = iter_VAR.get(key)
                if vars is not None:
                    dup: list | str = self.out_util_vars_duplicate(vars)
                    assert isinstance(dup, list)
                    if dup:
                        iter_VAR_dup[key] = dup
                        if bool_VARS is False: bool_VARS: bool = True
                    
        iter_PRE_dup: dict[str, list | str] = {}
        if iter_PRE is not False:
            assert isinstance(iter_PRE, dict)
            for iter in range(iter_count):
                key: str = str(iter + 1)
                vars: list[str] | None = iter_PRE.get(key)
                if vars is not None:
                    dup: list | str = self.out_util_vars_duplicate(vars)
                    assert isinstance(dup, list)
                    if dup:
                        iter_PRE_dup[key] = dup
                        if bool_VARS_PRE is False: bool_VARS_PRE: bool = True
        
        
        # FF: duplicates check
        #############################################################################
        _FF_VAR_dup: dict[str, list | str] = {}
        _FF_POST_dup: dict[str, list | str] = {}
        key: str = 'FF'
        if node.parm(PREFS_PVT_DOFF).eval():
            _FF_VAR: dict[str, list[str]] | bool  = self.out_collect_var_section_names_dict(node, 1, 'VAR')
            _FF_POST: dict[str, list[str]] | bool = self.out_collect_var_section_names_dict(node, 1, 'POST')
            if _FF_VAR is not False:
                assert isinstance(_FF_VAR, dict)
                vars: list[str] | None = _FF_VAR.get(key)
                if vars is not None:
                    dup: list | str = self.out_util_vars_duplicate(vars)
                    assert isinstance(dup, list)
                    if dup:
                        _FF_VAR_dup[key] = dup
                        bool_VARS_FF: bool = True
                    
            if _FF_POST is not False:
                assert isinstance(_FF_POST, dict)
                vars: list[str] | None = _FF_POST.get(key)
                if vars is not None:
                    dup: list | str = self.out_util_vars_duplicate(vars)
                    assert isinstance(dup, list)
                    if dup:
                        _FF_POST_dup[key] = dup
                        bool_VARS_POST_FF: bool = True
        
        if bool_VARS_PRE or bool_VARS or bool_VARS_POST or bool_VARS_PRE_FF or bool_VARS_FF or bool_VARS_POST_FF:
            
            _MSG_PRE = _MSG_VAR = ''
            if bool_VARS_PRE:
                dup = ''.join(f"\titerator.{key}\n\t\t{str(', '.join(val))}\n" for key, val in iter_PRE_dup.items())
                assert isinstance(dup, str)
                _MSG_PRE = f"\nPRE\n{dup}"
            
            if bool_VARS:
                dup = ''.join(f"\titerator.{key}\n\t\t{str(', '.join(val))}\n" for key, val in iter_VAR_dup.items())
                assert isinstance(dup, str)
                _MSG_VAR = f"\nVAR\n{dup}"
                
            _MSG_FF_VAR = _MSG_FF_POST = ''
            if bool_VARS_FF:
                dup = ''.join(f"{str(', '.join(val))}\n" for val in _FF_VAR_dup.values())
                assert isinstance(dup, str)
                _MSG_FF_VAR = f"\nFF VAR\n\t{dup}"
            
            if bool_VARS_POST_FF:
                dup = ''.join(f"{str(', '.join(val))}\n" for val in _FF_POST_dup.values())
                assert isinstance(dup, str)
                _MSG_FF_POST = f"\nFF POST\n\t{dup}"
                
            _MSG_INTRO: str = f"You are using the same variation multiple times\ninside the following iterators/FF types (PRE, VAR, POST):\n"
            _MSG_ALL_DUP: str = f"{_MSG_INTRO}{_MSG_PRE}{_MSG_VAR}{_MSG_FF_VAR}{_MSG_FF_POST}"
            
            _MSG_HELP: str  = "\n"
            _MSG_HELP += f"DOC:\n"
            _MSG_HELP += f"\tWhile this is doable within the tool, it is not compatible with FLAM3 file format.\n\tIt require that a variation is used only once per type ( types: PRE, VAR, POST )\n\totherwise you wont be able to save out the same result neither to load it back.\n\tFor example you are not allowed to use two Spherical variations inside an iterator VAR section.\n\n\tYou can however use\n\tone Spherical variation inside the VAR section, one inside the PRE and one inside the POST.\n\n"
            _MSG_HELP += f"TIP:\n"
            _MSG_HELP += f"\tSave the hip file instead if you desire to keep the Flame result as it is now.\n\tFractorium, Apophysis and all other FLAM3 compatible applications obey to the same rule."
            
            _MSG_ALL: str = f"{_MSG_ALL_DUP}{_MSG_HELP}"
            
            _MSG: str = f"{node.name()}: FLAM3 Compatibility -> The FLAM3 format is incompatible with the fractal Flame you are attempting to save."
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            if hou.isUIAvailable():
                _MSG_UI = "Duplicates variations of the same type not allowed.\nShow Details to learn more."
                hou.ui.displayMessage(_MSG_UI, buttons=("Got it, thank you",), severity=hou.severityType.ImportantMessage, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Compatibility", details=_MSG_ALL, details_label=None, details_expanded=False) # type: ignore
            flam3h_general_utils.set_status_msg('', 'MSG')
            return False
        
        else:
            return True
        
        
    def out_populate_xform_vars_XML(self, 
                                    varsPRM: tuple, 
                                    TYPES_tuple: tuple, 
                                    WEIGHTS_tuple: tuple, 
                                    XFORM: lxmlET.Element, # type: ignore
                                    MP_IDX: str, 
                                    FUNC: Callable) -> list[str]:
        """Set this iterator variations types parameters, weights parameters and their parametric parameters inside the xform (lxmlET.Element) to be written out into the XML file.
        It will also return a list of used variations in the provided iterator/xform.
        
        Args:
            varsPRM(tuple): FLAM3H variation's types and their parametric parameters names.
            TYPES_tuple(tuple): FLAM3H variation's types parameters names.
            WEIGHTS_tuple(tuple): FLAM3H variation's weights parameters names.
            XFORM(lxmlET.Element): The current xform (lxmlET.Element) to populate.
            MP_IDX(str): Current multiparameter index
            FUNC(Callable): Callable definition to convert variation's names between VAR, PRE and POST: in_flame_utils.in_util_make_NULL, in_flame_utils.in_util_make_PRE, in_flame_utils.in_util_make_POST

        Returns:
            (list[str]): List of used variation in this iterator/xform
        """
        node = self.node
        names: list = []
        for idx, prm in enumerate(WEIGHTS_tuple):
            prm_w: float = node.parm(f"{prm[0]}{MP_IDX}").eval()
            if prm_w != 0:
                v_type: int = node.parm(f"{TYPES_tuple[idx]}{MP_IDX}").eval()
                v_name: str = in_flame_utils.in_get_dict_key_from_value(VARS_FLAM3_DICT_IDX, v_type)
                names.append(v_name)
                XFORM.set(FUNC(v_name), self.out_util_round_float(prm_w))
                vars_prm: tuple = varsPRM[v_type]
                if vars_prm[-1]:
                    f3h_prm: tuple = varsPRM[v_type][1:-1]

                    # If OUT Tab -> USE_FRACTORIUM_PRM_NAMES toggle is ON
                    # make sure to use the parametric variation's parameters names that Fractorium expect.
                    apo_prm: tuple = flam3h_varsPRM_APO().varsPRM[v_type]
                    if node.parm(OUT_USE_FRACTORIUM_PRM_NAMES).eval():
                        out_prm: tuple = in_flame_utils.in_prm_name_exceptions(v_type, XML_APP_NAME_FRACTORIUM, apo_prm)[1:-1]
                    else:
                        out_prm: tuple = apo_prm[1:-1]
                        
                    for id, p in enumerate(out_prm):
                        if f3h_prm[id][-1]:
                            for i in range(len(p)): # for i, n in enumerate(p):
                                vals: tuple = node.parmTuple(f"{f3h_prm[id][0]}{MP_IDX}").eval()
                                XFORM.set(FUNC(p[i]), self.out_util_round_float(vals[i]))
                        else:
                            val: float = node.parm(f"{f3h_prm[id][0]}{MP_IDX}").eval()
                            XFORM.set(FUNC(p[0]), self.out_util_round_float(val))
                            
        return names


    def out_build_XML(self, flame: lxmlET.Element) -> bool: # type: ignore
        """Build the XML Flame data to be then written out.

        Args:
            (self):
            flame(lxmlET.Element): The root of either the flame to be written out or the flame file to append the new flame to.

        Returns:
            (bool): return True if the Flame is a compatible FLAM3 flame or False if not.
        """
        # Build Flame data and render properties
        f3d = out_flame_xforms_data(self.kwargs)
        f3r = out_flame_render_properties(self.kwargs)
        
        # SET Flame render properties
        [flame.set(key, value) for key, value in self.out_flame_properties_build(f3r).items() if value is not False]

        # SET xforms
        name_PRE_BLUR: str = ""
        names_VARS: list = []
        names_VARS_PRE: list = []
        names_VARS_POST: list = []
        xml_xf_names: tuple = self.out_buil_xf_names(f3d)
        for iter in range(f3d.iter_count):
            mp_idx = str(int(iter + 1))
            if int(f3d.xf_vactive[iter]):
                xf = lxmlET.SubElement(flame, XML_XF) # type: ignore
                xf.tag = XML_XF
                xf.set(XML_XF_NAME, xml_xf_names[iter])
                xf.set(XML_XF_WEIGHT, f3d.xf_weight[iter])
                xf.set(XML_XF_COLOR, f3d.xf_color[iter])
                xf.set(XML_XF_SYMMETRY, f3d.xf_symmetry[iter])
                xf.set(XML_XF_COLOR_SPEED, f3d.xf_color_speed[iter])
                if f3d.xf_pre_blur[iter]:
                    name_PRE_BLUR = XML_XF_PB
                    xf.set(XML_XF_PB, f3d.xf_pre_blur[iter])
                xf.set(XML_PRE_AFFINE, f3d.xf_preaffine[iter])
                if f3d.f3h_affine and float(f3d.xf_f3h_preaffine_angle[iter]) != 0:
                    xf.set(XML_FLAM3H_PRE_AFFINE, f3d.xf_f3h_preaffine[iter])
                    xf.set(XML_FLAM3H_PRE_AFFINE_ANGLE, f3d.xf_f3h_preaffine_angle[iter])
                if f3d.xf_postaffine[iter]:
                    xf.set(XML_POST_AFFINE, f3d.xf_postaffine[iter])
                    if f3d.f3h_affine and float(f3d.xf_f3h_postaffine_angle[iter]) != 0:
                        xf.set(XML_FLAM3H_POST_AFFINE, f3d.xf_f3h_postaffine[iter])
                        xf.set(XML_FLAM3H_POST_AFFINE_ANGLE, f3d.xf_f3h_postaffine_angle[iter])
                if f3d.xf_xaos[iter]:
                    xf.set(XML_XF_XAOS, f3d.xf_xaos[iter])
                xf.set(XML_XF_OPACITY, f3d.xf_opacity[iter])
                f3h_iter = flam3h_iterator()
                names_VARS.append(self.out_populate_xform_vars_XML(flam3h_varsPRM().varsPRM, f3h_iter.sec_varsT, f3h_iter.sec_varsW, xf, mp_idx, in_flame_utils.in_util_make_NULL))
                names_VARS_PRE.append(self.out_populate_xform_vars_XML(flam3h_varsPRM().varsPRM, f3h_iter.sec_prevarsT, f3h_iter.sec_prevarsW[1:], xf, mp_idx, in_flame_utils.in_util_make_PRE))
                names_VARS_POST.append(self.out_populate_xform_vars_XML(flam3h_varsPRM().varsPRM, f3h_iter.sec_postvarsT, f3h_iter.sec_postvarsW, xf, mp_idx, in_flame_utils.in_util_make_POST))
        
        # SET finalxform (FF)
        names_VARS_FF: list = []
        names_VARS_PRE_FF: list = []
        names_VARS_POST_FF: list = []
        if f3d.flam3h_do_FF:
            finalxf = lxmlET.SubElement(flame, XML_FF) # type: ignore
            finalxf.tag = XML_FF
            finalxf.set(XML_XF_NAME, f3d.finalxf_name)
            finalxf.set(XML_XF_COLOR, '0')
            finalxf.set(XML_XF_VAR_COLOR, '1')
            finalxf.set(XML_XF_COLOR_SPEED, '0')
            finalxf.set(XML_XF_SYMMETRY, '1')
            finalxf.set(XML_PRE_AFFINE, f3d.finalxf_preaffine)
            if f3d.f3h_affine and float(f3d.finalxf_f3h_preaffine_angle) != 0:
                finalxf.set(XML_FLAM3H_PRE_AFFINE, f3d.finalxf_f3h_preaffine)
                finalxf.set(XML_FLAM3H_PRE_AFFINE_ANGLE, f3d.finalxf_f3h_preaffine_angle)
            if f3d.finalxf_postaffine:
                finalxf.set(XML_POST_AFFINE, f3d.finalxf_postaffine)
                if f3d.f3h_affine and float(f3d.finalxf_f3h_postaffine_angle) != 0:
                    finalxf.set(XML_FLAM3H_POST_AFFINE, f3d.finalxf_f3h_postaffine)
                    finalxf.set(XML_FLAM3H_POST_AFFINE_ANGLE, f3d.finalxf_f3h_postaffine_angle)
            f3h_iter_FF = flam3h_iterator_FF()
            names_VARS_FF = self.out_populate_xform_vars_XML(flam3h_varsPRM_FF(f"{PRX_FF_PRM}").varsPRM_FF(), f3h_iter_FF.sec_varsT_FF, f3h_iter_FF.sec_varsW_FF, finalxf, '', in_flame_utils.in_util_make_NULL)
            names_VARS_PRE_FF = self.out_populate_xform_vars_XML(flam3h_varsPRM_FF(f"{PRX_FF_PRM_POST}").varsPRM_FF(), f3h_iter_FF.sec_prevarsT_FF, f3h_iter_FF.sec_prevarsW_FF, finalxf, '', in_flame_utils.in_util_make_PRE)
            names_VARS_POST_FF = self.out_populate_xform_vars_XML(flam3h_varsPRM_FF(f"{PRX_FF_PRM_POST}").varsPRM_FF(), f3h_iter_FF.sec_postvarsT_FF, f3h_iter_FF.sec_postvarsW_FF, finalxf, '', in_flame_utils.in_util_make_POST)
        
        # SET palette
        palette = lxmlET.SubElement(flame, XML_PALETTE) # type: ignore
        palette.tag = XML_PALETTE
        palette.set(XML_PALETTE_COUNT, self.out_palette_keys_count(self.palette_plus_do, len(self.palette.keys()), 0, False)) # When saving a Flame out, we always use a 256 color palette unless the OUT tab option "save palette 256+" is ON
        palette.set(XML_PALETTE_FORMAT, PALETTE_FORMAT)
        palette.text = f3d.palette_hex

        # SET unique used 'plugins' and 'new linear'
        names_VARS_flatten_unique: list = in_flame_utils.in_util_vars_flatten_unique_sorted(names_VARS + [names_VARS_FF], in_flame_utils.in_util_make_NULL)
        names_VARS_PRE_flatten_unique: list = in_flame_utils.in_util_vars_flatten_unique_sorted(names_VARS_PRE + [names_VARS_PRE_FF] + list(map(lambda x: in_flame_utils.in_util_make_VAR([x]) if x else x, [name_PRE_BLUR])), in_flame_utils.in_util_make_PRE)
        names_VARS_POST_flatten_unique: list = in_flame_utils.in_util_vars_flatten_unique_sorted(names_VARS_POST + [names_VARS_POST_FF], in_flame_utils.in_util_make_POST)
        flame.set(XML_FLAME_PLUGINS, i_cleandoc(" ".join(names_VARS_PRE_flatten_unique + names_VARS_flatten_unique + names_VARS_POST_flatten_unique)))
        flame.set(XML_FLAME_NEW_LINEAR, '1')
        
        # SET CC Curves
        cc: dict[str, str] = {  OUT_XML_FLAME_RENDER_CURVES: f3r.flame_render_curves,
                                OUT_XML_FLAME_RENDER_CURVE_OVERALL: f3r.flame_overall_curve,
                                OUT_XML_FLAME_RENDER_CURVE_RED: f3r.flame_red_curve,
                                OUT_XML_FLAME_RENDER_CURVE_GREEN: f3r.flame_green_curve,
                                OUT_XML_FLAME_RENDER_CURVE_BLUE: f3r.flame_blue_curve
                                }
        [flame.set(key, value) for key, value in cc.items()]
        
        # return if this flame is a valid 'flam3'
        return self.out_flam3_compatibility_check_and_msg()
            
            
    def out_userData_XML_last_loaded(self, data_name: str = FLAM3H_USER_DATA_XML_LAST, flame_name: str | None = None) -> None:
        """Store the loaded Flame preset into the FLAM3H node data storage.
        This definition run a full save out preset(a snapshot of the curernt status of the FLAM3H parameters).
        
        This is being added to have some sort of history/backup some how.
        Will probably never be used but it is something more to have in any case.
        This data is cleared every time a FLAM3H node is being created, or when FLAM3H is being reset to the default Sierpinsky triangle or its iterator's count is set to 0(Zero).

        Args:
            (self):
            data_name(str): Default to "FLAM3H_USER_DATA_XML_LAST". The name of the node user data to store the flame preset into.
            flame_name(str | None): Default to None. If a flame name is provided it will use it, otherwise it will either use the one set into the OUT flame name parameter or if this last is empty it will generate one based on today'sdate and time.
            
        Returns:
            (None):
        """ 
        node = self.node
        
        root = lxmlET.Element(XML_FLAME_NAME) # type: ignore
        if flame_name is None:
            if self.out_build_XML(root):
                self._out_pretty_print(root)
                flame = lxmlET.tostring(root, encoding="unicode") # type: ignore
                # Store the loaded Flame preset into the FLAM3H node data storage
                node.setUserData(data_name, flame)
                
        else:
            # Lets check if the OUT flame name parameter has a name already set and store it.
            out_flame_name: str = node.parm(OUT_FLAME_PRESET_NAME).eval()
            # Let's use the passed flame_name instead
            node.setParms({OUT_FLAME_PRESET_NAME: flame_name})
            if self.out_build_XML(root):
                self._out_pretty_print(root)
                flame = lxmlET.tostring(root, encoding="unicode") # type: ignore
                # Store the loaded Flame preset into the FLAM3H node data storage
                node.setUserData(data_name, flame)
            # Restore whatever flame name was there if any (even if it was empty)
            node.setParms({OUT_FLAME_PRESET_NAME: out_flame_name})
            
            
    def out_new_XML(self, outpath: str) -> None:
        """Write out a new XML flame file with only the current FLAM3H flame preset.

        Args:
           (self):
            outpath(str): Current OUT flame full file path.
            
        Returns:
            (none):
        """   
        node = self.node
        
        root = lxmlET.Element(XML_VALID_FLAMES_ROOT_TAG) # type: ignore
        flame = lxmlET.SubElement(root, XML_FLAME_NAME) # type: ignore
        flame.tag = XML_FLAME_NAME
        
        if self.out_build_XML(flame):
            self._out_pretty_print(root)
            tree = lxmlET.ElementTree(root)
            tree.write(outpath)
            
            node.setParms({OUT_FLAME_PRESET_NAME: ''}) #type: ignore
            _MSG: str = f"{self.node.name()}: SAVE Flame New: Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Flame SAVED")


    def out_new_XML_clipboard(self) -> None:
        """Write out a new XML flame file with only the current FLAM3H flame preset into the clipboard.

        Args:
            (self):
            
        Returns:
            (None):
        """ 
        node = self.node
        
        root = lxmlET.Element(XML_FLAME_NAME) # type: ignore
        
        if self.out_build_XML(root):
            self._out_pretty_print(root)
            flame = lxmlET.tostring(root, encoding="unicode") # type: ignore
            hou.ui.copyTextToClipboard(flame) # type: ignore
            
            node.setParms({OUT_FLAME_PRESET_NAME: ''}) #type: ignore
            _MSG: str = f"{self.node.name()}: SAVE Flame Clipboard: Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Flame SAVED to the Clipboard")


    def out_append_XML(self, apo_data: in_flame, out_path: str) -> None:
        """Append a XML flame file to the current OUT flame lib file.

        Args:
            (self):
            apo_data(in_flame): Current OUT flame lib file data for all its flame presets.
            out_path(str): Current OUT flame full file path.

        Returns:
            (None):
        """
        node = self.node
        
        root = apo_data.tree.getroot()
        
        flame = lxmlET.SubElement(root, XML_FLAME_NAME) # type: ignore
        flame.tag = XML_FLAME_NAME
        
        if self.out_build_XML(flame):
            self._out_pretty_print(root)
            tree = lxmlET.ElementTree(root)
            tree.write(out_path)
            
            node.setParms({OUT_FLAME_PRESET_NAME: ''}) #type: ignore
            _MSG: str = f"{self.node.name()}: SAVE Flame Append: Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Flame SAVED: Append")


    def out_XML(self) -> None:
        """Write out the XML Flame file.
        It allow for writing out a new file or append to the current XML flame file.
        
        Args:
            (self):
            
        Returns:
            (None):
        """
        node = self.node
        # Force this data to be rebuilt
        # This is needed to help to updates the menus from time to time so to pick up sneaky changes to the loaded files
        # (ex. the user perform hand made modifications like renaming a Preset and such).
        flam3h_iterator_utils(self.kwargs).destroy_all_menus_data(node)
        flam3h_iterator_utils(self.kwargs).update_xml_last_loaded()
        
        # if there is at least one iterator
        iterators_num: int = node.parm(FLAME_ITERATORS_COUNT).eval()
        if iterators_num:
            
            kwargs: dict = self.kwargs
            
            out_path: str = os.path.expandvars(node.parm(OUT_PATH).eval())
            out_path_checked: str | bool = self.out_check_outpath(node, out_path, OUT_FLAM3_FILE_EXT, AUTO_NAME_OUT)
            
            # Write to the clipboard
            if kwargs['alt']:
                self.out_new_XML_clipboard()
                
            # Otherwise if the output path is valid
            elif out_path_checked is not False:
                assert isinstance(out_path_checked, str)
                
                if kwargs['shift']:
                    flam3h_general_utils.util_open_file_explorer(out_path_checked)
                    
                else:

                    if flam3h_general_utils.isLOCK(out_path_checked):
                        ui_text: str = f"This Flame library is Locked."
                        ALL_msg: str = f"This Flame library is Locked and you can not modify this file.\n\nTo Lock a Flame lib file just rename it using:\n\"{FLAM3H_LIB_LOCK}\" as the start of the filename.\n\nOnce you are happy with a Flame library you built, you can rename the file to start with: \"{FLAM3H_LIB_LOCK}\"\nto prevent any further modifications to it. For example if you have a lib file call: \"my_grandJulia.flame\"\nyou can rename it to: \"{FLAM3H_LIB_LOCK}_my_grandJulia.flame\" to keep it safe."
                        _MSG: str = "FLAME library file -> is LOCKED"
                        # Print to Houdini's status bar
                        flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
                        flam3h_general_utils.flash_message(node, _MSG)
                        
                        # Pop up message window
                        if hou.isUIAvailable():
                            hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.ImportantMessage, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Lib Lock", details=ALL_msg, details_label=None, details_expanded=False) # type: ignore
                        # Clear up Houdini's status bar msg
                        flam3h_general_utils.set_status_msg('', 'MSG')
                        
                    else:
                        
                        node.setParms({OUT_PATH: out_path_checked})
                        exist: bool = os.path.exists(out_path_checked)
                        apo_data = in_flame(self.node, out_path_checked)
                        _CHK = True
                        
                        if kwargs["ctrl"]:
                            
                            if exist:
                                if apo_data.isvalidtree:
                                    self.out_new_XML(out_path_checked)
                                    # Clear OUT presets menu filepath cache (this is done to force update the preset menu)
                                    flam3h_iterator_utils.destroy_cachedUserData(node, "out_presets_filepath")
                                else:
                                    _CHK = False
                            else:
                                self.out_new_XML(out_path_checked)
                                # Clear OUT presets menu filepath cache (this is done to force update the preset menu)
                                flam3h_iterator_utils.destroy_cachedUserData(node, "out_presets_filepath")
                            
                        else:
                            
                            if exist:
                                if apo_data.isvalidtree:
                                    self.out_append_XML(apo_data, out_path_checked)
                                    # Clear OUT presets menu filepath cache (this is done to force update the preset menu)
                                    flam3h_iterator_utils.destroy_cachedUserData(node, "out_presets_filepath")
                                else:
                                    _CHK = False
                            else:
                                self.out_new_XML(out_path_checked)
                                # Clear OUT presets menu filepath cache (this is done to force update the preset menu)
                                flam3h_iterator_utils.destroy_cachedUserData(node, "out_presets_filepath")
                                
                        if not _CHK:
                            _MSG: str = "OUT File not a FLAME file"
                            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
                            flam3h_general_utils.flash_message(node, _MSG)
                                
                        # We forced the presets menus to update at the start of this definition, lets skip the destroy menus part on this one
                        flam3h_general_utils(kwargs).flam3h_init_presets_OUT_PRESETS(False)

            else:
                _MSG: str = f"{node.name()}: SAVE Flame: Select a valid output file or a valid filename to create first."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"OUT: Select a valid output file")


    '''
    The following definitions will prep all the data into proper strings to be then written into the XML flame/xform data keys/entries.
    The name of each is self explanatory of the data they will prep and two different classes will be used to hold all this data:
    
    OUT FLAME RENDER PROPERTIES:
    class out_flame_render_properties(out_flame_utils):
    
    OUT FLAME XFORMS DATA:
    class out_flame_xforms_data(out_flame_utils):
    
    This way they can be called elsewere anytime so to have this data always at hand.
    '''
    
    def __out_flame_data(self, prm_name: str = '') -> str:
        """Prepare the OUT render data FLAM3H parameters into proper strings to be written out.
        This will deal with tuple value (flame_size, flame_center, etc) as well with float values (flame_quality, flame_rotate, etc).

        Args:
            (self):
            prm_name(str): The name of the FLAM3H parameter to be prep into a string for writing out.

        Returns:
            (str): The FLAM3H parameter prepped into a string for writing out into the Flame preset file.
        """    
        if prm_name:
            prm_type: bool = False
            try:
                prm = self.node.parmTuple(prm_name)
                prm_type = True
            except: prm = self.node.parm(prm_name)
            if prm_type:
                return ' '.join([str(self.out_util_round_float(x.eval())) for x in prm])
            else:
                if type(prm) is not str:
                    return str(self.node.parm(prm_name).eval())
                else:
                    return self.out_util_round_float(self.node.parm(prm_name).eval())
        else:
            print(f"Warning:\n{self.node.name()}: parameter name: \"{prm_name}\" not found. Please pass in a valid FLAM3H parameter name.\n")
            return ''


    def __out_flame_name(self, prm_name: str | None = OUT_XML_RENDER_HOUDINI_DICT.get(XML_XF_NAME)) -> str:
        """Prepare the Flame name string for the XML Flame name key.
        It will either use an automated one if no Flame name is provided or use the one provided by the user.
        It will also auto add the iterations number to the string name if requested ("add iterations to Flame name" toggle ON)

        Args:
            (self):
            prm_name(str | None = OUT_XML_RENDER_HOUDINI_DICT.get(XML_XF_NAME)): Default to: OUT_XML_RENDER_HOUDINI_DICT.get(XML_XF_NAME). The FLAM3H "Flame name" parameter name.

        Returns:
            (str): The FLAM3H parameter prepped into a string for writing out into the Flame preset file.
        """    
        flame_name: str = self.node.parm(prm_name).eval()
        autoadd: int = self.node.parm(OUT_AUTO_ADD_ITER_NUM).eval()
        
        if not flame_name:
            return self.out_flame_default_name(self.node, autoadd)
        else:
            # otherwise get that name and use it
            iter_num: int = self.node.parm(GLB_ITERATIONS).eval()
            return self.out_auto_add_iter_num(iter_num, flame_name, autoadd)
        
        
    def __out_xf_data(self, prm_name: str) -> tuple:
        """Prepare the xform/iterator single value parameters into a proper string to be written out.

        Args:
            (self):
            prm_name(str): The name of the FLAM3H parameter to be prep into a string for writing out.

        Returns:
            (str): The FLAM3H parameter prepped into a string for writing out into the Flame preset file.
        """    
        val: list = [str(self.out_util_round_float(self.node.parm(f"{prm_name}_{iter + 1}").eval())) for iter in range(self.iter_count)]
        return tuple(val)
    
    
    def __out_xf_data_color_speed(self) -> tuple:
        """Prepare the xform/iterator color speed into a proper string to be written out.
        This is specifically for Fractorium as it is the one using this conversion of values.

        Args:
            (self):

        Returns:
            (str): The FLAM3H parameter prepped into a string for writing out into the Flame preset file.
        """    
        val: list = [str(self.out_util_round_float((1.0-self.node.parm(f"{flam3h_iterator_prm_names().shader_speed}_{iter + 1}").eval())/2.0)) for iter in range(self.iter_count)]
        return tuple(val)
    

    def __out_xf_name(self) -> tuple:
        """Prepare each xform/iterator names/notes parameters for writing out.

        Args:
            (self):

        Returns:
            (tuple): tuple of all the FLAM3H names/notes prepped into strings for writing out into the Flame preset file.
        """    
        val: list = [str(self.node.parm(f"{self.flam3h_iter_prm_names.main_note}_{iter + 1}").eval()).strip() for iter in range(self._iter_count)]
        return tuple(val)
    
    
    def __out_finalxf_name(self) -> str:
        """Prepare the FF/finalXform name/note parameter for writing out.

        Args:
            (self):

        Returns:
            (str): The FLAM3H FF name/note prepped into strings for writing out into the Flame preset file.
        """    
        FF_name: str = self.node.parm(f"{PRX_FF_PRM}{self.flam3h_iter_prm_names.main_note}").eval()
        return FF_name

    
    def __out_xf_pre_blur(self) -> tuple:
        """Prepare each xform/iterator pre_blur parameters for writing out.

        Args:
            (self):

        Returns:
            (tuple): tuple of all the FLAM3H xforms/iterators pre_blur parameters prepped into strings for writing out into the Flame preset file.
        """   
        val: list = [str( self.node.parm(f"{self.flam3h_iter_prm_names.prevar_weight_blur}_{iter + 1}").eval() ) if self.node.parm(f"{self.flam3h_iter_prm_names.prevar_weight_blur}_{iter + 1}").eval() > 0 else '' for iter in range(self.iter_count)]
        return tuple(val)


    def __out_xf_xaos(self) -> tuple:
        """Prepare each xform/iterator xaos parameters for writing out.

        Args:
            (self):

        Returns:
            (tuple): tuple of all the FLAM3H xforms/iterators xaos parameters prepped into strings for writing out into the Flame preset file.
        """   
        if self.xm: return self.out_xf_xaos_from(1)
        else: return self.out_xf_xaos_to()


    def __out_xf_preaffine(self) -> tuple[tuple, tuple, tuple]:
        """Prepare each xform/iterator pre_affine parameters for writing out.
        This will prep both flam3_affine style and F3H_affine style. In case of the F3H_affine style it will prep the Rotation angle parameter as well.

        Args:
            (self):

        Returns:
            (tuple[tuple, tuple, tuple]): tuple[tuple[flam3_affine], tuple[F3H_affine], tuple[F3H Rotation angle]]. tuple of all the FLAM3H xforms/iterators pre_affine parameters prepped into strings for writing out into the Flame preset file.
        """   
        val: list = []
        f3h_val: list = []
        f3h_angleDeg: list = []
        for iter in range(self.iter_count):
            collect: list = [self.node.parmTuple(f"{prm[0]}{iter + 1}").eval() for prm in self.flam3h_iter.sec_preAffine[:-1]]
            angleDeg: float = self.node.parm(f"{self.flam3h_iter.sec_preAffine[-1][0]}{iter + 1}").eval()
            f3h_angleDeg.append(str(round(angleDeg, ROUND_DECIMAL_COUNT)))
            flatten: list = [item for sublist in self.out_affine_rot(collect, angleDeg) for item in sublist]
            f3h_flatten: list = [item for sublist in collect for item in sublist]
            val.append([str(x) for x in flatten])
            f3h_val.append([str(x) for x in f3h_flatten])
        return tuple([" ".join(x) for x in self.out_util_round_floats(val)]), tuple([" ".join(x) for x in self.out_util_round_floats(f3h_val)]), tuple(f3h_angleDeg)
    
    
    def __out_xf_postaffine(self) -> tuple[tuple, tuple, tuple]:
        """Prepare each xform/iterator post_affine parameters for writing out.
        This will prep both flam3_affine style and F3H_affine style. In case of the F3H_affine style it will prep the Rotation angle parameter as well.

        Args:
            (self):

        Returns:
            (tuple[tuple, tuple, tuple]): tuple[tuple[str: flam3_affine], tuple[str: F3H_affine], tuple[str: F3H Rotation angle]]. tuple of all the FLAM3H xforms/iterators post_affine parameters prepped into strings for writing out into the Flame preset file.
        """   
        val: list = []
        f3h_val: list = []
        f3h_angleDeg: list = []
        for iter in range(self.iter_count):
            if self.node.parm(f"{self.flam3h_iter_prm_names.postaffine_do}_{iter + 1}").eval():
                collect: list = [self.node.parmTuple(f"{prm[0]}{iter + 1}").eval() for prm in self.flam3h_iter.sec_postAffine[1:-1]]
                angleDeg: float = self.node.parm(f"{self.flam3h_iter.sec_postAffine[-1][0]}{iter + 1}").eval()
                if AFFINE_IDENT != [item for sublist in collect for item in sublist] or angleDeg != 0:
                    f3h_angleDeg.append(str(round(angleDeg, ROUND_DECIMAL_COUNT)))
                    flatten: list = [item for sublist in self.out_affine_rot(collect, angleDeg) for item in sublist]
                    f3h_flatten: list = [item for sublist in collect for item in sublist]
                    val.append([str(x) for x in flatten])
                    f3h_val.append([str(x) for x in f3h_flatten])
                else:
                    val.append([])
                    f3h_val.append([])
                    f3h_angleDeg.append([])
            else:
                val.append([])
                f3h_val.append([])
                f3h_angleDeg.append([])
        return tuple([" ".join(x) for x in self.out_util_round_floats(val)]), tuple([" ".join(x) for x in self.out_util_round_floats(f3h_val)]), tuple(f3h_angleDeg)


    def __out_finalxf_preaffine(self) -> tuple[str, str, str]:
        """Prepare each FF/finalXform pre_affine parameters for writing out.
        This will prep both flam3_affine style and F3H_affine style. In case of the F3H_affine style it will prep the Rotation angle parameter as well.

        Args:
            (self):

        Returns:
            (tuple[str, str, str]): tuple[str: flam3_affine, str: F3H_affine, str: F3H Rotation angle]. tuple of strings for all the FLAM3H FF/finalXform pre_affine parameters prepped into strings for writing out into the Flame preset file.
        """   
        collect: list = [self.node.parmTuple(f"{prm[0]}").eval() for prm in self.flam3h_iter_FF.sec_preAffine_FF[:-1]]
        angleDeg: float = self.node.parm(f"{self.flam3h_iter_FF.sec_preAffine_FF[-1][0]}").eval()
        f3h_angleDeg: str = str(angleDeg)
        f3h_affine: list[str] | list[list[str]] | tuple[str] = self.out_util_round_floats(collect)
        if angleDeg != 0.0:
            affine: list[str] | list[list[str]] | tuple[str] = self.out_util_round_floats(self.out_affine_rot(collect, angleDeg)) # type: ignore
        else:
            affine: list[str] | list[list[str]] | tuple[str] = f3h_affine
        flatten: list = [item for sublist in affine for item in sublist]
        f3h_flatten: list = [item for sublist in f3h_affine for item in sublist]
        return " ".join(flatten), " ".join(f3h_flatten), f3h_angleDeg
    
    
    def __out_finalxf_postaffine(self) -> tuple[str, str, str]:
        """Prepare each FF/finalXform post_affine parameters for writing out.
        This will prep both flam3_affine style and F3H_affine style. In case of the F3H_affine style it will prep the Rotation angle parameter as well.

        Args:
            (self):

        Returns:
            (tuple[str, str, str]): tuple[str: flam3_affine, str: F3H_affine, str: F3H Rotation angle]. tuple of strings for all the FLAM3H FF/finalXform post_affine parameters prepped into strings for writing out into the Flame preset file.
        """  
        if self.node.parm(f"{PRX_FF_PRM}{self.flam3h_iter_prm_names.postaffine_do}").eval():
            collect: list = [self.node.parmTuple(f"{prm[0]}").eval() for prm in self.flam3h_iter_FF.sec_postAffine_FF[1:-1]]
            angleDeg: float = self.node.parm(f"{self.flam3h_iter_FF.sec_postAffine_FF[-1][0]}").eval()
            if AFFINE_IDENT != [item for sublist in collect for item in sublist] or angleDeg != 0:
                f3h_angleDeg: str = str(angleDeg)
                f3h_affine: list[str] | list[list[str]] | tuple[str] = self.out_util_round_floats(collect)
                if angleDeg != 0.0:
                    affine: list[str] | list[list[str]] | tuple[str] = self.out_util_round_floats(self.out_affine_rot(collect, angleDeg)) # type: ignore
                else:
                    affine: list[str] | list[list[str]] | tuple[str] = f3h_affine
                flatten: list = [item for sublist in affine for item in sublist]
                f3h_flatten: list = [item for sublist in f3h_affine for item in sublist]
                return " ".join(flatten), " ".join(f3h_flatten), f3h_angleDeg
            else:
                return '', '', ''
        else:
            return '', '', ''
    
    
    def __out_palette_hex(self) -> str:
        """Prepare the FLAM3H palette ramp parameter to be written out into the Flame preset file.

        Args:
            (self):

        Returns:
            (str): The FLAM3H palette prepped into a string and converted into hex values.
        """  
        _PALETTE_KEYS_OUT = self.out_palette_keys_count(self.palette_plus_do, len(self.palette.keys()), 0)
        POSs: list = list(iter_islice(iter_count(0, 1.0/(int(_PALETTE_KEYS_OUT)-1)), int(_PALETTE_KEYS_OUT)))
        HEXs: list = [flam3h_palette_utils.rgb_to_hex(tuple(self.palette.lookup(p))) for p in POSs]
        n: int = 8
        hex_grp: list = [HEXs[i:i + n] for i in range(0, len(HEXs), n)]
        hex_join: list = [f"      {''.join(grp)}\n" for grp in hex_grp] # 6 times \s
        return f"\n{''.join(hex_join)}    " # 4 times \s
        
    
    # custom to FLAM3H only
    def __out_flame_data_flam3h_hsv(self, prm_name = CP_RAMP_HSV_VAL_NAME) -> str | bool:
        """Prepare the FLAM3H palette HSV parameter to be written out into the Flame preset file.

        Args:
            (self):

        Returns:
            (str): The FLAM3H palette HSV parameter prepped into a string.
        """  
        if prm_name == CP_RAMP_HSV_VAL_NAME:
            # This is only for OUT ramp HSV vals.
            # If we are saving out a flame with the HSV ramp, 
            # we do not want to export the HSV values in the XML file anymore
            # so to not overimpose a color correction once we load it back.
            if self.palette_hsv_do:
                return False
            else:
                # Here we go ahead since we know the prm CP_RAMP_HSV_VAL_NAME is a tuple
                prm: tuple = self.node.parmTuple(prm_name).eval()
                # If the HSV values are at their defaults, do not export them into the XML file
                if prm[0] == prm[1] == prm[2] == 1:
                    return False
                else:
                    return ' '.join([self.out_util_round_float(x) for x in prm])
        else:
            print(f"Warning:\n{self.node.name()}: parameter name: \"{prm_name}\" not found. Please pass in a valid FLAM3H ramp hsv parameter name.\n")
            return False
        
        
    # custom to FLAM3H only
    def __out_flame_data_flam3h_mb_val(self, prm_name: str = '') -> str | bool:
        """Prepare the FLAM3H motion blur single val parameter to be written out into the Flame preset file.

        Args:
            (self):
            prm_name(str): The name of the FLAM3H motion blur parameter to be prep into a string for writing out.

        Returns:
            (str): The FLAM3H motion blur single val parameter prepped into a string.
        """  
        if self.flam3h_mb_do:
            try:
                self.out_util_round_float(self.node.parm(prm_name).eval())
            except:
                print(f"Warning:\n{self.node.name()}: parameter name: \"{prm_name}\" not found. Please pass in a valid FLAM3H val parameter name.\n")
                return False
            else:
                return self.out_util_round_float(self.node.parm(prm_name).eval())
        else:
            return False
        
        
    # custom to FLAM3H only
    def __out_flame_data_flam3h_toggle(self, toggle: bool) -> str:
        """Prepare a FLAM3H toggle value to be written out into the Flame preset file.

        Args:
            (self):
            toggle(bool): This data to be passed in is collected ahead of time inside class "out_flame_utils".

        Returns:
            (str): The FLAM3H toggle prepped into a string.
        """  
        return str(toggle)
    
    
    # custom to FLAM3H only
    def __out_flame_palette_lookup_samples(self) -> str | bool:
        """Prepare the FLAM3H lookup samples to be written out into the Flame preset file.
        It will check if palette 256+ is active and if so if the number of palette color keys are enough to use higher samples or not.
        IF plaette 256+ toggle is off, it will check if the user is using a lookup sample value different from default and store it if so.
        
        Args:
            (self):

        Returns:
            (str): The FLAM3H lookup samples for this Flame prepped into a string.
        """  
        if self.palette_plus_do:
            keys: str = out_flame_utils(self.kwargs).out_palette_keys_count(self.palette_plus_do, len(self.palette.keys()), 0, False)
            if self.flam3h_cp_lookup_samples > int(keys): keys: str = str(self.flam3h_cp_lookup_samples)
            if int(keys) == 256:
                return False
            else:
                return keys
        else:
            if self.flam3h_cp_lookup_samples == 256:
                return False
            else:
                return str(self.flam3h_cp_lookup_samples)


# OUT FLAME RENDER PROPERTIES start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class out_flame_render_properties(out_flame_utils):
    """
    Args:
        out_flame_utils ([class]): [inherit properties methods from the out_flame_utils class]
    """  

    __slots__ = ("_flame_name", "_flame_size", "_flame_center", "_flame_scale", "_flame_rotate", "_flame_quality", "_flame_brightness", "_flame_gamma", "_flame_k2", "_flame_vibrancy", "_flame_highlight", 
                 "_flame_render_curves", "_flame_overall_curve", "_flame_red_curve", "_flame_green_curve", "_flame_blue_curve", 
                 "_flam3h_sys_rip", "_flam3h_cp_hsv", "_flam3h_mb_fps", "_flam3h_mb_samples", "_flam3h_mb_shutter", "_flam3h_cp_samples", "_flam3h_prefs_f3c")

    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """ 
        super().__init__(kwargs)
        
        self._flame_name: str = self._out_flame_utils__out_flame_name() # type: ignore
        self._flame_size: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE)) # type: ignore
        self._flame_center: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER)) # type: ignore
        self._flame_scale: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE)) # type: ignore
        self._flame_rotate: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE)) # type: ignore
        self._flame_quality: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY)) # type: ignore
        self._flame_brightness: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS)) # type: ignore
        self._flame_gamma: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA)) # type: ignore
        self._flame_k2: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2)) # type: ignore
        self._flame_vibrancy: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY)) # type: ignore
        self._flame_highlight: str = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER)) # type: ignore
        
        # OUT render curves
        # We can directly get the data from the FLAM3H UI parameters since they have been checked on creation already.
        self._flame_render_curves: str = self.node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVES)).eval()
        self._flame_overall_curve: str = self.node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_OVERALL)).eval()
        self._flame_red_curve: str = self.node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_RED)).eval()
        self._flame_green_curve: str = self.node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_GREEN)).eval()
        self._flame_blue_curve: str = self.node.parm(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_RENDER_CURVE_BLUE)).eval()
        
        # custom to FLAM3H only
        self._flam3h_sys_rip: str = self._out_flame_utils__out_flame_data_flam3h_toggle(self._flam3h_rip) # type: ignore
        self._flam3h_cp_hsv: str | bool = self._out_flame_utils__out_flame_data_flam3h_hsv() # type: ignore
        self._flam3h_mb_fps: str | bool = self._out_flame_utils__out_flame_data_flam3h_mb_val(MB_FPS) # type: ignore
        self._flam3h_mb_samples: str | bool = self._out_flame_utils__out_flame_data_flam3h_mb_val(MB_SAMPLES) # type: ignore
        self._flam3h_mb_shutter: str | bool = self._out_flame_utils__out_flame_data_flam3h_mb_val(MB_SHUTTER) # type: ignore
        self._flam3h_cp_samples: str | bool = self._out_flame_utils__out_flame_palette_lookup_samples() # type: ignore
        self._flam3h_prefs_f3c: str = self._out_flame_utils__out_flame_data_flam3h_toggle(self._flam3h_f3c) # type: ignore
        

    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def flame_name(self):
        return self._flame_name
    
    @property
    def flame_size(self):
        return self._flame_size
    
    @property
    def flame_center(self):
        return self._flame_center
    
    @property
    def flame_scale(self):
        return self._flame_scale
    
    @property
    def flame_rotate(self):
        return self._flame_rotate
    
    @property
    def flame_quality(self):
        return self._flame_quality
    
    @property
    def flame_brightness(self):
        return self._flame_brightness
    
    @property
    def flame_gamma(self):
        return self._flame_gamma
    
    @property
    def flame_k2(self):
        return self._flame_k2
    
    @property
    def flame_vibrancy(self):
        return self._flame_vibrancy
    
    @property
    def flame_highlight(self):
        return self._flame_highlight
    
    # OUT render curves
    
    @property
    def flame_render_curves(self):
        return self._flame_render_curves
    
    @property
    def flame_overall_curve(self):
        return self._flame_overall_curve
    
    @property
    def flame_red_curve(self):
        return self._flame_red_curve
    
    @property
    def flame_green_curve(self):
        return self._flame_green_curve
    
    @property
    def flame_blue_curve(self):
        return self._flame_blue_curve
    
    # custom to FLAM3H only
    
    @property
    def flam3h_sys_rip(self):
        return self._flam3h_sys_rip
    
    @property
    def flam3h_cp_hsv(self):
        return self._flam3h_cp_hsv
    
    @property
    def flam3h_mb_fps(self):
        return self._flam3h_mb_fps
    
    @property
    def flam3h_mb_samples(self):
        return self._flam3h_mb_samples
    
    @property
    def flam3h_mb_shutter(self):
        return self._flam3h_mb_shutter
    
    @property
    def flam3h_cp_samples(self):
        return self._flam3h_cp_samples
    
    @property
    def flam3h_prefs_f3c(self):
        return self._flam3h_prefs_f3c


# OUT FLAME XFORMS DATA start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class out_flame_xforms_data(out_flame_utils):
    """
    Args:
        out_flame_utils ([class]): [inherit properties methods from the out_flame_utils class]
    """  
    
    __slots__ = ("_xf_name", "_xf_vactive", "_xf_weight", "_xf_xaos", 
                 "_xf_color", "_xf_symmetry", "_xf_color_speed", "_xf_opacity", 
                 "_xf_pre_blur", 
                 "_xf_preaffine", "_xf_f3h_preaffine", "_xf_f3h_preaffine_angle", "_xf_postaffine", "_xf_f3h_postaffine", "_xf_f3h_postaffine_angle", 
                 "_finalxf_name", "_finalxf_preaffine", "_finalxf_f3h_preaffine", "_finalxf_f3h_preaffine_angle", "_finalxf_postaffine", "_finalxf_f3h_postaffine", "_finalxf_f3h_postaffine_angle", 
                 "_palette_hex",)
    
    def __init__(self, kwargs: dict) -> None:
        """
        Args:
            kwargs(dict): this FLAM3H node houdini kwargs.
            
        Returns:
            (None):
        """ 
        super().__init__(kwargs)
        
        # FLAM3 data
        self._xf_name: tuple = self._out_flame_utils__out_xf_name() # type: ignore
        self._xf_vactive: tuple = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.main_vactive) # type: ignore
        self._xf_weight: tuple = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.main_weight) # type: ignore
        self._xf_xaos: tuple = self._out_flame_utils__out_xf_xaos() # type: ignore
        
        self._xf_color: tuple = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.shader_color) # type: ignore
        self._xf_symmetry: tuple = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.shader_speed) # type: ignore
        self._xf_color_speed: tuple = self._out_flame_utils__out_xf_data_color_speed() # type: ignore
        self._xf_opacity: tuple = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.shader_alpha) # type: ignore
        
        self._xf_pre_blur: tuple = self._out_flame_utils__out_xf_pre_blur() # type: ignore
        
        self._xf_preaffine: tuple = self._out_flame_utils__out_xf_preaffine()[0] # type: ignore
        self._xf_f3h_preaffine: tuple = self._out_flame_utils__out_xf_preaffine()[1] # type: ignore
        self._xf_f3h_preaffine_angle: tuple = self._out_flame_utils__out_xf_preaffine()[2] # type: ignore
        self._xf_postaffine: tuple = self._out_flame_utils__out_xf_postaffine()[0] # type: ignore
        self._xf_f3h_postaffine: tuple = self._out_flame_utils__out_xf_postaffine()[1] # type: ignore
        self._xf_f3h_postaffine_angle: tuple = self._out_flame_utils__out_xf_postaffine()[2] # type: ignore
        
        self._finalxf_name: str = self._out_flame_utils__out_finalxf_name() # type: ignore
        self._finalxf_preaffine: str = self._out_flame_utils__out_finalxf_preaffine()[0] # type: ignore
        self._finalxf_f3h_preaffine: str = self._out_flame_utils__out_finalxf_preaffine()[1] # type: ignore
        self._finalxf_f3h_preaffine_angle: str = self._out_flame_utils__out_finalxf_preaffine()[2] # type: ignore
        self._finalxf_postaffine: str = self._out_flame_utils__out_finalxf_postaffine()[0] # type: ignore
        self._finalxf_f3h_postaffine: str = self._out_flame_utils__out_finalxf_postaffine()[1] # type: ignore
        self._finalxf_f3h_postaffine_angle: str = self._out_flame_utils__out_finalxf_postaffine()[2] # type: ignore
        
        self._palette_hex: str = self._out_flame_utils__out_palette_hex() # type: ignore


    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def xf_name(self):
        return self._xf_name
    
    @property
    def xf_vactive(self):
        return self._xf_vactive
    
    @property
    def xf_weight(self):
        return self._xf_weight
    
    @property
    def xf_xaos(self):
        return self._xf_xaos
    
    @property
    def xf_pre_blur(self):
        return self._xf_pre_blur
    
    @property
    def xf_color(self):
        return self._xf_color
    
    @property
    def xf_symmetry(self):
        return self._xf_symmetry
    
    @property
    def xf_color_speed(self):
        return self._xf_color_speed
    
    @property
    def xf_opacity(self):
        return self._xf_opacity
    
    @property
    def xf_preaffine(self):
        return self._xf_preaffine
    
    @property
    def xf_f3h_preaffine(self):
        return self._xf_f3h_preaffine
    
    @property
    def xf_f3h_preaffine_angle(self):
        return self._xf_f3h_preaffine_angle
    
    @property
    def xf_postaffine(self):
        return self._xf_postaffine
    
    @property
    def xf_f3h_postaffine(self):
        return self._xf_f3h_postaffine
    
    @property
    def xf_f3h_postaffine_angle(self):
        return self._xf_f3h_postaffine_angle
    
    @property
    def palette_hex(self):
        return self._palette_hex
    
    @property
    def finalxf_name(self):
        return self._finalxf_name
    
    @property
    def finalxf_preaffine(self):
        return self._finalxf_preaffine
    
    @property
    def finalxf_f3h_preaffine(self):
        return self._finalxf_f3h_preaffine
    
    @property
    def finalxf_f3h_preaffine_angle(self):
        return self._finalxf_f3h_preaffine_angle
    
    @property
    def finalxf_postaffine(self):
        return self._finalxf_postaffine
    
    @property
    def finalxf_f3h_postaffine(self):
        return self._finalxf_f3h_postaffine
    
    @property
    def finalxf_f3h_postaffine_angle(self):
        return self._finalxf_f3h_postaffine_angle
