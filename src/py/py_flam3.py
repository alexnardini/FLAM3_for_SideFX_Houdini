from __future__ import division
from __future__ import annotations
from platform import python_version
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
from re import sub as re_sub
from sys import platform as sys_platform
from subprocess import call as sp_call
from lxml import etree as lxmlET    # This becasue in H19.0.x with Python 3.7.13 will keep the XML keys ordered as I create them.
import xml.etree.ElementTree as ET  # This will do the same but starting from Python 3.8 and up. Preview versions are unordered.
import numpy as np
import platform
import os
import hou
import json
import colorsys
import webbrowser
import inspect



#   Tested on PYTHON v3.7.13(H19) and PYTHON v3.9.10(H19.5)
 
#   Title:      SideFX Houdini FLAM3: 2D
#   Author:     Alessandro Nardini
#   date:       January 2023, Last revised September 2023
#
#   info:       Based on the original: "The Fractal Flame Algorithm"
#   Authors:    Scott Draves, Erik Reckase
#
#   Paper:      https://flam3.com/flame_draves.pdf
#   Date:       September 2003, Last revised November 2008
#
#   Github:     https://github.com/scottdraves/flam3
#   Date:       December 2002, Last revised May 2015
#
#   Name:       PY_FLAM3 "PYTHON"
#
#   Comment:    Python classes and definitions for:
#               - Menus builder
#               - Copy/Paste iterator's data
#               - Load/Save flame files
#               - Load/Save palettes
#               - Tool's user experience
#               
#               Everything is then glued together inside Houdini.



FLAM3HOUDINI_VERSION = "1.0.2"

CHARACTERS_ALLOWED = "_-().:"
CHARACTERS_ALLOWED_OUT_AUTO_ADD_ITER_NUM = "_-+!?().: "

DPT = '*'
PRM = '...'
PRX_FF_PRM = 'ff'
PRX_FF_PRM_POST = 'fp1'
SEC_MAIN = '.main'
SEC_XAOS = '.xaos'
SEC_SHADER = '.shader'
SEC_PREVARS = '.pre_vars'
SEC_VARS = '.vars'
SEC_POSTVARS = '.post_vars'
SEC_PREAFFINE = '.pre_affine'
SEC_POSTAFFINE = '.post_affine'

# Saving flames out will always use the standard PALETTE_COUNT_256
# but saving palette out will downsample if possible to save some data.
PALETTE_COUNT_64 = '64'
PALETTE_COUNT_128 = '128'
PALETTE_COUNT_256 = '256'
PALETTE_FORMAT = 'RGB'

# Parameters at hand
SYS_PT_COUNT = "ptcount"
SYS_PT_COUNT_PRESETS = "ptcount_presets"
SYS_ITERATIONS = "iter"
SYS_DO_FF = 'doff'
SYS_TAG = "tag"
SYS_TAG_SIZE = "tagsize"
SYS_RIP = "rip"
FLAM3_ITERATORS_COUNT = "flamefunc"
IN_ISVALID_FILE = 'isvalidfile'
IN_PATH = 'inpath'
IN_PRESETS = 'inpresets'
SYS_IN_PRESETS = 'sys_inpresets'
IN_COPY_RENDER_PROPERTIES_ON_LOAD = 'propertiescp'
OUT_PATH = 'outpath'
OUT_PRESETS = 'outpresets'
OUT_FLAME_PRESET_NAME = 'outname'
OUT_AUTO_ADD_ITER_NUM = 'autoadditer'
XAOS_MODE = 'xm'
REMAP_PRE_GAUSSIAN_BLUR = 'remappgb'
PALETTE_LIB_PATH = 'palettefile'
PALETTE_OUT_PRESET_NAME = 'palettename'
PALETTE_PRESETS = 'palettepresets'
SYS_PALETTE_PRESETS = 'sys_palettepresets'
OUT_HSV_PALETTE_DO = 'outpalette'
OUT_PALETTE_FILE_EXT = '.json'
USE_FRACTORIUM_COLOR_SPEED = 'fcs'
RAMP_SRC_NAME = 'palette'
RAMP_HSV_NAME = 'palettehsv'
RAMP_SAVE_HSV = 'savehsv'
RAMP_HSV_RESET_ON_LOAD = 'resethsv'
RAMP_HSV_VAL_NAME = 'hsv'
AUTO_PATH_CORRECTION = 'autopath'
# Motion blur
OUT_MB_DO = 'domb'
OUT_MB_FPS = 'fps'
OUT_MB_SAMPLES = 'mbsamples'
OUT_MB_SHUTTER = 'shutter'
# Message parameters
MSG_FLAMESTATS = 'flamestats_msg'
MSG_FLAMERENDER = 'flamerender_msg'
MSG_DESCRIPTIVE_PRM = 'descriptive_msg'
MSG_PALETTE = 'palettemsg'
MSG_OUT = 'outmsg'
MSG_FLAM3ABOUT = 'flam3about_msg'
MSG_FLAM3PLUGINS = 'flam3plugins_msg'

# File lock prefix
FLAM3_LIB_LOCK = 'F3H_LOCK'



class flam3_varsPRM:

    # Collect all variations and their parametric parameters properly ordered as per flame*.h files
    # Those names are what it will appear inside each variation's menu.
    varsPRM = ( ("linear", 0), 
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
                (f"waves{DPT}", 0), 
                ("fisheye", 0), 
                (f"popcorn{DPT}", 0), 
                ("exponential", 0), 
                ("power", 0), 
                ("cosine", 0), 
                (f"rings{DPT}", 0), 
                (f"fan{DPT}", 0), 
                ("bubble", 0), 
                ("cylinder", 0), 
                ("eyefish", 0), 
                ("blur", 0), 
                (f"curl{PRM}", ("curlc_", 1), 1), 
                (f"ngon{PRM}", ("ngon_", 1), 1), 
                (f"pdj{PRM}", ("pdjw_", 1), 1), 
                (f"blob{PRM}", ("blob_", 1), 1), 
                (f"juliaN{PRM}", ("julian_", 1), 1), 
                (f"juliascope{PRM}", ("juliascope_", 1), 1), 
                ("gaussian_blur", 0), 
                (f"fan2{PRM}", ("fan2_", 1), 1), 
                (f"rings2{PRM}", ("rings2val_", 0), 1), 
                (f"rectangles{PRM}", ("rectangles_", 1), 1), 
                (f"radialblur{PRM}", ("radialblur_", 0), 1), 
                (f"pie{PRM}", ("pie_", 1), 1), 
                ("arch", 0), 
                ("tangent", 0), 
                ("square", 0), 
                ("rays", 0), 
                ("blade", 0), 
                ("secant2", 0), 
                ("twintrian", 0), 
                ("cross", 0), 
                (f"disc2{PRM}", ("disc2_", 1), 1), 
                (f"supershape{PRM}", ("supershape_", 1), ("supershapen_", 1), 1), 
                (f"flower{PRM}", ("flower_", 1), 1), 
                (f"conic{PRM}", ("conic_", 1), 1), 
                (f"parabola{PRM}", ("parabola_", 1), 1), 
                (f"bent2{PRM}", ("bent2xy_", 1), 1), 
                (f"bipolar{PRM}", ("bipolarshift_", 0), 1),
                ("boarders", 0),
                ("butterfly", 0), 
                (f"cell{PRM}", ("cellsize_", 0), 1), 
                (f"cpow{PRM}", ("cpow_", 1), 1), 
                ("edisc", 0), 
                ("elliptic", 0), 
                ("noise", 0), 
                (f"escher{PRM}", ("escherbeta_", 0), 1), 
                ("foci", 0), 
                (f"lazysusan{PRM}", ("lazysusanxyz_", 1), ("lazysusan_", 1), 1), 
                ("loonie", 0), 
                ("pre blur", 0), 
                (f"modulus{PRM}", ("modulusXYZ_", 1), 1), 
                (f"oscope{PRM}", ("oscope_", 1), 1), 
                ("polar2", 0), 
                (f"popcorn2{PRM}", ("popcorn2xyz_", 1), ("popcorn2c_", 0), 1), 
                ("scry", 0), 
                (f"separation{PRM}", ("separationxyz_", 1), ("separationinsidexyz_", 1), 1), 
                (f"split{PRM}", ("splitxyz_", 1), 1), 
                (f"splits{PRM}", ("splitsxyz_", 1), 1), 
                (f"stripes{PRM}", ("stripes_", 1), 1), 
                (f"wedge{PRM}", ("wedge_", 1), 1), 
                (f"wedgejulia{PRM}", ("wedgejulia_", 1), 1), 
                (f"wedgesph{PRM}", ("wedgesph_", 1), 1), 
                (f"whorl{PRM}", ("whorl_", 1), 1), 
                (f"waves2{PRM}", ("waves2scalexyz_", 1), ("waves2freqxyz_", 1), 1), 
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
                (f"auger{PRM}", ("auger_", 1), 1), 
                (f"flux{PRM}", ("fluxspread_", 0), 1), 
                (f"mobius{PRM}", ("mobiusre_", 1), ("mobiusim_", 1), 1),
                (f"curve{PRM}", ("curvexyzlenght_", 1), ("curvexyzamp_", 1), 1), 
                (f"perspective{PRM}", ("persp_", 1), 1), 
                (f"bwraps{PRM}", ("bwraps_", 1), ("bwrapstwist_", 1), 1), 
                ("hemisphere", 0), 
                (f"polynomial{PRM}", ("polynomialpow_", 1), ("polynomiallc_", 1), ("polynomialsc_", 1), 1),
                (f"crop{PRM}", ("cropltrb_", 1), ("cropaz_", 1), 1),
                ("unpolar", 0), 
                ("glynnia", 0),
                (f"pt_symmetry{PRM}", ("ptsym_", 1), 1)
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

        vars = self.vars_all()
        vars_no_lin = list(enumerate(vars))[1:]
        vars_no_lin.remove((65, 'pre blur')) # remove "pre blur" as it is hard coded into the chaos game.
        vars_sorted = sorted(vars_no_lin, key=lambda var: var[1])

        return list(enumerate(['linear'])) + vars_sorted

    
    def menu_vars_no_PRM(self) -> list:
        """
        Returns:
            list: [return an enumerated variations menu list with "linear" being the first one for convenience and without parametrics]
        """   
        return list(map(lambda x: x, filter(lambda x: x[1][-3:]!=PRM, self.menu_vars_all())))


class flam3_iterator_prm_names:

    '''
    Mostly, handy to have all those packed into one class
    for easy access everywhere I need and better readability.

    '''
    # ITERATOR
    #
    # Main
    main_note = "note"
    main_prmpastesel = "prmpastesel"
    main_vactive = "vactive"
    main_weight = "iw"
    # Xaos
    xaos = "varnote"
    # Shader
    shader_color = "clr"
    shader_speed = "clrspeed"
    shader_alpha = "alpha"
    # Pre 
    prevar_blur = "preblurtype" # this can be omitted as it is always zero
    prevar_weight_blur = "preblurweight"
    prevar_type_1 = "pre1type"
    prevar_type_2 = "pre2type"    
    prevar_weight_1 = "pre1weight"
    prevar_weight_2 = "pre2weight"
    # Var
    var_type_1 = "v1type"
    var_type_2 = "v2type"
    var_type_3 = "v3type"
    var_type_4 = "v4type"
    var_weight_1 = "v1weight"
    var_weight_2 = "v2weight"
    var_weight_3 = "v3weight"
    var_weight_4 = "v4weight"
    # Post
    postvar_type_1 = "p1type"
    postvar_type_2 = "p2type"
    postvar_weight_1 = "p1weight"
    postvar_weight_2 = "p2weight"
    # Pre affine
    preaffine_x = "x"
    preaffine_y = "y"
    preaffine_o = "o"
    preaffine_ang = "ang"
    # post affine
    postaffine_do = "dopost"
    postaffine_x = "px"
    postaffine_y = "py"
    postaffine_o = "po"
    postaffine_ang = "pang"


class flam3_iterator:

    n = flam3_iterator_prm_names

    # SECTIONS method lists
    #
    # (*T)Types have no signature and always to be used with: pastePRM_T_from_list() for now.
    sec_main = ( (f"{n.main_vactive}_", 0), (f"{n.main_weight}_", 0) )
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


class flam3_varsPRM_FF(flam3_varsPRM):
    """
    Args:
        flam3_varsPRM ([class]): [inherit properties methods from the flam3_varsPRM class]
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


class flam3_iterator_FF:
    """
        Note that every parameters inside the FF have the same name as the iterator parameters 
        plus the string "ff" added at the beginning of their names. parametric variation's parameters have the string  "ff_" instead.
        If you create new parameters inside the FF, or change the parameters names inside the flam3 iterator,
        please be sure to follow the same nameing convetion so to keep the flam3_varsPRM: class as the only source for their names.
    """
    n = flam3_iterator_prm_names

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
    # allT_FF list is omitted here because FF VARS and FF POST VARS have their own unique parametric parameters
    # so I need to handle them one by one inside: def prm_paste_FF() and def prm_paste_sel_FF()
    allMisc_FF = sec_varsW_FF + sec_prevarsW_FF + sec_postvarsW_FF + sec_preAffine_FF + sec_postAffine_FF
        

###############################################################################################
# MENU - Build vars type menus
###############################################################################################
def menu_T(mode: int) -> list:
    """
    Args:
        int_mode (int): [int(0) build menu with all variations. int(1) build menu without parametrics variations.]

    Returns:
        list: [return menu list]
    """
    menu=[]
    if mode:
        # build menu without parametrics
        for i, item in flam3_varsPRM().menu_vars_no_PRM():
            menu.append(i)
            menu.append(item.capitalize())
    else:
        # build menu with parametrics
        for i, item in flam3_varsPRM().menu_vars_all():
            menu.append(i)
            menu.append(item.capitalize())
        
    return menu


###############################################################################################
# MENU - Build iterator copy paste menu
###############################################################################################
MARK_ITER_MSG = "Please mark an iterator first"
MARK_FF_MSG = "Please mark the FF first"
def menu_copypaste(kwargs: dict) -> list:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]

    Returns:
        list: [return menu list]
    """    
    # init menu
    menu=[]

    # Check if we copied an iterator
    try:
        hou.session.flam3node_mp_id # type: ignore
    except:
        hou.session.flam3node_mp_id = -1 # type: ignore

    id_from = hou.session.flam3node_mp_id # type: ignore

    # If an iterator has been copied on a node that has been deleted
    # revert to -1 so that we are forced to copy an iterator again.
    try:
        hou.session.flam3node.type() # type: ignore
    except:
        id_from = -1

    # If we did and the FLAM3 node still exist
    if id_from != -1:

        # current id
        id = kwargs['script_multiparm_index']

        node=kwargs['node']
        flam3node = hou.session.flam3node # type: ignore
        
        if node == flam3node and id==id_from:
            menuitems = ( "Iterator marked. Select a different iterator number or a different FLAM3 node to paste those values", "" )
        elif node == flam3node:
            menuitems = ( "", f"{str(id_from)}", f"{str(id_from)}: xaos:", f"{str(id_from)}: shader", f"{str(id_from)}: pre", f"{str(id_from)}: vars", f"{str(id_from)}: Post", f"{str(id_from)}: pre affine", f"{str(id_from)}: post affine", "" )
        else:
            flam3nodeIter = f"{str(flam3node)}.iter."
            menuitems = ( "", f"{flam3nodeIter}{str(id_from)}", f"{flam3nodeIter}{str(id_from)}: xaos:", f"{flam3nodeIter}{str(id_from)}: shader", f"{flam3nodeIter}{str(id_from)}: pre", f"{flam3nodeIter}{str(id_from)}: vars", f"{flam3nodeIter}{str(id_from)}: Post", f"{flam3nodeIter}{str(id_from)}: pre affine", f"{flam3nodeIter}{str(id_from)}: post affine", "" )
        for i, item in enumerate(menuitems):
            menu.append(i)
            menu.append(item)

        return menu
    else:
        menuitems = ( MARK_ITER_MSG, "" )
        for i, item in enumerate(menuitems):
            menu.append(i-1)
            menu.append(item)

        return menu


###############################################################################################
# MENU - Build FF copy paste menu
###############################################################################################
def menu_copypaste_FF(kwargs: dict) -> list:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]

    Returns:
        list: [return menu list]
    """    
    # init menu
    menu=[]

    # Check if we copied an iterator
    try:
        hou.session.flam3node_FF_check # type: ignore
    except:
        hou.session.flam3node_FF_check = -1 # type: ignore

    flam3node_FF_check = hou.session.flam3node_FF_check # type: ignore

    # If the FF has been copied on a node that has been deleted
    # revert to -1 so that we are forced to copy an FF again.
    try:
        hou.session.flam3node_FF.type() # type: ignore
    except:
        flam3node_FF_check = -1

    # If we did and the FLAM3 node still exist
    if flam3node_FF_check != -1:

        node=kwargs['node']
        flam3node_FF = hou.session.flam3node_FF # type: ignore
        
        if node == flam3node_FF:
            menuitems = ( "FF marked. Select a different FLAM3 node to paste those FF values.", "" )
        else:
            flam3nodeFF = f"{str(flam3node_FF)}.FF"
            menuitems = ( "", f"{flam3nodeFF}: pre", f"{flam3nodeFF}: var", f"{flam3nodeFF}: Post", f"{flam3nodeFF}: pre affine", f"{flam3nodeFF}: post affine", "" )
        for i, item in enumerate(menuitems):
            menu.append(i)
            menu.append(item)

        return menu
    else:
        menuitems = ( MARK_FF_MSG, "" )
        for i, item in enumerate(menuitems):
            menu.append(i-1)
            menu.append(item)

        return menu


###############################################################################################
# MENU - Density presets
###############################################################################################
def menu_density(self: hou.Node) -> list:
    """
    Args:
        int_mode (int): [int(0) build menu with all variations. int(1) build menu without parametrics variations.]

    Returns:
        list: [return menu list]
    """
    
    iterators = self.parm(FLAM3_ITERATORS_COUNT).evalAsInt()
    menu=[]
    menuitems = ()
    if iterators:
        menuitems = ( "", "default", "1M", "2M", "5M", "15M", "25M", "50M", "100M", "150M", "250M", "500M", "750M", "1 Billion", "" )
    else:
        menuitems = ("Please, add at least one iterator", "")
    for i, item in enumerate(menuitems):
        menu.append(i)
        menu.append(item)
    return menu

# Set menu_density() Menu
def menu_density_set(self: hou.Node) -> None:
    
    sel = self.parm(SYS_PT_COUNT_PRESETS).evalAsInt()
    
    if sel == 1:
        self.setParms({SYS_PT_COUNT: 500000}) # type: ignore
    elif sel == 2:
        self.setParms({SYS_PT_COUNT: 1000000}) # type: ignore
    elif sel == 3:
        self.setParms({SYS_PT_COUNT: 2000000}) # type: ignore
    elif sel == 4:
        self.setParms({SYS_PT_COUNT: 5000000}) # type: ignore
    elif sel == 5:
        self.setParms({SYS_PT_COUNT: 15000000}) # type: ignore
    elif sel == 6:
        self.setParms({SYS_PT_COUNT: 25000000}) # type: ignore
    elif sel == 7:
        self.setParms({SYS_PT_COUNT: 50000000}) # type: ignore
    elif sel == 8:
        self.setParms({SYS_PT_COUNT: 100000000}) # type: ignore
    elif sel == 9:
        self.setParms({SYS_PT_COUNT: 150000000}) # type: ignore
    elif sel == 10:
        self.setParms({SYS_PT_COUNT: 250000000}) # type: ignore
    elif sel == 11:
        self.setParms({SYS_PT_COUNT: 500000000}) # type: ignore
    elif sel == 12:
        self.setParms({SYS_PT_COUNT: 750000000}) # type: ignore
    elif sel == 13:
        self.setParms({SYS_PT_COUNT: 1000000000}) # type: ignore

    # reset to null value so we can set the same preset again
    self.setParms({SYS_PT_COUNT_PRESETS: 0}) # type: ignore


###############################################################################################
# FLAM3 paste list of parms
###############################################################################################
def paste_from_list(prm_list: tuple, node: hou.Node, flam3node: hou.Node, id: str, id_from: str) -> None:
    """
    Args:
        prm_list (tuple): [parameters list to query and set]
        node (hou.Node): [current hou.Node to set]
        flam3node (hou.Node): [hou.Node to copy values from]
        id (str): [current multiparamter index]
        id_from (str): [multiparameter index to copy from]
    """    
    for prm in prm_list:
        # if a tuple
        if prm[1]:
            prm_from = flam3node.parmTuple(f"{prm[0]}{id_from}")
            prm_to = node.parmTuple(f"{prm[0]}{id}")
            prm_idx = 0
            for p in prm_from:
                if len(p.keyframes()):
                    for k in p.keyframes():
                        prm_to[prm_idx].setKeyframe(k)
                else:
                    prm_to[prm_idx].set(p.eval())
                prm_idx += 1
        else:
            prm_from = flam3node.parm(f"{prm[0]}{id_from}")
            prm_to = node.parm(f"{prm[0]}{id}")
            if len(prm_from.keyframes()):
                    for k in prm_from.keyframes():
                        prm_to.setKeyframe(k)
            else:
                prm_to.set(prm_from.eval())


###############################################################################################
# FLAM3 (*T)Types-> paste parametric parms if any are found in the list of var types passed in
###############################################################################################
def pastePRM_T_from_list(prmT_list: tuple, varsPRM: tuple, node: hou.Node, flam3node: hou.Node, id: str, id_from: str) -> None:
    """
    Args:
        prmT_list (tuple): [variations list - types]
        varsPRM (tuple): [variation's parmaters list]
        node (hou.Node): [current hou.Node to set]
        flam3node (hou.Node): [hou.Node to copy values from]
        id (str): [current multiparamter index]
        id_from (str): [multiparameter index to copy from]
    """    
    for prm in prmT_list:

        prm_from = flam3node.parm(f"{prm}{id_from}").eval()
        node.setParms({f"{prm}{id}": prm_from}) # type: ignore
        # Check if this var is a parametric or not
        v_type = int(prm_from)
        if(varsPRM[v_type][-1]):
            
            paste_from_list(varsPRM[v_type][1:-1], node, flam3node, id, id_from)


###############################################################################################
# simple save existing note and add the iterator copy string info to it
###############################################################################################
def paste_save_note(_note: str) -> str:
    """
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


###############################################################################################
# FLAM3 paste note msg
# int_mode:
# 0 -> iterators
# 1 -> FF all
# 2 -> FF sections
###############################################################################################
def paste_set_note(int_mode: int, str_section: str, node: hou.Node, flam3node: hou.Node, id: str, id_from: str) -> None:
    """
    Args:
        int_mode (int): [int(0) copy/paste iterator into the same node. int(1) copy/paste FF between different nodes. int(2) copy/paste FF sections between different nodes]
        str_section (str): [section name string to be copied, this is only for msg print info]
        node (hou.Node): [current hou.Node to set]
        flam3node (hou.Node): [[hou.Node to copy values from]
        id (str): [current multiparamter index]
        id_from (str): [multiparameter index to copy from]
    """ 
    
    n = flam3_iterator_prm_names
    _current_note_FF = node.parm("ffnote").evalAsString()

    if int_mode == 0:
        _current_note = node.parm(f"note_{id}").evalAsString()
        # If on the same FLAM3 node
        if node == flam3node:
            if len(_current_note) == 0:
                node.setParms({f"{n.main_note}_{id}": f"iter.{id_from}{str_section}"}) # type: ignore
            else:
                node.setParms({f"{n.main_note}_{id}": f"{paste_save_note(_current_note)}iter.{id_from}{str_section}"}) # type: ignore
        else:
            if len(_current_note) == 0:
                node.setParms({f"{n.main_note}_{id}": f"{str(flam3node)}.iter.{id_from}{str_section}"}) # type: ignore
            else:
                node.setParms({f"{n.main_note}_{id}": f"{paste_save_note(_current_note)}{str(flam3node)}.iter.{id_from}{str_section}"}) # type: ignore
            print(f"{str(node)}: Copied values from: {str(flam3node)}.iter.{id_from}{str_section} to: {str(node)}.iter.{id}{str_section}")
    elif int_mode == 1:
        if node != flam3node:
            if len(_current_note_FF) == 0:
                node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{str(flam3node)}.FF"}) # type: ignore
            else:
                node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{paste_save_note(_current_note_FF)}{str(flam3node)}.FF"}) # type: ignore
            print(f"{str(node)}: Copied FF from: {str(flam3node)}.FF to: {str(node)}.FF")
    elif int_mode == 2:
        if node != flam3node:
            if len(_current_note_FF) == 0:
                node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{str(flam3node)}.FF{str_section}"}) # type: ignore
            else:
                node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{paste_save_note(_current_note_FF)}{str(flam3node)}.FF{str_section}"}) # type: ignore
            print(f"{str(node)}: Copied FF from: {str(flam3node)}.FF{str_section} to: {str(node)}.FF{str_section}")


###############################################################################################
# Copy paste all iterator's values from one to another and also from different FLAM3 HDA nodes
###############################################################################################
def prm_paste(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """    
    if kwargs["ctrl"]:

        # current node
        node=kwargs['node']
        
        # current iterator
        id = kwargs['script_multiparm_index']

        # FLAM3 node and Iterator we just copied
        flam3node = hou.session.flam3node # type: ignore
        id_from = hou.session.flam3node_mp_id # type: ignore

        # If an iterator was copied on a node that has been deleted
        # revert to -1 so that we are forced to copy an iterator again.
        try:
            flam3node.type()
        except:
            id_from = -1

        # If we ever copied an iterator from a currently existing FLAM3 node
        if id_from != -1:
            if node==flam3node and id==id_from:
                print(f"{str(node)}: Iterator marked. Select a different iterator number to paste those values.")
            else:
                pastePRM_T_from_list(flam3_iterator.allT, flam3_varsPRM.varsPRM, node, flam3node, str(id), str(id_from))
                paste_from_list(flam3_iterator.allMisc, node, flam3node, str(id), str(id_from))
                paste_set_note(0, "", node, flam3node, str(id), str(id_from))

        else:
            print(f"{str(node)}: {MARK_ITER_MSG}.")

    elif kwargs["shift"]:
        del hou.session.flam3node_mp_id # type: ignore
        del hou.session.flam3node # type: ignore

    else:
        hou.session.flam3node_mp_id = kwargs['script_multiparm_index'] # type: ignore
        hou.session.flam3node = kwargs['node'] # type: ignore
        print(f"{str(kwargs['node'])}: Copied iterator: {str(hou.session.flam3node)}->iter.{str(hou.session.flam3node_mp_id)}") # type: ignore


###############################################################################################
# FF - Copy paste all FF's values from one FLAM3 node to another FLAM3 node
###############################################################################################
def prm_paste_FF(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """    
    if kwargs["ctrl"]:

        # current node
        node=kwargs['node']

        # FLAM3 node and its state we just copied
        flam3node_FF = hou.session.flam3node_FF # type: ignore
        flam3node_FF_check = hou.session.flam3node_FF_check # type: ignore

        # If the FF was copied from a node that has been deleted
        # revert to -1 so that we are forced to copy an iterator again.
        try:
            flam3node_FF.type()
        except:
            flam3node_FF_check = -1

        # If we ever copied an FF from a currently existing FLAM3 node
        if flam3node_FF_check != -1:
            if node==flam3node_FF:
                print(f"{str(node)}: FF marked. Select a different FLAM3 node to paste those FF values.")
            else:
                pastePRM_T_from_list(flam3_iterator_FF.sec_prevarsT_FF, flam3_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), node, flam3node_FF, "", "")
                pastePRM_T_from_list(flam3_iterator_FF.sec_varsT_FF, flam3_varsPRM_FF(PRX_FF_PRM).varsPRM_FF(), node, flam3node_FF, "", "")
                pastePRM_T_from_list(flam3_iterator_FF.sec_postvarsT_FF, flam3_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), node, flam3node_FF, "", "")
                paste_from_list(flam3_iterator_FF.allMisc_FF, node, flam3node_FF, "", "")
                paste_set_note(1, "", node, flam3node_FF, "", "")

        else:
            print(f"{str(node)}: {MARK_FF_MSG}.")

    elif kwargs["shift"]:
        del hou.session.flam3node_FF_check # type: ignore
        del hou.session.flam3node_FF # type: ignore

    else:
        hou.session.flam3node_FF_check = 1 # type: ignore
        hou.session.flam3node_FF = kwargs['node'] # type: ignore
        print(f"{str(kwargs['node'])}: Copied FF: {str(hou.session.flam3node_FF)}->FF") # type: ignore


###############################################################################################
# paste sections of iterator's values from one to another and also from different FLAM3 nodes
###############################################################################################
def prm_paste_sel(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """    
    # current node
    node=kwargs['node']
    
    # current iterator
    id = kwargs['script_multiparm_index']

    # FLAM3 node and Iterator we just copied
    flam3node = hou.session.flam3node # type: ignore
    id_from = hou.session.flam3node_mp_id # type: ignore

    # WE DO THE FOLLOWING IN THE SCRIPTED MENU LIST -> FLAM3node.prmpastesel_# parameter
    #
    # If an iterator was copied from a node that has been deleted
    # revert to -1 so that we are forced to copy an iterator again.
    '''
    try:
        flam3node.type()
    except:
        id_from = -1
    '''

    # If we ever copied an iterator from a currently existing FLAM3 node
    if id_from != -1:

        n = flam3_iterator_prm_names
        
        # Get user selection of paste methods
        paste_sel = node.parm(f"{n.main_prmpastesel}_{str(id)}").evalAsInt()

        # set MAIN
        if paste_sel == 1:
            paste_from_list(flam3_iterator.sec_main, node, flam3node, str(id), str(id_from))
            paste_set_note(0, SEC_MAIN, node, flam3node, str(id), str(id_from))
        # set XML_XF_XAOS
        elif paste_sel == 2:
            paste_from_list(flam3_iterator.sec_xaos, node, flam3node, str(id), str(id_from))
            paste_set_note(0, SEC_XAOS, node, flam3node, str(id), str(id_from))
        # set SHADER 
        elif paste_sel == 3:
            paste_from_list(flam3_iterator.sec_shader, node, flam3node, str(id), str(id_from))
            paste_set_note(0, SEC_SHADER, node, flam3node, str(id), str(id_from))
        # set PRE VARS
        elif paste_sel == 4:
            pastePRM_T_from_list(flam3_iterator.sec_prevarsT, flam3_varsPRM.varsPRM, node, flam3node, str(id), str(id_from))
            paste_from_list(flam3_iterator.sec_prevarsW, node, flam3node, str(id), str(id_from))
            paste_set_note(0, SEC_PREVARS, node, flam3node, str(id), str(id_from))
        # set VARS
        elif paste_sel == 5:
            pastePRM_T_from_list(flam3_iterator.sec_varsT, flam3_varsPRM.varsPRM, node, flam3node, str(id), str(id_from))
            paste_from_list(flam3_iterator.sec_varsW, node, flam3node, str(id), str(id_from))
            paste_set_note(0, SEC_VARS, node, flam3node, str(id), str(id_from))
        # set POST VARS
        elif paste_sel == 6:
            pastePRM_T_from_list(flam3_iterator.sec_postvarsT, flam3_varsPRM.varsPRM, node, flam3node, str(id), str(id_from))
            paste_from_list(flam3_iterator.sec_postvarsW, node, flam3node, str(id), str(id_from))
            paste_set_note(0, SEC_POSTVARS, node, flam3node, str(id), str(id_from))
        # set PRE AFFINE
        elif paste_sel == 7:
            paste_from_list(flam3_iterator.sec_preAffine, node, flam3node, str(id), str(id_from))
            paste_set_note(0, SEC_PREAFFINE, node, flam3node, str(id), str(id_from))
        # set POST AFFINE
        elif paste_sel == 8:
            paste_from_list(flam3_iterator.sec_postAffine, node, flam3node, str(id), str(id_from))
            paste_set_note(0, SEC_POSTAFFINE, node, flam3node, str(id), str(id_from))
     
        # Set it to a null value ( first in the menu array idx in this case )
        # so that we can paste the same section again, if we want to.
        #
        # please check the def->menu_copypaste() to know its size.
        node.setParms({f"{n.main_prmpastesel}_{str(id)}": str(0)})
        node.parm(f"{n.main_prmpastesel}_{str(id)}").eval()
        
    else:
        print(f"{str(node)}: {MARK_ITER_MSG}")


###############################################################################################
# FF paste sections of FF's values from one FLAM3 node to another FLAM3 node
###############################################################################################
def prm_paste_sel_FF(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """    
    # current node
    node=kwargs['node']

    # FLAM3 node and its state we just copied
    flam3node_FF = hou.session.flam3node_FF # type: ignore
    flam3node_FF_check = hou.session.flam3node_FF_check # type: ignore

    # WE DO THE FOLLOWING IN THE SCRIPTED MENU LIST -> FLAM3node.ffprmpastesel parameter
    #
    # If the FF was copied from a node that has been deleted
    # revert to -1 so that we are forced to copy an iterator again.
    '''
    try:
        flam3node_FF.type()
    except:
        flam3node_FF_check = -1
    '''

    # If we ever copied an FF from a currently existing FLAM3 node
    if flam3node_FF_check != -1:

        n = flam3_iterator_prm_names
        
        # Get user selection of paste methods
        ff_paste_sel = node.parm(f"{PRX_FF_PRM}{n.main_prmpastesel}").evalAsInt()
        
        # set FF PRE VARS
        if ff_paste_sel == 1:
            pastePRM_T_from_list(flam3_iterator_FF.sec_prevarsT_FF, flam3_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), node, flam3node_FF, "", "")
            paste_from_list(flam3_iterator_FF.sec_prevarsW_FF, node, flam3node_FF, "", "")
            paste_set_note(2, SEC_PREVARS, node, flam3node_FF, "", "")
        # set FF VARS
        elif ff_paste_sel == 2:
            pastePRM_T_from_list(flam3_iterator_FF.sec_varsT_FF, flam3_varsPRM_FF(PRX_FF_PRM).varsPRM_FF(), node, flam3node_FF, "", "")
            paste_from_list(flam3_iterator_FF.sec_varsW_FF, node, flam3node_FF, "", "")
            paste_set_note(2, SEC_VARS, node, flam3node_FF, "", "")
        # set FF POST VARS
        elif ff_paste_sel == 3:
            pastePRM_T_from_list(flam3_iterator_FF.sec_postvarsT_FF, flam3_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), node, flam3node_FF, "", "")
            paste_from_list(flam3_iterator_FF.sec_postvarsW_FF, node, flam3node_FF, "", "")
            paste_set_note(2, SEC_POSTVARS, node, flam3node_FF, "", "")
        # set FF PRE AFFINE
        elif ff_paste_sel == 4:
            paste_from_list(flam3_iterator_FF.sec_preAffine_FF, node, flam3node_FF, "", "")
            paste_set_note(2, SEC_PREAFFINE, node, flam3node_FF, "", "")
        # set FF POST AFFINE
        elif ff_paste_sel == 5:
            paste_from_list(flam3_iterator_FF.sec_postAffine_FF, node, flam3node_FF, "", "")
            paste_set_note(2, SEC_POSTAFFINE, node, flam3node_FF, "", "")

        # Set it to a null value ( first in the menu array idx in this case )
        # so that we can paste the same section again, if we want to.
        #
        # please check def->menu_copypaste_FF() to know its size.
        node.setParms({f"{PRX_FF_PRM}{n.main_prmpastesel}": str(0)})
        node.parm(f"{PRX_FF_PRM}{n.main_prmpastesel}").eval()
                
    else:
        print(f"{str(node)}: {MARK_FF_MSG}.")


###############################################################################################
# FLAM3 on create init
###############################################################################################
def flam3_on_create(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """
    
    # Set initial node color
    node = kwargs['node']
    node.setColor(hou.Color((0.825,0.825,0.825)))
    
    # Set about tab infos
    flam3_about_msg(node)
    flam3_about_plugins_msg(node)
    # Clear up stats if there already ( due to be stored into a houdini preset also, just in case... )
    node.setParms({MSG_FLAMESTATS: ""})
    node.setParms({MSG_FLAMERENDER: ""})
    node.setParms({MSG_PALETTE: ''})
    node.setParms({MSG_OUT: ''})
    
    # FLAM3 node and MultiParameter id for iterators
    #
    # If there were already a FLAM3 node in the scene
    # and we copied already an iterator's values, lets keep whats stored,
    # otherwise initialize those values.
    try:
        hou.session.flam3node # type: ignore
    except:
        hou.session.flam3node = node # type: ignore
    try:
        hou.session.flam3node_mp_id # type: ignore
    except:
        hou.session.flam3node_mp_id = -1 # type: ignore

    # If an iterator was copied from a node that has been deleted
    # revert to -1 so that we are forced to copy an iterator again.
    try:
        hou.session.flam3node.type() # type: ignore
    except:
        hou.session.flam3node_mp_id = -1 # type: ignore

    # FLAM3 node for FF.
    #
    # If there were already a FLAM3 node in the scene
    # and we copied already FF's values, lets keep whats stored,
    # otherwise initialize those values.
    try:
        hou.session.flam3node_FF # type: ignore
    except:
        hou.session.flam3node_FF = node # type: ignore
    try:
        hou.session.flam3node_FF_check # type: ignore
    except:
        hou.session.flam3node_FF_check = -1 # type: ignore

    # If the FF was copied from a node that has been deleted
    # revert to -1 so that we are forced to copy the FF again.
    try:
        hou.session.flam3node_FF.type() # type: ignore
    except:
        hou.session.flam3node_FF_check = -1 # type: ignore

    # Initialize flam3 viewport Color Scheme
    try:
        hou.session.flam3_CS # type: ignore
    except:
        hou.session.flam3_CS = [] # type: ignore



###############################################################################################
# FLAM3 on Loaded init
###############################################################################################
def flam3_on_loaded(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """
    # Check for left over JSON, IN and OUT file paths no longer valid and init_presets accordingly
    
    #  mode (int): ZERO: To be used to prevent to load a preset when loading back a hip file.
    init_presets(kwargs, PALETTE_PRESETS, 0)
    #  mode (int): ZERO: To be used to prevent to load a preset when loading back a hip file.
    init_presets(kwargs, IN_PRESETS, 0)
    init_presets(kwargs, OUT_PRESETS)

    node = kwargs['node']
    # update about tab just in case
    flam3_about_msg(node)
    flam3_about_plugins_msg(node)
    # The following is a workaround to keep the correct preset inside the IN Tab when the hip file was saved
    # as it always get reset to ZERO on load for some reason. The preset inside the SYS Tab is correct after load.
    # Need to investigate why. the SYS_IN_PRESETS menu parameter is set inside the apo_to_flam3()
    node.setParms({IN_PRESETS: node.parm(SYS_IN_PRESETS).eval()}) # type: ignore
    # Same goes for the palette preset entrie, and some time goes also out of range
    # so we store the selection first inside a mem menu parameter first inside json_to_ramp()
    # and call it back here.
    node.setParms({PALETTE_PRESETS: node.parm(SYS_PALETTE_PRESETS).eval()}) # type: ignore



###############################################################################################
# Init parameter presets menu list as soon as you load a valid json/flame file
###############################################################################################
def init_presets(kwargs: dict, prm_presets_name: str, mode=1) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
        mode (int): To be used to prevent to load a left over preset when loading back a hip file.
    """    
    node = kwargs['node']
    prm = node.parm(prm_presets_name)
    prm.set('-1')
    
    if IN_PRESETS in prm_presets_name:
        xml = node.parm(IN_PATH).evalAsString()
        if os.path.isfile(xml) is True:
            apo = apo_flame(node, xml)
            if not apo.isvalidtree:
                prm.set('-1')
                node.setParms({MSG_FLAMESTATS: "Please load a valid *.flame file."})
                node.setParms({MSG_FLAMERENDER: ""})
                node.setParms({MSG_DESCRIPTIVE_PRM: ""})
            else:
                # Only set when NOT on an: onLoaded python script
                if mode:
                    prm.set('0')
                    node.setParms({IN_ISVALID_FILE: 1})
                    apo_to_flam3(node)
        else:
            prm.set('-1')
            node.setParms({IN_ISVALID_FILE: 0})
            node.setParms({MSG_FLAMESTATS: ""})
            node.setParms({MSG_FLAMERENDER: ""})
            node.setParms({MSG_DESCRIPTIVE_PRM: ""})
            # We do not want to print if the file path parameter is empty
            if xml:
                print(f'{str(node)}.IN: please select a valid file location.')
                
    elif OUT_PRESETS in prm_presets_name:
        xml = node.parm(OUT_PATH).evalAsString()
        xml_checked = out_check_outpath(node, xml, OUT_FLAM3_FILE_EXT, 'Flame')
        if xml_checked is not False:
            node.setParms({OUT_PATH: xml_checked}) 
            apo = apo_flame(node, xml_checked) #type: ignore
            if apo.isvalidtree:
                prm.set(f'{len(apo.name)-1}')
                # check if the selected Flame file is locked
                if isLock(xml_checked, FLAM3_LIB_LOCK):
                    flame_lib_locked = f"\nflame lib file: LOCKED"
                    node.setParms({MSG_OUT: flame_lib_locked})
                else:
                    node.setParms({MSG_OUT: ''})
            else:
                prm.set('-1')
                node.setParms({MSG_OUT: ''})
        else:
            # We do not want to print if the file path parameter is empty
            if xml:
                print(f'{str(node)}.OUT: please select a valid file location.')
                
    elif PALETTE_PRESETS in prm_presets_name:
        json_path = node.parm(PALETTE_LIB_PATH).evalAsString()
        json_path_checked = out_check_outpath(node,  json_path, OUT_PALETTE_FILE_EXT, 'Palette')
        if json_path_checked is not False:
            node.setParms({PALETTE_LIB_PATH: json_path_checked})
            if isJSON(node, json_path, PALETTE_LIB_PATH):
                # Only set when NOT on an: onLoaded python script
                if mode:
                    prm.set('0')
                    # check if the selected palette file is locked
                    if isLock(json_path_checked, FLAM3_LIB_LOCK):
                        palette_lib_locked = f"\npalette lib file: LOCKED"
                        node.setParms({MSG_PALETTE: palette_lib_locked})
                    else:
                        node.setParms({MSG_PALETTE: ''})
                        
            else:
                prm.set('-1')
                node.setParms({MSG_PALETTE: ''})
        else:
            # We do not want to print if the file path parameter is empty
            if json_path:
                print(f'{str(node)}.palette: please select a valid file location.')
            node.setParms({MSG_PALETTE: ''})
        

###############################################################################################
# OPEN FILE EXPLORER - Open a file explorer to the file location
###############################################################################################
def open_explorer_file(filename):
    path = os.path.dirname(filename)
    if os.path.isdir(path):
        if sys_platform == "win32":
            os.startfile(path)
        else:
            opener ="open" if sys_platform == "darwin" else "xdg-open"
            sp_call([opener, path])
    else:
        pass
        
###############################################################################################
# MENU - Palette presets
###############################################################################################
def menu_ramp_presets(kwargs: dict) -> list:

    node = kwargs['node']
    filepath = node.parm(PALETTE_LIB_PATH).evalAsString()

    menu=[]
    
    if isJSON(node, filepath, PALETTE_LIB_PATH):
        if node.parm(FLAM3_ITERATORS_COUNT).evalAsInt():
            with open(filepath) as f:
                data = json.load(f)
            menuitems = data.keys()
            for i, item in enumerate(menuitems):
                menu.append(i)
                menu.append(item)
        else:
            menuitems = ("Please, add at least one iterator", "")
            for i, item in enumerate(menuitems):
                menu.append(i)
                menu.append(item)
    else:
        if node.parm(FLAM3_ITERATORS_COUNT).evalAsInt():
            menu.append(-1)
            menu.append('Empty')
        else:
            menuitems = ("Please, add at least one iterator", "")
            for i, item in enumerate(menuitems):
                menu.append(i)
                menu.append(item)
    return menu


###############################################################################################
# Save current ramp to a json file
###############################################################################################
def get_ramp_keys_count(ramp: hou.Ramp) -> str:
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
        print(f'{str(hou.pwd())}: Colors: {str(keys_count)}: to many colors and will default back to the standard 256 color keys for this palette.')
        return PALETTE_COUNT_256


def isJSON(node: hou.Node, filepath: Union[str, bool], prm: str) -> bool:
    if filepath is not False:
        try:
            with open(str(filepath),'r') as r:
                data_check = json.load(r)
                node.setParms({prm: str(filepath)}) #type: ignore
                del data_check
                return True
        except:
            return False
    else:
        return False
    
def isLock(filepath: Union[str, bool], prefix: str) -> bool:
    if filepath is not False:
        if os.path.split(str(filepath))[-1].startswith(prefix):
            return True
        else:
            return False
    else:
        return False

def clamp(x): 
  return max(0, min(x, 255))
def rgb_to_hex(rgb: tuple) -> str:
    vals = [clamp(255*x) for x in rgb]
    hex = ''.join(['{:02X}'.format(int(round(x))) for x in vals])
    return hex
def ramp_save(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """
    node = kwargs['node']
    palettepath = node.parm(PALETTE_LIB_PATH).evalAsString()
    out_path_checked = out_check_outpath(node, palettepath, OUT_PALETTE_FILE_EXT, 'Palette')

    if out_path_checked is not False:
        
        if kwargs['shift']:
            open_explorer_file(out_path_checked)
        else:
                
            if isLock(out_path_checked, FLAM3_LIB_LOCK):
                ui_text = f"This Palette library is Locked."
                ALL_msg = f"This Palette library is Locked and you can not modify this file.\n\nTo Lock a Palete lib file just rename it using:\n\"{FLAM3_LIB_LOCK}\" as the start of the filename.\n\nOnce you are happy with a palette library you built, you can rename the file to start with: \"{FLAM3_LIB_LOCK}\"\nto prevent any further modifications to it. For example if you have a lib file call: \"my_rainbows_colors.json\"\nyou can rename it to: \"{FLAM3_LIB_LOCK}_my_rainbows_colors.json\" to keep it safe."
                hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3 Palette Lock", details=ALL_msg, details_label=None, details_expanded=False) # type: ignore
            else:
                # get user's preset name or build an automated one
                name = node.parm(PALETTE_OUT_PRESET_NAME).eval()
                if not name:
                    now = datetime.now()
                    presetname = now.strftime("Palette_%b-%d-%Y_%H%M%S")
                else:
                    # otherwise get that name and use it
                    presetname = name

                # Updated HSV ramp before getting it
                palette_hsv(node)
                palette_cp(node)

                ramp = hou.Ramp()
                
                if node.parm(RAMP_SAVE_HSV).eval():
                    ramp = node.parm(RAMP_HSV_NAME).evalAsRamp()
                else:
                    ramp = node.parm(RAMP_SRC_NAME).evalAsRamp()
                    
                keys_count = get_ramp_keys_count(ramp)
                
                POSs = list(iter_islice(iter_count(0, 1.0/(int(keys_count)-1)), int(keys_count)))
                HEXs = []
                json_data = ''
                for p in POSs:
                    clr = tuple(ramp.lookup(p))
                    HEXs.append(rgb_to_hex(clr))
                dict = { presetname: {'hex': ''.join(HEXs)} }
                json_data = json.dumps(dict, indent=4)

                if kwargs["ctrl"]:
                    os.remove(str(out_path_checked))
                    with open(str(out_path_checked),'w') as w:
                        w.write(json_data)
                else:
                    # if the file exist and is a valid JSON file
                    if isJSON(node, out_path_checked, PALETTE_LIB_PATH):
                        with open(str(out_path_checked),'r') as r:
                            prevdata = json.load(r)
                        with open(str(out_path_checked), 'w') as w:
                            newdata = dict
                            prevdata.update(newdata)
                            data = json.dumps(prevdata,indent = 4)
                            w.write(data)
                    # Otherwise mean it is either empty or not exist,
                    # just create one with the current ramp in it
                    #
                    # Note that we already checked for a proper file extension with:
                    # def out_check_outpath(...)
                    # so to not override something else by accident
                    else:
                        with open(str(out_path_checked),'w') as w:
                            w.write(json_data)

                # Set some parameters
                with open(out_path_checked) as f:
                    data = json.load(f)
                    node.setParms({PALETTE_PRESETS: str(len(data.keys())-1) })
                    node.setParms({PALETTE_OUT_PRESET_NAME: ''})
                    del data
                    
                # Set the file path to the corrected one
                node.setParms({PALETTE_LIB_PATH: str(out_path_checked)})


###############################################################################################
# Set ramp value from a json file
###############################################################################################
def hex_to_rgb(hex: str): 
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def sys_json_to_ramp(kwargs: dict) -> None:
    node = kwargs['node']
    preset_id = node.parm(SYS_PALETTE_PRESETS).eval()
    node.setParms({PALETTE_PRESETS: preset_id}) # type: ignore
    json_to_ramp(kwargs)
    
def json_to_ramp(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """    
    node = kwargs['node']
    
    #get ramp parm
    ramp_parm = node.parm(RAMP_SRC_NAME)
    ramp_parm.deleteAllKeyframes()
    
    filepath = node.parm(PALETTE_LIB_PATH).evalAsString()
    # get current preset
    preset_id = int(node.parm(PALETTE_PRESETS).eval())
    preset = node.parm(PALETTE_PRESETS).menuLabels()[preset_id]
    
    if os.path.isfile(filepath) and os.path.getsize(filepath)>0:
        HEXs = []
        with open(filepath) as f:
            data = json.load(f)[preset]
            hex_values = data['hex']
            [HEXs.append(hex) for hex in wrap(hex_values, 6)]

        rgb_from_XML_PALETTE = []
        for hex in HEXs:
            x = hex_to_rgb(hex)
            rgb_from_XML_PALETTE.append((abs(x[0])/(255 + 0.0), abs(x[1])/(255 + 0.0), abs(x[2])/(255 + 0.0)))
        
        # Initialize new ramp.
        POSs = list(iter_islice(iter_count(0, 1.0/(len(rgb_from_XML_PALETTE)-1)), len(rgb_from_XML_PALETTE)))
        BASEs = [hou.rampBasis.Linear] * len(rgb_from_XML_PALETTE) # type: ignore
        ramp = hou.Ramp(BASEs, POSs, rgb_from_XML_PALETTE)
        ramp_parm.set(ramp)

        # reset HSV after load ?
        if node.parm(RAMP_HSV_RESET_ON_LOAD).eval():
            node.setParms({RAMP_HSV_VAL_NAME: hou.Vector3((1, 1, 1))})
        palette_cp(node)
        palette_hsv(node)
        
        # Store selection into mem preset menu
        node.setParms({SYS_PALETTE_PRESETS: node.parm(PALETTE_PRESETS).eval()}) # type: ignore
        

###############################################################################################
# palette copy values to paletteHSV
###############################################################################################
def palette_cp(self: hou.Node) -> None:
    """
    Args:
        self (hou.Node): [current hou.Node]
    """    
    rmphsv = self.parm(RAMP_HSV_NAME)
    rmpsrc = self.parm(RAMP_SRC_NAME)
    rmphsv.set(hou.Ramp(rmpsrc.evalAsRamp().basis(), rmpsrc.evalAsRamp().keys(), rmpsrc.evalAsRamp().values()))
    # Apply HSV if any is currently set
    palette_hsv(self)
    

###############################################################################################
# palette apply HSV values
###############################################################################################
def palette_hsv(self: hou.Node) -> None:
    """
    Args:
        self (hou.Node): [current hou.Node]
    """    
    rmphsv = self.parm(RAMP_HSV_NAME)
    rmpsrc = self.parm(RAMP_SRC_NAME)
    hsvprm = self.parmTuple(RAMP_HSV_VAL_NAME)
    hsv = list(map(lambda x: colorsys.rgb_to_hsv(x[0], x[1], x[2]), rmpsrc.evalAsRamp().values()))
    
    rgb = []
    for item in hsv:
        h = item[0] + hsvprm[0].eval()
        s = item[1] * hsvprm[1].eval()
        v = item[2] * hsvprm[2].eval()
        rgb.append(colorsys.hsv_to_rgb(h, s, v))
    
    rmphsv.set(hou.Ramp(rmpsrc.evalAsRamp().basis(), rmpsrc.evalAsRamp().keys(), rgb))


###############################################################################################
# palette lock ( Lock the color corrected palette from user input )
###############################################################################################
def palette_lock(self: hou.Node) -> None:
    """
    Args:
        self (hou.Node): [current hou.Node]
    """    
    palette_cp(self)
    palette_hsv(self)


###############################################################################################
# Get scene viewers
###############################################################################################
def getSceneViewers() -> list:
    """
    Returns:
        list: [return a list of open scene viewers]
    """    
    views = hou.ui.paneTabs() # type: ignore
    viewers = []
    for v in views:
        if isinstance(v, hou.SceneViewer):
            viewers.append(v)
    return viewers


###############################################################################################
# Color scheme dark ( and remember the current color scheme if not dark )
###############################################################################################
def colorSchemeDark(self: hou.Node) -> None:

    try:
        module_test = hou.session.flam3_CS # type: ignore
    except:
        hou.session.flam3_CS = [] # type: ignore

    count = 0
    viewers_col = []

    setprm = self.parm("setdark").eval()
    Light = hou.viewportColorScheme.Light # type: ignore
    Grey  = hou.viewportColorScheme.Grey # type: ignore
    Dark  = hou.viewportColorScheme.Dark # type: ignore

    for view in getSceneViewers():

        settings = view.curViewport().settings()
        col = settings.colorScheme()
        viewers_col.append(col)
        try:
            idx_test = hou.session.flam3_CS[count] # type: ignore
        except:
            if len(hou.session.flam3_CS) > 0: # type: ignore
                hou.session.flam3_CS.append(viewers_col) # type: ignore
            else:
                hou.session.flam3_CS = [] # type: ignore
                hou.session.flam3_CS.append(viewers_col) # type: ignore

        if setprm:
            if len(hou.session.flam3_CS) == 0: # type: ignore
                if col == Light or col == Grey:
                    settings.setColorScheme(Dark)
            else:
                if col == Light or col == Grey:
                    settings.setColorScheme(Dark)
                elif col == Dark and hou.session.flam3_CS[count] != Dark: # type: ignore
                    if hou.session.flam3_CS[count] == Light: # type: ignore
                        settings.setColorScheme(Light)
                    elif hou.session.flam3_CS[count] == Grey: # type: ignore
                        settings.setColorScheme(Grey)

        else:
            if col == Dark and hou.session.flam3_CS[count] != Dark: # type: ignore
                if hou.session.flam3_CS[count] == Light: # type: ignore
                    settings.setColorScheme(Light)
                elif hou.session.flam3_CS[count] == Grey: # type: ignore
                    settings.setColorScheme(Grey)
        count += 1
    
    # Update history
    hou.session.flam3_CS = [] # type: ignore
    hou.session.flam3_CS = viewers_col # type: ignore


###############################################################################################
# set viewport particle display. ( Points or Pixels )
###############################################################################################
def viewportParticleDisplay(self: hou.Node) -> None:

    pttype = self.parm("vptype").evalAsInt()

    Points = hou.viewportParticleDisplay.Points # type: ignore
    Pixels = hou.viewportParticleDisplay.Pixels # type: ignore

    for view in getSceneViewers():
        settings = view.curViewport().settings()
        if pttype == 0:
            settings.particleDisplayType(Points)
        elif pttype == 1:
            settings.particleDisplayType(Pixels)


###############################################################################################
# set viewport particle size. ( Points or Pixels )
###############################################################################################
def viewportParticleSize(self: hou.Node) -> None:

    Points = hou.viewportParticleDisplay.Points # type: ignore
    ptsize = self.parm("vpptsize").evalAsFloat()

    for view in getSceneViewers():
        settings = view.curViewport().settings()
        settings.particleDisplayType(Points)
        settings.particlePointSize(ptsize)



###############################################################################################
# Convert and set "xaos:"" command strings between modes from the preferences xaos mode menu
###############################################################################################
def flam3_xaos_convert(self) -> None:
    """Here I am using a class function call from: out_flam3_data class.out_xf_xaos_from()
       down below inside the save XML/FLAME file section of this file.
       The class function: out_flam3_data class.out_xf_xaos_from() convert xaos from TO to FROM and back in one call.
    """    
    f3d = out_flam3_data(self)
    xaos_new = f3d.out_xf_xaos_from(0)
    for iter in range(f3d.iter_count):
        if xaos_new[iter]:
            xs = "xaos:" + ":".join(xaos_new[iter].split(" "))
            self.setParms({f"{flam3_iterator_prm_names.xaos}_{str(iter+1)}": xs})
        else:
            self.setParms({f"{flam3_iterator_prm_names.xaos}_{str(iter+1)}": "xaos:"})


###############################################################################################
# Parameters resets... 
###############################################################################################
def reset_preaffine(kwargs: dict) -> None:
    node = kwargs['node']
    id = kwargs['script_multiparm_index']
    n = flam3_iterator_prm_names
    # pre affine
    node.setParms({f"{n.preaffine_x}_{str(id)}": hou.Vector2((1.0, 0.0))})
    node.setParms({f"{n.preaffine_y}_{str(id)}": hou.Vector2((0.0, 1.0))})
    node.setParms({f"{n.preaffine_o}_{str(id)}": hou.Vector2((0.0, 0.0))})
    node.setParms({f"{n.preaffine_ang}_{str(id)}": 0})
    
def reset_postaffine(kwargs: dict) -> None:
    node = kwargs['node']
    id = kwargs['script_multiparm_index']
    n = flam3_iterator_prm_names
    # post affine
    if node.parm(f"{n.postaffine_do}_{str(id)}").eval():
        node.setParms({f"{n.postaffine_x}_{str(id)}": hou.Vector2((1.0, 0.0))})
        node.setParms({f"{n.postaffine_y}_{str(id)}": hou.Vector2((0.0, 1.0))})
        node.setParms({f"{n.postaffine_o}_{str(id)}": hou.Vector2((0.0, 0.0))})
        node.setParms({f"{n.postaffine_ang}_{str(id)}": 0})
    
def reset_preaffine_FF(kwargs: dict) -> None:
    node = kwargs['node']
    n = flam3_iterator_prm_names
    # pre affine
    node.setParms({f"{PRX_FF_PRM}{n.preaffine_x}": hou.Vector2((1.0, 0.0))})
    node.setParms({f"{PRX_FF_PRM}{n.preaffine_y}": hou.Vector2((0.0, 1.0))})
    node.setParms({f"{PRX_FF_PRM}{n.preaffine_o}": hou.Vector2((0.0, 0.0))})
    node.setParms({f"{PRX_FF_PRM}{n.preaffine_ang}": 0})
    
def reset_postaffine_FF(kwargs: dict) -> None:
    node = kwargs['node']
    n = flam3_iterator_prm_names
    # post affine
    if node.parm(f"{PRX_FF_PRM}{n.postaffine_do}").eval():
        node.setParms({f"{PRX_FF_PRM}{n.postaffine_x}": hou.Vector2((1.0, 0.0))})
        node.setParms({f"{PRX_FF_PRM}{n.postaffine_y}": hou.Vector2((0.0, 1.0))})
        node.setParms({f"{PRX_FF_PRM}{n.postaffine_o}": hou.Vector2((0.0, 0.0))})
        node.setParms({f"{PRX_FF_PRM}{n.postaffine_ang}": 0})


def reset_FF(self: hou.Node) -> None:

    n = flam3_iterator_prm_names

    self.setParms({f"{PRX_FF_PRM}{n.main_note}": "iterator_FF"}) # type: ignore
    # FF pre
    self.setParms({f"{PRX_FF_PRM}{n.prevar_type_1}":  0}) # type: ignore 
    self.setParms({f"{PRX_FF_PRM}{n.prevar_weight_1}": 0}) # type: ignore
    # FF var
    self.setParms({f"{PRX_FF_PRM}{n.var_type_1}": 0}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.var_type_2}": 0}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.var_weight_1}": 1}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.var_weight_2}": 0}) # type: ignore
    # FF post
    self.setParms({f"{PRX_FF_PRM}{n.postvar_type_1}": 0}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.postvar_type_2}": 0}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.postvar_weight_1}": 0}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.postvar_weight_2}": 0}) # type: ignore
    # FF affine
    self.setParms({f"{PRX_FF_PRM}{n.preaffine_x}": hou.Vector2((1.0, 0.0))}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.preaffine_y}": hou.Vector2((0.0, 1.0))}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.preaffine_o}": hou.Vector2((0.0, 0.0))}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.preaffine_ang}": 0}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_do}": 0}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_x}": hou.Vector2((1.0, 0.0))}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_y}": hou.Vector2((0.0, 1.0))}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_o}": hou.Vector2((0.0, 0.0))}) # type: ignore
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_ang}": 0}) # type: ignore


def reset_SYS(self: hou.Node, density: int, iter: int, mode: int) -> None:
    """
    Args:
        density (int): Numper of points to use
        iter (int): Number of iterations
        mode (int): 0: skip "doff" 1: reset "doff"
    """    
    
    self.setParms({SYS_PT_COUNT: density}) # type: ignore
    self.setParms({SYS_PT_COUNT_PRESETS: 0}) # type: ignore
    self.setParms({SYS_ITERATIONS: iter}) # type: ignore
    if mode:
        self.setParms({SYS_DO_FF: 0}) # type: ignore
    self.setParms({SYS_TAG: 1}) # type: ignore
    self.setParms({SYS_TAG_SIZE: 0}) # type: ignore
    self.setParms({SYS_RIP: 0}) # type: ignore
    
def reset_CP(self, mode=0) -> None:
    if not mode:
        # CP
        self.setParms({RAMP_HSV_VAL_NAME: hou.Vector3((1.0, 1.0, 1.0))})
        # CP->ramp
        ramp_parm = self.parm(RAMP_SRC_NAME)
        ramp_parm.deleteAllKeyframes()
        color_bases = [hou.rampBasis.Linear] * 3 # type: ignore
        color_keys = [0.0, 0.5, 1.0]
        color_values = [(1,0,0), (0,1,0), (0,0,1)]
        if mode==1:
            self.setParms({PALETTE_LIB_PATH: ""})
            self.setParms({PALETTE_OUT_PRESET_NAME: ""})
            self.setParms({PALETTE_PRESETS: "-1"})
            self.setParms({"palettemsg": ''})
        ramp_parm.set(hou.Ramp(color_bases, color_keys, color_values))
    elif mode == 2:
        self.setParms({RAMP_HSV_VAL_NAME: hou.Vector3((1.0, 1.0, 1.0))})
    elif mode == 3:
        ramp_parm = self.parm(RAMP_SRC_NAME)
        ramp_parm.deleteAllKeyframes()
        color_bases = [hou.rampBasis.Linear] * 3 # type: ignore
        color_keys = [0.0, 0.5, 1.0]
        color_values = [(1,0,0), (0,1,0), (0,0,1)]
        ramp_parm.set(hou.Ramp(color_bases, color_keys, color_values))
    # Update ramp py 
    palette_cp(self)
    palette_hsv(self)

def reset_MB(self) -> None:
    self.setParms({OUT_MB_DO: 0})
    self.setParms({OUT_MB_FPS: 24})
    self.setParms({OUT_MB_SAMPLES: 16})
    self.setParms({OUT_MB_SHUTTER: 0.5})
    
def reset_IN(self, mode=0) -> None:
    self.setParms({IN_ISVALID_FILE: 0})
    self.setParms({MSG_FLAMESTATS: ""})
    self.setParms({MSG_FLAMERENDER: ""})
    self.setParms({MSG_DESCRIPTIVE_PRM: ""})
    if mode:
        self.setParms({IN_PATH: ""})
        self.setParms({IN_PRESETS: str(-1)})
        self.setParms({"iternumonload": 64})
        self.setParms({"useiteronload": 0})
        self.setParms({IN_COPY_RENDER_PROPERTIES_ON_LOAD: 0})
    
def reset_OUT(self, mode=0) -> None:
    self.setParms({"outedit": 0})
    self.setParms({"outmsg": ''})
    self.setParms({USE_FRACTORIUM_COLOR_SPEED: 0})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE): hou.Vector2((1920, 1080))})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER): hou.Vector2((0, 0))})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE): 0})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE): 100})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY): 1000})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS): 1})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA): 2.5})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER): 1})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2): 0})
    self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY): 0.333333})
    if mode:
        self.setParms({OUT_PATH: ""})
        self.setParms({OUT_HSV_PALETTE_DO: 1})
        self.setParms({OUT_PRESETS: "-1"})
        self.setParms({OUT_FLAME_PRESET_NAME: ""})

def reset_PREFS(self: hou.Node, mode=0) -> None:
    self.setParms({"showprefs": 1}) # type: ignore
    self.setParms({XAOS_MODE: 0}) # type: ignore
    self.setParms({"camhandle": 0}) # type: ignore
    self.setParms({"camcull": 0}) # type: ignore
    self.setParms({"fcam": ""}) # type: ignore
    self.setParms({"cullamount": 0.99}) # type: ignore
    if mode:
        self.setParms({"f3c": 1}) # type: ignore


###############################################################################################
# Load default values. ( Sierpinsky triangle )
###############################################################################################
def flam3_default(self: hou.Node) -> None:
    """
    Args:
        self (hou.Node): [current hou.Node]
    """
    # Iterators reset
    self.setParms({FLAM3_ITERATORS_COUNT: 0}) # type: ignore
    for p in self.parms():
        p.deleteAllKeyframes()
    # Add back iterators
    # This way all parameters will reset to their default values.
    self.setParms({FLAM3_ITERATORS_COUNT: 3}) # type: ignore

    #
    # SYS
    reset_SYS(self, 1, 10, 1)
    reset_FF(self)
    reset_CP(self)
    reset_MB(self)
    reset_IN(self)
    reset_OUT(self)
    reset_PREFS(self)
    
    # iterators
    n = flam3_iterator_prm_names

    # iter 1
    #
    # shader
    self.setParms({f"{n.shader_color}_1": 0}) # type: ignore
    self.setParms({f"{n.shader_speed}_1": -0.5}) # type: ignore
    # vars
    self.setParms({f"{n.prevar_type_1}_1": 0}) # type: ignore
    self.setParms({f"{n.prevar_type_2}_1": 0}) # type: ignore
    self.setParms({f"{n.var_type_1}_1": 0}) # type: ignore
    self.setParms({f"{n.var_type_2}_1": 0}) # type: ignore
    self.setParms({f"{n.var_type_3}_1": 0}) # type: ignore
    self.setParms({f"{n.var_type_4}_1": 0}) # type: ignore
    self.setParms({f"{n.postvar_type_1}_1": 0}) # type: ignore
    # pre affine
    self.setParms({f"{n.preaffine_x}_1": hou.Vector2((0.5, 0.0))}) # type: ignore
    self.setParms({f"{n.preaffine_y}_1": hou.Vector2((0.0, 0.5))}) # type: ignore
    self.setParms({f"{n.preaffine_o}_1": hou.Vector2((0.0, 0.51225))}) # type: ignore

    # iter 2
    #
    # shader
    self.setParms({f"{n.shader_color}_2": 0.5}) # type: ignore
    self.setParms({f"{n.shader_speed}_2": -0.5}) # type: ignore
    # vars
    self.setParms({f"{n.prevar_type_1}_2": 0}) # type: ignore
    self.setParms({f"{n.prevar_type_2}_2": 0}) # type: ignore
    self.setParms({f"{n.var_type_1}_2": 0}) # type: ignore
    self.setParms({f"{n.var_type_2}_2": 0}) # type: ignore
    self.setParms({f"{n.var_type_3}_2": 0}) # type: ignore
    self.setParms({f"{n.var_type_4}_2": 0}) # type: ignore
    self.setParms({f"{n.postvar_type_1}_2": 0}) # type: ignore
    # pre affine
    self.setParms({f"{n.preaffine_x}_2": hou.Vector2((0.5, 0.0))}) # type: ignore
    self.setParms({f"{n.preaffine_y}_2": hou.Vector2((0.0, 0.5))}) # type: ignore
    self.setParms({f"{n.preaffine_o}_2": hou.Vector2((-0.29575, 0.0))}) # type: ignore

    # iter 3
    #
    # shader
    self.setParms({f"{n.shader_color}_3": 1.0}) # type: ignore
    self.setParms({f"{n.shader_speed}_3": -0.5}) # type: ignore
    # vars
    self.setParms({f"{n.prevar_type_1}_3": 0}) # type: ignore
    self.setParms({f"{n.prevar_type_2}_3": 0}) # type: ignore
    self.setParms({f"{n.var_type_1}_3": 0}) # type: ignore
    self.setParms({f"{n.var_type_2}_3": 0}) # type: ignore
    self.setParms({f"{n.var_type_3}_3": 0}) # type: ignore
    self.setParms({f"{n.var_type_4}_3": 0}) # type: ignore
    self.setParms({f"{n.postvar_type_1}_3": 0}) # type: ignore
    # pre affine
    self.setParms({f"{n.preaffine_x}_3": hou.Vector2((0.5, 0.0))}) # type: ignore
    self.setParms({f"{n.preaffine_y}_3": hou.Vector2((0.0, 0.5))}) # type: ignore
    self.setParms({f"{n.preaffine_o}_3": hou.Vector2((0.29575, 0.0))}) # type: ignore
    
    self.setParms({SYS_PT_COUNT: POINT_COUNT_LOAD_DEFAULT}) # type: ignore


###############################################################################################
# Parameters reset if iterators count is set to ZERO.
###############################################################################################
def iteratorCountZero(self: hou.Node) -> None:
    """
    Args:
        self (hou.Node): [current hou.Node]
    """

    if not self.parm(FLAM3_ITERATORS_COUNT).evalAsInt():
        # delete channel references
        for p in self.parms():
            p.deleteAllKeyframes()
        # SYS
        self.setParms({SYS_PT_COUNT: 500000}) # type: ignore
        self.setParms({SYS_DO_FF: 0}) # type: ignore
        self.setParms({SYS_RIP: 0}) # type: ignore
        # FF vars
        reset_FF(self)
        # MB
        reset_MB(self)
        # prefs
        self.setParms({"showprefs": 1}) # type: ignore
        #self.setParms({XAOS_MODE: 0})
        self.setParms({"camhandle": 0}) # type: ignore
        self.setParms({"camcull": 0}) # type: ignore
        #self.setParms({"fcam": ""})
        #self.setParms({"cullamount": 0.99})
        
        # descriptive message parameter
        self.setParms({MSG_DESCRIPTIVE_PRM: ""}) # type: ignore

###############################################################################################
# Open web browser to the FLAM3 for Houdini website
###############################################################################################
def web_flame3hda() -> None:
    page = "https://alexnardini.net/flame-home/"
    webbrowser.open(page)
    
###############################################################################################
# Open web browser to the FLAM3 for Houdini github
###############################################################################################
def web_flame3github() -> None:
    page = "https://github.com/alexnardini/FLAM3_for_SideFX_Houdini"
    webbrowser.open(page)
    
###############################################################################################
# Open web browser to the FLAM3 for Houdini instagram
###############################################################################################
def web_flame3insta() -> None:
    page = "https://www.instagram.com/alexnardini/"
    webbrowser.open(page)

###############################################################################################
# Open web browser to the FractalFlame Algorithm paper
###############################################################################################
def web_TFFA() -> None:
    page = "https://flam3.com/flame_draves.pdf"
    webbrowser.open(page)
    
###############################################################################################
# Open web browser to the FractalFlame Algorithm FLAM3 Github
###############################################################################################
def web_FLAM3github() -> None:
    page = "https://github.com/scottdraves/flam3"
    webbrowser.open(page)


###############################################################################################
# XAOS usage infos. Show a portion of the xaos documentation as an info window
###############################################################################################
def ui_xaos_infos() -> None:
    ALL_msg = """The default mode is \"xaos TO\". You can change it to use \"xaos FROM\" mode instead in the preferences tab.

To set XAOS for a flame with 4 iterators,
use the "xaos:" keyword followed by each iterator weights values separated by a colon:
\"xaos:1:2:3:4\" ( xaos keyword can be uppercase too if you prefer. )

If no set or when using a short descriptive note,
FLAM3 will assume all XAOS values are 1.0, the equivalent of: \"xaos:1:1:1:1\"

If you set only iterator 1 and iterator 2,
FLAM3 will always fill in the rest with a value of 1.0. \"xaos:0:0\" will be interpreted as \"xaos:0:0:1:1\"

When turning iterators OFF and ON, FLAM3 will internally remove and reformat XAOS values to account for missing iterator
so you wont need to remove values from the command string,
unless you delete an iterator in wich case you will require to modify the “xaos:” command string."""
    hou.ui.displayMessage(ALL_msg, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3 XAOS usage infos", details=None, details_label=None, details_expanded=False) # type: ignore

###############################################################################################
# OUT Presets name infos.
###############################################################################################
def ui_OUT_presets_name_infos() -> None:
    ALL_msg = """When choosing a preset name for your fractal flame,
you can bake into it the iteration number you want it to use once you load it back into FLAM3 for Houdini.

For example if you name a flame preset: \"My_Awesome_GrandJulia\" it will be loaded with a default 64 iterations.
But if you append the iteration number after a double colons to the preset name like so: \"My_Awesome_GrandJulia::16\"
it will override all settings and load it using 16 as iteration numbers.

Optionally, you can manually edit the saved XML/Flame file
and modify the flame → \"name\" key yourself after the fact if you desire so.

If no name is provided,
an automated name composed of today’s date and current time will be used instead."""
    hou.ui.displayMessage(ALL_msg, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3 Presets name infos", details=None, details_label=None, details_expanded=False) # type: ignore

###############################################################################################
# Disabled iterator save out info.
###############################################################################################
def ui_active_iterator_infos() -> None:
    ALL_msg = """If an iterator is disabled,
it wont be included when saving the flame out into a Flame file.

In case you still want to include the inactive iterator into the file,
set its Weight to Zero instead."""
    hou.ui.displayMessage(ALL_msg, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3 Active iterator infos", details=None, details_label=None, details_expanded=False) # type: ignore



# LOAD XML FLAME FILES start here

def make_NULL(name: Union[str, list[str], tuple[str]]) -> Union[str, list[str], tuple[str]]:
    return name

def make_VAR(name: Union[str, list[str], tuple[str]]) -> Union[Union[str, list[str]], None]:
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

def make_PRE(name: Union[str, Union[list[str], KeysView], tuple[str]]) -> Union[str, list[str], None]:
    if type(name) is str:
        if not (name.startswith(V_PRX_PRE) and name.startswith(V_PRX_POST)):
            return V_PRX_PRE + name
    elif type(name) is list or tuple:
        return [V_PRX_PRE + x for x in name if x.startswith(V_PRX_PRE) is False and x.startswith(V_PRX_POST) is False]
    else:
        return None

def make_POST(name: Union[str, Union[list[str], KeysView], tuple[str]]) -> Union[str, list[str], None]:
    if type(name) is str:
        if not (name.startswith(V_PRX_PRE) and name.startswith(V_PRX_POST)):
            return V_PRX_POST + name
    elif type(name) is list or tuple:
        return [V_PRX_POST + x for x in name if x.startswith(V_PRX_PRE) is False and x.startswith(V_PRX_POST) is False]
    else:
        return None


# It happen that Houdini sometime round value to many, many decimals.
# I am limiting this to max 8 decimals on export so not to have the xml file explode with trailing floats...
# Increase this if for some reason you need more precision.
ROUND_DECIMAL_COUNT = 8
# XML
XML_FLAME_NAME = "flame"
XML_FLAME_VERSION = "version"
XML_FLAME_PLUGINS = "plugins"
XML_FLAME_NEW_LINEAR = "new_linear"
XML_XF = "xform"
XML_XF_WEIGHT = "weight"
XML_XF_NAME = "name"
XML_XF_PB = "pre_blur"
XML_FF = "finalxform"
XML_PRE_AFFINE = "coefs"
XML_POST_AFFINE = "post"
XML_XF_XAOS = "chaos"
XML_PALETTE = "palette"
XML_PALETTE_COUNT = "count"
XML_PALETTE_FORMAT = "format"
XML_XF_COLOR = "color"
XML_XF_VAR_COLOR = "var_color"
XML_XF_SYMMETRY = "symmetry"
XML_XF_COLOR_SPEED = "color_speed"
XML_XF_OPACITY = "opacity"
# custom to FLAM3H only
OUT_XML_FLAM3H_HSV = 'flam3h_hsv'
OUT_XML_FLMA3H_MB_FPS = 'flam3h_fps'
OUT_XML_FLMA3H_MB_SAMPLES = 'flam3h_mbsamples'
OUT_XML_FLMA3H_MB_SHUTTER = 'flam3h_shutter'
# XML OUT render key data names
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
OUT_XML_RENDER_HOUDINI_DICT = {XML_XF_NAME: OUT_FLAME_PRESET_NAME,
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
XML_VALID_FLAMES_ROOT_TAG = "flames"
# Since we get the folowing keys in a separate action, we exclude them for later variation's names searches to help speed up a little.
XML_XF_KEY_EXCLUDE = ("weight", "color", "var_color", "symmetry", "color_speed", "name", "animate", "pre_blur", "coefs", "post", "chaos", "opacity")
# Note that "pre_gaussian_blur" has been added to this tuple as we force it to be remapped to "pre_blur" on load inside FLAM3 for Houdini
# if "remap "pre_gaussian_blur" to pre_blur" preference option is checked (ON by default)
XML_XF_KEY_EXCLUDE_PGB = ("weight", "color", "var_color", "symmetry", "color_speed", "name", "animate", "pre_blur", "pre_gaussian_blur", "coefs", "post", "chaos", "opacity")

# This has been fixed and now radial_blur variation matches all the other apps
# but I leave it here just in case other variation will need it.
XML_XF_PRM_EXCEPTION = ("None", )

POINT_COUNT_LOAD_DEFAULT = 500000
ITER_LOAD_DEFAULT = 64
OUT_FLAM3_FILE_EXT = '.flame'

# REGEX_ALL = "(?s:.*?)"
REGEX_PALETTE_LIB_LOCK = f"^(?:{FLAM3_LIB_LOCK})"
REGEX_PRE = "^(?:pre_)"
REGEX_POST = "^(?:post_)"

V_PRX_PRE = "pre_"
V_PRX_POST = "post_"

MAX_ITER_VARS = 4
MAX_ITER_VARS_PRE = 2
MAX_ITER_VARS_POST = 1
MAX_FF_VARS = 2
MAX_FF_VARS_PRE = 1
MAX_FF_VARS_POST = 2

XML_APP_NAME_FLAM3HOUDINI = "FLAM3H"
XML_APP_NAME_FRACTORIUM = "EMBER-"
XML_APP_NAME_APO = "Apophysis"

# This is used as a faster idx lookup table.
# From the XML's xforms, each variations look itself up inside here to get the corresponding FLAM3 for houdini var idx it is mapped to.
# The key names matter and must match the variation's names as known by other apps ( in my case: Apophysis and Fratorium )
VARS_FLAM3_DICT_IDX = { "linear": 0, 
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
VARS_FRACTORIUM_DICT = {"a": ("arch", "arcsech", "arcsech2", "arcsinh", "arctanh", "asteria", "auger"),
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
                        "z": ("z", "zblur", "zcone", "zscale","ztranslate") }

def vars_dict_type_maker(vars_dict: dict, func: Callable) -> dict:
    return dict(map(lambda item: (item[0], func(item[1])), vars_dict.items()))
VARS_FRACTORIUM_DICT_PRE  = vars_dict_type_maker(VARS_FRACTORIUM_DICT, make_PRE)
VARS_FRACTORIUM_DICT_POST = vars_dict_type_maker(VARS_FRACTORIUM_DICT, make_POST)


class flam3_varsPRM_APO:
    
    # The following parameters matches the Apophysis/Fractorium parameter's names,
    # so no need to regex for now as the strings names are matching already.
    #
    # There are a few exceptions so far witch I handled simply for now, but it work.
    #
    # They are grouped as follow and based on the FLAM3 Houdini node parametric parameters:
    #
    # for generic variation:
    # ("variation name", bool: (parametric or not parametric)),
    #
    # for parametric variation:
    # ("variation name", (prm_1, ..., prm_4), (prm_1, ..., prm_4), bool: (parametric or not parametric)),
    #
    # -> (prm_1, ..., prm_4) accept a max of 4 entries (hou.Vector4) and based on the number of parameters
    # they are then automatically converted to the expeted v_type using the function: 
    # typemaker(list[]) -> Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4]:
    #
    # The (("variation_name") entrie, is not used here and only for reference.
    
    varsPRM = ( ("linear", 0), 
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
    # Update this and def prm_name_exceptions() if you add/find more
    varsPRM_FRACTORIUM_EXCEPTIONS = { 67: ("oscilloscope", ("oscilloscope_frequency", "oscilloscope_amplitude", "oscilloscope_damping", "oscilloscope_separation"), 1),
                                      96: ("Mobius", ("Mobius_Re_A", "Mobius_Re_B", "Mobius_Re_C", "Mobius_Re_D"), ("Mobius_Im_A", "Mobius_Im_B", "Mobius_Im_C", "Mobius_Im_D"), 1)
                        }


class _xml_tree:

    def __init__(self, xmlfile: str) -> None:
        """
        Args:
            xmlfile (str): xmlfile (str): [xml *.flame file v_type to load]
        """        
        self._xmlfile = xmlfile
        self._isvalidtree = False
        try:
            self._tree = ET.parse(xmlfile)
            if isinstance(self._tree, ET.ElementTree):
                root = self._tree.getroot()
                if XML_VALID_FLAMES_ROOT_TAG in root.tag.lower():
                    self._isvalidtree = True
                else:
                    self._isvalidtree = False
            else:
                self._isvalidtree = False
        except:
            self._isvalidtree = False
            
    
    @property
    def xmlfile(self):
        return self._xmlfile
    
    @property
    def tree(self):
        return self._tree
    
    @property
    def isvalidtree(self):
        return self._isvalidtree
    

    def __get_name(self, key=XML_XF_NAME) -> Union[tuple, None]:
        if self._isvalidtree:
            root = self._tree.getroot()
            names = []
            for name in root:
                if name.get(key) is not None:
                    names.append(name.get(key))
                else:
                    names.append([])
            return tuple(names)
        else:
            return None
        
    def __get_flame(self, key=XML_FLAME_NAME) -> Union[tuple, None]:
        if self._isvalidtree:
            root = self._tree.getroot()
            flames = []    
            for f in root.iter(key):
                flames.append(f)
            return tuple(flames)
        else:
            return None

    def __get_flame_count(self, flames: list) -> int:
        if self._isvalidtree:
            return len(flames)
        return 0


class apo_flame(_xml_tree):

    def __init__(self, node: hou.Node, xmlfile: str) -> None:
        """
        Args:
            xmlfile (str): [xml *.flame v_type file to load]
        """        
        super().__init__(xmlfile)
        self._node = node
        self._name = self._xml_tree__get_name() # type: ignore
        self._apo_version = self._xml_tree__get_name(XML_FLAME_VERSION) # type: ignore
        self._flame = self._xml_tree__get_flame() # type: ignore
        self._flame_count = self._xml_tree__get_flame_count(self._flame) # type: ignore
        self._flame_plugins = self._xml_tree__get_name(XML_FLAME_PLUGINS) # type: ignore
        # render properties
        self._out_size = self._xml_tree__get_name(OUT_XML_FLAME_SIZE) # type: ignore
        self._out_center = self._xml_tree__get_name(OUT_XML_FLAME_CENTER) # type: ignore
        self._out_rotate = self._xml_tree__get_name(OUT_XML_FLAME_ROTATE) # type: ignore
        self._out_scale = self._xml_tree__get_name(OUT_XML_FLAME_SCALE) # type: ignore
        self._out_quality = self._xml_tree__get_name(OUT_XML_FLAME_QUALITY) # type: ignore
        self._out_brightness = self._xml_tree__get_name(OUT_XML_FLAME_BRIGHTNESS) # type: ignore
        self._out_gamma = self._xml_tree__get_name(OUT_XML_FLAME_GAMMA) # type: ignore
        self._out_highlight_power = self._xml_tree__get_name(OUT_XML_FLAME_POWER) # type: ignore
        self._out_logscale_k2 = self._xml_tree__get_name(OUT_XML_FLAME_K2) # type: ignore
        self._out_vibrancy = self._xml_tree__get_name(OUT_XML_FLAME_VIBRANCY) # type: ignore
        # custom to FLAM3H only
        self._flam3h_hsv = self._xml_tree__get_name(OUT_XML_FLAM3H_HSV) # type: ignore
        # just check any of the MB val and if exist mean there is MB data to be set.
        # this will act as bool and if true, it will hold our OUT_XML_FLMA3H_MB_FPS value ( as string )
        self._flam3h_mb = self._xml_tree__get_name(OUT_XML_FLMA3H_MB_FPS) # type: ignore
        self._flam3h_mb_samples = self._xml_tree__get_name(OUT_XML_FLMA3H_MB_SAMPLES) # type: ignore
        self._flam3h_mb_shutter = self._xml_tree__get_name(OUT_XML_FLMA3H_MB_SHUTTER) # type: ignore
    

    @staticmethod
    def affine_coupling(affine: list) -> list:
        """
        Args:
            affine (list): [affine values from the xml]

        Returns:
            list: [a list of hou.Vector2: ((X.x, X.y), (Y.x, Y.y), (O.x, O.y)) ready to be used to set affine parms]
        """        
        return [hou.Vector2((tuple(affine[i:i+2]))) for i in (0, 2, 4)]
    

    @property
    def node(self):
        return self._node
    
    @property
    def name(self):
        return self._name
    
    @property
    def apo_version(self):
        return self._apo_version

    @property
    def flame(self):
        return self._flame

    @property
    def flame_count(self):
        return self._flame_count
    
    @property
    def flame_plugins(self):
        return self._flame_plugins
    
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
    def flam3h_mb(self):
        return self._flam3h_mb
    
    @property
    def flam3h_mb_samples(self):
        return self._flam3h_mb_samples
    
    @property
    def flam3h_mb_shutter(self):
        return self._flam3h_mb_shutter
    




    def __is_valid_idx(self, idx: int) -> int:
        """Make sure the fractal flame's idx passed in will always be valid and never out of range.

        Args:
            idx (int): [flame idx out of all flames included in the loaded flame file]

        Returns:
            int: [clamped idx value just in case the user pass an invalid idx to this function]
        """     
        return 0 if idx < 0 else 0 if self._flame_count == 1 else self._flame_count - 1 if idx > self._flame_count - 1 else idx

    def __get_xforms(self, idx: int, key: str) -> Union[tuple, None]:
        """Get choosen fractal flame's xforms collected inside a dict each.
        every xform in xforms is a dict coming directly from the parsed XML file.

        Args:
            idx (int): [flame idx out of all flames included in the loaded flame file]
            key (str): [use "xform" for transforms and "finalxofrm" for final flame transform]

        Returns:
            list: [a list of all xforms inside the selected flame or None]
        """
        if  self._isvalidtree:
            xforms = []
            for xf in self._flame[idx].iter(key):
                xforms.append(xf.attrib)
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
    
    def __get_xaos(self, xforms: list, key=XML_XF_XAOS) -> Union[tuple, None]:
        """
        Args:
            tree (Type[ET.ElementTree]): [a valid xml.etree.ElementTree tree]
            xforms (list): [list of all xforms contained inside this flame]

        Returns:
            Union[list, None]: [either a list of xaos strings or None]
        """        
        if  self._isvalidtree:
            xaos = []
            for xform in xforms:
                if xform.get(key) is not None:
                    chaos = ":".join(xform.get(key).split())
                    xaos.append(f"xaos:{chaos}")
                else:
                    xaos.append([])
            if not max(list(map(lambda x: len(x), xaos))):
                return None
            else:
                return tuple(xaos)
        else:
            return None

    def __get_affine(self, xforms: list, key: str) -> Union[tuple, None]:
        """
        Args:
            tree (Type[ET.ElementTree]): [a valid xml.etree.ElementTree tree]
            xforms (list): [list of all xforms contained inside this flame]
            key (str): [affine xml tag name. Either 'coefs' for pre affine or 'post' for post affine]

        Returns:
            Union[list, None]: [Either a list of list of tuples ((X.x, X.y), (Y.x, Y.y), (O.x, O.y)) or None]
        """           
        if  self._isvalidtree:
            if xforms is not None:
                coefs = []
                for xform in xforms:
                    if xform.get(key) is not None:
                        affine = [float(x) for x in xform.get(key).split()]
                        coefs.append(tuple(self.affine_coupling(affine)))
                    else:
                        coefs.append([])
                if not max(list(map(lambda x: len(x), coefs))):
                    return None
                else:
                    return tuple(coefs)
        else:
            return None
        
    def __get_keyvalue(self, xforms: list, key: str) -> Union[tuple, None]:
        """
        Args:
            xforms (list): [list of all xforms contained inside this flame]
            key (str): [xml tag names. For shader: 'color', 'symmetry'->(color_speed), 'opacity']

        Returns:
            Union[list, None]: [description]
        """        
        if  self._isvalidtree:
            if xforms is not None:
                keyvalues = []
                for xform in xforms:
                    if xform.get(key) is not None:
                        if key in XML_XF_NAME:
                            keyvalues.append(xform.get(key))
                            continue
                        else:
                            keyvalues.append(float(xform.get(key)))
                            continue
                    else:
                        # Fractorium seem to always remap pre_blur to pre_gaussian_blur when you load a flame in.
                        # Lets do the same but we will remap pre_gaussian_blur back to pre_blur when we load a flame back in FLAM3 for Houdini.
                        pre_gaussian_blur = xform.get(make_PRE(var_name_from_dict(VARS_FLAM3_DICT_IDX, 33)))
                        if pre_gaussian_blur is not None:
                            if self._node.parm(REMAP_PRE_GAUSSIAN_BLUR).eval():
                                keyvalues.append(float(pre_gaussian_blur))
                                continue
                            else:
                                keyvalues.append(float(0))
                                continue
                        # Flame files created with Apophysis versions older than 7x ( or much older as the test file I have is from v2.06c )
                        # seem not to include those keys if not used or left at default values.
                        # We set them here so we can use them inside FLAM3 for Houdini on load.
                        elif key in XML_XF_OPACITY:
                            keyvalues.append(float(1))
                            continue
                        elif key in XML_XF_SYMMETRY:
                            keyvalues.append(float(0))
                            continue
                        else:
                            keyvalues.append([])
                            continue
                return tuple(keyvalues)
        else:
            return None

        
    def __get_palette(self, idx: int, key=XML_PALETTE) -> Union[tuple[hou.Ramp, int, str], None]:
        """
        Args:
            tree (Type[ET.ElementTree]): [a valid xml.etree.ElementTree tree]
            idx (int): [flame idx out of all flames included in the loaded flame file]

        Returns:
            hou.Ramp: [return an already made hou.Ramp with values from the flame xml palette]
        """        
        if  self._isvalidtree:
            try:
                palette_attrib = self._flame[idx].find(key).attrib
            except:
                palette_attrib = None
                
            if palette_attrib is not None:
                palette_hex = self._flame[idx].find(key).text
                format = dict(palette_attrib).get(XML_PALETTE_FORMAT)
                HEX = []
                for line in palette_hex.splitlines():
                    cleandoc = inspect.cleandoc(line)
                    if(len(cleandoc)>1):
                        [HEX.append(hex) for hex in wrap(cleandoc, 6)]
                try:
                    rgb_from_XML_PALETTE = []
                    for hex in HEX:
                        x = hex_to_rgb(hex)
                        rgb_from_XML_PALETTE.append((x[0]/(255 + 0.0), x[1]/(255 + 0.0), x[2]/(255 + 0.0)))
                    ramp_keys_count = len(rgb_from_XML_PALETTE)
                    POSs = list(iter_islice(iter_count(0, 1.0/(ramp_keys_count-1)), (ramp_keys_count)))
                    BASESs = [hou.rampBasis.Linear] * (ramp_keys_count) # type: ignore
                    return hou.Ramp(BASESs, POSs, rgb_from_XML_PALETTE), (ramp_keys_count), str(format)
                except:
                    hou.pwd().setParms({MSG_DESCRIPTIVE_PRM: "Error: IN->PALETTE\nHEX values not valid."})
                    ui_text = "Flame's Palette hex values not valid."
                    palette_warning_msg = f"PALETTE Error:\nPossibly some out of bounds values in it.\n\nYou can fix this by assigning a brand new palette before saving it out again.\nYou can open this Flame in Fractorium and assign a brand new palette\nto it and save it out to re load it again inside FLAM3 Houdini."
                    hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3 Palette Error", details=palette_warning_msg, details_label=None, details_expanded=True) # type: ignore
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
            hou.Vector3 or False: [a hou.Vector3 of HSV vals or False]
        """   
        if self._isvalidtree:
            palette_hsv_xml_list = self._flam3h_hsv[idx]
            if palette_hsv_xml_list:
                palette_hsv_xml_s = str(palette_hsv_xml_list).split(" ")
                return typemaker(list(map(lambda x: float(x), palette_hsv_xml_s)))
            else:
                return False
        else:
            return False
        
    def __get_mb_flam3h_mb(self, idx: int, key='') -> Union[int, float, bool, None]:
        """
        Args:
            idx (int): [flame idx out of all flames included in the loaded flame file]

        Returns:
            hou.Vector3 or False: [a hou.Vector3 of HSV vals or False]
        """   
        if self._isvalidtree:
            mb_do = self._flam3h_mb[idx]
            # self._flam3h_mb[idx] can also be an empty list, hence the double check
            if mb_do is not None and mb_do:
                if key == OUT_XML_FLMA3H_MB_FPS:
                    return int(mb_do)
                elif key == OUT_XML_FLMA3H_MB_SAMPLES:
                    return int(self._flam3h_mb_samples[idx])
                elif key == OUT_XML_FLMA3H_MB_SHUTTER:
                    return float(self._flam3h_mb_samples[idx])
                else:
                    return False
            else:
                return False
        else:
            return False



class apo_flame_iter_data(apo_flame):

    def __init__(self, node: hou.Node, xmlfile: str, idx=0) -> None:
        """
        Args:
            xmlfile (str): xmlfile (str): [xml flame v_type file to load]
            idx (int, optional): [flame idx out of all flames included in the loaded flame file]. Defaults to 0.
        """        
        super().__init__(node, xmlfile)
        self._idx = self._apo_flame__is_valid_idx(idx) # type: ignore
        self._xforms = self._apo_flame__get_xforms(self._idx, XML_XF) # type: ignore
        self._xf_name = self._apo_flame__get_keyvalue(self._xforms, XML_XF_NAME) # type: ignore
        self._weight = self._apo_flame__get_keyvalue(self._xforms, XML_XF_WEIGHT) # type: ignore
        self._pre_blur = self._apo_flame__get_keyvalue(self._xforms, XML_XF_PB) # type: ignore
        self._xaos  = self._apo_flame__get_xaos(self._xforms) # type: ignore
        self._coefs = self._apo_flame__get_affine(self._xforms, XML_PRE_AFFINE) # type: ignore
        self._post  = self._apo_flame__get_affine(self._xforms, XML_POST_AFFINE) # type: ignore
        self._finalxform = self._apo_flame__get_xforms(self._idx, XML_FF) # type: ignore
        self._finalxform_coefs = self._apo_flame__get_affine(self._finalxform, XML_PRE_AFFINE) # type: ignore
        self._finalxform_post  = self._apo_flame__get_affine(self._finalxform, XML_POST_AFFINE) # type: ignore
        self._finalxform_name = self._apo_flame__get_keyvalue(self._finalxform, XML_XF_NAME) # type: ignore
        self._palette = self._apo_flame__get_palette(self._idx) # type: ignore
        self._color = self._apo_flame__get_keyvalue(self._xforms, XML_XF_COLOR) # type: ignore
        self._color_speed = self._apo_flame__get_keyvalue(self._xforms, XML_XF_COLOR_SPEED) # type: ignore
        self._symmetry = self._apo_flame__get_keyvalue(self._xforms, XML_XF_SYMMETRY) # type: ignore
        self._opacity = self._apo_flame__get_keyvalue(self._xforms, XML_XF_OPACITY) # type: ignore
        # custom to FLAM3H only
        self._palette_flam3h_hsv = self._apo_flame__get_palette_flam3h_hsv(self._idx) # type: ignore
        self._mb_flam3h_mb_fps = self._apo_flame__get_mb_flam3h_mb(self._idx, OUT_XML_FLMA3H_MB_FPS) # type: ignore
        self._mb_flam3h_mb_samples= self._apo_flame__get_mb_flam3h_mb(self._idx, OUT_XML_FLMA3H_MB_SAMPLES) # type: ignore
        self._mb_flam3h_mb_shutter = self._apo_flame__get_mb_flam3h_mb(self._idx, OUT_XML_FLMA3H_MB_SHUTTER) # type: ignore


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
    def post(self):
        return self._post
    
    @property
    def finalxform_coefs(self):
        return self._finalxform_coefs
        
    @property
    def finalxform_post(self):
        return self._finalxform_post
    
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
    def palette_flam3h_hsv(self):
        return self._palette_flam3h_hsv
    
    @property
    def mb_flam3h_fps(self):
        return self._mb_flam3h_mb_fps
    
    @property
    def mb_flam3h_samples(self):
        return self._mb_flam3h_mb_samples
    
    @property
    def mb_flam3h_shutter(self):
        return self._mb_flam3h_mb_shutter
    
    
    
###############################################################################################
# MENU - APO - build menu from flame file presets
###############################################################################################
def menu_apo_presets(kwargs: dict) -> list:

    xml = kwargs['node'].parm(IN_PATH).evalAsString()
    menu=[]
    apo = apo_flame(kwargs['node'], xml)
    if apo.isvalidtree:
        for i, item in enumerate(apo.name):
            menu.append(i)
            menu.append(item)
        return menu
    else:
        menu.append(-1)
        menu.append('Empty')
        return menu


# Use this with everything but not PRE and POST dictionary lookup, use def get_xforms_var_keys_PP() instead
def get_xforms_var_keys(xforms: Union[tuple, None], 
                        vars: Union[str, list[str], tuple[str], dict[str, int], KeysView, None], 
                        exclude_keys: tuple
                        ) -> Union[list[str], None]:
    """
    Args:
        xforms (tuple): [list of all xforms contained inside this flame. This can be iterator's xforms or FF xform]

    Returns:
        Union[tuple[list, list], tuple[None, None]]: [return a list of variation's names in each xform,  or None]
    """    
    if xforms is not None:
        vars_keys = []
        if type(vars) is dict:
            for xf in xforms:
                vars_keys.append(list(map(lambda x: x, filter(lambda x: x in vars.get(x[0]), filter(lambda x: x not in exclude_keys, xf.keys())))))
        else:
            for xf in xforms:
                vars_keys.append(list(map(lambda x: x, filter(lambda x: x in vars, filter(lambda x: x not in exclude_keys, xf.keys())))))

        return vars_keys
    else:
        return None


def removeprefix(self: str, prefix: str) -> str:
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]
# to be used with VARS_FRACTORIUM_DICT - ONLY for PRE and POST lookup
def get_xforms_var_keys_PP(xforms: Union[tuple, None], 
                           vars: dict, 
                           prx: str, 
                           exclude_keys: tuple
                           ) -> Union[list[str], None]:
    """
    Args:
        xforms (tuple): [list of all xforms contained inside this flame. This can be iterator's xforms or FF xform]

    Returns:
        Union[tuple[list, list], tuple[None, None]]: [return a list of variation's names in each xform,  or None]
    """    
    if xforms is not None:
        vars_keys = []
        for xf in xforms:
            # Note the: vars.get(removeprefix(x, prx)[0]
            # as we need to remove the prefix in order to get the correct dictionary letter the processed variation start with, hence the [0]
             vars_keys.append(list(map(lambda x: x, filter(lambda x: x in vars.get(removeprefix(x, prx)[0]), filter(lambda x: x.startswith(prx), filter(lambda x: x not in exclude_keys, xf.keys()))))))
        return vars_keys
    else:
        return None


def typemaker(data: list) -> Union[list, float, hou.Vector2, hou.Vector3, hou.Vector4]:
    """
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


def apo_get_idx_by_key(key: str) -> Union[int, None]:
    """
    Args:
        key (str): [variation name we are processing]

    Returns:
        Union[int, None]: [return variation idx from the tuple look up table]
    """
    try: idx = VARS_FLAM3_DICT_IDX.get(key)
    except: return None
    return idx


def flam3_prx_mode(mode: int) -> tuple[str, str]:
    """
    Args:
        mode (int): [0 for iterator and 1 for FF]

    Returns:
        tuple[str, str]: [return parameter prefix based on mode: Iterator, FF, FF POST]
    """
    prx = ""
    prx_prm = ""
    if mode == 1:
        prx = PRX_FF_PRM
        prx_prm = PRX_FF_PRM + "_"
    if mode == 2:
        prx = PRX_FF_PRM
        prx_prm = PRX_FF_PRM_POST + "_"
    return prx, prx_prm


def apo_set_affine(mode: int, 
                   node: hou.Node, 
                   prx: str, 
                   apo_data: apo_flame_iter_data, 
                   n: flam3_iterator_prm_names, 
                   mp_idx: int
                   ) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        prx (str): [parameter name prefix]
        apo_data (apo_flame_iter_data): [Apophysis XML data collection from: class[apo_flame_iter_data]]
        n (flam3_iterator_prm_names): [FLAM3 houdini node iterator parameter's names from: class[apo_flame_iter_data]]
        mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
    """
    if mode:
        node.setParms({f"{prx}{n.preaffine_x}": apo_data.finalxform_coefs[mp_idx][0]}) # type: ignore
        node.setParms({f"{prx}{n.preaffine_y}": apo_data.finalxform_coefs[mp_idx][1]}) # type: ignore
        node.setParms({f"{prx}{n.preaffine_o}": apo_data.finalxform_coefs[mp_idx][2]}) # type: ignore
        if apo_data.finalxform_post is not None:
            node.setParms({f"{prx}{n.postaffine_do}": 1}) # type: ignore
            node.setParms({f"{prx}{n.postaffine_x}": apo_data.finalxform_post[mp_idx][0]}) # type: ignore
            node.setParms({f"{prx}{n.postaffine_y}": apo_data.finalxform_post[mp_idx][1]}) # type: ignore
            node.setParms({f"{prx}{n.postaffine_o}": apo_data.finalxform_post[mp_idx][2]}) # type: ignore
    else:
        node.setParms({f"{prx}{n.preaffine_x}_{str(mp_idx+1)}": apo_data.coefs[mp_idx][0]}) # type: ignore
        node.setParms({f"{prx}{n.preaffine_y}_{str(mp_idx+1)}": apo_data.coefs[mp_idx][1]}) # type: ignore
        node.setParms({f"{prx}{n.preaffine_o}_{str(mp_idx+1)}": apo_data.coefs[mp_idx][2]}) # type: ignore
        if apo_data.post is not None:
            if apo_data.post[mp_idx]:
                node.setParms({f"{prx}{n.postaffine_do}_{str(mp_idx+1)}": 1}) # type: ignore
                node.setParms({f"{prx}{n.postaffine_x}_{str(mp_idx+1)}": apo_data.post[mp_idx][0]}) # type: ignore
                node.setParms({f"{prx}{n.postaffine_y}_{str(mp_idx+1)}": apo_data.post[mp_idx][1]}) # type: ignore
                node.setParms({f"{prx}{n.postaffine_o}_{str(mp_idx+1)}": apo_data.post[mp_idx][2]}) # type: ignore



def apo_set_data(mode: int, 
                 node: hou.Node, 
                 prx: str, 
                 apo_data: list, 
                 prm_name: str, 
                 mp_idx: int
                 ) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        prx (str): [parameter name prefix]
        apo_data (apo_flame_iter_data): [Apophysis XML data collection from: class[apo_flame_iter_data]]
        prm_name (str): [parameter name for the current data we want to set]
        mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
    """
    if mode:
        pass
    else:
        if apo_data is not None:
            n = flam3_iterator_prm_names
            if prm_name not in [n.shader_alpha, n.main_weight]:
                if apo_data[mp_idx]:
                    node.setParms({f"{prx}{prm_name}_{str(mp_idx+1)}": apo_data[mp_idx]}) # type: ignore
            else:
                node.setParms({f"{prx}{prm_name}_{str(mp_idx+1)}": apo_data[mp_idx]}) # type: ignore
            


def prm_name_exceptions(v_type: int, app: str, apo_prm: tuple) -> tuple:
    if app.startswith(XML_APP_NAME_FRACTORIUM):
        check = flam3_varsPRM_APO.varsPRM_FRACTORIUM_EXCEPTIONS.get(v_type)
        if check is not None:
            return check
        else:
            return apo_prm
    else:
        return apo_prm


# I should merge all those v_parametric*() and v_generic*() into one for each
# but it is actually easier for me to debug those and make tests.
# Perhaps something for me to do in the future to make the code cleaner and slimmer.
#
# v_parametric()
# v_parametric_PRE()
# v_parametric_POST()
# v_parametric_PRE_FF()
# v_parametric_POST_FF()
# v_generic()
# v_generic_PRE()
# v_generic_POST()
# v_generic_PRE_FF()
# v_generic_POST_FF()

def var_name_from_dict(mydict: dict, idx: int):
    return list(mydict.keys())[list(mydict.values()).index(idx)]

def v_parametric_var_collect(node: hou.Node, 
                             mode: int, 
                             apo_prm: tuple, 
                             xform: dict, 
                             mp_idx: int, 
                             v_type: int, 
                             func: Callable) -> list:
    """
    Args:
        node (hou.Node): [Current FLAM3 houdini node]
        mode (int): [0 for iterator. 1 for FF]
        apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3_varsPRM_APO.varsPRM[v_type]]
        xform (dict): [current xform we are processing to the relative key names and values for the iterator]
        mp_idx (int): [for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        v_type (int): [the current variation type index]
        func (Callable): [function to change variation name between var, pre_var and post_var]
    """
    
    iter_type = f"Iterator.{mp_idx+1}:"
    if mode:
        iter_type = 'FF:'
    
    VAR: list = []
    for names in apo_prm[1:-1]:
        var_prm_vals: list = []
        for n in [x.lower() for x in names]:
            # If one of the FLAM3 parameter is not in the xform, skip it and set it to ZERO for now.
            n = func(n)
            if xform.get(n) is not None:
                var_prm_vals.append(float(str(xform.get(n))))
            else:
                # If a variation parameter FLAM3 has is not found, set it to ZERO. Print its name to let us know if not inside XML_XF_PRM_EXCEPTION
                if n not in XML_XF_PRM_EXCEPTION:
                    var_prm_vals.append(float(0))
                    print(f"{str(node)}: PARAMETER NOT FOUND: {iter_type} variation: \"{func(var_name_from_dict(VARS_FLAM3_DICT_IDX, v_type))}\": parameter: \"{func(n)}\"")
        VAR.append(typemaker(var_prm_vals))
    return VAR

def v_parametric(app: str, 
                 mode: int, 
                 node: hou.Node, 
                 mp_idx: int, 
                 t_idx: int, 
                 xform: dict, 
                 v_type: int, 
                 v_weight: float, 
                 var_prm: tuple, 
                 apo_prm: tuple
                 ) -> None:
    """
    Args:
        app (str): [What software were used to generate this flame preset]
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        t_idx (int): [current variation number idx to use with: flam3_iterator.sec_varsT, flam3_iterator.sec_varsW]
        xform (dict): [current xform we are processing to the relative key names and values for the iterator]
        v_type (int): [the current variation type index]
        weight (float): [the current variation weight]
        var_prm (tuple): [tuple of FLAM3 node parameteric parameters names: flam3_varsPRM.varsPRM[v_type]]
        apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3_varsPRM_APO.varsPRM[v_type]]
    """
    prx, prx_prm = flam3_prx_mode(mode)
    
    # Exceptions: check if this flame need different parameters names based on detected exception
    apo_prm = prm_name_exceptions(v_type, app, apo_prm)
    
    VAR = v_parametric_var_collect(node, 
                                   mode, 
                                   apo_prm, 
                                   xform, 
                                   mp_idx, 
                                   v_type, 
                                   make_NULL)

    for idx, prm in enumerate(var_prm[1:-1]):
        if mode: node.setParms({f"{prx_prm}{prm[0][:-1]}": VAR[idx]}) # type: ignore
        else: node.setParms({f"{prx_prm}{prm[0]}{str(mp_idx+1)}": VAR[idx]}) # type: ignore

    if mode:
        node.setParms({f"{prx}{flam3_iterator.sec_varsT[t_idx][:-1]}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3_iterator.sec_varsW[t_idx][0][:-1]}": v_weight}) # type: ignore
    else:
        node.setParms({f"{prx}{flam3_iterator.sec_varsT[t_idx]}{str(mp_idx+1)}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3_iterator.sec_varsW[t_idx][0]}{str(mp_idx+1)}": v_weight}) # type: ignore
        

def v_parametric_PRE(app: str, 
                     mode: int, 
                     node: hou.Node, 
                     mp_idx: int, 
                     t_idx: int, 
                     xform: dict, 
                     v_type: int, 
                     v_weight: float, 
                     var_prm: tuple, 
                     apo_prm: tuple
                     ) -> None:
    """
    Args:
        app (str): [What software were used to generate this flame preset]
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        t_idx (int): [current variation number idx to use with: flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW]
        xform (dict): [current xform we are processing to the relative key names and values for the iterator]
        v_type (int): [the current variation type index]
        weight (float): [the current variation weight]
        var_prm (tuple): [tuple of FLAM3 node parameteric parameters names: flam3_varsPRM.varsPRM[v_type]]
        apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3_varsPRM_APO.varsPRM[v_type]]
    """
    prx, prx_prm = flam3_prx_mode(mode)
    
    # Exceptions: check if this flame need different parameters names based on detected exception
    apo_prm = prm_name_exceptions(v_type, app, apo_prm)
    
    VAR = v_parametric_var_collect(node, 
                                   mode, 
                                   apo_prm, 
                                   xform, 
                                   mp_idx, 
                                   v_type, 
                                   make_PRE)
        
    for idx, prm in enumerate(var_prm[1:-1]):
        node.setParms({f"{prx_prm}{prm[0]}{str(mp_idx+1)}": VAR[idx]}) # type: ignore

    # Only on pre variations with parametric so:
    node.setParms({f"{prx}{flam3_iterator.sec_prevarsT[t_idx]}{str(mp_idx+1)}": v_type}) # type: ignore
    node.setParms({f"{prx}{flam3_iterator.sec_prevarsW[1:][t_idx][0]}{str(mp_idx+1)}": v_weight}) # type: ignore 


def v_parametric_POST(app: str, 
                      mode: int, 
                      node: hou.Node, 
                      mp_idx: int, 
                      t_idx: int, 
                      xform: dict, 
                      v_type: int, 
                      v_weight: float, 
                      var_prm: tuple, 
                      apo_prm: tuple
                      ) -> None:
    """
    Args:
        app (str): [What software were used to generate this flame preset]
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        t_idx (int): [current variation number idx to use with: flam3_iterator.sec_postvarsT, flam3_iterator.sec_postvarsW]
        xform (dict): [current xform we are processing to the relative key names and values for the iterator]
        v_type (int): [the current variation type index]
        weight (float): [the current variation weight]
        var_prm (tuple): [tuple of FLAM3 node parameteric parameters names: flam3_varsPRM.varsPRM[v_type]]
        apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3_varsPRM_APO.varsPRM[v_type]]
    """
    prx, prx_prm = flam3_prx_mode(mode)
    
    # Exceptions: check if this flame need different parameters names based on detected exception
    apo_prm = prm_name_exceptions(v_type, app, apo_prm)

    VAR = v_parametric_var_collect(node, 
                                   mode, 
                                   apo_prm, 
                                   xform, 
                                   mp_idx, 
                                   v_type, 
                                   make_POST)
        
    for idx, prm in enumerate(var_prm[1:-1]):
        node.setParms({f"{prx_prm}{prm[0]}{str(mp_idx+1)}": VAR[idx]}) # type: ignore

    # Only on post variation with parametric so:
    node.setParms({f"{prx}{flam3_iterator.sec_postvarsT[t_idx]}{str(mp_idx+1)}": v_type}) # type: ignore
    node.setParms({f"{prx}{flam3_iterator.sec_postvarsW[t_idx][0]}{str(mp_idx+1)}": v_weight}) # type: ignore
    
    
def v_parametric_PRE_FF(app: str, 
                        node: hou.Node, 
                        t_idx: int, 
                        xform: dict, 
                        v_type: int, 
                        v_weight: float, 
                        var_prm: tuple, 
                        apo_prm: tuple
                        ) -> None:
    """
    Args:
        app (str): [What software were used to generate this flame preset]
        node (hou.Node): [Current FLAM3 houdini node]
        t_idx (int): [current variation number idx to use with: flam3_iterator.sec_prevarsT_FF, flam3_iterator.sec_prevarsW_FF]
        xform (dict): [current xform we are processing to the relative key names and values for the iterator]
        v_type (int): [the current variation type index]
        weight (float): [the current variation weight]
        var_prm (tuple): [tuple of FLAM3 node parameteric parameters names: flam3_varsPRM.varsPRM[v_type]]
        apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3_varsPRM_APO.varsPRM[v_type]]
    """
    # Exceptions: check if this flame need different parameters names based on detected exception
    apo_prm = prm_name_exceptions(v_type, app, apo_prm)

    VAR = v_parametric_var_collect(node, 
                                   0, 
                                   apo_prm, 
                                   xform, 
                                   0, 
                                   v_type, 
                                   make_PRE)
        
    for idx, prm in enumerate(var_prm[1:-1]):
        node.setParms({f"{PRX_FF_PRM_POST}_{prm[0][0:-1]}": VAR[idx]}) # type: ignore

    # Only on post variation with parametric so:
    node.setParms({f"{flam3_iterator_FF.sec_prevarsT_FF[t_idx]}": v_type}) # type: ignore
    node.setParms({f"{flam3_iterator_FF.sec_prevarsW_FF[t_idx][0]}": v_weight}) # type: ignore


def v_parametric_POST_FF(app: str, 
                         node: hou.Node, 
                         t_idx: int, 
                         xform: dict, 
                         v_type: int, 
                         v_weight: float, 
                         var_prm: tuple, 
                         apo_prm: tuple
                         ) -> None:
    """
    Args:
        app (str): [What software were used to generate this flame preset]
        node (hou.Node): [Current FLAM3 houdini node]
        t_idx (int): [current variation number idx to use with: flam3_iterator.sec_postvarsT_FF, flam3_iterator.sec_postvarsW_FF]
        xform (dict): [current xform we are processing to the relative key names and values for the iterator]
        v_type (int): [the current variation type index]
        weight (float): [the current variation weight]
        var_prm (tuple): [tuple of FLAM3 node parameteric parameters names: flam3_varsPRM.varsPRM[v_type]]
        apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3_varsPRM_APO.varsPRM[v_type]]
    """
    # Exceptions: check if this flame need different parameters names based on detected exception
    apo_prm = prm_name_exceptions(v_type, app, apo_prm)

    VAR = v_parametric_var_collect(node, 
                                   0, 
                                   apo_prm, 
                                   xform, 
                                   0, 
                                   v_type, 
                                   make_POST)
        
    for idx, prm in enumerate(var_prm[1:-1]):
        node.setParms({f"{PRX_FF_PRM_POST}_{prm[0][0:-1]}": VAR[idx]}) # type: ignore

    # Only on post variation with parametric so:
    node.setParms({f"{flam3_iterator_FF.sec_postvarsT_FF[t_idx]}": v_type}) # type: ignore
    node.setParms({f"{flam3_iterator_FF.sec_postvarsW_FF[t_idx][0]}": v_weight}) # type: ignore


def v_generic(mode: int, 
              node: hou.Node, 
              mp_idx: int, 
              t_idx: int, 
              v_type: int, 
              v_weight: float
              ) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        t_idx (int): [Current variation number idx to use with: flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW]
        v_type (int): [Current variation type index]
        weight (float): [Current variation weight]
    """
    prx, prx_prm = flam3_prx_mode(mode)

    if mode:
        node.setParms({f"{prx}{flam3_iterator.sec_varsT[t_idx][:-1]}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3_iterator.sec_varsW[t_idx][0][:-1]}": v_weight}) # type: ignore
    else:
        node.setParms({f"{prx}{flam3_iterator.sec_varsT[t_idx]}{str(mp_idx+1)}": v_type}) # type: ignore
        node.setParms({f"{prx}{flam3_iterator.sec_varsW[t_idx][0]}{str(mp_idx+1)}":v_weight}) # type: ignore


def v_generic_PRE(mode: int, 
                  node: hou.Node, 
                  mp_idx: int, 
                  t_idx: int, 
                  v_type: int, 
                  v_weight: float
                  ) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        t_idx (int): [Current variation number idx to use with: flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW]
        v_type (int): [Current variation type index]
        weight (float): [Current variation weight]
    """
    prx, prx_prm = flam3_prx_mode(mode)
    node.setParms({f"{prx}{flam3_iterator.sec_prevarsT[t_idx]}{str(mp_idx+1)}": v_type}) # type: ignore
    node.setParms({f"{prx}{flam3_iterator.sec_prevarsW[1:][t_idx][0]}{str(mp_idx+1)}":v_weight}) # type: ignore


def v_generic_POST(mode: int, 
                   node: hou.Node, 
                   mp_idx: int, 
                   t_idx: int, 
                   v_type: int, 
                   v_weight: float
                   ) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        t_idx (int): [Current variation number idx to use with: flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW]
        v_type (int): [Current variation type index]
        weight (float): [Current variation weight]
    """
    prx, prx_prm = flam3_prx_mode(mode)
    node.setParms({f"{prx}{flam3_iterator.sec_postvarsT[t_idx]}{str(mp_idx+1)}": v_type}) # type: ignore
    node.setParms({f"{prx}{flam3_iterator.sec_postvarsW[t_idx][0]}{str(mp_idx+1)}":v_weight}) # type: ignore


def v_generic_PRE_FF(node: hou.Node, 
                     t_idx: int, 
                     v_type: int, 
                     v_weight: float
                     ) -> None:
    """
    Args:
        node (hou.Node): [Current FLAM3 houdini node]
        t_idx (int): [Current variation number idx to use with: flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW]
        v_type (int): [Current variation type index]
        weight (float): [Current variation weight]
    """
    node.setParms({f"{flam3_iterator_FF.sec_prevarsT_FF[t_idx]}": v_type}) # type: ignore
    node.setParms({f"{flam3_iterator_FF.sec_prevarsW_FF[t_idx][0]}":v_weight}) # type: ignore


def v_generic_POST_FF(node: hou.Node, 
                      t_idx: int, 
                      v_type: int, 
                      v_weight: float
                      ) -> None:
    """
    Args:
        node (hou.Node): [Current FLAM3 houdini node]
        t_idx (int): [Current variation number idx to use with: flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW]
        v_type (int): [Current variation type index]
        weight (float): [Current variation weight]
    """
    node.setParms({f"{flam3_iterator_FF.sec_postvarsT_FF[t_idx]}": v_type}) # type: ignore
    node.setParms({f"{flam3_iterator_FF.sec_postvarsW_FF[t_idx][0]}":v_weight}) # type: ignore


def v_pre_blur(mode: int, 
               node: hou.Node, 
               mp_idx: int, 
               pb_weights: tuple
               ) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        pb_weights (tuple): [all iterators pre_blur weight values]
    """
    prx, prx_prm = flam3_prx_mode(mode)
    if mode: pass
    else:
        if pb_weights[mp_idx]:
            node.setParms({f"{prx}{flam3_iterator_prm_names.prevar_weight_blur}_{str(mp_idx+1)}": pb_weights[mp_idx]}) # type: ignore

# To be used only with PRE and POST variations
def check_negative_weight(self: hou.Node, w: float, v_type_name: str) -> float:
    if w < 0:
        print(f"{str(self)} warning:\n{v_type_name.upper()} variation weight value: {w}\nNegative weight not allowed in PRE or POST vars.\nUsing its absolute value instead: {abs(w)}\n")
        return abs(w)
    else: return w
def apo_set_iterator(mode: int, 
                     node: hou.Node, 
                     apo_data: apo_flame_iter_data, 
                     preset_id: int, 
                     exclude_keys: tuple
                     ) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        apo_data (apo_flame_iter_data): [Apophysis XML data collection from: class[apo_flame_iter_data]]
    """    
    # What software were used to generate this flame preset
    app = apo_data.apo_version[preset_id]

    xforms = ()
    MAX_VARS_MODE = 0
    if mode:
        MAX_VARS_MODE = MAX_FF_VARS
        xforms = apo_data.finalxform
    else:
        MAX_VARS_MODE = MAX_ITER_VARS
        xforms = apo_data.xforms

    iterator_names = flam3_iterator_prm_names()
    prx, prx_prm = flam3_prx_mode(mode)

    var_prm: tuple = flam3_varsPRM.varsPRM
    apo_prm: tuple = flam3_varsPRM_APO.varsPRM
    
    vars_keys = get_xforms_var_keys(xforms, VARS_FLAM3_DICT_IDX.keys(), exclude_keys)
    assert vars_keys is not None
    vars_keys_pre = get_xforms_var_keys(xforms, make_PRE(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)
    assert vars_keys_pre is not None
    vars_keys_post = get_xforms_var_keys(xforms, make_POST(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)
    assert vars_keys_post is not None

    # Set variations ( iterator and FF )
    for mp_idx, xform in enumerate(xforms):
        for t_idx, key_name in enumerate(vars_keys[mp_idx][:MAX_VARS_MODE]):
            v_type = apo_get_idx_by_key(key_name)
            if v_type is not None:
                v_weight = float(xform.get(key_name))
                if apo_prm[v_type][-1]:
                    v_parametric(app, 
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
                    v_generic(mode, node, mp_idx, t_idx, v_type, v_weight)
            else:
                # if this variation is not found, set it to Linear and its weight to ZERO
                v_generic(mode, node, mp_idx, t_idx, 0, 0)
        v_pre_blur(mode, node, mp_idx, apo_data.pre_blur)
                
        if mode:
            # Set finalxform name first if any
            if apo_data.finalxform_name[0]:
                node.setParms({f"{prx}note": apo_data.finalxform_name[0]}) # type: ignore
            # FF PRE vars ( only the first one in "vars_keys_pre[mp_idx]" will be kept )
            if vars_keys_pre[mp_idx]: # type: ignore
                for t_idx, key_name in enumerate(vars_keys_pre[mp_idx][:MAX_FF_VARS_PRE]):
                    v_type = apo_get_idx_by_key(make_VAR(key_name)) # type: ignore
                    if v_type is not None:
                        w = float(xform.get(key_name))
                        v_weight = check_negative_weight(node, w, make_PRE(var_prm[v_type][0])) # type: ignore
                        if apo_prm[v_type][-1]:
                            v_parametric_PRE_FF(app, 
                                                node, 
                                                t_idx, 
                                                xform, 
                                                v_type, 
                                                v_weight, 
                                                var_prm[v_type], 
                                                apo_prm[v_type]
                                                )
                        else:
                            v_generic_PRE_FF(node, t_idx, v_type, v_weight)
            # FF POST vars ( only the first two in "vars_keys_post[mp_idx]" will be kept )
            if vars_keys_post[mp_idx]: # type: ignore
                for t_idx, key_name in enumerate(vars_keys_post[mp_idx][:MAX_FF_VARS_POST]):
                    v_type = apo_get_idx_by_key(make_VAR(key_name)) # type: ignore
                    if v_type is not None:
                        w = float(xform.get(key_name))
                        v_weight = check_negative_weight(node, w, make_POST(var_prm[v_type][0])) # type: ignore
                        if apo_prm[v_type][-1]:
                            v_parametric_POST_FF(app, 
                                                 node, 
                                                 t_idx, 
                                                 xform, 
                                                 v_type, 
                                                 v_weight, 
                                                 var_prm[v_type], 
                                                 apo_prm[v_type]
                                                 )
                        else:
                            v_generic_POST_FF(node, t_idx, v_type, v_weight)
                            
        else:
            # PRE vars in this iterator ( only the first two in "vars_keys_pre[mp_idx]" will be kept )
            if vars_keys_pre[mp_idx]: # type: ignore
                for t_idx, key_name in enumerate(vars_keys_pre[mp_idx][:MAX_ITER_VARS_PRE]):
                    v_type = apo_get_idx_by_key(make_VAR(key_name)) # type: ignore
                    if v_type is not None:
                        w = float(xform.get(key_name))
                        v_weight = check_negative_weight(node, w, make_PRE(var_prm[v_type][0])) # type: ignore
                        if apo_prm[v_type][-1]:
                            v_parametric_PRE(app, 
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
                            v_generic_PRE(mode, node, mp_idx, t_idx, v_type, v_weight)
                            
            # POST vars in this iterator ( only the first one in "vars_keys_post[mp_idx]" will be kept )
            if vars_keys_post[mp_idx]: # type: ignore
                for t_idx, key_name in enumerate(vars_keys_post[mp_idx][:MAX_ITER_VARS_POST]):
                    v_type = apo_get_idx_by_key(make_VAR(key_name)) # type: ignore
                    if v_type is not None:
                        w = float(xform.get(key_name))
                        v_weight = check_negative_weight(node, w, make_POST(var_prm[v_type][0])) # type: ignore
                        if apo_prm[v_type][-1]:
                            v_parametric_POST(app, 
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
                            v_generic_POST(mode, node, mp_idx, t_idx, v_type, v_weight)
                            
            # Activate iterator, just in case...
            node.setParms({f"{iterator_names.main_vactive}_{str(mp_idx+1)}": 1}) # type: ignore
            # Set the rest of the iterators
            if node.parm(USE_FRACTORIUM_COLOR_SPEED).eval():
                apo_set_data(mode, node, prx, apo_data.color_speed, iterator_names.shader_speed, mp_idx)
            else: 
                apo_set_data(mode, node, prx, apo_data.symmetry, iterator_names.shader_speed, mp_idx)
            apo_set_data(mode, node, prx, apo_data.xf_name, iterator_names.main_note, mp_idx)
            apo_set_data(mode, node, prx, apo_data.weight, iterator_names.main_weight, mp_idx)
            apo_set_data(mode, node, prx, apo_data.xaos, iterator_names.xaos, mp_idx)
            apo_set_data(mode, node, prx, apo_data.color, iterator_names.shader_color, mp_idx)       
            apo_set_data(mode, node, prx, apo_data.opacity, iterator_names.shader_alpha, mp_idx)
        
        # Affine ( PRE and POST) for iterator and FF
        apo_set_affine(mode, node, prx, apo_data, iterator_names, mp_idx)


def iter_on_load_callback(self):
    iter_on_load = self.parm("iternumonload").eval()
    self.setParms({SYS_ITERATIONS: iter_on_load})
    
def use_iter_on_load_callback(self):
    useiteronload = self.parm("useiteronload").eval()
    if useiteronload:
        iternumonload = self.parm("iternumonload").eval()
        iter = self.parm(SYS_ITERATIONS).eval()
        if iter != iternumonload:
            self.setParms({SYS_ITERATIONS: iternumonload})


def get_preset_name_iternum(preset_name: str) -> Union[int, None]:
    splt = preset_name.split("::")
    if len(splt) > 1:
        try:
            return int(splt[-1])
        except:
            return None
    else:
        return None


def set_iter_on_load(self: hou.Node, preset_id: int) -> int:
    iter_on_load = self.parm("iternumonload").eval()
    use_iter_on_load = self.parm("useiteronload").eval()
    preset_name = self.parm(IN_PRESETS).menuLabels()[preset_id]
    iter_on_load_preset = get_preset_name_iternum(preset_name)
    if iter_on_load_preset is not None:
        self.setParms({"iternumonload": iter_on_load_preset}) # type: ignore
        self.setParms({"useiteronload": 0}) # type: ignore
        iter_on_load = iter_on_load_preset
    else:
        if not use_iter_on_load:
            self.setParms({"iternumonload": ITER_LOAD_DEFAULT}) # type: ignore
            iter_on_load = ITER_LOAD_DEFAULT
    return iter_on_load    


'''
    The following function is just a shortcut to set and load
    a new preset from the IN Tab IN_PRESETS parameter,
    It works like a hook to then set and evaluate it from the SYS Tab.
'''
def sys_apo_to_flam3(self: hou.Node) -> None:

    xml = self.parm(IN_PATH).evalAsString()

    if apo_flame(self, xml).isvalidtree:
        
        preset_id = self.parm(SYS_IN_PRESETS).eval()
        self.setParms({IN_PRESETS: preset_id}) # type: ignore
        apo_to_flam3(self)
'''
    The following is the actual load preset/flame function to be used.
'''
def apo_to_flam3(self: hou.Node) -> None:

    xml = self.parm(IN_PATH).evalAsString()

    if apo_flame(self, xml).isvalidtree:
        
        self.setParms({IN_ISVALID_FILE: 1}) #type: ignore
        
        preset_id = int(self.parm(IN_PRESETS).eval())
        iter_on_load = set_iter_on_load(self, preset_id)
        reset_SYS(self, 1, iter_on_load, 0)
        reset_MB(self)
        reset_PREFS(self)

        apo_data = apo_flame_iter_data(self, xml, preset_id)
        if min(apo_data.opacity) == 0.0:
            self.setParms({SYS_RIP: 1}) # type: ignore
        # iterators
        self.setParms({FLAM3_ITERATORS_COUNT: 0}) # type: ignore
        for p in self.parms():
            p.deleteAllKeyframes()
        self.setParms({FLAM3_ITERATORS_COUNT:  len(apo_data.xforms)}) # type: ignore
        
        # get keys to exclude
        exclude_keys = XML_XF_KEY_EXCLUDE
        if self.parm(REMAP_PRE_GAUSSIAN_BLUR).eval():
            exclude_keys = XML_XF_KEY_EXCLUDE_PGB

        apo_set_iterator(0, self, apo_data, preset_id, exclude_keys)
        
        # if FF
        if apo_data.finalxform is not None:
            reset_FF(self)
            self.setParms({SYS_DO_FF: 1}) # type: ignore
            apo_set_iterator(1, self, apo_data, preset_id, exclude_keys)
        else:
            reset_FF(self)
            self.setParms({SYS_DO_FF: 0}) # type: ignore
        
        # if MB
        if apo_data.mb_flam3h_fps is not False:
            self.setParms({OUT_MB_DO: 1}) # type: ignore
            self.setParms({OUT_MB_FPS: apo_data.mb_flam3h_fps}) # type: ignore
            self.setParms({OUT_MB_SAMPLES: apo_data.mb_flam3h_samples}) # type: ignore
            self.setParms({OUT_MB_SHUTTER: apo_data.mb_flam3h_shutter}) # type: ignore
        else:
            reset_MB(self)
            
        
        # if CP HSV vals
        if apo_data.palette_flam3h_hsv is not False:
            self.setParms({RAMP_HSV_VAL_NAME: apo_data.palette_flam3h_hsv}) # type: ignore
        else:
        # CP HSV default vals
            self.setParms({RAMP_HSV_VAL_NAME: hou.Vector3((1.0, 1.0, 1.0))}) # type: ignore
            
        # self.setParms({PALETTE_LIB_PATH: ""})
        # self.setParms({PALETTE_PRESETS: "-1"})
        ramp_parm = self.parm(RAMP_SRC_NAME)
        ramp_parm.deleteAllKeyframes()
        # Set XML palette data
        ramp_parm.set(apo_data.palette[0])
        palette_cp(self)
        palette_hsv(self)
        # if "copy render properties on Load" is checked
        if self.parm(IN_COPY_RENDER_PROPERTIES_ON_LOAD).eval():
            apo_copy_render_stats_msg(self)
        # Set density back to default on load
        self.setParms({SYS_PT_COUNT: POINT_COUNT_LOAD_DEFAULT}) # type: ignore
        #Updated flame stats 
        self.setParms({MSG_FLAMESTATS: apo_load_stats_msg(self, preset_id, apo_data)}) # type: ignore
        self.setParms({MSG_FLAMERENDER: apo_load_render_stats_msg(self, preset_id, apo_data)}) # type: ignore
        # Updated SYS inpresets parameter
        self.setParms({SYS_IN_PRESETS: self.parm(IN_PRESETS).eval()}) # type: ignore
    else:
        if os.path.isfile(xml) and os.path.getsize(xml)>0:
            self.setParms({MSG_FLAMESTATS: "Please load a valid *.flame file."}) # type: ignore
            self.setParms({MSG_FLAMERENDER: ""}) # type: ignore
            # The following do not work, not sure why
            self.setParms({MSG_DESCRIPTIVE_PRM: ""}) # type: ignore
        else:
            self.setParms({MSG_FLAMESTATS: ""}) # type: ignore
            self.setParms({MSG_FLAMERENDER: ""}) # type: ignore
            # The following do not work, not sure why
            self.setParms({MSG_DESCRIPTIVE_PRM: ""}) # type: ignore


def apo_join_vars_grp(groups: list) -> str:
    vars = []
    for id, grp in enumerate(groups):
        if id < len(groups)-1:
            vars.append(", ".join(grp) + "\n")
        else:
            vars.append(", ".join(grp))
    return ''.join(vars)

def out_vars_flatten_unique_sorted(VARS_list: Union[list[str], list[list[str]]], func: Callable) -> list[str]:
    flatten = [item for sublist in VARS_list for item in sublist]
    result = []
    [result.append(x) for x in flatten if x not in result]
    sort = sorted(result, key=lambda var: var)
    return [func(x) for x in sort]


def apo_load_stats_msg(self: hou.Node, preset_id: int, apo_data: apo_flame_iter_data) -> str:
    
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
    sw = f"Software: {apo_data.apo_version[preset_id]}"
    name = f"NAME: {apo_data.name[preset_id]}"
    iter_count = f"iterators count: {str(len(apo_data.xforms))}"
    post = f"post affine: {post_bool_msg}"
    opacity = f"opacity: {opacity_bool_msg}"
    xaos = f"xaos: {xaos_bool_msg}"
    if flam3h_mb_bool:
        mb = f"Motion blur{nnl}"
    else:
        mb = nnl
    
    ff_msg = ""
    if ff_bool:
        ff_msg = f"FF: YES\nFF post affine: {ff_post_bool_msg}"
    else:
        ff_msg = f"FF: NO"
        
    if palette_bool:
        if apo_data.palette_flam3h_hsv is not False:
            # custom to FLAM3H only
            palette_count_format = f"Palette count: {apo_data.palette[1]}, format: {apo_data.palette[2]} ( -> HSV )"
        else:
            palette_count_format = f"Palette count: {apo_data.palette[1]}, format: {apo_data.palette[2]}"
    else:
        palette_count_format = f"Palette not found."
    
    exclude_keys = XML_XF_KEY_EXCLUDE
    if self.parm(REMAP_PRE_GAUSSIAN_BLUR).eval():
        exclude_keys = XML_XF_KEY_EXCLUDE_PGB
    vars_keys = get_xforms_var_keys(apo_data.xforms, VARS_FLAM3_DICT_IDX.keys(), exclude_keys) 
    vars_keys_PRE = get_xforms_var_keys(apo_data.xforms, make_PRE(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)
    vars_keys_POST = get_xforms_var_keys(apo_data.xforms, make_POST(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)

    # FF
    vars_keys_FF = vars_keys_PRE_FF = vars_keys_POST_FF = []
    if ff_bool:
        vars_keys_FF = get_xforms_var_keys(apo_data.finalxform, VARS_FLAM3_DICT_IDX.keys(), exclude_keys)
        vars_keys_PRE_FF = get_xforms_var_keys(apo_data.finalxform, make_PRE(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)
        vars_keys_POST_FF = get_xforms_var_keys(apo_data.finalxform, make_POST(VARS_FLAM3_DICT_IDX.keys()), exclude_keys)
    vars_all = vars_keys_PRE + vars_keys + vars_keys_POST +  vars_keys_PRE_FF + vars_keys_FF + vars_keys_POST_FF # type: ignore
    if pb_bool:
        vars_all += [["pre_blur"]] # + vars_keys_PRE + vars_keys_POST
    result_sorted = out_vars_flatten_unique_sorted(vars_all, make_NULL) # type: ignore
    
    n = 5
    var_used_heading = "Variations used:"
    result_grp = [result_sorted[i:i+n] for i in range(0, len(result_sorted), n)]  
    vars_used_msg = f"{var_used_heading} {int(len(result_sorted))}\n{apo_join_vars_grp(result_grp)}"
    
    # Build and set descriptive parameter msg
    preset_name = self.parm(IN_PRESETS).menuLabels()[preset_id]
    descriptive_prm = ( f"sw: {apo_data.apo_version[preset_id]}\n",
                        f"{preset_name}", )
    self.setParms({MSG_DESCRIPTIVE_PRM: "".join(descriptive_prm)}) # type: ignore

    # Build missing:
    vars_keys_from_fractorium = get_xforms_var_keys(apo_data.xforms, VARS_FRACTORIUM_DICT, exclude_keys)
    vars_keys_from_fractorium_pre = get_xforms_var_keys_PP(apo_data.xforms, VARS_FRACTORIUM_DICT_PRE, V_PRX_PRE, exclude_keys)
    vars_keys_from_fractorium_post = get_xforms_var_keys_PP(apo_data.xforms, VARS_FRACTORIUM_DICT_POST, V_PRX_POST, exclude_keys)
    
    vars_keys_from_fractorium_FF = vars_keys_from_fractorium_pre_FF = vars_keys_from_fractorium_post_FF = []
    if ff_bool:
        vars_keys_from_fractorium_FF = get_xforms_var_keys(apo_data.finalxform, VARS_FRACTORIUM_DICT, exclude_keys)
        vars_keys_from_fractorium_pre_FF = get_xforms_var_keys_PP(apo_data.finalxform, VARS_FRACTORIUM_DICT_POST, V_PRX_PRE, exclude_keys)
        vars_keys_from_fractorium_post_FF = get_xforms_var_keys_PP(apo_data.finalxform, VARS_FRACTORIUM_DICT_POST, V_PRX_POST, exclude_keys)
    vars_keys_from_fractorium_all = vars_keys_from_fractorium + vars_keys_from_fractorium_pre + vars_keys_from_fractorium_post + vars_keys_from_fractorium_pre_FF + vars_keys_from_fractorium_FF + vars_keys_from_fractorium_post_FF # type: ignore
    result_sorted_fractorium = out_vars_flatten_unique_sorted(vars_keys_from_fractorium_all, make_NULL)
    
    # Compare and keep and build missing vars msg
    vars_missing = [x for x in result_sorted_fractorium if x not in result_sorted]
    result_grp_fractorium = [vars_missing[i:i+n] for i in range(0, len(vars_missing), n)]  
    vars_missing_msg = ""
    if vars_missing:
        vars_missing_msg = f"{nnl}MISSING:\n{apo_join_vars_grp(result_grp_fractorium)}"
    # Check if the loaded Flame file is locked.
    in_path = self.parm(IN_PATH).evalAsString()
    in_path_checked = out_check_outpath(self, in_path, OUT_FLAM3_FILE_EXT, 'Flame')
    if os.path.split(str(in_path_checked))[-1].startswith(FLAM3_LIB_LOCK):
        flame_lib_locked = f"\nflame lib file: LOCKED"
    else: flame_lib_locked = ''
    # build full stats msg
    build = ( sw, flame_lib_locked, nnl,
              name, nl,
              palette_count_format, nl,
              mb,
              iter_count, nl,
              post, nl,
              opacity, nl,
              xaos, nl,
              ff_msg, nnl,
              vars_used_msg,
              vars_missing_msg )
    build_stats_msg = "".join(build)
    
    return build_stats_msg


def apo_load_render_stats_msg(self: hou.Node, preset_id: int, apo_data: apo_flame_iter_data) -> str:
    
    # spacers
    nl = "\n"
    nnl = "\n\n"
    na = 'n/a'
    
    size = f'Size: {na}'
    if apo_data.out_size[preset_id]:
        size = f"Size: {apo_data.out_size[preset_id]}"
        
    center = f'Center: {na}'
    if apo_data.out_center[preset_id]:
        center = f"Center: {apo_data.out_center[preset_id]}"
        
    rotate = f'Rotate: {na}'
    if apo_data.out_rotate[preset_id]:
        rotate = f"Rotate: {apo_data.out_rotate[preset_id]}"

    scale = f'Scale: {na}'
    if apo_data.out_scale[preset_id]:
        scale = f"Scale: {apo_data.out_scale[preset_id]}"
    
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
    
    build = (size, nl,
             center, nl,
             rotate, nl,
             scale, nl,
             quality, nl,
             brightness, nl,
             gamma, nl,
             highlight, nl,
             K2, nl,
             vibrancy
            )
    
    build_render_stats_msg = "".join(build)
    return build_render_stats_msg


def apo_copy_render_stats_msg(self: hou.Node) -> None:
    
    xml = self.parm(IN_PATH).evalAsString()
    preset_id = int(self.parm(IN_PRESETS).eval())
    f3r = apo_flame_iter_data(self, xml, preset_id)
    if f3r.isvalidtree:
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE): hou.Vector2((int(f3r.out_size[preset_id].split(" ")[0]), int(f3r.out_size[preset_id].split(" ")[1])))}) # type: ignore
        except:
            pass
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER): hou.Vector2((float(f3r.out_center[preset_id].split(" ")[0]), float(f3r.out_center[preset_id].split(" ")[1])))}) # type: ignore
        except:
            pass
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE): int(f3r.out_rotate[preset_id])}) # type: ignore
        except:
            pass
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE): int(f3r.out_scale[preset_id])}) # type: ignore
        except:
            pass
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY): int(f3r.out_quality[preset_id])}) # type: ignore
        except:
            pass
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS): float(f3r.out_brightness[preset_id])}) # type: ignore
        except:
            pass
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA): float(f3r.out_gamma[preset_id])}) # type: ignore
        except:
            pass
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER): float(f3r.out_highlight_power[preset_id])}) # type: ignore
        except:
            pass
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2): float(f3r._out_logscale_k2[preset_id])}) # type: ignore
        except:
            pass
        try: self.setParms({OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY): float(f3r.out_vibrancy[preset_id])}) # type: ignore
        except:
            pass
        self.setParms({"outedit": 1}) # type: ignore
    else:
        pass


def flam3_about_msg(self):
    
    nl = "\n"
    nnl = "\n\n"

    flam3_houdini_version = f"Version: {FLAM3HOUDINI_VERSION}"
    Implementation_years = "2020/2023"
    Implementation_build = f"Author: Alessandro Nardini ( Italy )\nCode language: CVEX H19.x, Python 3.9.10\n{flam3_houdini_version}\n{Implementation_years}"
    
    code_references = """Code references:
flam3 :: (GPL v2)
Apophysis :: (GPL)
Fractorium :: (GPL v3)"""
    
    h_version = '.'.join(str(x) for x in hou.applicationVersion())
    Houdini_version = f"Host:\nSideFX Houdini {h_version}"
    Python_version = f"Python: {python_version()}"
    license_type = str(hou.licenseCategory()).split(".")[-1]
    Houdini_license = f"License: {license_type}"
    Platform = f"Platform: {hou.applicationPlatformInfo()}"
    PC_name = f"Machine name: {hou.machineName()}"
    User = f"User: {hou.userName()}"
    
    example_flames = """example Flames:
C-91, Gabor Timar, Golubaja, Pillemaster,
Plangkye, Tatasz, Triptychaos, TyrantWave, Zy0rg,
Seph, Lucy, b33rheart, Neonrauschen"""
    
    build = (Implementation_build, nnl,
             code_references, nnl,
             example_flames, nnl,
             Houdini_version, nl,
             Houdini_license, nl,
             Python_version, nl,
             Platform, nl,
             PC_name, nl,
             User
             )
    
    build_about_msg = "".join(build)

    self.setParms({MSG_FLAM3ABOUT: build_about_msg})


def flam3_about_plugins_msg(self):
    
    vars_sorted = sorted(VARS_FLAM3_DICT_IDX.keys()) 
    n = 6
    vars_sorted_grp = [vars_sorted[i:i+n] for i in range(0, len(vars_sorted), n)] 
    _vars = []
    for idx, grp in enumerate(vars_sorted_grp):
        if idx == (len(vars_sorted_grp)-1):
            _vars.append(", ".join(grp))
        else:
            _vars.append(", ".join(grp) + "\n")
    vars_txt = "".join(_vars)
    
    self.setParms({MSG_FLAM3PLUGINS: vars_txt})


# SAVE XML FILES start here

class _out_utils():

    def __init__(self, node: hou.Node) -> None:
        self._node = node
        self._prm_names = flam3_iterator_prm_names()
        self._flam3_iterator = flam3_iterator()
        self._flam3_iterator_FF = flam3_iterator_FF()
        self._flam3_do_FF = self._node.parm(SYS_DO_FF).eval()
        self._iter_count = self._node.parm(FLAM3_ITERATORS_COUNT).evalAsInt()
        self._palette = self._node.parm(RAMP_SRC_NAME).evalAsRamp()
        self._palette_hsv_do = self._node.parm(OUT_HSV_PALETTE_DO).eval()
        if self._palette_hsv_do:
            # Update hsv ramp before storing it.
            palette_cp(self._node)
            palette_hsv(self._node)
            self._palette = self._node.parm(RAMP_HSV_NAME).evalAsRamp()
        self._xm = self._node.parm(XAOS_MODE).eval()
        # custom to FLAM3H only
        self._flam3h_mb_do = self._node.parm(OUT_MB_DO).eval()
    
    @staticmethod
    def affine_rot(affine: list[Union[tuple[str], list[str]]], angleDeg: float) -> list[Union[list[str], tuple[str]]]:
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
    def out_round_floats(VAL_LIST: Union[list[list[str]], tuple[list]]) -> Union[list[str], list[list[str]], tuple[str]]:
        """remove floating Zero if it is an integer value ( ex: from '1.0' to '1' )

        Args:
            VAL_LIST (list[list[str]]): A list of list[str] of values to rounds

        Returns:
            list[list[str]]: A list of list[str] with the rounded values if any
        """    
        v_ROUND = []
        for item in VAL_LIST:
            collect = []
            for i in item:
                if float(i).is_integer():
                    collect.append(str(int(float(i))))
                else:
                    collect.append(str(round(float(i), ROUND_DECIMAL_COUNT)))
            v_ROUND.append(collect)
        return v_ROUND

    @staticmethod
    def xaos_cleanup(xaos: Union[list[str], list[list[str]], tuple[str]]) -> list[list[str]]:
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
    def xaos_collect(node: hou.Node, iter_count: int, prm: str) -> list[list[str]]:
        """Collect all xaos command string weights.

        Args:
            node (hou.Node): FLAM3H node
            iter_count (int): Iterator's count
            prm (str): xaos varnote parameter

        Returns:
            list[list[str]]: A list of xaos list[str] of values
        """        
        val = []
        for iter in range(iter_count):
            iter_xaos = node.parm(f"{prm}_{iter+1}").eval()
            if iter_xaos:
                strip = iter_xaos.split(':')
                if strip[0].lower().strip() == 'xaos':
                    try:
                        build_strip = [x.strip() for x in strip[1:iter_count+1] if x]
                        # The following is only used to check if any of the xaos weights is not a legit number.
                        # If not it will raise an exception and the entire xaos weight string for this iterator will be filled with a value of '1'
                        build_f = [float(x.strip()) for x in build_strip]
                        val.append(build_strip)
                    except:
                        val.append([])
                else:
                    val.append([])
            else:
                val.append([])
        return val

    @staticmethod
    def xaos_collect_vactive(node: hou.Node, fill: list[np.array], prm: str) -> list[list[str]]:
        """Check for any NO-active iterators and account for those.

        Args:
            node (hou.Node): FLAM3H node
            fill (list[np.array]): List of [np.array] representing all xaos weights.
            prm (str): iterator vactive parameter.

        Returns:
            list[list[str]]: return a list of list[str] with the NO-active iterators taken into consideration.
        """    
        xaos_no_vactive = []
        for x in fill:
            collect = []
            for idx, item in enumerate(x):
                if node.parm(f"{prm}_{idx+1}").eval():
                    collect.append(str(item))
                else:
                    continue
            if collect:
                xaos_no_vactive.append(collect)
            else:
                xaos_no_vactive.append([])
        return xaos_no_vactive

    def out_xf_xaos_to(self) -> tuple[str]:
        """Export in a list[str] the xaos TO values to write out
        Returns:
            tuple[str]: the xaos TO values to write out.
        """
        val = self.xaos_collect(self._node, self._iter_count, self._prm_names.xaos)
        fill = [np.pad(item, (0,self._iter_count-len(item)), 'constant', constant_values=(str(int(1)))) for item in val]
        xaos_vactive = self.xaos_collect_vactive(self._node, fill, self._prm_names.main_vactive)
        return tuple([" ".join(x) for x in self.xaos_cleanup(self.out_round_floats(xaos_vactive))])

    def out_xf_xaos_from(self, mode=0) -> tuple[str]:
        """Export in a list[str] the xaos FROM values to write out
        Args:
            mode (int, optional): mode=1 is for writing out flame file while the default mode=0 is for converting between xaos modes only
        Returns:
            tuple[str]: the xaos FROM values transposed into xaos TO values to write out.
        """
        val = self.xaos_collect(self._node, self._iter_count, self._prm_names.xaos)
        fill = [np.pad(item, (0,self._iter_count-len(item)), 'constant', constant_values=(str(int(1)))) for item in val]
        t = np.transpose(np.resize(fill, (self._iter_count, self._iter_count)))
        if mode:
            xaos_vactive = self.xaos_collect_vactive(self._node, t, self._prm_names.main_vactive)
            return tuple([" ".join(x) for x in self.xaos_cleanup(self.out_round_floats(xaos_vactive))])
        else:
            return tuple([" ".join(x) for x in self.xaos_cleanup(self.out_round_floats(t))])


    @property
    def node(self):
        return self._node

    @property
    def prm_name(self):
        return self._prm_names
    
    @property
    def flam3_iterator(self):
        return self._flam3_iterator
    
    @property
    def flam3_do_FF(self):
        return self._flam3_do_FF

    @property
    def iter_count(self):
        return self._iter_count

    @property
    def palette(self):
        return self._palette
    
    @property
    def palette_hsv_do(self):
        return self._palette_hsv_do
    
    # custom to FLAM3H only
    
    @property
    def flam3h_mb_do(self):
        return self._flam3h_mb_do
    

    def __out_flame_data(self, prm_name='') -> str:
        if prm_name:
            prm_type = False
            try:
                prm = self._node.parmTuple(prm_name)
                prm_type = True
            except:
                prm = self._node.parm(prm_name)
            if prm_type:
                return ' '.join([str(out_round_float(x.eval())) for x in prm])
            else:
                if type(prm) is not str:
                    return str(self._node.parm(prm_name).eval())
                else:
                    return out_round_float(self._node.parm(prm_name).eval())
        else:
            print(f"{str(self.node)}: parameter name not found. Please pass in a valid FLAM3H parameter name.")
            return ''


    def __out_flame_name(self, prm_name=OUT_XML_RENDER_HOUDINI_DICT.get(XML_XF_NAME)) -> str:
        
        # If the name field is empty, build a name based on current date/time
        flame_name = self._node.parm(prm_name).eval()
        autoadd = self._node.parm(OUT_AUTO_ADD_ITER_NUM).evalAsInt()
        
        # Lets make some name checks first
        splt = ':'
        div = '::'
        rp = flame_name.split(splt)
        rp[:] = [item for item in rp if item]
        # if the filename start with either a ':' or '::' followed by a valid integer
        # lets give it a default name
        if (flame_name[0:1] == splt or flame_name[0:2] == div) and isinstance(int(rp[-1]), int):
            
            now = datetime.now()
            flame_name = now.strftime("Flame_%b-%d-%Y_%H%M%S")
            iter_num = self._node.parm(SYS_ITERATIONS).evalAsInt()
            return out_auto_add_iter_num(iter_num, flame_name, autoadd)
        # else if the filename end with either a ':' or '::' preceded by a valid integer
        # lets give it a default name
        elif (flame_name[-1:] == splt or flame_name[-2:] == div) and isinstance(int(rp[0]), int):
            
            now = datetime.now()
            flame_name = now.strftime("Flame_%b-%d-%Y_%H%M%S")
            iter_num = self._node.parm(SYS_ITERATIONS).evalAsInt()
            return out_auto_add_iter_num(iter_num, flame_name, autoadd)
        else:
            
            if not flame_name:
                
                print("AAAAAA")
                now = datetime.now()
                flame_name = now.strftime("Flame_%b-%d-%Y_%H%M%S")
                iter_num = self._node.parm(SYS_ITERATIONS).evalAsInt()
                return out_auto_add_iter_num(iter_num, flame_name, autoadd)
            else:
                
                # otherwise get that name and use it
                return flame_name


    def __out_xf_data(self, prm_name: str) -> tuple[str]:
        val = []
        for iter in range(self._iter_count):
            val.append(str(out_round_float(self._node.parm(f"{prm_name}_{iter+1}").eval())))
        return tuple(val)


    def __out_xf_name(self) -> list[str]:
        val = []
        for iter in range(self._iter_count):
            val.append(self._node.parm(f"{self._prm_names.main_note}_{iter+1}").eval())
        return val
    
    def __out_finalxf_name(self) -> list[str]:
        return self._node.parm(f"{PRX_FF_PRM}{self._prm_names.main_note}").eval()

    
    def __out_xf_pre_blur(self) -> list[str]:
        val = []
        for iter in range(self._iter_count):
            value = self._node.parm(f"{self._prm_names.prevar_weight_blur}_{iter+1}").eval()
            if value > 0.0:
                val.append(str(self._node.parm(f"{self._prm_names.prevar_weight_blur}_{iter+1}").eval()))
            else:
                val.append('')
        return val


    def __out_xf_xaos(self) -> tuple[str]:
        if self._xm:
            return self.out_xf_xaos_from(1)
        else:
            return self.out_xf_xaos_to()


    def __out_xf_preaffine(self) -> list[str]:
        val = []
        for iter in range(self._iter_count):
            collect = []
            for prm in self._flam3_iterator.sec_preAffine[:-1]:
                collect.append(self._node.parmTuple(f"{prm[0]}{iter+1}").eval())
            angleDeg = self._node.parm(f"{self._flam3_iterator.sec_preAffine[-1][0]}{iter+1}").eval()
            flatten = [item for sublist in self.affine_rot(collect, angleDeg) for item in sublist]
            val.append([str(x) for x in flatten])
        return [" ".join(x) for x in self.out_round_floats(val)]
    
    
    def __out_xf_postaffine(self) -> list[str]:
        val = []
        for iter in range(self._iter_count):
            if self._node.parm(f"{self._prm_names.postaffine_do}_{iter+1}").eval():
                collect = []
                for prm in self._flam3_iterator.sec_postAffine[1:-1]:
                    collect.append(self._node.parmTuple(f"{prm[0]}{iter+1}").eval())
                angleDeg = self._node.parm(f"{self._flam3_iterator.sec_postAffine[-1][0]}{iter+1}").eval()
                flatten = [item for sublist in self.affine_rot(collect, angleDeg) for item in sublist]
                val.append([str(x) for x in flatten])
            else:
                val.append([])
        return [" ".join(x) for x in self.out_round_floats(val)]
    
    
    def __out_palette_hex(self) -> str:
        POSs = list(iter_islice(iter_count(0, 1.0/(int(PALETTE_COUNT_256)-1)), int(PALETTE_COUNT_256)))
        HEXs = []
        for p in POSs:
            HEXs.append(rgb_to_hex(tuple(self._palette.lookup(p))))
        n = 8
        hex_grp = [HEXs[i:i+n] for i in range(0, len(HEXs), n)]  
        hex_join = []
        for grp in hex_grp:
            # 6 time \s
            hex_join.append("      " + "".join(grp) + "\n")
        return "\n" + "".join(hex_join) + "    " # 4 times \s


    def __out_finalxf_preaffine(self) -> str:
        collect = []
        for prm in self._flam3_iterator_FF.sec_preAffine_FF[:-1]:
            collect.append(self._node.parmTuple(f"{prm[0]}").eval())
        angleDeg = self._node.parm(f"{self._flam3_iterator_FF.sec_preAffine_FF[-1][0]}").eval()
        if angleDeg != 0.0:
            affine = self.out_round_floats(self.affine_rot(collect, angleDeg)) # type: ignore
        else:
            affine = self.out_round_floats(collect)
        flatten = [item for sublist in affine for item in sublist]
        return " ".join(flatten)
    
    
    def __out_finalxf_postaffine(self) -> str:
        if self._node.parm(f"{PRX_FF_PRM}{self._prm_names.postaffine_do}").eval():
            collect = []
            for prm in self._flam3_iterator_FF.sec_postAffine_FF[1:-1]:
                collect.append(self._node.parmTuple(f"{prm[0]}").eval())
            angleDeg = self._node.parm(f"{self._flam3_iterator_FF.sec_postAffine_FF[-1][0]}").eval()
            if angleDeg != 0.0:
                affine = self.out_round_floats(self.affine_rot(collect, angleDeg)) # type: ignore
            else:
                affine = self.out_round_floats(collect)
            flatten = [item for sublist in affine for item in sublist]
            return " ".join(flatten)
        else:
            return ''
        
    
    # custom to FLAM3H only
    def __out_flame_data_flam3h_hsv(self, prm_name='') -> Union[str, bool, None]:

        if prm_name == RAMP_HSV_VAL_NAME:
            # This is only for OUT ramp HSV vals.
            # If we are saving out a flame with the HSV ramp, 
            # we do not want to export the HSV values in the XML file anymore
            # so to not overimpose a color correction once we load it back.
            if self._palette_hsv_do:
                return False
            else:
                # Here we go ahead since we know the prm 'RAMP_HSV_VAL_NAME' is a tuple
                prm = self._node.parmTuple(prm_name).eval()
                # If the HSV values are at their defaults, do not export them into the XML file
                if fsum(prm) == 3:
                    return False
                else:
                    return ' '.join([out_round_float(x) for x in prm])
        else:
            print(f"{str(self.node)}: parameter name not found. Please pass in a valid FLAM3H ramp hsv parameter name.")
            return ''
        
    # custom to FLAM3H only
    def __out_flame_data_flam3h_mb_val(self, prm_name='') -> Union[str, bool, None]:

        if self._flam3h_mb_do:
            try:
                return out_round_float(self._node.parm(prm_name).eval())
            except:
                print(f"{str(self.node)}: parameter name not found. Please pass in a valid FLAM3H val parameter name.")
                return False
        else:
            return False


class out_flame_properties(_out_utils):

    def __init__(self, node: hou.Node) -> None:
        super().__init__(node)
        self.flame_name = self._out_utils__out_flame_name() # type: ignore
        self.flame_size = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SIZE)) # type: ignore
        self.flame_center = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_CENTER)) # type: ignore
        self.flame_scale = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_SCALE)) # type: ignore
        self.flame_rotate = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_ROTATE)) # type: ignore
        self.flame_quality = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_QUALITY)) # type: ignore
        self.flame_brightness = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_BRIGHTNESS)) # type: ignore
        self.flame_gamma = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_GAMMA)) # type: ignore
        self.flame_k2 = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_K2)) # type: ignore
        self.flame_vibrancy = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_VIBRANCY)) # type: ignore
        self.flame_highlight = self._out_utils__out_flame_data(OUT_XML_RENDER_HOUDINI_DICT.get(OUT_XML_FLAME_POWER)) # type: ignore
        # The following are not really needed for our purpose and we assume all curves are defaults to start with.
        #
        # self.flame_render_curves = OUT_XML_FLAME_RENDER_OVERALL_CURVE_VAL
        # self.flame_overall_curve = OUT_XML_FLAME_RENDER_OVERALL_CURVE_VAL
        # self.flame_red_curve = OUT_XML_FLAME_RENDER_RED_CURVE_VAL
        # self.flame_green_curve = OUT_XML_FLAME_RENDER_GREEN_CURVE_VAL
        # self.flame_blue_curve = OUT_XML_FLAME_RENDER_BLUE_CURVE_VAL
        
        # custom to FLAM3H only
        self.flam3h_hsv = self._out_utils__out_flame_data_flam3h_hsv(RAMP_HSV_VAL_NAME) # type: ignore
        self.flam3h_mb_fps = self._out_utils__out_flame_data_flam3h_mb_val(OUT_MB_FPS) # type: ignore
        self.flam3h_mb_samples = self._out_utils__out_flame_data_flam3h_mb_val(OUT_MB_SAMPLES) # type: ignore
        self.flam3h_mb_shutter = self._out_utils__out_flame_data_flam3h_mb_val(OUT_MB_SHUTTER) # type: ignore


class out_flam3_data(_out_utils):
    def __init__(self, node: hou.Node) -> None:
        super().__init__(node)
        # FLAM3 data
        self.xf_name = self._out_utils__out_xf_name() # type: ignore
        self.xf_vactive = self._out_utils__out_xf_data(self._prm_names.main_vactive) # type: ignore
        self.xf_weight = self._out_utils__out_xf_data(self._prm_names.main_weight) # type: ignore
        self.xf_xaos = self._out_utils__out_xf_xaos() # type: ignore
        self.xf_pre_blur = self._out_utils__out_xf_pre_blur() # type: ignore
        self.xf_color = self._out_utils__out_xf_data(self._prm_names.shader_color) # type: ignore
        self.xf_symmetry = self._out_utils__out_xf_data(self._prm_names.shader_speed) # type: ignore
        self.xf_opacity = self._out_utils__out_xf_data(self._prm_names.shader_alpha) # type: ignore
        self.xf_preaffine = self._out_utils__out_xf_preaffine() # type: ignore
        self.xf_postaffine = self._out_utils__out_xf_postaffine() # type: ignore
        self.palette_hex = self._out_utils__out_palette_hex() # type: ignore
        self.finalxf_name = self._out_utils__out_finalxf_name() # type: ignore
        self.finalxf_preaffine = self._out_utils__out_finalxf_preaffine() # type: ignore
        self.finalxf_postaffine = self._out_utils__out_finalxf_postaffine() # type: ignore

def my_system() -> str:
    mysys = platform.system()
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
def out_flame_properties_build(self) -> dict:
    f3p = out_flame_properties(self)
    return {OUT_XML_VERSION: f'{XML_APP_NAME_FLAM3HOUDINI}-{my_system()}-{FLAM3HOUDINI_VERSION}',
            XML_XF_NAME: f3p.flame_name,
            OUT_XML_FLAM3H_HSV: f3p.flam3h_hsv, # custom to FLAM3H only
            OUT_XML_FLMA3H_MB_FPS: f3p.flam3h_mb_fps, # custom to FLAM3H only
            OUT_XML_FLMA3H_MB_SAMPLES: f3p.flam3h_mb_samples, # custom to FLAM3H only
            OUT_XML_FLMA3H_MB_SHUTTER: f3p.flam3h_mb_shutter, # custom to FLAM3H only
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


def out_round_float(VAL) -> str:
    if float(VAL).is_integer():
        return str(int(float(VAL)))
    else:
        return str(round(float(VAL), ROUND_DECIMAL_COUNT))

def out_populate_xform_vars_XML(self: hou.Node, 
                                varsPRM: tuple, 
                                TYPES_tuple: tuple, 
                                WEIGHTS_tuple: tuple, 
                                XFORM: lxmlET.Element, # type: ignore
                                MP_IDX: str, 
                                FUNC: Callable) -> list[str]:
    names = []
    for idx, prm in enumerate(WEIGHTS_tuple):
        prm_w = self.parm(f"{prm[0]}{MP_IDX}").eval()
        if prm_w != 0:
            v_type = self.parm(f"{TYPES_tuple[idx]}{MP_IDX}").eval()
            v_name = var_name_from_dict(VARS_FLAM3_DICT_IDX, v_type)
            names.append(v_name)
            XFORM.set(FUNC(v_name), out_round_float(prm_w))
            vars_prm = varsPRM[v_type]
            if vars_prm[-1]:
                f3_prm = varsPRM[v_type][1:-1]
                apo_prm = flam3_varsPRM_APO.varsPRM[v_type][1:-1]
                for id, p in enumerate(apo_prm):
                    if f3_prm[id][-1]:
                        for i, n in enumerate(p):
                            vals = self.parmTuple(f"{f3_prm[id][0]}{MP_IDX}").eval()
                            XFORM.set(FUNC(p[i]), out_round_float(vals[i]))
                    else:
                        val = self.parm(f"{f3_prm[id][0]}{MP_IDX}").eval()
                        XFORM.set(FUNC(p[0]), out_round_float(val))
    return names


# This solution works great and its nice to be lazy for once
# https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file
def _pretty_print(current, parent=None, index=-1, depth=0) -> None:
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('  ' * depth)
        else:
            parent[index - 1].tail = '\n' + ('  ' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('  ' * (depth - 1))
            
            
def out_check_duplicate(vars: list) -> bool:
    result = []
    [result.append(x) for x in vars if x not in result]
    if(len(vars) != len(result)):
        return True
    return False


# Check for FLAM3 compatibility and let the user know.
def flam3_compatibility_check_and_msg(self: hou.Node, 
                                      names_VARS: list, 
                                      names_VARS_PRE: list, 
                                      flam3_do_FF: list, 
                                      names_VARS_FF: list, 
                                      names_VARS_POST_FF: list) -> bool:
    
    bool_VARS = bool_VARS_PRE = bool_VARS_POST = bool_VARS_FF = bool_VARS_PRE_FF = bool_VARS_POST_FF = False
    for n in names_VARS:
        if n:
            if bool_VARS is False: bool_VARS = out_check_duplicate(n)
            else: break
    for n in names_VARS_PRE:
        if n:
            if bool_VARS_PRE is False: bool_VARS_PRE = out_check_duplicate(n)
            else: break
    if flam3_do_FF:
        bool_VARS_FF = out_check_duplicate(names_VARS_FF)
        bool_VARS_POST_FF = out_check_duplicate(names_VARS_POST_FF)
        
    ui_text = "Multiple variations of the same type not allowed"
    ALL_msg = f"Node: {str(self)}\nType: Warning:\n\n"
    VARS_msg = f"Iterators Vars:\nYou are using the same variation multiple times inside one of the iterator VAR section.\n"
    VARS_PRE_msg = f"Iterators PRE Vars:\nYou are using the same variation multiple times inside one of the iterator PRE section.\n"
    VARS_FF_msg = f"FF Vars:\nYou are using the same variation multiple times inside the FF VAR section.\n"
    VARS_POST_FF_msg = f"FF POST Vars:\nYou are using the same variation multiple times inside the FF POST section.\n"
    HELP_msg = f"\nWhile this is doable within the tool, it is not compatible with FLAM3 file format.\nIt require that a variation is used only once per type ( types: PRE, VAR, POST )\notherwise you wont be able to save out the same result neither to load it back.\nFor example you are not allowed to use two Spherical variations inside an iterator VARS section.\nYou can however use one Spherical variation inside the VARS section, one Spherical inside the PRE section and one inside the POST section.\n\nSave the hip file instead if you desire to keep the Flame result as it is now.\nFractorium, Apophysis and all other FLAM3 compatible applications obey to the same rule."
    if bool_VARS:
        ALL_msg += VARS_msg
    if bool_VARS_PRE:
        ALL_msg += "\n" + VARS_PRE_msg
    if bool_VARS_FF:
       ALL_msg += "\n" + VARS_FF_msg
    if bool_VARS_POST_FF:
        ALL_msg += "\n" + VARS_POST_FF_msg
    if bool_VARS or bool_VARS_PRE or bool_VARS_FF or bool_VARS_POST_FF:
        ALL_msg += HELP_msg
        hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3 compatibility warning", details=ALL_msg, details_label=None, details_expanded=True) # type: ignore
        return False
    else:
        return True


def out_build_XML(self, root: lxmlET.Element) -> bool: # type: ignore
    # Build Flame properties
    flame = lxmlET.SubElement(root, XML_FLAME_NAME) # type: ignore
    flame.tag = XML_FLAME_NAME
    for key, value in out_flame_properties_build(self).items():
        if value is not False: # this is important for custom flam3h xml values. Every class def that collect those must return False in case we do not need them.
            flame.set(key, value)
    # Build xforms
    is_PRE_BLUR = False
    name_PRE_BLUR = ''
    names_VARS = []
    names_VARS_PRE = []
    names_VARS_POST = []
    f3d = out_flam3_data(self)
    for iter in range(f3d.iter_count):
        iter_var = iter + 1
        if int(f3d.xf_vactive[iter]):
            xf = lxmlET.SubElement(flame, XML_XF) # type: ignore
            xf.tag = XML_XF
            xf.set(XML_XF_NAME, f3d.xf_name[iter])
            xf.set(XML_XF_WEIGHT, f3d.xf_weight[iter])
            xf.set(XML_XF_COLOR, f3d.xf_color[iter])
            xf.set(XML_XF_SYMMETRY, f3d.xf_symmetry[iter])
            if f3d.xf_pre_blur[iter]:
                is_PRE_BLUR =True
                xf.set(XML_XF_PB, f3d.xf_pre_blur[iter])
            xf.set(XML_PRE_AFFINE, f3d.xf_preaffine[iter])
            if f3d.xf_postaffine[iter]:
                xf.set(XML_POST_AFFINE, f3d.xf_postaffine[iter])
            if f3d.xf_xaos[iter]:
                xf.set(XML_XF_XAOS, f3d.xf_xaos[iter])
            xf.set(XML_XF_OPACITY, f3d.xf_opacity[iter])
            names_VARS.append(out_populate_xform_vars_XML(self, flam3_varsPRM.varsPRM, flam3_iterator.sec_varsT, flam3_iterator.sec_varsW, xf, str(iter_var), make_NULL))
            names_VARS_PRE.append(out_populate_xform_vars_XML(self, flam3_varsPRM.varsPRM, flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW[1:], xf, str(iter_var), make_PRE))
            names_VARS_POST.append(out_populate_xform_vars_XML(self, flam3_varsPRM.varsPRM, flam3_iterator.sec_postvarsT, flam3_iterator.sec_postvarsW, xf, str(iter_var), make_POST))
    # Build finalxform
    names_VARS_FF = []
    names_VARS_PRE_FF = []
    names_VARS_POST_FF = []
    if f3d.flam3_do_FF:
        finalxf = lxmlET.SubElement(flame, XML_FF) # type: ignore
        finalxf.tag = XML_FF
        finalxf.set(XML_XF_COLOR, '0')
        finalxf.set(XML_XF_VAR_COLOR, '1')
        finalxf.set(XML_XF_COLOR_SPEED, '0')
        finalxf.set(XML_XF_SYMMETRY, '1')
        finalxf.set(XML_XF_NAME, f3d.finalxf_name)
        finalxf.set(XML_PRE_AFFINE, f3d.finalxf_preaffine)
        if f3d.finalxf_postaffine:
            finalxf.set(XML_POST_AFFINE, f3d.finalxf_postaffine)
        names_VARS_FF = out_populate_xform_vars_XML(self, flam3_varsPRM_FF(f"{PRX_FF_PRM}").varsPRM_FF(), flam3_iterator_FF.sec_varsT_FF, flam3_iterator_FF.sec_varsW_FF, finalxf, '', make_NULL)
        names_VARS_PRE_FF = out_populate_xform_vars_XML(self, flam3_varsPRM_FF(f"{PRX_FF_PRM_POST}").varsPRM_FF(), flam3_iterator_FF.sec_prevarsT_FF, flam3_iterator_FF.sec_prevarsW_FF, finalxf, '', make_PRE)
        names_VARS_POST_FF = out_populate_xform_vars_XML(self, flam3_varsPRM_FF(f"{PRX_FF_PRM_POST}").varsPRM_FF(), flam3_iterator_FF.sec_postvarsT_FF, flam3_iterator_FF.sec_postvarsW_FF, finalxf, '', make_POST)
    # Build palette
    palette = lxmlET.SubElement(flame, XML_PALETTE) # type: ignore
    palette.tag = XML_PALETTE
    palette.set(XML_PALETTE_COUNT, PALETTE_COUNT_256)
    palette.set(XML_PALETTE_FORMAT, PALETTE_FORMAT)
    palette.text = f3d.palette_hex

    # Get unique plugins used
    if is_PRE_BLUR: name_PRE_BLUR = XML_XF_PB
    names_VARS_flatten_unique = out_vars_flatten_unique_sorted(names_VARS+[names_VARS_FF], make_NULL)
    names_VARS_PRE_flatten_unique = out_vars_flatten_unique_sorted(names_VARS_PRE+[names_VARS_PRE_FF], make_PRE) + [name_PRE_BLUR]
    names_VARS_POST_flatten_unique = out_vars_flatten_unique_sorted(names_VARS_POST+[names_VARS_POST_FF], make_POST)
    # Set unique 'plugins' used and 'new linear' as last
    flame.set(XML_FLAME_PLUGINS, inspect.cleandoc(" ".join(names_VARS_PRE_flatten_unique + names_VARS_flatten_unique + names_VARS_POST_flatten_unique)))
    flame.set(XML_FLAME_NEW_LINEAR, '1')
    
    return flam3_compatibility_check_and_msg(self, names_VARS, names_VARS_PRE, f3d.flam3_do_FF, names_VARS_FF, names_VARS_POST_FF)


###############################################################################################
# MENU - OUT - build menu from output flame file
###############################################################################################
def menu_out_contents_presets(kwargs: dict) -> list:
    xml = kwargs['node'].parm(OUT_PATH).evalAsString()
    menu=[]
    if apo_flame(kwargs['node'], xml).isvalidtree:
        apo = apo_flame(kwargs['node'], xml)
        for i, item in enumerate(apo.name):
            menu.append(i)
            menu.append(item)
        return menu
    else:
        menu.append(-1)
        menu.append('Empty')
        return menu


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
        
        if flame_name:
            splt = ':'
            div = '::'
            rp = flame_name.split(splt)
            rp[:] = [item for item in rp if item]
            
            # Lets make some name checks first
            try:
                # if the filename start with either a ':' or '::' followed by a valid integer
                # lets give it a default name
                if (flame_name[0:1] == splt or flame_name[0:2] == div) and isinstance(int(rp[-1]), int):
                    now = datetime.now()
                    flame_name_new = now.strftime("Flame_%b-%d-%Y_%H%M%S")
                    rp = flame_name_new.split(splt)
                    rp[:] = [item for item in rp if item]
                # else if the filename end with either a ':' or '::' preceded by a valid integer
                # lets give it a default name
                elif (flame_name[-1:] == splt or flame_name[-2:] == div) and isinstance(int(rp[0]), int):
                    now = datetime.now()
                    flame_name_new = now.strftime("Flame_%b-%d-%Y_%H%M%S")
                    rp = flame_name_new.split(splt)
                    rp[:] = [item for item in rp if item]
            except:
                pass
            
            is_int = True
            try:
                # if the name is a number, we want to still add the iteration num to it
                # and not evaluate this as integer
                if rp[-1] != flame_name:
                    int(rp[-1])
                else:
                    is_int = False
            except:
                is_int = False
                
            if is_int is False:
                rp_clean = []
                for item in rp:
                    item_cleaned =''.join(letter for letter in item if letter.isalnum() or letter in CHARACTERS_ALLOWED_OUT_AUTO_ADD_ITER_NUM)
                    rp_clean.append(item_cleaned)
                    
                flame_name_new = ' '.join(rp_clean) + div + str(iter_num)
                return flame_name_new
            else:
                return flame_name
        else:
            return flame_name
    else:
        return flame_name    


def out_auto_change_iter_num(iter_num: int, flame_name: str, autoadd: int) -> str:
    """It will check the passed Flame name 
    and update the iteration number when changing iterations.
    If not iteration number is present in the passed Flame name
    it will add it to the end of the Flame name.

    Args:
        iter_num (int): the current iteration's number
        flame_name (str): The Flame name to check
        autoadd (int): Auto add iter num toggle value

    Returns:
        str: A new Flame name with the iter num updated/added if needed.
    """
    if autoadd:
        
        if flame_name:
            splt = ':'
            div = '::'
            rp = str(flame_name).rpartition(div)
            
            # Lets make some name checks first
            try:
                # if the filename start with either a ':' or '::' followed by a valid integer
                # lets give it a default name
                if (flame_name[0:1] == splt or flame_name[0:2] == div) and isinstance(int(rp[-1]), int):
                    now = datetime.now()
                    flame_name_new = now.strftime("Flame_%b-%d-%Y_%H%M%S")
                    rp = flame_name_new.split(splt)
                    rp[:] = [item for item in rp if item]
                # else if the filename end with either a ':' or '::' preceded by a valid integer
                # lets give it a default name
                elif (flame_name[-1:] == splt or flame_name[-2:] == div) and isinstance(int(rp[0]), int):
                    now = datetime.now()
                    flame_name_new = now.strftime("Flame_%b-%d-%Y_%H%M%S")
                    rp = flame_name_new.split(splt)
                    rp[:] = [item for item in rp if item]
            except:
                pass

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
                return out_auto_add_iter_num(iter_num, flame_name, autoadd)
        else:
            return flame_name
    else:
        return flame_name
    
    
def out_auto_add_iter_num_to_prm(self: hou.Node) -> None:
    
    autoadd = self.parm(OUT_AUTO_ADD_ITER_NUM).evalAsInt()
    flame_name = self.parm(OUT_FLAME_PRESET_NAME).eval()
    iter_num = self.parm(SYS_ITERATIONS).evalAsInt()
    flame_name_new = out_auto_add_iter_num(iter_num, flame_name, autoadd)
    
    self.setParms({OUT_FLAME_PRESET_NAME: flame_name_new}) #type: ignore


def out_auto_change_iter_num_to_prm(self: hou.Node) -> None:
    
    autoadd = self.parm(OUT_AUTO_ADD_ITER_NUM).evalAsInt()
    flame_name = self.parm(OUT_FLAME_PRESET_NAME).eval()
    iter_num = self.parm(SYS_ITERATIONS).evalAsInt()
    flame_name_new = out_auto_change_iter_num(iter_num, flame_name, autoadd)
    
    self.setParms({OUT_FLAME_PRESET_NAME: flame_name_new}) #type: ignore



def out_check_build_file(file_split: tuple[str, str], file_name: str, file_ext: str) -> str:
    """_summary_

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
    build_f_s_cleaned = []
    # Clean location directories.
    # Probably not needed as I check for the validity of the parent directory eitherway
    # but i leave it here and remove it if causing any trouble down the line.
    for item in build_f_s:
        item_cleaned =''.join(letter for letter in item if letter.isalnum() or letter in CHARACTERS_ALLOWED)
        build_f_s_cleaned.append(item_cleaned)
    # append cleaned file_name
    build_f_s_cleaned.append(''.join(letter for letter in file_name if letter.isalnum() or letter in CHARACTERS_ALLOWED))
    # the file_ext start with a dot so its added as last
    return "/".join(build_f_s_cleaned) + file_ext
def out_check_outpath(self, infile: str, file_ext: str, prx: str) -> Union[str, bool]:
    
    now = datetime.now()
    new_name = now.strftime(f"{prx}_%b-%d-%Y_%H%M%S")
    
    file = os.path.expandvars(infile)
    file_s = os.path.split(file)
    
    autopath = self.parm(AUTO_PATH_CORRECTION).evalAsInt()

    if autopath:
        
        # Just in case lets check is a valid location
        if os.path.isdir(file_s[0]):

            filename_s = os.path.splitext(file_s[-1])
            
            if filename_s[-1] == file_ext:
                build_f_s = file.split("/")
                build_f_s[:] = [item for item in build_f_s if item]
                build_f_s[-1] = ''.join(letter for letter in build_f_s[-1] if letter.isalnum() or letter in CHARACTERS_ALLOWED)
                return "/".join(build_f_s)
            
            elif not filename_s[-1] and filename_s[0]:
                # this is done in case only the extension is left in the prm field
                if file_s[-1] in file_ext or file_s[-1][0] == ".":
                    return out_check_build_file(file_s, new_name, file_ext)
                else:
                    return out_check_build_file(file_s, file_s[-1], file_ext)
            
            elif not filename_s[-1] and not filename_s[0]:
                return out_check_build_file(file_s, new_name, file_ext)
            
            # this as last for now
            #
            # If there is a file extension and it match part or all of the file_ext string.
            #
            # This will execute only if the string match at the beginning of the file extension
            # otherwise the above if/elif statements would have executed already.
            elif len(filename_s) > 1 and filename_s[-1] in file_ext:
                return out_check_build_file(file_s, filename_s[0], file_ext)
            else:
                # Print out proper msg based on file extension
                if ".flame" == file_ext:
                    print(f"{str(self)}.OUT: You selected an OUT file that is not a {prx} file type.")
                elif ".json" == file_ext:
                    print(f"{str(self)}.Palette: You selected an OUT file that is not a {prx} file type.")
                return False
        else:
            # If the path string is empty we do not want to print out
            if file:
                if ".flame" == file_ext:
                    print(f"{str(self)}.OUT: Select a valid OUT directory location.")
                elif ".json" == file_ext:
                    print(f"{str(self)}.Palette: Select a valid OUT directory location.")
            return False
    else:
        # just check if the user input is a valid file
        if os.path.isfile(file_s[0]):
            return infile
        else:
            # If the path string is empty we do not want to print out
            if file:
                if ".flame" == file_ext:
                    print(f"{str(self)}.OUT: Select a valid OUT directory location.")
                elif ".json" == file_ext:
                    print(f"{str(self)}.Palette: Select a valid OUT directory location.")
            return False



def out_new_XML(self: hou.Node, outpath: str) -> None:
    root = lxmlET.Element(XML_VALID_FLAMES_ROOT_TAG) # type: ignore
    if out_build_XML(self, root):
        _pretty_print(root)
        tree = lxmlET.ElementTree(root)
        tree.write(outpath)


def out_append_XML(self: hou.Node, apo_data: apo_flame, out_path: str) -> None:
    # with ET since I have the XML tree already stored using its Element type
    # root = apo_data.tree.getroot()
    
    # with lxmlET
    tree = lxmlET.parse(apo_data.xmlfile) # type: ignore
    root = tree.getroot()
    
    if out_build_XML(self, root):
        _pretty_print(root)
        tree = lxmlET.ElementTree(root)
        tree.write(out_path)


def out_XML(kwargs: dict) -> None:
    node = kwargs['node']
    out_path = node.parm(OUT_PATH).evalAsString()
    out_path_checked = out_check_outpath(node, out_path, OUT_FLAM3_FILE_EXT, 'Flame')
    
    if out_path_checked is not False:
        if kwargs['shift']:
            open_explorer_file(out_path_checked)
        else:

            if isLock(out_path_checked, FLAM3_LIB_LOCK):
                ui_text = f"This Flam3 library is Locked."
                ALL_msg = f"This Flame library is Locked and you can not modify this file.\n\nTo Lock a Flame lib file just rename it using:\n\"{FLAM3_LIB_LOCK}\" as the start of the filename.\n\nOnce you are happy with a Flame library you built, you can rename the file to start with: \"{FLAM3_LIB_LOCK}\"\nto prevent any further modifications to it. For example if you have a lib file call: \"my_grandJulia.flame\"\nyou can rename it to: \"{FLAM3_LIB_LOCK}_my_grandJulia.flame\" to keep it safe."
                hou.ui.displayMessage(ui_text, buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="FLAM3 Lib Lock", details=ALL_msg, details_label=None, details_expanded=False) # type: ignore
            else:
                apo_data = apo_flame(kwargs['node'], str(out_path_checked))
                if kwargs["ctrl"]:
                    node.setParms({OUT_PATH: str(out_path_checked)})
                    out_new_XML(node, str(out_path_checked))
                    node.setParms({OUT_FLAME_PRESET_NAME: ''})
                else:
                    node.setParms({OUT_PATH: str(out_path_checked)})
                    if apo_data.isvalidtree:
                        out_append_XML(node, apo_data, str(out_path_checked))
                        node.setParms({OUT_FLAME_PRESET_NAME: ''})
                    else:
                        out_new_XML(node, str(out_path_checked))
                        node.setParms({OUT_FLAME_PRESET_NAME: ''})
                init_presets(kwargs, OUT_PRESETS)
