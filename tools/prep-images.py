# Makes web-sized copies of the game's art and screenshots for the site, from the (private) game folder.
#   ~/VoxCPM/.venv/bin/python -I tools/prep-images.py
# Full images go to docs/media/img/<name>.jpg (at most 1800 px wide); the cast portraits are cut to squares.
import os, sys
from PIL import Image
G = os.environ.get("GAME_DIR", "/Volumes/MacMiniAdded/Projects/SamuraiFightFight")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "media", "img")
os.makedirs(OUT, exist_ok=True)

def save(im, name, maxw=1800, q=86):
    im = im.convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, name + ".jpg"), quality=q, optimize=True, progressive=True)

def full(name, src, **kw): save(Image.open(os.path.join(G, src)), name, **kw)

def quad(src, names):  # a 2 x 2 sheet of portraits -> four squares
    im = Image.open(os.path.join(G, src)); w, h = im.width // 2, im.height // 2
    for i, n in enumerate(names):
        if n: save(im.crop(((i % 2) * w, (i // 2) * h, (i % 2 + 1) * w, (i // 2 + 1) * h)), "cast-" + n, maxw=640)

# key art
full("backdrop", "Art/UI/title_backdrop.png")
full("keyart", "Art/Title/option1-tower.png")
full("hero-rin", "Art/Title/hero-rin-left.png", maxw=1920)  # the home page's landing backdrop: the tower, Rin at the left, no lettering
for i, n in enumerate(["blade", "panels", "ink", "office"], 2): full("title-option-" + n, f"Art/Title/option{i}-{n}.png", maxw=1400)
logo = Image.open(os.path.join(G, "Art/UI/title_logo.png")); logo.save(os.path.join(OUT, "logo.png"), optimize=True)
for n in ["dawn", "arrival"]: full("garden-" + n, f"Art/UI/Finale/garden_{n}.png")
full("card-court", "Art/UI/Finale/card_court.png", maxw=1400)
full("card-back", "Art/UI/Finale/card_back.png", maxw=700)
full("field-joker", "Art/UI/Finale/field_joker.png", maxw=700)
# cast portraits
for n, f in [("rin", "rin"), ("homura", "homura"), ("whisper", "whisper"), ("falcifer", "falcifer"), ("collector", "collector"), ("subject-001", "elder")]:
    full("cast-" + n, f"Art/UI/{f}_portrait.png", maxw=640)
quad("Art/UI/Finale/portrait_staff.png", ["winter-widow", "chief", "chair", "hana"])
quad("Art/UI/Finale/portrait_gala.png", ["sky-elder", "conductor", "sun-messiah", "amagiri"])
quad("Art/UI/Finale/portrait_amenities.png", ["porter", "pacer", "galahad", "envoy"])
full("cast-sheet", "Docs/Shots/Horai-Cast.jpg")
for n in ["whisper", "falcifer", "homura", "elder", "collector"]: full("name-" + n, f"Art/UI/title_{n}.png", maxw=900)
# screenshots and studies
for name, src in [
    ("shot-world", "Docs/Shots/Horai-World-Polish.jpg"), ("shot-rooms", "Docs/Shots/Horai-Room-Audit.jpg"),
    ("shot-floor5", "Docs/Shots/Floor-5-Guardian.jpg"), ("shot-floor30", "Docs/Shots/Floor-30-Retry.jpg"), ("shot-floor45", "Docs/Shots/Floor-45-Guardian.jpg"),
    ("shot-clinic-crossfire", "Docs/Shots/Clinic-Guardian-Crossfire.jpg"), ("shot-clinic-recovery", "Docs/Shots/Clinic-Field-Recovery.jpg"), ("shot-clinic-ward", "Docs/Shots/Clinic-Ward-Record.jpg"),
    ("shot-gala-android", "Docs/Shots/Android-Gala-Playtest.jpg"), ("shot-ophiel", "Docs/Shots/Ophiel-Core-Briefing.png"),
    ("shot-card-deal", "Docs/Shots/Rin-Card-Deal.png"), ("shot-card-collection", "Docs/Shots/Rin-Card-Collection.png"), ("shot-printed-deck", "Docs/Shots/Rin-Printed-Deck.jpg"),
    ("shot-roll-tutorial", "Docs/Shots/Roll-Tutorial-iPhone.png"), ("shot-iphone-compare", "Docs/Shots/iPhone-Desk-Render-Comparison.png"),
    ("shot-falcifer-intro", "Docs/Shots/falcifer_comic_intro.jpg"), ("shot-falcifer-fight", "Docs/Shots/falcifer_comic_fight.jpg"),
    ("shot-falcifer-arena", "Docs/Shots/falcifer_arena_overview.png"), ("shot-falcifer-arena-fight", "Docs/Shots/falcifer_arena_fight.png"),
    ("shot-office-zombie", "Docs/Shots/office_worker_zombie.png"), ("shot-elbow-study", "Docs/Shots/Boss-Elbow-Study.png"), ("shot-icon-options", "Docs/Shots/Horai-Icon-Options.jpg"),
]: full(name, src)
# Day 6's evening: a guardian room each for four of them, the phone's picture before and after, and Galahad drawn and built
for name, src in [
    ("shot-room-whisper", "Saved/Rooms/room-15.png"), ("shot-room-chair", "Saved/Rooms/room-55.png"), ("shot-room-collector", "Saved/Rooms/room-70.png"),
    ("shot-room-conductor", "Saved/Rooms/room-95.png"), ("shot-room-sun", "Saved/Rooms/room-99.png"), ("shot-room-subject", "Saved/Rooms/room-30.png"),
    ("shot-sharpness", "Saved/Sharpness/Sharpness-Before-After.png"),
]: full(name, src)
full("ref-galahad", "Art/Galahad/galahad_reference_front.png", maxw=900)
full("shot-galahad-built", "Art/Galahad/gh-front.png", maxw=700)
# the drawings three guardians were modelled from (made with the image tool; turned into 3D models in Tripo)
for n in ["porter", "pacer", "amagiri"]: full("ref-" + n, f"Art/{n.capitalize()}/{n}_reference_front.png", maxw=900)
# the cast as photographs (made with Seedream on JanaArt from the ink portraits; kept in the game's Saved/EndCredits/photos)
for n in ["1-rin", "2-hana", "3-homura", "4-winter-widow", "6-rin-cut"]:
    src = "Saved/EndCredits/photos/" + n + ".png"
    if os.path.exists(os.path.join(G, src)): full("photo-" + n[2:], src)
# favicon and social card
rin = Image.open(os.path.join(G, "Art/UI/rin_portrait.png")).convert("RGB")
rin.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "icon-180.png")); rin.resize((48, 48), Image.LANCZOS).save(os.path.join(OUT, "icon-48.png"))
key = Image.open(os.path.join(G, "Art/Title/option1-tower.png")).convert("RGB"); w = key.width; h = round(w * 630 / 1200)
key.crop((0, (key.height - h) // 2, w, (key.height + h) // 2)).resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, "social.jpg"), quality=86)
print(len(os.listdir(OUT)), "files")
