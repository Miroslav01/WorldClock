"""Quick single alert test"""
import os
from playsound import playsound

ALERT_SOUND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "alert_1.mp3")

print(f"Sound file: {ALERT_SOUND}")
print(f"File exists: {os.path.exists(ALERT_SOUND)}")

print("\nPlaying alert sound...")
playsound(ALERT_SOUND)
print("Done!")
