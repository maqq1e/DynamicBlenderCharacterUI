import bpy
from .main import UsesClasses, UsesProps

# Addon Info
bl_info = {
    "name": "Dynamic Character UI",
    "author": "daniel.hovach@gmail.com",
    "description": "Simply create UI for your characters",
    "blender": (3, 5, 0),
    "version": (0, 1, 3),
}


# Register Classes
def register():
    UsesProps()

    bpy.utils.register_class(UsesClasses[0])
    bpy.utils.register_class(UsesClasses[1])
    bpy.utils.register_class(UsesClasses[2])
    bpy.utils.register_class(UsesClasses[3])
    bpy.utils.register_class(UsesClasses[4])
    bpy.utils.register_class(UsesClasses[5])
    bpy.utils.register_class(UsesClasses[6])
    bpy.utils.register_class(UsesClasses[7])


def unregister():

    bpy.utils.unregister_class(UsesClasses[0])
    bpy.utils.unregister_class(UsesClasses[1])
    bpy.utils.unregister_class(UsesClasses[2])
    bpy.utils.unregister_class(UsesClasses[3])
    bpy.utils.unregister_class(UsesClasses[4])
    bpy.utils.unregister_class(UsesClasses[5])
    bpy.utils.unregister_class(UsesClasses[6])
    bpy.utils.unregister_class(UsesClasses[7])


if __name__ == "__main__":
    register()
