"""
Time Zone Widget for Windows
Displays current time in Sofia, London, Chicago, and New York
Bloomberg Terminal style theme
"""

import tkinter as tk
from datetime import datetime
from zoneinfo import ZoneInfo
import threading
import win32com.client
import os
import sys
from playsound import playsound

# Define your time zones (Chicago before New York)
ZONES = [
    ("Sofia", "Europe/Sofia"),
    ("London", "Europe/London"),
    ("Chicago", "America/Chicago"),
    ("New York", "America/New_York"),
]

# Bloomberg Terminal colors
BG_COLOR = "#000000"
TEXT_COLOR = "#FF6600"  # Bloomberg orange
TITLE_BG = "#1a1a1a"
TITLE_FG = "#FF6600"

# Path to sound files (handles both script and frozen executable)
if getattr(sys, 'frozen', False):
    SOUND_DIR = sys._MEIPASS
else:
    SOUND_DIR = os.path.dirname(os.path.abspath(__file__))

# Attention sound (plays before all announcements)
ALERT_SOUND = os.path.join(SOUND_DIR, "alert_1.mp3")

# UK session specific sounds
UK_PREMARKET_AUCTION = os.path.join(SOUND_DIR, "uk_premarket_auctoin.mp3")
UK_LONDON_START = os.path.join(SOUND_DIR, "london_start.mp3")
UK_30MIN_TO_CLOSE = os.path.join(SOUND_DIR, "30min_to_L_close.mp3")
UK_LONDON_CLOSE = os.path.join(SOUND_DIR, "Lonodn_close.mp3")

# NY session specific sounds
NY_30MIN_TO_OPEN = os.path.join(SOUND_DIR, "30mintostartNY.mp3")
NY_START = os.path.join(SOUND_DIR, "NY_start.mp3")
NY_30MIN_TO_CLOSE = os.path.join(SOUND_DIR, "30min_to_close_NY.mp3")
NY_CLOSE = os.path.join(SOUND_DIR, "NY_close.mp3")

class TimeZoneWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("World Clock")
        self.root.configure(bg=BG_COLOR)
        self.root.attributes("-topmost", True)  # Always on top
        self.root.resizable(False, False)
        self.root.overrideredirect(True)  # Remove default title bar

        self.labels = {}
        self.title_label = None  # Reference to title label for date updates
        self.last_alert_date = None  # Track date for resetting alerts

        # Alert flags for each notification
        self.alerts_played = {
            # UK alerts
            "uk_0750": False,   # Premarket auction
            "uk_0800": False,   # London start
            "uk_1600": False,   # 30min to London close
            "uk_1630": False,   # London close
            # US alerts
            "ny_0900": False,   # 30min to NY open
            "ny_0930": False,   # NY trading day starts
            "ny_1530": False,   # 30min to NY close
            "ny_1600": False,   # NY trading day ends
        }

        self._drag_data = {"x": 0, "y": 0}

        self.create_title_bar()
        self.create_ui()
        self.position_bottom_right()
        self.update_times()

    def get_ordinal_suffix(self, day):
        """Get ordinal suffix for day (1st, 2nd, 3rd, etc.)"""
        if 11 <= day <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    def get_formatted_date(self):
        """Format date as 'Mon 15th April' with short months for long names"""
        now = datetime.now()
        day = now.day
        suffix = self.get_ordinal_suffix(day)
        weekday = now.strftime("%a")

        # Short month names for long months
        month_map = {
            "January": "Jan", "February": "Feb", "September": "Sep",
            "October": "Oct", "November": "Nov", "December": "Dec"
        }
        month = now.strftime("%B")
        month = month_map.get(month, month)

        return f"{weekday} {day}{suffix} {month}"

    def position_bottom_right(self):
        """Position window at bottom right corner of screen"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Position with small margin from edges (accounting for taskbar)
        x = screen_width - window_width - 10
        y = screen_height - window_height - 50
        self.root.geometry(f"+{x}+{y}")

    def create_title_bar(self):
        # Thin classic Windows-style title bar
        title_bar = tk.Frame(self.root, bg=TITLE_BG, height=20)
        title_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_bar.grid_propagate(False)

        # Close button on the right
        close_btn = tk.Label(
            title_bar,
            text="×",
            font=("Segoe UI", 10, "bold"),
            fg=TITLE_FG,
            bg=TITLE_BG,
            cursor="hand2"
        )
        close_btn.pack(side="right", padx=5)
        close_btn.bind("<Button-1>", lambda e: self.root.destroy())
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg="#ff0000"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg=TITLE_FG))

        # Date label centered
        self.title_label = tk.Label(
            title_bar,
            text=self.get_formatted_date(),
            font=("Segoe UI", 9),
            fg=TITLE_FG,
            bg=TITLE_BG
        )
        self.title_label.pack(expand=True)

        # Make title bar draggable
        title_bar.bind("<Button-1>", self.start_drag)
        title_bar.bind("<B1-Motion>", self.do_drag)
        self.title_label.bind("<Button-1>", self.start_drag)
        self.title_label.bind("<B1-Motion>", self.do_drag)

    def start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self._drag_data["x"]
        y = self.root.winfo_y() + event.y - self._drag_data["y"]
        self.root.geometry(f"+{x}+{y}")

    def create_ui(self):
        for i, (city, _) in enumerate(ZONES):
            row = i + 1  # Account for title bar

            # City name
            city_label = tk.Label(
                self.root,
                text=city,
                font=("Consolas", 11),
                fg=TEXT_COLOR,
                bg=BG_COLOR,
                anchor="w",
                width=12
            )
            city_label.grid(row=row, column=0, padx=(10, 5), pady=(8 if i == 0 else 2, 2))

            # Time display
            time_label = tk.Label(
                self.root,
                text="--:--:--",
                font=("Consolas", 12, "bold"),
                fg=TEXT_COLOR,
                bg=BG_COLOR,
                anchor="e",
                width=10
            )
            time_label.grid(row=row, column=1, padx=(5, 10), pady=(8 if i == 0 else 2, 2))

            self.labels[city] = time_label

        # Add bottom padding
        spacer = tk.Frame(self.root, height=8, bg=BG_COLOR)
        spacer.grid(row=len(ZONES) + 1, column=0, columnspan=2)

    def play_attention_sound(self):
        """Play attention sound once"""
        def play_sound():
            playsound(ALERT_SOUND)
        threading.Thread(target=play_sound, daemon=True).start()

    def play_alert_then_sound(self, sound_file):
        """Play alert sound then a specific sound file"""
        def play_sounds():
            playsound(ALERT_SOUND)
            playsound(sound_file)
        threading.Thread(target=play_sounds, daemon=True).start()

    def speak(self, text):
        """Text-to-speech announcement with female voice"""
        def say():
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            voices = speaker.GetVoices()
            for i in range(voices.Count):
                if "Zira" in voices.Item(i).GetDescription():
                    speaker.Voice = voices.Item(i)
                    break
            speaker.Speak(text)
        threading.Thread(target=say, daemon=True).start()

    def announce_with_sound(self, text):
        """Play alert sound once then speak announcement with female voice"""
        def do_announce():
            # Play alert sound once
            playsound(ALERT_SOUND)
            # Speak the announcement
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            voices = speaker.GetVoices()
            for i in range(voices.Count):
                if "Zira" in voices.Item(i).GetDescription():
                    speaker.Voice = voices.Item(i)
                    break
            speaker.Speak(text)
        threading.Thread(target=do_announce, daemon=True).start()

    def reset_daily_alerts(self, current_date):
        """Reset all alerts for a new day"""
        if self.last_alert_date != current_date:
            for key in self.alerts_played:
                self.alerts_played[key] = False
            self.last_alert_date = current_date

    def check_market_alerts(self):
        """Check for all market alerts"""
        london_tz = ZoneInfo("Europe/London")
        ny_tz = ZoneInfo("America/New_York")
        london_time = datetime.now(london_tz)
        ny_time = datetime.now(ny_tz)
        current_date = london_time.date()

        # Reset alerts on new day
        self.reset_daily_alerts(current_date)

        # Only trigger on weekdays
        if london_time.weekday() >= 5:
            return

        # === UK ALERTS ===

        # UK 07:50 - Premarket auction
        if (london_time.hour == 7 and london_time.minute == 50 and london_time.second == 0
                and not self.alerts_played["uk_0750"]):
            self.alerts_played["uk_0750"] = True
            self.play_alert_then_sound(UK_PREMARKET_AUCTION)

        # UK 08:00 - London start
        if (london_time.hour == 8 and london_time.minute == 0 and london_time.second == 0
                and not self.alerts_played["uk_0800"]):
            self.alerts_played["uk_0800"] = True
            self.play_alert_then_sound(UK_LONDON_START)

        # UK 16:00 - 30min to London close
        if (london_time.hour == 16 and london_time.minute == 0 and london_time.second == 0
                and not self.alerts_played["uk_1600"]):
            self.alerts_played["uk_1600"] = True
            self.play_alert_then_sound(UK_30MIN_TO_CLOSE)

        # UK 16:30 - London close
        if (london_time.hour == 16 and london_time.minute == 30 and london_time.second == 0
                and not self.alerts_played["uk_1630"]):
            self.alerts_played["uk_1630"] = True
            self.play_alert_then_sound(UK_LONDON_CLOSE)

        # === US/NY ALERTS ===

        # NY 09:00 - 30min to NY open
        if (ny_time.hour == 9 and ny_time.minute == 0 and ny_time.second == 0
                and not self.alerts_played["ny_0900"]):
            self.alerts_played["ny_0900"] = True
            self.play_alert_then_sound(NY_30MIN_TO_OPEN)

        # NY 09:30 - NY trading day starts
        if (ny_time.hour == 9 and ny_time.minute == 30 and ny_time.second == 0
                and not self.alerts_played["ny_0930"]):
            self.alerts_played["ny_0930"] = True
            self.play_alert_then_sound(NY_START)

        # NY 15:30 - 30min to NY close
        if (ny_time.hour == 15 and ny_time.minute == 30 and ny_time.second == 0
                and not self.alerts_played["ny_1530"]):
            self.alerts_played["ny_1530"] = True
            self.play_alert_then_sound(NY_30MIN_TO_CLOSE)

        # NY 16:00 - NY trading day ends
        if (ny_time.hour == 16 and ny_time.minute == 0 and ny_time.second == 0
                and not self.alerts_played["ny_1600"]):
            self.alerts_played["ny_1600"] = True
            self.play_alert_then_sound(NY_CLOSE)

    def update_times(self):
        for city, tz_name in ZONES:
            tz = ZoneInfo(tz_name)
            current_time = datetime.now(tz).strftime("%H:%M:%S")
            self.labels[city].config(text=current_time)

        # Update date in title bar
        self.title_label.config(text=self.get_formatted_date())

        # Check for market alerts
        self.check_market_alerts()

        # Update every second
        self.root.after(1000, self.update_times)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    widget = TimeZoneWidget()
    widget.run()
