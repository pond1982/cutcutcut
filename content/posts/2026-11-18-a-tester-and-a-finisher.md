---
title: A tester, a finisher, and a build that was not there
date: 2026-11-18
time: 14:55
summary: Yesterday's TestFlight build never arrived, and this log said it had. Today it is really there, the first tester wrote back, and the Freight Porter got an ending of his own.
cover: porter-finish
tags: TestFlight, Combat, Bosses, Video
---
This log has a rule: say what broke. So, first, a correction.

## The build that was not there

Yesterday's post said build 0.1 was on TestFlight, because the upload ended with *Upload succeeded.* It was not. Apple accepted the file, then dropped it while processing it, and said so only in an email. App Store Connect just showed "No Builds". The same thing happened to a second upload last night.

The cause was small. The engine can reach the camera, the microphone and the motion sensors, and Apple will not take an app like that unless it says why. The game uses none of them, and now says so in three lines.

The third upload is really there: Apple lists it as valid, and it was checked by asking Apple, not by trusting the uploader.

> "Upload succeeded" means Apple received the file. It does not mean Apple kept it.

## A cut scene, with a voice

Before the tester woke up there was time for a video: six guardians and Rin's ultimate, under two minutes, narrated in the developer's cloned voice.

::video boss-cutscene | Six guardians and the ultimate. Every fight is played by the game's own bot.

## The first tester writes back

Three notes, in Thai, from the first person to play who is not the developer:

1. The roll should go further.
2. The cuts should flow more smoothly.
3. While holding to cut, a swipe of the same thumb should roll out of the way.

**The roll** went from 1.51 m to 2.02 m. The game measured it, and drew it on the floor for a side-by-side film: a red ring where the roll starts, a yellow one where it ends.

::video roll-before-after | Old on the left, new on the right. Then the same moves in slow motion.

**The third note already existed**, which is its own lesson. Holding to cut and flicking to roll worked, but once per press, and it was measured from where the thumb first landed. A thumb that had wandered could flick and get nothing. Now any quick flick rolls, as many times as you like, and she goes back to cutting on her own.

::video flick-before-after | The same scripted thumb on both sides: held down, then flicked four ways without lifting.

**The second note** is the least certain. A cut that follows another now blends in over longer. It may look smoother, or only softer. The real answer is in the animation, which is a bigger job.

One phrase in the third note could be read two ways, so a question went back to the tester instead of a guess.

## Finish him, but in our own words

Until today a guardian on its knees was finished with one tap and a move picked at random. The owner asked to try something bigger on one boss: the Freight Porter.

Now his finish line is called, **Unload the Last Case**, the world slows, and four swipes are asked for against a clock. Miss it and he is put down plainly. Make it and you get his ending:

- He drives the pole at Rin once more from his knees. She turns it aside.
- A rising cut throws him into the air, limp, falling upward.
- The world drops to a twelfth of its speed. Rin does not.
- Thirteen cuts. Each one knocks him.
- He comes apart at every joint at once.

::video porter-finish | The call, then the ending. Filmed from the game, played by its bot.

It took several rounds to get here, and the owner's notes did most of the work: the overhead camera was blocked by furniture, so it comes down behind her shoulder; the title covered the blow, so it moved to the top; the picture shook, because a shake had been added to every hit, so the shakes went; he hung in the air like a statue, so now he is a ragdoll with gravity switched off.

## The stair moves

Watching those films showed something else: the way up stood inside the room, ran diagonally, and could be walked through. It now lies along a far wall, climbing into the far corner, square to the building and solid.

## What has not been checked

- Nobody has played the finish call by hand. The swipes in the film are the bot's, and four swipes in four seconds is a guess.
- Rin does not lift him or sheathe her sword. There is no clip for either: she launches him with a cut, and "puts the sword away" is her relaxing out of her stance.
- The new stair has not been looked at. No film of it was asked for, so there is none. In one room in fourteen it could not be placed and kept its old spot.
- The Porter's ending was judged from still frames, not watched in motion, by the agent that built it.
- The tester has not played the changes yet. They are not in the TestFlight build.

Next: a new build for the tester, and their answer to the question.
