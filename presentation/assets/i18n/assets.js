(function () {
  const I18N_PART = {
  "zh": {
    "assets": {
      "env_kicker": "MaholoBioBench · M0 Asset Inventory",
      "env_title": "Maholo Laboratory 环境视角",
      "assets_kicker": "MaholoBioBench · M0 Asset Inventory",
      "assets_title": "Maholo 资产清单",
      "filter_all": "全部",
      "filter_fixed": "固定场景",
      "filter_movable": "可移动物品",
      "filter_instrument": "实验仪器",
      "footer_status": "DONE / PARTIAL / NOT DONE",
      "footer_source": "robosuite_maholo assets",
      "category_fixed": "固定场景",
      "category_movable": "可移动物品",
      "category_instrument": "实验仪器",
      "status_done": "DONE",
      "status_todo": "NOT DONE"
    }
  },
  "ja": {
    "assets": {
      "env_kicker": "MaholoBioBench · M0 Asset Inventory",
      "env_title": "Maholo ラボ環境ビュー",
      "assets_kicker": "MaholoBioBench · M0 Asset Inventory",
      "assets_title": "Maholo 資産一覧",
      "filter_all": "すべて",
      "filter_fixed": "固定シーン",
      "filter_movable": "可動物",
      "filter_instrument": "実験機器",
      "footer_status": "DONE / PARTIAL / NOT DONE",
      "footer_source": "robosuite_maholo assets",
      "category_fixed": "固定シーン",
      "category_movable": "可動物",
      "category_instrument": "実験機器",
      "status_done": "DONE",
      "status_todo": "NOT DONE"
    }
  },
  "en": {
    "assets": {
      "env_kicker": "MaholoBioBench · M0 Asset Inventory",
      "env_title": "Maholo laboratory environment view",
      "assets_kicker": "MaholoBioBench · M0 Asset Inventory",
      "assets_title": "Maholo asset inventory",
      "filter_all": "All",
      "filter_fixed": "Fixed scenes",
      "filter_movable": "Movable items",
      "filter_instrument": "Instruments",
      "footer_status": "DONE / PARTIAL / NOT DONE",
      "footer_source": "robosuite_maholo assets",
      "category_fixed": "Fixed scenes",
      "category_movable": "Movable items",
      "category_instrument": "Instruments",
      "status_done": "DONE",
      "status_todo": "NOT DONE"
    }
  }
};
  window.MaholoI18N = window.MaholoI18N || {};
  for (const lang in I18N_PART) {
    window.MaholoI18N[lang] = window.MaholoI18N[lang] || {};
    Object.assign(window.MaholoI18N[lang], I18N_PART[lang]);
  }
})();
