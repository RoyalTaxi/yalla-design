# yalla-design

Canonical design source for Yalla SDKs.

This repo owns design inputs that must stay consistent across:

- `yalla-sdk` Compose Multiplatform design module
- `yalla-sdk-android` native Android design resources/helpers
- `yalla-sdk-ios` native iOS design resources/helpers

The platform repos should consume generated outputs. Design changes should be
made here first, then generated into each platform's native format.

## Scope

The design system intentionally stays small:

```text
tokens/colors.json
    +-> Compose Multiplatform ColorScheme source
    +-> Android native color resources/helpers
    +-> iOS native YallaColors.xcassets .colorset resources

tokens/fonts.json
    +-> Compose Multiplatform FontScheme source
    +-> Android native font helpers
    +-> iOS native font helpers

tokens/themed-images.json
    +-> Compose Multiplatform ThemedImage registry
    +-> Android drawable / drawable-night mapping
```

This repo does not own strings, copy, icons, or general image/font binaries.
Those assets live in `yalla-resources`; this repo owns the design meaning and
mapping around them. iOS image light/dark appearance mapping is handled by
`yalla-resources` through asset catalog appearances.

## Commands

Validate canonical token files:

```bash
python3 tools/yalla_design.py validate
```

Generate sample outputs into `build/generated`:

```bash
python3 tools/yalla_design.py generate --out build/generated
```

Sync generated outputs into sibling SDK repos:

```bash
python3 tools/yalla_design.py sync
```

The default sync destinations are:

- `../yalla-sdk`
- `../yalla-sdk-android`
- `../yalla-sdk-ios`

Override them when needed:

```bash
python3 tools/yalla_design.py sync \
  --cmp-root /path/to/yalla-sdk \
  --android-root /path/to/yalla-sdk-android \
  --ios-root /path/to/yalla-sdk-ios
```

Run generator checks:

```bash
python3 tools/yalla_design.py check
```

Run unit tests:

```bash
python3 -m unittest discover -s tools -p 'test_*.py'
```
