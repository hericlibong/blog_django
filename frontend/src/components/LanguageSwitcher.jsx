// frontend/src/components/LanguageSwitcher.jsx
import { useEffect, useState } from "react";

function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? decodeURIComponent(m.pop()) : null;
}

export default function LanguageSwitcher() {
  const [lang, setLang] = useState(() => getCookie("django_language") || "fr");

  useEffect(() => {
    // Mets à jour l'attribut lang de la page
    document.documentElement.setAttribute("lang", lang);
  }, [lang]);

  const handleChange = async (newLang) => {
    setLang(newLang);

    // Envoie la nouvelle langue à Django via /i18n/setlang/
    await fetch("/i18n/setlang/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: `language=${newLang}`,
    });

    // Recharge la page pour appliquer les traductions serveur
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
        gap: 8,
        alignItems: "center",
        fontSize: 14,
      }}
    >
      <span style={{ opacity: 0.7 }}>Langue</span>
      <select
        value={lang}
        onChange={(e) => handleChange(e.target.value)}
        style={{ border: "1px solid #ccc", borderRadius: 6, padding: "4px 6px" }}
        aria-label="Sélecteur de langue"
      >
        <option value="fr">FR</option>
        <option value="en">EN</option>
      </select>
    </div>
  );
}
