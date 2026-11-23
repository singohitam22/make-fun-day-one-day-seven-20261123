// Entry program for the make.fun "Day one, day seven" TikTok bounty
// (post-tiktok-day-one-day-seven-20261123-0327). Node 22, standard
// library only, no network, no wall clock, no files outside the repo.
//
// The entry itself is the video: a short 9:16 TikTok clip about STARFALL,
// one tiny agent-built game shown on day one and again on day seven
// after a week of daily updates — same map, same start, visibly more
// going on the second time — ending with make.fun's referral end card
// from the press pack carrying referral code rn8nv1d9. The video file
// lives in this repository as day-one-day-seven.mp4; the game it shows
// lives in game/v1/index.html (day one) and game/v2/index.html (day
// seven), both playable in a browser.
//
// All this program has to do is hand the video's TikTok address to the
// house: it copies VIDEO.json from the repository root to /output,
// where the gate reads it. The house reads the video's views and
// interactions itself; nothing this program writes about the video
// counts.
//
// VIDEO.json currently holds the placeholder address from the kit:
// the video has been rendered but not posted yet (posting needs the
// user — TikTok only accepts a public video posted from the TikTok app
// or site, or an audited app). Once it is posted, VIDEO.json is updated
// with the video's full address, https://www.tiktok.com/@<handle>/video/<id>.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// The address must be a JSON object with a string `url`, so a broken
// VIDEO.json fails loudly here instead of silently handing the gate a
// bad file. The placeholder passes this shape check on purpose: the
// gate itself refuses it as "no video yet" until the real address lands.
const source = join(BOT_DIR, 'VIDEO.json');
const parsed: unknown = JSON.parse(readFileSync(source, 'utf8'));
if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
  throw new Error('VIDEO.json must be a JSON object with a url field');
}
if (typeof (parsed as { url?: unknown }).url !== 'string') {
  throw new Error('VIDEO.json must be a JSON object with a string url field');
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(source, join(OUTPUT_DIR, 'VIDEO.json'));
} catch (err) {
  console.error(`VIDEO.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
