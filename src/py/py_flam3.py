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

    # Simple class for now to hold all parameters
    # so I can access those from everywhere on demand,
    # other than having all of them in one place for future updates.


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
                [["curlc_", 1], 1], 
                [["ngon_", 1], 1], 
                [["pdjw_", 1], 1], 
                [["blob_", 1], 1], 
                [["julian_", 1], 1], 
                [["juliascope", 1], 1], 
                ["gaussian", 0], 
                [["fan2_", 1], 1], 
                [["rings2val_", 0], 1], 
                [["rectangles_", 1], 1], 
                [["radialblur_", 1], 1], 
                [["pie_", 1], 1], 
                ["arch", 0], 
                ["tangent", 0], 
                ["square", 0], 
                ["rays", 0], 
                ["blade", 0], 
                ["secant2", 0], 
                ["twintrian", 0], 
                ["cross", 0], 
                [["disc2_", 1], 1], 
                [["supershape_", 1], ["supershapen_", 1], 1], 
                [["flower_", 1], 1], 
                [["conic_", 1], 1], 
                [["parabola_", 1], 1], 
                [["bent2xy_", 1], 1], 
                [["bipolarshift_", 0], 1],
                ["boarders", 0],
                ["butterfly", 0], 
                [["cellsize_", 0], 1], 
                [["cpow_", 1], 1], 
                ["edisc", 0], 
                ["elliptic", 0], 
                ["noise", 0], 
                [["escherbeta_", 0], 1], 
                ["foci", 0], 
                [["lazysusanxyz_", 1], ["lazysusan_", 1], 1], 
                ["loonie", 0], 
                ["preblur", 0], 
                [["modulusXYZ_", 1], 1], 
                [["oscope_", 1], 1], 
                ["polar2", 0], 
                [["popcorn2xyz_", 1], ["popcorn2c_", 0], 1], 
                ["scry", 0], 
                [["separationxyz_", 1], ["separationinsidexyz_", 1], 1], 
                [["splitxyz_", 1], 1], 
                [["splitsxyz_", 1], 1], 
                [["stripes_", 1], 1], 
                [["wedge_", 1], 1], 
                [["wedgejulia_", 1], 1], 
                [["wedgesph_", 1], 1], 
                [["whorl_", 1], 1], 
                [["waves2scalexyz_", 1], ["waves2freqxyz_", 1], 1], 
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
                [["auger_", 1], 1], 
                [["fluxspread_", 0], 1], 
                [["mobiusre_", 1], ["mobiusim_", 1], 1],
                [["curvexyzlenght_", 1], ["curvexyzamp_", 1], 1], 
                [["persp_", 1], 1], 
                [["bwraps_", 1], ["bwrapstwist_", 1], 1], 
                ["hemisphere", 0], 
                [["polynomialpow_", 1], ["polynomiallc_", 1], ["polynomialsc_", 1], 1] )


    # ALL method lists
    allType = [ "pre1type_", "pre2type_", "v1type_", "v2type_", "v3type_", "v4type_", "p1type_" ] # preblur is omitted as it is always ZERO
    allMisc = [ "vactive_", "iw_", "clr_", "clrspeed_", "alpha_", "preblurweight_", "pre1weight_", "pre2weight_", "v1weight_", "v2weight_", "v3weight_", "v4weight_", "p1weight_", "dopost_", "ang_", "pang_" ]
    allAffineTUPLE = [ "x_", "y_", "o_", "px_", "py_", "po_" ]

    # SECTIONS method lists
    #
    # Names that start with an underscore "_" are single parms and not lists
    sec_main = [ "vactive_", "iw_" ]
    sec_shader = [ "clr_", "clrspeed_", "alpha_" ]
    sec__xaos = "varnote_"
    sec_prevarsT = [ "pre1type_", "pre2type_" ] # preblur is omitted as it is always ZERO
    sec_prevarsW = [ "preblurweight_", "pre1weight_", "pre2weight_" ]
    sec_varsT = [ "v1type_", "v2type_", "v3type_", "v4type_" ]
    sec_varsW = [ "v1weight_", "v2weight_", "v3weight_", "v4weight_" ]
    sec_postvarsT = [ "p1type_" ]
    sec_postvarsW = [ "p1weight_" ]
    sec_preAffineTuple = [ "x_", "y_", "o_" ]
    sec__preAffineAng = "ang_"
    sec__postAffineCheck = "dopost_"
    sec_postAffineTuple = [ "px_", "py_", "po_" ]
    sec__postAffineAng = "pang_"





###############################################################################################
# FLAM3 paste list of parms
###############################################################################################
def paste_from_list(prmlist, node, flam3node, id, id_from):
    for prm in prmlist:
        prm_from = flam3node.parm(prm + str(id_from)).eval()
        node.setParms({prm + str(id): prm_from})





###############################################################################################
# FLAM3 paste list of tuple parms
###############################################################################################
def pasteTuple_from_list(prmlist, node, flam3node, id, id_from):
    for prm in prmlist:
        prm_from = flam3node.parmTuple(prm + str(id_from)).eval()
        node.setParms({prm + str(id): prm_from})





###############################################################################################
# FLAM3 paste parametric parms if any are found in the list of var types passed in
###############################################################################################
def pastePRM_from_list(prmlist, varsPRM, node, flam3node, id, id_from):
    
    for prm in prmlist:
        prm_from = flam3node.parm(prm + str(id_from)).eval()
        node.setParms({prm + str(id): prm_from})
        # Check if this var is a parametric or not
        type = int(prm_from)
        if(varsPRM[type][-1]):
            for t in varsPRM[type][:-1]:
                # if a tuple
                if t[1]:
                    t_prm_from = flam3node.parmTuple(t[0] + str(id_from)).eval()
                    node.setParms({t[0] + str(id): t_prm_from})
                else:
                    t_prm_from = flam3node.parm(t[0] + str(id_from)).eval()
                    node.setParms({t[0] + str(id): t_prm_from})





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

            # Create flam3 variation's parameter object
            FLAM3VARS = flam3_varsPRM()

            # var's type
            pastePRM_from_list(FLAM3VARS.allType, FLAM3VARS.varsPRM, node, flam3node, id, id_from)

            for prm in FLAM3VARS.allMisc:
                prm_from = flam3node.parm(prm + str(id_from)).eval()
                node.setParms({prm + str(id): prm_from})
                
            for prm in FLAM3VARS.allAffineTUPLE:
                prm_from = flam3node.parmTuple(prm + str(id_from)).eval()
                node.setParms({prm + str(id): prm_from})
                
            # Set note to know the node and iterator those values are coming from
            if node == flam3node:
                node.setParms({'variter_' + str(id): 'Cloned iter.' + str(id_from)})
                print(str(node) + ": Copied values from: " + "iter." + str(id_from) + " to: " + "iter." + str(id))
            else:
                node.setParms({'variter_' + str(id): 'Cloned ' + str(flam3node) + '->iter.' + str(id_from)})
                print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + " to: " + str(node) + "->iter." + str(id))

        else:
            print(str(node) + ": Please copy an iterator first.")

    else:
        hou.session.flam3node_mp_id = kwargs['script_multiparm_index']
        hou.session.flam3node = kwargs['node']
        print(str(kwargs['node']) + ": Copied values from: " + str(hou.session.flam3node) + "->iter." + str(hou.session.flam3node_mp_id))






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
                
            # Set note to know the node and iterator those values are coming from
            if node == flam3node:
                node.setParms({'variter_' + str(id): 'iter.' + str(id_from) + ".main"})
                print(str(node) + ": Copied values from: " + "iter." + str(id_from) + ".main" + " to: " + "iter." + str(id) + ".main")
            else:
                node.setParms({'variter_' + str(id): str(flam3node) + '->iter.' + str(id_from) + ".main"})
                print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + ".main" + " to: " + str(node) + "->iter." + str(id) + ".main")

        # set XAOS
        ################################################################################
        elif paste_sel == 2:
        
            xaos_from = flam3node.parm(FLAM3VARS.sec__xaos + str(id_from)).eval()
            node.setParms({FLAM3VARS.sec__xaos + str(id): xaos_from})
                
            # Set note to know the node and iterator those values are coming from
            if node == flam3node:
                node.setParms({'variter_' + str(id): 'iter.' + str(id_from) + ".xaos"})
                print(str(node) + ": Copied values from: " + "iter." + str(id_from) + ".xaos" + " to: " + "iter." + str(id) + ".xaos")
            else:
                node.setParms({'variter_' + str(id): str(flam3node) + '->iter.' + str(id_from) + ".xaos"})
                print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + ".xaos" + " to: " + str(node) + "->iter." + str(id) + ".xaos")

        # set SHADER
        ################################################################################ 
        elif paste_sel == 3:
        
            paste_from_list(FLAM3VARS.sec_shader, node, flam3node, id, id_from)
                
            # Set note to know the node and iterator those values are coming from
            if node == flam3node:
                node.setParms({'variter_' + str(id): 'iter.' + str(id_from) + ".shader"})
                print(str(node) + ": Copied values from: " + "iter." + str(id_from) + ".shader" + " to: " + "iter." + str(id) + ".shader")
            else:
                node.setParms({'variter_' + str(id): str(flam3node) + '->iter.' + str(id_from) + ".shader"})
                print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + ".shader" + " to: " + str(node) + "->iter." + str(id) + ".shader")
        
        # set PRE VARS
        ################################################################################
        elif paste_sel == 4:
            
            # var's type and set parametric variation's parameter if it find any
            pastePRM_from_list(FLAM3VARS.sec_prevarsT, FLAM3VARS.varsPRM, node, flam3node, id, id_from)
            # var's weight
            paste_from_list(FLAM3VARS.sec_prevarsW, node, flam3node, id, id_from)
                
            # Set note to know the node and iterator those values are coming from
            if node == flam3node:
                node.setParms({'variter_' + str(id): 'iter.' + str(id_from) + ".pre_vars"})
                print(str(node) + ": Copied values from: " + "iter." + str(id_from) + ".pre_vars" + " to: " + "iter." + str(id) + ".pre_vars")
            else:
                node.setParms({'variter_' + str(id): str(flam3node) + '->iter.' + str(id_from) + ".pre_vars"})
                print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + ".pre_vars" + " to: " + str(node) + "->iter." + str(id) + ".pre_vars")

        # set VARS
        ################################################################################
        elif paste_sel == 5:

            # var's type and set parametric variation's parameter if it find any
            pastePRM_from_list(FLAM3VARS.sec_varsT, FLAM3VARS.varsPRM, node, flam3node, id, id_from)
            # var's weight
            paste_from_list(FLAM3VARS.sec_varsW, node, flam3node, id, id_from)
                
            # Set note to know the node and iterator those values are coming from
            if node == flam3node:
                node.setParms({'variter_' + str(id): 'iter.' + str(id_from) + ".vars"})
                print(str(node) + ": Copied values from: " + "iter." + str(id_from) + ".vars" + " to: " + "iter." + str(id) + ".vars")
            else:
                node.setParms({'variter_' + str(id): str(flam3node) + '->iter.' + str(id_from) + ".vars"})
                print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + ".vars" + " to: " + str(node) + "->iter." + str(id) + ".vars")

        # set POST VARS
        ################################################################################
        elif paste_sel == 6:

            # var's type and set parametric variation's parameter if it find any
            pastePRM_from_list(FLAM3VARS.sec_postvarsT, FLAM3VARS.varsPRM, node, flam3node, id, id_from)
            # var's weight
            paste_from_list(FLAM3VARS.sec_postvarsW, node, flam3node, id, id_from)
                
            # Set note to know the node and iterator those values are coming from
            if node == flam3node:
                node.setParms({'variter_' + str(id): 'iter.' + str(id_from) + ".post_vars"})
                print(str(node) + ": Copied values from: " + "iter." + str(id_from) + ".post_var" + " to: " + "iter." + str(id) + ".post_var")
            else:
                node.setParms({'variter_' + str(id): str(flam3node) + '->iter.' + str(id_from) + ".post_vars"})
                print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + ".post_var" + " to: " + str(node) + "->iter." + str(id) + ".post_var")
                
        # set PRE AFFINE
        ################################################################################
        elif paste_sel == 7:
        
            pasteTuple_from_list(FLAM3VARS.sec_preAffineTuple, node, flam3node, id, id_from)
            # One off angle parameter
            ang_from = flam3node.parm(FLAM3VARS.sec__preAffineAng + str(id_from)).eval()
            node.setParms({FLAM3VARS.sec__preAffineAng + str(id): ang_from})
            
            # Set note to know the node and iterator those values are coming from
            if node == flam3node:
                node.setParms({'variter_' + str(id): 'iter.' + str(id_from) + ".pre_affine"})
                print(str(node) + ": Copied values from: " + "iter." + str(id_from) + ".pre_affine" + " to: " + "iter." + str(id) + ".pre_affine")
            else:
                node.setParms({'variter_' + str(id): str(flam3node) + '->iter.' + str(id_from) + ".pre_affine"})
                print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + ".pre_affine" + " to: " + str(node) + "->iter." + str(id) + ".pre_affine")
        
        # set POST AFFINE
        ################################################################################
        elif paste_sel == 8:
        
            pasteTuple_from_list(FLAM3VARS.sec_postAffineTuple, node, flam3node, id, id_from)
            # One off dopost paramter
            dop_from = flam3node.parm(FLAM3VARS.sec__postAffineCheck + str(id_from)).eval()
            node.setParms({FLAM3VARS.sec__postAffineCheck + str(id): dop_from})
            # One off angle parameter
            ang_from = flam3node.parm(FLAM3VARS.sec__postAffineAng + str(id_from)).eval()
            node.setParms({FLAM3VARS.sec__postAffineAng + str(id): ang_from})
            
            # Set note to know the node and iterator those values are coming from
            if node == flam3node:
                node.setParms({'variter_' + str(id): 'iter.' + str(id_from) + ".post_affine"})
                print(str(node) + ": Copied values from: " + "iter." + str(id_from) + ".post_affine" + " to: " + "iter." + str(id) + ".post_affine")
            else:
                node.setParms({'variter_' + str(id): str(flam3node) + '->iter.' + str(id_from) + ".post_affine"})
                print(str(node) + ": Copied values from: " + str(flam3node) + "->iter." + str(id_from) + ".post_affine" + " to: " + str(node) + "->iter." + str(id) + ".post_affine")
     
        # Set it to a null value ( first in the menu array idx in this case )
        # so that we can paste the same section again, if we want to.
        #
        # please check the "prmpastesel_" python menu script to know its size.
        node.setParms({"prmpastesel_" + str(id): str(0)})
                
    
    else:
        print(str(node) + ": Please copy an iterator first.")





###############################################################################################
# FLAM3 on create init
###############################################################################################
def flam3_on_create(kwargs):

    # Set initial node color
    node = kwargs['node']
    node.setColor(hou.Color((0.825,0.825,0.825)))

    # FLAM3 node and MultiParameter id.
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