<p align="center">
  <img src=".github/banner.svg" width="100%" alt="Reference Tools · XR/3D Scenes with MPEG-I Scene Description: XR/3D Scene Authoring (Blender)">
</p>

<p align="center">
  A Blender add-on that extends the built-in glTF exporter with the
  <a href="https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Vendor">MPEG_* glTF extensions</a>
  of MPEG-I Scene Description (ISO/IEC 23090-14).
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fwww.5g-mag.com%2Fbadges%2Fstatus%2Frt-xr-blender-exporter.json">
  <a href="https://github.com/5G-MAG/rt-xr-blender-exporter/releases"><img alt="Version"
    src="https://img.shields.io/github/v/release/5G-MAG/rt-xr-blender-exporter?label=Version"></a>
  <a href="LICENSE.md"><img alt="License: 5G-MAG Public License v1.0"
    src="https://img.shields.io/badge/License-5G--MAG%20PL%20v1.0-blue"></a>
</p>

<p align="center">
  <a href="https://www.5g-mag.com/reference-tools/xr/">Project page</a> &nbsp;&middot;&nbsp;
  <a href="https://github.com/5G-MAG/rt-xr-blender-exporter/issues">Issues</a> &nbsp;&middot;&nbsp;
  <a href="https://www.5g-mag.com/contributing">Contributing</a>
</p>

---

## At a glance

|  |  |
|---|---|
| **Implements** | [MPEG_* glTF extensions](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Vendor) of ISO/IEC 23090-14, export only (the repository does not state an edition) |
| **Part of** | [XR/3D Scenes with MPEG-I Scene Description](https://www.5g-mag.com/reference-tools/xr/), alongside [rt-xr-content](https://github.com/5G-MAG/rt-xr-content), [rt-xr-gITFast](https://github.com/5G-MAG/rt-xr-gITFast), [rt-xr-maf-native](https://github.com/5G-MAG/rt-xr-maf-native), [rt-xr-unity-player](https://github.com/5G-MAG/rt-xr-unity-player) |

## Introduction

The add-on lets Blender scenes be exported as glTF documents that use MPEG_anchor,
MPEG_texture_video and MPEG_audio_spatial, for use with the
[XR Unity Player](https://github.com/5G-MAG/rt-xr-unity-player). It works through Blender's own
glTF 2.0 exporter, and import is not supported.

More documentation is on the [project page](https://www.5g-mag.com/reference-tools/xr/).

## Specification

The extensions are those of ISO/IEC 23090-14 (MPEG-I Scene Description), which the source code
cites; the repository does not state which edition.

Clause-by-clause coverage, and what is still absent, is recorded on the project page rather than
here: <https://www.5g-mag.com/reference-tools/xr/>

## Install dependencies

The add-on is compatible with [Blender 3.6 LTS and 4.2 LTS](https://www.blender.org/download/lts/).

## Installing

### 1. Get the source code

```
git clone https://github.com/5G-MAG/rt-xr-blender-exporter.git
```

### 2. Add it to Blender's script directories

See [Blender's script directories](https://docs.blender.org/manual/en/3.6/editors/preferences/file_paths.html#script-directories).

- open `Edit > Preferences ...`
- on the left of the preferences panel, select the `File Paths` section. See the [documentation](https://docs.blender.org/manual/en/3.6/editors/preferences/file_paths.html) for more information.
- in the `Script Directories` sub-section, add the directory the git repository was cloned to (rt-xr-blender-exporter).
- save the preferences

If the add-on does not show up in the add-on list after this step, reload the scripts:
- press the *F3* key, type and select *reload scripts*.

### 3. Enable the add-on

- open `Edit > Preferences ...`
- on the left of the preferences panel, select the [`Add-ons`] section. See the [documentation](https://docs.blender.org/manual/en/3.6/editors/preferences/addons.html) for more information.
- find the 'rt-xr-blender-exporter' add-on under the 'Import-Export' add-ons.
- tick the checkbox to enable the add-on.

### Uninstalling

To uninstall, undo the installation steps. Disable only 'Import-Export: rt-xr-blender-exporter'.

> [!WARNING]
> **Do not remove Blender's built-in glTF add-on, 'Import-Export: glTF 2.0 format'**: that would remove glTF support from Blender.

## Running

This add-on [extends Blender's core glTF exporter](https://docs.blender.org/manual/en/3.6/addons/import_export/scene_gltf2.html#third-party-gltf-extensions). Import is not supported.

To use it, follow the usual glTF export procedure: *File > Export > glTF 2.0 (.glb/.gltf)*

Export of the MPEG_* extensions is enabled or disabled directly from the export panel:

![export panel options](/doc/img/export-panel-options.jpg)

### MPEG_anchor

#### Configure anchoring of a node

![configure anchor](/doc/img/anchoring-configrure-anchor.png)

1. select the node to be anchored
2. locate the XR Anchoring panel in object properties, select an anchor type and configure the anchor

The following anchor types can be configured:
- TRACKABLE_FLOOR
- TRACKABLE_VIEWER
- TRACKABLE_CONTROLLER
- TRACKABLE_PLANE
- TRACKABLE_MARKER_2D
- TRACKABLE_MARKER_GEO
- TRACKABLE_APPLICATION

#### Creating a 2D marker node

![configure anchor](/doc/img/anchoring-create-marker-2d.png)

1. locate the XR Anchoring panel (press N while the UI is focused on the 3D view)
2. select an image and hit 'create marker node', the marker 2D node is added to the scene and can now be used to configure an anchor

### MPEG_texture_video

To add a video and export it as MPEG_texture_video, first make sure that Blender's [scene output format](https://docs.blender.org/manual/en/3.6/render/output/properties/format.html) matches the frame rate of the videos used as textures.

1. Create or select a material
2. Select the shader slot which will be using the video, and make it an 'Image texture'
3. Open or Select the video to use

Every Image texture with a movie source is exported as an MPEG_texture_video extension:

![image texture](/doc/img/image-texture.jpg)

### MPEG_audio_spatial

#### Audio sources

To add an audio source to the scene:

1. Add a *[Speaker](https://docs.blender.org/manual/en/latest/render/output/audio/speaker.html)* node to the scene: *3D Viewport > Add > Speaker*
2. Add a file source to the speaker's *Sound*. The file is assumed to contain a single channel of audio (MONO).
3. Configure speaker's *Distance* parameters:
    - Max Distance
    - Attenuation (roll-off factor)
    - Distance Reference
All other parameters are ignored.

The **audio attenuation model** is set as [a scene property](https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html#data-scenes-audio) in Blender.

![audio source](/doc/img/audio-source.jpg)

![audio attenuation model](/doc/img/audio-attenuation-model.jpg)

## Development

### Debugging

The [Blender debugger for VS Code](https://github.com/AlansCodeLog/blender-debugger-for-vscode)
works well for debugging Blender add-ons and scripts; it uses
[debugpy](https://github.com/microsoft/debugpy). The glTF-Blender-IO project has a good
[introduction](https://github.com/KhronosGroup/glTF-Blender-IO/blob/main/DEBUGGING.md) to using it.

### Testing

The repository has no tests yet. They are to use the glTF-Validator to check that the output
conforms. Because import is not planned, round-trip tests are not planned either.

### Limitations

1. **Media MUST have a single track**. Handling media tracks is not possible with the Blender API alone; third-party libraries may be needed (especially to probe codecs). Another option is a panel where users configure tracks by hand, which assumes they understand the tracks in their media (error prone).
2. The media MIME type used in the video export is always 'video/mp4'.
3. MPEG_texture_video's format is assumed to be sRGB and is exported as such.
4. The [bpy.Type.Image(ID)](https://docs.blender.org/api/current/bpy.types.Image.html) API lacks information needed to implement *MPEG_texture_video*:
    - there is no way to identify which track of a media is used, so the add-on assumes one track per media
    - the frame rates involved in decoding a media are not exposed. As Blender renders video textures at the scene's output frame rate, that value is used to set the timed accessor's *suggestedUpdateRate*
5. When export fails because of invalid input (for example stereo audio, or an invalid attenuation model), there is no clear error message: the glTF is exported, but without the extensions.
6. Import is not supported, see: https://github.com/5G-MAG/rt-xr-blender-exporter/issues/1#issuecomment-1948209409

## Contributing

Contributions are welcome. How to raise an issue, fork the repository and open a pull request, and
the Contributor License Agreement required before code can be merged, are described at
<https://www.5g-mag.com/contributing>.

## License

Distributed under the 5G-MAG Public License v1.0. See [LICENSE.md](LICENSE.md).
