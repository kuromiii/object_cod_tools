bl_info = {
    "name": "CoD Tools",
    "author": "Grey Ruessler, updated by kuromiii",
    "version": (1, 0, 0),
    "blender": (4, 4, 0),
    "location": "Search > CoD Tools",
    "description": "Assemble, Bind, and Rename Bones for viewmodels ripped from the Call of Duty series",
    "category": "Object",
}

from .codAssembleWeapon import CODAssembleWeapon
from .codBindWeapon import CODBindWeapon
from .codNormalizeView import CODNormalizeView
from .codRenameBones import CODRenameBones

classes = (
    CODAssembleWeapon,
    CODBindWeapon,
    CODNormalizeView,
    CODRenameBones,
)

import bpy

class CODToolsCombinedOperator(bpy.types.Operator):
    bl_idname = "object.cod_combined"
    bl_label = "CoD Tools - EZ Fix"
    bl_options = {'REGISTER', 'UNDO'}
    
    doAssemble: bpy.props.BoolProperty(
        name = "Assemble Parts", 
        description = "Assemble armatures together.", 
        default = True, 
        subtype = 'NONE'
    )
    doRename: bpy.props.BoolProperty(
        name = "Rename Bones", 
        description = "Rename bones from j_gun to tag_weapon, etc.", 
        default = True, 
        subtype = 'NONE'
    )
    doBind: bpy.props.BoolProperty(
        name = "Bind Weapon", 
        description = "Bind weapon to hand reposition.", 
        default = True, 
        subtype = 'NONE'
    )
    doNormalize: bpy.props.BoolProperty(
        name = "Normalize View", 
        description = "Move gun to view position.", 
        default = True, 
        subtype = 'NONE'
    )

    @classmethod    
    def poll(cls, context):
        return ( not context.object is None ) and context.object.type == 'ARMATURE'

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "doAssemble", text="Assemble armatures together.")
        row.prop(self, "doRename", text="Rename bones from j_gun to tag_weapon, etc.")
        row.prop(self, "doBind", text="Bind weapon to hand reposition.")
        row.prop(self, "doNormalize", text="Move gun to view position.")

    def execute(self, context):
        if self.doAssemble:
            bpy.ops.object.cod_assemble()
        if self.doRename:
            bpy.ops.object.cod_rename()
        if self.doBind:
            bpy.ops.object.cod_bind()
        if self.doNormalize:
            bpy.ops.object.cod_normalize()
        return {'FINISHED'}

class CODToolsMenu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_pose_cod_tools"
    bl_label = "CoD Tools"
    
    @classmethod
    def poll(cls, context):
        return ( not context.object is None ) and context.object.type == 'ARMATURE'

    def draw(self, context):
        self.layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.operator("object.cod_combined", text = "EZ Fix")
        self.layout.operator("object.cod_assemble", text = "Assemble Weapon")
        self.layout.operator("object.cod_bind", text = "Bind Weapon")
        self.layout.operator("object.cod_rename", text = "Rename Weapon Bones")
        self.layout.operator("object.cod_normalize", text = "Normalise Viewmodel Origin")

def menu_func(self, context):
    self.layout.menu(CODToolsMenu.bl_idname)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_class(CODToolsMenu)
    bpy.utils.register_class(CODToolsCombinedOperator)
    bpy.types.VIEW3D_MT_pose.append(menu_func)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_pose.remove(menu_func)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(CODToolsCombinedOperator)
    bpy.utils.unregister_class(CODToolsMenu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
