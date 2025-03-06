from enum import StrEnum
import logging
import bpy


class XRMarkerType(StrEnum):
    MARKER_2D = 'MARKER_2D'
    MARKER_3D = 'MARKER_3D'


class XRMarkerFactory:

    @staticmethod
    def create_xr_marker_2d(image:bpy.types.Image):
        marker_id = image.name
        if XRMarkerFactory.get(marker_id) != None:
            logging.warning(f'XR marker already exists with image {marker_id}. Don\'t duplicate anchors. Use a parent node as the root for the anchor instead.')
            return
        # Create a plane
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=(0, 0, 0))
        plane = bpy.context.active_object
        plane.name = marker_id
        plane.xr_marker.enabled = True
        plane.xr_marker.type = XRMarkerType.MARKER_2D
        plane.xr_marker.name = marker_id

        # Create a new material
        mat = bpy.data.materials.new(name="XRMarkerMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")

        # Add texture node and link image
        tex_image_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex_image_node.image = image
        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image_node.outputs['Color'])

        # Assign the material to the plane
        if plane.data.materials:
            plane.data.materials[0] = mat
        else:
            plane.data.materials.append(mat)

        return plane

    @staticmethod
    def iter_xr_marker_objects():
        for obj in bpy.context.scene.objects:
            if (obj.type == 'MESH' and obj.xr_marker.enabled):
                yield obj

    @staticmethod
    def scene_has_markers():
        for _ in XRMarkerFactory.iter_xr_marker_objects():
            return True
        return False

    @staticmethod
    def list_all():
        return [*XRMarkerFactory.iter_xr_marker_objects()]

    @staticmethod
    def name_all():
        return [obj.xr_marker.name for obj in XRMarkerFactory.iter_xr_marker_objects()]
        
    @staticmethod
    def get(marker_id):
        for obj in XRMarkerFactory.iter_xr_marker_objects():
            if obj.xr_marker.name == marker_id:
                return obj


class XRMarkerProperties(bpy.types.PropertyGroup):
    # it's not possible to store a reference to a native blender object, 
    # the only way is to reference objects by names, which users may update and break
    enabled: bpy.props.BoolProperty()
    type: bpy.props.StringProperty()
    name: bpy.props.StringProperty()

    def __str__(self):
        return f'{self.type} - {self.name}' if self.enabled else 'diasbled'


class XRMarkersPanelProperties(bpy.types.PropertyGroup):
    image: bpy.props.PointerProperty(type=bpy.types.Image)


class XRMarker2dPanel(bpy.types.Panel):
    bl_label = "Image Markers"
    bl_idname = "VIEW3D_PT_XrMarker2d"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "XR Anchoring"

    def draw(self, context):
        layout = self.layout
        props = context.scene.xr_markers_panel
        markers = XRMarkerFactory.list_all()

        layout.label(text="Select image:")
        layout.template_ID(props, "image", open="image.open")

        if props.image:
            exists = False
            for m in markers:
                if m.name == props.image.name:
                    exists = True
                    continue
            if not exists:
                layout.operator("xr_markers.create_marker", text="Create marker node")

        layout.separator()
        for obj in markers:
            row = layout.row()
            row.label(text=obj.xr_marker.name)
            row.operator("xr_markers.set_active_selection", icon='SELECT_SET').marker_id = obj.xr_marker.name


class XRMarker_OT_Create(bpy.types.Operator):
    bl_idname = "xr_markers.create_marker"
    bl_label = "Create marker node"
    bl_description = "Create a marker using the selected image"

    def execute(self, context):
        props = context.scene.xr_markers_panel
        image = props.image
        if not image:
            self.report({'WARNING'}, "No image selected")
            return {'CANCELLED'}
        obj = XRMarkerFactory.create_xr_marker_2d(image)
        if obj:
            self.report({'INFO'}, f"XR Marker '{obj.name}' created.")
        return {'FINISHED'}


class XRMarkersSetActiveSelectionOperator(bpy.types.Operator):
    bl_idname = "xr_markers.set_active_selection"
    bl_label = ""
    bl_description = "Set active selection to this marker node"
    marker_id: bpy.props.StringProperty()

    def execute(self, context):
        obj = XRMarkerFactory.get(self.marker_id)
        if obj:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
        else:
            print("No valid object selected")
        return {'FINISHED'}


classes = [
    XRMarkerProperties,
    XRMarkersPanelProperties,
    XRMarker2dPanel,
    XRMarker_OT_Create,
    XRMarkersSetActiveSelectionOperator
]

def register_markers():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.xr_marker = bpy.props.PointerProperty(type=XRMarkerProperties)
    bpy.types.Scene.xr_markers_panel = bpy.props.PointerProperty(type=XRMarkersPanelProperties)

def unregister_markers():
    del bpy.types.Scene.xr_markers_panel
    del bpy.types.Object.xr_marker
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

