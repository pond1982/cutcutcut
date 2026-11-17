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
    else new IntersectionObserver(([e]) => { seen = e.isIntersecting; if (seen) v.play().catch(() => {}); else v.pause(); }, { threshold: 0.35 }).observe(reel);
  }
  const vids = [...document.querySelectorAll("video")].filter((x) => !x.closest(".reel-player"));
  vids.forEach((v) => v.addEventListener("play", () => vids.forEach((o) => { if (o !== v) o.pause(); })));
})();
