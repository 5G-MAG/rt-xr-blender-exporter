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

# https://docs.blender.org/api/current/aud.html
import aud 

from io_scene_gltf2.io.com import gltf2_io, gltf2_io_extensions
from io_scene_gltf2.io.com.gltf2_io_constants import ComponentType, DataType

from ..com.MPEG_audio_spatial import Attenuation, TypeEnum #, MPEGAudioSpatialSource
from ..exp.mpeg_media import MediaLibrary, MediaFrame

MPEG_AUDIO_SPATIAL = "MPEG_audio_spatial"


def get_audio_source_extension(blender_node, audio_source_id, export_settings):
    if blender_node.data.sound is None:
        return None
    elif not export_settings["mpeg_enable_spatial_audio"]:
        return None

    src = {
        "id": audio_source_id,
        "type": TypeEnum.Object.value,
        "targetSampleRate": _get_audio_source_samplerate(blender_node.data.sound, export_settings),
        "accessors": _get_audio_source_accessors(blender_node.data.sound, export_settings),
        "attenuation": _get_audio_attenuation_model(export_settings),
        "attenuationParameters": _get_audio_attenuation_args(blender_node, export_settings),
        "referenceDistance": blender_node.data.distance_reference
    }

    return gltf2_io_extensions.Extension(
            name=MPEG_AUDIO_SPATIAL,
            extension={
                "sources": [ src ]
            }
        )


def export_audio_source(sound, export_settings):
    src = bpy.path.abspath(sound.filepath)
    output_dir = Path(export_settings['gltf_texturedirectory'])
    out = output_dir/Path(src).stem+'.mp3'
    tmp = aud.Sound.file(src)
    tmp.write(out, aud.RATE_44100, aud.CHANNELS_MONO, aud.FORMAT_FLOAT32, aud.CONTAINER_MP3, aud.CODEC_MP3, 128000, 128000)    


def _get_audio_attenuation_args(blender_node, export_settings):
    # see ISO/IEC 23090-14 for audio attenuation functions args [d, md, rf]
    md = blender_node.data.distance_max
    rf = blender_node.data.attenuation
    return [md, rf]


def _get_audio_attenuation_model(export_settings):
    m = bpy.context.scene.audio_distance_model
    if m.startswith('EXPONENTIAL'):    
        return Attenuation.exponentialDistance.value
    elif m.startswith('INVERSE'):
        return Attenuation.inverseDistance.value
    elif m.startswith('LINEAR'):
        return Attenuation.linearDistance.value
    elif m == 'NONE':
        return Attenuation.noAttenuation.value
    else:
        return Attenuation.custom.value


def _get_audio_source_samplerate(sound, export_settings):
    audio_object_codec = export_settings["mpeg_audio_object_codec"]
    if audio_object_codec == "MP3":
        return 44100
    elif audio_object_codec == "AAC":
        return 48000
    else:
        return -1


def _get_audio_source_accessors(sound, export_settings):
    
    samplerate = _get_audio_source_samplerate(sound, export_settings)
    samples_per_frame = -1

    if samplerate == 44100:
        samples_per_frame = 1152
    elif samplerate == 48000:
        samples_per_frame = 1024
    else:
        raise Exception("Invalid audio codec export configuration")

    # the audio in the source media is not mono. 
    # it could be converted using Blender's `aud` library
    if sound.channels != "MONO":
        raise Exception(f"audio channel layout {sound.channels} not supported")

    media = MediaLibrary.get_audio_media(sound, export_settings)
    frame = MediaFrame(media)

    # this assumes decoding to fltp sample format
    # TODO: investigate if interleaved is desirable
    accessor = gltf2_io.Accessor(
        buffer_view=None, 
        byte_offset=0, 
        component_type=ComponentType.Float, 
        count=samples_per_frame, 
        extensions=None, 
        extras=None,
        max=None, 
        min=None, 
        name="MPEG_texture_video.accessor", 
        normalized=False,
        sparse=None, 
        type=DataType.Scalar
    )

    fps = samplerate / samples_per_frame

    accessors = [accessor]
    frame.add_buffer_view(accessors, suggestedUpdateRate=fps, use_headers=True)
    frame.finalize()

    return accessors
