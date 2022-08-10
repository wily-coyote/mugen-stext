# MUGEN for Sublime Text 3

Language utility package for MUGEN, a fighting game engine.

### Installation

Just `git clone` it to the Packages folder. I can't be bothered to host it on packagecontrol.

### Features

- A port of all the snippets and state controllers from Fighter Factory 3
- Syntax highlighting for CNS/CMD/DEF and AIR
- Build targets for running MUGEN and sndmaker/sprmake2 (config file allows you to change which version of MUGEN to run)
- Autocomplete for state controllers and their parameters

### TODO

- More snippets (things like QCB, QCF, see `kfm.cns`)

### Changelog

#### 09-08-2022 - 1.2.0
- Rewrite CNS syntax
- Rewrite AIR syntax from CNS rewrite

#### 24-07-2022 - 1.1.0
- Added stage build target
- Changelog now uses SemVer

#### 03-05-2022 - 1.0.0
- Added Python modules for build systems, effectively redoing the entire thing
- Package now has a config file instead of relying on `PATH`
- Added changelog to README
- Added the ability to change user config through Preferences > Package Settings > MUGEN

#### 10-01-2022 - 0.0.2
- Improved comment detection for CNS

#### 19-12-2021 - 0.0.1
- Initial commit