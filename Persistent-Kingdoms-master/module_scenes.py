from header_common import *
from header_operations import *
from header_triggers import *
from header_scenes import *
from module_constants import *

####################################################################################################################
#  Each scene record contains the following fields:
#  1) Scene id {string}: used for referencing scenes in other files. The prefix scn_ is automatically added before each scene-id.
#  2) Scene flags {int}. See header_scenes.py for a list of available flags
#  3) Mesh name {string}: This is used for indoor scenes only. Use the keyword "none" for outdoor scenes.
#  4) Body name {string}: This is used for indoor scenes only. Use the keyword "none" for outdoor scenes.
#  5) Min-pos {(float,float)}: minimum (x,y) coordinate. Player can't move beyond this limit.
#  6) Max-pos {(float,float)}: maximum (x,y) coordinate. Player can't move beyond this limit.
#  7) Water-level {float}: doesn't seem to work for outdoor scenes in multiplayer, at least.
#  8) Terrain code {string}: You can obtain the terrain code by copying it from the terrain generator screen
#  9) List of other scenes accessible from this scene {list of strings}.
#     (deprecated. This will probably be removed in future versions of the module system)
#     (In the new system passages are used to travel between scenes and
#     the passage's variation-no is used to select the game menu item that the passage leads to.)
# 10) List of chest-troops used in this scene {list of strings}. You can access chests by placing them in edit mode.
#     The chest's variation-no is used with this list for selecting which troop's inventory it will access.
####################################################################################################################

# When adding a new scene entry, remember to add a name at the correct place in module_strings.

scenes = [
  ("scene_1",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_2",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_3",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_4",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_5",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_6",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_7",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_8",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_9",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_10",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_11",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_12",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_13",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_14",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_15",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_16",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_17",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_18",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_19",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_20",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_21",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_22",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_23",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_24",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_25",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_26",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_27",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_28",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_29",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scene_30",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
  ("scenes_end",sf_generate,"none","none",(0,0),(300,300),-100,"0x000000033000124c000acab40000280700000c9f00000ab5",[],[],"outer_terrain_pw_1"),
]
