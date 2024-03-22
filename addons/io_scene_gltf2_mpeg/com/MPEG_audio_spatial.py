# Copyright (c) 2023 MotionSpell
# Licensed under the License terms and conditions for use, reproduction,
# and distribution of 5GMAG software (the “License”).
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at https://www.5g-mag.com/license .
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from typing import Dict, Any, Optional, List, TypeVar, Callable, Type, cast
from enum import Enum

"""
these files were generated using Quicktype and then manually fixed.
do NOT assume simply regenerating the classes using quicktype will work out of the box !
"""


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class MPEGAudioSpatialListener:
    """An audio listener item"""
    """A unique identifier"""
    id: int
    extensions: Optional[Dict[str, Dict[str, Any]]]
    extras: Optional[Dict[str, Dict[str, Any]]] = None

    def __init__(self, id: int, extensions: Optional[Dict[str, Dict[str, Any]]], extras: Optional[Dict[str, Any]]) -> None:
        self.id = id
        self.extensions = extensions
        self.extras = extras

    @staticmethod
    def from_dict(obj: Any) -> 'MPEGAudioSpatialListener':
        assert isinstance(obj, dict)
        extensions = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("extensions"))
        extras = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extras"))
        id = from_int(obj.get("id"))
        return MPEGAudioSpatialListener(id, extensions, extras)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        if self.extensions is not None:
            result["extensions"] = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], self.extensions)
        if self.extras is not None:
            result["extras"] = self.extras
        return result


class MPEGAudioSpatialReverbProperty:
    """Frequency for RT60 and DSR values"""
    frequency: float
    """Specifies RT60 value in `second` for the frequency provided in the `frequency` field"""
    RT60: float
    """Specifies Diffuse-to-Source Ratio value in dB for the frequency provided in the `frequency` field.
    """
    DSR: float
    extensions: Optional[Dict[str, Dict[str, Any]]]
    extras: Optional[Dict[str, Dict[str, Any]]] = None

    def __init__(self, frequency: float, RT60: float, DSR: float, extensions: Optional[Dict[str, Dict[str, Any]]], extras: Optional[Dict[str, Any]]) -> None:
        self.frequency = frequency
        self.RT60 = RT60
        self.DSR = DSR
        self.extensions = extensions
        self.extras = extras

    @staticmethod
    def from_dict(obj: Any) -> 'MPEGAudioSpatialReverbProperty':
        assert isinstance(obj, dict)
        frequency = from_float(obj.get("frequency"))
        RT60 = from_float(obj.get("RT60"))
        DSR = from_float(obj.get("DSR"))
        extensions = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("extensions"))
        extras = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extras"))
        return MPEGAudioSpatialReverbProperty(frequency, RT60, DSR, extensions, extras)

    def to_dict(self) -> dict:
        result: dict = {}
        result["frequency"] = to_float(self.frequency)
        result["RT60"] = to_float(self.RT60)
        result["DSR"] = to_float(self.DSR)
        if self.extensions is not None:
            result["extensions"] = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], self.extensions)
        if self.extras is not None:
            result["extras"] = self.extras
        return result


class MPEGAudioSpatialReverb:
    """Indicates if the reverb unit can be bypassed if the audio renderer does not support it."""
    """A unique identifier"""
    id: int
    """An array of property items"""
    properties: List[MPEGAudioSpatialReverbProperty]
    bypass: Optional[bool]
    predelay: Optional[float]
    extensions: Optional[Dict[str, Dict[str, Any]]]
    extras: Optional[Dict[str, Dict[str, Any]]] = None
    """Delay of audio source."""

    def __init__(self, id: int, properties: List[MPEGAudioSpatialReverbProperty], bypass: Optional[bool], predelay: Optional[float], extensions: Optional[Dict[str, Dict[str, Any]]], extras: Optional[Dict[str, Any]]) -> None:
        self.id = id
        self.properties = properties
        self.bypass = bypass
        self.predelay = predelay
        self.extensions = extensions
        self.extras = extras

    @staticmethod
    def from_dict(obj: Any) -> 'MPEGAudioSpatialReverb':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        bypass = from_union([from_bool, from_none], obj.get("bypass"))
        extensions = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("extensions"))
        extras = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extras"))
        predelay = from_union([from_float, from_none], obj.get("predelay"))
        properties = from_list(MPEGAudioSpatialReverbProperty.from_dict, obj.get("properties"))
        return MPEGAudioSpatialReverb(id, properties, bypass, predelay, extensions, extras)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = self.id
        result["properties"] = from_list(lambda x: to_class(MPEGAudioSpatialReverbProperty, x), self.properties)
        if self.bypass is not None:
            result["bypass"] = from_union([from_bool, from_none], self.bypass)
        if self.predelay is not None:
            result["predelay"] = from_union([to_float, from_none], self.predelay)
        if self.extensions is not None:
            result["extensions"] = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], self.extensions)
        if self.extras is not None:
            result["extras"] = self.extras
        return result


class Attenuation(Enum):
    """A function used to calculate the attenuation of the audio source."""
    custom = "custom"
    exponentialDistance = "exponentialDistance"
    inverseDistance = "inverseDistance"
    linearDistance = "linearDistance"
    noAttenuation = "noAttenuation"


class TypeEnum(Enum):
    """A type of the audio source"""
    HOA = "HOA"
    Object = "Object"


class MPEGAudioSpatialSource:
    """A unique identifier"""
    id: int
    """A type of the audio source"""
    type: TypeEnum
    """An array of accessors that describe the audio source"""
    accessors: List[int]
    """A function used to calculate the attenuation of the audio source."""
    attenuation: Optional[Attenuation]
    """An array of attenuation parameters"""
    attenuationParameters: Optional[List[float]]
    extensions: Optional[Dict[str, Dict[str, Any]]]
    extras: Optional[Dict[str, Dict[str, Any]]] = None
    """Playback speed of the audio source"""
    playbackSpeed: Optional[float]
    """A level-adjustment of the audio source"""
    pregain: Optional[float]
    """A distance in meters."""
    referenceDistance: Optional[float]
    """An array of pointers to reverb units"""
    reverbFeed: Optional[List[int]]
    """An array of gain values"""
    reverbFeedGain: Optional[List[float]]

    def __init__(self, id: int, type: TypeEnum, accessors: List[int], attenuation: Optional[Attenuation], attenuationParameters: Optional[List[float]], extensions: Optional[Dict[str, Dict[str, Any]]], extras: Optional[Dict[str, Any]], playbackSpeed: Optional[float], pregain: Optional[float], referenceDistance: Optional[float], reverbFeed: Optional[List[int]], reverbFeedGain: Optional[List[float]]) -> None:
        self.id = id
        self.type = type
        self.accessors = accessors
        self.attenuation = attenuation
        self.attenuationParameters = attenuationParameters
        self.extensions = extensions
        self.extras = extras
        self.playbackSpeed = playbackSpeed
        self.pregain = pregain
        self.referenceDistance = referenceDistance
        self.reverbFeed = reverbFeed
        self.reverbFeedGain = reverbFeedGain

    @staticmethod
    def from_dict(obj: Any) -> 'MPEGAudioSpatialSource':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        type = TypeEnum(obj.get("type"))
        accessors = from_list(from_int, obj.get("accessors"))
        attenuation = from_union([Attenuation, from_none], obj.get("attenuation"))
        attenuationParameters = from_union([lambda x: from_list(from_float, x), from_none], obj.get("attenuationParameters"))
        extensions = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("extensions"))
        extras = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extras"))
        playbackSpeed = from_union([from_float, from_none], obj.get("playbackSpeed"))
        pregain = from_union([from_float, from_none], obj.get("pregain"))
        referenceDistance = from_union([from_float, from_none], obj.get("referenceDistance"))
        reverbFeed = from_union([lambda x: from_list(from_int, x), from_none], obj.get("reverbFeed"))
        reverbFeedGain = from_union([lambda x: from_list(from_float, x), from_none], obj.get("reverbFeedGain"))
        return MPEGAudioSpatialSource(id, type, accessors, attenuation, attenuationParameters, extensions, extras, playbackSpeed, pregain, referenceDistance, reverbFeed, reverbFeedGain)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["type"] = to_enum(TypeEnum, self.type)
        result["accessors"] = from_list(from_int, self.accessors)
        if self.attenuation is not None:
            result["attenuation"] = from_union([lambda x: to_enum(Attenuation, x), from_none], self.attenuation)
        if self.attenuationParameters is not None:
            result["attenuationParameters"] = from_union([lambda x: from_list(to_float, x), from_none], self.attenuationParameters)
        if self.extensions is not None:
            result["extensions"] = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], self.extensions)
        if self.extras is not None:
            result["extras"] = self.extras
        if self.playbackSpeed is not None:
            result["playbackSpeed"] = from_union([to_float, from_none], self.playbackSpeed)
        if self.pregain is not None:
            result["pregain"] = from_union([to_float, from_none], self.pregain)
        if self.referenceDistance is not None:
            result["referenceDistance"] = from_union([to_float, from_none], self.referenceDistance)
        if self.reverbFeed is not None:
            result["reverbFeed"] = from_union([lambda x: from_list(from_int, x), from_none], self.reverbFeed)
        if self.reverbFeedGain is not None:
            result["reverbFeedGain"] = from_union([lambda x: from_list(to_float, x), from_none], self.reverbFeedGain)
        return result


class MPEG_audio_spatial:
    """glTF extension to specify spatial audio support"""
    extensions: Optional[Dict[str, Dict[str, Any]]]
    extras: Optional[Dict[str, Dict[str, Any]]] = None
    """An audio listener item"""
    listener: Optional[MPEGAudioSpatialListener]
    """An array of reverb items"""
    reverbs: Optional[List[MPEGAudioSpatialReverb]]
    """An array of audio sources."""
    sources: Optional[List[MPEGAudioSpatialSource]]

    def __init__(self, extensions: Optional[Dict[str, Dict[str, Any]]], extras: Optional[Dict[str, Any]], listener: Optional[MPEGAudioSpatialListener], reverbs: Optional[List[MPEGAudioSpatialReverb]], sources: Optional[List[MPEGAudioSpatialSource]]) -> None:
        self.extensions = extensions
        self.extras = extras
        self.listener = listener
        self.reverbs = reverbs
        self.sources = sources

    @staticmethod
    def from_dict(obj: Any) -> 'MPEG_audio_spatial':
        assert isinstance(obj, dict)
        extensions = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("extensions"))
        extras = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extras"))
        listener = from_union([MPEGAudioSpatialListener.from_dict, from_none], obj.get("listener"))
        reverbs = from_union([lambda x: from_list(MPEGAudioSpatialReverb.from_dict, x), from_none], obj.get("reverbs"))
        sources = from_union([lambda x: from_list(MPEGAudioSpatialSource.from_dict, x), from_none], obj.get("sources"))
        return MPEG_audio_spatial(extensions, extras, listener, reverbs, sources)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.extensions is not None:
            result["extensions"] = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], self.extensions)
        if self.extras is not None:
            result["extras"] = self.extras
        if self.listener is not None:
            result["listener"] = from_union([lambda x: to_class(MPEGAudioSpatialListener, x), from_none], self.listener)
        if self.reverbs is not None:
            result["reverbs"] = from_union([lambda x: from_list(lambda x: to_class(MPEGAudioSpatialReverb, x), x), from_none], self.reverbs)
        if self.sources is not None:
            result["sources"] = from_union([lambda x: from_list(lambda x: to_class(MPEGAudioSpatialSource, x), x), from_none], self.sources)
        return result


def MPEGAudioSpatialfromdict(s: Any) -> MPEG_audio_spatial:
    return MPEG_audio_spatial.from_dict(s)


def MPEGAudioSpatialtodict(x: MPEG_audio_spatial) -> Any:
    return to_class(MPEG_audio_spatial, x)
