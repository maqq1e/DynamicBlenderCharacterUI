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

        # Add drivers for hair objects
        Hairs = context.scene.HairsGroup

        for group in Hairs.children:
            if (group.get('isHide') == None):
                group['isHide'] = 0
            for child in group.children:
                hide_viewport = child.driver_add("hide_viewport")
                hide_render = child.driver_add("hide_render")

                hide_viewport.driver.variables.new()
                hide_viewport.driver.expression = "var"
                var = hide_viewport.driver.variables.get("var")
                var.targets[0].id = group
                var.targets[0].data_path = '[\"isHide\"]'

                hide_render.driver.variables.new()
                hide_render.driver.expression = "var"
                var = hide_render.driver.variables.get("var")
                var.targets[0].id = group
                var.targets[0].data_path = '[\"isHide\"]'

        return {'FINISHED'}


class DeleteUI(bpy.types.Operator):
    """Delete UI"""
    bl_idname = "object.delete_ui"
    bl_label = "Delete UI"

    def execute(self, context):
        active_object = context.active_object

        # Delete drivers for hair objects
        Hairs = active_object[StoreData.Hairs.value]

        for group in Hairs.children:
            for child in group.children:
                child.driver_remove("hide_viewport")
                child.driver_remove("hide_render")

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
    bl_idname = "TWEAKS_PT_4"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"

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
    bl_idname = "TWEAKS_PT_3"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object
        if (active_object):
            if (active_object.get(StoreData.Name.value)):
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


class OutfitTweaks(bpy.types.Panel):
    bl_label = "Character UI - Outfit Tweaks"
    bl_idname = "TWEAKS_PT_2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object

        if (active_object):
            if (active_object.get(StoreData.Name.value)):
                Outfit = active_object.get(StoreData.Outfit.value)

                for group in Outfit.children:
                    box = layout.box()
                    box.label(text=group.name)
                    for child in group.children:
                        row = box.row()
                        row.label(text=child.name)
                        row.prop(child, "hide_viewport",
                                 text="Viewport", invert_checkbox=True)
                        row.prop(child, "hide_render",
                                 text="Render", invert_checkbox=True)


class HairsTweaks(bpy.types.Panel):
    bl_label = "Character UI - Hairs Tweaks"
    bl_idname = "TWEAKS_PT_1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object

        if (active_object):
            if (active_object.get(StoreData.Name.value)):
                hairs = active_object.get(StoreData.Hairs.value)

                for group in hairs.children:
                    box = layout.box()
                    row = box.row()
                    row.label(text=group.name)
                    row.prop(group, '[\"isHide\"]',
                             text="Hide", toggle=1)


class InfoTab(bpy.types.Panel):
    bl_label = "Character UI - Info"
    bl_idname = "INFO_TAB_PT_info_tab"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object

        box = layout.box()

        box.label(
            text='Version: 0.0.1', icon="BLENDER")

        box.operator(
            "wm.url_open", text="Source Code").url = "https://github.com/maqq1e/DynamicBlenderCharacterUI"

        if (active_object):
            if (active_object.get(StoreData.Name.value)):
                box = layout.box()
                box.operator("object.delete_ui", icon="BACK")


UsesClasses = [
    InfoTab,
    HairsTweaks,
    OutfitTweaks,
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
