# Cut Cut Cut: the website

The public site and dev log for the game *Cut Cut Cut: 100 Floors of Zombies*. Plain static files: no framework,
no server. The game itself is a separate, private repository (`/Volumes/MacMiniAdded/Projects/SamuraiFightFight`);
nothing here contains its source or its licensed assets, only web-sized pictures and videos made from it.

## Look at it

    python3 build.py            # writes the site into docs/
    python3 tools/serve.py      # http://localhost:4173

## Add a dev log post

1. Make `content/posts/YYYY-MM-DD-some-slug.md`:

       ---
       title: What the post is called
       date: 2026-11-18
       time: 14:30
       summary: One or two sentences. Shown on the card, under the title and in the RSS feed.
       cover: winter-widow
       tags: Bosses, Combat
       ---
       Ordinary paragraphs. **Bold**, *italic*, `code`, [links](https://example.com).

       ## A heading

       - a list item

       > A pull quote.

       ::video winter-widow | A caption
       ::video intro | A caption | portrait
       ::img shot-floor5 | A caption
       ::gallery shot-world shot-ophiel shot-floor45

   `cover` and the names after `::video`, `::img`, `::gallery` are file names in `docs/media/video` or
   `docs/media/img`, without the extension. `time` is optional; it orders posts made on the same day.
2. If the day matters to the story, add an entry to `content/timeline.json` (with `"link": "devlog/some-slug.html"`).
3. `python3 build.py`. It prints `MISSING:` for any link or media file that does not exist.

## Add a video or a picture

- Video: add a `vid <name> <source file> <poster time in seconds>` line to `tools/prep-media.sh`, then
  `bash tools/prep-media.sh`. It makes `<name>.mp4` (H.264, at most 1280 wide) and `<name>.jpg` (the poster).
- Picture: add it to `tools/prep-images.py`, then `~/VoxCPM/.venv/bin/python -I tools/prep-images.py`
  (that Python has Pillow; the system one does not).
- To show it on the Media page, add it to `content/media.json`.

## Where things are

| Path | What |
|---|---|
| `build.py` | The generator. Reads `content/`, writes `docs/`. Standard library only. |
| `content/site.json` | Site name, navigation, and the public address (`url`, used for RSS and share cards). |
| `content/pages/*.html` | The fixed pages. First line: `<!-- title | description | body class -->`. `{{name}}` asks `build.py` for a block (posts, cast, timeline, a video shelf, a gallery). |
| `content/posts/*.md` | Dev log posts. |
| `content/timeline.json`, `cast.json`, `media.json` | The timeline, the cast, the video shelves and galleries. |
| `static/` | `style.css` and `site.js`, copied as they are. |
| `docs/` | The built site, plus `docs/media` (about 175 MB). This is what gets published. |
| `tools/` | Media preparation and the local server. |

## Publish

Published with GitHub Pages at https://pond1982.github.io/cutcutcut/ from the `docs/` folder of `main`: after a build, commit and push, and the site updates in a minute or two. To set it up again elsewhere: push this repository, then in the
repository's Settings, Pages, choose "Deploy from a branch", branch `main`, folder `/docs`. Then set `url` in
`content/site.json` to the real address and rebuild. No single file is over GitHub's 100 MB limit (largest: 27 MB).

## Rules for the writing

- Every date and time on the site is real: taken from the game's commit history or an actual upload.
- Say what was not checked as plainly as what was.
- Do not give away the ending.
