import bpy
import logging
from .markers import register_markers, unregister_markers, XRMarkerFactory

ANCHORABLE_TYPES = (
    'CAMERA',
    'LIGHT',
    'MESH',
    'NODETREE',
    'SCENE',
    'SPEAKER',
    'EMPTY'
)

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

def xr_marker_2d_list(struct, context):
    return ((obj.xr_marker.name, obj.xr_marker.name, str(obj)) for obj in XRMarkerFactory.iter_xr_marker_objects())


class XRAnchorObjectProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty()
    #############################################
    # TRACKABLE OBJECT PROPERTIES
    trackable_type: bpy.props.EnumProperty(items=XR_TRACKABLE_TYPES)
    trackable_controller: bpy.props.StringProperty(name="XrPath")
    trackable_plane: bpy.props.EnumProperty(items=TRACKABLE_GEOMETRIC_CONSTRAINT)
    trackable_marker_node: bpy.props.EnumProperty(items=xr_marker_2d_list)
    trackable_marker_geo: bpy.props.FloatVectorProperty(name="Geo coords")
    trackable_id: bpy.props.StringProperty(name="Custom ID")
    #############################################
    # ANCHOR OBJECT PROPERTIES
    requiresAnchoring: bpy.props.BoolProperty(name="Requires anchoring")
    minimumRequiredSpace: bpy.props.FloatVectorProperty(name="Min required space")
    aligned: bpy.props.BoolProperty(name="Aligned")


class XRAnchor_OT_SetType(bpy.types.Operator):
    bl_idname = "object.set_xr_anchor_type"
    bl_label = "Anchor"
    bl_description = "Set the anchoring type for the selected object"

    trackable_type: bpy.props.EnumProperty(items=XR_TRACKABLE_TYPES)

    def execute(self, context):
        obj = context.object
        if obj is None:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}
        
        obj.xr_anchor.trackable_type = self.trackable_type
        return {'FINISHED'}

class XRAnchor_OT_SelectXrMarker2d(bpy.types.Operator):
    bl_idname = "object.select_xr_marker_2d"
    bl_label = "Marker"
    bl_description = "Select a 2D marker"

    trackable_marker_node: bpy.props.EnumProperty(items=xr_marker_2d_list)

    def execute(self, context):
        obj = context.object
        if obj is None:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}
        obj.xr_anchor.trackable_marker_node = self.trackable_marker_node
        return {'FINISHED'}


class XrAnchorObjectPropertiesPanel(bpy.types.Panel):
    bl_label = "XR Anchoring"
    bl_idname = "OBJECT_PT_XrAnchor"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        return context.object.type in ANCHORABLE_TYPES

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj is None:
            layout.label(text="No active object selected.")
        else:
            row = layout.row()
            if obj.xr_marker.enabled:
                row.label(text=f'XR Marker: {str(obj.xr_marker)}')
                return
            xr_anchor = obj.xr_anchor
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
                if XRMarkerFactory.scene_has_markers():
                    row.operator_menu_enum("object.select_xr_marker_2d", "xr_marker_id", text=xr_anchor.trackable_marker_node)
                else:
                    # TODO: set focus on the panel for users to create anchor
                    row.label(text='no XR marker found')
            elif xr_anchor.trackable_type == 'TRACKABLE_MARKER_GEO':
                row = layout.row()
                row.prop(xr_anchor, "trackable_marker_geo")
            elif xr_anchor.trackable_type == 'TRACKABLE_MARKER_3D':
                row = layout.label(text="Not Available")
            elif xr_anchor.trackable_type == 'TRACKABLE_MARKER_APPLICATION':
                row.prop(xr_anchor, "trackable_id") 

classes = [
    XRAnchor_OT_SetType,
    XRAnchor_OT_SelectXrMarker2d,
    XrAnchorObjectPropertiesPanel
]

def register_xr_anchors():
    register_markers()
    bpy.utils.register_class(XRAnchorObjectProperties)
    bpy.types.Object.xr_anchor = bpy.props.PointerProperty(type=XRAnchorObjectProperties)
    for cls in classes:
       bpy.utils.register_class(cls)


def unregister_xr_anchors():
    del bpy.types.Object.xr_anchor
    bpy.utils.unregister_class(XRAnchorObjectProperties)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    unregister_markers()