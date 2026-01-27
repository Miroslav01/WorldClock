# WorldClock

A Bloomberg Terminal styled timezone widget for Windows with market open/close voice alerts.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## Features

- **Multi-timezone display**: Sofia, London, Chicago, New York
- **Bloomberg Terminal theme**: Black background with orange text
- **Market alerts with voice notifications**:
  - NYSE open (9:30 AM ET) - 3 bells + voice
  - NYSE 30-min warning (3:30 PM ET) - 1 bell + voice
  - NYSE close (4:00 PM ET) - 2 bells + voice
  - London FX/Futures 15-min warning (3:45 PM UK)
  - London FX/Futures close (4:00 PM UK)
  - London Stock Exchange close (4:30 PM UK)
- **Always-on-top** draggable window
- **Auto-start** with Windows
- **Date display** in title bar (e.g., "Mon 27th Jan")

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/Miroslav01/WorldClock.git
   cd WorldClock
   ```

2. Install dependencies:
   ```bash
   pip install pywin32
   ```

3. Run:
   ```bash
   python timezone_widget.py
   ```

### Build Executable

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "bell.wav;." --name "WorldClock" timezone_widget.py
```

The executable will be in the `dist/` folder.

## Requirements

- Windows 10/11
- Python 3.11+ (for running from source)
- pywin32

## License

MIT
