bl_info = {
    "name" : "Ice-Hail Collision Info",
    "author" : "kreny",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
}

import bpy
import re
from enum import Enum


class Materials(Enum):
    Undefined=0
    Soil=1
    Stone=2
    Sand=3
    Metal=4
    WireNet=5
    Grass=6
    Wood=7
    Water=8
    Snow=9
    Ice=10
    Lava=11
    Bog=12
    HeavySand=13
    Cloth=14
    Glass=15
    Bone=16
    Rope=17
    CharControl=18
    Ragdoll=19
    Surfing=20
    GuardianFoot=21
    HeavySnow=22
    Unused0=23
    LaunchPad=24
    Conveyer=25
    Rail=26
    Grudge=27
    Meat=28
    Vegetable=29
    Bomb=30
    MagicBall=31
    Barrier=32
    AirWall=33
    Misc=34
    GrudgeSlow=35


submaterials = {
    "Barrier": {
        "HolyWall": 1,
    },
    "Bone": {
        "Pile": 1,
    },
    "Cloth": {
        "Carpet": 1,
        "Leather": 2,
    },
    "Grass": {
        "Short": 1,
        "Unknown0": 2,
        "WithMud": 3,
        "Unknown1": 4,
        "Straw": 5,
        "Thatch": 6,
    },
    "Ice": {
        "Unknown": 1,
        "Hard": 2,
    },
    "Metal": {
        "Light": 1,
    },
    "Sand": {
        "Shallow": 1,
    },
    "Snow": {
        "Shallow": 1,
    },
    "Soil": {
        "Soft": 1,
        "Hard": 2,
    },
    "Stone": {
        "Light": 1,
        "Heavy": 2,
        "Marble": 3,
        "DgnLight": 4,
        "DgnHeavy": 5,
    },
    "Water": {
        "Unknown0": 1,
        "Unknown1": 2,
        "Unknown2": 3,
        "StoneBottom": 4
    },
    "Wood": {
        "Thin": 1,
        "Thick": 2,
    },
}


class Wallcodes(Enum):
    Null=0
    NoClimb=1
    Hang=2
    LadderUp=3
    Ladder=4
    Slip=5
    LadderSide=6
    NoSlipRain=7
    NoDashUpAndNoClimb=8
    IceMakerBlock=9


class Floorcodes(Enum):
    Null=0
    Return=1
    FlowStraight=2
    FlowLeft=3
    FlowRight=4
    Slip=5
    NarrowPlace=6
    TopBroadleafTree=7
    TopConiferousTree=8
    Fall=9
    Attach=10
    NoImpulseUpperMove=11
    NoPreventFall=12


class IceHailCI(bpy.types.Operator):
    bl_idname = "view3d.icehailci"
    bl_label = "Ice-Hail Collision Info Editor"
    bl_description = "Edit collision info (material, filters, etc.)"


    def materials_callback(self, context):
        return (tuple((m.name, m.name, "") for m in Materials))


    def submaterials_callback(self, context):
        mat = submaterials.get(self.material)

        if not mat:
            submats = ()
        else:
            submats = (tuple((str(v), k, "") for k,v in mat.items()))

        return (("0", "Default", "",),)+submats

    def wallcodes_callback(self, context):
        return (tuple((w.name, w.name, "") for w in Wallcodes))

    def floorcodes_callback(self, context):
        return (tuple((f.name, f.name, "") for f in Floorcodes))

    extrafilterik: bpy.props.BoolProperty(
        name="ExtraFilterIK",
        description="",
        default=False,
    )

    filter_player: bpy.props.BoolProperty(
        name="Player",
        description="",
        default=False,
    )

    filter_animal: bpy.props.BoolProperty(
        name="Animal",
        description="",
        default=False,
    )

    filter_npc: bpy.props.BoolProperty(
        name="NPC",
        description="",
        default=False,
    )

    filter_camera: bpy.props.BoolProperty(
        name="Camera",
        description="",
        default=False,
    )

    filter_attackhitplayer: bpy.props.BoolProperty(
        name="AttackHitPlayer",
        description="",
        default=False,
    )
    filter_attackhitenemy: bpy.props.BoolProperty(
        name="AttackHitEnemy",
        description="",
        default=False,
    )

    filter_arrow: bpy.props.BoolProperty(
        name="Arrow",
        description="",
        default=False,
    )

    filter_bomb: bpy.props.BoolProperty(
        name="Bomb",
        description="",
        default=False,
    )

    filter_magnet: bpy.props.BoolProperty(
        name="Magnet",
        description="",
        default=False,
    )

    filter_camerabody: bpy.props.BoolProperty(
        name="ameraBody",
        description="",
        default=False,
    )

    filter_ik: bpy.props.BoolProperty(
        name="IK",
        description="",
        default=False,
    )

    filter_grudge: bpy.props.BoolProperty(
        name="Grudge",
        description="",
        default=False,
    )

    filter_movingtrolley: bpy.props.BoolProperty(
        name="MovingTrolley",
        description="",
        default=False,
    )

    filter_lineofsight: bpy.props.BoolProperty(
        name="LineOfSight",
        description="",
        default=False,
    )

    filter_giant: bpy.props.BoolProperty(
        name="Giant",
        description="",
        default=False,
    )

    filter_hitall: bpy.props.BoolProperty(
        name="HitAll",
        description="",
        default=False,
    )

    filter_ignore: bpy.props.BoolProperty(
        name="Ignore",
        description="",
        default=False,
    )

    material: bpy.props.EnumProperty(
        name="Material",
        description="Material of the object",
        items=materials_callback,
    )

    submaterial: bpy.props.EnumProperty(
        name="Submaterial",
        description="Submaterial of the object",
        items=submaterials_callback,
    )

    wallcode: bpy.props.EnumProperty(
        name="Wall code",
        description="Wall code of the object",
        items=wallcodes_callback,
    )

    floorcode: bpy.props.EnumProperty(
        name="Floor code",
        description="Floor code of the object",
        items=floorcodes_callback,
    )

    def execute(self, context):
        try:
            selected_objs = bpy.context.selected_objects
            if not selected_objs:
                self.report({"ERROR"}, "No objects selected")
                return {"CANCELLED"}

            collisionFilterInfo = 0x90000000|self.extrafilterik|\
            (self.filter_player<<8)|(self.filter_animal<<9)|(self.filter_npc<<10)|\
            (self.filter_camera<<11)|(self.filter_attackhitplayer<<12)|\
            (self.filter_attackhitenemy<<13)|(self.filter_arrow<<14)|(self.filter_bomb<<15)|\
            (self.filter_magnet<<16)|(self.filter_camerabody<<17)|(self.filter_ik<<18)|\
            (self.filter_grudge<<19)|(self.filter_movingtrolley<<20)|(self.filter_lineofsight<<21)|\
            (self.filter_giant<<22)|(self.filter_hitall<<23)|(self.filter_ignore<<24)

            material = getattr(Materials, self.material).value
            submaterial = int(self.submaterial)
            wallcode = getattr(Wallcodes, self.wallcode).value
            floorcode = getattr(Floorcodes, self.floorcode).value

            userData = material | submaterial<<6 | floorcode<<10 | wallcode<<15

            for obj in selected_objs:
                obj.name = re.sub("\s\[0x[a-zA-Z0-9]+\]", "", obj.name)
                obj.name = f"{obj.name} [0x{collisionFilterInfo:08X}] [0x{userData:08X}]"

            return {"FINISHED"}

        except Exception as e:
            print(e)
            self.report({"ERROR"}, f"{e}")
            return {"CANCELLED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()

        col.prop(self, "extrafilterik")
        col.prop(self, "filter_player")
        col.prop(self, "filter_animal")
        col.prop(self, "filter_npc")
        col.prop(self, "filter_camera")
        col.prop(self, "filter_attackhitplayer")
        col.prop(self, "filter_attackhitenemy")
        col.prop(self, "filter_arrow")
        col.prop(self, "filter_bomb")
        col.prop(self, "filter_magnet")
        col.prop(self, "filter_camerabody")
        col.prop(self, "filter_ik")
        col.prop(self, "filter_grudge")
        col.prop(self, "filter_movingtrolley")
        col.prop(self, "filter_lineofsight")
        col.prop(self, "filter_giant")
        col.prop(self, "filter_hitall")
        col.prop(self, "filter_ignore")


        col = row.column()

        col.prop(self, "material")
        col.prop(self, "submaterial")
        col.prop(self, "wallcode")
        col.prop(self, "floorcode")


classes = (IceHailCI,)


rgstr, unrgstr = bpy.utils.register_classes_factory(classes)


def register():
    rgstr()


def unregister():
    unrgstr()


if __name__ == "__main__":
    register()

