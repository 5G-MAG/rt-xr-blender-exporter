# rt-xr-blender-exported

This Blender add-on adds support for [MPEG_* glTF extensions](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Vendor) to the built-in gltf exporter.


## Installation

The addon is compatible with Blender 3.6.


### 1. Get the source code:

```
git clone https://github.com/5G-MAG/rt-xr-blender-exporter.git .
```

### 2. Add it to [Blender's script directories](https://docs.blender.org/manual/en/3.6/editors/preferences/file_paths.html#script-directories):

- open `Edit > Preferences ...`
- on the left of the preferences panel, select the `File Paths` section
- find the `Script Directories` sub-section add the directory where the git repo was cloned to the list (rt-xr-blender-exporter).
- save the preferences

If the add-on isn't showing show up in the add-on list after this step, try reloading the scripts: 
- hit the *F3* key, type and select *reload scripts*.


### 3. Enable the add-on

In Blender's preferences panel, select the [`Add-ons` section]((https://docs.blender.org/manual/en/3.6/editors/preferences/addons.html)). 

The add-on is found under the 'Import-Export' and is named 'glTF 2.0 MPEG extensions'.

Tick the checkbox to enable the add-on.


### Uninstalling

To uninstall, simply undo the installation steps. Make sure to disable only 'Import-Export: glTF 2.0 MPEG extensions'.

/!\ **DO NOT remove Blender's built-in glTF add-on: 'Import-Export: glTF 2.0 format'** as it would remove support for gltf in blender.


## Usage

This add-on [extends Blender's core gltf exporter](https://docs.blender.org/manual/en/3.6/addons/import_export/scene_gltf2.html#third-party-gltf-extensions). Import is currently not supported.

To use it, follow the usual glTF export procedure: *File > Export > glTF 2.0 (.glb/.gltf)*

Exporting MPEG_* extension can be enabled or disabled from the export panel directly:

![export panel options](/doc/img/export-panel-options.jpg)



### MPEG_texture_video

To add a video and export it as MPEG_texture_video, first make sure that the blender's [scene output format](https://docs.blender.org/manual/en/3.6/render/output/properties/format.html) matches the framerate of the videos used as texture.

1. Create or select a material
2. Select the shader slot which will be using the video, and make it an 'Image texture'
3. Open or Select the video to use

All Image textures with a movie source are exported as MPEG_texture_video extensions:

![image texture](/doc/img/image-texture.jpg)

### MPEG_audio_spatial

#### audio sources 

To add an audio source to the scene:

1. Add a *[Speaker](https://docs.blender.org/manual/en/latest/render/output/audio/speaker.html)* node to the scene: *3D Viewport > Add > Speaker*
2. Add a file source to the speaker's *Sound*. The file is assumed to contain a single channel of audio (MONO).
3. Configure speaker's *Distance* parameters:
    - Max Distance
    - Attenuation (roll-off factor)
    - Distance Reference
All other parameters are ignored.

The **audio attenuation model** is configured as [a scene property](https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html#data-scenes-audio) in Blender.

![audio source](/doc/img/audio-source.jpg)

![audio attenuation model](/doc/img/audio-attenuation-model.jpg)

## Development

### Debugging

The [blender debugger for vscode](https://github.com/AlansCodeLog/blender-debugger-for-vscode) is a great way to debug blender addons and scripts.
The glTF-Blender-IO plugin provides a good [introduction](https://github.com/KhronosGroup/glTF-Blender-IO/blob/main/DEBUGGING.md) on using it.
The vscode plugin for Blender works well for debugging, it uses [debugpy](https://github.com/microsoft/debugpy).

### Testing

Testing will to use gltf-validator to ensure conformance of the output.

As support for importing is not planned, there is currently no plan to implement round-trip tests.


## Known issues

1. **Media MUST have a single track**. handling media tracks is not possible with Blender API only, third party libraries may be required (especialy to probe codecs). Another option is to add a panel for users to manually configure tracks assuming they know understand the tracks in their media (error prone).
2. The media mime type used in the video export is always 'video/mp4'
3. MPEG_texture_video's format is assumed to be sRGB and is exported as such
4. The [bpy.Type.Image(ID)](https://docs.blender.org/api/current/bpy.types.Image.html) API is missing informations that are needed to implement *MPEG_texture_video*:
    - there is no way to identify which track of a media is being used, therefore the add-on currently assumes there is only one track per media
    - the framerates involved in decoding a media are not exposed. As Blender renders video textures at the scene's output framerate, currently that value is used to set the timed accessor's *suggestedUpdateRate*
5. when export fails because of invalid input (eg. stereo audio, invalid attenuation model ...) there is no easy to clear error message. It exports gltf but without the extensions.
6. audio attenuation function names in the json schema doesn't match the values in FDIS


## License

Licensed under the License terms and conditions for use, reproduction, and distribution of 5GMAG software (the “License”).

You may not use this file except in compliance with the License. You may obtain a copy of the License at https://www.5g-mag.com/license .

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.