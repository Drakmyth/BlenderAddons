bl_info = {
    "name": "Unreal Animation FBX",
    "description": "Exports NLA tracks as individual FBX files for Unreal Engine 4",
    "author": "Shaun Hamman",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "NLA Editor",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "TESTING",
    "category": "Import-Export"
}

import bpy

class UnrealAnimationExporter(bpy.types.Operator):
    """Export NLA tracks as individual FBX files"""
    bl_idname = "export_scene.unreal_nla"
    bl_label = "Export NLA Tracks to Unreal FBX"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        nla_tracks = context.active_object.animation_data.nla_tracks
        initial_track_state = {}
        
        selected_tracks = [track for track in nla_tracks if track.select]
        
        for track in nla_tracks:
            print(dir(track))
            print(track.is_solo)
            initial_track_state[track.name] = {
                'is_solo': track.is_solo,
                'mute': track.mute,
                'select': track.select
            }
            
            track.is_solo = False
            track.mute = True
            track.select = False
        
        orig_frame_end = context.scene.frame_end
        
        for track in selected_tracks:
            track.select = True
            track.mute = False
            
            context.scene.frame_end = track.strips[-1].frame_end
            
            file = '{base}_Anim_{name}'.format(base=bpy.path.basename(bpy.data.filepath)[:-6],
                                               name=track.name)
            filepath = '{path}{file}.fbx'.format(path=bpy.path.abspath('//'),
                                                 file=file)
            
            bpy.ops.export_scene.fbx(filepath=filepath,
                                     check_existing=False,
                                     axis_forward='X',
                                     axis_up='Z',
                                     version='BIN7400',
                                     ui_tab='MAIN',
                                     use_selection=True,
                                     global_scale=1.00,
                                     apply_unit_scale=True,
                                     bake_space_transform=True,
                                     object_types={'ARMATURE'},
                                     use_mesh_modifiers=True,
                                     mesh_smooth_type='FACE',
                                     use_mesh_edges=False,
                                     use_tspace=False,
                                     use_custom_props=False,
                                     add_leaf_bones=False,
                                     primary_bone_axis='Y',
                                     secondary_bone_axis='X',
                                     use_armature_deform_only=False,
                                     armature_nodetype='NULL',
                                     bake_anim=True,
                                     bake_anim_use_all_bones=True,
                                     bake_anim_use_nla_strips=False,
                                     bake_anim_use_all_actions=False,
                                     bake_anim_force_startend_keying=True,
                                     bake_anim_step=1.00,
                                     bake_anim_simplify_factor=1.00,
                                     use_anim=True,
                                     use_anim_action_all=True,
                                     use_default_take=True,
                                     use_anim_optimize=True,
                                     anim_optimize_precision=6.00,
                                     path_mode='AUTO',
                                     embed_textures=False,
                                     batch_mode='OFF',
                                     use_batch_own_dir=True
                                     )

            track.mute = True
            track.select = False
            
        context.scene.frame_end = orig_frame_end
        for track in nla_tracks:
            orig = initial_track_state[track.name]
            track.is_solo = orig['is_solo']
            track.mute = orig['mute']
            track.select = orig['select']
            
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(UnrealAnimationExporter)
    
def unregister():
    bpy.utils.unregister_class(UnrealAnimationExporter)

if __name__ == "__main__":
    register()