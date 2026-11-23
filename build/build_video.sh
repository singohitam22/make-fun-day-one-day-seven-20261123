#!/bin/bash
# Assemble day-one-day-seven.mp4 (1080x1920, 30 fps, 24.5 s).
# Segments: title 2.5s | 3x (DAY 1 2.5s / DAY 7 2.5s) | DAY 7 final 4s |
# make.fun referral end card (manifest mp4, as-is) 3s with code rn8nv1d9.
set -e
E=~/workspace/make-fun/entries/post-tiktok-day-one-day-seven-20261123-0327
B="$E/build"
cd "$B"

F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
FM=/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf
mkdir -p captions
printf '%s' "DAY 1" > captions/d1.txt
printf '%s' "DAY 7" > captions/d7.txt
printf '%s' "DAY 7 — THE NEWEST BUILD" > captions/fin_top.txt
printf '%s' "Day one: one ship, five stars, three rocks." > captions/d1a.txt
printf '%s' "Day seven: same map — plus coins, gems, drones." > captions/d7a.txt
printf '%s' "Same start. Same lanes. Almost nothing in the sky." > captions/d1b.txt
printf '%s' "Comets, combos, shields, a trail — a week of updates." > captions/d7b.txt
printf '%s' "Still just a ship and a few stars." > captions/d1c.txt
printf '%s' "Same moment, visibly more going on." > captions/d7c.txt
printf '%s' "Still growing. Start yours at make.fun" > captions/fin_bot.txt

LBL="fontfile=$F:fontsize=96:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=24:x=(w-text_w)/2:y=110"
LBLFIN="fontfile=$F:fontsize=62:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=20:x=(w-text_w)/2:y=110"
CAP="fontfile=$F:fontsize=34:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=16:x=(w-text_w)/2:y=h-520"

ffmpeg -y -v error \
  -loop 1 -t 2.5 -i title.png \
  -framerate 30 -i frames/v1_%04d.png \
  -framerate 30 -i frames/v2_%04d.png \
  -i ../assets/makefun-card-9x16.mp4 \
  -i ../assets/makefun-badge-9x16.png \
  -i music.wav \
  -filter_complex "\
[0:v]fps=30,format=yuv420p,setpts=PTS-STARTPTS[title];\
[1:v]fps=30,format=yuv420p,split=3[v1a][v1b][v1c];\
[v1a]trim=0:2.5,setpts=PTS-STARTPTS,drawtext=textfile=captions/d1.txt:$LBL,drawtext=textfile=captions/d1a.txt:$CAP[d1a];\
[v1b]trim=2.5:5.0,setpts=PTS-STARTPTS,drawtext=textfile=captions/d1.txt:$LBL,drawtext=textfile=captions/d1b.txt:$CAP[d1b];\
[v1c]trim=5.0:7.5,setpts=PTS-STARTPTS,drawtext=textfile=captions/d1.txt:$LBL,drawtext=textfile=captions/d1c.txt:$CAP[d1c];\
[2:v]fps=30,format=yuv420p,split=4[v2a][v2b][v2c][v2f];\
[v2a]trim=0:2.5,setpts=PTS-STARTPTS,drawtext=textfile=captions/d7.txt:$LBL,drawtext=textfile=captions/d7a.txt:$CAP[d7a];\
[v2b]trim=2.5:5.0,setpts=PTS-STARTPTS,drawtext=textfile=captions/d7.txt:$LBL,drawtext=textfile=captions/d7b.txt:$CAP[d7b];\
[v2c]trim=5.0:7.5,setpts=PTS-STARTPTS,drawtext=textfile=captions/d7.txt:$LBL,drawtext=textfile=captions/d7c.txt:$CAP[d7c];\
[v2f]trim=7.5:11.5,setpts=PTS-STARTPTS,drawtext=textfile=captions/fin_top.txt:$LBLFIN,drawtext=textfile=captions/fin_bot.txt:$CAP[fin];\
[3:v]fps=30,format=yuv420p,setpts=PTS-STARTPTS,drawbox=x=208:y=1230:w=9:h=82:color=white:t=fill,drawtext=text='rn8nv1d9':fontfile=$FM:fontsize=62:fontcolor=#191419:x=210:y=1240[card];\
[title][d1a][d7a][d1b][d7b][d1c][d7c][fin][card]concat=n=9:v=1:a=0[vcat];\
[vcat][4:v]overlay=0:0:enable='lt(t,21.5)'[vout];\
[5:a]atrim=0:24.5,asetpts=PTS-STARTPTS[aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 128k -movflags +faststart \
  "$E/day-one-day-seven.mp4"

ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 "$E/day-one-day-seven.mp4"
