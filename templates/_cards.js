/* anki-code-cards: editor + line-diff logic (shared by all templates) */
(function () {
  var STORE_KEY = "anki_typed_code";

  function decode(b64) {
    if (!b64) return "";
    try { return decodeURIComponent(escape(window.atob(b64))); }
    catch (e) { return b64; }
  }

  function tabKey(cm) {
    if (cm.somethingSelected()) cm.execCommand("indentMore");
    else cm.replaceSelection("    ", "end");
  }

  function opts(lang, extra) {
    var base = {
      mode: lang || "rust",
      theme: "vscdark",
      lineNumbers: true,
      indentUnit: 4, tabSize: 4, indentWithTabs: false,
      matchBrackets: true, autoCloseBrackets: true,
      viewportMargin: Infinity,
      extraKeys: { "Tab": tabKey }
    };
    for (var k in (extra || {})) base[k] = extra[k];
    return base;
  }

  function rstrip(s) { return (s || "").replace(/\s+$/, ""); }
  function data() { return document.getElementById("cm-data"); }

  // FRONT of a code card: editable editor that saves typed code
  window.ankiCodeFront = function () {
    var d = data(); if (!d || typeof CodeMirror === "undefined") return;
    var lang = d.getAttribute("data-lang") || "rust";
    var starter = decode(d.getAttribute("data-starter"));
    var host = document.getElementById("editor"); if (!host) return;
    host.innerHTML = "";
    var cm = CodeMirror(host, opts(lang, { value: starter, autofocus: true }));
    function save() { try { sessionStorage.setItem(STORE_KEY, cm.getValue()); } catch (e) {} }
    save();
    cm.on("change", save);
    setTimeout(function () { cm.refresh(); cm.focus(); }, 60);
  };

  // BACK of a code card: read-only typed code with wrong lines in red + solution
  window.ankiCodeBack = function () {
    var d = data(); if (!d || typeof CodeMirror === "undefined") return;
    var lang = d.getAttribute("data-lang") || "rust";
    var solution = decode(d.getAttribute("data-solution"));
    var typed = "";
    try { typed = sessionStorage.getItem(STORE_KEY) || ""; } catch (e) {}

    var host = document.getElementById("editor"), cm = null;
    if (host) {
      host.innerHTML = "";
      cm = CodeMirror(host, opts(lang, { value: typed, readOnly: "nocursor" }));
    }

    var ut = typed.replace(/\r\n/g, "\n").split("\n");
    var st = solution.replace(/\r\n/g, "\n").split("\n");
    var n = Math.max(ut.length, st.length), wrong = 0;
    for (var i = 0; i < n; i++) {
      if (rstrip(ut[i]) !== rstrip(st[i])) {
        wrong++;
        if (cm && i < ut.length) cm.addLineClass(i, "background", "wrong-line");
      }
    }
    if (cm) setTimeout(function () { cm.refresh(); }, 60);

    renderReadonly("solution", solution, lang);

    var status = document.getElementById("status");
    if (status) {
      if (wrong === 0) {
        status.textContent = "✓ Correct"; status.className = "status ok";
      } else {
        status.textContent = wrong + (wrong === 1 ? " line differs" : " lines differ");
        status.className = "status bad";
      }
    }
  };

  // Read-only highlighted snippet (used by concept-card backs)
  function renderReadonly(id, code, lang) {
    var host = document.getElementById(id);
    if (!host || typeof CodeMirror === "undefined") return;
    host.innerHTML = "";
    var cm = CodeMirror(host, opts(lang, { value: code, readOnly: "nocursor" }));
    setTimeout(function () { cm.refresh(); }, 60);
  }

  window.ankiCodeShow = function () {
    var d = data(); if (!d) return;
    var lang = d.getAttribute("data-lang") || "rust";
    var code = decode(d.getAttribute("data-solution"));
    if (code) renderReadonly("solution", code, lang);
  };
})();
