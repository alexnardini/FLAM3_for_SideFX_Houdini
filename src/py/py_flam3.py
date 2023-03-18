import os, hou, json, colorsys, webbrowser





'''  
#   Title:      SideFX Houdini FLAM3: 2D
#   Author:     Alessandro Nardini
#   date:       January 2023, Last revised February 2023
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
'''





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
                ("hiperbolic", 0), 
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
                ("gaussian", 0), 
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
                ("cothe exp", 0), 
                ("cothe log", 0), 
                ("cothe sin", 0), 
                ("cothe cos", 0), 
                ("cothe tan", 0), 
                ("cothe sec", 0), 
                ("cothe csc", 0), 
                ("cothe cot", 0), 
                ("cothe sinh", 0), 
                ("cothe cosh", 0), 
                ("cothe tanh", 0), 
                ("cothe sech", 0), 
                ("cothe csch", 0), 
                ("cothe coth", 0), 
                (f"auger{PRM}", ("auger_", 1), 1), 
                (f"flux{PRM}", ("fluxspread_", 0), 1), 
                (f"mobius{PRM}", ("mobiusre_", 1), ("mobiusim_", 1), 1),
                (f"curve{PRM}", ("curvexyzlenght_", 1), ("curvexyzamp_", 1), 1), 
                (f"persp{PRM}", ("persp_", 1), 1), 
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
    for easy access everywhere I need.

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
        type = int(prm_from)
        if(varsPRM[type][-1]):
            
            paste_from_list(varsPRM[type][1:-1], node, flam3node, id, id_from)





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
    
    _current_note_FF = node.parm("ffnote").evalAsString()

    if int_mode == 0:
        _current_note = node.parm(f"note_{id}").evalAsString()
        # If on the same FLAM3 node
        if node == flam3node:
            if len(_current_note) == 0:
                node.setParms({f"note_{id}": f"iter.{id_from}{str_section}"})
            else:
                node.setParms({f"note_{id}": f"{paste_save_note(_current_note)}iter.{id_from}{str_section}"})
        else:
            if len(_current_note) == 0:
                node.setParms({f"note_{id}": f"{str(flam3node)}.iter.{id_from}{str_section}"})
            else:
                node.setParms({f"note_{id}": f"{paste_save_note(_current_note)}{str(flam3node)}.iter.{id_from}{str_section}"})
            print(f"{str(node)}: Copied values from: {str(flam3node)}.iter.{id_from}{str_section} to: {str(node)}.iter.{id}{str_section}")
    elif int_mode == 1:
        if node != flam3node:
            if len(_current_note_FF) == 0:
                node.setParms({'ffnote': f"{str(flam3node)}.FF"})
            else:
                node.setParms({'ffnote': f"{paste_save_note(_current_note_FF)}{str(flam3node)}.FF"})
            print(f"{str(node)}: Copied FF from: {str(flam3node)}.FF to: {str(node)}.FF")
    elif int_mode == 2:
        if node != flam3node:
            if len(_current_note_FF) == 0:
                node.setParms({'ffnote': f"{str(flam3node)}.FF{str_section}"})
            else:
                node.setParms({'ffnote': f"{paste_save_note(_current_note_FF)}{str(flam3node)}.FF{str_section}"})
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
        
        # Get user selection of paste methods
        paste_sel = node.parm(f"prmpastesel_{str(id)}").evalAsInt()

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
        node.setParms({f"prmpastesel_{str(id)}": str(0)})
    
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
        
        # Get user selection of paste methods
        ff_paste_sel = node.parm("ffprmpastesel").evalAsInt()

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
        node.setParms({"ffprmpastesel": str(0)})
                
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
# Init parameter presets menu list as soon as you load a valid ramp json file
###############################################################################################
def ramp_init_presets(kwargs: dict) -> None:
    """
    Args:
        kwargs (dict): [kwargs[] dictionary]
    """    
    node = kwargs['node']
    ramp_presets = node.parm('presets')
    ramp_presets.set('0')





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
# Load default values. ( Sierpinsky triangle )
###############################################################################################
def flam3_default(self: hou.Node) -> None:
    """
    Args:
        self (hou.Node): [current hou.Node]
    """    
    # Iterators reset
    self.setParms({"flamefunc": 0})
    # delete channel references
    for p in self.parms():
        p.deleteAllKeyframes()
    # Add back iterators
    # This way all parameters will reset to their default values.
    self.setParms({"flamefunc": 3})

    #
    # SYS
    self.setParms({"ptcount": 500000})
    self.setParms({"iter": 10})
    self.setParms({"doff": 0})
    self.setParms({"tag": 1})
    self.setParms({"tagsize": 0})
    self.setParms({"rip": 0})
    
    # TM
    self.setParms({"dotm": 0})
    self.setParms({"tmrt": 0})
    
    # FF vars
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
    self.setParms({"xm": 0})
    self.setParms({"camhandle": 0})
    self.setParms({"camcull": 0})
    self.setParms({"fcam": ""})
    self.setParms({"cullamount": 0.99})

    #######################################################################
    
    # iterators
    iter = flam3_iterator

    # Iterator 1
    #
    # shader
    self.setParms({f"{n.shader_color}_1": 0})
    self.setParms({f"{n.shader_speed}_1": 0.75})
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

    # Iterator 2
    #
    # shader
    self.setParms({f"{n.shader_color}_2": 0.5})
    self.setParms({f"{n.shader_speed}_2": 0.75})
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

    # Iterator 3
    #
    # shader
    self.setParms({f"{n.shader_color}_3": 1.0})
    self.setParms({f"{n.shader_speed}_3": 0.75})
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

    #######################################################################





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


