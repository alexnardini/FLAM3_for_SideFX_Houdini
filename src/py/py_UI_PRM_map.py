

#   Title:      SideFX Houdini FLAM3: 2D
#   Author:     Alessandro Nardini
#   date:       April 2023, Last revised April 2023
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
#               This is only informative and for easy find instead of
#               navigating the parameters inside the OTL type properties window.




"""py_flam3.py loaded inside the Extra Files section. Renamed as py_flam3"""

"""First inside the OTL->type_properties->Scripts->PythonModule
the FLAM3 module is created out of the py_flam3 renamed file inside the Extra Files section"""
import toolutils
flam3 = toolutils.createModuleFromSection("flam3", kwargs["type"], "py_flam3")

"""Inside: OTL->type_properties->Scripts->OnCreated
initialize what the tool need when you create its node in the network editor."""
kwargs["node"].hdaModule().flam3.flam3_default(kwargs["node"])
kwargs["node"].hdaModule().flam3.flam3_on_create(kwargs)



# SYS

'loaddef' 'Callback Script'
hou.pwd().hdaModule().flam3.flam3_default(kwargs['node'])

'sysaporeload' 'Callback Script'
hou.pwd().hdaModule().flam3.apo_to_flam3(kwargs['node'])



# PARAMETERS ITERATORS ( FLAME Tab )

'flamefunc' 'Callback Script'
hou.pwd().hdaModule().flam3.iteratorCountZero(kwargs['node'])

'activetip_#' 'Callback Script'
hou.pwd().hdaModule().flam3.ui_active_iterator_infos()

'prmpastesel_#'
'Callback Script'
hou.pwd().hdaModule().flam3.prm_paste_sel(kwargs)
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_copypaste(kwargs)
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.prm_paste(kwargs)

'varnote_#' 'Action Button'
kwargs['node'].hdaModule().flam3.ui_xaos_infos()

'All ITERATORS variations type parameters'
"pre1type_#, pre2type_#, v1type_#, v2type_#, v3type_#, v4type_#, p1type_#"
menu = kwargs['node'].hdaModule().flam3.menu_T(0)
return menu

'ang_#' 'Action Button'
kwargs['node'].hdaModule().flam3.reset_preaffine(kwargs)

'pang_#' 'Action Button'
kwargs['node'].hdaModule().flam3.reset_postaffine(kwargs)



# PARAMETERS FINAL FLAME ( FF Tab )


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

'ffang' 'Action Button'
kwargs['node'].hdaModule().flam3.reset_preaffine_FF(kwargs)

'ffpang' 'Action Button'
kwargs['node'].hdaModule().flam3.reset_postaffine_FF(kwargs)


# PARAMETRS COLOR PALETTE ( CP Tab )

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



# PARAMETERS LOAD FLAMES ( IN Tab )

'aporeload' 'Callback Script'
hou.pwd().hdaModule().flam3.apo_to_flam3(kwargs['node'])

'inpresets'
'Callback Script'
hou.pwd().hdaModule().flam3.apo_to_flam3(kwargs['node'])
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_apo_presets(kwargs)
return menu

'inpath' 'Callback Script'
hou.pwd().hdaModule().flam3.init_presets(kwargs, "inpresets")

'iternumonload' 'Callback Script'
hou.pwd().hdaModule().flam3.iter_on_load_callback(kwargs['node'])

'useiteronload' 'Callback Script'
hou.pwd().hdaModule().flam3.use_iter_on_load_callback(kwargs['node'])



# PARAMETERS SAVE FLAMES ( OUT Tab )

'outpath'
'Callback Script'
hou.pwd().hdaModule().flam3.init_presets(kwargs, "outpresets")
'Action Button'
kwargs['node'].hdaModule().flam3.out_XML(kwargs)

'outpresets'
'Callback Script'
hou.pwd().hdaModule().flam3.apo_to_flam3_OUT_STATS(kwargs['node'])
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.menu_out_contents_presets(kwargs)
return menu

'outname' 'Action Button'
kwargs['node'].hdaModule().flam3.ui_OUT_presets_name_infos()

'outedit' 'Action Button'
kwargs['node'].hdaModule().flam3.reset_OUT(kwargs['node'], 1)


# PREFERENCES ( prefs Tab )

'xm' 'Callback Script'
hou.pwd().hdaModule().flam3.flam3_xaos_convert(kwargs['node'])


