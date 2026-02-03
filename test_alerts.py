"""Test script to verify all MP3 alerts are working"""
import os
import time
from playsound import playsound

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
ALERT_SOUND = os.path.join(AUDIO_DIR, "alert_1.mp3")

# All alerts to test (UK + NY)
alerts = [
    # UK alerts
    ("UK 07:50 - Premarket Auction", "uk_premarket_auctoin.mp3"),
    ("UK 08:00 - London Start", "london_start.mp3"),
    ("UK 16:00 - 30min to London Close", "30min_to_L_close.mp3"),
    ("UK 16:30 - London Close", "Lonodn_close.mp3"),
    # NY alerts
    ("NY 09:00 - 30min to NY Open", "30mintostartNY.mp3"),
    ("NY 09:30 - NY Start", "NY_start.mp3"),
    ("NY 15:30 - 30min to NY Close", "30min_to_close_NY.mp3"),
    ("NY 16:00 - NY Close", "NY_close.mp3"),
]

print("=" * 50)
print("TESTING ALL MP3 ALERTS")
print(f"Audio directory: {AUDIO_DIR}")
print(f"Alert sound exists: {os.path.exists(ALERT_SOUND)}")
print("=" * 50)
print()

for i, (name, sound_file) in enumerate(alerts, 1):
    sound_path = os.path.join(AUDIO_DIR, sound_file)
    print(f"[{i}/{len(alerts)}] {name}")
    print(f"  File: {sound_file} (exists: {os.path.exists(sound_path)})")
    print("-" * 40)

    playsound(ALERT_SOUND)
    playsound(sound_path)

    if i < len(alerts):
        print("Next alert in 1 second...")
        time.sleep(1)
    print()

print("=" * 50)
print("ALL ALERTS TESTED")
print("=" * 50)
