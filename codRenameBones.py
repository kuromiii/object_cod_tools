import bpy

RENAME_DICTONARY = {
    ("tag_weapon", "tag_torso") : "tag_weapon_right",
    ("tag_weapon1", "tag_torso") : "tag_weapon_left",
    ("j_gun", None) : "tag_weapon",
    ("j_gun1", None) : "tag_weapon_le",
    ("tag_flash1", "j_gun1") : "tag_flash_le",
    ("tag_brass1", None) : "tag_brass_le"
}

CODWW2Flag = "j_clavicle_ri"

def run():
    view_layer = bpy.context.view_layer
    oldActive = view_layer.objects.active

    for ob in bpy.data.objects:
        if ob.type != 'ARMATURE':
            continue

        if not ob.select:
            continue

        view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode = 'POSE')

        if CODWW2Flag in ob.data.bones:
            print("CoD WW2 Rig Detected; skipping " + ob.name)
        else:
            for boneOb in ob.data.bones:
                for potjoints, new_name in RENAME_DICTONARY.items():
                    # Found one
                    if boneOb.name == potjoints[0]:
                        # Check if it's a child bone of what we want, None to rename regardless.
                        if potjoints[1] is None or ( not ( boneOb.parent is None ) and potjoints[1] == boneOb.parent.name ):
                            boneOb.name = new_name

    view_layer.objects.active = oldActive

class CODRenameBones(bpy.types.Operator):
    bl_idname = "object.cod_rename"
    bl_label = "CoD Tools - Rename Weapon Bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return ( not context.object is None ) and context.object.type == 'ARMATURE'

    def execute(self, context):
        run()
        return {'FINISHED'}