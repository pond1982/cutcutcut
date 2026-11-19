---
title: The Envoy, and every guardian in phrases
date: 2026-11-19
time: 23:00
summary: Sounds, a size check that found a broken build, and a long day on the Envoy that ended with the real reason his body kept vanishing. Then every guardian's fight is rebuilt from short mixed phrases, and a new build goes to TestFlight and Android.
cover: envoy-body-stays
tags: Bosses, Combat, Builds, Video
---
Yesterday ended on a build for TestFlight. Today started with sound and finished with every guardian fighting differently.

## Fourteen sounds, and a size check

The owner added a free pack of game sounds. Fourteen of them went in: the Expedition's gunfire, a weapon being drawn, explosions, debris, a creature's roar. Before adding them the owner asked whether sound files would bloat a phone game. Together they are under five megabytes.

The owner then asked why the iPhone app was already near 400 MB. Counting it showed most of that is the engine and a handful of art packs, with perhaps 80 to 100 MB that could be cut. Counting it also showed something worse. Yesterday's TestFlight build did not contain Galahad's new body, the room effects or the impact frames. The game loads those by name, and the list of folders to pack into a phone build did not name them. The list is fixed, and today's build was checked file by file.

## The Envoy

The Envoy is the Expedition's field commander on floor 85, and he fights from range. The owner wanted a distortion effect to make him harder to fight. He went through four versions today, each changed after the owner watched the last.

1. **A cloak.** He bent the air and turned half invisible. The owner found it confusing: he flickered, ghosted, and seemed to run in place.
2. **A rifleman who leaps.** The cloak went. He keeps his distance and jumps away fast and far when she closes, with the air bending where he left. The owner asked for a knife for when she does get close.
3. **Phrases.** His attacks were rebuilt as short runs of moves mixed together, so the next one cannot be learned by rote: suppress, break contact, sweep, crossfire. Single shots, fans of shots, a concussion ring, leaps and the knife are the pieces. After the last move of a phrase he is open.
4. **Fixed.** The owner reported that he still vanished, and that he kept running at Rin when he should only go away or to the side.

## Why he vanished

The first guesses were wrong. His leaps took him past the edge of the screen for a second. He wears black, kneels to aim, and the floor is dark. Both were true, and both were fixed: he carries a small light now, leaps less far, and the camera holds him larger. Neither was the real cause.

The owner sent a single stopped frame: his name label and his light on the floor, and no body under them. That frame was the clue. His firing animation was the kind made to be layered on top of another pose, a recoil and nothing more. Played on its own, it puts every bone of the body at one point. For the length of every volley, his body was drawn as a dot.

The game now refuses to play that kind of clip as a whole pose, for every character. His rifle team used the same clip when kneeling, so they are fixed too. He fires from his aim with no recoil, and in the film he is never gone.

::video envoy-body-stays | The Envoy after the fix: lit, never closing in, and present for every shot.

He also no longer moves toward her. The knife is only for when she has come to him.

## Every guardian in phrases

The owner asked for an audit of how every guardian chooses its next move. Only the Envoy had phrases. Five guardians drew forms from a shuffled bag. Four of the last five guardians repeated a single floor attack. Five of the older ones swung at random.

The owner's answer was that every guardian should have a complex fight. So every guardian but Homura and the Orderly now fights in phrases: two or three moves run together with barely a pause, then an opening, never the same phrase twice in a row, and one phrase each held back for when they are badly hurt.

- **27 new floor attacks.** Galahad rams, slams the floor and sweeps his shield. The Sky Elder sends crossing currents, a whirlpool that closes from the outside in, and pools round her feet. The Sun Messiah throws his halo, burns where Rin stands and fires one broad beam. Dr. Amagiri cuts, lights the garden's beds in rows and sends roots up under her.
- **The older guardians** mix their old swings with new floor attacks. Whisper throws papers and stamps the floor. Subject 001 charges the length of the room. The Collector drops a display case round her: the frame first, then the middle.
- **The guardians who fight in forms** now chain them: one or two forms in a row at first, two or three once hurt, with no opening inside a run.
- **Left as they were:** Homura and the Orderly already mix their moves, and the first meeting with Falcifer is a lesson.

None of it has been filmed yet. The attack names are the agent's, not yet the owner's.

## New builds

A new build is on TestFlight, and Apple has marked it valid. It carries everything above and everything the last one was missing. An Android build was made too.

## What has not been checked

- **Nothing here has been played by hand.** Every fight was run by the game's own bot.
- **No guardian's new phrases have been seen.** They were checked in fights run without a picture, by their logs: every guardian's phrases ran, with no errors. No film was made of them.
- **Every new floor attack plays its guardian's one attack animation.** Only the marks on the floor differ.
- **Difficulty is untuned.** Openings now come less often, so every guardian is harder and the fights are longer.
- **Neither build has been opened on a phone.** The Android build is 434 MB; the iPhone build is likely larger than before, with what was missing now added.
- **The Envoy's distortion has never shown in a Mac film.** It is switched on for newer Pro iPhones only.
- The automated tests that need no special setup pass.

Next: the owner's hands on the new fights.
