# In adiutorium Frescobaldi extension

[Extension][ext] for the [Frescobaldi][fresco] editor
assisting common workflows of the [In adiutorium][ia] project.

For a long time a [customized fork][fork] of the editor has been used,
now when Frescobaldi 3 has an extensions API
the customizations were extracted to an extension.

## Installation

- In Frescobaldi `Preferences`, section `Extensions`
  - enable extensions
  - set up your extensions directory
- `git clone` this repository
- in the extensions directory create a symlink to the cloned repo
- restart Frescobaldi, the extension will show up in `Preferences > Extensions`; make sure it's enabled (checkbox checked)

## Usage

The extension provides additional actions in

- `Tools` menu
- editor context menu
- editor tab context menu

The In adiutorium project consists of a large amount of small simple
scores connected by relations - partly implicit
(relation between an "official" score and its development variants
in the `variationes/` directory), partly explicit
(relation to a melody source encoded in the `fial` header field).
Most of the extension's functionality helps navigating this network
of relations.

[fresco]: https://github.com/frescobaldi/frescobaldi
[ext]: https://github.com/frescobaldi-extensions/
[fork]: https://github.com/igneus/frescobaldi
[ia]: https://github.com/igneus/In-adiutorium
