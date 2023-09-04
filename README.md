# In adiutorium Frescobaldi extension

[Extension][ext] for the [Frescobaldi][fresco] editor
assisting common workflows of the [In adiutorium][ia] project.

For a long time a [customized fork][fork] of the editor has been used,
now when extensions API was added to Frescobaldi 3
the customizations are being extracted to an extension.

## Installation

- In Frescobaldi `Preferences`, section `Extensions`
  - enable extensions
  - set up your extensions directory
- `git clone` this repository
- in the extensions directory create a symlink to the cloned repo
- restart Frescobaldi, the extension will show up in `Preferences > Extensions`; make sure it's enabled (checkbox checked)

## Usage

The extension provides actions in the editor context menu
and `Tools` menu.

[fresco]: https://github.com/frescobaldi/frescobaldi
[ext]: https://github.com/frescobaldi-extensions/
[fork]: https://github.com/igneus/frescobaldi
[ia]: https://github.com/igneus/In-adiutorium
