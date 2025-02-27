# Copyright (c) 2023 MotionSpell
# Licensed under the License terms and conditions for use, reproduction,
# and distribution of 5GMAG software (the “License”).
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at https://www.5g-mag.com/license .
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import bpy

from .mpeg_video_texture import get_video_texture_extension
from .mpeg_audio_source import get_audio_source_extension
from .mpeg_anchor import AnchorRegistry
from .mpeg_media import MediaLibrary

class glTF2ExportMpegExtension:

    audio_source_id = 0

    def gather_node_hook(self, gltf2_object, blender_node, export_settings):
        if not self.enabled:
            return
        if blender_node.type == "SPEAKER":
            ext = get_audio_source_extension(blender_node, self.audio_source_id, export_settings)
            if ext is None:
                return
            _add_gltf_extension(gltf2_object, ext)
            self.audio_source_id += 1
        if blender_node.xr_anchor.enabled:
            ext = AnchorRegistry.get_node_anchor_extension(blender_node)
            if ext is None:
                return
            _add_gltf_extension(gltf2_object, ext)

    def gather_texture_hook(self, texture, blender_shader_sockets, export_settings):
        if not self.enabled:
            return
        if len(blender_shader_sockets) != 1:
            raise Exception("Unsupported shader sockets configuration")
        ext = get_video_texture_extension(blender_shader_sockets[0], export_settings)
        if ext is None:
            return
        _add_gltf_extension(texture, ext)

    def gather_gltf_extensions_hook(self, gltf2_object, export_settings):
        if self.enabled:
            if export_settings["mpeg_media_exports"]:
                try:
                    MediaLibrary.export(export_settings)
                except BaseException as e:
                    print(e)
            _fix_up_buffer_references(gltf2_object, export_settings)
            _fix_anchoring_marker_nodes(gltf2_object, export_settings)
    

def _add_gltf_extension(gltf_object, extension):
    if gltf_object.extensions is None:
        gltf_object.extensions = {}
    gltf_object.extensions[extension.name] = extension


def _fix_up_buffer_references(gltf2_object, export_settings):
    # the core gltf exporter uses an hardcoded buffer_id=0 resulting in invalid buffer references
    # the core gltf buffer is created last, just before json serialization
    main_buffer_id = len(gltf2_object.buffers)-1
    for accessor in gltf2_object.accessors:
        if (accessor.extensions is not None) and ("MPEG_accessor_timed" in accessor.extensions):
            continue
        else:
            gltf2_object.buffer_views[accessor.buffer_view].buffer = main_buffer_id


def _fix_anchoring_marker_nodes(gltf2_object, export_settings):
    if "MPEG_anchor" in gltf2_object.extensions:
        marker_nodes_i = set()
        node_name_i_map = {n.name: i for i, n in enumerate(gltf2_object.nodes)}
        # replace marker node name with node indice
        for t in gltf2_object.extensions["MPEG_anchor"]["trackables"]:
            marker_node_name = t.get("markerNode") 
            if marker_node_name:
                i = node_name_i_map[marker_node_name]
                marker_nodes_i.add(i)
                t["markerNode"] = i
        # marker nodes can't have parents
        for n in gltf2_object.nodes:
            n.children = [i for i in n.children if not i in marker_nodes_i]
        # prevent marker node instantiation
        for s in gltf2_object.scenes:
            s.nodes = [i for i in s.nodes if not i in marker_nodes_i]
