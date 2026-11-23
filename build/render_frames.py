#!/usr/bin/env python3
"""Render STARFALL gameplay frames (v1 = day one, v2 = day seven).

Mirrors game/v1/index.html and game/v2/index.html: same 540x960 world,
same ship start, same star lanes, same falling speeds — drawn at 2x
(1080x1920). The ship flies a fixed scripted path (the same sine in
both versions) so the video's cuts show identical moments a week apart.
Frames carry NO text: ffmpeg adds the DAY 1 / DAY 7 labels later.
"""
import math, os
from PIL import Image, ImageDraw

W, H = 1080, 1920
S = 2  # game units (540x960) -> pixels
LANES = [90, 180, 270, 360, 450]
FPS = 30
OUT = os.path.expanduser("~/workspace/make-fun/entries/post-tiktok-day-one-day-seven-20261123-0327/build/frames")
os.makedirs(OUT, exist_ok=True)

def ship_x(t):
    # Scripted flight path, identical in both versions: the ship sweeps
    # across the same lanes in v1 and v2. (Kept for reference; the
    # renderer below steers with a simple autopilot instead so the ship
    # actually collects stars — same autopilot in both versions.)
    return 270 + 180 * math.sin(0.55 * t)

class Sim:
    """60 Hz logic, identical rules to the JS games."""
    def __init__(self, version):
        self.v = version
        self.t = 0.0
        self.sx = 270.0  # ship x (game units); same start as the JS games
        self.score = 0
        self.combo = 1
        self.combo_timer = 0.0
        self.stars = [{"x": x, "y": -40 - i * 170, "r": 14, "got": False}
                      for i, x in enumerate(LANES)]
        self.rocks = [{"x": 135, "y": -260, "r": 24},
                      {"x": 315, "y": -560, "r": 24},
                      {"x": 405, "y": -860, "r": 24}]
        self.coins = [{"x": x, "y": -120 - i * 210, "r": 10, "got": False}
                      for i, x in enumerate([135, 225, 315, 405])]
        self.gems = [{"x": 270, "y": -700, "r": 12, "got": False}]
        self.drones = [{"x": 90, "y": -420, "r": 18, "dir": 1},
                       {"x": 450, "y": -900, "r": 18, "dir": -1}]
        self.comets = [{"x": 60, "y": -100, "vx": 3.2, "vy": 5.5}]
        self.trail = []
        self.popups = []

    def collect(self, x, y, pts, label):
        self.score += pts * self.combo
        self.popups.append({"x": x, "y": y, "label": f"{label} +{pts * self.combo}", "life": 1.0})
        self.combo = min(self.combo + 1, 8)
        self.combo_timer = 3.0

    def step(self):
        dt = 1 / 60
        self.t += dt
        # Autopilot (same in both versions): steer toward the lowest
        # uncollected star, max 5 units/step — so the ship really plays.
        targets = [s for s in self.stars if not s["got"]]
        if self.v == 2:
            targets += [c for c in self.coins if not c["got"]]
            targets += [g for g in self.gems if not g["got"]]
        if targets:
            tgt = max(targets, key=lambda o: o["y"])
            if tgt["x"] > self.sx + 2:
                self.sx = min(self.sx + 5, tgt["x"])
            elif tgt["x"] < self.sx - 2:
                self.sx = max(self.sx - 5, tgt["x"])
        sx = self.sx
        sy = H / S - 140
        if self.v == 2:
            self.trail.append({"x": sx, "y": sy + 20, "life": 1.0})
            if len(self.trail) > 40:
                self.trail.pop(0)
            if self.combo_timer > 0:
                self.combo_timer -= dt
                if self.combo_timer <= 0:
                    self.combo = 1
        for s in self.stars:
            s["y"] += 2.2
            if s["y"] > 960 + 30:
                s["y"] = -30; s["got"] = False
            if not s["got"] and math.hypot(s["x"] - sx, s["y"] - sy) < s["r"] + 22:
                s["got"] = True
                if self.v == 2:
                    self.collect(s["x"], s["y"], 10, "STAR")
                else:
                    self.score += 10
        for r in self.rocks:
            r["y"] += 2.6
            if r["y"] > 960 + 40:
                r["y"] = -40
        if self.v == 2:
            for c in self.coins:
                c["y"] += 3.0
                if c["y"] > 960 + 30:
                    c["y"] = -30; c["got"] = False
                if not c["got"] and math.hypot(c["x"] - sx, c["y"] - sy) < c["r"] + 22:
                    c["got"] = True; self.collect(c["x"], c["y"], 25, "COIN")
            for g in self.gems:
                g["y"] += 2.0
                if g["y"] > 960 + 30:
                    g["y"] = -30; g["got"] = False
                if not g["got"] and math.hypot(g["x"] - sx, g["y"] - sy) < g["r"] + 22:
                    g["got"] = True; self.collect(g["x"], g["y"], 50, "GEM")
            for d in self.drones:
                d["y"] += 1.8; d["x"] += d["dir"] * 1.6
                if d["x"] < 50 or d["x"] > 540 - 50:
                    d["dir"] *= -1
                if d["y"] > 960 + 40:
                    d["y"] = -40
            for c in self.comets:
                c["x"] += c["vx"]; c["y"] += c["vy"]
                if c["y"] > 960 + 60:
                    c["x"] = 120; c["y"] = -60
            for p in self.popups:
                p["y"] -= 1.2; p["life"] -= dt
            for p in self.trail:
                p["life"] -= 1 / 30

    def draw(self):
        img = Image.new("RGB", (W, H), (5, 5, 16) if self.v == 1 else (7, 5, 24))
        d = ImageDraw.Draw(img, "RGBA")
        if self.v == 2:
            # Nebula clouds (smaller, softer than the first pass).
            d.ellipse([120*S-150, ((self.t*9) % 1100 - 60)*S-150, 120*S+150, ((self.t*9) % 1100 - 60)*S+150], fill=(196, 28, 131, 35))
            d.ellipse([430*S-130, ((self.t*7+400) % 1100 - 60)*S-130, 430*S+130, ((self.t*7+400) % 1100 - 60)*S+130], fill=(196, 28, 131, 35))
            for i in range(70):
                x = (i * 173) % 540 * S; y = (i * 311 + self.t * 26) % 960 * S
                d.rectangle([x, y, x+4, y+4], fill=(205, 216, 255))
            for i in range(40):
                x = (i * 97 + 40) % 540 * S; y = (i * 211 + self.t * 12) % 960 * S
                d.rectangle([x, y, x+6, y+6], fill=(136, 153, 187))
        else:
            for i in range(24):
                x = (i * 173) % 540 * S; y = (i * 311 + self.t * 12) % 960 * S
                d.rectangle([x, y, x+4, y+4], fill=(136, 153, 187))
        if self.v == 2:
            for c in self.comets:
                d.line([c["x"]*S, c["y"]*S, (c["x"]-c["vx"]*12)*S, (c["y"]-c["vy"]*12)*S], fill=(174, 243, 255), width=6)
                d.ellipse([c["x"]*S-10, c["y"]*S-10, c["x"]*S+10, c["y"]*S+10], fill=(255, 255, 255))
        for s in self.stars:
            if s["got"]:
                continue
            d.ellipse([s["x"]*S-s["r"]*S, s["y"]*S-s["r"]*S, s["x"]*S+s["r"]*S, s["y"]*S+s["r"]*S], fill=(255, 217, 77))
            if self.v == 2:
                d.ellipse([s["x"]*S-12, s["y"]*S-12, s["x"]*S+12, s["y"]*S+12], fill=(255, 246, 200))
        if self.v == 2:
            for c in self.coins:
                if c["got"]:
                    continue
                d.ellipse([c["x"]*S-20, c["y"]*S-20, c["x"]*S+20, c["y"]*S+20], fill=(255, 157, 46))
            for g in self.gems:
                if g["got"]:
                    continue
                d.ellipse([g["x"]*S-24, g["y"]*S-24, g["x"]*S+24, g["y"]*S+24], fill=(196, 77, 255))
        for r in self.rocks:
            d.ellipse([r["x"]*S-r["r"]*S, r["y"]*S-r["r"]*S, r["x"]*S+r["r"]*S, r["y"]*S+r["r"]*S], fill=(138, 143, 158))
            if self.v == 2:
                d.ellipse([(r["x"]-7)*S-16, (r["y"]-6)*S-16, (r["x"]-7)*S+16, (r["y"]-6)*S+16], fill=(92, 97, 112))
        if self.v == 2:
            for dr in self.drones:
                d.ellipse([dr["x"]*S-36, dr["y"]*S-36, dr["x"]*S+36, dr["y"]*S+36], fill=(255, 77, 109))
                d.ellipse([(dr["x"]-6)*S-6, (dr["y"]-4)*S-6, (dr["x"]-6)*S+6, (dr["y"]-4)*S+6], fill=(255, 255, 255))
                d.ellipse([(dr["x"]+6)*S-6, (dr["y"]-4)*S-6, (dr["x"]+6)*S+6, (dr["y"]-4)*S+6], fill=(255, 255, 255))
            for p in self.trail:
                a = int(max(p["life"], 0) * 0.7 * 255)
                d.ellipse([p["x"]*S-10, p["y"]*S-10, p["x"]*S+10, p["y"]*S+10], fill=(77, 215, 255, a))
        sx = self.sx * S
        sy = (960 - 140) * S
        d.polygon([(sx, sy-52), (sx-40, sy+36), (sx+40, sy+36)], fill=(77, 215, 255))
        if self.v == 2:
            d.ellipse([sx-12, sy-20, sx+12, sy+4], fill=(232, 251, 255))
            d.ellipse([sx-64, sy-64, sx+64, sy+64], outline=(77, 215, 255, 153), width=4)
        return img

def render(version, seconds):
    sim = Sim(version)
    n = int(seconds * FPS)
    for f in range(n):
        # two 60 Hz logic steps per 30 fps frame
        sim.step(); sim.step()
        img = sim.draw()
        img.save(f"{OUT}/v{version}_{f:04d}.png")
    print(f"v{version}: {n} frames, final score {sim.score}, combo x{sim.combo}")

render(1, 7.5)
render(2, 11.5)
print("done")
