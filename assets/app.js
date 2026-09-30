(function () {
  const state = {
    library: null,
    step: 1,
    answers: defaultAnswers(),
    result: null,
    applicable: [],
    tab: "controls",
    view: "home",
    libraryFilter: { q: "", framework: "all" },
    openId: null,
  };

  function defaultAnswers() {
    return {
      system_name: "",
      owner: "",
      business_unit: "",
      auditor: "",
      engagement_id: "",
      engagement_date: new Date().toISOString().slice(0, 10),
      intended_purpose: "",
      role: "deployer",
      markets: [],
      architecture: [],
      iso42001_aims: true,
      third_party_model_or_api: false,
      personal_data: false,
      automated_decision: false,
      interacts_with_natural_persons: false,
      synthetic_content: false,
      deepfake: false,
      profiles_natural_persons: false,
      annex_i_safety_component: false,
      annex_iii_1: false,
      annex_iii_2: false,
      annex_iii_3: false,
      annex_iii_4: false,
      annex_iii_5: false,
      annex_iii_6: false,
      annex_iii_7: false,
      annex_iii_8: false,
      art63_narrow_procedural: false,
      art63_improves_human: false,
      art63_detects_patterns: false,
      art63_preparatory: false,
      art5_practices: [],
      gpai_model_provider: false,
      gpai_systemic_flops: false,
      us_supervised_bank: false,
      material_business_decision_model: false,
      fria_role: false,
    };
  }

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  function route() {
    const hash = (location.hash || "#home").replace("#", "");
    const view = hash.split("/")[0] || "home";
    state.view = view;
    $$("nav.primary a").forEach((a) => {
      a.classList.toggle("active", a.getAttribute("href") === `#${view}`);
    });
    $$("[data-view]").forEach((el) => {
      el.classList.toggle("hidden", el.getAttribute("data-view") !== view);
    });
    if (view === "results") {
      if (state.result) renderResults();
      else renderResultsEmpty();
    }
    if (view === "library") renderLibrary();
    if (view === "sources") renderSources();
    if (view === "scope") renderWizard();
  }

  function esc(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

    function collectForm() {
    const root = $("[data-view='scope']");
    if (!root) return;
    $$("input[type='text'], input[type='date'], textarea, select", root).forEach((el) => {
      if (el.name) state.answers[el.name] = el.value;
    });
    $$("input[type='checkbox'][data-group]", root).forEach((el) => {
      const group = el.getAttribute("data-group");
      const vals = $$("input[data-group='" + group + "']:checked", root).map((c) => c.value);
      state.answers[group] = vals;
    });
    $$("input[type='checkbox'][name]", root).forEach((el) => {
      if (el.dataset.group) return;
      state.answers[el.name] = el.checked;
    });
    const named = $("#sys-name");
    if (named && named.value.trim()) state.answers.system_name = named.value.trim();
    if ((state.answers.markets || []).includes("us_banking")) {
      state.answers.us_supervised_bank = true;
    }
    if ((state.answers.markets || []).includes("eu")) {
      state.answers.eu_in_scope = true;
    }
  }

  function resetEngagement() {
    sessionStorage.removeItem("abf-workpaper");
    state.answers = defaultAnswers();
    state.result = null;
    state.applicable = [];
    state.step = 1;
    state.tab = "controls";
    const root = $("[data-view='scope']");
    $$("input[type='text'], textarea", root).forEach((el) => {
      el.value = "";
    });
    const dateInput = $("input[name='engagement_date']");
    if (dateInput) dateInput.value = state.answers.engagement_date;
    $$("input[type='checkbox']", root).forEach((el) => {
      if (el.name === "iso42001_aims") el.checked = true;
      else el.checked = false;
    });
    const role = $("select[name='role']");
    if (role) role.value = "deployer";
    renderWizard();
    location.hash = "scope";
  }

  function generate() {
    collectForm();
    if (!state.answers.system_name.trim()) {
      state.answers.system_name = "Unnamed AI system";
    }
    state.result = ABFEngine.classify(state.answers);
    state.applicable = state.library.obligations.filter((o) =>
      ABFEngine.obligationApplies(o, state.result)
    );
    sessionStorage.setItem(
      "abf-workpaper",
      JSON.stringify({
        answers: state.answers,
        result: state.result,
        generated_at: new Date().toISOString(),
      })
    );
    location.hash = "results";
    renderResults();
  }

  function renderWizard() {
    const root = $("[data-view='scope']");
    $$(".wizard-pane", root).forEach((p) => {
      p.classList.toggle("hidden", Number(p.dataset.step) !== state.step);
    });
    $$(".steps li", root).forEach((li) => {
      const n = Number(li.dataset.step);
      li.classList.toggle("active", n === state.step);
      li.classList.toggle("done", n < state.step);
    });
  }

  function renderResultsEmpty() {
    const mount = $("#results-mount");
    if (!mount) return;
    mount.innerHTML = `
      <div class="notice info">
        No workpaper in this session. Start a scoping engagement to extract applicable official requirements.
      </div>
      <a class="btn" href="#scope">Open scoping wizard</a>`;
  }

  function countByFramework(items) {
    const m = {};
    items.forEach((o) => {
      m[o.framework] = (m[o.framework] || 0) + 1;
    });
    return m;
  }

  function renderResults() {
    const mount = $("#results-mount");
    if (!mount || !state.result) return;
    const a = state.answers;
    const r = state.result;
    const counts = countByFramework(state.applicable);
    const findings = r.findings
      .map(
        (f) => `
      <article class="finding">
        <span class="status ${esc(f.tone || "info")}">${esc(f.status)}</span>
        <h3>${esc(f.topic)}</h3>
        <p>${esc(f.summary)}</p>
        <p class="cite">${esc(f.rule)}</p>
        <p><a href="${esc(f.source_url)}" target="_blank" rel="noopener">${esc(f.citation)}</a></p>
      </article>`
      )
      .join("");

    mount.innerHTML = `
      <p class="kicker">Engagement workpaper</p>
      <h2>${esc(a.system_name)}</h2>
      <p class="help">${esc(a.business_unit || "—")} · Owner ${esc(a.owner || "—")} · Auditor ${esc(a.auditor || "—")} · ${esc(a.engagement_id || a.engagement_date)}</p>
      <div class="notice">
        ${esc(state.library.disclaimer)}
      </div>
      <div class="stats">
        <div class="stat"><b>${state.applicable.length}</b><span>Applicable sourced items</span></div>
        <div class="stat"><b>${state.applicable.filter((x) => x.procedure).length}</b><span>Walkthrough procedures</span></div>
        <div class="stat"><b>${r.eu_high_risk ? "Yes*" : "No*"}</b><span>EU high-risk (indicative)</span></div>
        <div class="stat"><b>${r.sr117 ? "Yes*" : "No*"}</b><span>SR 11-7 (indicative)</span></div>
      </div>
      <p class="help">*Indicative screening with cited rules — not a legal opinion or conformity assessment.</p>
      <h3 class="serif">Screening conclusions</h3>
      ${findings || "<p>No additional findings. NIST AI RMF outcomes remain available as a voluntary backbone.</p>"}
      <p class="help">Coverage in this workpaper:
        ${Object.entries(counts)
          .map(([k, v]) => `<span class="chip">${esc(k)} · ${v}</span>`)
          .join(" ")}
      </p>
      <div class="btn-row no-print">
        <button class="btn" data-export="json">Export JSON</button>
        <button class="btn btn-secondary" data-export="csv">Export CSV</button>
        <button class="btn btn-secondary" data-export="md">Export walkthrough Markdown</button>
        <button class="btn btn-secondary" onclick="window.print()">Print / PDF</button>
        <button class="btn btn-secondary" type="button" id="reset-from-results">Start a new engagement</button>
      </div>
      <div class="tabs no-print">
        <button data-tab="controls" class="${state.tab === "controls" ? "active" : ""}">Controls &amp; requirements</button>
        <button data-tab="walk" class="${state.tab === "walk" ? "active" : ""}">Walkthroughs</button>
        <button data-tab="evidence" class="${state.tab === "evidence" ? "active" : ""}">Evidence register</button>
        <button data-tab="matrix" class="${state.tab === "matrix" ? "active" : ""}">Alignment</button>
      </div>
      <div id="tab-mount"></div>
    `;
    renderTab();
    $$("[data-tab]", mount).forEach((btn) => {
      btn.addEventListener("click", () => {
        state.tab = btn.dataset.tab;
        $$("[data-tab]", mount).forEach((b) => b.classList.toggle("active", b === btn));
        renderTab();
      });
    });
    $$("[data-export]", mount).forEach((btn) => {
      btn.addEventListener("click", () => exportWorkpaper(btn.dataset.export));
    });
    $("#reset-from-results")?.addEventListener("click", resetEngagement);
  }

  function renderTab() {
    const mount = $("#tab-mount");
    if (!mount) return;
    const withProc = state.applicable.filter((o) => o.procedure);
    const without = state.applicable.filter((o) => !o.procedure);
    if (state.tab === "controls") {
      mount.innerHTML =
        `<p class="help">${withProc.length} items have ABF walkthroughs (listed first). Remaining rows are official text for the audit file.</p>` +
        controlTable(withProc.concat(without));
      bindRows(mount);
    } else if (state.tab === "walk") {
      const withProc = state.applicable.filter((o) => o.procedure);
      const byRole = {};
      withProc.forEach((o) => {
        const role = o.procedure.target_roles[0] || "Engagement team";
        byRole[role] = byRole[role] || [];
        byRole[role].push(o);
      });
      mount.innerHTML =
        `<p class="help">${withProc.length} ABF-authored procedures, grouped by primary interview role. Expand a card to run the walkthrough. These are not the source standard.</p>` +
        Object.entries(byRole)
          .map(([role, items]) => `<h3>${esc(role)}</h3>${items.map((o, i) => walkCard(o, i === 0)).join("")}`)
          .join("");
    } else if (state.tab === "evidence") {
      const rows = [];
      state.applicable.forEach((o) => {
        (o.procedure?.evidence || []).forEach((e) => {
          rows.push(`<tr><td>${esc(o.code)}</td><td>${esc(o.framework)}</td><td>${esc(e)}</td><td>${esc((o.procedure.target_roles || []).join(", "))}</td></tr>`);
        });
      });
      mount.innerHTML = `
        <p class="help">Evidence items are ABF workpaper suggestions derived from the cited requirement. They are not themselves regulatory mandates.</p>
        <table>
          <thead><tr><th>ID</th><th>Framework</th><th>Evidence to request</th><th>Likely holder</th></tr></thead>
          <tbody>${rows.join("") || "<tr><td colspan=4>No procedure-linked evidence in this scope. Use official text in the controls tab to derive requests.</td></tr>"}</tbody>
        </table>`;
    } else {
      mount.innerHTML = `
        <p class="help">Crosswalks are ABF mappings of related public identifiers. They are not official ISO or Commission transpositions.</p>
        <table>
          <thead><tr><th>Official ID</th><th>Title</th><th>Related identifiers</th></tr></thead>
          <tbody>
            ${state.applicable
              .map(
                (o) =>
                  `<tr><td>${esc(o.code)}</td><td>${esc(o.title)}</td><td>${(o.crosswalk || [])
                    .map((c) => esc(c))
                    .join(", ") || "—"}</td></tr>`
              )
              .join("")}
          </tbody>
        </table>`;
    }
  }

  function controlTable(items) {
    const body = items
      .map(
        (o) => `
      <tr data-open="${esc(o.id)}">
        <td>${esc(o.code)}</td>
        <td>${esc(o.framework)}</td>
        <td>${esc(o.title)}</td>
        <td>${o.procedure ? "Yes" : "—"}</td>
      </tr>
      <tr class="detail-row"><td colspan="4">
        <div class="detail" id="d-${esc(o.id)}">
          <p class="cite">${esc(o.citation)}</p>
          <p><a href="${esc(o.source_url)}" target="_blank" rel="noopener">Open source</a> · ${esc(o.kind)}</p>
          <h4>Official / public text</h4>
          <p>${esc(o.official_text)}</p>
          ${
            o.procedure
              ? `<h4>ABF walkthrough procedure</h4>
                 <p><strong>${esc(o.procedure.title)}</strong> — ${esc(o.procedure.authored_by)}</p>
                 <p><em>Ask:</em> ${esc(o.procedure.inquiry)}</p>
                 <p><em>Observe:</em> ${esc(o.procedure.observe)}</p>`
              : ""
          }
        </div>
      </td></tr>`
      )
      .join("");
    return `
      <table>
        <thead><tr><th>ID</th><th>Source</th><th>Requirement / outcome</th><th>Procedure</th></tr></thead>
        <tbody>${body}</tbody>
      </table>`;
  }

    function walkCard(o, expanded) {
    const p = o.procedure;
    return `
      <article class="walk">
        <header>
          <p class="cite">${esc(o.citation)}</p>
          <h3>${esc(p.title)}</h3>
          <p>Roles: ${esc(p.target_roles.join(" · "))}</p>
        </header>
        <div class="body">
          <details${expanded ? " open" : ""}>
            <summary>${expanded ? "Walkthrough" : "Open walkthrough"}</summary>
            <h4>1. Architectural inquiry</h4>
            <blockquote>${esc(p.inquiry)}</blockquote>
            <h4>2. What to observe live</h4>
            <p>${esc(p.observe)}</p>
            <h4>3. Evidence checklist</h4>
            <ul>${p.evidence.map((e) => `<li>${esc(e)}</li>`).join("")}</ul>
            <h4>4. Test procedure</h4>
            <p>${esc(p.test)}</p>
            <p class="cite">${esc(p.authored_by)}</p>
          </details>
        </div>
      </article>`;
  }

  function bindRows(root) {
    $$("tr[data-open]", root).forEach((tr) => {
      tr.addEventListener("click", () => {
        const id = tr.getAttribute("data-open");
        const det = document.getElementById("d-" + id);
        if (det) det.classList.toggle("open");
      });
    });
  }

    function renderLibrary() {
    const mount = $("#library-mount");
    if (!mount || !state.library) return;
    const q = state.libraryFilter.q.toLowerCase();
    const fw = state.libraryFilter.framework;
    const items = state.library.obligations.filter((o) => {
      const matchFw = fw === "all" || o.framework === fw;
      const blob = (o.id + o.title + o.official_text + o.citation).toLowerCase();
      return matchFw && (!q || blob.includes(q));
    });
    const frameworks = [...new Set(state.library.obligations.map((o) => o.framework))];
    if (!$("#lib-q")) {
      mount.innerHTML = `
      <p class="kicker">Sourced library</p>
      <h2>Official requirements, titles, and threat categories</h2>
      <p class="help">${state.library.obligations.length} items. NIST subcategory outcomes are reproduced from NIST AI 100-1. EU articles are auditor paraphrases of public law. ISO/IEC 42001 entries are titles only.</p>
      <div class="library-toolbar">
        <label>Search<input id="lib-q" type="text" value="${esc(state.libraryFilter.q)}" placeholder="GOVERN 1.1, Article 14, A.8.4…"></label>
        <label>Framework
          <select id="lib-fw">
            <option value="all">All sources</option>
            ${frameworks
              .map((f) => `<option ${f === fw ? "selected" : ""} value="${esc(f)}">${esc(f)}</option>`)
              .join("")}
          </select>
        </label>
      </div>
      <p class="help" id="lib-count"></p>
      <div id="lib-table"></div>
    `;
      $("#lib-q").addEventListener("input", (e) => {
        state.libraryFilter.q = e.target.value;
        paintLibraryTable(itemsForLibrary());
      });
      $("#lib-fw").addEventListener("change", (e) => {
        state.libraryFilter.framework = e.target.value;
        paintLibraryTable(itemsForLibrary());
      });
    }
    paintLibraryTable(items);
  }

  function itemsForLibrary() {
    const q = state.libraryFilter.q.toLowerCase();
    const fw = state.libraryFilter.framework;
    return state.library.obligations.filter((o) => {
      const matchFw = fw === "all" || o.framework === fw;
      const blob = (o.id + o.title + o.official_text + o.citation).toLowerCase();
      return matchFw && (!q || blob.includes(q));
    });
  }

  function paintLibraryTable(items) {
    const count = $("#lib-count");
    if (count) count.textContent = items.length + " shown.";
    const table = $("#lib-table");
    if (!table) return;
    table.innerHTML = controlTable(items);
    bindRows(table);
  }

  function renderSources() {
    const mount = $("#sources-mount");
    if (!mount || !state.library) return;
    mount.innerHTML = `
      <p class="kicker">Bibliography</p>
      <h2>Authoritative sources used in this build</h2>
      <p class="help">Every library item stores a citation and URL. ABF does not generate unnamed “ABF-CTL” controls.</p>
      <ul class="source-list">
        ${state.library.sources
          .map(
            (s) => `
          <li>
            <h3>${esc(s.name)}</h3>
            <p class="cite">${esc(s.id)}${s.document ? " · " + esc(s.document) : ""} · ${esc(s.date || "")}</p>
            <p><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.url)}</a></p>
            <p>${esc(s.license_note || "")}</p>
          </li>`
          )
          .join("")}
      </ul>
      <h3>How classification works</h3>
      <ul>
        <li>EU high-risk follows Article 6: Annex I product-safety path or Annex III use cases. Personal data or “agentic” architecture is not a high-risk trigger.</li>
        <li>If Annex III applies and the system profiles natural persons, the Article 6(3) exception is unavailable.</li>
        <li>If Annex III applies and a 6(3) condition is indicated without profiling, ABF reports a possible exception — the provider must document it.</li>
        <li>Article 5 hits are labeled indicative and require counsel review against the authentic list and exceptions.</li>
        <li>SR 11-7 is included only when the auditee is a US supervised banking organization and the system is used as a material decision model.</li>
        <li>ISO/IEC 42001 rows are public control titles. Obtain the standard for authentic “shall” text.</li>
      </ul>
    `;
  }

  function download(filename, text, mime) {
    const blob = new Blob([text], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  function csvEscape(v) {
    const s = String(v ?? "");
    if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
    return s;
  }

  function exportWorkpaper(kind) {
    const stamp = (state.answers.system_name || "system").replace(/\s+/g, "_").slice(0, 40);
    if (kind === "json") {
      download(
        `abf_workpaper_${stamp}.json`,
        JSON.stringify(
          {
            disclaimer: state.library.disclaimer,
            answers: state.answers,
            screening: state.result,
            applicable: state.applicable,
          },
          null,
          2
        ),
        "application/json"
      );
    } else if (kind === "csv") {
      const header = [
        "id",
        "framework",
        "citation",
        "source_url",
        "title",
        "official_text",
        "procedure_title",
        "evidence",
      ];
      const lines = [header.join(",")];
      state.applicable.forEach((o) => {
        lines.push(
          [
            o.id,
            o.framework,
            o.citation,
            o.source_url,
            o.title,
            o.official_text,
            o.procedure?.title || "",
            (o.procedure?.evidence || []).join(" | "),
          ]
            .map(csvEscape)
            .join(",")
        );
      });
      download(`abf_controls_${stamp}.csv`, lines.join("\n"), "text/csv");
    } else if (kind === "md") {
      const parts = [
        `# ABF walkthrough packet — ${state.answers.system_name}`,
        "",
        `> ${state.library.disclaimer}`,
        "",
        `Auditor: ${state.answers.auditor || "—"} · Date: ${state.answers.engagement_date}`,
        "",
      ];
      state.applicable
        .filter((o) => o.procedure)
        .forEach((o) => {
          const p = o.procedure;
          parts.push(`## ${o.code}: ${p.title}`);
          parts.push(`**Official source:** ${o.citation}`);
          parts.push(`**Roles:** ${p.target_roles.join(", ")}`);
          parts.push("");
          parts.push("### Inquiry");
          parts.push(`> ${p.inquiry}`);
          parts.push("");
          parts.push("### Observe");
          parts.push(p.observe);
          parts.push("");
          parts.push("### Evidence");
          p.evidence.forEach((e) => parts.push(`- [ ] ${e}`));
          parts.push("");
          parts.push("### Test");
          parts.push(p.test);
          parts.push("");
          parts.push(`_${p.authored_by}_`);
          parts.push("");
        });
      download(`abf_walkthrough_${stamp}.md`, parts.join("\n"), "text/markdown");
    }
  }

  function bindScope() {
    const root = $("[data-view='scope']");
    $$(".steps li", root).forEach((li) => {
      li.addEventListener("click", () => {
        collectForm();
        state.step = Number(li.dataset.step);
        renderWizard();
      });
    });
    $$("[data-next]", root).forEach((btn) => {
      btn.addEventListener("click", () => {
        collectForm();
        state.step = Math.min(6, state.step + 1);
        renderWizard();
      });
    });
    $$("[data-back]", root).forEach((btn) => {
      btn.addEventListener("click", () => {
        collectForm();
        state.step = Math.max(1, state.step - 1);
        renderWizard();
      });
    });
    $("#generate-btn")?.addEventListener("click", generate);
    $("#reset-engagement")?.addEventListener("click", resetEngagement);
  }

  async function boot() {
    const res = await fetch("data/library.json");
    if (!res.ok) {
      document.body.insertAdjacentHTML(
        "afterbegin",
        `<div class="notice alert">Could not load data/library.json (${res.status}). Serve the site from the repository root.</div>`
      );
      return;
    }
    state.library = await res.json();
    const saved = sessionStorage.getItem("abf-workpaper");
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        state.answers = { ...defaultAnswers(), ...parsed.answers };
        state.result = parsed.result;
        state.applicable = state.library.obligations.filter((o) =>
          ABFEngine.obligationApplies(o, state.result)
        );
      } catch (err) {
        console.warn("ABF: could not restore session", err);
      }
    }
    bindScope();
    const dateInput = document.querySelector("input[name='engagement_date']");
    if (dateInput && !dateInput.value) dateInput.value = state.answers.engagement_date;
    window.addEventListener("hashchange", route);
    route();
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
