// Small behaviours only: the phone menu, the picture lightbox, and one video playing at a time.
(() => {
  const menu = document.querySelector(".menu"), nav = document.querySelector(".nav");
  if (menu) menu.addEventListener("click", () => { const open = nav.classList.toggle("open"); menu.setAttribute("aria-expanded", open); });
  const box = document.querySelector(".lightbox"), big = box && box.querySelector("img");
  const close = () => { box.hidden = true; big.removeAttribute("src"); };
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a.zoom");
    if (a && box) { e.preventDefault(); big.src = a.href; big.alt = (a.querySelector("img") || {}).alt || ""; box.hidden = false; return; }
    if (box && !box.hidden && e.target.closest(".lightbox")) close();
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && box && !box.hidden) close(); });
  // The reel: one silent video that plays each clip of real play in turn, only while it is on screen.
  const reel = document.querySelector(".reel-player");
  if (reel) {
    const clips = JSON.parse(reel.dataset.clips), v = reel.querySelector("video"), label = reel.querySelector(".reel-label");
    const dots = [...reel.querySelectorAll(".reel-dots button")], still = matchMedia("(prefers-reduced-motion: reduce)").matches;
    let i = 0, seen = false;
    const show = (n, play) => {
      i = (n + clips.length) % clips.length;
      v.poster = clips[i].poster; v.src = clips[i].src; label.textContent = clips[i].label;
      dots.forEach((d, k) => d.classList.toggle("on", k === i));
      if (play) v.play().catch(() => {});
    };
    dots.forEach((d, k) => d.addEventListener("click", () => show(k, true)));
    reel.querySelector(".reel-prev").addEventListener("click", () => show(i - 1, true));
    reel.querySelector(".reel-next").addEventListener("click", () => show(i + 1, true));
    v.addEventListener("ended", () => show(i + 1, true));
    dots[0].classList.add("on");
    if (still) v.controls = true; // no motion unless asked for
    else {
      // Play only while a good part of the player is on screen. Checked on scroll, on resize and whenever a clip
      // becomes ready, because an observer alone sometimes misses the first jump to the section.
      let queued = false;
      const sync = () => {
        queued = false;
        const r = reel.getBoundingClientRect(), vis = Math.min(r.bottom, innerHeight) - Math.max(r.top, 0);
        seen = vis > 0.35 * r.height;
        if (seen && v.paused) v.play().catch(() => {}); else if (!seen && !v.paused) v.pause();
      };
      const ask = () => { if (!queued) { queued = true; requestAnimationFrame(sync); } };
      addEventListener("scroll", ask, { passive: true }); addEventListener("resize", ask); addEventListener("load", ask);
      v.addEventListener("canplay", ask);
      new IntersectionObserver(ask, { threshold: [0, 0.35, 0.7] }).observe(reel);
      ask();
    }
  }
  // The launch list: post the form to Kit without leaving the page and say what happened. If that request cannot be
  // made at all, the form is sent the ordinary way, in a new tab, where Kit answers with its own page.
  document.querySelectorAll("form.signup").forEach((f) => {
    const msg = f.querySelector(".signup-msg"), btn = f.querySelector("button"), email = f.querySelector("input[type=email]");
    const say = (text, ok) => { msg.textContent = text; msg.className = "signup-msg " + (ok ? "ok" : "bad"); msg.hidden = false; };
    f.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!email.value.trim() || !email.checkValidity()) { say("Please enter a valid email address.", false); email.focus(); return; }
      btn.disabled = true;
      fetch(f.action, { method: "POST", body: new FormData(f), headers: { Accept: "application/json" } })
        .then((r) => r.json().catch(() => ({})).then((d) => ({ r, d })))
        .then(({ r, d }) => {
          if (r.ok && d.status !== "failed") {
            // The form gives way to the next step: where to look and what to press.
            const done = f.querySelector(".signup-done");
            if (!done) { say("Almost there: check your inbox and click the link to confirm.", true); f.reset(); return; }
            done.querySelector(".signup-done-to").textContent = email.value.trim();
            msg.hidden = true; f.classList.add("is-done"); done.hidden = false; f.reset();
            done.querySelector(".signup-again").onclick = () => { f.classList.remove("is-done"); done.hidden = true; email.focus(); };
          }
          else say("That did not go through. Please check the address and try again.", false);
        })
        .catch(() => { f.submit(); })
        .finally(() => { btn.disabled = false; });
    });
  });
  const vids = [...document.querySelectorAll("video")].filter((x) => !x.closest(".reel-player"));
  vids.forEach((v) => v.addEventListener("play", () => vids.forEach((o) => { if (o !== v) o.pause(); })));
})();
