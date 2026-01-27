# WorldClock

A Bloomberg Terminal styled timezone widget for Windows with market open/close voice alerts.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## Features

- **Multi-timezone display**: Sofia, London, Chicago, New York
- **Bloomberg Terminal theme**: Black background with orange text
- **Always-on-top** draggable window
- **Auto-start** with Windows
- **Date display** in title bar (e.g., "Mon 27th Jan")
- **Voice alerts** with bell sounds (female voice - Microsoft Zira)

### UK Market Alerts

| Time (UK) | Alert |
|-----------|-------|
| 07:50 | UK premarket auction |
| 08:00 | UK trading day starts |
| 15:30 | 30 minutes to London FX and futures close |
| 16:00 | London FX and Futures close |
| 16:30 | UK trading day ends / LSE close |

### US/NY Market Alerts

| Time (ET) | Alert |
|-----------|-------|
| 09:00 | 30 minutes to NY trading session |
| 09:30 | US New York trading day starts |
| 15:30 | 30 minutes to end of NY trading day |
| 16:00 | US New York trading day ends |

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

### Add to Windows Startup

The executable can be added to Windows startup by placing a shortcut in:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

## Requirements

- Windows 10/11
- Python 3.11+ (for running from source)
- pywin32

## License

MIT
