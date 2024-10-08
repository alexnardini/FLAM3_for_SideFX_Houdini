from __future__ import division
from __future__ import annotations
from platform import python_version
from platform import system as platform_system
from typing import Union
from typing import Callable
from typing import KeysView
from itertools import count as iter_count
from itertools import islice as iter_islice
from textwrap import wrap
from datetime import datetime
from math import sin
from math import cos
from math import fsum
from copy import copy
from re import sub as re_sub
from numpy import pad as np_pad
from numpy import resize as np_resize
from numpy import transpose as np_transpose
from numpy import searchsorted as np_searchsorted
from webbrowser import open as www_open
from inspect import cleandoc as i_cleandoc
import lxml.etree as lxmlET
import os
import json
import colorsys
import hou
import nodesearch



#   Tested on:  PYTHON v3.7.13  (H19)
#               PYTHON v3.9.10  (H19.5)
#               PYTHON v3.10.10 (H20)
#               PYTHON v3.11.7  (H20.5)
#
#   Title:      SideFX Houdini FLAM3: PYTHON
#   Author:     Alessandro Nardini
#   date:       January 2023, Last revised October 2024
#
#   Name:       PY_FLAM3 "PYTHON"
#
#   Comment:    Python classes and definitions for:
#               - General UX
#               - Menus builder
#               - Copy/Paste iterator's data
#               - Load/Save flame files
#               - Load/Save palettes
#               - Fully automated UX Xaos
#               - Tool's user experience
#               
#               Everything is then glued together inside Houdini.



'''
LIST OF CLASSES:

    flam3h_iterator_prm_names
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




FLAM3H_VERSION = '1.4.84'
FLAM3H_VERSION_STATUS_BETA = " - Beta"
FLAM3H_VERSION_STATUS_GOLD = " - Gold"

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

# Node user data
FLAM3H_USER_DATA_PRX = "nodeinfo_"
FLAM3H_USER_DATA_ITER = "Marked iterator"
FLAM3H_USER_DATA_FF = "Marked FF"

# Main tab in the UI
FLAM3H_ITERATORS_TAB = "f_flam3h"

# Default affine values
AFFINE_DEFAULTS: dict = {"affine_x": hou.Vector2((1.0, 0.0)), "affine_y": hou.Vector2((0.0, 1.0)), "affine_o": hou.Vector2((0.0, 0.0)), "angle": float(0.0)} # X, Y, O, ANGLE
AFFINE_IDENT: list = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

# FF parametric parameter's prefixes
PRX_FF_PRM = 'ff'
PRX_FF_PRM_POST = 'fp1'

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
PALETTE_COUNT_64 = '64'
PALETTE_COUNT_128 = '128'
PALETTE_COUNT_256 = '256'
PALETTE_COUNT_512 = '512' # not used
PALETTE_COUNT_1024 = '1024'
PALETTE_OUT_MENU_OPTIONS: tuple = (256, 512, 1024)
PALETTE_PLUS_MSG = '[256+]'
# The following will always be used for now
# even tho we check for the XML palette format on load.
PALETTE_FORMAT = 'RGB'

# Parameters at hand
GLB_DENSITY = 'ptcount'
GLB_DENSITY_PRESETS = 'ptcount_presets'
GLB_ITERATIONS = 'iter'
SYS_SELECT_ITERATOR = 'iterlist'
SYS_DO_FF = 'doff'
SYS_RIP = 'rip'
SYS_TAG = 'tag'
SYS_TAG_SIZE = 'tagsize'
SYS_FRAME_VIEW_SENSOR = 'frameviewsensor'
FLAME_ITERATORS_COUNT = 'flamefunc'
CP_ISVALID_FILE = 'cpisvalidfile'
CP_ISVALID_PRESET = 'cpisvalidpreset'
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
CP_RAMP_SAVE_256_PLUS = 'cppaletteplus'
CP_RAMP_SAVE_HSV = 'savehsv'
CP_RAMP_HSV_KEEP_ON_LOAD = 'keephsv'
CP_RAMP_HSV_VAL_NAME = 'hsv'
MB_DO = 'domb'
MB_FPS = 'fps'
MB_SAMPLES = 'mbsamples'
MB_SHUTTER = 'shutter'
IN_ISVALID_FILE = 'inisvalidfile'
IN_ISVALID_PRESET = 'inisvalidpreset'
IN_CLIPBOARD_TOGGLE = 'inclipboard'
IN_CLIPBOARD_LABEL_MSG = '[CLIPBOARD]'
IN_PATH = 'inpath'
IN_PRESETS = 'inpresets'
IN_PRESETS_OFF = "inpresets_disabled"
IN_SYS_PRESETS = 'sys_inpresets'
IN_SYS_PRESETS_OFF = 'sys_inpresets_disabled'
IN_USE_ITER_ON_LOAD = 'useiteronload'
IN_OVERRIDE_ITER_FLAME_NAME = 'oritername'
IN_ITER_NUM_ON_LOAD = 'iternumonload'
IN_FLAM3H_AFFINE_STYLE = 'in_f3h_affine'
IN_REMAP_PRE_GAUSSIAN_BLUR = 'remappgb'
IN_COPY_RENDER_PROPERTIES_ON_LOAD = 'propertiescp'
OUT_ISVALID_FILE = 'outisvalidfile'
OUT_PATH = 'outpath'
OUT_PRESETS = 'outpresets'
OUT_SYS_PRESETS = 'sys_outpresets'
OUT_FLAME_PRESET_NAME = 'outname'
OUT_AUTO_ADD_ITER_NUM = 'autoadditer'
OUT_UPDATE_SENSOR = 'outsensorupdate'
OUT_PALETTE_256_PLUS = 'outpaletteplus'
OUT_HSV_PALETTE_DO = 'outpalette'
OUT_FLAM3H_AFFINE_STYLE = 'out_f3h_affine'
OUT_USE_FRACTORIUM_PRM_NAMES = 'outfractoriumprm'
OUT_PALETTE_FILE_EXT = '.json'
OUT_FLAM3_FILE_EXT = '.flame'
OUT_RENDER_PROPERTIES_EDIT = 'outedit'
OUT_RENDER_PROPERTIES_SENSOR = 'outsensor'
OUT_RENDER_PROPERTIES_RES_PRESETS_MENU = 'outrespresets'

# Those Null node names are hard coded here and represent the nodes name's prefix.
# If you change those Null node names inside the FLAM3H houdini HDA network, update those global variables as well.
# If not, the camera sensor mode wont be able to properly frame itself in the current viewport.
OUT_BBOX_NODE_NAME_SENSOR = 'OUT_bbox_sensor'
OUT_BBOX_NODE_NAME_REFRAME = 'OUT_bbox_reframe'

PREFS_TOGGLE = 'showprefs'
PREFS_FLASH_MSG = 'flashmsg'
PREFS_F3C = 'f3c'
PREFS_ITERATOR_BOOKMARK_ICONS = 'itericons'
PREFS_ENUMERATE_MENU = 'enumeratemenu'
PREFS_AUTO_PATH_CORRECTION = 'autopath'
PREFS_CVEX_PRECISION = 'vex_precision'
PREFS_XAOS_MODE = 'xm'
PREFS_XAOS_AUTO_SPACE = 'xaosdiv'
PREFS_CAMERA_HANDLE = 'camhandle'
PREFS_CAMERA = 'fcam'
PREFS_CAMERA_CULL = 'camcull'
PREFS_CAMERA_CULL_AMOUNT = 'cullamount'
PREFS_VIEWPORT_DARK = 'setdark'
PREFS_VIEWPORT_PT_TYPE = 'vptype'
PREFS_VIEWPORT_PT_SIZE = 'vpptsize'
# Message parameters
MSG_FLAMESTATS = 'flamestats_msg'
MSG_FLAMESENSOR = 'flamesensor_msg'
MSG_FLAMERENDER = 'flamerender_msg'
MSG_DESCRIPTIVE_PRM = 'descriptive_msg'
MSG_PALETTE = 'palettemsg'
MSG_OUT = 'outmsg'
# Message About Tab parameters
MSG_FLAM3H_ABOUT = 'flam3about_msg'
MSG_FLAM3H_PLUGINS = 'flam3plugins_msg'
MSG_FLAM3H_WEB = 'flam3h_heading_web'
MSG_FLAM3H_GIT = 'flam3h_heading_git'
MSG_FLAM3H_INSTA = 'flam3h_heading_insta'
MSG_FLAM3H_YOUTUBE = 'flam3h_heading_youtube'
MSG_FLAM3_PDF = 'flam3_heading_pdf'
MSG_FLAM3_GIT = 'flam3_heading_git'
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
# self prm names for user data
FLAM3H_DATA_PRM_XAOS_MP_MEM = 'flam3h_data_mpmem'
FLAM3H_DATA_PRM_XAOS_PREV = 'flam3h_data_xaos'
FLAM3H_DATA_PRM_MPIDX = 'flam3h_data_mpidx'

# Flash messages timer
FLAM3H_FLASH_MESSAGE_TIMER: float = 2



class flam3h_iterator_prm_names:

    '''
    Mostly, handy to have all those packed into one class
    for easy access everywhere is needed and better readability.
    
    The parameter names for the FF(finalXform) are the same but with a string prefix: 'ff'
    The FF parametric parameter names are as well the same but with a string presfix: 'ff_'
    Main, Xaos and Shader parameters are not included in the FF but only: Pre, Var, post, Pre affine and Post affine.
    
    Note:
        The following definitions:
        
            flam3h_iterator_utils.iterator_keep_last_vactive(self) -> None:
            flam3h_iterator_utils.iterator_keep_last_vactive_STAR(self) -> None:
            flam3h_iterator_utils.iterator_keep_last_weight(self) -> None:
            flam3h_iterator_utils.menu_select_iterator_data(self) -> list:
            flam3h_iterator_utils.menu_select_iterator(self) -> list:
            flam3h_iterator_utils.menu_copypaste(self) -> list:
            flam3h_iterator_utils.menu_copypaste_FF(self) -> list:
            
        have houdini parameter's names hard coded inside as they are not using
        this class in an attempt to try to speed up a tiny, tiny bit.
        
        The hard coded parameter's names are:
        
            flam3h_iterator_prm_names.main_vactive = 'vactive'
            flam3h_iterator_prm_names.main_weight = 'iw'
            
        If you update/change those, please update inside the above mentioned functions.
    
    '''
    # ITERATOR
    #
    # Main
    main_mpmem = 'mpmem' # auto set xaos: custom data
    main_note = 'note'
    main_prmpastesel = 'prmpastesel'
    main_selmem = 'selmem' # custom data
    main_vactive = 'vactive'
    main_weight = 'iw'
    # Xaos
    xaos = 'xaos'
    # Shader
    shader_color = 'clr'
    shader_speed = 'clrspeed'
    shader_alpha = 'alpha'
    # Pre 
    prevar_blur = 'preblurtype' # this can be omitted as it is always zero
    prevar_weight_blur = 'preblurweight'
    prevar_type_1 = 'pre1type'
    prevar_type_2 = 'pre2type'
    prevar_weight_1 = 'pre1weight'
    prevar_weight_2 = 'pre2weight'
    # Var
    var_type_1 = 'v1type'
    var_type_2 = 'v2type'
    var_type_3 = 'v3type'
    var_type_4 = 'v4type'
    var_weight_1 = 'v1weight'
    var_weight_2 = 'v2weight'
    var_weight_3 = 'v3weight'
    var_weight_4 = 'v4weight'
    # Post
    postvar_type_1 = 'p1type'
    postvar_type_2 = 'p2type'
    postvar_weight_1 = 'p1weight'
    postvar_weight_2 = 'p2weight'
    # Pre affine
    preaffine_x = 'x'
    preaffine_y = 'y'
    preaffine_o = 'o'
    preaffine_ang = 'ang'
    # post affine
    postaffine_do = 'dopost'
    postaffine_x = 'px'
    postaffine_y = 'py'
    postaffine_o = 'po'
    postaffine_ang = 'pang'
    

class flam3h_varsPRM:

    DPT = '*'
    PRM = '...'
    # Collect all variations and their parametric parameters properly ordered as per flame*.h files
    # Those names are what it will appear inside each variation's menu.
    varsPRM = ( ("Linear", 0), 
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
    
    
    
    def vars_all(self) -> list:
        """
        Returns:
            list: [return a list of all the variation names properly ordered as per flame*.h files]
        """

        return list(map(lambda x: x[0], self.varsPRM))
    
    
    def menu_vars_all(self) -> list:
        """
        Returns:
            list: [return an enumerated variations menu list with "linear" being the first one for convenience]
        """        

        vars_no_lin = list(enumerate(self.vars_all()))[1:]
        vars_no_lin.remove((65, 'Pre blur')) # remove "pre blur" as it is hard coded into the chaos game.
        vars_sorted = sorted(vars_no_lin, key=lambda var: var[1])
        return list(enumerate(['Linear'])) + vars_sorted
    
    
    def menu_vars_no_PRM(self) -> list:
        """
        Returns:
            list: [return an enumerated variations menu list with "linear" being the first one for convenience and without parametrics]
        """   
        return list(map(lambda x: x, filter(lambda x: x[1][-3:]!=self.PRM, self.menu_vars_all())))
    
    
    def menu_vars_all_linear(self) -> list:
        """
        Returns:
            list: [return an linearly composed list with the var index followed by the var name as if it was a Houdini valid menu data]
        """  
        linear = []
        for idx, item in self.menu_vars_all():
            linear.append(idx)
            linear.append(item)
        return linear
    
    
    def build_menu_vars_indexes(self) -> dict[int, int]:
        """
        Returns:
            dict: [a dictionary for the variation indexes used by the menu_T_ICONS definitions]
        """   
        keys = []
        values = []
        for id, var in enumerate(self.menu_vars_all_linear()):
            try:
                int(var)
                keys.append(var)
            except:
                values.append(id)
                
        return dict(zip(keys, values))



class flam3h_iterator:

    n = flam3h_iterator_prm_names

    # SECTIONS method lists
    #
    # (*T)Types have no signature and always to be used with: pastePRM_T_from_list() for now.
    
    # sec_main = ( (f"{n.main_vactive}_", 0), (f"{n.main_weight}_", 0) )
    
    sec_main = ( (f"{n.main_weight}_", 0), ) # When copy/paste the main section it will not copy the ON/OFF(vactive) iterator parameter anymore.
    sec_xaos = ( (f"{n.xaos}_", 0), )
    sec_shader = ( (f"{n.shader_color}_", 0), (f"{n.shader_speed}_", 0), (f"{n.shader_alpha}_", 0) )
    sec_prevarsT = ( f"{n.prevar_type_1}_", f"{n.prevar_type_2}_" ) # preblur is omitted as it is always ZERO
    sec_prevarsW = ( (f"{n.prevar_weight_blur}_", 0), (f"{n.prevar_weight_1}_", 0), (f"{n.prevar_weight_2}_", 0) )
    sec_varsT = ( f"{n.var_type_1}_", f"{n.var_type_2}_", f"{n.var_type_3}_", f"{n.var_type_4}_" )
    sec_varsW = ( (f"{n.var_weight_1}_", 0), (f"{n.var_weight_2}_", 0), (f"{n.var_weight_3}_", 0), (f"{n.var_weight_4}_", 0) )
    sec_postvarsT = ( f"{n.postvar_type_1}_", )
    sec_postvarsW = ( (f"{n.postvar_weight_1}_", 0), )
    sec_preAffine = ( (f"{n.preaffine_x}_", 1), (f"{n.preaffine_y}_", 1), (f"{n.preaffine_o}_", 1), (f"{n.preaffine_ang}_", 0) )
    sec_postAffine = ( (f"{n.postaffine_do}_", 0), (f"{n.postaffine_x}_", 1), (f"{n.postaffine_y}_", 1), (f"{n.postaffine_o}_", 1), (f"{n.postaffine_ang}_", 0) )
    
    # ALL method lists
    allT = sec_prevarsT + sec_varsT + sec_postvarsT
    allMisc = sec_main + sec_shader + sec_prevarsW + sec_varsW + sec_postvarsW + sec_preAffine + sec_postAffine


class flam3h_varsPRM_FF(flam3h_varsPRM):
    """
    Args:
        flam3h_varsPRM ([class]): [inherit properties methods from the flam3h_varsPRM class]
    """    
    def __init__(self, prx: str):
        """
        Args:
            prx (str): [parameter name prefix string]
        """        
        self.prx = prx

    def varsPRM_FF(self) -> tuple:

        varsPRM_FF = (  self.varsPRM[0], 
                        self.varsPRM[1], 
                        self.varsPRM[2], 
                        self.varsPRM[3], 
                        self.varsPRM[4], 
                        self.varsPRM[5], 
                        self.varsPRM[6], 
                        self.varsPRM[7], 
                        self.varsPRM[8], 
                        self.varsPRM[9], 
                        self.varsPRM[10], 
                        self.varsPRM[11], 
                        self.varsPRM[12], 
                        self.varsPRM[13], 
                        self.varsPRM[14], 
                        self.varsPRM[15], 
                        self.varsPRM[16], 
                        self.varsPRM[17], 
                        self.varsPRM[18], 
                        self.varsPRM[19], 
                        self.varsPRM[20], 
                        self.varsPRM[21], 
                        self.varsPRM[22], 
                        self.varsPRM[23], 
                        self.varsPRM[24], 
                        self.varsPRM[25], 
                        self.varsPRM[26], 
                        (self.varsPRM[27][0], (f"{self.prx}_{self.varsPRM[27][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[28][0], (f"{self.prx}_{self.varsPRM[28][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[29][0], (f"{self.prx}_{self.varsPRM[29][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[30][0], (f"{self.prx}_{self.varsPRM[30][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[31][0], (f"{self.prx}_{self.varsPRM[31][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[32][0], (f"{self.prx}_{self.varsPRM[32][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[33][0], 0), 
                        (self.varsPRM[34][0], (f"{self.prx}_{self.varsPRM[34][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[35][0], (f"{self.prx}_{self.varsPRM[35][1][0][:-1]}", 0), 1), 
                        (self.varsPRM[36][0], (f"{self.prx}_{self.varsPRM[36][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[37][0], (f"{self.prx}_{self.varsPRM[37][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[38][0], (f"{self.prx}_{self.varsPRM[38][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[39][0], 0), 
                        (self.varsPRM[40][0], 0), 
                        (self.varsPRM[41][0], 0), 
                        (self.varsPRM[42][0], 0), 
                        (self.varsPRM[43][0], 0), 
                        (self.varsPRM[44][0], 0), 
                        (self.varsPRM[45][0], 0), 
                        (self.varsPRM[46][0], 0), 
                        (self.varsPRM[47][0], (f"{self.prx}_{self.varsPRM[47][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[48][0], (f"{self.prx}_{self.varsPRM[48][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[48][2][0][:-1]}", 1), 1), 
                        (self.varsPRM[49][0], (f"{self.prx}_{self.varsPRM[49][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[50][0], (f"{self.prx}_{self.varsPRM[50][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[51][0], (f"{self.prx}_{self.varsPRM[51][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[52][0], (f"{self.prx}_{self.varsPRM[52][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[53][0], (f"{self.prx}_{self.varsPRM[53][1][0][:-1]}", 0), 1),
                        (self.varsPRM[54][0], 0),
                        (self.varsPRM[55][0], 0), 
                        (self.varsPRM[56][0], (f"{self.prx}_{self.varsPRM[56][1][0][:-1]}", 0), 1), 
                        (self.varsPRM[57][0], (f"{self.prx}_{self.varsPRM[57][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[58][0], 0), 
                        (self.varsPRM[59][0], 0), 
                        (self.varsPRM[60][0], 0), 
                        (self.varsPRM[61][0], (f"{self.prx}_{self.varsPRM[61][1][0][:-1]}", 0), 1), 
                        (self.varsPRM[62][0], 0), 
                        (self.varsPRM[63][0], (f"{self.prx}_{self.varsPRM[63][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[63][2][0][:-1]}", 1), 1), 
                        (self.varsPRM[64][0], 0), 
                        (self.varsPRM[65][0], 0), 
                        (self.varsPRM[66][0], (f"{self.prx}_{self.varsPRM[66][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[67][0], (f"{self.prx}_{self.varsPRM[67][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[68][0], 0), 
                        (self.varsPRM[69][0], (f"{self.prx}_{self.varsPRM[69][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[69][2][0][:-1]}", 0), 1), 
                        (self.varsPRM[70][0], 0), 
                        (self.varsPRM[71][0], (f"{self.prx}_{self.varsPRM[71][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[71][2][0][:-1]}", 1), 1), 
                        (self.varsPRM[72][0], (f"{self.prx}_{self.varsPRM[72][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[73][0], (f"{self.prx}_{self.varsPRM[73][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[74][0], (f"{self.prx}_{self.varsPRM[74][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[75][0], (f"{self.prx}_{self.varsPRM[75][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[76][0], (f"{self.prx}_{self.varsPRM[76][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[77][0], (f"{self.prx}_{self.varsPRM[77][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[78][0], (f"{self.prx}_{self.varsPRM[78][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[79][0], (f"{self.prx}_{self.varsPRM[79][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[79][2][0][:-1]}", 1), 1), 
                        (self.varsPRM[80][0], 0), 
                        (self.varsPRM[81][0], 0), 
                        (self.varsPRM[82][0], 0), 
                        (self.varsPRM[83][0], 0), 
                        (self.varsPRM[84][0], 0), 
                        (self.varsPRM[85][0], 0), 
                        (self.varsPRM[86][0], 0), 
                        (self.varsPRM[87][0], 0), 
                        (self.varsPRM[88][0], 0), 
                        (self.varsPRM[89][0], 0), 
                        (self.varsPRM[90][0], 0), 
                        (self.varsPRM[91][0], 0), 
                        (self.varsPRM[92][0], 0), 
                        (self.varsPRM[93][0], 0), 
                        (self.varsPRM[94][0], (f"{self.prx}_{self.varsPRM[94][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[95][0], (f"{self.prx}_{self.varsPRM[95][1][0][:-1]}", 0), 1), 
                        (self.varsPRM[96][0], (f"{self.prx}_{self.varsPRM[96][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[96][2][0][:-1]}", 1), 1),
                        (self.varsPRM[97][0], (f"{self.prx}_{self.varsPRM[97][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[97][2][0][:-1]}", 1), 1), 
                        (self.varsPRM[98][0], (f"{self.prx}_{self.varsPRM[98][1][0][:-1]}", 1), 1), 
                        (self.varsPRM[99][0], (f"{self.prx}_{self.varsPRM[99][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[99][2][0][:-1]}", 1), 1), 
                        (self.varsPRM[100][0], 0), 
                        (self.varsPRM[101][0], (f"{self.prx}_{self.varsPRM[101][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[101][2][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[101][3][0][:-1]}", 1), 1),
                        (self.varsPRM[102][0], (f"{self.prx}_{self.varsPRM[102][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[102][2][0][:-1]}", 1), 1), 
                        (self.varsPRM[103][0], 0),
                        (self.varsPRM[104][0], 0), 
                        (self.varsPRM[105][0], (f"{self.prx}_{self.varsPRM[105][1][0][:-1]}", 1), 1)
                        )
        
        return varsPRM_FF


class flam3h_iterator_FF:
    """
        Note that every parameters inside the FF have the same name as the iterator parameters 
        plus the string "ff" added at the beginning of their names. parametric variation's parameters have the string  "ff_" instead.
        If you create new parameters inside the FF, or change the parameters names inside the FLAM3H iterator,
        please be sure to follow the same nameing convetion so to keep the flam3h_varsPRM: class as the only source for their names.
    """
    n = flam3h_iterator_prm_names

    # SECTIONS method lists
    #
    # (*T)Types have no signature and always to be used with: pastePRM_T_from_list()
    sec_prevarsT_FF = ( f"{PRX_FF_PRM}{n.prevar_type_1}", )
    sec_prevarsW_FF = ( (f"{PRX_FF_PRM}{n.prevar_weight_1}", 0), )
    sec_varsT_FF = ( f"{PRX_FF_PRM}{n.var_type_1}", f"{PRX_FF_PRM}{n.var_type_2}" )
    sec_varsW_FF = ( (f"{PRX_FF_PRM}{n.var_weight_1}", 0), (f"{PRX_FF_PRM}{n.var_weight_2}", 0) )
    sec_postvarsT_FF = ( f"{PRX_FF_PRM}{n.postvar_type_1}", f"{PRX_FF_PRM}{n.postvar_type_2}" )
    sec_postvarsW_FF = ( (f"{PRX_FF_PRM}{n.postvar_weight_1}", 0), (f"{PRX_FF_PRM}{n.postvar_weight_2}", 0) )
    sec_preAffine_FF = ( (f"{PRX_FF_PRM}{n.preaffine_x}", 1), (f"{PRX_FF_PRM}{n.preaffine_y}", 1), (f"{PRX_FF_PRM}{n.preaffine_o}", 1), (f"{PRX_FF_PRM}{n.preaffine_ang}", 0) )
    sec_postAffine_FF = ( (f"{PRX_FF_PRM}{n.postaffine_do}", 0), (f"{PRX_FF_PRM}{n.postaffine_x}", 1), (f"{PRX_FF_PRM}{n.postaffine_y}", 1), (f"{PRX_FF_PRM}{n.postaffine_o}", 1), (f"{PRX_FF_PRM}{n.postaffine_ang}", 0) )
    
    
    # ALL method lists
    # allT_FF list is omitted here because FF PRE VARS, FF VARS and FF POST VARS have their own unique parametric parameters
    # so I need to handle them one by one inside: def prm_paste_FF(kwargs).prm_paste_FF() and prm_paste_FF(kwargs).def prm_paste_sel_FF()
    allMisc_FF = sec_varsW_FF + sec_prevarsW_FF + sec_postvarsW_FF + sec_preAffine_FF + sec_postAffine_FF





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

STATIC METHODS:

set_first_instance_global_var(cvex_precision: int) -> None:

flam3h_check_first_node_instance_msg_status_bar_display_flag(cvex_precision: int, _MSG_INFO: str, _MSG_DONE: str, sys_updated_mode: hou.EnumValue) -> None:

flam3h_check_first_node_instance_msg_status_bar_no_display_flag(node: hou.SopNode, cvex_precision: int, _MSG_INFO: str, _MSG_DONE: str, sys_updated_mode: hou.EnumValue) -> None:

flam3h_set_first_instance_global_var(cvex_precision: int, first_instance_32bit: bool, first_instance_64bit: bool) -> None:

...

METHODS:

flam3h_check_first_node_instance_msg(self, FIRST_TIME_MSG=True) -> None:

flam3h_on_create_set_houdini_session_data(self) -> None:

flam3h_on_create_set_prefs_viewport(self) -> None:

flam3h_on_create(self) -> None:

flam3h_on_loaded(self) -> None:

flam3h_on_deleted(self) -> None:

    """    
    
    def __init__(self, kwargs: dict) -> None:
        self._kwargs = kwargs
        self._node = kwargs['node']



    @staticmethod
    def set_first_instance_global_var(cvex_precision: int) -> None:
        if cvex_precision == 32:
            hou.session.FLAM3H_FIRST_INSTANCE_32BIT = False # type: ignore
        elif cvex_precision == 64:
            hou.session.FLAM3H_FIRST_INSTANCE_64BIT = False # type: ignore


    @staticmethod
    def flam3h_check_first_node_instance_msg_status_bar_display_flag(cvex_precision: int, _MSG_INFO: str, _MSG_DONE: str, sys_updated_mode: hou.EnumValue) -> None:
        """This is temporary until I dnt have time to find a better solution
        to advice the user about the first node compile time without having any leftover
        messages in the Houdini status bar.
        
        This definition will cook and updated the FLAM3H node on creation based on its CVEX precision preference's setting
        if its display flag is True.

        Args:
            cvex_precision (int): 32bit or 64bit - This is the cvex precision preference's option parameter
            _MSG_INFO (str): The message to print in the status bar
            _MSG_DONE (str): The message to print in the hou window 
            sys_updated_mode (hou.EnumValue): houdini updated mode before dropping a FLAM3H node for the first time ( stored from the preFirstCreate script )
        """        
        flam3h_general_utils.set_status_msg(_MSG_INFO, 'WARN')
        if hou.isUIAvailable():
            if hou.ui.displayMessage(_MSG_DONE, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title = "FLAM3H: CVEX 32bit compile", details=None, details_label=None, details_expanded=False) == 0: # type: ignore
                flam3h_scripts.set_first_instance_global_var(cvex_precision)
                hou.setUpdateMode(sys_updated_mode) # type: ignore
                # Print to the Houdini console
                print(f"\nFLAM3H CVEX node compile: DONE\n")
                
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
            node (hou.SopNode): This FLAM3H node
            cvex_precision (int): 32bit or 64bit - This is the cvex precision preference's option parameter
            _MSG_INFO (str): The message to print in the status bar
            _MSG_DONE (str): The message to print in the hou window 
            sys_updated_mode (hou.EnumValue): houdini updated mode before dropping a FLAM3H node for the first time ( stored from the preFirstCreate script )
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
        if cvex_precision == 32 and first_instance_32bit is True:
            hou.session.FLAM3H_FIRST_INSTANCE_32BIT = False # type: ignore
        elif cvex_precision == 64 and first_instance_64bit is True:
            hou.session.FLAM3H_FIRST_INSTANCE_64BIT = False # type: ignore




    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def kwargs(self):
        return self._kwargs
    
    @property
    def node(self):
        return self._node




    def flam3h_check_first_node_instance_msg(self, FIRST_TIME_MSG=True) -> None:
        """This is temporary until I dnt have time to find a better solution
        to advice the user about the first node compile time without having any leftover
        messages in the Houdini status bar.
        
        This definition will cook and updated the FLAM3H node on creation based on its CVEX precision preference's setting
        and based on its display flag status ( Tru or False ).
        
        It will also restore the houdini session update mode if not set already on AutoUpdate.

        Args:
            node (hou.SopNode): FLAM3H node
            FIRST_TIME_MSG (int): False for onLoaded and True for onCreated
        """        
        
        try:
            hou.session.FLAM3H_FIRST_INSTANCE_32BIT # type: ignore
            first_instance_32bit = False
        except:
            first_instance_32bit = True
            
        try:
            hou.session.FLAM3H_FIRST_INSTANCE_64BIT # type: ignore
            first_instance_64bit = False
        except:
            first_instance_64bit = True
            
        node = self.node
        cvex_precision = int( node.parm(PREFS_CVEX_PRECISION).eval() )
                
        if FIRST_TIME_MSG is True and ( first_instance_32bit is True or first_instance_64bit is True ): # type: ignore
            
            if cvex_precision == 32 and first_instance_32bit is True:
                
                hou.setUpdateMode(hou.updateMode.AutoUpdate) # type: ignore
                sys_updated_mode = hou.session.FLAM3H_SYS_UPDATE_MODE # type: ignore
                
                _MSG_INFO = f"FLAM3H v{FLAM3H_VERSION}  first instance -> Compiling FLAM3H CVEX node. Depending on your PC configuration it can take up to 1 minute. It is a one time compile process."
                _MSG_DONE = f"FLAM3H CVEX node compile: DONE \nversion: {FLAM3H_VERSION}{FLAM3H_VERSION_STATUS_GOLD}"
            
                if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
                    flam3h_scripts.flam3h_check_first_node_instance_msg_status_bar_display_flag(cvex_precision, _MSG_INFO, _MSG_DONE, sys_updated_mode) # type: ignore
                else:
                    flam3h_scripts.flam3h_check_first_node_instance_msg_status_bar_no_display_flag(node, cvex_precision,_MSG_INFO, _MSG_DONE, sys_updated_mode) # type: ignore
                    
                    
            elif cvex_precision == 64 and first_instance_64bit is True:

                hou.setUpdateMode(hou.updateMode.AutoUpdate) # type: ignore
                sys_updated_mode = hou.session.FLAM3H_SYS_UPDATE_MODE # type: ignore
                
                _MSG_INFO = f"FLAM3H v{FLAM3H_VERSION} 64-bit  first instance -> Compiling FLAM3H CVEX 64-bit node. Depending on your PC configuration it can take up tp 1 minute. It is a one time compile process."
                _MSG_DONE = f"FLAM3H CVEX 64-bit node compile: DONE\nversion: {FLAM3H_VERSION}"
                
                if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
                    flam3h_scripts.flam3h_check_first_node_instance_msg_status_bar_display_flag(cvex_precision, _MSG_INFO, _MSG_DONE, sys_updated_mode) # type: ignore
                else:
                    flam3h_scripts.flam3h_check_first_node_instance_msg_status_bar_no_display_flag(node, cvex_precision,_MSG_INFO, _MSG_DONE, sys_updated_mode) # type: ignore
                    
            else:
                pass
                
        else:
            flam3h_scripts.flam3h_set_first_instance_global_var(cvex_precision, first_instance_32bit, first_instance_64bit)



    def flam3h_check_first_node_instance_prefs_cvex_precision_msg(self) -> None:
        """When changing CVEX precison modes in the preference's tab,
        this definition will let the user node of the compilie time if a mode is selected for the first time in the current houdini's session.

        Args:
            node (hou.SopNode): FLAM3H node
            FIRST_TIME_MSG (int): False for onLoaded and True for onCreated
        """        
        
        try:
            hou.session.FLAM3H_FIRST_INSTANCE_32BIT # type: ignore
            first_instance_32bit = False
        except:
            first_instance_32bit = True
            
        try:
            hou.session.FLAM3H_FIRST_INSTANCE_64BIT # type: ignore
            first_instance_64bit = False
        except:
            first_instance_64bit = True
                
        if first_instance_32bit is True or first_instance_64bit is True: # type: ignore

            node = self.node
            cvex_precision = int( node.parm(PREFS_CVEX_PRECISION).eval() )
            
            sys_updated_mode = hou.updateModeSetting() # type: ignore
            hou.setUpdateMode(hou.updateMode.AutoUpdate) # type: ignore
            
            if cvex_precision == 32:
                _MSG_INFO = f" FLAM3H v{FLAM3H_VERSION}  first instance -> Compiling FLAM3H CVEX node. Depending on your PC configuration it can take up tp 1 minute. It is a one time compile process."
                _MSG_DONE = f"FLAM3H CVEX node compile: DONE \nversion: {FLAM3H_VERSION}"
            else:
                _MSG_INFO = f" FLAM3H v{FLAM3H_VERSION} 64-bit  first instance -> Compiling FLAM3H CVEX 64-bit node. Depending on your PC configuration it can take up tp 1 minute. It is a one time compile process."
                _MSG_DONE = f"FLAM3H CVEX 64-bit node compile: DONE\nversion: {FLAM3H_VERSION}"
            
            density = node.parm(GLB_DENSITY).evalAsInt()
            if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
                flam3h_general_utils.set_status_msg(_MSG_INFO, 'WARN')
                node.setParms({GLB_DENSITY: 1})
                node.cook(force=True)
                if hou.isUIAvailable():
                    if hou.ui.displayMessage(_MSG_DONE, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title = "FLAM3H: CVEX 64bit compile", details=None, details_label=None, details_expanded=False) == 0: # type: ignore
                        # node.cook(force=True)
                        flam3h_scripts.flam3h_set_first_instance_global_var(cvex_precision, first_instance_32bit, first_instance_64bit)

                        node.setParms({GLB_DENSITY: density})
                        hou.setUpdateMode(sys_updated_mode) # type: ignore
                        flam3h_general_utils.set_status_msg(_MSG_DONE, 'IMP')
                else:
                    flam3h_scripts.flam3h_set_first_instance_global_var(cvex_precision, first_instance_32bit, first_instance_64bit)

                    node.setParms({GLB_DENSITY: density})
                    hou.setUpdateMode(sys_updated_mode) # type: ignore
            else:
                # m = nodesearch.State("Display", True)
                # _display_node = m.nodes(node.parent(), recursive=False)[0]
                flam3h_general_utils.set_status_msg(_MSG_INFO, 'WARN')
                node.setParms({GLB_DENSITY: 1})
                node.cook(force=True)
                flam3h_scripts.flam3h_set_first_instance_global_var(cvex_precision, first_instance_32bit, first_instance_64bit)

                node.setParms({GLB_DENSITY: density})
                hou.setUpdateMode(sys_updated_mode) # type: ignore
                flam3h_general_utils.set_status_msg(_MSG_DONE, 'IMP')



    def flam3h_on_create_set_houdini_session_data(self) -> None:
        """Initialize the necessary data for the copy/paste iterator and FF methods on creation.
        """        
        
        node = self.node
        node_instances = self.node.type().instances()
        
        # FLAM3H node and MultiParameter id for iterators
        # This is to make sure the hou.session's data is at least initialized.
        flam3h_iterator_utils.flam3h_init_hou_session_iterator_data(node)

        # If an iterator was copied from a node that has been deleted
        try:
            hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
        except:
            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = None # type: ignore
            # If we deleted all FLAM3H nodes and we then create a new one,
            # Lets initialize back to himself.
            if len(node_instances) == 1:
                hou.session.FLAM3H_MARKED_ITERATOR_NODE = node # type: ignore

        # FLAM3H node for FF.
        # This is to make sure the hou.session's data is at least initialized.
        flam3h_iterator_utils.flam3h_init_hou_session_ff_data(node)

        # If the FF was copied from a node that has been deleted
        try:
            hou.session.FLAM3H_MARKED_FF_NODE.type() # type: ignore
        except:
            hou.session.FLAM3H_MARKED_FF_CHECK = None # type: ignore
            # If we deleted all FLAM3H nodes and we then create a new one,
            # Lets initialize back to himself.
            if len(node_instances) == 1:
                hou.session.FLAM3H_MARKED_FF_NODE = node # type: ignore
                
        # Initialize FLAM3H viewport Color Scheme
        try:
            hou.session.flam3h_viewport_CS # type: ignore
        except:
            hou.session.flam3h_viewport_CS = [] # type: ignore



    def flam3h_on_create_set_prefs_viewport(self) -> None:
        """Initialize the necessary data for the viewport display preference's option on creation.
        """        
        
        node = self.node
        
        # Update dark history
        flam3h_general_utils(self.kwargs).colorSchemeDark(False) # type: ignore
        # Set other FLAM3H instances to dark if any
        all_f3h = node.type().instances()
        all_f3h_vpptsize = []
        all_f3h_vptype = []
        
        if len(all_f3h) > 1:

            for f3h in all_f3h:
                if f3h != node:
                    all_f3h_vpptsize.append(f3h.parm(PREFS_VIEWPORT_PT_SIZE).evalAsFloat())
                    all_f3h_vptype.append(f3h.parm(PREFS_VIEWPORT_PT_TYPE).evalAsInt())
                    if f3h.parm(PREFS_VIEWPORT_DARK).eval():
                        node.setParms({PREFS_VIEWPORT_DARK: 1})
                        flam3h_general_utils(self.kwargs).colorSchemeDark(False)
                        break
                    else:
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
            
            for view in flam3h_general_utils.util_getSceneViewers():
                settings = view.curViewport().settings()
                size = settings.particlePointSize()
                
                if size != 1:
                    node.setParms({PREFS_VIEWPORT_PT_SIZE: size})
                    
                type = settings.particleDisplayType()
                if type == Pixels:
                    node.setParms({PREFS_VIEWPORT_PT_TYPE: 1})


 
    def flam3h_on_create(self) -> None:
        """Initialize FLAM3H node on creation and all the data it need to run.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
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
        
        # Remove any comment and user data from the node
        flam3h_iterator_utils.del_comment_and_user_data_iterator(node)
        flam3h_iterator_utils.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)



    def flam3h_on_loaded(self) -> None:
        """Initialize FLAM3H node on hip file load and all the data it need to run.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """
        node = self.node
        
        if hou.hipFile.isLoadingHipFile(): #type: ignore
            
            # This is important so loading a hip file with a FLAM3H node inside
            # it wont block the houdini session until user input.
            self.flam3h_check_first_node_instance_msg(False)
            
            # Updated FLAM3H viewport preferences
            self.flam3h_on_create_set_prefs_viewport()
            
            #  mode (int): ZERO: To be used to prevent to load a preset when loading back a hip file.
            flam3h_general_utils(self.kwargs).flam3h_init_presets_CP_PALETTE_PRESETS(0)
            #  mode (int): ZERO: To be used to prevent to load a preset when loading back a hip file.
            flam3h_general_utils(self.kwargs).flam3h_init_presets_IN_PRESETS(0)
            
            flam3h_general_utils(self.kwargs).flam3h_init_presets_OUT_PRESETS()

            # update about tab just in case
            flam3h_about_utils(self.kwargs).flam3h_about_msg()
            flam3h_about_utils(self.kwargs).flam3h_about_plugins_msg()
            flam3h_about_utils(self.kwargs).flam3h_about_web_msg()
            
            # Init xaos
            flam3h_iterator_utils(self.kwargs).auto_set_xaos()
            
            # CAMERA SENSOR
            #
            # If a FLAM3H node is in camera sensor mode and its display flag ON, update the viewport to actually be in camera sensor mode.
            # This work with multiple FLAM3H node becasue there can only be one FLAM3H node in camera sensor mode at any given time.
            if node.isGenericFlagSet(hou.nodeFlag.Display) and node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt(): # type: ignore
                flam3h_general_utils(self.kwargs).util_set_front_viewer(False)
            else:
                # Otherwise just turn the camera sensor mode OFF.
                if node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt():
                    node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
            
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
            # This is being run also from inside: def flam3h_default() - so probably not needed but its not bad to have either.
            #
            # This was causing some issues and got updated.
            flam3h_iterator_utils(self.kwargs).flam3h_paste_reset_hou_session_data()
            
            # Finally reset the hou.session data 
            # ( This probaly not needed but just incase the preview flam3h_paste_reset_hou_session_data() isnt clearing everything properly )
            in_flame_utils(self.kwargs).in_to_flam3h_reset_user_data()
            
            # hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX is already set to None
            # lets set those to ourself to avoid a deleted marked node message on load
            hou.session.FLAM3H_MARKED_ITERATOR_NODE = node # type: ignore
            hou.session.FLAM3H_MARKED_FF_NODE = node # type: ignore
            
        else:
            # CAMERA SENSOR
            # If camera sensor is ON, lets turn it OFF.
            if node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt():
                node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                
            # INIT XAOS - this probably is not needed but I leave it for now
            flam3h_iterator_utils(self.kwargs).auto_set_xaos()
            
            # Reset memory mpidx prm data
            flam3h_iterator_utils.iterator_mpidx_mem_set(node, 0)
            
            # Remove any comment and user data from the node
            if flam3h_iterator_utils.exist_user_data(node):
                flam3h_iterator_utils.del_comment_and_user_data_iterator(node)
            if flam3h_iterator_utils.exist_user_data(node, FLAM3H_USER_DATA_FF):
                flam3h_iterator_utils.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)


    # Wip
    def flam3h_on_deleted(self) -> None:
        """Cleanup the data on deletion.
        """        
        node = self.node
        node_instances = node.type().instances()
        
        if len(node_instances) == 1:
            
            try:
                hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
            except:
                try:
                    if hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX is not None:  # type: ignore
                        hou.session.FLAM3H_MARKED_ITERATOR_NODE = None # type: ignore
                except:
                    pass
                
            try:
                hou.session.FLAM3H_MARKED_FF_NODE.type() # type: ignore
            except:
                try:
                    if hou.session.FLAM3H_MARKED_FF_CHECK is not None:  # type: ignore
                        hou.session.FLAM3H_MARKED_FF_NODE = None # type: ignore
                except:
                    pass
                
            try:
                del hou.session.FLAM3H_SYS_UPDATE_MODE # type: ignore
            except:
                pass
            
            # Delete all data related to the Camera sensor viz
            flam3h_general_utils.util_clear_stashed_cam_data()
            
        else:
            
            if hou.session.FLAM3H_MARKED_FF_CHECK: # type: ignore
                from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
                
                if node == from_FLAM3H_NODE and node_instances:
                    hou.session.FLAM3H_MARKED_FF_CHECK = None # type: ignore
                    hou.session.FLAM3H_MARKED_FF_NODE = node_instances[0] # type: ignore
                    
                    _MSG = f"The FLAM3H node you just deleted had its FF marked for being copied. Please, mark a FF first to copy parameters from."
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                    flam3h_general_utils.flash_message(node, f"FF marked node: DELETED")








# FLAM3H GENERAL UTLIS start here
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

STATIC METHODS:

flash_message(node: hou.SopNode, msg: Union[str, None], timer=FLAM3H_FLASH_MESSAGE_TIMER, img=None) -> None:

clamp(x, val_max=255) -> float:

my_system() -> str:

set_status_msg(msg: str, type: str) -> None:

isLOCK(filepath: Union[str, bool], prx=FLAM3H_LIB_LOCK) -> bool:

util_open_file_explorer(filepath_name) -> None:

util_getSceneViewers() -> list:

util_clear_stashed_cam_data() -> None:

util_set_stashed_cam() -> None:

METHODS:

menus_refresh_enum_prefs(self) -> None:

get_bbox_node_path(self, node_name: str) -> Union[str, None]:

util_set_clipping_viewers(self) -> None:

util_set_front_viewer(self, update=True) -> None:

util_set_front_viewer_all(self) -> None:

util_viewport_bbox_frame(self) -> None:

flam3h_other_sensor_viz_off(self, node: hou.SopNode) -> None:

flam3h_outsensor_toggle(self, prm=OUT_RENDER_PROPERTIES_SENSOR) -> None:

flam3h_toggle(self, prm=SYS_TAG) -> None:

flam3h_toggle_off(self, prm: str) -> None:

flam3h_init_presets_IN_PRESETS(self, mode=1) -> None:

flam3h_init_presets_OUT_PRESETS(self) -> None:

flam3h_init_presets_CP_PALETTE_PRESETS(self, mode=1) -> None:

flam3h_display_help(self) -> None:

colorSchemeDark(self, update_others=True) -> None:

viewportParticleDisplay(self) -> None:

viewportParticleSize(self, reset_val=None) -> None:

reset_SYS(self, density: int, iter: int, mode: int) -> None:

reset_MB(self) -> None:

reset_PREFS(self, mode=0) -> None:
    """    
    
    def __init__(self, kwargs: dict) -> None:
        self._kwargs = kwargs
        self._node = kwargs['node']
        self._bbox_sensor_path = self.get_bbox_node_path(OUT_BBOX_NODE_NAME_SENSOR)
        self._bbox_reframe_path = self.get_bbox_node_path(OUT_BBOX_NODE_NAME_REFRAME)



    @staticmethod
    def flash_message(node: hou.SopNode, msg: Union[str, None], timer=FLAM3H_FLASH_MESSAGE_TIMER, img=None) -> None:
        if hou.isUIAvailable() and node.parm(PREFS_FLASH_MSG).eval():
            for ne in [p for p in hou.ui.paneTabs() if p.type() == hou.paneTabType.NetworkEditor]: # type: ignore
                ne.flashMessage(img, msg, timer)


    @staticmethod
    def houdini_version() -> int:
        return int(''.join(str(x) for x in hou.applicationVersion()[:1]))

    @staticmethod  
    def clamp(x, val_max=255) -> float:
        """clamp a value to be between Zero and 255.

        Args:
            x (_type_): the value to clamp.
            val_max (int/float): Default to: 255. Max value to clamp to.

        Returns:
            _type_: value clamped between Zero and 255.
        """        
        return max(0, min(x, val_max))


    @staticmethod
    def my_system() -> str:
        """Return the OS we are on.

        Returns:
            str: Possible outcomes are: WIN (windows)
                                        LNX (linux)
                                        MAC
                                        JAVA
                                        UNKNW
        """        
        mysys = platform_system()
        if mysys == 'Windows':
            return 'WIN'
        elif mysys == 'Linux':
            return 'LNX'
        elif mysys == 'Darwin':
            return 'MAC'
        elif mysys == 'Java':
            return 'JAVA'
        else:
            return 'UNKNW'


    @staticmethod
    def set_status_msg(msg: str, type: str) -> None:
        """Print a message to the Houdini's status bar if the UI is available.

        Args:
            msg (str): The message string to print
            type (str): The type of severity message to use, Possible choises are: MSG ( message ), IMP ( important message ), WARN ( warning ).
        """

        if hou.isUIAvailable():
            st = { 'MSG': hou.severityType.Message, 'IMP': hou.severityType.ImportantMessage, 'WARN': hou.severityType.Warning }  # type: ignore
            hou.ui.setStatusMessage(msg, st.get(type)) # type: ignore


    @staticmethod
    def isLOCK(filepath: Union[str, bool], prx=FLAM3H_LIB_LOCK) -> bool:
        """Check if the loaded lib file ( Palette or flame XML ) is locked .

        Args:
            filepath (Union[str, bool]): the full lib file path.
            prx (_type_, optional): The lock prefix in the file name. Defaults to gobal FLAM3H_LIB_LOCK.

        Returns:
            bool: True if locked. False if not.
        """        
        if filepath is not False:
            if os.path.split(str(filepath))[-1].startswith(prx):
                return True
            else:
                return False
        else:
            return False


    @staticmethod
    def util_open_file_explorer(filepath_name) -> None:
        """Open the file explorer to the currently loaded file location.

        Args:
            filepath_name (_type_): The currently loaded file name full path.
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
        """
        Returns:
            list: [return a list of open scene viewers]
        """    
        views = hou.ui.paneTabs() # type: ignore
        return [v for v in views if isinstance(v, hou.SceneViewer)]


    @staticmethod
    def util_clear_stashed_cam_data() -> None:
        try:
            del hou.session.FLAM3H_SENSOR_CAM_STASH # type: ignore
        except:
            pass
        try:
            del hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE # type: ignore
        except:
            pass


    @staticmethod
    def util_set_stashed_cam() -> None:
        desktop = hou.ui.curDesktop() # type: ignore
        viewport = desktop.paneTabOfType(hou.paneTabType.SceneViewer) # type: ignore
        
        if viewport.isCurrentTab():
            view = viewport.curViewport()
            
            try:
                _CAM_STASHED = hou.session.FLAM3H_SENSOR_CAM_STASH # type: ignore
            except:
                _CAM_STASHED = None
                
            if _CAM_STASHED is not None:
                
                if _CAM_STASHED.isPerspective():
                    view.changeType(hou.geometryViewportType.Perspective) # type: ignore
                    view.setDefaultCamera(_CAM_STASHED) # type: ignore
                    
                elif _CAM_STASHED.isOrthographic:
                    
                    try:
                        _CAM_STASHED_TYPE = hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE # type: ignore
                    except:
                        _CAM_STASHED_TYPE = None
                        
                    if _CAM_STASHED_TYPE is not None:
                        view.changeType(_CAM_STASHED_TYPE) # type: ignore
                        view_obj = view.defaultCamera()
                        view_obj.setOrthoWidth(_CAM_STASHED.orthoWidth())
                        view_obj.setTranslation(_CAM_STASHED.translation())





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
        """ 
        node = self.node
        
        # Clear menu caches
        flam3h_iterator_utils.destroy_data(node, 'cp_presets_menu')
        flam3h_iterator_utils.destroy_data(node, 'cp_presets_menu_off')
        flam3h_iterator_utils.destroy_data(node, 'in_presets_menu')
        flam3h_iterator_utils.destroy_data(node, 'in_presets_menu_off')
        flam3h_iterator_utils.destroy_data(node, 'out_presets_menu')
        
        # CP PRESETS menus
        prm_CP_PALETTE_PRESETS = node.parm(CP_PALETTE_PRESETS)
        prm_CP_PALETTE_PRESETS.set(prm_CP_PALETTE_PRESETS.eval())
        prm_CP_PALETTE_PRESETS_OFF = node.parm(CP_PALETTE_PRESETS_OFF)
        prm_CP_PALETTE_PRESETS_OFF.set(prm_CP_PALETTE_PRESETS_OFF.eval())
        prm_CP_SYS_PALETTE_PRESETS = node.parm(CP_SYS_PALETTE_PRESETS)
        prm_CP_SYS_PALETTE_PRESETS.set(prm_CP_SYS_PALETTE_PRESETS.eval())
        prm_CP_SYS_PALETTE_PRESETS_OFF = node.parm(CP_SYS_PALETTE_PRESETS_OFF)
        prm_CP_SYS_PALETTE_PRESETS_OFF.set(prm_CP_SYS_PALETTE_PRESETS_OFF.eval())
        
        # IN PRESETS menus
        prm_IN_PRESETS = node.parm(IN_PRESETS)
        prm_IN_PRESETS.set(prm_IN_PRESETS.eval())
        prm_IN_PRESETS_OFF = node.parm(IN_PRESETS_OFF)
        prm_IN_PRESETS_OFF.set(prm_IN_PRESETS_OFF.eval())
        prm_IN_SYS_PRESETS = node.parm(IN_SYS_PRESETS)
        prm_IN_SYS_PRESETS.set(prm_IN_SYS_PRESETS.eval())
        prm_IN_SYS_PRESETS_OFF = node.parm(IN_SYS_PRESETS_OFF)
        prm_IN_SYS_PRESETS_OFF.set(prm_IN_SYS_PRESETS_OFF.eval())
        
        # OUT PRESETS menus
        prm_OUT_PRESETS = node.parm(OUT_PRESETS)
        prm_OUT_PRESETS.set(prm_OUT_PRESETS.eval())
        prm_OUT_SYS_PRESETS = node.parm(OUT_SYS_PRESETS)
        prm_OUT_SYS_PRESETS.set(prm_OUT_SYS_PRESETS.eval())


    def get_bbox_node_path(self, node_name: str) -> Union[str, None]:
        """Find the full path of the bbox data null node
        inside the current FLAM3H node.
        
        The Null node name prefixex to search are stored inside the global variables:
        
        OUT_BBOX_NODE_NAME_SENSOR
        OUT_BBOX_NODE_NAME_REFRAME

        Returns:
            Union[str, None]: The full path string to the bbox null data node used by the Camera sensor mode or the Re-frame mode.
        """        
        matcher = nodesearch.Name(node_name, exact=True)
        # Using hou.pwd() instead of self.node make this work also on creation from my tests.
        search = matcher.nodes(hou.pwd(), recursive=True)
        if search:
            return search[0].path()
        else:
            _MSG = f"{str(self.node)} -> Camera sensor BBOX data node not found."
            self.set_status_msg(_MSG, 'WARN')
            return None



    def util_set_clipping_viewers(self) -> None:
        """Set current viewport camera clipping near/far planes
        """        
        for view in self.util_getSceneViewers():
            curView = view.curViewport()
            settings = curView.settings()
            settings.setHomeAutoAdjustsClip( hou.viewportHomeClipMode.Neither ) # type: ignore
            settings.setClipPlanes( [0.001, 1000] )
            settings.homeAutoAdjustClip()
            settings.clipPlanes()



    def util_set_front_viewer(self, update=True) -> None:
        """Set front view when entering the camera sensor mode.
        This include storing and restoring the current viewport prior to entering the camera sensor mode.
        
        This definition is multipurpose, it is run from multiple parameters:
        - When run from the SYS prm: _SYS_FRAME_VIEW_SENSOR_prm it will also print a flash message.
        - When run from the OUT Sensor prms, it will re frame the sensor based of if update sensor prm is ON or OFF.
        - When run while loading a hip file it will test the necessary condition to see if it can work ort not.
        
        Maybe it would be better to split all those purposes into their own definition for each...but good for now.

        Args:
            update (bool, optional): _description_. Defaults to True.
        """     
           
        if self.node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt():
            desktop = hou.ui.curDesktop() # type: ignore
            viewport = desktop.paneTabOfType(hou.paneTabType.SceneViewer) # type: ignore
            if viewport.isCurrentTab():
                
                _SYS_FRAME_VIEW_SENSOR_prm = False
                try:
                    if self.kwargs['parm'].name() == SYS_FRAME_VIEW_SENSOR:
                        _SYS_FRAME_VIEW_SENSOR_prm =True
                except:
                    pass
                
                view = viewport.curViewport()

                try:
                    _CAM_STASHED = hou.session.FLAM3H_SENSOR_CAM_STASH # type: ignore
                except:
                    _CAM_STASHED = None
                    
                if _CAM_STASHED is None:
                    cam = view.defaultCamera()
                    hou.session.FLAM3H_SENSOR_CAM_STASH = cam.stash() # type: ignore
                    hou.session.FLAM3H_SENSOR_CAM_STASH_TYPE = view.type() # type: ignore
                
                if view.type() != hou.geometryViewportType.Front: # type: ignore
                    view.changeType(hou.geometryViewportType.Front) # type: ignore
                    
                if update:
                    if self.bbox_sensor_path is not None:
                        node_bbox = hou.node(self.bbox_sensor_path)
                        if hou.hipFile.isLoadingHipFile(): # type: ignore
                            try:
                                # This fail on "isLoadingHipFile" under H19.x, H19.5.x and H20.0.506
                                # but work on H20.0.590 and up, hence the try/except block
                                view.frameBoundingBox(node_bbox.geometry().boundingBox())
                            except:
                                self.node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                        else:
                            view.frameBoundingBox(node_bbox.geometry().boundingBox())

                        if _SYS_FRAME_VIEW_SENSOR_prm:
                            self.flash_message(self.node, f"Camera sensor REFRAMED")

                else:
                    update_sensor = self.node.parm(OUT_UPDATE_SENSOR).evalAsInt()
                    if update_sensor or _SYS_FRAME_VIEW_SENSOR_prm:
                        if self.bbox_sensor_path is not None:
                            node_bbox = hou.node(self.bbox_sensor_path)
                            if hou.hipFile.isLoadingHipFile(): # type: ignore
                                try:
                                    # This fail on "isLoadingHipFile" under H19.x, H19.5.x and H20.0.506
                                    # but work on H20.0.590 and up, hence the try/except block
                                    view.frameBoundingBox(node_bbox.geometry().boundingBox())
                                except:
                                    self.node.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                            else:
                                view.frameBoundingBox(node_bbox.geometry().boundingBox())
                                
                                if _SYS_FRAME_VIEW_SENSOR_prm:
                                    self.flash_message(self.node, f"Camera sensor REFRAMED")



    # Wip and not currently used.
    def util_set_front_viewer_all(self) -> None:
        if self.node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt():
            self.util_set_clipping_viewers()
            for v in self.util_getSceneViewers():
                view = v.curViewport()
                if view.type() != hou.geometryViewportType.Front: # type: ignore
                    view.changeType(hou.geometryViewportType.Front) # type: ignore
                if self.bbox_sensor_path is not None:
                    node_bbox = hou.node(self.bbox_sensor_path)
                    view.frameBoundingBox(node_bbox.geometry().boundingBox())



    def util_viewport_bbox_frame(self) -> None:
        """Re-frame the current viewport based on camera sensor node's bounding box.
        """  
        if self.node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt() and not self.node.parm(OUT_UPDATE_SENSOR).evalAsInt():
            self.util_set_clipping_viewers()
            self.util_set_front_viewer()
        
        else:
            desktop = hou.ui.curDesktop() # type: ignore
            viewport = desktop.paneTabOfType(hou.paneTabType.SceneViewer) # type: ignore
            
            if viewport.isCurrentTab():
                
                view = viewport.curViewport()
                
                # if view.type() != hou.geometryViewportType.Front: # type: ignore
                #     view.changeType(hou.geometryViewportType.Front) # type: ignore
                
                if self.bbox_reframe_path is not None:
                    node_bbox = hou.node(self.bbox_reframe_path)
                    view.frameBoundingBox(node_bbox.geometry().boundingBox())
                    # Set clipping planes just in case
                    self.util_set_clipping_viewers()
                    self.flash_message(self.node, f"Viewport REFRAMED")



    def flam3h_other_sensor_viz_off(self, node: hou.SopNode) -> None:
        """When activating the Camera sensor viz, check if there is another FLAM3H in camera sensor mode
        and turn it Off if so. this way we guarantee there can be only one FLAM3H node in Camera sensor viz mode at any given time.

        Args:
            node (hou.SopNode): This FLAM3H node
            prm (_type_, optional): Defaults to OUT_RENDER_PROPERTIES_SENSOR.
        """
        all_f3h = node.type().instances()
        if len(all_f3h) > 1:
            for f3h in all_f3h:
                if f3h != node:
                    if f3h.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt():
                        f3h.setParms({OUT_RENDER_PROPERTIES_SENSOR: 0})
                        # If another FLAM3H node is in Camera Sensor mode, clear up its data.
                        self.util_clear_stashed_cam_data()
                        break



    def flam3h_outsensor_toggle(self, prm=OUT_RENDER_PROPERTIES_SENSOR) -> None:
        """If a toggle is OFF it will switch ON, and viceversa.

        Args:
            prm (_type_, optional): _description_. Defaults to SYS_TAG. Toggle parameter name to use.
        """        
        
        node = self.node
        toggle = node.parm(prm).evalAsInt()
        
        if toggle:
            node.setParms({prm: 0})
            # Restore the viewport prior to entering the Camera sensor mode
            self.util_set_stashed_cam()
            self.util_clear_stashed_cam_data()

            _MSG = f"Sensor viz -> OFF"
            self.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
            self.flash_message(node, _MSG)
            
        else:
            node.setParms({prm: 1})
            # If the current FLAM3H node is displayed ( its displayFlag is On )
            if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
                # Check if any other FLAM3H node is in Camera Sensor viz mode
                self.flam3h_other_sensor_viz_off(node)
                # Set this FLAM3H node to enter the camera sensor viz mode
                self.util_set_clipping_viewers()
                self.util_set_front_viewer()
                
                _MSG = f"Sensor viz -> ON"
                self.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                self.flash_message(node, _MSG)
            else:
                # IF displayFlag is OFF, turn the outsensor toggle OFF, too.
                node.setParms({prm: 0})
                _MSG = f"This node display flag is OFF. Please use a FLAM3H node that is currently displayed to enter the Camera sensor viz."
                self.set_status_msg(f"{node.name()}: {prm.upper()} -> {_MSG}", 'WARN')
                self.flash_message(node, f"{_MSG[:30]}")



    def flam3h_toggle(self, prm=SYS_TAG) -> None:
        """If a toggle is OFF it will switch ON, and viceversa.

        Args:
            prm (_type_, optional): _description_. Defaults to SYS_TAG. Toggle parameter name to use.
        """        
        node = self.node
        toggle = node.parm(prm).evalAsInt()
        
        if toggle:
            node.setParms({prm: 0})
            _MSG = f"{node.name()}: {prm.upper()} -> OFF"
            self.set_status_msg(_MSG, 'MSG')
            
        else:
            node.setParms({prm: 1})
            _MSG = f"{node.name()}: {prm.upper()} -> ON"
            self.set_status_msg(_MSG, 'MSG')



    def flam3h_toggle_off(self, prm: str) -> None:
        """If a toggle is ON it will switch it OFF.

        Args:
            prm (str): Toggle parameter name to use
        """        
        toggle = self.node.parm(prm).evalAsInt()
        
        if toggle:
            self.node.setParms({prm: 0})
            # If the passed toggle's name argument is the camera sensor: 'outsensor'
            # restore the viewport prior to entering the Camera sensor mode and clearup all related data
            if prm == OUT_RENDER_PROPERTIES_SENSOR:
                self.util_set_stashed_cam()
                self.util_clear_stashed_cam_data()



    def flam3h_init_presets_IN_PRESETS(self, mode=1) -> None:
        """Initialize parameter's menu presets for the IN tab.
        
        Args:
            mode (int): To be used to prevent to load a left over preset when loading back a hip file.
        """    
        node = self.node
        clipboard = node.parm(IN_CLIPBOARD_TOGGLE).evalAsInt()
        
        prm = node.parm(IN_PRESETS)
        prm_off = node.parm(IN_PRESETS_OFF)
        prm.set('-1')
        prm_off.set('-1')
        
        xml = node.parm(IN_PATH).evalAsString()
        if os.path.isfile(xml):
            # We are using the class: _xml_tree becasue we really need to carefully validate the loaded flame file.
            # This is important as all the toggles we are setting here will be used to speed up the population of the menu presets.
            # apo = _xml_tree(xml)
            if not _xml_tree(xml).isvalidtree:
                if clipboard:
                    node.setParms({IN_ISVALID_FILE: 0})
                else:
                    node.setParms({IN_ISVALID_FILE: 0})
                    node.setParms({IN_ISVALID_PRESET: 0})
                    node.setParms({IN_CLIPBOARD_TOGGLE: 0})
                    
                    node.setParms({MSG_FLAMESTATS: ""})
                    node.setParms({MSG_FLAMERENDER: ""})
                    node.setParms({MSG_FLAMESENSOR: ""})
                    node.setParms({MSG_DESCRIPTIVE_PRM: ""})
                        
                # If it is not a chaotica xml file do print out from here,
                # other wise we are printing out from:
                # class: _xml_tree(...) @staticmethod -> xmlfile_root_chk(...)
                if not in_flame_utils.in_to_flam3h_is_CHAOS(xml):
                    _MSG = "Flame IN -> Nothing to load"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    flam3h_general_utils.flash_message(node, _MSG)
            else:
                # Only set when NOT on an: onLoaded python script
                if mode:
                    prm.set('0')
                    prm_off.set('0')
                    node.setParms({IN_ISVALID_FILE: 1})
                    # the IN_ISVALID_PRESET is set inside the following: in_flame_utils(self.kwargs).in_to_flam3h()
                    in_flame_utils(self.kwargs).in_to_flam3h()
        else:
            # If there is not a flame preset loaded from the clipboard
            if not clipboard:
                node.setParms({IN_ISVALID_FILE: 0})
                node.setParms({IN_ISVALID_PRESET: 0})
                node.setParms({IN_CLIPBOARD_TOGGLE: 0})
                
                node.setParms({MSG_FLAMESTATS: ""})
                node.setParms({MSG_FLAMERENDER: ""})
                node.setParms({MSG_FLAMESENSOR: ""})
                node.setParms({MSG_DESCRIPTIVE_PRM: ""})
                # We do not want to print if the file path parameter is empty
                if xml:
                    print(f'{node.name()}.IN: please select a valid file location.')
            else:
                # Otherwise just mark the absence of a valid file and leave everything else untouched
                node.setParms({IN_ISVALID_FILE: 0})
                
        # Force preset menu to updated
        prm.eval()



    def flam3h_init_presets_OUT_PRESETS(self) -> None:
        """Initialize parameter's menu presets for the OUT tab.
        
        Args:
        """    
        node = self.node
        # Clear menu caches
        flam3h_iterator_utils.destroy_data(node, 'out_presets_menu')
        flam3h_iterator_utils.destroy_data(node, 'in_presets_menu')
        flam3h_iterator_utils.destroy_data(node, 'in_presets_menu_off')
        
        prm = node.parm(OUT_PRESETS)
        prm_sys = node.parm(OUT_SYS_PRESETS)
        prm.set('-1')
        prm_sys.set('-1')
        
        xml = node.parm(OUT_PATH).evalAsString()
        xml_checked = out_flame_utils.out_check_outpath(node, xml, OUT_FLAM3_FILE_EXT, 'Flame')
        if xml_checked is not False:
            node.setParms({OUT_PATH: xml_checked}) 
            apo = _xml_tree(xml_checked) #type: ignore
            if apo.isvalidtree:
                prm.set(f'{len(apo.name)-1}')
                prm_sys.set(f'{len(apo.name)-1}')
                # check if the selected Flame file is locked
                if self.isLOCK(xml_checked):
                    _MSG = f"Flame lib file: LOCKED"
                    node.setParms({MSG_OUT: _MSG})
                else:
                    node.setParms({MSG_OUT: ''})
                node.setParms({OUT_ISVALID_FILE: 1})
                
            else:
                prm.set('-1')
                prm_sys.set('-1')
                node.setParms({MSG_OUT: ''})
                node.setParms({OUT_ISVALID_FILE: 0})
                
        else:
            node.setParms({MSG_OUT: ''})
            node.setParms({OUT_ISVALID_FILE: 0})
            # We do not want to print if the file path parameter is empty
            if xml:
                print(f'{node.name()}.OUT: please select a valid file location.')
                
        # Force preset menu to updated
        prm.eval()



    def flam3h_init_presets_CP_PALETTE_PRESETS(self, mode=1) -> None:
        """Initialize parameter's menu presets for the CP tab.
        
        Args:
            mode (int): To be used to prevent to load a left over preset when loading back a hip file.
        """    
        node = self.node
        prm = node.parm(CP_PALETTE_PRESETS)
        prm_off = node.parm(CP_PALETTE_PRESETS_OFF)
        prm.set('-1')
        prm_off.set('-1')

        json_path = node.parm(CP_PALETTE_LIB_PATH).evalAsString()
        json_path_checked = out_flame_utils.out_check_outpath(node,  json_path, OUT_PALETTE_FILE_EXT, 'Palette')
        if json_path_checked is not False:
            node.setParms({CP_PALETTE_LIB_PATH: json_path_checked})
            
            json_file, f3h_json_file = flam3h_palette_utils.isJSON_F3H(node, json_path)
            if json_file and f3h_json_file:
                
                # Clear menu cache
                flam3h_iterator_utils.destroy_data(node, 'cp_presets_menu')
                flam3h_iterator_utils.destroy_data(node, 'cp_presets_menu_off')
                
                # CP is valid file
                node.setParms({CP_ISVALID_FILE: 1})
                # Only set when NOT on an: onLoaded python script
                if mode:
                    prm.set('0')
                    prm_off.set('0')
                    # Mark this as not a loaded preset
                    node.setParms({CP_ISVALID_PRESET: 0})
                    # check if the selected palette file is locked
                    if self.isLOCK(json_path_checked):
                        _MSG = f"Palette lib file: LOCKED"
                        flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, _MSG)
                    else:
                        flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, "")
                
            else:
                prm.set('-1')
                prm_off.set('-1')
                # CP not a valid file
                node.setParms({CP_ISVALID_FILE: 0})
                flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, "")
                # Mark this as not a loaded preset
                node.setParms({CP_ISVALID_PRESET: 0})

        else:
            # CP not a valid file
            node.setParms({CP_ISVALID_FILE: 0})
            flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, "")
            # Mark this as not a loaded preset
            node.setParms({CP_ISVALID_PRESET: 0})
            
            # We do not want to print if the file path parameter is empty
            if json_path:
                print(f'{node.name()}.PALETTE: please select a valid file location.')
            else:
                self.set_status_msg('', 'MSG')
        
        # Force preset menu to updated
        prm.eval()



    def flam3h_display_help(self) -> None:
        hou.ui.displayNodeHelp(self.node.type()) # type: ignore



    def colorSchemeDark(self, update_others=True) -> None:
        """Change viewport color scheme to dark
        and remember the current color scheme so to switch back to it when unchecked.
        If the viewport color scheme is already dark, checking this option will do nothing. 
        """
        node = self.node
        
        try:
            module_test = hou.session.flam3h_viewport_CS # type: ignore
        except:
            hou.session.flam3h_viewport_CS = [] # type: ignore

        count = 0
        viewers_col = []

        setprm = node.parm(PREFS_VIEWPORT_DARK).eval()
        
        Light = hou.viewportColorScheme.Light # type: ignore
        Grey  = hou.viewportColorScheme.Grey # type: ignore
        Dark  = hou.viewportColorScheme.Dark # type: ignore
        # The following is a lazy way to make this backward compatible with H19.x
        # as the DarkGrey color scheme has been introduced in H20.x first
        if flam3h_general_utils.houdini_version() < 20: DarkGrey = Grey
        else: DarkGrey = hou.viewportColorScheme.DarkGrey # type: ignore

        for view in self.util_getSceneViewers():

            settings = view.curViewport().settings()
            col = settings.colorScheme()
            viewers_col.append(col)
            try:
                idx_test = hou.session.flam3h_viewport_CS[count] # type: ignore
            except:
                if len(hou.session.flam3h_viewport_CS) > 0: # type: ignore
                    hou.session.flam3h_viewport_CS.append(viewers_col) # type: ignore
                else:
                    hou.session.flam3h_viewport_CS = [] # type: ignore
                    hou.session.flam3h_viewport_CS.append(viewers_col) # type: ignore

            if setprm:
                if len(hou.session.flam3h_viewport_CS) == 0: # type: ignore
                    if col == Light or col == Grey or col == DarkGrey:
                        settings.setColorScheme(Dark)
                else:
                    if col == Light or col == Grey or col == DarkGrey:
                        settings.setColorScheme(Dark)
                    elif col == Dark and hou.session.flam3h_viewport_CS[count] != Dark: # type: ignore
                        if hou.session.flam3h_viewport_CS[count] == Light: # type: ignore
                            settings.setColorScheme(Light)
                        elif hou.session.flam3h_viewport_CS[count] == Grey: # type: ignore
                            settings.setColorScheme(Grey)
                        elif hou.session.flam3h_viewport_CS[count] == DarkGrey: # type: ignore
                            settings.setColorScheme(DarkGrey)

            else:
                if col == Dark and hou.session.flam3h_viewport_CS[count] != Dark: # type: ignore
                    if hou.session.flam3h_viewport_CS[count] == Light: # type: ignore
                        settings.setColorScheme(Light)
                    elif hou.session.flam3h_viewport_CS[count] == Grey: # type: ignore
                        settings.setColorScheme(Grey)
                    elif hou.session.flam3h_viewport_CS[count] == DarkGrey: # type: ignore
                        settings.setColorScheme(DarkGrey)
                    
            count += 1
            
        if update_others:
            # Updated dark preference's option toggle on other FLAM3H nodes instances
            all_f3h = self.node.type().instances()
            if len(all_f3h) > 1:
                [f3h.setParms({PREFS_VIEWPORT_DARK: setprm}) for f3h in all_f3h if f3h != node if f3h.parm(PREFS_VIEWPORT_DARK).eval() != setprm]
        
        # Update history
        hou.session.flam3h_viewport_CS = [] # type: ignore
        hou.session.flam3h_viewport_CS = viewers_col # type: ignore
        
        
    def viewportParticleDisplay(self) -> None:
        """Switch viewport particle display mode
        between Pixel and Points.
        """        
        node = self.node
        pttype = node.parm(PREFS_VIEWPORT_PT_TYPE).evalAsInt()

        Points = hou.viewportParticleDisplay.Points # type: ignore
        Pixels = hou.viewportParticleDisplay.Pixels # type: ignore

        for view in self.util_getSceneViewers():
            settings = view.curViewport().settings()
            if pttype == 0:
                settings.particleDisplayType(Points)
                self.viewportParticleSize()
            elif pttype == 1:
                settings.particleDisplayType(Pixels)
                
        # Updated Point Display type preference's option toggle on other FLAM3H nodes instances
        all_f3h = self.node.type().instances()
        if len(all_f3h) > 1:
            [f3h.parm(PREFS_VIEWPORT_PT_TYPE).deleteAllKeyframes() for f3h in node.type().instances()]
            [f3h.setParms({PREFS_VIEWPORT_PT_TYPE: pttype}) for f3h in all_f3h if f3h != node if f3h.parm(PREFS_VIEWPORT_PT_TYPE).eval() != pttype]
                
                
    def viewportParticleSize(self, reset_val=None) -> None:
        """When the viewport particle display type is set to Point
        this will change their viewport size.
        
        reset_val -> can be either "None" or a float value.
                     If "None" it will use the current parameter value, otherwise it will use the one passed in this function.
        """        
        node = self.node
        Points = hou.viewportParticleDisplay.Points # type: ignore
        ptsize = node.parm(PREFS_VIEWPORT_PT_SIZE).evalAsFloat()

        for view in self.util_getSceneViewers():
            settings = view.curViewport().settings()
            settings.particleDisplayType(Points)
            if reset_val is None:
                settings.particlePointSize(ptsize)
            else:
                ptsize = float(reset_val)
                settings.particlePointSize(ptsize)
                prm = node.parm(self.kwargs['parmtuple'].name())
                prm.deleteAllKeyframes()
                prm.set(ptsize)
            
        # Updated Point Size preference's option toggle on other FLAM3H nodes instances
        if node.parm(PREFS_VIEWPORT_PT_TYPE).evalAsInt() == 0:
            [f3h.parm(PREFS_VIEWPORT_PT_SIZE).deleteAllKeyframes() for f3h in node.type().instances()]
            [f3h.setParms({PREFS_VIEWPORT_PT_SIZE: ptsize}) for f3h in node.type().instances() if f3h.parm(PREFS_VIEWPORT_PT_SIZE).eval() != ptsize]
            
            
            
    def reset_SYS(self, density: int, iter: int, mode: int) -> None:
        """Reset the FLAM3H SYS Tab parameters.
        
        Args:
            density (int): Numper of points to use
            iter (int): Number of iterations
            mode (int): 0: skip "doff" 1: reset "doff"
        """    
        node = self.node
        node.setParms({GLB_DENSITY: density})
        node.setParms({GLB_DENSITY_PRESETS: 0})
        node.setParms({GLB_ITERATIONS: iter})
        if mode:
            node.setParms({SYS_DO_FF: 0})
        node.setParms({SYS_TAG: 1})
        node.setParms({SYS_TAG_SIZE: 0})
        node.setParms({SYS_RIP: 0})
        

    def reset_MB(self) -> None:
        """Reset the FLAM3H MB Tab parameters.
        """        
        node = self.node
        node.setParms({MB_DO: 0})
        node.setParms({MB_FPS: 24})
        node.setParms({MB_SAMPLES: 16})
        node.setParms({MB_SHUTTER: 0.5})


    def reset_PREFS(self, mode=0) -> None:
        """Reset the FLAM3H PREFS Tab parameters.

        Args:
            mode (int, optional): _description_. Defaults to 0.
        """        
        node = self.node
        node.setParms({PREFS_TOGGLE: 1})
        node.setParms({PREFS_XAOS_MODE: 0})
        node.setParms({PREFS_CAMERA_HANDLE: 0})
        node.setParms({PREFS_CAMERA_CULL: 0})
        node.setParms({PREFS_CAMERA: ""})
        node.setParms({PREFS_CAMERA_CULL_AMOUNT: 0.99})
        if mode:
            node.setParms({PREFS_F3C: 1})





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
FLAM3H_ICON_COPY_PASTE = '![opdef:/alexnardini::Sop/FLAM3H?iconStarSwapRedCopyPasteSVG.svg]'
FLAM3H_ICON_COPY_PASTE_INFO = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]'
FLAM3H_ICON_COPY_PASTE_INFO_ORANGE = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarOrangeSVG.svg]'
FLAM3H_ICON_COPY_PASTE_ENTRIE = '![opdef:/alexnardini::Sop/FLAM3H?iconStarSwapRedCopyPasteEntrieSVG.svg]'
FLAM3H_ICON_COPY_PASTE_ENTRIE_ZERO = '![opdef:/alexnardini::Sop/FLAM3H?iconStarSwapRedCopyPasteZeroWSVG.svg]'
FLAM3H_ICON_COPY_PASTE_ENTRIE_FF = '![opdef:/alexnardini::Sop/FLAM3H?iconStarSwapRedCopyPasteEntrieFFSVG.svg]'

# ICONS menu vars and palette bookmarks
FLAM3H_ICON_STAR_EMPTY = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledSVG.svg]'
FLAM3H_ICON_STAR_EMPTY_OPACITY = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]'
FLAM3H_ICON_STAR_FLAME_LOAD = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionFlameINEntrieSVG.svg]'
FLAM3H_ICON_STAR_FLAME_LOAD_CB = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg]'
FLAM3H_ICON_STAR_FLAME_LOAD_EMPTY = '![opdef:/alexnardini::Sop/FLAM3H?iconWhiteSVG_disabled.svg]'
FLAM3H_ICON_STAR_FLAME_SAVE = '![opdef:/alexnardini::Sop/FLAM3H?iconWhiteStarSVG.svg]'
FLAM3H_ICON_STAR_FLAME_SAVE_ENTRIE = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionFlameOUTEntrieSVG.svg]'
FLAM3H_ICON_STAR_PALETTE_LOAD = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionCPSVG.svg]'
FLAM3H_ICON_STAR_PALETTE_LOAD_EMPTY = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionPRIDEDisabledSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_ACTV = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionEnabledSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_ACTV_OVER_ONE = '![opdef:/alexnardini::Sop/FLAM3H?iconStarSwapRedSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_ACTV_NEGATIVE = '![opdef:/alexnardini::Sop/FLAM3H?iconStarSwapCyanSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhitePBSVG.svg]'
FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV_OVER_ONE = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhitePBHSVG.svg]'
FLAM3H_ICON_STAR_FLAME_ITER_ACTV = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarYellowOrangeSVG.svg]'
# High tier menu entrie
FLAM3H_ICON_STAR_HIGH_TIER = '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]'

# The following are pre built to speed up the generations of the menus.
# MENU_VARS_ALL: list = [(0, 'Linear'), (39, 'Arch'), (94, 'Auger...'), (14, 'Bent'), (52, 'Bent2...'), (53, 'Bipolar...'), (43, 'Blade'), (30, 'Blob...'), (26, 'Blur'), (54, 'Boarders'), (23, 'Bubble'), (55, 'Butterfly'), (99, 'Bwraps...'), (56, 'Cell...'), (50, 'Conic...'), (83, 'Cos'), (89, 'Cosh'), (20, 'Cosine'), (87, 'Cot'), (93, 'Coth'), (57, 'Cpow...'), (102, 'Crop...'), (46, 'Cross'), (86, 'Csc'), (92, 'Csch'), (27, 'Curl...'), (97, 'Curve...'), (24, 'Cylinder'), (11, 'Diamond'), (8, 'Disc'), (47, 'Disc2...'), (58, 'Edisc'), (59, 'Elliptic'), (61, 'Escher...'), (12, 'Ex'), (80, 'Exp'), (18, 'Exponential'), (25, 'Eyefish'), (22, 'Fan*'), (34, 'Fan2...'), (16, 'Fisheye'), (49, 'Flower...'), (95, 'Flux...'), (62, 'Foci'), (33, 'Gaussian_blur'), (104, 'Glynnia'), (6, 'Handkerchief'), (7, 'Heart'), (100, 'Hemisphere'), (4, 'Horseshoe'), (10, 'Hyperbolic'), (13, 'Julia'), (31, 'JuliaN...'), (32, 'Juliascope...'), (63, 'Lazysusan...'), (81, 'Log'), (64, 'Loonie'), (96, 'Mobius...'), (66, 'Modulus...'), (28, 'Ngon...'), (60, 'Noise'), (67, 'Oscope...'), (51, 'Parabola...'), (29, 'Pdj...'), (98, 'Perspective...'), (38, 'Pie...'), (5, 'Polar'), (68, 'Polar2'), (101, 'Polynomial...'), (17, 'Popcorn*'), (69, 'Popcorn2...'), (19, 'Power'), (105, 'Pt_symmetry...'), (37, 'Radialblur...'), (42, 'Rays'), (36, 'Rectangles...'), (21, 'Rings*'), (35, 'Rings2...'), (70, 'Scry'), (85, 'Sec'), (44, 'Secant2'), (91, 'Sech'), (71, 'Separation...'), (82, 'Sin'), (88, 'Sinh'), (1, 'Sinusoidal'), (2, 'Spherical'), (9, 'Spiral'), (72, 'Split...'), (73, 'Splits...'), (41, 'Square'), (74, 'Stripes...'), (48, 'Supershape...'), (3, 'Swirl'), (84, 'Tan'), (40, 'Tangent'), (90, 'Tanh'), (45, 'Twintrian'), (103, 'Unpolar'), (15, 'Waves*'), (79, 'Waves2...'), (75, 'Wedge...'), (76, 'Wedgejulia...'), (77, 'Wedgesph...'), (78, 'Whorl...')]
MENU_VARS_ALL_SIMPLE: list = [0, 'Linear     ', 39, 'Arch          ', 94, 'Auger...          ', 14, 'Bent          ', 52, 'Bent2...          ', 53, 'Bipolar...          ', 43, 'Blade          ', 30, 'Blob...          ', 26, 'Blur          ', 54, 'Boarders          ', 23, 'Bubble          ', 55, 'Butterfly          ', 99, 'Bwraps...          ', 56, 'Cell...          ', 50, 'Conic...          ', 83, 'Cos          ', 89, 'Cosh          ', 20, 'Cosine          ', 87, 'Cot          ', 93, 'Coth          ', 57, 'Cpow...          ', 102, 'Crop...          ', 46, 'Cross          ', 86, 'Csc          ', 92, 'Csch          ', 27, 'Curl...          ', 97, 'Curve...          ', 24, 'Cylinder          ', 11, 'Diamond          ', 8, 'Disc          ', 47, 'Disc2...          ', 58, 'Edisc          ', 59, 'Elliptic          ', 61, 'Escher...          ', 12, 'Ex          ', 80, 'Exp          ', 18, 'Exponential          ', 25, 'Eyefish          ', 22, 'Fan*          ', 34, 'Fan2...          ', 16, 'Fisheye          ', 49, 'Flower...          ', 95, 'Flux...          ', 62, 'Foci          ', 33, 'Gaussian_blur          ', 104, 'Glynnia          ', 6, 'Handkerchief          ', 7, 'Heart          ', 100, 'Hemisphere          ', 4, 'Horseshoe          ', 10, 'Hyperbolic          ', 13, 'Julia          ', 31, 'JuliaN...          ', 32, 'Juliascope...          ', 63, 'Lazysusan...          ', 81, 'Log          ', 64, 'Loonie          ', 96, 'Mobius...          ', 66, 'Modulus...          ', 28, 'Ngon...          ', 60, 'Noise          ', 67, 'Oscope...          ', 51, 'Parabola...          ', 29, 'Pdj...          ', 98, 'Perspective...          ', 38, 'Pie...          ', 5, 'Polar          ', 68, 'Polar2          ', 101, 'Polynomial...          ', 17, 'Popcorn*          ', 69, 'Popcorn2...          ', 19, 'Power          ', 105, 'Pt_symmetry...          ', 37, 'Radialblur...          ', 42, 'Rays          ', 36, 'Rectangles...          ', 21, 'Rings*          ', 35, 'Rings2...          ', 70, 'Scry          ', 85, 'Sec          ', 44, 'Secant2          ', 91, 'Sech          ', 71, 'Separation...          ', 82, 'Sin          ', 88, 'Sinh          ', 1, 'Sinusoidal          ', 2, 'Spherical          ', 9, 'Spiral          ', 72, 'Split...          ', 73, 'Splits...          ', 41, 'Square          ', 74, 'Stripes...          ', 48, 'Supershape...          ', 3, 'Swirl          ', 84, 'Tan          ', 40, 'Tangent          ', 90, 'Tanh          ', 45, 'Twintrian          ', 103, 'Unpolar          ', 15, 'Waves*          ', 79, 'Waves2...          ', 75, 'Wedge...          ', 76, 'Wedgejulia...          ', 77, 'Wedgesph...          ', 78, 'Whorl...          ']
MENU_DENSITY: list = [0, '', 1, '1M', 2, '2M', 3, '5M', 4, '15M', 5, '25M', 6, '50M', 7, '100M', 8, '150M', 9, '250M', 10, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]500M', 11, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]750M', 12, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarRedHighSVG.svg]1 Billion', 13, '']
MENU_PRESETS_EMPTY: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionDisabledZeroIterSVG.svg]  Empty     ']
MENU_IN_PRESETS_EMPTY_CB: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarWhiteSVG.svg]  Clipboard     ']
MENU_FF_COPY_PASTE_EMPTY: list = [-1, '![opdef:/alexnardini::Sop/FLAM3H?iconStarSwapRedCopyPasteSVG.svg]  Please, mark the FF first.', 0, '']
MENU_FF_COPY_PASTE_SELECT: list = [0, '![opdef:/alexnardini::Sop/FLAM3H?icon_optionStarBlueSVG.svg]  FF: MARKED.\n-> Select a different FLAM3H node to paste those FF values.', 1, '']

MENU_VARS_INDEXES: dict = { 0: 1, 
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
                            78: 209 }

class flam3h_iterator_utils:
    """
class flam3h_iterator_utils

STATIC METHODS:

sierpinski_settings(node: hou.SopNode) -> None:

get_user_data(node: hou.SopNode, data=FLAM3H_USER_DATA_ITER) -> Union[int, bool]:

exist_user_data(node: hou.SopNode, data=FLAM3H_USER_DATA_ITER) -> bool:

set_comment_and_user_data_iterator(node: hou.SopNode, value: str, data=FLAM3H_USER_DATA_ITER) -> None:

del_comment_and_user_data_iterator(node: hou.SopNode, data=FLAM3H_USER_DATA_ITER) -> None:

flam3h_init_hou_session_iterator_data(node: hou.SopNode) -> None:

flam3h_init_hou_session_ff_data(node: hou.SopNode) -> None:

iterator_mpidx_mem_set(node, data: int) -> None:

paste_from_list(node: hou.SopNode, flam3node: Union[hou.SopNode, None], prm_list: tuple, id: str, id_from: str) -> None:

paste_from_list_affine(node: hou.SopNode, prm_list_affine_to: tuple, prm_list_affine_from: tuple, id: str) -> None:

pastePRM_T_from_list(node: hou.SopNode, flam3node: Union[hou.SopNode, None], prmT_list: tuple, varsPRM: tuple, id: str, id_from: str) -> None:

paste_save_note(_note: str) -> str:

paste_set_note(node: hou.SopNode, flam3node: Union[hou.SopNode, None], int_mode: int, str_section: str, id: str, id_from: str) -> None:

auto_set_xaos_data_get_MP_MEM(node: hou.SopNode) -> Union[list, None]:

auto_set_xaos_data_get_XAOS_PREV(node: hou.SopNode) -> Union[list, None]:

auto_set_xaos_data_set_MP_MEM(node: hou.SopNode, data: Union[list, tuple]) -> None:

auto_set_xaos_data_set_XAOS_PREV(node: hou.SopNode, data: Union[list, tuple]) -> None:

destroy_data(node, data: str, must_exist: bool = False) -> None:

menu_T_get_type_icon(w: float) -> str:

menu_T_PP_get_type_icon(w: float) -> str:

menu_T_FF_get_var_data(self) -> tuple[int, float]:

METHODS:

menu_T_get_var_data(self) -> tuple[int, float]:

refresh_iterator_vars_menu(self) -> None:

menu_T_data(self) -> tuple[int, str]:

menu_T_PP_data(self) -> tuple[int, str]:

menu_T_FF_data(self) -> tuple[int, str]:

menu_T_PP_FF_data(self) -> tuple[int, str]:

menu_T_pb_data(self) -> str:

menu_T_ICON(self, FF=False) -> list:

menu_T_PP_ICON(self, FF=False) -> list:

menu_T_simple(self, FF=False) -> list:

menu_T(self, FF=False) -> list:

menu_T_pb(self) -> list:

menu_select_iterator_data(self) -> list:

menu_select_iterator(self) -> list:

prm_select_iterator(self) -> None:

flam3h_paste_reset_hou_session_data(self) -> None:

menu_global_density(self) -> list:

menu_global_density_set(self) -> None:

menu_global_density_set_default(self) -> None:

menu_copypaste(self) -> list:

menu_copypaste_FF(self) -> list:

prm_paste_update_for_undo(self, node: hou.SopNode) -> tuple[Union[hou.SopNode, None], Union[int, None], bool]:

prm_paste_update_for_undo_ff(self, node: hou.SopNode) -> tuple[Union[hou.SopNode, None], Union[int, None], bool]:

prm_paste_CTRL(self, id: int) -> None:

prm_paste_SHIFT(self, id: int) -> None:

prm_paste_CLICK(self, id: int) -> None:

prm_paste(self) -> None:

prm_paste_FF_CTRL(self) -> None:

prm_paste_FF_SHIFT(self) -> None:

prm_paste_FF_CLICK(self) -> None:

prm_paste_FF(self) -> None:

prm_paste_sel(self) -> None:

prm_paste_sel_pre_affine(self) -> None:

prm_paste_sel_post_affine(self) -> None:

prm_paste_sel_pre_affine_FF(self) -> None:

prm_paste_sel_post_affine_FF(self) -> None:

prm_paste_sel_FF(self) -> None:

flam3h_xaos_convert(self) -> None:

reset_preaffine(self) -> None:

reset_postaffine(self) -> None:

reset_preaffine_FF(self) -> None:

reset_postaffine_FF(self) -> None:

swap_iter_pre_vars(self) -> None:

swap_FF_post_vars(self) -> None:

reset_FF(self) -> None:

flam3h_default(self) -> None:

flam3h_reset_iterator(self) -> None:

auto_set_xaos(self) -> None:

iterators_count(self) -> None:

iterator_keep_last_vactive(self) -> None:

iterator_keep_last_vactive_STAR(self) -> None:

iterator_keep_last_weight(self) -> None:
    """    
    
    def __init__(self, kwargs: dict) -> None:
        self._kwargs = kwargs
        self._node = kwargs['node']


    @staticmethod
    def sierpinski_settings(node: hou.SopNode) -> None:
        # iterator prm names
        n = flam3h_iterator_prm_names

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
    def get_user_data(node: hou.SopNode, data=FLAM3H_USER_DATA_ITER) -> Union[int, bool]:
        """Get the node user data associated to the copy/paste data.
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
            data (str): Default to: " FLAM3H_USER_DATA_ITER ". The name of the data we want to get. 
        """   
        
        data_name = f"{FLAM3H_USER_DATA_PRX}{data}"
        data = node.userData(f"{data_name}")
        if data is not None:
            return data
        else:
            return False


    @staticmethod
    def exist_user_data(node: hou.SopNode, data=FLAM3H_USER_DATA_ITER) -> bool:
        """Confirm the node user data associated to the copy/paste data Exist.
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
            data (str): Default to: " FLAM3H_USER_DATA_ITER ". The name of the data we want to get. For FF it wil be: " FLAM3H_USER_DATA_FF "
        """   
        data_name = f"{FLAM3H_USER_DATA_PRX}{data}"
        if node.userData(f"{data_name}") is None:
            return False
        else:
            return True


    @staticmethod
    def set_comment_and_user_data_iterator(node: hou.SopNode, value: str, data=FLAM3H_USER_DATA_ITER) -> None:
        """Set the node comment associated to the copy/paste data. It can be for an iterator number or for the FF.
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
            data (str): Default to: " FLAM3H_USER_DATA_ITER ". The name of the data we want to set the comment for. 
        """   
        
        data_name = f"{FLAM3H_USER_DATA_PRX}{data}"
        data_iter_name = f"{FLAM3H_USER_DATA_PRX}{FLAM3H_USER_DATA_ITER}"
        data_FF_name = f"{FLAM3H_USER_DATA_PRX}{FLAM3H_USER_DATA_FF}"
        
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
    def del_comment_and_user_data_iterator(node: hou.SopNode, data=FLAM3H_USER_DATA_ITER) -> None:
        """Delete the node comment associated to the copy/paste data. It can be for an iterator number or for the FF.
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
            data (str): Default to: " FLAM3H_USER_DATA_ITER ". The name of the data we want to delete the comment for. 
        """   
        
        data_name = f"{FLAM3H_USER_DATA_PRX}{data}"
        data_iter_name = f"{FLAM3H_USER_DATA_PRX}{FLAM3H_USER_DATA_ITER}"
        data_FF_name = f"{FLAM3H_USER_DATA_PRX}{FLAM3H_USER_DATA_FF}"
        
        if data_name == data_iter_name:
            if node.userData(f"{data_FF_name}") is None:
                if node.userData(f"{data_name}") is not None:
                    with hou.undos.group(f"FLAM3H DEL user data iter None"): # type: ignore
                        node.destroyUserData(f"{data_name}")
                        node.setComment("")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, False) # type: ignore
                    
            else:
                if node.userData(f"{data_name}") is not None:
                    with hou.undos.group(f"FLAM3H DEL user data iter"): # type: ignore
                        node.destroyUserData(f"{data_name}")
                        # node.setComment("")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, False) # type: ignore
                        node.setComment("FF")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore
                    
        elif data_name == data_FF_name:
            
            if node.userData(f"{data_iter_name}") is None:
                if node.userData(f"{data_name}") is not None:
                    with hou.undos.group(f"FLAM3H DEL FF user data None"): # type: ignore
                        node.destroyUserData(f"{data_name}")
                        node.setComment("")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, False) # type: ignore
                    
            else:
                if node.userData(f"{data_name}") is not None:
                    with hou.undos.group(f"FLAM3H DEL FF user data"): # type: ignore
                        data_iter = node.userData(f"{data_iter_name}")
                        node.destroyUserData(f"{data_name}")
                        # node.setComment("")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, False) # type: ignore
                        node.setComment(f"{str(data_iter)}")
                        node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore


    @staticmethod            
    def flam3h_init_hou_session_iterator_data(node: hou.SopNode) -> None:
        """Initialize the copy/paste data need by FLAM3H iterators and stored into the current hou.session.
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
        """   
        
        # The following try/except blocks are not really needed
        # becasue FLAM3H node will create and initialize those on creation
        # but just in case this data is deleted somehow.
        try:
            hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
        except:
            hou.session.FLAM3H_MARKED_ITERATOR_NODE = node # type: ignore
        try:
            hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
        except:
            hou.session.FLAM3H_MARKED_ITERATOR_NODE = None # type: ignore
        try:
            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
        except:
            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = None # type: ignore


    @staticmethod
    def flam3h_init_hou_session_ff_data(node: hou.SopNode) -> None:
        """Initialize the copy/paste data need by FLAM3H FF and stored into the current hou.session.
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
        """   
        
        # The following try/except blocks are not really needed
        # becasue FLAM3H node will create and initialize those on creation
        # but just in case this data is deleted somehow.
        try:
            hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
        except:
            hou.session.FLAM3H_MARKED_FF_NODE = node # type: ignore
        try:
            hou.session.FLAM3H_MARKED_FF_NODE.type() # type: ignore
        except:
            hou.session.FLAM3H_MARKED_FF_NODE = None # type: ignore
        try:
            hou.session.FLAM3H_MARKED_FF_CHECK # type: ignore
        except:
            hou.session.FLAM3H_MARKED_FF_CHECK = None # type: ignore


    @staticmethod
    def iterator_mpidx_mem_set(node, data: int) -> None:
        """Work as an history space to store the marked iterator info in it.
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
            data (int): Marked iterator number and info. The possible option are from 1 to n for the number of the marked iterator. 0 to signal no iterator has been marked. -1 if a marked iterator has been deleted.
        """   
        # unlock
        node.parm(FLAM3H_DATA_PRM_MPIDX).lock(False)
        # set
        node.setParms({FLAM3H_DATA_PRM_MPIDX: data})
        # lock
        node.parm(FLAM3H_DATA_PRM_MPIDX).lock(True)


        
    @staticmethod
    def paste_from_list(node: hou.SopNode, flam3node: Union[hou.SopNode, None], prm_list: tuple, id: str, id_from: str) -> None:
        """Paste value for a parameter, including keyframes and expressions if any,
        between different multiparameter indexes.
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
            flam3node (hou.SopNode): [hou.SopNode to copy values from]
            prm_list (tuple): [parameters list to query and set]
            id (str): [current multiparamter index]
            id_from (str): [multiparameter index to copy from]
        """    
        
        if flam3node is not None:
            
            for prm in prm_list:
                # if a tuple
                if prm[1]:
                    prm_from = flam3node.parmTuple(f"{prm[0]}{id_from}")
                    prm_to = node.parmTuple(f"{prm[0]}{id}")
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
                    if len(prm_from.keyframes()):
                        [prm_to.setKeyframe(k) for k in prm_from.keyframes()]
                    else:
                        prm_to.set(prm_from.eval())
        else:
            _MSG = f"{node.name()} -> The FLAM3H node you are trying to copy data from do not exist"
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            
            
    @staticmethod
    def paste_from_list_affine(node: hou.SopNode, prm_list_affine_to: tuple, prm_list_affine_from: tuple, id: str) -> None:
        """Paste value from the post affine into the pre affine and viceversa ( just swap  )
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
            prm_list_affine_to (tuple): [parameters list to query and set for the either the PRE or POST affine]
            prm_list_affine_from (tuple): [parameters list to query and set for the either the PRE or POST affine]
            id (str): [current multiparamter index]
        """    
        
        for idx, prm in enumerate(prm_list_affine_to):
            # if a tuple
            if prm[1]:
                prm_from = node.parmTuple(f"{prm[0]}{id}")
                prm_to = node.parmTuple(f"{prm_list_affine_from[idx][0]}{id}")
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
                if len(prm_from.keyframes()):
                    [prm_to.setKeyframe(k) for k in prm_from.keyframes()]
                else:
                    prm_to.set(prm_from.eval())
            
                
    
    @staticmethod
    def pastePRM_T_from_list(node: hou.SopNode, flam3node: Union[hou.SopNode, None], prmT_list: tuple, varsPRM: tuple, id: str, id_from: str) -> None:
        """Paste variation parameter values
        between different multiparameter indexes.
        In case of a parametric variation, it will paste its parameters using:
        flam3h_iterator_utils.paste_from_list() definition.
         
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
            flam3node (hou.SopNode): [hou.SopNode to copy values from]
            prmT_list (tuple): [variations list - types]
            varsPRM (tuple): [variation's parmaters list]
            id (str): [current multiparamter index]
            id_from (str): [multiparameter index to copy from]
        """    
        for prm in prmT_list:
            if flam3node is not None:
                prm_from = flam3node.parm(f"{prm}{id_from}").eval()
                node.setParms({f"{prm}{id}": prm_from}) # type: ignore
                # Check if this var is a parametric or not
                v_type = int(prm_from)
                if(varsPRM[v_type][-1]):  
                    flam3h_iterator_utils.paste_from_list(node, flam3node, varsPRM[v_type][1:-1], id, id_from)


    @staticmethod
    def paste_save_note(_note: str) -> str:
        """When copy/paste parameter values between different multiparameter indexes,
        this will save the current note and place it into parenthesis as a form of backup.
        
        Args:
            _note (str): [current note in the parameter]

        Returns:
            str: [simple new note append]
        """

        search_iter = "iter."
        search_FF = ".FF"

        if _note.find("(") or _note.find(")") == -1:
            _note_split = _note.split(" ")
            if len(_note_split) > 1 and (search_iter in _note_split[-1].rpartition(search_iter) or search_FF in _note_split[-1].rpartition(search_FF)):
                note = "(" + " ".join(_note_split[0:-1]) + ")" + " "
            elif len(_note.split(".")) > 1 and ("iter" in _note.split(".") or "FF" in _note.split(".")):
                note = ""
            else:
                note = "(" + _note + ")" + " "
        else:
            note = "(" + _note[_note.find("(")+1:_note.find(")")] + ")" + " "
        return note


    @staticmethod
    def paste_set_note(node: hou.SopNode, flam3node: Union[hou.SopNode, None], int_mode: int, str_section: str, id: str, id_from: str) -> None:
        """After a copy/paste, it will set the note parameter with a string indicating what has been pasted ( when copy/paste iterator's sections )
        
        Args:
            node (hou.SopNode): [current hou.SopNode to set]
            flam3node (hou.SopNode): [[hou.SopNode to copy values from]
            int_mode (int): [int(0) copy/paste iterator into the same node. int(1) copy/paste FF between different nodes. int(2) copy/paste FF sections between different nodes]
            str_section (str): [section name string to be copied, this is only for msg print info]
            id (str): [current multiparamter index]
            id_from (str): [multiparameter index to copy from]
        """ 
        
        n = flam3h_iterator_prm_names
        node_name = str(flam3node)
        _current_note_FF = node.parm("ffnote").evalAsString()

        if int_mode == 0:
            _current_note = node.parm(f"note_{id}").evalAsString()
            # If on the same FLAM3H node
            if node == flam3node:
                if len(_current_note) == 0:
                    node.setParms({f"{n.main_note}_{id}": f"iter.{id_from}{str_section}"}) # type: ignore
                else:
                    node.setParms({f"{n.main_note}_{id}": f"{flam3h_iterator_utils.paste_save_note(_current_note)}iter.{id_from}{str_section}"}) # type: ignore
                _MSG = f"{node.name()}.iter.{id}{str_section} -> Copied values from: iter.{id_from}{str_section}"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            else:
                if len(_current_note) == 0:
                    node.setParms({f"{n.main_note}_{id}": f"{node_name}.iter.{id_from}{str_section}"}) # type: ignore
                else:
                    node.setParms({f"{n.main_note}_{id}": f"{flam3h_iterator_utils.paste_save_note(_current_note)}{node_name}.iter.{id_from}{str_section}"}) # type: ignore
                _MSG = f"{node.name()}.iter.{id}{str_section} -> Copied values from: {node_name}.iter.{id_from}{str_section}"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
        elif int_mode == 1:
            if node != flam3node:
                if len(_current_note_FF) == 0:
                    node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{node_name}.FF"}) # type: ignore
                else:
                    node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{flam3h_iterator_utils.paste_save_note(_current_note_FF)}{node_name}.FF"}) # type: ignore
                _MSG = f"{node.name()} -> Copied FF from: {node_name}.FF"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
        elif int_mode == 2:
            if node != flam3node:
                if len(_current_note_FF) == 0:
                    node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{node_name}.FF{str_section}"}) # type: ignore
                else:
                    node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{flam3h_iterator_utils.paste_save_note(_current_note_FF)}{node_name}.FF{str_section}"}) # type: ignore
                _MSG = f"{node.name()}.FF{str_section} -> Copied from: {node_name}.FF{str_section}"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')


    @staticmethod
    def auto_set_xaos_data_get_MP_MEM(node: hou.SopNode) -> Union[list, None]:
        """Retrieve the desire data from FLAM3H data srting parameters
    and reconvert it back to usable types.

        Args:
            self (hou.SopNode): FLAM3H node

        Returns:
            Union[list, None]: A valid data type of the same data retrieved to be used inside: auto_set_xaos()
        """
        get_prm = node.parm(FLAM3H_DATA_PRM_XAOS_MP_MEM).eval()
        if get_prm:
            return [int(x) for x in get_prm.split(' ')]
        else:
            return None
        
        
    @staticmethod
    def auto_set_xaos_data_get_XAOS_PREV(node: hou.SopNode) -> Union[list, None]:
        """Retrieve the desire data from FLAM3H data srting parameters
    and reconvert it back to usable types.

        Args:
            self (hou.SopNode): FLAM3H node

        Returns:
            Union[list, None]: A valid data type of the same data retrieved to be used inside: auto_set_xaos()
        """
        get_prm = node.parm(FLAM3H_DATA_PRM_XAOS_PREV).eval()
        if get_prm:
            return [x.split(' ') for x in get_prm.split(':')]
        else:
            return None
        


    @staticmethod
    def auto_set_xaos_data_set_MP_MEM(node: hou.SopNode, data: Union[list, tuple]) -> None:
        """Set the data_name data into FLAM3H data parameters.
    Note that all the data will be of type: string.

        Args:
            self (hou.SopNode): FLAM3H node
            data (list): The actual data to set.
        """
        data_to_prm = ' '.join([str(x) for x in data])
        # unlock
        node.parm(FLAM3H_DATA_PRM_XAOS_MP_MEM).lock(False)
        # set
        node.setParms({FLAM3H_DATA_PRM_XAOS_MP_MEM: data_to_prm}) # type: ignore
        # lock
        node.parm(FLAM3H_DATA_PRM_XAOS_MP_MEM).lock(True)
                
                
                
    @staticmethod
    def auto_set_xaos_data_set_XAOS_PREV(node: hou.SopNode, data: Union[list, tuple]) -> None:
        """Set the data_name data into FLAM3H data parameters.
    Note that all the data will be of type: string.

        Args:
            self (hou.SopNode): FLAM3H node
            data (list): The actual data to set. A tuple can only come from: out_flame_utils.out_xf_xaos_from(self, mode=0) -> tuple:
        """
        # unlock
        node.parm(FLAM3H_DATA_PRM_XAOS_PREV).lock(False)
        # to prm from: flam3_xaos_convert()
        if isinstance(data, tuple):
            data_to_prm = ':'.join(data)
            # set
            node.setParms({FLAM3H_DATA_PRM_XAOS_PREV: data_to_prm}) # type: ignore
            # lock
            node.parm(FLAM3H_DATA_PRM_XAOS_PREV).lock(True)
        else:
            collect = []
            for xaos in data:
                collect.append(' '.join(xaos))
            data_to_prm = ':'.join(collect)
            # set
            node.setParms({FLAM3H_DATA_PRM_XAOS_PREV: data_to_prm}) # type: ignore
            # lock
            node.parm(FLAM3H_DATA_PRM_XAOS_PREV).lock(True)


    @staticmethod
    def destroy_data(node, data: str, must_exist: bool = False) -> None:
        """This is to be run as a callback script inside parms that are responsible to update the menu.
        For now: Iterator shader's opacity  

        Returns:
        """
        if not must_exist:
            try: node.destroyCachedUserData(data)
            except: pass
        else: node.destroyCachedUserData(data)
            

    @staticmethod
    def menu_T_get_type_icon(w: float) -> str:
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
    
    
    
    def menu_T_get_var_data(self) -> tuple[int, float]:
        """Get this menu variation type idx and its weight value.

        Returns:
            tuple[int, float]: int: variation idx.    float: weight value
        """  
        _TYPE = self.kwargs['parm'].eval()
        idx = self.kwargs['script_multiparm_index']
        prm_weight_name = f"{str(self.kwargs['parm'].name()).split('type')[0]}weight_{str(idx)}"
        return _TYPE, self.node.parm(prm_weight_name).eval()
    
    
    
    def menu_T_FF_get_var_data(self) -> tuple[int, float]:
        """Get this FF menu variation type idx and its weight value.

        Returns:
            tuple[int, float]: int: variation idx.    float: weight value
        """  
        _TYPE = self.kwargs['parm'].eval()
        prm_weight_name = f"{ str(self.kwargs['parm'].name()).split('type')[0]}weight"
        return _TYPE, self.node.parm(prm_weight_name).eval()
        

    
    def refresh_iterator_vars_menu(self) -> None:
        """Refresh the iterator (FLAME and FF tabs) menus
        to update to the new menu style mode.

        Returns:
            None: int:
        """  
        node = self.node
        if not self.node.parm(PREFS_ITERATOR_BOOKMARK_ICONS).eval():
            node.setParms({GLB_DENSITY: FLAM3H_DEFAULT_GLB_DENSITY}) # type: ignore
            
            # Reset memory mpidx prm data
            flam3h_iterator_utils.iterator_mpidx_mem_set(node, 0)
            
            # Remove any comment and user data from the node
            if self.exist_user_data(node):
                self.destroy_data(node, 'iter_sel')
                self.del_comment_and_user_data_iterator(node)
            if self.exist_user_data(node, FLAM3H_USER_DATA_FF):
                self.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)
            
            # This is the only way I found to update the FLAME tab multiparameter's menus, for now...
            node.type().definition().updateFromNode(node)
            node.matchCurrentDefinition()
            
            _MSG = "Iterator var menus: SIMPLE"
            flam3h_general_utils.flash_message(node, f"{_MSG}")
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
            
        else:
            self.destroy_data(node, 'vars_menu_all_simple')
            
            # For some reasons the FF menus do not update so we force them to
            node.parm(f"{PRX_FF_PRM}{flam3h_iterator_prm_names.prevar_type_1}").pressButton()
            node.parm(f"{PRX_FF_PRM}{flam3h_iterator_prm_names.var_type_1}").pressButton()
            node.parm(f"{PRX_FF_PRM}{flam3h_iterator_prm_names.var_type_2}").pressButton()
            node.parm(f"{PRX_FF_PRM}{flam3h_iterator_prm_names.postvar_type_1}").pressButton()
            node.parm(f"{PRX_FF_PRM}{flam3h_iterator_prm_names.postvar_type_2}").pressButton()
            
            _MSG = "Iterator var menus: ICONS"
            flam3h_general_utils.flash_message(node, f"{_MSG}")
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
            
        # Change focus back to the FLAME's Tab
        node.parmTuple(FLAM3H_ITERATORS_TAB).set((0,))

    
    
    def menu_T_data(self) -> tuple[int, str]:
        """Rerturn the selected variation index and the correct bookmark icon to use
        based on its weight value.

        Returns:
            tuple[int, str]: int: variation idx.    str: icon
        """        
        _TYPE, w = self.menu_T_get_var_data()
        return _TYPE, self.menu_T_get_type_icon(w)


    
    def menu_T_PP_data(self) -> tuple[int, str]:
        """Rerturn the selected variation index and the correct bookmark icon to use
        based on its weight value.

        Returns:
            tuple[int, str]: int: variation idx.    str: icon
        """        
        _TYPE, w = self.menu_T_get_var_data()
        return _TYPE, self.menu_T_PP_get_type_icon(w)
    
    
    
    def menu_T_FF_data(self) -> tuple[int, str]:
        """Rerturn the selected FF variation index and the correct bookmark icon to use
        based on its weight value.

        Returns:
            tuple[int, str]: int: variation idx.    str: icon
        """        
        _TYPE, w = self.menu_T_FF_get_var_data()
        return _TYPE, self.menu_T_get_type_icon(w)
    
    
    
    def menu_T_PP_FF_data(self) -> tuple[int, str]:
        """Rerturn the selected FF variation index and the correct bookmark icon to use
        based on its weight value.

        Returns:
            tuple[int, str]: int: variation idx.    str: icon
        """        
        _TYPE, w = self.menu_T_FF_get_var_data()
        return _TYPE, self.menu_T_PP_get_type_icon(w)
    
    
    
    def menu_T_pb_data(self) -> str:
        """Rerturn the bookmark icon to use for the Pre blur variation
        based on its weight value.

        Returns:
            tuple[int, str]: int: variation idx.    str: icon
        """        
        idx = self.kwargs['script_multiparm_index']
        prm_weight_name = f"{flam3h_iterator_prm_names.prevar_weight_blur}_{str(idx)}"

        w = self.node.parm(prm_weight_name).eval()

        if w > 0:
            if w > 1:
                return FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV_OVER_ONE
            else:
                return FLAM3H_ICON_STAR_FLAME_VAR_PP_ACTV
            
        return FLAM3H_ICON_STAR_EMPTY_OPACITY
    
    
    
    def menu_T_ICON(self, FF=False) -> list:
        """Populate variation names parameter menu list and add proper bookmark icons based on their weights.
        Differentiate iterators and FF
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.

        Returns:
            list: [return menu list]
        """
        menu = copy(MENU_VARS_ALL_SIMPLE)
        if not FF: _TYPE, _ICON = self.menu_T_data()
        else: _TYPE, _ICON = self.menu_T_FF_data()
        var = MENU_VARS_INDEXES.get(_TYPE)
        assert var is not None
        menu[var] = f"{_ICON} {menu[var][:13]}     "

        return menu



    def menu_T_PP_ICON(self, FF=False) -> list:
        """Populate variation names parameter menu list and add proper bookmark icons based on their weights.
        Differentiate iterators and FF
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.

        Returns:
            list: [return menu list]
        """
        menu = copy(MENU_VARS_ALL_SIMPLE)
        if not FF: _TYPE, _ICON = self.menu_T_PP_data()
        else: _TYPE, _ICON = self.menu_T_PP_FF_data()
        var = MENU_VARS_INDEXES.get(_TYPE)
        assert var is not None
        menu[var] = f"{_ICON} {menu[var][:13]}     "
            
        return menu
    
    
    
    def menu_T_simple(self, FF=False) -> list:
        """Populate variation names parameter menu list.

        Returns:
            list: [return menu list]
        """
        self.node.setCachedUserData('vars_menu_all_simple', MENU_VARS_ALL_SIMPLE)
        return MENU_VARS_ALL_SIMPLE
    
    
    def menu_T(self, FF=False) -> list:
        """Populate variation names parameter menu list.
        Differentiate iterators and FF
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.

        Returns:
            list: [return menu list]
        """
        node = self.node
        
        # This data get created inside: menu_T_simple(self, FF=False) -> list:
        # This data get destroyed inside: refresh_iterator_vars_menu(self) -> None:
        data = node.cachedUserData('vars_menu_all_simple')
        if data is not None:
            return data
        else:
            run = (self.menu_T_simple, self.menu_T_ICON)
            _ICONS_TOGGLE = node.parm(PREFS_ITERATOR_BOOKMARK_ICONS).eval()
            return run[_ICONS_TOGGLE](FF)

    
    
    def menu_T_PP(self, FF=False) -> list:
        """Populate variation names parameter menu list.
        Differentiate iterators and FF
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.

        Returns:
            list: [return menu list]
        """
        node = self.node
        # This data get created inside: menu_T_simple(self, FF=False) -> list:
        # This data get destroyed inside: refresh_iterator_vars_menu(self) -> None:
        data = node.cachedUserData('vars_menu_all_simple')
        if data is not None:
            return data
        else:
            run = (self.menu_T_simple, self.menu_T_PP_ICON)
            _ICONS_TOGGLE = node.parm(PREFS_ITERATOR_BOOKMARK_ICONS).eval()
            return run[_ICONS_TOGGLE](FF)
    
    
    
    def menu_T_pb(self) -> list:
        """Populate variation name parameter menu list for Pre blur variation
        
        _NOTE:
            When changing weight's value, the bookmark icon will updated too
            but it wont updated when we click the menu parameter to see all its entries until we dnt make a new selection.
            Not sure if this is to be considered a bug or is intended, perhaps I should note this to SideFx.

        Returns:
            list: [return menu list]
        """
        _ICON = self.menu_T_pb_data()
        return [ 0,  f"{_ICON} Pre blur                   "] # 19 times \s



    def menu_select_iterator_data(self) -> list:
        """Build a menu of iterators using their states as bookmark icon

        Returns:
        """
        node = self.node
        menu = []

        iter_count = node.parm(FLAME_ITERATORS_COUNT).eval()
        if iter_count:
            
            note = [node.parm(f'note_{idx+1}').eval() for idx in range(iter_count)]
            
            active: list = [node.parm(f'vactive_{idx+1}').eval() for idx in range(iter_count)]
            weight: list = [node.parm(f'iw_{idx+1}').eval() for idx in range(iter_count)]
            shader_opacity: list = [node.parm(f'alpha_{idx+1}').eval() for idx in range(iter_count)]
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
                
                idx = i+1
                menu.append(idx)

                _OPACITY_MSG = ""
                if shader_opacity[i] == 0: _OPACITY_MSG = "[ZERO opacity] "
                
                if active[i] and weight[i] > 0:
                    # check if it is marked for being copied
                    if node == from_FLAM3H_NODE and mp_id_from == idx:
                        menu.append(f"{FLAM3H_ICON_COPY_PASTE}  {idx}:  {_OPACITY_MSG}{note[i]}")
                    else:
                        menu.append(f"{FLAM3H_ICON_STAR_FLAME_ITER_ACTV}  {idx}:  {_OPACITY_MSG}{note[i]}")
                        
                elif active[i] and weight[i] == 0:
                    # check if it is marked for being copied
                    if node == from_FLAM3H_NODE and mp_id_from == idx:
                        menu.append(f"{FLAM3H_ICON_COPY_PASTE_ENTRIE_ZERO}  {idx}:  {_OPACITY_MSG}{note[i]}")
                    else:
                        menu.append(f"{FLAM3H_ICON_STAR_EMPTY_OPACITY}  {idx}:  {_OPACITY_MSG}{note[i]}")
                else:
                    # check if it is marked for being copied
                    if node == from_FLAM3H_NODE and mp_id_from == idx:
                        menu.append(f"{FLAM3H_ICON_COPY_PASTE_ENTRIE}  {idx}:  {_OPACITY_MSG}{note[i]}")
                    else:
                        menu.append(f"{FLAM3H_ICON_STAR_EMPTY}  {idx}:  {_OPACITY_MSG}{note[i]}")
                        
        else:
            menu = [0, f"{FLAM3H_ICON_COPY_PASTE_INFO}  ZERO ITERATORS.\n-> Please, create at least one iterator or load a IN flame file first.", 1, ""]
                
        node.setCachedUserData('iter_sel', menu)
        return menu
    
    
    
    def menu_select_iterator(self) -> list:
        node = self.node
        
        mem_id = node.parm(FLAM3H_DATA_PRM_MPIDX).eval()
        if node.cachedUserData('iter_sel_id') != mem_id and mem_id:
            self.destroy_data(node, 'iter_sel')

        # For undos: compare old data_* against current data_*
        # Another piece for the undos to work is inside: def prm_paste_update_for_undo(self, node: hou.SopNode)
        iter_count = node.parm(FLAME_ITERATORS_COUNT).eval()
        data_awo_now = [[node.parm(f'vactive_{idx+1}').eval() for idx in range(iter_count)], [node.parm(f'iw_{idx+1}').eval() for idx in range(iter_count)], [node.parm(f'alpha_{idx+1}').eval() for idx in range(iter_count)]]
        [self.destroy_data(node, 'iter_sel') if node.cachedUserData('iter_sel') is not None and data != data_awo_now[idx] else ... for idx, data in ((0, node.cachedUserData('iter_sel_a')), (1, node.cachedUserData('iter_sel_w')), (2, node.cachedUserData('iter_sel_o')))]
        
        menu = node.cachedUserData('iter_sel')
        if menu is not None:
            return menu
        else:
            return self.menu_select_iterator_data()
        
    
    
    def prm_select_iterator(self) -> None:
        """Change multi-parameter index focus based on the selected iterator number from: def menu_select_iterator(self) -> list:
        
        _NOTE:
            Need to investigate more how to control the Network Editor's Parameter Dialog displayed when pressing the "p" key.
            For now, it will just do nothing and let the user know.

        Returns:
        """
        node = self.node
        iter_count = node.parm(FLAME_ITERATORS_COUNT).evalAsInt()

        if iter_count:
            
            # This definition probably can be made more light-weight for this particular case
            from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)
            
            prm = node.parm(FLAME_ITERATORS_COUNT)
            preset_id = node.parm(SYS_SELECT_ITERATOR).eval()
            
            try:
                # We first try to set them all with this
                hou.ui.setMultiParmTabInEditors(prm, preset_id-1) # type: ignore
                _CHECK = True
            except:
                _CHECK = False

            if _CHECK:
                
                # Change focus back to the FLAME's Tab
                node.parmTuple(FLAM3H_ITERATORS_TAB).set((0,))
                
                _MSG = f"iterator: {preset_id}"
                active = node.parm(f"{flam3h_iterator_prm_names.main_vactive}_{preset_id}").eval()
                weight = node.parm(f"{flam3h_iterator_prm_names.main_weight}_{preset_id}").eval()
                
                if node == from_FLAM3H_NODE and mp_id_from == preset_id:
                    if active and weight>0: flam3h_general_utils.flash_message(node, f"{_MSG} (Marked)")
                    elif active and weight==0: flam3h_general_utils.flash_message(node, f"{_MSG} (Zero Weight and Marked)")
                    else: flam3h_general_utils.flash_message(node, f"{_MSG} (Disabled and Marked)")
                    
                else:
                    if active and weight>0: flam3h_general_utils.flash_message(node, _MSG)
                    elif active and weight==0: flam3h_general_utils.flash_message(node, f"{_MSG} (Zero Weight)")
                    else: flam3h_general_utils.flash_message(node, f"{_MSG} (Disabled)")
                
            else:
                # If we can not set them all, lets see different cases one by one
                
                paneTab_uc = hou.ui.paneTabUnderCursor() # type: ignore

                if paneTab_uc is not None:

                    if paneTab_uc.type() == hou.paneTabType.Parm: # type: ignore
                        
                        paneTab_uc.setMultiParmTab(prm.name(), preset_id-1)
                        
                        # Change focus back to the FLAME's Tab
                        node.parmTuple(FLAM3H_ITERATORS_TAB).set((0,))
                        
                        _MSG = f"iterator: {preset_id}"
                        active = node.parm(f"{flam3h_iterator_prm_names.main_vactive}_{preset_id}").eval()
                        
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
                            _MSG = "This feature is not working over the Network Editor's Parameter Dialog displayed when pressing the \"p\" key.\nPlease, open a Parameter Editor in its own pane tab or floating panel for this feature to work."
                            hou.ui.displayMessage(_MSG, buttons=("Got it, thank you",), severity=hou.severityType.ImportantMessage, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Select Iterator mini-menu", details=None, details_label=None, details_expanded=False) # type: ignore
                        
                        _MSG = "Selection do not work over Network Editors"
                        flam3h_general_utils.flash_message(node, f"{_MSG}")
                        flam3h_general_utils.set_status_msg(f"{node.name()}: Iterator's {_MSG.lower()}.", 'IMP')
                        
                    else:
                        _MSG = "Ops! That did not work!"
                        flam3h_general_utils.flash_message(node, f"{_MSG}")
                        flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG} The pane under the cursor must be a valid Parameter Editor pane or floating panel.", 'IMP')
                    
                else:
                    _MSG = "Ops! That did not work!"
                    flam3h_general_utils.flash_message(node, f"{_MSG}")
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG} The pane under the cursor must be a valid Parameter Editor pane or floating panel.", 'IMP')
        
        # reset selection to null value
        node.setParms({SYS_SELECT_ITERATOR: 0}) # type: ignore
    
    
    
    def flam3h_paste_reset_hou_session_data(self) -> None:
        """init/clear copy/paste iterator's data and prm
        """        
        node = self.node
        
        try:
            hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
            from_FLAM3HNODE = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
        except:
            from_FLAM3HNODE = None
        
        if from_FLAM3HNODE is not None and node == from_FLAM3HNODE:  # type: ignore
            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = None # type: ignore
            hou.session.FLAM3H_MARKED_FF_NODE = node # type: ignore
            hou.session.FLAM3H_MARKED_FF_CHECK = None # type: ignore
            # Reset internal mpidx memory to a None value
            if node.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt() != 0:
                self.iterator_mpidx_mem_set(node, 0)
                    
            # Remove any comment and user data from the node
            self.del_comment_and_user_data_iterator(node)
            self.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)
    

    def menu_global_density_py(self) -> list:
        """Build density menu parameter with a list of options.
        This is obsolete now and replaced with: def menu_global_density(self) -> None
        
        NOT USED ANYMORE
        
        Args:
            NONE (None): [description.]

        Returns:
            list: [return menu list]
        """
        iterators = self.node.parm(FLAME_ITERATORS_COUNT).evalAsInt()
        menu=[]
        menuitems = ()
        if iterators:
            menuitems = ( "", "1M", "2M", "5M", "15M", "25M", "50M", "100M", "150M", "250M", f"{FLAM3H_ICON_STAR_HIGH_TIER}500M", f"{FLAM3H_ICON_STAR_HIGH_TIER}750M", f"{FLAM3H_ICON_STAR_HIGH_TIER}1 Billion", "" )
        else:
            menuitems = ("Please, add at least one iterator", "")
        for i, item in enumerate(menuitems):
            menu.append(i)
            menu.append(item)
    
        return menu
    
    
    
    def menu_global_density(self) -> list:
        """Return a pre built static menu data.
        
        Args:
            NONE (None): [description.]

        Returns:
            list: [return menu list]
        """
        return MENU_DENSITY
    
    
    def menu_global_density_set(self) -> None:
        """Set density menu parameter based on user choice.
        
        """        
        node = self.node
        ptcount = node.parm(GLB_DENSITY).evalAsInt()
        sel = self.kwargs['parm'].evalAsInt()
        vals = { 0: 500000, 1: 1000000, 2: 2000000, 3: 5000000, 4: 15000000, 5: 25000000, 6: 50000000, 7: 100000000, 8: 150000000, 9: 250000000, 10: 500000000, 11: 750000000, 12: 1000000000}
        vals_name = { 0: "Default: 500K points", 1: "1 Millions points", 2: "2 Millions points", 3: "5 Millions points", 4: "15 Millions points", 5: "25 Millions points", 6: "50 Millions points", 7: "100 Millions points", 8: "150 Millions points", 9: "250 Millions points", 10: "500 Millions points", 11: "750 Millions points", 12: "1 Billions points"}
        
        if ptcount != vals[sel]:
            node.parm(GLB_DENSITY).deleteAllKeyframes()
            node.setParms({GLB_DENSITY: vals.get(sel)}) # type: ignore
            _MSG = f"{node.name()} -> DENSITY preset: \" {vals_name.get(sel)} \" -> SET"
            flam3h_general_utils.set_status_msg(_MSG, 'MSG')
  
        # reset to null value so we can set the same preset again
        node.setParms({GLB_DENSITY_PRESETS: 0}) # type: ignore


    # Set menu_density() Menu
    def menu_global_density_set_default(self) -> None:
        """Revert density parameter to its default value.
        """        
        node = self.node
        ptcount = node.parm(GLB_DENSITY).evalAsInt()
        if ptcount != FLAM3H_DEFAULT_GLB_DENSITY:
            node.parm(GLB_DENSITY).deleteAllKeyframes()
            node.setParms({GLB_DENSITY: FLAM3H_DEFAULT_GLB_DENSITY}) # type: ignore
            _MSG = f"{node.name()} -> DENSITY preset: \" Default: 500K points \" -> SET"
            flam3h_general_utils.set_status_msg(_MSG, 'MSG')
        else:
            _MSG = f"{node.name()}: DENSITY -> already at its default value."
            flam3h_general_utils.set_status_msg(_MSG, 'MSG')
    
    
    def menu_copypaste(self) -> list:
        """Build copy/paste parameter menu entries.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]

        Returns:
            list: [return menu list]
        """    
        menu=[]
        
        node = self.node
        id = self.kwargs['script_multiparm_index']
        idx = str(id)
        
        if self.exist_user_data(node):
            node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore
        
        # Updated data for copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)
        
        # This undo's disabler is needed to make the undo work in H20.5 ater copy/paste an iterator's section from the mini-menu.
        with hou.undos.disabler(): # type: ignore
            
            if mp_id_from is not None:
                assert from_FLAM3H_NODE is not None
                
                idx_from = str(mp_id_from)
                
                prm_selmem = node.parm(f"selmem_{idx}")
                if prm_selmem.evalAsInt() > 0:
                    node.setParms({f"prmpastesel_{idx}": 0})
                    prm_selmem.set(0)
                    
                # Menu entrie sections bookmark icon
                active = from_FLAM3H_NODE.parm(f"vactive_{idx_from}").eval()
                weight = from_FLAM3H_NODE.parm(f"iw_{idx_from}").eval()
                if active and weight > 0: _ICON = FLAM3H_ICON_COPY_PASTE_ENTRIE
                else: _ICON = FLAM3H_ICON_COPY_PASTE_ENTRIE_ZERO
                
                # Build menu
                if node == from_FLAM3H_NODE and id==mp_id_from:
                    menu = [ 0, f"{FLAM3H_ICON_COPY_PASTE_INFO}  {idx}: MARKED.\n-> Select a different iterator number or a different FLAM3H node to paste its values.", 1,"" ]
                elif node == from_FLAM3H_NODE:
                    menu = [ 0, "", 1, f"{FLAM3H_ICON_COPY_PASTE}  All (no xaos:)", 2, f"{_ICON}  {idx_from}", 3, f"{_ICON}  {idx_from}:  xaos:", 4, f"{_ICON}  {idx_from}:  shader", 5, f"{_ICON}  {idx_from}:  PRE", 6, f"{_ICON}  {idx_from}:  VAR", 7, f"{_ICON}  {idx_from}:  POST", 8, f"{_ICON}  {idx_from}:  pre affine", 9, f"{_ICON}  {idx_from}:  post affine", 10, "" ]
                else:
                    assert from_FLAM3H_NODE is not None
                    parent = f".../{from_FLAM3H_NODE.parent()}"
                    flam3nodeIter = f"{from_FLAM3H_NODE.name()}.iter."
                    menu = [ 0, "", 1, f"{FLAM3H_ICON_COPY_PASTE}  All (no xaos:)", 2, f"{_ICON}  {parent}/{flam3nodeIter}{idx_from}", 3, f"{_ICON}  {parent}/{flam3nodeIter}{idx_from}:  xaos:", 4, f"{_ICON}  {parent}/{flam3nodeIter}{idx_from}:  shader", 5, f"{_ICON}  {parent}/{flam3nodeIter}{idx_from}:  PRE", 6, f"{_ICON}  {parent}/{flam3nodeIter}{idx_from}:  VAR", 7, f"{_ICON}  {parent}/{flam3nodeIter}{idx_from}:  POST", 8, f"{_ICON}  {parent}/{flam3nodeIter}{idx_from}:  pre affine", 9, f"{_ICON}  {parent}/{flam3nodeIter}{idx_from}:  post affine", 10, "" ]
                
                return menu
            
            else:
                if isDELETED:
                    return [ 0, f"{FLAM3H_ICON_COPY_PASTE_INFO_ORANGE}  DELETED: Marked iterator's node has been deleted.\n-> Mark another iterator first.", 1, "" ]
                
                else:
                    if from_FLAM3H_NODE is not None:
                        assert from_FLAM3H_NODE is not None
                        _FLAM3H_DATA_PRM_MPIDX = node.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt()
                        __FLAM3H_DATA_PRM_MPIDX = from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt()
                        if node == from_FLAM3H_NODE and _FLAM3H_DATA_PRM_MPIDX == -1:
                            menu = [ 0, f"{FLAM3H_ICON_COPY_PASTE_INFO_ORANGE}  REMOVED: The marked iterator has been removed.\n-> Mark an existing iterator instead.", 1, "" ]
                        elif node != from_FLAM3H_NODE and __FLAM3H_DATA_PRM_MPIDX == -1:
                            parent = f".../{from_FLAM3H_NODE.parent()}"
                            menu = [ 0, f"{FLAM3H_ICON_COPY_PASTE_INFO_ORANGE}  REMOVED: The marked iterator has been removed from node: {parent}/{from_FLAM3H_NODE.name()}\n-> Mark an existing iterator instead.", 1, "" ]
                        else:
                            menu = [ 0, f"{FLAM3H_ICON_COPY_PASTE}  {MARK_ITER_MSG}.", 1, "" ]
                    
                        return menu
                    
                    else:
                        return [ 0, f"{FLAM3H_ICON_COPY_PASTE}  {MARK_ITER_MSG}.", 1, "" ]

    
    
    def menu_copypaste_FF(self) -> list:
        """Build copy/paste FF parameter menu entries.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]

        Returns:
            list: [return menu list]
        """    
        menu=[]
        
        node = self.node
        
        # This is to make sure the hou.session's data is at least initialized.
        self.flam3h_init_hou_session_ff_data(node)
        
        # Updated data for FF copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, from_FLAM3H_NODE_FF_CHECK, isDELETED = self.prm_paste_update_for_undo_ff(node)

        if from_FLAM3H_NODE_FF_CHECK is not None:

            flam3node_FF = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
            
            # This undo's disabler is needed to make the undo work in H20.5 after copy/paste an FF's section from the mini-menu.
            with hou.undos.disabler(): # type: ignore
            
                if node == flam3node_FF:
                    return MENU_FF_COPY_PASTE_SELECT

                else:
                    # Menu entrie sections bookmark icon
                    active = flam3node_FF.parm(SYS_DO_FF).eval()
                    if active: _ICON = FLAM3H_ICON_COPY_PASTE_ENTRIE_FF
                    else: _ICON = FLAM3H_ICON_COPY_PASTE_ENTRIE_ZERO
                    
                    prm_selmem = node.parm(f"{PRX_FF_PRM}selmem")
                    if prm_selmem.evalAsInt() > 0:
                        node.setParms({f"{PRX_FF_PRM}prmpastesel": 0})
                        prm_selmem.set(0)
                    
                    parent = f".../{flam3node_FF.parent()}"
                    flam3nodeFF = f"{str(flam3node_FF)}.FF"
                    return [ 0, "", 1, f"{FLAM3H_ICON_COPY_PASTE}  All", 2, f"{_ICON}  {parent}/{flam3nodeFF}:  PRE", 3, f"{_ICON}  {parent}/{flam3nodeFF}:  VAR", 4, f"{_ICON}  {parent}/{flam3nodeFF}:  POST", 5, f"{_ICON}  {parent}/{flam3nodeFF}:  pre affine", 6, f"{_ICON}  {parent}/{flam3nodeFF}:  post affine", 7, "" ]
        
        else:
            return MENU_FF_COPY_PASTE_EMPTY
        
        
        
    def prm_paste_update_for_undo(self, node: hou.SopNode) -> tuple[Union[hou.SopNode, None], Union[int, None], bool]:
        """Updated data for copy/paste iterator's methods in case of Undos.
        It will make sure that the houdini.session data about the iterator index
        will always be up to date.
        
        It is for: hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX -> UNDO, so to speak -> prm: FLAM3H_DATA_PRM_MPIDX

        Args:
            node (hou.SopNode): the current FLAM3H node

        Returns:
            tuple[Union[hou.SopNode, None], Union[int, None], bool]: 
            
            from_FLAM3H_NODE -> is the node we are copying the data from. 
            
            mp_id_from -> Multiparameter index. Is the iterator number we are copying from inside "from_FLAM3H_NODE".
            
            isDELETED -> will tell us if "from_FLAM3H_NODE" still exist.
        """        
        
        isDELETED = False
        _FLAM3H_DATA_PRM_MPIDX = node.parm(FLAM3H_DATA_PRM_MPIDX).eval()
            
        try:
            from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore 
            assert from_FLAM3H_NODE is not None
            __FLAM3H_DATA_PRM_MPIDX = from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).eval()
        except:
            from_FLAM3H_NODE = None
            __FLAM3H_DATA_PRM_MPIDX = 0
            
        try:
            hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
            mp_id_from = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
            
            if node == from_FLAM3H_NODE:
                if _FLAM3H_DATA_PRM_MPIDX > 0:
                    if mp_id_from != _FLAM3H_DATA_PRM_MPIDX:
                        mp_id_from = _FLAM3H_DATA_PRM_MPIDX
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = mp_id_from  # type: ignore
                        self.del_comment_and_user_data_iterator(node)
                        self.set_comment_and_user_data_iterator(node, str(mp_id_from))
                        self.destroy_data(node, 'iter_sel')
                else:
                    if _FLAM3H_DATA_PRM_MPIDX == -1:
                        mp_id_from = None
                        self.del_comment_and_user_data_iterator(node)
                        self.destroy_data(node, 'iter_sel')
            else:
                if __FLAM3H_DATA_PRM_MPIDX > 0:
                    if mp_id_from != __FLAM3H_DATA_PRM_MPIDX:
                        mp_id_from = __FLAM3H_DATA_PRM_MPIDX
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = mp_id_from  # type: ignore
                        assert from_FLAM3H_NODE is not None
                        self.del_comment_and_user_data_iterator(from_FLAM3H_NODE)
                        self.set_comment_and_user_data_iterator(from_FLAM3H_NODE, str(mp_id_from))
                        self.destroy_data(node, 'iter_sel')
                else:
                    if __FLAM3H_DATA_PRM_MPIDX == -1:
                        mp_id_from = None
                        assert from_FLAM3H_NODE is not None
                        self.del_comment_and_user_data_iterator(from_FLAM3H_NODE)
                        self.destroy_data(node, 'iter_sel')
                        
        except:
            mp_id_from = None
            isDELETED = True
            self.destroy_data(self.node, 'iter_sel')
            
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
                        self.destroy_data(node, 'iter_sel')
                        break
            # Mark, mark another node, Undo, Redo
            elif node != from_FLAM3H_NODE and self.exist_user_data(node):
                from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_ITERATOR_NODE = node # type: ignore
                mp_id_from = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = self.get_user_data(node) # type: ignore
                self.iterator_mpidx_mem_set(node, int(self.get_user_data(node)))
                self.destroy_data(node, 'iter_sel')

        # Mark, Clear, Mark, Undo
        elif mp_id_from is None and from_FLAM3H_NODE is not None:
            if node == from_FLAM3H_NODE and self.exist_user_data(from_FLAM3H_NODE):
                mp_id_from = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = self.get_user_data(from_FLAM3H_NODE) # type: ignore
                self.iterator_mpidx_mem_set(from_FLAM3H_NODE, int(self.get_user_data(from_FLAM3H_NODE)))
                self.destroy_data(node, 'iter_sel')


        if isDELETED is False:
            if mp_id_from is not None and from_FLAM3H_NODE is not None:
                if not self.exist_user_data(from_FLAM3H_NODE):
                    mp_id_from = None
                    self.destroy_data(node, 'iter_sel')
        
        return from_FLAM3H_NODE, mp_id_from, isDELETED



    def prm_paste_update_for_undo_ff(self, node: hou.SopNode) -> tuple[Union[hou.SopNode, None], Union[int, None], bool]:
        """Updated data for copy/paste iterator's methods in case of Undos.
        It will make sure that the houdini.session data about the iterator index
        will always be up to date.
        
        It is for: hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX -> UNDO, so to speak -> prm: FLAM3H_DATA_PRM_MPIDX

        Args:
            node (hou.SopNode): the current FLAM3H node

        Returns:
            tuple[Union[hou.SopNode, None], Union[int, None], bool]: 
            
            from_FLAM3H_NODE -> is the node we are copying the data from. 
            
            from_FLAM3H_NODE_FF_CHECK -> Is the FF being marked or not".
            
            isDELETED -> will tell us if "from_FLAM3H_NODE" still exist.
        """     
        
        from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
        from_FLAM3H_NODE_FF_CHECK = hou.session.FLAM3H_MARKED_FF_CHECK # type: ignore
        
        
        isDELETED = False
        try:
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
            id (int): current multi parameter index
            node (hou.SopNode): this FLAM3H node
        """    
        node = self.node
        # Updated data for copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)
                
        if mp_id_from is not None:
            
            idx = str(id)
            idx_from = str(mp_id_from)
            
            if node==from_FLAM3H_NODE and id==mp_id_from:
                _MSG = f"{node.name()}: This iterator is marked: {idx_from} -> Select a different iterator number or a different FLAM3H node to paste its values."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"This iterator is Marked")
            else:
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator.allT, flam3h_varsPRM.varsPRM, idx, idx_from)
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator.allMisc, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_ALL, idx, idx_from)

        else:
            if isDELETED:
                _MSG_DEL = "Marked iterator's node has been deleted"
                _MSG = f"{node.name()}: {_MSG_DEL} -> {MARK_ITER_MSG_STATUS_BAR}"
                flam3h_general_utils.set_status_msg(_MSG, 'WARN') 
                flam3h_general_utils.flash_message(node, _MSG_DEL)
                
            else:
                _MSG_REM = "Marked iterator has been removed"
                if node == from_FLAM3H_NODE:
                    _FLAM3H_DATA_PRM_MPIDX = node.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt()
                    if _FLAM3H_DATA_PRM_MPIDX == -1:
                        _MSG = f"{node.name()} -> {_MSG_REM} -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, _MSG_REM)
                    else:
                        _MSG = f"{node.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, MARK_ITER_MSG)
                        
                elif node != from_FLAM3H_NODE:
                    assert from_FLAM3H_NODE is not None
                    __FLAM3H_DATA_PRM_MPIDX = from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt()
                    
                    if __FLAM3H_DATA_PRM_MPIDX == -1:
                        _MSG = f"{node.name()} -> {_MSG_REM} from node: {from_FLAM3H_NODE.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, _MSG_REM)
                    else:
                        _MSG = f"{node.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, MARK_ITER_MSG)
                        
                else:
                    _MSG = f"{node.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                    flam3h_general_utils.flash_message(node, MARK_ITER_MSG)


    def prm_paste_SHIFT(self, id: int) -> None:
        """Everything about unmarking iterators from being copied.

        Args:
            id (int): current multi parameter index
            node (hou.SopNode): this FLAM3H node
        """   
        node = self.node
        # Updated data for copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)

        if node == from_FLAM3H_NODE: # type: ignore
            
            _MSG_UNMARKED = "This iterator is Unmarked already"
            assert from_FLAM3H_NODE is not None
            
            if mp_id_from is not None:
                _MSG = f"{node.name()}: iterator UNMARKED -> {str(mp_id_from)}" # type: ignore
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = None # type: ignore
                self.iterator_mpidx_mem_set(node, 0)
                self.del_comment_and_user_data_iterator(node)
                
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                flam3h_general_utils.flash_message(node, f"iterator UNMARKED")
                
            else:
                if from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt() == -1:
                    _MSG = f"{node.name()}: {_MSG_UNMARKED}:  {str(id)}   Unmarked removed iterator -> {str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}" # type: ignore
                else:
                    _MSG = f"{node.name()}: {_MSG_UNMARKED} -> {str(id)}"
                    
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = None # type: ignore
                self.iterator_mpidx_mem_set(node, 0)
                self.del_comment_and_user_data_iterator(node)
                
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        else:
            if isDELETED:
                _MSG_DEL = "Marked iterator's node has been deleted"
                _MSG = f"{node.name()}: {_MSG_DEL} -> Mark a new iterator first."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, _MSG_DEL)
                
            else:
                assert from_FLAM3H_NODE is not None
                __FLAM3H_DATA_PRM_MPIDX = from_FLAM3H_NODE.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt()
                
                if __FLAM3H_DATA_PRM_MPIDX == -1:
                    _MSG = f"{node.name()}: {_MSG_UNMARKED} -> The marked iterator has been removed from node: {from_FLAM3H_NODE.name()} ->  Mark an existing iterator instead." # type: ignore
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                else:
                    _MSG = f"{node.name()}: {_MSG_UNMARKED} -> The marked iterator is from node: {from_FLAM3H_NODE.name()}.iterator.{str(mp_id_from)}" # type: ignore
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
        

    def prm_paste_CLICK(self, id: int) -> None:
        """Everything about marking iterators for being copied.

        Args:
            id (int): current multi parameter index
            node (hou.SopNode): this FLAM3H node
        """        
        node = self.node
        # Updated data for copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, mp_id_from, isDELETED = self.prm_paste_update_for_undo(node)
                
        if self.exist_user_data(node):
            if node.isGenericFlagSet(hou.nodeFlag.DisplayComment) is False: # type: ignore
                node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore


        if node == hou.session.FLAM3H_MARKED_ITERATOR_NODE: # type: ignore
            
            if hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX != id: # type: ignore
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = id # type: ignore
                hou.session.FLAM3H_MARKED_ITERATOR_NODE = self.node # type: ignore
                self.iterator_mpidx_mem_set(node, id)
                self.del_comment_and_user_data_iterator(node)
                self.set_comment_and_user_data_iterator(node, str(id))
                
                _MSG = f"{str(self.node)}: iterator MARKED:  {str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}" # type: ignore
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                flam3h_general_utils.flash_message(node, f"iterator MARKED:  {str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}") # type: ignore
                
            else:
                self.iterator_mpidx_mem_set(node, id)
                self.del_comment_and_user_data_iterator(node)
                self.set_comment_and_user_data_iterator(node, str(id))
                
                _MSG = f"{str(self.node)} -> This iterator is already Marked." # type: ignore
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        else:
            hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = id # type: ignore
            hou.session.FLAM3H_MARKED_ITERATOR_NODE = self.node # type: ignore
            self.iterator_mpidx_mem_set(node, id)
            self.del_comment_and_user_data_iterator(node)
            self.set_comment_and_user_data_iterator(node, str(id))
            
            # Reset the other node mp_idx data
            if from_FLAM3H_NODE is not None:
                self.iterator_mpidx_mem_set(from_FLAM3H_NODE, 0)
                self.del_comment_and_user_data_iterator(from_FLAM3H_NODE)
                
            _MSG = f"{str(self.node)}: iterator MARKED:  {str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}" # type: ignore
            flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            flam3h_general_utils.flash_message(node, f"iterator MARKED:  {str(hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX)}") # type: ignore


    def prm_paste(self) -> None:
        """Paste the entire iterator's data.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """    
        
        node = self.node
        # Clear menu cache
        self.destroy_data(node, 'iter_sel')
        
        id = self.kwargs['script_multiparm_index']
        idx = str(id)
        
        # This is to make sure the hou.session's data is at least initialized.
        self.flam3h_init_hou_session_iterator_data(node)
        
        if self.kwargs["ctrl"]:
            with hou.undos.group(f"FLAM3H paste iterator data CTRL {idx}"): # type: ignore
                self.prm_paste_CTRL(id)
                
        elif self.kwargs["shift"]:
            with hou.undos.group(f"FLAM3H unmark iterator SHIFT {idx}"): # type: ignore
                self.prm_paste_SHIFT(id)
                
        # Adding ability to reset the current iterator to its default values.      
        elif self.kwargs["alt"]:
            with hou.undos.group(f"FLAM3H reset iterator {idx}"): # type: ignore
                self.flam3h_reset_iterator()
                _MSG = f"{node.name()}: Iterator {idx} -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
        
        else:
            if self.exist_user_data(node) and int(self.get_user_data(node))==id and id==hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX and node==hou.session.FLAM3H_MARKED_ITERATOR_NODE: # type: ignore
                with hou.undos.group(f"FLAM3H unmark iterator CLICK {idx}"): # type: ignore
                    self.prm_paste_SHIFT(id)
            else:
                with hou.undos.group(f"FLAM3H mark iterator CLICK {idx}"): # type: ignore
                    self.prm_paste_CLICK(id)
    
    
    def prm_paste_FF_CTRL(self) -> None:
        """Everything about paste FF's data.

        Args:
            node (hou.SopNode): this FLAM3H node
        """    
        node = self.node
        # Updated data for FF copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, from_FLAM3H_NODE_FF_CHECK, isDELETED = self.prm_paste_update_for_undo_ff(node)
            
        if from_FLAM3H_NODE_FF_CHECK is not None:
            
            if node == from_FLAM3H_NODE:
                _MSG = f"{node.name()}: This FF is marked -> Select a different FLAM3H node's FF to paste its values."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"Select a different FLAM3H node's FF")
            else:
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_prevarsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), "", "")
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_varsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM).varsPRM_FF(), "", "")
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_postvarsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), "", "")
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.allMisc_FF, "", "")
                self.paste_set_note(node, from_FLAM3H_NODE, 1, SEC_ALL, "", "")

        else:
            if isDELETED:
                _MSG = f"{node.name()}: Marked FF's node has been deleted -> {MARK_FF_MSG_STATUS_BAR}"
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"Marked FF's node has been deleted")
            else:
                _MSG = f"{node.name()} -> {MARK_FF_MSG_STATUS_BAR}"
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, MARK_FF_MSG)
    
    
    def prm_paste_FF_SHIFT(self) -> None:
        """Everything about unmarking FF from being copied.

        Args:
            node (hou.SopNode): this FLAM3H node
        """  
        node = self.node
        # Updated data for FF copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, from_FLAM3H_NODE_FF_CHECK, isDELETED = self.prm_paste_update_for_undo_ff(node)
            
        if from_FLAM3H_NODE_FF_CHECK is not None: # type: ignore
            if node == from_FLAM3H_NODE:
                assert from_FLAM3H_NODE is not None
                _MSG = f"{node.name()} ->  Unmarked FF: {from_FLAM3H_NODE.name()}.FF" # type: ignore
                hou.session.FLAM3H_MARKED_FF_CHECK = None # type: ignore
                hou.session.FLAM3H_MARKED_FF_NODE = node # type: ignore
                
                self.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)
                
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                flam3h_general_utils.flash_message(node, f"FF UNMARKED")
            else:
                _MSG = f"{node.name()}: This FF is Unmarked already -> The marked FF is from node: {str(hou.session.FLAM3H_MARKED_FF_NODE)}.FF" # type: ignore
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
        else:
            if isDELETED:
                _MSG = f"{node.name()} -> Marked FF's node has been deleted -> Mark a new FF first."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            else:
                _MSG = f"{node.name()}: This FF is Unmarked already"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')


    def prm_paste_FF_CLICK(self) -> None:
        """Everything about marking FF for being copied.

        Args:
            node (hou.SopNode): this FLAM3H node
        """ 
        node = self.node
        # Updated data for FF copy/paste iterator's methods in case of Undos.
        from_FLAM3H_NODE, from_FLAM3H_NODE_FF_CHECK, isDELETED = self.prm_paste_update_for_undo_ff(node)
        
        if self.exist_user_data(node, FLAM3H_USER_DATA_FF):
            if node.isGenericFlagSet(hou.nodeFlag.DisplayComment) is False: # type: ignore
                node.setGenericFlag(hou.nodeFlag.DisplayComment, True) # type: ignore
            
        if from_FLAM3H_NODE_FF_CHECK and node == from_FLAM3H_NODE:
            _MSG = f"{str(self.node)} -> This FF is already Marked." # type: ignore
            flam3h_general_utils.set_status_msg(_MSG, 'MSG')

        else:
            # Remove the FF data and comment from the other node
            if from_FLAM3H_NODE is not None:
                
                self.del_comment_and_user_data_iterator(from_FLAM3H_NODE, FLAM3H_USER_DATA_FF)
                
            hou.session.FLAM3H_MARKED_FF_CHECK = 1 # type: ignore
            hou.session.FLAM3H_MARKED_FF_NODE = self.node # type: ignore
            
            self.del_comment_and_user_data_iterator(node, FLAM3H_USER_DATA_FF)
            self.set_comment_and_user_data_iterator(node, "Yes", FLAM3H_USER_DATA_FF)
            
            _MSG = f"{str(self.node)}: FF MARKED" # type: ignore
            flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            flam3h_general_utils.flash_message(node, f"FF -> MARKED")


    def prm_paste_FF(self) -> None:
        """Paste the entire FF data.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """   
        
        node = self.node
        # This is to make sure the hou.session's data is at least initialized.
        self.flam3h_init_hou_session_ff_data(node)
        
        if self.kwargs["ctrl"]:
            with hou.undos.group(f"FLAM3H paste FF data CTRL"): # type: ignore
                self.prm_paste_FF_CTRL()
                
        elif self.kwargs["shift"]:
            with hou.undos.group(f"FLAM3H unmark FF SHIFT"): # type: ignore
                self.prm_paste_FF_SHIFT()

        # Adding ability to reset the FF to its default values. 
        elif self.kwargs["alt"]:
            with hou.undos.group(f"FLAM3H FF RESET"): # type: ignore
                self.reset_FF()
                _MSG = f"{node.name()}: FF -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
        
        else:
            if self.exist_user_data(node, FLAM3H_USER_DATA_FF) and hou.session.FLAM3H_MARKED_FF_CHECK is not None and node==hou.session.FLAM3H_MARKED_FF_NODE: # type: ignore
                with hou.undos.group(f"FLAM3H unmark FF CLICK"): # type: ignore
                    self.prm_paste_FF_SHIFT()
            else:
                with hou.undos.group(f"FLAM3H mark FF CLICK"): # type: ignore
                    self.prm_paste_FF_CLICK()



    def prm_paste_sel(self) -> None:
        """Paste only sections of an iterator.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """    

        node = self.node
        
        # Marked iterator ( not needed but just in case lets "try" so to speak )
        try:
            mp_id_from = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
        except:
            mp_id_from = None

        if mp_id_from is not None:

            # current iterator
            id = self.kwargs['script_multiparm_index']
            idx = str(id)
            idx_from = str(mp_id_from)

            # Marked iterator node
            from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
            
            # Get user selection of paste methods
            paste_sel = node.parm(f"{flam3h_iterator_prm_names.main_prmpastesel}_{idx}").evalAsInt()
            node.setParms({f"{flam3h_iterator_prm_names.main_selmem}_{idx}": paste_sel})

            # set ALL
            if paste_sel == 1:
                self.prm_paste_CTRL(id)
            # set MAIN
            elif paste_sel == 2:
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_main, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_MAIN, idx, idx_from)
            # set XML_XF_XAOS
            elif paste_sel == 3:
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_xaos, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_XAOS, idx, idx_from)
            # set SHADER 
            elif paste_sel == 4:
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_shader, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_SHADER, idx, idx_from)
            # set PRE VARS
            elif paste_sel == 5:
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_prevarsT, flam3h_varsPRM.varsPRM, idx, idx_from)
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_prevarsW, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_PREVARS, idx, idx_from)
            # set VARS
            elif paste_sel == 6:
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_varsT, flam3h_varsPRM.varsPRM, idx, idx_from)
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_varsW, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_VARS, idx, idx_from)
            # set POST VARS
            elif paste_sel == 7:
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_postvarsT, flam3h_varsPRM.varsPRM, idx, idx_from)
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_postvarsW, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_POSTVARS, idx, idx_from)
            # set PRE AFFINE
            elif paste_sel == 8:
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_preAffine, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_PREAFFINE, idx, idx_from)
            # set POST AFFINE
            elif paste_sel == 9:
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator.sec_postAffine, idx, idx_from)
                self.paste_set_note(node, from_FLAM3H_NODE, 0, SEC_POSTAFFINE, idx, idx_from)
        
            node.setParms({f"{flam3h_iterator_prm_names.main_prmpastesel}_{idx}": 0})
            node.setParms({f"{flam3h_iterator_prm_names.main_selmem}_{idx}": paste_sel})
            
        else:
            _MSG = f"{node.name()} -> {MARK_ITER_MSG_STATUS_BAR}"
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            


    def prm_paste_sel_pre_affine(self) -> None:
        """Paste only either the POST affine.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """    
        # current iterator
        id = self.kwargs['script_multiparm_index']
        idx = str(id)
        
        self.paste_from_list_affine(self.node, flam3h_iterator.sec_postAffine[1:], flam3h_iterator.sec_preAffine, idx)
        
        
        
    def prm_paste_sel_post_affine(self) -> None:
        """Paste only either the PRE affine.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """    
        # current iterator
        id = self.kwargs['script_multiparm_index']
        idx = str(id)
        
        self.paste_from_list_affine(self.node, flam3h_iterator.sec_preAffine, flam3h_iterator.sec_postAffine[1:], idx)
        
        
        
    def prm_paste_sel_pre_affine_FF(self) -> None:
        """Paste only either the FF POST affine.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """    
        
        self.paste_from_list_affine(self.node, flam3h_iterator_FF.sec_postAffine_FF[1:], flam3h_iterator_FF.sec_preAffine_FF, "")
        
        
        
    def prm_paste_sel_post_affine_FF(self) -> None:
        """Paste only either the FF PRE affine.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """    
        
        self.paste_from_list_affine(self.node, flam3h_iterator_FF.sec_preAffine_FF, flam3h_iterator_FF.sec_postAffine_FF[1:], "")
            
            

    def prm_paste_sel_FF(self) -> None:
        """Paste only sections of a FF.
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """    
        
        node = self.node

        # Marked FF check ( not needed but just in case lets "try" so to speak )
        try:
            from_FLAM3H_NODE_FF_CHECK = hou.session.FLAM3H_MARKED_FF_CHECK # type: ignore
        except:
            from_FLAM3H_NODE_FF_CHECK = None
            
        if from_FLAM3H_NODE_FF_CHECK is not None:
            
            # Marked FF node
            from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
            
            # Get user selection of paste methods
            ff_paste_sel = node.parm(f"{PRX_FF_PRM}{flam3h_iterator_prm_names.main_prmpastesel}").evalAsInt()
            node.setParms({f"{PRX_FF_PRM}{flam3h_iterator_prm_names.main_selmem}": ff_paste_sel})
            
            # set FF ALL
            if ff_paste_sel == 1:
                self.prm_paste_FF_CTRL()
            # set FF PRE VARS
            elif ff_paste_sel == 2:
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_prevarsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), "", "")
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_prevarsW_FF, "", "")
                self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_PREVARS, "", "")
            # set FF VARS
            elif ff_paste_sel == 3:
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_varsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM).varsPRM_FF(), "", "")
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_varsW_FF, "", "")
                self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_VARS, "", "")
            # set FF POST VARS
            elif ff_paste_sel == 4:
                self.pastePRM_T_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_postvarsT_FF, flam3h_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), "", "")
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_postvarsW_FF, "", "")
                self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_POSTVARS, "", "")
            # set FF PRE AFFINE
            elif ff_paste_sel == 5:
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_preAffine_FF, "", "")
                self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_PREAFFINE, "", "")
            # set FF POST AFFINE
            elif ff_paste_sel == 6:
                self.paste_from_list(node, from_FLAM3H_NODE, flam3h_iterator_FF.sec_postAffine_FF, "", "")
                self.paste_set_note(node, from_FLAM3H_NODE, 2, SEC_POSTAFFINE, "", "")

            node.setParms({f"{PRX_FF_PRM}{flam3h_iterator_prm_names.main_prmpastesel}": 0})
                    
        else:
            _MSG = f"{node.name()} -> {MARK_FF_MSG_STATUS_BAR}"
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            

    def flam3h_xaos_convert(self) -> None:
        """Here I am using a class function call from: out_flame_utils.out_xf_xaos_from()
        down below inside the save XML/FLAME file section of this file.
        The class function: out_flame_utils.out_xf_xaos_from() convert xaos from TO to FROM and back in one call.
        """
        node = self.node
        autodiv = node.parm(PREFS_XAOS_AUTO_SPACE).evalAsInt()
        div_xaos = 'xaos:'
        div_weight = ':'
        if autodiv:
            div_xaos = 'xaos :'
            div_weight = ' :'
        
        # Get xaos
        f3d = out_flame_utils(self.kwargs)
        # Convert xaos
        xaos_new = f3d.out_xf_xaos_from(0)
        # updated CachedUserData: flam3h_xaos_iterators_prev
        self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_new)
        prm_xaos = flam3h_iterator_prm_names.xaos
        [node.setParms({f"{prm_xaos}_{str(idx+1)}": div_xaos + div_weight.join(xaos_new[idx].split(" "))}) if xaos_new[idx] else node.setParms({f"{prm_xaos}_{str(idx+1)}": div_xaos}) for idx in range(f3d.iter_count)]

        # for idx in range(f3d.iter_count):
        #     if xaos_new[idx]:
        #         xs = div_xaos + div_weight.join(xaos_new[idx].split(" "))
        #         node.setParms({f"{prm_xaos}_{str(idx+1)}": xs})
        #     else:
        #         # I dnt think this is needed anymore but i leave it here.
        #         node.setParms({f"{prm_xaos}_{str(idx+1)}": div_xaos})

        # Get preference xaos mode and print to Houdini's status bar
        if f3d.xm:
            _MSG = f"{node.name()}: XAOS Mode -> FROM"
        else:
            _MSG = f"{node.name()}: XAOS Mode -> TO"
        flam3h_general_utils.set_status_msg(_MSG, 'MSG')



    def reset_preaffine(self) -> None:
        """Reset an iterator pre affine values to their defaults.
        """        
        node = self.node
        n = flam3h_iterator_prm_names
        id = self.kwargs['script_multiparm_index']
        idx = str(id)
        check = True
        
        current = { "affine_x": node.parmTuple(f"{n.preaffine_x}_{idx}"), "affine_y": node.parmTuple(f"{n.preaffine_y}_{idx}"), "affine_o": node.parmTuple(f"{n.preaffine_o}_{idx}"), "angle": node.parm(f"{n.preaffine_ang}_{idx}") }
        
        if self.kwargs["shift"]:
            for key in list(AFFINE_DEFAULTS.keys())[:1]:
                if current[key].eval() != AFFINE_DEFAULTS.get(key):
                    check = False
                    # pre affine
                    current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                    current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                    # Print to Houdini's status bar
                    _MSG = f"{node.name()}: Iterator.{idx} PRE Affine X, Y -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    break
            if check:
                _MSG = f"{node.name()}: Iterator.{idx} PRE Affine X, Y -> already at their default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        elif self.kwargs["ctrl"]:
            if current["affine_o"].eval() != AFFINE_DEFAULTS.get("affine_o"):
                check = False
                current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                # Print to Houdini's status bar
                _MSG = f"{node.name()}: Iterator.{idx} PRE Affine O -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            if check:
                _MSG = f"{node.name()}: Iterator.{idx} PRE Affine O -> already at its default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        elif self.kwargs["alt"]:
            if current["angle"].eval() != AFFINE_DEFAULTS.get("angle"):
                check = False
                current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                # Print to Houdini's status bar
                _MSG = f"{node.name()}: Iterator.{idx} PRE Affine Rotation Angle -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            if check:
                _MSG = f"{node.name()}: Iterator.{idx} PRE Affine Rotation Angle -> already at its default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            
        else:
            for key in list(AFFINE_DEFAULTS.keys()):
                if current[key].eval() != AFFINE_DEFAULTS[key]:
                    check = False
                    # pre affine
                    current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                    current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                    current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                    current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                    # Print to Houdini's status bar
                    _MSG = f"{node.name()}: Iterator.{idx} PRE Affine -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    break
            if check:
                _MSG = f"{node.name()}: Iterator.{idx} PRE Affine -> already at their default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')


        
    def reset_postaffine(self) -> None:
        """Reset an iterator post affine values to their defaults.
        """        
        node = self.node
        n = flam3h_iterator_prm_names
        id = self.kwargs['script_multiparm_index']
        idx = str(id)
        
        if node.parm(f"{n.postaffine_do}_{idx}").eval(): # This can be omitted as the post affine tab wont be accessible if this toggle is off.
                
            check = True
            current = { "affine_x": node.parmTuple(f"{n.postaffine_x}_{idx}"), "affine_y": node.parmTuple(f"{n.postaffine_y}_{idx}"), "affine_o": node.parmTuple(f"{n.postaffine_o}_{idx}"), "angle": node.parm(f"{n.postaffine_ang}_{idx}") }
            
            if self.kwargs["shift"]:
                for key in list(AFFINE_DEFAULTS.keys())[:1]:
                    if current[key].eval() != AFFINE_DEFAULTS[key]:
                        check = False
                        # pre affine
                        current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                        current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                        # Print to Houdini's status bar
                        _MSG = f"{node.name()}: Iterator.{idx} POST Affine X, Y -> RESET"
                        flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                        break
                if check:
                    _MSG = f"{node.name()}: Iterator.{idx} POST Affine X, Y -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    
            elif self.kwargs["ctrl"]:
                if current["affine_o"].eval() != AFFINE_DEFAULTS.get("affine_o"):
                    check = False
                    current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                    # Print to Houdini's status bar
                    _MSG = f"{node.name()}: Iterator.{idx} POST Affine O -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                if check:
                    _MSG = f"{node.name()}: Iterator.{idx} POST Affine O -> already at its default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    
            elif self.kwargs["alt"]:
                if current["angle"].eval() != AFFINE_DEFAULTS.get("angle"):
                    check = False
                    # post affine
                    current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                    # Print to Houdini's status bar
                    _MSG = f"{node.name()}: Iterator.{idx} POST Affine Rotation Angle -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                if check:
                    _MSG = f"{node.name()}: Iterator.{idx} POST Affine Rotation Angle -> already at its default value."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
            else:
                for key in list(AFFINE_DEFAULTS.keys()):
                    if current[key].eval() != AFFINE_DEFAULTS[key]:
                        check = False
                        # post affine
                        current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                        current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                        current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                        current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                        # Print to Houdini's status bar
                        _MSG = f"{node.name()}: Iterator.{idx} POST Affine -> RESET"
                        flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                        break
                if check:
                    _MSG = f"{node.name()}: Iterator.{idx} POST Affine -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
        
        
    def reset_preaffine_FF(self) -> None:
        """Reset FF pre affine values to their defaults.
        """        
        node = self.node
        n = flam3h_iterator_prm_names
        check = True
        
        current = { "affine_x": node.parmTuple(f"{PRX_FF_PRM}{n.preaffine_x}"), "affine_y": node.parmTuple(f"{PRX_FF_PRM}{n.preaffine_y}"), "affine_o": node.parmTuple(f"{PRX_FF_PRM}{n.preaffine_o}"), "angle": node.parm(f"{PRX_FF_PRM}{n.preaffine_ang}") }

        if self.kwargs["shift"]:
            for key in list(AFFINE_DEFAULTS.keys())[:1]:
                if current[key].eval() != AFFINE_DEFAULTS[key]:
                    check = False
                    # pre affine
                    current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                    current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                    # Print to Houdini's status bar
                    _MSG = f"{node.name()}: FF PRE Affine X, Y -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    break
            if check:
                _MSG = f"{node.name()}: FF PRE Affine X, Y -> already at their default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')

        elif self.kwargs["ctrl"]:
            if current["affine_o"].eval() != AFFINE_DEFAULTS.get("affine_o"):
                check = False
                current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                # Print to Houdini's status bar
                _MSG = f"{node.name()}: FF PRE Affine O -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            if check:
                _MSG = f"{node.name()}: FF PRE Affine O -> already at its default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        elif self.kwargs["alt"]:
            if current["angle"].eval() != AFFINE_DEFAULTS.get("angle"):
                check = False
                current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                # Print to Houdini's status bar
                _MSG = f"{node.name()}: FF PRE Affine Rotation Angle -> RESET"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            if check:
                _MSG = f"{node.name()}: Iterator.{str(id)} FF PRE Affine Rotation Angle -> already at its default value."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
        else:
            for key in list(AFFINE_DEFAULTS.keys()):
                if current[key].eval() != AFFINE_DEFAULTS[key]:
                    check = False
                    # pre affine
                    current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                    current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                    current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                    current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                    # Print to Houdini's status bar
                    _MSG = f"{node.name()}: FF PRE Affine -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    break
            if check:
                _MSG = f"{node.name()}: FF PRE Affine -> already at their default values."
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')


    def reset_postaffine_FF(self) -> None:
        """Reset FF post affine values to their defaults.
        """        
        node = self.node
        n = flam3h_iterator_prm_names
        
        if node.parm(f"{PRX_FF_PRM}{n.postaffine_do}").eval(): # This can be omitted as the post affine tab wont be accessible if this toggle is off.
                
            check = True
            current = { "affine_x": node.parmTuple(f"{PRX_FF_PRM}{n.postaffine_x}"), "affine_y": node.parmTuple(f"{PRX_FF_PRM}{n.postaffine_y}"), "affine_o": node.parmTuple(f"{PRX_FF_PRM}{n.postaffine_o}"), "angle": node.parm(f"{PRX_FF_PRM}{n.postaffine_ang}") }
            
            if self.kwargs["shift"]:
                for key in list(AFFINE_DEFAULTS.keys())[:1]:
                    if current[key].eval() != AFFINE_DEFAULTS[key]:
                        check = False
                        # pre affine
                        current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                        current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                        # Print to Houdini's status bar
                        _MSG = f"{node.name()}: FF POST Affine X, Y -> RESET"
                        flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                        break
                if check:
                    _MSG = f"{node.name()}: FF POST Affine X, Y -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                    
            elif self.kwargs["ctrl"]:
                if current["affine_o"].eval() != AFFINE_DEFAULTS.get("affine_o"):
                    check = False
                    current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                    # Print to Houdini's status bar
                    _MSG = f"{node.name()}: FF POST Affine O -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                if check:
                    _MSG = f"{node.name()}: FF POST Affine O -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
            elif self.kwargs["alt"]:
                if current["angle"].eval() != AFFINE_DEFAULTS.get("angle"):
                    check = False
                    # post affine
                    current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                    # Print to Houdini's status bar
                    _MSG = f"{node.name()}: FF POST Affine Rotation Angle -> RESET"
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                if check:
                    _MSG = f"{node.name()}: FF POST Affine Rotation Angle -> already at their default value."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')

            else:
                for key in list(AFFINE_DEFAULTS.keys()):
                    if current[key].eval() != AFFINE_DEFAULTS[key]:
                        check = False
                        # post affine
                        current["affine_x"].set(AFFINE_DEFAULTS.get("affine_x"))
                        current["affine_y"].set(AFFINE_DEFAULTS.get("affine_y"))
                        current["affine_o"].set(AFFINE_DEFAULTS.get("affine_o"))
                        current["angle"].set(AFFINE_DEFAULTS.get("angle"))
                        # Print to Houdini's status bar
                        _MSG = f"{node.name()}: FF POST Affine -> RESET"
                        flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                        break
                if check:
                    _MSG = f"{node.name()}: FF POST Affine -> already at their default values."
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')


    def swap_iter_pre_vars(self) -> None:
        
        node = self.node
        id = self.kwargs['script_multiparm_index']
        idx = str(id)
        _MSG = f"{node.name()}.iterator.{idx} PRE variations -> SWAP"
        
        # Get prm names
        pvT = flam3h_iterator.sec_prevarsT
        pvW = flam3h_iterator.sec_prevarsW[1:]

        # Get values
        pvT_vals = (node.parm(f"{pvT[0]}{idx}").eval(), node.parm(f"{pvT[1]}{idx}").eval())
        pvW_vals = (node.parm(f"{pvW[0][0]}{idx}").eval(), node.parm(f"{pvW[1][0]}{idx}").eval())
        
        if self.kwargs["ctrl"]:
            # Swap types
            if pvT_vals[0] != pvT_vals[1]:
                node.setParms({f"{pvT[0]}{idx}": pvT_vals[1]})
                node.setParms({f"{pvT[1]}{idx}": pvT_vals[0]})
                
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
        else:
            # Swap types
            if pvT_vals[0] != pvT_vals[1]:
                node.setParms({f"{pvT[0]}{idx}": pvT_vals[1]})
                node.setParms({f"{pvT[1]}{idx}": pvT_vals[0]})
            
                # Swap weights
                if fsum(pvW_vals) > 0:
                    node.setParms({f"{pvW[0][0]}{idx}": pvW_vals[1]})
                    node.setParms({f"{pvW[1][0]}{idx}": pvW_vals[0]})
                
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            else:
                # Swap weights only
                if fsum(pvW_vals) > 0:
                    node.setParms({f"{pvW[0][0]}{idx}": pvW_vals[1]})
                    node.setParms({f"{pvW[1][0]}{idx}": pvW_vals[0]})
                    
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
                
    def swap_FF_post_vars(self) -> None:
        
        node = self.node
        _MSG = f"{node.name()} FF POST variations -> SWAP"
        
        # Get prm names
        pvT = flam3h_iterator_FF.sec_postvarsT_FF
        pvW = flam3h_iterator_FF.sec_postvarsW_FF

        # Get values
        pvT_vals = (node.parm(f"{pvT[0]}").eval(), node.parm(f"{pvT[1]}").eval())
        pvW_vals = (node.parm(f"{pvW[0][0]}").eval(), node.parm(f"{pvW[1][0]}").eval())
        
        if self.kwargs["ctrl"]:
            # Swap types
            if pvT_vals[0] != pvT_vals[1]:
                node.setParms({f"{pvT[0]}": pvT_vals[1]})
                node.setParms({f"{pvT[1]}": pvT_vals[0]})
                
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
        else:
            # Swap types
            if pvT_vals[0] != pvT_vals[1]:
                node.setParms({f"{pvT[0]}": pvT_vals[1]})
                node.setParms({f"{pvT[1]}": pvT_vals[0]})
            
                # Swap weights
                if fsum(pvW_vals) > 0:
                    node.setParms({f"{pvW[0][0]}": pvW_vals[1]})
                    node.setParms({f"{pvW[1][0]}": pvW_vals[0]})
                    
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
            else:
                # Swap weights only
                if fsum(pvW_vals) > 0:
                    node.setParms({f"{pvW[0][0]}": pvW_vals[1]})
                    node.setParms({f"{pvW[1][0]}": pvW_vals[0]})
                    
                    flam3h_general_utils.set_status_msg(_MSG, 'MSG')


    def reset_FF(self) -> None:
        """Reset the FLAM3H FF Tab parameters.
        """
        node = self.node

        n = flam3h_iterator_prm_names

        node.setParms({f"{PRX_FF_PRM}{n.main_note}": "iterator_FF"}) # type: ignore
        # FF pre
        node.setParms({f"{PRX_FF_PRM}{n.prevar_type_1}":  0}) # type: ignore 
        node.setParms({f"{PRX_FF_PRM}{n.prevar_weight_1}": 0}) # type: ignore
        # FF var
        node.setParms({f"{PRX_FF_PRM}{n.var_type_1}": 0}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.var_type_2}": 0}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.var_weight_1}": 1}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.var_weight_2}": 0}) # type: ignore
        # FF post
        node.setParms({f"{PRX_FF_PRM}{n.postvar_type_1}": 0}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.postvar_type_2}": 0}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.postvar_weight_1}": 0}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.postvar_weight_2}": 0}) # type: ignore
        # FF affine
        node.setParms({f"{PRX_FF_PRM}{n.preaffine_x}": hou.Vector2((1.0, 0.0))}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.preaffine_y}": hou.Vector2((0.0, 1.0))}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.preaffine_o}": hou.Vector2((0.0, 0.0))}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.preaffine_ang}": 0}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.postaffine_do}": 0}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.postaffine_x}": hou.Vector2((1.0, 0.0))}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.postaffine_y}": hou.Vector2((0.0, 1.0))}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.postaffine_o}": hou.Vector2((0.0, 0.0))}) # type: ignore
        node.setParms({f"{PRX_FF_PRM}{n.postaffine_ang}": 0}) # type: ignore



    def flam3h_default(self) -> None:
        """Sierpiński triangle parameters vaule.
        This is used to reset back FLAM3H node entire parameter template.
        
        Args:
            self:
        """
        
        node = self.node
        # Clear menu cache
        self.destroy_data(node, 'iter_sel')
        
        # Iterators reset
        in_flame_utils(self.kwargs).in_to_flam3h_reset_iterators_parms(node, 3)
        
        # update xaos
        self.auto_set_xaos()

        # resets Tab contexts
        self.reset_FF()
        flam3h_general_utils(self.kwargs).reset_SYS(1, FLAM3H_DEFAULT_GLB_ITERATIONS, 1)
        flam3h_palette_utils(self.kwargs).reset_CP()
        flam3h_general_utils(self.kwargs).reset_MB()
        in_flame_utils(self.kwargs).reset_IN()
        out_flame_utils(self.kwargs).reset_OUT(1) # dnt clear the MSG_OUT if any
        flam3h_general_utils(self.kwargs).reset_PREFS()
        
        # Clear up stats if there already ( due to be stored into a houdini preset also, just in case... )
        node.setParms({MSG_FLAMESTATS: ""})
        node.setParms({MSG_FLAMERENDER: ""})
        node.setParms({MSG_FLAMESENSOR: ""})
        # node.setParms({MSG_PALETTE: ''})
        # node.setParms({MSG_OUT: ''})
        node.setParms({GLB_DENSITY: FLAM3H_DEFAULT_GLB_DENSITY}) # type: ignore
        
        # Sierpiński triangle settings
        self.sierpinski_settings(node)
        
        # init/clear copy/paste iterator's data and prm if needed.
        self.flam3h_paste_reset_hou_session_data()
        
        # If the node has its display flag ON
        if node.isGenericFlagSet(hou.nodeFlag.Display): # type: ignore
            # Print to Houdini's status bar
            _MSG = f"{node.name()}: LOAD Flame preset: \"Sierpiński triangle\" -> Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Flame LOAD -> Sierpiński triangle")
            
            
    def flam3h_reset_iterator(self) -> None:
        
        node = self.node
        id = self.kwargs['script_multiparm_index']
        idx = str(id)
        
        # iterator prm names
        n = flam3h_iterator_prm_names
        
        # iter 1
        #
        # main
        node.setParms({f"{n.main_note}_{idx}": f"iterator_{idx}"}) # type: ignore
        node.setParms({f"{n.main_weight}_{idx}": 0.5}) # type: ignore
        # shader
        node.setParms({f"{n.shader_color}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.shader_speed}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.shader_alpha}_{idx}": 1.0}) # type: ignore
        # vars
        node.setParms({f"{n.prevar_blur}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.prevar_weight_blur}_{idx}": 0.0}) # type: ignore
        node.setParms({f"{n.prevar_type_1}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.prevar_weight_1}_{idx}": 0.0}) # type: ignore
        node.setParms({f"{n.prevar_type_2}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.prevar_weight_2}_{idx}": 0.0}) # type: ignore
        node.setParms({f"{n.var_type_1}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.var_weight_1}_{idx}": 1.0}) # type: ignore
        node.setParms({f"{n.var_type_2}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.var_weight_2}_{idx}": 0.0}) # type: ignore
        node.setParms({f"{n.var_type_3}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.var_weight_3}_{idx}": 0.0}) # type: ignore
        node.setParms({f"{n.var_type_4}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.var_weight_4}_{idx}": 0.0}) # type: ignore
        node.setParms({f"{n.postvar_type_1}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.postvar_weight_1}_{idx}": 0.0}) # type: ignore
        # pre affine
        node.setParms({f"{n.preaffine_x}_{idx}": AFFINE_DEFAULTS.get("affine_x")}) # type: ignore
        node.setParms({f"{n.preaffine_y}_{idx}": AFFINE_DEFAULTS.get("affine_y")}) # type: ignore
        node.setParms({f"{n.preaffine_o}_{idx}": AFFINE_DEFAULTS.get("affine_o")}) # type: ignore
        node.setParms({f"{n.preaffine_ang}_{idx}": AFFINE_DEFAULTS.get("angle")}) # type: ignore
        # post affine
        node.setParms({f"{n.postaffine_do}_{idx}": 0}) # type: ignore
        node.setParms({f"{n.postaffine_x}_{idx}": AFFINE_DEFAULTS.get("affine_x")}) # type: ignore
        node.setParms({f"{n.postaffine_y}_{idx}": AFFINE_DEFAULTS.get("affine_y")}) # type: ignore
        node.setParms({f"{n.postaffine_o}_{idx}": AFFINE_DEFAULTS.get("affine_o")}) # type: ignore
        node.setParms({f"{n.postaffine_ang}_{idx}": AFFINE_DEFAULTS.get("angle")}) # type: ignore
        


    def auto_set_xaos(self) -> None:
        """Set iterator's xaos values every time an iterator is added or removed.

        Args:
            self: 
        """

        node = self.node
        
        iter_num = node.parm(FLAME_ITERATORS_COUNT).evalAsInt()
        
        autodiv = node.parm(PREFS_XAOS_AUTO_SPACE).evalAsInt()
        div_xaos = 'xaos:'
        div_weight = ':'
        if autodiv:
            div_xaos = 'xaos :'
            div_weight = ' :'
        
        # unlock
        node.parm(FLAM3H_DATA_PRM_MPIDX).lock(False)
        
        # init indexes
        idx_del_inbetween = None
        idx_add_inbetween = None
        
        mpmem = []
        mpmem_hou_get = []
        xaos_str_hou_get = []
        
        # get mpmem parms now
        prm_mp_mem = flam3h_iterator_prm_names.main_mpmem
        [mpmem.append(int(node.parm(f"{prm_mp_mem}_{str(mp_idx+1)}").eval())) for mp_idx in range(iter_num)]
        
        # get mpmem from CachedUserData
        __mpmem_hou_get = self.auto_set_xaos_data_get_MP_MEM(node)
        if __mpmem_hou_get is None:
            mpmem_hou_get = mpmem
        else:
            mpmem_hou_get = list(__mpmem_hou_get)
        
        # collect all xaos
        val = out_flame_utils.out_xaos_collect(node, iter_num, flam3h_iterator_prm_names.xaos)
        # fill missing weights if any
        fill_all_xaos = [np_pad(item, (0, iter_num-len(item)), 'constant', constant_values=1).tolist() for item in val]
        
        # convert all xaos into array of strings
        xaos_str = []
        for xaos in fill_all_xaos:
            collect = [str(item) for item in xaos]
            xaos_str.append(collect)
            
        # get xaos from CachedUserData
        __xaos_str_hou_get = self.auto_set_xaos_data_get_XAOS_PREV(node)
        if __xaos_str_hou_get is None:
            xaos_str_hou_get = xaos_str
        else:
            xaos_str_hou_get = list(__xaos_str_hou_get)
            
        # DEL: INBETWEEN get index: try
        s_current = set(mpmem)
        s_history = set(mpmem_hou_get)
        _idx = list(set(s_history - s_current))
        if _idx: idx_del_inbetween = int(_idx[0]) - 1
        # ADD: INBETWEEN get index : try
        for mp in range(iter_num-1):
            if mpmem[mp] == mpmem[mp + 1]:
                idx_add_inbetween = mp
                break
        
        # DEL -> ONLY LAST ITERATOR
        if idx_del_inbetween is not None and idx_del_inbetween == iter_num:
            
            # Clear menu cache
            self.destroy_data(node, 'iter_sel')

            # updated CachedUserData: flam3h_xaos_iterators_prev
            self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_str)
            
            # Update copy/paste iterator's index if there is a need to do so
            flam3h_node_mp_id = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
            
            if flam3h_node_mp_id is not None:
                # Check if the node still exist
                try:
                    hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                    flam3h_node = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
                except:
                    flam3h_node_mp_id = None
                    flam3h_node = None
                    
                # If the node exist
                if flam3h_node_mp_id is not None and node == flam3h_node:
                        
                    if (idx_del_inbetween+1) == flam3h_node_mp_id: # just in case..
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = None # type: ignore
                        # set
                        node.setParms({FLAM3H_DATA_PRM_MPIDX: -1})
                        self.del_comment_and_user_data_iterator(node)
                        # Let us know
                        _MSG = f"{node.name()}: The iterator you just removed was marked for being copied -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        
                    else:
                        pass
        
        # DEL
        elif idx_del_inbetween is not None and idx_del_inbetween < iter_num:
            
            # Clear menu cache
            self.destroy_data(node, 'iter_sel')

            xaos_str = xaos_str_hou_get
            del xaos_str[idx_del_inbetween]
            for x in xaos_str:
                del x[idx_del_inbetween]

            # updated CachedUserData: flam3h_xaos_iterators_prev
            self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_str)
            
            # Update copy/paste iterator's index if there is a need to do so
            flam3h_node_mp_id = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
            if flam3h_node_mp_id is not None:
                # Check if the node still exist
                try:
                    hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                    flam3h_node = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
                except:
                    flam3h_node_mp_id = None
                    flam3h_node = None
                    
                # If the node exist and if it is the selected one
                if flam3h_node_mp_id is not None and node == flam3h_node:
                        
                    if (idx_del_inbetween+1) < flam3h_node_mp_id:
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = flam3h_node_mp_id - 1 # type: ignore
                        # set
                        idx_new = node.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt() - 1
                        node.setParms({FLAM3H_DATA_PRM_MPIDX: idx_new})
                        self.del_comment_and_user_data_iterator(node)
                        self.set_comment_and_user_data_iterator(node, str(idx_new))

                    elif (idx_del_inbetween+1) == flam3h_node_mp_id:
                        
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = None # type: ignore
                        # set
                        node.setParms({FLAM3H_DATA_PRM_MPIDX: -1})
                        self.del_comment_and_user_data_iterator(node)
                        # Let us know
                        _MSG = f"{node.name()}: The iterator you just removed was marked for being copied -> {MARK_ITER_MSG_STATUS_BAR}"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        
                    else:
                        pass

        # otherwise ADD
        # If it is true that an iterator has been added in between ( 'idx_add_inbetween' not 'None' ) lets add the new weight at index
        elif idx_add_inbetween is not None:
            
            # Clear menu cache
            self.destroy_data(node, 'iter_sel')

            for xidx, x in enumerate(xaos_str):
                if xidx != idx_add_inbetween:
                    x.insert(idx_add_inbetween, '1.0')
                    # x already had the new iterator weight added to the end of it
                    # so lets remove the last element as it is not longer needed
                    del x[-1]
                    
            # updated CachedUserData: flam3h_xaos_iterators_prev
            self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_str)
            
            # Update copy/paste iterator's index if there is a need to do so
            flam3h_node_mp_id = hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX # type: ignore
            
            if flam3h_node_mp_id is not None:
                # Check if the node still exist
                try:
                    hou.session.FLAM3H_MARKED_ITERATOR_NODE.type() # type: ignore
                    flam3h_node = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
                except:
                    flam3h_node_mp_id = None
                    flam3h_node = None
                    
                # If the node exist and if it is the selected one
                if flam3h_node_mp_id is not None and node == flam3h_node:
                        
                    if (idx_add_inbetween+1) <= flam3h_node_mp_id:
                        hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = flam3h_node_mp_id + 1 # type: ignore
                        # set
                        idx_new = node.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt() + 1
                        node.setParms({FLAM3H_DATA_PRM_MPIDX: idx_new})
                        self.del_comment_and_user_data_iterator(node)
                        self.set_comment_and_user_data_iterator(node, str(idx_new))
                        
                    else:
                        pass
            
        else:
            # updated CachedUserData: flam3h_xaos_iterators_prev
            self.auto_set_xaos_data_set_XAOS_PREV(node, xaos_str)
            
        # set all multi parms xaos strings parms
        xaos_str_round_floats = tuple([div_weight.join(x) for x in out_flame_utils.out_util_round_floats(xaos_str)])
        prm_xaos = flam3h_iterator_prm_names.xaos
        [node.setParms({f"{prm_xaos}_{str(mp_idx+1)}": (div_xaos + xaos)}) for mp_idx, xaos in enumerate(xaos_str_round_floats)]
            
        # lock
        node.parm(FLAM3H_DATA_PRM_XAOS_PREV).lock(True)
            
        # reset iterator's mpmem prm
        [node.setParms({f"{prm_mp_mem}_{str(mp_idx+1)}": str(mp_idx+1)}) for mp_idx in range(iter_num)] # type: ignore
        # update flam3h_xaos_mpmem
        __mpmem_hou = [int(node.parm(f"{prm_mp_mem}_{str(mp_idx+1)}").eval()) for mp_idx in range(iter_num)]
        
        # export mpmem into CachedUserData
        self.auto_set_xaos_data_set_MP_MEM(node, __mpmem_hou)
        # lock
        node.parm(FLAM3H_DATA_PRM_MPIDX).lock(True)


    def iterators_count(self) -> None:
        """Every time an iterator is added or remove
        this will run and execute based on iterator's number: Zero or more then Zero.
        Args:
            self:
        """

        _MSG_str = "Iterators count set to Zero. Add at least one iterator or load a valid IN flame file"

        node = self.node
        # Clear menu cache
        self.destroy_data(node, 'iter_sel')
        
        iterators_count = node.parm(FLAME_ITERATORS_COUNT).evalAsInt()
        
        if not iterators_count:
            
            # delete channel references
            [p.deleteAllKeyframes() for p in node.parms() if not p.isLocked()]
                
            # GLOBAL
            node.setParms({GLB_DENSITY: FLAM3H_DEFAULT_GLB_DENSITY}) # type: ignore
            node.setParms({GLB_ITERATIONS: FLAM3H_DEFAULT_GLB_ITERATIONS}) # type: ignore
            # SYS
            node.setParms({SYS_DO_FF: 0}) # type: ignore
            node.setParms({SYS_RIP: 0}) # type: ignore
            # FF vars
            self.reset_FF()
            # MB
            flam3h_general_utils(self.kwargs).reset_MB()
            # IN
            node.setParms({IN_ISVALID_PRESET: 0})
            node.setParms({IN_CLIPBOARD_TOGGLE: 0})
            # prefs
            node.setParms({PREFS_TOGGLE: 1}) # type: ignore
            node.setParms({PREFS_CAMERA_HANDLE: 0}) # type: ignore
            node.setParms({PREFS_CAMERA_CULL: 0}) # type: ignore

            # descriptive message parameter
            node.setParms({MSG_DESCRIPTIVE_PRM: ""}) # type: ignore
            
            # init/clear copy/paste iterator's data and prm
            self.flam3h_paste_reset_hou_session_data()
            
            # Print to Houdini's status bar
            _MSG = f"{node.name()}: {_MSG_str}"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Iterators count ZERO")
            
        else:
            
            # set xaos every time an iterator is added or removed
            self.auto_set_xaos()
            
            # Clear status bar msg if needed
            if  _MSG_str in hou.ui.statusMessage()[0]: # type: ignore
                flam3h_general_utils.set_status_msg('', 'MSG')
                
        # If OUT Camera sensor viz mode is ON.
        if node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt():
            # We can avoid to set the clipping planes as they are already set
            flam3h_general_utils(self.kwargs).util_set_front_viewer()


    def iterator_keep_last_vactive(self) -> None:
        """While it is possible to delete all iterators,
        we must always have at least one active iterator, if at least one iterator is present and its weight above Zero.
        This will prevent the last active iterator to being disabled.
        
        _NOTE:
            The parameters names are hard coded here to try to speed up even if a tiny bit.
            If class flam3h_iterator_prm_names: is updated, need to be updated here too.
        """    
        
        node = self.node
        # Clear menu cache
        self.destroy_data(node, 'iter_sel')
        
        iter_num = node.parm(FLAME_ITERATORS_COUNT).evalAsInt()
        
        # The following will collect the active iterator bool value if and only if the iterator is active and its weight is above zero.
        # What it is going to happen is that by the time we try to disable the last active iterator, it wont collect anything becasue
        # by the time we click to disable the last iterator they will all be disabled for a moment, just right before we switch this last one back to being enabled.
        # Hence the case we are interested in is when the va: list variable is empty, thats how we know we tried to switch the last active iterator OFF.
        va = [int(node.parm(f"vactive_{str(mp_idx+1)}").eval()) 
             for mp_idx in range(iter_num) 
                if node.parm(f"vactive_{str(mp_idx+1)}").eval() 
                and node.parm(f"iw_{str(mp_idx+1)}").eval() > 0]

        # If this va: list variable is empty, mean we switched the last active irterator to OFF so lets do something about it.
        if not va:
            id = self.kwargs['script_multiparm_index']
            node.setParms({f"vactive_{str(id)}": 1})
            _MSG = f"{node.name()}: iterator {str(id)} reverted back to being Active. There must always be at least one active iterator."
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"iterator {str(id)} -> back to being Active")


    def iterator_keep_last_vactive_STAR(self) -> None:
        """This is the actual definition that run in a callback script.
        It will prevent the lasct active iterator to be turned OFF.
        
        _NOTE:
            The parameters names is hard coded here to try to speed up even if a tiny bit.
            If class flam3h_iterator_prm_names: is updated, need to be updated here too.
        """        
        id = self.kwargs['script_multiparm_index']
        vactive_prm_name = f"vactive_{str(id)}"
        flam3h_general_utils(self.kwargs).flam3h_toggle(vactive_prm_name)
        self.iterator_keep_last_vactive()


    def iterator_keep_last_weight(self) -> None:
        """While it is possible to delete all iterators,
        we must always have at least one iterator's weight above Zero, if at least one iterator is present or active.
        This will prevent to set the last active iterator's Weight to be Zero.
        
        _NOTE:
            The parameters names is hard coded here to try to speed up even if a tiny bit.
            If class flam3h_iterator_prm_names: is updated, need to be updated here too.
        """  
        node = self.node
        # Clear menu cache
        self.destroy_data(node, 'iter_sel')
        
        iter_num = node.parm(FLAME_ITERATORS_COUNT).evalAsInt()
        W = [int(node.parm(f"iw_{str(mp_idx+1)}").eval()) 
            for mp_idx in range(iter_num) 
                if node.parm(f"iw_{str(mp_idx+1)}").eval() == 0 
                and int(node.parm(f"vactive_{str(mp_idx+1)}").eval())]
        
        vactive_iters = [int(node.parm(f"vactive_{str(mp_idx+1)}").eval()) 
                        for mp_idx in range(iter_num) 
                            if node.parm(f"vactive_{str(mp_idx+1)}").eval()]
        
        if len(W) == len(vactive_iters):
            min_weight = 0.00000001
            id = self.kwargs['script_multiparm_index']
            node.setParms({f"iw_{str(id)}": min_weight})
            _MSG = f"{node.name()}: iterator {str(id)}'s Weight reverted back to a value of: {min_weight} instead of Zero. There must always be at least one active iterator's weight above Zero."
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"iterator {str(id)} Weight -> back to being NON-ZERO")







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

STATIC METHODS:

build_ramp_palette_default(ramp_parm: hou.Parm) -> None:

build_ramp_palette_temp(ramp_tmp_parm: hou.Parm) -> None:

build_ramp_palette_error() -> tuple[list, list, list]

delete_ramp_all_keyframes(ramp_parm: hou.Parm) -> None:

get_ramp_keys_count(ramp: hou.Ramp) -> str:

isJSON_F3H_get_first_preset(filepath: Union[str, bool]) -> Union[str, bool]:

isJSON_F3H(node: hou.SopNode, filepath: Union[str, bool],  msg=True, parm_path_name=CP_PALETTE_LIB_PATH) -> tuple[bool, bool]:

rgb_to_hex(rgb: tuple) -> str:

hex_to_rgb(hex: str) -> tuple:

find_nearest_idx(array: Union[list, tuple], value: Union[int, float]) -> Union[int, float]:

json_to_flam3h_palette_plus_MSG(node: hou.SopNode, HEXs: list, mode=False) -> None:

json_to_flam3h_palette_plus_preset_MSG(node: hou.SopNode, _MSG: str) -> None:

METHODS:

menu_ramp_presets_data(self) -> list:

menu_ramp_presets(self) -> list:

menu_ramp_presets_empty_data(self) -> list:

menu_ramp_presets_empty(self) -> list:

flam3h_ramp_save_JSON_DATA(self) -> tuple[dict, str]:

flam3h_ramp_save(self) -> None:

json_to_flam3h_ramp_initialize(self, rgb_from_XML_PALETTE: list) -> hou.Ramp:

json_to_flam3h_ramp_set_HSV(self, node, hsv_check: bool, hsv_vals: list) -> None:

json_to_flam3h_ramp_SET_PRESET_DATA(self) -> None:

json_to_flam3h_ramp_sys(self, use_kwargs=True) -> None:

json_to_flam3h_ramp(self, use_kwargs=True) -> None:

palette_cp(self) -> None:

palette_cp_to_tmp(self) -> None:

palette_hsv(self) -> None:

palette_lock(self) -> None:

reset_CP_LOCK_MSG(self) -> None:

reset_CP_TMP(self) -> None:

reset_CP_options(self) -> None:

reset_CP_run_0(self) -> None:

reset_CP_run_2(self) -> None:

reset_CP_run_3(self) -> None:

reset_CP(self, mode=0) -> None:
    """
    
    def __init__(self, kwargs: dict) -> None:
        self._kwargs = kwargs
        self._node = kwargs['node']
        self._palette_plus_do = self._node.parm(CP_RAMP_SAVE_256_PLUS).eval()
        
        
    @staticmethod
    def build_ramp_palette_default(ramp_parm: hou.Parm) -> None:
        cp_def_bases = [hou.rampBasis.Linear] * 4 # type: ignore
        cp_def_keys = [0.0, 0.25, 0.5, 0.75, 1.0]
        cp_def_values = [(0.2, 0.05, 1), (0.1, 0.85 , 1), (0.05, 1, 0.1), (0.95, 1, 0.1), (1, 0.05, 0.05)]
        ramp_parm.set(hou.Ramp(cp_def_bases, cp_def_keys, cp_def_values)) # type: ignore
        
        
    @staticmethod
    def build_ramp_palette_temp(ramp_tmp_parm: hou.Parm) -> None:
        cp_tmp_bases = [hou.rampBasis.Linear] * 2  # type: ignore
        cp_tmp_keys = [0.0, 1.0]
        cp_tmp_values = [(0.9989989989989989987654, 0, 0), (0.9989989989989989987654, 0 , 0)]
        ramp_tmp_parm.set(hou.Ramp(cp_tmp_bases, cp_tmp_keys, cp_tmp_values)) # type: ignore
        
        
    @staticmethod
    def build_ramp_palette_error() -> tuple[list, list, list]:
        return [(1,0,0)], [0], [hou.rampBasis.Linear] # type: ignore
    
    
    @staticmethod
    def delete_ramp_all_keyframes(ramp_parm: hou.Parm) -> None:
        posList = ramp_parm.evalAsRamp().keys()
        [hou.parm(f"{ramp_parm.path()}{str(i+1)}pos").deleteAllKeyframes() for i in range(0, len(posList))]
        [hou.parmTuple(f"{ramp_parm.path()}{str(i+1)}c").deleteAllKeyframes() for i in range(0, len(posList))]

        

    @staticmethod 
    def get_ramp_keys_count(ramp: hou.Ramp) -> str:
        """Based on how many color keys are present in the provided ramp,
        select a palette colors/keys count preset to use for better resample it.
        
        _NOTE:
            This need to be revised and smartened up a little as there may be cases where it will fail
            to sample the palette enough to collect the proper colors based on their location and proxymity to each other in the ramp.

        Args:
            ramp (hou.Ramp): The current ramp being considered.

        Returns:
            str: a palette colors/keys count string preset.
        """        
        keys_count = len(ramp.keys())
        if keys_count <= 32:
            return PALETTE_COUNT_64
        elif keys_count == 64:
            return PALETTE_COUNT_64
        elif keys_count <= 128:
            return PALETTE_COUNT_128
        elif keys_count <= 256:
            return PALETTE_COUNT_256
        else:
            _MSG = f'{str(hou.pwd())}: Colors: {str(keys_count)}: to many colors and will default back to the standard 256 color keys for this palette.'
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            print(_MSG)
            return PALETTE_COUNT_256
        
        
    @staticmethod
    def isJSON_F3H_get_first_preset(filepath: Union[str, bool]) -> Union[str, bool]:
        """Try to get the first palette preset of a JSON FLAM3H palette file.

        Args:
            filepath (Union[str, bool]): The JSON FLAM3H Palette file path

        Returns:
            Union[str, bool]: The preset name, or False if not.
        """        
        try:
            # get presets if any
            with open(filepath, 'r') as r:
                data = json.load(r)
            # get the first preset of them all
            return list(data.keys())[0]
        except:
            return False



    @staticmethod
    def isJSON_F3H(node: hou.SopNode, filepath: Union[str, bool],  msg=True, parm_path_name=CP_PALETTE_LIB_PATH) -> tuple[bool, bool]:
        """Check if the loaded palette lib file is a valid FLAM3H palette json file.

        Args:
            node (hou.SopNode): current FLAM3H node
            filepath (Union[str, bool]): Palette lib full file path.
            msg (bool): Default to True, print out messages to the Houdini's status bar. Set it to False to not print out messages.
            parm_path_name (str): Default to global: CP_PALETTE_LIB_PATH. The actual Houdini's palette file parameter name.

        Returns:
            bool: True if valid. False if not valid.
        """      
        if filepath is not False:
            
            preset = flam3h_palette_utils.isJSON_F3H_get_first_preset(filepath)
            if preset is not False:
                # If we made it this far, mean we loaded a valid JSON file,
                # lets now check if the preset is actually a FLAM3H Palette preset.
                with open(filepath, 'r') as r:
                    data = json.load(r)[preset]
                    # This is the moment of the truth ;)
                    try:
                        hex_values = data[CP_JSON_KEY_NAME_HEX]
                    except:
                        if msg:
                            _MSG = f"{node.name()}: Palette JSON load -> Although the JSON file you loaded is legitimate, it does not contain any valid FLAM3H Palette data."
                            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                            flam3h_general_utils.flash_message(node, f"Palette LOAD -> Not a valid FLAM3H JSON palette file")
                        del data
                        return True, False
                    
                    # Validate the file path setting it
                    node.setParms({parm_path_name: filepath}) #type: ignore
                    sm = hou.ui.statusMessage() # type: ignore
                    if sm[0] and msg:
                        flam3h_general_utils.set_status_msg('', 'MSG')
                    del data
                    return True, True
            else:
                flam3h_general_utils.set_status_msg('', 'MSG')
                return False, False
        else:
            flam3h_general_utils.set_status_msg('', 'MSG')
            return False, False
        
        
    @staticmethod
    def rgb_to_hex(rgb: tuple) -> str:
        """Convert a RGB color value into HEX color value.

        Args:
            rgb (tuple): the RGB color value to convert.

        Returns:
            str: HEX color value
        """        
        vals = [flam3h_general_utils.clamp(255*x) for x in rgb]
        hex = ''.join(['{:02X}'.format(int(round(x))) for x in vals])
        return hex


    @staticmethod
    def hex_to_rgb(hex: str) -> tuple:
        """Convert a HEX color value into RGB color value.

        Args:
            rgb (tuple): the HEX color value to convert.

        Returns:
            tuple: RGB color value
        """   
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    
    
    @staticmethod
    def find_nearest_idx(array: Union[list, tuple], value: Union[int, float]) -> Union[int, float]:
        """Given a value, find the closest value in the array that is bigger than the value passed in.
        Args:
            array (list, tuple): the array of values to search into.
            value: (int, float): The value to use to find its closest and bigger value into the array.

        Returns:
            int, float: the closest value in the array that is bigger than the value passed in.
        """   
        idx = np_searchsorted(array, value, side="left")
        return array[idx]
    
    
    @staticmethod
    def json_to_flam3h_palette_plus_MSG(node: hou.SopNode, HEXs: list, mode=False) -> None:
        """Given a value, find the closest value in the array that is bigger than the value passed in.
        I am using a manual f-string build here. Probably dynamically build a list would be better but if i'll need to add more strings i'll look into it.
        
        Args:
            node (hou.SopNode): The current FLAM3H node.
            HEXs (list): The array/list of hex colors.
                         In case of: palette_cp(self) definition -> this argument will be the number of the (source)palette color keys 
                                                                    and it is used only to check if we need to update the palette message while editing it.
            mode (bool): (default to False) For now True only to use inside: palette_cp(self) -> None:

        Returns:
            None: 
        """  
        palette_msg: str = node.parm(MSG_PALETTE).evalAsString()
        if len(HEXs) > 256:
            if PALETTE_PLUS_MSG in palette_msg:
                pass
            else:
                node.setParms({MSG_PALETTE: f"{PALETTE_PLUS_MSG.strip()} {palette_msg.strip()}"}) # type: ignore
        else:
            if PALETTE_PLUS_MSG in palette_msg:
                node.setParms({MSG_PALETTE: f"{palette_msg[len(PALETTE_PLUS_MSG.strip()):]}"}) # type: ignore
            else:
                if not mode:
                    pass
                else:
                    # I do not remember why I am doing this else statement
                    # ...I leave it here for now as there must be a reason for this to exist ;)
                    #
                    # I think it was becasue from inside the palette_cp(self) definition we are constantly checking
                    # if the current number of color keys are greater than 256 and adjust the palette msg on the fly.
                    flam3h_palette_utils.json_to_flam3h_palette_plus_preset_MSG(node, palette_msg)
                
    
    
    @staticmethod 
    def json_to_flam3h_palette_plus_preset_MSG(node: hou.SopNode, _MSG: str) -> None:
        """Check is the plaette plus str "[256+]" is displayed already and add a custom string message(_MSG) to it.
        This is used inside: flam3h_init_presets_CP_PALETTE_PRESETS(self, mode=1) and its run everytime we load a palette file while the presets menu is being initialized.
        
        Args:
            node (hou.SopNode): The current FLAM3H node.
            _MSG (str): The message to add
            
        Returns:
            None: 
        """  
        
        palette_msg = node.parm(MSG_PALETTE).evalAsString()
        if PALETTE_PLUS_MSG in palette_msg:
            node.setParms({MSG_PALETTE: f"{PALETTE_PLUS_MSG.strip()} {_MSG.strip()}"}) # type: ignore
        else:
            node.setParms({MSG_PALETTE: f"{_MSG}"}) # type: ignore
        




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



    def menu_ramp_presets_data(self) -> list:
        """Build the palette preset parameter menu entries based on the loaded json palette lib file.
        When a palette preset is currently loaded. This will use the color star icon to signal wich preset is being loaded.

        Returns:
            list: _description_
        """
        node = self.node
        menu=[]
        if node.parm(CP_ISVALID_FILE).eval() and self.node.parm(CP_ISVALID_PRESET).eval():
            
            filepath = os.path.expandvars(node.parm(CP_PALETTE_LIB_PATH).evalAsString())
            if os.path.isfile(filepath):
                
                with open(filepath) as f:
                    menuitems = json.load(f).keys()

                if node.parm(PREFS_ENUMERATE_MENU).eval():
                    
                    for i, item in enumerate(menuitems):
                        
                        menu.append(str(i))
                        
                        # ICON tag
                        if i == int(node.parm(CP_PALETTE_PRESETS).eval()):
                            node.setCachedUserData('cp_presets_menu_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_PALETTE_LOAD}  {str(i)}:  {item}     ") # 5 ending \s to be able to read the full label
                        else:
                            menu.append(f"{str(i)}:  {item}")

                else:
                    
                    for i, item in enumerate(menuitems):
                        
                        menu.append(str(i))
                        
                        # ICON tag
                        if i == int(node.parm(CP_PALETTE_PRESETS).eval()):
                            node.setCachedUserData('cp_presets_menu_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_PALETTE_LOAD}  {item}     ") # 5 ending \s to be able to read the full label
                        else:
                            menu.append(f"{item}")
                            
                node.setCachedUserData('cp_presets_menu', menu)
                return menu

        flam3h_iterator_utils.destroy_data(node, 'cp_presets_menu')
        return MENU_PRESETS_EMPTY
    
    
    def menu_ramp_presets(self) -> list:
        node = self.node
        data = node.cachedUserData('cp_presets_menu')
        data_idx = node.cachedUserData('cp_presets_menu_idx')
        preset_idx = node.parm(CP_PALETTE_PRESETS).eval()
        if data is not None and data_idx == preset_idx:
            return data
        else:
            return self.menu_ramp_presets_data()
    

    def menu_ramp_presets_empty_data(self) -> list:
        """Build the palette preset parameter menu entries based on the loaded json palette lib file.
        When no palette preset has been loaded. This will use the empty star icon to signal wich preset is being selected but not loaded.

        This definition exist only becasue if I change the icon dynamically inside: def menu_ramp_presets(self) -> list:
        Houdini not updated them until I dnt execute a "next" selection in the menu parameter.

        Returns:
            list: _description_
        """
        node = self.node
        menu=[]
        if node.parm(CP_ISVALID_FILE).eval() and not node.parm(CP_ISVALID_PRESET).eval():
            
            filepath = os.path.expandvars(self.node.parm(CP_PALETTE_LIB_PATH).evalAsString())
            if os.path.isfile(filepath):
                
                with open(filepath) as f:
                    menuitems = json.load(f).keys()

                if node.parm(PREFS_ENUMERATE_MENU).eval():
                    
                    for i, item in enumerate(menuitems):
                        
                        menu.append(i)
                        
                        # ICON tag
                        if i == int(node.parm(CP_PALETTE_PRESETS_OFF).eval()):
                            node.setCachedUserData('cp_presets_menu_off_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_PALETTE_LOAD_EMPTY}  {str(i)}:  {item}     ") # 5 ending \s to be able to read the full label
                        else:
                            menu.append(f"{str(i)}:  {item}")
                            
                else:
                    
                    for i, item in enumerate(menuitems):
                        
                        menu.append(i)
                        
                        # ICON tag
                        if i == int(node.parm(CP_PALETTE_PRESETS_OFF).eval()):
                            node.setCachedUserData('cp_presets_menu_off_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_PALETTE_LOAD_EMPTY}  {item}     ") # 5 ending \s to be able to read the full label
                        else:
                            menu.append(f"{item}")
                
                node.setCachedUserData('cp_presets_menu_off', menu)
                return menu
            
        flam3h_iterator_utils.destroy_data(node, 'cp_presets_menu_off')
        return MENU_PRESETS_EMPTY
    
    
    def menu_ramp_presets_empty(self) -> list:
        node = self.node
        data = node.cachedUserData('cp_presets_menu_off')
        data_idx = node.cachedUserData('cp_presets_menu_off_idx')
        preset_idx = node.parm(CP_PALETTE_PRESETS_OFF).eval()
        if data is not None and data_idx == preset_idx:
            return data
        else:
            return self.menu_ramp_presets_empty_data()



    def flam3h_ramp_save_JSON_DATA(self) -> tuple[dict, str]:
        """Build palette data to save out into a *.json file

        Returns:
            tuple (dict, str): (dict): Raw json data dictionary. (str): indented json data as string
        """
        node = self.node
        # get user's preset name or build an automated one
        presetname = str(node.parm(CP_PALETTE_OUT_PRESET_NAME).eval()).strip()
        if not presetname:
            presetname = datetime.now().strftime("Palette_%b-%d-%Y_%H%M%S")

        # Updated HSV ramp before getting it
        self.palette_cp()

        hsv_vals = []
        hsv_vals_prm = node.parmTuple(CP_RAMP_HSV_VAL_NAME).eval()
        if node.parm(CP_RAMP_SAVE_HSV).eval():
            palette = node.parm(CP_RAMP_HSV_NAME).evalAsRamp()
            hsv_vals_prm = [1.0, 1.0, 1.0]
        else:
            palette =  node.parm(CP_RAMP_SRC_NAME).evalAsRamp()
            
        keys_count = out_flame_utils(self.kwargs).out_palette_keys_count(self.palette_plus_do, len(palette.keys()), 1, False)
        POSs = list(iter_islice(iter_count(0, 1.0/(int(keys_count)-1)), int(keys_count)))
        HEXs = [self.rgb_to_hex(palette.lookup(p)) for p in POSs]
        
        if hsv_vals_prm[0] == hsv_vals_prm[1] == hsv_vals_prm[2] == 1:
            json_dict = { presetname: {CP_JSON_KEY_NAME_HEX: ''.join(HEXs),  } }
        else:
            hsv_vals = ' '.join([str(x) for x in hsv_vals_prm])
            json_dict = { presetname: {CP_JSON_KEY_NAME_HEX: ''.join(HEXs), CP_JSON_KEY_NAME_HSV: hsv_vals} }
            
        # OUTPUT DATA
        return json_dict, json.dumps(json_dict, indent=4)



    def flam3h_ramp_save(self) -> None:
        """Save the current color palette into a json file.
        This wil also save the HSV values along with it.
        
        There is also the option to save the HSV palette instead but be cautious
        as when saving the HSV palette, its colors will be clamped. [0-255]
        """
        
        # ALT - Copy palette to the clipboard
        if self.kwargs['alt']:
            node =  self.node
            json_dict, json_data = self.flam3h_ramp_save_JSON_DATA()
            hou.ui.copyTextToClipboard(json_data) # type: ignore
            # Clear up palette preset name if any
            node.setParms({CP_PALETTE_OUT_PRESET_NAME: ''})
            # Satus message
            _MSG = f"{node.name()}: SAVE Palette Clipboard. Palette copied to the clipboard -> Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Palette SAVED to the Clipboard")
        
        # Save palette into a file
        else:
            node = self.node
            palettepath = node.parm(CP_PALETTE_LIB_PATH).evalAsString()
            out_path_checked = out_flame_utils.out_check_outpath(node, palettepath, OUT_PALETTE_FILE_EXT, 'Palette')

            if out_path_checked is not False:
                
                # SHIFT - Open a file explorer to the file location
                if self.kwargs['shift']:
                    flam3h_general_utils.util_open_file_explorer(out_path_checked)
                    
                else:
                    
                    if flam3h_general_utils.isLOCK(out_path_checked):
                        ui_text = f"This Palette library is Locked."
                        ALL_msg = f"This Palette library is Locked and you can not modify this file.\n\nTo Lock a Palete lib file just rename it using:\n\"{FLAM3H_LIB_LOCK}\" as the start of the filename.\n\nOnce you are happy with a palette library you built, you can rename the file to start with: \"{FLAM3H_LIB_LOCK}\"\nto prevent any further modifications to it. For example if you have a lib file call: \"my_rainbows_colors.json\"\nyou can rename it to: \"{FLAM3H_LIB_LOCK}_my_rainbows_colors.json\" to keep it safe."
                        _MSG = f"{node.name()}: PALETTE library file -> is LOCKED"
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, f"This Palette file is LOCKED")
                        if hou.isUIAvailable():
                            hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Palette Lock", details=ALL_msg, details_label=None, details_expanded=False) # type: ignore
                        
                        # Clear up status bar msg
                        flam3h_general_utils.set_status_msg('', 'MSG')
                        
                    else:
                        
                        # F3H palette json file checks
                        json_file, f3h_json_file = self.isJSON_F3H(node, out_path_checked, False)
                        
                        # build palette data to save
                        json_dict, json_data = self.flam3h_ramp_save_JSON_DATA()

                        if self.kwargs["ctrl"]:
                            
                            if not os.path.exists(out_path_checked):
                                with open(str(out_path_checked),'w') as w:
                                    w.write(json_data)
                                    
                            elif json_file and f3h_json_file:
                                os.remove(str(out_path_checked))
                                with open(str(out_path_checked),'w') as w:
                                    w.write(json_data)
                                    
                            else:
                                _MSG = f"{node.name()}: Palette JSON SAVE -> Although the JSON file you loaded is legitimate, it does not contain any valid FLAM3H Palette data."
                                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                                flam3h_general_utils.flash_message(node, f"Palette SAVE -> Not a valid FLAM3H JSON palette file")
                                
                        else:
                            # if the file exist and is a valid JSON file
                            if json_file and f3h_json_file:
                                with open(str(out_path_checked),'r') as r:
                                    prevdata = json.load(r)
                                with open(str(out_path_checked), 'w') as w:
                                    newdata = json_dict
                                    prevdata.update(newdata)
                                    data = json.dumps(prevdata,indent = 4)
                                    w.write(data)
                            # Otherwise mean it is either empty or not exist,
                            # just create one with the current ramp in it
                            #
                            # Note that we already checked for a proper file extension with:
                            # def out_flame_utils.out_check_outpath(...)
                            # so to not override something else by accident
                            else:
                                # If the file do not exist, lets create it and save the palette in it
                                if not os.path.isfile(out_path_checked):
                                    with open(str(out_path_checked),'w') as w:
                                        w.write(json_data)

                        # We do this again so we can read the newly created file if any 
                        json_file, f3h_json_file = self.isJSON_F3H(node, out_path_checked, False)
                        if json_file:
                            if f3h_json_file:
                                # Set some parameters
                                with open(out_path_checked) as f:
                                    data = json.load(f)
                                    preset_last_idx = str(len(data.keys())-1)
                                    # Set all CP preset menus parameter index
                                    node.setParms({CP_PALETTE_PRESETS: preset_last_idx })
                                    node.setParms({CP_PALETTE_PRESETS_OFF: preset_last_idx })
                                    node.setParms({CP_SYS_PALETTE_PRESETS: preset_last_idx })
                                    node.setParms({CP_SYS_PALETTE_PRESETS_OFF: preset_last_idx })
                                    # Clearup the Palette name if any were given
                                    node.setParms({CP_PALETTE_OUT_PRESET_NAME: ''})
                                    # Mark this as a valid file and as the currently loaded preset as it is the preset we just saved
                                    node.setParms({CP_ISVALID_FILE: 1})
                                    node.setParms({CP_ISVALID_PRESET: 1})
                                    # Make sure to update the tmp ramp with the just saved one
                                    self.palette_cp_to_tmp()
                                    del data
                                    
                                # Set the file path to the corrected one
                                node.setParms({CP_PALETTE_LIB_PATH: str(out_path_checked)})
                                
                                _MSG = f"Palette SAVED"
                                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
                                flam3h_general_utils.flash_message(node, f"Palette SAVED")
                                
                            else:
                                # Just in case lets set those
                                node.setParms({CP_ISVALID_FILE: 0})
                                node.setParms({CP_ISVALID_PRESET: 0})
                                
                                _MSG = f"{node.name()}: Palette JSON SAVE -> Although the JSON file you loaded is legitimate, it does not contain any valid FLAM3H Palette data."
                                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                                flam3h_general_utils.flash_message(node, f"Palette SAVE -> Not a valid FLAM3H JSON palette file")
                        
            else:
                _MSG = f"{node.name()}: SAVE Palette -> Select a valid output file or a valid filename to create first."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"PALETTE -> Select a valid output file")


                
    def json_to_flam3h_ramp_initialize(self, rgb_from_XML_PALETTE: list) -> tuple[hou.Ramp, int, bool]:
        """It will check the passed list of colors for validity and build a Houdini ramp parameter's values from it.
        If not valid, or only one coclor is included, it will output one RED color and mark this palette as an Error.

        Args:
            rgb_from_XML_PALETTE (list): a list of colors collected from the palette json file preset (from file or from Clipboard)
        """  
        _CHECK = True
        if rgb_from_XML_PALETTE:
            
            try:
                POSs = list(iter_islice(iter_count(0, 1.0/(len(rgb_from_XML_PALETTE)-1)), len(rgb_from_XML_PALETTE)))
                BASEs = [hou.rampBasis.Linear] * len(rgb_from_XML_PALETTE) # type: ignore
            except:
                # If something goes wrong...set one RED key only
                rgb_from_XML_PALETTE, POSs, BASEs = self.build_ramp_palette_error()
                _CHECK = False
                
        else:
            rgb_from_XML_PALETTE, POSs, BASEs = self.build_ramp_palette_error()
            _CHECK = False
            
        # Set lookup samples to the default value of: 256
        self.node.setParms({CP_RAMP_LOOKUP_SAMPLES: 256})
        return hou.Ramp(BASEs, POSs, rgb_from_XML_PALETTE), len(POSs), _CHECK



    def json_to_flam3h_ramp_set_HSV(self, node, hsv_check: bool, hsv_vals: list) -> None:
            keep_hsv = node.parm(CP_RAMP_HSV_KEEP_ON_LOAD).eval()
            if not keep_hsv:
                if hsv_check:
                    node.setParms({CP_RAMP_HSV_VAL_NAME: hou.Vector3(hsv_vals)})
                else:
                    # This is for backward compatibility ( when the hsv data wasn't being exported yet )
                    node.setParms({CP_RAMP_HSV_VAL_NAME: hou.Vector3((1, 1, 1))})



    def json_to_flam3h_ramp_SET_PRESET_DATA(self) -> None:

        node = self.node
        
        iterators_num = node.parm(FLAME_ITERATORS_COUNT).evalAsInt()
        if iterators_num:
            
            # get ramp parm
            ramp_parm = node.parm(CP_RAMP_SRC_NAME)
            # Reset ramps to default
            self.build_ramp_palette_default(ramp_parm)
            self.delete_ramp_all_keyframes(ramp_parm)
            self.delete_ramp_all_keyframes(node.parm(CP_RAMP_HSV_NAME))
            
            filepath = node.parm(CP_PALETTE_LIB_PATH).evalAsString()
            
            if os.path.isfile(filepath) and os.path.getsize(filepath)>0 and node.parm(CP_ISVALID_FILE).evalAsInt():

                HEXs = []
                hsv_vals = []
                
                # get current preset name
                if node.parm(CP_ISVALID_PRESET).evalAsInt():
                    preset_id = int(node.parm(CP_PALETTE_PRESETS).eval())
                    menu_label = str(node.parm(CP_PALETTE_PRESETS).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_PALETTE_LOAD)[-1].strip()
                else:
                    preset_id = int(node.parm(CP_PALETTE_PRESETS_OFF).eval())
                    menu_label = str(node.parm(CP_PALETTE_PRESETS_OFF).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_PALETTE_LOAD_EMPTY)[-1].strip()
                    
                # Remove the enumeration menu index string from the preset name.
                #
                # We are using "str.lstrip()" because the preset name has been "str.strip()" already on save from inside: self.flam3h_ramp_save_JSON_DATA()
                # and there are only the leading white spaces left from the menu enumaration index number string to remove.
                if node.parm(PREFS_ENUMERATE_MENU).eval():
                    preset = ':'.join(str(menu_label).split(':')[1:]).lstrip()
                else:
                    preset = menu_label
                
                # The following 'hsv_check' is for backward compatibility
                hsv_check = False
                
                with open(filepath, 'r') as r:
                    
                    data = json.load(r)[preset]
                    hex_values = data[CP_JSON_KEY_NAME_HEX]
                    try:
                        [hsv_vals.append(float(x)) for x in data[CP_JSON_KEY_NAME_HSV].split(' ')]
                        hsv_check = True
                    except:
                        pass
                    [HEXs.append(hex) for hex in wrap(hex_values, 6)]
                    
                rgb_from_XML_PALETTE = []
                for hex in HEXs:
                    x = self.hex_to_rgb(hex)
                    rgb_from_XML_PALETTE.append((abs(x[0])/(255 + 0.0), abs(x[1])/(255 + 0.0), abs(x[2])/(255 + 0.0)))
                
                # Initialize and SET new ramp
                _RAMP, _COUNT, _CHECK = self.json_to_flam3h_ramp_initialize(rgb_from_XML_PALETTE)
                ramp_parm.set(_RAMP)
                
                # Set HSV values
                self.json_to_flam3h_ramp_set_HSV(node, hsv_check, hsv_vals)
                # Make sure we update the HSV palette
                self.palette_cp()
                # Update palette temp
                self.palette_cp_to_tmp()

                # Update/Set palette MSG
                flam3h_palette_utils.json_to_flam3h_palette_plus_MSG(node, HEXs)
                
                # Set palette lookup samples
                # Note we are setting the function type to: Flame(0) so we always clamp at the minimun of 256 lookup samples
                keys = out_flame_utils(self.kwargs).out_palette_keys_count(self.palette_plus_do, _COUNT, 0, False)
                node.setParms({CP_RAMP_LOOKUP_SAMPLES: int(keys)}) # type: ignore
                
                # Store selection into all preset menu just in case ;)
                pidx = str(preset_id)
                node.setParms({CP_SYS_PALETTE_PRESETS: pidx})
                node.setParms({CP_SYS_PALETTE_PRESETS_OFF: pidx})
                node.setParms({CP_PALETTE_PRESETS: pidx})
                node.setParms({CP_PALETTE_PRESETS_OFF: pidx})
                
                # Mark this as a loaded preset if valid
                if _CHECK: node.setParms({CP_ISVALID_PRESET: 1})
                else: node.setParms({CP_ISVALID_PRESET: 0})
                
                # Print to status Bar
                _MSG = f"{node.name()}: LOAD Palette preset: \"{preset}\" -> Completed"
                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                
                if _CHECK:
                    _MSG = f"{node.name()}: LOAD Palette preset: \"{preset}\" -> Completed"
                    flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                    flam3h_general_utils.flash_message(node, f"Palette LOADED")
                else:
                    _MSG = f"{node.name()}: PALETTE -> ERROR on preset: \"{preset}\""
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                    flam3h_general_utils.flash_message(node, f"Palette ERROR")
            
            else:
                _MSG = f"{node.name()}: PALETTE -> Nothing to load"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                flam3h_general_utils.flash_message(node, f"PALETTE -> Nothing to load")



    def json_to_flam3h_ramp_sys(self, use_kwargs=True) -> None:
        """Load the selected palette preset from the provided json file
        using the SYS load palette button.

        Args:
            use_kwargs (bool, optional): Use the houdini kwargs arguments or not. Defaults to True.
                                         This is being done as when this definition run from a menu parameter
                                         the kwargs arguments are not available. 
        """
        
        if use_kwargs:
            self.json_to_flam3h_ramp(use_kwargs)
            
        else:
            node = self.node
            if node.parm(CP_ISVALID_PRESET).evalAsInt():
                preset_id = node.parm(CP_SYS_PALETTE_PRESETS).eval()
                node.setParms({CP_SYS_PALETTE_PRESETS_OFF: str(preset_id)})
            else:
                preset_id = node.parm(CP_SYS_PALETTE_PRESETS_OFF).eval()
                node.setParms({CP_SYS_PALETTE_PRESETS: str(preset_id)})
                
            node.setParms({CP_PALETTE_PRESETS: str(preset_id)})
            node.setParms({CP_PALETTE_PRESETS_OFF: str(preset_id)}) 
            self.json_to_flam3h_ramp(use_kwargs)


    def json_to_flam3h_ramp(self, use_kwargs=True) -> None:
        """Load the selected palette preset from the provided json file
        
        Args:
            kwargs (dict): [kwargs[] dictionary]
        """
        
        node = self.node
        
        # KWARGS
        if use_kwargs:
                
            # SHIFT - If we are selecting a palette json file to load
            if self.kwargs['shift']:
                filepath = hou.ui.selectFile(start_directory=None, title="FLAM3H: Load a palette *.json file", collapse_sequences=False, file_type=hou.fileType.Any, pattern="*.json", default_value=None, multiple_select=False, image_chooser=None, chooser_mode=hou.fileChooserMode.Read, width=0, height=0)  # type: ignore
                filepath_expandvars = os.path.expandvars(filepath)
                dir = os.path.dirname(filepath_expandvars)
                if os.path.isdir(dir):
                    node.setParms({CP_PALETTE_LIB_PATH: filepath_expandvars})
                    # The following definition use the default arg's value so it can set the proper ramp message if needed.
                    flam3h_general_utils(self.kwargs).flam3h_init_presets_CP_PALETTE_PRESETS()
                
            # ALT - If we are loading a palette from the clipboard
            elif self.kwargs['alt']:
                
                palette = hou.ui.getTextFromClipboard() # type: ignore
                try:
                    data = json.loads(palette)
                except:
                    data = None
                
                # If it is a valid json data
                if data is not None:
                    
                    try:
                        preset = list(data.keys())[0]
                    except:
                        preset = None
                        
                    if preset is not None:
                        
                        f3h_palette_data = json.loads(palette)[preset]
                        
                        # Check if it is a valid FLAM3H JSON data. This is the moment of the truth ;)
                        try:
                            hex_values = f3h_palette_data[CP_JSON_KEY_NAME_HEX]
                            isJSON_F3H = True
                        except:
                            isJSON_F3H = False
                            _MSG = f"{node.name()}: PALETTE JSON load -> Although the JSON file you loaded is legitimate, it does not contain any valid FLAM3H Palette data."
                            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                            del data
                            
                        # If it is a valid FLAM3H Palette JSON data
                        if isJSON_F3H:
                            
                            # get ramp parm
                            ramp_parm = node.parm(CP_RAMP_SRC_NAME)
                            # Reset ramps to default
                            self.build_ramp_palette_default(ramp_parm)
                            self.delete_ramp_all_keyframes(ramp_parm)
                            self.delete_ramp_all_keyframes(node.parm(CP_RAMP_HSV_NAME))

                            
                            hsv_vals = []
                            hsv_check = False
                            try:
                                [hsv_vals.append(float(x)) for x in f3h_palette_data[CP_JSON_KEY_NAME_HSV].split(' ')]
                                hsv_check = True
                            except:
                                pass
                            
                            rgb_from_XML_PALETTE = []
                            HEXs = [hex for hex in wrap(f3h_palette_data[CP_JSON_KEY_NAME_HEX], 6)]
                            for hex in HEXs:
                                x = self.hex_to_rgb(hex)
                                rgb_from_XML_PALETTE.append((abs(x[0])/(255 + 0.0), abs(x[1])/(255 + 0.0), abs(x[2])/(255 + 0.0)))
                            
                            # Initialize and SET new ramp.
                            _RAMP, _COUNT, _CHECK = self.json_to_flam3h_ramp_initialize(rgb_from_XML_PALETTE)
                            ramp_parm.set(_RAMP)
                            
                            # Set HSV values
                            self.json_to_flam3h_ramp_set_HSV(node, hsv_check, hsv_vals)
                            # Make sure we update the HSV palette
                            self.palette_cp()
                            # Update palette tmp
                            self.reset_CP_TMP()
                            
                            # Update/Set palette MSG
                            flam3h_palette_utils.json_to_flam3h_palette_plus_MSG(node, HEXs)
                            
                            # Set palette lookup samples
                            # Note we are setting the function type to: Flame so we always clamp at the minimun of 256 lookup samples
                            keys = out_flame_utils(self.kwargs).out_palette_keys_count(self.palette_plus_do, _COUNT, 0, False)
                            node.setParms({CP_RAMP_LOOKUP_SAMPLES: int(keys)}) # type: ignore
                            
                            # Mark this as not a loaded preset since it is coming from the Clipboard
                            node.setParms({CP_ISVALID_PRESET: 0})
                            
                            if _CHECK:
                                _MSG = f"{node.name()}: PALETTE Clipboard -> LOAD Palette preset: \"{preset}\" -> Completed"
                                flam3h_general_utils.set_status_msg(_MSG, 'IMP')
                                flam3h_general_utils.flash_message(node, f"Palette LOADED from the Clipboard")
                            else:
                                _MSG = f"{node.name()}: PALETTE Clipboard -> ERROR on preset: \"{preset}\""
                                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                                flam3h_general_utils.flash_message(node, f"Palette ERROR from the Clipboard")
                            
                    else:
                        _MSG = f"{node.name()}: PALETTE Clipboard -> The data from the clipboard is not a valid JSON data."
                        flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                        flam3h_general_utils.flash_message(node, f"Palette Clipboard -> Nothing to load")
                        
                else:
                    _MSG = f"{node.name()}: Palette Clipboard -> The data from the clipboard is not a valid JSON data."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                    flam3h_general_utils.flash_message(node, f"Palette Clipboard -> Nothing to load")

            # LMB - Load the currently selected palette preset
            else:   
                self.json_to_flam3h_ramp_SET_PRESET_DATA()

        # NO KWARGS - LMB - Load the currently selected palette preset
        #
        # This is used from the preset menus parameter, since kwargs are not available from here.
        else:
            self.json_to_flam3h_ramp_SET_PRESET_DATA()



    def palette_cp(self) -> None:
        """Force the HSV palette colors/keys to match the source palette colors/keys.
        
        """    
        node = self.node
        rmpsrc = node.parm(CP_RAMP_SRC_NAME)
        rmphsv = node.parm(CP_RAMP_HSV_NAME)
        rmphsv.set(hou.Ramp(rmpsrc.evalAsRamp().basis(), rmpsrc.evalAsRamp().keys(), rmpsrc.evalAsRamp().values()))
        # Apply HSV if any
        #
        # self.palette_hsv is running also inside self.palette_lock()
        # becasue it used to get call also from other Houdini parameter's callback scripts.
        # Need to come back and make changes...
        self.palette_hsv()
        
        if node.parm(CP_ISVALID_FILE).eval():
            rmptmp = node.parm(CP_RAMP_TMP_NAME)
            if rmpsrc.evalAsRamp().keys() != rmptmp.evalAsRamp().keys() or rmpsrc.evalAsRamp().values() != rmptmp.evalAsRamp().values():
                # Mark this as not a loaded palette preset
                node.setParms({CP_ISVALID_PRESET: 0})
            else:
                # Mark this as a loaded palette preset since they match
                node.setParms({CP_ISVALID_PRESET: 1})

        # Update/Set palette MSG
        flam3h_palette_utils.json_to_flam3h_palette_plus_MSG(node, rmpsrc.evalAsRamp().keys(), True)    


    def palette_cp_to_tmp(self) -> None:
        """Make a copy of the source palette into the temp palette.
        This is used when loading a palette preset to check if the user made modifications to the loaded palette.

        """    
        node = self.node
        rmpsrc = node.parm(CP_RAMP_SRC_NAME)
        rmptmp = node.parm(CP_RAMP_TMP_NAME)
        rmptmp.set(hou.Ramp(rmpsrc.evalAsRamp().basis(), rmpsrc.evalAsRamp().keys(), rmpsrc.evalAsRamp().values()))



    def palette_hsv(self) -> None:
        """Apply a HSV to the paltte colors/keys.
        
        Args:
        """  
        node = self.node
        rmpsrc = node.parm(CP_RAMP_SRC_NAME)
        rmphsv = node.parm(CP_RAMP_HSV_NAME)
        hsvprm = node.parmTuple(CP_RAMP_HSV_VAL_NAME)
        # Convert to HSV
        hsv = list(map(lambda x: colorsys.rgb_to_hsv(x[0], x[1], x[2]), rmpsrc.evalAsRamp().values()))
        # Apply color correction
        rgb = [colorsys.hsv_to_rgb( item[0]+hsvprm[0].eval(), item[1]*hsvprm[1].eval(), item[2]*hsvprm[2].eval() ) for item in hsv]
        # Set the ramp
        rmphsv.set(hou.Ramp(rmpsrc.evalAsRamp().basis(), rmpsrc.evalAsRamp().keys(), rgb))



    def palette_lock(self) -> None:
        """Lock the HSV palette color/keys from being modified.
        This is also used to updated the palette HSV to keep it up to date with the source palette.
        
        Args:
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
        """
        node = self.node
        filepath = node.parm(CP_PALETTE_LIB_PATH).evalAsString()
        if self.isJSON_F3H(node, filepath, False)[0]:
            if flam3h_general_utils.isLOCK(filepath) is False:
                node.setParms({MSG_PALETTE: ''})
        else:
            node.setParms({MSG_PALETTE: ''})



    def reset_CP_TMP(self) -> None:
        """Reset the TEMP palette to its defaults.

        Args:
        """
        # CP->tmp ramp RESET
        ramp_tmp_parm = self.node.parm(CP_RAMP_TMP_NAME)
        self.delete_ramp_all_keyframes(ramp_tmp_parm)
        # Build TMP ramp
        self.build_ramp_palette_temp(ramp_tmp_parm)
        
        
        
    def reset_CP_options(self) -> None:
        """Reset the CP tab options toggles to their defaults.

        Args:
        """
        node = self.node
        node.setParms({CP_RAMP_LOOKUP_SAMPLES: 256})
        node.setParms({CP_RAMP_SAVE_256_PLUS: 1})
        node.setParms({CP_RAMP_SAVE_HSV: 0})
        self.reset_CP_LOCK_MSG()


    def reset_CP_run_0(self) -> None:
        """Reset the CP tab to its defaults.

        Args:
        """
        node = self.node
        # CP
        node.setParms({CP_RAMP_HSV_VAL_NAME: hou.Vector3((1.0, 1.0, 1.0))})
        # CP->ramp
        ramp_parm = node.parm(CP_RAMP_SRC_NAME)
        # Reset ramps
        self.build_ramp_palette_default(ramp_parm)
        self.palette_cp()
        self.delete_ramp_all_keyframes(ramp_parm)
        self.delete_ramp_all_keyframes(node.parm(CP_RAMP_HSV_NAME))
        # Reset CP options tab
        self.reset_CP_options()
        # CP->tmp ramp RESET
        self.reset_CP_TMP()
        # Mark this as not a loaded preset
        node.setParms({CP_ISVALID_PRESET: 0})
        
        
    def reset_CP_run_2(self) -> None:
        """Reset the CP tab HSV values to their defaults.

        Args:
        """
        node = self.node
        hsv_prm = node.parmTuple(CP_RAMP_HSV_VAL_NAME)
        _hsv = hsv_prm.eval()
        if _hsv[0] == _hsv[1] == _hsv[2] == 1:
            hsv_prm.deleteAllKeyframes()
            _MSG = f"CP HSV: already at its default values."
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
            flam3h_general_utils.flash_message(node, _MSG)
        else:
            hsv_prm.deleteAllKeyframes()
            hsv_prm.set(hou.Vector3((1.0, 1.0, 1.0)))
            # Print out to Houdini's status bar
            _MSG = f"CP HSV RESET"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
            flam3h_general_utils.flash_message(node, _MSG)
            
        # CP->tmp ramp RESET
        self.reset_CP_TMP()
        # # Update palette py
        self.palette_cp()
        # Mark this as not a loaded preset
        node.setParms({CP_ISVALID_PRESET: 0})


    def reset_CP_run_3(self) -> None:
        """Reset the CP tab Palette ramp to its defaults ( and the HSV palette too ).

        Args:
        """
        node = self.node
        ramp_parm = node.parm(CP_RAMP_SRC_NAME)
        # Build ramp
        self.build_ramp_palette_default(ramp_parm)
        self.palette_cp()
        self.delete_ramp_all_keyframes(ramp_parm)
        self.delete_ramp_all_keyframes(node.parm(CP_RAMP_HSV_NAME))
        # CP->tmp ramp RESET
        self.reset_CP_TMP()
        # Mark this as not a loaded preset
        node.setParms({CP_ISVALID_PRESET: 0})
        # Set lookup samples to the default value of: 256
        node.setParms({CP_RAMP_LOOKUP_SAMPLES: 256})
        
        # Print out to Houdini's status bar
        _MSG = f"CP Palette RESET"
        flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
        flam3h_general_utils.flash_message(node, _MSG)
        
    
    def reset_CP(self, mode: int=0) -> None:
        """Run the desired reset_CP(...) definition.

        Args:
            mode (int): definition idx to run
        """
        func_list = {0: self.reset_CP_run_0, 2: self.reset_CP_run_2, 3: self.reset_CP_run_3}
        run = func_list.get(mode)
        if run is not None: run()
        else: flam3h_general_utils.set_status_msg(f"{self.node.name()}: reset_CP(...) python definition have nothing to run with the passed \"mode\" value.", 'WARN')





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

METHODS:

flam3h_about_msg(self) -> None:

flam3h_about_plugins_msg(self) -> None:

flam3h_about_web_msg(self) -> None:

flam3h_about_web_homepage(self) -> None:

flam3h_about_web_github(self) -> None:

flam3h_about_web_instagram(self) -> None:

flam3h_about_web_youtube(self) -> None:

flam3h_about_web_flam3_paper(self) -> None:

flam3h_about_web_flam3_github(self) -> None:

flam3h_web_run(self, key: str) -> None:
    """
    
    def __init__(self, kwargs: dict) -> None:
        self._kwargs = kwargs
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
        """    
        
        nl = "\n"
        nnl = "\n\n"
            
        year = datetime.now().strftime("%Y")
        
        flam3h_cvex_version = f"Code language: CVEX H19.x.x"
        hou_version = flam3h_general_utils.houdini_version()
        if hou_version >= 19:
            flam3h_cvex_version = f"Code language: CVEX H{str(hou_version)}.x.x"
        flam3h_author = f"Author: Alessandro Nardini ( Italy )"
        flam3h_python_version = f"Python 3.7.13"
        flam3h_houdini_version = f"Version: {FLAM3H_VERSION}{FLAM3H_VERSION_STATUS_GOLD} (GPL v3)"
        Implementation_years = f"2020/{year}"
        Implementation_build = f"{flam3h_author}\n{flam3h_cvex_version}, {flam3h_python_version}\n{flam3h_houdini_version}\n{Implementation_years}"
        
        code_references = """CODE REFERENCES
Flam3 :: (GPL v2)
Apophysis :: (GPL)
Fractorium :: (GPL v3)"""

        example_flames = """EXAMPLE FLAMES
C-91, Gabor Timar, Golubaja, Pillemaster,
Plangkye, Tatasz, Triptychaos, TyrantWave,
Zy0rg, Seph, Lucy, b33rheart, Neonrauschen."""
        
        h_version = '.'.join(str(x) for x in hou.applicationVersion())
        Houdini_version = f"HOST\nSideFX Houdini {h_version}"
        Python_version = f"Python: {python_version()}"
        license_type = str(hou.licenseCategory()).split(".")[-1]
        Houdini_license = f"License: {license_type}"
        User = f"User: {hou.userName()}"
        PC_name = f"Machine name: {hou.machineName()}"
        Platform = f"Platform: {hou.applicationPlatformInfo()}"
        
        build = (   Implementation_build, nnl,
                    code_references, nnl,
                    example_flames, nnl,
                    Houdini_version, nl,
                    Houdini_license, nl,
                    Python_version, nl,
                    User, nl,
                    PC_name, nl,
                    Platform
                    )
        
        build_about_msg = "".join(build)
        self.node.setParms({MSG_FLAM3H_ABOUT: build_about_msg})


    def flam3h_about_plugins_msg(self) -> None:
        """Build and set the FLAM3H about plugins message.
        """    
        vars_sorted = [var.capitalize() for var in sorted(VARS_FLAM3_DICT_IDX.keys())]
        n = 5
        vars_sorted_grp = [vars_sorted[i:i+n] for i in range(0, len(vars_sorted), n)]
        vars_txt = "".join( [", ".join(grp) + "." if idx == (len(vars_sorted_grp)-1) else ", ".join(grp) + ",\n" for idx, grp in enumerate(vars_sorted_grp)] )
        vars_txt_MSG = f"They are also available as PRE and POST:\n\n{vars_txt}"
        self.node.setParms({MSG_FLAM3H_PLUGINS: vars_txt_MSG})
        
        
    def flam3h_about_web_msg(self) -> None:
        """Build and set the FLAM3H about web heading's msgs.
        """    
        
        node = self.node
        
        _FLAM3HWEB_MSG = 'FLAM3H web'
        _FLAM3HGIT_MSG = 'FLAM3H github'
        _FLAM3HINSTA_MSG = 'FLAM3H instagram'
        _FLAM3HYOUTUBE_MSG = 'FLAM3H video tutorials'
        _FLAM3PDF_MSG = 'The Fractal Flame Algorithm pdf'
        _FLAM3GIT_MSG = 'The Fractal Flame Algorithm github'
        
        node.setParms({MSG_FLAM3H_WEB: _FLAM3HWEB_MSG})
        node.setParms({MSG_FLAM3H_GIT: _FLAM3HGIT_MSG})
        node.setParms({MSG_FLAM3H_INSTA: _FLAM3HINSTA_MSG})
        node.setParms({MSG_FLAM3H_YOUTUBE: _FLAM3HYOUTUBE_MSG})
        node.setParms({MSG_FLAM3_PDF: _FLAM3PDF_MSG})
        node.setParms({MSG_FLAM3_GIT: _FLAM3GIT_MSG})
        

    def flam3h_about_web_homepage(self) -> None:
        """Open a web browser to the FLAM3H homepage.
        """        
        page = "https://www.alexnardini.net/"
        www_open(page)
        

    def flam3h_about_web_github(self) -> None:
        """Open a web browser to the FLAM3H github repository.
        """  
        page = "https://github.com/alexnardini/FLAM3_for_SideFX_Houdini"
        www_open(page)
        

    def flam3h_about_web_instagram(self) -> None:
        """Open a web browser to the FLAM3H instagram account.
        """  
        page = "https://www.instagram.com/alexnardini/"
        www_open(page)
        
    def flam3h_about_web_youtube(self) -> None:
        """Open a web browser to the FLAM3H youtube video tutorials.
        """  
        page = "https://www.youtube.com/@alexnardiniITALY/videos"
        www_open(page)


    def flam3h_about_web_flam3_paper(self) -> None:
        """Open a web browser to the original "the fractal flame algorithm" publication/paper pdf.
        """  
        page = "https://flam3.com/flame_draves.pdf"
        www_open(page)
        

    def flam3h_about_web_flam3_github(self) -> None:
        """Open a web browser to the original FLAM3 github repository.
        """  
        page = "https://github.com/scottdraves/flam3"
        www_open(page)
        
        
    def flam3h_web_run(self, key: str) -> None:
        
        web = {'web': self.flam3h_about_web_homepage,
               'git': self.flam3h_about_web_github,
               'insta': self.flam3h_about_web_instagram,
               'youtube': self.flam3h_about_web_youtube,
               'paper': self.flam3h_about_web_flam3_paper,
               'flam3git': self.flam3h_about_web_flam3_github}
        
        run = web.get(key)
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

METHODS:

ui_xaos_infos(self) -> None:

ui_OUT_presets_name_infos(self) -> None:

ui_active_iterator_infos(self) -> None:
    """
    
    def __init__(self, kwargs: dict) -> None:
        self._kwargs = kwargs
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

If you dnt use the “xaos” keywork at the beginning,
the entire xaos string will be reset to all weights with value: 1

If you type a number,
the entire xaos string will be reset to all weights set to that number.

If you type a floating point number,
the entire xaos string will be reset to all weights set to the integer part of that number.
ex: 123.876 will become -> 123

If you type a negative number, it will be reset to a value of: 1"""
        
        node = self.node

        if self.kwargs["ctrl"]:
            if hou.isUIAvailable():
                hou.ui.displayMessage(ALL_msg, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3H: XAOS usage infos", details=None, details_label=None, details_expanded=False) # type: ignore

        else:
            # current node
            autodiv = node.parm(PREFS_XAOS_AUTO_SPACE).eval()
            if autodiv:
                node.setParms({PREFS_XAOS_AUTO_SPACE: 0})
                flam3h_iterator_utils(self.kwargs).auto_set_xaos()
                
                _MSG = f"{node.name()}: Xaos weights auto space: OFF"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                
            else:
                node.setParms({PREFS_XAOS_AUTO_SPACE: 1})
                flam3h_iterator_utils(self.kwargs).auto_set_xaos()
                
                _MSG = f"{node.name()}: Xaos weights auto space: ON"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')

            
    def ui_OUT_presets_name_infos(self) -> None:
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


    
    def ui_active_iterator_infos(self) -> None:
        ALL_msg = """If an xform/iterator is disabled,
it wont be included when saving the Flame out into a flame file.

In case you still want to include the inactive iterator into the file,
set its Weight to Zero instead."""
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
OUT_XML_FLAME_RENDER_CURVES = 'curves'
OUT_XML_FLAME_RENDER_CURVES_VAL = "0 0 1 0.25 0.25 1 0.5 0.5 1 0.75 0.75 1 0 0 1 0.25 0.25 1 0.5 0.5 1 0.75 0.75 1 0 0 1 0.25 0.25 1 0.5 0.5 1 0.75 0.75 1 0 0 1 0.25 0.25 1 0.5 0.5 1 0.75 0.75 1 "
OUT_XML_FLAME_RENDER_OVERALL_CURVE = 'overall_curve'
OUT_XML_FLAME_RENDER_OVERALL_CURVE_VAL = "0 0 0.25 0.25 0.5 0.5 0.75 0.75 1 1 "
OUT_XML_FLAME_RENDER_RED_CURVE = 'red_curve'
OUT_XML_FLAME_RENDER_GREEN_CURVE = 'green_curve'
OUT_XML_FLAME_RENDER_BLUE_CURVE = 'blue_curve'
OUT_XML_FLAME_RENDER_RED_CURVE_VAL=OUT_XML_FLAME_RENDER_GREEN_CURVE_VAL=OUT_XML_FLAME_RENDER_BLUE_CURVE_VAL=OUT_XML_FLAME_RENDER_OVERALL_CURVE_VAL
# XML OUT render key data prm names HOUDINI
# for now make sense to expose those, I may add more in the future if needed
# Note that those are the FLAM3H UI parameter's names for the OUT Render properties tab.
OUT_XML_RENDER_HOUDINI_DICT: dict = {   XML_XF_NAME: OUT_FLAME_PRESET_NAME,
                                        OUT_XML_FLAME_SIZE: 'outres',
                                        OUT_XML_FLAME_CENTER: 'outcenter',
                                        OUT_XML_FLAME_ROTATE: 'outrotate',
                                        OUT_XML_FLAME_SCALE: 'outscale',
                                        OUT_XML_FLAME_QUALITY: 'outquality',
                                        OUT_XML_FLAME_BRIGHTNESS: 'outbrightness',
                                        OUT_XML_FLAME_GAMMA: 'outgamma',
                                        OUT_XML_FLAME_POWER: 'outhighlight',
                                        OUT_XML_FLAME_K2: 'outk2',
                                        OUT_XML_FLAME_VIBRANCY: 'outvibrancy'  
                                    }

# For now we force to assume a valid flame's XML file must have this tree.root name.
XML_VALID_FLAMES_ROOT_TAG = 'flames'
# and this for a valid chaotica file ( not supported )
XML_VALID_CHAOS_ROOT_TAG = 'ifs'

# Since we get the folowing keys in a separate action, we exclude them for later variation's names searches to help speed up a little.
XML_XF_KEY_EXCLUDE = ("weight", "color", "var_color", "symmetry", "color_speed", "name", "animate", "pre_blur", "coefs", "post", "chaos", "opacity")
# Note that "pre_gaussian_blur" has been added to the below tuple as we force it to be remapped to "pre_blur" on load inside FLAM3H if "remap "pre_gaussian_blur" IN load option is checked (ON by default)
# note: for FF I swap back to the above  XML_XF_KEY_EXCLUDE to make possible to load pre_gaussian_blur since FF do not posses an hard coded pre_blur.
XML_XF_KEY_EXCLUDE_PGB = ("weight", "color", "var_color", "symmetry", "color_speed", "name", "animate", "pre_blur", "pre_gaussian_blur", "coefs", "post", "chaos", "opacity")

# This has been fixed and now radial_blur variation matches all the other apps
# but I leave it here just in case other variation will need it.
XML_XF_PRM_EXCEPTION = ("None", )

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

VARS_FLAM3_DICT_IDX: dict = {   "linear": 0, 
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

VARS_FRACTORIUM_DICT: dict = {  "a": ("arch", "arcsech", "arcsech2", "arcsinh", "arctanh", "asteria", "auger"),
                                "b": ( "barycentroid", "bcircle", "bcollide", "bent", "bent2", "bipolar", "bisplit", "blade", "blade3d", "blob", "blob2", "blob3d", "block", "blocky", "blur", "blur_circle", "blur_heart", "blur_linear", "blur_pixelize", "blur_square", "blur_zoom", "blur3d", "bmod", "boarders", "boarders2", "bswirl", "btransform", "bubble", "bubble2", "bubblet3d", "butterfly", "bwraps", "bwraps_rand"),
                                "c": ( "cardioid", "cell", "checks", "circleblur", "circlecrop", "circlecrop2", "circlelinear", "circlerand", "circlesplit", "circletrans1", "circlize", "circlize2", "circus", "collideoscope", "concentric", "conic", "cos", "cos_wrap", "cosh", "coshq", "cosine", "cosq", "cot", "coth", "coth_spiral", "cothq", "cotq", "cpow", "cpow2", "cpow3", "crackle", "crackle2", "crescents", "crob", "crop", "cropn", "cross", "csc", "csch", "cschq", "cscq", "cubic3d", "cubic_lattice3d", "curl", "curl3d", "curl_sp", "curvature", "curve", "cylinder", "cylinder2"),
                                "d": ("delta_a", "depth", "depth_blur", "depth_blur2", "depth_gaussian", "depth_gaussian2", "depth_ngon", "depth_ngon2", "depth_sine", "depth_sine2", "diamond", "disc", "disc2", "disc3d", "dragonfire", "dust","d_spherical"),
                                "e": ("eclipse", "ecollide", "edisc", "ejulia", "elliptic", "emod", "emotion", "ennepers", "epispiral", "epush", "erf", "erotate", "escale", "escher", "estiq", "eswirl", "ex", "excinis", "exp", "exp2", "expo", "exponential", "extrude", "eyefish"),
                                "f": ("falloff", "falloff2", "falloff3", "fan", "fan2", "farblur", "fdisc", "fibonacci", "fibonacci2", "fisheye", "flatten", "flip_circle", "flip_x", "flip_y", "flower", "flower_db", "flux", "foci", "foci3d", "foci_p", "fourth", "funnel"),
                                "g": ("gamma", "gaussian", "gaussian_blur", "gdoffs", "glynnia", "glynnia2", "glynnsim1", "glynnsim2", "glynnsim3", "glynnsim4", "glynnsim5", "gnarly", "gridout"),
                                "h": ("handkerchief", "heart", "heat", "helicoid", "helix", "hemisphere", "henon", "hexaplay3d", "hexcrop", "hexes", "hexnix3d", "hex_modulus", "hex_rand", "hex_truchet", "ho", "hole", "horseshoe", "hyperbolic", "hypercrop", "hypershift", "hypershift2", "hypertile", "hypertile1", "hypertile2", "hypertile3d", "hypertile3d1", "hypertile3d2"),
                                "i": ("idisc", "inkdrop", "interference2"),
                                "j": ("jac_cn", "jac_dn", "jac_sn", "julia", "julia3d", "julia3dq", "julia3dz", "juliac", "julian", "julian2", "julian3dx", "julianab", "juliaq", "juliascope"), 
                                "k": ("kaleidoscope", ),
                                "l": ("lazyjess", "lazysusan", "lazy_travis", "lens", "line", "linear", "linear_t", "linear_t3d", "linear_xz", "linear_yz", "linear3d", "lissajous", "log", "log_db", "loq", "loonie", "loonie2", "loonie3", "loonie3d", "lozi"),
                                "m": ("mask", "mcarpet", "mirror_x", "mirror_y", "mirror_z", "mobiq", "mobius", "mobius_strip", "mobiusn", "modulus", "modulusx", "modulusy", "murl", "murl2"),
                                "n": ("nblur", "ngon", "noise", "npolar"),
                                "o": ("octagon", "octapol", "ortho", "oscilloscope", "oscilloscope2", "ovoid", "ovoid3d"),
                                "p": ("panorama1", "panorama2", "parabola", "pdj", "perspective", "petal", "phoenix_julia", "pie", "pie3d", "pixel_flow", "poincare", "poincare2", "poincare3d", "point_symmetry", "polar", "polar2", "polynomial", "popcorn", "popcorn2", "popcorn23d", "pow_block", "power", "pressure_wave", "projective", "prose3d", "psphere", "pulse"),
                                "q": ("q_ode", ),
                                "r": ("radial_blur", "radial_gaussian", "rand_cubes", "rational3", "rays", "rays1", "rays2", "rays3", "rblur", "rectangles", "rings", "rings2", "ripple", "rippled", "rotate", "rotate_x", "rotate_y", "rotate_z", "roundspher", "roundspher3d"),
                                "s": ("scry", "scry2", "scry3d", "sec", "secant2", "sech", "sechq", "secq", "separation", "shift", "shred_rad", "shred_lin", "sigmoid", "sin", "sineblur", "sinh", "sinhq", "sinq", "sintrange", "sinus_grid", "sinusoidal", "sinusoidal3d", "smartshape", "smartcrop", "spher", "sphereblur", "spherical", "spherical3d", "sphericaln", "spherivoid", "sphyp3d", "spiral", "spiral_wing", "spirograph", "split", "split_brdr", "splits", "splits3d", "square", "squares", "square3d", "squarize", "squirrel", "squish", "sschecks", "starblur", "starblur2", "stripes", "stwin", "super_shape", "super_shape3d","svf", "swirl", "swirl3", "swirl3r", "synth"),
                                "t": ("tan", "tancos", "tangent", "tanh", "tanhq", "tanh_spiral", "tanq", "target", "target0", "target2", "taurus", "tile_hlp", "tile_log", "trade", "truchet", "truchet_fill", "truchet_hex_fill", "truchet_hex_crop", "truchet_glyph", "truchet_inv", "truchet_knot", "twintrian", "twoface"),
                                "u": ("unicorngaloshen", "unpolar"),
                                "v": ("vibration", "vibration2", "vignette", "voron"),
                                "w": ("w", "waffle", "waves", "waves2", "waves22", "waves23", "waves23d", "waves2b", "waves2_radial", "waves3", "waves4", "waves42", "wavesn", "wdisc", "wedge", "wedge_julia", "wedge_sph", "whorl"),
                                "x": ("x", "xerf", "xheart", "xtrb"),
                                "y": ("y", ),
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
    in_flame_utils.in_util_typemaker(list[]) -> Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4]:
    
    The (("variation_name") entrie, is not used here and only for reference.
    '''
    
    varsPRM: tuple = (  ("linear", 0), 
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
                        ("rings2", ("rings2_val", ), 1), 
                        ("rectangles", ("rectangles_x", "rectangles_y"), 1), 
                        ("radial_blur", ("radial_blur_angle", ), 1), 
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
                        ("bipolar", ("bipolar_shift", ), 1),
                        ("boarders", 0),
                        ("butterfly", 0), 
                        ("cell", ("cell_size", ), 1), 
                        ("cpow", ("cpow_power", "cpow_r", "cpow_i"), 1), 
                        ("edisc", 0), 
                        ("elliptic", 0), 
                        ("noise", 0), 
                        ("escher", ("escher_beta", ), 1), 
                        ("foci", 0), 
                        ("lazysusan", ("lazysusan_x", "lazysusan_y"), ("lazysusan_spin", "lazysusan_twist", "lazysusan_space"), 1), 
                        ("loonie", 0), 
                        ("pre blur", 0), 
                        ("modulus", ("modulus_x", "modulus_y"), 1), 
                        ("oscilloscope", ("oscope_frequency", "oscope_amplitude", "oscope_damping", "oscope_separation"), 1), 
                        ("polar2", 0), 
                        ("popcorn2", ("popcorn2_x", "popcorn2_y"), ("popcorn2_c", ), 1), 
                        ("scry", 0), 
                        ("separation", ("separation_x", "separation_y"), ("separation_xinside", "separation_yinside"), 1), 
                        ("split", ("split_xsize", "split_ysize"), 1), 
                        ("splits", ("splits_x", "splits_y"), 1), 
                        ("stripes", ("stripes_space", "stripes_warp"), 1), 
                        ("wedge", ("wedge_swirl", "wedge_angle", "wedge_hole", "wedge_count", ), 1), 
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
                        ("flux", ("flux_spread", ), 1), 
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
    varsPRM_FRACTORIUM_EXCEPTIONS: dict = { 67: ("oscilloscope", ("oscilloscope_frequency", "oscilloscope_amplitude", "oscilloscope_damping", "oscilloscope_separation"), 1),
                                            96: ("Mobius", ("Mobius_Re_A", "Mobius_Re_B", "Mobius_Re_C", "Mobius_Re_D"), ("Mobius_Im_A", "Mobius_Im_B", "Mobius_Im_C", "Mobius_Im_D"), 1)
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

METHODS:

get_name(self, key=XML_XF_NAME) -> tuple

    """    
    
    def __init__(self, xmlfile: str) -> None:
        """This Class is only to try to speedup the python menu UI evaulation.
        Here I assume that if the parameter IN_ISVALID_FILE is 1,
        than we can proceed without worries about actually checking and iterate through the flame file for its validity.
        It is a mere attempt to speedup but it should help a little bit ;)
        as we are not evaluating the _xml_tree() class witch is more heavy and sophisticated, something we do not need for this purpose.
        This is a very lightweight way to gather the Flames names.
        
        A parameter to the IN Tab has been added: IN_ISVALID_PRESET
        This parameter will tell us if a preset is currently loaded or not.
        
        Before we only had: IN_ISVALID_FILE
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
        
        
    def get_name(self, key=XML_XF_NAME) -> tuple:
        """Collect all Flame presets name from the XML Flame file.
        
        This is being added as a quick and cheap way to do so making some assumption ahead of time.
        Read this class __init__ doc string to know more.

        Args:
            key (_type_, optional): _description_. Defaults to XML_XF_NAME. The XML Flame's name key.

        Returns:
            Union[tuple, None]: Flame presets names.
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
                hou.pwd().setParm({IN_ISVALID_FILE: 0})
                hou.pwd().setParm({IN_ISVALID_PRESET: 0})
                return ()
            except:
                _MSG = ("\nFLAM3H -> warning: Could not evaluate the current hou.SopNode. Class _xml(...).get_name(...)\n")
                print(_MSG)
                flam3h_general_utils.set_status_msg(f"{_MSG}", 'WARN')
                return ()




class _xml_tree:
    """
class _xml_tree

STATIC METHODS:

xmlfile_root_chk(xmlfile: Union[str, None], clipboard=False) -> Union[str, None]:

METHODS:

get_name(self, key=XML_XF_NAME) -> tuple:

__get_name_val_str(self, key: str) -> tuple:

__get_name_list_str(self, key: str) -> tuple:

__get_flame(self, key=XML_FLAME_NAME) -> Union[tuple, None]:

__get_flame_count(self, flames: list) -> int:

"""

    def __init__(self, xmlfile: str) -> None:
        """
        Args:
            xmlfile (str): xmlfile (str): [xml *.flame file v_type to load]
        """        
        self._xmlfile = xmlfile
        self._xmlfile_data = self.xmlfile_root_chk(self._xmlfile)
        self._xmlfile_data_clipboard = self.xmlfile_root_chk(self._xmlfile, True)
        self._isvalidtree = self.xmlfile_isvalidtree_chk(self._xmlfile)
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
        self._name = self.get_name()
        self._plugins = self.get_name(XML_FLAME_PLUGINS)
        self._sw_version = self.get_name(XML_FLAME_VERSION) # type: ignore



    @staticmethod
    def xmlfile_root_chk(xmlfile: Union[str, None], clipboard=False) -> Union[str, None]:
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
                        _MSG = "Flame IN -> Chaotica XML not supported"
                        print(f"{hou.pwd().name()}: {_MSG}")
                        flam3h_general_utils.set_status_msg(f"{hou.pwd().name()}: {_MSG}", 'MSG')
                        flam3h_general_utils.flash_message(hou.pwd(), _MSG)
                    return None
            else:
                # If there are flames, proceed
                if tuple([f for f in root.iter(XML_FLAME_NAME)]):
                    out_flame_utils._out_pretty_print(root)
                    return lxmlET.tostring(root, encoding="unicode") # type: ignore
                else:
                    return None
        except:
            return None



    @staticmethod
    def xmlfile_isvalidtree_chk(xmlfile: str) -> bool:
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
        except:
            return False



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
    def get_name(self, key=XML_XF_NAME) -> tuple:
        """Collect all Flame presets name from the XML Flame file.

        Args:
            key (_type_, optional): _description_. Defaults to XML_XF_NAME. The XML Flame's name key.

        Returns:
            Union[tuple, None]: Flame presets names.
        """        
        if self.isvalidtree:
            root = self.tree.getroot()
            if key == XML_XF_NAME: return tuple( [str(name.get(key)).strip() if name.get(key) is not None else '[]' for name in root] )
            else: return tuple( [str(name.get(key)).strip() if name.get(key) is not None else [] for name in root] )
        else:
            return () 
        
        
    def __get_name_val_str(self, key: str) -> tuple:
        """Collect all Flame presets single value from the XML Flame file.

        Args:
            key (str): _description_. Defaults to XML_XF_NAME. The XML Flame's name key.

        Returns:
            Union[tuple, None]: Flame presets names.
        """        
        if self.isvalidtree:
            root = self.tree.getroot()
            return tuple( [str(in_flame.xf_val_cleanup_str(name.get(key)).strip()) if name.get(key) is not None else [] for name in root] )
        else:
            return () 
        
        
    def __get_name_list_str(self, key: str) -> tuple:
        """Collect all Flame presets list values from the XML Flame file.

        Args:
            key (str): _description_. Defaults to XML_XF_NAME. The XML Flame's name key.

        Returns:
            Union[tuple, None]: Flame presets names.
        """        
        if self.isvalidtree:
            root = self.tree.getroot()
            return tuple( [str(in_flame.xf_list_cleanup_str(str(name.get(key)).strip().split())) if name.get(key) is not None else [] for name in root] )
        else:
            return () 
        
        
    def __get_flame(self, key=XML_FLAME_NAME) -> Union[tuple, None]:
        """Collect the actual Flame presets object data from the XML file.

        Args:
            key (_type_, optional): _description_. Defaults to XML_FLAME_NAME. The XML Flame's flame key.

        Returns:
            Union[tuple, None]: Flames objects data.
        """        
        if self.isvalidtree:
            root = self.tree.getroot()
            return tuple( [f for f in root.iter(key)] )
        else:
            return None


    def __get_flame_count(self, flames: list) -> int:
        """Get the number of Flame presets inside the XML file.

        Args:
            flames (list): Flames objects data.

        Returns:
            int: Number of Flames.
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

STATIC METHODS:

xf_val_cleanup_str(val: str, default_val: str = '0') -> str:

xf_list_cleanup(affine: list, default_val: str = '0') -> list:

xf_list_cleanup_str(affine: list, default_val: str = '0') -> str:

affine_coupling(affine: list, key='', mp_idx=None, type: int=0) -> list:

check_all_iterator_weights(node: hou.SopNode, keyvalues: list) -> None:

METHODS:

__is_valid_idx(self, idx: int) -> int:

__get_xforms(self, idx: int, key: str) -> Union[tuple, None]:

__get_xaos(self, xforms: Union[tuple, None], key=XML_XF_XAOS) -> Union[tuple, None]:

__get_affine(self, xforms: Union[tuple, None], key: str, type: int=0) -> Union[tuple, None]:

__get_keyvalue(self, xforms: Union[tuple, None], key: str) -> Union[tuple, None]:

__get_palette(self, idx: int, key=XML_PALETTE) -> Union[tuple[hou.Ramp, int, str], None]:

__get_palette_flam3h_hsv(self, idx: int) -> Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4, bool]:

__get_mb_flam3h_mb(self, idx: int, key='') -> Union[int, float, bool, None]:

__get_flam3h_toggle(self, toggle: bool) -> Union[int, None]:

    Args:
        _xml_tree ([class]): [inherit properties methods from the _xml_tree class]
    """  

    def __init__(self, node: hou.SopNode, xmlfile: str) -> None:
        """
        Args:
            xmlfile (str): [xml *.flame v_type file to load]
        """        
        super().__init__(xmlfile)
        self._node = node
        # self._name = self._xml_tree__get_name() # type: ignore
        # self._sw_version = self.get_name(XML_FLAME_VERSION) # type: ignore
        # self._flame_plugins = self.get_name(XML_FLAME_PLUGINS) # type: ignore
        self._flame = self._xml_tree__get_flame() # type: ignore
        self._flame_count = self._xml_tree__get_flame_count(self._flame) # type: ignore
        # render properties
        self._out_size = self._xml_tree__get_name_list_str(OUT_XML_FLAME_SIZE) # type: ignore
        self._out_center = self._xml_tree__get_name_list_str(OUT_XML_FLAME_CENTER) # type: ignore
        self._out_rotate = self._xml_tree__get_name_val_str(OUT_XML_FLAME_ROTATE) # type: ignore
        self._out_scale = self._xml_tree__get_name_list_str(OUT_XML_FLAME_SCALE) # type: ignore
        self._out_quality = self._xml_tree__get_name_val_str(OUT_XML_FLAME_QUALITY) # type: ignore
        self._out_brightness = self._xml_tree__get_name_val_str(OUT_XML_FLAME_BRIGHTNESS) # type: ignore
        self._out_gamma = self._xml_tree__get_name_val_str(OUT_XML_FLAME_GAMMA) # type: ignore
        self._out_highlight_power = self._xml_tree__get_name_val_str(OUT_XML_FLAME_POWER) # type: ignore
        self._out_logscale_k2 = self._xml_tree__get_name_val_str(OUT_XML_FLAME_K2) # type: ignore
        self._out_vibrancy = self._xml_tree__get_name_val_str(OUT_XML_FLAME_VIBRANCY) # type: ignore
        # custom to FLAM3H only
        self._flam3h_sys_rip = self._xml_tree__get_name_val_str(OUT_XML_FLAM3H_SYS_RIP) # type: ignore
        self._flam3h_hsv = self._xml_tree__get_name_list_str(OUT_XML_FLAM3H_HSV) # type: ignore
        # just check any of the MB val and if exist mean there is MB data to be set.
        # this will act as bool and if true, it will hold our OUT_XML_FLMA3H_MB_FPS value ( as string )
        self._flam3h_mb = self._xml_tree__get_name_val_str(OUT_XML_FLMA3H_MB_FPS) # type: ignore
        self._flam3h_mb_samples = self._xml_tree__get_name_val_str(OUT_XML_FLMA3H_MB_SAMPLES) # type: ignore
        self._flam3h_mb_shutter = self._xml_tree__get_name_val_str(OUT_XML_FLMA3H_MB_SHUTTER) # type: ignore
        self._flam3h_cp_samples = self._xml_tree__get_name_val_str(OUT_XML_FLAM3H_CP_SAMPLES) # type: ignore
        self._flam3h_prefs_f3c = self._xml_tree__get_name_val_str(OUT_XML_FLAM3H_PREFS_F3C) # type: ignore



    @staticmethod
    def xf_val_cleanup_str(val: str, default_val: str = '0') -> str:
        """ Attempt to remove invalid characters from the passed value.
        
        Args:
            val (str): [value from the xml]

        Returns:
            str: [value cleaned up from invalid characters]
        """  
        clean = [letter for letter in val if letter in CHARACTERS_ALLOWED_XFORM_VAL]
        new_val = ''.join(clean)
        try:
            float(new_val)
            return new_val
        except:
            return default_val


    @staticmethod
    def xf_list_cleanup(affine: list, default_val: str = '0') -> list:
        """ Attempt to remove invalid characters from the list values and return a list.
        
        Args:
            affine (list): [affine values from the xml]

        Returns:
            list: [a list of affine values cleaned up from invalid characters]
        """  
        new = []
        for val in affine:
            clean = [letter for letter in val if letter in CHARACTERS_ALLOWED_XFORM_VAL]
            new_val = ''.join(clean)
            try:
                float(new_val)
                new.append(new_val)
            except:
                new.append(default_val)
        return new
    
    
    @staticmethod
    def xf_list_cleanup_str(affine: list, default_val: str = '0') -> str:
        """ Attempt to remove invalid characters from the list values and return a spaced joined string of the list.
        
        Args:
            affine (list): [affine values from the xml]

        Returns:
            str: [a string of spaced joined affine values cleaned up from invalid characters]
        """  
        new = []
        for val in affine:
            clean = [letter for letter in val if letter in CHARACTERS_ALLOWED_XFORM_VAL]
            new_val = ''.join(clean)
            try:
                float(new_val)
                new.append(new_val)
            except:
                new.append(default_val)
        return ' '.join(new)


    @staticmethod
    def affine_coupling(affine: list, key='', mp_idx=None, type: int=0) -> list:
        """ Build proper affine values composed of hou.Vector2 tuples.
        It will also check the affine passed in and provide an alternative defaults affine values if not correct and print out messages to inform the user about different cases.
        
        Args:
            affine (list): [affine values from the xml]
            key (str, default to: ''): [The type of affine to build: XML_PRE_AFFINE, XML_POST_AFFINE, XML_FLAM3H_PRE_AFFINE, XML_FLAM3H_POST_AFFINE]
            mp_idx (int, default to: None): [multi parameter index, for messaging purpose only]

        Returns:
            list: [a list of hou.Vector2: ((X.x, X.y), (Y.x, Y.y), (O.x, O.y)) ready to be used to set affine parms, or an empty list if something is wrong]
        """      
        affine_count = len(affine)
        if affine_count == 6:
            return [hou.Vector2((tuple(affine[i:i+2]))) for i in (0, 2, 4)]
        
        else:
            print(datetime.now().strftime('%b-%d-%Y %H:%M:%S'))
            
            sel = {XML_PRE_AFFINE: f"Pre affine", XML_POST_AFFINE: f"Post affine", XML_FLAM3H_PRE_AFFINE: f"F3H Pre affine", XML_FLAM3H_POST_AFFINE: f"F3H Post affine"}
            sel_key = sel.get(key)
            
            # Is it an iterator or an FF or None ?
            if mp_idx is not None:
                if type == 0: iter_type = mp_idx
                elif type == 1: iter_type = 'FF'
                else: iter_type = None
            
            if key in [XML_PRE_AFFINE, XML_POST_AFFINE]:
                if affine_count == 0:
                    if iter_type is not None: _MSG = f"\t{sel_key} on iterator {iter_type}, have no affine values. Expeted are: 6\n\t:Reverted back to default affine values."
                    else:_MSG = f"\t{sel_key} have {affine_count} values. Expeted are: 6\n\t:Reverted back to default affine values."
                    print(_MSG)
                    return [hou.Vector2((tuple( AFFINE_IDENT[i:i+2] ))) for i in (0, 2, 4)]
                else:
                    if iter_type is not None: _MSG = f"\t{sel_key} on iterator {iter_type}, have {affine_count} values. Expeted are: 6\n\t:Using 0.0(Zeros) for missing affine values."
                    else:_MSG = f"\t{sel_key} have {affine_count} values. Expeted are: 6\n\t:Using 0.0(Zeros) for missing affine values."
                    print(_MSG)
                    return [hou.Vector2((tuple( np_pad(affine, (0, 6-min(6, affine_count)), 'constant', constant_values=0).tolist()[i:i+2] ))) for i in (0, 2, 4)]
            
            if sel_key is not None:
                if iter_type is not None:
                    _MSG = f"\t{sel_key} on iterator {iter_type}, have {affine_count} values. Expeted are: 6\n\t:Skipped"
                    print(_MSG)
                else:
                    _MSG = f"\t{sel_key} have {affine_count} values. Expeted are: 6\n\t:Skipped"
                    print(_MSG)
                    
            return []
    
    
    
    @staticmethod
    def check_all_iterator_weights(node: hou.SopNode, keyvalues: list) -> None:
        """If all iterators have their weights set to: 0.0(ZERO), set the first one to a very small number instead because Houdini was crashing otherwise.
        It will modify the passed keyvalues arg.
        
        Args:
            self:
            node (hou.SopNode): Current FLAM3H node we are loading a Flame preset from.
            kevalues (list): list of all iterators key values, in this case all iterator;s weights values.

        Returns:
           None
        """   
        if min(keyvalues) == max(keyvalues) == 0:
            min_weight = 0.00000001
            keyvalues[0] = min_weight
            _MSG = f"{node.name()}:\nThe loaded Flame preset have all iterator's weights set to: 0.0(Zero).\nIterator 1 has been reverted back to a value of: {min_weight}\nThere must always be at least one active iterator's weight above 0.0(Zero).\n"
            print(f"{_MSG}")
    
    
    # CLASS: PROPERTIES
    ##########################################
    ##########################################

    @property
    def node(self):
        return self._node
    
    # @property
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
            idx (int): [flame idx out of all flames included in the loaded flame file]

        Returns:
            int: [clamped idx value just in case the user pass an invalid idx to this function]
        """     
        return 0 if idx < 0 else 0 if self.flame_count == 1 else self.flame_count-1 if idx > self.flame_count-1 else idx


    def __get_xforms(self, idx: int, key: str) -> Union[tuple, None]:
        """Get choosen fractal flame's xforms collected inside a dict each.
        every xform in xforms is a dict coming directly from the parsed XML file.

        Args:
            self:
            idx (int): [flame idx out of all flames included in the loaded flame file]
            key (str): [use "xform" for transforms and "finalxform" for final flame transform]

        Returns:
            tuple: [a tuple of all xforms inside the selected flame or None]
        """
        if  self.isvalidtree:
            xforms = [xf.attrib for xf in self.flame[idx].iter(key)]
            xforms_lower = []
            if xforms:
                for xf in xforms:
                    k = [str(x).lower() for x in xf.keys()]
                    kv = zip(k, xf.values())
                    xforms_lower.append(dict(kv))
            else:
                return None
            
            return tuple(xforms_lower)
        else:
            return None
    
    
    def __get_xaos(self, xforms: Union[tuple, None], key=XML_XF_XAOS) -> Union[tuple, None]:
        """
        Args:
            self:
            xforms (list): [list of all xforms contained inside this flame]
            key (str): the flame XML xaos tag name.

        Returns:
            Union[tuple, None]: [either a list of xaos strings or None]
        """        
        if  self.isvalidtree and xforms is not None:

            xaos = [f"xaos:{':'.join(self.xf_list_cleanup(str(xf.get(key)).split()))}" if xf.get(key) is not None else [] for xf in xforms]
            if not max(list(map(lambda x: len(x), xaos))):
                return None
            
            else:
                return tuple(xaos)
            
        else:
            return None


    def __get_affine(self, xforms: Union[tuple, None], key: str, type: int=0) -> Union[tuple, None]:
        """
        Args:
            self:
            xforms (list): [list of all xforms contained inside this flame]
            key (str): [affine xml tag name. Either 'coefs' for pre affine or 'post' for post affine]
            type (int): [Only used by the self.affine_coupling(...) definition. It is either an iterator: 0 or an FF: 1]

        Returns:
            Union[tuple, None]: [Either a list of list of tuples ((X.x, X.y), (Y.x, Y.y), (O.x, O.y)) or None]
        """           
        if  self.isvalidtree and xforms is not None:
            coefs = [tuple(self.affine_coupling([float(x) for x in self.xf_list_cleanup(str(xf.get(key)).split())], key, int(idx+1), type)) if xf.get(key) is not None else [] for idx, xf in enumerate(xforms)]
            
            if max(list(map(lambda x: len(x), coefs))):
                return tuple(coefs)
            
            else:
                return None
            
        else:
            return None


    def __get_keyvalue(self, xforms: Union[tuple, None], key: str) -> Union[tuple, None]:
        """
        Args:
            self:
            xforms (list): [list of all xforms contained inside this flame]
            key (str): [xml tag names. For shader: 'color', 'symmetry'->(color_speed), 'opacity']

        Returns:
            Union[tuple, None]: [description]
        """        
        if self.isvalidtree and xforms is not None:
            
            keyvalues = []
            for xform in xforms:
                
                if xform.get(key) is not None:
                    
                    if key in XML_XF_NAME:
                        keyvalues.append(xform.get(key))
                        continue
                    
                    else:
                        if key in XML_XF_OPACITY: default_val = '1'
                        else: default_val = '0'
                        keyvalues.append(float(self.xf_val_cleanup_str(xform.get(key), default_val)))
                        continue
                    
                else:
                    # Fractorium always remap "pre_blur" to "pre_gaussian_blur" when you load a flame in.
                    # This mean that every time you save the Flame again from Fractorium and load it back in FLAM3H you loose a PRE variation's slot.
                    #
                    # Lets do the same but we will remap "pre_gaussian_blur" back to "pre_blur" when we load a flame back in FLAM3H.
                    # An IN Tab load option is provided to change this behavior and load/use the "pre_gaussian_blur" variation instead on load.
                    pre_gaussian_blur = xform.get(in_flame_utils.in_util_make_PRE(in_flame_utils.in_get_var_name_from_dict(VARS_FLAM3_DICT_IDX, 33)))
                    if pre_gaussian_blur is not None:
                        
                        if self.node.parm(IN_REMAP_PRE_GAUSSIAN_BLUR).eval():
                            keyvalues.append(float(self.xf_val_cleanup_str(pre_gaussian_blur)))
                            continue
                        
                        else:
                            keyvalues.append(float(0))
                            continue
                        
                    # Flame files created with Apophysis versions older than 7x ( or much older as the test file I have is from v2.06c )
                    # seem not to include those keys if not used or left at default values.
                    # We set them here so we can use them inside FLAM3H on load.
                    elif key in XML_XF_OPACITY:
                        keyvalues.append(float(1))
                        continue
                    
                    elif key in XML_XF_SYMMETRY:
                        keyvalues.append(float(0))
                        continue
                    
                    else:
                        keyvalues.append([])
                        continue
            
            # CHECKS
            if key in XML_XF_WEIGHT:
                in_flame.check_all_iterator_weights(self.node, keyvalues)
                
            return tuple(keyvalues)
        
        else:
            return None

        
    def __get_palette(self, idx: int, key=XML_PALETTE) -> Union[tuple[hou.Ramp, int, str], None]:
        """
        Args:
            self:
            idx (int): [flame idx out of all flames included in the loaded flame file]
            key (str): the flame XML palette tag name.

        Returns:
            hou.Ramp: [return an already made hou.Ramp with values from the flame xml palette]
        """        
        if  self.isvalidtree:
            try:
                palette_attrib = self.flame[idx].find(key).attrib
            except:
                palette_attrib = None
                
            if palette_attrib is not None:
                palette_hex = self.flame[idx].find(key).text
                format = dict(palette_attrib).get(XML_PALETTE_FORMAT)
                
                _HEX = []
                for line in palette_hex.splitlines():
                    cleandoc = i_cleandoc(line)
                    if(len(cleandoc)>1):
                        [_HEX.append(hex) for hex in wrap(cleandoc, 6)]
                try:
                    rgb_from_XML_PALETTE = [(flam3h_palette_utils.hex_to_rgb(hex)[0]/(255 + 0.0), flam3h_palette_utils.hex_to_rgb(hex)[1]/(255 + 0.0), flam3h_palette_utils.hex_to_rgb(hex)[2]/(255 + 0.0)) for hex in _HEX]
                    ramp_keys_count = len(rgb_from_XML_PALETTE)
                    POSs = list(iter_islice(iter_count(0, 1.0/(ramp_keys_count-1)), (ramp_keys_count)))
                    BASESs = [hou.rampBasis.Linear] * (ramp_keys_count) # type: ignore
                    return hou.Ramp(BASESs, POSs, rgb_from_XML_PALETTE), (ramp_keys_count), str(format)
                except:
                    hou.pwd().setParms({MSG_DESCRIPTIVE_PRM: "Error: IN->PALETTE\nHEX values not valid."})
                    if hou.isUIAvailable():
                        ui_text = "Flame's Palette hex values not valid."
                        palette_warning_msg = f"PALETTE Error:\nPossibly some out of bounds values in it.\n\nYou can fix this by assigning a brand new palette before saving it out again.\nYou can open this Flame in Fractorium and assign a brand new palette\nto it and save it out to re load it again inside FLAM3H."
                        hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Palette Error", details=palette_warning_msg, details_label=None, details_expanded=True) # type: ignore
                        return None
                    else:
                        return None
            else:
                return None
        else:
            return None
    
    
    # custom to FLAM3H only
    def __get_palette_flam3h_hsv(self, idx: int) -> Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4, bool]:
        """
        Args:
            idx (int): [flame idx out of all flames included in the loaded flame file]

        Returns:
            hou.Vector3 or False: [a hou.Vector3 of HSV vals or False] Since we know the HSV is made out of 3 floats, it will always rreturn a: hou.Vector3
        """   
        if self.isvalidtree:
            palette_hsv_xml_list = self.flam3h_hsv[idx]
            if palette_hsv_xml_list:
                palette_hsv_xml_s = str(palette_hsv_xml_list).split(" ")
                if len(palette_hsv_xml_s) != 3: palette_hsv_xml_s = np_pad(palette_hsv_xml_s, (0, 3-min(3, len(palette_hsv_xml_s))), 'constant', constant_values=1).tolist()
                return in_flame_utils.in_util_typemaker(list(map(lambda x: float(x), palette_hsv_xml_s )))
            else:
                return False
        else:
            return False
    
    
    # custom to FLAM3H only
    def __get_mb_flam3h_mb(self, idx: int, key='') -> Union[int, float, bool, None]:
        """
        Args:
            self:
            idx (int): [flame idx out of all flames included in the loaded flame file]
            key (str): the flame XML motion blur tag name you are interested to get:
            
            OUT_XML_FLMA3H_MB_FPS -> flam3h_mb_fps
            OUT_XML_FLMA3H_MB_SAMPLES -> flam3h_mb_samples
            OUT_XML_FLMA3H_MB_SHUTTER -> flam3h_mb_shutter

        Returns:
            Union[int, float, bool, None]: [FLAM3H motion blur parameter's values.]
        """   
        if self.isvalidtree:
            mb_do = self.flam3h_mb[idx]
            # self._flam3h_mb[idx] can also be an empty list, hence the double check
            if mb_do is not None and mb_do:
                if key == OUT_XML_FLMA3H_MB_FPS:
                    try:
                        return int(mb_do)
                    except:
                        return False
                elif key == OUT_XML_FLMA3H_MB_SAMPLES:
                    return int(self.flam3h_mb_samples[idx])
                elif key == OUT_XML_FLMA3H_MB_SHUTTER:
                    return float(self.flam3h_mb_shutter[idx])
                else:
                    return False
            else:
                return False
        else:
            return False
        
        
    # custom to FLAM3H only
    def __get_cp_flam3h_samples(self, idx: int) -> Union[int, bool]:
        """
        Args:
            self:
            idx (int): [flame idx out of all flames included in the loaded flame file]

        Returns:
            Union[int, bool]: [FLAM3H palette lookup samples parameter values.]
        """   
        if self.isvalidtree:
            cp_samples_key = self.flam3h_cp_samples[idx]
            if cp_samples_key:
                samples = int(cp_samples_key)
                if samples in (16, 32, 64, 128, 256, 512, 1024): # just make sure the lookup samples count is one of the valid options.
                    return samples
                else:
                    # else return the default value
                    return 256
            else:
                # else return the default value
                return 256
        else:
            return False
        
        
    # custom to FLAM3H only
    def __get_flam3h_toggle(self, toggle: bool) -> Union[int, None]:
        """Get FLAM3H toggle parameter value: ON or OFF ( 1 or 0 )

        Args:
            toggle (bool): _description_

        Returns:
            Union[int, None]: This flame toggle
        """        

        if self.isvalidtree:
            # f3c = self._flam3h_prefs_f3c[idx]
            # self._flam3h_prefs_f3c[idx] can also be an empty list, hence the double check
            if toggle is not None and toggle:
                try:
                    return int(toggle)
                except:
                    return None
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
    
    def __init__(self, node: hou.SopNode, xmlfile: str, idx=0) -> None:
        """
        Args:
            xmlfile (str): xmlfile (str): [xml flame v_type file to load]
            idx (int, optional): [flame idx out of all flames included in the loaded flame file]. Defaults to 0.
        """        
        super().__init__(node, xmlfile)
        self._idx = self._in_flame__is_valid_idx(idx) # type: ignore
        self._xforms = self._in_flame__get_xforms(self._idx, XML_XF) # type: ignore
        self._xf_name = self._in_flame__get_keyvalue(self._xforms, XML_XF_NAME) # type: ignore
        self._weight = self._in_flame__get_keyvalue(self._xforms, XML_XF_WEIGHT) # type: ignore
        self._pre_blur = self._in_flame__get_keyvalue(self._xforms, XML_XF_PB) # type: ignore
        self._xaos  = self._in_flame__get_xaos(self._xforms) # type: ignore
        self._coefs = self._in_flame__get_affine(self._xforms, XML_PRE_AFFINE) # type: ignore
        self._f3h_coefs = self._in_flame__get_affine(self._xforms, XML_FLAM3H_PRE_AFFINE) # type: ignore
        self._f3h_coefs_angle = self._in_flame__get_keyvalue(self._xforms, XML_FLAM3H_PRE_AFFINE_ANGLE) # type: ignore
        self._post  = self._in_flame__get_affine(self._xforms, XML_POST_AFFINE) # type: ignore
        self._f3h_post  = self._in_flame__get_affine(self._xforms, XML_FLAM3H_POST_AFFINE) # type: ignore
        self._f3h_post_angle = self._in_flame__get_keyvalue(self._xforms, XML_FLAM3H_POST_AFFINE_ANGLE) # type: ignore
        self._finalxform = self._in_flame__get_xforms(self._idx, XML_FF) # type: ignore
        self._finalxform_coefs = self._in_flame__get_affine(self._finalxform, XML_PRE_AFFINE, 1) # type: ignore
        self._finalxform_f3h_coefs = self._in_flame__get_affine(self._finalxform, XML_FLAM3H_PRE_AFFINE, 1) # type: ignore
        self._finalxform_f3h_coefs_angle = self._in_flame__get_keyvalue(self._finalxform, XML_FLAM3H_PRE_AFFINE_ANGLE) # type: ignore
        self._finalxform_post  = self._in_flame__get_affine(self._finalxform, XML_POST_AFFINE, 1) # type: ignore
        self._finalxform_f3h_post = self._in_flame__get_affine(self._finalxform, XML_FLAM3H_POST_AFFINE, 1) # type: ignore
        self._finalxform_f3h_post_angle = self._in_flame__get_keyvalue(self._finalxform, XML_FLAM3H_POST_AFFINE_ANGLE) # type: ignore
        self._finalxform_name = self._in_flame__get_keyvalue(self._finalxform, XML_XF_NAME) # type: ignore
        self._palette = self._in_flame__get_palette(self._idx) # type: ignore
        self._color = self._in_flame__get_keyvalue(self._xforms, XML_XF_COLOR) # type: ignore
        self._color_speed = self._in_flame__get_keyvalue(self._xforms, XML_XF_COLOR_SPEED) # type: ignore
        self._symmetry = self._in_flame__get_keyvalue(self._xforms, XML_XF_SYMMETRY) # type: ignore
        self._opacity = self._in_flame__get_keyvalue(self._xforms, XML_XF_OPACITY) # type: ignore
        # custom to FLAM3H only
        self._sys_flam3h_rip = self._in_flame__get_flam3h_toggle(self._flam3h_sys_rip[self._idx]) # type: ignore
        self._cp_flam3h_hsv = self._in_flame__get_palette_flam3h_hsv(self._idx) # type: ignore
        self._mb_flam3h_mb_fps = self._in_flame__get_mb_flam3h_mb(self._idx, OUT_XML_FLMA3H_MB_FPS) # type: ignore
        self._mb_flam3h_mb_samples= self._in_flame__get_mb_flam3h_mb(self._idx, OUT_XML_FLMA3H_MB_SAMPLES) # type: ignore
        self._mb_flam3h_mb_shutter = self._in_flame__get_mb_flam3h_mb(self._idx, OUT_XML_FLMA3H_MB_SHUTTER) # type: ignore
        self._cp_flam3h_cp_samples = self._in_flame__get_cp_flam3h_samples(self._idx) # type: ignore
        self._prefs_flam3h_f3c = self._in_flame__get_flam3h_toggle(self._flam3h_prefs_f3c[self._idx]) # type: ignore




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

STATIC METHODS:

in_util_key_name_isalnum(key_name: str) -> str:

in_util_make_NULL(name: Union[str, list[str], tuple[str]]) -> Union[str, list[str], tuple[str]]:

in_util_make_VAR(name: Union[str, list[str], tuple[str]]) -> Union[Union[str, list[str]], None]:

in_util_make_PRE(name: Union[str, Union[list[str], KeysView], tuple[str]]) -> Union[str, list[str], None]:

in_util_make_POST(name: Union[str, Union[list[str], KeysView], tuple[str]]) -> Union[str, list[str], None]:

in_load_stats_unknown_vars(preset_id: int, apo_data: in_flame_iter_data) -> list:

in_to_flam3h_is_CHAOS(xml: str) -> bool:

in_to_flam3h_clipboard_is_CHAOS() -> bool:

in_get_xforms_var_keys( xforms: Union[tuple, None], 
                        vars: Union[str, list[str], tuple[str], dict[str, int], dict[str, tuple], KeysView, None], 
                        exclude_keys: tuple
                        ) -> Union[list[str], None]:
                            
in_util_removeprefix(var_name: str, prefix: str) -> str:

in_get_xforms_var_keys_PP(xforms: Union[tuple, None], 
                          vars: dict, 
                          prx: str, 
                          exclude_keys: tuple
                          ) -> Union[list[str], None]:

in_util_typemaker(data: list) -> Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4]:

in_get_idx_by_key(key: str) -> Union[int, None]:

in_util_flam3h_prx_mode(mode: int) -> tuple[str, str]:

in_set_affine(mode: int, 
              node: hou.SopNode, 
              prx: str, 
              apo_data: in_flame_iter_data, 
              flam3h_prm_names: flam3h_iterator_prm_names, 
              mp_idx: int
              ) -> None:

in_set_data(mode: int, 
            node: hou.SopNode, 
            prx: str, 
            apo_data: list, 
            prm_name: str, 
            mp_idx: int
            ) -> None:

in_prm_name_exceptions(v_type: int, app: str, apo_prm: tuple) -> tuple:

def in_get_var_name_from_dict(mydict: dict, idx: int) -> str:

in_v_parametric_var_collect(node: hou.SopNode, 
                            mode: int, 
                            apo_prm: tuple, 
                            xform: dict, 
                            mp_idx: int, 
                            v_type: int, 
                            func: Callable) -> Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4]:

in_v_parametric(app: str, 
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

in_v_parametric_PRE(app: str, 
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

in_v_parametric_POST(app: str, 
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

in_v_parametric_PRE_FF(app: str, 
                       node: hou.SopNode, 
                       t_idx: int, 
                       xform: dict, 
                       v_type: int, 
                       v_weight: float, 
                       var_prm: tuple, 
                       apo_prm: tuple
                       ) -> None:

in_v_parametric_POST_FF(app: str, 
                        node: hou.SopNode, 
                        t_idx: int, 
                        xform: dict, 
                        v_type: int, 
                        v_weight: float, 
                        var_prm: tuple, 
                        apo_prm: tuple
                        ) -> None:

in_v_generic(mode: int, 
             node: hou.SopNode, 
             mp_idx: int, 
             t_idx: int, 
             v_type: int, 
             v_weight: float
             ) -> None:

in_v_generic_PRE(mode: int, 
                 node: hou.SopNode, 
                 mp_idx: int, 
                 t_idx: int, 
                 v_type: int, 
                 v_weight: float
                 ) -> None:

in_v_generic_POST(mode: int, 
                  node: hou.SopNode, 
                  mp_idx: int, 
                  t_idx: int, 
                  v_type: int, 
                  v_weight: float
                  ) -> None:

in_v_generic_PRE_FF(node: hou.SopNode, 
                    t_idx: int, 
                    v_type: int, 
                    v_weight: float
                    ) -> None:

in_v_generic_POST_FF(node: hou.SopNode, 
                     t_idx: int, 
                     v_type: int, 
                     v_weight: float
                     ) -> None:

in_v_pre_blur(mode: int, 
              node: hou.SopNode, 
              mp_idx: int, 
              pb_weights: tuple
              ) -> None:

in_util_check_negative_weight(node: hou.SopNode, w: float, v_type_name: str) -> float:

in_get_xforms_data_and_flam3h_vars_limit(mode: int, apo_data: in_flame_iter_data) -> tuple[tuple, int]:

in_get_preset_name_iternum(preset_name: str) -> Union[int, None]:

in_util_join_vars_grp(groups: list) -> str:

in_util_vars_flatten_unique_sorted(VARS_list: Union[list[str], list[list[str]]], func: Callable, capitalize=False) -> list[str]:

in_presets_in_isvalid_file_menu_label(node: hou.SopNode, preset_id: int) -> str:

in_set_iter_on_load(node: hou.SopNode, preset_id: int, clipboard: bool, flame_name_clipboard: str) -> int:

in_load_sensor_stats_msg(preset_id: int, apo_data: in_flame_iter_data) -> str:

in_load_render_stats_msg(preset_id: int, apo_data: in_flame_iter_data) -> str:

in_copy_render_all_stats_msg(kwargs: dict, clipboard=False, apo_data=None) -> None:

in_copy_sensor_stats_msg(kwargs: dict) -> None:

in_copy_render_stats_msg(kwargs: dict) -> None:

in_util_vars_dict_type_maker(vars_dict: dict, func: Callable) -> dict:

METHODS:

in_flam3h_set_iterators(self, 
                        mode: int, 
                        node: hou.SopNode, 
                        apo_data: in_flame_iter_data, 
                        preset_id: int, 
                        exclude_keys: tuple
                        ) -> None:
                    

in_load_stats_msg(self, clipboard: bool, preset_id: int, apo_data: in_flame_iter_data) -> str:

menu_in_presets_data(self) -> list:

menu_in_presets(self) -> list:

menu_in_presets_empty_data(self) -> list:

menu_in_presets_empty(self) -> list:

set_iter_on_load_callback(self) -> None:

use_iter_on_load_callback(self) -> None:

in_to_flam3h_toggle(self, prm: str) -> None:

in_to_flam3h_toggle_pgb(self) -> None:

in_to_flam3h_toggle_f3h_affine(self) -> None:

in_to_flam3h_reset_user_data(self) -> None:

in_to_flam3h_reset_iterators_parms(self, node: hou.SopNode, in_flame_iter_count: int) -> None:

in_to_flam3h_init_data_ALT(self, node: hou.SopNode) -> tuple[Union[str, None], bool, int, str, bool]:

in_to_flam3h_init_data_SHIFT(self, node: hou.SopNode) -> tuple[Union[str, None], bool, int, str, bool]:

in_to_flam3h_init_data(self, node: hou.SopNode) -> tuple[Union[str, None], bool, int, str, bool, bool]:

in_to_flam3h_sys(self) -> None:

in_to_flam3h(self) -> None:

reset_IN(self, mode=0) -> None:

    """
    
    def __init__(self, kwargs: dict) -> None:
        self._kwargs = kwargs
        self._node = kwargs['node']
        
        
    @staticmethod
    def in_util_key_name_isalnum(key_name: str) -> str:
        return ''.join(letter for letter in key_name.strip() if letter.isalnum())
    
    
    @staticmethod
    def in_util_make_NULL(name: Union[str, list[str], tuple[str]]) -> Union[str, list[str], tuple[str]]:
        """This definition is used as a place holder.

        Args:
            name (Union[str, list[str], tuple[str]]): name or names to convert.

        Returns:
            Union[Union[str, list[str]], None]: The untouched name's value passed in as argument.
        """       
        return name


    @staticmethod
    def in_util_make_VAR(name: Union[str, list[str], tuple[str]]) -> Union[Union[str, list[str]], None]:
        """Convert a PRE or POST variation name into a variation name.

        Args:
            name (Union[str, list[str], tuple[str]]): name or names to convert.

        Returns:
            Union[Union[str, list[str]], None]: A converted str, list[str], tuple[str] of variation's names.
        """        
        if type(name) is str:
            if name.startswith(V_PRX_PRE):
                return re_sub(REGEX_PRE, '', name)
            elif name.startswith(V_PRX_POST):
                return re_sub(REGEX_POST, '', name)
            else:
                return name
        elif type(name) is list or tuple:
            _names = [re_sub(REGEX_PRE, '', x) for x in name if x.startswith(V_PRX_PRE) is True]
            if not _names:
                _names = [re_sub(REGEX_POST, '', x) for x in name if x.startswith(V_PRX_POST) is True]
            if not _names:
                return None
            else:
                return _names
        else:
            return None


    @staticmethod
    def in_util_make_PRE(name: Union[str, Union[list[str], KeysView], tuple[str]]) -> Union[str, list[str], None]:
        """Convert a variation name into a variation PRE variation name.

        Args:
            name (Union[str, list[str], tuple[str]]): name or names to convert.

        Returns:
            Union[Union[str, list[str]], None]: A converted str, list[str], tuple[str] of variation's names.
        """  
        if type(name) is str:
            if not (name.startswith(V_PRX_PRE) and name.startswith(V_PRX_POST)):
                return V_PRX_PRE + name
        elif type(name) is list or tuple:
            return [V_PRX_PRE + x for x in name if x.startswith(V_PRX_PRE) is False and x.startswith(V_PRX_POST) is False]
        else:
            return None


    @staticmethod
    def in_util_make_POST(name: Union[str, Union[list[str], KeysView], tuple[str]]) -> Union[str, list[str], None]:
        """Convert a variation name into a variation POST variation name.

        Args:
            name (Union[str, list[str], tuple[str]]): name or names to convert.

        Returns:
            Union[Union[str, list[str]], None]: A converted str, list[str], tuple[str] of variation's names.
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
            preset_id (int): The loaded flame preset idx
            apo_data (in_flame_iter_data): The loaded flame preset data from the xml

        Returns:
            list: List of sorted uinknown variations if any
        """
        if apo_data.plugins[preset_id]:
            plugins = [p.strip() for p in str(apo_data.plugins[preset_id]).split(" ") if p]
        else:
            plugins = ()
        
        unknown = []
        if plugins:
            for var in plugins:
                if str(var).startswith(V_PRX_PRE):
                    name = str(in_flame_utils.in_util_make_VAR(var)).lower()
                    if name not in VARS_FRACTORIUM_DICT[name[0]]:
                        unknown.append(var.capitalize())
                elif str(var).startswith(V_PRX_POST):
                    name = str(in_flame_utils.in_util_make_VAR(var)).lower()
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
            xml (str): the xml file to load from.

        Returns:
            bool: attempt_to_load_from_clipboard ( bool ): Is it a Chaotica's flame preset ? True or False.
        """ 
        try:
            tree = lxmlET.parse(xml) # type: ignore
        except:
            tree = None
              
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

        Returns:
            bool: attempt_to_load_from_clipboard ( bool ): Is it a Chaotica's flame preset ? True or False.
        """     
        xml = hou.ui.getTextFromClipboard() # type: ignore
        try:
            tree = lxmlET.ElementTree(lxmlET.fromstring(xml)) # type: ignore
        except:
            tree = None
        
        if tree is not None:
            if XML_VALID_CHAOS_ROOT_TAG in tree.getroot().tag.lower():
                return True
            else:
                return False
        else:
            return False



    
    @staticmethod
    def in_get_xforms_var_keys( xforms: Union[tuple, None], 
                                vars: Union[str, list[str], tuple[str], dict[str, int], dict[str, tuple], KeysView, None], 
                                exclude_keys: tuple
                                ) -> Union[list, None]:
        """Return a list of all the variation names included in all xforms compared against the available FLAM3H variations.
        This is used to find variation names and PRE and POST variation names based on the provided vars argument.
        
        Use this with everything but not PRE and POST dictionary lookup, use def in_get_xforms_var_keys_PP() instead
        
        Args:
            xforms (tuple): [list of all xforms contained inside this flame. This can be iterator's xforms or FF xform]

        Returns:
            Union[tuple[list, list], tuple[None, None]]: [return a list of variation's names in each xform,  or None]
        """    
        if xforms is not None:
            if type(vars) is dict:
                return [list(map(lambda x: x, filter(lambda x: x in vars.get(x[0]), filter(lambda x: x not in exclude_keys, xf.keys())))) for xf in xforms] # type: ignore
            else:
                return [list(map(lambda x: x, filter(lambda x: x in vars, filter(lambda x: x not in exclude_keys, xf.keys())))) for xf in xforms] # type: ignore
        else:
            return None
        
        
    @staticmethod
    def in_util_removeprefix(var_name: str, prefix: str) -> str:
        """Remove any prefix, if a prefix is present, from a variation name.
    ex: from: pre_linear to: linear
    ex: from post_mobius to: mobius
    
        Args:
            var_name (str): the variation name to remove the prefix from
            prefix (str): the prefix to check

        Returns:
            str: a variation name without the prefix, or the original variation name if it did not have any prefix. 
        """
        if var_name.startswith(prefix):
            return var_name[len(prefix):]
        else:
            return var_name[:]
        
        
    @staticmethod 
    def in_get_xforms_var_keys_PP(xforms: Union[tuple, None], 
                                vars: dict, 
                                prx: str, 
                                exclude_keys: tuple
                                ) -> Union[list, None]:
        """find a PRE or POST variation inside the currently processed xform/iterator. All xforms are passed in.

        Args:
            xforms (Union[tuple, None]): All the xforms of this flame. This can be iterator's xforms or FF xform.
            vars (dict): the variations we are searching for
            prx (str): the current type of the variation expressed as a prefix: "pre" or "post"
            exclude_keys (tuple): exclude those keys inside the current xform/iterator from the search to speed up a little

        Returns:
            Union[list[str], None]: return the a list of variations found using the prefix criteria
        """  
        if xforms is not None:
            return [list(map(lambda x: x, filter(lambda x: x in vars.get(in_flame_utils.in_util_removeprefix(x, prx)[0]), filter(lambda x: x.startswith(prx), filter(lambda x: x not in exclude_keys, xf.keys()))))) for xf in xforms] # type: ignore
        else:
            return None
        
        
    @staticmethod
    def in_util_typemaker(data: list) -> Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4]:
        """Based on how many element in the passed list return the proper type of data.
        
        Args:
            data (list): [a list of floats containinig the current parameter values to be converted into hou types]

        Returns:
            Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4]: [Based on how many element in the passed list return the proper type of data]
        """
        len_data = len(data)
        if len_data == 1:
            return float(data[0])
        elif len_data == 2:
            return hou.Vector2((data))
        elif len_data == 3:
            return hou.Vector3((data))
        elif len_data == 4:
            return hou.Vector4((data))
        else:
            return data
        
        
    @staticmethod  
    def in_get_idx_by_key(key: str) -> Union[int, None]:
        """Return the variation idx based on its name from the variation's dictionary.
        
        Args:
            key (str): [variation name we are processing]

        Returns:
            Union[int, None]: [return variation idx from the tuple look up table]
        """
        try: idx = VARS_FLAM3_DICT_IDX.get(key)
        except: return None
        return idx
        
        
    @staticmethod
    def in_util_flam3h_prx_mode(mode: int) -> tuple[str, str]:
        """Set a prefix based on modes ( iterator, FF, FF PRE/POST )
        Args:
            mode (int): [0 for iterator and 1 for FF]

        Returns:
            tuple[str, str]: [return parameter prefix based on mode: Iterator, FF, FF POST]
        """
        prx = ""
        prx_prm = ""
        if mode == 1:
            prx = PRX_FF_PRM
            prx_prm = f"{PRX_FF_PRM}_"
        if mode == 2:
            prx = PRX_FF_PRM
            prx_prm = f"{PRX_FF_PRM_POST}_"
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
            mode (int): [0 for iterator. 1 for FF]
            node (hou.SopNode): [Current FLAM3H node]
            prx (str): [parameter name prefix]
            apo_data (in_flame_iter_data): [Apophysis XML data collection from: class[in_flame_iter_data]]
            n (flam3h_iterator_prm_names): [FLAM3H node iterator parameter's names from: class[in_flame_iter_data]]
            mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        """
        idx = str(mp_idx+1)
        pre_affine = (flam3h_prm_names.preaffine_x, flam3h_prm_names.preaffine_y, flam3h_prm_names.preaffine_o)
        post_affine = (flam3h_prm_names.postaffine_x, flam3h_prm_names.postaffine_y, flam3h_prm_names.postaffine_o)
        f3h_affine = node.parm(IN_FLAM3H_AFFINE_STYLE).eval()
        
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
                    [node.setParms({f"{prx}{pre_affine[id]}": [hou.Vector2((tuple( [0, 0, 0, 0, 0, 0][i:i+2] ))) for i in (0, 2, 4)][id]}) for id in range(3)] # type: ignore
                
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
                if apo_data.coefs[mp_idx] and apo_data.coefs[mp_idx] is not None:
                    # The affine XML key: "coefs" must always be present in the XML file.
                    [node.setParms({f"{prx}{pre_affine[id]}_{idx}": apo_data.coefs[mp_idx][id]}) for id in range(3)] # type: ignore
                else:
                    # If not present, we set all the pre affine values for this iterator to a value of: 0(Zero)
                    # Doing so it wont error out on load and it will act as a warning sign.
                    [node.setParms({f"{prx}{pre_affine[id]}_{idx}": [hou.Vector2((tuple( [0, 0, 0, 0, 0, 0][i:i+2] ))) for i in (0, 2, 4)][id]}) for id in range(3)] # type: ignore
                
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
                    apo_data: list, 
                    prm_name: str, 
                    mp_idx: int
                    ) -> None:
        """Set single parameter data value from the loaded flame preset.
        An example of the parameter you will set using this function are:
        
        main_note
        main_weight
        shader_speed
        shader_color
        shader_alpha
        xaos
        ...
        
        Args:
            mode (int): [0 for iterator. 1 for FF]
            node (hou.SopNode): [Current FLAM3H node]
            prx (str): [parameter name prefix]
            apo_data (in_flame_iter_data): [Apophysis XML data collection from: class[in_flame_iter_data]]
            prm_name (str): [parameter name for the current data we want to set]
            mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        """
        if mode:
            pass
        else:
            if apo_data is not None:
                n = flam3h_iterator_prm_names
                if prm_name not in [n.shader_alpha, n.main_weight]:
                    if apo_data[mp_idx]:
                        node.setParms({f"{prx}{prm_name}_{str(mp_idx+1)}": apo_data[mp_idx]}) # type: ignore
                else:
                    node.setParms({f"{prx}{prm_name}_{str(mp_idx+1)}": apo_data[mp_idx]}) # type: ignore
           
           
    @staticmethod  
    def in_prm_name_exceptions(v_type: int, app: str, apo_prm: tuple) -> tuple:
        """Some software have variation names and parameters names different from FLAM3H and Apophysis.
        This will take care of those special cases.
        It will swap the current variation dictionary item with the one the posses the corret names.

        Args:
            v_type (int): The current variation we are processing
            app (str): The software used to generate the loaded flame preset.
            apo_prm (tuple): If no exception is found, return the original variation and parameter's names.

        Returns:
            tuple: _description_
        """        
        if app.startswith(XML_APP_NAME_FRACTORIUM):
            check = flam3h_varsPRM_APO.varsPRM_FRACTORIUM_EXCEPTIONS.get(v_type)
            if check is not None:
                return check
            else:
                return apo_prm
        else:
            return apo_prm
        
        
    @staticmethod
    def in_get_var_name_from_dict(mydict: dict, idx: int) -> str:
        """Get the current variation string name from its index.

        Args:
            mydict (dict): The dictionary for lookup
            idx (int): The variation index to retrieve its string name from.

        Returns:
            str: The variation string name.
        """       
        var_name = list(mydict.keys())[list(mydict.values()).index(idx)] 
        return var_name
    
    
    @staticmethod
    def in_v_parametric_var_collect(node: hou.SopNode, 
                                    mode: int, 
                                    apo_prm: tuple, 
                                    xform: dict, 
                                    mp_idx: int, 
                                    v_type: int, 
                                    func: Callable) -> Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4]:
        """Every parametric variation posses a certain number of parameters to control its behavior.
        In FLAM3H, those parameters have been grouped into a single data type.
        For example the Curl variation posses two parametric parameters: c1, c2
        Those two parameters have been packed into a vector2 data type: vector2[c1, c2].
        This has been done to help with performance as querying many, many different parameters did end up being costly,
        especially considering having many iterators each with parametric variations at the same time.
        
        Args:
            node (hou.SopNode): [Current FLAM3H node]
            mode (int): [0 for iterator. 1 for FF]
            apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3h_varsPRM_APO.varsPRM[v_type]]
            xform (dict): [current xform we are processing to the relative key names and values for the iterator]
            mp_idx (int): [for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
            v_type (int): [the current variation type index]
            func (Callable): [function to change variation name between var, pre_var and post_var]
        
        Returns:
            tuple: Expected data type of the collected parametric variation's parameters values.
        """   
        
        iter_type = f"Iterator.{mp_idx+1}"
        if mode:
            iter_type = 'FF'

        VAR: list = []
        for names in apo_prm[1:-1]:
            var_prm_vals: list = []
            for n in [x.lower() for x in names]:
                # If one of the FLAM3H parameter is not in the xform, skip it and set it to ZERO for now.
                n = func(n)
                if xform.get(n) is not None:
                    var_prm_vals.append(float(in_flame.xf_val_cleanup_str(str(xform.get(n)))))
                else:
                    # If a variation parameter FLAM3H has is not found, set it to ZERO. Print its name to let us know if not inside XML_XF_PRM_EXCEPTION
                    if n not in XML_XF_PRM_EXCEPTION:
                        var_prm_vals.append(float(0))
                        print(f"{node.name()}: PARAMETER NOT FOUND: {iter_type}: variation: \"{func(in_flame_utils.in_get_var_name_from_dict(VARS_FLAM3_DICT_IDX, v_type))}\": parameter: \"{func(n)}\"")
                        
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
            app (str): [What software were used to generate this flame preset]
            mode (int): [0 for iterator. 1 for FF]
            node (hou.SopNode): [Current FLAM3H node]
            mp_idx (int): [for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
            t_idx (int): [current variation number idx to use with: flam3h_iterator.sec_varsT, flam3h_iterator.sec_varsW]
            xform (dict): [current xform we are processing to the relative key names and values for the iterator]
            v_type (int): [the current variation type index]
            weight (float): [the current variation weight]
            var_prm (tuple): [tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM.varsPRM[v_type]]
            apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3h_varsPRM_APO.varsPRM[v_type]]
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)

        VAR = in_flame_utils.in_v_parametric_var_collect(node, 
                                                         mode, 
                                                         apo_prm, 
                                                         xform, 
                                                         mp_idx, 
                                                         v_type, 
                                                         in_flame_utils.in_util_make_NULL)

        mpidx = str(mp_idx+1)
        [node.setParms({f"{prx_prm}{prm[0][:-1]}": VAR[idx]}) if mode else node.setParms({f"{prx_prm}{prm[0]}{mpidx}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        if mode:
            node.setParms({f"{prx}{flam3h_iterator.sec_varsT[t_idx][:-1]}": v_type}) # type: ignore
            node.setParms({f"{prx}{flam3h_iterator.sec_varsW[t_idx][0][:-1]}": v_weight}) # type: ignore
        else:
            node.setParms({f"{prx}{flam3h_iterator.sec_varsT[t_idx]}{mpidx}": v_type}) # type: ignore
            node.setParms({f"{prx}{flam3h_iterator.sec_varsW[t_idx][0]}{mpidx}": v_weight}) # type: ignore
            
            
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
            app (str): [What software were used to generate this flame preset]
            mode (int): [0 for iterator. 1 for FF]
            node (hou.SopNode): [Current FLAM3H node]
            mp_idx (int): [for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
            t_idx (int): [current variation number idx to use with: flam3h_iterator.sec_prevarsT, flam3h_iterator.sec_prevarsW]
            xform (dict): [current xform we are processing to the relative key names and values for the iterator]
            v_type (int): [the current variation type index]
            weight (float): [the current variation weight]
            var_prm (tuple): [tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM.varsPRM[v_type]]
            apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3h_varsPRM_APO.varsPRM[v_type]]
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)
        
        VAR = in_flame_utils.in_v_parametric_var_collect(node, 
                                                         mode, 
                                                         apo_prm, 
                                                         xform, 
                                                         mp_idx, 
                                                         v_type, 
                                                         in_flame_utils.in_util_make_PRE)
        
        mpidx = str(mp_idx+1)
        [node.setParms({f"{prx_prm}{prm[0]}{mpidx}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        # Only on pre variations with parametric so:
        node.setParms({f"{prx}{flam3h_iterator.sec_prevarsT[t_idx]}{mpidx}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3h_iterator.sec_prevarsW[1:][t_idx][0]}{mpidx}": v_weight}) # type: ignore 


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
            app (str): [What software were used to generate this flame preset]
            mode (int): [0 for iterator. 1 for FF]
            node (hou.SopNode): [Current FLAM3H node]
            mp_idx (int): [for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
            t_idx (int): [current variation number idx to use with: flam3h_iterator.sec_postvarsT, flam3h_iterator.sec_postvarsW]
            xform (dict): [current xform we are processing to the relative key names and values for the iterator]
            v_type (int): [the current variation type index]
            weight (float): [the current variation weight]
            var_prm (tuple): [tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM.varsPRM[v_type]]
            apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3h_varsPRM_APO.varsPRM[v_type]]
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)

        VAR = in_flame_utils.in_v_parametric_var_collect(node, 
                                                         mode, 
                                                         apo_prm, 
                                                         xform, 
                                                         mp_idx, 
                                                         v_type, 
                                                         in_flame_utils.in_util_make_POST)
        
        mpidx = str(mp_idx+1)
        [node.setParms({f"{prx_prm}{prm[0]}{mpidx}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        # Only on post variation with parametric so:
        node.setParms({f"{prx}{flam3h_iterator.sec_postvarsT[t_idx]}{mpidx}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3h_iterator.sec_postvarsW[t_idx][0]}{mpidx}": v_weight}) # type: ignore
    
    
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
            app (str): [What software were used to generate this flame preset]
            node (hou.SopNode): [Current FLAM3H houdini node]
            t_idx (int): [current variation number idx to use with: flam3h_iterator.sec_prevarsT_FF, flam3h_iterator.sec_prevarsW_FF]
            xform (dict): [current xform we are processing to the relative key names and values for the iterator]
            v_type (int): [the current variation type index]
            weight (float): [the current variation weight]
            var_prm (tuple): [tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM.varsPRM[v_type]]
            apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3h_varsPRM_APO.varsPRM[v_type]]
        """
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)

        VAR = in_flame_utils.in_v_parametric_var_collect(node, 
                                                         0, 
                                                         apo_prm, 
                                                         xform, 
                                                         0, 
                                                         v_type, 
                                                         in_flame_utils.in_util_make_PRE)
            
        [node.setParms({f"{PRX_FF_PRM_POST}_{prm[0][0:-1]}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        # Only on post variation with parametric so:
        node.setParms({f"{flam3h_iterator_FF.sec_prevarsT_FF[t_idx]}": v_type}) # type: ignore
        node.setParms({f"{flam3h_iterator_FF.sec_prevarsW_FF[t_idx][0]}": v_weight}) # type: ignore


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
            app (str): [What software were used to generate this flame preset]
            node (hou.SopNode): [Current FLAM3H node]
            t_idx (int): [current variation number idx to use with: flam3h_iterator.sec_postvarsT_FF, flam3h_iterator.sec_postvarsW_FF]
            xform (dict): [current xform we are processing to the relative key names and values for the iterator]
            v_type (int): [the current variation type index]
            weight (float): [the current variation weight]
            var_prm (tuple): [tuple of FLAM3H node parameteric parameters names: flam3h_varsPRM.varsPRM[v_type]]
            apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3h_varsPRM_APO.varsPRM[v_type]]
        """
        # Exceptions: check if this flame need different parameters names based on detected exception
        apo_prm = in_flame_utils.in_prm_name_exceptions(v_type, app.upper(), apo_prm)

        VAR = in_flame_utils.in_v_parametric_var_collect(node, 
                                                         0, 
                                                         apo_prm, 
                                                         xform, 
                                                         0, 
                                                         v_type, 
                                                         in_flame_utils.in_util_make_POST)
            
        [node.setParms({f"{PRX_FF_PRM_POST}_{prm[0][0:-1]}": VAR[idx]}) for idx, prm in enumerate(var_prm[1:-1])] # type: ignore
        # Only on post variation with parametric so:
        node.setParms({f"{flam3h_iterator_FF.sec_postvarsT_FF[t_idx]}": v_type}) # type: ignore
        node.setParms({f"{flam3h_iterator_FF.sec_postvarsW_FF[t_idx][0]}": v_weight}) # type: ignore


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
            mode (int): [0 for iterator. 1 for FF]
            node (hou.SopNode): [Current FLAM3H node]
            mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
            t_idx (int): [Current variation number idx to use with: flam3h_iterator.sec_prevarsT, flam3h_iterator.sec_prevarsW]
            v_type (int): [Current variation type index]
            weight (float): [Current variation weight]
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)

        if mode:
            node.setParms({f"{prx}{flam3h_iterator.sec_varsT[t_idx][:-1]}": v_type}) # type: ignore
            node.setParms({f"{prx}{flam3h_iterator.sec_varsW[t_idx][0][:-1]}": v_weight}) # type: ignore
        else:
            idx = str(mp_idx+1)
            node.setParms({f"{prx}{flam3h_iterator.sec_varsT[t_idx]}{idx}": v_type}) # type: ignore
            node.setParms({f"{prx}{flam3h_iterator.sec_varsW[t_idx][0]}{idx}":v_weight}) # type: ignore


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
            mode (int): [0 for iterator. 1 for FF]
            node (hou.SopNode): [Current FLAM3H node]
            mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
            t_idx (int): [Current variation number idx to use with: flam3h_iterator.sec_prevarsT, flam3h_iterator.sec_prevarsW]
            v_type (int): [Current variation type index]
            weight (float): [Current variation weight]
        """
        idx = str(mp_idx+1)
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        node.setParms({f"{prx}{flam3h_iterator.sec_prevarsT[t_idx]}{idx}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3h_iterator.sec_prevarsW[1:][t_idx][0]}{idx}":v_weight}) # type: ignore


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
            mode (int): [0 for iterator. 1 for FF]
            node (hou.SopNode): [Current FLAM3H node]
            mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
            t_idx (int): [Current variation number idx to use with: flam3h_iterator.sec_prevarsT, flam3h_iterator.sec_prevarsW]
            v_type (int): [Current variation type index]
            weight (float): [Current variation weight]
        """
        idx = str(mp_idx+1)
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        node.setParms({f"{prx}{flam3h_iterator.sec_postvarsT[t_idx]}{idx}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3h_iterator.sec_postvarsW[t_idx][0]}{idx}":v_weight}) # type: ignore


    @staticmethod
    def in_v_generic_PRE_FF(node: hou.SopNode, 
                            t_idx: int, 
                            v_type: int, 
                            v_weight: float
                            ) -> None:
        """Set a FLAM3H FF PRE variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        
        Args:
            node (hou.SopNode): [Current FLAM3H node]
            t_idx (int): [Current variation number idx to use with: flam3h_iterator.sec_prevarsT, flam3h_iterator.sec_prevarsW]
            v_type (int): [Current variation type index]
            weight (float): [Current variation weight]
        """
        node.setParms({f"{flam3h_iterator_FF.sec_prevarsT_FF[t_idx]}": v_type}) # type: ignore
        node.setParms({f"{flam3h_iterator_FF.sec_prevarsW_FF[t_idx][0]}":v_weight}) # type: ignore


    @staticmethod
    def in_v_generic_POST_FF(node: hou.SopNode, 
                             t_idx: int, 
                             v_type: int, 
                             v_weight: float
                             ) -> None:
        """Set a FLAM3H FF POST variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        
        Args:
            node (hou.SopNode): [Current FLAM3H node]
            t_idx (int): [Current variation number idx to use with: flam3h_iterator.sec_prevarsT, flam3h_iterator.sec_prevarsW]
            v_type (int): [Current variation type index]
            weight (float): [Current variation weight]
        """
        node.setParms({f"{flam3h_iterator_FF.sec_postvarsT_FF[t_idx]}": v_type}) # type: ignore
        node.setParms({f"{flam3h_iterator_FF.sec_postvarsW_FF[t_idx][0]}":v_weight}) # type: ignore


    @staticmethod
    def in_v_pre_blur(mode: int, 
                      node: hou.SopNode, 
                      mp_idx: int, 
                      pb_weights: tuple
                      ) -> None:
        """Set a FLAM3H pre_blur variation parameter data from the corresponding data found in the loaded XML Flame preset xform.
        
        Args:
            mode (int): [0 for iterator. 1 for FF]
            node (hou.SopNode): [Current FLAM3H node]
            mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
            pb_weights (tuple): [all iterators pre_blur weight values]
        """
        prx, prx_prm = in_flame_utils.in_util_flam3h_prx_mode(mode)
        if mode: pass
        else:
            if pb_weights[mp_idx]:
                node.setParms({f"{prx}{flam3h_iterator_prm_names.prevar_weight_blur}_{str(mp_idx+1)}": pb_weights[mp_idx]}) # type: ignore


    @staticmethod
    def in_util_check_negative_weight(node: hou.SopNode, w: float, v_type_name: str) -> float:
        """FLAM3H do not allow negative variation's weights for the PRE and POST variations.
        This function will turn a negative weight into its absoulute value instead.

        Args:
            node (hou.SopNode): FLAM3H node
            w (float): The variation weight to check.
            v_type_name (str): The name of the variation to print out if it turn out to have its weight with a negative value.

        Returns:
            float: _description_
        """        
        if w < 0:
            print(f"{node.name()} warning:\n{v_type_name.upper()} variation weight value: {w}\nNegative weight not allowed in PRE or POST vars.\nUsing its absolute value instead: {abs(w)}\n")
            return abs(w)
        else: return w


    @staticmethod
    def in_get_xforms_data_and_flam3h_vars_limit(mode: int, apo_data: in_flame_iter_data) -> tuple[tuple, int]:
        """Get all the xforms data based on mode ( iterator or FF ),
        and get all the allowed variations to be used based on mode ( iterator or FF ).

        Args:
            mode (int): iterator or FF
            apo_data (in_flame_iter_data): Flames data from the flame file loaded in: class: in_flame_iter_data()

        Returns:
            tuple[tuple, int]: _description_
        """        
        xf = ()
        _MAX_VARS = 0
        if mode:
            _MAX_VARS = MAX_FF_VARS
            xf = apo_data.finalxform
        else:
            _MAX_VARS = MAX_ITER_VARS
            xf = apo_data.xforms
        return xf, _MAX_VARS


    @staticmethod
    def in_get_preset_name_iternum(menu_label: str) -> Union[int, None]:
        """Get the iteration number from the loaded Flame preset if any.

        Args:
            preset_name (str): The Flame preset name.

        Returns:
            Union[int, None]: The iteration number or none.
        """        
        splt = list(menu_label.rpartition(FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV))
        if len([item for item in splt if item]) > 1:
            try: return int(splt[-1])
            except: return None
        else:
            return None


    @staticmethod
    def in_util_join_vars_grp(groups: list) -> str:
        """When formatting a message to print out we use groups as if they were each line of the meesage and join them.
        This function will avoid to have an extra empty line at the very end.

        Args:
            groups (list): The groups to join

        Returns:
            str: The final message without the extra empty line at the end.
        """     
        vars = [", ".join(grp) + "\n" if id < len(groups)-1 else ", ".join(grp) + "." for id, grp in enumerate(groups)]   
        return ''.join(vars)


    @staticmethod
    def in_util_vars_flatten_unique_sorted(VARS_list: Union[list[str], list[list[str]]], func: Callable, capitalize=False) -> list[str]:
        """Return a flattened list of unique and sorted items without duplicates.

        Args:
            VARS_list (Union[list[str], list[list[str]]]): The data to flatten, remove duplicates and sort.
            func (Callable): Function to turn variation names from VAR to PRE or POST or none based on the function provided.
            capitalize (bool): (default to: False) capitalize the variation's names if any are found.

        Returns:
            list[str]: Return a flattened list of unique and sorted items without duplicates.
        """        
        flatten = [item for sublist in VARS_list for item in sublist]
        result = []
        [result.append(x) for x in flatten if x not in result]
        sort = sorted(result, key=lambda var: var)
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
            node (hou.SopNode): This FLAM3H node
            preset_id (int): the menu preset selction index to use to retrive its menu label string

        Returns:
            str: The selected menu preset menu label string
        """

        toggle_PREFS_ENUMERATE_MENU = node.parm(PREFS_ENUMERATE_MENU).eval()
        
        if node.parm(IN_ISVALID_PRESET).evalAsInt():
            
            if node.parm(IN_CLIPBOARD_TOGGLE).evalAsInt():
                menu_label = str(node.parm(IN_PRESETS).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_FLAME_LOAD_CB)[-1].strip()
                # We are using "str.lstrip()" because the preset name has been "str.strip()" already in the above line.
                # and there are only the leading white spaces left from the menu enumaration index number string to remove.
                if toggle_PREFS_ENUMERATE_MENU:
                    return ':'.join(str(menu_label).split(':')[1:]).lstrip()
                else:
                    return menu_label
            else:
                menu_label = str(node.parm(IN_PRESETS).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_FLAME_LOAD)[-1].strip()
                # We are using "str.lstrip()" because the preset name has been "str.strip()" already in the above line.
                # and there are only the leading white spaces left from the menu enumaration index number string to remove.
                if toggle_PREFS_ENUMERATE_MENU:
                    return ':'.join(str(menu_label).split(':')[1:]).lstrip()
                else:
                    return menu_label
        else:
            menu_label = str(node.parm(IN_PRESETS_OFF).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_FLAME_LOAD_EMPTY)[-1].strip()
            # We are using "str.lstrip()" because the preset name has been "str.strip()" already in the above line.
            # and there are only the leading white spaces left from the menu enumaration index number string to remove.
            if toggle_PREFS_ENUMERATE_MENU:
                return ':'.join(str(menu_label).split(':')[1:]).lstrip()
            else:
                return menu_label
    
    
    @staticmethod
    def in_set_iter_on_load(node: hou.SopNode, preset_id: int, clipboard: bool, flame_name_clipboard: str) -> int:
        """When loading a FLame preset, set the FLAM3H iteration number
        to the value backed into the Flame preset name we just loaded.

        Args:
            node (hou.SopNode): FLAM3H houdini node
            preset_id (int): The Flame preset we loaded

        Returns:
            int: The iteration number to set. If none is found, use the default value of 64 to load this Flame preset.
        """        
        iter_on_load = node.parm(IN_ITER_NUM_ON_LOAD).eval()
        use_iter_on_load = node.parm(IN_USE_ITER_ON_LOAD).eval()
        
        if clipboard: preset_name = flame_name_clipboard
        else:
            # Get the correct menu parameter's preset menu label
            preset_name = in_flame_utils.in_presets_in_isvalid_file_menu_label(node, preset_id)
        
        iter_on_load_preset = in_flame_utils.in_get_preset_name_iternum(preset_name)
        if iter_on_load_preset is not None:
            # override iterations from the Flame preset name
            if use_iter_on_load and node.parm(IN_OVERRIDE_ITER_FLAME_NAME).eval():
                return node.parm(IN_ITER_NUM_ON_LOAD).evalAsInt()
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
            preset_id (int): The loaded XML Flame preset id to gather the data from.
            apo_data (in_flame_iter_data): The XML Flame file data

        Returns:
            str: A string to be used to set the IN Render properties data parameter message.
        """        
        # spacers
        nl = "\n"
        nnl = "\n\n"
        na = 'n/a'
        
        size = f'Resolution: {na}'
        if apo_data.out_size[preset_id]:
            size = f"Resolution: {apo_data.out_size[preset_id]}"
            
        center = f'Center: {na}'
        if apo_data.out_center[preset_id]:
            center = f"Center: {apo_data.out_center[preset_id]}"
            
        rotate = f'Rotate: {na}'
        if apo_data.out_rotate[preset_id]:
            rotate = f"Rotate: {apo_data.out_rotate[preset_id]}"

        scale = f'Scale: {na}'
        if apo_data.out_scale[preset_id]:
            scale = f"Scale: {apo_data.out_scale[preset_id]}"
        
        
        build = (size, nl,
                 center, nl,
                 rotate, nl,
                 scale, nl,
                 )
        
        build_render_stats_msg = "".join(build)
        return build_render_stats_msg


    
    @staticmethod
    def in_load_render_stats_msg(preset_id: int, apo_data: in_flame_iter_data) -> str:
        """Collect and write a summuary of the loaded IN Flame file preset render properties.

        Args:
            preset_id (int): The loaded XML Flame preset id to gather the data from.
            apo_data (in_flame_iter_data): The XML Flame file data

        Returns:
            str: A string to be used to set the IN Render properties data parameter message.
        """        
        # spacers
        nl = "\n"
        nnl = "\n\n"
        na = 'n/a'
        
        quality = f'Quality: {na}'
        if apo_data.out_quality[preset_id]:
            quality = f"Quality: {apo_data.out_quality[preset_id]}"

        brightness = f'Brightness: {na}'
        if apo_data.out_brightness[preset_id]:
            brightness = f"Brightness: {apo_data.out_brightness[preset_id]}"
            
        gamma = f'Gamma: {na}'
        if apo_data.out_gamma[preset_id]:
            gamma = f"Gamma: {apo_data.out_gamma[preset_id]}"
            
        highlight = f'Highlight power: {na}'
        if apo_data.out_highlight_power[preset_id]:
            highlight = f"Highlight power: {apo_data.out_highlight_power[preset_id]}"
            
        K2 = f'Logscale K2: {na}'
        if apo_data._out_logscale_k2[preset_id]:
            K2 = f"Logscale K2: {apo_data._out_logscale_k2[preset_id]}"
            
        vibrancy = f'Vibrancy: {na}'
        if apo_data.out_vibrancy[preset_id]:
            vibrancy = f"Vibrancy: {apo_data.out_vibrancy[preset_id]}"
        
        build = (quality, nl,
                 brightness, nl,
                 gamma, nl,
                 highlight, nl,
                 K2, nl,
                 vibrancy
                 )
        
        build_render_stats_msg = "".join(build)
        return build_render_stats_msg
    
    
    @staticmethod
    def in_copy_render_all_stats_msg(kwargs: dict, clipboard=False, apo_data=None) -> None:
        """Copy the loaded IN Flame preset ALL properties into the OUT Flame render properties to be written out. 

        Args:
            kwargs (hou.SopNode): houdini kwargs.
            clipboard (bool): True: load from clipboard. False: load from disk file.
            apo_data (in_flame_iter_data): The XML Flame file data to get the loaded preset data from.
        """        
        node = kwargs['node']

        if clipboard:
            preset_id = 0
            f3r = apo_data
        else:
            xml = node.parm(IN_PATH).evalAsString()
            
            # Get the correct menu parameter's preset idx
            if node.parm(IN_ISVALID_PRESET).evalAsInt():
                preset_id = int(node.parm(IN_PRESETS).eval())
            else:
                preset_id = int(node.parm(IN_PRESETS_OFF).eval())
                
            f3r = in_flame_iter_data(node, xml, preset_id)
            
        assert f3r is not None
        if f3r.isvalidtree:
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE): hou.Vector2((int(f3r.out_size[preset_id].split(" ")[0]), int(f3r.out_size[preset_id].split(" ")[1])))}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER): hou.Vector2((float(f3r.out_center[preset_id].split(" ")[0]), float(f3r.out_center[preset_id].split(" ")[1])))}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE): float(f3r.out_rotate[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE): float(f3r.out_scale[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY): int(f3r.out_quality[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS): float(f3r.out_brightness[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA): float(f3r.out_gamma[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER): float(f3r.out_highlight_power[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2): float(f3r._out_logscale_k2[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY): float(f3r.out_vibrancy[preset_id])}) # type: ignore
            except:
                pass
            
            node.setParms({OUT_RENDER_PROPERTIES_EDIT: 1}) # type: ignore
            
            if node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt():
                flam3h_general_utils(kwargs).util_set_clipping_viewers()
                flam3h_general_utils(kwargs).util_set_front_viewer()
                
            _MSG = f"IN Preset properties: COPIED"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
            flam3h_general_utils.flash_message(node, _MSG)
            
        else:
            pass


    @staticmethod
    def in_copy_sensor_stats_msg(kwargs: dict) -> None:
        """Copy the loaded IN Flame preset RENDER properties into the OUT Flame render properties to be written out. 

        Args:
            kwargs (hou.SopNode): houdini kwargs.
        """        
        node = kwargs['node']
        
        inisvalidfile = node.parm(IN_ISVALID_FILE).eval()
        inisvalidpreset = node.parm(IN_ISVALID_PRESET).eval()
        clipboard = node.parm(IN_CLIPBOARD_TOGGLE).eval()
        
        if inisvalidfile and inisvalidpreset and not clipboard:
            
            # Get the correct menu parameter's preset idx
            preset_id = int(node.parm(IN_PRESETS).eval())

            xml = node.parm(IN_PATH).evalAsString()
            f3r = in_flame_iter_data(node, xml, preset_id)
            
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE): hou.Vector2((int(f3r.out_size[preset_id].split(" ")[0]), int(f3r.out_size[preset_id].split(" ")[1])))}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER): hou.Vector2((float(f3r.out_center[preset_id].split(" ")[0]), float(f3r.out_center[preset_id].split(" ")[1])))}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE): float(f3r.out_rotate[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE): float(f3r.out_scale[preset_id])}) # type: ignore
            except:
                pass
            
            node.setParms({OUT_RENDER_PROPERTIES_EDIT: 1}) # type: ignore
            
            if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                flam3h_general_utils(kwargs).util_set_clipping_viewers()
                flam3h_general_utils(kwargs).util_set_front_viewer()
                
            _MSG = f"IN SENSOR settings: COPIED"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
            flam3h_general_utils.flash_message(node, _MSG)
            
        else:
            _MSG = f"Load a valid IN Preset first"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
            flam3h_general_utils.flash_message(node, _MSG)
        


    @staticmethod
    def in_copy_render_stats_msg(kwargs: dict) -> None:
        """Copy the loaded IN Flame preset SENSOR properties into the OUT Flame render properties to be written out. 

        Args:
            kwargs (hou.SopNode): houdini kwargs.
        """        
        node = kwargs['node']
        
        inisvalidfile = node.parm(IN_ISVALID_FILE).eval()
        inisvalidpreset = node.parm(IN_ISVALID_PRESET).eval()
        clipboard = node.parm(IN_CLIPBOARD_TOGGLE).eval()
        
        if inisvalidfile and inisvalidpreset and not clipboard:
            
            # Get the correct menu parameter's preset idx
            preset_id = int(node.parm(IN_PRESETS).eval())

            xml = node.parm(IN_PATH).evalAsString()
            f3r = in_flame_iter_data(node, xml, preset_id)
                
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY): int(f3r.out_quality[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS): float(f3r.out_brightness[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA): float(f3r.out_gamma[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER): float(f3r.out_highlight_power[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2): float(f3r._out_logscale_k2[preset_id])}) # type: ignore
            except:
                pass
            try: node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY): float(f3r.out_vibrancy[preset_id])}) # type: ignore
            except:
                pass
            
            node.setParms({OUT_RENDER_PROPERTIES_EDIT: 1}) # type: ignore
            
            if node.parm(OUT_RENDER_PROPERTIES_SENSOR).eval():
                flam3h_general_utils(kwargs).util_set_clipping_viewers()
                flam3h_general_utils(kwargs).util_set_front_viewer()
                
            _MSG = f"IN RENDER settings: COPIED"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'IMP')
            flam3h_general_utils.flash_message(node, _MSG)
            
        else:
            _MSG = f"Load a valid IN Preset first"
            flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
            flam3h_general_utils.flash_message(node, _MSG)


        
    @staticmethod
    def in_util_vars_dict_type_maker(vars_dict: dict, func: Callable) -> dict:
        return dict(map(lambda item: (item[0], func(item[1])), vars_dict.items()))




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
        
        kwargs = self.kwargs
        if kwargs["ctrl"]:
            self.in_copy_render_stats_msg(kwargs)
        else:
            self.in_copy_sensor_stats_msg(kwargs)
    
    
    def in_flam3h_set_iterators(self, 
                                mode: int, 
                                node: hou.SopNode, 
                                apo_data: in_flame_iter_data, 
                                preset_id: int, 
                                exclude_keys: tuple
                                ) -> None:
        """Set the FLAM3H iterators/FF parameters based on collected XML data from the flame file loaded.
        
    The collection of XML data happen inside: class: in_flame_iter_data()

        Args:
            mode (int): iterator or FF
            node (hou.SopNode): FLAM3H node
            apo_data (in_flame_iter_data): Flames data from the flame file loaded in: class: in_flame_iter_data()
            preset_id (int): the flame preset we are loading out of all the presets included in the flame file
            exclude_keys (tuple): exclude those keys inside the current xform/iterator from the search to speed up a little
        """ 
        
        # timenow = datetime.now().strftime('%b-%d-%Y %H:%M:%S')
        
        xforms, _MAX_VARS_MODE = self.in_get_xforms_data_and_flam3h_vars_limit(mode, apo_data)
        
        vars_keys = self.in_get_xforms_var_keys(xforms, VARS_FLAM3_DICT_IDX.keys(), exclude_keys)
        assert vars_keys is not None
        vars_keys_pre = self.in_get_xforms_var_keys(xforms, self.in_util_make_PRE(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)
        assert vars_keys_pre is not None
        vars_keys_post = self.in_get_xforms_var_keys(xforms, self.in_util_make_POST(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)
        assert vars_keys_post is not None

        app = apo_data.sw_version[preset_id]
        var_prm: tuple = flam3h_varsPRM.varsPRM
        apo_prm: tuple = flam3h_varsPRM_APO.varsPRM
        iterator_names = flam3h_iterator_prm_names()
        prx, prx_prm = self.in_util_flam3h_prx_mode(mode)
        
        # Set variations ( iterator and FF )
        for mp_idx, xform in enumerate(xforms):
            
            iterator_vars_skipped = []
            FF_vars_skipped = []
            
            # Collect iterator or FF vars in excess  
            if len(vars_keys[mp_idx]) > _MAX_VARS_MODE:
                if mode:
                    FF_vars_skipped.append(f"\n\t\tFF VAR -> {', '.join(vars_keys[mp_idx][_MAX_VARS_MODE:])}")
                else:
                    iterator_vars_skipped.append(f"\n\t\tVAR -> {', '.join(vars_keys[mp_idx][_MAX_VARS_MODE:])}")
            
            # in case of an iterator only the first 4. In case of an FF only the first 2
            for t_idx, key_name in enumerate(vars_keys[mp_idx][:_MAX_VARS_MODE]):
                v_type = self.in_get_idx_by_key(key_name)
                if v_type is not None:
                    v_weight = float(xform.get(key_name))
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
                    self.in_v_generic(mode, node, mp_idx, t_idx, 0, 0)
                    
            # Set pre blur if found
            self.in_v_pre_blur(mode, node, mp_idx, apo_data.pre_blur)
                    
            if mode:
                # Set finalxform name first if any
                if apo_data.finalxform_name[0]:
                    node.setParms({f"{prx}{iterator_names.main_note}": apo_data.finalxform_name[0]}) # type: ignore
                    
                # Collect FF PRE vars in excess  
                if len(vars_keys_pre[mp_idx]) > MAX_FF_VARS_PRE:
                    if FF_vars_skipped:
                        FF_vars_skipped.insert(0, f"\n\t\tFF PRE -> {', '.join(vars_keys_pre[mp_idx][MAX_FF_VARS_PRE:])}")
                    else:
                        FF_vars_skipped.append(f"\n\t\tFF PRE -> {', '.join(vars_keys_pre[mp_idx][MAX_FF_VARS_PRE:])}")
                    
                # FF PRE vars ( only the first one in "vars_keys_pre[mp_idx]" will be kept )
                if vars_keys_pre[mp_idx]: # type: ignore
                    for t_idx, key_name in enumerate(vars_keys_pre[mp_idx][:MAX_FF_VARS_PRE]):
                        v_type = self.in_get_idx_by_key(self.in_util_make_VAR(key_name)) # type: ignore
                        if v_type is not None:
                            w = float(xform.get(key_name))
                            v_weight = self.in_util_check_negative_weight(node, w, self.in_util_make_PRE(var_prm[v_type][0])) # type: ignore
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
                            else:
                                self.in_v_generic_PRE_FF(node, t_idx, v_type, v_weight)
                         
                # Collect FF POST vars in excess       
                if len(vars_keys_post[mp_idx]) > MAX_FF_VARS_POST:
                    FF_vars_skipped.append(f"\n\t\tFF POST -> {', '.join(vars_keys_post[mp_idx][MAX_FF_VARS_POST:])}")
                
                # FF POST vars ( only the first two in "vars_keys_post[mp_idx]" will be kept )
                if vars_keys_post[mp_idx]: # type: ignore
                    for t_idx, key_name in enumerate(vars_keys_post[mp_idx][:MAX_FF_VARS_POST]):
                        v_type = self.in_get_idx_by_key(self.in_util_make_VAR(key_name)) # type: ignore
                        if v_type is not None:
                            w = float(xform.get(key_name))
                            v_weight = self.in_util_check_negative_weight(node, w, self.in_util_make_POST(var_prm[v_type][0])) # type: ignore
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
                            else:
                                self.in_v_generic_POST_FF(node, t_idx, v_type, v_weight)
                
                # Print all skipped FF vars if any
                if FF_vars_skipped:
                    build = f"WARNING: {self.node}.FF\n\tThe following variations are in excess and skipped:{''.join(FF_vars_skipped)}\n"
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
                        v_type = self.in_get_idx_by_key(self.in_util_make_VAR(key_name)) # type: ignore
                        if v_type is not None:
                            w = float(xform.get(key_name))
                            v_weight = self.in_util_check_negative_weight(node, w, self.in_util_make_PRE(var_prm[v_type][0])) # type: ignore
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
                            else:
                                self.in_v_generic_PRE(mode, node, mp_idx, t_idx, v_type, v_weight)
                
                # Collect iterator POST vars in excess
                if len(vars_keys_post[mp_idx]) > MAX_ITER_VARS_POST:
                    iterator_vars_skipped.append(f"\n\t\tPOST -> {', '.join(vars_keys_post[mp_idx][MAX_ITER_VARS_POST:])}")

                # POST vars in this iterator ( only the first one in "vars_keys_post[mp_idx]" will be kept )
                if vars_keys_post[mp_idx]: # type: ignore
                    for t_idx, key_name in enumerate(vars_keys_post[mp_idx][:MAX_ITER_VARS_POST]):
                        v_type = self.in_get_idx_by_key(self.in_util_make_VAR(key_name)) # type: ignore
                        if v_type is not None:
                            w = float(xform.get(key_name))
                            v_weight = self.in_util_check_negative_weight(node, w, self.in_util_make_POST(var_prm[v_type][0])) # type: ignore
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
                            else:
                                self.in_v_generic_POST(mode, node, mp_idx, t_idx, v_type, v_weight)
                       
                # Print all skipped iterators vars if any
                if iterator_vars_skipped:
                    build = f"WARNING: {self.node}.iterator.{mp_idx+1}\n\tThe following variations are in excess and skipped:{''.join(iterator_vars_skipped)}\n"
                    print(build)
                                
                # Activate iterator, just in case...
                node.setParms({f"{iterator_names.main_vactive}_{str(mp_idx+1)}": 1}) # type: ignore
                # Set the rest of the iterator or FF parameters
                self.in_set_data(mode, node, prx, apo_data.xf_name, iterator_names.main_note, mp_idx)
                self.in_set_data(mode, node, prx, apo_data.weight, iterator_names.main_weight, mp_idx)
                self.in_set_data(mode, node, prx, apo_data.xaos, iterator_names.xaos, mp_idx)
                self.in_set_data(mode, node, prx, apo_data.color, iterator_names.shader_color, mp_idx)
                self.in_set_data(mode, node, prx, apo_data.symmetry, iterator_names.shader_speed, mp_idx)    
                self.in_set_data(mode, node, prx, apo_data.opacity, iterator_names.shader_alpha, mp_idx)
            
            # Set Affine ( PRE, POST and F3H_PRE, F3H_POST) for this iterator or FF
            self.in_set_affine(mode, node, prx, apo_data, iterator_names, mp_idx)
            
        _MSG = f"{node.name()}: Iterators and FF parameters SET -> Completed"
        flam3h_general_utils.set_status_msg(_MSG, 'MSG')



    def in_load_stats_msg(self, clipboard: bool, preset_id: int, apo_data: in_flame_iter_data) -> str:
        """Build a message with all the informations about the Flame preset we just loaded.

        Args:
            node (hou.SopNode): The current FLAM3H houdini node.
            preset_id (int): The loaded XML Flame preset
            apo_data (in_flame_iter_data): The XML Flame file data to get the loaded preset data from.

        Returns:
            str: A string to be used to set the IN Flame info data parameter message.
        """     
         
        node = self.node  
        # spacers
        nl = "\n"
        nnl = "\n\n"
        
        # checks
        pb_bool = opacity_bool = post_bool = xaos_bool = palette_bool = ff_bool = ff_post_bool = flam3h_mb_bool = False
        
        for item in apo_data.pre_blur:
            if item:
                pb_bool = True
                break
        if min(apo_data.opacity) == 0.0:
            opacity_bool = True
        if apo_data.post is not None:
            post_bool = True
        if apo_data.xaos is not None:
            xaos_bool = True
        if apo_data.palette is not None:
            palette_bool = True
        if apo_data.finalxform is not None:
            ff_bool = True
        if apo_data.finalxform_post is not None:
            ff_post_bool = True
        # custom to FLAM3H only
        if apo_data.mb_flam3h_fps is not False:
            flam3h_mb_bool = True
            
        # checks msgs
        opacity_bool_msg = post_bool_msg = xaos_bool_msg = ff_post_bool_msg = "NO"
        
        if opacity_bool:
            opacity_bool_msg = "YES"
        if post_bool:
            post_bool_msg = "YES"
        if xaos_bool:
            xaos_bool_msg = "YES"
        if ff_post_bool:
            ff_post_bool_msg = "YES"

            
        # build msgs
        cb = ''
        if clipboard: cb =  " -> Clipboard"
        sw = f"Software: {apo_data.sw_version[preset_id]}{cb}"
        name = f"Name: {apo_data.name[preset_id]}"
        iter_count = f"Iterators count: {str(len(apo_data.xforms))}"
        post = f"Post affine: {post_bool_msg}"
        opacity = f"Opacity: {opacity_bool_msg}"
        xaos = f"Xaos: {xaos_bool_msg}"
        
        mb = nnl
        if flam3h_mb_bool:
            mb = f"Motion blur{nnl}"
            
        ff_msg = ""
        if ff_bool:
            ff_msg = f"FF: YES\nFF Post affine: {ff_post_bool_msg}"
        else:
            ff_msg = f"FF: NO\n"
            
        if palette_bool:
            if apo_data.cp_flam3h_hsv is not False:
                # custom to FLAM3H only
                palette_count_format = f"Palette count: {apo_data.palette[1]}, format: {apo_data.palette[2]} -> HSV"
            else:
                palette_count_format = f"Palette count: {apo_data.palette[1]}, format: {apo_data.palette[2]}"
        else:
            palette_count_format = f"Palette not found."
        
        # ITERATOR COLLECT
        exclude_keys = XML_XF_KEY_EXCLUDE
        # ITERATOR posses an hard coded pre_blur, if the user toggle this option, lets exclude pre_gaussian_blur's key so we force pre_blur instead.
        if node.parm(IN_REMAP_PRE_GAUSSIAN_BLUR).eval():
            exclude_keys = XML_XF_KEY_EXCLUDE_PGB
            
        vars_keys = self.in_get_xforms_var_keys(apo_data.xforms, VARS_FLAM3_DICT_IDX.keys(), exclude_keys) 
        vars_keys_PRE = self.in_get_xforms_var_keys(apo_data.xforms, self.in_util_make_PRE(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)
        vars_keys_POST = self.in_get_xforms_var_keys(apo_data.xforms, self.in_util_make_POST(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)

        # FF COLLECT
        vars_keys_FF = vars_keys_PRE_FF = vars_keys_POST_FF = []
        if ff_bool:
            # FF do not posses an hard coded pre_blur so lets restore the standard XML_XF_KEY_EXCLUDE so we can have pre_gaussian_blur included if present.
            vars_keys_FF = self.in_get_xforms_var_keys(apo_data.finalxform, VARS_FLAM3_DICT_IDX.keys(), XML_XF_KEY_EXCLUDE)
            vars_keys_PRE_FF = self.in_get_xforms_var_keys(apo_data.finalxform, self.in_util_make_PRE(VARS_FLAM3_DICT_IDX.keys()), XML_XF_KEY_EXCLUDE)
            vars_keys_POST_FF = self.in_get_xforms_var_keys(apo_data.finalxform, self.in_util_make_POST(VARS_FLAM3_DICT_IDX.keys()), XML_XF_KEY_EXCLUDE)
            
        vars_all = vars_keys_PRE + vars_keys + vars_keys_POST + vars_keys_PRE_FF + vars_keys_FF + vars_keys_POST_FF # type: ignore
        
        if pb_bool:
            vars_all += [["pre_blur"]] # + vars_keys_PRE + vars_keys_POST
            
        result_sorted = self.in_util_vars_flatten_unique_sorted(vars_all, self.in_util_make_NULL, True) # type: ignore
        
        n = 5
        var_used_heading = "Variations used:"
        result_grp = [result_sorted[i:i+n] for i in range(0, len(result_sorted), n)]  
        vars_used_msg = f"{var_used_heading} {int(len(result_sorted))}\n{self.in_util_join_vars_grp(result_grp)}"
        
        # Build and set descriptive parameter msg
        if clipboard: preset_name = apo_data.name[0]
        else:
            # Get the correct menu parameter's preset menu label
            # The apo_data.name[idx] is used for the descriptive parameter
            # so to not print the icon path into the name.
            preset_name = apo_data.name[preset_id]
                
        descriptive_prm = ( f"sw: {apo_data.sw_version[preset_id]}\n",
                            f"{out_flame_utils.out_remove_iter_num(preset_name)}", )
        node.setParms({MSG_DESCRIPTIVE_PRM: "".join(descriptive_prm)}) # type: ignore

        # Build MISSING
        vars_keys_from_fractorium = self.in_get_xforms_var_keys(apo_data.xforms, VARS_FRACTORIUM_DICT, exclude_keys)
        vars_keys_from_fractorium_pre = self.in_get_xforms_var_keys_PP(apo_data.xforms, VARS_FRACTORIUM_DICT_PRE, V_PRX_PRE, exclude_keys)
        vars_keys_from_fractorium_post = self.in_get_xforms_var_keys_PP(apo_data.xforms, VARS_FRACTORIUM_DICT_POST, V_PRX_POST, exclude_keys)
        
        vars_keys_from_fractorium_FF = vars_keys_from_fractorium_pre_FF = vars_keys_from_fractorium_post_FF = []
        if ff_bool:
            vars_keys_from_fractorium_FF = self.in_get_xforms_var_keys(apo_data.finalxform, VARS_FRACTORIUM_DICT, exclude_keys)
            vars_keys_from_fractorium_pre_FF = self.in_get_xforms_var_keys_PP(apo_data.finalxform, VARS_FRACTORIUM_DICT_PRE, V_PRX_PRE, exclude_keys)
            vars_keys_from_fractorium_post_FF = self.in_get_xforms_var_keys_PP(apo_data.finalxform, VARS_FRACTORIUM_DICT_POST, V_PRX_POST, exclude_keys)
        
        vars_keys_from_fractorium_all = vars_keys_from_fractorium + vars_keys_from_fractorium_pre + vars_keys_from_fractorium_post + vars_keys_from_fractorium_pre_FF + vars_keys_from_fractorium_FF + vars_keys_from_fractorium_post_FF # type: ignore
        result_sorted_fractorium = self.in_util_vars_flatten_unique_sorted(vars_keys_from_fractorium_all, self.in_util_make_NULL, True)
        
        # Build MISSING: Compare, keep and build
        vars_missing = [x for x in result_sorted_fractorium if x not in result_sorted]
        result_grp_fractorium = [vars_missing[i:i+n] for i in range(0, len(vars_missing), n)]  
        vars_missing_msg = ""
        if vars_missing:
            vars_missing_msg = f"{nnl}MISSING:\n{self.in_util_join_vars_grp(result_grp_fractorium)}"
        
        
        # Build UNKNOWN
        vars_unknown = in_flame_utils.in_load_stats_unknown_vars(preset_id, apo_data)
        vars_unknown_msg = ""
        if vars_unknown:
            unknown_grp_fractorium = [vars_unknown[i:i+n] for i in range(0, len(vars_unknown), n)] 
            vars_unknown_msg = f"{nnl}UNKNOWN:\n{self.in_util_join_vars_grp(unknown_grp_fractorium)}"
        
        # Check if the loaded Flame file is locked.
        in_path = node.parm(IN_PATH).evalAsString()
        in_path_checked = out_flame_utils.out_check_outpath(node, in_path, OUT_FLAM3_FILE_EXT, 'Flame')
        
        flame_lib_locked = ""
        if flam3h_general_utils.isLOCK(in_path_checked):
            flame_lib_locked = f"-> LOCKED"
        # If the Flame use a 256+ palette, update the CP palette MSG
        if apo_data.palette[1] > 256:
            palette_msg: str = node.parm(MSG_PALETTE).evalAsString()
            if PALETTE_PLUS_MSG in palette_msg:
                pass
            else:
                node.setParms({MSG_PALETTE: f"{PALETTE_PLUS_MSG.strip()} {palette_msg.strip()}"})
        
        # build full stats msg
        build = (   flame_lib_locked, nl,
                    sw, nl,
                    name, nnl,
                    palette_count_format, nl,
                    mb,
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

        Note:
        If you change the icon gobal variable name inside here,
        remember to updated with the same global variable names inside: in_flame_utils.in_presets_in_isvalid_file_menu_label(...)

        Returns:
            list: the actual menu
        """
        node = self.node

        menu=[]
        if node.parm(IN_ISVALID_FILE).eval() and node.parm(IN_ISVALID_PRESET).eval():
            
            # This is really to force an extra check
            xml = os.path.expandvars(node.parm(IN_PATH).evalAsString())
            if os.path.isfile(xml):
                
                if node.parm(PREFS_ENUMERATE_MENU).eval():
                    
                    for i, item in enumerate(_xml(xml).get_name()):
                        
                        menu.append(i)
                        
                        # ICON bookmarks
                        #
                        # If a flame preset from a file is loaded
                        if i == int(node.parm(IN_PRESETS).eval()) and not node.parm(IN_CLIPBOARD_TOGGLE).eval():
                            node.setCachedUserData('in_presets_menu_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_FLAME_LOAD}  {str(i)}:  {item}     ") # 5 ending \s to be able to read the full label
                            
                        # If a flame preset from the clipboard is loaded
                        elif i == int(node.parm(IN_PRESETS).eval()) and node.parm(IN_CLIPBOARD_TOGGLE).eval():
                            node.setCachedUserData('in_presets_menu_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_FLAME_LOAD_CB}  {str(i)}:  {IN_CLIPBOARD_LABEL_MSG} {item}     ") # 5 ending \s to be able to read the full label
                            
                        else:
                            menu.append(f"{str(i)}:  {item}")
                            
                else:
                    
                    for i, item in enumerate(_xml(xml).get_name()):
                        
                        menu.append(i)
                        
                        # ICON bookmarks
                        #
                        # If a flame preset from a file is loaded
                        if i == int(node.parm(IN_PRESETS).eval()) and not node.parm(IN_CLIPBOARD_TOGGLE).eval():
                            node.setCachedUserData('in_presets_menu_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_FLAME_LOAD}  {item}     ") # 5 ending \s to be able to read the full label
                            
                        # If a flame preset from the clipboard is loaded
                        elif i == int(node.parm(IN_PRESETS).eval()) and node.parm(IN_CLIPBOARD_TOGGLE).eval():
                            node.setCachedUserData('in_presets_menu_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_FLAME_LOAD_CB}  {item}     ") # 5 ending \s to be able to read the full label
                            
                        else:
                            menu.append(f"{item}")
                            
                node.setCachedUserData('in_presets_menu', menu)   
                return menu
        
        flam3h_iterator_utils.destroy_data(node, 'in_presets_menu')
        return MENU_PRESETS_EMPTY


            
    def menu_in_presets(self) -> list:
        node = self.node
        data = node.cachedUserData('in_presets_menu')
        data_idx = node.cachedUserData('in_presets_menu_idx')
        preset_idx = node.parm(IN_PRESETS).eval()
        if data is not None and data_idx == preset_idx:
            return data
        else:
            return self.menu_in_presets_data()
        

    def menu_in_presets_empty_data(self) -> list:
        """Populate the IN menu parameters with entries based on the loaded IN XML Flame file.
        When no flame preset has been loaded. This will use the empty star icon to signal wich preset is being selected but not loaded.

        This definition exist only becasue if I change the icon dynamically inside: def menu_in_presets(self) -> list:
        Houdini will mix them up sometime, giving inconsistent results until I perform a new selection from the menu labels list.

        Note:
        If you change the icon gobal variable name inside here,
        remember to updated with the same global variable names inside: in_flame_utils.in_presets_in_isvalid_file_menu_label(...)

        Returns:
            list: the actual menu
        """
        node = self.node
        
        menu=[]
        if node.parm(IN_ISVALID_FILE).eval() and not node.parm(IN_ISVALID_PRESET).eval():
            
            # This is really to force an extra check
            xml = os.path.expandvars(node.parm(IN_PATH).evalAsString())
            if os.path.isfile(xml):
                
                if node.parm(PREFS_ENUMERATE_MENU).eval():
                    
                    for i, item in enumerate(_xml(xml).get_name()):
                        
                        menu.append(i)
                        
                        # ICON bookmarks
                        #
                        # If a flame preset from a file is loaded
                        if i == int(node.parm(IN_PRESETS_OFF).eval()) and not node.parm(IN_CLIPBOARD_TOGGLE).eval():
                            node.setCachedUserData('in_presets_menu_off_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_FLAME_LOAD_EMPTY}  {str(i)}:  {item}     ") # 5 ending \s to be able to read the full label

                        else:
                            menu.append(f"{str(i)}:  {item}")

                else:
                    
                    for i, item in enumerate(_xml(xml).get_name()):
                        
                        menu.append(i)
                        
                        # ICON bookmarks
                        #
                        # If a flame preset from a file is loaded
                        if i == int(node.parm(IN_PRESETS_OFF).eval()) and not node.parm(IN_CLIPBOARD_TOGGLE).eval():
                            node.setCachedUserData('in_presets_menu_off_idx', str(i))
                            menu.append(f"{FLAM3H_ICON_STAR_FLAME_LOAD_EMPTY}  {item}     ") # 5 ending \s to be able to read the full label

                        else:
                            menu.append(f"{item}")
                            
                node.setCachedUserData('in_presets_menu_off', menu)            
                return menu
            
        else:
            if node.parm(IN_ISVALID_PRESET).eval() and node.parm(IN_CLIPBOARD_TOGGLE).eval():
                return MENU_IN_PRESETS_EMPTY_CB
                    
        flam3h_iterator_utils.destroy_data(node, 'in_presets_menu_off')

        return MENU_PRESETS_EMPTY

            
            
    def menu_in_presets_empty(self) -> list:
        node = self.node
        data = node.cachedUserData('in_presets_menu_off')
        data_idx = node.cachedUserData('in_presets_menu_off_idx')
        preset_idx = node.parm(IN_PRESETS_OFF).eval()
        if data is not None and data_idx == preset_idx:
            return data
        else:
            return self.menu_in_presets_empty_data()
        
        
    def set_iter_on_load_callback(self) -> None:
        """Set the iteration number based on the "iteration on load" number.
        """        
        iter_on_load = self.node.parm(IN_ITER_NUM_ON_LOAD).eval()
        self.node.setParms({GLB_ITERATIONS: iter_on_load})
        # updated Flame preset name if any
        out_flame_utils(self.kwargs).out_auto_change_iter_num_to_prm()
        
        
    def use_iter_on_load_callback(self) -> None:
        """When the IN tab "force iterations on Load" option is turned ON it will set the initial iteration number wisely.
        """        
        node = self.node
        useiteronload = node.parm(IN_USE_ITER_ON_LOAD).eval()
        if useiteronload:
            iternumonload = node.parm(IN_ITER_NUM_ON_LOAD).eval()
            iter = node.parm(GLB_ITERATIONS).eval()
            if iternumonload == iter:
                pass
            elif iternumonload > iter:
                # node.setParms({GLB_ITERATIONS: iter})
                node.setParms({IN_ITER_NUM_ON_LOAD: iter})
            else:
                node.setParms({GLB_ITERATIONS: iternumonload})
                # updated Flame preset name if any
                out_flame_utils(self.kwargs).out_auto_change_iter_num_to_prm()


    def in_to_flam3h_toggle(self, prm: str) -> None:
        
        xml = self.node.parm(IN_PATH).evalAsString()
        # Here we could take a shortcut and use: if node.parm(IN_ISVALID_FILE).eval(): instead,
        # but for now we keep it safe and use the class: _xml_tree(..) instead.
        if _xml_tree(xml).isvalidtree:
            flam3h_general_utils(self.kwargs).flam3h_toggle(prm)
            self.in_to_flam3h()
        else:
            _MSG = f"{str(self.node)}: {prm.upper()}: No valid flame file to load the flame from, load a valid flame file first."
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')


    def in_to_flam3h_toggle_pgb(self) -> None:
        """When loading a flame preset that use a pre_gaussian_blur variation, this function will reload it
        and switch the "remap pre_gaussian_blur" toggle ON/OFF on the fly.
        
        If no pre_gaussian_blur variation is present in the currently selected flame preset, nothing will happen and a status bar warning message will let the user know about it.
        """ 
        node = self.node
        xml, clipboard, preset_id, flame_name_clipboard, load_from_clipboard, chaos = self.in_to_flam3h_init_data(node)
        
        # Here we are forced to use the class: _xml_tree(...) becasue a Flame can come from the clipboard
        # and we need to carefully validate it before proceding.
        if xml is not None and _xml_tree(xml).isvalidtree:
            
            apo_data = in_flame_iter_data(node, xml, preset_id)
            pgb_var_name = self.in_util_make_PRE(in_flame_utils.in_get_var_name_from_dict(VARS_FLAM3_DICT_IDX, 33))
            vars_key_PRE = self.in_get_xforms_var_keys(apo_data.xforms, self.in_util_make_PRE(VARS_FLAM3_DICT_IDX.keys()), XML_XF_KEY_EXCLUDE)
            vars_key_PRE_unique = self.in_util_vars_flatten_unique_sorted(vars_key_PRE, self.in_util_make_NULL) # type: ignore

            if vars_key_PRE is not None and vars_key_PRE and pgb_var_name in vars_key_PRE_unique:
                flam3h_general_utils(self.kwargs).flam3h_toggle(IN_REMAP_PRE_GAUSSIAN_BLUR)
                self.in_to_flam3h()
                
            else:
                if clipboard:
                    _MSG = f"{node.name()}: Reload of preset: {flame_name_clipboard} from Clipboard -> SKIPPED. The flame preset stored into the Clipboard do not have a \"pre_gaussian_blur\" variation in it."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                else:
                    # Get the correct menu parameter's preset menu label
                    preset_name = in_flame_utils.in_presets_in_isvalid_file_menu_label(node, preset_id)
                        
                    _MSG = f"{node.name()}: Reload of preset: {preset_name} -> SKIPPED. The currently selected flame preset do not have a \"pre_gaussian_blur\" variation in it."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                
        else:
            if load_from_clipboard:
                _MSG = f"{node.name()}: No valid flame preset to load from the Clipboard, copy a valid flame to the Clipboard first or load from a valid flame file instead."
            else:
                if chaos:
                    _MSG = f"Flame IN -> Chaotica XML not supported"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    flam3h_general_utils.flash_message(node, _MSG)
                else:
                    _MSG = f"{node.name()}: No valid flame file to load the flame from, load a valid flame file first."
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            


    def in_to_flam3h_toggle_f3h_affine(self) -> None:
        """When loading a flame preset that use FLAM3H affine style, this function will reload it
        and switch the "FLAM3H affine style" toggle ON/OFF on the fly.
        
        If no FLAM3H affine style are present in the currently selected flame preset, nothing will happen and a status bar warning message will let the user know about it.
        """ 
        node = self.node
        xml, clipboard, preset_id, flame_name_clipboard, load_from_clipboard, chaos = self.in_to_flam3h_init_data(node)
        
        # Here we are forced to use the class: _xml_tree(...) becasue a Flame can come from the clipboard
        # and we need to carefully validate it before proceding.
        if xml is not None and _xml_tree(xml).isvalidtree:
            
            apo_data = in_flame_iter_data(node, xml, preset_id)
            if apo_data.f3h_coefs is not None:
                flam3h_general_utils(self.kwargs).flam3h_toggle(IN_FLAM3H_AFFINE_STYLE)
                self.in_to_flam3h()
                
            else:
                if clipboard:
                    _MSG = f"{node.name()}: Reload of preset: {flame_name_clipboard} from Clipboard -> SKIPPED. The flame preset stored into the Clipboard do not have FLAM3H affine style."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                else:
                    # Get the correct menu parameter's preset menu label
                    preset_name = in_flame_utils.in_presets_in_isvalid_file_menu_label(node, preset_id)
                        
                    _MSG = f"{node.name()}: Reload of preset: {preset_name} -> SKIPPED. The currently selected flame preset do not have FLAM3H affine style."
                    flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                
        else:
            if load_from_clipboard:
                _MSG = f"{node.name()}: No valid flame preset to load from the Clipboard, copy a valid flame to the Clipboard first or load from a valid flame file instead."
            else:
                if chaos:
                    _MSG = f"Flame IN -> Chaotica XML not supported"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    flam3h_general_utils.flash_message(node, _MSG)
                else:
                    _MSG = f"{node.name()}: No valid flame file to load the flame from, load a valid flame file first."
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            


    def in_to_flam3h_reset_user_data(self) -> None:
        
        node = self.node
        
        # lets initialize those to default values in case their data no longer exist.
        flam3h_iterator_utils.flam3h_init_hou_session_iterator_data(node)
        flam3h_iterator_utils.flam3h_init_hou_session_ff_data(node)
        
        # Reset iterator user data if needed
        from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_ITERATOR_NODE # type: ignore
        if from_FLAM3H_NODE is not None and node == from_FLAM3H_NODE:
            if flam3h_iterator_utils.exist_user_data(from_FLAM3H_NODE):
                flam3h_iterator_utils.del_comment_and_user_data_iterator(from_FLAM3H_NODE)
                hou.session.FLAM3H_MARKED_ITERATOR_MP_IDX = None # type: ignore
        
        # Reset mp idx flam3h mem parameter
        if node.parm(FLAM3H_DATA_PRM_MPIDX).evalAsInt() != 0:
            flam3h_iterator_utils.iterator_mpidx_mem_set(node, 0)
        
        # Reset FF user data if needed
        from_FLAM3H_NODE = hou.session.FLAM3H_MARKED_FF_NODE # type: ignore
        if from_FLAM3H_NODE is not None and node == from_FLAM3H_NODE:
            if flam3h_iterator_utils.exist_user_data(from_FLAM3H_NODE, FLAM3H_USER_DATA_FF):
                flam3h_iterator_utils.del_comment_and_user_data_iterator(from_FLAM3H_NODE, FLAM3H_USER_DATA_FF)
                hou.session.FLAM3H_MARKED_FF_CHECK = None # type: ignore



    def in_to_flam3h_reset_iterators_parms(self, node: hou.SopNode, in_flame_iter_count: int) -> None:
        """Prior to this, I was setting the iterator's count to zero and then back to the requested count to reset all their values.
        It was not the fastest solution and this is actually making it more performant overall.

        Args:
            node (hou.SopNode): This FLAM3H node
            in_flame_iter_count (int): IN flame iterator's count ( number of xforms )
        """        
        # iterators
        flam3h_iter_count = node.parm(FLAME_ITERATORS_COUNT).evalAsInt()
        
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



    def in_to_flam3h_init_data_ALT(self) -> tuple[Union[str, None], bool, int, str, bool, bool]:
        """Load a flame preset from the clipboard.

        Args:
            node (hou.SopNode): FLAM3H node to load the flame preset into.

        Returns:
            tuple[Union[str, None], bool, int, str, bool]:  tuple(  xml, 
                                                                    clipboard, 
                                                                    preset_id, 
                                                                    clipboard_flame_name, 
                                                                    attempt_to_load_from_clipboard, 
                                                                    chaos
                                                                    )
            
                                                                    -> xml ( Union[str, None] ): either a flame preset from a flame file or from the Clipboard.
                                                                    
                                                                    -> clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                                    
                                                                    -> clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                                    
                                                                    -> attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> chaos ( bool ): Is it a chaotica XML file type ? True or False.
        """     
        xml = hou.ui.getTextFromClipboard() # type: ignore
        try:
            tree = lxmlET.ElementTree(lxmlET.fromstring(xml)) # type: ignore
        except:
            tree = None
        if tree is not None:
            assert xml is not None
            if tuple([f for f in tree.getroot().iter(XML_FLAME_NAME)]):
                flame_name_clipboard = _xml_tree(xml).name[0]
                return xml, True, 0, flame_name_clipboard, True, False
            else:
                if self.in_to_flam3h_is_CHAOS(xml):
                    return None, False, 0, '', True, True
                else:
                    return None, False, 0, '', True, False
        else:
            return None, False, 0, '', True, False



    def in_to_flam3h_init_data_SHIFT(self, node: hou.SopNode) -> tuple[Union[str, None], bool, int, str, bool, bool]:
        """Load a flame file from a file dialog.

        Args:
            node (hou.SopNode): FLAM3H node to load the flame file/preset into.

        Returns:
            tuple[Union[str, None], bool, int, str, bool]:  tuple(  xml, 
                                                                    clipboard, 
                                                                    preset_id, 
                                                                    clipboard_flame_name, 
                                                                    attempt_to_load_from_clipboard, 
                                                                    chaos
                                                                    )
            
                                                                    -> xml ( Union[str, None] ): either a flame preset from a flame file or from the Clipboard.
                                                                    
                                                                    -> clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                                    
                                                                    -> clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                                    
                                                                    -> attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> chaos ( bool ): Is it a chaotica XML file type ? True or False.
        """        
        
        flameFile = hou.ui.selectFile(start_directory=None, title="FLAM3H: Load a *.flame file", collapse_sequences=False, file_type=hou.fileType.Any, pattern="*.flame", default_value=None, multiple_select=False, image_chooser=None, chooser_mode=hou.fileChooserMode.Read, width=0, height=0)  # type: ignore
        flameFile_expandvars = os.path.expandvars(flameFile)
        
        dir = os.path.dirname(flameFile_expandvars)
        if os.path.isdir(dir):
            
            if _xml_tree(flameFile_expandvars).isvalidtree:
                
                node.setParms({IN_PATH: flameFile_expandvars}) # type: ignore
                # Since this goes directly into: self.in_to_flam3h() definition only
                # its argument is set to 0 so not to create a loop of loading processes
                # becasue inside the following definition there is another call to: self.in_to_flam3h()
                flam3h_general_utils(self.kwargs).flam3h_init_presets_IN_PRESETS(0)
                
                # Set menu parameters index to the first entry
                node.setParms({IN_PRESETS: "0"}) # type: ignore
                node.setParms({IN_PRESETS_OFF: "0"}) # type: ignore
                node.setParms({IN_SYS_PRESETS: "0"}) # type: ignore
                node.setParms({IN_SYS_PRESETS_OFF: "0"}) # type: ignore
                
                return flameFile_expandvars, False, 0, '', False, False
            
            else:
                if self.in_to_flam3h_is_CHAOS(flameFile_expandvars):
                    return None, False, 0, '', False, True
                else:
                    return None, False, 0, '', False, False
            
        else:
            return None, False, 0, '', False, False
        
        
        
    def in_to_flam3h_init_data_CTRL(self) -> tuple[Union[str, None], bool, int, str, bool, bool]:
        """Load nothing with as the kwargs['ctrl'] is not mapped to anything else yet so this is a place holder.

        Returns:
            tuple[Union[str, None], bool, int, str, bool]:  tuple(  xml, 
                                                                    clipboard, 
                                                                    preset_id, 
                                                                    clipboard_flame_name, 
                                                                    attempt_to_load_from_clipboard, 
                                                                    chaos
                                                                    )
            
                                                                    -> xml ( Union[str, None] ): either a flame preset from a flame file or from the Clipboard.
                                                                    
                                                                    -> clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                                    
                                                                    -> clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                                    
                                                                    -> attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> chaos ( bool ): Is it a chaotica XML file type ? True or False.
    """
        return None, False, 0, '', False, False
    
    
    
    def in_to_flam3h_init_data_LMB(self, node: hou.SopNode) -> tuple[Union[str, None], bool, int, str, bool, bool]:
        """Load a flame preset with a mouse click, no kwargs.

        Args:
            node (hou.SopNode): FLAM3H node to load the flame file/preset into.

        Returns:
            tuple[Union[str, None], bool, int, str, bool]:  tuple(  xml, 
                                                                    clipboard, 
                                                                    preset_id, 
                                                                    clipboard_flame_name, 
                                                                    attempt_to_load_from_clipboard, 
                                                                    chaos
                                                                    )
            
                                                                    -> xml ( Union[str, None] ): either a flame preset from a flame file or from the Clipboard.
                                                                    
                                                                    -> clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                                    
                                                                    -> clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                                    
                                                                    -> attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> chaos ( bool ): Is it a chaotica XML file type ? True or False.
    """
        xml = node.parm(IN_PATH).evalAsString()
        
        # Get the correct menu parameter's preset idx
        if node.parm(IN_ISVALID_PRESET).evalAsInt():
            preset_id = node.parm(IN_PRESETS).eval()
            # Update
            node.setParms({IN_PRESETS_OFF: preset_id}) # type: ignore
        else:
            preset_id = node.parm(IN_PRESETS_OFF).eval()
            # Update
            node.setParms({IN_PRESETS: preset_id}) # type: ignore
            
        return xml, False, int(preset_id), '', False, False



    def in_to_flam3h_init_data(self, node: hou.SopNode) -> tuple[Union[str, None], bool, int, str, bool, bool]:
        """Check if we are able to load a flame from a selected file or to parse a flame from the clipboard
        and provide some output data to work with if any of those cases is true.
        
        Args:
            node (hou.SopNode): FLAM3H node to load the flame file/preset into.

        Returns:
            tuple[Union[str, None], bool, int, str, bool]:  tuple(  xml, 
                                                                    clipboard, 
                                                                    preset_id, 
                                                                    clipboard_flame_name, 
                                                                    attempt_to_load_from_clipboard, 
                                                                    chaos
                                                                    )
            
                                                                    -> xml ( Union[str, None] ): either a flame preset from a flame file or from the Clipboard.
                                                                    
                                                                    -> clipboard ( bool ): did we get a valid flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> preset_id ( int ): flame preset index. From clipboard will always be ZERO.
                                                                    
                                                                    -> clipboard_flame_name ( str ): If a valid flame preset from the clipboard is loaded, this will store the preset name of it.
                                                                    
                                                                    -> attempt_to_load_from_clipboard ( bool ): Did we try to load flame preset from the clipboard ? True or False.
                                                                    
                                                                    -> chaos ( bool ): Is it a chaotica XML file type ? True or False.
        """ 
        # The following try/except block is in place to avoid a 'KeyError' when
        # loading a flame preset from the menu parameter entries instead of clicking the Action Button's icon.
        
        try:
            self.kwargs['alt']
            _K = True
        except:
            _K = False

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
        """
        node = self.node
        xml = node.parm(IN_PATH).evalAsString()

        if xml and node.parm(IN_ISVALID_FILE).evalAsInt():
            if node.parm(IN_ISVALID_PRESET).evalAsInt():
                preset_id = node.parm(IN_SYS_PRESETS).eval()
                # Updated other PRESETS menu parameters
                node.setParms({IN_SYS_PRESETS_OFF: preset_id})
                node.setParms({IN_PRESETS: preset_id})
                node.setParms({IN_PRESETS_OFF: preset_id})
            else:
                preset_id = node.parm(IN_SYS_PRESETS_OFF).eval()
                # Updated other PRESETS menu parameters
                node.setParms({IN_SYS_PRESETS: preset_id})
                node.setParms({IN_PRESETS: preset_id})
                node.setParms({IN_PRESETS_OFF: preset_id})
        
            self.in_to_flam3h()

    '''
        The following is the actual load preset/flame function to be used.
    '''
    def in_to_flam3h(self) -> None:
        """Load a Flame preset into FLAM3H.
        This will set all FLAM3H node parameters based on values from the loaded XML Flame preset.
        """
        node = self.node
        xml, clipboard, preset_id, flame_name_clipboard, attempt_from_clipboard, chaos = self.in_to_flam3h_init_data(node)

        if xml is not None and _xml_tree(xml).isvalidtree:
            
            # Resets
            ####################################################
            iter_on_load = in_flame_utils.in_set_iter_on_load(node, preset_id, clipboard, flame_name_clipboard)
            flam3h_general_utils(self.kwargs).reset_SYS(1, iter_on_load, 0)
            flam3h_general_utils(self.kwargs).reset_MB()
            flam3h_general_utils(self.kwargs).reset_PREFS()

            # get keys to exclude to be used inside: self.in_flam3h_set_iterators(...) definition
            ####################################################
            exclude_keys = XML_XF_KEY_EXCLUDE
            if node.parm(IN_REMAP_PRE_GAUSSIAN_BLUR).eval():
                exclude_keys = XML_XF_KEY_EXCLUDE_PGB


            # ITERATOR
            ####################################################
            ####################################################
            # IN flame preset data
            apo_data = in_flame_iter_data(node, xml, preset_id)
            
            # prepare iterators
            self.in_to_flam3h_reset_iterators_parms( node, len(apo_data.xforms) )
            
            # RIP: if there are ZERO opacities, always turn RIP toggle ON
            if min(apo_data.opacity) == 0.0:
                node.setParms({SYS_RIP: 1}) # type: ignore
            else:
                # Otherwise set RIP toggle accordingly from the XML data if any
                if apo_data.sys_flam3h_rip is not None:
                    node.setParms({SYS_RIP: apo_data.sys_flam3h_rip}) # type: ignore

            # Set iterators
            self.in_flam3h_set_iterators(0, node, apo_data, preset_id, exclude_keys)
            ####################################################
            
            
            # FF
            ####################################################
            ####################################################
            if apo_data.finalxform is not None:
                # get keys to exclude
                # FF do not posses an hard coded pre_blur so lets restore the standard exclude_keys so we can have pre_gaussian_blur included.
                exclude_keys = XML_XF_KEY_EXCLUDE
                flam3h_iterator_utils(self.kwargs).reset_FF()
                node.setParms({SYS_DO_FF: 1}) # type: ignore
                # Set FF
                self.in_flam3h_set_iterators(1, node, apo_data, preset_id, exclude_keys)
            else:
                flam3h_iterator_utils(self.kwargs).reset_FF()
                node.setParms({SYS_DO_FF: 0}) # type: ignore
            ####################################################
            
            
            # MB
            ####################################################
            ####################################################
            if apo_data.mb_flam3h_fps is not False:
                node.setParms({MB_DO: 1}) # type: ignore
                node.setParms({MB_FPS: apo_data.mb_flam3h_fps}) # type: ignore
                node.setParms({MB_SAMPLES: apo_data.mb_flam3h_samples}) # type: ignore
                node.setParms({MB_SHUTTER: apo_data.mb_flam3h_shutter}) # type: ignore
            else:
                flam3h_general_utils(self.kwargs).reset_MB()
            ####################################################
            
            
            # PALETTE
            ####################################################
            ####################################################
            # if CP HSV vals
            if apo_data.cp_flam3h_hsv is not False:
                node.setParms({CP_RAMP_HSV_VAL_NAME: apo_data.cp_flam3h_hsv}) # type: ignore
            else:
            # CP HSV default vals
                node.setParms({CP_RAMP_HSV_VAL_NAME: hou.Vector3((1.0, 1.0, 1.0))}) # type: ignore
            
            # Set XML palette data
            ramp_parm = node.parm(CP_RAMP_SRC_NAME)
            # Reset ramps to default
            flam3h_palette_utils.build_ramp_palette_default(ramp_parm)
            flam3h_palette_utils.delete_ramp_all_keyframes(ramp_parm)
            flam3h_palette_utils.delete_ramp_all_keyframes(node.parm(CP_RAMP_HSV_NAME))
            ramp_parm.set(apo_data.palette[0])
            flam3h_palette_utils(self.kwargs).palette_cp()
            # Set palette lookup samples
            node.setParms({CP_RAMP_LOOKUP_SAMPLES: apo_data.cp_flam3h_samples})
            # Mark this as not a loaded palette preset
            node.setParms({CP_ISVALID_PRESET: 0})
            # reset tmp ramp palette
            flam3h_palette_utils(self.kwargs).reset_CP_TMP()
            ####################################################
            
            
            # Set density back to default on load
            ####################################################
            node.setParms({GLB_DENSITY: FLAM3H_DEFAULT_GLB_DENSITY}) # type: ignore
            
            
            # Update flame stats
            ####################################################
            node.setParms({MSG_FLAMESTATS: self.in_load_stats_msg(clipboard, preset_id, apo_data)}) # type: ignore
            node.setParms({MSG_FLAMESENSOR: self.in_load_sensor_stats_msg(preset_id, apo_data)}) # type: ignore
            node.setParms({MSG_FLAMERENDER: self.in_load_render_stats_msg(preset_id, apo_data)}) # type: ignore
            
            
            # if we are loading from the clipboard, always copy the render settings on load
            ####################################################
            ####################################################
            if clipboard:
                self.in_copy_render_all_stats_msg(self.kwargs, clipboard, apo_data)
            else:
                # If not from clipboard
                # Update SYS inpresets parameters
                node.setParms({IN_SYS_PRESETS: str(preset_id)}) # type: ignore
                node.setParms({IN_SYS_PRESETS_OFF: str(preset_id)}) # type: ignore
                
                # if "copy render properties on Load" is checked
                if node.parm(IN_COPY_RENDER_PROPERTIES_ON_LOAD).eval():
                    self.in_copy_render_stats_msg(self.kwargs)
            ####################################################
            
            
            # Update xaos
            ####################################################
            flam3h_iterator_utils(self.kwargs).auto_set_xaos()
            
            
            # Update OUT Flame name iter num if any
            ####################################################
            out_flame_utils(self.kwargs).out_auto_change_iter_num_to_prm()
            
            
            # F3C ( the if statement is for backward compatibility )
            ####################################################
            if apo_data.prefs_flam3h_f3c is not None:
                node.setParms({PREFS_F3C: apo_data.prefs_flam3h_f3c}) # type: ignore
            
            # Reset iterator and FF user data if needed
            ####################################################
            self.in_to_flam3h_reset_user_data()
            
            # Clear menu caches
            flam3h_iterator_utils.destroy_data(node, 'iter_sel')
            flam3h_iterator_utils.destroy_data(node, 'in_presets_menu')
            flam3h_iterator_utils.destroy_data(node, 'in_presets_menu_idx')
            flam3h_iterator_utils.destroy_data(node, 'in_presets_menu_off')
            flam3h_iterator_utils.destroy_data(node, 'in_presets_menu_off_idx')

            
            
            # Set toggles and MSG
            ####################################################
            if clipboard:
                # If it is a valid preset from the clipboard, set the "valid preset" and "clipboard" toggles
                # but do not change the "is valid file" toggle as we dnt know if a valid file is already loaded.
                node.setParms({IN_ISVALID_PRESET: 1}) 
                node.setParms({IN_CLIPBOARD_TOGGLE: 1})
                
                preset_name = flame_name_clipboard
                _MSG = f"{node.name()}: LOAD Flame preset from Clipboard: \"{out_flame_utils.out_remove_iter_num(preset_name)}\" -> Completed"
            else:
                # Otherwise mean the preset is coming from a file,
                # set all of them and uncheck the clipboard toggle just in case.
                node.setParms({IN_ISVALID_FILE: 1})
                node.setParms({IN_ISVALID_PRESET: 1})
                node.setParms({IN_CLIPBOARD_TOGGLE: 0})
                
                # Get the correct menu parameter's preset menu label
                preset_name = apo_data.name[preset_id] 
                _MSG = f"{node.name()}: LOAD Flame preset: \"{out_flame_utils.out_remove_iter_num(preset_name)}\" -> Completed"
                
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            ####################################################
            
        else:
            
            # If there is an already loaded file set in the parameter
            in_xml = os.path.expandvars(node.parm(IN_PATH).evalAsString())
            
            # If we loaded a Chaotica XML style preset from the Clipboard 
            if self.in_to_flam3h_clipboard_is_CHAOS():
                _MSG = "Flame IN Clipboard -> Chaotica XML not supported"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                flam3h_general_utils.flash_message(node, _MSG)

            # If we are trying to load from the Clipboard
            elif attempt_from_clipboard:
                _MSG = "Flame IN Clipboard -> Nothing to load"
                flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                flam3h_general_utils.flash_message(node, _MSG)
                
            else:
                
                # If we did try to load a chaotica XML style file
                if chaos:
                    _MSG = f"Flame IN -> Chaotica XML not supported"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    flam3h_general_utils.flash_message(node, _MSG)
                
                # If there was already a valid flame file
                elif _xml_tree(in_xml).isvalidtree:
                    pass
                    
                # If there was already a preset loaded from the clipboard
                elif node.parm(IN_ISVALID_PRESET).eval() and node.parm(IN_CLIPBOARD_TOGGLE).eval():
                    
                    node.setParms({IN_ISVALID_FILE: 0})

                    _MSG = "Flame IN -> Nothing to load"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    flam3h_general_utils.flash_message(node, _MSG)
                     
                # Anything else   
                else:
                    node.setParms({IN_ISVALID_FILE: 0})
                    node.setParms({IN_ISVALID_PRESET: 0})
                    node.setParms({IN_CLIPBOARD_TOGGLE: 0})
                    # clear info msgs
                    node.setParms({MSG_FLAMESTATS: ""})
                    node.setParms({MSG_FLAMERENDER: ""})
                    node.setParms({MSG_DESCRIPTIVE_PRM: ""})

                    _MSG = "Flame IN -> Nothing to load"
                    flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'MSG')
                    flam3h_general_utils.flash_message(node, _MSG)



    def reset_IN(self, mode=0) -> None:
        """Reset the FLAM3H IN Tab parameters.

        Args:
            mode (int, optional): _description_. Defaults to 0. 1 will reset the remainder of the parameters.
        """        
        node = self.node

        node.setParms({IN_ISVALID_PRESET: 0})
        node.setParms({IN_CLIPBOARD_TOGGLE: 0})
        node.setParms({MSG_FLAMESTATS: ""})
        node.setParms({MSG_FLAMERENDER: ""})
        node.setParms({MSG_DESCRIPTIVE_PRM: ""})
        if mode:
            node.setParms({IN_PATH: ""})
            node.setParms({IN_PRESETS: str(-1)})
            node.setParms({IN_PRESETS_OFF: str(-1)})
            node.setParms({IN_ITER_NUM_ON_LOAD: 64})
            node.setParms({IN_USE_ITER_ON_LOAD: 0})
            node.setParms({IN_COPY_RENDER_PROPERTIES_ON_LOAD: 0})







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
VARS_FRACTORIUM_DICT_PRE: dict  = in_flame_utils.in_util_vars_dict_type_maker(VARS_FRACTORIUM_DICT, in_flame_utils.in_util_make_PRE)
VARS_FRACTORIUM_DICT_POST: dict = in_flame_utils.in_util_vars_dict_type_maker(VARS_FRACTORIUM_DICT, in_flame_utils.in_util_make_POST)








# SAVE XML FILES start here
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


class out_flame_utils:
    """
class out_flame_utils

STATIC METHODS:

out_auto_add_iter_num(iter_num: int, flame_name: str, autoadd: int) -> str:

out_auto_change_iter_num(iter_num: int, flame_name: str, autoadd: int) -> str:

out_remove_iter_num(flame_name: str) -> str:

out_flame_default_name(node: hou.SopNode, autoadd: int) -> str:

out_util_round_float(VAL) -> str:

out_util_round_floats(VAL_LIST: Union[list[list[str]], tuple[list]]) -> Union[list[str], list[list[str]], tuple[str]]:

out_util_check_duplicate_var_section(vars: list) -> bool:

out_util_iterators_vars_duplicate(vars: list) -> list:

out_check_build_file(file_split: Union[tuple[str, str], list[str]], file_name: str, file_ext: str) -> str:

out_check_outpath(node: hou.SopNode, infile: str, file_ext: str, prx: str) -> Union[str, bool]:

out_affine_rot(affine: list[Union[tuple[str], list[str]]], angleDeg: float) -> list[Union[list[str], tuple[str]]]:

out_xaos_cleanup(xaos: Union[list[str], list[list[str]], tuple[str]]) -> list[list[str]]:

out_xaos_collect(node: hou.SopNode, iter_count: int, prm: str) -> list[list[str]]:

out_xaos_collect_vactive(node: hou.SopNode, fill: list, prm: str) -> list[list[str]]:

_out_pretty_print(current, parent=None, index=-1, depth=0) -> None:

METHODS:

out_presets_get_selected_menu_label(self) -> Union[str, None]:

out_presets_copy_menu_label_callback(self) -> None:

out_palette_keys_count(self, palette_plus: int, keys: int, type: int, _MSG = True) -> str:

menu_sensor_resolution(self) -> list:

menu_sensor_resolution_set(self, update=True) -> None:

reset_OUT_sensor(self) -> None:

reset_OUT_render(self) -> None:

reset_OUT_kwargs(self) -> None:

reset_OUT_options(self) -> None:

reset_OUT(self, mode=0) -> None:

out_xf_xaos_to(self) -> tuple:

out_xf_xaos_from(self, mode=0) -> tuple:

menu_out_contents_presets_data(self) -> list:

menu_out_contents_presets(self) -> list:

out_auto_add_iter_data(self) -> tuple[int, str, int]:

out_auto_add_iter_num_to_prm(self) -> None:

out_auto_change_iter_num_to_prm(self) -> None:

out_flame_properties_build(self) -> dict:

out_flam3_compatibility_check_and_msg(self,
                                        names_VARS_PRE: list, 
                                        names_VARS: list, 
                                        names_VARS_POST: list, 
                                        flam3h_do_FF: bool, 
                                        names_VARS_PRE_FF: list, 
                                        names_VARS_FF: list, 
                                        names_VARS_POST_FF: list) -> bool:
                                        
out_collect_var_section_names(self, _SECTION='VAR') -> Union[list[str], None]:
                                      
out_populate_xform_vars_XML(self, 
                            varsPRM: tuple, 
                            TYPES_tuple: tuple, 
                            WEIGHTS_tuple: tuple, 
                            XFORM: lxmlET.Element, # type: ignore
                            MP_IDX: str, 
                            FUNC: Callable) -> list[str]:

out_build_XML(self, flame: lxmlET.Element) -> bool:

out_new_XML(self, outpath: str) -> None:

out_new_XML_clipboard(self) -> None:

out_append_XML(self, apo_data: in_flame, out_path: str) -> None:

out_XML(self) -> None:

__out_flame_data(self, prm_name='') -> str:

__out_flame_name(self, prm_name=OUT_XML_RENDER_HOUDINI_DICT.get(XML_XF_NAME)) -> str:

__out_xf_data(self, prm_name: str) -> tuple:

__out_xf_name(self) -> tuple:

__out_finalxf_name(self) -> str:

__out_xf_pre_blur(self) -> tuple:

__out_xf_xaos(self) -> tuple:

__out_xf_preaffine(self) -> tuple:

__out_xf_postaffine(self) -> tuple:

__out_finalxf_preaffine(self) -> str:

__out_finalxf_postaffine(self) -> Union[str, bool]:

__out_palette_hex(self) -> str:

__out_flame_data_flam3h_hsv(self, prm_name=CP_RAMP_HSV_VAL_NAME) -> Union[str, bool]:

__out_flame_data_flam3h_mb_val(self, prm_name='') -> Union[str, bool]:

__out_flame_data_flam3h_toggle(self, toggle: bool) -> str:
    """

    def __init__(self, kwargs: dict) -> None:
        self._kwargs = kwargs
        self._node = kwargs['node']
        self._flam3h_iter_prm_names = flam3h_iterator_prm_names()
        self._flam3h_iter = flam3h_iterator()
        self._flam3h_iter_FF = flam3h_iterator_FF()
        self._flam3h_do_FF = self._node.parm(SYS_DO_FF).eval()
        self._iter_count = self._node.parm(FLAME_ITERATORS_COUNT).evalAsInt()
        self._palette: hou.Ramp = self._node.parm(CP_RAMP_SRC_NAME).evalAsRamp()
        self._palette_hsv_do = self._node.parm(OUT_HSV_PALETTE_DO).eval()
        self._palette_plus_do = self._node.parm(OUT_PALETTE_256_PLUS).eval()
        if self._palette_hsv_do:
            # Update hsv ramp before storing it.
            flam3h_palette_utils(self.kwargs).palette_cp()
            self._palette: hou.Ramp = self._node.parm(CP_RAMP_HSV_NAME).evalAsRamp()
        self._f3h_affine: bool = self._node.parm(OUT_FLAM3H_AFFINE_STYLE).eval()
        self._xm = self._node.parm(PREFS_XAOS_MODE).eval()
        # custom to FLAM3H only
        self._flam3h_rip = self._node.parm(SYS_RIP).eval()
        self._flam3h_mb_do = self._node.parm(MB_DO).eval()
        self._flam3h_f3c = self._node.parm(PREFS_F3C).eval()
        self._flam3h_cp_lookup_samples = self._node.parm(CP_RAMP_LOOKUP_SAMPLES).evalAsInt()
        
    
        
    
    @staticmethod
    def out_auto_add_iter_num(iter_num: int, flame_name: str, autoadd: int) -> str:
        """It will check the passed Flame name 
        and add the iteration number to it if needed.

        Args:
            iter_num (int): the current iteration's number
            flame_name (str): The Flame name to check
            autoadd (int): Auto add iter num toggle value

        Returns:
            str: A new Flame name with the iter num added if needed.
        """
        if autoadd:
            
            flame_name = flame_name.strip()
            if flame_name:
                
                splt = ':'
                flame_name_new = datetime.now().strftime("Flame_%b-%d-%Y_%H%M%S")
                
                rp = flame_name.split(splt)
                rp[:] = [item for item in rp if item]
                # Lets make some name checks first
                #
                # if it start with a special character
                if not flame_name[0].isalnum():
                    rp = flame_name_new.split(splt)
                    rp[:] = [item for item in rp if item]
                # if it end with special character
                elif not flame_name[-1].isalnum():
                    rp = flame_name.split(splt)
                    if len(rp)==1 and len(rp[0]):
                        item_cleaned =''.join(letter for letter in rp[0].strip() if letter.isalnum() or letter in CHARACTERS_ALLOWED_OUT_AUTO_ADD_ITER_NUM)
                        rp = [item_cleaned]
                    elif len(rp)>1:
                        flame_name_new = ' '.join(rp[:-1])
                        rp = flame_name_new.split(splt)
                        rp[:] = [item for item in rp if item]
                    else:
                        rp = flame_name_new.split(splt)
                        rp[:] = [item for item in rp if item]
                
                is_int = True
                try:
                    # if the name is a number, I want to still add the iteration num to it
                    # and not evaluate this as integer, even if it is an integer.
                    if rp[-1] != flame_name:
                        int(rp[-1].strip())
                    else:
                        is_int = False
                except:
                    is_int = False
                    
                if is_int is False:
                    rp_clean = [''.join(letter for letter in item.strip() if letter.isalnum() or letter in CHARACTERS_ALLOWED_OUT_AUTO_ADD_ITER_NUM) for item in rp]
                    flame_name_new = ' '.join(rp_clean) + FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV + str(iter_num)
                    return flame_name_new.strip()
                else:
                    splt = flame_name.split(":")
                    if len(splt)>1:
                        return ''.join([item.strip() for item in splt[:-1]]) + FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV + str(iter_num)
                    else:
                        return flame_name
            else:
                return flame_name
        else:
            return flame_name
    
    
    @staticmethod 
    def out_auto_change_iter_num(iter_num: int, flame_name: str, autoadd: int) -> str:
        """It will check the passed Flame name 
        and update the iteration number when changing iterations.
        If no iteration number is present in the passed Flame name
        it will add it to the end of the Flame name.

        Args:
            iter_num (int): the current iteration's number
            flame_name (str): The Flame name to check
            autoadd (int): Auto add iter num toggle value

        Returns:
            str: A new Flame name with the iter num updated/added if needed.
        """
        if autoadd:
            
            flame_name = flame_name.strip()
            if flame_name:
                
                flame_name = out_flame_utils.out_auto_add_iter_num(iter_num, flame_name, autoadd)
                rp = str(flame_name).rpartition(FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV)

                is_int = False
                try:
                    if rp[-1] != flame_name:
                        int(rp[-1])
                        is_int = True
                    else:
                        pass
                except:
                    pass
                
                if is_int:
                    flame_name_changed = ''.join(rp[:-1]) + str(iter_num)
                    return flame_name_changed
                else:
                    return flame_name
            else:
                return flame_name
        else:
            return flame_name
        
        
    @staticmethod 
    def out_remove_iter_num(flame_name: str) -> str:
        """Remove the iterations number from the Flame name if any

        Args:
            flame_name (str): The Flame name to check

        Returns:
            str: A new Flame name without the iter num if any.
        """
            
        flame_name = flame_name.strip()
        
        if flame_name:
            
            rp = flame_name.rpartition(FLAM3H_IN_ITERATIONS_FLAME_NAME_DIV)

            is_int = False
            try:
                if rp[-1] != flame_name:
                    int(rp[-1])
                    is_int = True
                else:
                    pass
            except:
                pass
            
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
            node (hou.SopNode): Current FLAM3H houdini node
            autoadd (int): Autoadd ON/OFF value. If ON, it will auto add the iteration number to the filename, otherwise not.

        Returns:
            str: _description_
        """        
        flame_name = datetime.now().strftime("Flame_%b-%d-%Y_%H%M%S")
        iter_num = node.parm(GLB_ITERATIONS).evalAsInt()
        return out_flame_utils.out_auto_add_iter_num(iter_num, flame_name, autoadd)
    
    
    @staticmethod
    def out_util_round_float(val) -> str:
        """remove floating Zero if it is an integer value ( ex: from '1.0' to '1' )

        Args:
            VAL (_type_): The value to remove the floating zeros from

        Returns:
            str: A value without the floating zeros
        """        
        if float(val).is_integer(): # type: ignore - float.is_integer() is a valid method for a float
            return str(int(float(val)))
        else:
            return str(round(float(val), ROUND_DECIMAL_COUNT))
        
        
    @staticmethod
    def out_util_round_floats(val_list: Union[list[list[str]], tuple[list]]) -> Union[list[str], list[list[str]], tuple[str]]:
        """remove floating Zero if it is an integer value ( ex: from '1.0' to '1' ) in a list or tuple of values 

        Args:
            VAL_LIST (list[list[str]]): A list of list[str] of values to rounds

        Returns:
            list[list[str]]: A list of list[str] with the rounded values if any
        """    
        return [[str(int(float(i))) if float(i).is_integer() else str(round(float(i), ROUND_DECIMAL_COUNT)) for i in item] for item in val_list]
        
        
    @staticmethod  
    def out_util_check_duplicate_var_section(vars: list) -> bool:
        """Check if any of the iterator sections (PRE, VAR or POST, same for FF) is using a variation multiple times.

        Args:
            vars (list): a section list of used variations

        Returns:
            bool: True if there are duplicates and False if not.
        """        
        result = []
        [result.append(x) for x in vars if x not in result]
        if(len(vars) != len(result)):
            return True
        return False
    
    
    @staticmethod
    def out_util_iterators_vars_duplicate(vars: list) -> list:
        """Collect duplicate variation's names per each iterator.

        Args:
            VARS (list): List of all variation's list names

        Returns:
            list: duplicate variation's names per each iterator
        """
        duplicate = []
        for iterator in vars:
            v = []
            d = []
            for var in iterator:
                if var not in v:
                    v.append(var)
                else:
                    if var not in d:
                        d.append(var)
            duplicate.append(d)
        
        return in_flame_utils.in_util_vars_flatten_unique_sorted(duplicate, in_flame_utils.in_util_make_NULL)

    

    @staticmethod
    def out_check_build_file(file_split: Union[tuple[str, str], list[str]], file_name: str, file_ext: str) -> str:
        """Used in conjuction with: def out_check_outpath()
        help to make spelling auto corrections to the provided output file path.

        Args:
            file_split (tuple[str, str]): Returns tuple "(head, tail)" where "tail" is everything after the final slash. Either part may be empty
            file_name (str): The input filename to be checked
            file_ext (str): the desired filename extension

        Returns:
            str: A corrected file path
        """    
        build_f = "/".join(file_split) + file_ext
        build_f_s = os.path.split(build_f)[0].split("/")
        build_f_s[:] = [item for item in build_f_s if item]
        # Clean location directories. ( maybe not needed but whatever )
        build_f_s_cleaned = [''.join(letter for letter in item if letter.isalnum() or letter in CHARACTERS_ALLOWED) for item in build_f_s]
        # append cleaned file_name
        build_f_s_cleaned.append(''.join(letter for letter in file_name if letter.isalnum() or letter in CHARACTERS_ALLOWED))
        # the file_ext start with a dot so its added as last
        return "/".join(build_f_s_cleaned) + file_ext
    
    
    @staticmethod
    def out_check_outpath(node: hou.SopNode, infile: str, file_ext: str, prx: str) -> Union[str, bool]:
        """Check for the validity of the provided output file path.

        Args:
            node (hou.SopNode): Current FLAM3H node.
            infile (str): THe file path to check.
            file_ext (str): Provide an extension to tell this function if it is a Flame file or a palette file.
            prx (str): A prefix for an automated file name to be provided for the XML Flame file or a Palette flame file.

        Returns:
            Union[str, bool]: Either a corrected/valid file path or False if not valid.
        """        
        new_name = datetime.now().strftime(f"{prx}_%b-%d-%Y_%H%M%S")
        
        file = os.path.expandvars(infile)
        file_s = [''.join(x.split(' ')) for x in os.path.split(file)]
        
        autopath = node.parm(PREFS_AUTO_PATH_CORRECTION).evalAsInt()

        if autopath:
            
            # Just in case lets check is a valid location
            if os.path.isdir(file_s[0]):

                filename_s = os.path.splitext(file_s[-1].strip())
                
                if filename_s[-1] == file_ext:
                    build_f_s = file.split("/")
                    build_f_s[:] = [item for item in build_f_s if item]
                    build_f_s[-1] = ''.join(letter for letter in build_f_s[-1] if letter.isalnum() or letter in CHARACTERS_ALLOWED)
                    return "/".join(build_f_s)
                
                elif not filename_s[-1] and filename_s[0]:
                    # this is done in case only the extension is left in the prm field
                    if file_s[-1] in file_ext and file_s[-1][0] == ".":
                        return out_flame_utils.out_check_build_file(file_s, new_name, file_ext)
                    else:
                        if not file_s[-1][0].isalnum():
                            return out_flame_utils.out_check_build_file(file_s, new_name, file_ext)
                        else:
                            return out_flame_utils.out_check_build_file(file_s, file_s[-1], file_ext)
                
                elif not filename_s[-1] and not filename_s[0]:
                    return out_flame_utils.out_check_build_file(file_s, new_name, file_ext)
                
                # this as last for now
                #
                # If there is a file extension and it match part or all of the file_ext string.
                #
                # This will execute only if the string match at the beginning of the file extension
                # otherwise the above if/elif statements would have executed already.
                elif len(filename_s) > 1 and filename_s[-1] in file_ext:
                    return out_flame_utils.out_check_build_file(file_s, filename_s[0], file_ext)
                else:
                    # Print out proper msg based on file extension
                    if OUT_FLAM3_FILE_EXT == file_ext:
                        print(f"{node.name()}.OUT: You selected an OUT file that is not a {prx} file type.")
                    elif OUT_PALETTE_FILE_EXT == file_ext:
                        print(f"{node.name()}.Palette: You selected an OUT file that is not a {prx} file type.")
                    return False
            else:
                # If the path string is empty we do not want to print out
                if file:
                    if OUT_FLAM3_FILE_EXT == file_ext:
                        print(f"{node.name()}.OUT: Select a valid OUT directory location.")
                    elif OUT_PALETTE_FILE_EXT == file_ext:
                        print(f"{node.name()}.Palette: Select a valid OUT directory location.")
                return False
        else:
            # just check if the user input is a valid file
            if os.path.isfile(file_s[0]):
                return infile
            else:
                # If the path string is empty we do not want to print out
                if file:
                    if OUT_FLAM3_FILE_EXT == file_ext:
                        print(f"{node.name()}.OUT: Select a valid OUT directory location.")
                    elif OUT_PALETTE_FILE_EXT == file_ext:
                        print(f"{node.name()}.Palette: Select a valid OUT directory location.")
                return False
            
 
    @staticmethod
    def out_affine_rot(affine: list[Union[tuple[str], list[str]]], angleDeg: float) -> list[Union[list[str], tuple[str]]]:
        """Every affine has an Angle parameter wich rotate the affine values internally.
        When we save out an iterator that use the angle parameter, we need to transform the affine by this angle
        and export the resulting values out so we can get the same result once we load it back.

        Args:
            affine (list[tuple]): X, Y, O afffine component
            angleDeg (float): a float value that represent the angle in degrees ( The iterator.affine's angle parameter )

        Returns:
            list[tuple]: A new affine list of tuples ( (X), (Y), (O) ) rotated by the angle amount.
        """
        if angleDeg != 0.0:      
            angleRad = hou.hmath.degToRad(angleDeg) # type: ignore
            m2 = hou.Matrix2((affine[0], affine[1]))
            rot = hou.Matrix2(((cos(angleRad), -(sin(angleRad))), (sin(angleRad), cos(angleRad))))
            new = (m2 * rot).asTupleOfTuples()
            return [new[0], new[1], affine[2]]
        else:
            return affine


    @staticmethod
    def out_xaos_cleanup(xaos: Union[list[str], list[list[str]], tuple[str]]) -> list[list[str]]:
        """Remove all inactive iterators from each xaos weight list.

        Args:
            xaos (Union[list[str], list[list[str]], tuple[str]]): All iterators xaos values.

        Returns:
            list[list[str]]: _description_
        """        
        xaos_cleaned = []
        for x in xaos:
            invert = x[::-1]
            trace = 0
            for idx, item in enumerate(x):
                if invert[idx-trace] == '1':
                    invert.pop(idx-trace) # type: ignore
                    trace = trace + 1
                else:
                    break
            xaos_cleaned.append(invert[::-1])
        return xaos_cleaned
    

    @staticmethod
    def out_xaos_collect(node: hou.SopNode, iter_count: int, prm: str) -> list[list[str]]:
        """Collect all xaos command string weights.
        Provide also a form of Undo in the case we enter non numeric characters instead.
        
        Allow for different combinations as:
        
        - Undo to preview state.
        
        - Fill with all: 1
        
        - Fill with all: 0 ( Zero )
        
        - Check for negative xaos values
        
        Negative values will be reset to a value of: 1

        Args:
            node (hou.SopNode): FLAM3H node
            iter_count (int): Iterator's count
            prm (str): xaos varnote parameter

        Returns:
            list[list[str]]: A list of xaos list[str] of values
        """   

        val = []
        val_prev = flam3h_iterator_utils.auto_set_xaos_data_get_XAOS_PREV(node)
        
        for iter in range(iter_count):
            iter_xaos = node.parm(f"{prm}_{iter+1}").eval()
            
            # If the xaos string is not empty
            if iter_xaos:
                strip = iter_xaos.split(':')
                
                # if you just type "xaos" only
                if str(iter_xaos.lower()).strip() == 'xaos':
                    if val_prev is not None:
                        # retrive from the history instead ( Undo )
                        val.append(val_prev[iter])
                    else:
                        # Otherwise reset to all values of 1
                        val.append([])
                        
                # if the first element of the strip is: "xaos"
                elif str(strip[0].lower()).strip() == 'xaos':
                    try:
                        build_strip = [str(float(str(x).strip())) if float(str(x).strip()) >= 0 else '1' for x in strip[1:iter_count+1] if x]
                        val.append([float(x.strip()) for x in build_strip])
                    except:
                        # ( Assuming the "xaos:" keyword is present )
                        # if we enterd an invalid string,
                        # retrive from the history instead ( Undo )
                        if val_prev is not None:
                            val.append(val_prev[iter])
                        else:
                            # Otherwise reset to all values of 1
                            val.append([])
                            
                # If the split fail to validate and it just start with the word: 'xaos'
                elif str(iter_xaos.lower()).strip().startswith('xaos'):
                    if val_prev is not None:
                        # retrive from the history instead ( Undo )
                        val.append(val_prev[iter])
                    else:
                        # Otherwise reset to all values of 1
                        val.append([])
                        
                else:
                    isNUM = False
                    try:
                        if isinstance(float(str(iter_xaos.lower()).strip()), float):
                            isNUM = True
                    except:
                        pass
                    # If a number is typed, fill all xaos weights with that number.
                    # If a floating point number is typed, use the integer part of it ( ex: 123.687 will become -> 123 )
                    if isNUM:
                        v = [str(int((float(str(iter_xaos.lower()).strip())))) if float(str(iter_xaos.lower()).strip()) >= 0 else '1' for x in range(iter_count)]
                        val.append(v)
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
            node (hou.SopNode): FLAM3H node
            fill (list[np.array]): List of [np.array] representing all xaos weights.
            prm (str): iterator vactive parameter.

        Returns:
            list[list[str]]: return a list of list[str] with the NO-active iterators taken into consideration.
        """    
        xaos_no_vactive = []
        for x in fill:
            collect = [str(item) for idx, item in enumerate(x) if node.parm(f"{prm}_{idx+1}").eval()]
            if collect:
                xaos_no_vactive.append(collect)
            else:
                xaos_no_vactive.append([])
        return xaos_no_vactive


    @staticmethod
    def _out_pretty_print(current, parent=None, index=-1, depth=0) -> None:
        """Reformat the XML data in a pretty way.

        Args:
            current (_type_): The Flame XML root we want to reformat.
            parent (_type_, optional): _description_. Defaults to None.
            index (int, optional): _description_. Defaults to -1.
            depth (int, optional): _description_. Defaults to 0.
        """        
        [out_flame_utils._out_pretty_print(node, current, i, depth + 1) for i, node in enumerate(current)]
        if parent is not None:
            if index == 0:
                parent.text = '\n' + ('  ' * depth)
            else:
                parent[index - 1].tail = '\n' + ('  ' * depth)
            if index == len(parent) - 1:
                current.tail = '\n' + ('  ' * (depth - 1))




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


    def out_presets_get_selected_menu_label(self) -> Union[str, None]:
        """Get the currently selected OUT preset menu label string.

        Returns:
            str: The selected menu preset menu label string if any or None
        """
        node = self.node

        if node.parm(OUT_ISVALID_FILE).eval():
            toggle_PREFS_ENUMERATE_MENU = node.parm(PREFS_ENUMERATE_MENU).eval()
            preset_id = int(node.parm(OUT_PRESETS).eval())
            menu_label = str(node.parm(OUT_PRESETS).menuLabels()[preset_id]).split(FLAM3H_ICON_STAR_FLAME_SAVE_ENTRIE)[-1].strip()

            if toggle_PREFS_ENUMERATE_MENU:
                # We are using "str.lstrip()" because the preset name has been "str.strip()" already in the above line.
                # and there are only the leading white spaces left from the menu enumaration index number string to remove.
                flame_name = ':'.join(str(menu_label).split(':')[1:]).lstrip()
            else:
                flame_name = menu_label
                
            return flame_name
        
        else:
            return None
    
    
    def out_presets_copy_menu_label_callback(self) -> None:
        """Get the currently selected OUT preset menu label string and copy it into the OUT Flame name string field.

        """
        
        node = self.node
        kwargs = self.kwargs
        
        if kwargs['ctrl']:
            flam3h_ui_msg_utils(kwargs).ui_OUT_presets_name_infos()
        else:
            menu_label = self.out_presets_get_selected_menu_label()
            if menu_label is not None:
                flame_name = self.out_remove_iter_num(menu_label)
                iter_num = node.parm(GLB_ITERATIONS).evalAsInt()
                autoadd = node.parm(OUT_AUTO_ADD_ITER_NUM).evalAsInt()
                flame_name_new = self.out_auto_add_iter_num(iter_num, flame_name, autoadd)
                node.setParms({OUT_FLAME_PRESET_NAME: flame_name_new})
                
                _MSG = f"{node.name()}: COPY Flame name -> {flame_name_new}"
                flam3h_general_utils.set_status_msg(_MSG, 'MSG')
                flam3h_general_utils.flash_message(node, f"{flame_name_new}")
                
            else:
                _MSG = f"{node.name()}: COPY Flame name -> Select an existing preset name. There are no presets to copy the name from."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                
                

    def out_palette_keys_count(self, palette_plus: int, keys: int, type: int, _MSG = True) -> str:
        """This is used to find the number of colors we want to export when saving out a Flame file.
        We need to always export as many colors to include the current color keys count in the palette based on a predefined set of value:
        So for example, if the current palette posses 270 color keys, we will export using the closest but greater menu entry whitch is: 512 (the smaller being: 256).
        The minimum will always be clamped at: 256

        Args:
            palette_plus (bool): "save palette 256+" toggle parameter value.
            keys (int): number of color keys in the palette.
            type (int): 0 for a Flame and 1 for a Palette.
            _MSG: (bool): Print a warning message or not. Default to: True

        Returns:
            str: number of color to export
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
                    return str(flam3h_palette_utils.find_nearest_idx(PALETTE_OUT_MENU_OPTIONS, keys))
            else:
                # Otherwise clamp to 1024 color keys
                if _MSG:
                    print(f"{str(self.node)}: the palette exceed the allowed amount of color keys and it has been clamped at: 1024")
                return PALETTE_COUNT_1024
        else:
            # Otherwise always export the Flame with 256 color palette
            return PALETTE_COUNT_256


    def menu_sensor_resolution(self) -> list:
        """Build sensor resolution menu parameter with a list of options.
        
        """

        outedit = self.node.parm(OUT_RENDER_PROPERTIES_EDIT).evalAsInt()
        menu=[]
        menuitems = ()
        if outedit:
            menuitems = (   "", "640x480", "HDTV 720", "HDTV 1080", "HDTV 2160 (4K)", # 1 2 3 4
                            "", "NTSC", "NTSC D1", "PAL", "PAL 16:9 (1 to 1)", # 6 7 8 9
                            "", "Full Ap 4K", "Full Ap 2K", "Acad 4K", "Acad 2K", "Scope 4K", "Scope 2K", "Vista 2K", # 11 12 13 14 15 16 17
                            "", "256^2", "512^2", "1024^2", "2048^2", "4096^2"  ) # 19 20 21 22 23
        else:
            menuitems = ( "", )
            
        for i, item in enumerate(menuitems):
            menu.append(i)
            menu.append(item)
        return menu


    def menu_sensor_resolution_set(self, update=True) -> None:
        """Set sensor resolution parameter based on user choice.
        """        
        node = self.node
        sel = int(node.parm(OUT_RENDER_PROPERTIES_RES_PRESETS_MENU).eval())
        res = { -1: None, 1: (640, 480), 2: (1280, 720), 3: (1920, 1080), 4: (3840, 2160), # 1 2 3 4
                -1: None, 6: (640, 486), 7: (720, 486), 8: (768, 586), 9: (1024, 576), # 6 7 8 9
                -1: None, 11: (4096, 3112), 12: (2048, 1556), 13: (3656, 2664), 14: (1828, 1332), 15: (3656, 3112), 16: (1828, 1556), 17: (3072, 2048), # 11 12 13 14 15 16 17
                -1: None, 19: (256, 256), 20: (512, 512), 21: (1024, 1024), 22: (2048, 2048), 23: (4096, 4096) } # 19 20 21 22 23
 
        if res.get(sel) is not None:
            self.node.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE): hou.Vector2(res.get(sel))}) # type: ignore

            if update:
                flam3h_general_utils(self.kwargs).util_set_front_viewer()
            else:
                update_sensor = self.node.parm(OUT_UPDATE_SENSOR).evalAsInt()
                if update_sensor:
                    flam3h_general_utils(self.kwargs).util_set_front_viewer()
        
        # reset to null value so we can set the same preset again
        node.setParms({OUT_RENDER_PROPERTIES_RES_PRESETS_MENU: "0"}) # type: ignore


        
    def reset_OUT_sensor(self) -> None:
        """Reset the OUT Camera sensor settings parameters tab.
        """
        
        node = self.node
        
        prms_out_sensor = ( OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE),
                            OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE) )
        
        prms_out_sensor_tuple = ( OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE),
                                  OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER) )
        
        # Sensor
        [node.parm(name).deleteAllKeyframes() for name in prms_out_sensor]
        [node.parmTuple(name).deleteAllKeyframes() for name in prms_out_sensor_tuple]
        node.setParms({prms_out_sensor_tuple[0]: hou.Vector2((1024, 1024))})
        node.setParms({prms_out_sensor_tuple[1]: hou.Vector2((0, 0))})
        node.setParms({prms_out_sensor[0]: 0})
        node.setParms({prms_out_sensor[1]: 400})


        
    def reset_OUT_render(self) -> None:
        """Reset the OUT Render settings parameters tab.
        """
        node = self.node
        
        prms_out_render = ( OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY),
                            OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS),
                            OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA),
                            OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER),
                            OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2),
                            OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY) )
        
        # Render
        [node.parm(name).deleteAllKeyframes() for name in prms_out_render]
        node.setParms({prms_out_render[0]: 1000})
        node.setParms({prms_out_render[1]: 3})
        node.setParms({prms_out_render[2]: 2.5})
        node.setParms({prms_out_render[3]: 1})
        node.setParms({prms_out_render[4]: 0})
        node.setParms({prms_out_render[5]: 0.333333})



    def reset_OUT_kwargs(self) -> None:
        """Build a multifunctional reset OUT render properties method.
        IT will allow to reset the entire tab or either only the Sensor or Render settings tab.
        """
        
        kwargs = self.kwargs
        
        if kwargs['ctrl']:
            self.reset_OUT_sensor()
            flam3h_general_utils.flash_message(self.node, f"OUT Camera sensor -> RESET")
            
        elif kwargs['shift']:
            self.reset_OUT_render()
            flam3h_general_utils.flash_message(self.node, f"OUT Render settings -> RESET")
            
        else:
            self.reset_OUT_sensor()
            self.reset_OUT_render()
            flam3h_general_utils.flash_message(self.node, f"OUT Render properties -> RESET")
        
        if self.node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt():
            flam3h_general_utils(self.kwargs).util_set_front_viewer()



    def reset_OUT_options(self) -> None:
        """Reset the OUT save options tab parameters.
        """
        node = self.node
        node.setParms({OUT_PALETTE_256_PLUS: 0})
        node.setParms({OUT_HSV_PALETTE_DO: 0})
        node.setParms({OUT_AUTO_ADD_ITER_NUM: 1})
        node.setParms({OUT_USE_FRACTORIUM_PRM_NAMES: 1})



    def reset_OUT(self, mode=0) -> None:
        """Reset the OUT flame render properties to their default.

        Args:
            mode (int, optional): _description_. Defaults to 0. 1 will reset the remainder of the parameters.
        """        
        node = self.node

        self.reset_OUT_options()
        self.reset_OUT_sensor()
        self.reset_OUT_render()
        
        # If we are in sensor viz and we reset, make sure the sensor is framed properly.
        if node.parm(OUT_RENDER_PROPERTIES_SENSOR).evalAsInt():
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
            node.setParms({OUT_PRESETS: "-1"})
            node.setParms({OUT_SYS_PRESETS: "-1"})
            node.setParms({OUT_FLAME_PRESET_NAME: ""})



    def out_xf_xaos_to(self) -> tuple:
        """Export in a tuple[str] the xaos TO values to write out
        Returns:
            tuple[str]: the xaos TO values to write out.
        """
        val = self.out_xaos_collect(self.node, self.iter_count, self.flam3h_iter_prm_names.xaos)
        fill = [np_pad(item, (0,self.iter_count-len(item)), 'constant', constant_values=1).tolist() for item in val]
        xaos_vactive = self.out_xaos_collect_vactive(self.node, fill, self.flam3h_iter_prm_names.main_vactive)
        return tuple([" ".join(x) for x in self.out_xaos_cleanup(self.out_util_round_floats(xaos_vactive))])



    def out_xf_xaos_from(self, mode=0) -> tuple:
        """Export in a tuple[str] the xaos FROM values to write out
        Args:
            mode (int, optional): mode=1 is for writing out flame file while the default mode=0 is for converting between xaos modes only
        Returns:
            tuple[str]: the xaos FROM values transposed into xaos TO values to write out.
        """
        val = self.out_xaos_collect(self.node, self.iter_count, self.flam3h_iter_prm_names.xaos)
        fill = [np_pad(item, (0,self.iter_count-len(item)), 'constant', constant_values=1) for item in val]
        t = np_transpose(np_resize(fill, (self.iter_count, self.iter_count))).tolist()
        if mode:
            xaos_vactive = self.out_xaos_collect_vactive(self.node, t, self.flam3h_iter_prm_names.main_vactive)
            return tuple([" ".join(x) for x in self.out_xaos_cleanup(self.out_util_round_floats(xaos_vactive))])
        else:
            return tuple([" ".join(x) for x in self.out_util_round_floats(t)])


    def menu_out_contents_presets_data(self) -> list:
        """Populate OUT parameter menu items for the SYS and OUT tab.

        Returns:
            list: _description_
        """
        node = self.node
        menu=[]
        xml = node.parm(OUT_PATH).evalAsString()
        # For the OUT Tab menu presets we are forced to use the class: _xml_tree(...)
        # Instead of the lightweight version class: _xml(...)
        apo = _xml_tree(xml)
        
        if apo.isvalidtree:
            
            if node.parm(PREFS_ENUMERATE_MENU).eval():
                
                for i, item in enumerate(apo.name):
                    menu.append(str(i))
                    menu.append(f"{FLAM3H_ICON_STAR_FLAME_SAVE_ENTRIE}  {str(i)}:  {item}     ")
            else:
                
                for i, item in enumerate(apo.name):
                    menu.append(str(i))
                    menu.append(f"{FLAM3H_ICON_STAR_FLAME_SAVE_ENTRIE}  {item}     ")
                    
            node.setCachedUserData('out_presets_menu', menu)
            return menu
        
        else:
            flam3h_iterator_utils.destroy_data(node, 'out_presets_menu')
            return MENU_PRESETS_EMPTY
        
        
        
    def menu_out_contents_presets(self) -> list:
        node = self.node
        data = node.cachedUserData('out_presets_menu')
        if data is not None:
            return data
        else:
            return self.menu_out_contents_presets_data()

    
    
    def out_auto_add_iter_data(self) -> tuple[int, str, int]:
        """Collect data needed by:
        
        def out_auto_add_iter_num_to_prm()
        
        def out_auto_change_iter_num_to_prm()

        Returns:
            tuple[int, str, int]: A tuple with the needed data
        """        
        node = self.node
        iter_num = node.parm(GLB_ITERATIONS).evalAsInt()
        flame_name = str(node.parm(OUT_FLAME_PRESET_NAME).eval()).strip()
        autoadd = node.parm(OUT_AUTO_ADD_ITER_NUM).evalAsInt()
        return iter_num, flame_name, autoadd


    # Callback script
    def out_auto_add_iter_num_to_prm(self) -> None:
        """Add the iteration number string to the OUT Flame name after you type one name string in.
        """        
        node = self.node
        iter_num, flame_name, autoadd = self.out_auto_add_iter_data()
        flame_name_new = self.out_auto_add_iter_num(iter_num, flame_name, autoadd)
        node.setParms({OUT_FLAME_PRESET_NAME: flame_name_new}) #type: ignore


    # Callback script
    def out_auto_change_iter_num_to_prm(self) -> None:
        """Change the iteration number string to the OUT Flame name when you change FLAM3H iterations.
        """      
        node = self.node
        iter_num, flame_name, autoadd = self.out_auto_add_iter_data()
        if autoadd:
            flame_name_new = self.out_auto_change_iter_num(iter_num, flame_name, autoadd)
            node.setParms({OUT_FLAME_PRESET_NAME: flame_name_new}) #type: ignore
            
            # Update "iter num on load" if "force iterations on Load" toggle is ON 
            if node.parm(IN_USE_ITER_ON_LOAD).eval():
                node.setParms({IN_ITER_NUM_ON_LOAD: iter_num})
        else:
            flame_name_new = self.out_remove_iter_num(flame_name)
            node.setParms({OUT_FLAME_PRESET_NAME: flame_name_new}) #type: ignore
            
        # Flash message if needed
        if flame_name_new:
            flam3h_general_utils.flash_message(node, f"{flame_name_new}")


    def out_flame_properties_build(self) -> dict:
        """Return a dictionary with all the flame properties to written out.

        Args:
            kwargs (dict): _description_

        Returns:
            dict: _description_
        """   
        # If "use Fractorium parametric prm names" OUT option is ON, lets append the EMBER name to the app name
        # so that we can pick up the proper parametric parameter names if we load it back in Houdini.
        if self.node.parm(OUT_USE_FRACTORIUM_PRM_NAMES).evalAsInt():
            XML_APP_NAME = f"{XML_APP_NAME_FRACTORIUM}-{XML_APP_NAME_FLAM3H}"
        else:
            XML_APP_NAME = XML_APP_NAME_FLAM3H
             
        f3p = out_flame_render_properties(self.kwargs)
        return {OUT_XML_VERSION: f'{XML_APP_NAME}-{flam3h_general_utils.my_system()}-{FLAM3H_VERSION}',
                XML_XF_NAME: f3p.flame_name,
                OUT_XML_FLAM3H_SYS_RIP: f3p.flam3h_sys_rip, # custom to FLAM3H only
                OUT_XML_FLAM3H_HSV: f3p.flam3h_cp_hsv, # custom to FLAM3H only
                OUT_XML_FLMA3H_MB_FPS: f3p.flam3h_mb_fps, # custom to FLAM3H only
                OUT_XML_FLMA3H_MB_SAMPLES: f3p.flam3h_mb_samples, # custom to FLAM3H only
                OUT_XML_FLMA3H_MB_SHUTTER: f3p.flam3h_mb_shutter, # custom to FLAM3H only
                OUT_XML_FLAM3H_CP_SAMPLES: f3p.flam3h_cp_samples, # custom to FLAM3H only
                OUT_XML_FLAM3H_PREFS_F3C: f3p.flam3h_prefs_f3c, # custom to FLAM3H only
                OUT_XML_FLAME_SIZE: f3p.flame_size, 
                OUT_XML_FLAME_CENTER: f3p.flame_center,
                OUT_XML_FLAME_SCALE: f3p.flame_scale,
                OUT_XML_FLAME_ROTATE: f3p.flame_rotate,
                OUT_XML_FLAME_BG: '0 0 0',
                OUT_XML_FLAME_SUPERSAMPLE: '2',
                OUT_XML_FLAME_FILTER: '0.5',
                OUT_XML_FLAME_QUALITY: f3p.flame_quality,
                OUT_XML_FLAME_BRIGHTNESS: f3p.flame_brightness,
                OUT_XML_FLAME_GAMMA: f3p.flame_gamma,
                OUT_XML_FLAME_GAMMA_THRESHOLD: '0.0423093658828749',
                OUT_XML_FLAME_K2: f3p.flame_k2,
                OUT_XML_FLAME_VIBRANCY: f3p.flame_vibrancy,
                OUT_XML_FLAME_POWER: f3p.flame_highlight,
                OUT_XML_FLAME_RADIUS: '9',
                OUT_XML_FLAME_ESTIMATOR_MINIMUM: '0',
                OUT_XML_FLAME_ESTIMATOR_CURVE: '0.4',
                OUT_XML_FLAME_PALETTE_MODE: 'linear',
                OUT_XML_FLAME_INTERPOLATION: 'linear',
                OUT_XML_FLAME_INTERPOLATION_TYPE: 'log'
                
                # The following are not really needed for our purpose and we assume all curves are defaults to start with.
                
                # OUT_XML_FLAME_RENDER_CURVES: f3p.flame_render_curves,
                # OUT_XML_FLAME_RENDER_OVERALL_CURVE: f3p.flame_overall_curve,
                # OUT_XML_FLAME_RENDER_RED_CURVE: f3p.flame_red_curve,
                # OUT_XML_FLAME_RENDER_GREEN_CURVE: f3p.flame_green_curve,
                # OUT_XML_FLAME_RENDER_BLUE_CURVE: f3p.flame_blue_curve
                }
        

    def out_flam3_compatibility_check_and_msg(self,
                                              names_VARS_PRE: list, 
                                              names_VARS: list, 
                                              names_VARS_POST: list, 
                                              flam3h_do_FF: bool, 
                                              names_VARS_PRE_FF: list, 
                                              names_VARS_FF: list, 
                                              names_VARS_POST_FF: list) -> bool:
        
        """Check if the Flame we want to write out is compatible with the FLAM3 flame format.
        If not, print out details to let us know what is wrong with it.
        
        _NOTE:
            This need a bit more work to format the collected data better.

        Args:
            names_VARS_PRE (list): A list of all iterators PRE variations used.
            names_VARS (list): A list of all iterators variations used.
            names_VARS_POST (list): A list of all iterators POST variations used.
            flam3h_do_FF (list): Is FF active or not.
            names_VARS_PRE_FF (list): A list of all iterators FF PRE variations used.
            names_VARS_FF (list): A list of all iterators FF variations used.
            names_VARS_POST_FF (list): A list of all iterators FF POST variations used.

        Returns:
            bool: Return True if the Flame is valid or False if not.
        """        
        
        # Here we are adding POST VARS and FF PRE VARS even tho they are only one slot,
        # just in case in the future I add more.
        bool_VARS_PRE = bool_VARS = bool_VARS_POST = bool_VARS_PRE_FF = bool_VARS_FF = bool_VARS_POST_FF = False

        # ITERATORS dublicate vars check
        pre_vars_duplicate_idx = []
        for idx, n in enumerate(names_VARS_PRE):
            if n:
                check = self.out_util_check_duplicate_var_section(n)
                if check:
                    pre_vars_duplicate_idx.append(str(idx+1))
                    if bool_VARS_PRE is False:
                        bool_VARS_PRE = True
        VARS_PRE_duplicate = []
        if bool_VARS_PRE:
            VARS_PRE_duplicate = in_flame_utils.in_util_vars_flatten_unique_sorted([self.out_util_iterators_vars_duplicate(names_VARS_PRE)], in_flame_utils.in_util_make_PRE)
        
        vars_duplicate_idx = []
        for idx, n in enumerate(names_VARS):
            if n:
                check = self.out_util_check_duplicate_var_section(n)
                if check:
                    vars_duplicate_idx.append(str(idx+1))
                    if bool_VARS is False:
                        bool_VARS = True
        VARS_duplicate = []
        if bool_VARS:
            VARS_duplicate = self.out_util_iterators_vars_duplicate(names_VARS)

        # FF dublicate vars check
        VARS_FF_duplicate = []
        VARS_POST_FF_duplicate = []
        if flam3h_do_FF:
            bool_VARS_FF = self.out_util_check_duplicate_var_section(names_VARS_FF)
            if bool_VARS_FF:
                VARS_FF_duplicate = in_flame_utils.in_util_vars_flatten_unique_sorted([names_VARS_FF], in_flame_utils.in_util_make_NULL)
                
            bool_VARS_POST_FF = self.out_util_check_duplicate_var_section(names_VARS_POST_FF)
            if bool_VARS_POST_FF:
                VARS_POST_FF_duplicate = in_flame_utils.in_util_vars_flatten_unique_sorted([names_VARS_POST_FF], in_flame_utils.in_util_make_POST)
            
        # Build messages accordinlgy
        # This need a bit more work in the way it is formatted and presented to the user.
        if bool_VARS_PRE or bool_VARS or bool_VARS_POST or bool_VARS_PRE_FF or bool_VARS_FF or bool_VARS_POST_FF:
            
            node = self.node
            ui_text = "Multiple variations of the same type not allowed.\nShow Details to learn more."
            ALL_msg = f"Node: {node.name()}\nType: Warning:\n"
            
            VARS_PRE_msg = f"\nPRE:\nYou are using the same PRE variation multiple times inside iterator:\n-> {', '.join(pre_vars_duplicate_idx)}\n-> {', '.join(VARS_PRE_duplicate)}\n"
            VARS_msg = f"VAR:\nYou are using the same variation multiple times inside iterator:\n-> {', '.join(vars_duplicate_idx)}\n-> {', '.join(VARS_duplicate)}\n"
            VARS_FF_msg = f"FF VAR:\nYou are using the same variation multiple times inside the FF VAR section.\n-> {', '.join(VARS_FF_duplicate)}\n"
            VARS_POST_FF_msg = f"FF POST:\nYou are using the same POST variation multiple times inside the FF POST section.\n-> {', '.join(VARS_POST_FF_duplicate)}\n"
            
            HELP_msg  = ""
            HELP_msg += f"\nNOTE:\n"
            HELP_msg += f"While this is doable within the tool, it is not compatible with FLAM3 file format.\nIt require that a variation is used only once per type ( types: PRE, VAR, POST )\notherwise you wont be able to save out the same result neither to load it back.\nFor example you are not allowed to use two Spherical variations inside an iterator VAR section.\nYou can however use one Spherical variation inside the VAR section, one Spherical inside the PRE section and one inside the POST section.\n"
            HELP_msg += f"\nTIP:\n"
            HELP_msg += f"Save the hip file instead if you desire to keep the Flame result as it is now.\nFractorium, Apophysis and all other FLAM3 compatible applications obey to the same rule."
            
            if bool_VARS_PRE:
                ALL_msg += VARS_PRE_msg
            if bool_VARS:
                ALL_msg += "\n" + VARS_msg
            if bool_VARS_FF:
                ALL_msg += "\n" + VARS_FF_msg
            if bool_VARS_POST_FF:
                ALL_msg += "\n" + VARS_POST_FF_msg
            
            ALL_msg += HELP_msg
            
            _MSG = f"{node.name()}: FLAM3 Compatibility -> The FLAM3 format is incompatible with the fractal Flame you are attempting to save."
            flam3h_general_utils.set_status_msg(_MSG, 'WARN')
            if hou.isUIAvailable():
                hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Compatibility", details=ALL_msg, details_label=None, details_expanded=False) # type: ignore
            flam3h_general_utils.set_status_msg('', 'MSG')
            return False
        else:
            return True
        
        
    # Not used yet
    def out_collect_var_section_names(self, var_section="VAR") -> Union[list[str], None]:
        """Collect all the variation's names inside any of the available sections (PRE, VAR, POST)
        
        Args:
            section (str): Default to: 'VAR'. Desired variation's section to query, Can be one of: 'PRE', 'VAR' or 'POST' keynames.

        Returns:
            list[str]: List of used variations in this iterator/xform
        """
        # Build var parameter's sections
        prm_sections_T = {'VAR': flam3h_iterator.sec_varsT, 'PRE': flam3h_iterator.sec_prevarsT, 'POST': flam3h_iterator.sec_postvarsT}
        prm_sections_W = {'VAR': flam3h_iterator.sec_varsW, 'PRE': flam3h_iterator.sec_prevarsW[1:], 'POST': flam3h_iterator.sec_postvarsW}
        
        # Get correct parameter's names based on the desired var section
        T_tuple = prm_sections_T.get(var_section)
        W_tuple = prm_sections_W.get(var_section)
        
        if T_tuple is not None and W_tuple is not None:
            assert T_tuple is not None
            assert W_tuple is not None
            node = self.node
            names = []
            for iter in range(node.parm(FLAME_ITERATORS_COUNT).evalAsInt()):
                _MP_IDX = str(int(iter + 1))
                for idx, prm in enumerate(W_tuple):
                    prm_w = node.parm(f"{prm[0]}{_MP_IDX}").eval()
                    if prm_w != 0:
                        v_type = node.parm(f"{T_tuple[idx]}{_MP_IDX}").eval()
                        names.append(in_flame_utils.in_get_var_name_from_dict(VARS_FLAM3_DICT_IDX, v_type))
                    
            return names
        else:
            return None
        

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
            varsPRM (tuple): FLAM3H variation's types and their parametric parameters names.
            TYPES_tuple (tuple): FLAM3H variation's types parameters names.
            WEIGHTS_tuple (tuple): FLAM3H variation's weights parameters names.
            XFORM (lxmlET.Element): The current xform (lxmlET.Element) to populate.
            MP_IDX (str): Current multiparameter index
            FUNC (Callable): Callable definition to convert variation's names between VAR, PRE and POST: in_flame_utils.in_util_make_NULL, in_flame_utils.in_util_make_PRE, in_flame_utils.in_util_make_POST

        Returns:
            list[str]: List of used variation in this iterator/xform
        """
        node = self.node
        names = []
        for idx, prm in enumerate(WEIGHTS_tuple):
            prm_w = node.parm(f"{prm[0]}{MP_IDX}").eval()
            if prm_w != 0:
                v_type = node.parm(f"{TYPES_tuple[idx]}{MP_IDX}").eval()
                v_name = in_flame_utils.in_get_var_name_from_dict(VARS_FLAM3_DICT_IDX, v_type)
                names.append(v_name)
                XFORM.set(FUNC(v_name), self.out_util_round_float(prm_w))
                vars_prm = varsPRM[v_type]
                if vars_prm[-1]:
                    f3h_prm = varsPRM[v_type][1:-1]

                    # If OUT Tab -> USE_FRACTORIUM_PRM_NAMES toggle is ON
                    # make sure to use the parametric variation's parameters names that Fractorium expect.
                    apo_prm = flam3h_varsPRM_APO.varsPRM[v_type]
                    if node.parm(OUT_USE_FRACTORIUM_PRM_NAMES).evalAsInt():
                        out_prm = in_flame_utils.in_prm_name_exceptions(v_type, XML_APP_NAME_FRACTORIUM, apo_prm)[1:-1]
                    else:
                        out_prm = apo_prm[1:-1]
                        
                    for id, p in enumerate(out_prm):
                        if f3h_prm[id][-1]:
                            for i, n in enumerate(p):
                                vals = node.parmTuple(f"{f3h_prm[id][0]}{MP_IDX}").eval()
                                XFORM.set(FUNC(p[i]), self.out_util_round_float(vals[i]))
                        else:
                            val = node.parm(f"{f3h_prm[id][0]}{MP_IDX}").eval()
                            XFORM.set(FUNC(p[0]), self.out_util_round_float(val))
        return names



    def out_build_XML(self, flame: lxmlET.Element) -> bool: # type: ignore
        """Build the XML Flame data to be then written out.

        Args:
            kwargs (dict): _description_
            root (lxmlET.Element): The root of either the flame to be written out or the flame file to append the new flame to.

        Returns:
            bool: return True if the Flame is a compatible FLAM3 flame or False if not.
        """        
        # Build Flame properties
        for key, value in self.out_flame_properties_build().items():
            if value is not False: # this is important for custom flam3h xml values. Every class def that collect those must return False in case we do not need them.
                flame.set(key, value)
        # Build xforms
        name_PRE_BLUR = ""
        names_VARS = []
        names_VARS_PRE = []
        names_VARS_POST = []
        f3d = out_flame_xforms_data(self.kwargs)
        for iter in range(f3d.iter_count):
            mp_idx = str(int(iter + 1))
            if int(f3d.xf_vactive[iter]):
                xf = lxmlET.SubElement(flame, XML_XF) # type: ignore
                xf.tag = XML_XF
                xf.set(XML_XF_NAME, f3d.xf_name[iter])
                xf.set(XML_XF_WEIGHT, f3d.xf_weight[iter])
                xf.set(XML_XF_COLOR, f3d.xf_color[iter])
                xf.set(XML_XF_SYMMETRY, f3d.xf_symmetry[iter])
                xf.set(XML_XF_COLOR_SPEED, str((1.0-float(f3d.xf_symmetry[iter]))/2.0))
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
                names_VARS.append(self.out_populate_xform_vars_XML(flam3h_varsPRM.varsPRM, flam3h_iterator.sec_varsT, flam3h_iterator.sec_varsW, xf, mp_idx, in_flame_utils.in_util_make_NULL))
                names_VARS_PRE.append(self.out_populate_xform_vars_XML(flam3h_varsPRM.varsPRM, flam3h_iterator.sec_prevarsT, flam3h_iterator.sec_prevarsW[1:], xf, mp_idx, in_flame_utils.in_util_make_PRE))
                names_VARS_POST.append(self.out_populate_xform_vars_XML(flam3h_varsPRM.varsPRM, flam3h_iterator.sec_postvarsT, flam3h_iterator.sec_postvarsW, xf, mp_idx, in_flame_utils.in_util_make_POST))
        # Build finalxform
        names_VARS_FF = []
        names_VARS_PRE_FF = []
        names_VARS_POST_FF = []
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
            names_VARS_FF = self.out_populate_xform_vars_XML(flam3h_varsPRM_FF(f"{PRX_FF_PRM}").varsPRM_FF(), flam3h_iterator_FF.sec_varsT_FF, flam3h_iterator_FF.sec_varsW_FF, finalxf, '', in_flame_utils.in_util_make_NULL)
            names_VARS_PRE_FF = self.out_populate_xform_vars_XML(flam3h_varsPRM_FF(f"{PRX_FF_PRM_POST}").varsPRM_FF(), flam3h_iterator_FF.sec_prevarsT_FF, flam3h_iterator_FF.sec_prevarsW_FF, finalxf, '', in_flame_utils.in_util_make_PRE)
            names_VARS_POST_FF = self.out_populate_xform_vars_XML(flam3h_varsPRM_FF(f"{PRX_FF_PRM_POST}").varsPRM_FF(), flam3h_iterator_FF.sec_postvarsT_FF, flam3h_iterator_FF.sec_postvarsW_FF, finalxf, '', in_flame_utils.in_util_make_POST)
        # Build palette
        palette = lxmlET.SubElement(flame, XML_PALETTE) # type: ignore
        palette.tag = XML_PALETTE
        palette.set(XML_PALETTE_COUNT, self.out_palette_keys_count(self.palette_plus_do, len(self.palette.keys()), 0, False)) # When saving a Flame out, we always use a 256 color palette unless the OUT tab option "save palette 256+" is ON
        palette.set(XML_PALETTE_FORMAT, PALETTE_FORMAT)
        palette.text = f3d.palette_hex

        # Get unique plugins used
        names_VARS_flatten_unique = in_flame_utils.in_util_vars_flatten_unique_sorted(names_VARS+[names_VARS_FF], in_flame_utils.in_util_make_NULL)
        names_VARS_PRE_flatten_unique = in_flame_utils.in_util_vars_flatten_unique_sorted(names_VARS_PRE+[names_VARS_PRE_FF]+list(map(lambda x: in_flame_utils.in_util_make_VAR([x]) if x else x, [name_PRE_BLUR])), in_flame_utils.in_util_make_PRE)
        names_VARS_POST_flatten_unique = in_flame_utils.in_util_vars_flatten_unique_sorted(names_VARS_POST+[names_VARS_POST_FF], in_flame_utils.in_util_make_POST)
        # Set unique used 'plugins' and 'new linear' as last
        flame.set(XML_FLAME_PLUGINS, i_cleandoc(" ".join(names_VARS_PRE_flatten_unique + names_VARS_flatten_unique + names_VARS_POST_flatten_unique)))
        flame.set(XML_FLAME_NEW_LINEAR, '1')
        
        return self.out_flam3_compatibility_check_and_msg(names_VARS_PRE, names_VARS, names_VARS_POST, f3d.flam3h_do_FF, names_VARS_PRE_FF, names_VARS_FF, names_VARS_POST_FF)



    def out_new_XML(self, outpath: str) -> None:
        """Write out a new XML flame file with only the current FLAM3H flame preset.

        Args:
            kwargs (dict): _description_
            outpath (str): Current OUT flame full file path.
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
            _MSG = f"{str(self.node)}: SAVE Flame: New -> Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Flame SAVED")



    def out_new_XML_clipboard(self) -> None:
        """Write out a new XML flame file with only the current FLAM3H flame preset into the clipboard.

        Args:
        """ 
        node = self.node
        
        root = lxmlET.Element(XML_FLAME_NAME) # type: ignore
        
        if self.out_build_XML(root):
            self._out_pretty_print(root)
            flame = lxmlET.tostring(root, encoding="unicode") # type: ignore
            hou.ui.copyTextToClipboard(flame) # type: ignore
            
            node.setParms({OUT_FLAME_PRESET_NAME: ''}) #type: ignore
            _MSG = f"{str(self.node)}: SAVE Flame: Clipboard -> Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Flame SAVED to the Clipboard")



    def out_append_XML(self, apo_data: in_flame, out_path: str) -> None:
        """Append a XML flame file to the current OUT flame lib file.

        Args:
            kwargs (dict): _description_
            apo_data (in_flame): Current OUT flame lib file data for all its flame presets.
            out_path (str): Current OUT flame full file path.
        """                
        node = self.node
        
        # with lxmlET
        # tree = lxmlET.parse(apo_data.xmlfile) # type: ignore
        # root = tree.getroot()
        root = apo_data.tree.getroot()
        
        flame = lxmlET.SubElement(root, XML_FLAME_NAME) # type: ignore
        flame.tag = XML_FLAME_NAME
        
        if self.out_build_XML(flame):
            self._out_pretty_print(root)
            tree = lxmlET.ElementTree(root)
            tree.write(out_path)
            
            node.setParms({OUT_FLAME_PRESET_NAME: ''}) #type: ignore
            _MSG = f"{str(self.node)}: SAVE Flame: Append -> Completed"
            flam3h_general_utils.set_status_msg(_MSG, 'IMP')
            flam3h_general_utils.flash_message(node, f"Flame SAVED: Append")



    def out_XML(self) -> None:
        """Write out the XML Flame file.
        It allow for writing out a new file or append to the current XML flame file.
        """        
        node = self.node
        kwargs = self.kwargs
        iterators_num = node.parm(FLAME_ITERATORS_COUNT).evalAsInt()
        
        # if there is at least one iterator
        if iterators_num:
            
            out_path = node.parm(OUT_PATH).evalAsString()
            out_path_checked = self.out_check_outpath(node, out_path, OUT_FLAM3_FILE_EXT, 'Flame')
            
            # Write to the clipboard
            if kwargs['alt']:
                self.out_new_XML_clipboard()
                
            # Otherwise if the output path is valid
            elif out_path_checked is not False:
                
                if kwargs['shift']:
                    flam3h_general_utils.util_open_file_explorer(out_path_checked)
                    
                else:

                    if flam3h_general_utils.isLOCK(out_path_checked):
                        ui_text = f"This Flame library is Locked."
                        ALL_msg = f"This Flame library is Locked and you can not modify this file.\n\nTo Lock a Flame lib file just rename it using:\n\"{FLAM3H_LIB_LOCK}\" as the start of the filename.\n\nOnce you are happy with a Flame library you built, you can rename the file to start with: \"{FLAM3H_LIB_LOCK}\"\nto prevent any further modifications to it. For example if you have a lib file call: \"my_grandJulia.flame\"\nyou can rename it to: \"{FLAM3H_LIB_LOCK}_my_grandJulia.flame\" to keep it safe."
                        _MSG = "FLAME library file -> is LOCKED"
                        # Print to Houdini's status bar
                        flam3h_general_utils.set_status_msg(f"{node.name()}: {_MSG}", 'WARN')
                        flam3h_general_utils.flash_message(node, _MSG)
                        
                        # Pop up message window
                        if hou.isUIAvailable():
                            hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3H: Lib Lock", details=ALL_msg, details_label=None, details_expanded=False) # type: ignore
                        # Clear up Houdini's status bar msg
                        flam3h_general_utils.set_status_msg('', 'MSG')
                        
                    else:
                        
                        if kwargs["ctrl"]:
                            node.setParms({OUT_PATH: str(out_path_checked)}) #type: ignore
                            self.out_new_XML(str(out_path_checked))
                            
                        else:
                            apo_data = in_flame(self.node, str(out_path_checked))
                            node.setParms({OUT_PATH: str(out_path_checked)}) #type: ignore
                            
                            if apo_data.isvalidtree:
                                self.out_append_XML(apo_data, str(out_path_checked))
                                
                            else:
                                self.out_new_XML(str(out_path_checked))
                                
                        flam3h_general_utils(kwargs).flam3h_init_presets_OUT_PRESETS()

            else:
                _MSG = f"{node.name()}: SAVE Flame -> Select a valid output file or a valid filename to create first."
                flam3h_general_utils.set_status_msg(_MSG, 'WARN')
                flam3h_general_utils.flash_message(node, f"Flame OUT -> Select a valid output file")




    '''
    The following definitions will prep all the data into proper strings to be then written into the XML flame/xform data keys/entries.
    The name of each is self explanatory of the data they will prep and two different classes will be used to hold all this data:
    
    OUT FLAME RENDER PROPERTIES:
    class out_flame_render_properties(out_flame_utils):
    
    OUT FLAME XFORMS DATA:
    class out_flame_xforms_data(out_flame_utils):
    
    This way they can be called elsewere anytime so to have this data always at hand.
    '''
    
    def __out_flame_data(self, prm_name='') -> str:
        if prm_name:
            prm_type = False
            try:
                prm = self.node.parmTuple(prm_name)
                prm_type = True
            except:
                prm = self.node.parm(prm_name)
            if prm_type:
                return ' '.join([str(self.out_util_round_float(x.eval())) for x in prm])
            else:
                if type(prm) is not str:
                    return str(self.node.parm(prm_name).eval())
                else:
                    return self.out_util_round_float(self.node.parm(prm_name).eval())
        else:
            print(f"{str(self.node)}: parameter name: \"{prm_name}\" not found. Please pass in a valid FLAM3H parameter name.")
            return ''


    def __out_flame_name(self, prm_name=OUT_XML_RENDER_HOUDINI_DICT.get(XML_XF_NAME)) -> str:
        flame_name = self.node.parm(prm_name).eval()
        autoadd = self.node.parm(OUT_AUTO_ADD_ITER_NUM).evalAsInt()
        
        if not flame_name:
            return self.out_flame_default_name(self.node, autoadd)
        else:
            # otherwise get that name and use it
            iter_num = self.node.parm(GLB_ITERATIONS).evalAsInt()
            return self.out_auto_add_iter_num(iter_num, flame_name, autoadd)
        
        
    def __out_xf_data(self, prm_name: str) -> tuple:
        val = [str(self.out_util_round_float(self.node.parm(f"{prm_name}_{iter+1}").eval())) for iter in range(self.iter_count)]
        return tuple(val)


    def __out_xf_name(self) -> tuple:
        val = [self.node.parm(f"{self.flam3h_iter_prm_names.main_note}_{iter+1}").eval() for iter in range(self._iter_count)]
        return tuple(val)
    
    
    def __out_finalxf_name(self) -> str:
        FF_name = self.node.parm(f"{PRX_FF_PRM}{self.flam3h_iter_prm_names.main_note}").eval()
        return FF_name

    
    def __out_xf_pre_blur(self) -> tuple:
        val = [str( self.node.parm(f"{self.flam3h_iter_prm_names.prevar_weight_blur}_{iter+1}").eval() ) if self.node.parm(f"{self.flam3h_iter_prm_names.prevar_weight_blur}_{iter+1}").eval() > 0 else '' for iter in range(self.iter_count)]
        return tuple(val)


    def __out_xf_xaos(self) -> tuple:
        if self.xm:
            return self.out_xf_xaos_from(1)
        else:
            return self.out_xf_xaos_to()


    def __out_xf_preaffine(self) -> tuple[tuple, tuple, tuple]:
        val = []
        f3h_val = []
        f3h_angleDeg = []
        for iter in range(self.iter_count):
            collect = [self.node.parmTuple(f"{prm[0]}{iter+1}").eval() for prm in self.flam3h_iter.sec_preAffine[:-1]]
            angleDeg = self.node.parm(f"{self.flam3h_iter.sec_preAffine[-1][0]}{iter+1}").eval()
            f3h_angleDeg.append(str(round(self.node.parm(f"{self.flam3h_iter.sec_preAffine[-1][0]}{iter+1}").eval(), ROUND_DECIMAL_COUNT)))
            flatten = [item for sublist in self.out_affine_rot(collect, angleDeg) for item in sublist]
            f3h_flatten = [item for sublist in collect for item in sublist]
            val.append([str(x) for x in flatten])
            f3h_val.append([str(x) for x in f3h_flatten])
        return tuple([" ".join(x) for x in self.out_util_round_floats(val)]), tuple([" ".join(x) for x in self.out_util_round_floats(f3h_val)]), tuple(f3h_angleDeg)
    
    
    def __out_xf_postaffine(self) -> tuple[tuple, tuple, tuple]:
        val = []
        f3h_val = []
        f3h_angleDeg = []
        for iter in range(self.iter_count):
            if self.node.parm(f"{self.flam3h_iter_prm_names.postaffine_do}_{iter+1}").eval():
                collect = [self.node.parmTuple(f"{prm[0]}{iter+1}").eval() for prm in self.flam3h_iter.sec_postAffine[1:-1]]
                angleDeg = self.node.parm(f"{self.flam3h_iter.sec_postAffine[-1][0]}{iter+1}").eval()
                if AFFINE_IDENT != [item for sublist in collect for item in sublist] or angleDeg != 0:
                    f3h_angleDeg.append(str(round(self.node.parm(f"{self.flam3h_iter.sec_postAffine[-1][0]}{iter+1}").eval(), ROUND_DECIMAL_COUNT)))
                    flatten = [item for sublist in self.out_affine_rot(collect, angleDeg) for item in sublist]
                    f3h_flatten = [item for sublist in collect for item in sublist]
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
        collect = [self.node.parmTuple(f"{prm[0]}").eval() for prm in self.flam3h_iter_FF.sec_preAffine_FF[:-1]]
        angleDeg = self.node.parm(f"{self.flam3h_iter_FF.sec_preAffine_FF[-1][0]}").eval()
        f3h_angleDeg = str(angleDeg)
        f3h_affine = self.out_util_round_floats(collect)
        if angleDeg != 0.0:
            affine = self.out_util_round_floats(self.out_affine_rot(collect, angleDeg)) # type: ignore
        else:
            affine = f3h_affine
        flatten = [item for sublist in affine for item in sublist]
        f3h_flatten = [item for sublist in f3h_affine for item in sublist]
        return " ".join(flatten), " ".join(f3h_flatten), f3h_angleDeg
    
    
    def __out_finalxf_postaffine(self) -> tuple[str, str, str]:
        if self.node.parm(f"{PRX_FF_PRM}{self.flam3h_iter_prm_names.postaffine_do}").eval():
            collect = [self.node.parmTuple(f"{prm[0]}").eval() for prm in self.flam3h_iter_FF.sec_postAffine_FF[1:-1]]
            angleDeg = self.node.parm(f"{self.flam3h_iter_FF.sec_postAffine_FF[-1][0]}").eval()
            if AFFINE_IDENT != [item for sublist in collect for item in sublist] or angleDeg != 0:
                f3h_angleDeg = str(angleDeg)
                f3h_affine = self.out_util_round_floats(collect)
                if angleDeg != 0.0:
                    affine = self.out_util_round_floats(self.out_affine_rot(collect, angleDeg)) # type: ignore
                else:
                    affine = f3h_affine
                flatten = [item for sublist in affine for item in sublist]
                f3h_flatten = [item for sublist in f3h_affine for item in sublist]
                return " ".join(flatten), " ".join(f3h_flatten), f3h_angleDeg
            else:
                return '', '', ''
        else:
            return '', '', ''
    
    
    def __out_palette_hex(self) -> str:

        _PALETTE_KEYS_OUT = self.out_palette_keys_count(self.palette_plus_do, len(self.palette.keys()), 0)
        
        POSs = list(iter_islice(iter_count(0, 1.0/(int(_PALETTE_KEYS_OUT)-1)), int(_PALETTE_KEYS_OUT)))
        HEXs = [flam3h_palette_utils.rgb_to_hex(tuple(self.palette.lookup(p))) for p in POSs]
        n = 8
        hex_grp = [HEXs[i:i+n] for i in range(0, len(HEXs), n)] 
        hex_join = ["      " + "".join(grp) + "\n" for grp in hex_grp] # 6 time \s
        return "\n" + "".join(hex_join) + "    " # 4 times \s
        
    
    # custom to FLAM3H only
    def __out_flame_data_flam3h_hsv(self, prm_name=CP_RAMP_HSV_VAL_NAME) -> Union[str, bool]:

        if prm_name == CP_RAMP_HSV_VAL_NAME:
            # This is only for OUT ramp HSV vals.
            # If we are saving out a flame with the HSV ramp, 
            # we do not want to export the HSV values in the XML file anymore
            # so to not overimpose a color correction once we load it back.
            if self.palette_hsv_do:
                return False
            else:
                # Here we go ahead since we know the prm CP_RAMP_HSV_VAL_NAME is a tuple
                prm = self.node.parmTuple(prm_name).eval()
                # If the HSV values are at their defaults, do not export them into the XML file
                if prm[0] == prm[1] == prm[2] == 1:
                    return False
                else:
                    return ' '.join([self.out_util_round_float(x) for x in prm])
        else:
            print(f"{str(self.node)}: parameter name: \"{prm_name}\" not found. Please pass in a valid FLAM3H ramp hsv parameter name.")
            return False
        
        
    # custom to FLAM3H only
    def __out_flame_data_flam3h_mb_val(self, prm_name='') -> Union[str, bool]:

        if self.flam3h_mb_do:
            try:
                return self.out_util_round_float(self.node.parm(prm_name).eval())
            except:
                print(f"{str(self.node)}: parameter name: \"{prm_name}\" not found. Please pass in a valid FLAM3H val parameter name.")
                return False
        else:
            return False
        
        
    # custom to FLAM3H only
    def __out_flame_data_flam3h_toggle(self, toggle: bool) -> str:
        return str(toggle)
    
    
    # custom to FLAM3H only
    def __out_flame_palette_lookup_samples(self) -> Union[str, bool]:
        if self.palette_plus_do:
            keys = out_flame_utils(self.kwargs).out_palette_keys_count(self.palette_plus_do, len(self.palette.keys()), 0, False)
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

    def __init__(self, kwargs: dict) -> None:
        super().__init__(kwargs)
        self._flame_name = self._out_flame_utils__out_flame_name() # type: ignore
        self._flame_size = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE)) # type: ignore
        self._flame_center = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER)) # type: ignore
        self._flame_scale = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE)) # type: ignore
        self._flame_rotate = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE)) # type: ignore
        self._flame_quality = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY)) # type: ignore
        self._flame_brightness = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS)) # type: ignore
        self._flame_gamma = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA)) # type: ignore
        self._flame_k2 = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2)) # type: ignore
        self._flame_vibrancy = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY)) # type: ignore
        self._flame_highlight = self._out_flame_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER)) # type: ignore
        
        # The following are not really needed for our purpose and we assume all curves are defaults to start with.

        # self._flame_render_curves = OUT_XML_FLAME_RENDER_OVERALL_CURVE_VAL
        # self._flame_overall_curve = OUT_XML_FLAME_RENDER_OVERALL_CURVE_VAL
        # self._flame_red_curve = OUT_XML_FLAME_RENDER_RED_CURVE_VAL
        # self._flame_green_curve = OUT_XML_FLAME_RENDER_GREEN_CURVE_VAL
        # self._flame_blue_curve = OUT_XML_FLAME_RENDER_BLUE_CURVE_VAL
        
        # custom to FLAM3H only
        self._flam3h_sys_rip = self._out_flame_utils__out_flame_data_flam3h_toggle(self._flam3h_rip) # type: ignore
        self._flam3h_cp_hsv = self._out_flame_utils__out_flame_data_flam3h_hsv() # type: ignore
        self._flam3h_mb_fps = self._out_flame_utils__out_flame_data_flam3h_mb_val(MB_FPS) # type: ignore
        self._flam3h_mb_samples = self._out_flame_utils__out_flame_data_flam3h_mb_val(MB_SAMPLES) # type: ignore
        self._flam3h_mb_shutter = self._out_flame_utils__out_flame_data_flam3h_mb_val(MB_SHUTTER) # type: ignore
        self._flam3h_cp_samples = self._out_flame_utils__out_flame_palette_lookup_samples() # type: ignore
        self._flam3h_prefs_f3c = self._out_flame_utils__out_flame_data_flam3h_toggle(self._flam3h_f3c) # type: ignore
        


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
    
    # The following are not really needed for our purpose and we assume all curves are defaults to start with.
    
    # @property
    # def flame_render_curves(self):
    #     return self._flame_render_curves
    
    # @property
    # def flame_overall_curve(self):
    #     return self._flame_overall_curve
    
    # @property
    # def flame_red_curve(self):
    #     return self._flame_red_curve
    
    # @property
    # def flame_green_curve(self):
    #     return self._flame_green_curve
    
    # @property
    # def flame_blue_curve(self):
    #     return self._flame_blue_curve
    
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
    
    def __init__(self, kwargs: dict) -> None:
        super().__init__(kwargs)
        # FLAM3 data
        self._xf_name = self._out_flame_utils__out_xf_name() # type: ignore
        self._xf_vactive = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.main_vactive) # type: ignore
        self._xf_weight = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.main_weight) # type: ignore
        self._xf_xaos = self._out_flame_utils__out_xf_xaos() # type: ignore
        self._xf_pre_blur = self._out_flame_utils__out_xf_pre_blur() # type: ignore
        self._xf_color = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.shader_color) # type: ignore
        self._xf_symmetry = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.shader_speed) # type: ignore
        self._xf_opacity = self._out_flame_utils__out_xf_data(self.flam3h_iter_prm_names.shader_alpha) # type: ignore
        self._xf_preaffine = self._out_flame_utils__out_xf_preaffine()[0] # type: ignore
        self._xf_f3h_preaffine = self._out_flame_utils__out_xf_preaffine()[1] # type: ignore
        self._xf_f3h_preaffine_angle = self._out_flame_utils__out_xf_preaffine()[2] # type: ignore
        self._xf_postaffine = self._out_flame_utils__out_xf_postaffine()[0] # type: ignore
        self._xf_f3h_postaffine = self._out_flame_utils__out_xf_postaffine()[1] # type: ignore
        self._xf_f3h_postaffine_angle = self._out_flame_utils__out_xf_postaffine()[2] # type: ignore
        self._palette_hex = self._out_flame_utils__out_palette_hex() # type: ignore
        self._finalxf_name = self._out_flame_utils__out_finalxf_name() # type: ignore
        self._finalxf_preaffine = self._out_flame_utils__out_finalxf_preaffine()[0] # type: ignore
        self._finalxf_f3h_preaffine = self._out_flame_utils__out_finalxf_preaffine()[1] # type: ignore
        self._finalxf_f3h_preaffine_angle = self._out_flame_utils__out_finalxf_preaffine()[2] # type: ignore
        self._finalxf_postaffine = self._out_flame_utils__out_finalxf_postaffine()[0] # type: ignore
        self._finalxf_f3h_postaffine = self._out_flame_utils__out_finalxf_postaffine()[1] # type: ignore
        self._finalxf_f3h_postaffine_angle = self._out_flame_utils__out_finalxf_postaffine()[2] # type: ignore



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
