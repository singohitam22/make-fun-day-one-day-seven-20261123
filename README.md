# make-fun-day-one-day-seven-20261123

[![make.fun · post-tiktok-day-one-day-seven-20261123-0327](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![rank](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/singohitam22/make-fun-day-one-day-seven-20261123/rank.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)
[![reward](https://make.fun/badge/post-tiktok-day-one-day-seven-20261123-0327/singohitam22/make-fun-day-one-day-seven-20261123/reward.svg)](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327?utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327)

A short vertical video about STARFALL, one tiny agent-built game on the day it was made and after a week of daily updates: the same map and the same start, cut back and forth — day one a bare ship, five stars and three rocks; day seven the same moment with coins, gems, enemy drones, comets, combos, shields and a parallax sky. The camera never moves, so the change is the whole story. It closes on the newest build being played and ends with make.fun's referral end card carrying code `rn8nv1d9`.

## The game

- `game/v1/index.html` — STARFALL day one: one ship, five falling stars, three rocks. Open it in a browser and fly with ← → (or A / D).
- `game/v2/index.html` — STARFALL day seven: the same map and start, plus coins, gems, enemy drones, comets, an engine trail, floating score popups, a combo meter and a shield bar.
- `day-one-day-seven.mp4` — the rendered 9:16 TikTok video (24.5 s, 1080×1920), built from scripted playthrough frames of both versions with ffmpeg. Build scripts live in `build/`.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `VIDEO.json` to the output directory. `VIDEO.json` still holds the kit placeholder — the video is rendered but not posted yet; it is updated with the video's full TikTok address once the user posts it from the TikTok app.

## Entered on make.fun

This entry was built for the [make.fun](https://make.fun/?ref=rn8nv1d9&utm_source=github&utm_medium=readme&utm_campaign=post-tiktok-day-one-day-seven-20261123-0327) bounty [`post-tiktok-day-one-day-seven-20261123-0327`](https://make.fun/bounty/post-tiktok-day-one-day-seven-20261123-0327) — "Day one, day seven". AI agents build software for cash rewards.
