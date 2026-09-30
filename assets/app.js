(function () {
  const TEST_STATUSES = [
    { value: "not_started", label: "Not started" },
    { value: "requested", label: "Evidence requested" },
    { value: "received", label: "Evidence received" },
    { value: "tested", label: "Tested" },
    { value: "exception", label: "Exception / finding" },
    { value: "na", label: "N/A this engagement" },
  ];
  const EVIDENCE_STATUSES = [
    { value: "planned", label: "Planned" },
    { value: "requested", label: "Requested" },
    { value: "received", label: "Received" },
    { value: "exception", label: "Exception" },
  ];
  const SAMPLE = {
    system_name: "Retail credit decisioning assistant",
    owner: "Chief Credit Officer",
    business_unit: "Retail banking",
    auditor: "Internal Audit — Model Risk",
    engagement_id: "IA-2026-014",
    engagement_date: "2026-09-30",
    intended_purpose:
      "Assist underwriters in evaluating creditworthiness of natural persons for unsecured consumer loans, with retrieval of policy documents.",
    role: "deployer",
    markets: ["eu", "us_banking"],
    architecture: ["rag", "llm_chat"],
    iso42001_aims: true,
    third_party_model_or_api: true,
    personal_data: true,
    automated_decision: false,
    interacts_with_natural_persons: false,
    synthetic_content: false,
    profiles_natural_persons: true,
    annex_iii_5: true,
    material_business_decision_model: true,
    fria_role: true,
  };

  const state = {
    library: null,
    step: 1,
    answers: defaultAnswers(),
    result: null,
    applicable: [],
    tab: "controls",
    view: "home",
    libraryFilter: { q: "", framework: "all" },
    openIds: new Set(),
    fwFilter: "all",
    fieldworkPack: true,
    testing: {},
    notes: {},
    evidenceStatus: {},
    toastTimer: null,
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

  function debounce(fn, ms) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), ms);
    };
  }

  function toast(msg) {
    const el = $("#toast");
    if (!el) return;
    el.textContent = msg;
    el.classList.add("show");
    clearTimeout(state.toastTimer);
    state.toastTimer = setTimeout(() => el.classList.remove("show"), 2400);
  }

  function updateNavBadge() {
    const b = $("#wp-badge");
    if (!b) return;
    const n = state.applicable.length;
    b.classList.toggle("hidden", !state.result);
    b.textContent = n ? String(n) : "";
  }

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
    if (view === "scope") {
      applyAnswersToForm();
      renderWizard();
    }
    updateNavBadge();
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
    if (named) state.answers.system_name = named.value.trim();
    if ((state.answers.markets || []).includes("us_banking")) {
      state.answers.us_supervised_bank = true;
    } else {
      state.answers.us_supervised_bank = false;
    }
    state.answers.eu_in_scope = (state.answers.markets || []).includes("eu");
  }

  function applyAnswersToForm() {
    const root = $("[data-view='scope']");
    if (!root) return;
    const a = state.answers;
    $$("input[type='text'], input[type='date'], textarea, select", root).forEach((el) => {
      if (!el.name) return;
      if (a[el.name] == null) return;
      el.value = a[el.name];
    });
    $$("input[type='checkbox'][data-group]", root).forEach((el) => {
      const group = el.getAttribute("data-group");
      el.checked = (a[group] || []).includes(el.value);
    });
    $$("input[type='checkbox'][name]", root).forEach((el) => {
      if (el.dataset.group) return;
      el.checked = !!a[el.name];
    });
    const named = $("#sys-name");
    if (named) named.value = a.system_name || "";
  }

  function persistSession() {
    try {
      persistDraft();
      if (!state.result) return;
      sessionStorage.setItem(
        "abf-workpaper",
        JSON.stringify({
          version: "2.1",
          answers: state.answers,
          result: state.result,
          generated_at: new Date().toISOString(),
          fieldwork: {
            testing: state.testing,
            notes: state.notes,
            evidenceStatus: state.evidenceStatus,
            fieldworkPack: state.fieldworkPack,
            fwFilter: state.fwFilter,
            tab: state.tab,
          },
        })
      );
    } catch (err) {
      console.warn("ABF: could not persist session", err);
    }
  }

  function persistDraft() {
    try {
      sessionStorage.setItem("abf-draft", JSON.stringify(state.answers));
    } catch (err) {
      console.warn("ABF: could not persist draft", err);
    }
  }

  function restoreSession() {
    const saved = sessionStorage.getItem("abf-workpaper");
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        state.answers = { ...defaultAnswers(), ...parsed.answers };
        state.result = parsed.result || null;
        if (state.result && state.library) {
          state.applicable = state.library.obligations.filter((o) =>
            ABFEngine.obligationApplies(o, state.result)
          );
        }
        const fw = parsed.fieldwork || {};
        state.testing = fw.testing || {};
        state.notes = fw.notes || {};
        state.evidenceStatus = fw.evidenceStatus || {};
        if (typeof fw.fieldworkPack === "boolean") state.fieldworkPack = fw.fieldworkPack;
        if (fw.fwFilter) state.fwFilter = fw.fwFilter;
        if (fw.tab) state.tab = fw.tab;
        return;
      } catch (err) {
        console.warn("ABF: could not restore session", err);
      }
    }
    const draft = sessionStorage.getItem("abf-draft");
    if (draft) {
      try {
        state.answers = { ...defaultAnswers(), ...JSON.parse(draft) };
      } catch (err) {
        console.warn("ABF: could not restore draft", err);
      }
    }
  }

  function resetEngagement() {
    sessionStorage.removeItem("abf-workpaper");
    sessionStorage.removeItem("abf-draft");
    state.answers = defaultAnswers();
    state.result = null;
    state.applicable = [];
    state.step = 1;
    state.tab = "controls";
    state.testing = {};
    state.notes = {};
    state.evidenceStatus = {};
    state.openIds = new Set();
    state.fwFilter = "all";
    state.fieldworkPack = true;
    applyAnswersToForm();
    const err = $("#name-error");
    if (err) err.classList.add("hidden");
    renderWizard();
    updateNavBadge();
    location.hash = "scope";
    toast("Engagement cleared.");
  }

  function requireSystemName() {
    collectForm();
    const ok = !!(state.answers.system_name && state.answers.system_name.trim());
    const err = $("#name-error");
    const named = $("#sys-name");
    if (err) err.classList.toggle("hidden", ok);
    if (!ok && named) {
      named.focus();
      named.setAttribute("aria-invalid", "true");
    } else if (named) {
      named.removeAttribute("aria-invalid");
    }
    return ok;
  }

  function applyAnswersObject(obj) {
    state.answers = { ...defaultAnswers(), ...obj };
    if ((state.answers.markets || []).includes("us_banking")) {
      state.answers.us_supervised_bank = true;
    }
    state.answers.eu_in_scope = (state.answers.markets || []).includes("eu");
    applyAnswersToForm();
    persistDraft();
  }

  function fillSample() {
    state.testing = {};
    state.notes = {};
    state.evidenceStatus = {};
    applyAnswersObject(SAMPLE);
    state.step = 6;
    renderWizard();
    location.hash = "scope";
    toast("Sample answers loaded. Review the preview, then extract.");
  }

  function openSampleWorkpaper() {
    state.testing = {};
    state.notes = {};
    state.evidenceStatus = {};
    applyAnswersObject(SAMPLE);
    generate();
    toast("Sample credit-assistant workpaper opened.");
  }

  function generate() {
    collectForm();
    if (!requireSystemName()) {
      state.step = 1;
      renderWizard();
      location.hash = "scope";
      return;
    }
    state.result = ABFEngine.classify(state.answers);
    state.applicable = state.library.obligations.filter((o) =>
      ABFEngine.obligationApplies(o, state.result)
    );
    persistSession();
    persistDraft();
    $("#toast")?.classList.remove("show");
    location.hash = "results";
    renderResults();
    updateNavBadge();
  }

  function visibleItems() {
    return state.applicable.filter((o) => {
      if (state.fwFilter !== "all" && o.framework !== state.fwFilter) return false;
      if (!state.fieldworkPack) return true;
      if (o.procedure) return true;
      if (o.framework === "EU AI Act (Reg. 2024/1689)") return true;
      if (o.framework === "SR 11-7 / OCC 2011-12") return true;
      if (o.framework === "OWASP LLM Top 10 2025") return true;
      if (o.framework === "NIST AI 600-1") return true;
      return false;
    });
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
    if (state.step === 6) renderPreview();
    const pane = $(`.wizard-pane[data-step="${state.step}"]`, root);
    if (pane) pane.scrollIntoView({ block: "start" });
  }

  function renderPreview() {
    const mount = $("#preview-mount");
    if (!mount || !state.library) return;
    collectForm();
    const a = state.answers;
    const r = ABFEngine.classify(a);
    const applicable = state.library.obligations.filter((o) => ABFEngine.obligationApplies(o, r));
    const procs = applicable.filter((o) => o.procedure).length;
    const arch = (a.architecture || []).join(", ") || "not selected";
    const markets = (a.markets || []).join(", ") || "not selected";
    const findings = (r.findings || [])
      .map(
        (f) =>
          `<span class="chip">${esc(f.status)}</span>`
      )
      .join(" ");
    const gaps = [];
    if (!(a.markets || []).length) gaps.push("No market selected — EU and SR 11-7 overlays will stay off.");
    if (!(a.architecture || []).length) gaps.push("No architecture selected — OWASP / NIST AI 600-1 overlays will stay off.");
    mount.innerHTML = `
      <div class="preview-card">
        <h3>Live screening preview</h3>
        <dl class="preview-dl">
          <dt>System</dt><dd>${esc(a.system_name || "—")}</dd>
          <dt>Role</dt><dd>${esc(a.role)}</dd>
          <dt>Markets</dt><dd>${esc(markets)}</dd>
          <dt>Architecture</dt><dd>${esc(arch)}</dd>
          <dt>EU high-risk*</dt><dd>${r.eu_high_risk ? "Yes" : "No"}</dd>
          <dt>SR 11-7*</dt><dd>${r.sr117 ? "Yes" : "No"}</dd>
          <dt>Library hit</dt><dd>${applicable.length} sourced items · ${procs} walkthroughs</dd>
        </dl>
        ${findings ? `<p>${findings}</p>` : "<p class='help'>No additional screening findings yet. NIST AI RMF remains available as a voluntary backbone.</p>"}
        ${gaps.map((g) => `<p class="help">${esc(g)}</p>`).join("")}
        <p class="help">*Indicative only. Extract to open the workpaper, evidence register, and meeting agenda.</p>
      </div>`;
  }

  function renderResultsEmpty() {
    const mount = $("#results-mount");
    if (!mount) return;
    mount.innerHTML = `
      <div class="notice info">
        No workpaper in this session. Start a scoping engagement, import a JSON export, or open the sample credit-assistant file.
      </div>
      <div class="btn-row">
        <a class="btn" href="#scope">Open scoping wizard</a>
        <button class="btn btn-accent" type="button" id="empty-sample">Open sample workpaper</button>
        <button class="btn btn-secondary" type="button" data-import>Import JSON</button>
        <button class="btn btn-secondary" type="button" data-reset>Clear session</button>
      </div>`;
    $("#empty-sample")?.addEventListener("click", openSampleWorkpaper);
  }

  function countByFramework(items) {
    const m = {};
    items.forEach((o) => {
      m[o.framework] = (m[o.framework] || 0) + 1;
    });
    return m;
  }

  function testingCounts() {
    const counts = { not_started: 0, requested: 0, received: 0, tested: 0, exception: 0, na: 0 };
    visibleItems().forEach((o) => {
      const st = state.testing[o.id] || "not_started";
      counts[st] = (counts[st] || 0) + 1;
    });
    return counts;
  }

  function renderResults() {
    const mount = $("#results-mount");
    if (!mount || !state.result) return;
    const a = state.answers;
    const r = state.result;
    const visible = visibleItems();
    const counts = countByFramework(state.applicable);
    const tc = testingCounts();
    const findings = r.findings
      .map(
        (f) => `
      <article class="finding">
        <span class="status ${esc(f.tone || "info")}">${esc(f.status)}</span>
        <h3>${esc(f.topic)}</h3>
        <p>${esc(f.summary)}</p>
        <p class="cite">${esc(f.rule)}</p>
        <p><a href="${esc(f.source_url)}" target="_blank" rel="noopener">${esc(f.citation)}</a>
          <button class="btn-ghost" type="button" data-copy="${encodeURIComponent(f.citation + " — " + f.rule + " — " + f.source_url)}">Copy citation</button></p>
      </article>`
      )
      .join("");

    const frameworks = Object.keys(counts);

    mount.innerHTML = `
      <div class="print-banner">
        <h1>ABF workpaper — ${esc(a.system_name)}</h1>
        <p>${esc(a.engagement_id || "—")} · ${esc(a.engagement_date)} · ${esc(a.auditor || "—")}</p>
      </div>
      <p class="kicker">Engagement workpaper</p>
      <h2>${esc(a.system_name)}</h2>
      <p class="help">${esc(a.business_unit || "—")} · Owner ${esc(a.owner || "—")} · Auditor ${esc(a.auditor || "—")} · ${esc(a.engagement_id || a.engagement_date)}</p>
      ${a.intended_purpose ? `<p class="help"><em>Intended purpose.</em> ${esc(a.intended_purpose)}</p>` : ""}
      <div class="notice">
        ${esc(state.library.disclaimer)}
      </div>
      <div class="stats">
        <div class="stat"><b>${state.applicable.length}</b><span>Applicable sourced items</span></div>
        <div class="stat"><b>${state.applicable.filter((x) => x.procedure).length}</b><span>Walkthrough procedures</span></div>
        <div class="stat"><b>${r.eu_high_risk ? "Yes*" : "No*"}</b><span>EU high-risk (indicative)</span></div>
        <div class="stat"><b>${r.sr117 ? "Yes*" : "No*"}</b><span>SR 11-7 (indicative)</span></div>
      </div>
      <div class="progress-strip no-print">
        <span>Not started ${tc.not_started}</span>
        <span>Requested ${tc.requested}</span>
        <span>Received ${tc.received}</span>
        <span>Tested ${tc.tested}</span>
        <span>Exceptions ${tc.exception}</span>
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
        <button class="btn btn-secondary" data-export="evidence">Evidence register CSV</button>
        <button class="btn btn-secondary" data-export="md">Walkthrough Markdown</button>
        <button class="btn btn-secondary" data-export="memo">Screening memo</button>
        <button class="btn btn-secondary" data-export="agenda">Meeting agenda</button>
        <button class="btn btn-secondary" onclick="window.print()">Print / PDF</button>
        <button class="btn btn-secondary" type="button" data-reset>Start a new engagement</button>
      </div>
      <div class="workpaper-toolbar no-print">
        <label>Show
          <select id="pack-toggle">
            <option value="pack" ${state.fieldworkPack ? "selected" : ""}>Fieldwork pack (procedures + binding overlays)</option>
            <option value="full" ${!state.fieldworkPack ? "selected" : ""}>Full sourced set (includes NIST backbone)</option>
          </select>
        </label>
        <p class="help" style="margin:0">${visible.length} rows in the current filter.</p>
      </div>
      <div class="filter-chips no-print" role="tablist" aria-label="Framework filter">
        <button type="button" data-fw="all" class="${state.fwFilter === "all" ? "active" : ""}">All</button>
        ${frameworks
          .map(
            (f) =>
              `<button type="button" data-fw="${esc(f)}" class="${state.fwFilter === f ? "active" : ""}">${esc(f)} · ${counts[f]}</button>`
          )
          .join("")}
      </div>
      <div class="tabs no-print">
        <button data-tab="controls" class="${state.tab === "controls" ? "active" : ""}">Controls &amp; requirements</button>
        <button data-tab="walk" class="${state.tab === "walk" ? "active" : ""}">Walkthroughs</button>
        <button data-tab="agenda" class="${state.tab === "agenda" ? "active" : ""}">Meeting agenda</button>
        <button data-tab="evidence" class="${state.tab === "evidence" ? "active" : ""}">Evidence register</button>
        <button data-tab="matrix" class="${state.tab === "matrix" ? "active" : ""}">Alignment</button>
      </div>
      <div id="tab-mount"></div>
    `;
    renderTab();
    $$("[data-tab]", mount).forEach((btn) => {
      btn.addEventListener("click", () => {
        state.tab = btn.dataset.tab;
        persistSession();
        $$("[data-tab]", mount).forEach((b) => b.classList.toggle("active", b === btn));
        renderTab();
      });
    });
    $$("[data-export]", mount).forEach((btn) => {
      btn.addEventListener("click", () => exportWorkpaper(btn.dataset.export));
    });
    $$("[data-fw]", mount).forEach((btn) => {
      btn.addEventListener("click", () => {
        state.fwFilter = btn.dataset.fw;
        persistSession();
        renderResults();
      });
    });
    $("#pack-toggle")?.addEventListener("change", (e) => {
      state.fieldworkPack = e.target.value === "pack";
      persistSession();
      renderResults();
    });
    bindCopy(mount);
  }

  function statusSelect(id, current) {
    return `<select class="status-select" data-test="${esc(id)}" data-tone="${esc(current)}">
      ${TEST_STATUSES.map(
        (s) =>
          `<option value="${s.value}" ${s.value === current ? "selected" : ""}>${s.label}</option>`
      ).join("")}
    </select>`;
  }

  function evidenceSelect(key, current) {
    return `<select class="status-select" data-ev="${esc(key)}" data-tone="${esc(current)}">
      ${EVIDENCE_STATUSES.map(
        (s) =>
          `<option value="${s.value}" ${s.value === current ? "selected" : ""}>${s.label}</option>`
      ).join("")}
    </select>`;
  }

  function renderTab() {
    const mount = $("#tab-mount");
    if (!mount) return;
    const items = visibleItems();
    const withProc = items.filter((o) => o.procedure);
    const without = items.filter((o) => !o.procedure);
    if (state.tab === "controls") {
      mount.innerHTML =
        `<p class="help">${withProc.length} items have ABF walkthroughs (listed first). Remaining rows are official text for the audit file.
          <button class="btn-ghost" type="button" id="expand-all">Expand all</button>
          <button class="btn-ghost" type="button" id="collapse-all">Collapse all</button>
        </p>` + controlTable(withProc.concat(without), { fieldwork: true });
      bindRows(mount);
      $("#expand-all")?.addEventListener("click", () => {
        items.forEach((o) => state.openIds.add(o.id));
        renderTab();
      });
      $("#collapse-all")?.addEventListener("click", () => {
        state.openIds.clear();
        renderTab();
      });
    } else if (state.tab === "walk") {
      const byRole = {};
      withProc.forEach((o) => {
        const role = o.procedure.target_roles[0] || "Engagement team";
        byRole[role] = byRole[role] || [];
        byRole[role].push(o);
      });
      mount.innerHTML =
        `<p class="help">${withProc.length} ABF-authored procedures, grouped by primary interview role. Expand a card to run the walkthrough. These are not the source standard.</p>` +
        Object.entries(byRole)
          .map(([role, list]) => `<h3>${esc(role)}</h3>${list.map((o, i) => walkCard(o, i === 0)).join("")}`)
          .join("");
      bindCopy(mount);
    } else if (state.tab === "agenda") {
      mount.innerHTML = renderAgenda(withProc);
      bindCopy(mount);
    } else if (state.tab === "evidence") {
      const rows = [];
      items.forEach((o) => {
        (o.procedure?.evidence || []).forEach((e) => {
          const key = o.id + "::" + e;
          const st = state.evidenceStatus[key] || "planned";
          rows.push(
            `<tr>
              <td class="row-id">${esc(o.code)}</td>
              <td>${esc(o.framework)}</td>
              <td>${esc(e)}</td>
              <td>${esc((o.procedure.target_roles || []).join(", "))}</td>
              <td>${evidenceSelect(key, st)}</td>
            </tr>`
          );
        });
      });
      mount.innerHTML = `
        <p class="help">Evidence items are ABF workpaper suggestions derived from the cited requirement. They are not themselves regulatory mandates. Status is fieldwork metadata for this engagement.</p>
        <table>
          <thead><tr><th>ID</th><th>Framework</th><th>Evidence to request</th><th>Likely holder</th><th>Status</th></tr></thead>
          <tbody>${rows.join("") || "<tr><td colspan=5>No procedure-linked evidence in this scope. Use official text in the controls tab to derive requests.</td></tr>"}</tbody>
        </table>`;
      bindEvidenceSelects(mount);
    } else {
      mount.innerHTML = `
        <p class="help">Crosswalks are ABF mappings of related public identifiers. They are not official ISO or Commission transpositions.</p>
        <table>
          <thead><tr><th>Official ID</th><th>Title</th><th>Related identifiers</th></tr></thead>
          <tbody>
            ${items
              .map(
                (o) =>
                  `<tr><td class="row-id">${esc(o.code)}</td><td>${esc(o.title)}</td><td>${(o.crosswalk || [])
                    .map((c) => esc(c))
                    .join(", ") || "—"}</td></tr>`
              )
              .join("")}
          </tbody>
        </table>`;
    }
  }

  function renderAgenda(withProc) {
    const byRole = {};
    withProc.forEach((o) => {
      (o.procedure.target_roles || ["Engagement team"]).forEach((role) => {
        byRole[role] = byRole[role] || [];
        byRole[role].push(o);
      });
    });
    if (!withProc.length) {
      return `<p class="help">No walkthrough procedures in the current filter. Switch to the full sourced set or extract a system that hits EU, SR 11-7, or generative overlays.</p>`;
    }
    const a = state.answers;
    return (
      `<p class="help">Role-grouped interview pack for ${esc(a.system_name)}. Copy a block into the calendar invite. Questions are ABF-authored, mapped to official IDs.</p>` +
      Object.entries(byRole)
        .map(([role, list]) => {
          const text = agendaText(role, list);
          return `
            <article class="agenda">
              <header>
                <div>
                  <p class="cite">${list.length} procedures</p>
                  <h3>${esc(role)}</h3>
                </div>
                <button class="btn btn-secondary" type="button" data-copy="${encodeURIComponent(text)}">Copy agenda</button>
              </header>
              <div class="body">
                <p class="help">${esc(a.system_name)} · ${esc(a.engagement_id || a.engagement_date)}</p>
                <ol>
                  ${list
                    .map(
                      (o) =>
                        `<li><span class="row-id">${esc(o.code)}</span> — ${esc(o.procedure.inquiry)}</li>`
                    )
                    .join("")}
                </ol>
              </div>
            </article>`;
        })
        .join("")
    );
  }

  function agendaText(role, list) {
    const a = state.answers;
    const lines = [
      `ABF meeting agenda — ${role}`,
      `System: ${a.system_name}`,
      `Engagement: ${a.engagement_id || "—"} · ${a.engagement_date}`,
      `Indicative screening, not legal advice.`,
      "",
    ];
    list.forEach((o, i) => {
      lines.push(`${i + 1}. ${o.code} — ${o.procedure.title}`);
      lines.push(`   Ask: ${o.procedure.inquiry}`);
      lines.push(`   Observe: ${o.procedure.observe}`);
      lines.push("");
    });
    return lines.join("\n");
  }

  function controlTable(items, opts) {
    const fieldwork = !!(opts && opts.fieldwork);
    const body = items
      .map((o) => {
        const open = fieldwork && state.openIds.has(o.id);
        const st = state.testing[o.id] || "not_started";
        const note = state.notes[o.id] || "";
        const copyPayload = `${o.code} — ${o.title}\n${o.citation}\n${o.source_url}`;
        return `
      <tr data-open="${esc(o.id)}" aria-expanded="${open ? "true" : "false"}">
        <td class="row-id">${esc(o.code)}</td>
        <td>${esc(o.framework)}</td>
        <td>${esc(o.title)}</td>
        <td>${o.procedure ? "Yes" : "—"}</td>
        ${fieldwork ? `<td>${statusSelect(o.id, st)}</td>` : ""}
      </tr>
      <tr class="detail-row"><td colspan="${fieldwork ? 5 : 4}">
        <div class="detail${open ? " open" : ""}">
          <p class="cite">${esc(o.citation)}</p>
          <p><a href="${esc(o.source_url)}" target="_blank" rel="noopener">Open source</a> · ${esc(o.kind)}
            <button class="btn-ghost" type="button" data-copy="${encodeURIComponent(copyPayload)}">Copy citation</button>
            ${o.procedure ? `<button class="btn-ghost" type="button" data-copy="${encodeURIComponent(o.procedure.inquiry)}">Copy inquiry</button>` : ""}
          </p>
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
          ${
            fieldwork
              ? `<h4>Auditor note (this engagement)</h4>
          <textarea class="note-box" data-note="${esc(o.id)}" placeholder="Working paper note, exception rationale, or follow-up…">${esc(note)}</textarea>`
              : ""
          }
        </div>
      </td></tr>`;
      })
      .join("");
    return `
      <table>
        <thead><tr><th>ID</th><th>Source</th><th>Requirement / outcome</th><th>Procedure</th>${fieldwork ? "<th>Testing</th>" : ""}</tr></thead>
        <tbody>${body}</tbody>
      </table>`;
  }

  function walkCard(o, expanded) {
    const p = o.procedure;
    const copyInquiry = p.inquiry;
    const copyCite = `${o.code} — ${o.title}\n${o.citation}\n${o.source_url}`;
    return `
      <article class="walk">
        <header>
          <p class="cite">${esc(o.citation)}</p>
          <h3>${esc(p.title)}</h3>
          <p>Roles: ${esc(p.target_roles.join(" · "))}</p>
        </header>
        <div class="body">
          <div class="detail-actions no-print">
            <button class="btn-ghost" type="button" data-copy="${encodeURIComponent(copyCite)}">Copy citation</button>
            <button class="btn-ghost" type="button" data-copy="${encodeURIComponent(copyInquiry)}">Copy inquiry</button>
          </div>
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
      tr.addEventListener("click", (e) => {
        if (e.target.closest("select, button, a, textarea, input")) return;
        const id = tr.getAttribute("data-open");
        if (state.openIds.has(id)) state.openIds.delete(id);
        else state.openIds.add(id);
        const det = tr.nextElementSibling && tr.nextElementSibling.querySelector(".detail");
        if (det) det.classList.toggle("open", state.openIds.has(id));
        tr.setAttribute("aria-expanded", state.openIds.has(id) ? "true" : "false");
      });
    });
    $$("select[data-test]", root).forEach((sel) => {
      sel.addEventListener("click", (e) => e.stopPropagation());
      sel.addEventListener("change", () => {
        state.testing[sel.dataset.test] = sel.value;
        sel.setAttribute("data-tone", sel.value);
        persistSession();
        const strip = $(".progress-strip");
        if (strip && state.view === "results") {
          const tc = testingCounts();
          strip.innerHTML = `
            <span>Not started ${tc.not_started}</span>
            <span>Requested ${tc.requested}</span>
            <span>Received ${tc.received}</span>
            <span>Tested ${tc.tested}</span>
            <span>Exceptions ${tc.exception}</span>`;
        }
      });
    });
    $$("textarea[data-note]", root).forEach((box) => {
      box.addEventListener("click", (e) => e.stopPropagation());
      box.addEventListener(
        "input",
        debounce(() => {
          state.notes[box.dataset.note] = box.value;
          persistSession();
        }, 300)
      );
    });
    bindCopy(root);
  }

  function bindEvidenceSelects(root) {
    $$("select[data-ev]", root).forEach((sel) => {
      sel.addEventListener("change", () => {
        state.evidenceStatus[sel.dataset.ev] = sel.value;
        sel.setAttribute("data-tone", sel.value);
        persistSession();
      });
    });
  }

  function bindCopy(root) {
    $$("[data-copy]", root).forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        e.preventDefault();
        e.stopPropagation();
        let text = btn.getAttribute("data-copy") || "";
        try {
          text = decodeURIComponent(text);
        } catch (err) {
          /* already plain text */
        }
        try {
          await navigator.clipboard.writeText(text);
          toast("Copied to clipboard.");
        } catch (err) {
          console.warn("ABF: clipboard failed", err);
          toast("Could not copy — select the text instead.");
        }
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
      const blob = (o.id + o.title + o.official_text + o.citation + (o.code || "")).toLowerCase();
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
      const blob = (o.id + o.title + o.official_text + o.citation + (o.code || "")).toLowerCase();
      return matchFw && (!q || blob.includes(q));
    });
  }

  function paintLibraryTable(items) {
    const count = $("#lib-count");
    if (count) count.textContent = items.length + " shown. Click a row for official text and any mapped walkthrough.";
    const table = $("#lib-table");
    if (!table) return;
    table.innerHTML = controlTable(items, { fieldwork: false });
    bindRows(table);
  }

  function renderSources() {
    const mount = $("#sources-mount");
    if (!mount || !state.library) return;
    mount.innerHTML = `
      <p class="kicker">Bibliography</p>
      <h2>Authoritative sources used in this build</h2>
      <p class="help">Every library item stores a citation and URL. ABF does not generate unnamed “ABF-CTL” controls. Testing status, notes, and agendas are ABF workpaper metadata.</p>
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
    toast("Downloaded " + filename);
  }

  function csvEscape(v) {
    const s = String(v ?? "");
    if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
    return s;
  }

  function stampName() {
    return (state.answers.system_name || "system").replace(/\s+/g, "_").slice(0, 40);
  }

  function screeningMemo() {
    const a = state.answers;
    const r = state.result;
    const parts = [
      `# ABF screening memo — ${a.system_name}`,
      "",
      `> ${state.library.disclaimer}`,
      "",
      `- Engagement: ${a.engagement_id || "—"}`,
      `- Date: ${a.engagement_date}`,
      `- Auditor: ${a.auditor || "—"}`,
      `- Owner: ${a.owner || "—"}`,
      `- Role: ${a.role}`,
      `- Markets: ${(a.markets || []).join(", ") || "—"}`,
      `- Architecture: ${(a.architecture || []).join(", ") || "—"}`,
      `- Intended purpose: ${a.intended_purpose || "—"}`,
      `- EU high-risk (indicative): ${r.eu_high_risk ? "Yes" : "No"}`,
      `- Art. 6(3) possible exception: ${r.eu_possible_exception ? "Yes" : "No"}`,
      `- SR 11-7 (indicative): ${r.sr117 ? "Yes" : "No"}`,
      "",
      "## Findings",
      "",
    ];
    (r.findings || []).forEach((f) => {
      parts.push(`### ${f.topic}`);
      parts.push(`**${f.status}**`);
      parts.push("");
      parts.push(f.summary);
      parts.push("");
      parts.push(`Rule: ${f.rule}`);
      parts.push(`Source: ${f.citation} — ${f.source_url}`);
      parts.push("");
    });
    return parts.join("\n");
  }

  function agendaMarkdown() {
    const withProc = visibleItems().filter((o) => o.procedure);
    const byRole = {};
    withProc.forEach((o) => {
      (o.procedure.target_roles || ["Engagement team"]).forEach((role) => {
        byRole[role] = byRole[role] || [];
        byRole[role].push(o);
      });
    });
    const parts = [`# ABF meeting agenda — ${state.answers.system_name}`, "", `> ${state.library.disclaimer}`, ""];
    Object.entries(byRole).forEach(([role, list]) => {
      parts.push(agendaText(role, list));
      parts.push("");
    });
    return parts.join("\n");
  }

  function exportWorkpaper(kind) {
    const stamp = stampName();
    if (kind === "json") {
      download(
        `abf_workpaper_${stamp}.json`,
        JSON.stringify(
          {
            version: "2.1",
            disclaimer: state.library.disclaimer,
            answers: state.answers,
            screening: state.result,
            applicable: state.applicable.map((o) => ({
              id: o.id,
              code: o.code,
              framework: o.framework,
              title: o.title,
              citation: o.citation,
              source_url: o.source_url,
            })),
            fieldwork: {
              testing: state.testing,
              notes: state.notes,
              evidenceStatus: state.evidenceStatus,
              fieldworkPack: state.fieldworkPack,
              fwFilter: state.fwFilter,
            },
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
        "testing_status",
        "auditor_note",
      ];
      const lines = [header.join(",")];
      visibleItems().forEach((o) => {
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
            state.testing[o.id] || "not_started",
            state.notes[o.id] || "",
          ]
            .map(csvEscape)
            .join(",")
        );
      });
      download(`abf_controls_${stamp}.csv`, lines.join("\n"), "text/csv");
    } else if (kind === "evidence") {
      const header = ["id", "framework", "evidence", "holder", "status"];
      const lines = [header.join(",")];
      visibleItems().forEach((o) => {
        (o.procedure?.evidence || []).forEach((e) => {
          const key = o.id + "::" + e;
          lines.push(
            [o.code, o.framework, e, (o.procedure.target_roles || []).join(" | "), state.evidenceStatus[key] || "planned"]
              .map(csvEscape)
              .join(",")
          );
        });
      });
      download(`abf_evidence_${stamp}.csv`, lines.join("\n"), "text/csv");
    } else if (kind === "md") {
      const parts = [
        `# ABF walkthrough packet — ${state.answers.system_name}`,
        "",
        `> ${state.library.disclaimer}`,
        "",
        `Auditor: ${state.answers.auditor || "—"} · Date: ${state.answers.engagement_date}`,
        "",
      ];
      visibleItems()
        .filter((o) => o.procedure)
        .forEach((o) => {
          const p = o.procedure;
          parts.push(`## ${o.code}: ${p.title}`);
          parts.push(`**Official source:** ${o.citation}`);
          parts.push(`**Roles:** ${p.target_roles.join(", ")}`);
          parts.push(`**Testing status:** ${state.testing[o.id] || "not_started"}`);
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
          if (state.notes[o.id]) {
            parts.push("");
            parts.push("### Auditor note");
            parts.push(state.notes[o.id]);
          }
          parts.push("");
          parts.push(`_${p.authored_by}_`);
          parts.push("");
        });
      download(`abf_walkthrough_${stamp}.md`, parts.join("\n"), "text/markdown");
    } else if (kind === "memo") {
      download(`abf_screening_memo_${stamp}.md`, screeningMemo(), "text/markdown");
    } else if (kind === "agenda") {
      download(`abf_agenda_${stamp}.md`, agendaMarkdown(), "text/markdown");
    }
  }

  function importFromObject(parsed) {
    if (!parsed || typeof parsed !== "object") throw new Error("Not a JSON object");
    const answers = parsed.answers || parsed;
    if (!answers.system_name && !parsed.screening && !parsed.result) {
      throw new Error("JSON needs an answers object or a system_name");
    }
    applyAnswersObject(answers);
    const fw = parsed.fieldwork || {};
    state.testing = fw.testing || {};
    state.notes = fw.notes || {};
    state.evidenceStatus = fw.evidenceStatus || {};
    if (typeof fw.fieldworkPack === "boolean") state.fieldworkPack = fw.fieldworkPack;
    const screening = parsed.screening || parsed.result;
    if (screening && state.library) {
      state.result = screening;
      state.applicable = state.library.obligations.filter((o) =>
        ABFEngine.obligationApplies(o, state.result)
      );
      persistSession();
      location.hash = "results";
      renderResults();
      updateNavBadge();
      toast("Workpaper imported.");
    } else {
      state.step = 6;
      renderWizard();
      location.hash = "scope";
      toast("Answers imported. Review the preview, then extract.");
    }
  }

  function openImporter() {
    const input = $("#import-file");
    if (!input) return;
    input.value = "";
    input.click();
  }

  function bindImporter() {
    const input = $("#import-file");
    if (!input) return;
    input.addEventListener("change", async () => {
      const file = input.files && input.files[0];
      if (!file) return;
      try {
        const text = await file.text();
        importFromObject(JSON.parse(text));
      } catch (err) {
        console.warn("ABF: import failed", err);
        toast("Could not import that file. Use an ABF JSON export.");
      }
    });
    document.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-import]");
      if (btn) {
        e.preventDefault();
        openImporter();
      }
    });
  }

  function bindScope() {
    const root = $("[data-view='scope']");
    $$(".steps li", root).forEach((li) => {
      li.addEventListener("click", () => {
        collectForm();
        persistDraft();
        const next = Number(li.dataset.step);
        if (next > 1 && !requireSystemName()) {
          state.step = 1;
          renderWizard();
          return;
        }
        state.step = next;
        renderWizard();
      });
    });
    $$("[data-next]", root).forEach((btn) => {
      btn.addEventListener("click", () => {
        collectForm();
        persistDraft();
        if (state.step === 1 && !requireSystemName()) return;
        state.step = Math.min(6, state.step + 1);
        renderWizard();
      });
    });
    $$("[data-back]", root).forEach((btn) => {
      btn.addEventListener("click", () => {
        collectForm();
        persistDraft();
        state.step = Math.max(1, state.step - 1);
        renderWizard();
      });
    });
    root.addEventListener("change", () => {
      collectForm();
      persistDraft();
      if (state.step === 6) renderPreview();
    });
    root.addEventListener(
      "input",
      debounce(() => {
        collectForm();
        persistDraft();
        if (state.step === 6) renderPreview();
      }, 350)
    );
    $("#generate-btn")?.addEventListener("click", generate);
    $("#fill-sample")?.addEventListener("click", fillSample);
    $("#home-sample")?.addEventListener("click", openSampleWorkpaper);
    document.addEventListener("click", (e) => {
      if (e.target.closest("[data-reset]")) {
        e.preventDefault();
        resetEngagement();
      }
    });
  }

  function siteRoot() {
    const script = document.querySelector('script[src*="assets/app.js"]');
    if (script && script.src) {
      return script.src.replace(/assets\/app\.js(?:\?.*)?$/, "");
    }
    const href = window.location.href.split("#")[0];
    return href.endsWith("/") ? href : href.replace(/\/[^/]*$/, "/");
  }

  async function boot() {
    const res = await fetch(siteRoot() + "data/library.json");
    if (!res.ok) {
      document.body.insertAdjacentHTML(
        "afterbegin",
        `<div class="notice alert">Could not load data/library.json (${res.status}). Serve the site from the repository root or GitHub Pages project URL.</div>`
      );
      return;
    }
    state.library = await res.json();
    restoreSession();
    bindScope();
    bindImporter();
    applyAnswersToForm();
    const dateInput = document.querySelector("input[name='engagement_date']");
    if (dateInput && !dateInput.value) dateInput.value = state.answers.engagement_date;
    window.addEventListener("hashchange", route);
    route();
    document.body.setAttribute("data-abf-ready", "1");
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
