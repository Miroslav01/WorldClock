"""Test UK alerts"""
import time
from playsound import playsound

ALERT_SOUND = "audio/alert_1.mp3"

uk_alerts = [
    ("07:50 - UK Premarket Auction", "audio/uk_premarket_auctoin.mp3"),
    ("08:00 - London Start", "audio/london_start.mp3"),
    ("16:00 - 30min to London Close", "audio/30min_to_L_close.mp3"),
    ("16:30 - London Close", "audio/Lonodn_close.mp3"),
]

for name, sound_file in uk_alerts:
    print(f"\nPlaying: {name}")
    print(f"  alert_1.mp3 + {sound_file}")
    playsound(ALERT_SOUND)
    playsound(sound_file)
    time.sleep(1)

print("\nDone!")
