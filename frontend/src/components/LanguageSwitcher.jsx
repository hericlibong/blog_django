// frontend/src/components/LanguageSwitcher.jsx
import { useEffect, useState } from "react";

function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? decodeURIComponent(m.pop()) : null;
}

export default function LanguageSwitcher() {
  const [lang, setLang] = useState(() => getCookie("django_language") || "fr");

  useEffect(() => {
    document.documentElement.setAttribute("lang", lang);
  }, [lang]);

  const handleChange = async (newLang) => {
    setLang(newLang);

    await fetch("/i18n/setlang/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: `language=${newLang}`,
    });

    window.location.reload();
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 12,
        right: 12,
        zIndex: 1000,
        background: "white",
        border: "1px solid #ddd",
        borderRadius: 8,
        padding: "6px 10px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        display: "flex",
        gap: 12,
        alignItems: "center",
        fontSize: 18,
        cursor: "pointer",
      }}
    >
      <span
        onClick={() => handleChange("fr")}
        style={{ filter: lang === "fr" ? "none" : "grayscale(80%)" }}
        role="button"
        aria-label="Français"
      >
        🇫🇷
      </span>
      <span
        onClick={() => handleChange("en")}
        style={{ filter: lang === "en" ? "none" : "grayscale(80%)" }}
        role="button"
        aria-label="English"
      >
        🇬🇧
      </span>
    </div>
  );
}
