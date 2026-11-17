---
title: An animated intro, narrated by Rin
date: 2026-11-17
time: 13:40
summary: Seventy seconds that explain the premise, drawn as a cartoon and told in Rin's own dry voice. It also settled what Rin sounds like in the game.
cover: intro
tags: Video, Voice
---
::video intro | The intro. 70 seconds, vertical. | portrait

## Why a cartoon

The game is isometric and small on screen. The premise needs faces: a sales pitch, a gala, a text message. So the intro is drawn in a different style, flat characters in a painted 3D world, using an open-source recipe for animated shorts built on three.js and Remotion. It renders on the same Mac as everything else.

## Script first

Rin tells it herself, in the first person. The script follows a simple shape: a hook, the setting, an escalation, and a deadpan pair of lines in the middle.

> Luckily, it worked. Nobody in that building can die. Unluckily, it worked. Nobody in that building can die.

It ends on the title, said three times.

## Rin's voice

The narration was generated with ElevenLabs. The voice chosen for Rin is wry, low and unimpressed, and its ID is now recorded in the project so that every line she speaks in the game uses the same one.

## How the picture was made

- 23 shots timed to the pauses in the recording.
- Seven sets: the street and tower, the penthouse, the trial ward, the gala hall, the stairwell, the office and a corridor.
- The cast drawn in code: Rin, Hana, the founder, soldiers, and a great many undying.
- The game's own logo for the title card.
- A synthesized score and effects. Nothing is sampled.

## Two things that went wrong

The renderer drew blank frames until it was told to redraw on every frame. And the first full render failed in its last second because the output height worked out to 2559.94 pixels.

## First cut

This is a first cut, checked from stills. The opening crowd sits low, the dusk shots came out blue, and the music is simple. It will get another pass.
