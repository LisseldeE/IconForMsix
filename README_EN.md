# IconForMsix - MSIX Icon Generator

## Overview

IconForMsix is a simple and efficient MSIX package icon generator. Just drag and drop a PNG image to automatically generate 40 different sized icon files, perfectly adapted for Microsoft Store app packaging. Uses supersampling technology to ensure smooth icon edges without jagged edges.

## Screenshots

![Main Interface](https://lisseldee.github.io/images/webp/5-1.webp)

## Project Info

- **Project Name**: IconForMsix
- **Author**: Lisselde_E
- **Homepage**: https://lisseldee.github.io/#5
- **Repository**: https://github.com/LisseldeE/IconForMsix

## Features

### Icon Generation
- Drag and drop PNG image to generate 40 sizes of icons
- Supports StoreLogo, Square44x44Logo, Square71x71Logo, Square150x150Logo, Square310x310Logo, Wide310x150Logo and more
- Supersampling technology reduces edge aliasing
- 96dpi standard output, meets Microsoft Store requirements

### Interface Interaction
- Simple and intuitive drag-and-drop operation
- Chinese/English interface switching
- Automatic system language detection
- Automatic uppercase conversion for English letters
- Background thread processing prevents UI freezing

### User Experience
- Bottom notification toast, non-intrusive
- Fixed window height, no layout jumping
- Windows taskbar icon displays correctly

## How to Use

1. Drag and drop a PNG image to the drop area
2. Enter the app name (English letters auto-convert to uppercase)
3. Click the save button to choose save location
4. Assets folder and 40 icons are generated automatically

## Icon Specifications

| Type | Count | Description |
|------|-------|-------------|
| StoreLogo | 5 | Store Logo series |
| Square44x44Logo | 15 | 44x44 icon series (including targetsize) |
| Square71x71Logo | 5 | 71x71 icon series |
| Square150x150Logo | 5 | 150x150 icon series |
| Square310x310Logo | 5 | 310x310 icon series |
| Wide310x150Logo | 5 | Wide icon series |

## Changelog

### 2026.7.16 R1

**#02**
- Optimized some details

See [Changelog](https://github.com/LisseldeE/IconForMsix/blob/main/CHANGELOG.md) for details

## Tech Stack

- Python 3.x
- PySide6
- Pillow

## Installation & Running

### System Requirements
- Python 3.8 or higher
- Windows 10 or higher

### Install Dependencies
```bash
pip install PySide6 Pillow
```

### Run
```bash
python IconForMsix.py
```

## License

This project is licensed under the MIT License, see [LICENSE](https://github.com/LisseldeE/IconForMsix/blob/main/LICENSE) file.

## Feedback

If you have any questions or suggestions, feel free to submit an Issue!