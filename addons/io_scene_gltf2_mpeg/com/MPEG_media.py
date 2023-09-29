# Copyright (c) 2023 MotionSpell
# Licensed under the License terms and conditions for use, reproduction,
# and distribution of 5GMAG software (the “License”).
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at https://www.5g-mag.com/license .
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from dataclasses import dataclass
from typing import Dict, Any, Optional, List, TypeVar, Callable, Type, cast


"""
these files were generated using Quicktype and then manually fixed.
do NOT assume simply regenerating the classes using quicktype will work out of the box !
"""

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


@dataclass
class MediaAlternativeTrack:
    """The codecs parameter, as defined in IETF RFC 6381, of the media included in the track."""
    codecs: str
    """URL fragment to access the track within the media alternative."""
    track: str
    extensions: Optional[Dict[str, Dict[str, Any]]] = None
    extras: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MediaAlternativeTrack':
        assert isinstance(obj, dict)
        codecs = from_str(obj.get("codecs"))
        track = from_str(obj.get("track"))
        extensions = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("extensions"))
        extras = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extras"))
        return MediaAlternativeTrack(codecs, track, extensions, extras)

    def to_dict(self) -> dict:
        result: dict = {}
        result["codecs"] = from_str(self.codecs)
        result["track"] = from_str(self.track)
        if self.extensions is not None:
            result["extensions"] = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], self.extensions)
        if self.extras is not None:
            result["extras"] = self.extras
        return result


@dataclass
class MediaAlternative:
    """The media's MIME type."""
    mime_type: str
    """The uri of the media."""
    uri: str
    extensions: Optional[Dict[str, Dict[str, Any]]] = None
    """An object that may contain any additional media-specific parameters."""
    extra_params: Optional[Dict[str, Any]] = None
    extras: Optional[Dict[str, Any]] = None
    """An array of items that lists the components of the referenced media source that are to be
    used.
    """
    tracks: Optional[List[MediaAlternativeTrack]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MediaAlternative':
        assert isinstance(obj, dict)
        mime_type = from_str(obj.get("mimeType"))
        uri = from_str(obj.get("uri"))
        extensions = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("extensions"))
        extra_params = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extraParams"))
        extras = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extras"))
        tracks = from_union([lambda x: from_list(MediaAlternativeTrack.from_dict, x), from_none], obj.get("tracks"))
        return MediaAlternative(mime_type, uri, extensions, extra_params, extras, tracks)

    def to_dict(self) -> dict:
        result: dict = {}
        result["mimeType"] = from_str(self.mime_type)
        result["uri"] = from_str(self.uri)
        if self.extensions is not None:
            result["extensions"] = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], self.extensions)
        if self.extra_params is not None:
            result["extraParams"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.extra_params)
        if self.extras is not None:
            result["extras"] = self.extras
        if self.tracks is not None:
            result["tracks"] = from_union([lambda x: from_list(lambda x: to_class(MediaAlternativeTrack, x), x), from_none], self.tracks)
        return result


@dataclass
class Media:
    """Media used to create a texture, audio source, or any other media type."""
    """An array of alternatives of the same media (e.g. different video code used)"""
    alternatives: List[MediaAlternative]
    """Specifies that the media start playing as soon as it is ready."""
    autoplay: Optional[bool] = None
    """Specifies that playback starts simultaneously for all media sources with the autoplay
    flag set to true.
    """
    autoplay_group: Optional[int] = None
    """Specifies that media controls should be exposed to end user"""
    controls: Optional[bool] = None
    """The endTimeOffset indicates the time offset into the source, up to which the timed media
    is generated.
    """
    end_time_offset: Optional[float] = None
    extensions: Optional[Dict[str, Dict[str, Any]]] = None
    extras: Optional[Dict[str, Any]] = None
    """Specifies that the media start over again, every time it is finished."""
    loop: Optional[bool] = None
    """User-defined name of the media."""
    name: Optional[str] = None
    """The startTime gives the time at which the rendering of the timed media will be in seconds."""
    start_time: Optional[float] = None
    """The startTimeOffset indicates the time offset into the source, starting from which the
    timed media is generated.
    """
    start_time_offset: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Media':
        assert isinstance(obj, dict)
        alternatives = from_list(MediaAlternative.from_dict, obj.get("alternatives"))
        autoplay = from_union([from_bool, from_none], obj.get("autoplay"))
        autoplay_group = from_union([from_int, from_none], obj.get("autoplayGroup"))
        controls = from_union([from_bool, from_none], obj.get("controls"))
        end_time_offset = from_union([from_float, from_none], obj.get("endTimeOffset"))
        extensions = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("extensions"))
        extras = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extras"))
        loop = from_union([from_bool, from_none], obj.get("loop"))
        name = from_union([from_str, from_none], obj.get("name"))
        start_time = from_union([from_float, from_none], obj.get("startTime"))
        start_time_offset = from_union([from_float, from_none], obj.get("startTimeOffset"))
        return Media(alternatives, autoplay, autoplay_group, controls, end_time_offset, extensions, extras, loop, name, start_time, start_time_offset)

    def to_dict(self) -> dict:
        result: dict = {}
        result["alternatives"] = from_list(lambda x: to_class(MediaAlternative, x), self.alternatives)
        if self.autoplay is not None:
            result["autoplay"] = from_union([from_bool, from_none], self.autoplay)
        if self.autoplay_group is not None:
            result["autoplayGroup"] = from_union([from_int, from_none], self.autoplay_group)
        if self.controls is not None:
            result["controls"] = from_union([from_bool, from_none], self.controls)
        if self.end_time_offset is not None:
            result["endTimeOffset"] = from_union([to_float, from_none], self.end_time_offset)
        if self.extensions is not None:
            result["extensions"] = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], self.extensions)
        if self.extras is not None:
            result["extras"] = self.extras
        if self.loop is not None:
            result["loop"] = from_union([from_bool, from_none], self.loop)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.start_time is not None:
            result["startTime"] = from_union([to_float, from_none], self.start_time)
        if self.start_time_offset is not None:
            result["startTimeOffset"] = from_union([to_float, from_none], self.start_time_offset)
        return result


@dataclass
class MPEG_media:
    """Media used to create a texture, audio source or other objects in the scene."""
    """An array of media. A media contains data referred by other object in a scene"""
    media: List[Media]
    extensions: Optional[Dict[str, Dict[str, Any]]] = None
    extras: Optional[Dict[str, Dict[str, Any]]] = None
    """The user-defined name of this object."""
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MPEG_media':
        assert isinstance(obj, dict)
        media = from_list(Media.from_dict, obj.get("media"))
        extensions = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], obj.get("extensions"))
        extras = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("extras"))
        name = from_union([from_str, from_none], obj.get("name"))
        return MPEG(media, extensions, extras, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["media"] = from_list(lambda x: to_class(Media, x), self.media)
        if self.extensions is not None:
            result["extensions"] = from_union([lambda x: from_dict(lambda x: from_dict(lambda x: x, x), x), from_none], self.extensions)
        if self.extras is not None:
            result["extras"] = self.extras
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        return result


def media_from_dict(s: Any) -> Media:
    return Media.from_dict(s)


def media_to_dict(x: Media) -> Any:
    return to_class(Media, x)
