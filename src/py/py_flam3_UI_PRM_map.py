

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
# Check Houdini version
def flam3_first_time() -> None:
    hou_version = int(''.join(str(x) for x in hou.applicationVersion()[:1]))
    if hou_version != 19:
        hou.ui.displayMessage("Sorry, you need Houdini 19 or 19.5 to run FLAM3H", buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="Houdini version check", details=None, details_label=None, details_expanded=False)
flam3_first_time()


"""Inside: OTL->type_properties->Scripts->OnCreated
initialize what the tool need when you create its node in the network editor."""
kwargs["node"].hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_default()
kwargs["node"].hdaModule().flam3.flam3h_iterator_utils(kwargs).auto_set_xaos()
kwargs["node"].hdaModule().flam3.flam3h_on_create(kwargs)



"""Inside: OTL->type_properties->Scripts->OnLoaded
When loading a hip file with a FLAM3H node in it do some checks."""
kwargs["node"].hdaModule().flam3.flam3h_on_loaded(kwargs)
kwargs["node"].hdaModule().flam3.flam3h_iterator_utils(kwargs).auto_set_xaos()



#######################################################
# GLOBAL Tab
#######################################################
'ptcount_presets'
'callback script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density_set()
'Menu script'
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density()
return menu

'iter'
'Callback Script'
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_change_iter_num_to_prm()


#######################################################
# SYS Tab
#######################################################

'loaddef'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_default()

'sys_palettepresets'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).sys_json_to_ramp()
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_ramp_presets()
return menu
'Action Script'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_ramp()

'sys_inpresets'
'Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_sys()
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets()
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()

'sys_outpresets'
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_XML(kwargs)

#######################################################
# PARAMETERS ITERATORS ( FLAME Tab )
#######################################################

'flamefunc'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterators_count()

'prmpastesel_#'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel()
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste()
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste()

'activetip_#'
'Callback Script'
hou.pwd().hdaModule().flam3.ui_active_iterator_infos()

'vactive_#'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).vactive_keep_last()

'xaos_#'
'Action Button'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).auto_set_xaos()

'All ITERATORS variations type parameters'
"pre1type_#, pre2type_#, v1type_#, v2type_#, v3type_#, v4type_#, p1type_#"
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils.menu_T(0)
return menu

'ang_#'
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_preaffine()

'pang_#'
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_postaffine()


#######################################################
# PARAMETERS FINAL FLAME ( FF Tab )
#######################################################

'ffprmpastesel_#'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_FF()
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste_FF()
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_FF()

'All FF variations type parameters'
"ffpre1type_#, ffv1type_#, ffv2type_#, ffp1type_#, ffp2type_#"
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils.menu_T(0)
return menu

'ffang_#'
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_preaffine_FF()

'ffpang_#'
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_postaffine_FF()



#######################################################
# PARAMETRS COLOR PALETTE ( CP Tab )
#######################################################

'hsv'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_hsv()
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).reset_CP(2)

'palettehsv'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_lock()
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).palette_cp()

'palette'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_cp()
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).reset_CP(3)

'palettefile'
'Callbac Script'
hou.pwd().hdaModule().flam3.flam3h_init_presets(kwargs, "palettepresets")
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).ramp_save()

'palettepresets'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_ramp()
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_ramp_presets()
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_ramp()



#######################################################
# PARAMETERS LOAD FLAMES ( IN Tab )
#######################################################


'inpath'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_init_presets(kwargs, "inpresets")

'inpresets'
'Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets()
return menu
'Action Button'
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()

'iternumonload'
'Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).set_iter_on_load_callback()

'useiteronload'
'Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).use_iter_on_load_callback()

'cprendervals'
'Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_copy_render_stats_msg(kwargs['node'])


#######################################################
# PARAMETERS SAVE FLAMES ( OUT Tab )
#######################################################


'outpath'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_init_presets(kwargs, "outpresets")
'Action Button'
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_XML()

'outname'
'Callback Script'
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_add_iter_num_to_prm()
'Action Button'
kwargs['node'].hdaModule().flam3.ui_OUT_presets_name_infos()

'outpresets'
'Menu Script'
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu

'outedit'
'Action Button'
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).reset_OUT()


#######################################################
# PREFERENCES ( prefs Tab )
#######################################################

'xm'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3_xaos_convert()

'autoxaos'
'allback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).auto_set_xaos()

'setdark'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).colorSchemeDark()

'vptype'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleDisplay()

'vpptsize'
'Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleSize()