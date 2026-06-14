(function () {
  const STORAGE_KEY = "maholobiobench-lang";
  const DEFAULT_LANG = "zh";

  const I18N = {
    zh: {
      nav: {
        overview: "总览",
        tasks: "任务汇报",
        assets: "资产页",
        legacy: "旧版页",
      },
      tasks: {
        cover_kicker: "MaholoBioBench · Task Overview",
        cover_title: "当前已经定义了哪些任务",
        cover_lead: "覆盖三层级任务定义，以及对应的协议状态、评价指标和统一输出格式。",
        cover_tags: "Level 1 / Level 2 / Level 3 / Task / Status / State / Metrics / Output",
        level1_kicker: "Level 1",
        level1_title: "基础操控任务",
        level2_kicker: "Level 2",
        level2_title: "实验室技能任务",
        level3_kicker: "Level 3",
        level3_title: "长流程协议任务",
        output_kicker: "Output format",
        output_title: "统一输出格式",
        col_task: "任务",
        col_status: "状态",
        col_state: "协议状态",
        col_metrics: "评价指标",
        status_done: "已实现",
        status_partial: "部分实现",
        status_todo: "未实现",
      },
      assets: {
        env_kicker: "MaholoBioBench · M0 Asset Inventory",
        env_title: "Maholo Laboratory 环境视角",
        assets_kicker: "MaholoBioBench · M0 Asset Inventory",
        assets_title: "Maholo 资产清单",
        filter_all: "全部",
        filter_fixed: "固定场景",
        filter_movable: "可移动物品",
        filter_instrument: "实验仪器",
        footer_status: "DONE / PARTIAL / NOT DONE",
        footer_source: "robosuite_maholo assets",
      },
    },
    ja: {
      nav: {
        overview: "概要",
        tasks: "タスク報告",
        assets: "資産ページ",
        legacy: "旧版ページ",
      },
      tasks: {
        cover_kicker: "MaholoBioBench · Task Overview",
        cover_title: "どのタスクが定義済みか",
        cover_lead: "3 層のタスク定義と、対応するプロトコル状態・評価指標・統一出力形式を扱う。",
        level1_kicker: "Level 1",
        level1_title: "基礎操作タスク",
        level2_kicker: "Level 2",
        level2_title: "ラボ技能タスク",
        level3_kicker: "Level 3",
        level3_title: "長期プロトコルタスク",
        output_kicker: "Output format",
        output_title: "統一出力形式",
        col_task: "タスク",
        col_status: "状態",
        col_state: "プロトコル状態",
        col_metrics: "評価指標",
        status_done: "実装済み",
        status_partial: "一部実装",
        status_todo: "未実装",
      },
      assets: {
        env_kicker: "MaholoBioBench · M0 Asset Inventory",
        env_title: "Maholo ラボ環境ビュー",
        assets_kicker: "MaholoBioBench · M0 Asset Inventory",
        assets_title: "Maholo 資産一覧",
        filter_all: "すべて",
        filter_fixed: "固定シーン",
        filter_movable: "可動物",
        filter_instrument: "実験機器",
        footer_status: "DONE / PARTIAL / NOT DONE",
        footer_source: "robosuite_maholo assets",
      },
    },
    en: {
      nav: {
        overview: "Overview",
        tasks: "Task Report",
        assets: "Assets",
        legacy: "Legacy",
      },
      tasks: {
        cover_kicker: "MaholoBioBench · Task Overview",
        cover_title: "Which tasks are already defined",
        cover_lead: "Covers three task levels, plus protocol state, evaluation metrics, and a unified output format.",
        level1_kicker: "Level 1",
        level1_title: "Basic Manipulation Tasks",
        level2_kicker: "Level 2",
        level2_title: "Laboratory Skill Tasks",
        level3_kicker: "Level 3",
        level3_title: "Long-Horizon Protocol Tasks",
        output_kicker: "Output format",
        output_title: "Unified output format",
        col_task: "Task",
        col_status: "Status",
        col_state: "Protocol state",
        col_metrics: "Metrics",
        status_done: "Implemented",
        status_partial: "Partially implemented",
        status_todo: "Not implemented",
      },
      assets: {
        env_kicker: "MaholoBioBench · M0 Asset Inventory",
        env_title: "Maholo laboratory environment view",
        assets_kicker: "MaholoBioBench · M0 Asset Inventory",
        assets_title: "Maholo asset inventory",
        filter_all: "All",
        filter_fixed: "Fixed scenes",
        filter_movable: "Movable items",
        filter_instrument: "Instruments",
        footer_status: "DONE / PARTIAL / NOT DONE",
        footer_source: "robosuite_maholo assets",
      },
    },
  };

  function getLang() {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored && I18N[stored] ? stored : DEFAULT_LANG;
  }

  function resolve(path, lang) {
    return path.split(".").reduce((acc, part) => (acc && acc[part] != null ? acc[part] : null), I18N[lang]);
  }

  function translate(root, lang) {
    root.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.dataset.i18n;
      const value = resolve(key, lang);
      if (value != null) {
        el.textContent = value;
      }
    });
  }

  function setLanguage(lang) {
    const next = I18N[lang] ? lang : DEFAULT_LANG;
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

  window.MaholoSiteI18n = { getLang, setLanguage, translate, I18N };
})();
