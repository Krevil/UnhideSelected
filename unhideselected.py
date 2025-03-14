bl_info = {
    "name": "Unhide Selected",
    "description": "Unhide selected objects in the outliner with a keybind",
    "author": "Krevil",
    "version": (1, 0, 0),
    "blender": (4, 1, 0),
    "location": "3D View - Objects",
    "category": "Interface",
}

import bpy
 

class UnhideSelectedPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    invert_visibility: bpy.props.BoolProperty(
        name="Invert Visibility", 
        description="Invert the visibility of objects when using the keybind", 
        default=True,
        )
    
    def draw(self, context):
        layout = self.layout
        new_row = layout.row()
        new_row.column().prop(self, "invert_visibility")
        long_column = new_row.column()
        long_column.label(text="Invert the visibility of objects when using the keybind")
        long_column.scale_x = 1.65
        
class UnhideSelectedOperator(bpy.types.Operator):
    bl_idname = "unhideselected.unhide"
    bl_label = "Unhide Selected"
    
    def execute(self, context):
        scr = context.screen
        areas = [area for area in scr.areas if area.type == 'OUTLINER']
        regions = [region for region in areas[0].regions if region.type == 'WINDOW']
        invert_visibility = bpy.context.preferences.addons[__name__].preferences.invert_visibility
        if scr ==-1 or areas[0] == -1 or regions[0] == -1:
            return {'CANCELLED'}
        with context.temp_override(area=areas[0], region=regions[0], screen=scr):
            for obj in context.selected_ids:
                if obj:
                    if not hasattr(obj, 'hide_set'):
                        continue
                    if invert_visibility:
                        obj.hide_set(not obj.hide_get())
                    else:
                        obj.hide_set(False)
        return {'FINISHED'}
  
addon_keymaps = []
  
def addbinding():
    key_config = bpy.context.window_manager.keyconfigs.addon
    if key_config:
        km = key_config.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("unhideselected.unhide",
                                            type='H',
                                            value='PRESS',
                                            shift=True,
                                            alt=True,
        )
        addon_keymaps.append((km, kmi))

def removebinding():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
        

def register():
    bpy.utils.register_class(UnhideSelectedOperator)
    bpy.utils.register_class(UnhideSelectedPreferences)
    addbinding()

def unregister():
    bpy.utils.unregister_class(UnhideSelectedOperator)
    bpy.utils.unregister_class(UnhideSelectedPreferences)
    removebinding()

if __name__ == '__main__':
    register()