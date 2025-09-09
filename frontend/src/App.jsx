import LanguageSwitcher from "./components/LanguageSwitcher.jsx";
import { useState, useEffect } from "react";

function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? decodeURIComponent(m.pop()) : null;
}

export default function App() {
  const [lang, setLang] = useState(() => getCookie("preferred_lang") || "fr");

  useEffect(() => {
    const observer = new MutationObserver(() => {
      setLang(document.documentElement.lang);
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
    return () => observer.disconnect();
  }, []);

  const messages = {
    fr: "Bienvenue sur mon site !",
    en: "Welcome to my website!"
  };

  return (
    <>
      <LanguageSwitcher />
      <div style={{ position: "fixed", bottom: 20, right: 20, background: "#f8f9fa", padding: "10px 15px", borderRadius: 8, boxShadow: "0 2px 6px rgba(0,0,0,0.15)" }}>
        <strong>{messages[lang]}</strong>
      </div>
    </>
  );
}
