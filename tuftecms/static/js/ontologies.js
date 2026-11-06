/* Ontologies explorer. The picture is derived from /ontologies/data. */
(function () {
    const app = document.getElementById("ontology-app");
    if (!app || typeof d3 === "undefined") return;

    const canvas = document.getElementById("ontology-canvas");
    const wrap = document.getElementById("ontology-wrap");
    const ctx = canvas.getContext("2d");
    const statsEl = document.getElementById("ontology-stats");
    const panel = document.getElementById("ontology-panel");
    const sectionsEl = document.getElementById("ontology-sections");
    const domainsEl = document.getElementById("ontology-domains");
    const resultsEl = document.getElementById("ontology-results");
    const queryEl = document.getElementById("ontology-q");
    const emptyEl = document.getElementById("ontology-empty");

    let data = null;
    let byId = new Map();
    let sectionFilter = "";
    let domainFilter = "";
    let pin = null;
    let selectedId = "";
    let hoverId = "";
    let transform = d3.zoomIdentity;
    let userScale = 1;
    let placed = [];
    let placedLinks = [];
    let layoutKey = "";
    let simulation = null;
    let frameTimer = 0;
    const hubCount = new Map();
    const degree = new Map();

    // Plain wheel scrolls the page. Zoom is pinch, modifier+wheel, or the buttons.
    canvas.addEventListener("wheel", (event) => {
        if (!(event.ctrlKey || event.metaKey)) return;
        event.preventDefault();
        zoomAt(event.clientX, event.clientY, event.deltaY < 0 ? 1.08 : 1 / 1.08);
    }, { passive: false });

    let pinch = null;
    canvas.addEventListener("touchstart", (event) => {
        if (event.touches.length === 2) {
            pinch = { dist: touchDist(event.touches), scale: userScale, x: touchMid(event.touches).x, y: touchMid(event.touches).y };
        }
    }, { passive: true });
    canvas.addEventListener("touchmove", (event) => {
        if (event.touches.length !== 2 || !pinch) return;
        event.preventDefault();
        const mid = touchMid(event.touches);
        const factor = touchDist(event.touches) / pinch.dist;
        userScale = clampScale(pinch.scale * factor);
        sizeToGraph();
        const screenX = canvas.getBoundingClientRect().left + transform.x;
        const screenY = canvas.getBoundingClientRect().top + transform.y;
        window.scrollBy(screenX - mid.x, screenY - mid.y);
    }, { passive: false });
    canvas.addEventListener("touchend", () => { pinch = null; });

    document.getElementById("ontology-zoom-in").addEventListener("click", () => {
        zoomAt(window.innerWidth / 2, window.innerHeight / 2, 1.2);
    });
    document.getElementById("ontology-zoom-out").addEventListener("click", () => {
        zoomAt(window.innerWidth / 2, window.innerHeight / 2, 1 / 1.2);
    });

    let pointer = null;
    canvas.addEventListener("pointerdown", (event) => {
        const node = hit(event);
        pointer = { x: event.clientX, y: event.clientY, node: node, moved: false };
        if (node) {
            event.preventDefault();
            canvas.setPointerCapture(event.pointerId);
            node.fx = node.x;
            node.fy = node.y;
            if (simulation) simulation.alphaTarget(0.2).restart();
        }
    });
    canvas.addEventListener("pointermove", (event) => {
        if (pointer && (Math.abs(event.clientX - pointer.x) > 4 || Math.abs(event.clientY - pointer.y) > 4)) {
            pointer.moved = true;
        }
        if (pointer && pointer.node && pointer.moved) {
            const rect = canvas.getBoundingClientRect();
            pointer.node.fx = (event.clientX - rect.left - transform.x) / transform.k;
            pointer.node.fy = (event.clientY - rect.top - transform.y) / transform.k;
            pointer.node.x = pointer.node.fx;
            pointer.node.y = pointer.node.fy;
            draw();
            return;
        }
        const node = hit(event);
        const next = node ? node.id : "";
        if (next !== hoverId) {
            hoverId = next;
            draw();
        }
    });
    canvas.addEventListener("pointerup", () => {
        if (pointer && pointer.node) {
            pointer.node.fx = null;
            pointer.node.fy = null;
            if (simulation) simulation.alphaTarget(0);
            if (!pointer.moved) pick(pointer.node);
            else scheduleFrame();
        }
        pointer = null;
    });
    canvas.addEventListener("pointerleave", () => {
        hoverId = "";
        draw();
    });

    document.getElementById("ontology-reset").addEventListener("click", () => {
        sectionFilter = "";
        domainFilter = "";
        pin = null;
        selectedId = "";
        if (location.hash) history.replaceState(null, "", location.pathname);
        render();
    });

    queryEl.addEventListener("input", showResults);
    queryEl.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            resultsEl.hidden = true;
            queryEl.blur();
        } else if (event.key === "Enter") {
            const first = resultsEl.querySelector("button");
            if (first) {
                event.preventDefault();
                first.click();
            }
        }
    });

    window.addEventListener("resize", () => {
        layoutKey = "";
        render();
    });

    new MutationObserver(() => draw()).observe(document.body, {
        attributes: true,
        attributeFilter: ["class"],
    });

    fetch("/ontologies/data")
        .then((res) => {
            if (!res.ok) throw new Error("status " + res.status);
            return res.json();
        })
        .then((payload) => {
            data = payload;
            byId = new Map(data.nodes.map((node) => [node.id, node]));
            data.nodes.forEach((node) => {
                if (!node.hub) return;
                hubCount.set(node.hub, (hubCount.get(node.hub) || 0) + 1);
            });
            data.edges.forEach((edge) => {
                degree.set(edge.source, (degree.get(edge.source) || 0) + 1);
                degree.set(edge.target, (degree.get(edge.target) || 0) + 1);
            });
            const hashed = decodeURIComponent(location.hash.replace(/^#/, ""));
            if (hashed && byId.has(hashed)) {
                pin = { type: "near", id: hashed };
                selectedId = hashed;
            }
            render();
        })
        .catch(() => {
            statsEl.textContent = "The map could not be read.";
        });

    function touchDist(touches) {
        return Math.hypot(touches[0].clientX - touches[1].clientX, touches[0].clientY - touches[1].clientY);
    }

    function touchMid(touches) {
        return {
            x: (touches[0].clientX + touches[1].clientX) / 2,
            y: (touches[0].clientY + touches[1].clientY) / 2,
        };
    }

    function clampScale(value) {
        return Math.max(0.45, Math.min(2.8, value));
    }

    function zoomAt(clientX, clientY, factor) {
        const prev = userScale;
        const next = clampScale(prev * factor);
        if (next === prev || !placed.length) return;
        const wx = (clientX - canvas.getBoundingClientRect().left - transform.x) / prev;
        const wy = (clientY - canvas.getBoundingClientRect().top - transform.y) / prev;
        userScale = next;
        sizeToGraph();
        const screenX = canvas.getBoundingClientRect().left + transform.x + wx * userScale;
        const screenY = canvas.getBoundingClientRect().top + transform.y + wy * userScale;
        window.scrollBy(screenX - clientX, screenY - clientY);
    }

    function scheduleFrame() {
        if (frameTimer) return;
        frameTimer = window.setTimeout(() => {
            frameTimer = 0;
            sizeToGraph();
        }, 80);
    }

    function cssVar(name) {
        return getComputedStyle(document.body).getPropertyValue(name).trim();
    }

    function isDark() {
        const body = document.body;
        if (body.classList.contains("dark-mode")) return true;
        if (body.classList.contains("light-mode")) return false;
        return window.matchMedia("(prefers-color-scheme: dark)").matches;
    }

    function colorFor(node) {
        const key = node.section === "knowledge"
            ? (node.domain || "knowledge")
            : (node.kind === "theme" ? node.id : node.section);
        let hash = 0;
        for (let i = 0; i < key.length; i++) hash = (hash * 33 + key.charCodeAt(i)) >>> 0;
        const hue = (hash * 47) % 360;
        return isDark()
            ? "hsl(" + hue + " 42% 68%)"
            : "hsl(" + hue + " 36% 34%)";
    }

    function sectionTitle(id) {
        const found = (data.sections || []).find((section) => section.id === id);
        return found ? found.title : id;
    }

    function domainTitle(id) {
        const found = (data.domains || []).find((domain) => domain.id === id);
        return found ? found.title : id;
    }

    function esc(value) {
        return String(value || "").replace(/[&<>"']/g, (ch) => ({
            "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
        }[ch]));
    }

    function overviewNodes() {
        return data.nodes.filter((node) => node.overview);
    }

    function connectionsOf(id) {
        const map = new Map();
        data.edges.forEach((edge) => {
            const other = edge.source === id ? edge.target : edge.target === id ? edge.source : null;
            if (!other) return;
            const node = byId.get(other);
            if (!node) return;
            let rec = map.get(other);
            if (!rec) {
                rec = { node: node, kinds: [], labels: [] };
                map.set(other, rec);
            }
            edge.kinds.forEach((kind) => {
                if (!rec.kinds.includes(kind)) rec.kinds.push(kind);
            });
            (edge.labels || []).forEach((label) => {
                if (label && !rec.labels.includes(label)) rec.labels.push(label);
            });
        });
        const rank = (item) => item.kinds.includes("correspondence") ? 0
            : (item.kinds.includes("theme") || item.kinds.includes("tag") || item.kinds.includes("series")) ? 1
            : 2;
        return [...map.values()].sort((a, b) => rank(a) - rank(b) || a.node.title.localeCompare(b.node.title));
    }

    function linkedIds(ids) {
        const score = new Map();
        data.edges.forEach((edge) => {
            let other = null;
            if (ids.has(edge.source) && !ids.has(edge.target)) other = edge.target;
            else if (ids.has(edge.target) && !ids.has(edge.source)) other = edge.source;
            if (!other) return;
            const bump = (edge.kinds || []).includes("correspondence") ? 3
                : ((edge.kinds || []).includes("theme") || (edge.kinds || []).includes("tag")) ? 2
                : 1;
            score.set(other, (score.get(other) || 0) + bump);
        });
        return [...score.entries()].sort((a, b) => b[1] - a[1]);
    }

    function expandHub(hub) {
        const hubNode = byId.get(hub);
        const members = data.nodes.filter((node) => node.hub === hub || node.id === hub);
        const ids = new Set(members.map((node) => node.id));
        const isDomain = hubNode && hubNode.section === "knowledge" && hubNode.kind === "domain";
        const isTheme = hubNode && hubNode.kind === "theme";
        const cap = isTheme ? 60 : isDomain ? 36 : 12;
        const extra = [];
        linkedIds(ids).forEach(([id]) => {
            if (extra.length >= cap) return;
            const node = byId.get(id);
            if (!node || ids.has(node.id)) return;
            if (!isDomain && !isTheme && node.kind === "page" && node.section !== "pages") return;
            extra.push(node);
            ids.add(node.id);
        });
        return members.concat(extra);
    }

    function neighborhood(id) {
        const center = byId.get(id);
        if (!center) return [];
        const out = [center];
        connectionsOf(id).forEach((item) => {
            if (out.length <= 48) out.push(item.node);
        });
        return out;
    }

    function intersection(domainUrl, sectionId) {
        const inDomain = new Set(data.nodes.filter((node) => node.hub === domainUrl).map((node) => node.id));
        const hit = new Set();
        data.edges.forEach((edge) => {
            if (inDomain.has(edge.source) && byId.get(edge.target) && byId.get(edge.target).section === sectionId) {
                hit.add(edge.target);
            }
            if (inDomain.has(edge.target) && byId.get(edge.source) && byId.get(edge.source).section === sectionId) {
                hit.add(edge.source);
            }
        });
        const nodes = data.nodes.filter((node) => hit.has(node.id));
        const hub = byId.get(domainUrl);
        if (hub) nodes.unshift(hub);
        return nodes;
    }

    function linksAmong(list) {
        const ids = new Set(list.map((node) => node.id));
        return data.edges.filter((edge) => ids.has(edge.source) && ids.has(edge.target));
    }

    function overviewLinks(visible) {
        const ids = new Set(visible.map((node) => node.id));
        const weights = new Map();
        data.edges.forEach((edge) => {
            const a = byId.get(edge.source) && byId.get(edge.source).hub;
            const b = byId.get(edge.target) && byId.get(edge.target).hub;
            if (!a || !b || a === b || !ids.has(a) || !ids.has(b)) return;
            const key = a < b ? a + "\n" + b : b + "\n" + a;
            weights.set(key, (weights.get(key) || 0) + 1);
        });
        const all = [];
        weights.forEach((weight, key) => {
            const parts = key.split("\n");
            all.push({ source: parts[0], target: parts[1], weight: weight, kinds: [] });
        });
        all.sort((a, b) => b.weight - a.weight);
        const keep = new Set();
        const best = new Map();
        all.forEach((link) => {
            [link.source, link.target].forEach((end) => {
                const prev = best.get(end);
                if (!prev || prev.weight < link.weight) best.set(end, link);
            });
        });
        best.forEach((link) => keep.add(link));
        all.slice(0, 28).forEach((link) => keep.add(link));
        return [...keep];
    }

    function current() {
        if (pin && pin.type === "near") {
            const nodes = neighborhood(pin.id);
            const title = (byId.get(pin.id) && byId.get(pin.id).title) || "Page";
            return { mode: "detail", nodes: nodes, links: linksAmong(nodes), label: title + " neighborhood" };
        }
        if (domainFilter && sectionFilter && !["knowledge", "themes", "pages"].includes(sectionFilter)) {
            const nodes = intersection(domainFilter, sectionFilter);
            const domain = data.domains.find((item) => item.url === domainFilter);
            const section = data.sections.find((item) => item.id === sectionFilter);
            const label = (section ? section.title : "Pages") + " connected to " + (domain ? domain.title : "this domain");
            return { mode: "detail", nodes: nodes, links: linksAmong(nodes), label: label };
        }
        if (domainFilter) {
            const nodes = expandHub(domainFilter);
            const domain = data.domains.find((item) => item.url === domainFilter);
            return { mode: "detail", nodes: nodes, links: linksAmong(nodes), label: domain ? domain.title : "Domain" };
        }
        if (sectionFilter === "knowledge") {
            const nodes = overviewNodes().filter((node) => node.section === "knowledge");
            return { mode: "overview", nodes: nodes, links: overviewLinks(nodes), label: "Knowledge" };
        }
        if (sectionFilter === "themes") {
            const nodes = overviewNodes().filter((node) => node.kind === "theme");
            return { mode: "overview", nodes: nodes, links: overviewLinks(nodes), label: "Themes" };
        }
        if (sectionFilter === "pages") {
            const nodes = data.nodes.filter((node) => node.section === "pages");
            return { mode: "detail", nodes: nodes, links: linksAmong(nodes), label: "Pages" };
        }
        if (sectionFilter) {
            const nodes = expandHub("/" + sectionFilter);
            const section = data.sections.find((item) => item.id === sectionFilter);
            return { mode: "detail", nodes: nodes, links: linksAmong(nodes), label: section ? section.title : sectionFilter };
        }
        if (pin && pin.type === "hub") {
            const nodes = expandHub(pin.id);
            const title = (byId.get(pin.id) && byId.get(pin.id).title) || "Opened";
            return { mode: "detail", nodes: nodes, links: linksAmong(nodes), label: title };
        }
        const nodes = overviewNodes();
        return { mode: "overview", nodes: nodes, links: overviewLinks(nodes), label: "All systems" };
    }

    function render() {
        if (!data) return;
        const view = current();
        paintChips();
        paintStats(view);
        paintPanel();
        emptyEl.hidden = view.nodes.length > 0;
        ensureLayout(view);
        draw();
    }

    function paintChips() {
        const sectionButtons = [{ id: "", title: "All" }].concat(data.sections.map((section) => ({
            id: section.id,
            title: section.title,
        })));
        sectionsEl.innerHTML = sectionButtons.map((section) => {
            const pressed = section.id === sectionFilter;
            return '<button type="button" data-section="' + esc(section.id) + '" class="' + (pressed ? "active" : "") + '" aria-pressed="' + pressed + '">' + esc(section.title) + "</button>";
        }).join("");
        sectionsEl.querySelectorAll("button").forEach((button) => {
            button.addEventListener("click", () => {
                sectionFilter = button.getAttribute("data-section") || "";
                pin = null;
                selectedId = "";
                render();
            });
        });

        const domainButtons = [{ url: "", title: "All domains" }].concat(data.domains);
        domainsEl.innerHTML = domainButtons.map((domain) => {
            const pressed = (domain.url || "") === domainFilter;
            return '<button type="button" data-domain="' + esc(domain.url || "") + '" class="' + (pressed ? "active" : "") + '" aria-pressed="' + pressed + '">' + esc(domain.title) + "</button>";
        }).join("");
        domainsEl.querySelectorAll("button").forEach((button) => {
            button.addEventListener("click", () => {
                domainFilter = button.getAttribute("data-domain") || "";
                pin = null;
                selectedId = domainFilter;
                render();
            });
        });
    }

    function paintStats(view) {
        if (view.mode === "overview" && !sectionFilter && !domainFilter && !pin) {
            const themes = data.nodes.filter((node) => node.kind === "theme").length;
            statsEl.textContent = data.domains.length + " domains · " + themes + " themes · " + data.nodes.length + " pages";
            return;
        }
        const noun = view.nodes.length === 1 ? "page" : "pages";
        statsEl.textContent = view.label + " · " + view.nodes.length + " " + noun + " on the map";
    }

    function paintPanel() {
        const node = byId.get(selectedId);
        if (!node) {
            panel.innerHTML = '<p class="ontology-hint">Select a point on the map, or search for a page.</p>';
            return;
        }
        const bits = [sectionTitle(node.section)];
        if (node.section === "knowledge" && node.kind === "page") bits.push(domainTitle(node.domain));
        else if (node.kind === "domain") bits.push("domain");
        else if (node.kind === "theme") bits[0] = "Theme";
        else if (node.kind === "section") bits[0] = "Shelf";
        const links = [];
        if (node.url) links.push('<a href="' + esc(node.url) + '">Read the page</a>');
        links.push('<button type="button" class="ontology-textbtn" data-act="near">Neighborhood</button>');
        if (node.hub && node.id !== node.hub) {
            links.push('<button type="button" class="ontology-textbtn" data-act="hub">Show this group</button>');
        }
        let tags = "";
        if (node.tags && node.tags.length) {
            tags = '<p class="ontology-tags">Tagged ' + esc(node.tags.join(", ")) + "</p>";
        }
        const grouped = node.kind === "domain" || node.kind === "section"
            ? insideAndBeyond(node)
            : groupConnections(connectionsOf(node.id));
        let lists = "";
        grouped.forEach((group) => {
            if (!group.items.length) return;
            const shown = group.items.slice(0, 24);
            lists += "<h3>" + esc(group.title) + "</h3><ul>";
            shown.forEach((item) => {
                const note = item.labels[0] ? '<span>' + esc(item.labels[0]) + "</span>" : "";
                lists += '<li><button type="button" class="ontology-jump" data-id="' + esc(item.node.id) + '">' + esc(item.node.title) + note + "</button></li>";
            });
            lists += "</ul>";
            if (group.items.length > shown.length) {
                lists += '<p class="ontology-more">And ' + (group.items.length - shown.length) + " more.</p>";
            }
        });
        panel.innerHTML = '<p class="ontology-kicker">' + esc(bits.join(" · ")) + "</p>"
            + "<h2>" + esc(node.title) + "</h2>"
            + (node.summary ? '<p class="ontology-summary">' + esc(node.summary) + "</p>" : "")
            + tags
            + '<p class="ontology-actions">' + links.join("") + "</p>"
            + lists;
        panel.querySelector('[data-act="near"]').addEventListener("click", () => openNeighborhood(node.id));
        const hubBtn = panel.querySelector('[data-act="hub"]');
        if (hubBtn) {
            hubBtn.addEventListener("click", () => {
                pin = { type: "hub", id: node.hub };
                sectionFilter = "";
                domainFilter = "";
                selectedId = node.hub;
                render();
            });
        }
        panel.querySelectorAll(".ontology-jump").forEach((button) => {
            button.addEventListener("click", () => {
                const id = button.getAttribute("data-id");
                selectedId = id;
                if (pin && pin.type === "near") openNeighborhood(id);
                else render();
            });
        });
    }

    function insideAndBeyond(node) {
        const members = data.nodes
            .filter((item) => item.hub === node.id && item.id !== node.id)
            .sort((a, b) => a.title.localeCompare(b.title))
            .map((item) => ({ node: item, kinds: [], labels: [] }));
        const beyond = connectionsOf(node.id).filter((item) => item.node.hub !== node.id);
        return [
            { title: "Inside", items: members },
            { title: "Beyond", items: beyond },
        ];
    }

    function groupConnections(items) {
        const used = new Set();
        function take(title, pred) {
            const group = [];
            items.forEach((item) => {
                if (used.has(item.node.id) || !pred(item)) return;
                used.add(item.node.id);
                group.push(item);
            });
            return { title: title, items: group };
        }
        return [
            take("Correspondences", (item) => item.kinds.includes("correspondence")),
            take("Themes and tags", (item) => item.kinds.includes("theme") || item.kinds.includes("tag") || item.kinds.includes("series")),
            take("Links", () => true),
        ];
    }

    function openNeighborhood(id) {
        pin = { type: "near", id: id };
        selectedId = id;
        sectionFilter = "";
        domainFilter = "";
        history.replaceState(null, "", "#" + encodeURIComponent(id));
        render();
    }

    function pick(node) {
        selectedId = node.id;
        const view = current();
        if (view.mode === "overview" && node.overview && node.kind !== "page") {
            pin = { type: "hub", id: node.id };
            sectionFilter = "";
            domainFilter = "";
        } else if (view.mode === "overview" && node.section === "pages") {
            openNeighborhood(node.id);
            return;
        }
        render();
    }

    function showResults() {
        const q = queryEl.value.trim().toLowerCase();
        if (q.length < 2) {
            resultsEl.hidden = true;
            resultsEl.innerHTML = "";
            return;
        }
        const matches = [];
        data.nodes.forEach((node) => {
            if (!node._hay) {
                node._hay = (node.title + " " + (node.tags || []).join(" ") + " " + node.section + " " + node.domain + " " + (node.summary || "")).toLowerCase();
            }
            if (!node._hay.includes(q)) return;
            const title = node.title.toLowerCase();
            const score = title === q ? -1 : title.startsWith(q) ? 0 : title.includes(q) ? 1 : 2;
            matches.push({ node: node, score: score });
        });
        matches.sort((a, b) => a.score - b.score || (degree.get(b.node.id) || 0) - (degree.get(a.node.id) || 0) || a.node.title.length - b.node.title.length);
        resultsEl.innerHTML = matches.slice(0, 8).map((item) => {
            return '<li><button type="button" data-id="' + esc(item.node.id) + '">' + esc(item.node.title)
                + '<span class="result-meta">' + esc(sectionTitle(item.node.section)) + "</span></button></li>";
        }).join("");
        resultsEl.hidden = matches.length === 0;
        resultsEl.querySelectorAll("button").forEach((button) => {
            button.addEventListener("click", () => {
                resultsEl.hidden = true;
                queryEl.value = byId.get(button.getAttribute("data-id")).title;
                openNeighborhood(button.getAttribute("data-id"));
            });
        });
    }

    function radius(node, mode) {
        if (mode === "overview") {
            const count = Math.max(hubCount.get(node.id) || 1, (degree.get(node.id) || 0) / 4);
            return Math.min(13, 4.2 + Math.sqrt(count) * 0.55);
        }
        if (node.kind === "page") return 4.6;
        return 7;
    }

    function ensureLayout(view) {
        const key = view.mode + "|" + view.nodes.map((node) => node.id).sort().join("|");
        if (key === layoutKey) return;
        layoutKey = key;
        if (simulation) simulation.stop();
        placed = view.nodes.map((node) => Object.assign({}, node, { r: radius(node, view.mode) }));
        const index = new Map(placed.map((node) => [node.id, node]));
        placedLinks = view.links.map((edge) => ({
            source: index.get(edge.source),
            target: index.get(edge.target),
            weight: edge.weight || 1,
            kinds: edge.kinds || [],
        })).filter((edge) => edge.source && edge.target);
        userScale = 1;
        if (view.mode === "overview") {
            ring(placed);
            sizeToGraph();
            return;
        }
        if (placed.length > 80) {
            cluster(placed);
            sizeToGraph();
            return;
        }
        const width = layoutSpan();
        placed.forEach((node, i) => {
            const turn = i * 2.399963;
            node.seedY = 80 + i * 36;
            node.x = width / 2 + Math.cos(turn) * (40 + (i % 9) * 22);
            node.y = node.seedY + Math.sin(turn) * 48;
        });
        let ticks = 0;
        simulation = d3.forceSimulation(placed)
            .force("link", d3.forceLink(placedLinks).distance(84).strength(0.28))
            .force("charge", d3.forceManyBody().strength(-220))
            .force("x", d3.forceX(width / 2).strength(0.02))
            .force("y", d3.forceY((node) => node.seedY).strength(0.012))
            .force("collide", d3.forceCollide().radius((node) => node.r + 16))
            .alpha(1)
            .alphaDecay(0.035)
            .on("tick", () => {
                ticks += 1;
                if (ticks % 6 === 0) sizeToGraph();
                else draw();
            })
            .on("end", () => sizeToGraph());
    }

    function stageWidth() {
        return Math.max(320, document.documentElement.clientWidth);
    }

    function layoutSpan() {
        const panel = window.innerWidth >= 900 ? 340 : 16;
        return Math.max(280, stageWidth() - panel);
    }

    function ring(list) {
        const w = layoutSpan();
        const narrow = w < 640;
        const n = Math.max(list.length, 1);
        const rx = narrow ? Math.max(78, w * 0.30) : Math.max(220, Math.min(w * 0.34, 480));
        const ry = Math.max(rx * (narrow ? 2.1 : 1.25), n * (narrow ? 20 : 28));
        const cx = w / 2;
        const cy = ry + (narrow ? 36 : 72);
        const order = list.slice().sort((a, b) => {
            const rank = (node) => node.kind === "domain" ? 0 : node.kind === "theme" ? 1 : 2;
            return rank(a) - rank(b) || a.title.localeCompare(b.title);
        });
        order.forEach((node, i) => {
            const angle = (i / order.length) * Math.PI * 2 - Math.PI / 2;
            node.x = cx + Math.cos(angle) * rx;
            node.y = cy + Math.sin(angle) * ry;
            if (narrow) {
                node.lx = node.x;
                node.ly = node.y + node.r + 12;
                node.anchor = "center";
            } else {
                node.lx = cx + Math.cos(angle) * (rx + 18);
                node.ly = cy + Math.sin(angle) * (ry + 16);
                node.anchor = Math.cos(angle) > 0.25 ? "left" : Math.cos(angle) < -0.25 ? "right" : "center";
            }
        });
    }

    function cluster(list) {
        const w = layoutSpan();
        const groups = d3.group(list, (node) => node.domain || node.section || "");
        let y = 100;
        groups.forEach((members) => {
            const reach = 24 + Math.sqrt(members.length) * 34;
            const cx = w / 2;
            members.forEach((node, j) => {
                const turn = j * 2.399963;
                const dist = 18 + Math.sqrt(j) * 30;
                node.x = cx + Math.cos(turn) * dist;
                node.y = y + reach + Math.sin(turn) * dist * 1.45;
            });
            y += reach * 2.6 + 120;
        });
    }

    function nodeBox(node) {
        let left = node.x - node.r - 8;
        let right = node.x + node.r + 8;
        let top = node.y - node.r - 8;
        let bottom = node.y + node.r + 18;
        const label = clipTitle(displayTitle(node));
        const textWidth = Math.min(label.length, window.innerWidth < 640 ? 16 : 28) * 6.6;
        const lx = node.lx != null ? node.lx : node.x;
        const ly = node.ly != null ? node.ly : node.y + node.r + 14;
        if (node.anchor === "right") {
            left = Math.min(left, lx - textWidth);
            right = Math.max(right, lx);
        } else if (node.anchor === "left") {
            left = Math.min(left, lx);
            right = Math.max(right, lx + textWidth);
        } else {
            left = Math.min(left, lx - textWidth / 2);
            right = Math.max(right, lx + textWidth / 2);
        }
        top = Math.min(top, ly - 14);
        bottom = Math.max(bottom, ly + 6);
        return { left: left, right: right, top: top, bottom: bottom };
    }

    function containHorizontally() {
        const gutter = window.innerWidth >= 900 ? 360 : 36;
        const limit = Math.max(140, stageWidth() - gutter);
        let minX = Infinity, maxX = -Infinity;
        placed.forEach((node) => {
            minX = Math.min(minX, node.x);
            maxX = Math.max(maxX, node.x);
        });
        const span = maxX - minX;
        if (!isFinite(span) || span <= limit) return;
        const scale = limit / span;
        const mid = (minX + maxX) / 2;
        const target = layoutSpan() / 2;
        placed.forEach((node) => {
            node.x = target + (node.x - mid) * scale;
            if (node.lx != null) node.lx = target + (node.lx - mid) * scale;
        });
    }

    function sizeToGraph() {
        containHorizontally();
        if (!placed.length) {
            setCanvas(stageWidth(), 240);
            transform = d3.zoomIdentity;
            draw();
            return;
        }
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        placed.forEach((node) => {
            const box = nodeBox(node);
            minX = Math.min(minX, box.left);
            maxX = Math.max(maxX, box.right);
            minY = Math.min(minY, box.top);
            maxY = Math.max(maxY, box.bottom);
        });
        const padX = 36;
        const padY = 48;
        const worldW = Math.max(1, maxX - minX);
        const worldH = Math.max(1, maxY - minY);
        const cssW = stageWidth();
        const cssH = worldH * userScale + padY * 2;
        setCanvas(cssW, cssH);
        const ox = (cssW - worldW * userScale) / 2 - minX * userScale;
        const oy = padY - minY * userScale;
        transform = d3.zoomIdentity.translate(ox, oy).scale(userScale);
        draw();
    }

    function setCanvas(cssW, cssH) {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const width = Math.max(1, Math.round(cssW));
        const height = Math.max(1, Math.round(cssH));
        canvas.style.width = width + "px";
        canvas.style.height = height + "px";
        const bw = Math.round(width * dpr);
        const bh = Math.round(height * dpr);
        if (canvas.width !== bw || canvas.height !== bh) {
            canvas.width = bw;
            canvas.height = bh;
        }
    }

    function hit(event) {
        const rect = canvas.getBoundingClientRect();
        const x = (event.clientX - rect.left - transform.x) / transform.k;
        const y = (event.clientY - rect.top - transform.y) / transform.k;
        let best = null;
        let bestD = 20;
        placed.forEach((node) => {
            const dist = Math.hypot((node.x || 0) - x, (node.y || 0) - y);
            if (dist <= node.r + 8 && dist < bestD) {
                best = node;
                bestD = dist;
            }
        });
        return best;
    }

    function displayTitle(node) {
        let title = node.kind === "section" ? sectionTitle(node.section) : node.title;
        if (node.kind === "section" && data.nodes.some((other) => other.overview && other.kind === "domain" && other.title.toLowerCase() === title.toLowerCase())) {
            title = title + " pages";
        }
        return title;
    }

    function clipTitle(title) {
        const limit = window.innerWidth < 640 ? 16 : 28;
        return title.length > limit ? title.slice(0, limit - 1) + "…" : title;
    }

    function labelsThatFit(list) {
        const boxes = [];
        const show = new Set();
        const ordered = list.slice().sort((a, b) => (hubCount.get(b.id) || 0) - (hubCount.get(a.id) || 0));
        ctx.save();
        ctx.font = 'italic 12px Palatino, "Palatino Linotype", Georgia, serif';
        ordered.forEach((node) => {
            const label = clipTitle(displayTitle(node));
            const width = ctx.measureText(label).width;
            const x = node.lx || node.x;
            const y = node.ly || node.y;
            const left = node.anchor === "left" ? x : node.anchor === "right" ? x - width : x - width / 2;
            const box = { left: left, right: left + width, top: y - 12, bottom: y + 3 };
            const hit = boxes.some((other) => !(box.right < other.left || box.left > other.right || box.bottom < other.top || box.top > other.bottom));
            if (hit) return;
            boxes.push(box);
            show.add(node.id);
        });
        ctx.restore();
        return show;
    }

    function draw() {
        if (!placed.length && data) {
            ctx.setTransform(1, 0, 0, 1, 0, 0);
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            return;
        }
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const cssW = canvas.clientWidth || stageWidth();
        const cssH = canvas.clientHeight || 240;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, cssW, cssH);
        ctx.save();
        ctx.translate(transform.x, transform.y);
        ctx.scale(transform.k, transform.k);
        const ink = cssVar("--ink-faint") || "#999";
        const accent = cssVar("--accent") || "#9c4b2f";
        const paper = cssVar("--paper") || "#fffff8";
        const labelInk = cssVar("--ink-muted") || "#666";
        const overview = layoutKey.startsWith("overview");
        const focus = hoverId || (!overview && pin && pin.type === "near" ? selectedId : "");
        const near = new Set();
        if (focus) {
            near.add(focus);
            placedLinks.forEach((edge) => {
                if (edge.source.id === focus) near.add(edge.target.id);
                if (edge.target.id === focus) near.add(edge.source.id);
            });
        }
        const labeled = overview ? labelsThatFit(placed) : null;
        placedLinks.forEach((edge) => {
            const hot = focus && (edge.source.id === focus || edge.target.id === focus);
            const correspondence = (edge.kinds || []).includes("correspondence");
            ctx.globalAlpha = focus && !hot ? 0.05 : (hot ? 0.9 : 0.35);
            ctx.strokeStyle = hot || correspondence ? accent : ink;
            ctx.lineWidth = edge.weight ? Math.min(3.5, 0.6 + Math.sqrt(edge.weight) * 0.45) : (correspondence ? 1.4 : 0.8);
            ctx.beginPath();
            ctx.moveTo(edge.source.x, edge.source.y);
            ctx.lineTo(edge.target.x, edge.target.y);
            ctx.stroke();
        });
        placed.forEach((node) => {
            ctx.globalAlpha = focus && !near.has(node.id) ? 0.18 : 1;
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
            ctx.fillStyle = colorFor(node);
            ctx.fill();
            ctx.lineWidth = node.id === selectedId ? 2.4 : 1.2;
            ctx.strokeStyle = node.id === selectedId ? accent : paper;
            ctx.stroke();
        });
        ctx.font = 'italic 12px Palatino, "Palatino Linotype", Georgia, serif';
        ctx.lineJoin = "round";
        placed.forEach((node) => {
            const show = overview
                ? (labeled.has(node.id) || node.id === hoverId || node.id === selectedId)
                : (node.id === selectedId || node.id === hoverId || node.kind !== "page" || placed.length <= 24);
            if (!show) return;
            if (!overview && focus && !near.has(node.id) && node.id !== hoverId) return;
            const label = clipTitle(displayTitle(node));
            const x = overview && node.lx ? node.lx : node.x;
            const y = overview && node.ly ? node.ly : node.y + node.r + 13;
            ctx.globalAlpha = 1;
            ctx.textAlign = overview && node.anchor ? node.anchor : "center";
            ctx.strokeStyle = paper;
            ctx.lineWidth = 3;
            ctx.strokeText(label, x, y);
            ctx.fillStyle = labelInk;
            ctx.fillText(label, x, y);
        });
        ctx.restore();
    }
})();
