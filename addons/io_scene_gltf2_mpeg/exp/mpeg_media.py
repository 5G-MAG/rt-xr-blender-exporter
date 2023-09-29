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

import os
import shutil
import struct
from pathlib import Path

from io_scene_gltf2.io.com import gltf2_io_extensions
from io_scene_gltf2.io.com.gltf2_io_constants import ComponentType, DataType
from io_scene_gltf2.io.com import gltf2_io  # Accessor, BufferView, Buffer

from typing import List
from ..com.MPEG_media import Media, MediaAlternative, MediaAlternativeTrack, media_to_dict


class MediaLibrary:

    medias = {}

    @classmethod
    def get_video_media(cls, image, export_settings) -> Media:
        filepath = cls.abspath(image.filepath)

        # FIXME: this results in missing tracks definitions
        if filepath in cls.medias:
            return cls.medias[filepath]

        m = Media(alternatives=[MediaAlternative('video/mp4', filepath.name)], autoplay=True, loop=True)
        cls.medias[filepath] = m
        
        return m


    @classmethod
    def get_audio_media(cls, sound, export_settings) -> Media:
        filepath = cls.abspath(sound.filepath)
        codec = str(export_settings["mpeg_audio_object_codec"]).lower()
        mime_type = f'audio/{codec}'

        # FIXME: this results in missing tracks definitions
        if filepath in cls.medias:
            return cls.medias[filepath]
        
        m = Media(alternatives=[MediaAlternative(mime_type, filepath.name)], autoplay=True, loop=True)
        cls.medias[filepath] = m
        return m

    @classmethod
    def abspath(cls, filepath):
        return Path(bpy.path.abspath(filepath)).resolve()

    @classmethod
    def export(cls, export_settings):
        output_dir = Path(export_settings['gltf_texturedirectory'])
        os.makedirs(output_dir, exist_ok=True)
        for src, _ in cls.medias.items():
            shutil.copy(src, output_dir/src.name)

    
#############################################################################


class MediaFrame:

    def __init__(self, media, tracks=None, name="MPEG_media.frame"):
        self.buffer = self.create_media_buffer(media, tracks)
        self.buffer_views = []
        self.accessors = []
        self._header_byte_offset = 0


    def add_buffer_view(self, accessors:List[gltf2_io.Accessor], suggestedUpdateRate:float, use_headers=False, interleave=False):
        """
        given a list of accessors, append bufferView to the frame
        """
        if interleave and (len(accessors) < 2):
            raise Exception("interleaving requires at least 2 accessors")

        count = 0
        byte_offset = 0
        buffer_view = gltf2_io.BufferView(
            buffer=self.buffer,
            byte_length=None,
            byte_offset=None,
            byte_stride=None,
            extensions=None,
            extras=None,
            name="MPEG_media.frame",
            target=None
        )
        
        for accessor in accessors:
            count = max(count, accessor.count)
            accessor.buffer_view = buffer_view
            extension_dict = { "suggestedUpdateRate": suggestedUpdateRate }
            if use_headers:
                header = _get_immutable_header(accessor)
                if self._header_byte_offset > 0:
                    header.byte_offet = self._header_byte_offset
                self._header_byte_offset += header.byte_length
                extension_dict["bufferView"] = header
            ext = gltf2_io_extensions.Extension(
                    name="MPEG_accessor_timed",
                    extension=extension_dict
                )
            if accessor.extensions is None:
                accessor.extensions = {}
            accessor.extensions[ext.name] = ext
            if interleave:
                accessor.byte_offset = byte_offset
            
            byte_offset += _accessor_element_size_with_padding(accessor)

        if interleave and (byte_offset > 0):
            buffer_view.byte_stride = byte_offset
             
        buffer_view.byte_length = count * byte_offset
        self.buffer_views.append(buffer_view)
        self.accessors.append(accessors)
        
    
    def finalize(self):
        self.buffer.byte_length = self._header_byte_offset
        for buffer_view in self.buffer_views:
            buffer_view.byte_offset = self.buffer.byte_length
            self.buffer.byte_length += buffer_view.byte_length

    @staticmethod
    def create_media_buffer(media:Media, tracks=None, name=None):
        buffer_ext = gltf2_io_extensions.Extension(
                name="MPEG_buffer_circular",
                extension=_get_buffer_source_extension(media)
            )
        buffer = gltf2_io.Buffer(
            byte_length=0,
            extensions={buffer_ext.name: buffer_ext},
            extras=None,
            name="MPEG_media.frame.buffer" if name is None else name,
            uri=None
        )
        return buffer
    

def _get_buffer_source_extension(media:Media, tracks=None):
    # TODO: handle tracks ...
    m = gltf2_io_extensions.ChildOfRootExtension(
        name="MPEG_media",
        path=["media"],
        extension=media_to_dict(media)
    )
    return {
        "media": m
    }


def _get_immutable_header(accessor, byte_offset=None):
    return gltf2_io.BufferView(
        buffer=accessor.buffer_view.buffer,
        byte_length=_calc_immutable_header_size(accessor),
        byte_offset=None,
        byte_stride=None,
        extensions=None,
        extras=None,
        name="MPEG_accessor_timed.header",
        target=None
    )


def _calc_immutable_header_size(accessor):
    # calculates the size of the header refered to by the MPEG_accessor_timed.bufferView
    # see: ISO/IEC 23090-14 - Table 8 – Definition of timed accessor information header fields
    maxMin = None
    count = DataType.num_elements(accessor.type)

    if accessor.component_type == ComponentType.Float:
        maxMin = "f" * count * 2
    elif accessor.component_type == ComponentType.UnsignedByte:
        maxMin = "B" * count
    elif accessor.component_type == ComponentType.Byte:
        maxMin = "b" * count
    elif accessor.component_type == ComponentType.UnsignedShort:
        maxMin = "H" * count
    elif accessor.component_type == ComponentType.Short:
        maxMin = "h" * count
    else:
        raise NotImplementedError(self.component)
    
    return struct.calcsize(f'<fII{maxMin}III')


def _accessor_element_size_with_padding(accessor):
    # FIXME: some matrix configurations are not properly padded
    # see: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#data-alignment
    length = ComponentType.get_size(accessor.component_type) * DataType.num_elements(accessor.type)
    padding = (4 - (length % 4))
    return length + padding if padding > 0 else length