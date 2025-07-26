import bpy

def bone_merge(src, trg):
    for bone in src.pose.bones:
        if bone.name in trg.pose.bones:
            nc = bone.constraints.new(type = 'COPY_ROTATION')
            nc.target = trg
            nc.subtarget = bone.name
            nc.influence = 1

            nc2 = bone.constraints.new(type = 'COPY_LOCATION')
            nc2.target = trg
            nc2.subtarget = bone.name
            nc2.influence = 1

def apply_pose(obj):
    view_layer = bpy.context.view_layer
    oldAct = view_layer.objects.active
    view_layer.objects.active = obj
    obj.select = True
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    obj.select = False
    view_layer.objects.active = oldAct

def reparent_armature_children(src, trg):
    view_layer = bpy.context.view_layer
    oldAct = view_layer.objects.active

    for obj in bpy.context.scene.objects:
        oldSel = obj.select
        obj.select = True
        view_layer.objects.active = obj

        for mod in obj.modifiers:
            if mod.type == "ARMATURE" and mod.object == src:
                bpy.ops.object.modifier_apply(modifier = mod.name )

                if not (trg is None):
                    obj.modifiers.new(name = 'Skeleton', type = 'ARMATURE')
                    if 'Skeleton' in obj.modifiers:
                        obj.modifiers['Skeleton'].object = trg
        
        obj.select = oldSel
    
    view_layer.objects.active = oldAct

def merge_armature(src,trg):
    view_layer = bpy.context.view_layer
    parents = {}
    oldAct = view_layer.objects.active
    view_layer.objects.active = src
    src.select = True

    bpy.ops.object.mode_set(mode='EDIT')

    for bone in src.data.edit_bones:
        if not (bone.parent is None):
            parents[bone.name] = bone.parent.name

    for bone in src.data.edit_bones:
        if bone.name in trg.data.bones:
            src.data.edit_bones.remove(bone)

    bpy.ops.object.mode_set(mode='OBJECT')

    view_layer.objects.active = trg
    trg.select = True
    bpy.ops.object.join()

    bpy.ops.object.mode_set(mode = 'EDIT')

    for boneName, boneParentName in parents.items():
        if boneName in trg.data.edit_bones and boneParentName in trg.data.edit_bones:
            bone = trg.data.edit_bones[boneName]
            if bone.parent is None:
                bone.parent = trg.data.edit_bones[boneParentName]

    bpy.ops.object.mode_set(mode = 'POSE')
    view_layer.objects.active = oldAct

def run(reqSelected):
    bpy.ops.object.mode_set(mode = 'POSE')
    view_layer = bpy.context.view_layer
    rootSkel = view_layer.objects.active

    for ob in bpy.data.objects:
        if ob.type != 'ARMATURE':
            continue

        if ob == rootSkel:
            continue

        if reqSelected and not ob.select:
            continue

        bone_merge(ob, rootSkel)
        reparent_armature_children(ob, rootSkel)
        apply_pose(ob)
        merge_armature(ob, rootSkel)

class CODAssembleWeapon(bpy.types.Operator):
    bl_idname = "object.cod_assemble"
    bl_label = "CoD Tools - Assemble Weapon Bones"
    bl_options = {'REGISTER', 'UNDO'}

    requireSelected: bpy.props.BoolProperty(
        name = "Require Selected", 
        description = "Require armature to be selected in order to assemble?", 
        default = False, 
        subtype = 'NONE'
    )
    
    @classmethod
    def poll(cls, context):
        return ( not context.object is None ) and context.object.type == 'ARMATURE'

    def execute(self, context):
        run( self.requireSelected )
        return {'FINISHED'}