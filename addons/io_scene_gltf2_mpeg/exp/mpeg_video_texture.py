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

from io_scene_gltf2.io.com import gltf2_io, gltf2_io_extensions
from io_scene_gltf2.io.com.gltf2_io_constants import ComponentType, DataType

from ..blender.utils import get_tex_from_socket
from ..exp.mpeg_media import MediaLibrary, MediaFrame

MPEG_TEXTURE_VIDEO = "MPEG_texture_video"


def get_video_texture_extension(shader_socket: bpy.types.NodeSocket, export_settings):
        if not export_settings["mpeg_enable_video_textures"]:
            return
        
        tex = get_tex_from_socket(shader_socket, export_settings)
        if tex is None:
            return None

        ext = _get_video_texture_extension(tex.shader_node.image, export_settings)
        if ext is None:
            return None

        return gltf2_io_extensions.Extension(
                    name=MPEG_TEXTURE_VIDEO,
                    extension=ext
        )


def _get_video_texture_extension(img, export_settings):
    # glTF assumes sRGB images
    # TODO: investigate non RGB data (num channels, yuv ...)
    if img is None:
        return None
    if img.source != 'MOVIE':
        return None
    if img.filepath_from_user() == '':
        return None
    if (img.size[0] == 0) or (img.size[1] == 0):
        print(f'invalid image size: {img}')
        return None
    if img.use_deinterlace:
        return None
    if img.depth != 24:
        return None
    
    return {
        "accessor": _get_video_texture_accessor(img, export_settings),
        "width": img.size[0],
        "height": img.size[1],
        "format": "RGB" 
    }


def _get_video_texture_accessor(image, export_settings) -> gltf2_io.Accessor:
    # several assumptions here:
    # 1. pipeline decodes RGB24 image textures
    # 2. single image texture per buffer, so buffer.byte_length is known

    count = image.size[0] * image.size[1]

    accessor = gltf2_io.Accessor(
        buffer_view=None, 
        byte_offset=0, 
        component_type=ComponentType.UnsignedByte, 
        count=count, 
        extensions=None, 
        extras=None,
        max=None, 
        min=None, 
        name="MPEG_texture_video.accessor", 
        normalized=False,
        sparse=None, 
        type=DataType.Vec3
    )

    media = MediaLibrary.get_video_media(image, export_settings)
    frame = MediaFrame(media)
    frame.add_buffer_view(accessors=[accessor], suggestedUpdateRate=bpy.context.scene.render.fps)
    frame.finalize()
    return accessor
