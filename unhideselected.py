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
    
    invert_hidden: bpy.props.BoolProperty(
        name="Invert Hidden", 
        description="Hide and unhide with the same keybind", 
        default=False,
        )
    
    def draw(self, context):
        layout = self.layout
        new_row = layout.row()
        new_row.column().prop(self, "invert_hidden")
        new_row.column().label(text="Hide and unhide with the same keybind")
        
class UnhideSelectedOperator(bpy.types.Operator):
    bl_idname = "unhideselected.unhide"
    bl_label = "Unhide Selected"
    
    def execute(self, context):
        scr = context.screen
        areas = [area for area in scr.areas if area.type == 'OUTLINER']
        regions = [region for region in areas[0].regions if region.type == 'WINDOW']
        invert_hidden = bpy.context.preferences.addons[__name__].preferences.invert_hidden
        if scr ==-1 or areas[0] == -1 or regions[0] == -1:
            return {'ERROR'}
        with context.temp_override(area=areas[0], region=regions[0], screen=scr):
            for obj in context.selected_ids:
                if invert_hidden:
                    if obj: obj.hide_set(not obj.hide_get())
                else:
                    if obj: obj.hide_set(False)
        return {'FINISHED'}
        


key_config = bpy.context.window_manager.keyconfigs.addon
if key_config:
    key_map = key_config.keymaps.new(name='3D View', space_type='VIEW_3D')
    key_entry = key_map.keymap_items.new("unhideselected.unhide",
                                        type='H',
                                        value='PRESS',
                                        shift=True,
                                        alt=True,
    )
    mode_keymap = (key_map, key_entry)
    
def register():
    bpy.utils.register_class(UnhideSelectedOperator)
    bpy.utils.register_class(UnhideSelectedPreferences)

def unregister():
    bpy.utils.unregister_class(UnhideSelectedOperator)
    bpy.utils.unregister_class(UnhideSelectedPreferences)

if __name__ == '__main__':
    register()