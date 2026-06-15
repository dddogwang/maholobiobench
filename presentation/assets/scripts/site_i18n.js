(function () {
  const STORAGE_KEY = "maholobiobench-lang";
  const DEFAULT_LANG = "zh";

  function dictionary() {
    return window.MaholoI18N || {};
  }

  function getLang() {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored && dictionary()[stored] ? stored : DEFAULT_LANG;
  }

  function resolve(path, lang) {
    const root = dictionary()[lang];
    if (!root || !path) return null;
    return path.split(".").reduce((value, part) => {
      if (value && Object.prototype.hasOwnProperty.call(value, part)) return value[part];
      return null;
    }, root);
  }

  function translate(root, lang) {
    root.querySelectorAll("[data-i18n]").forEach((el) => {
      const value = resolve(el.dataset.i18n, lang);
      if (value != null) el.textContent = value;
    });
    root.querySelectorAll("[data-i18n-html]").forEach((el) => {
      const value = resolve(el.dataset.i18nHtml, lang);
      if (value != null) el.innerHTML = value;
    });
  }

  function setLanguage(lang) {
    const next = dictionary()[lang] ? lang : DEFAULT_LANG;
    document.documentElement.lang = next === "zh" ? "zh-CN" : next;
    document.querySelectorAll(".lang-switch button[data-lang]").forEach((button) => {
      button.classList.toggle("is-active", button.dataset.lang === next);
    });
    translate(document, next);
    localStorage.setItem(STORAGE_KEY, next);
    window.dispatchEvent(new CustomEvent("maholobiobench:langchange", { detail: { lang: next } }));
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".lang-switch button[data-lang]").forEach((button) => {
      button.addEventListener("click", () => setLanguage(button.dataset.lang));
    });
    setLanguage(getLang());
  });

  window.MaholoSiteI18n = { getLang, resolve, setLanguage, translate };
})();
