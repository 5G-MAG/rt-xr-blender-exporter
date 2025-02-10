import bpy

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

ANCHOR_ALIGNMENT = [
    ('NOT_USED', 'Not used', 'Not used'),
    ('ALIGNED_NOTSCALED', 'Not scale', 'Not scaled'),
    ('ALIGNED_SCALED', 'Scaled', 'Scaled')
]

class XRAnchorObjectProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty()
    #############################################
    # TRACKABLE OBJECT PROPERTIES
    trackable_type: bpy.props.EnumProperty(items=XR_TRACKABLE_TYPES)
    trackable_controller: bpy.props.StringProperty(
        name="Path"
    )
    trackable_plane: bpy.props.EnumProperty(items=TRACKABLE_GEOMETRIC_CONSTRAINT)
    trackable_marker_2D: bpy.props.PointerProperty(
        type=bpy.types.Image,
        name="2D marker"
    )
    trackable_marker_geo: bpy.props.FloatVectorProperty(name="Geo coords")
    #############################################
    # ANCHOR OBJECT PROPERTIES
    requiresAnchoring: bpy.props.BoolProperty(name="Requires anchoring")
    minimumRequiredSpace: bpy.props.FloatVectorProperty(name="Min required space")
    aligned: bpy.props.BoolProperty(name="Aligned")



class OBJECT_OT_set_xr_anchor_type(bpy.types.Operator):
    bl_idname = "object.set_xr_anchor_type"
    bl_label = "Set Anchoring Type"
    bl_description = "Set the anchoring type for the selected object"

    trackable_type: bpy.props.EnumProperty(items=XR_TRACKABLE_TYPES)

    def execute(self, context):
        obj = context.object
        if obj is None:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}
        
        obj.xr_anchor.trackable_type = self.trackable_type
        return {'FINISHED'}


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
            xr_anchor = obj.xr_anchor
            row = layout.row()
            row.prop(xr_anchor, "enabled") 
            if not xr_anchor.enabled:
                return
            row = layout.row()
            row.operator_menu_enum("object.set_xr_anchor_type", "trackable_type", text=xr_anchor.trackable_type)
            if xr_anchor.trackable_type == 'TRACKABLE_CONTROLLER':
                row = layout.row()
                row.prop(xr_anchor, "trackable_controller") 
            elif xr_anchor.trackable_type == 'TRACKABLE_PLANE':
                row = layout.row()
                row.prop(xr_anchor, "trackable_plane") 
            elif xr_anchor.trackable_type == 'TRACKABLE_MARKER_2D':
                row = layout.row()
                row.prop(xr_anchor, "trackable_marker_2D")
                # row.template_ID(xr_anchor, "marker_2D", new="image.new", open="image.open")
            elif xr_anchor.trackable_type == 'TRACKABLE_MARKER_GEO':
                row = layout.row()
                row.prop(xr_anchor, "trackable_marker_geo")
            elif xr_anchor.trackable_type == 'TRACKABLE_MARKER_3D' or \
                    xr_anchor.trackable_type == 'TRACKABLE_MARKER_APPLICATION':
                row = layout.row()
                row.label(text="request this feature on github")


def register_xr_anchors():
    bpy.utils.register_class(XRAnchorObjectProperties)
    bpy.types.Object.xr_anchor = bpy.props.PointerProperty(type=XRAnchorObjectProperties)
    bpy.utils.register_class(OBJECT_OT_set_xr_anchor_type)
    bpy.utils.register_class(OBJECT_PT_xr_anchor_panel)

def unregister_xr_anchors():
    bpy.utils.unregister_class(OBJECT_PT_xr_anchor_panel)
    bpy.utils.unregister_class(OBJECT_OT_set_xr_anchor_type)
    bpy.utils.unregister_class(XRAnchorObjectProperties)
    del bpy.types.Object.xr_anchor
