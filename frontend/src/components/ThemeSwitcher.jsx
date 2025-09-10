import { useEffect, useState } from "react";

// --- Helpers cookies ---
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

function setCookie(name, value, days) {
  const d = new Date();
  d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
  const expires = "expires=" + d.toUTCString();
  document.cookie = `${name}=${value};${expires};path=/`;
}

export default function ThemeSwitcher() {
  const [theme, setTheme] = useState("light");

  // Au montage → lire cookie et appliquer
  useEffect(() => {
    const savedTheme = getCookie("theme") || "light";
    setTheme(savedTheme);
    document.documentElement.setAttribute("data-theme", savedTheme);
  }, []);

  // Au changement de thème → maj <html> + cookie
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    setCookie("theme", theme, 365); // persiste 1 an
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  return (
    <button
      onClick={toggleTheme}
      className="btn btn-outline-secondary ms-2"
      aria-label="Basculer le thème"
      style={{ borderRadius: "50%" }}
    >
      {theme === "light" ? (
        <i className="bi bi-moon-fill" style={{ fontSize: "1.2rem" }}></i>
      ) : (
        <i className="bi bi-sun-fill text-warning" style={{ fontSize: "1.2rem" }}></i>
      )}
    </button>
  );
}
