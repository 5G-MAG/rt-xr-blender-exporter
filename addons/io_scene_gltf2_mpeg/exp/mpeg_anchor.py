import bpy
from io_scene_gltf2.io.com import gltf2_io, gltf2_io_extensions

MPEG_ANCHOR = "MPEG_anchor"


def _get_trackable_dict(blender_node):
    xr_anchor = blender_node.xr_anchor
    r = {}
    if xr_anchor.trackable_type == "TRACKABLE_FLOOR":
        r["type"] = 0
    elif xr_anchor.trackable_type == "TRACKABLE_VIEWER":
        r["type"] = 1
    elif xr_anchor.trackable_type == "TRACKABLE_CONTROLLER":
        r["type"] = 2
        r["path"] = xr_anchor.trackable_controller
    elif xr_anchor.trackable_type == "TRACKABLE_PLANE":
        r["type"] = 3
        r["geometricConstraint"] = 0 if xr_anchor.trackable_plane == 'HORIZONTAL_PLANE' else 1
    elif xr_anchor.trackable_type == "TRACKABLE_MARKER_2D":
        r["type"] = 4
        r["markerNode"] = xr_anchor.trackable_marker_node
    elif xr_anchor.trackable_type == "TRACKABLE_MARKER_3D":
        r["type"] = 5
        r["markerNode"] = xr_anchor.trackable_marker_3d
    elif xr_anchor.trackable_type == "TRACKABLE_MARKER_GEO":
        r["type"] = 6
        r["coordinates"] = [*xr_anchor.trackable_marker_geo]
    elif xr_anchor.trackable_type == "TRACKABLE_APPLICATION":
        r["type"] = 7
        r["id"] = xr_anchor.trackable_id
    return r

def _get_anchor_dict(trackable_ext, blender_node):
    xr_anchor = blender_node.xr_anchor
    r = {
        "trackable": trackable_ext,
        "requiresAnchoring": xr_anchor.requiresAnchoring
    }
    if sum(xr_anchor.minimumRequiredSpace) > 0.0:
        r["minimumRequiredSpace"] = [*xr_anchor.minimumRequiredSpace]
    if xr_anchor.aligned == 'ALIGNED_NOTSCALED': 
        r["aligned"] = 1
    elif xr_anchor.aligned == 'ALIGNED_SCALED': 
        r["aligned"] = 2
    # OPTIONAL, not yet implemented in player:
    # - actions
    # - light
    return r

class AnchorRegistry:

    trackables = []
    anchors = []

    # de-duplicate trrackables
    trackable_floor = None
    trackable_viewer = None
    trackable_plane = {}
    trackable_controller = {}
    trackable_marker_node = {}
        
    @classmethod
    def _get_trackable_ext(cls, blender_node):
        xr_anchor = blender_node.xr_anchor
        trackable_type = xr_anchor.trackable_type
        trackable_ext = None

        if trackable_type == "TRACKABLE_FLOOR":
            if cls.trackable_floor is None:
                cls.trackable_floor = gltf2_io_extensions.ChildOfRootExtension(
                    name="MPEG_anchor",
                    path=["trackables"],
                    extension=_get_trackable_dict(blender_node)
                )
            trackable_ext = cls.trackable_floor
        
        elif trackable_type == "TRACKABLE_VIEWER":
            if cls.trackable_viewer is None:
                cls.trackable_viewer = gltf2_io_extensions.ChildOfRootExtension(
                    name="MPEG_anchor",
                    path=["trackables"],
                    extension=_get_trackable_dict(blender_node)
                )
            trackable_ext = cls.trackable_viewer

        elif trackable_type == "TRACKABLE_PLANE":
            constraint = xr_anchor.trackable_plane
            if not (constraint in cls.trackable_plane):
                cls.trackable_plane[constraint] = gltf2_io_extensions.ChildOfRootExtension(
                    name="MPEG_anchor",
                    path=["trackables"],
                    extension=_get_trackable_dict(blender_node)
                )
            trackable_ext = cls.trackable_plane[constraint]

        elif trackable_type == "TRACKABLE_CONTROLLER":
            path = xr_anchor.trackable_controller
            if not (path in cls.trackable_plane):
                cls.trackable_controller[path] = gltf2_io_extensions.ChildOfRootExtension(
                    name="MPEG_anchor",
                    path=["trackables"],
                    extension=_get_trackable_dict(blender_node)
                )
            trackable_ext = cls.trackable_controller[path]

        if trackable_type == "TRACKABLE_MARKER_2D":
            markerNode = xr_anchor.trackable_marker_node
            if not (markerNode in cls.trackable_marker_node):
                cls.trackable_marker_node[markerNode] = gltf2_io_extensions.ChildOfRootExtension(
                    name="MPEG_anchor",
                    path=["trackables"],
                    extension=_get_trackable_dict(blender_node)
                )
            trackable_ext = cls.trackable_marker_node[markerNode]

        else:
            trackable_ext = gltf2_io_extensions.ChildOfRootExtension(
                    name="MPEG_anchor",
                    path=["trackables"],
                    extension=_get_trackable_dict(blender_node)
                )
        
        return trackable_ext 


    @classmethod
    def get_node_anchor_extension(cls, blender_node):

        trackable_ext = cls._get_trackable_ext(blender_node)
        
        anchor_ext = gltf2_io_extensions.ChildOfRootExtension(
            name="MPEG_anchor",
            path=["anchors"],
            extension=_get_anchor_dict(trackable_ext, blender_node)
        )
        
        return gltf2_io_extensions.Extension(
                name=MPEG_ANCHOR,
                extension={
                    "anchor": anchor_ext
                }
        )