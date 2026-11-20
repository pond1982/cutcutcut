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
vid chair                "$G/Saved/Showcase/chair.mp4" 12
vid conductor            "$G/Saved/Showcase/conductor.mp4" 22
vid porter               "$G/Saved/Showcase/porter.mp4" 9
vid pacer                "$G/Saved/Showcase/pacer.mp4" 6
vid amagiri              "$G/Saved/Showcase/amagiri.mp4" 5
vid balance-playthrough  "$G/Docs/Shots/Horai-Balance-Playthrough.mp4" 60 29
vid showcase-thai        "$G/Docs/Shots/Horai-Showcase-Thai.mp4" 100 29
vid dev-update-thai      "$G/Docs/Shots/Horai-Dev-Update-TH.mp4" 150 29
vid dev-update-day5      "$G/Saved/DevUpdate/CutCutCut-DevUpdate-Day5.mp4" 1 29
vid boss-cutscene        "$G/Saved/CutScene/CutCutCut-Bosses-CutScene.mp4" 58 30
vid porter-finish        "$G/Saved/FinishCall/Porter-Own-Ending.mp4" 8
vid six-endings          "$G/Saved/FinishCall/Six-Endings.mp4" 9 28
vid roll-before-after    "$G/Saved/FeelCompare/Feel-Before-After.mp4" 3
vid flick-before-after   "$G/Saved/FeelCompare/Flick-Roll-Before-After.mp4" 5
vid six-endings-rebuilt  "$G/Saved/FinishCall/Six-Endings.mp4" 9 28
vid galahad-new-body     "$G/Saved/Galahad/Galahad-Oval-Shield.mp4" 6 28
vid ultimate-impact-frame "$G/Saved/ImpactFrames/Rin-Ultimate-New-Landing.mp4" 2.2
vid envoy-body-stays     "$G/Saved/Envoy/Envoy-Body-Stays.mp4" 12 28
du -sh "$OUT"

# ---- the home page's rotating reel: short silent clips of real play, cut from the videos above ----
REEL="$OUT/../reel"; mkdir -p "$REEL"
clip() { # name, source name (in $OUT), start (s), length (s)
  if [ ! -f "$REEL/$1.mp4" ] || [ "${FORCE:-0}" = 1 ]; then
    ffmpeg -loglevel error -y -ss "$3" -t "$4" -i "$OUT/$2.mp4" -an -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 27 -pix_fmt yuv420p -movflags +faststart "$REEL/$1.mp4"
  fi
  ffmpeg -loglevel error -y -ss 1 -i "$REEL/$1.mp4" -frames:v 1 -q:v 5 "$REEL/$1.jpg"
  echo "reel $1 $(du -h "$REEL/$1.mp4" | cut -f1)"
}
clip first-fight   first-fight         5   8
clip ink-kick      ultimate-ink-kick   1.5 9
clip widow         winter-widow        11  8
clip homura        homura-duel-1       27  8
clip desk          balance-playthrough 20  7
clip clinic        balance-playthrough 62  7
clip residences    balance-playthrough 105 7
clip gala          balance-playthrough 185 7
vid sound-porter         "$G/Saved/SoundFilms/06-porter-louder-lines.mp4" 20 28
vid sound-clinic         "$G/Saved/SoundFilms/02-clinic-crowd.mp4" 12 28
# Day 8: a job floor, a memo floor, and the stair page that teaches a technique (floor 5 with its guardian switched off)
vid floor-job            "$G/Saved/Day8Films/job.mp4" 26 28
vid floor-memo           "$G/Saved/Day8Films/memo.mp4" 4 28
vid technique-stair      "$G/Saved/Day8Films/stair-cut.mp4" 18 28
vid stair-door           "$G/Saved/Day8Films/stair-door.mp4" 16 28
