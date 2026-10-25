// Override of Blowfish v3.6.0 assets/js/appearance.js.
//
// The theme's version only ever adds the `dark` class for the system, so a
// dark site default kept light-system visitors in dark, and one click on the
// switcher pinned the choice in localStorage for good. Here the page follows
// the system until the visitor picks the other appearance; toggling back to
// what the system shows clears the choice and the page follows the system
// again. Everything below the appearance logic is unchanged from the theme.

const sitePreference = document.documentElement.getAttribute("data-default-appearance");
const autoAppearance = document.documentElement.getAttribute("data-auto-appearance") === "true";
const systemDarkQuery = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

// The visitor's explicit choice, or null when they have not made one.
var readPreference = () => {
  try {
    const value = localStorage.getItem("appearance");
    return value === "dark" || value === "light" ? value : null;
  } catch (e) {
    return null;
  }
};

var writePreference = (value) => {
  try {
    if (value === null) {
      localStorage.removeItem("appearance");
    } else {
      localStorage.setItem("appearance", value);
    }
  } catch (e) {}
};

// What the page shows when the visitor has not chosen.
var systemAppearance = () => {
  if (autoAppearance && systemDarkQuery) {
    return systemDarkQuery.matches ? "dark" : "light";
  }
  return sitePreference === "dark" ? "dark" : "light";
};

var applyAppearance = (appearance) => {
  document.documentElement.classList.toggle("dark", appearance === "dark");
};

applyAppearance(readPreference() || systemAppearance());

// Mermaid dark mode support
var updateMermaidTheme = () => {
  if (typeof mermaid !== 'undefined') {
    const isDark = document.documentElement.classList.contains("dark");

    const mermaids = document.querySelectorAll('pre.mermaid');
    mermaids.forEach(e => {
      if (e.getAttribute('data-processed')) {
        // Already rendered, clean the processed attributes
        e.removeAttribute('data-processed');
        // Replace the rendered HTML with the stored text
        e.innerHTML = e.getAttribute('data-graph');
      } else {
        // First time, store the text
        e.setAttribute('data-graph', e.textContent);
      }
    });

    if (isDark) {
      initMermaidDark();
      mermaid.run();
    } else {
      initMermaidLight();
      mermaid.run();
    }
  }
}

window.addEventListener("DOMContentLoaded", (event) => {
  const switcher = document.getElementById("appearance-switcher");
  const switcherMobile = document.getElementById("appearance-switcher-mobile");

  // Load the i18n translations for the tooltips
  const darkLabel = {{ i18n "footer.dark_appearance" | jsonify }};
  const lightLabel = {{ i18n "footer.light_appearance" | jsonify }};

  // Helper to update the tooltip depending on the current mode
  const updateTooltip = (targetAppearance) => {
    // If target is dark, the next action will be switching to light
    const label = targetAppearance === "dark" ? lightLabel : darkLabel;
    if (switcher) {
      switcher.setAttribute("aria-label", label);
      switcher.setAttribute("title", label);
    }
    if (switcherMobile) {
      switcherMobile.setAttribute("aria-label", label);
      switcherMobile.setAttribute("title", label);
    }
  };

  // Show an appearance and bring everything that depends on it along.
  const showAppearance = (appearance) => {
    applyAppearance(appearance);
    updateMeta();
    updateMermaidTheme();
    updateTooltip(appearance);
    this.updateLogo?.(appearance);
  };

  updateMeta();
  this.updateLogo?.(getTargetAppearance());

  // Initialize mermaid theme on page load
  updateMermaidTheme();

  // Set initial tooltip on load
  updateTooltip(getTargetAppearance());

  // Picking what the system already shows means "follow the system".
  const toggle = () => {
    const next = getTargetAppearance() === "dark" ? "light" : "dark";
    writePreference(next === systemAppearance() ? null : next);
    showAppearance(next);
  };

  if (switcher) {
    switcher.addEventListener("click", toggle);
  }
  if (switcherMobile) {
    switcherMobile.addEventListener("click", toggle);
  }

  // The system changed while the page is open: follow it unless the visitor
  // has chosen otherwise.
  if (autoAppearance && systemDarkQuery) {
    systemDarkQuery.addEventListener("change", () => {
      if (readPreference() === null) {
        showAppearance(systemAppearance());
      }
    });
  }

  // A choice made in another tab applies here too.
  window.addEventListener("storage", (event) => {
    if (event.key === "appearance" || event.key === null) {
      showAppearance(readPreference() || systemAppearance());
    }
  });
});


var updateMeta = () => {
  var elem, style;
  elem = document.querySelector('body');
  style = getComputedStyle(elem);
  document.querySelector('meta[name="theme-color"]').setAttribute('content', style.backgroundColor);
}

{{ if and (.Site.Params.Logo) (.Site.Params.SecondaryLogo) }}
{{ $primaryLogo := resources.Get .Site.Params.Logo }}
{{ $secondaryLogo := resources.Get .Site.Params.SecondaryLogo }}
{{ if and ($primaryLogo) ($secondaryLogo) }}
var updateLogo = (targetAppearance) => {
  var imgElems = document.querySelectorAll("img.logo");
  var logoContainers = document.querySelectorAll("span.logo");

  targetLogoPath =
    targetAppearance == "{{ .Site.Params.DefaultAppearance }}" ?
    "{{ $primaryLogo.RelPermalink }}" : "{{ $secondaryLogo.RelPermalink }}"
  for (const elem of imgElems) {
    elem.setAttribute("src", targetLogoPath)
  }

  {{ if eq $primaryLogo.MediaType.SubType "svg" }}
  targetContent =
    targetAppearance == "{{ .Site.Params.DefaultAppearance }}" ?
    `{{ $primaryLogo.Content | safeHTML }}` : `{{ $secondaryLogo.Content | safeHTML }}`
  for (const container of logoContainers) {
    container.innerHTML = targetContent;
  }
  {{ end }}
}
{{ end }}
{{- end }}

var getTargetAppearance = () => {
  return document.documentElement.classList.contains("dark") ? "dark" : "light"
}

window.addEventListener("DOMContentLoaded", (event) => {
  const scroller = document.getElementById("top-scroller");
  const footer = document.getElementById("site-footer");
  if(scroller && footer && scroller.getBoundingClientRect().top > footer.getBoundingClientRect().top) {
    scroller.hidden = true;
  }
});
