import os
import bpy
import bpy.utils.previews

class Panel(bpy.types.Panel):
    """Creates a Panel in the 3D view Tools panel"""
    bl_label = "Custom Icon Preview Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        global custom_icons
        self.layout.label(text="Blender SE", icon_value=imgDir["custom_icon"].icon_id

# global variable to store icons in
custom_icons = None

def register():
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    script_path = bpy.context.space_data.text.filepath
    imgDir = os.path.join(os.path.dirname(__file__), "images")    
    imgDir.load("custom_icon", os.path.join(imgDir, "icon.gif"), 'ICON')
    bpy.utils.register_module(__name__)

def unregister():
    global custom_icons
    bpy.utils.previews.remove(custom_icons)
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()