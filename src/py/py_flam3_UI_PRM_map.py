

#   Title:      SideFX Houdini FLAM3: MAP PRM Definitions
#   Author:     Alessandro Nardini
#   date:       April 2023, Last revised January 2024
#
#   Name:       PY_MAP "Whatever"
#
#   Comment:    List of all UI parameters wired with a python definition
#               and the command string they actually run and from where.
#
#               THIS IS ONLY INFORMATIVE AND FOR EASY FIND INSTEAD OF
#               NAVIGATING THE PARAMETERS INSIDE THE OTL TYPE PROPERTIES WINDOW.





"""
py_flam3.py loaded inside the Extra Files section. Renamed as py_flam3
"""

"""
First inside the OTL->type_properties->Scripts->PythonModule
the FLAM3 module is created out of the py_flam3's renamed file inside the Extra Files section.
"""
import toolutils
flam3 = toolutils.createModuleFromSection("flam3", kwargs["type"], "py_flam3")



"""
Inside: OTL->type_properties->Scripts->PreFirstCreate
"""
FLAM3H_VERSION = '1.2.30 - Gold'

def flam3h_first_time() -> None:
    hou_version = int(''.join(str(x) for x in hou.applicationVersion()[:1]))
    if hou_version < 19:
        hou.ui.displayMessage("Sorry, you need Houdini 19 or higher to run FLAM3H", buttons=("Got it, thank you",), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title="Houdini version check", details=None, details_label=None, details_expanded=False)

def flam3h_sys_updated_mode() -> None:
    current = hou.updateModeSetting()
    hou.session.FLAM3H_SYS_UPDATE_MODE = current

def flam3h_compile_first_time_msg() -> None:
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

    if first_instance_32bit:
        _MSG_INFO = f"\nversion: {FLAM3H_VERSION}\nFLAM3H CVEX node need to cook once to compile its definition\nfor this Houdini session.\n\nDepending on your PC configuration\nit can take anywhere between 30s and 1 minute.\nIt is a one time compile process.\n"
        print(_MSG_INFO)
        hou.ui.setStatusMessage(_MSG_INFO, hou.severityType.Warning) # type: ignore
        
    # we skip 64bit check for now as FLAM3H should always be at 32bit to start with.


flam3h_first_time()
flam3h_sys_updated_mode()
flam3h_compile_first_time_msg()





"""
Inside: OTL->type_properties->Scripts->OnCreated
initialize what the tool need when you create its node in the network editor.
"""
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_create()



"""
Inside: OTL->type_properties->Scripts->OnLoaded
When loading a hip file with a FLAM3H node in it do some checks.
"""
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_loaded()



"""
Inside: OTL->type_properties->Scripts->OnDeleted
When deleting a FLAM3H node.
"""
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_deleted()



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

'parameter name     sys_help'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_display_help()


'parameter name     sys_out_sensorviz'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle()


'parameter name     sys_tag_off'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle()


'parameter name     sys_tag'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_sys_tag()


'parameter name:    loaddef'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_default()


'parameter name:    frameview'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_viewport_bbox_frame()


'parameter name:    frameviewsensor'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_viewport_bbox_frame()


'parameter name:    sys_palettepresets'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp_sys(False)
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_ramp_presets()
return menu
'script type:       Action Script'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()


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


'parameter name:    doiter_disabled_#'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_keep_last_vactive_STAR()


'parameter name:    doiter_#'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_keep_last_vactive_STAR()


'parameter name:    activetip_#'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_ui_msg_utils(kwargs).ui_active_iterator_infos()


'parameter name:    iw_#'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_keep_last_weight()


'parameter name:    prmpastesel_#'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel()
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste()
return menu
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste()


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
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets_CP_PALETTE_PRESETS()
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).flam3h_ramp_save()


'parameter name:    palettepresets'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp(False)
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_ramp_presets()
return menu
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()



#######################################################
# PARAMETERS LOAD FLAMES ( IN Tab )
#######################################################


'parameter name:    inpath'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets_IN_PRESETS()


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


'parameter name:    remappgb'
'script type:       Menu Script'
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_toggle_pgb()


'parameter name:    propertiescp'
'script type:       Menu Script'
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_toggle("propertiescp")


'parameter name:    cprendervals'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_stats_msg(kwargs)



#######################################################
# PARAMETERS SAVE FLAMES ( OUT Tab )
#######################################################


'parameter name:    outpath'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets_OUT_PRESETS()


'parameter name:    outname'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_add_iter_num_to_prm()
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_XML()


'parameter name:    outpresets'
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.flam3h_ui_msg_utils(kwargs).ui_OUT_presets_name_infos()


'parameter name:    outedit'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_off("outsensor")
'script type:       Action Button'
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).reset_OUT_kwargs()


'parameter name:    out_sensorviz_disabled'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle()


'parameter name:    out_sensorviz'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle()


'parameter name:    outres'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)


'parameter name:    outrespresets'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).menu_sensor_resolution_set(False)
'script type:       Menu Script'
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_sensor_resolution()
return menu


'parameter name:    outcprendervals'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_stats_msg(kwargs)


'parameter name:    outcenter'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)


'parameter name:    outrotate'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)


'parameter name:    outscale'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)


'parameter name:    outsensorupdate'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)



#######################################################
# PREFERENCES ( prefs Tab )
#######################################################

'parameter name:    xm'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_xaos_convert()


'parameter name:    vex_precision'
'script type:       Callback Script'
hou.pwd().hdaModule().flam3.flam3h_scripts(kwargs).flam3h_check_first_node_instance_prefs_cvex_precision_msg()


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

