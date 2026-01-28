# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Added new directive `list-table-thumbs` ([#72](https://github.com/Robpol86/sphinx-thumb-image/issues/72))

## [0.3.0] - 2026-01-26

### Added

- `:is-animated:` directive option ([#66](https://github.com/Robpol86/sphinx-thumb-image/issues/66)).

### Removed

- Automatic detection of animated image files. Use `:is-animated:` instead.

### Fixed

- Docs not rebuilding when `thumb_image_default_target` is changed ([#60](https://github.com/Robpol86/sphinx-thumb-image/issues/60)).

## [0.2.0] - 2026-01-24

### Added

- `thumb_image_default_target` Sphinx config ([#48](https://github.com/Robpol86/sphinx-thumb-image/issues/48)).
- Support for absolute paths within SOURCE_DIR ([#49](https://github.com/Robpol86/sphinx-thumb-image/issues/49)).
- `:no-resize:` directive option ([#57](https://github.com/Robpol86/sphinx-thumb-image/issues/57)).
- Support for callables in `thumb_image_target_format_substitutions` ([#26](https://github.com/Robpol86/sphinx-thumb-image/issues/26)).
- Support for string slicing in format substitutions.

### Removed

- Support for specifying absolute paths to images outside of SOURCE_DIR.

## [0.1.0] - 2026-01-06

### Added

- Initial release.
