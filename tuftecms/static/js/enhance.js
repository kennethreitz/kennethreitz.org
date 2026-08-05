/* Progressive enhancements: internal-link hover previews, heading
   anchor links, and theme-color sync. Everything here degrades to
   nothing — the site reads fine without it. */

(function () {
    "use strict";

    /* =========================================
       Internal link hover previews
       ========================================= */

    // Pointer-driven devices only; touch gets no hover cards.
    var canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

    // Routes that are apps or feeds, not articles — never previewable.
    var SKIP_PREFIXES = [
        "/archive", "/search", "/random", "/graph", "/api/", "/static/",
        "/feed", "/rss", "/sitemap", "/og-image", "/thumb/",
    ];
    var SKIP_EXTENSIONS = /\.(pdf|md|xml|png|jpe?g|gif|svg|webp|txt|ico|zip)$/i;

    function previewPath(href) {
        if (!href || href.indexOf("/") !== 0 || href.indexOf("//") === 0) return null;
        if (href.indexOf("#") !== -1 || href.indexOf("?") !== -1) return null;
        if (SKIP_EXTENSIONS.test(href)) return null;
        for (var i = 0; i < SKIP_PREFIXES.length; i++) {
            if (href.indexOf(SKIP_PREFIXES[i]) === 0) return null;
        }
        var path = href.replace(/\/+$/, "");
        if (!path || path === window.location.pathname.replace(/\/+$/, "")) return null;
        return path.slice(1); // drop leading slash for the API
    }

    if (canHover) {
        var cache = {};          // path -> preview data, or null for "no card"
        var card = null;
        var currentLink = null;
        var showTimer = null;
        var hideTimer = null;

        function buildCard() {
            card = document.createElement("div");
            card.className = "link-preview";
            card.setAttribute("role", "tooltip");
            card.addEventListener("mouseenter", function () {
                clearTimeout(hideTimer);
            });
            card.addEventListener("mouseleave", scheduleHide);
            document.body.appendChild(card);
        }

        function renderCard(data) {
            var head = document.createElement("div");
            head.className = "link-preview-head";
            if (data.icon) {
                var img = document.createElement("img");
                img.src = data.icon;
                img.alt = "";
                img.className = "link-preview-icon";
                head.appendChild(img);
            }
            var title = document.createElement("span");
            title.className = "link-preview-title";
            title.textContent = data.title;
            head.appendChild(title);

            card.textContent = "";
            card.appendChild(head);

            if (data.excerpt) {
                var excerpt = document.createElement("p");
                excerpt.className = "link-preview-excerpt";
                excerpt.textContent = data.excerpt;
                card.appendChild(excerpt);
            }

            var metaParts = [];
            if (data.section) metaParts.push(data.section);
            if (data.date) metaParts.push(data.date);
            if (data.reading_time) metaParts.push(data.reading_time + " min read");
            if (metaParts.length) {
                var meta = document.createElement("div");
                meta.className = "link-preview-meta";
                meta.textContent = metaParts.join(" · ");
                card.appendChild(meta);
            }
        }

        function positionCard(link) {
            var rect = link.getBoundingClientRect();
            var margin = 16;
            card.style.visibility = "hidden";
            card.classList.add("visible");
            var cardRect = card.getBoundingClientRect();

            var left = rect.left + window.scrollX;
            var maxLeft = window.scrollX + document.documentElement.clientWidth - cardRect.width - margin;
            left = Math.max(window.scrollX + margin, Math.min(left, maxLeft));

            var top = rect.bottom + window.scrollY + 10;
            var spaceBelow = window.innerHeight - rect.bottom;
            if (spaceBelow < cardRect.height + 24 && rect.top > cardRect.height + 24) {
                top = rect.top + window.scrollY - cardRect.height - 10;
            }

            card.style.left = left + "px";
            card.style.top = top + "px";
            card.style.visibility = "";
        }

        function showCard(link, data) {
            if (!card) buildCard();
            renderCard(data);
            positionCard(link);
        }

        function hideCard() {
            if (card) card.classList.remove("visible");
            currentLink = null;
        }

        function scheduleHide() {
            clearTimeout(hideTimer);
            hideTimer = setTimeout(hideCard, 220);
        }

        function fetchPreview(path, callback) {
            if (path in cache) {
                callback(cache[path]);
                return;
            }
            fetch("/api/preview/" + path)
                .then(function (r) { return r.ok ? r.json() : null; })
                .then(function (data) {
                    cache[path] = data && data.success ? data : null;
                    callback(cache[path]);
                })
                .catch(function () {
                    cache[path] = null;
                    callback(null);
                });
        }

        function onEnter(link, path) {
            clearTimeout(showTimer);
            clearTimeout(hideTimer);
            showTimer = setTimeout(function () {
                fetchPreview(path, function (data) {
                    // The pointer may have moved on while we fetched.
                    if (data && link.matches(":hover")) {
                        currentLink = link;
                        showCard(link, data);
                    }
                });
            }, 320);
        }

        document.addEventListener("mouseover", function (e) {
            var link = e.target.closest && e.target.closest("main a[href]");
            if (!link) return;
            if (link.closest(".link-preview")) return;
            var path = previewPath(link.getAttribute("href"));
            if (!path) return;
            if (currentLink === link) {
                clearTimeout(hideTimer);
                return;
            }
            onEnter(link, path);
        });

        document.addEventListener("mouseout", function (e) {
            var link = e.target.closest && e.target.closest("main a[href]");
            if (!link) return;
            clearTimeout(showTimer);
            if (currentLink === link) scheduleHide();
        });

        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape") {
                clearTimeout(showTimer);
                hideCard();
            }
        });

        window.addEventListener("scroll", function () {
            if (currentLink) {
                clearTimeout(showTimer);
                hideCard();
            }
        }, { passive: true });
    }

    /* =========================================
       Heading anchor links (§ on hover)
       ========================================= */

    document.addEventListener("DOMContentLoaded", function () {
        var headings = document.querySelectorAll(
            ".post-body h2[id], .post-body h3[id], .post-body h4[id]"
        );
        headings.forEach(function (heading) {
            var anchor = document.createElement("a");
            anchor.className = "heading-anchor";
            anchor.href = "#" + heading.id;
            anchor.textContent = "§";
            anchor.setAttribute("aria-label", "Link to this section");
            heading.appendChild(anchor);
        });
    });

    /* =========================================
       Theme-color follows the theme toggle
       ========================================= */

    function syncThemeColor() {
        var dark = document.body.classList.contains("dark-mode");
        var color = dark ? "#0d1117" : "#fffff8";
        document.querySelectorAll('meta[name="theme-color"]').forEach(function (meta) {
            meta.setAttribute("content", color);
            meta.removeAttribute("media");
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        // The body class is authoritative (saved theme may differ from the
        // OS preference), so sync once at load and again on every toggle.
        syncThemeColor();
        var toggle = document.getElementById("theme-toggle");
        if (toggle) toggle.addEventListener("click", syncThemeColor);
    });
})();
