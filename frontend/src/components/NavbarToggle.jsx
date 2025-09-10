import { useEffect } from "react";

export default function NavbarToggle() {
  useEffect(() => {
    const toolbar = document.getElementById("site-toolbar");
    const btn = document.getElementById("navbar-toggle");
    const nav = document.getElementById("primary-nav");
    if (!toolbar || !btn || !nav) return;

    const mdQuery = window.matchMedia("(min-width: 768px)");

    const setOpen = (open) => {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      toolbar.classList.toggle("is-open", open);
      document.body.style.overflow = open ? "hidden" : ""; // ✅ lock scroll en mobile

      if (open) {
        nav.classList.remove("d-none");
        nav.classList.add("d-flex");
      } else if (!mdQuery.matches) {
        nav.classList.add("d-none");
        nav.classList.remove("d-flex");
      }

      const icon = btn.querySelector("i");
      if (icon) {
        icon.classList.toggle("bi-list", !open);
        icon.classList.toggle("bi-x", open);
      }
    };

    const onClick = (e) => {
      e.preventDefault();
      const expanded = btn.getAttribute("aria-expanded") === "true";
      setOpen(!expanded);
    };

    const onResize = () => {
      if (mdQuery.matches) {
        // desktop : menu toujours visible
        toolbar.classList.remove("is-open");
        nav.classList.remove("d-none");
        btn.setAttribute("aria-expanded", "false");
        const icon = btn.querySelector("i");
        if (icon) { icon.classList.add("bi-list"); icon.classList.remove("bi-x"); }
      } else {
        // mobile : replier par défaut
        nav.classList.add("d-none");
        btn.setAttribute("aria-expanded", "false");
      }
    };

    btn.addEventListener("click", onClick);
    mdQuery.addEventListener ? mdQuery.addEventListener("change", onResize)
                             : window.addEventListener("resize", onResize);
    onResize();

    return () => {
      btn.removeEventListener("click", onClick);
      mdQuery.removeEventListener ? mdQuery.removeEventListener("change", onResize)
                                  : window.removeEventListener("resize", onResize);
    };
  }, []);

  return null; // contrôle DOM uniquement
}
