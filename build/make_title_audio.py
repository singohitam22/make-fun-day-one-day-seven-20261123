#!/usr/bin/env python3
"""Title card + chiptune audio for the day-one-day-seven video."""
import math, os, struct, wave
from PIL import Image, ImageDraw, ImageFont

E = os.path.expanduser("~/workspace/make-fun/entries/post-tiktok-day-one-day-seven-20261123-0327/build")
W, H = 1080, 1920
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# --- title card ---
img = Image.new("RGB", (W, H), (8, 8, 22))
d = ImageDraw.Draw(img, "RGBA")
for y in range(H):  # vertical gradient, dark blue -> deep magenta tint
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(8 + 20 * t), int(8 + 6 * t), int(22 + 34 * t)))
# magenta accent bar
d.rectangle([90, 330, 990, 342], fill=(196, 28, 131))
# little ship + stars doodle
d.polygon([(540, 420), (500, 500), (580, 500)], fill=(77, 215, 255))
for (x, y, r) in [(200, 480, 16), (880, 460, 16), (150, 700, 10), (930, 720, 10)]:
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 217, 77))

def center(y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)

center(560, "DAY 1 vs DAY 7", font(BOLD, 92), (255, 255, 255))
center(760, "I built a tiny game.", font(BOLD, 64), (255, 217, 77))
center(850, "Then I updated it", font(BOLD, 64), (255, 255, 255))
center(940, "every day for a week.", font(BOLD, 64), (255, 255, 255))
center(1180, "Same map. Same start.", font(BOLD, 52), (77, 215, 255))
center(1260, "Watch what changed.", font(BOLD, 52), (77, 215, 255))
center(1560, "STARFALL — a tiny game", font(MONO, 40), (180, 190, 220))
center(1620, "made by my AI agent", font(MONO, 40), (180, 190, 220))
img.save(f"{E}/title.png")
print("title.png written")

# --- chiptune: bright pentatonic arpeggio, 24.5 s, quiet ---
SR = 44100
DUR = 24.5
NOTES = [523.25, 587.33, 659.25, 783.99, 880.00, 1046.50, 783.99, 659.25]
STEP = 0.22  # seconds per eighth note
frames = int(SR * DUR)
out = bytearray()
for n in range(frames):
    t = n / SR
    idx = int(t / STEP) % len(NOTES)
    f = NOTES[idx]
    tt = t % STEP
    env = min(1.0, tt / 0.02) * (1 - tt / STEP)
    s = 0.5 * math.sin(2 * math.pi * f * t) + 0.25 * math.sin(2 * math.pi * f * 2 * t)
    # soft bass on the beat
    b = 0.20 * math.sin(2 * math.pi * 130.81 * t) if int(t / STEP) % 4 == 0 else 0.0
    v = int(max(-1.0, min(1.0, (s * env + b) * 0.35)) * 32767)
    out += struct.pack("<h", v)
with wave.open(f"{E}/music.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(bytes(out))
print("music.wav written")
