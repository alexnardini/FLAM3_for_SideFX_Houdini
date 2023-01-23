import hou
import os
import json
import webbrowser





'''  
    Title:      SideFX Houdini FLAM3: 2D
    Author:     Alessandro Nardini
    date:       January 2023, Last revised January 2023

    info:       Based on the original: "The Fractal Flame Algorithm"
    Authors:    Scott Draves, Erik Reckase

    Paper:      https://flam3.com/flame_draves.pdf
    Date:       September 2003, Last revised November 2008

    Github:     https://github.com/scottdraves/flam3
    Date:       December 2002, Last revised May 2015

    Name:       PY_FLAM3 "PYTHON"

    Comment:    Python classes and definitions for tool's user experience.
'''





class flam3_varsPRM:

    # Collect all variations and their parametric parameters.
    varsPRM = ( ["linear", 0], 
                ["sinusoidal", 0], 
                ["spherical", 0], 
                ["swirl", 0], 
                ["horseshoe", 0], 
                ["polar", 0], 
                ["handkerchief", 0], 
                ["heart", 0], 
                ["disc", 0], 
                ["spiral", 0], 
                ["hiperbolic", 0], 
                ["diamond", 0], 
                ["ex", 0], 
                ["julia", 0], 
                ["bent", 0], 
                ["*waves", 0], 
                ["fisheye", 0], 
                ["*popcorn", 0], 
                ["expo", 0], 
                ["power", 0], 
                ["cosine", 0], 
                ["*rings", 0], 
                ["*fan", 0], 
                ["bubble", 0], 
                ["cylinder", 0], 
                ["eyefish", 0], 
                ["blur", 0], 
                ["curl...", ["curlc_", 1], 1], 
                ["ngon...", ["ngon_", 1], 1], 
                ["pdj...", ["pdjw_", 1], 1], 
                ["blob...", ["blob_", 1], 1], 
                ["juliaN...", ["julian_", 1], 1], 
                ["juliascope...", ["juliascope_", 1], 1], 
                ["gaussian", 0], 
                ["fan2...", ["fan2_", 1], 1], 
                ["rings2...", ["rings2val_", 0], 1], 
                ["rectangles...", ["rectangles_", 1], 1], 
                ["radialblur...", ["radialblur_", 1], 1], 
                ["pie...", ["pie_", 1], 1], 
                ["arch", 0], 
                ["tangent", 0], 
                ["square", 0], 
                ["rays", 0], 
                ["blade", 0], 
                ["secant2", 0], 
                ["twintrian", 0], 
                ["cross", 0], 
                ["disc2...", ["disc2_", 1], 1], 
                ["supershape...", ["supershape_", 1], ["supershapen_", 1], 1], 
                ["flower...", ["flower_", 1], 1], 
                ["conic...", ["conic_", 1], 1], 
                ["parabola...", ["parabola_", 1], 1], 
                ["bent2...", ["bent2xy_", 1], 1], 
                ["bipolar...", ["bipolarshift_", 0], 1],
                ["boarders", 0],
                ["butterfly", 0], 
                ["cell...", ["cellsize_", 0], 1], 
                ["cpow...", ["cpow_", 1], 1], 
                ["edisc", 0], 
                ["elliptic", 0], 
                ["noise", 0], 
                ["escher...", ["escherbeta_", 0], 1], 
                ["foci", 0], 
                ["lazysusan...", ["lazysusanxyz_", 1], ["lazysusan_", 1], 1], 
                ["loonie", 0], 
                ["preblur", 0], 
                ["modulus...", ["modulusXYZ_", 1], 1], 
                ["oscope...", ["oscope_", 1], 1], 
                ["polar2", 0], 
                ["popcorn...", ["popcorn2xyz_", 1], ["popcorn2c_", 0], 1], 
                ["scry", 0], 
                ["separation...", ["separationxyz_", 1], ["separationinsidexyz_", 1], 1], 
                ["split...", ["splitxyz_", 1], 1], 
                ["splits...", ["splitsxyz_", 1], 1], 
                ["stripes...", ["stripes_", 1], 1], 
                ["wedge...", ["wedge_", 1], 1], 
                ["wedgejulia...", ["wedgejulia_", 1], 1], 
                ["wedgesph", ["wedgesph_", 1], 1], 
                ["whorl...", ["whorl_", 1], 1], 
                ["waves2...", ["waves2scalexyz_", 1], ["waves2freqxyz_", 1], 1], 
                ["cothe exp", 0], 
                ["cothe log", 0], 
                ["cothe sin", 0], 
                ["cothe cos", 0], 
                ["cothe tan", 0], 
                ["cothe sec", 0], 
                ["cothe csc", 0], 
                ["cothe cot", 0], 
                ["cothe sinh", 0], 
                ["cothe cosh", 0], 
                ["cothe tanh", 0], 
                ["cothe sech", 0], 
                ["cothe csch", 0], 
                ["cothe coth", 0], 
                ["auger...", ["auger_", 1], 1], 
                ["flux...", ["fluxspread_", 0], 1], 
                ["mobius...", ["mobiusre_", 1], ["mobiusim_", 1], 1],
                ["curve...", ["curvexyzlenght_", 1], ["curvexyzamp_", 1], 1], 
                ["persp...", ["persp_", 1], 1], 
                ["bwraps...", ["bwraps_", 1], ["bwrapstwist_", 1], 1], 
                ["hemisphere", 0], 
                ["polynomial...", ["polynomialpow_", 1], ["polynomiallc_", 1], ["polynomialsc_", 1], 1] )





    # SECTIONS method lists
    #
    # (*T)Types have no signature and always to be used with: pastePRM_T_from_list() for now.
    sec_main = [ ["vactive_", 0], ["iw_", 0] ]
    sec_xaos = [ ["varnote_", 0] ]
    sec_shader = [ ["clr_", 0], ["clrspeed_", 0], ["alpha_", 0] ]
    sec_prevarsT = [ "pre1type_", "pre2type_" ] # preblur is omitted as it is always ZERO
    sec_prevarsW = [ ["preblurweight_", 0], ["pre1weight_", 0], ["pre2weight_", 0] ]
    sec_varsT = [ "v1type_", "v2type_", "v3type_", "v4type_" ]
    sec_varsW = [ ["v1weight_", 0], ["v2weight_", 0], ["v3weight_", 0], ["v4weight_", 0] ]
    sec_postvarsT = [ "p1type_" ]
    sec_postvarsW = [ ["p1weight_", 0] ]
    sec_preAffine = [ ["x_", 1], ["y_", 1], ["o_", 1], ["ang_", 0] ]
    sec_postAffine = [ ["dopost_", 0], ["px_", 1], ["py_", 1], ["po_", 1], ["pang_", 0] ]
    
    # ALL method lists
    allT = sec_prevarsT + sec_varsT + sec_postvarsT
    allMisc = sec_main + sec_shader + sec_prevarsW + sec_varsW + sec_postvarsW + sec_preAffine + sec_postAffine




class flam3_varsPRM_FF:

    # Collect all FF variations and their parametric parameters.
    varsPRM_FF = (  ["linear", 0], 
                    ["sinusoidal", 0], 
                    ["spherical", 0], 
                    ["swirl", 0], 
                    ["horseshoe", 0], 
                    ["polar", 0], 
                    ["handkerchief", 0], 
                    ["heart", 0], 
                    ["disc", 0], 
                    ["spiral", 0], 
                    ["hiperbolic", 0], 
                    ["diamond", 0], 
                    ["ex", 0], 
                    ["julia", 0], 
                    ["bent", 0], 
                    ["*waves", 0], 
                    ["fisheye", 0], 
                    ["*popcorn", 0], 
                    ["expo", 0], 
                    ["power", 0], 
                    ["cosine", 0], 
                    ["*rings", 0], 
                    ["*fan", 0], 
                    ["bubble", 0], 
                    ["cylinder", 0], 
                    ["eyefish", 0], 
                    ["blur", 0], 
                    ["curl...", ["ff_curlc", 1], 1], 
                    ["ngon...", ["ff_ngon", 1], 1], 
                    ["pdj...", ["ff_pdjw", 1], 1], 
                    ["blob...", ["ff_blob", 1], 1], 
                    ["juliaN...", ["ff_julian", 1], 1], 
                    ["juliascope...", ["ff_juliascope", 1], 1], 
                    ["gaussian", 0], 
                    ["fan2...", ["ff_fan2", 1], 1], 
                    ["rings2...", ["ff_rings2val", 0], 1], 
                    ["rectangles...", ["ff_rectangles", 1], 1], 
                    ["radialblur...", ["ff_radialblur", 1], 1], 
                    ["pie...", ["ff_pie", 1], 1], 
                    ["arch", 0], 
                    ["tangent", 0], 
                    ["square", 0], 
                    ["rays", 0], 
                    ["blade", 0], 
                    ["secant2", 0], 
                    ["twintrian", 0], 
                    ["cross", 0], 
                    ["disc2...", ["ff_disc2", 1], 1], 
                    ["supershape...", ["ff_supershape", 1], ["ff_supershapen", 1], 1], 
                    ["flower...", ["ff_flower", 1], 1], 
                    ["conic...", ["ff_conic", 1], 1], 
                    ["parabola...", ["ff_parabola", 1], 1], 
                    ["bent2...", ["ff_bent2xy", 1], 1], 
                    ["bipolar...", ["ff_bipolarshift", 0], 1],
                    ["boarders", 0],
                    ["butterfly", 0], 
                    ["cell...", ["ff_cellsize", 0], 1], 
                    ["cpow...", ["ff_cpow", 1], 1], 
                    ["edisc", 0], 
                    ["elliptic", 0], 
                    ["noise", 0], 
                    ["escher...", ["ff_escherbeta", 0], 1], 
                    ["foci", 0], 
                    ["lazysusan...", ["ff_lazysusanxyz", 1], ["ff_lazysusan", 1], 1], 
                    ["loonie", 0], 
                    ["preblur", 0], 
                    ["modulus...", ["ff_modulusXYZ", 1], 1], 
                    ["oscope...", ["ff_oscope", 1], 1], 
                    ["polar2", 0], 
                    ["popcorn...", ["ff_popcorn2xyz", 1], ["ff_popcorn2c", 0], 1], 
                    ["scry", 0], 
                    ["separation...", ["ff_separationxyz", 1], ["ff_separationinsidexyz", 1], 1], 
                    ["split...", ["ff_splitxyz", 1], 1], 
                    ["splits...", ["ff_splitsxyz", 1], 1], 
                    ["stripes...", ["ff_stripes", 1], 1], 
                    ["wedge...", ["ff_wedge", 1], 1], 
                    ["wedgejulia...", ["ff_wedgejulia", 1], 1], 
                    ["wedgesph", ["ff_wedgesph", 1], 1], 
                    ["whorl...", ["ff_whorl", 1], 1], 
                    ["waves2...", ["ff_waves2scalexyz", 1], ["ff_waves2freqxyz", 1], 1], 
                    ["cothe exp", 0], 
                    ["cothe log", 0], 
                    ["cothe sin", 0], 
                    ["cothe cos", 0], 
                    ["cothe tan", 0], 
                    ["cothe sec", 0], 
                    ["cothe csc", 0], 
                    ["cothe cot", 0], 
                    ["cothe sinh", 0], 
                    ["cothe cosh", 0], 
                    ["cothe tanh", 0], 
                    ["cothe sech", 0], 
                    ["cothe csch", 0], 
                    ["cothe coth", 0], 
                    ["auger...", ["ff_auger", 1], 1], 
                    ["flux...", ["ff_fluxspread", 0], 1], 
                    ["mobius...", ["ff_mobiusre", 1], ["ff_mobiusim", 1], 1],
                    ["curve...", ["ff_curvexyzlenght", 1], ["ff_curvexyzamp", 1], 1], 
                    ["persp...", ["ff_persp", 1], 1], 
                    ["bwraps...", ["ff_bwraps", 1], ["ff_bwrapstwist", 1], 1], 
                    ["hemisphere", 0], 
                    ["polynomial...", ["ff_polynomialpow", 1], ["ff_polynomiallc", 1], ["ff_polynomialsc", 1], 1] )




    varsPRM_FP = (  ["linear", 0], 
                    ["sinusoidal", 0], 
                    ["spherical", 0], 
                    ["swirl", 0], 
                    ["horseshoe", 0], 
                    ["polar", 0], 
                    ["handkerchief", 0], 
                    ["heart", 0], 
                    ["disc", 0], 
                    ["spiral", 0], 
                    ["hiperbolic", 0], 
                    ["diamond", 0], 
                    ["ex", 0], 
                    ["julia", 0], 
                    ["bent", 0], 
                    ["*waves", 0], 
                    ["fisheye", 0], 
                    ["*popcorn", 0], 
                    ["expo", 0], 
                    ["power", 0], 
                    ["cosine", 0], 
                    ["*rings", 0], 
                    ["*fan", 0], 
                    ["bubble", 0], 
                    ["cylinder", 0], 
                    ["eyefish", 0], 
                    ["blur", 0], 
                    ["curl...", ["fp1_curlc", 1], 1], 
                    ["ngon...", ["fp1_ngon", 1], 1], 
                    ["pdj...", ["fp1_pdjw", 1], 1], 
                    ["blob...", ["fp1_blob", 1], 1], 
                    ["juliaN...", ["fp1_julian", 1], 1], 
                    ["juliascope...", ["fp1_juliascope", 1], 1], 
                    ["gaussian", 0], 
                    ["fan2...", ["fp1_fan2", 1], 1], 
                    ["rings2...", ["fp1_rings2val", 0], 1], 
                    ["rectangles...", ["fp1_rectangles", 1], 1], 
                    ["radialblur...", ["fp1_radialblur", 1], 1], 
                    ["pie...", ["fp1_pie", 1], 1], 
                    ["arch", 0], 
                    ["tangent", 0], 
                    ["square", 0], 
                    ["rays", 0], 
                    ["blade", 0], 
                    ["secant2", 0], 
                    ["twintrian", 0], 
                    ["cross", 0], 
                    ["disc2...", ["fp1_disc2", 1], 1], 
                    ["supershape...", ["fp1_supershape", 1], ["fp1_supershapen", 1], 1], 
                    ["flower...", ["fp1_flower", 1], 1], 
                    ["conic...", ["fp1_conic", 1], 1], 
                    ["parabola...", ["fp1_parabola", 1], 1], 
                    ["bent2...", ["fp1_bent2xy", 1], 1], 
                    ["bipolar...", ["fp1_bipolarshift", 0], 1],
                    ["boarders", 0],
                    ["butterfly", 0], 
                    ["cell...", ["fp1_cellsize", 0], 1], 
                    ["cpow...", ["fp1_cpow", 1], 1], 
                    ["edisc", 0], 
                    ["elliptic", 0], 
                    ["noise", 0], 
                    ["escher...", ["fp1_escherbeta", 0], 1], 
                    ["foci", 0], 
                    ["lazysusan...", ["fp1_lazysusanxyz", 1], ["fp1_lazysusan", 1], 1], 
                    ["loonie", 0], 
                    ["preblur", 0], 
                    ["modulus...", ["fp1_modulusXYZ", 1], 1], 
                    ["oscope...", ["fp1_oscope", 1], 1], 
                    ["polar2", 0], 
                    ["popcorn...", ["fp1_popcorn2xyz", 1], ["fp1_popcorn2c", 0], 1], 
                    ["scry", 0], 
                    ["separation...", ["fp1_separationxyz", 1], ["fp1_separationinsidexyz", 1], 1], 
                    ["split...", ["fp1_splitxyz", 1], 1], 
                    ["splits...", ["fp1_splitsxyz", 1], 1], 
                    ["stripes...", ["fp1_stripes", 1], 1], 
                    ["wedge...", ["fp1_wedge", 1], 1], 
                    ["wedgejulia...", ["fp1_wedgejulia", 1], 1], 
                    ["wedgesph", ["fp1_wedgesph", 1], 1], 
                    ["whorl...", ["fp1_whorl", 1], 1], 
                    ["waves2...", ["fp1_waves2scalexyz", 1], ["fp1_waves2freqxyz", 1], 1], 
                    ["cothe exp", 0], 
                    ["cothe log", 0], 
                    ["cothe sin", 0], 
                    ["cothe cos", 0], 
                    ["cothe tan", 0], 
                    ["cothe sec", 0], 
                    ["cothe csc", 0], 
                    ["cothe cot", 0], 
                    ["cothe sinh", 0], 
                    ["cothe cosh", 0], 
                    ["cothe tanh", 0], 
                    ["cothe sech", 0], 
                    ["cothe csch", 0], 
                    ["cothe coth", 0], 
                    ["auger...", ["fp1_auger", 1], 1], 
                    ["flux...", ["fp1_fluxspread", 0], 1], 
                    ["mobius...", ["fp1_mobiusre", 1], ["fp1_mobiusim", 1], 1],
                    ["curve...", ["fp1_curvexyzlenght", 1], ["fp1_curvexyzamp", 1], 1], 
                    ["persp...", ["fp1_persp", 1], 1], 
                    ["bwraps...", ["fp1_bwraps", 1], ["fp1_bwrapstwist", 1], 1], 
                    ["hemisphere", 0], 
                    ["polynomial...", ["fp1_polynomialpow", 1], ["fp1_polynomiallc", 1], ["fp1_polynomialsc", 1], 1] )





    # SECTIONS method lists
    #
    # (*T)Types have no signature and always to be used with: pastePRM_T_from_list()
    sec_varsT_FF = [ "ffv1type", "ffv2type", "ffv3type" ]
    sec_varsW_FF = [ ["ffv1weight", 0], ["ffv2weight", 0], ["ffv3weight", 0] ]
    sec_postvarsT_FF = [ "ffp1type", "ffp2type" ]
    sec_postvarsW_FF = [ ["ffp1weight", 0], ["ffp2weight", 0] ]
    sec_preAffine_FF = [ ["ffx", 1], ["ffy", 1], ["ffo", 1], ["ffang", 0] ]
    sec_postAffine_FF = [ ["dofp", 0], ["ffpx", 1], ["ffpy", 1], ["ffpo", 1], ["ffpang", 0] ]
    
    # ALL method lists
    # allT_FF list is omitted here because FF VARS and FF POST VARS have their own unique parametric parameters
    # so I need to handle them one by one inside: def prm_paste_FF() and def prm_paste_sel_FF()
    allMisc_FF = sec_varsW_FF + sec_postvarsW_FF + sec_preAffine_FF + sec_postAffine_FF





###############################################################################################
# FLAM3 paste list of parms
###############################################################################################
def paste_from_list(prm_list, node, flam3node, id, id_from):

    for prm in prm_list:
        # if a tuple
        if prm[1]:
            prm_from = flam3node.parmTuple(prm[0] + str(id_from))
            prm_to = node.parmTuple(prm[0] + str(id))
            prm_idx = 0
            for p in prm_from:
                if len(p.keyframes()):
                    for k in p.keyframes():
                        prm_to[prm_idx].setKeyframe(k)
                else:
                    prm_to[prm_idx].set(p.eval())
                prm_idx += 1
        else:
            prm_from = flam3node.parm(prm[0] + str(id_from))
            prm_to = node.parm(prm[0] + str(id))
            if len(prm_from.keyframes()):
                    for k in prm_from.keyframes():
                        prm_to.setKeyframe(k)
            else:
                prm_to.set(prm_from.eval())





###############################################################################################
# FLAM3 (*T)Types-> paste parametric parms if any are found in the list of var types passed in
###############################################################################################
def pastePRM_T_from_list(prmT_list, varsPRM, node, flam3node, id, id_from):
    
    for prm in prmT_list:
        prm_from = flam3node.parm(prm + str(id_from)).eval()
        node.setParms({prm + str(id): prm_from})
        # Check if this var is a parametric or not
        type = int(prm_from)
        if(varsPRM[type][-1]):
            paste_from_list(varsPRM[type][1:-1], node, flam3node, id, id_from)





###############################################################################################
# FLAM3 paste note msg
# int_mode:
# 0 -> iterators
# 1 -> FF all
# 2 -> FF sections
###############################################################################################
def paste_set_note(int_mode, str_section, node, flam3node, id, id_from):

    if int_mode == 0:
        # If on the same FLAM3 node
        if node == flam3node:
            node.setParms({'variter_' + str(id): 'iter.' + str(id_from) + str_section})
            print(str(node) + ": Copied values from: " + "iter." + str(id_from) + str_section + " to: " + "iter." + str(id) + str_section)
        else:
            node.setParms({'variter_' + str(id): str(flam3node) + '->iter.' + str(id_from) + str_section})
            print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + str_section + " to: " + str(node) + "->iter." + str(id) + str_section)
    elif int_mode == 1:
        if node != flam3node:
            node.setParms({'ffnote': str(flam3node) + "->FF"})
            print(str(node) + ": Copied FF from: " + str(flam3node) + "->FF" + " to: " + str(node) + "->FF")
    elif int_mode == 2:
        if node != flam3node:
            node.setParms({'ffnote': str(flam3node) + "->FF" + str_section})
            print(str(node) + ": Copied FF from: " + str(flam3node) + "->FF" + str_section + " to: " + str(node) + "->FF" + str_section)




###############################################################################################
# Copy paste all iterator's values from one to another and also from different FLAM3 HDA nodes
###############################################################################################
def prm_paste(kwargs):

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
                print(str(node) + ": Iterator copied. Select a different iterator number to paste those values.")
            else:
                # Create flam3 variation's parameter object
                FLAM3VARS = flam3_varsPRM()

                # var's type and set parametric variation's parameter if it find any
                pastePRM_T_from_list(FLAM3VARS.allT, FLAM3VARS.varsPRM, node, flam3node, id, id_from)
                # paste rest
                paste_from_list(FLAM3VARS.allMisc, node, flam3node, id, id_from)
                # set note
                paste_set_note(0, "", node, flam3node, id, id_from)

        else:
            print(str(node) + ": Please copy an iterator first.")

    elif kwargs["shift"]:
        del hou.session.flam3node_mp_id
        del hou.session.flam3node

    else:
        hou.session.flam3node_mp_id = kwargs['script_multiparm_index']
        hou.session.flam3node = kwargs['node']
        print(str(kwargs['node']) + ": Copied iterator: " + str(hou.session.flam3node) + "->iter." + str(hou.session.flam3node_mp_id))





###############################################################################################
# FF - Copy paste all FF's values from one FLAM3 node to another FLAM3 node
###############################################################################################
def prm_paste_FF(kwargs):

    if kwargs["ctrl"]:

        # current node
        node=kwargs['node']

        # FLAM3 node and Iterator we just copied
        flam3node_FF = hou.session.flam3node_FF
        flam3node_FF_check = hou.session.flam3node_FF_check

        # If an iterator was copied on a node that has been deleted
        # revert to -1 so that we are forced to copy an iterator again.
        try:
            flam3node_FF.type()
        except:
            flam3node_FF_check = -1

        # If we ever copied an iterator from a currently existing FLAM3 node
        if flam3node_FF_check != -1:
            if node==flam3node_FF:
                print(str(node) + ": FF copied. Select a different FLAM3 node to paste those FF values.")
            else:
                # Create flam3 variation's parameter object
                FLAM3VARS_FF = flam3_varsPRM_FF()

                # var's type and set parametric variation's parameter if it find any
                pastePRM_T_from_list(FLAM3VARS_FF.sec_varsT_FF, FLAM3VARS_FF.varsPRM_FF, node, flam3node_FF, "", "")
                pastePRM_T_from_list(FLAM3VARS_FF.sec_postvarsT_FF, FLAM3VARS_FF.varsPRM_FP, node, flam3node_FF, "", "")
                # paste rest
                paste_from_list(FLAM3VARS_FF.allMisc_FF, node, flam3node_FF, "", "")
                # set note
                paste_set_note(1, "", node, flam3node_FF, "", "")

        else:
            print(str(node) + ": Please copy FF first.")

    elif kwargs["shift"]:
        del hou.session.flam3node_FF_check
        del hou.session.flam3node_FF

    else:
        hou.session.flam3node_FF_check = 1
        hou.session.flam3node_FF = kwargs['node']
        print(str(kwargs['node']) + ": Copied FF: " + str(hou.session.flam3node_FF) + "->FF" )





###############################################################################################
# paste sections of iterator's values from one to another and also from different FLAM3 nodes
###############################################################################################
def prm_paste_sel(kwargs):

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
        
        # Create flam3 variation's parameter object
        FLAM3VARS = flam3_varsPRM()
        # Get user selection of paste methods
        paste_sel = node.parm("prmpastesel_" + str(id)).evalAsInt()




        # set MAIN
        ################################################################################
        if paste_sel == 1:
        
            paste_from_list(FLAM3VARS.sec_main, node, flam3node, id, id_from)
            # set note
            paste_set_note(0, ".main", node, flam3node, id, id_from)

        # set XAOS
        ################################################################################
        elif paste_sel == 2:
        
            paste_from_list(FLAM3VARS.sec_xaos, node, flam3node, id, id_from)
            # set note
            paste_set_note(0, ".xaos", node, flam3node, id, id_from)

        # set SHADER
        ################################################################################ 
        elif paste_sel == 3:
        
            paste_from_list(FLAM3VARS.sec_shader, node, flam3node, id, id_from)
            # set note
            paste_set_note(0, ".shader", node, flam3node, id, id_from)
        
        # set PRE VARS
        ################################################################################
        elif paste_sel == 4:
            
            # var's type and set parametric variation's parameter if it find any
            pastePRM_T_from_list(FLAM3VARS.sec_prevarsT, FLAM3VARS.varsPRM, node, flam3node, id, id_from)
            # var's weight
            paste_from_list(FLAM3VARS.sec_prevarsW, node, flam3node, id, id_from)
            # set note
            paste_set_note(0, ".pre_vars", node, flam3node, id, id_from)

        # set VARS
        ################################################################################
        elif paste_sel == 5:

            # var's type and set parametric variation's parameter if it find any
            pastePRM_T_from_list(FLAM3VARS.sec_varsT, FLAM3VARS.varsPRM, node, flam3node, id, id_from)
            # var's weight
            paste_from_list(FLAM3VARS.sec_varsW, node, flam3node, id, id_from)
            # set note
            paste_set_note(0, ".vars", node, flam3node, id, id_from)

        # set POST VARS
        ################################################################################
        elif paste_sel == 6:

            # var's type and set parametric variation's parameter if it find any
            pastePRM_T_from_list(FLAM3VARS.sec_postvarsT, FLAM3VARS.varsPRM, node, flam3node, id, id_from)
            # var's weight
            paste_from_list(FLAM3VARS.sec_postvarsW, node, flam3node, id, id_from)
            # set note
            paste_set_note(0, ".post_var", node, flam3node, id, id_from)
                
        # set PRE AFFINE
        ################################################################################
        elif paste_sel == 7:
        
            paste_from_list(FLAM3VARS.sec_preAffine, node, flam3node, id, id_from)
            # set note
            paste_set_note(0, ".pre_affine", node, flam3node, id, id_from)
        
        # set POST AFFINE
        ################################################################################
        elif paste_sel == 8:
        
            paste_from_list(FLAM3VARS.sec_postAffine, node, flam3node, id, id_from)
            # set note
            paste_set_note(0, ".post_affine", node, flam3node, id, id_from)
     



        # Set it to a null value ( first in the menu array idx in this case )
        # so that we can paste the same section again, if we want to.
        #
        # please check the FLAM3node.ff_prmpastesel parameter python menu script to know its size.
        node.setParms({"prmpastesel_" + str(id): str(0)})
    
    else:
        print(str(node) + ": Please copy the FF first.")





###############################################################################################
# FF paste sections of FF's values from one FLAM3 node to another FLAM3 node
###############################################################################################
def prm_paste_sel_FF(kwargs):

    # current node
    node=kwargs['node']

    # FLAM3 node and its state we just copied
    flam3node_FF = hou.session.flam3node_FF
    flam3node_FF_check = hou.session.flam3node_FF_check

    # WE DO THE FOLLOWING IN THE SCRIPTED MENU LIST -> FLAM3node.ff_prmpastesel parameter
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
        
        # Create flam3 variation's parameter object
        FLAM3VARS_FF = flam3_varsPRM_FF()
        # Get user selection of paste methods
        ff_paste_sel = node.parm("ff_prmpastesel").evalAsInt()





        # set FF VARS
        ################################################################################
        if ff_paste_sel == 1:

            # var's type and set parametric variation's parameter if it find any
            pastePRM_T_from_list(FLAM3VARS_FF.sec_varsT_FF, FLAM3VARS_FF.varsPRM_FF, node, flam3node_FF, "", "")
            # var's weight
            paste_from_list(FLAM3VARS_FF.sec_varsW_FF, node, flam3node_FF, "", "")
            # set note
            paste_set_note(2, ".vars", node, flam3node_FF, "", "")
        
        # set FF POST VARS
        ################################################################################
        elif ff_paste_sel == 2:

            # var's type and set parametric variation's parameter if it find any
            pastePRM_T_from_list(FLAM3VARS_FF.sec_postvarsT_FF, FLAM3VARS_FF.varsPRM_FP, node, flam3node_FF, "", "")
            # var's weight
            paste_from_list(FLAM3VARS_FF.sec_postvarsW_FF, node, flam3node_FF, "", "")
            # set note
            paste_set_note(2, ".post_vars", node, flam3node_FF, "", "")

        # set FF PRE AFFINE
        ################################################################################
        elif ff_paste_sel == 3:
        
            paste_from_list(FLAM3VARS_FF.sec_preAffine_FF, node, flam3node_FF, "", "")
            # set note
            paste_set_note(2, ".pre_affine", node, flam3node_FF, "", "")
        
        # set FF POST AFFINE
        ################################################################################
        elif ff_paste_sel == 4:
        
            paste_from_list(FLAM3VARS_FF.sec_postAffine_FF, node, flam3node_FF, "", "")
            # set note
            paste_set_note(2, ".post_affine", node, flam3node_FF, "", "")





        # Set it to a null value ( first in the menu array idx in this case )
        # so that we can paste the same section again, if we want to.
        #
        # please check the FLAM3node.ff_prmpastesel parameter python menu script to know its size.
        node.setParms({"ff_prmpastesel": str(0)})
                
    else:
        print(str(node) + ": Please copy the FF first.")





###############################################################################################
# FLAM3 on create init
###############################################################################################
def flam3_on_create(kwargs):

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


###############################################################################################
# Init parameter presets menu list as soon as you load a valid ramp json file
###############################################################################################
def ramp_init_presets(kwargs):

    node = kwargs['node']
    ramp_presets = node.parm('presets')
    ramp_presets.set('0')





###############################################################################################
# Save current ramp to a json file
###############################################################################################
def ramp_save(kwargs):

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
        parm = node.parm('palette')
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
            
            user = hou.ui.displayMessage('a file already exists', buttons=('Append','Overwrite','Cancel')) 
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
def json_to_ramp(kwargs):

    node = kwargs['node']
    
    #get ramp parm
    ramp_parm = node.parm('palette')
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





###############################################################################################
# Load default values. ( Sierpinsky triangle )
###############################################################################################
def flam3_default(self):

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
    self.setParms({"ffnote": ""})
    self.setParms({"ffv1type": 0})
    self.setParms({"ffv2type": 0})
    self.setParms({"ffv3type": 0})
    self.setParms({"ffv1weight": 1})
    self.setParms({"ffv2weight": 0})
    self.setParms({"ffv3weight": 0})
    # FF post
    self.setParms({"ffp1type": 0})
    self.setParms({"ffp2type": 0})
    self.setParms({"ffp1weight": 0})
    self.setParms({"ffp2weight": 0})
    # FF affine
    self.setParms({"ffx": hou.Vector2((1.0, 0.0))})
    self.setParms({"ffy": hou.Vector2((0.0, 1.0))})
    self.setParms({"ffo": hou.Vector2((0.0, 0.0))})
    self.setParms({"ffang": 0})
    self.setParms({"dofp": 0})
    self.setParms({"ffpx": hou.Vector2((1.0, 0.0))})
    self.setParms({"ffpy": hou.Vector2((0.0, 1.0))})
    self.setParms({"ffpo": hou.Vector2((0.0, 0.0))})
    self.setParms({"ffpang": 0})

    # CP
    self.setParms({"filepath": ""})
    self.setParms({"palettehsv_": hou.Vector3((0.0, 1.0, 1.0))})
    # CP->ramp
    ramp_parm = self.parm('palette')
    ramp_parm.deleteAllKeyframes()
    color_bases = [hou.rampBasis.Linear] * 3
    color_keys = [0.0, 0.5, 1.0]
    color_values = [(1,0,0), (0,1,0), (0,0,1)]
    ramp_parm.set(hou.Ramp(color_bases, color_keys, color_values))

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
    
    # Iterator 1
    #
    # shader
    self.setParms({"clr_1": 0})
    self.setParms({"clrspeed_1": 0.75})
    # pre affine
    self.setParms({"x_1": hou.Vector2((0.5, 0.0))})
    self.setParms({"y_1": hou.Vector2((0.0, 0.5))})
    self.setParms({"o_1": hou.Vector2((0.0, 0.51225))})

    # Iterator 2
    #
    # shader
    self.setParms({"clr_2": 0.5})
    self.setParms({"clrspeed_2": 0.75})
    # pre affine
    self.setParms({"x_2": hou.Vector2((0.5, 0.0))})
    self.setParms({"y_2": hou.Vector2((0.0, 0.5))})
    self.setParms({"o_2": hou.Vector2((-0.29575, 0.0))})
    
    # Iterator 3
    #
    # shader
    self.setParms({"clr_3": 1.0})
    self.setParms({"clrspeed_3": 0.75})
    # pre affine
    self.setParms({"x_3": hou.Vector2((0.5, 0.0))})
    self.setParms({"y_3": hou.Vector2((0.0, 0.5))})
    self.setParms({"o_3": hou.Vector2((0.29575, 0.0))})

    #######################################################################





###############################################################################################
# Open web browser to the FLAM3 for Houdini website
###############################################################################################
def web_flame3hda():
    page = "https://alexnardini.net/flame-home/"
    webbrowser.open(page)





###############################################################################################
# Open web browser to the FractalFlame Algorithm paper
###############################################################################################
def web_TFFA():
    page = "https://flam3.com/flame_draves.pdf"
    webbrowser.open(page)