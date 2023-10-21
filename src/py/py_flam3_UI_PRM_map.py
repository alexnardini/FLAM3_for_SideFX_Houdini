

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
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_create()



"""Inside: OTL->type_properties->Scripts->OnLoaded
When loading a hip file with a FLAM3H node in it do some checks."""
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_loaded()
kwargs["node"].hdaModule().flam3.flam3h_iterator_utils(kwargs).auto_set_xaos()



#######################################################
# GLOBAL Tab
#######################################################

'parameter name:    ptcount_presets'
'script type:       callback script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density_set()
'Menu script'
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density()
return menu

'parameter name:    iter'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_change_iter_num_to_prm()



#######################################################
# SYS Tab
#######################################################

'parameter name:    loaddef'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_default()


'parameter name:    sys_palettepresets'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_ramp_sys()
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_ramp_presets()
return menu
'script type:       Action Script'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_ramp()


'parameter name:    sys_inpresets'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_sys()
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets()
return menu
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()


'parameter name:    sys_outpresets'
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_XML(kwargs)



#######################################################
# PARAMETERS ITERATORS ( FLAME Tab )
#######################################################

'parameter name:    flamefunc'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterators_count()


'parameter name:    prmpastesel_#'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel()
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste()

return menu
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste()


'parameter name:    activetip_#'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_ui_msg_utils(kwargs).ui_active_iterator_infos()


'parameter name:    vactive_#'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).vactive_keep_last()


'parameter name:    xaos_#'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_ui_msg_utils(kwargs).ui_xaos_infos()


'All ITERATORS variations type parameters'
"parameter name:    pre1type_#, pre2type_#, v1type_#, v2type_#, v3type_#, v4type_#, p1type_#"
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils.menu_T(0)
return menu


'parameter name:    ang_#'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_preaffine()


'parameter name:    pang_#'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_postaffine()



#######################################################
# PARAMETERS FINAL FLAME ( FF Tab )
#######################################################

'parameter name:    ffprmpastesel_#'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_FF()
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste_FF()
return menu
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_FF()


'All FF variations type parameters'
"parameter name:    ffpre1type, ffv1type, ffv2type, ffp1type, ffp2type"
'script type:       Callback Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils.menu_T(0)
return menu


'parameter name:    ffang'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_preaffine_FF()


'parameter name:    ffpang'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_postaffine_FF()



#######################################################
# PARAMETRS COLOR PALETTE ( CP Tab )
#######################################################

'parameter name:    hsv'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_hsv()
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).reset_CP(2)


'parameter name:    palettehsv'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_lock()
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).palette_cp()


'parameter name:    palette'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_cp()
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).reset_CP(3)


'parameter name:    palettefile'
'script type:       Callbac Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets("palettepresets")
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).ramp_save()


'parameter name:    palettepresets'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_ramp()
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_ramp_presets()
return menu
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_ramp()



#######################################################
# PARAMETERS LOAD FLAMES ( IN Tab )
#######################################################


'parameter name:    inpath'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets("inpresets")


'parameter name:    inpresets'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets()
return menu
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()


'parameter name:    iternumonload'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).set_iter_on_load_callback()


'parameter name:    useiteronload'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).use_iter_on_load_callback()


'parameter name:    cprendervals'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_copy_render_stats_msg(kwargs['node'])



#######################################################
# PARAMETERS SAVE FLAMES ( OUT Tab )
#######################################################


'parameter name:    outpath'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets("outpresets")
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_XML()


'parameter name:    outname'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_add_iter_num_to_prm()
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_ui_msg_utils(kwargs).ui_OUT_presets_name_infos()


'parameter name:    outpresets'
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu


'parameter name:    outedit'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).reset_OUT()



#######################################################
# PREFERENCES ( prefs Tab )
#######################################################

'parameter name:    xm'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_xaos_convert()


'parameter name:    autoxaos'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).auto_set_xaos()


'parameter name:    setdark'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).colorSchemeDark()


'parameter name:    vptype'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleDisplay()


'parameter name:    vpptsize'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleSize()



#######################################################
# ABOUT ( about Tab )
#######################################################

'parameter name:    flam3homepage'
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_about_web_homepage()


'parameter name:    flam3github'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_about_web_github()


'parameter name:    flam3insta'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_about_web_instagram()


'parameter name:    tffa_pdf'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_about_web_paper()


'parameter name:    tffa_flam3github'
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_about_web_flam3_github()

