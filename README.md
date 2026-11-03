# Rigs of Rods for iOS

[![latest-ipa](https://img.shields.io/github/v/tag/wayl-t/Rigs-of-Rods-for-iOS/latest-ipa?label=latest-ipa&color=blue)](https://github.com/wayl-t/Rigs-of-Rods-for-iOS/releases/tag/latest-ipa)
[![Build](https://img.shields.io/github/actions/workflow/status/wayl-t/Rigs-of-Rods-for-iOS/build-ror-ios.yml?branch=main)](https://github.com/wayl-t/Rigs-of-Rods-for-iOS/actions)
[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

An unofficial native port of [Rigs of Rods](https://www.rigsofrods.org/), the soft-body vehicle simulator, to iPhone and iPad (arm64). The game can be sideloaded as an IPA.

The original game and all credit belong to the [Rigs of Rods team](https://www.rigsofrods.org/credits).

---

## Download the latest version

The latest build is published in the **latest-ipa** release and is automatically replaced after each successful CI run:

| File | Description | Link |
| --- | --- | --- |
| **RoR-ios.ipa** | Full game, about 115 MB | [Download](https://github.com/wayl-t/Rigs-of-Rods-for-iOS/releases/download/latest-ipa/RoR-ios.ipa) |
| **RoR-ios-lite.ipa** | Lite build, about 43 MB | [Download](https://github.com/wayl-t/Rigs-of-Rods-for-iOS/releases/download/latest-ipa/RoR-ios-lite.ipa) |
| All releases | Version history | [Releases](https://github.com/wayl-t/Rigs-of-Rods-for-iOS/releases) |

Install by sideloading with [SideStore](https://sidestore.io/), [Sideloadly](https://sideloadly.io/), or [ESIGN](https://esign.yyyue.xyz/). With a free Apple ID, the app must be re-signed every 7 days.

## Status

- Full game runs on device: menus, map and vehicle selection, settings, and driving
- Touch controls: steering, pedals, vehicle systems panel, and free camera
- Custom mods can be loaded from the Files app's `content` folder without rebuilding
- Built-in mod repository: downloads use `NSURLSession`, not libcurl
- The IPA is built and packaged entirely on free GitHub Actions macOS runners

## Features and implementation

### On-screen controls

The driving controls are analog: sliders and a gauge rather than on/off buttons.

- **Pedal slider** (right edge) — drag up from the rest mark for throttle, 0–100%; drag down for brake, 0–100%. The thumb springs back to rest when you let go.
- **Turn slider** (bottom left) — drag left or right to steer; it springs back to center.
- **Gear box** (left of the pedal slider) — tap **+** or **−** to shift; the middle shows the current gear.
- **Speed gauge** (top right) — needle plus a digital km/h read-out. The scale grows in steps of 60 km/h as you speed up. Tap it to open the vehicle panel.
- **Top-left keys** — **≡** main menu, **S** spawn a vehicle, **R** repair/reset, **E** engine (tap to start: it switches the ignition on and holds the starter until the engine runs; tap again to stop), **C** change camera.
- **Vehicle panel** — large **LIGHTS / DRIVE / EXTRAS** pages for lights, horn, parking brake, turn signals, gearbox modes and more.
- In free-camera mode, use a floating joystick, swipe across the scene to look around, and use the altitude buttons.
- Controls use light, translucent glass-like styling with dark labels to avoid obscuring the 3D scene.

### Compact HUD

While driving, the speed gauge and gear box (see above) are the read-outs. The older compact card, which also showed RPM, an engine-load bar and lamp indicators for lights and turn signals, is still in the code but switched off; it is still used for the free-camera label.

### Free camera instead of an on-foot character

The player mesh does not render with GLES2. The logical player object remains for game code, while the on-foot character is replaced by a free camera.

### Custom mods

Place any vehicle or map `.zip` file in **Files › On My iPhone › Rigs of Rods › content**. The game automatically mounts the archive. File sharing is enabled for the app.

### Key fixes based on device logs

- Black sky → Sandstorm is selected by default and shadows are disabled.
- Touches did not reach menus → added a touch-to-mouse bridge for ImGui.
- Crash when spawning soft-body vehicles → fixed `GLES2HardwareBuffer::readData()` in OGRE so the buffer is bound before `glMapBufferRangeEXT`.
- Vehicle materials selected the unusable Cg `nicemetal` variant → enabled `gfx_alt_actor_materials`.
- Repository mods failed to install → `.part` files are renamed to `.zip` using `std::filesystem::rename`, with a fallback.

## How it works

This repository builds the game on GitHub Actions macOS runners, without requiring a Mac or a paid Apple Developer account:

1. **`build-ios-deps.yml`** cross-compiles dependencies (OGRE, OIS, MyGUI, AngelScript, SocketW, and others) into a single SDK artifact.
2. **`build-ror-ios.yml`** downloads that SDK, applies `patches/ror/apply_ios_patches.py` to the RoR source, builds for arm64, packages the app with ad-hoc signing, and publishes the IPA to the `latest-ipa` release.
3. **`patches/verify_ipa.py`** runs about 25 checks on the finished IPA, including bundle structure, `skeleton.zip`, MyGUI shaders, RTSS, icons, and touch controls.

All changes to the RoR source are collected in `patches/ror/apply_ios_patches.py`. Each patch is guarded by `#ifdef ROR_PLATFORM_IOS`, so desktop builds are unaffected.

The separate **`build-ipa.yml`** workflow builds only a pipeline-test app (tag: `pipeline-check`); it does not contain the game.

## Installation

1. Open the RoR-ios.ipa link in Safari on your iPhone, or download the file to a computer and transfer it to your device.
2. Install it with SideStore, Sideloadly, or ESIGN using a regular Apple ID.
3. With a free Apple ID, renew the signing every 7 days.

> If the release page is slow to load, download the IPA from the Actions artifacts with `gh run download`.

## On-device diagnostics

If the game crashes or fails to render, inspect **Files › On My iPhone › Rigs of Rods › ror-trace.log**. The log is written line by line and preserves its tail across crashes. It includes startup, fatal, and crash entries, as well as CVar values after `RoR.cfg` is loaded.

## Limitations

- Shadows are not rendered: PSSM is not supported on the current GLES2 path.
- Only the Sandstorm sky is available; Caelum and SkyX are not built.
- Multiplayer has not been tested on device (SocketW is built without OpenSSL).
- Sideloading with a free Apple ID requires re-signing every 7 days.

## Repository layout

```text
.github/workflows/
  build-ror-ios.yml         Main build: RoR → IPA → Release
  build-ios-deps.yml        Reusable iOS dependencies
  build-ipa.yml             Pipeline smoke test; not the game
patches/
  ror/apply_ios_patches.py  iOS patches for the RoR source
  ios/make_app_icon.py      Icon generator
  verify_ipa.py             IPA validation checks
docs/RELEASE_NOTES.md       Release notes for the latest-ipa page
PORT_FINDINGS.md            Detailed analysis of issues found
```

## Roadmap

- [x] Actions → IPA → Release → sideload pipeline
- [x] Game runs on device: menus, maps, vehicles, and controls
- [x] Custom mods through `content` and the built-in repository
- [x] Compact HUD with lights and turn-signal indicators
- [x] Light, translucent controls
- [x] SYS opens the full desktop menu
- [ ] Multiplayer on device (not tested)
- [ ] Shadows: PSSM on GLES2 or an alternative
- [ ] iPad layout

## Credits

- **Original game:** [Rigs of Rods](https://www.rigsofrods.org/) by the [Rigs of Rods team](https://www.rigsofrods.org/credits), GPLv3.
- **iOS port and build pipeline:** this repository.

## License

Rigs of Rods is distributed under GPLv3, and this port is too. App Store publication is not possible under the license terms, but the app can be sideloaded.
