

#   Title:      SideFX Houdini FLAM3: 2D
#   Author:     Alessandro Nardini
#   date:       April 2023, Last revised September 2023
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
#   Name:       PY_MAP "Whatever"
#
#   Comment:    List of all UI parameters wired with a python definition
#               and the command string they actually run and from where.
#
#               THIS IS ONLY INFORMATIVE AND FOR EASY FIND INSTEAD OF
#               NAVIGATING THE PARAMETERS INSIDE THE OTL TYPE PROPERTIES WINDOW.




"""py_flam3.py loaded inside the Extra Files section. Renamed as py_flam3"""

"""First inside the OTL->type_properties->Scripts->PythonModule
the FLAM3 module is created out of the py_flam3 renamed file inside the Extra Files section"""
import toolutils
flam3 = toolutils.createModuleFromSection("flam3", kwargs["type"], "py_flam3")


"""Inside: OTL->type_properties->Scripts->PreFirstCreate
Check Houdini version and let us know."""
def flam3_first_time() -> None:
    hou_version = int(''.join(str(x) for x in hou.applicationVersion()[:2]))
    if hou_version < 190:
        hou.ui.displayMessage("Sorry, you need at least Houdini 19.0 to run FLAM3H", buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="Houdini version check", details=None, details_label=None, details_expanded=False)
flam3_first_time()

"""Inside: OTL->type_properties->Scripts->OnCreated
initialize what the tool need when you create its node in the network editor."""
kwargs["node"].hdaModule().flam3.flam3_default(kwargs["node"])
kwargs["node"].hdaModule().flam3.flam3_on_create(kwargs)

"""Inside: OTL->type_properties->Scripts->OnLoaded
When loading a hip file with a FLAM3H node in it do some checks."""
kwargs["node"].hdaModule().flam3.flam3_on_loaded(kwargs)


#######################################################
# GLOBAL Tab
#######################################################
'ptcount_presets'
'callback script'
hou.pwd().hdaModule().flam3.menu_density_set(kwargs['node'])
'Menu script'
menu = kwargs['node'].hdaModule().flam3.menu_density(kwargs['node'])
return menu


#######################################################
# SYS Tab
#######################################################

'loaddef'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3_default(kwargs['node'])

'sys_palettepresets'
'Callback Script'
hou.pwd().hdaModule().flam3.sys_json_to_ramp(kwargs)
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_ramp_presets(kwargs)
return menu
'Action Script'
kwargs['node'].hdaModule().flam3.json_to_ramp(kwargs)

'sys_inpresets'
'Callback Script'
hou.pwd().hdaModule().flam3.sys_apo_to_flam3(kwargs['node'])
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_apo_presets(kwargs)
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.apo_to_flam3(kwargs['node'])

'sys_outpresets'
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_out_contents_presets(kwargs)
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.out_XML(kwargs)

#######################################################
# PARAMETERS ITERATORS ( FLAME Tab )
#######################################################

'flamefunc'
'Callback Script'
hou.pwd().hdaModule().flam3.iteratorCountZero(kwargs['node'])

'activetip_#'
'Callback Script'
hou.pwd().hdaModule().flam3.ui_active_iterator_infos()

'prmpastesel_#'
'Callback Script'
hou.pwd().hdaModule().flam3.prm_paste_sel(kwargs)
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_copypaste(kwargs)
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.prm_paste(kwargs)

'varnote_#'
'Action Button'
kwargs['node'].hdaModule().flam3.ui_xaos_infos()

'All ITERATORS variations type parameters'
"pre1type_#, pre2type_#, v1type_#, v2type_#, v3type_#, v4type_#, p1type_#"
menu = kwargs['node'].hdaModule().flam3.menu_T(0)
return menu

'ang_#'
'Action Button'
kwargs['node'].hdaModule().flam3.reset_preaffine(kwargs)

'pang_#'
'Action Button'
kwargs['node'].hdaModule().flam3.reset_postaffine(kwargs)


#######################################################
# PARAMETERS FINAL FLAME ( FF Tab )
#######################################################


'ffprmpastesel'
'Callback Script'
hou.pwd().hdaModule().flam3.prm_paste_sel_FF(kwargs)
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_copypaste_FF(kwargs)
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.prm_paste_FF(kwargs)



'All FF variations type parameters'
"ffpre1type, ffv1type, ffv2type, ffp1type, ffp2type"
menu = kwargs['node'].hdaModule().flam3.menu_T(0)
return menu

'ffang'
'Action Button'
kwargs['node'].hdaModule().flam3.reset_preaffine_FF(kwargs)

'ffpang'
'Action Button'
kwargs['node'].hdaModule().flam3.reset_postaffine_FF(kwargs)


#######################################################
# PARAMETRS COLOR PALETTE ( CP Tab )
#######################################################

'hsv'
'Callback Script'
hou.pwd().hdaModule().flam3.palette_hsv(kwargs['node'])
'Action Button'
kwargs['node'].hdaModule().flam3.reset_CP(kwargs['node'], 2)

'palettehsv'
'Callback Script'
hou.pwd().hdaModule().flam3.palette_lock(kwargs['node'])
'Action Button'
kwargs['node'].hdaModule().flam3.palette_cp(kwargs['node'])

'palette'
'Callback Script'
hou.pwd().hdaModule().flam3.palette_cp(kwargs['node'])
'Action Button'
kwargs['node'].hdaModule().flam3.reset_CP(kwargs['node'], 3)

'palettefile'
'Callbac Script'
hou.pwd().hdaModule().flam3.init_presets(kwargs, "palettepresets")
'Action Button'
kwargs['node'].hdaModule().flam3.ramp_save(kwargs)

'palettepresets'
'Callback Script'
hou.pwd().hdaModule().flam3.json_to_ramp(kwargs)
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_ramp_presets(kwargs)
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.json_to_ramp(kwargs)

'mem_palettepresets'
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_ramp_presets(kwargs)
return menu


#######################################################
# PARAMETERS LOAD FLAMES ( IN Tab )
#######################################################


'inpresets'
'Callback Script'
hou.pwd().hdaModule().flam3.apo_to_flam3(kwargs['node'])
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_apo_presets(kwargs)
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.apo_to_flam3(kwargs['node'])

'inpath'
'Callback Script'
hou.pwd().hdaModule().flam3.init_presets(kwargs, "inpresets")

'iternumonload'
'Callback Script'
hou.pwd().hdaModule().flam3.iter_on_load_callback(kwargs['node'])

'useiteronload'
'Callback Script'
hou.pwd().hdaModule().flam3.use_iter_on_load_callback(kwargs['node'])


#######################################################
# PARAMETERS SAVE FLAMES ( OUT Tab )
#######################################################


'outpath'
'Callback Script'
hou.pwd().hdaModule().flam3.init_presets(kwargs, "outpresets")
'Action Button'
kwargs['node'].hdaModule().flam3.out_XML(kwargs)

'outpresets'
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_out_contents_presets(kwargs)
return menu

'outname'
'Callback Script'
hou.pwd().hdaModule().flam3.out_auto_add_iter_num(kwargs['node'])
'Action Button'
kwargs['node'].hdaModule().flam3.ui_OUT_presets_name_infos()

'outedit'
'Action Button'
kwargs['node'].hdaModule().flam3.reset_OUT(kwargs['node'], 1)

#######################################################
# PREFERENCES ( prefs Tab )
#######################################################

'xm'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3_xaos_convert(kwargs['node'])


