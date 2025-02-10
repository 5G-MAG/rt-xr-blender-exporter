import bpy

################################################################################################
# MPEG_anchor model
    ################################################################################################

# List of anchoring types for the dropdown
XR_TRACKABLE_TYPES = [
    ('TRACKABLE_FLOOR', "Floor", "Anchor to the floor"),
    ('TRACKABLE_VIEWER', "Viewer", "Anchor to the viewer (1st person)"),
    ('TRACKABLE_CONTROLLER', 'Controller', 'Anchor to the controller path'),
    ('TRACKABLE_PLANE', "Plane", "Anchor to a plane"),
    ('TRACKABLE_MARKER_2D', "2D Marker", "Anchor to a 2D marker"),
    ('TRACKABLE_MARKER_3D', "3D Marker", "Anchor to a 3D marker"),
    ('TRACKABLE_MARKER_GEO', "GeoCoord", "Anchor using geographic coordinates"),
    ('TRACKABLE_APPLICATION', "Application", "Application specific")
]

TRACKABLE_GEOMETRIC_CONSTRAINT = [
    ('HORIZONTAL_PLANE', 'Horizontal', 'Horizontal'),
    ('VERTICAL_PLANE', 'Vertical', 'Vertical')
]


def update_trackable_type(self, context):
    # Find and assign the trackable from scene.xr_trackables by name
    name = '_'.join(self.type.split('_')[0:]).lower()
    if not self.type in ('TRACKABLE_FLOOR', 'TRACKABLE_VIEWER'):
        count = 0
        for trackable in context.scene.xr_trackables:
            if trackable.type == self.type:
                count +=1
        name = f'{name}_{count}'
    self.name = name
    
class XRTrackableObjectProperty(bpy.types.PropertyGroup):

    type: bpy.props.EnumProperty(items=XR_TRACKABLE_TYPES, update=update_trackable_type)

    # TRACKABLE_FLOOR
    # TRACKABLE_VIEWER
    # - no additional properties -

    # TRACKABLE_CONTROLLER
    path: bpy.props.StringProperty(
        name="Path", 
        description="A path that describes the action space as specified by the OpenXR specification in clause 6.2. An example is '/user/hand/left/input'."
    )

    # TRACKABLE_GEOMETRIC
    geometricConstraint: bpy.props.EnumProperty(items=TRACKABLE_GEOMETRIC_CONSTRAINT)

    # TRACKABLE_MARKER_2D
    # TRACKABLE_MARKER_3D
    marker_2D: bpy.props.PointerProperty(
        type=bpy.types.Image,
        name="2D marker",
        description="Select an anchor image"
    )

    # TRACKABLE_MARKER_GEO
    coordinates: bpy.props.FloatVectorProperty(name="longitude[-180.0:180.0], latitude[-90.0:90.0], elevation[meters above the WGS 84 reference ellipsoid]")


def update_anchor_trackable(self, context):
    # Find and assign the trackable from scene.xr_trackables by name
    scene = context.scene
    for trackable in scene.xr_trackables:
        if trackable.name == self.trackable_name:
            self.trackable = trackable
            break

class XRAnchorObjectProperties(bpy.types.PropertyGroup):
    # Mandatory
    trackable_name: bpy.props.StringProperty(name="Trackable Name", update=update_anchor_trackable)
    trackable: bpy.props.PointerProperty(
        type=XRTrackableObjectProperty,
        name="trackable",
        description="Select a trackable item"
    )
    requiresAnchoring: bpy.props.BoolProperty(name="Requires anchoring")
    minimumRequiredSpace: bpy.props.FloatVectorProperty(name="Min required space")
    aligned: bpy.props.BoolProperty(name="Aligned")

    # https://docs.blender.org/api/current/bpy.props.html#bpy.props.CollectionProperty
    # actions: bpy.props.CollectionProperty(InteractivityActionsObjectProperty)
    
    # MPEG_lights_texture_based
    # light: bpy.props.PointerProperty(type=MPEGLightTextureProperty)
    


################################################################################################
# Trackable / Anchor list management
################################################################################################

class XR_TRACKABLE_UL_List(bpy.types.UIList): 
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index): 
        # We could write some code to decide which icon to use here... 
        custom_icon = 'OBJECT_DATAMODE' # Make sure your code supports all 3 layout types 
        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(text=item.name, icon = custom_icon) 
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label(text="", icon = custom_icon)


class LIST_OT_NewXrTrackable(bpy.types.Operator): 
    bl_idname = "xr_trackables.new_item" 
    bl_label = "Add XR trackable"

    def execute(self, context): 
        context.scene.xr_trackables.add()
        return{'FINISHED'}


class LIST_OT_DeleteXrTrackable(bpy.types.Operator):
    bl_idname = "xr_trackables.delete_item"
    bl_label = "Delete XR trackable"

    @classmethod
    def poll(cls, context):
        return context.scene.xr_trackables

    def execute(self, context):
        xr_trackables = context.scene.xr_trackables
        idx = context.scene.xr_trackable_idx
        xr_trackables.remove(idx)
        context.scene.xr_trackable_idx = min(max(0, idx-1), len(xr_trackables)-1)
        return{'FINISHED'}


class XR_OT_set_trackable_type(bpy.types.Operator):
    bl_idname = "xr_trackable.set_type"
    bl_label = "Set trackable type"
    bl_description = "Set type for the selected trackable"
    type: bpy.props.EnumProperty(items=XR_TRACKABLE_TYPES)

    def execute(self, context):
        scene = context.scene
        idx = context.scene.xr_trackable_idx
        trackable = context.scene.xr_trackables[idx]
        if trackable is None:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}
        
        trackable.type = self.type
        return {'FINISHED'}
    
    """
class LIST_OT_MoveXrTrackable(bpy.types.Operator): 
    bl_idname = "xr_trackables.move_item" 
    bl_label = "Move XR trackable" 
    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""), ('DOWN', 'Down', ""),)) 
    
    @classmethod 
    def poll(cls, context): 
        return context.scene.xr_trackables 
    
    def move_index(self): 
        index = bpy.context.scene.xr_trackable_idx 
        list_length = len(bpy.context.scene.xr_trackables) - 1 # (index starts at 0) 
        new_index = index + (-1 if self.direction == 'UP' else 1) 
        bpy.context.scene.xr_trackable_idx = max(0, min(new_index, list_length)) 
        
    def execute(self, context): 
        xr_trackables = context.scene.xr_trackables 
        index = context.scene.xr_trackable_idx 
        neighbor = index + (-1 if self.direction == 'UP' else 1) 
        xr_trackables.move(neighbor, index) 
        self.move_index() 
        return{'FINISHED'}
    """


################################################################################################

class XR_ANCHOR_UL_List(bpy.types.UIList): 
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index): 
        # We could write some code to decide which icon to use here... 
        custom_icon = 'OBJECT_DATAMODE' # Make sure your code supports all 3 layout types 
        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(text=item.name, icon = custom_icon) 
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label(text="", icon = custom_icon)



class LIST_OT_NewXrAnchor(bpy.types.Operator): 
    bl_idname = "xr_anchors.new_item" 
    bl_label = "Add XR anchor"

    def execute(self, context): 
        context.scene.xr_anchors.add()
        return{'FINISHED'}


class LIST_OT_DeleteXrAnchor(bpy.types.Operator):
    bl_idname = "xr_anchors.delete_item"
    bl_label = "Delete XR anchor"

    @classmethod
    def poll(cls, context):
        return context.scene.xr_anchors

    def execute(self, context):
        xr_anchors = context.scene.xr_anchors
        idx = context.scene.xr_anchor_idx
        xr_anchors.remove(idx)
        context.scene.xr_anchor_idx = min(max(0, idx-1), len(xr_anchors)-1)
        return{'FINISHED'}
        

class RTXR_PT_anchors_panel(bpy.types.Panel):
    """
    Show all anchors. In 3D View, Press N to toggle tabs overlay (top right corner).
    """
    bl_label = "XR Anchors"
    bl_idname = "RTXR_PT_anchors_panel"
    bl_category = "XR Anchors"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #  ('DEFAULT_CLOSED', 'HIDE_HEADER', 'INSTANCED', 'HEADER_LAYOUT_EXPAND')
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout 
        scene = context.scene 
        
        row = layout.row()         
        row.label(text="Scene TRACKABLES:")
        row = layout.row() 
        row.template_list("XR_TRACKABLE_UL_List", "XR_trackables_list", scene, "xr_trackables", scene, "xr_trackable_idx") 
        row = layout.row() 
        row.operator('xr_trackables.new_item', text='NEW') 
        row.operator('xr_trackables.delete_item', text='REMOVE') 
        # row.operator('xr_trackables.move_item', text='UP').direction = 'UP' 
        # row.operator('xr_trackables.move_item', text='DOWN').direction = 'DOWN' 
        
        if scene.xr_trackable_idx >= 0 and scene.xr_trackables: 
            active_trackable = scene.xr_trackables[scene.xr_trackable_idx] 
            row = layout.row()
            row.operator_menu_enum("xr_trackable.set_type", "type", text=active_trackable.type)
            if active_trackable.type == 'TRACKABLE_FLOOR':
                pass
            elif active_trackable.type == 'TRACKABLE_VIEWER':
                pass
            elif active_trackable.type == 'TRACKABLE_CONTROLLER':
                row = layout.row()
                row.prop(active_trackable, "path") 
            elif active_trackable.type == 'TRACKABLE_PLANE':
                row = layout.row()
                row.prop(active_trackable, "geometricConstraint") 
            elif active_trackable.type == 'TRACKABLE_MARKER_2D':
                row = layout.row()
                row.prop(active_trackable, "name") 
                row = layout.row()
                row.prop(active_trackable, "marker_2D")
                # row.template_ID(active_trackable, "marker_2D", new="image.new", open="image.open")
            elif active_trackable.type == 'TRACKABLE_MARKER_GEO':
                row = layout.row()
                row.prop(active_trackable, "name") 
                row = layout.row()
                row.prop(active_trackable, "coordinates")
            else:
                row = layout.row()
                row.label(text="request this feature on github")

        row = layout.row()         
        row.label(text="Scene ANCHOR:")
        row = layout.row() 
        row.template_list("XR_ANCHOR_UL_List", "XR_anchors_list", scene, "xr_anchors", scene, "xr_anchor_idx") 
        row = layout.row() 
        row.operator('xr_anchors.new_item', text='NEW') 
        row.operator('xr_anchors.delete_item', text='REMOVE') 
        # row.operator('xr_anchors.move_item', text='UP').direction = 'UP' 
        # row.operator('xr_anchors.move_item', text='DOWN').direction = 'DOWN' 
        
        if scene.xr_anchor_idx >= 0 and scene.xr_anchors: 
            active_anchor = scene.xr_anchors[scene.xr_anchor_idx] 
            row = layout.row()
            row.prop(active_anchor, 'name')
            row = layout.row()
            row.prop_search(active_anchor, 'trackable_name', scene, 'xr_trackables', icon='OBJECT_DATA')
            row = layout.row()
            row.label(text=active_anchor.trackable_name)
            row = layout.row()
            row.label(text=active_anchor.trackable.name)
            row = layout.row()
            row.prop(active_anchor, 'requiresAnchoring')
            row = layout.row()
            row.prop(active_anchor, 'minimumRequiredSpace')
            row = layout.row()
            row.prop(active_anchor, 'aligned')


################################################################################################
# Node anchor selection
################################################################################################

    """
class OBJECT_OT_set_xr_anchor_type(bpy.types.Operator):
    bl_idname = "object.set_xr_anchor_type"
    bl_label = "Set Anchoring Type"
    bl_description = "Set the anchoring type for the selected object"

    anchor_type: bpy.props.EnumProperty(items=XR_TRACKABLE_TYPES)

    def execute(self, context):
        obj = context.object
        if obj is None:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}
        
        obj.xr_anchor.anchor_type = self.anchor_type
        return {'FINISHED'}
    """


    """
class OBJECT_PT_xr_anchor_panel(bpy.types.Panel):
    bl_label = "XR anchoring"
    bl_idname = "OBJECT_PT_xr_anchor_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj is None:
            layout.label(text="No active object selected.")
        else:
            xr_anchor = obj.xr_anchor # get('anchor_type', 'NONE')
            row = layout.row()
            row.operator_menu_enum("object.set_xr_anchor_type", "anchor_type", text=xr_anchor.anchor_type)

            anchor_row = layout.row()
            anchor_row.label(text='not available')

            if xr_anchor.anchor_type == '2D_MARKER':
                layout.template_ID(obj.xr_anchor, "marker_2D", new="image.new", open="image.open")
    """


def register_xr_anchors():
    # Scene level ANCHOR def 
    bpy.utils.register_class(XRTrackableObjectProperty)
    bpy.types.Scene.xr_trackables = bpy.props.CollectionProperty(type=XRTrackableObjectProperty)
    bpy.types.Scene.xr_trackable_idx = bpy.props.IntProperty(name = "Selected trackable", default = 0)
    bpy.utils.register_class(XR_TRACKABLE_UL_List) 
    bpy.utils.register_class(LIST_OT_NewXrTrackable) 
    bpy.utils.register_class(LIST_OT_DeleteXrTrackable) 
    # bpy.utils.register_class(LIST_OT_MoveXrTrackable)
    bpy.utils.register_class(XR_OT_set_trackable_type)

    # Scene level ANCHOR def 
    bpy.utils.register_class(XRAnchorObjectProperties)
    bpy.types.Scene.xr_anchors = bpy.props.CollectionProperty(type=XRAnchorObjectProperties)
    bpy.types.Scene.xr_anchor_idx = bpy.props.IntProperty(name = "Selected anchor", default = 0)
    bpy.utils.register_class(XR_ANCHOR_UL_List) 
    bpy.utils.register_class(LIST_OT_NewXrAnchor) 
    bpy.utils.register_class(LIST_OT_DeleteXrAnchor) 
    # bpy.utils.register_class(LIST_OT_MoveXrAnchor)

    # Node configuration
    # bpy.types.Object.xr_anchor = bpy.props.PointerProperty(type=XRAnchorObjectProperties)
    # bpy.utils.register_class(OBJECT_OT_set_xr_anchor_type)
    # bpy.utils.register_class(OBJECT_PT_xr_anchor_panel)

    # Scene configuration
    bpy.utils.register_class(RTXR_PT_anchors_panel)


def unregister_xr_anchors():
    bpy.utils.unregister_class(RTXR_PT_anchors_panel)
    # Scene level anchor def
    bpy.utils.unregister_class(LIST_OT_NewXrTrackable) 
    bpy.utils.unregister_class(LIST_OT_DeleteXrTrackable) 
    # bpy.utils.unregister_class(LIST_OT_MoveXrTrackable)
    bpy.utils.unregister_class(XR_OT_set_trackable_type)
    bpy.utils.unregister_class(XR_TRACKABLE_UL_List)    
    del bpy.types.Scene.xr_trackables
    del bpy.types.Scene.xr_trackable_idx

    bpy.utils.unregister_class(LIST_OT_NewXrAnchor) 
    bpy.utils.unregister_class(LIST_OT_DeleteXrAnchor) 
    # bpy.utils.unregister_class(LIST_OT_MoveXrAnchor)
    bpy.utils.unregister_class(XR_ANCHOR_UL_List) 
    del bpy.types.Scene.xr_anchors
    del bpy.types.Scene.xr_anchor_idx
    # Node level anchor ref
    # bpy.utils.unregister_class(OBJECT_OT_set_xr_anchor_type)
    # bpy.utils.unregister_class(OBJECT_PT_xr_anchor_panel)
    # del bpy.types.Object.xr_anchor
    # Anchor model 
    bpy.utils.unregister_class(XRAnchorObjectProperties)
    bpy.utils.unregister_class(XRTrackableObjectProperty)
