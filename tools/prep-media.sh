#!/bin/bash
# Makes web-sized copies of the game's videos and art for the site, from the (private) game folder.
# Videos: H.264, at most 1280 px wide, fast-start, plus a poster frame. Images: see prep-images.py.
#   bash tools/prep-media.sh            everything missing
#   FORCE=1 bash tools/prep-media.sh    redo all
set -euo pipefail
G="${GAME_DIR:-/Volumes/MacMiniAdded/Projects/SamuraiFightFight}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/docs/media/video"
mkdir -p "$OUT"
vid() { # name, source, poster time (s), crf
  local name="$1" src="$2" at="${3:-2}" crf="${4:-27}"
  if [ ! -f "$OUT/$name.mp4" ] || [ "${FORCE:-0}" = 1 ]; then
    ffmpeg -loglevel error -y -i "$src" -vf "scale='min(1280,iw)':-2" -c:v libx264 -preset slow -crf "$crf" -pix_fmt yuv420p \
      -c:a aac -b:a 128k -movflags +faststart "$OUT/$name.mp4"
  fi
  ffmpeg -loglevel error -y -ss "$at" -i "$OUT/$name.mp4" -frames:v 1 -q:v 4 "$OUT/$name.jpg"
  echo "$name $(du -h "$OUT/$name.mp4" | cut -f1)"
}
vid intro                "$G/Saved/Intro/CutCutCut-Intro.mp4" 51 26
vid first-fight          "$G/Docs/Shots/First-Fight-and-Card-Hand.mp4" 9
vid campaign-showcase    "$G/Docs/Shots/Horai-Campaign-Showcase.mp4" 20
vid ultimate-ink-kick    "$G/Docs/Shots/Rin-Ultimate-Ink-Kick.mp4" 4
vid kick-facing          "$G/Docs/Shots/Rin-Kick-Facing.mp4" 6
vid ink-kick-study       "$G/Docs/Shots/Rin-Ink-Kick-Motion-Study.mp4" 4
vid winter-widow         "$G/Saved/Showcase/winter-widow-2.mp4" 14
vid winter-widow-frost   "$G/Saved/Showcase/winter-widow-frost.mp4" 9
vid winter-widow-rounds  "$G/Saved/Showcase/winter-widow-rounds.mp4" 8
vid nurse-first-try      "$G/Saved/Showcase/orderly-nurse.mp4" 12
vid homura-duel-1        "$G/Saved/Homura-Duel-1-Floor-30.mp4" 30
vid homura-duel-2        "$G/Saved/Homura-Duel-2-Floor-65.mp4" 25
vid homura-forms         "$G/Saved/Homura-All-Forms-Floor-65.mp4" 15
vid balance-playthrough  "$G/Docs/Shots/Horai-Balance-Playthrough.mp4" 60 29
vid showcase-thai        "$G/Docs/Shots/Horai-Showcase-Thai.mp4" 100 29
vid dev-update-thai      "$G/Docs/Shots/Horai-Dev-Update-TH.mp4" 150 29
du -sh "$OUT"
