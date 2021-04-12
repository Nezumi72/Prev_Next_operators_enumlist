bl_info = {
    "name": "Test Addon",
    "author": "Your Name Here",
    "version": (0, 0, 1),
    "blender": (2, 92, 0),
    "location": "View3D > UI > Test Panel",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "Development",
    "support": "TESTING"
}

import bpy


class TEST_PG(bpy.types.PropertyGroup):
    proplist: bpy.props.EnumProperty(
        items=(
            ("BoolProperty", "Bool", "Boolean"),
            ("BoolVectorProperty", "Bool Vector", "Boolean Vector"),
            ("FloatProperty", "Float", "Floating Point"),
            ("FloatVectorProperty", "Float Vector", "Floating Point Vector"),
            ("IntProperty", "Int", "Integer"),
            ("IntVectorProperty", "Int Vector", "Integer Vector"),
            ("PointerProperty", "Pointer", "Pointer Property"),
            ),
        name="proplist",
        description="Selectable properties to add",
        default="BoolProperty",
        )


class PROPLIST_OT_next(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "property.next"
    bl_label = "Move to next item in property list"

    def execute(self, context):
        props = context.scene.MyPropertyGroup
        print('-- PROPLIST_OT_next pressed --')
        try:
            idx = props['proplist']
        except KeyError:
            props.proplist = props.proplist
            idx = props['proplist']
        list_len = len(props.bl_rna.properties['proplist'].enum_items)
        idx += 1
        if idx == list_len:
            idx = 0
        props['proplist'] = idx
        return {'FINISHED'}


class PROPLIST_OT_prev(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "property.previous"
    bl_label = "Move to previous item in property list"

    def execute(self, context):
        props = context.scene.MyPropertyGroup
        print('-- PROPLIST_OT_prev pressed --')
        try:
            idx = props['proplist']
        except KeyError:
            props.proplist = props.proplist
            idx = props['proplist']
        list_len = len(props.bl_rna.properties['proplist'].enum_items)
        idx -= 1
        if idx < 0:
            idx = list_len-1
        props['proplist'] = idx
        return {'FINISHED'}


class VIEW3D_PT_test():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Test Panel"


class TEST_PT_sub_01(VIEW3D_PT_test, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_panel_1"
    bl_label = "Test Panel 1"

    def draw(self, context):
        props = context.scene.MyPropertyGroup
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        row = col.row()
        row.operator("property.previous", icon='TRIA_LEFT', text="")
        row.prop(props, "proplist")
        row.operator("property.next", icon='TRIA_RIGHT', text="")
        items = props.bl_rna.properties['proplist'].enum_items
        col.label(text=f"Identifier: {items[props.proplist].identifier}")
        col.label(text=f"Name: {items[props.proplist].name}")
        col.label(text=f"Description: {items[props.proplist].description}")


classes = [
        TEST_PG,
        PROPLIST_OT_prev,
        PROPLIST_OT_next,
        TEST_PT_sub_01,
        ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.MyPropertyGroup = bpy.props.PointerProperty(
            type=TEST_PG)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.MyPropertyGroup

if __name__ == "__main__":
    register()
