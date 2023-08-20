import bpy
from .gVariables import StoreData


class AutoFillGroups(bpy.types.Operator):
    """Auto Fill Groups"""
    bl_idname = "object.auto_fill_groups"
    bl_label = "Auto Fill Groups"

    def execute(self, context):
        active_object = context.active_object

        for child in active_object.children:
            if (child.name == StoreData.Hairs.value):
                context.scene.HairsGroup = child
            if (child.name == StoreData.Outfit.value):
                context.scene.OutfitGroup = child
            if (StoreData.Body.value in child.name):
                context.scene.BodyGroup = child

        return {'FINISHED'}


class CreateUI(bpy.types.Operator):
    """Create UI"""
    bl_idname = "object.create_ui"
    bl_label = "Create UI"

    def execute(self, context):
        active_object = context.active_object

        active_object[StoreData.Name.value] = active_object.name
        active_object[StoreData.Body.value] = context.scene.BodyGroup
        active_object[StoreData.Hairs.value] = context.scene.HairsGroup
        active_object[StoreData.Outfit.value] = context.scene.OutfitGroup

        return {'FINISHED'}


class DeleteUI(bpy.types.Operator):
    """Delete UI"""
    bl_idname = "object.delete_ui"
    bl_label = "Delete UI"

    def execute(self, context):
        active_object = context.active_object

        if "Name" in active_object:
            del active_object[StoreData.Name.value]
        if "Body" in active_object:
            del active_object[StoreData.Body.value]
        if "Hairs" in active_object:
            del active_object[StoreData.Hairs.value]
        if "Outfit" in active_object:
            del active_object[StoreData.Outfit.value]

        return {'FINISHED'}


class SettingsTab(bpy.types.Panel):
    bl_label = "Character UI - Settings"
    bl_idname = "A"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"
    bl_order = 10

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object
        if (active_object):
            if (active_object.get(StoreData.Name.value)):
                if (active_object.type == "ARMATURE"):

                    box = layout.box()

                    box.prop(active_object, "name", text="Name")

                else:
                    box = layout.box()
                    box.label(
                        text='You need to select armature of your character')
            else:
                box = layout.box()

                box.label(
                    text='You have no UI yet.')
                box.label(
                    text='Fill all inputs and press the button to create UI.')

                box.prop(context.scene, "HairsGroup", text="Hairs Group")
                box.prop(context.scene, "OutfitGroup", text="Hairs Group")
                box.prop(context.scene, "BodyGroup", text="Body")

                box.operator("object.auto_fill_groups", icon="EXPERIMENTAL")

                if (context.scene.HairsGroup and context.scene.OutfitGroup and context.scene.BodyGroup):
                    box.operator("object.create_ui", icon="FORWARD")


class BodyTweaks(bpy.types.Panel):
    bl_label = "Character UI - Body Tweaks"
    bl_idname = "C"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"
    bl_order = 5

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object
        Body = active_object.get(StoreData.Body.value)

        for mod in Body.modifiers:
            box = layout.box()
            row = box.row()
            row.label(text=mod.name)
            row.prop(mod, "show_viewport")
            row.prop(mod, "show_render")
            if (mod.type == "SUBSURF"):
                row = box.row()
                row.prop(mod, "levels", text="Viewport")
                row.prop(mod, "render_levels", text="Render")


class InfoTab(bpy.types.Panel):
    bl_label = "Character UI - Info"
    bl_idname = "Info_Tab"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 0

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object

        box = layout.box()

        box.label(
            text='Version: 0.0.1', icon="BLENDER")

        box.operator(
            "wm.url_open", text="Source Code").url = "https://github.com/maqq1e/DynamicBlenderCharacterUI"

        if (active_object.get(StoreData.Name.value)):
            box = layout.box()
            box.operator("object.delete_ui", icon="BACK")


UsesClasses = [
    InfoTab,
    BodyTweaks,
    SettingsTab,
    DeleteUI,
    CreateUI,
    AutoFillGroups,
]


def UsesProps():

    bpy.types.Scene.HairsGroup = bpy.props.PointerProperty(
        name="Hairs",
        type=bpy.types.Object,
    )
    bpy.types.Scene.OutfitGroup = bpy.props.PointerProperty(
        name="Outfit",
        type=bpy.types.Object,
    )
    bpy.types.Scene.BodyGroup = bpy.props.PointerProperty(
        name="Body",
        type=bpy.types.Object,
    )
