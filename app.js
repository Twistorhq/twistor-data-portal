/* Twistor Data portal - minimal interactions. No dependencies. */
(function () {
  "use strict";

  /* Mobile nav */
  var toggle = document.querySelector(".nav-toggle");
  var navList = document.getElementById("nav-list");
  if (toggle && navList) {
    toggle.addEventListener("click", function () {
      var open = navList.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    navList.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        navList.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && navList.classList.contains("open")) {
        navList.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  /* Copy buttons for code samples */
  document.querySelectorAll(".copy-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var target = document.getElementById(btn.getAttribute("data-copy-target"));
      if (!target) return;
      var text = target.textContent;
      function done() {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy"; }, 1600);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, done);
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta);
        done();
      }
    });
  });

  /* Dataset catalog filter (TW-667): domain chips + search, a stated
     result count, and a structured empty state. State also reads from
     ?lane= and ?q= so a filtered view is shareable and screenshot-able. */
  var catalogRows = Array.prototype.slice.call(document.querySelectorAll(".dataset-row[data-lane]"));
  var catalogChips = Array.prototype.slice.call(document.querySelectorAll("[data-lane-filter]"));
  var catalogSearch = document.getElementById("dataset-search");
  var catalogCount = document.getElementById("dataset-count");
  var catalogEmpty = document.getElementById("dataset-empty");
  var catalogClear = document.getElementById("dataset-clear");
  if (catalogRows.length && catalogCount) {
    var activeLane = "all";
    var totalRows = catalogRows.reduce(function (sum, row) {
      var dts = row.querySelectorAll(".dataset-meta dt");
      var value = 0;
      dts.forEach(function (dt) {
        if (dt.textContent.indexOf("Rows") === 0) {
          value = parseInt(dt.parentElement.querySelector("dd").textContent, 10) || 0;
        }
      });
      return sum + value;
    }, 0);
    function applyCatalog() {
      var q = catalogSearch ? catalogSearch.value.trim().toLowerCase() : "";
      var shown = 0;
      catalogRows.forEach(function (row) {
        var laneOk = activeLane === "all" || row.getAttribute("data-lane") === activeLane;
        var textOk = !q || row.textContent.toLowerCase().indexOf(q) !== -1;
        var visible = laneOk && textOk;
        row.hidden = !visible;
        if (visible) shown += 1;
      });
      catalogCount.textContent =
        "Showing " + shown + " of " + catalogRows.length + " datasets. " +
        totalRows + " rows in v1.0 across the three datasets, every row a synthetic-labeled seed.";
      if (catalogEmpty) catalogEmpty.hidden = shown !== 0;
      catalogChips.forEach(function (chip) {
        var selected = chip.getAttribute("data-lane-filter") === activeLane;
        chip.classList.toggle("is-selected", selected);
        chip.setAttribute("aria-pressed", selected ? "true" : "false");
      });
    }
    catalogChips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        activeLane = chip.getAttribute("data-lane-filter");
        applyCatalog();
      });
    });
    if (catalogSearch) catalogSearch.addEventListener("input", applyCatalog);
    if (catalogClear) {
      catalogClear.addEventListener("click", function () {
        activeLane = "all";
        if (catalogSearch) catalogSearch.value = "";
        applyCatalog();
        if (catalogSearch) catalogSearch.focus();
      });
    }
    var params = new URLSearchParams(window.location.search);
    var laneParam = params.get("lane");
    if (laneParam && catalogChips.some(function (c) { return c.getAttribute("data-lane-filter") === laneParam; })) {
      activeLane = laneParam;
    }
    if (catalogSearch && params.get("q")) catalogSearch.value = params.get("q");
    applyCatalog();
  }

  /* Access request form: no self-serve endpoint yet (TW-605), so compose
     an email to the Twistor team with the request prefilled. */
  var form = document.getElementById("access-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var subject = "Dataset access request: " + (data.get("dataset") || "unspecified");
      var body = [
        "Name: " + data.get("name"),
        "Email: " + data.get("email"),
        "Institution: " + data.get("org"),
        "Dataset: " + data.get("dataset"),
        "",
        "Research:",
        data.get("use")
      ].join("\n");
      var note = document.getElementById("form-note");
      if (note) {
        note.textContent = "Opening your email client with the request prefilled - send it and we will provision your access.";
      }
      window.location.href =
        "mailto:holla@twistor.co?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
    });
  }
})();
