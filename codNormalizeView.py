import bpy

from mathutils import Matrix

OriginBone = "tag_view"

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

        if OriginBone in ob.data.bones:
            poseBone = ob.pose.bones[OriginBone]
            mat = ob.matrix_world * poseBone.matrix
            loc, rot, scale = mat.decompose()
            loc.x = 0
            loc.y = 0
            loc.z = 0
            locMat = Matrix.Translation(loc)
            rotMat = rot.to_matrix().to_4x4()
            scaleMat = Matrix.Scale(scale[0],4,(1,0,0)) * Matrix.Scale(scale[1],4,(0,1,0)) * Matrix.Scale(scale[2],4,(0,0,1))
            poseBone.matrix = locMat * rotMat * scaleMat

    view_layer.objects.active = oldActive

class CODNormalizeView(bpy.types.Operator):
    bl_idname = "object.cod_normalize"
    bl_label = "CoD Tools - Normalize Viewmodel Origin"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return ( not context.object is None ) and context.object.type == 'ARMATURE'

    def execute(self, context):
        run()
        return {'FINISHED'}