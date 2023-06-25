# MUGEN for Sublime Text 4

Language utility package for MUGEN, a fighting game engine. Includes support for IKEMEN.

### Installation

Just `git clone` it to the Packages folder. I can't be bothered to host it on packagecontrol.

### Features

- A port of some snippets from Fighter Factory 3
- Auto completions and hover for SCTRLs and triggers
- Syntax highlighting for CNS/CMD/DEF and AIR
- Syntax highlighting for IKEMEN ZSS (Zantei State Script)
- Build targets for running MUGEN and sndmaker/sprmake2 (config file allows you to change which version of MUGEN to run)
- Build targets for running IKEMEN

### Changelog

#### 18-06-2023 - 2.2.0
- IKEMEN: Rewrite ZSS syntax
- Fix `<prefix>n` (i.e. `F2, 3`) CNS number detection
- Highlight argument inside const, map, stagevar, gethitvar triggers as string

#### 18-06-2023 - 2.1.0
- Add "KFM vs KFM" build target
- Add "Storyboard" build target
- Improve CNS trigger syntax highlighting
- MUGEN: Properly highlight A1 in AIR
- MUGEN: Add .st to CNS syntax file extension list
- MUGEN: Add symbol navigation to CNS sections

#### 04-04-2023 - 2.0.0
- Add `-c`, `-f`, `-p` to sprmake2 build target
- Make base command class check `ikemen_path` if needed
- Move hovers and auto completions to Python
- Reordered changelog lists
- Add "Normalize" command for CNS, which removes comments, extra spaces and extra newlines
- IKEMEN: Ability to run IKEMEN from Lua files
- IKEMEN: Add hovers and autocomplete for IKEMEN features

#### 06-09-2022 - 1.3.0
- Add support for subfolders in chars/
- Adjustable KFM config
- Output window tells execution time when finished
- IKEMEN: Refine ZSS operator detection

#### 25-08-2022 - 1.2.0
- IKEMEN: Add build targets
- IKEMEN: Add ZSS syntax highlighting
- MUGEN: Add commonly used motion snippets
- MUGEN: Add config for running sprmake2/sndmaker in file's directory rather than in MUGEN's directory
- MUGEN: Add tooltips for SCTRLs

#### 19-08-2022 - 1.1.2
- Refine number syntax in CNS 
- Replace SCTRL and trigger snippets with autogenerated ones from 1.0 docs for Sublime Text 4

#### 09-08-2022 - 1.1.1
- Rewrite AIR syntax from CNS rewrite
- Rewrite CNS syntax

#### 24-07-2022 - 1.1.0
- Added stage build target
- Changelog now uses SemVer

#### 03-05-2022 - 1.0.0
- Added changelog to README
- Added Python modules for build systems, effectively redoing the entire thing
- Added the ability to change user config through Preferences > Package Settings > MUGEN
- Package now has a config file instead of relying on `PATH`

#### 10-01-2022 - 0.0.2
- Improved comment detection for CNS

#### 19-12-2021 - 0.0.1
- Initial commit