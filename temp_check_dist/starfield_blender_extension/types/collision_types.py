# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Script copyright (C) 2024, Zenimax Media

import bpy
from ..utils import bgs
from ..utils import bs_plugin_data

#
collider_shapes = [
    "Box",
    "Sphere",
    "Capsule",
    # "Cylinder", # not supported in starfield, converts as capsule
    "ConvexHull",
    "ConcaveMesh"
]


def shape_enum_items(self, context):
    items = []
    for k in collider_shapes:
        items.append((k, k, ''))
    return items


# source: enum COL_LAYER
collision_layers = {
    "Unidentified": 0,
    "Static": 1,
    "Anim Static": 2,
    "Transparent": 3,
    "Clutter": 4,
    "Weapon": 5,
    "Projectile": 6,
    "Spell": 7,
    "Biped": 8,
    "Tree": 9,
    "Prop": 10,
    "Water": 11,
    "Trigger": 12,
    "Terrain": 13,
    "Trap": 14,
    "NonCollidable": 15,
    "CloudTrap": 16,
    "Ground": 17,
    "Portal": 18,
    "Small Debris": 19,
    "Large Debris": 20,
    "Acoustic Space": 21,
    "ActorZone": 22,
    "ProjectileZone": 23,
    "GasTrap": 24,
    "ShellCasing": 25,
    "Transparent Small": 26,
    "Invisible Wall": 27,
    "Transparent Small Anim": 28,
    "Clutter Large": 29,
    "Character Controller": 30,
    "Stair Helper": 31,
    "Shield": 43,
    "FX Collider": 44,
    "Falling Trap": 48,
    "NavMesh Cut": 49,
    "Critter": 50,
    "spellTrigger": 51,
    "Living and Dead Actors": 52,
    "Clutter NoNavCut": 55,
}


def layer_enum_items(self, context):
    items = []
    for k, v in collision_layers.items():
        items.append((str(v), k, ''))
    return items


# source: enum BIPED_PART
biped_parts = {
    "P_OTHER": 0,
    "P_HEAD": 1,
    "P_BODY": 2,
    "P_SPINE1": 3,
    "P_SPINE2": 4,
    "P_LUPPERARM": 5,
    "P_LFOREARM": 6,
    "P_LHAND": 7,
    "P_LTHIGH": 8,
    "P_LCALF": 9,
    "P_LFOOT": 10,
    "P_RUPPERARM": 11,
    "P_RFOREARM": 12,
    "P_RHAND": 13,
    "P_RTHIGH": 14,
    "P_RCALF": 15,
    "P_RFOOT": 16,
    "P_TAIL": 17,
    "P_SHIELD": 18,
    "P_QUIVER": 19,
    "P_WEAPON": 20,
    "P_PONYTAIL": 21,
    "P_WING": 22,
    "P_PACK": 23,
    "P_CHAIN": 24,
    "P_ADDONHEAD": 25,
    "P_ADDONCHEST": 26,
    "P_ADDONLEG": 27,
    "P_ADDONARM": 28,
}


def biped_part_enum_items(self, context):
    items = []
    for k, v in biped_parts.items():
        items.append((str(v), k, ''))
    return items


# source: one entry for every BGSMaterialType form
material_types = {
    "Custom": bgs.custom_enum_value(),
    "alduin": 1730220269,
    "Barrel": 732141076,
    "BoneActor": 2058949504,
    "Bottle": 493553910,
    "Broken Stone": 131151687,
    "Cloth": 3839073443,
    "Dirt": 3106094762,
    "Dragon": 2518321175,
    "ghost": 3312543676,
    "GLASS": 3739830338,
    "Grass": 1848600814,
    "Gravel": 428587608,
    "Heavy Metal": 2229413539,
    "Heavy Stone": 1570821952,
    "Heavy Wood": 3070783559,
    "Ice": 873356572,
    "Insect": 668408902,
    "Light Wood": 365420259,
    "MaterialArmorHeavy": 3708432437,
    "MaterialArmorLight": 3424720541,
    "MaterialArrow": 3725505938,
    "MaterialAsh": 534864873,
    "MaterialAxe1Hand": 1305674443,
    "MaterialBasket": 790784366,
    "MaterialBlade1Hand": 1060167844,
    "MaterialBlade1HandSmall": 2617944780,
    "MaterialBlade2Hand": 2022742644,
    "MaterialBlockAxe": 3400476823,
    "MaterialBlockBlade1Hand": 165778930,
    "MaterialBlockBlade2Hand": 1312943906,
    "MaterialBlockBlunt": 593401068,
    "MaterialBlockBlunt2Hand": 3662306947,
    "MaterialBlockBowsStaves": 1763418903,
    "MaterialBlunt1Hand": 2872791301,
    "MaterialBlunt2Hand": 3969592277,
    "MaterialBone": 3049421844,
    "MaterialBook": 1264672850,
    "MaterialBottleSmall": 2025794648,
    "MaterialBoulderLarge": 1885326971,
    "MaterialBoulderMedium": 4283869410,
    "MaterialBoulderSmall": 1550912982,
    "MaterialBowsStaves": 1607128641,
    "MaterialCarpet": 1286705471,
    "MaterialCarriageWheel": 322207473,
    "MaterialCeramicMedium": 781661019,
    "MaterialChain": 3074114406,
    "MaterialChainMetal": 438912228,
    "MaterialCoin": 3589100606,
    "MaterialIceForm": 2431524493,
    "MaterialMeat": 220124585,
    "MaterialMetalLight": 346811165,
    "MaterialPotsPans": 2742858142,
    "MaterialShieldHeavy": 3702389584,
    "MaterialShieldLight": 3448167928,
    "MaterialSkinLarge": 2965929619,
    "MaterialSkinMetalLarge": 3387452107,
    "MaterialSkinMetalSmall": 3855001958,
    "MaterialSkinSkeleton": 2821299363,
    "MaterialSkinSmall": 2632367422,
    "MaterialStoneAsStairs": 1886078335,
    "MaterialWaterPuddle": 3764646153,
    "MaterialWoodAsStairs": 1803571212,
    "Mud": 1486385281,
    "Organic": 2974920155,
    "OrganicLarge": 1322093133,
    "Sand": 2168343821,
    "skin": 591247106,
    "Snow": 398949039,
    "Solid Metal": 1288358971,
    "StairsBrokenStone": 2892392795,
    "StairsGlass": 880200008,
    "StairsSnow": 1560365355,
    "StairsStone": 899511101,
    "StairsWood": 1461712277,
    "Stone": 3741512247,
    "WARD": 3895166727,
    "Water": 1024582599,
    "Web": 3934839107,
    "WOOD": 500811281,
}


def material_type_enum_items(self, context):
    items = []
    for k, v in material_types.items():
        items.append((str(v), k, ''))
    return items


class BGS_STARFIELD_PG_havok_collider(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(
        items=shape_enum_items, default=0, name="Type",
        description="Collision shape geometry (Box, Sphere, Capsule, etc.)")  # MeshBoundType # type: ignore
    layer: bpy.props.EnumProperty(items=layer_enum_items, default=bgs.items_index_of(
        layer_enum_items(None, None), "Static"), name="Layer",
        description="Collision layer determining interaction rules")  # COL_LAYER aeLayer # type: ignore
    part: bpy.props.EnumProperty(
        items=biped_part_enum_items, default=0, name="Part",
        description="Biped body part for hit detection and damage")  # BIPED_PART aePart # type: ignore
    material: bpy.props.EnumProperty(
        items=material_type_enum_items, default=bgs.items_index_of(
            material_type_enum_items(None, None),
            "Dirt"),
        name="Material", description="Material type affecting collision sounds and effects")  # BGSMaterialType form # type: ignore
    custom_material: bpy.props.IntProperty(default=0, name="Custom Material",
                                           description="Custom material ID for advanced collision properties")  # type: ignore
    is_collider: bpy.props.BoolProperty(default=False,
                                        description="Enable collision detection for this object")  # type: ignore


def constraint_type_items(self, context):
    items = [
        ("RAGDOLL", "Ragdoll", ""),
        ("HINGE", "Hinge", ""),
        ("PRISMATIC", "Prismatic", ""),
    ]
    return items


class BGS_STARFIELD_PG_constraint(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(items=constraint_type_items,
                                 description="Type of physics constraint")  # type: ignore

    child_space_translation: bpy.props.FloatVectorProperty(
        name="Child Space Translation", size=3,
        description="Position offset in the child's local space")  # type: ignore
    child_space_rotation_e: bpy.props.FloatVectorProperty(
        name="Child Space Rotation", subtype='EULER', size=3,
        description="Rotation offset in the child's local space")  # type: ignore
    parent_space_translation: bpy.props.FloatVectorProperty(
        name="Parent Space Translation", size=3,
        description="Position offset in the parent's local space")  # type: ignore
    parent_space_rotation_e: bpy.props.FloatVectorProperty(
        name="Parent Space Rotation", subtype='EULER', size=3,
        description="Rotation offset in the parent's local space")  # type: ignore

    connected_node: bpy.props.PointerProperty(type=bpy.types.Object,
                                              description="Object this constraint connects to")  # type: ignore
    # world_or_parent: bpy.props.BoolProperty(default=False)
    # is_breakable: bpy.props.BoolProperty(default=False)
    # break_threshold: bpy.props.FloatProperty(default=0.0)

    ragdoll_cone_min_angle: bpy.props.FloatProperty(default=0.0,
                                                description="Minimum cone angle for ragdoll constraint")  # type: ignore
    ragdoll_max_friction_torque: bpy.props.FloatProperty(default=0.0,
                                                         description="Maximum friction torque for ragdoll")  # type: ignore
    ragdoll_plane_max_angle: bpy.props.FloatProperty(default=0.0,
                                                     description="Maximum plane angle for ragdoll constraint")  # type: ignore
    ragdoll_plane_min_angle: bpy.props.FloatProperty(default=0.0,
                                                     description="Minimum plane angle for ragdoll constraint")  # type: ignore
    ragdoll_twist_max_angle: bpy.props.FloatProperty(default=0.0,
                                                     description="Maximum twist angle for ragdoll constraint")  # type: ignore
    ragdoll_twist_min_angle: bpy.props.FloatProperty(default=0.0,
                                                     description="Minimum twist angle for ragdoll constraint")  # type: ignore

    hinge_limited: bpy.props.BoolProperty(default=False,
                                          description="Enable angle limits for hinge constraint")  # type: ignore
    hinge_min_angle: bpy.props.FloatProperty(default=0.0,
                                             description="Minimum hinge angle limit")  # type: ignore
    hinge_max_angle: bpy.props.FloatProperty(default=0.0,
                                             description="Maximum hinge angle limit")  # type: ignore
    hinge_max_friction_torque: bpy.props.FloatProperty(default=0.0,
                                                       description="Maximum friction torque for hinge")  # type: ignore

    prismatic_is_limited_min: bpy.props.BoolProperty(default=False,
                                                     description="Enable minimum linear limit for prismatic")  # type: ignore
    prismatic_is_limited_max: bpy.props.BoolProperty(default=False,
                                                     description="Enable maximum linear limit for prismatic")  # type: ignore
    prismatic_min_linear_limit: bpy.props.FloatProperty(default=0.0,
                                                        description="Minimum linear limit for prismatic")  # type: ignore
    prismatic_max_linear_limit: bpy.props.FloatProperty(default=0.0,
                                                        description="Maximum linear limit for prismatic")  # type: ignore
    prismatic_max_friction_force: bpy.props.FloatProperty(default=0.0,
                                                          description="Maximum friction force for prismatic")  # type: ignore


class BGS_STARFIELD_PG_havok_rigidbody(bpy.types.PropertyGroup):
    mass: bpy.props.FloatProperty(default=80.0, name="Mass",
                                  description="Physical mass of the object")  # type: ignore
    friction: bpy.props.FloatProperty(default=0.5, name="Friction",
                                      description="Surface friction coefficient")  # type: ignore
    restitution: bpy.props.FloatProperty(
        default=0.40000000596046448, name="Restitution",
        description="Bounciness/elasticity of the object")  # type: ignore
    unyielding: bpy.props.BoolProperty(default=False, name="Unyielding",
                                       description="Makes rigidbody unyielding for keyframed animation")  # Unyielding # type: ignore
    compound: bpy.props.BoolProperty(default=False, name="Compound",
                                     description="Combine multiple colliders into compound body")   # MakeCompoundBody # type: ignore
    is_rigidbody: bpy.props.BoolProperty(default=False,
                                         description="Enable physics simulation for this object")  # type: ignore
    constraints: bpy.props.CollectionProperty(type=BGS_STARFIELD_PG_constraint,
                                              description="Physics constraints connecting rigidbodies")  # type: ignore
    has_bone_proxy: bpy.props.BoolProperty(default=False, name="Bone Proxy",
                                           description="Link rigidbody to a bone for animation control")  # type: ignore
    bone_proxy_armature: bpy.props.PointerProperty(type=bpy.types.Armature,
                                                   name="Armature",
                                                   description="Armature containing the proxy bone")  # type: ignore
    bone_proxy_name: bpy.props.StringProperty(default="", name="Bone Name",
                                              description="Name of the bone to proxy")  # type: ignore


def late_register():
    bs_plugin_data.object_assign_bgs_collider(
        bpy.props.PointerProperty(type=BGS_STARFIELD_PG_havok_collider))
    bs_plugin_data.object_assign_bgs_rigidbody(
        bpy.props.PointerProperty(type=BGS_STARFIELD_PG_havok_rigidbody))


def register():
    bpy.utils.register_class(BGS_STARFIELD_PG_havok_collider)
    bpy.utils.register_class(BGS_STARFIELD_PG_constraint)
    bpy.utils.register_class(BGS_STARFIELD_PG_havok_rigidbody)
    late_register()

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_PG_havok_collider)
    bpy.utils.unregister_class(BGS_STARFIELD_PG_constraint)
    bpy.utils.unregister_class(BGS_STARFIELD_PG_havok_rigidbody)
