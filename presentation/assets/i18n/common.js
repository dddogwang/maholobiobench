(function () {
  const I18N_PART = {
  "zh": {
    "lang": {
      "zh": "中文",
      "ja": "日本語",
      "en": "English"
    },
    "nav": {
      "overview": "总览",
      "tasks": "任务",
      "assets": "资产"
    }
  },
  "ja": {
    "lang": {
      "zh": "中文",
      "ja": "日本語",
      "en": "English"
    },
    "nav": {
      "overview": "概要",
      "tasks": "タスク",
      "assets": "資産"
    }
  },
  "en": {
    "lang": {
      "zh": "中文",
      "ja": "日本語",
      "en": "English"
    },
    "nav": {
      "overview": "Overview",
      "tasks": "Tasks",
      "assets": "Assets"
    }
  }
};
  window.MaholoI18N = window.MaholoI18N || {};
  for (const lang in I18N_PART) {
    window.MaholoI18N[lang] = window.MaholoI18N[lang] || {};
    Object.assign(window.MaholoI18N[lang], I18N_PART[lang]);
  }
})();
