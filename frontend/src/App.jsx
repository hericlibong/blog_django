import LanguageSwitcher from "./components/LanguageSwitcher.jsx";
import ThemeSwitcher from "./components/ThemeSwitcher.jsx";
import { useState, useEffect } from "react";

function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? decodeURIComponent(m.pop()) : null;
}

export default function App() {
  const [lang, setLang] = useState("fr");

  useEffect(() => {
    setLang(getCookie("django_language") || "fr");
  }, []);

  const messages = { fr: "Bienvenue sur mon site !", en: "Welcome to my website!" };

  return (
    <>
      {/* Conteneur vertical, deux blocs séparés → plus de chevauchement */}
      <div style={{ position: "fixed", top: 112, right: 20, display: "flex", flexDirection: "column", gap: "10px", alignItems: "flex-end", zIndex: 1200 }}>
        <div style={{ background: "var(--card-bg)", padding: "8px 12px", borderRadius: 8, boxShadow: "0 2px 6px rgba(0,0,0,0.15)" }}>
          <LanguageSwitcher />
        </div>
        <div style={{ background: "var(--card-bg)", padding: "6px 8px", borderRadius: 999, boxShadow: "0 2px 6px rgba(0,0,0,0.15)" }}>
          <ThemeSwitcher />
        </div>
      </div>

      {/* Toast de bienvenue */}
      <div style={{ position: "fixed", bottom: 20, right: 20, background: "var(--card-bg)", padding: "10px 15px", borderRadius: 8, boxShadow: "0 2px 6px rgba(0,0,0,0.15)" }}>
        <strong>{messages[lang]}</strong>
      </div>
    </>
  );
}
