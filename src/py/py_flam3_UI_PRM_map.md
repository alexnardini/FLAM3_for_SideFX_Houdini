

```python
#   Title:      FLAM3H. SideFX Houdini FLAM3: PYTHON MAP PRM Definitions
#   Author:     Alessandro Nardini
#   date:       April 2023, Last revised October 2024
#
#   Name:       PY_FLAM3_UI_PRM_MAP
#
#   Comment:    List of all UI parameters wired with a python definition
#               and the command string they actually run and from where.
#
#               THIS IS ONLY INFORMATIVE AND FOR EASY FIND INSTEAD OF
#               NAVIGATING THE PARAMETERS INSIDE THE OTL TYPE PROPERTIES WINDOW.
```


<br>
<br>



The file **`py_flam3.py`** is loaded inside the **Extra Files** section. Renamed as **`py_flam3`** (no extension).

First inside the **OTL**->**type_properties**->**Scripts**->**PythonModule**:
the FLAM3 module is created out of the **`py_flam3`** renamed file inside the **Extra Files** section.

```python
import toolutils
flam3 = toolutils.createModuleFromSection("flam3", kwargs["type"], "py_flam3")
```

Inside: **OTL**->**type_properties**->**Scripts**->**PreFirstCreate**: Before the node is even created but invoked.

```python
FLAM3H_VERSION = '1.5.00 - Gold'

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
        _MSG_INFO = f"\nFLAM3H version: {FLAM3H_VERSION}\nThe CVEX nodes need to cook once to compile their definitions.\n\nDepending on your PC configuration it can take up to 1 minute.\nIt is a one time compile process.\n"
        print(_MSG_INFO)
        hou.ui.setStatusMessage(_MSG_INFO, hou.severityType.Warning) # type: ignore
        
    # we skip 64bit check for now as FLAM3H should always be at 32bit to start with.


flam3h_first_time()
flam3h_sys_updated_mode()
flam3h_compile_first_time_msg()
```

Inside: **OTL**->**type_properties**->**Scripts**->**OnCreated**:
initialize what the tool need when you create its node in the network editor.
```python
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_create()
```

Inside: **OTL**->**type_properties**->**Scripts**->**OnLoaded**:
When loading a hip file with a FLAM3H node in it do some checks.
```python
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_loaded()
```

Inside: **OTL**->**type_properties**->**Scripts**->**OnDeleted**:
When deleting a FLAM3H node.
```python
kwargs["node"].hdaModule().flam3.flam3h_scripts(kwargs).flam3h_on_deleted()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


# GLOBAL Tab
# parameter name:    `ptcount_presets`
### Callback script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density_set()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density()
return menu
```
### Action Script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_global_density_set_default()
```
# GLOBAL Tab
# parameter name:    `iter`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_change_iter_num_to_prm()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

# SYS Tab
# parameter name:    `sys_help`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_display_help()
```
# SYS Tab
# parameter name:    `iterlist`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_select_iterator()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_SEL_ITER()
return menu
```
# SYS Tab
# parameter name:    `doff_sysdisabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle("doff")
```
# SYS Tab
# parameter name:    `doff_sysenabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle("doff")
```
# SYS Tab
# parameter name:    `rip_disabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle("rip")
```
# SYS Tab
# parameter name:    `rip_enabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle("rip")
```
# SYS Tab
# parameter name:    `f3c_chaotica`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle("f3c")
```
# SYS Tab
# parameter name:    `f3c_apophysis`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle("f3c")
```
# SYS Tab
# parameter name:    `sys_out_sensorviz`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle()
```
# SYS Tab
# parameter name:    `sys_out_sensorviz_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle()
```
# SYS Tab
# parameter name:    `sys_tag_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle()
```
# SYS Tab
# parameter name:    `sys_tag`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_sys_tag()
```
# SYS Tab
# parameter name:    `loaddef`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_default()
```
# SYS Tab
# parameter name:    `frameview`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_viewport_bbox_frame()
```
# SYS Tab
# parameter name:    `frameviewsensor`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```
# SYS Tab
# parameter name:    `sys_palettepresets_disabled`
### Action Button script
```python
n = None
```
# SYS Tab
# parameter name:    `sys_palettepresets_off`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets_empty()
return menu
```
### Action Button Script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()
```
# SYS Tab
# parameter name:    `sys_palettepresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp_sys(False)
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets()
return menu
```
### Action Button Script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()
```
# SYS Tab
# parameter name:    `sys_inpresets_disabled`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets_empty()
return menu
```
### Action Button script
```python
n = None
```
# SYS Tab
# parameter name:    `sys_inpresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_sys()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
```
# SYS Tab
# parameter name:    `sys_outpresets_disabled`
### Action Button script
```python
n = None
```
# SYS Tab
# parameter name:    `sys_outpresets`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_XML(kwargs)
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

# FLAME Tab
# parameter name:    `flamefunc`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterators_count()
```
# FLAME Tab
# parameter name:    `doiter_disabled_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_keep_last_vactive_STAR()
```
# FLAME Tab
# parameter name:    `doiter_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_keep_last_vactive_STAR()
```
# FLAME Tab
# parameter name:    `activetip_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_ui_msg_utils(kwargs).ui_active_iterator_infos()
```
# FLAME Tab
### parameter name:    `iw_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_keep_last_weight()
```
# FLAME Tab
# parameter name:    `prmpastesel_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste()
return menu
```
# FLAME Tab
### parameter name:    `xaos_#`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_ui_msg_utils(kwargs).ui_xaos_infos()
return menu
```
# FLAME Tab
# parameter name:    `alpha_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils.destroy_data(kwargs['node'], 'iter_sel')
```
# FLAME Tab
### parameter name:    `preblurtype_#`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T_pb()
return menu
```
# FLAME Tab
# parameter name:    `pre1type_#`, `pre2type_#`, `p1type_#`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T_PP()
return menu
```
# FLAME Tab
# parameter name:    `v1type_#`, `v2type_#`, `v3type_#`, `v4type_#`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_T()
return menu
```
# FLAME Tab
# parameter name:    `scl_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_affine_scale()
```
### Action Button script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_pre_affine()
```
# FLAME Tab
# parameter name:    `ang_#`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_preaffine()
```
# FLAME Tab
# parameter name:    `pscl_#`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_post_affine_scale()
```
### Action Button script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_post_affine()
```
# FLAME Tab
# parameter name:    `pang_#`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_postaffine()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

# FF Tab
# parameter name:    `ffprmpastesel`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_FF()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).menu_copypaste_FF()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_FF()
```
# FF Tab
# parameter name:    `ffpre1type`, `ffp1type`, `ffp2type`
### Callback Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils.menu_T_PP(True)
return menu
```
# FF Tab
# parameter name:    `ffv1type`, `ffv2type`
### Callback Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_iterator_utils.menu_T(True)
return menu
```
# FF Tab
# parameter name:    `ffscl`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_FF_affine_scale()
```
### Action Button script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_pre_affine_FF()
```
# FF Tab
# parameter name:    `ffang`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_preaffine_FF()
```
# FF Tab
# parameter name:    `ffpscl`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).iterator_FF_post_affine_scale()
```
### Action Button script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).prm_paste_sel_post_affine_FF()
```
# FF Tab
# parameter name:    `ffpang`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_iterator_utils(kwargs).reset_postaffine_FF()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

# CP Tab
# parameter name:    `hsv`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_hsv()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).reset_CP(2)
```
# CP Tab
# parameter name:    `palettehsv`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_lock()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).palette_cp()
```
# CP Tab
# parameter name:    `palette`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).palette_cp()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).reset_CP(3)
```
# CP Tab
# parameter name:    `palettefile`
### Callbac Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets_CP_PALETTE_PRESETS()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).flam3h_ramp_save()
```
# CP Tab
# parameter name:    `palettepresets_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp(False)
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets_empty()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()
```
# CP Tab
# parameter name:    `palettepresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp(False)
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).menu_cp_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_palette_utils(kwargs).json_to_flam3h_ramp()
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


# IN Tab
# parameter name:    `inpath`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets_IN_PRESETS()
```
# IN Tab
# parameter name:    `inpresets_disabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets_empty()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
```
# IN Tab
# parameter name:    `inpresets`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).menu_in_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h()
```
# IN Tab
# parameter name:    `iternumonload`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).set_iter_on_load_callback()
```
# IN Tab
# parameter name:    `useiteronload`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).use_iter_on_load_callback()
```
# IN Tab
# parameter name:    `oritername`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils(kwargs).use_iter_on_load_callback()
```
# IN Tab
# parameter name:    `in_f3h_affine`
### Menu Script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_toggle_f3h_affine()
```
# IN Tab
# parameter name:    `remappgb`
### Menu Script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_toggle_pgb()
```
# IN Tab
# parameter name:    `propertiescp`
### Menu Script
```python
kwargs['node'].hdaModule().flam3.in_flame_utils(kwargs).in_to_flam3h_toggle("propertiescp")
```
# IN Tab
# parameter name:    `cprendervals`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_all_stats_msg(kwargs)
```
# IN Tab
# parameter name:    `cprendervals_cb`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_all_stats_msg(kwargs)
```
# IN Tab
# parameter name:    `icon_in_infos_sensor`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_sensor_stats_msg(kwargs)
```
# IN Tab
# parameter name:    `icon_in_infos_render`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_stats_msg(kwargs)
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


# OUT Tab
# parameter name:    `outpath`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_init_presets_OUT_PRESETS()
```
# OUT Tab
# parameter name:    `outname`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_add_iter_num_to_prm()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_XML()
```
# OUT Tab
# parameter name:    `outpresets`
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_out_contents_presets()
return menu
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).out_presets_copy_menu_label_callback()
```
# OUT Tab
# parameter name:    `autoadditer`
### Callback Script
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).out_auto_change_iter_num_to_prm()
```
# OUT Tab
# parameter name:    `outedit`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_toggle_off("outsensor")
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).reset_OUT_kwargs()
```
# OUT Tab
# parameter name:    `out_sensorviz_disabled`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle()
```
# OUT Tab
# parameter name:    `out_sensorviz`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle()
```
# OUT Tab
'parameter name:    `out_sensorviz_off`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).flam3h_outsensor_toggle()
```
# OUT Tab
# parameter name:    `outres`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```
# OUT Tab
# parameter name:    `outrespresets`
### Callback Script'
```python
hou.pwd().hdaModule().flam3.out_flame_utils(kwargs).menu_sensor_resolution_set(False)
```
### Menu Script
```python
menu = kwargs['node'].hdaModule().flam3.out_flame_utils(kwargs).menu_sensor_resolution()
return menu
```
# OUT Tab
# parameter name:    `outcprendervals`
### Callback Script
```python
hou.pwd().hdaModule().flam3.in_flame_utils.in_copy_render_stats_msg(kwargs)
```
# OUT Tab
# parameter name:    `outcenter`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```
# OUT Tab
# parameter name:    `outrotate`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```
# OUT Tab
# parameter name:    `outscale`
### Callback Script'
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```
# OUT Tab
# parameter name:    `outsensorupdate`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).util_set_front_viewer(False)
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


# prefs Tab
# parameter name:    `enumeratemenu`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).menus_refresh_enum_prefs()
```
# prefs Tab
# parameter name:    `itericons`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).refresh_iterator_vars_menu()
```
# prefs Tab
# parameter name:    `xm`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).flam3h_xaos_convert()
```
# prefs Tab
# parameter name:    `vex_precision`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_scripts(kwargs).flam3h_check_first_node_instance_prefs_cvex_precision_msg()
```
# prefs Tab
# parameter name:    `autoxaos`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_iterator_utils(kwargs).auto_set_xaos()
```
# prefs Tab
# parameter name:    `setdark`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).colorSchemeDark()
```
# prefs Tab
# parameter name:    `vptype`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleDisplay()
```
# prefs Tab
# parameter name:    `vpptsize`
### Callback Script
```python
hou.pwd().hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleSize()
```
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_general_utils(kwargs).viewportParticleSize(1.0)
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


# about Tab
# parameter name:    `flam3homepage`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('web')
```
# about Tab
# parameter name:    `flam3github`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('git')
```
# about Tab
# parameter name:    `flam3insta`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('insta')
```
# about Tab
# parameter name:    `flam3youtube`
'script type:       Action Button script'
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('youtube')
```
# about Tab
# parameter name:    `tffa_pdf`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('paper')
```
# about Tab
# parameter name:    `tffa_flam3github`
### Action Button script
```python
kwargs['node'].hdaModule().flam3.flam3h_about_utils(kwargs).flam3h_web_run('flam3git')
```