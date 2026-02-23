(() => {
  const root = document.documentElement;

  // YEAR
  const y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // THEME
  const themeBtn = document.getElementById("themeToggle");
  function setTheme(t) {
    root.setAttribute("data-theme", t);
    localStorage.setItem("theme", t);
  }

  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const current = root.getAttribute("data-theme") || "light";
      setTheme(current === "dark" ? "light" : "dark");
    });
  }

  // DROPDOWNS
  const dotsBtn = document.getElementById("dotsBtn");
  const dotsMenu = document.getElementById("dotsMenu");
  const avatarBtn = document.getElementById("avatarBtn");
  const avatarMenu = document.getElementById("avatarMenu");

  function closeDropdowns() {
    if (dotsMenu) dotsMenu.classList.remove("open");
    if (avatarMenu) avatarMenu.classList.remove("open");
  }

  if (dotsBtn && dotsMenu) {
    dotsBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = dotsMenu.classList.toggle("open");
      if (open && avatarMenu) avatarMenu.classList.remove("open");
    });
  }

  if (avatarBtn && avatarMenu) {
    avatarBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = avatarMenu.classList.toggle("open");
      if (open && dotsMenu) dotsMenu.classList.remove("open");
    });
  }

  document.addEventListener("click", closeDropdowns);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeDropdowns();
  });

  // MOBILE MENU (pages + close)
  const hamburger = document.getElementById("hamburger");
  const mobileMenu = document.getElementById("mobileMenu");
  const closeMenu = document.getElementById("closeMenu");

  function openMobile() {
    if (!mobileMenu) return;
    mobileMenu.classList.add("isOpen");
    mobileMenu.setAttribute("aria-hidden", "false");
    if (hamburger) hamburger.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  }

  function closeMobile() {
    if (!mobileMenu) return;
    mobileMenu.classList.remove("isOpen");
    mobileMenu.setAttribute("aria-hidden", "true");
    if (hamburger) hamburger.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }

  if (hamburger) hamburger.addEventListener("click", openMobile);
  if (closeMenu) closeMenu.addEventListener("click", closeMobile);

  if (mobileMenu) {
    mobileMenu.addEventListener("click", (e) => {
      if (e.target === mobileMenu) closeMobile(); // click outside panel
    });

    mobileMenu.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", closeMobile);
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMobile();
  });

  // BACK TO TOP
  const toTop = document.getElementById("toTop");
  if (toTop) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 450) toTop.classList.add("show");
      else toTop.classList.remove("show");
    });
    toTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }
})();