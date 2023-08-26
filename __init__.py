import bpy
from .main import *

# Addon Info
bl_info = {
    "name": "Dynamic Character UI",
    "author": "daniel.hovach@gmail.com",
    "description": "Simply create UI for your characters",
    "blender": (3, 5, 0),
    "version": (0, 2, 1),
}


# Register Classes
def register():
    UsesProps()

    bpy.utils.register_class(SettingsTab)
    bpy.utils.register_class(BodyTweaks)
    bpy.utils.register_class(OutfitTweaks)
    bpy.utils.register_class(HairsTweaks)
    bpy.utils.register_class(CustomTweaks)
    bpy.utils.register_class(InfoTab)

    for useClass in UsesClasses:
        bpy.utils.register_class(useClass)


def unregister():

    bpy.utils.unregister_class(SettingsTab)
    bpy.utils.unregister_class(BodyTweaks)
    bpy.utils.unregister_class(OutfitTweaks)
    bpy.utils.unregister_class(HairsTweaks)
    bpy.utils.unregister_class(CustomTweaks)
    bpy.utils.unregister_class(InfoTab)

    for useClass in UsesClasses:
        bpy.utils.unregister_class(useClass)


if __name__ == "__main__":
    register()
