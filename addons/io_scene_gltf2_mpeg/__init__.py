# Copyright (c) 2023 MotionSpell
# Licensed under the License terms and conditions for use, reproduction,
# and distribution of 5GMAG software (the “License”).
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at https://www.5g-mag.com/license .
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import importlib
import inspect
import pkgutil
from pathlib import Path

import bpy

bl_info = {
    "name": "rt-xr-blender-exporter",
    "author": "Nils Duval",
    "description": "Export MPEG_* gltf extensions from Blender",
    "blender": (3, 6, 0),
    "version": (0, 0, 2),
    "location": "File > Import-Export",
    "category": "Import-Export",
    "tracker_url": "https://github.com/5G-MAG/rt-xr-blender-exporter/issues"
}

def get_version_string():
    return str(bl_info['version'][0]) + '.' + str(bl_info['version'][1]) + '.' + str(bl_info['version'][2])


class MPEG_ExporterProperties(bpy.types.PropertyGroup):

    enabled: bpy.props.BoolProperty(
        name='MPEG glTF extensions',
        description='Enable MPEG glTF export extensions',
        default=True,
    )

    enable_video_textures: bpy.props.BoolProperty(
        name='MPEG_texture_video',
        description='Enable MPEG_texture_video export',
        default=True,
    )

    enable_spatial_audio: bpy.props.BoolProperty(
        name='MPEG_audio_spatial',
        description='Enable MPEG_audio_spatial export',
        default=True,
    )

    media_export: bpy.props.BoolProperty(
        name='media export',
        description='Copy medias to export dir',
        default=True,
    )

    audio_object_codec: bpy.props.EnumProperty(
        items= [
            ('MP3', "mp3", ""),
            ('AAC', "aac", "")
        ],
        name='audio object codec',
        description='audio codec used for audio sources of type "Object"',
    )


class GLTF_PT_MPEGExporterExtensionPanel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_location = "File > Export > glTF 2.0"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="MPEG Extensions", icon='TOOL_SETTINGS')

    def draw(self, context):
        props = bpy.context.scene.MPEG_ExporterProperties

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(props, 'enabled', text="Enable MPEG_* extensions")
        layout.prop(props, 'enable_video_textures', text="MPEG_texture_video")
        layout.prop(props, 'enable_spatial_audio', text="MPEG_audio_spatial")
        layout.prop(props, 'media_export', text="Copy media files to output dir")
        layout.prop(props, 'audio_object_codec', text="Codec for Object audio sources")


def register():
    bpy.utils.register_class(MPEG_ExporterProperties)
    bpy.types.Scene.MPEG_ExporterProperties = bpy.props.PointerProperty(type=MPEG_ExporterProperties)


def unregister():
    unregister_panel()
    bpy.utils.unregister_class(MPEG_ExporterProperties)
    del bpy.types.Scene.MPEG_ExporterProperties


def register_panel():
    try:
        bpy.utils.register_class(GLTF_PT_MPEGExporterExtensionPanel)
    except Exception:
        pass
    return unregister_panel


def unregister_panel():
    try:
        bpy.utils.unregister_class(GLTF_PT_MPEGExporterExtensionPanel)
    except Exception:
        pass


##################################################################################
from .exp.mpeg_export import glTF2ExportMpegExtension

def glTF2_pre_export_callback(export_settings):
    props = bpy.context.scene.MPEG_ExporterProperties
    export_settings["mpeg_media_exports"] = props.media_export
    export_settings["mpeg_enable_video_textures"] = props.enable_video_textures
    export_settings["mpeg_enable_spatial_audio"] = props.enable_spatial_audio
    export_settings["mpeg_audio_object_codec"] = props.audio_object_codec

class glTF2ExportUserExtension(glTF2ExportMpegExtension):

    @property
    def enabled(self): 
        return bpy.context.scene.MPEG_ExporterProperties.enabled
