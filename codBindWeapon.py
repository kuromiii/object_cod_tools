import bpy

# Tags to attach
GUN_PARENT_TAGS = {
    "tag_weapon":"tag_weapon_right",
    "tag_weapon1":"tag_weapon_left",
    "tag_clip":"j_gun",
    "tag_clip":"tag_weapon",
    "tag_knife":"tag_knife_attach"
}

GUN_PARENT_TAGS_JGUN = {
    "j_gun":"tag_weapon",
    "j_gun1":"tag_weapon1",
    "tag_clip":"j_gun",
    "tag_clip1":"j_gun1"
}

GUN_ORIGIN_TAGS = [
    "j_gun",
    "j_gun1",
    "tag_weapon_right",
    "tag_weapon_left",
    "tag_weapon",
    "tag_knife"
]

def apply_armature(ob, remake):
    view_layer = bpy.context.view_layer
    oldAct = view_layer.objects.active

    for obj in bpy.context.scene.objects:
        oldSel = obj.select
        obj.select = True
        view_layer.objects.active = obj

        for mod in obj.modifiers:
            if mod.type == "ARMATURE" and mod.object == ob:
                bpy.ops.object.modifier_apply(modifier = mod.name)
                if remake:
                    obj.modifiers.new(name = 'Skeleton', type = 'ARMATURE')
                    if 'Skeleton' in obj.modifiers:
                        obj.modifiers['Skeleton'].object = ob

        obj.select = oldSel
    
    view_layer.objects.active = oldAct

def weapon_bind(ob):
    view_layer = bpy.context.view_layer
    view_layer.objects.active = ob
    ob.select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    targetAr = GUN_PARENT_TAGS

    if "j_gun" in ob.data.bones:
        targetAr = GUN_PARENT_TAGS_JGUN
        print("using j_gun type parents for " + ob.name)

    for boneTarget, boneParTarget in targetAr.items():
        if boneTarget in ob.data.edit_bones and boneParTarget in ob.data.edit_bones:
            ob.data.edit_bones[boneTarget].parent = ob.data.edit_bones[boneParTarget]

    bpy.ops.object.mode_set(mode = 'POSE')

    for boneName in GUN_ORIGIN_TAGS:
        if boneName in ob.pose.bones:

            poseBone = ob.pose.bones[boneName]

            if not poseBone.parent is None:
                nc = poseBone.constraints.new(type='COPY_ROTATION')
                nc.target = ob
                nc.subtarget = poseBone.parent.name
                nc.influence = 1
                nc.name = "bindRot"

                nc2 = poseBone.constraints.new(type='COPY_LOCATION')
                nc2.target = ob
                nc2.subtarget = poseBone.parent.name
                nc2.influence = 1
                nc2.name = "bindPos"

    apply_armature(ob, True)

    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode = 'POSE')

    for poseBone in ob.pose.bones:
        for const in poseBone.constraints:
            if nc.name == "bindRot" or nc.name == "bindPos":
                poseBone.constraints.remove(const)

def run():
    view_layer = bpy.context.view_layer
    oldActive = view_layer.objects.active

    for ob in bpy.data.objects:
        if ob.type != 'ARMATURE':
            continue

        if not ob.select:
            continue

        view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode='POSE')
        weapon_bind(ob)

    view_layer.objects.active = oldActive


class CODBindWeapon(bpy.types.Operator):
    bl_idname = "object.cod_bind"
    bl_label = "CoD Tools - Bind Weapon Bones"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return ( not context.object is None ) and context.object.type == 'ARMATURE'

    def execute(self, context):
        run()
        return {'FINISHED'}