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
  const vids = [...document.querySelectorAll("video")];
  vids.forEach((v) => v.addEventListener("play", () => vids.forEach((o) => { if (o !== v) o.pause(); })));
})();
