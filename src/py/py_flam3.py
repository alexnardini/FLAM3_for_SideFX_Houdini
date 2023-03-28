from __future__ import division, annotations
from platform import python_version
from typing import Union, Callable
from itertools import count as iter_count
from itertools import islice as iter_islice
from textwrap import wrap
import xml.etree.ElementTree as ET
import os, hou, re, json, colorsys, webbrowser, inspect



#   Tested on PYTHON v3.7.13(H19) and PYTHON v3.9.10(H19.5)
 
#   Title:      SideFX Houdini FLAM3: 2D
#   Author:     Alessandro Nardini
#   date:       January 2023, Last revised March 2023
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
#   Comment:    WIP - Python classes and definitions for tool's user experience.
#               Everything is then glued together inside Houdini.





DPT = "*"
PRM = "..."
PRX_FF_PRM = "ff"
PRX_FF_PRM_POST = "fp1"
SEC_MAIN = ".main"
SEC_XAOS = ".xaos"
SEC_SHADER = ".shader"
SEC_PREVARS = ".pre_vars"
SEC_VARS = ".vars"
SEC_POSTVARS = ".post_vars"
SEC_PREAFFINE = ".pre_affine"
SEC_POSTAFFINE = ".post_affine"
RAMP_SRC_NAME = "palette"
RAMP_HSV_NAME = "palettehsv"
RAMP_HSV_VAL_NAME = "hsv"





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
                (f"radialblur{PRM}", ("radialblur_", 1), 1), 
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
                (f"polynomial{PRM}", ("polynomialpow_", 1), ("polynomiallc_", 1), ("polynomialsc_", 1), 1) )


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
                        (self.varsPRM[101][0], (f"{self.prx}_{self.varsPRM[101][1][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[101][2][0][:-1]}", 1), (f"{self.prx}_{self.varsPRM[101][3][0][:-1]}", 1), 1) )
        
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
    sec_varsT_FF = ( f"{PRX_FF_PRM}{n.var_type_1}", f"{PRX_FF_PRM}{n.var_type_2}", f"{PRX_FF_PRM}{n.var_type_3}" )
    sec_varsW_FF = ( (f"{PRX_FF_PRM}{n.var_weight_1}", 0), (f"{PRX_FF_PRM}{n.var_weight_2}", 0), (f"{PRX_FF_PRM}{n.var_weight_3}", 0) )
    sec_postvarsT_FF = ( f"{PRX_FF_PRM}{n.postvar_type_1}", f"{PRX_FF_PRM}{n.postvar_type_2}" )
    sec_postvarsW_FF = ( (f"{PRX_FF_PRM}{n.postvar_weight_1}", 0), (f"{PRX_FF_PRM}{n.postvar_weight_2}", 0) )
    sec_preAffine_FF = ( (f"{PRX_FF_PRM}{n.preaffine_x}", 1), (f"{PRX_FF_PRM}{n.preaffine_y}", 1), (f"{PRX_FF_PRM}{n.preaffine_o}", 1), (f"{PRX_FF_PRM}{n.preaffine_ang}", 0) )
    sec_postAffine_FF = ( (f"{PRX_FF_PRM}{n.postaffine_do}", 0), (f"{PRX_FF_PRM}{n.postaffine_x}", 1), (f"{PRX_FF_PRM}{n.postaffine_y}", 1), (f"{PRX_FF_PRM}{n.postaffine_o}", 1), (f"{PRX_FF_PRM}{n.postaffine_ang}", 0) )
    
    
    # ALL method lists
    # allT_FF list is omitted here because FF VARS and FF POST VARS have their own unique parametric parameters
    # so I need to handle them one by one inside: def prm_paste_FF() and def prm_paste_sel_FF()
    allMisc_FF = sec_varsW_FF + sec_postvarsW_FF + sec_preAffine_FF + sec_postAffine_FF





###############################################################################################
# MENU - Build vars type menus
###############################################################################################
def menu_T(int_mode: int) -> list:
    """
    Args:
        int_mode (int): [int(0) build menu with all variations. int(1) build menu without parametrics variations.]

    Returns:
        list: [return menu list]
    """
    menu=[]
    if int_mode:
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
        hou.session.flam3node_mp_id
    except:
        hou.session.flam3node_mp_id = -1

    id_from = hou.session.flam3node_mp_id

    # If an iterator has been copied on a node that has been deleted
    # revert to -1 so that we are forced to copy an iterator again.
    try:
        hou.session.flam3node.type()
    except:
        id_from = -1

    # If we did and the FLAM3 node still exist
    if id_from != -1:

        # current id
        id = kwargs['script_multiparm_index']

        node=kwargs['node']
        flam3node = hou.session.flam3node
        
        if node == flam3node and id==id_from:
            menuitems = ( "Iterator copied. Select a different iterator number or a different FLAM3 node to paste those values", "" )
        elif node == flam3node:
            menuitems = ( "", f"{str(id_from)}", f"{str(id_from)}: xaos:", f"{str(id_from)}: shader", f"{str(id_from)}: pre", f"{str(id_from)}: vars", f"{str(id_from)}: post", f"{str(id_from)}: pre affine", f"{str(id_from)}: post affine", "" )
        else:
            flam3nodeIter = f"{str(flam3node)}.iter."
            menuitems = ( "", f"{flam3nodeIter}{str(id_from)}", f"{flam3nodeIter}{str(id_from)}: xaos:", f"{flam3nodeIter}{str(id_from)}: shader", f"{flam3nodeIter}{str(id_from)}: pre", f"{flam3nodeIter}{str(id_from)}: vars", f"{flam3nodeIter}{str(id_from)}: post", f"{flam3nodeIter}{str(id_from)}: pre affine", f"{flam3nodeIter}{str(id_from)}: post affine", "" )
        for i, item in enumerate(menuitems):
            menu.append(i)
            menu.append(item)

        return menu
    else:
        menuitems = ( "Please copy an iterator first", "" )
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
        hou.session.flam3node_FF_check
    except:
        hou.session.flam3node_FF_check = -1

    flam3node_FF_check = hou.session.flam3node_FF_check

    # If the FF has been copied on a node that has been deleted
    # revert to -1 so that we are forced to copy an FF again.
    try:
        hou.session.flam3node_FF.type()
    except:
        flam3node_FF_check = -1

    # If we did and the FLAM3 node still exist
    if flam3node_FF_check != -1:

        node=kwargs['node']
        flam3node_FF = hou.session.flam3node_FF
        
        if node == flam3node_FF:
            menuitems = ( "FF copied. Select a different FLAM3 node to paste those FF values.", "" )
        else:
            flam3nodeFF = f"{str(flam3node_FF)}.FF"
            menuitems = ( "", f"{flam3nodeFF}: var", f"{flam3nodeFF}: post", f"{flam3nodeFF}: pre affine", f"{flam3nodeFF}: post affine", "" )
        for i, item in enumerate(menuitems):
            menu.append(i)
            menu.append(item)

        return menu
    else:
        menuitems = ( "Please copy the FF first", "" )
        for i, item in enumerate(menuitems):
            menu.append(i-1)
            menu.append(item)

        return menu





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
        node.setParms({f"{prm}{id}": prm_from})
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
                node.setParms({f"{n.main_note}_{id}": f"iter.{id_from}{str_section}"})
            else:
                node.setParms({f"{n.main_note}_{id}": f"{paste_save_note(_current_note)}iter.{id_from}{str_section}"})
        else:
            if len(_current_note) == 0:
                node.setParms({f"{n.main_note}_{id}": f"{str(flam3node)}.iter.{id_from}{str_section}"})
            else:
                node.setParms({f"{n.main_note}_{id}": f"{paste_save_note(_current_note)}{str(flam3node)}.iter.{id_from}{str_section}"})
            print(f"{str(node)}: Copied values from: {str(flam3node)}.iter.{id_from}{str_section} to: {str(node)}.iter.{id}{str_section}")
    elif int_mode == 1:
        if node != flam3node:
            if len(_current_note_FF) == 0:
                node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{str(flam3node)}.FF"})
            else:
                node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{paste_save_note(_current_note_FF)}{str(flam3node)}.FF"})
            print(f"{str(node)}: Copied FF from: {str(flam3node)}.FF to: {str(node)}.FF")
    elif int_mode == 2:
        if node != flam3node:
            if len(_current_note_FF) == 0:
                node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{str(flam3node)}.FF{str_section}"})
            else:
                node.setParms({f"{PRX_FF_PRM}{n.main_note}": f"{paste_save_note(_current_note_FF)}{str(flam3node)}.FF{str_section}"})
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
        flam3node = hou.session.flam3node
        id_from = hou.session.flam3node_mp_id

        # If an iterator was copied on a node that has been deleted
        # revert to -1 so that we are forced to copy an iterator again.
        try:
            flam3node.type()
        except:
            id_from = -1

        # If we ever copied an iterator from a currently existing FLAM3 node
        if id_from != -1:
            if node==flam3node and id==id_from:
                print(f"{str(node)}: Iterator copied. Select a different iterator number to paste those values.")
            else:
                pastePRM_T_from_list(flam3_iterator.allT, flam3_varsPRM.varsPRM, node, flam3node, str(id), str(id_from))
                paste_from_list(flam3_iterator.allMisc, node, flam3node, str(id), str(id_from))
                paste_set_note(0, "", node, flam3node, str(id), str(id_from))

        else:
            print(f"{str(node)}: Please copy an iterator first.")

    elif kwargs["shift"]:
        del hou.session.flam3node_mp_id
        del hou.session.flam3node

    else:
        hou.session.flam3node_mp_id = kwargs['script_multiparm_index']
        hou.session.flam3node = kwargs['node']
        print(f"{str(kwargs['node'])}: Copied iterator: {str(hou.session.flam3node)}->iter.{str(hou.session.flam3node_mp_id)}")





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
        flam3node_FF = hou.session.flam3node_FF
        flam3node_FF_check = hou.session.flam3node_FF_check

        # If the FF was copied from a node that has been deleted
        # revert to -1 so that we are forced to copy an iterator again.
        try:
            flam3node_FF.type()
        except:
            flam3node_FF_check = -1

        # If we ever copied an FF from a currently existing FLAM3 node
        if flam3node_FF_check != -1:
            if node==flam3node_FF:
                print(f"{str(node)}: FF copied. Select a different FLAM3 node to paste those FF values.")
            else:
                pastePRM_T_from_list(flam3_iterator_FF.sec_varsT_FF, flam3_varsPRM_FF(PRX_FF_PRM).varsPRM_FF(), node, flam3node_FF, "", "")
                pastePRM_T_from_list(flam3_iterator_FF.sec_postvarsT_FF, flam3_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), node, flam3node_FF, "", "")
                paste_from_list(flam3_iterator_FF.allMisc_FF, node, flam3node_FF, "", "")
                paste_set_note(1, "", node, flam3node_FF, "", "")

        else:
            print(f"{str(node)}: Please copy FF first.")

    elif kwargs["shift"]:
        del hou.session.flam3node_FF_check
        del hou.session.flam3node_FF

    else:
        hou.session.flam3node_FF_check = 1
        hou.session.flam3node_FF = kwargs['node']
        print(f"{str(kwargs['node'])}: Copied FF: {str(hou.session.flam3node_FF)}->FF")





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
    flam3node = hou.session.flam3node
    id_from = hou.session.flam3node_mp_id

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

        # set XAOS
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
    
    else:
        print(f"{str(node)}: Please copy an iterator first")





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
    flam3node_FF = hou.session.flam3node_FF
    flam3node_FF_check = hou.session.flam3node_FF_check

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

        # set FF VARS
        if ff_paste_sel == 1:
            pastePRM_T_from_list(flam3_iterator_FF.sec_varsT_FF, flam3_varsPRM_FF(PRX_FF_PRM).varsPRM_FF(), node, flam3node_FF, "", "")
            paste_from_list(flam3_iterator_FF.sec_varsW_FF, node, flam3node_FF, "", "")
            paste_set_note(2, SEC_VARS, node, flam3node_FF, "", "")
        
        # set FF POST VARS
        elif ff_paste_sel == 2:
            pastePRM_T_from_list(flam3_iterator_FF.sec_postvarsT_FF, flam3_varsPRM_FF(PRX_FF_PRM_POST).varsPRM_FF(), node, flam3node_FF, "", "")
            paste_from_list(flam3_iterator_FF.sec_postvarsW_FF, node, flam3node_FF, "", "")
            paste_set_note(2, SEC_POSTVARS, node, flam3node_FF, "", "")

        # set FF PRE AFFINE
        elif ff_paste_sel == 3:
            paste_from_list(flam3_iterator_FF.sec_preAffine_FF, node, flam3node_FF, "", "")
            paste_set_note(2, SEC_PREAFFINE, node, flam3node_FF, "", "")
        
        # set FF POST AFFINE
        elif ff_paste_sel == 4:
            paste_from_list(flam3_iterator_FF.sec_postAffine_FF, node, flam3node_FF, "", "")
            paste_set_note(2, SEC_POSTAFFINE, node, flam3node_FF, "", "")


        # Set it to a null value ( first in the menu array idx in this case )
        # so that we can paste the same section again, if we want to.
        #
        # please check def->menu_copypaste_FF() to know its size.
        node.setParms({f"{PRX_FF_PRM}{n.main_prmpastesel}": str(0)})
                
    else:
        print(f"{str(node)}: Please copy the FF first.")





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
    
    # Clear up stats if there already ( due to be stored into a houdini preset also )
    node.setParms({"flamestats_msg": ""})
    
    # Set about tab infos
    flam3_about_msg(node)
    flam3_about_plugins_msg(node)

    # FLAM3 node and MultiParameter id for iterators
    #
    # If there were already a FLAM3 node in the scene
    # and we copied already an iterator's values, lets keep whats stored,
    # otherwise initialize those values.
    try:
        hou.session.flam3node
    except:
        hou.session.flam3node = node
    try:
        hou.session.flam3node_mp_id
    except:
        hou.session.flam3node_mp_id = -1

    # If an iterator was copied from a node that has been deleted
    # revert to -1 so that we are forced to copy an iterator again.
    try:
        hou.session.flam3node.type()
    except:
        hou.session.flam3node_mp_id = -1



    # FLAM3 node for FF.
    #
    # If there were already a FLAM3 node in the scene
    # and we copied already FF's values, lets keep whats stored,
    # otherwise initialize those values.
    try:
        hou.session.flam3node_FF
    except:
        hou.session.flam3node_FF = node
    try:
        hou.session.flam3node_FF_check
    except:
        hou.session.flam3node_FF_check = -1

    # If the FF was copied from a node that has been deleted
    # revert to -1 so that we are forced to copy the FF again.
    try:
        hou.session.flam3node_FF.type()
    except:
        hou.session.flam3node_FF_check = -1

    # Initialize flam3 viewport Color Scheme
    try:
        hou.session.flam3_CS
    except:
        hou.session.flam3_CS = []



###############################################################################################
# Init parameter presets menu list as soon as you load a valid json/flame file
###############################################################################################
def init_presets(kwargs: dict, prm_name: str) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """    
    node = kwargs['node']
    prm = node.parm(prm_name)
    prm.set('999999')
    
    
    if "apopresets" in prm_name:
        xml = node.parm('apofilepath').evalAsString()
        if not apo_flame(xml).isvalidtree:
            node.setParms({"flamestats_msg": "Please load a valid *.flame file."})
        else:
            prm.set('0')
            apo_to_flam3(node)
        



###############################################################################################
# MENU - JSON - build menu from ramp presets file
###############################################################################################
def menu_ramp_presets(kwargs: dict) -> list:

    filepath = kwargs['node'].parm('filepath').evalAsString()

    menu=[]
    if os.path.isfile(filepath) and os.path.getsize(filepath)>0:

        with open(filepath) as f:
            data = json.load(f)
        
        menuitems = data.keys()

        for i, item in enumerate(menuitems):
            menu.append(i)
            menu.append(item)
            
        return menu
    else:
        return menu




###############################################################################################
# Save current ramp to a json file
###############################################################################################
def ramp_save(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """    
    filepath = kwargs['node'].parm('filepath').evalAsString()
    path = os.path.dirname(filepath)
    if not os.path.exists(path):
        os.makedirs(path)
        print('Created Directory')
        
    #pop up window - enter preset name for json file entries
    uitext = hou.ui.readInput('Write the name of your preset', buttons=('OK', 'Cancel'), severity=hou.severityType.Message, 
    default_choice=0, close_choice=-1, help=None, title='Preset Name', initial_contents=None)
    if uitext[0]==1:
        pass
    else:
        presetname = uitext[1]
    
        #get ramp parameters to a dictionary
        node=kwargs['node']
        parm = node.parm(RAMP_SRC_NAME)
        ramp = parm.evalAsRamp()
        interplookup = [hou.rampBasis.Constant, hou.rampBasis.Linear, hou.rampBasis.CatmullRom, hou.rampBasis.MonotoneCubic, hou.rampBasis.Bezier, hou.rampBasis.BSpline, hou.rampBasis.Hermite]
        
        keylist = []
        for i,key in enumerate(ramp.keys()):
            data = { 'posindex': i,
                     'pos' : key,   
                     'value': ramp.values()[i],
                     'interp': interplookup.index(ramp.basis()[i])}    
            keylist.append(data)
        
        dict = { presetname: keylist } #we use the preset name from the pop up window
        
        #convert dict to json
        json_data = json.dumps(dict, indent=4)
        
        #write - overwrite or append json to disk
        if os.path.isfile(filepath) and os.path.getsize(filepath)>0: #if file exists and is not zero bytes
            
            user = hou.ui.displayMessage('This file already exist: "Append" this palette to the current file or "Override" the current file with this palette.', buttons=('Append','Overwrite','Cancel')) 
            if user==0:#append mode
                with open(filepath,'r') as r:
                    prevdata = json.load(r)
                with open(filepath, 'w') as w:
                    newdata = dict
                    prevdata.update(newdata)
                    data = json.dumps(prevdata,indent = 4)
                    w.write(data)
        
            if user==1:#write mode
                os.remove(filepath)
                with open(filepath,'w') as f:
                    f.write(json_data)
            if user==2:
                pass
        else:
            with open(filepath,'w') as f:
                f.write(json_data)





###############################################################################################
# Set ramp value from a json file
###############################################################################################
def json_to_ramp(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """    
    node = kwargs['node']
    
    #get ramp parm
    ramp_parm = node.parm(RAMP_SRC_NAME)
    ramp_parm.deleteAllKeyframes()
    
    #read from json and set ramp values
    filepath = node.parm('filepath').evalAsString()
    #get current preset
    preset_id = int(node.parm('presets').eval())
    preset = node.parm('presets').menuLabels()[preset_id]
    
    if os.path.isfile(filepath) and os.path.getsize(filepath)>0:

        with open(filepath) as f:
            data = json.load(f)[preset]
            keys = []
            values = []
            bases = []
            interplookup = [hou.rampBasis.Constant, hou.rampBasis.Linear, hou.rampBasis.CatmullRom, hou.rampBasis.MonotoneCubic, hou.rampBasis.Bezier, hou.rampBasis.BSpline, hou.rampBasis.Hermite]
            for i in data:
                keys.append(i['pos'])
                values.append(i['value'])
                bases.append(interplookup[i['interp']])
       
        # Initialize new ramp.
        ramp = hou.Ramp(bases, keys, values)
        ramp_parm.set(ramp)

        # Apply HSV if any is currently set
        palette_hsv(node)





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
    views = hou.ui.paneTabs()
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
        module_test = hou.session.flam3_CS;
    except:
        hou.session.flam3_CS = []

    count = 0
    viewers_col = []

    setprm = self.parm("setdark").eval()
    Light = hou.viewportColorScheme.Light
    Grey  = hou.viewportColorScheme.Grey
    Dark  = hou.viewportColorScheme.Dark

    for view in getSceneViewers():

        settings = view.curViewport().settings()
        col = settings.colorScheme()
        viewers_col.append(col)
        try:
            idx_test = hou.session.flam3_CS[count]
        except:
            if len(hou.session.flam3_CS) > 0:
                hou.session.flam3_CS.append(viewers_col)
            else:
                hou.session.flam3_CS = [];
                hou.session.flam3_CS.append(viewers_col)

        if setprm:
            if len(hou.session.flam3_CS) == 0:
                if col == Light or col == Grey:
                    settings.setColorScheme(Dark)
            else:
                if col == Light or col == Grey:
                    settings.setColorScheme(Dark)
                elif col == Dark and hou.session.flam3_CS[count] != Dark:
                    if hou.session.flam3_CS[count] == Light:
                        settings.setColorScheme(Light)
                    elif hou.session.flam3_CS[count] == Grey:
                        settings.setColorScheme(Grey)

        else:
            if col == Dark and hou.session.flam3_CS[count] != Dark:
                if hou.session.flam3_CS[count] == Light:
                    settings.setColorScheme(Light)
                elif hou.session.flam3_CS[count] == Grey:
                    settings.setColorScheme(Grey)
        count += 1
    
    # Update history
    hou.session.flam3_CS = []
    hou.session.flam3_CS = viewers_col





###############################################################################################
# set viewport particle display. ( Points or Pixels )
###############################################################################################
def viewportParticleDisplay(self: hou.Node) -> None:

    pttype = self.parm("vptype").evalAsInt()

    Points = hou.viewportParticleDisplay.Points
    Pixels = hou.viewportParticleDisplay.Pixels

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

    ptsize = self.parm("vpptsize").evalAsFloat()

    for view in getSceneViewers():
        settings = view.curViewport().settings()
        settings.particlePointSize(ptsize)





###############################################################################################
# Parameters resets... 
###############################################################################################
def reset_FF(self: hou.Node) -> None:

    n = flam3_iterator_prm_names

    self.setParms({f"{PRX_FF_PRM}{n.main_note}": ""})
    self.setParms({f"{PRX_FF_PRM}{n.var_type_1}": 0})
    self.setParms({f"{PRX_FF_PRM}{n.var_type_2}": 0})
    self.setParms({f"{PRX_FF_PRM}{n.var_type_3}": 0})
    self.setParms({f"{PRX_FF_PRM}{n.var_weight_1}": 1})
    self.setParms({f"{PRX_FF_PRM}{n.var_weight_2}": 0})
    self.setParms({f"{PRX_FF_PRM}{n.var_weight_3}": 0})
    # FF post
    self.setParms({f"{PRX_FF_PRM}{n.postvar_type_1}": 0})
    self.setParms({f"{PRX_FF_PRM}{n.postvar_type_2}": 0})
    self.setParms({f"{PRX_FF_PRM}{n.postvar_weight_1}": 0})
    self.setParms({f"{PRX_FF_PRM}{n.postvar_weight_2}": 0})
    # FF affine
    self.setParms({f"{PRX_FF_PRM}{n.preaffine_x}": hou.Vector2((1.0, 0.0))})
    self.setParms({f"{PRX_FF_PRM}{n.preaffine_y}": hou.Vector2((0.0, 1.0))})
    self.setParms({f"{PRX_FF_PRM}{n.preaffine_o}": hou.Vector2((0.0, 0.0))})
    self.setParms({f"{PRX_FF_PRM}{n.preaffine_ang}": 0})
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_do}": 0})
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_x}": hou.Vector2((1.0, 0.0))})
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_y}": hou.Vector2((0.0, 1.0))})
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_o}": hou.Vector2((0.0, 0.0))})
    self.setParms({f"{PRX_FF_PRM}{n.postaffine_ang}": 0})


def reset_SYS(self: hou.Node, density: int, iter: int, mode: int) -> None:
    """
    Args:
        density (int): Numper of points to use
        iter (int): Number of iterations
        mode (int): 0: skip "doff" 1: reset "doff"
    """    
    
    self.setParms({"ptcount": density})
    self.setParms({"iter": iter})
    if mode:
        self.setParms({"doff": 0})
    self.setParms({"tag": 1})
    self.setParms({"tagsize": 0})
    self.setParms({"rip": 0})


def reset_TM(self) -> None:
    self.setParms({"dotm": 0})
    self.setParms({"tmrt": 0})
        

def reset_SM(self) -> None:
    self.setParms({"sm": 0})
    self.setParms({"smrot": 0})


def reset_MB(self) -> None:
    self.setParms({"domb": 0})
    self.setParms({"fps": 24})
    self.setParms({"mbsamples": 16})
    self.setParms({"shutter": 0.5})


def reset_PREFS(self) -> None:
    self.setParms({"showprefs": 1})
    self.setParms({"xm": 0})
    self.setParms({"camhandle": 0})
    self.setParms({"camcull": 0})
    self.setParms({"fcam": ""})
    self.setParms({"cullamount": 0.99})




###############################################################################################
# Load default values. ( Sierpinsky triangle )
###############################################################################################
def flam3_default(self: hou.Node) -> None:
    """
    Args:
        self (hou.Node): [current hou.Node]
    """
    # Iterators reset
    self.setParms({"flamefunc": 0})
    for p in self.parms():
        p.deleteAllKeyframes()
    # Add back iterators
    # This way all parameters will reset to their default values.
    self.setParms({"flamefunc": 3})

    #
    # SYS
    reset_SYS(self, 500000, 10, 1)
    reset_TM(self)
    reset_FF(self)
    reset_SM(self)
    reset_MB(self)
    reset_PREFS(self)

    # CP
    self.setParms({"filepath": ""})
    self.setParms({RAMP_HSV_VAL_NAME: hou.Vector3((0.0, 1.0, 1.0))})
    # CP->ramp
    ramp_parm = self.parm(RAMP_SRC_NAME)
    ramp_parm.deleteAllKeyframes()
    color_bases = [hou.rampBasis.Linear] * 3
    color_keys = [0.0, 0.5, 1.0]
    color_values = [(1,0,0), (0,1,0), (0,0,1)]
    ramp_parm.set(hou.Ramp(color_bases, color_keys, color_values))
    # Update ramp py 
    palette_cp(self)
    palette_hsv(self)
    
    # IN
    self.setParms({"apofilepath": ""})
    self.setParms({"apopresets": str(0)})
    self.setParms({"flamestats_msg": ""})
    self.setParms({"descriptive_msg": ""})
    
    # iterators
    n = flam3_iterator_prm_names

    # iter 1
    #
    # shader
    self.setParms({f"{n.shader_color}_1": 0})
    self.setParms({f"{n.shader_speed}_1": -0.5})
    # vars
    self.setParms({f"{n.prevar_type_1}_1": 0})
    self.setParms({f"{n.prevar_type_2}_1": 0})
    self.setParms({f"{n.var_type_1}_1": 0})
    self.setParms({f"{n.var_type_2}_1": 0})
    self.setParms({f"{n.var_type_3}_1": 0})
    self.setParms({f"{n.var_type_4}_1": 0})
    self.setParms({f"{n.postvar_type_1}_1": 0})
    # pre affine
    self.setParms({f"{n.preaffine_x}_1": hou.Vector2((0.5, 0.0))})
    self.setParms({f"{n.preaffine_y}_1": hou.Vector2((0.0, 0.5))})
    self.setParms({f"{n.preaffine_o}_1": hou.Vector2((0.0, 0.51225))})

    # iter 2
    #
    # shader
    self.setParms({f"{n.shader_color}_2": 0.5})
    self.setParms({f"{n.shader_speed}_2": -0.5})
    # vars
    self.setParms({f"{n.prevar_type_1}_2": 0})
    self.setParms({f"{n.prevar_type_2}_2": 0})
    self.setParms({f"{n.var_type_1}_2": 0})
    self.setParms({f"{n.var_type_2}_2": 0})
    self.setParms({f"{n.var_type_3}_2": 0})
    self.setParms({f"{n.var_type_4}_2": 0})
    self.setParms({f"{n.postvar_type_1}_2": 0})
    # pre affine
    self.setParms({f"{n.preaffine_x}_2": hou.Vector2((0.5, 0.0))})
    self.setParms({f"{n.preaffine_y}_2": hou.Vector2((0.0, 0.5))})
    self.setParms({f"{n.preaffine_o}_2": hou.Vector2((-0.29575, 0.0))})

    # iter 3
    #
    # shader
    self.setParms({f"{n.shader_color}_3": 1.0})
    self.setParms({f"{n.shader_speed}_3": -0.5})
    # vars
    self.setParms({f"{n.prevar_type_1}_3": 0})
    self.setParms({f"{n.prevar_type_2}_3": 0})
    self.setParms({f"{n.var_type_1}_3": 0})
    self.setParms({f"{n.var_type_2}_3": 0})
    self.setParms({f"{n.var_type_3}_3": 0})
    self.setParms({f"{n.var_type_4}_3": 0})
    self.setParms({f"{n.postvar_type_1}_3": 0})
    # pre affine
    self.setParms({f"{n.preaffine_x}_3": hou.Vector2((0.5, 0.0))})
    self.setParms({f"{n.preaffine_y}_3": hou.Vector2((0.0, 0.5))})
    self.setParms({f"{n.preaffine_o}_3": hou.Vector2((0.29575, 0.0))})






###############################################################################################
# Parameters reset if iterators count is set to ZERO.
###############################################################################################
def iteratorCountZero(self: hou.Node) -> None:
    """
    Args:
        self (hou.Node): [current hou.Node]
    """

    if not self.parm("flamefunc").evalAsInt():

        # delete channel references
        for p in self.parms():
            p.deleteAllKeyframes()

        # SYS
        self.setParms({"doff": 0})
        self.setParms({"rip": 0})
        
        # TM
        self.setParms({"dotm": 0})
        self.setParms({"tmrt": 0})
        
        # FF vars
        reset_FF(self)

        # SM
        self.setParms({"sm": 0})
        self.setParms({"smrot": 0})
        
        # MB
        self.setParms({"domb": 0})
        self.setParms({"fps": 24})
        self.setParms({"mbsamples": 16})
        self.setParms({"shutter": 0.5})
        
        #prefs
        self.setParms({"showprefs": 1})
        #self.setParms({"xm": 0})
        self.setParms({"camhandle": 0})
        self.setParms({"camcull": 0})
        #self.setParms({"fcam": ""})
        #self.setParms({"cullamount": 0.99})





###############################################################################################
# Open web browser to the FLAM3 for Houdini website
###############################################################################################
def web_flame3hda() -> None:
    page = "https://alexnardini.net/flame-home/"
    webbrowser.open(page)





###############################################################################################
# Open web browser to the FractalFlame Algorithm paper
###############################################################################################
def web_TFFA() -> None:
    page = "https://flam3.com/flame_draves.pdf"
    webbrowser.open(page)





# LOAD XML FLAME FILES start here



def make_VAR(name: Union[str, list[str], tuple[str]]) -> Union[Union[str, list[str]], None]:
    if type(name) is str:
        if name.startswith(V_PRX_PRE):
            return re.sub(REGEX_PRE, '', name)
        elif name.startswith(V_PRX_POST):
            return re.sub(REGEX_POST, '', name)
        else:
            return None
    elif type(name) is list or tuple:
        _names = [re.sub(REGEX_PRE, '', x) for x in name if x.startswith(V_PRX_PRE) is True]
        if not _names:
            _names = [re.sub(REGEX_POST, '', x) for x in name if x.startswith(V_PRX_PRE) is True]
        if not _names:
            return None
        else:
            return _names
    else:
        return None

def make_PRE(name: Union[str, list[str], tuple[str]]) -> Union[Union[str, list[str]], None]:
    if type(name) is str:
        if not (name.startswith(V_PRX_PRE) and name.startswith(V_PRX_POST)):
            return "pre_" + name
    elif type(name) is list or tuple:
        return ["pre_" + x for x in name if x.startswith(V_PRX_PRE) is False and x.startswith(V_PRX_POST) is False]
    else:
        return None

def make_POST(name: Union[str, list[str], tuple[str]]) -> Union[Union[str, list[str]], None]:
    if type(name) is str:
        if not (name.startswith(V_PRX_PRE) and name.startswith(V_PRX_POST)):
            return V_PRX_POST + name
    elif type(name) is list or tuple:
        return [V_PRX_POST + x for x in name if x.startswith(V_PRX_PRE) is False and x.startswith(V_PRX_POST) is False]
    else:
        return None



# XML
FLAME = "flame"
NAME = "name"
XF = "xform"
XF_WEIGHT = "weight"
XF_NAME = "name"
PB = "pre_blur"
FF = "finalxform"
PRE_AFFINE = "coefs"
POST_AFFINE = "post"
XAOS = "chaos"
PALETTE = "palette"
PALETTE_COUNT = "count"
PALETTE_FORMAT = "format"
COLOR = "color"
SYMMETRY = "symmetry"
COLOR_SPEED = "color_speed"
OPACITY = "opacity"
XML_VALID_FLAMES_ROOT_TAG = "flames"

XML_XF_KEY_EXCLUDE = ("weight", "color", "var_color", "symmetry", "color_speed", "name", "animate", "flatten", "pre_blur", "coefs", "post", "chaos", "opacity")
# The prm names inside here are allowed to pass a check even if not found in the XML.
# radial_blur var->"radial_blur_zoom" parameter is present into my implementation but not in Apo or Fractorium etc.
# so we allow it to pass anyway and set its value to zero inside FLAM3 for Houdini on load.
XML_XF_PRM_EXCEPTION = ("radial_blur_zoom", )

ITER_ON_LOAD_DEFAULT = 64

# REGEX_ALL = "(?s:.*?)"
REGEX_PRE = "^(?:pre_)"
REGEX_POST = "^(?:post_)"

V_PRX_PRE = "pre_"
V_PRX_POST = "post_"

MAX_ITER_VARS = 4
MAX_FF_VARS = 3
MAX_ITER_VARS_PRE = 2
MAX_ITER_VARS_POST = 1
MAX_FF_VARS_POST = 2

XML_APP_NAME_FRACTORIUM = "EMBER-"
XML_APP_NAME_APO = "Apophysis"


# This is used as a faster idx lookup table.
# From the XML's xforms, each variations look itself up inside here to get
# the corresponding FLAM3 for houdini var idx it is mapped to.
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
                        "polynomial": 101 }


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
    # They are gouped as follow and based on the FLAM3 Houdini node parametric parameters:
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
    # The (("variation_name") entrie, is not used here and only for reference, especially the initial index number.
    
    # Note:
    # radial_blur's parameter "radial_blur_zoom" is not used and always ZERO as everyone else only use "radiual_blur_angle".
    
    varsPRM = ( ("00 linear", 0), 
                ("01 sinusoidal", 0), 
                ("02 spherical", 0), 
                ("03 swirl", 0), 
                ("04 horseshoe", 0), 
                ("05 polar", 0), 
                ("06 handkerchief", 0), 
                ("07 heart", 0), 
                ("08 disc", 0), 
                ("09 spiral", 0), 
                ("10 hyperbolic", 0), 
                ("11 diamond", 0), 
                ("12 ex", 0), 
                ("13 julia", 0), 
                ("14 bent", 0), 
                ("15 waves", 0), 
                ("16 fisheye", 0), 
                ("17 popcorn", 0), 
                ("18 exponential", 0), 
                ("19 power", 0), 
                ("20 cosine", 0), 
                ("21 rings", 0), 
                ("22 fan", 0), 
                ("23 bubble", 0), 
                ("24 cylinder", 0), 
                ("25 eyefish", 0), 
                ("26 blur", 0), 
                ("27 curl", ("curl_c1", "curl_c2"), 1), 
                ("28 ngon", ("ngon_power", "ngon_sides", "ngon_corners", "ngon_circle"), 1), 
                ("29 pdj", ("pdj_a", "pdj_b", "pdj_c", "pdj_d"), 1), 
                ("30 blob", ("blob_low", "blob_high", "blob_waves"), 1), 
                ("31 juliaN", ("julian_power", "julian_dist"), 1), 
                ("32 juliascope", ("juliascope_power", "juiascope_dist"), 1), 
                ("33 gaussian_blur", 0), 
                ("34 fan2", ("fan2_x", "fan2_y"), 1), 
                ("35 rings2", ("rings2_val", ), 1), 
                ("36 rectangles", ("rectangles_x", "rectangles_y"), 1), 
                ("37 radial_blur", ("radial_blur_angle", "radial_blur_zoom"), 1), 
                ("38 pie", ("pie_slices", "pie_thickness", "pie_rotation"), 1), 
                ("39 arch", 0), 
                ("40 tangent", 0), 
                ("41 square", 0), 
                ("42 rays", 0), 
                ("43 blade", 0), 
                ("44 secant2", 0), 
                ("45 twintrian", 0), 
                ("46 cross", 0), 
                ("47 disc2", ("disc2_rot", "disc2_twist"), 1), 
                ("48 supershape", ("super_shape_m", "super_shape_rnd", "super_shape_holes"), ("super_shape_n1", "super_shape_n2", "super_shape_n3"), 1), 
                ("49 flower", ("flower_petals", "flower_holes"), 1), 
                ("50 conic", ("conic_eccentricity", "conic_holes"), 1), 
                ("51 parabola", ("parabola_height", "parabola_width"), 1), 
                ("52 bent2", ("bent2_x", "bent2_y"), 1), 
                ("53 bipolar", ("bipolar_shift", ), 1),
                ("54 boarders", 0),
                ("55 butterfly", 0), 
                ("56 cell", ("cell_size", ), 1), 
                ("57 cpow", ("cpow_power", "cpow_r", "cpow_i"), 1), 
                ("58 edisc", 0), 
                ("59 elliptic", 0), 
                ("60 noise", 0), 
                ("61 escher", ("escher_beta", ), 1), 
                ("62 foci", 0), 
                ("63 lazysusan", ("lazysusan_x", "lazysusan_y"), ("lazysusan_spin", "lazysusan_twist", "lazysusan_space"), 1), 
                ("64 loonie", 0), 
                ("65 pre blur", 0), 
                ("66 modulus", ("modulus_x", "modulus_y"), 1), 
                ("67 oscope", ("oscope_frequency", "oscope_amplitude", "oscope_damping", "oscope_separation"), 1), 
                ("68 polar2", 0), 
                ("69 popcorn2", ("popcorn2_c", "popcorn2_x"), ("popcorn2_y"), 1), 
                ("70 scry", 0), 
                ("71 separation", ("separation_x", "separation_y"), ("separation_xinside", "separation_yinside"), 1), 
                ("72 split", ("split_xsize", "split_ysize"), 1), 
                ("73 splits", ("splits_x", "splits_y"), 1), 
                ("74 stripes", ("stripes_space", "stripes_warp"), 1), 
                ("75 wedge", ("wedge_swirl", "wedge_angle", "wedge_hole", "wedge_count", ), 1), 
                ("76 wedge_julia", ("wedge_julia_power", "wedge_julia_angle", "wedge_julia_dist", "wedge_julia_count"), 1), 
                ("77 wedge_sph", ("wedge_sph_swirl", "wedge_sph_angle", "wedge_sph_hole", "wedge_sph_count"), 1), 
                ("78 whorl", ("whorl_inside", "whorl_outside"), 1), 
                ("79 waves2", ("waves2_scalex", "waves2_scaley"), ("waves2_freqx", "waves2_freqy"), 1), 
                ("80 exp", 0), 
                ("81 log", 0), 
                ("82 sin", 0), 
                ("83 cos", 0), 
                ("84 tan", 0), 
                ("85 sec", 0), 
                ("86 csc", 0), 
                ("87 cot", 0), 
                ("88 sinh", 0), 
                ("89 cosh", 0), 
                ("90 tanh", 0), 
                ("91 sech", 0), 
                ("92 csch", 0), 
                ("93 coth", 0), 
                ("94 auger", ("auger_freq", "auger_scale", "auger_sym", "auger_weight"), 1), 
                ("95 flux", ("flux_spread", ), 1), 
                ("96 mobius", ("re_a", "re_b", "re_c", "re_d"), ("im_a", "im_b", "im_c", "im_d"), 1),
                ("97 curve", ("curve_xlength", "curve_ylength"), ("curve_xamp", "curve_yamp"), 1), 
                ("98 persp", ("perspective_angle", "perspective_dist"), 1), 
                ("99 bwraps", ("bwraps_cellsize", "bwraps_space", "bwraps_gain"), ("bwraps_inner_twist", "bwraps_outer_twist"), 1), 
                ("100 hemisphere", 0), 
                ("101 polynomial", ("polynomial_powx", "polynomial_powy"), ("polynomial_lcx", "polynomial_lcy"), ("polynomial_scx", "polynomial_scy"), 1) )


    # EXCEPTIONS: so I dnt go into regex...
    # Update def prm_name_exceptions() if you add/find more
    fractorium_96_var_prm_mobius = ("96 mobius", ("mobius_re_a", "mobius_re_b", "mobius_re_c", "mobius_re_d"), ("mobius_im_a", "mobius_im_b", "mobius_im_c", "mobius_im_d"), 1),
    fractorium_67_var_prm_oscope = ("67 oscilloscope", ("oscilloscope_frequency", "oscilloscope_amplitude", "oscilloscope_damping", "oscilloscope_separation"), 1), 



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
                if XML_VALID_FLAMES_ROOT_TAG in root.tag:
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
    

    
    def __get_name(self, key=NAME) -> Union[tuple, None]:
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
        
    def __get_flame(self, key=FLAME) -> Union[tuple, None]:
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

    def __init__(self, xmlfile: str) -> None:
        """
        Args:
            xmlfile (str): [xml *.flame v_type file to load]
        """        
        super().__init__(xmlfile)
        self._name = self._xml_tree__get_name()
        self._apo_version = self._xml_tree__get_name("version")
        self._flame = self._xml_tree__get_flame()
        self._flame_count = self._xml_tree__get_flame_count(self._flame)
        

    def hex_to_rgb(self, hex: str):
        """
        Args:
            hex ([v_type]): [hex value to be converted into rgb value]

        Returns:
            [v_type]: [rgb value]
        """        
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    
    def affine_coupling(self, affine: list) -> list:
        """
        Args:
            affine (list): [affine values from the xml]

        Returns:
            list: [a list of hou.Vector2: ((X.x, X.y), (Y.x, Y.y), (O.x, O.y)) ready to be used to set affine parms]
        """        
        return [hou.Vector2((tuple(affine[i:i+2]))) for i in (0, 2, 4)]
    

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
    
    def __get_xaos(self, xforms: list, key=XAOS) -> Union[tuple, None]:
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
                        if key in XF_NAME:
                            keyvalues.append(xform.get(key))
                        else:
                            keyvalues.append(float(xform.get(key)))
                    else:
                        keyvalues.append([])
                return tuple(keyvalues)
        else:
            return None

        
    def __get_palette(self, idx: int, key=PALETTE) -> Union[tuple[hou.Ramp, int, str], None]:
        """
        Args:
            tree (Type[ET.ElementTree]): [a valid xml.etree.ElementTree tree]
            idx (int): [flame idx out of all flames included in the loaded flame file]

        Returns:
            hou.Ramp: [return an already made hou.Ramp with values from the flame xml palette]
        """        
        if  self._isvalidtree:
            palette_hex = self._flame[idx].find(key).text
            palette_attrib = self._flame[idx].find(key).attrib
            count = int(palette_attrib.get(PALETTE_COUNT)) - 1
            # optional
            format = dict(palette_attrib).get(PALETTE_FORMAT)
    
            HEX = []
            for line in palette_hex.splitlines():
                cleandoc = inspect.cleandoc(line)
                if(len(cleandoc)>1):
                    [HEX.append(hex) for hex in wrap(cleandoc, 6)]
    
            RGB = []
            for hex in HEX:
                x = self.hex_to_rgb(hex)
                RGB.append((x[0]/(count + 0.0), x[1]/(count + 0.0), x[2]/(count + 0.0)))
    
            POS = list(iter_islice(iter_count(0,1.0/count), (count+1)))
            BASES = [hou.rampBasis.Linear] * (count + 1)
            
            return hou.Ramp(BASES, POS, RGB), (count+1), str(format)
        else:
            return None





class apo_flame_iter_data(apo_flame):

    def __init__(self, xmlfile: str, idx=0) -> None:
        """
        Args:
            xmlfile (str): xmlfile (str): [xml flame v_type file to load]
            idx (int, optional): [flame idx out of all flames included in the loaded flame file]. Defaults to 0.
        """        
        super().__init__(xmlfile)
        self._idx = self._apo_flame__is_valid_idx(idx)
        self._xforms = self._apo_flame__get_xforms(self._idx, XF)
        self._xf_name = self._apo_flame__get_keyvalue(self._xforms, XF_NAME)
        self._weight = self._apo_flame__get_keyvalue(self._xforms, XF_WEIGHT)
        self._pre_blur = self._apo_flame__get_keyvalue(self._xforms, PB)
        self._xaos  = self._apo_flame__get_xaos(self._xforms)
        self._coefs = self._apo_flame__get_affine(self._xforms, PRE_AFFINE)
        self._post  = self._apo_flame__get_affine(self._xforms, POST_AFFINE)
        self._finalxform = self._apo_flame__get_xforms(self._idx, FF)
        self._finalxform_coefs = self._apo_flame__get_affine(self._finalxform, PRE_AFFINE)
        self._finalxform_post  = self._apo_flame__get_affine(self._finalxform, POST_AFFINE)
        self._palette = self._apo_flame__get_palette(self._idx)
        self._color = self._apo_flame__get_keyvalue(self._xforms, COLOR)
        self._color_speed = self._apo_flame__get_keyvalue(self._xforms, COLOR_SPEED)
        self._symmetry = self._apo_flame__get_keyvalue(self._xforms, SYMMETRY)
        self._opacity = self._apo_flame__get_keyvalue(self._xforms, OPACITY)


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
    def weight(self):
        return self._weight
    
    @property
    def pre_blur(self):
        return self._pre_blur
    
    @property
    def finalxform(self):
        return self._finalxform
         
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
    
    
    
    
    
###############################################################################################
# MENU - APO - build menu from flame file presets
###############################################################################################
def menu_apo_presets(kwargs: dict) -> list:

    xml = kwargs['node'].parm('apofilepath').evalAsString()
    menu=[]
    if apo_flame(xml).isvalidtree:
        apo = apo_flame(xml)
        names = apo.name
        for i, item in enumerate(apo.name):
            menu.append(i)
            menu.append(item)
            
        return menu
    else:
        return menu




# Use this with everything but not PRE and POST dictionary lookup, use def get_xforms_var_keys_PP() instead
def get_xforms_var_keys(xforms: tuple, vars: Union[list, tuple, dict]) -> Union[list[str], None]:
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
                vars_keys.append(list(map(lambda x: x, filter(lambda x: x in vars.get(x[0]), filter(lambda x: x not in XML_XF_KEY_EXCLUDE, xf.keys())))))
        else:
            for xf in xforms:
                vars_keys.append(list(map(lambda x: x, filter(lambda x: x in vars, filter(lambda x: x not in XML_XF_KEY_EXCLUDE, xf.keys())))))
            
        return vars_keys
    else:
        return None


def removeprefix(self: str, prefix: str) -> str:
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]
# to be used with VARS_FRACTORIUM_DICT - ONLY for PRE and POST lookup
def get_xforms_var_keys_PP(xforms: tuple, vars: dict, prx: str) -> Union[list[str], None]:
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
             vars_keys.append(list(map(lambda x: x, filter(lambda x: x in vars.get(removeprefix(x, prx)[0]), filter(lambda x: x.startswith(prx), xf.keys())))))
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
    if len(data) == 1:
        return float(data[0])
    elif len(data) == 2:
        return hou.Vector2((data))
    elif len(data) == 3:
        return hou.Vector3((data))
    elif len(data) == 4:
        return hou.Vector4((data))
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



def apo_set_affine(mode: int, node: hou.Node, prx: str, apo_data: apo_flame_iter_data, n: flam3_iterator_prm_names, mp_idx: int) -> None:
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
        node.setParms({f"{prx}{n.preaffine_x}": apo_data.finalxform_coefs[mp_idx][0]})
        node.setParms({f"{prx}{n.preaffine_y}": apo_data.finalxform_coefs[mp_idx][1]})
        node.setParms({f"{prx}{n.preaffine_o}": apo_data.finalxform_coefs[mp_idx][2]})
        if apo_data.finalxform_post is not None:
            node.setParms({f"{prx}{n.postaffine_do}": 1})
            node.setParms({f"{prx}{n.postaffine_x}": apo_data.finalxform_post[mp_idx][0]})
            node.setParms({f"{prx}{n.postaffine_y}": apo_data.finalxform_post[mp_idx][1]})
            node.setParms({f"{prx}{n.postaffine_o}": apo_data.finalxform_post[mp_idx][2]})
    else:
        node.setParms({f"{prx}{n.preaffine_x}_{str(mp_idx+1)}": apo_data.coefs[mp_idx][0]})
        node.setParms({f"{prx}{n.preaffine_y}_{str(mp_idx+1)}": apo_data.coefs[mp_idx][1]})
        node.setParms({f"{prx}{n.preaffine_o}_{str(mp_idx+1)}": apo_data.coefs[mp_idx][2]})
        if apo_data.post is not None:
            if apo_data.post[mp_idx]:
                node.setParms({f"{prx}{n.postaffine_do}_{str(mp_idx+1)}": 1})
                node.setParms({f"{prx}{n.postaffine_x}_{str(mp_idx+1)}": apo_data.post[mp_idx][0]})
                node.setParms({f"{prx}{n.postaffine_y}_{str(mp_idx+1)}": apo_data.post[mp_idx][1]})
                node.setParms({f"{prx}{n.postaffine_o}_{str(mp_idx+1)}": apo_data.post[mp_idx][2]})





def apo_set_data(mode: int, node: hou.Node, prx: str, apo_data: list, prm_name: str, mp_idx: int) -> None:
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
            if prm_name not in n.shader_alpha:
                if apo_data[mp_idx]:
                    node.setParms({f"{prx}{prm_name}_{str(mp_idx+1)}": apo_data[mp_idx]})
            else:
                node.setParms({f"{prx}{prm_name}_{str(mp_idx+1)}": apo_data[mp_idx]})
            


def prm_name_exceptions(v_type: int, app: str, apo_prm: tuple) -> tuple:
    if v_type == 96 and app.startswith(XML_APP_NAME_FRACTORIUM):
        return flam3_varsPRM_APO.fractorium_96_var_prm_mobius[0]
    elif v_type == 67 and app.startswith(XML_APP_NAME_FRACTORIUM):
        return flam3_varsPRM_APO.fractorium_67_var_prm_oscope[0]
    else:
        return apo_prm



def var_name_from_dict(mydict: dict, idx: int):
    return list(mydict.keys())[list(mydict.values()).index(idx)]
def v_parametric(app: str, mode: int, node: hou.Node, mp_idx: int, t_idx: int, xform: dict, v_type: int, v_weight: float, var_prm: tuple, apo_prm: tuple) -> None:
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

    VAR: list = []
    for names in apo_prm[1:-1]:
        var_prm_vals: list = []
        for n in names:
            # If one of the FLAM3 parameter is not in the xform, skip it and set it to ZERO for now.
            # This allow me to use "radial_blur" variation as everyone else
            # only have "radial_blur_angle" and not "radial_blur_zoom".
            if xform.get(n) is not None:
                for k in xform.keys():
                    if n in k:
                        var_prm_vals.append(float(str(xform.get(k))))
                        break
            else:
                var_prm_vals.append(float(0))
                # If a prm name is not found inside the XML, let us know unless is included in the exception tuple.
                if n not in XML_XF_PRM_EXCEPTION:
                    print(f"{str(node)}: PARAMETER NOT FOUND: Iterator.{mp_idx+1}: variation: \"{var_name_from_dict(VARS_FLAM3_DICT_IDX, v_type)}\": parameter: \"{n}\"")
            
        VAR.append(typemaker(var_prm_vals))

    for idx, prm in enumerate(var_prm[1:-1]):
        if mode: node.setParms({f"{prx_prm}{prm[0][:-1]}": VAR[idx]})
        else: node.setParms({f"{prx_prm}{prm[0]}{str(mp_idx+1)}": VAR[idx]})

    if mode:
        node.setParms({f"{prx}{flam3_iterator.sec_varsT[t_idx][:-1]}": v_type})
        node.setParms({f"{prx}{flam3_iterator.sec_varsW[t_idx][0][:-1]}": v_weight})
    else:
        node.setParms({f"{prx}{flam3_iterator.sec_varsT[t_idx]}{str(mp_idx+1)}": v_type})
        node.setParms({f"{prx}{flam3_iterator.sec_varsW[t_idx][0]}{str(mp_idx+1)}": v_weight})
        
        


def v_parametric_PRE(app: str, mode: int, node: hou.Node, mp_idx: int, t_idx: int, xform: dict, v_type: int, v_weight: float, var_prm: tuple, apo_prm: tuple) -> None:
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

    VAR: list = []
    for names in apo_prm[1:-1]:
        var_prm_vals: list = []
        for n in names:
            # If one of the FLAM3 parameter is not in the xform, skip it and set it to ZERO for now.
            # This allow me to use "radial_blur" variation as everyone else
            # only have "radial_blur_angle" and not "radial_blur_zoom".
            n_pre = make_PRE(n)
            if xform.get(n_pre) is not None:
                for k in xform.keys():
                    if n_pre in k:
                        var_prm_vals.append(float(str(xform.get(k))))
                        break
            else:
                var_prm_vals.append(float(0))
                if n not in XML_XF_PRM_EXCEPTION:
                    # If a variation parameter FLAM3 has is not found, set it to ZERO. Print its name to let us know in not inside XML_XF_PRM_EXCEPTION
                    print(f"{str(node)}: PARAMETER NOT FOUND: Iterator.{mp_idx+1}: variation: \"{make_PRE(var_name_from_dict(VARS_FLAM3_DICT_IDX, v_type))}\": parameter: \"{make_PRE(n)}\"")
            
        VAR.append(typemaker(var_prm_vals))
        
    for idx, prm in enumerate(var_prm[1:-1]):
        node.setParms({f"{prx_prm}{prm[0]}{str(mp_idx+1)}": VAR[idx]})

    # Only on pre variations with parametric so:
    # idx set by hand for now: flam3_iterator.sec_prevarsT[1] ... because in here we have a non parametric as first"
    # idx set by hand for now: flam3_iterator.sec_prevarsW[2][0] ... because in here we have "pre_blur" and a non parametric as first"
    node.setParms({f"{prx}{flam3_iterator.sec_prevarsT[t_idx]}{str(mp_idx+1)}": v_type})
    node.setParms({f"{prx}{flam3_iterator.sec_prevarsW[t_idx+1][0]}{str(mp_idx+1)}": v_weight})





def v_parametric_POST(app: str, mode: int, node: hou.Node, mp_idx: int, t_idx: int, xform: dict, v_type: int, v_weight: float, var_prm: tuple, apo_prm: tuple) -> None:
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

    VAR: list = []
    for names in apo_prm[1:-1]:
        var_prm_vals: list = []
        for n in names:
            # If one of the FLAM3 parameter is not in the xform, skip it and set it to ZERO for now.
            # This allow me to use "radial_blur" variation as everyone else
            # only have "radial_blur_angle" and not "radial_blur_zoom".
            n_post = make_POST(n)
            if xform.get(n_post) is not None:
                for k in xform.keys():
                    if n_post in k:
                        var_prm_vals.append(float(str(xform.get(k))))
                        break
            else:
                var_prm_vals.append(float(0))
                if n not in XML_XF_PRM_EXCEPTION:
                    # If a variation parameter FLAM3 has is not found, set it to ZERO. Print its name to let us know in not inside XML_XF_PRM_EXCEPTION
                    print(f"{str(node)}: PARAMETER NOT FOUND: Iterator.{mp_idx+1}: variation: \"{make_POST(var_name_from_dict(VARS_FLAM3_DICT_IDX, v_type))}\": parameter: \"{make_POST(n)}\"")
            
        VAR.append(typemaker(var_prm_vals))
        
    for idx, prm in enumerate(var_prm[1:-1]):
        node.setParms({f"{prx_prm}{prm[0]}{str(mp_idx+1)}": VAR[idx]})

    # Only on post variation with parametric so:
    # idx set by hand for now: flam3_iterator.sec_prevarsT[0]
    # idx set by hand for now: flam3_iterator.sec_prevarsW[0]
    node.setParms({f"{prx}{flam3_iterator.sec_postvarsT[0]}{str(mp_idx+1)}": v_type})
    node.setParms({f"{prx}{flam3_iterator.sec_postvarsW[0][0]}{str(mp_idx+1)}": v_weight})
    
    
    
    
def v_parametric_POST_FF(app: str, node: hou.Node, mp_idx: int, t_idx: int, xform: dict, v_type: int, v_weight: float, var_prm: tuple, apo_prm: tuple) -> None:
    """
    Args:
        app (str): [What software were used to generate this flame preset]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [for multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        t_idx (int): [current variation number idx to use with: flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW]
        xform (dict): [current xform we are processing to the relative key names and values for the iterator]
        v_type (int): [the current variation type index]
        weight (float): [the current variation weight]
        var_prm (tuple): [tuple of FLAM3 node parameteric parameters names: flam3_varsPRM.varsPRM[v_type]]
        apo_prm (tuple): [tuple of APO variation parametric parameters names: flam3_varsPRM_APO.varsPRM[v_type]]
    """
    prx_ff_prm_post = "fp1_"
    
    # Exceptions: check if this flame need different parameters names based on detected exception
    apo_prm = prm_name_exceptions(v_type, app, apo_prm)

    VAR: list = []
    for names in apo_prm[1:-1]:
        var_prm_vals: list = []
        for n in names:
            # If one of the FLAM3 parameter is not in the xform, skip it and set it to ZERO for now.
            # This allow me to use "radial_blur" variation as everyone else
            # only have "radial_blur_angle" and not "radial_blur_zoom".
            n_post = make_POST(n)
            if xform.get(n_post) is not None:
                for k in xform.keys():
                    if n_post in k:
                        var_prm_vals.append(float(str(xform.get(k))))
                        break
            else:
                var_prm_vals.append(float(0))
                if n not in XML_XF_PRM_EXCEPTION:
                    # If a variation parameter FLAM3 has is not found, set it to ZERO. Print its name to let us know in not inside XML_XF_PRM_EXCEPTION
                    print(f"{str(node)}: PARAMETER NOT FOUND: Iterator.{mp_idx+1}: variation: \"{make_POST(var_name_from_dict(VARS_FLAM3_DICT_IDX, v_type))}\": parameter: \"{make_POST(n)}\"")
            
        VAR.append(typemaker(var_prm_vals))
        
    for idx, prm in enumerate(var_prm[1:-1]):
        node.setParms({f"{prx_ff_prm_post}{prm[0][0:-1]}": VAR[idx]})

    # Only on post variation with parametric so:
    # idx set by hand for now: flam3_iterator.sec_prevarsT[0]
    # idx set by hand for now: flam3_iterator.sec_prevarsW[0]
    node.setParms({f"{flam3_iterator_FF.sec_postvarsT_FF[t_idx]}": v_type})
    node.setParms({f"{flam3_iterator_FF.sec_postvarsW_FF[t_idx][0]}": v_weight})




def v_generic(mode: int, node: hou.Node, mp_idx: int, t_idx: int, v_type: int, v_weight: float) -> None:
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
        node.setParms({f"{prx}{flam3_iterator.sec_varsT[t_idx][:-1]}": v_type})
        node.setParms({f"{prx}{flam3_iterator.sec_varsW[t_idx][0][:-1]}": v_weight})
    else:
        node.setParms({f"{prx}{flam3_iterator.sec_varsT[t_idx]}{str(mp_idx+1)}": v_type})
        node.setParms({f"{prx}{flam3_iterator.sec_varsW[t_idx][0]}{str(mp_idx+1)}":v_weight})
        
        
        
def v_generic_PRE(mode: int, node: hou.Node, mp_idx: int, t_idx: int, v_type: int, v_weight: float) -> None:
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

    # Only pre variations with no parametric so:
    # idx set by hand for now: flam3_iterator.sec_prevarsT[0]
    # idx set by hand for now: flam3_iterator.sec_prevarsW[1][0] ... because in here we have "pre_blur as first"
    node.setParms({f"{prx}{flam3_iterator.sec_prevarsT[t_idx]}{str(mp_idx+1)}": v_type})
    node.setParms({f"{prx}{flam3_iterator.sec_prevarsW[t_idx+1][0]}{str(mp_idx+1)}":v_weight})
        
    

def v_generic_POST(mode: int, node: hou.Node, mp_idx: int, t_idx: int, v_type: int, v_weight: float) -> None:
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

    # Only post variation with no parametric so:
    # idx set by hand for now: flam3_iterator.sec_prevarsT[0]
    # idx set by hand for now: flam3_iterator.sec_prevarsW[0][0]
    node.setParms({f"{prx}{flam3_iterator.sec_postvarsT[0]}{str(mp_idx+1)}": v_type})
    node.setParms({f"{prx}{flam3_iterator.sec_postvarsW[0][0]}{str(mp_idx+1)}":v_weight})



def v_generic_POST_FF(node: hou.Node, mp_idx: int, t_idx: int, v_type: int, v_weight: float) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        t_idx (int): [Current variation number idx to use with: flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW]
        v_type (int): [Current variation type index]
        weight (float): [Current variation weight]
    """

    node.setParms({f"{flam3_iterator_FF.sec_postvarsT_FF[t_idx]}": v_type})
    node.setParms({f"{flam3_iterator_FF.sec_postvarsW_FF[t_idx][0]}":v_weight})




def v_pre_blur(mode: int, node: hou.Node, mp_idx: int, t_idx: int, pb_weights: tuple) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        mp_idx (int): [Multiparameter index -> the xform count from the outer loop: (mp_idx + 1)]
        t_idx (int): [Current variation number idx to use with: flam3_iterator.sec_prevarsT, flam3_iterator.sec_prevarsW]
        pb_weights (tuple): [all iterators pre_blur weight values]
    """
    prx, prx_prm = flam3_prx_mode(mode)
    if mode: pass
    else:
        if pb_weights[mp_idx]:
            node.setParms({f"{prx}{flam3_iterator_prm_names.prevar_weight_blur}_{str(mp_idx+1)}": pb_weights[mp_idx]})




def apo_set_iterator(mode: int, node: hou.Node, apo_data: apo_flame_iter_data, preset_id: int) -> None:
    """
    Args:
        mode (int): [0 for iterator. 1 for FF]
        node (hou.Node): [Current FLAM3 houdini node]
        apo_data (apo_flame_iter_data): [Apophysis XML data collection from: class[apo_flame_iter_data]]
    """    

    # What software were used to generate this flame preset
    app = apo_data.apo_version[preset_id]

    xforms = ()
    max_vars = 0
    if mode:
        max_vars = MAX_FF_VARS
        xforms = apo_data.finalxform
    else:
        max_vars = MAX_ITER_VARS
        xforms = apo_data.xforms

    iterator_names = flam3_iterator_prm_names()
    prx, prx_prm = flam3_prx_mode(mode)

    var_prm: tuple = flam3_varsPRM.varsPRM
    apo_prm: tuple = flam3_varsPRM_APO.varsPRM
    vars_keys = get_xforms_var_keys(xforms, VARS_FLAM3_DICT_IDX.keys())
    vars_keys_pre = get_xforms_var_keys(xforms, make_PRE(VARS_FLAM3_DICT_IDX.keys()))
    vars_keys_post = get_xforms_var_keys(xforms, make_POST(VARS_FLAM3_DICT_IDX.keys()))


    # Set variations ( iterator and FF )
    for mp_idx, xform in enumerate(xforms):
        for t_idx, key_name in enumerate(vars_keys[mp_idx][:max_vars]):
            v_type = apo_get_idx_by_key(key_name)
            if v_type is not None:
                v_weight: float = float(xform.get(key_name))
                if apo_prm[v_type][-1]:
                    v_parametric(app, mode, node, mp_idx, t_idx, xform, v_type, v_weight, var_prm[v_type], apo_prm[v_type])
                else:
                    v_pre_blur(mode, node, mp_idx, t_idx, apo_data.pre_blur)
                    v_generic(mode, node, mp_idx, t_idx, v_type, v_weight)

            else:
                # if this variation is not found, set it to Linear and its weight to ZERO
                v_generic(mode, node, mp_idx, t_idx, 0, 0)
                
        if mode:
            # FF POST vars in this iterator ( only the first two in "vars_keys_post[mp_idx]" will be kept )
            if vars_keys_post[mp_idx]:
                for t_idx, key_name in enumerate(vars_keys_post[mp_idx][:MAX_FF_VARS_POST]):
                    v_type = apo_get_idx_by_key(make_VAR(key_name))
                    if v_type is not None:
                        v_weight: float = float(xform.get(key_name))
                        if apo_prm[v_type][-1]:
                            v_parametric_POST_FF(app, node, mp_idx, t_idx, xform, v_type, v_weight, var_prm[v_type], apo_prm[v_type])
                        else:
                            v_generic_POST_FF(node, mp_idx, t_idx, v_type, v_weight)
                            
        else:
            # PRE vars in this iterator ( only the first two in "vars_keys_pre[mp_idx]" will be kept )
            # For now the execution order will always be:
            # -> First: non parametric.
            # -> Second: parametric.
            if vars_keys_pre[mp_idx]:
                for t_idx, key_name in enumerate(vars_keys_pre[mp_idx][:MAX_ITER_VARS_PRE]):
                    v_type = apo_get_idx_by_key(make_VAR(key_name))
                    if v_type is not None:
                        v_weight: float = float(xform.get(key_name))
                        if apo_prm[v_type][-1]:
                            v_parametric_PRE(app, mode, node, mp_idx, t_idx, xform, v_type, v_weight, var_prm[v_type], apo_prm[v_type])
                        else:
                            v_generic_PRE(mode, node, mp_idx, t_idx, v_type, v_weight)
                            
            # POST vars in this iterator ( only the first one in "vars_keys_post[mp_idx]" will be kept )
            if vars_keys_post[mp_idx]:
                for t_idx, key_name in enumerate(vars_keys_post[mp_idx][:MAX_ITER_VARS_POST]):
                    v_type = apo_get_idx_by_key(make_VAR(key_name))
                    if v_type is not None:
                        v_weight: float = float(xform.get(key_name))
                        if apo_prm[v_type][-1]:
                            v_parametric_POST(app, mode, node, mp_idx, t_idx, xform, v_type, v_weight, var_prm[v_type], apo_prm[v_type])
                        else:
                            v_generic_POST(mode, node, mp_idx, t_idx, v_type, v_weight)
                            
            # Activate iterator, just in case...
            node.setParms({f"{iterator_names.main_vactive}_{str(mp_idx+1)}": 1})
            # Set the rest of the iterators
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
    self.setParms({"iter": iter_on_load})




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
    preset_name = self.parm('apopresets').menuLabels()[preset_id]

    iter_on_load_preset = get_preset_name_iternum(preset_name)
    if iter_on_load_preset is not None:
        iter_on_load = iter_on_load_preset
        self.setParms({"iternumonload": iter_on_load})
        self.setParms({"useiteronload": 0})
    else:
        if not use_iter_on_load:
            iter_on_load = ITER_ON_LOAD_DEFAULT
            self.setParms({"iternumonload": ITER_ON_LOAD_DEFAULT})
    return iter_on_load    

    


def apo_to_flam3(self: hou.Node) -> None:

    xml = self.parm('apofilepath').evalAsString()

    if apo_flame(xml).isvalidtree:
        
        preset_id = int(self.parm('apopresets').eval())
        iter_on_load = set_iter_on_load(self, preset_id)

        reset_SYS(self, 500000, iter_on_load, 0)
        reset_TM(self)
        reset_SM(self)
        reset_MB(self)
        reset_PREFS(self)
        
        apo_data = apo_flame_iter_data(xml, preset_id)
        if min(apo_data.opacity) == 0.0:
            self.setParms({"rip": 1})

        # iterators
        self.setParms({"flamefunc": 0})
        for p in self.parms():
            p.deleteAllKeyframes()
        self.setParms({"flamefunc":  len(apo_data.xforms)})
        apo_set_iterator(0, self, apo_data, preset_id)
        # if FF
        if apo_data.finalxform is not None:
            reset_FF(self)
            self.setParms({"doff": 1})
            apo_set_iterator(1, self, apo_data, preset_id)
        else:
            reset_FF(self)
            self.setParms({"doff": 0})

        # CP
        self.setParms({RAMP_HSV_VAL_NAME: hou.Vector3((0.0, 1.0, 1.0))})
        ramp_parm = self.parm(RAMP_SRC_NAME)
        ramp_parm.deleteAllKeyframes()
        # Set XML palette data
        ramp_parm.set(apo_data.palette[0])
        palette_cp(self)
        palette_hsv(self)
        
        #Updated flame stats 
        self.setParms({"flamestats_msg": apo_load_stats_msg(self, preset_id, apo_data)})
        
    else:
        if os.path.isfile(xml) and os.path.getsize(xml)>0:
            self.setParms({"flamestats_msg": "Please load a valid *.flame file."})
            # The following do not work, not sure why
            self.setParms({"descriptive_msg": ""})
        else:
            self.setParms({"flamestats_msg": ""})
            # The following do not work, not sure why
            self.setParms({"descriptive_msg": ""})




def apo_load_stats_msg(self: hou.Node, preset_id: int, apo_data: apo_flame_iter_data) -> str:
    
    # spacers
    nl = "\n"
    nnl = "\n\n"
    
    # checks
    pb_bool = False
    for item in apo_data.pre_blur:
        if item:
            pb_bool = True
            break
    opacity_bool = False
    post_bool = False
    xaos_bool = False
    ff_bool = False
    ff_post_bool = False
    if min(apo_data.opacity) == 0.0:
        opacity_bool = True
    if apo_data.post is not None:
        post_bool = True
    if apo_data.xaos is not None:
        xaos_bool = True
    if apo_data.finalxform is not None:
        ff_bool = True
    if apo_data.finalxform_post is not None:
        ff_post_bool = True
        
    # checks msgs
    opacity_bool_msg = "NO"
    post_bool_msg = "NO"
    xaos_bool_msg = "NO"
    ff_post_bool_msg = "NO"
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
    ff_msg = ""
    if ff_bool:
        ff_msg = f"FF: YES\nFF post affine: {ff_post_bool_msg}"
    else:
        ff_msg = f"FF: NO"
    palette_count_format = f"Palette count: {apo_data.palette[1]}, format: {apo_data.palette[2]}"
    var_used_heading = "Variations used:"
    
    # get all vars used
    vars_keys = get_xforms_var_keys(apo_data.xforms, VARS_FLAM3_DICT_IDX.keys())
    # get all pre vars used
    vars_keys_PRE = get_xforms_var_keys(apo_data.xforms, make_PRE(VARS_FLAM3_DICT_IDX.keys()))
    # get all post vars used
    vars_keys_POST = get_xforms_var_keys(apo_data.xforms, make_POST(VARS_FLAM3_DICT_IDX.keys()))
    # FF
    vars_keys_FF = []
    vars_keys_POST_FF = []
    if ff_bool:
        # get allFF vars used
        vars_keys_FF = get_xforms_var_keys(apo_data.finalxform, VARS_FLAM3_DICT_IDX.keys())
        # get all FF post vars used
        vars_keys_POST_FF = get_xforms_var_keys(apo_data.finalxform, make_POST(VARS_FLAM3_DICT_IDX.keys()))
    vars_all = vars_keys_PRE + vars_keys + vars_keys_POST + vars_keys_FF + vars_keys_POST_FF
    # add pre_blur is used
    if pb_bool:
        vars_all += [["pre_blur"]] + vars_keys_PRE + vars_keys_POST
        
    # flatten, sort and build vars used msg
    flatten = [item for sublist in vars_all for item in sublist]
    result = []
    [result.append(x) for x in flatten if x not in result]
    result_sorted = sorted(result, key=lambda var: var)
    n = 5
    result_grp = [result_sorted[i:i+n] for i in range(0, len(result_sorted), n)]  
    vars = []
    for grp in result_grp:
        vars.append(", ".join(grp) + "\n")
    vars_txt = "".join(vars)
    vars_used_msg = f"{var_used_heading}\n{vars_txt}"
    
    # Build and set descriptive parameter msg
    preset_name = self.parm('apopresets').menuLabels()[preset_id]
    descriptive_prm = ( f"sw: {apo_data.apo_version[preset_id]}\n",
                        f"{preset_name}", )
    self.setParms({"descriptive_msg": "".join(descriptive_prm)})

    
    
    # Build missing:

    # get all vars
    vars_keys_from_fractorium = get_xforms_var_keys(apo_data.xforms, VARS_FRACTORIUM_DICT)
    # get all pre vars
    vars_keys_from_fractorium_pre = get_xforms_var_keys_PP(apo_data.xforms, VARS_FRACTORIUM_DICT_PRE, V_PRX_PRE)
    # get all post vars
    vars_keys_from_fractorium_post = get_xforms_var_keys_PP(apo_data.xforms, VARS_FRACTORIUM_DICT_POST, V_PRX_POST)
    # get all FF vars
    vars_keys_from_fractorium_FF = []
    vars_keys_from_fractorium_post_FF = []
    if ff_bool:
        # get all FF vars
        vars_keys_from_fractorium_FF = get_xforms_var_keys(apo_data.finalxform, VARS_FRACTORIUM_DICT)
        # get all FF post vars
        vars_keys_from_fractorium_post_FF = get_xforms_var_keys_PP(apo_data.finalxform, VARS_FRACTORIUM_DICT_POST, V_PRX_POST)
    # flatten and sort all vars
    vars_keys_from_fractorium_all = vars_keys_from_fractorium + vars_keys_from_fractorium_pre + vars_keys_from_fractorium_post + vars_keys_from_fractorium_FF + vars_keys_from_fractorium_post_FF
    flatten_fractorium = [item for sublist in vars_keys_from_fractorium_all for item in sublist]
    result_fractorium = []
    [result_fractorium.append(x) for x in flatten_fractorium if x not in result_fractorium]
    result_sorted_fractorium = sorted(result_fractorium, key=lambda var: var)
    
    # Compare and keep and build missing vars msg
    vars_missing = [x for x in result_sorted_fractorium if x not in result_sorted]
    result_grp_fractorium = [vars_missing[i:i+n] for i in range(0, len(vars_missing), n)]  
    missing_vars = []
    for grp in result_grp_fractorium:
        missing_vars.append(", ".join(grp) + "\n")
    vars_missing = "".join(missing_vars)
    vars_missing_msg = ""
    if vars_missing:
        vars_missing_msg = f"MISSING:\n{vars_missing}"
        
    # build full stats msg
    build = ( sw, nnl,
              name, nl,
              palette_count_format, nnl,
              iter_count, nl,
              post, nl,
              opacity, nl,
              xaos, nl,
              ff_msg, nnl,
              vars_used_msg, nl,
              vars_missing_msg )
    build_stats_msg = "".join(build)
    
    return build_stats_msg




def flam3_about_msg(self):
    
    nl = "\n"
    nnl = "\n\n"

    flam3_houdini_version = "Version: 0.9.5"
    Implementation_years = "2020/2023"
    Implementation_build = f"Author: Alessandro Nardini\nCode language: CVEX H19.x, Python {python_version()}\n{flam3_houdini_version}\n{Implementation_years}"
    
    code_copied = """Code references:
flam3 :: (GPL v2)
Apophysis :: (GPL)
Fractorium :: (GPL v3)"""
    
    h_version = '.'.join(str(x) for x in hou.applicationVersion())
    Houdini_version = f"Host:\nSideFX Houdini {h_version}"
    license_type = str(hou.licenseCategory()).split(".")[-1]
    Houdini_license = f"License: {license_type}"
    Platform = f"Platform: {hou.applicationPlatformInfo()}"
    PC_name = f"Machine name: {hou.machineName()}"
    User = f"User: {hou.userName()}"
    
    example_flames = f"example Flames:\nC-91, Gabor Timar, Golubaja, Pillemaster,\nPlangkye, Tatasz, Triptychaos, TyrantWave, Zy0rg"
    
    build = (Implementation_build, nnl,
             code_copied, nnl,
             example_flames, nnl,
             Houdini_version, nl,
             Houdini_license, nl,
             Platform, nl,
             PC_name, nl,
             User)
    
    build_about_msg = "".join(build)
    
    self.setParms({"flam3about_msg": build_about_msg})
    
    
    
def flam3_about_plugins_msg(self):
    
    vars_sorted = sorted(VARS_FLAM3_DICT_IDX.keys()) 
    n = 6
    vars_sorted_grp = [vars_sorted[i:i+n] for i in range(0, len(vars_sorted), n)] 
    _vars = []
    for grp in vars_sorted_grp:
        _vars.append(", ".join(grp) + "\n")
    vars_txt = "".join(_vars)
    
    self.setParms({"flam3plugins_msg": vars_txt})


