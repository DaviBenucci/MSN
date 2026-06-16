(function () {
  var storageKey = "msn-theme-preference";
  var validPreferences = ["system", "light", "dark"];

  function readPreference() {
    try {
      var stored = window.localStorage.getItem(storageKey);
      return validPreferences.indexOf(stored) !== -1 ? stored : "system";
    } catch (error) {
      return "system";
    }
  }

  function resolveTheme(preference) {
    if (preference === "light" || preference === "dark") return preference;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  var preference = readPreference();
  var theme = resolveTheme(preference);
  var root = document.documentElement;

  root.dataset.theme = theme;
  root.dataset.themePreference = preference;
  root.style.colorScheme = theme;

  var themeColor = document.querySelector('meta[name="theme-color"]');
  if (themeColor) themeColor.setAttribute("content", theme === "dark" ? "#07111f" : "#0f3d5e");
})();
