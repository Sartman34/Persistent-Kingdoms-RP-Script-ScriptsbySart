#!/usr/bin/env python
# -*- coding: utf-8 -*-

from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from header_items import *
from module_constants import *
import header_debug as dbg
import header_lazy_evaluation as lazy

####################################################################################################################
#   Each mission-template is a tuple that contains the following fields:
#  1) Mission-template id (string): used for referencing mission-templates in other files.
#     The prefix mt_ is automatically added before each mission-template id.
#  2) Mission-template flags (int): See header_mission-templates.py for a list of available flags.
#  3) Mission-type (int): Which mission types this mission template matches.
#     For mission-types to be used with the default party-meeting system,
#     this should be 'charge' or 'charge_with_ally' otherwise must be -1.
#  4) Mission description text (string).
#
#  5) List of spawn records (list): Each spawn record is a tuple that contains the following fields:
#    5.1) Entry point number: Troops spawned from this spawn record will use this entry.
#    5.2) Spawn flags.
#    5.3) Alter flags: which equipment will be overriden.
#    5.4) AI flags.
#    5.5) Number of troops to spawn.
#    5.6) List of equipment to add to troops spawned from here (maximum 8).
#
#  6) List of triggers (list): Each trigger contains the following fields:
#    6.1) Check interval: How frequently this trigger will be checked. Also used for special triggers listed in header_triggers.py.
#    6.2) Delay interval: Time to wait before applying the consequences of the trigger after its conditions have been evaluated as true.
#    6.3) Re-arm interval. How much time must pass after applying the consequences of the trigger for the trigger to become active again.
#    You can put the constant ti_once here to make sure that the trigger never becomes active again after it fires once.
#    6.4) Conditions block (list), must be a valid operation block. Every time the trigger is checked, this block will be executed.
#    If the conditions block returns true or is empty, the consequences block will be executed.
#    6.5) Consequences block (list), must be a valid operation block. Executed only if the conditions block succeeded.
####################################################################################################################
                                                 #aif_start_alarmed
spawn_points_0_99 = [(x, mtef_visitor_source, 0, aif_start_alarmed, 1, []) for x in xrange(0, 100)]

before_mission_start_setup = (ti_before_mission_start, 0, 0, [], # set up basic mission and scene values
   [
  (display_message, "@^- Initializing scripts..."),
    (server_set_friendly_fire, 1),
    (server_set_melee_friendly_fire, 1),
    (server_set_friendly_fire_damage_self_ratio, 0),
    (server_set_friendly_fire_damage_friend_ratio, 100),
    (try_begin),
      (eq, "$g_game_type", "mt_multiplayer_dm"),
      (multiplayer_make_everyone_enemy),#necessary to hide the white name labels on the middle
    (else_try),
      (team_set_relation, team_default, team_default, -1),
      (team_set_relation, team_default, team_spawn_invulnerable, 0),
      (team_set_relation, team_spawn_invulnerable, team_default, 0),
    (try_end),

    (call_script, "script_initialize_scene_globals"),
    (call_script, "script_scene_set_day_time"),
    (call_script, "script_scene_setup_factions_castles"),
    (call_script, "script_setup_all_linked_scene_props"),
    (try_begin),
      (multiplayer_is_server),
      (call_script, "script_setup_castle_money_chests"),
    (else_try),
      (call_script, "script_load_profile_options"),
    (try_end),
    (assign, "$skybox_current", -1),
    (assign, "$g_last_lighting_update_time", -1),
    (try_begin),
      (lt, "$g_day_duration", 1),
      (assign, "$g_day_duration", hours(0.5)),
      (store_div, "$g_in_game_hour_in_seconds", "$g_day_duration", 24),
    (try_end),
    (try_begin),
      (lt, "$g_skybox_scale", 1),
      (assign, "$g_skybox_scale", skybox_scale),
    (try_end),
    ])

after_mission_start_setup = (ti_after_mission_start, 0, 0, [], [ # spawn and move certain things after most other set up is done
  (set_spawn_effector_scene_prop_kind, 0, -1),
  (set_spawn_effector_scene_prop_kind, 1, -1),
  (assign, "$g_preset_message_display_enabled", 0),
  (multiplayer_is_server),
  (assign, "$g_next_scene", -1),
  (call_script, "script_setup_ship_collision_props"),
  (call_script, "script_setup_scene_props_after_mission_start"),
  (init_position, pos1),
  (set_spawn_position, pos1), # spawn a respawn position marker scene prop for each possible player
  (server_get_max_num_players, "$g_spawn_marker_count"),
  (val_add, "$g_spawn_marker_count", 1),
  (try_for_range, ":unused", 0, "$g_spawn_marker_count"),
    (spawn_scene_prop, "spr_code_spawn_marker"),
  (try_end),
  (assign, "$g_spawned_bot_count", 0),
  (try_for_range, ":faction_id", castle_factions_begin, factions_end),
     (try_for_range, ":target_faction_id", castle_factions_begin, factions_end),
        (neq, ":faction_id", ":target_faction_id"),
        (call_script, "script_cf_faction_change_relation", ":faction_id", ":target_faction_id", 1),
     (try_end),
  (try_end),
  #Spawn SRP Skyboxes if wanted
  (try_begin),
    (eq, "$g_day_night_cycle_enabled", 1),
    (multiplayer_is_server),
    (call_script, "script_skybox_spawn_all"),
  (try_end),

  (try_for_prop_instances, ":instance_id", "spr_arena_spectator_c"),
    (prop_instance_get_position, pos0, ":instance_id"),
    (position_rotate_z, pos0, 180),
    (set_spawn_position, pos0),
    (spawn_agent, "trp_knight"),
    (assign, ":agent_id", reg0),
    (init_position, pos0),
    (prop_instance_set_position, ":instance_id", pos0),
    (agent_set_team, ":agent_id", 1),
    (store_random_in_range, ":head_item", 0, 3),
    (try_begin),
      (eq, ":head_item", 0),
      (assign, ":head_item", "itm_north_noseguard"),
    (else_try),
      (eq, ":head_item", 1),
      (assign, ":head_item", "itm_guard_helmet"),
    (else_try),
      (eq, ":head_item", 2),
      (assign, ":head_item", "itm_north_aventail"),
    (try_end),
    (store_random_in_range, ":body_item", 0, 3),
    (try_begin),
      (eq, ":body_item", 0),
      (assign, ":body_item", "itm_cwe_sergeant_armor_3"),
      (assign, ":boot_item", "itm_civil_rich_boots_b"),
    (else_try),
      (eq, ":body_item", 1),
      (assign, ":body_item", "itm_gambeson"),
      (assign, ":boot_item", "itm_leather_boots_noble"),
    (else_try),
      (eq, ":body_item", 2),
      (assign, ":body_item", "itm_cwe_archer_armor_2"),
      (assign, ":boot_item", "itm_narf_greaves2"),
    (try_end),
    (store_random_in_range, ":hand_item", 0, 3),
    (try_begin),
      (eq, ":hand_item", 0),
      (assign, ":hand_item", "itm_leather_gauntlet"),
    (else_try),
      (eq, ":hand_item", 1),
      (assign, ":hand_item", "itm_leather_gloves"),
    (else_try),
      (eq, ":hand_item", 2),
      (assign, ":hand_item", "itm_mail_gauntlets"),
    (try_end),
    (call_script, "script_change_armor", ":agent_id", ":head_item"),
    (call_script, "script_change_armor", ":agent_id", ":body_item"),
    (call_script, "script_change_armor", ":agent_id", ":boot_item"),
    (call_script, "script_change_armor", ":agent_id", ":hand_item"),
    (agent_equip_item, ":agent_id", "itm_heavy_lance"),
    (agent_equip_item, ":agent_id", "itm_war_bow1"),
    (agent_equip_item, ":agent_id", "itm_surgeon_scalpel"),
    (agent_equip_item, ":agent_id", "itm_spiked_mace"),
  (try_end),
  (init_position, pos0),
  (try_for_prop_instances, ":instance_id", "spr_barrier_8m"),
    (prop_instance_get_variation_id, ":var1", ":instance_id"),
    (eq, ":var1", 1),
    (prop_instance_set_position, ":instance_id", pos0),
  (try_end),
  
  (display_message, "@^- Connecting to script server."),

  (assign, "$g_loading_settings", 1),
  (send_message_to_url_advanced, script_ip_address + "/update_settings", "@WSE2", "script_ping_tcp_return", "script_update_settings_fail"),

] + [elem for sublist in [[
  (call_script, "script_load_chests", "spr_" + scene_prop),
] for scene_prop in storage_scene_props] for elem in sublist] + [
])

player_joined = (ti_server_player_joined, 0, 0, [], [ # server: handle connecting players
  (store_trigger_param_1, ":player_id"),
  (call_script, "script_setup_player_joined", ":player_id"),
  (call_script, "script_update_ghost_mode_rule", ":player_id"),
  (call_script, "script_apply_mute", ":player_id", "$g_mute_all_players"),

  (player_get_unique_id, reg0, ":player_id"),
  (dict_set_int, "$g_player_id_dict", "@{reg0}", ":player_id"),

  (str_store_string, s0, "@Loading..."),
  (call_script, "script_send_coloured_message", ":player_id", colors["beyaz"], 0),
  (call_script, "script_load_player", ":player_id"),
])

player_exit = (ti_on_player_exit, 0, 0, [], [ # server: save player values on exit
  (store_trigger_param_1, ":player_id"),

  (player_get_unique_id, reg0, ":player_id"),
  (dict_erase, "$g_player_id_dict", "@{reg0}"),

  (try_begin),
     (call_script, "script_cf_save_player", ":player_id"),
     (call_script, "script_cf_save_gear", ":player_id", 0),
  (try_end),

  (try_for_agents, ":agent_id"),
    (agent_is_human, ":agent_id"),
    (agent_is_non_player, ":agent_id"),
    (agent_get_group, ":group_id", ":agent_id"),
    (eq, ":group_id", ":player_id"),
    (agent_fade_out, ":agent_id"),
  (try_end),

##    (try_begin),
##      (player_get_slot, reg6, ":player_id", slot_player_equip_head),
##      (player_get_slot, reg7, ":player_id", slot_player_equip_body),
##      (player_get_slot, reg8, ":player_id", slot_player_equip_foot),
##      (player_get_slot, reg9, ":player_id", slot_player_equip_gloves),
##
##      (agent_get_item_slot, reg10, ":agent_id", 0),
##      (agent_get_item_slot, reg11, ":agent_id", 1),
##      (agent_get_item_slot, reg12, ":agent_id", 2),
##      (agent_get_item_slot, reg13, ":agent_id", 3),
##
##      (agent_get_position, pos1, ":agent_id"),
##      
##      (agent_fade_out, ":agent_id"),
##      (set_spawn_position, pos1),
##      (spawn_agent, "trp_multiplayer_profile_troop_female"),
##      (assign, ":agent_id", reg0),
##      (agent_set_team, ":agent_id", team_spawn_invulnerable),
####      (agent_set_crouch_mode, ":agent_id", 1),
##      (agent_set_animation, ":agent_id", "anim_sleeping", 0),
##      
##      (call_script, "script_change_armor", ":agent_id", reg6),
##      (call_script, "script_change_armor", ":agent_id", reg7),
##      (call_script, "script_change_armor", ":agent_id", reg8),
##      (call_script, "script_change_armor", ":agent_id", reg9),
##      (try_begin),
##        (gt, reg10, -1),
##        (agent_equip_item, ":agent_id", reg10),
##      (try_end),
##      (try_begin),
##        (gt, reg11, -1),
##        (agent_equip_item, ":agent_id", reg11),
##      (try_end),
##      (try_begin),
##        (gt, reg12, -1),
##        (agent_equip_item, ":agent_id", reg12),
##      (try_end),
##      (try_begin),
##        (gt, reg13, -1),
##        (agent_equip_item, ":agent_id", reg13),
##      (try_end),
##    (try_end),
])


agent_spawn = (ti_on_agent_spawn, 0, 0, [(multiplayer_is_server),], [ # server: set up new agents after they spawn
  (store_trigger_param_1, ":agent_id"),
  
  (call_script, "script_on_agent_spawned", ":agent_id"),

  (try_begin),
    (agent_is_player, ":agent_id"),
    (agent_get_player_id, ":player_id", ":agent_id"),
  
    (try_begin),
      (player_slot_eq, ":player_id", slot_player_spawn_state, player_spawn_state_dead),
      (try_begin),
        (player_slot_eq, ":player_id", slot_player_first_spawn_occured, 0),
        (call_script, "script_load_gear", ":player_id"),
      (else_try),
        (assign, ":is_naked", 1),
        (try_begin),
          (eq, "$g_keep_equipment", 1),
          (call_script, "script_player_set_stored_ammo_counts", ":player_id"),
          (try_for_range, ":slot_id", slot_player_equip_head, slot_player_equip_gloves + 1),
            (player_get_slot, ":item_id", ":player_id", ":slot_id"),
            (ge, ":item_id", all_items_begin),
            (assign, ":is_naked", 0),
          (try_end),
        (try_end),
        (try_begin),
          (eq, "$g_is_knock_out_enabled", 0),
          (eq, ":is_naked", 1),
          (call_script, "script_player_give_naked_clothes", ":player_id"),
        (try_end),
        (try_begin),
          (eq, "$g_is_knock_out_enabled", 1),
          (set_fixed_point_multiplier, 100),
          (player_get_slot, ":x", ":player_id", slot_player_death_coord_x),
          (player_get_slot, ":y", ":player_id", slot_player_death_coord_y),
          (player_get_slot, ":z", ":player_id", slot_player_death_coord_z),
          (this_or_next|neq, ":x", 0),
          (this_or_next|neq, ":y", 0),
          (neq, ":z", 0),
          (init_position, pos0),
          (position_set_x, pos0, ":x"),
          (position_set_y, pos0, ":y"),
          (position_set_z, pos0, ":z"),
          (agent_set_position, ":agent_id", pos0),
        (try_end),
        (agent_set_hit_points, ":agent_id", "$g_base_health", 0),
        (agent_set_slot, ":agent_id", slot_agent_food_amount, "$g_base_hunger"),
        (multiplayer_send_3_int_to_player, ":player_id", server_event_agent_set_slot, ":agent_id", slot_agent_food_amount, "$g_base_hunger"),
      (try_end),
    (try_end),
  
    (player_set_slot, ":player_id", slot_player_spawn_state, player_spawn_state_alive),
  
    (try_begin),
      (player_slot_eq, ":player_id", slot_player_first_spawn_occured, 0),
      (player_set_slot, ":player_id", slot_player_first_spawn_occured, 1),
      (call_script, "script_log_equipment", ":player_id"),
      (call_script, "script_setup_singings", ":player_id"),
    (try_end),

    (try_begin),
      (player_get_slot, ":faction_id", ":player_id", slot_player_faction_id),
      (faction_slot_eq, ":faction_id", slot_faction_is_active, 0),
      (call_script, "script_change_faction", ":player_id", "fac_commoners", change_faction_type_no_respawn),
      (call_script, "script_player_set_worse_respawn_troop", ":player_id", "trp_peasant"),
      (multiplayer_send_3_int_to_player, ":player_id", server_event_preset_message, "str_inactive_faction_change", preset_message_chat_log|preset_message_red, ":faction_id"),
    (try_end),

    (team_give_order, ":player_id", grc_everyone, mordr_follow),
    (team_give_order, ":player_id", grc_cavalry, mordr_mount), #Mount cavalry...
  (try_end),

  (call_script, "script_agent_init_relations", ":agent_id"),

  (try_begin),
    (agent_is_human, ":agent_id"),
    (agent_is_non_player, ":agent_id"),
    (agent_get_group, ":player_id", ":agent_id"),
    (player_is_active, ":player_id"),
    (player_get_agent_id, ":leader_agent_id", ":player_id"),
    (agent_is_active, ":leader_agent_id"),
    (agent_is_alive, ":leader_agent_id"),
    (agent_get_position, pos0, ":leader_agent_id"),
    (agent_set_position, ":agent_id", pos0),
    (try_for_range, ":slot_id", 0, 8),
      (val_add, ":slot_id", slot_player_army_equipment_begin),
      (player_get_slot, ":item_id", ":player_id", ":slot_id"),
      (neq, ":item_id", 0),
      (item_get_type, ":item_type", ":item_id"),
      (try_begin),
        (is_between, ":item_type", itp_type_head_armor, itp_type_hand_armor + 1),
        (call_script, "script_change_armor", ":agent_id", ":item_id"),
      (else_try),
        (agent_equip_item, ":agent_id", ":item_id"),
      (try_end),
    (try_end),
  (try_end),
])

agent_killed = (ti_on_agent_killed_or_wounded, 0, 0, [], # server and clients: handle messages, score, loot, and more after agents die
   [(store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":killer_agent_id"),

    (try_begin), # put person in other team is spectator is disabled to prevent player click through
      (agent_get_player_id, ":player_id", ":agent_id"),
      (player_is_active, ":player_id"),
      (try_begin),
        (server_get_ghost_mode, ":spectator_is_enabled"),
        (ge, ":spectator_is_enabled", 2),
        (neg | player_is_admin, ":player_id"),
        (player_set_team_no, ":player_id", 3),
      (try_end),
    (try_end),

    (call_script, "script_client_check_show_respawn_time_counter", ":agent_id"),
    (call_script, "script_death_cam", ":agent_id"),
    (call_script, "script_apply_consequences_for_agent_death", ":agent_id", ":killer_agent_id"),
    
    (multiplayer_is_server),

    (try_begin),
      (agent_is_player, ":agent_id"),
      (agent_get_player_id, ":player_id", ":agent_id"),
      (try_for_agents, ":horse_agent_id"),
        (agent_is_horse, ":horse_agent_id"),
        (agent_get_slot, ":owner_agent_id", ":horse_agent_id", slot_agent_owner_agent_id),
        (eq, ":owner_agent_id", ":agent_id"),
        (agent_set_no_dynamics, ":horse_agent_id", 0),
        (agent_set_slot, ":horse_agent_id", slot_agent_owner_agent_id, 0),
        (str_store_string, s0, "@Atın bağı çözüldü."),
        (call_script, "script_send_coloured_message", ":player_id", colors["beyaz"], 0),
      (try_end),
    (try_end),

    (try_begin),
      (agent_is_human, ":agent_id"),
      (agent_is_non_player, ":agent_id"),
      (agent_get_group, ":group_id", ":agent_id"),
      (player_is_active, ":group_id"),
      (try_for_range, ":slot", 0, 4),
        (agent_get_item_slot, ":item_id", ":agent_id", ":slot"),
        (gt, ":item_id", -1),
        (store_add, ":weapon_slot", ":slot", 1),
        (agent_unequip_item, ":agent_id", ":item_id", ":weapon_slot"),
      (try_end),
      (agent_get_horse, ":horse_agent_id", ":agent_id"),
      (agent_is_active, ":horse_agent_id"),
      (agent_is_alive, ":horse_agent_id"),
      (remove_agent, ":horse_agent_id"),
    (try_end),

    (call_script, "script_setup_agent_for_respawn", ":agent_id", ":killer_agent_id"),
    (call_script, "script_check_animal_killed", ":agent_id", ":killer_agent_id"),
##    (call_script, "script_check_spawn_bots", ":agent_id"),
    ])

agent_hit = (ti_on_agent_hit, 0, 0, [], [ # server: apply extra scripted effects for special weapons, hitting animals, and when overloaded by armor
  (store_trigger_param_1, ":attacked_agent_id"),
  (store_trigger_param_2, ":attacker_agent_id"),
  (store_trigger_param_3, ":damage_dealt"),
  (assign, ":damage_dealt_original", ":damage_dealt"),
  (try_begin), # check if damage should bleed through the armor due to unmet requirements
    (agent_slot_ge, ":attacked_agent_id", slot_agent_armor_damage_through, 5),
    (agent_get_slot, ":damage_through_multiplier", ":attacked_agent_id", slot_agent_armor_damage_through),
    (gt, reg0, -1),
    (item_get_slot, ":damage_through", reg0, slot_item_max_raw_damage),
    (val_mul, ":damage_through", ":damage_through_multiplier"),
    (val_div, ":damage_through", 100),
    (gt, ":damage_through", ":damage_dealt"),
    (store_random_in_range, ":damage_dealt", ":damage_dealt", ":damage_through"),
  (try_end),
  (try_begin),
    (is_between, reg0, scripted_items_begin, scripted_items_end),
    (call_script, "script_agent_hit_with_scripted_item", ":attacked_agent_id", ":attacker_agent_id", ":damage_dealt", reg0),
    (assign, ":damage_dealt", reg0),
  (try_end),
  (try_begin),
    (eq, reg0, "itm_baton"),
    (assign, ":damage_dealt", 0),
    (neg|agent_is_non_player, ":attacked_agent_id"),
    (agent_set_animation, ":attacked_agent_id", "anim_strike_fall_back_rise", 0),
    (agent_get_player_id, ":player_id", ":attacked_agent_id"),
    (player_get_gender, ":gender", ":player_id"),
    (try_begin),
      (gt, ":gender", 0),#woman
      (agent_play_sound, ":attacked_agent_id", "snd_woman_hit"),
    (else_try),
      (agent_play_sound, ":attacked_agent_id", "snd_man_hit"),
    (try_end),
  (try_end),
  (try_begin),
    (neg|agent_is_non_player, ":attacked_agent_id"),
    (agent_get_player_id, ":player_id", ":attacked_agent_id"),
    (call_script, "script_toggle_walk", ":player_id", 1, 0),
  (try_end),
  (try_begin),
    (eq, "$g_is_hit_disabled", 1),
    (neq, ":attacked_agent_id", ":attacker_agent_id"),
    (assign, ":fail", 0),
    (try_begin),
      (agent_is_human, ":attacker_agent_id"),
    (else_try),
      (agent_get_rider, ":attacker_agent_id", ":attacker_agent_id"),
      (agent_is_active, ":attacker_agent_id"),
    (else_try),
      (assign, ":fail", 1),
    (try_end),
    (eq, ":fail", 0),
    (agent_get_player_id, ":player_id", ":attacker_agent_id"),
    (player_is_active, ":player_id"),
    (neg^player_is_admin, ":player_id"),
    (assign, ":damage_dealt", 0),
    (store_mission_timer_a, ":time"),
    (agent_get_slot, ":last_action_time", ":attacker_agent_id", slot_agent_last_hit_time),
    (store_sub, ":interval", ":time", ":last_action_time"),
    (try_begin),
      (ge, ":interval", 10),
      (agent_set_slot, ":attacker_agent_id", slot_agent_last_hit_time, ":time"),
      (multiplayer_send_2_int_to_player, ":player_id", server_event_script_message_set_color, 4293938509),
      (multiplayer_send_string_to_player, ":player_id", server_event_script_message_announce, "@Hitler kapatildi."),
    (try_end),
  (else_try),
    (agent_get_player_id, ":attacker_player_id", ":attacker_agent_id"),
    (agent_get_player_id, ":attacked_player_id", ":attacked_agent_id"),
    (player_is_active, ":attacker_player_id"),
    (player_is_active, ":attacked_player_id"),
    (neg^player_is_admin, ":attacker_player_id"),
    (neg^player_is_admin, ":attacked_player_id"),
    (player_get_slot, ":attacker_time", ":attacker_player_id", slot_player_time),
    (player_get_slot, ":attacked_time", ":attacked_player_id", slot_player_time),
    (assign, ":fail", 1),
    (try_begin),
      (lt, ":attacker_time", "$g_authentication_time"),
      (str_store_string, s0, "@Dogrulanmadan agresif yapamazsiniz."),
      (call_script, "script_send_coloured_message", ":attacker_player_id", colors["koyu kirmizi"], 1),
      (assign, ":fail", 0),
    (else_try),
      (lt, ":attacked_time", "$g_authentication_time"),
      (str_store_string, s0, "@Dogrulanmamis oyunculara agresif yapamazsiniz."),
      (call_script, "script_send_coloured_message", ":attacker_player_id", colors["koyu kirmizi"], 1),
      (assign, ":fail", 0),
    (try_end),
    (eq, ":fail", 0),
    (assign, ":damage_dealt", 0),
  (else_try),
    (call_script, "script_log_hit", ":attacked_agent_id", ":attacker_agent_id", ":damage_dealt", reg0, 0),
  (try_end),
  (try_begin),
    (agent_slot_ge, ":attacked_agent_id", slot_agent_animal_birth_time, 1),
    (call_script, "script_animal_hit", ":attacked_agent_id", ":attacker_agent_id", ":damage_dealt_original", reg0),
    (assign, ":damage_dealt", reg0),
  (try_end),
  
  (try_begin),
##    (eq, "$g_is_knock_out_enabled", 1),
##    (neg|agent_is_non_player, ":attacked_agent_id"),
##    (agent_get_player_id, ":player_id", ":attacked_agent_id"),
##    (store_agent_hit_points, ":hit_points", ":attacked_agent_id", 1),
##    (val_sub, ":hit_points", ":damage_dealt"),
##    (le, ":hit_points", 0),
##    (agent_slot_eq, ":attacked_agent_id", slot_agent_is_downed, 0),
##    (agent_set_slot, ":attacked_agent_id", slot_agent_is_downed, 1),
##    (try_begin),
##      (agent_get_horse, ":horse_agent_id", ":attacked_agent_id"),
##      (agent_is_active, ":horse_agent_id"),
##      (agent_is_alive, ":horse_agent_id"),
##      (agent_set_horse, ":attacked_agent_id", -1),
##    (try_end),
##    (agent_get_position, pos1, ":attacked_agent_id"),
##    (set_fixed_point_multiplier, 100),
##    (try_for_range, ":equip_slot", ek_item_0, ek_item_3 + 1),
##      (agent_get_item_slot, ":item_id", ":attacked_agent_id", ":equip_slot"),
##      (ge, ":item_id", all_items_begin),
##      (store_add, ":unequip_slot", ":equip_slot", 1),
##      (agent_unequip_item, ":attacked_agent_id", ":item_id", ":unequip_slot"),
##      (call_script, "script_set_random_spawn_position", 50),
##      (spawn_item, ":item_id", 0, "$g_spawn_item_prune_time"),
##      (call_script, "script_check_on_item_dropped", ":attacked_agent_id", ":item_id", reg0, 1),
##    (try_end),
##    (agent_set_speed_modifier, ":attacked_agent_id", 0),
##    (agent_set_no_dynamics, ":attacked_agent_id", 1),
##    (agent_set_hit_points, ":attacked_agent_id", "$g_base_health", 0),
##    (agent_set_animation, ":attacked_agent_id", "anim_sleeping_final"),
##    (set_trigger_result, 0),
##  (else_try),
    (set_trigger_result, ":damage_dealt"),
  (try_end),
])

item_picked_up = (ti_on_item_picked_up, 0, 0, [], # handle agents picking up an item
   [(store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":item_id"),
    (store_trigger_param_3, ":instance_id"),
    (call_script, "script_agent_calculate_stat_modifiers_for_item", ":agent_id", ":item_id", 1, 1),
    (multiplayer_is_server),
    (call_script, "script_check_on_item_picked_up", ":agent_id", ":item_id", ":instance_id"),
    ])

item_dropped = (ti_on_item_dropped, 0, 0, [], # handle agents dropping an item
   [(store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":item_id"),
    (store_trigger_param_3, ":instance_id"),
    (call_script, "script_agent_calculate_stat_modifiers_for_item", ":agent_id", ":item_id", 0, 1),
    (multiplayer_is_server),
    (call_script, "script_check_on_item_dropped", ":agent_id", ":item_id", ":instance_id", 0),
    ])

item_wielded = (ti_on_item_wielded, 0, 0, [], # handle agents wielding an item
   [(store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":item_id"),
    (call_script, "script_agent_calculate_stat_modifiers_for_item", ":agent_id", ":item_id", 1, 1),
    (call_script, "script_check_wielding_during_position_animation", ":agent_id", ":item_id"),
    ])

item_unwielded = (ti_on_item_unwielded, 0, 0, [], # handle agents un-wielding an item
   [(store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":item_id"),
    (call_script, "script_agent_calculate_stat_modifiers_for_item", ":agent_id", ":item_id", 0, 1),
    ])

agent_mount = (ti_on_agent_mount, 0, 0, [], # server: check speed factor and attached carts when agents mount a horse
   [(store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":horse_agent_id"),
    (agent_set_slot, ":horse_agent_id", slot_agent_horse_last_rider, ":agent_id"),
    (agent_set_slot, ":agent_id", slot_agent_last_horse_ridden, ":horse_agent_id"),
    (multiplayer_is_server),
    (call_script, "script_check_agent_horse_speed_factor", ":agent_id", ":horse_agent_id", 0),
    (try_begin),
      (call_script, "script_cf_attach_cart", ":agent_id", -1, ":agent_id"),
    (try_end),

    (agent_get_player_id, ":player_id", ":agent_id"),
    (player_is_active, ":player_id"),
    (str_store_player_username, s0, ":player_id"),
    (agent_get_item_id, ":horse_item_id", ":horse_agent_id"),
    (str_store_item_name, s1, ":horse_item_id"),
    #Alter mount/dismount logs to show the agent_id of the mount
    (assign, reg31, ":horse_agent_id"),
    (server_add_message_to_log, "str_s0_has_mounted_a_s1"),
    ])

agent_dismount = (ti_on_agent_dismount, 0, 0, [], # server: make horses stand still after being dismounted from
   [(store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":horse_agent_id"),
    (agent_set_slot, ":horse_agent_id", slot_agent_horse_last_rider, ":agent_id"),
    (agent_set_slot, ":agent_id", slot_agent_last_horse_ridden, ":horse_agent_id"),
    (multiplayer_is_server),
    (agent_get_position, pos1, ":horse_agent_id"),
    (agent_set_scripted_destination, ":horse_agent_id", pos1, 0),

    (agent_get_player_id, ":player_id", ":agent_id"),
    (str_store_player_username, s0, ":player_id"),
    (agent_get_item_id, ":horse_item_id", ":horse_agent_id"),
    (str_store_item_name, s1, ":horse_item_id"),
    #Alter mount/dismount logs to show the agent_id of the mount
    (assign, reg31, ":horse_agent_id"),
    (server_add_message_to_log, "str_s0_has_dismounted_a_s1"),
    ])

instrument_check = (2, 0, 0, [], # server: handle agents playing instruments
   [(multiplayer_is_server),
    (call_script, "script_cf_check_musical_instrument"),
    ])

instrument_killed = (ti_on_agent_killed_or_wounded, 0, 0, [], # handle instruments
   [(store_trigger_param_1, ":dead_agent_id"),
    (call_script, "script_client_stop_playing_musical_instrument", ":dead_agent_id"),
    ])

instrument_unwielded = (ti_on_item_unwielded, 0, 0, [], # handle instruments
   [(store_trigger_param_1, ":agent_id"),
    (call_script, "script_cf_stop_playing_musical_instrument", ":agent_id"),
    (eq,reg20,1),
    (call_script, "script_client_stop_playing_musical_instrument", ":agent_id"),
    ])

instrument_dropped = (ti_on_item_dropped, 0, 0, [], # handle instruments
   [(store_trigger_param_1, ":agent_id"),
    (call_script, "script_cf_stop_playing_musical_instrument", ":agent_id"),
    (eq,reg20,1),
    (call_script, "script_client_stop_playing_musical_instrument", ":agent_id"),
    ])

instrument_with_sheild_wield = (ti_on_item_wielded, 0, 0, [], # handle instruments
   [(store_trigger_param_1, ":agent_id"),

    (agent_get_wielded_item, ":r_item_id", ":agent_id", 0),
    (this_or_next|eq, ":r_item_id", "itm_lute"),
    (eq, ":r_item_id", "itm_lyre"),

    (agent_get_wielded_item, ":item_id", ":agent_id", 1),
    (gt, ":item_id", all_items_begin),
    (item_get_type, ":item_type", ":item_id"),
    (eq, ":item_type", itp_type_shield),

    (agent_set_wielded_item, ":agent_id", -1),
    (agent_set_wielded_item, ":agent_id", ":r_item_id"),
    ])

instrument_with_sheild_pickup = (ti_on_item_picked_up, 0, 0, [],  # handle instruments
    [(store_trigger_param_1, ":agent_id"),

    (agent_get_wielded_item, ":r_item_id", ":agent_id", 0),
    (this_or_next|eq, ":r_item_id", "itm_lute"),
    (eq, ":r_item_id", "itm_lyre"),

    (agent_get_wielded_item, ":item_id", ":agent_id", 1),
    (gt, ":item_id", all_items_begin),
    (item_get_type, ":item_type", ":item_id"),
    (eq, ":item_type", itp_type_shield),

    (agent_set_wielded_item, ":agent_id", -1),
    (agent_set_wielded_item, ":agent_id", ":r_item_id"),
    ])

player_check_loop = (0, 0, 0.5, # server: check all players to see if any need agents spawned, also periodically lowering outlaw ratings
   [(multiplayer_is_server),
    (store_mission_timer_a, ":time"),
    (get_max_players, ":max_players"),
    (assign, ":loop_end", ":max_players"),
    (try_for_range, ":player_id", "$g_loop_player_id", ":loop_end"), # continue from the last player id checked
      (player_is_active, ":player_id"),
      (try_begin),
        (player_slot_eq, ":player_id", slot_player_spawn_state, player_spawn_state_dead),
        (call_script, "script_cf_player_check_spawn_agent", ":player_id"),
        (assign, ":loop_end", -1), # if the spawn checks were run, end the loop to give other triggers a chance to run, then immediately continue
        (store_add, "$g_loop_player_id", ":player_id", 1),
      (try_end),
      (try_begin),
        (eq, "$g_loop_player_check_outlaw", 1),
        (player_get_slot, ":outlaw_rating", ":player_id", slot_player_outlaw_rating),
        (try_begin),
          (gt, ":outlaw_rating", 0),
          (val_sub, ":outlaw_rating", 1),
          (player_set_slot, ":player_id", slot_player_outlaw_rating, ":outlaw_rating"),
          (multiplayer_send_3_int_to_player, ":player_id", server_event_player_set_slot, ":player_id", slot_player_outlaw_rating, ":outlaw_rating"),
        (try_end),
      (try_end),
      (try_begin),
        (player_is_active, ":player_id"),
        (player_get_slot, ":suicide_at_time", ":player_id", slot_player_commit_suicide_time),
        (try_begin),
          (gt, ":suicide_at_time", 0),
          (try_begin),
            (ge, ":time", ":suicide_at_time"),
            (player_get_agent_id, ":agent_id", ":player_id"),
            (agent_deliver_damage_to_agent, ":agent_id", ":agent_id", 500),

            (str_store_player_username, s1, ":player_id"),
            (server_add_message_to_log, "str_log_s1_committed_suicide"),

            (player_set_slot, ":player_id", slot_player_commit_suicide_time, 0),
          (try_end),
        (try_end),
      (try_end),
    (try_end),
    (eq, ":loop_end", ":max_players"), # if all players were checked, the trigger will succeed and wait the rearm interval before checking again
    (assign, "$g_loop_player_id", 1), # go back to the start (player id 0 is the server)
    (try_begin), # only decrease outlaw ratings at certain intervals, not every time
      (ge, ":time", "$g_loop_player_check_outlaw_time"),
      (val_add, "$g_loop_player_check_outlaw_time", loop_player_check_outlaw_interval),
      (assign, "$g_loop_player_check_outlaw", 1),
    (else_try),
      (assign, "$g_loop_player_check_outlaw", 0),
    (try_end),
    ], [])

agent_check_attack_loop = (0, 0, 0.2, [], # server: repeatedly check all agents for attacking with a weapon they can't use - should be kept as simple as possible
   [(multiplayer_is_server),
    (try_for_agents, ":agent_id"),
      (agent_slot_eq, ":agent_id", slot_agent_cannot_attack, 1),
      (agent_get_attack_action, ":action", ":agent_id"),
      (is_between, ":action", 1, 7), # if the agent attack action is anything except "free" or "cancelling attack", unwield the weapon
      (agent_set_wielded_item, ":agent_id", -1),
    (try_end),
    ])

agent_check_drowning_loop = (loop_drowning_check_interval, 0, 0, #** agent_check_loop split to 3 loops
   [(multiplayer_is_server),
    (try_for_agents, ":agent_id"),
      (call_script, "script_check_agent_drowning", ":agent_id"),
    (try_end),
    ], [])

agent_check_health_loop = (loop_health_check_interval, 0, 0,
   [(multiplayer_is_server),
    (try_for_agents, ":agent_id"),
      (call_script, "script_check_agent_health", ":agent_id"),
    (try_end),
    ], [])

agent_check_horse_ammo_loop = (loop_horse_ammo_check_interval, 0, 0,
   [(multiplayer_is_server),
    (try_for_agents, ":agent_id"),
      (try_begin),
        (neg|agent_is_human, ":agent_id"),
        (call_script, "script_check_remove_lost_horse", ":agent_id"),
      (else_try),
        (call_script, "script_agent_remove_empty_ammo_stacks", ":agent_id"),
      (try_end),
    (try_end),
    ], [])#


ship_movement_loop = (0, 0, 0.1, # server: update ship movement animations approximately every second
   [(try_begin),
      (multiplayer_is_server),
      (troop_get_slot, ":ship_array_end", "trp_ship_array", slot_ship_array_count),
      (gt, ":ship_array_end", 0),
      (try_begin), # after running the script for a moving ship, end the loop to allow other triggers to run, then immediately continue the loop
        (ge, "$g_loop_ship_to_check", slot_ship_array_begin),
        (val_add, ":ship_array_end", slot_ship_array_begin),
        (assign, ":loop_end", ":ship_array_end"),
        (try_for_range, ":ship_slot", "$g_loop_ship_to_check", ":loop_end"),
          (troop_get_slot, ":hull_instance_id", "trp_ship_array", ":ship_slot"),
          (scene_prop_slot_eq, ":hull_instance_id", slot_scene_prop_state, scene_prop_state_active),
          (try_begin), # if all possible movement slots make the ship stationary, skip
            (scene_prop_slot_eq, ":hull_instance_id", slot_scene_prop_position, 0),
            (scene_prop_slot_eq, ":hull_instance_id", slot_scene_prop_target_position, 0),
            (scene_prop_get_slot, ":ramp_instance_id", ":hull_instance_id", slot_scene_prop_linked_ramp),
            (try_begin),
              (neq, ":ramp_instance_id", -1),
              (scene_prop_get_slot, ":ramp_position", ":ramp_instance_id", slot_scene_prop_position),
              (scene_prop_slot_eq, ":ramp_instance_id", slot_scene_prop_target_position, ":ramp_position"),
              (assign, ":ramp_instance_id", -1),
            (try_end),
            (eq, ":ramp_instance_id", -1),
          (else_try), # otherwise, move the ship
            (call_script, "script_move_ship", ":hull_instance_id"),
            (assign, ":loop_end", -1),
          (try_end),
        (try_end),
        (store_add, "$g_loop_ship_to_check", ":ship_slot", 1),
        (try_begin),
          (ge, "$g_loop_ship_to_check", ":ship_array_end"),
          (assign, "$g_loop_ship_to_check", -1),
        (try_end),
      (else_try),
        (store_mission_timer_a, ":time"),
        (try_begin), # recheck the time every 0.1 seconds, but only move the ships every 1 second, so small extra delays in the trigger timer don't accumulate
          (ge, ":time", "$g_loop_ship_check_time"),
          (val_add, "$g_loop_ship_check_time", 1),
          (val_sub, ":time", 1),
          (val_max, "$g_loop_ship_check_time", ":time"),
          (assign, "$g_loop_ship_to_check", slot_ship_array_begin),
        (try_end),
      (try_end),
    (try_end),
    (this_or_next|eq, "$g_loop_ship_to_check", -1),
    (this_or_next|neg|multiplayer_is_server),
    (eq, ":ship_array_end", 0),
    ], [])

resource_regrow_check = (10, 0, 0, [], # server: call the script to regrow a removed scene prop after the required time
   [(multiplayer_is_server),
    (troop_get_slot, ":resources_count", "trp_removed_scene_props", slot_array_count),
    (gt, ":resources_count", 0),
    (val_add, ":resources_count", slot_array_begin),
    (try_for_range, ":resource_slot", slot_array_begin, ":resources_count"), # loop over all scene props added to the removed list
      (troop_get_slot, ":instance_id", "trp_removed_scene_props", ":resource_slot"),
      (le, ":instance_id", 0),
    (else_try),
      (scene_prop_get_slot, ":regrow_script", ":instance_id", slot_scene_prop_regrow_script),
      (eq, ":regrow_script", 0),
      (neg|scene_prop_slot_eq, ":instance_id", slot_scene_prop_state, scene_prop_state_hidden),
      (troop_set_slot, "trp_removed_scene_props", ":resource_slot", -1),
    (else_try),
      (scene_prop_get_slot, ":regen_time", ":instance_id", slot_scene_prop_state_time),
      (store_mission_timer_a, ":time"),
      (ge, ":time", ":regen_time"), # if the regeneration time is passed, remove from the list and call the stored script
      (troop_set_slot, "trp_removed_scene_props", ":resource_slot", -1),
      (try_begin),
        (eq, ":regrow_script", 0),
        (call_script, "script_regrow_resource", ":instance_id"),
      (else_try),
        (call_script, ":regrow_script", ":instance_id"),
      (try_end),
    (try_end),
    ])

polls_check = (2, 0, 0, [], # server: regularly check to see if any polls have ended
   [(multiplayer_is_server),
    (call_script, "script_check_polls_ended"),
    ])

game_ended_check = (1, 5, 0, # server: check for game end from victory or an admin scene change
   [(multiplayer_is_server),
    (eq, "$g_game_ended", 0),
    (store_mission_timer_a, ":current_time"),
    (store_mul, ":game_end_time", "$g_game_time_limit", 60),
    (try_begin), # check for the victory condition
      (call_script, "script_cf_victory_condition_met"),
      (assign, ":faction_id", reg0),
      (try_begin), # if only just met, store the time when the game could end
        (le, "$g_victory_condition_time", 0),
        (store_mul, "$g_victory_condition_time", "$g_victory_condition", 60),
        (val_add, "$g_victory_condition_time", ":current_time"),
      (else_try),
        (gt, "$g_victory_condition_time", 0),
        (this_or_next|ge, ":current_time", "$g_victory_condition_time"), # if the victory condition has held for the required time, end the game
        (ge, ":current_time", ":game_end_time"),
        (try_for_players, ":player_id", 1),
          (player_is_active, ":player_id"),
          (multiplayer_send_3_int_to_player, ":player_id", server_event_preset_message, "str_s1_reign_supreme", preset_message_faction|preset_message_big|preset_message_log, ":faction_id"),
        (try_end),
        (assign, "$g_game_ended", 1),
      (try_end),
    (else_try), # reset the victory condition timer
      (assign, "$g_victory_condition_time", 0),
    (try_end),
    (this_or_next|eq, "$g_game_ended", 1),
    (this_or_next|is_between, "$g_next_scene", scenes_begin, scenes_end), # end the mission if an admin changes the scene
    (ge, ":current_time", ":game_end_time"),
    (assign, "$g_game_ended", 1),
    ],
   [(try_begin), # after the delay, start the next mission
      (neg|is_between, "$g_next_game_type", game_type_mission_templates_begin, game_type_mission_templates_end),
      (assign, "$g_next_game_type", game_type_mission_templates_begin),
    (try_end),
    (assign, ":started_manually", 1),
    (try_begin),
      (neg|is_between, "$g_next_scene", scenes_begin, scenes_end),
      (assign, "$g_next_scene", scenes_begin),
      (assign, ":started_manually", 0),
    (try_end),
    (start_multiplayer_mission, "$g_next_game_type", "$g_next_scene", ":started_manually"),
    (call_script, "script_game_set_multiplayer_mission_end"),
    ])

draw_initial_banners = (0, 0, ti_once, [], # server: calculate and draw all castle banners at mission start
   [(multiplayer_is_server),
    (call_script, "script_redraw_castle_banners", redraw_all_banners, -1),
    ])

fill_chests_starting_inventory = (8, 0, ti_once, [], # server: wait so the pseudo random number generator can get some entropy
   [(multiplayer_is_server),
    (eq, random_gear_in_chests, 1),
    (call_script, "script_scene_fill_chests_starting_inventory"),
    ])

fire_place_check = (1, 0, 60, # server: wait 1 second between checks of fire heaps, then 60 seconds after all have been checked
   [(multiplayer_is_server),
    (scene_prop_get_instance, ":instance_id", "spr_pw_fire_wood_heap", "$g_fire_place_instance_no"),
    (call_script, "script_fire_place_burn", ":instance_id"),
    (val_add, "$g_fire_place_instance_no", 1),
    (scene_prop_get_num_instances, ":num_instances", "spr_pw_fire_wood_heap"),
    (try_begin),
      (ge, "$g_fire_place_instance_no", ":num_instances"),
      (assign, "$g_fire_place_instance_no", 0),
    (try_end),
    (eq, "$g_fire_place_instance_no", 0),
    ], [])

fish_school_loop = (0.1, 0, 30, # server: wait 0.1 seconds between checks of fish schools, then 30 seconds after all have been checked
   [(multiplayer_is_server),
    (try_begin),
      (scene_prop_get_instance, ":instance_id", "spr_pw_fish_school", "$g_fish_school_instance_no"),
      (call_script, "script_move_fish_school", ":instance_id"),
      (val_add, "$g_fish_school_instance_no", 1),
    (else_try), # at the loop end, check all nets as well
      (assign, "$g_fish_school_instance_no", 0),
      (call_script, "script_check_fishing_nets"),
    (try_end),
    (eq, "$g_fish_school_instance_no", 0),
    ], [])

herd_leader_movement_loop = (5, 0, 0, [], # server: check all animal herd leaders to see if any are ready to move
   [(multiplayer_is_server),
    (le, "$g_loop_animal_herd_begin", 0), # not currently moving a herd
    (scene_spawned_item_get_num_instances, ":herds_end", "itm_animal_herd_manager"),
    (try_begin),
      (ge, "$g_loop_animal_herd_to_move", ":herds_end"),
      (assign, "$g_loop_animal_herd_to_move", 0),
    (try_end),
    (store_mission_timer_a, ":time"), # loop over next herd managers to check if any are ready to move
    (try_for_range, "$g_loop_animal_herd_to_move", "$g_loop_animal_herd_to_move", ":herds_end"),
      (scene_spawned_item_get_instance, ":herd_manager", "itm_animal_herd_manager", "$g_loop_animal_herd_to_move"),
      (assign, "$g_loop_animal_herd_leader", -1),
      (scene_prop_get_slot, ":adult_item_id", ":herd_manager", slot_animal_herd_manager_adult_item_id),
      (item_get_slot, ":loop_end", ":adult_item_id", slot_item_animal_max_in_herd),
      (try_for_range, ":herd_slot", 0, ":loop_end"), # loop over animals in the herd
        (scene_prop_get_slot, ":herd_agent_id", ":herd_manager", ":herd_slot"),
        (gt, ":herd_agent_id", -1),
        (try_begin),
          (agent_is_active, ":herd_agent_id"),
          (agent_get_item_id, ":herd_item_id", ":herd_agent_id"),
          (agent_slot_eq, ":herd_agent_id", slot_agent_animal_herd_manager, ":herd_manager"),
          (gt, ":herd_item_id", -1),
          (item_slot_eq, ":herd_item_id", slot_item_animal_adult_item_id, ":adult_item_id"),
          (try_begin), # if the leader has been found, set the times for the followers to move
            (neq, "$g_loop_animal_herd_leader", -1),
            (store_random_in_range, ":move_time", 0, 6),
            (val_add, ":move_time", ":time"),
            (agent_set_slot, ":herd_agent_id", slot_agent_animal_move_time, ":move_time"),
          (else_try), # the first valid animal found is the leader: start the movement if the set time is met
            (assign, "$g_loop_animal_herd_leader", ":herd_agent_id"),
            (neg|agent_slot_ge, ":herd_agent_id", slot_agent_animal_move_time, ":time"),
            (assign, ":herds_end", -1), # break out of the herd manager checking loop after the animal loop is finished
            (store_add, "$g_loop_animal_herd_begin", ":herd_slot", 1),
            (store_random_in_range, ":move_time", 5, 31), # set the next move time
            (val_add, ":move_time", ":time"),
            (agent_set_slot, "$g_loop_animal_herd_leader", slot_agent_animal_move_time, ":move_time"),
            (call_script, "script_animal_move", "$g_loop_animal_herd_leader", "$g_loop_animal_herd_leader"), # move the leader
          (else_try), # if the leader movement time is not met, skip to the next herd manager to check
            (assign, ":loop_end", -1),
          (try_end),
        (else_try), # if the animal or agent id is not valid, remove it from the herd manager
          (scene_prop_set_slot, ":herd_manager", ":herd_slot", -1),
          (agent_is_active, ":herd_agent_id"),
          (le, ":herd_item_id", -1),
          (agent_set_slot, ":herd_agent_id", slot_agent_animal_herd_manager, -1),
        (try_end),
      (try_end),
      (try_begin), # if no valid animals are found, remove the herd manager
        (eq, "$g_loop_animal_herd_leader", -1),
        (scene_prop_set_prune_time, ":herd_manager", 1),
      (try_end),
    (try_end),
    ])

herd_follower_movement_loop = (0.5, 0, 0, [], # server: when currently moving a herd, check the follower animals for any ready to move
   [(multiplayer_is_server),
    (gt, "$g_loop_animal_herd_begin", 0), # currently moving a herd
    (try_begin), # if the herd leader and manager are valid
      (agent_is_active, "$g_loop_animal_herd_leader"),
      (scene_spawned_item_get_instance, ":herd_manager", "itm_animal_herd_manager", "$g_loop_animal_herd_to_move"),
      (store_mission_timer_a, ":time"),
      (scene_prop_get_slot, ":adult_item_id", ":herd_manager", slot_animal_herd_manager_adult_item_id),
      (item_get_slot, ":loop_end", ":adult_item_id", slot_item_animal_max_in_herd),
      (assign, ":remaining_to_move", 0),
      (try_for_range, ":herd_slot", "$g_loop_animal_herd_begin", ":loop_end"), # loop over the followers to check if any are ready to move
        (scene_prop_get_slot, ":herd_agent_id", ":herd_manager", ":herd_slot"),
        (agent_is_active, ":herd_agent_id"),
        (agent_get_slot, ":move_time", ":herd_agent_id", slot_agent_animal_move_time),
        (gt, ":move_time", 0),
        (try_begin),
          (ge, ":time", ":move_time"),
          (agent_set_slot, ":herd_agent_id", slot_agent_animal_move_time, 0),
          (call_script, "script_animal_move", ":herd_agent_id", "$g_loop_animal_herd_leader"),
        (else_try),
          (val_add, ":remaining_to_move", 1),
        (try_end),
      (try_end),
      (gt, ":remaining_to_move", 0), # if any followers are still waiting
    (else_try), # otherwise, go back to the herd manager checking loop
      (assign, "$g_loop_animal_herd_begin", 0),
      (val_add, "$g_loop_animal_herd_to_move", 1),
    (try_end),
    ])

herd_animal_count_check = (300, 0, 0, [], # server: periodically update the global count of herd animals - rare conditions seemed to make this value incorrect over time
   [(multiplayer_is_server),
    (assign, "$g_herd_animal_count", 0),
    (try_for_agents, ":agent_id"),
      (agent_slot_ge, ":agent_id", slot_agent_animal_birth_time, 1),
      (val_add, "$g_herd_animal_count", 1),
    (try_end),
    ])

herd_animal_spawn_check = (60, 0, 0, [], # server: check all herd animal spawners to see if any are ready to activate
   [(multiplayer_is_server),
    (try_begin), # if the maximum number of herd animals in the server is not reached, check the spawners
      (lt, "$g_herd_animal_count", "$g_max_herd_animal_count"),
      (scene_prop_get_instance, ":instance_id", "spr_pw_herd_animal_spawn", "$g_herd_animal_spawn_instance_no"),
      (val_add, "$g_herd_animal_spawn_instance_no", 1),
      (assign, ":fail", 0),
      (try_for_agents, ":agent_id"),
        (agent_is_active, ":agent_id"),
        (agent_is_alive, ":agent_id"),
        (neg^agent_is_human, ":agent_id"),
        (agent_slot_eq, ":agent_id", slot_agent_animal_spawn_instance, ":instance_id"),
        (assign, ":fail", 1),
        (break_loop),
      (try_end),
      (eq, ":fail", 0),
      (scene_prop_get_slot, ":spawn_time", ":instance_id", slot_scene_prop_state_time),
      (store_mission_timer_a, ":time"),
      (try_begin), # if the spawning time has been reached
        (gt, ":time", ":spawn_time"),
        (prop_instance_get_variation_id_2, ":next_spawn_time", ":instance_id"),
        (try_begin), # if the spawn interval value is not set, get a random time between 1 and 4 hours
          (lt, ":next_spawn_time", 1),
          (store_random_in_range, ":next_spawn_time", 3600, 24001),
        (else_try), # otherwise, convert it to hours and apply a random adjustment between +/- 20%
          (val_mul, ":next_spawn_time", 3600),
          (store_random_in_range, ":random_adjustment", 80, 121),
          (val_mul, ":next_spawn_time", ":random_adjustment"),
          (val_div, ":next_spawn_time", 100),
        (try_end),
        (scene_prop_set_slot, ":instance_id", slot_scene_prop_state_time, ":next_spawn_time"),
        (gt, ":spawn_time", 0), # if not mission start
        (prop_instance_get_variation_id, ":animal_item_id", ":instance_id"),
        (try_begin), # use the animal type if set
          (val_add, ":animal_item_id", herd_animal_items_begin),
          (val_sub, ":animal_item_id", 1),
          (is_between, ":animal_item_id", herd_animal_items_begin, herd_animal_items_end),
        (else_try), # otherwise get a random herd animal
          (store_random_in_range, ":animal_item_id", herd_animal_items_begin, herd_animal_items_end),
        (try_end),
        (prop_instance_get_position, pos1, ":instance_id"),
        (call_script, "script_cf_spawn_herd_animal", ":animal_item_id", -1),
        (agent_set_slot, reg0, slot_agent_animal_spawn_instance, ":instance_id"),
      (try_end),
    (else_try),
      (assign, "$g_herd_animal_spawn_instance_no", 0),
    (try_end),
    ])

weather_situation_check = (loop_weather_adjust_interval, 0, 0, [], # server: adjust the weather systems in the scene
   [(multiplayer_is_server),
    (call_script, "script_scene_adjust_weather_situation"),
    ])

skybox_update_interval = (5, 0, 0, [], [
  (multiplayer_is_server),
  (eq, "$g_day_night_cycle_enabled", 1),
  (call_script, "script_skybox_send_info_to_players"),
])

#** Added by us.
flood_log_refresh = (5, 0, 0, [
  (multiplayer_is_server),
  (try_for_players, ":player_id", 1),
    (player_set_slot, ":player_id", slot_player_flood_log, 0),
  (try_end),
], [])

#ScriptsBySartman
teleport_door_refresh = (2, 0, 0, [
  (multiplayer_is_server),
  (troop_get_slot, ":cache_count", "trp_teleport_timer_caches", 0),
  (val_add, ":cache_count", 1),
  (try_for_range, ":cache_index", 0, ":cache_count"),
    (troop_get_slot, ":instance_id", "trp_teleport_timer_caches", ":cache_index"),
    (neg^scene_prop_slot_eq, ":instance_id", slot_scene_prop_teleport_timer, 0),
    (scene_prop_get_slot, ":value", ":instance_id", slot_scene_prop_teleport_timer),
    (val_sub, ":value", 2),
    (val_max, ":value", 0),
    (scene_prop_set_slot, ":instance_id", slot_scene_prop_teleport_timer, ":value"),
    (try_begin),
      (scene_prop_slot_eq, ":instance_id", slot_scene_prop_teleport_timer, 0),
      (prop_instance_play_sound, ":instance_id", "snd_lock"),
    (try_end),
  (try_end),
], [])

idle_income = (900, 0, 0, [
  (multiplayer_is_server),
  (neq, "$g_idle_income", 0),
  (try_for_players, ":player_id", 1),
    (call_script, "script_player_adjust_gold", ":player_id", "$g_idle_income", 1),
  (try_end),
], [])

ping_tcp_server = (10, 0, 0, [
  (multiplayer_is_server),
  (send_message_to_url_advanced, script_ip_address + "/ping_tcp", "@WSE2", "script_ping_tcp_return", "script_ping_tcp_fail"),
], [])

autosave = (900, 0, 0, [
  (multiplayer_is_server),
  (eq, "$g_is_autosave_enabled", 1),
], [
  (call_script, "script_save_server"),
])

time_update = (60, 0, 0, [
  (multiplayer_is_server),
  (try_for_players, ":player_id", 1),
    (player_get_slot, ":time", ":player_id", slot_player_time),
    (val_add, ":time", 1),
    (player_set_slot, ":player_id", slot_player_time, ":time"),
  (try_end),
], [])

rot_update = (120, 0, 0, [
  (multiplayer_is_server),
  (try_for_prop_instances, ":instance_id"),
    (scene_prop_get_slot, ":count", ":instance_id", slot_scene_prop_inventory_count),
    (gt, ":count", 0),
    
  (try_end),
], [])

load_fail_update = (5, 0, 0, [
  (try_for_players, ":player_id", 1),
    (try_begin),
      (player_slot_eq, ":player_id", slot_player_has_loaded_player, 0),
      (call_script, "script_load_player", ":player_id"),
    (else_try),
      (player_is_admin, ":player_id"),
      (player_slot_eq, ":player_id", slot_player_has_loaded_admin, 0),
      (call_script, "script_load_admin", ":player_id"),
    (else_try),
      (player_get_agent_id, ":agent_id", ":player_id"),
      (agent_is_active, ":agent_id"),
      (agent_is_alive, ":agent_id"),
      (player_slot_eq, ":player_id", slot_player_has_loaded_gear, 0),
      (call_script, "script_load_gear", ":player_id"),
    (else_try),
      (this_or_next|player_slot_eq, ":player_id", slot_player_saving_player, 1),
      (player_slot_eq, ":player_id", slot_player_saving_inventory, 1),
      (call_script, "script_cf_save_player", ":player_id"),
    (else_try),
      (player_slot_eq, ":player_id", slot_player_saving_gear, 1),
      (call_script, "script_cf_save_gear", ":player_id", 0),
    (try_end),
  (try_end),

  (try_begin),
    (eq, "$g_loading_settings", 1),
    (send_message_to_url_advanced, script_ip_address + "/update_settings", "@WSE2", "script_ping_tcp_return", "script_update_settings_fail"),
  (try_end),
  
] + [elem for sublist in [[
  (call_script, "script_check_chests", "spr_" + scene_prop),
] for scene_prop in storage_scene_props] for elem in sublist] + [
], [])
#

def common_triggers(mission_template):
    return [
        (ti_before_mission_start, 0, 0, [(assign, "$g_game_type", "mt_" + mission_template)], []),#0
        before_mission_start_setup,#1
        after_mission_start_setup,#2
        player_joined,#3
        player_exit,#4
        agent_spawn,#5
        agent_killed,#6
        agent_hit,#7
        item_picked_up,#8
        item_dropped,#9
        item_wielded,#10
        item_unwielded,#11
        agent_mount,#12
        agent_dismount,#13
        instrument_check,#14
        instrument_killed,#15
        instrument_unwielded,#16
        instrument_dropped,#17
        instrument_with_sheild_wield,#18
        instrument_with_sheild_pickup,#19
        player_check_loop,#20
        agent_check_attack_loop,#21
        agent_check_drowning_loop,#22
        agent_check_health_loop,#23
        agent_check_horse_ammo_loop,#24#
        ship_movement_loop,#25
        resource_regrow_check,#26
        polls_check,#27
        game_ended_check,#28
        draw_initial_banners,#29
        fire_place_check,#30
        fish_school_loop,#31
        herd_leader_movement_loop,#32
        herd_follower_movement_loop,#33
        herd_animal_count_check,#34
        herd_animal_spawn_check,#35
        weather_situation_check,#36
        flood_log_refresh,#37
        idle_income,#38
        ping_tcp_server,#39
        autosave,#40
        time_update,#41
        teleport_door_refresh,#42
        skybox_update_interval,#43
        rot_update,#44
        load_fail_update,#45
    ]

mission_templates = [
  ("conquest", mtf_battle_mode, -1, "Conquest.", spawn_points_0_99,
    common_triggers("conquest") + [
    ]),
    
  ("multiplayer_dm", mtf_battle_mode, -1, "Deathmatch.", spawn_points_0_99,
    common_triggers("multiplayer_dm") + [
    ]),

  ("quick_battle", mtf_battle_mode, -1, "Quick battle.", spawn_points_0_99,
    common_triggers("quick_battle") + [
    ]),

  ("no_money", mtf_battle_mode, -1, "No money.", spawn_points_0_99,
    common_triggers("no_money")
    ),

  ("feudalism", mtf_battle_mode, -1, "Feudalism.", spawn_points_0_99,
    common_triggers("feudalism") + [
    ]),

  ("permanent_death", mtf_battle_mode, -1, "Permanent death.", spawn_points_0_99,
    common_triggers("permanent_death") + [
    ]),

  ("edit_scene", 0, -1, "edit_scene", [(0,mtef_visitor_source,0,aif_start_alarmed,1,[])],
    common_triggers("edit_scene") + [
    ]),
]
