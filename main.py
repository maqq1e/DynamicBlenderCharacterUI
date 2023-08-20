import bpy


class AutoFillGroups(bpy.types.Operator):
    """Auto Fill Groups"""
    bl_idname = "object.auto_fill_groups"
    bl_label = "Auto Fill Groups"

    def execute(self, context):
        active_object = context.active_object

        for child in active_object.children:
            if (child.name == "Hairs"):
                context.scene.HairsGroup = child
            if (child.name == "Outfit"):
                context.scene.OutfitGroup = child
            if ("Body" in child.name):
                context.scene.BodyGroup = child

        return {'FINISHED'}


class CreateUI(bpy.types.Operator):
    """Create UI"""
    bl_idname = "object.create_ui"
    bl_label = "Create UI"

    def execute(self, context):
        active_object = context.active_object

        active_object['Name'] = active_object.name
        active_object['Body'] = context.scene.BodyGroup
        active_object['Hairs'] = context.scene.HairsGroup
        active_object['Outfit'] = context.scene.OutfitGroup

        return {'FINISHED'}


class DeleteUI(bpy.types.Operator):
    """Delete UI"""
    bl_idname = "object.delete_ui"
    bl_label = "Delete UI"

    def execute(self, context):
        active_object = context.active_object

        if "Name" in active_object:
            del active_object["Name"]
        if "Body" in active_object:
            del active_object["Body"]
        if "Hairs" in active_object:
            del active_object["Hairs"]
        if "Outfit" in active_object:
            del active_object["Outfit"]

        return {'FINISHED'}


class SettingsTab(bpy.types.Panel):
    bl_label = "Character UI - Settings"
    bl_idname = "OBJECT_PT_character_ui_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object
        if (active_object):
            if (active_object.get("Name")):
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


class InfoTab(bpy.types.Panel):
    bl_label = "Character UI - Info"
    bl_idname = "OBJECT_PT_character_ui_info"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object

        box = layout.box()

        box.label(
            text='Version: 0.0.1', icon="BLENDER")

        box.operator(
            "wm.url_open", text="Source Code").url = "https://github.com/maqq1e/DynamicBlenderCharacterUI"

        if (active_object.get("Name")):
            box = layout.box()
            box.operator("object.delete_ui", icon="BACK")


UsesClasses = [
    DeleteUI,
    CreateUI,
    AutoFillGroups,
    SettingsTab,
    InfoTab,
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
