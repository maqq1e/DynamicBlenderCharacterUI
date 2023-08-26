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


class AddProperty(bpy.types.Operator):
    """Add Object Property"""
    bl_idname = "object.add_property"
    bl_label = "Add Property"

    def execute(self, context):
        active_object = context.active_object

        if (active_object.get(context.scene.NameProperty) == None):
            active_object[context.scene.NameProperty + "_P"] = 0

        context.scene.NameProperty = ""
        return {'FINISHED'}


class SettingsTab(bpy.types.Panel):
    bl_label = "Character UI - Settings"
    bl_idname = "OBJECT_PT_first_panel"
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
    bl_idname = "OBJECT_PT_second_panel"
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
    bl_idname = "OBJECT_PT_third_panel"
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
    bl_idname = "OBJECT_PT_forth_panel"
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


class CustomTweaks(bpy.types.Panel):
    bl_label = "Character UI - Custom Tweaks"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object

        if (active_object):
            layout.label(text="Create you own custom properties")
            # Get all object custom properties
            index = 0
            for k in active_object.keys():
                if (index == 0):
                    index = 1
                    continue
                if ("_P" not in k):
                    continue
                box = layout.box()
                row = box.row()
                row.prop(active_object, '[\"' + k + '\"]', toggle=1)
                # Create a button that opens the property editing popup
                op = row.operator("wm.properties_edit",
                                  text="", icon='SETTINGS')
                op.data_path = 'active_object'
                op.property_name = k

            box = layout.box()
            box.label(text="Create new Property")
            row = box.row()
            row.prop(context.scene, "NameProperty", text="Property Name")

            if (active_object.get(context.scene.NameProperty + "_P") == None):
                if (context.scene.NameProperty != ""):
                    box.operator("object.add_property", icon="ADD")
                else:
                    box.label(text="You need to set the name!", icon="ERROR")

            else:
                box.label(text="You need to make unique name!", icon="ERROR")

            box.label(
                text="You property must contain '_P' postfix. This postfix will add automaticly.", icon="QUESTION")


class InfoTab(bpy.types.Panel):
    bl_label = "Character UI - Info"
    bl_idname = "OBJECT_PT_fifth_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CharacterUI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        active_object = context.active_object

        box = layout.box()

        box.label(
            text='Version: 0.1.3', icon="BLENDER")

        box.operator(
            "wm.url_open", text="Source Code and Docs", icon="DOCUMENTS").url = "https://github.com/maqq1e/DynamicBlenderCharacterUI"

        if (active_object):
            if (active_object.get(StoreData.Name.value)):
                box = layout.box()
                box.operator("object.delete_ui", icon="BACK")


UsesClasses = [
    DeleteUI,
    CreateUI,
    AutoFillGroups,
    AddProperty,
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
    bpy.types.Scene.NameProperty = bpy.props.StringProperty(
        name="Name of Property",
        default=""
    )
