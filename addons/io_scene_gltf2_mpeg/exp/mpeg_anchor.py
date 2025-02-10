import bpy
from io_scene_gltf2.io.com import gltf2_io, gltf2_io_extensions

MPEG_ANCHOR = "MPEG_anchor"


def _get_trackable_dict(blender_node):
    xr_anchor = blender_node.xr_anchor
    r = {
        "type": xr_anchor.trackable_type
    }
    if xr_anchor.trackable_type == "TRACKABLE_PLANE":
        r["geometricConstraint"] = 0 if xr_anchor.trackable_plane == 'HORIZONTAL_PLANE' else 1
    elif xr_anchor.trackable_type == "TRACKABLE_MARKER_GEO":
        r["coordinates"] = [*xr_anchor.trackable_marker_geo]
    elif xr_anchor.trackable_type == "TRACKABLE_MARKER_2D":
        # TODO: get the IDX of the node using this marker image
        # r["markerNode"] = -1
        pass
    elif xr_anchor.trackable_type == "TRACKABLE_MARKER_3D":
        pass
    elif xr_anchor.trackable_type == "TRACKABLE_APPLICATION":
        pass
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

    # internal
    marker_images = {}

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