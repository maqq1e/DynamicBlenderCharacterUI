import bpy
from .main import UsesClasses, UsesProps

# Addon Info
bl_info = {
    "name": "Dynamic Character UI",
    "author": "daniel.hovach@gmail.com",
    "description": "Simply create UI for your characters",
    "blender": (3, 5, 0),
    "version": (0, 1, 2),
}


# Register Classes
def register():
    UsesProps()

    for useClass in UsesClasses:
        bpy.utils.register_class(useClass)


def unregister():
    for useClass in UsesClasses:
        bpy.utils.unregister_class(useClass)


if __name__ == "__main__":
    register()
