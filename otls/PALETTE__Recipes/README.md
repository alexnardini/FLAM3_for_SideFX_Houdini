## FLAM3H™ Palette recipes HDAs ##
### Houdini version: H21, H22 and up ###

<br>

These **H**oudini **D**igital **A**ssets collect all the **FLAM3H™** palette available inside the palette libraries JSON files but converted into a Houdini native Recipe format. In **H22** and up they will show up also inside the new ramp gallery panel which is really nice.

You need to copy those files inside: `$HOME/houdini‹X›.‹Y›/otls/` (where ‹X›.‹Y› is the version number of Houdini).

They work with **H21**, **H22** and up.

<br>

- _These new Recipes have been organized into 2(two) separate Houdini Digital Assets:_
    
    - **alexnardini__FLAM3H_f3h_palette.hda** ( _FLAM3H™ palette libs_ )
    - **alexnardini__FLAM3H_apo_palette.hda** ( _APOPHYSIS palette libs_ )

</br>
</br>
</br>
</br>

# Contents

</br>

For a visual preview of all the palette presets included: 
[**`Palette library previews`**](../../__FLAM3H_palette_libs/README.md#palette-previews)</br>

</br>
</br>

A list of all Recipe HDA definition names and their categories.<br />
You can display their help card using the following python template code (_copy it inside a python SOP node_):

   ```python
   # The name of the Recipe HDA definition for which you want to display the Help.
   #
   # Just change it with the one you desire to display its help card:
   definition_name: str = "alexnardini::Data/f3h_archviz_hq_set_a_01"

   # Get its node type
   definition_node_type: hou.OpNodeType = hou.nodeType(definition_name)

   # Display its Documentation
   hou.ui.displayNodeHelp(definition_node_type)

   # You can also print its internal version number
   print(definition_node_type.definition().version())
   ```

<details>
<summary>
<img src="../../icons/iconSVGR.svg" width="64" height="40" style="vertical-align: middle;">
<h1 style="display: inline;">FLAM3H™ Palette libs</h1>
</summary>

</br>

- alexnardini::Data/f3h_50s_superman<br />
- alexnardini::Data/f3h_50s_thor<br />
- alexnardini::Data/f3h_50s_batman<br />
- alexnardini::Data/f3h_50s_spiderman<br />
- alexnardini::Data/f3h_50s_old_superman<br />
- alexnardini::Data/f3h_50s_old_batman<br />
- alexnardini::Data/f3h_50s_old_wolverine<br />
- alexnardini::Data/f3h_50s_x_man_origin_wolverine<br />
- alexnardini::Data/f3h_50s_hulk<br />
- alexnardini::Data/f3h_50s_fat_batman<br />
- alexnardini::Data/f3h_50s_young_joker<br />
- alexnardini::Data/f3h_50s_fat_captain_america<br />
- alexnardini::Data/f3h_50s_fat_ironman<br />
- alexnardini::Data/f3h_50s_fat_x_man_origin_wolverine<br />
- alexnardini::Data/f3h_50s_fat_deadpool<br />
- alexnardini::Data/f3h_50s_old_x_man<br />
- alexnardini::Data/f3h_50s_old_captain_america<br />
- alexnardini::Data/f3h_50s_fat_spiderman<br />
- alexnardini::Data/f3h_50s_akira<br />
- alexnardini::Data/f3h_50s_demon_in_the_wood<br />
- alexnardini::Data/f3h_50s_old_demon_in_roots<br />
- alexnardini::Data/f3h_50s_tree_man<br />
- alexnardini::Data/f3h_50s_tree_goblin<br />
- alexnardini::Data/f3h_50s_goblin<br />
- alexnardini::Data/f3h_archviz_hq_set_a_02<br />
- alexnardini::Data/f3h_archviz_hq_set_a_03<br />
- alexnardini::Data/f3h_archviz_hq_set_a_04<br />
- alexnardini::Data/f3h_archviz_hq_set_a_05<br />
- alexnardini::Data/f3h_archviz_hq_set_a_06<br />
- alexnardini::Data/f3h_archviz_hq_set_a_07<br />
- alexnardini::Data/f3h_archviz_hq_set_a_08<br />
- alexnardini::Data/f3h_archviz_hq_set_a_09<br />
- alexnardini::Data/f3h_archviz_hq_set_a_10<br />
- alexnardini::Data/f3h_archviz_hq_set_a_11<br />
- alexnardini::Data/f3h_archviz_hq_set_a_12<br />
- alexnardini::Data/f3h_archviz_hq_set_a_13<br />
- alexnardini::Data/f3h_archviz_hq_set_a_14<br />
- alexnardini::Data/f3h_archviz_hq_set_a_15<br />
- alexnardini::Data/f3h_archviz_hq_set_a_16<br />
- alexnardini::Data/f3h_archviz_hq_set_a_17<br />
- alexnardini::Data/f3h_archviz_hq_set_a_18<br />
- alexnardini::Data/f3h_archviz_hq_set_a_19<br />
- alexnardini::Data/f3h_archviz_hq_set_a_20<br />
- alexnardini::Data/f3h_archviz_hq_set_a_21<br />
- alexnardini::Data/f3h_archviz_hq_set_a_22<br />
- alexnardini::Data/f3h_archviz_hq_set_a_23<br />
- alexnardini::Data/f3h_archviz_hq_set_a_24<br />
- alexnardini::Data/f3h_archviz_hq_set_a_25<br />
- alexnardini::Data/f3h_archviz_hq_set_a_26<br />
- alexnardini::Data/f3h_archviz_hq_set_b_01<br />
- alexnardini::Data/f3h_archviz_hq_set_b_02<br />
- alexnardini::Data/f3h_archviz_hq_set_b_03<br />
- alexnardini::Data/f3h_archviz_hq_set_b_04<br />
- alexnardini::Data/f3h_archviz_hq_set_b_05<br />
- alexnardini::Data/f3h_archviz_hq_set_b_06<br />
- alexnardini::Data/f3h_archviz_hq_set_b_07<br />
- alexnardini::Data/f3h_archviz_hq_set_b_08<br />
- alexnardini::Data/f3h_archviz_hq_set_b_09<br />
- alexnardini::Data/f3h_archviz_hq_set_b_10<br />
- alexnardini::Data/f3h_archviz_hq_set_b_11<br />
- alexnardini::Data/f3h_archviz_hq_set_b_12<br />
- alexnardini::Data/f3h_archviz_hq_set_b_14<br />
- alexnardini::Data/f3h_archviz_hq_set_b_15<br />
- alexnardini::Data/f3h_archviz_hq_set_b_16<br />
- alexnardini::Data/f3h_archviz_hq_set_b_17<br />
- alexnardini::Data/f3h_archviz_hq_set_b_18<br />
- alexnardini::Data/f3h_archviz_hq_set_b_19<br />
- alexnardini::Data/f3h_archviz_hq_set_b_20<br />
- alexnardini::Data/f3h_archviz_hq_set_b_21<br />
- alexnardini::Data/f3h_archviz_hq_set_b_22<br />
- alexnardini::Data/f3h_archviz_hq_set_b_23<br />
- alexnardini::Data/f3h_archviz_hq_set_b_24<br />
- alexnardini::Data/f3h_archviz_hq_set_c_01<br />
- alexnardini::Data/f3h_archviz_hq_set_c_02<br />
- alexnardini::Data/f3h_archviz_hq_set_c_03<br />
- alexnardini::Data/f3h_archviz_hq_set_c_04<br />
- alexnardini::Data/f3h_archviz_hq_set_c_05<br />
- alexnardini::Data/f3h_archviz_hq_set_c_06<br />
- alexnardini::Data/f3h_archviz_hq_set_c_07<br />
- alexnardini::Data/f3h_archviz_hq_set_c_08<br />
- alexnardini::Data/f3h_archviz_hq_set_c_09<br />
- alexnardini::Data/f3h_archviz_hq_set_c_10<br />
- alexnardini::Data/f3h_archviz_hq_set_c_11<br />
- alexnardini::Data/f3h_archviz_hq_set_c_12<br />
- alexnardini::Data/f3h_archviz_hq_set_c_13<br />
- alexnardini::Data/f3h_archviz_hq_set_c_14<br />
- alexnardini::Data/f3h_archviz_hq_set_c_15<br />
- alexnardini::Data/f3h_archviz_hq_set_c_16<br />
- alexnardini::Data/f3h_archviz_hq_set_c_17<br />
- alexnardini::Data/f3h_archviz_hq_set_c_18<br />
- alexnardini::Data/f3h_archviz_hq_set_c_19<br />
- alexnardini::Data/f3h_archviz_hq_set_c_20<br />
- alexnardini::Data/f3h_archviz_hq_set_c_21<br />
- alexnardini::Data/f3h_archviz_hq_set_c_22<br />
- alexnardini::Data/f3h_a_women_in_pink_and_cyan_hairs<br />
- alexnardini::Data/f3h_shiny_cyborg_enjoying_the_moment<br />
- alexnardini::Data/f3h_under_the_northern_lights<br />
- alexnardini::Data/f3h_teckno_kid_facing_the_green_gem<br />
- alexnardini::Data/f3h_mazinga_zeta_fashion_style<br />
- alexnardini::Data/f3h_cow_in_a_grass_field_enjoying_the_day<br />
- alexnardini::Data/f3h_gems_and_burgers_for_the_queen<br />
- alexnardini::Data/f3h_hot_spas_with_salty_walls<br />
- alexnardini::Data/f3h_picasso_women_looking_at_you<br />
- alexnardini::Data/f3h_waxed_cyborg_thoughts<br />
- alexnardini::Data/f3h_portrait_like_the_old_one<br />
- alexnardini::Data/f3h_samurai_in_a_pose<br />
- alexnardini::Data/f3h_at_the_barber_shop<br />
- alexnardini::Data/f3h_metro_in_iceland_on_a_clear_day<br />
- alexnardini::Data/f3h_river_cactusses_on_sunset<br />
- alexnardini::Data/f3h_midnight_fever_in_hongkong<br />
- alexnardini::Data/f3h_dusty_helmet_on_explorer_sunset<br />
- alexnardini::Data/f3h_tree_of_life_and_lonely<br />
- alexnardini::Data/f3h_little_canadian_house_in_the_wood<br />
- alexnardini::Data/f3h_dark_punk_clown_trying_to_smile<br />
- alexnardini::Data/f3h_the_path_to_pandora_is_beautiful<br />
- alexnardini::Data/f3h_warrior_and_his_armour<br />
- alexnardini::Data/f3h_the_hobbyt_house_on_a_cloudy_day<br />
- alexnardini::Data/f3h_scifi_in_the_50s_was_great<br />
- alexnardini::Data/f3h_fancy_women_at_a_pub_in_violet<br />
- alexnardini::Data/f3h_pink_hairy_punk_girls<br />
- alexnardini::Data/f3h_walkmen_girls_in_japan<br />
- alexnardini::Data/f3h_ulysse_in_a_dramatic_moment<br />
- alexnardini::Data/f3h_dark_girl_with_metal_hairs<br />
- alexnardini::Data/f3h_butterfly_wings_on_dress<br />
- alexnardini::Data/f3h_monster_attach_with_energy<br />
- alexnardini::Data/f3h_painted_env_on_a_rainy_day<br />
- alexnardini::Data/f3h_castle_so_high_it_reach_the_sky<br />
- alexnardini::Data/f3h_little_devil_fox<br />
- alexnardini::Data/f3h_sport_car_at_nigh_in_the_rain<br />
- alexnardini::Data/f3h_magical_sky_lights<br />
- alexnardini::Data/f3h_prince_of_arabia<br />
- alexnardini::Data/f3h_soulless_dark_punk<br />
- alexnardini::Data/f3h_girl_with_big_red_petals<br />
- alexnardini::Data/f3h_serene_water_in_venice<br />
- alexnardini::Data/f3h_alice_in_wonderland<br />
- alexnardini::Data/f3h_flying_from_the_deepest_ocean<br />
- alexnardini::Data/f3h_walking_on_an_alien_planet<br />
- alexnardini::Data/f3h_sunset_and_high_grass_field<br />
- alexnardini::Data/f3h_girl_smiling_with_a_pinky<br />
- alexnardini::Data/f3h_nazy_but_elegant<br />
- alexnardini::Data/f3h_planet_skies_fantasy<br />
- alexnardini::Data/f3h_the_old_elegant_man<br />
- alexnardini::Data/f3h_angels_on_fire<br />
- alexnardini::Data/f3h_fancy_wearing_glasses<br />
- alexnardini::Data/f3h_crystal_with_colors<br />
- alexnardini::Data/f3h_tsunamy_but_bigger<br />
- alexnardini::Data/f3h_starry_night_on_a_tulips_field<br />
- alexnardini::Data/f3h_lovely_cabin_in_the_wood<br />
- alexnardini::Data/f3h_gems_over_gems_over_gems<br />
- alexnardini::Data/f3h_smoky_night_in_the_city<br />
- alexnardini::Data/f3h_portal_to_ice_and_flowers<br />
- alexnardini::Data/f3h_mad_scientist_office_at_night<br />
- alexnardini::Data/f3h_pink_evrything_on_a_blue_sky<br />
- alexnardini::Data/f3h_archviz_hq_set_b_13<br />
- alexnardini::Data/f3h_golden_tree_at_the_pool<br />
- alexnardini::Data/f3h_sunset_war_for_the_kids<br />
- alexnardini::Data/f3h_rainbows_in_the_desert<br />
- alexnardini::Data/f3h_walking_on_red_moss<br />
- alexnardini::Data/f3h_mountain_under_colors_sky<br />
- alexnardini::Data/f3h_magical_trees_with_stars<br />
- alexnardini::Data/f3h_subway_neons<br />
- alexnardini::Data/f3h_green_soldier_on_cyan_smoke<br />
- alexnardini::Data/f3h_sky_timelapse_with_a_tree<br />
- alexnardini::Data/f3h_city_inside_a_violet_sky<br />
- alexnardini::Data/f3h_plexiglass_watch<br />
- alexnardini::Data/f3h_color_bushes_on_grey_env<br />
- alexnardini::Data/f3h_dinner_in_tokyo<br />
- alexnardini::Data/f3h_peach_and_yougurt_with_nuts<br />
- alexnardini::Data/f3h_the_teacher_was_listening<br />
- alexnardini::Data/f3h_the_museum_entrance_was_bright<br />
- alexnardini::Data/f3h_wet_city_in_the_eveing<br />
- alexnardini::Data/f3h_kimonos_for_the_occasions<br />
- alexnardini::Data/f3h_a_poster_for_scifi<br />
- alexnardini::Data/f3h_good_looking_piece_of_sushi<br />
- alexnardini::Data/f3h_the_monastery_was_packed<br />
- alexnardini::Data/f3h_waling_peacefully_and_serene<br />
- alexnardini::Data/f3h_davinci_marble_block<br />
- alexnardini::Data/f3h_turquoise_sky_and_red_trees<br />
- alexnardini::Data/f3h_indian_woman_thinking<br />
- alexnardini::Data/f3h_a_chrystal_mountain<br />
- alexnardini::Data/f3h_aline_wandering_at_the_market<br />
- alexnardini::Data/f3h_hidden_world<br />
- alexnardini::Data/f3h_this_watch_is_misty<br />
- alexnardini::Data/f3h_precious_stone<br />
- alexnardini::Data/f3h_lake_under_shiny_stars<br />
- alexnardini::Data/f3h_waxed_skeleton<br />
- alexnardini::Data/f3h_monster_and_candle_lights<br />
- alexnardini::Data/f3h_interior_and_lemons<br />
- alexnardini::Data/f3h_alone_inside_fantasy_worlds<br />
- alexnardini::Data/f3h_the_doll_house<br />
- alexnardini::Data/f3h_dutch_living_room<br />
- alexnardini::Data/f3h_portrait_of_a_serene_woman<br />
- alexnardini::Data/f3h_pinups_and_comic_books<br />
- alexnardini::Data/f3h_barbie_house<br />
- alexnardini::Data/f3h_synthetic_pets_portraits<br />
- alexnardini::Data/f3h_colibries_and_oranges<br />
- alexnardini::Data/f3h_little_and_yellow_kid<br />
- alexnardini::Data/f3h_queen_and_prince_on_a_sofa<br />
- alexnardini::Data/f3h_moulin_rouge_star<br />
- alexnardini::Data/f3h_final_fantasy_girl<br />
- alexnardini::Data/f3h_smiling_pumpkin<br />
- alexnardini::Data/f3h_deepspace_ship_over_planet<br />
- alexnardini::Data/f3h_oil_painting_about_nature<br />
- alexnardini::Data/f3h_watercolors_on_paper<br />
- alexnardini::Data/f3h_butterfly_in_pencils<br />
- alexnardini::Data/f3h_at_the_pool<br />
- alexnardini::Data/f3h_eiffel_on_a_rainy_night<br />
- alexnardini::Data/f3h_natural_with_flowers<br />
- alexnardini::Data/f3h_morning_breakfast_at_home<br />
- alexnardini::Data/f3h_sensorial_swim<br />
- alexnardini::Data/f3h_cold_bikini_bath<br />
- alexnardini::Data/f3h_stanley_park_jogging_on_a_sunny_day<br />
- alexnardini::Data/f3h_pinky_wall_and_a_turquoise_kimono<br />
- alexnardini::Data/f3h_elegant_old_and_beautiful<br />
- alexnardini::Data/f3h_young_and_astute<br />
- alexnardini::Data/f3h_diligent_in_the_city_streets<br />
- alexnardini::Data/f3h_without_compromises<br />
- alexnardini::Data/f3h_casual_shopping<br />
- alexnardini::Data/f3h_heros_by_accident<br />
- alexnardini::Data/f3h_yeah_that_midnight_date<br />
- alexnardini::Data/f3h_swimming_in_a_japanese_pool<br />
- alexnardini::Data/f3h_playboy_bunny<br />
- alexnardini::Data/f3h_tan_in_a_yellow_bikini<br />
- alexnardini::Data/f3h_flintstones_mama<br />
- alexnardini::Data/f3h_train_waiting_on_a_red_dress<br />
- alexnardini::Data/f3h_music_listening_in_malibu<br />
- alexnardini::Data/f3h_sofa_chair_thinking_of_you<br />
- alexnardini::Data/f3h_multiframe_shq_01<br />
- alexnardini::Data/f3h_multiframe_shq_02<br />
- alexnardini::Data/f3h_multiframe_shq_04<br />
- alexnardini::Data/f3h_multiframe_shq_05<br />
- alexnardini::Data/f3h_archviz_hq_set_a_01<br />
- alexnardini::Data/f3h_multiframe_shq_03<br />
- alexnardini::Data/f3h_multiframe_shq_06<br />
- alexnardini::Data/f3h_multiframe_shq_07<br />
- alexnardini::Data/f3h_multiframe_shq_08<br />
- alexnardini::Data/f3h_multiframe_shq_09<br />
- alexnardini::Data/f3h_multiframe_shq_10<br />
- alexnardini::Data/f3h_multiframe_shq_11<br />
- alexnardini::Data/f3h_multiframe_shq_12<br />
- alexnardini::Data/f3h_multiframe_shq_13<br />
- alexnardini::Data/f3h_multiframe_shq_14<br />
- alexnardini::Data/f3h_multiframe_shq_15<br />
- alexnardini::Data/f3h_multiframe_shq_16<br />
- alexnardini::Data/f3h_multiframe_shq_17<br />
- alexnardini::Data/f3h_multiframe_shq_18<br />
- alexnardini::Data/f3h_multiframe_shq_19<br />
- alexnardini::Data/f3h_multiframe_shq_20<br />
- alexnardini::Data/f3h_ninja_cat_with_furry_cloths<br />
- alexnardini::Data/f3h_50s_x_man_origin_wolverin<br />

</details>

<br />

<details>
<summary>
<img src="../../icons/iconSVGR.svg" width="64" height="40" style="vertical-align: middle;">
<h1 style="display: inline;">APOPHYSIS Palette libs</h1>
</summary>

</br>

- alexnardini::Data/apo_at_corner<br />
- alexnardini::Data/apo_beam<br />
- alexnardini::Data/apo_blood_in_bathroom<br />
- alexnardini::Data/apo_bright_but_also_dark<br />
- alexnardini::Data/apo_chocolate<br />
- alexnardini::Data/apo_cold_again<br />
- alexnardini::Data/apo_desudesu_err<br />
- alexnardini::Data/apo_fresh<br />
- alexnardini::Data/apo_hey_lets_go<br />
- alexnardini::Data/apo_hipster_cat<br />
- alexnardini::Data/apo_i_see_it_tehe<br />
- alexnardini::Data/apo_i_sit_and_wait<br />
- alexnardini::Data/apo_just_cycling<br />
- alexnardini::Data/apo_kaamos<br />
- alexnardini::Data/apo_kawaii_cafe<br />
- alexnardini::Data/apo_lisardz<br />
- alexnardini::Data/apo_looking_at_me<br />
- alexnardini::Data/apo_melons<br />
- alexnardini::Data/apo_nice_feet_you_got<br />
- alexnardini::Data/apo_obsidian<br />
- alexnardini::Data/apo_somewhat_blurry<br />
- alexnardini::Data/apo_sun_and_sea<br />
- alexnardini::Data/apo_take_them_off<br />
- alexnardini::Data/apo_teatable<br />
- alexnardini::Data/apo_that_chinese_you_mentioned<br />
- alexnardini::Data/apo_tiger<br />
- alexnardini::Data/apo_underwear<br />
- alexnardini::Data/apo_werewolves_toilet<br />
- alexnardini::Data/apo_yeo_thats_the_trick<br />
- alexnardini::Data/apo_after_hard_day<br />
- alexnardini::Data/apo_alone_floating_stone<br />
- alexnardini::Data/apo_another_day<br />
- alexnardini::Data/apo_capes<br />
- alexnardini::Data/apo_custom_skies<br />
- alexnardini::Data/apo_death<br />
- alexnardini::Data/apo_diamond<br />
- alexnardini::Data/apo_dirt<br />
- alexnardini::Data/apo_dirties<br />
- alexnardini::Data/apo_dyes<br />
- alexnardini::Data/apo_emerald<br />
- alexnardini::Data/apo_eyes_in_dark<br />
- alexnardini::Data/apo_flower_forest<br />
- alexnardini::Data/apo_flowers<br />
- alexnardini::Data/apo_found_apples<br />
- alexnardini::Data/apo_hero<br />
- alexnardini::Data/apo_juice<br />
- alexnardini::Data/apo_jungle<br />
- alexnardini::Data/apo_light_forest<br />
- alexnardini::Data/apo_melons_and_carrots<br />
- alexnardini::Data/apo_mesa<br />
- alexnardini::Data/apo_mossy_cobble<br />
- alexnardini::Data/apo_nether<br />
- alexnardini::Data/apo_rich_over_vein<br />
- alexnardini::Data/apo_smooth_stone<br />
- alexnardini::Data/apo_spider<br />
- alexnardini::Data/apo_tall_grass<br />
- alexnardini::Data/apo_torch<br />
- alexnardini::Data/apo_unknown_sun<br />
- alexnardini::Data/apo_village<br />
- alexnardini::Data/apo_water_sheep_meat<br />
- alexnardini::Data/apo_witch<br />
- alexnardini::Data/apo_a_really_pleasing_red_thing<br />
- alexnardini::Data/apo_a_warm_dark_place<br />
- alexnardini::Data/apo_almost_all_sea_green<br />
- alexnardini::Data/apo_almost_too_classic<br />
- alexnardini::Data/apo_amber<br />
- alexnardini::Data/apo_amigo<br />
- alexnardini::Data/apo_anime<br />
- alexnardini::Data/apo_arthropod_colors<br />
- alexnardini::Data/apo_backlit<br />
- alexnardini::Data/apo_barton<br />
- alexnardini::Data/apo_barton_contrast<br />
- alexnardini::Data/apo_beautiful_overexposure<br />
- alexnardini::Data/apo_beige_and_grey<br />
- alexnardini::Data/apo_bioluminescence<br />
- alexnardini::Data/apo_blue_green_orange<br />
- alexnardini::Data/apo_blue_orange_and_creamy<br />
- alexnardini::Data/apo_blue_white_pink<br />
- alexnardini::Data/apo_blue_and_dark_salmon<br />
- alexnardini::Data/apo_blue_and_dust<br />
- alexnardini::Data/apo_blue_and_green<br />
- alexnardini::Data/apo_blue_and_red<br />
- alexnardini::Data/apo_cadet_and_cream<br />
- alexnardini::Data/apo_cadet_and_olive<br />
- alexnardini::Data/apo_cadet_and_orange<br />
- alexnardini::Data/apo_cadet_and_red<br />
- alexnardini::Data/apo_cave_crystals<br />
- alexnardini::Data/apo_cave_flashlights<br />
- alexnardini::Data/apo_city<br />
- alexnardini::Data/apo_city_at_night<br />
- alexnardini::Data/apo_clouds_and_icecream<br />
- alexnardini::Data/apo_cyan_sienna_black<br />
- alexnardini::Data/apo_cyan_goes_with_everything<br />
- alexnardini::Data/apo_dark_blue_with_gold_and_orange<br />
- alexnardini::Data/apo_desaturated_midtones<br />
- alexnardini::Data/apo_desaturated_with_red<br />
- alexnardini::Data/apo_disney_polaroid<br />
- alexnardini::Data/apo_dusty_rose_and_lavander<br />
- alexnardini::Data/apo_florence<br />
- alexnardini::Data/apo_fuchsia_and_gold<br />
- alexnardini::Data/apo_fuck_yeah_rainbows<br />
- alexnardini::Data/apo_gold_and_cyan<br />
- alexnardini::Data/apo_grey_salmon_cyan<br />
- alexnardini::Data/apo_grey_and_red_forever<br />
- alexnardini::Data/apo_grey_with_orange<br />
- alexnardini::Data/apo_grey_with_shocks<br />
- alexnardini::Data/apo_greyed_rainbow<br />
- alexnardini::Data/apo_greygreen_with_pink<br />
- alexnardini::Data/apo_hardcore<br />
- alexnardini::Data/apo_high_contrast_banana<br />
- alexnardini::Data/apo_high_contrast_fern<br />
- alexnardini::Data/apo_i_hardly_ever_use_green<br />
- alexnardini::Data/apo_ice_and_orange<br />
- alexnardini::Data/apo_impressionism<br />
- alexnardini::Data/apo_just_after_dawn_in_winter<br />
- alexnardini::Data/apo_lavander_gold_cyan<br />
- alexnardini::Data/apo_like_a_bomb_pop<br />
- alexnardini::Data/apo_lime_cyan_orange<br />
- alexnardini::Data/apo_lut_gholein<br />
- alexnardini::Data/apo_mauve_and_cyan<br />
- alexnardini::Data/apo_mint_orange_blue<br />
- alexnardini::Data/apo_modern_orange<br />
- alexnardini::Data/apo_monochrome_is_unimaginative<br />
- alexnardini::Data/apo_mood_swings<br />
- alexnardini::Data/apo_mostly_grey<br />
- alexnardini::Data/apo_movie_posters<br />
- alexnardini::Data/apo_muted_but_wide_hued<br />
- alexnardini::Data/apo_neonest_of_the_rainbows<br />
- alexnardini::Data/apo_never_as_good<br />
- alexnardini::Data/apo_nom_those_rainbows<br />
- alexnardini::Data/apo_oil_painting<br />
- alexnardini::Data/apo_oil_painting_at_night<br />
- alexnardini::Data/apo_olive_and_sky<br />
- alexnardini::Data/apo_opening_the_drapes<br />
- alexnardini::Data/apo_orange_lime_aqua<br />
- alexnardini::Data/apo_orange_and_dark_cyan<br />
- alexnardini::Data/apo_orange_and_ff00ff<br />
- alexnardini::Data/apo_orange_like_a_sunset<br />
- alexnardini::Data/apo_paradiso<br />
- alexnardini::Data/apo_pink_cyan_grey<br />
- alexnardini::Data/apo_pink_cyan_white<br />
- alexnardini::Data/apo_pink_royal_purple_cyan<br />
- alexnardini::Data/apo_pink_yellow_white<br />
- alexnardini::Data/apo_pink_and_blue<br />
- alexnardini::Data/apo_pink_and_green<br />
- alexnardini::Data/apo_pretty_damn_yellow<br />
- alexnardini::Data/apo_purple_cyan_beige<br />
- alexnardini::Data/apo_purple_and_red<br />
- alexnardini::Data/apo_purple_and_yellow<br />
- alexnardini::Data/apo_purple_with_mint_stripes<br />
- alexnardini::Data/apo_rainbow_and_black<br />
- alexnardini::Data/apo_red_beige_black<br />
- alexnardini::Data/apo_red_black_and_cyan<br />
- alexnardini::Data/apo_red_blue_black<br />
- alexnardini::Data/apo_red_blue_yellow<br />
- alexnardini::Data/apo_red_grey_beige<br />
- alexnardini::Data/apo_red_and_cadet<br />
- alexnardini::Data/apo_red_and_pale_green<br />
- alexnardini::Data/apo_sand_sea_bonfire<br />
- alexnardini::Data/apo_scuba_lights<br />
- alexnardini::Data/apo_shades_of_pink<br />
- alexnardini::Data/apo_shanty_metropolis<br />
- alexnardini::Data/apo_silhouette<br />
- alexnardini::Data/apo_soap_bubbles_fuck_yeah<br />
- alexnardini::Data/apo_sparsely_flowered_meadown<br />
- alexnardini::Data/apo_strawberries<br />
- alexnardini::Data/apo_strawberries_at_night<br />
- alexnardini::Data/apo_subtlety<br />
- alexnardini::Data/apo_sunlight_and_motes<br />
- alexnardini::Data/apo_sunlight_and_teacups<br />
- alexnardini::Data/apo_sunlight_by_the_lake<br />
- alexnardini::Data/apo_super_blue<br />
- alexnardini::Data/apo_super_motherfucking_blue<br />
- alexnardini::Data/apo_theme_and_variation<br />
- alexnardini::Data/apo_they_were_here_first<br />
- alexnardini::Data/apo_too_many_colors<br />
- alexnardini::Data/apo_universalism<br />
- alexnardini::Data/apo_variations_on_grey<br />
- alexnardini::Data/apo_very_desaturated<br />
- alexnardini::Data/apo_warm_flame<br />
- alexnardini::Data/apo_white_and_burgundy<br />
- alexnardini::Data/apo_white_blue_mauvish<br />
- alexnardini::Data/apo_why_so_desaturated<br />
- alexnardini::Data/apo_agnus_dei<br />
- alexnardini::Data/apo_beige_with_colors<br />
- alexnardini::Data/apo_black_yellow_teal_maroon<br />
- alexnardini::Data/apo_black_and_cyan<br />
- alexnardini::Data/apo_blue_green_red<br />
- alexnardini::Data/apo_brown_cyan_green<br />
- alexnardini::Data/apo_brown_cyan_purple_coral<br />
- alexnardini::Data/apo_brown_with_brights<br />
- alexnardini::Data/apo_burgundy_and_flame<br />
- alexnardini::Data/apo_burgundy_and_sea_green<br />
- alexnardini::Data/apo_chromatic_aberration<br />
- alexnardini::Data/apo_coral_and_moss<br />
- alexnardini::Data/apo_cyan_and_orange<br />
- alexnardini::Data/apo_cyan_and_pink<br />
- alexnardini::Data/apo_cyan_and_plum<br />
- alexnardini::Data/apo_cyan_and_warms<br />
- alexnardini::Data/apo_cyanoburgundygrey<br />
- alexnardini::Data/apo_dark_pink_cyan_purple<br />
- alexnardini::Data/apo_dark_red_and_cyan<br />
- alexnardini::Data/apo_dawn<br />
- alexnardini::Data/apo_desaturated_green_and_purple<br />
- alexnardini::Data/apo_encore<br />
- alexnardini::Data/apo_evening_reflection<br />
- alexnardini::Data/apo_garish<br />
- alexnardini::Data/apo_gold_and_turquoise<br />
- alexnardini::Data/apo_green_grey_pink<br />
- alexnardini::Data/apo_green_and_pink<br />
- alexnardini::Data/apo_grey_and_red<br />
- alexnardini::Data/apo_high_contrast<br />
- alexnardini::Data/apo_i_hate_spring<br />
- alexnardini::Data/apo_kites<br />
- alexnardini::Data/apo_lime_pink_orange<br />
- alexnardini::Data/apo_melon_modern<br />
- alexnardini::Data/apo_midnight_reflection<br />
- alexnardini::Data/apo_morning_reflection<br />
- alexnardini::Data/apo_mostly_blush<br />
- alexnardini::Data/apo_mostly_orange<br />
- alexnardini::Data/apo_mostrly_pink<br />
- alexnardini::Data/apo_multihue<br />
- alexnardini::Data/apo_multihue_balanced<br />
- alexnardini::Data/apo_multihue_cool_pastel<br />
- alexnardini::Data/apo_multihue_pastel<br />
- alexnardini::Data/apo_multihue_photo<br />
- alexnardini::Data/apo_multihue_plus_grey<br />
- alexnardini::Data/apo_multihue_saturated<br />
- alexnardini::Data/apo_neon_beige_night<br />
- alexnardini::Data/apo_neovictorian<br />
- alexnardini::Data/apo_neutral_cyan_red<br />
- alexnardini::Data/apo_noon_reflection<br />
- alexnardini::Data/apo_orange_and_sea_green<br />
- alexnardini::Data/apo_periwinkle_burgundy_yellow<br />
- alexnardini::Data/apo_pink_and_cyan<br />
- alexnardini::Data/apo_pink_and_purple<br />
- alexnardini::Data/apo_polaroid<br />
- alexnardini::Data/apo_purple_and_gold<br />
- alexnardini::Data/apo_red_and_cyan<br />
- alexnardini::Data/apo_red_and_cyan_2<br />
- alexnardini::Data/apo_red_and_neutrals<br />
- alexnardini::Data/apo_red_and_royal_purple<br />
- alexnardini::Data/apo_scene_kids_discover_instagram<br />
- alexnardini::Data/apo_tasteful_decor<br />
- alexnardini::Data/apo_thunderstorm_meadow<br />
- alexnardini::Data/apo_trifecta<br />
- alexnardini::Data/apo_violet_and_lights<br />
- alexnardini::Data/apo_watermelon<br />
- alexnardini::Data/apo_white_cyan_red<br />
- alexnardini::Data/apo_yellow_pink_cyan<br />
- alexnardini::Data/apo_yellow_pink_cyan_royal_purple<br />
- alexnardini::Data/apo_tatasz_pack_01_01<br />
- alexnardini::Data/apo_tatasz_pack_01_02<br />
- alexnardini::Data/apo_tatasz_pack_01_03<br />
- alexnardini::Data/apo_tatasz_pack_01_04<br />
- alexnardini::Data/apo_tatasz_pack_01_05<br />
- alexnardini::Data/apo_tatasz_pack_01_06<br />
- alexnardini::Data/apo_tatasz_pack_01_07<br />
- alexnardini::Data/apo_tatasz_pack_01_08<br />
- alexnardini::Data/apo_tatasz_pack_01_09<br />
- alexnardini::Data/apo_tatasz_pack_01_10<br />
- alexnardini::Data/apo_tatasz_pack_01_11<br />
- alexnardini::Data/apo_tatasz_pack_01_12<br />
- alexnardini::Data/apo_tatasz_pack_01_13<br />
- alexnardini::Data/apo_tatasz_pack_01_14<br />
- alexnardini::Data/apo_tatasz_pack_01_15<br />
- alexnardini::Data/apo_tatasz_pack_01_16<br />
- alexnardini::Data/apo_tatasz_pack_01_17<br />
- alexnardini::Data/apo_tatasz_pack_01_18<br />
- alexnardini::Data/apo_tatasz_pack_01_19<br />
- alexnardini::Data/apo_tatasz_pack_01_20<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_01<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_10<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_13<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_17<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_19<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_02<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_21<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_23<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_26<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_27<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_29<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_30<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_34<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_35<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_38<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_39<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_40<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_41<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_42<br />
- alexnardini::Data/apo_tatasz_pack_02_colder_48<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_11<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_14<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_15<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_31<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_37<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_45<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_47<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_49<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_05<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_06<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_08<br />
- alexnardini::Data/apo_tatasz_pack_02_dark_09<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_16<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_18<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_20<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_22<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_24<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_25<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_28<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_03<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_32<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_33<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_36<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_04<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_43<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_44<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_46<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_50<br />
- alexnardini::Data/apo_tatasz_pack_02_warmer_07<br />
- alexnardini::Data/apo_tatasz_pack_03_01<br />
- alexnardini::Data/apo_tatasz_pack_03_10<br />
- alexnardini::Data/apo_tatasz_pack_03_11<br />
- alexnardini::Data/apo_tatasz_pack_03_12<br />
- alexnardini::Data/apo_tatasz_pack_03_13<br />
- alexnardini::Data/apo_tatasz_pack_03_14<br />
- alexnardini::Data/apo_tatasz_pack_03_15<br />
- alexnardini::Data/apo_tatasz_pack_03_16<br />
- alexnardini::Data/apo_tatasz_pack_03_17<br />
- alexnardini::Data/apo_tatasz_pack_03_18<br />
- alexnardini::Data/apo_tatasz_pack_03_19<br />
- alexnardini::Data/apo_tatasz_pack_03_2<br />
- alexnardini::Data/apo_tatasz_pack_03_20<br />
- alexnardini::Data/apo_tatasz_pack_03_03<br />
- alexnardini::Data/apo_tatasz_pack_03_04<br />
- alexnardini::Data/apo_tatasz_pack_03_05<br />
- alexnardini::Data/apo_tatasz_pack_03_06<br />
- alexnardini::Data/apo_tatasz_pack_03_07<br />
- alexnardini::Data/apo_tatasz_pack_03_08<br />
- alexnardini::Data/apo_tatasz_pack_03_09<br />
- alexnardini::Data/apo_tatasz_pack_04_01<br />
- alexnardini::Data/apo_tatasz_pack_04_02<br />
- alexnardini::Data/apo_tatasz_pack_04_03<br />
- alexnardini::Data/apo_tatasz_pack_04_04<br />
- alexnardini::Data/apo_tatasz_pack_04_05<br />
- alexnardini::Data/apo_tatasz_pack_04_06<br />
- alexnardini::Data/apo_tatasz_pack_04_07<br />
- alexnardini::Data/apo_tatasz_pack_04_08<br />
- alexnardini::Data/apo_tatasz_pack_04_09<br />
- alexnardini::Data/apo_tatasz_pack_04_10<br />
- alexnardini::Data/apo_tatasz_pack_04_11<br />
- alexnardini::Data/apo_tatasz_pack_04_12<br />
- alexnardini::Data/apo_tatasz_pack_04_13<br />
- alexnardini::Data/apo_tatasz_pack_04_14<br />
- alexnardini::Data/apo_tatasz_pack_04_15<br />
- alexnardini::Data/apo_tatasz_pack_04_16<br />
- alexnardini::Data/apo_tatasz_pack_04_17<br />
- alexnardini::Data/apo_tatasz_pack_04_18<br />
- alexnardini::Data/apo_tatasz_pack_04_19<br />
- alexnardini::Data/apo_tatasz_pack_04_20<br />
- alexnardini::Data/apo_tatasz_pack_04_21<br />
- alexnardini::Data/apo_tatasz_pack_04_22<br />
- alexnardini::Data/apo_tatasz_pack_04_23<br />
- alexnardini::Data/apo_tatasz_pack_04_24<br />
- alexnardini::Data/apo_tatasz_pack_04_25<br />
- alexnardini::Data/apo_tatasz_pack_04_26<br />
- alexnardini::Data/apo_tatasz_pack_04_27<br />
- alexnardini::Data/apo_tatasz_pack_04_39<br />
- alexnardini::Data/apo_tatasz_pack_04_40<br />
- alexnardini::Data/apo_tatasz_pack_04_41<br />
- alexnardini::Data/apo_tatasz_pack_04_42<br />
- alexnardini::Data/apo_tatasz_pack_04_43<br />
- alexnardini::Data/apo_tatasz_pack_04_44<br />
- alexnardini::Data/apo_tatasz_pack_04_28<br />
- alexnardini::Data/apo_tatasz_pack_04_29<br />
- alexnardini::Data/apo_tatasz_pack_04_30<br />
- alexnardini::Data/apo_tatasz_pack_04_31<br />
- alexnardini::Data/apo_tatasz_pack_04_32<br />
- alexnardini::Data/apo_tatasz_pack_04_33<br />
- alexnardini::Data/apo_tatasz_pack_04_34<br />
- alexnardini::Data/apo_tatasz_pack_04_35<br />
- alexnardini::Data/apo_tatasz_pack_04_36<br />
- alexnardini::Data/apo_tatasz_pack_04_37<br />
- alexnardini::Data/apo_tatasz_pack_04_38<br />
- alexnardini::Data/apo_tatasz_pack_04_45<br />
- alexnardini::Data/apo_tatasz_pack_04_46<br />
- alexnardini::Data/apo_tatasz_pack_04_47<br />
- alexnardini::Data/apo_tatasz_pack_04_48<br />
- alexnardini::Data/apo_tatasz_pack_04_49<br />
- alexnardini::Data/apo_tatasz_pack_04_50<br />
- alexnardini::Data/apo_tatasz_pack_04_51<br />
- alexnardini::Data/apo_tatasz_pack_04_52<br />
- alexnardini::Data/apo_tatasz_pack_04_53<br />
- alexnardini::Data/apo_tatasz_pack_04_54<br />
- alexnardini::Data/apo_tatasz_pack_04_55<br />
- alexnardini::Data/apo_tatasz_pack_04_56<br />
- alexnardini::Data/apo_tatasz_pack_04_57<br />
- alexnardini::Data/apo_tatasz_pack_04_58<br />
- alexnardini::Data/apo_tatasz_pack_04_59<br />
- alexnardini::Data/apo_tatasz_pack_04_60<br />
- alexnardini::Data/apo_tatasz_pack_04_61<br />
- alexnardini::Data/apo_tatasz_pack_04_62<br />
- alexnardini::Data/apo_tatasz_pack_04_63<br />
- alexnardini::Data/apo_tatasz_pack_04_64<br />
- alexnardini::Data/apo_tatasz_pack_04_65<br />
- alexnardini::Data/apo_tatasz_pack_04_66<br />
- alexnardini::Data/apo_tatasz_pack_04_67<br />
- alexnardini::Data/apo_tatasz_pack_04_68<br />
- alexnardini::Data/apo_tatasz_pack_04_69<br />
- alexnardini::Data/apo_tatasz_pack_04_70<br />
- alexnardini::Data/apo_tatasz_pack_04_71<br />
- alexnardini::Data/apo_tatasz_pack_04_72<br />
- alexnardini::Data/apo_tatasz_pack_04_73<br />
- alexnardini::Data/apo_tatasz_pack_04_74<br />
- alexnardini::Data/apo_tatasz_pack_04_75<br />
- alexnardini::Data/apo_tatasz_pack_04_76<br />
- alexnardini::Data/apo_tatasz_pack_04_77<br />
- alexnardini::Data/apo_tatasz_pack_04_79<br />
- alexnardini::Data/apo_tatasz_pack_04_80<br />
- alexnardini::Data/apo_tatasz_pack_04_81<br />
- alexnardini::Data/apo_tatasz_pack_04_82<br />
- alexnardini::Data/apo_tatasz_pack_04_83<br />
- alexnardini::Data/apo_tatasz_pack_04_84<br />
- alexnardini::Data/apo_tatasz_pack_04_85<br />
- alexnardini::Data/apo_tatasz_pack_04_86<br />
- alexnardini::Data/apo_tatasz_pack_04_87<br />
- alexnardini::Data/apo_tatasz_pack_04_88<br />
- alexnardini::Data/apo_tatasz_pack_04_89<br />
- alexnardini::Data/apo_tatasz_pack_04_90<br />
- alexnardini::Data/apo_tatasz_pack_04_91<br />
- alexnardini::Data/apo_tatasz_pack_04_92<br />
- alexnardini::Data/apo_tatasz_pack_04_93<br />
- alexnardini::Data/apo_tatasz_pack_04_94<br />
- alexnardini::Data/apo_tatasz_pack_04_95<br />
- alexnardini::Data/apo_tatasz_pack_04_96<br />
- alexnardini::Data/apo_tatasz_pack_04_97<br />
- alexnardini::Data/apo_tatasz_pack_04_98<br />
- alexnardini::Data/apo_tatasz_pack_04_99<br />
- alexnardini::Data/apo_garden_b<br />
- alexnardini::Data/apo_garden_a<br />
- alexnardini::Data/apo_primaries_bt<br />
- alexnardini::Data/apo_primaries_c<br />
- alexnardini::Data/apo_blue_and_orange_a<br />
- alexnardini::Data/apo_blue_and_orange_b<br />
- alexnardini::Data/apo_motherfucking_rainbow<br />

</details>


<br/>
<br/>
<br/>
<br/>

_Copyright (c) 2021 F stands for liFe_<br/>
