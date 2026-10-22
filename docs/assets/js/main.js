(function () {
  "use strict";
  var lang = document.documentElement.lang === "en" ? "en" : "he";

  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Forms without a backend yet: show a confirmation instead of submitting.
  // Point the form's action at your form service (e.g. Formspree) and remove data-demo.
  document.querySelectorAll("form[data-demo]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status");
      if (status) status.textContent = form.getAttribute("data-success");
    });
  });

  // ---------- Public registry search ----------
  var T = {
    he: {
      credential: "הסמכה", number: "מספר הסמכה", city: "עיר", expires: "בתוקף עד", status: "סטטוס",
      active: "בתוקף", expired: "פג תוקף", inactive: "לא פעיל",
      none: "לא נמצאו תוצאות. בדקו את האיות או חפשו לפי מספר ההסמכה. אם לדעתכם מדובר בטעות, צרו קשר עם המועצה.",
      count: function (n) { return n === 1 ? "נמצאה תוצאה אחת" : "נמצאו " + n + " תוצאות"; },
      prompt: "יש להזין לפחות 2 תווים לחיפוש."
    },
    en: {
      credential: "Credential", number: "Certificate no.", city: "City", expires: "Valid until", status: "Status",
      active: "Active", expired: "Expired", inactive: "Inactive",
      none: "No matching records. Check the spelling or search by certificate number. If you believe this is an error, contact ICBAP.",
      count: function (n) { return n + (n === 1 ? " result" : " results"); },
      prompt: "Please enter at least 2 characters."
    }
  }[lang];

  var form = document.getElementById("registry-form");
  var results = document.getElementById("registry-results");
  if (!form || !results || !window.REGISTRY) return;

  function norm(s) { return (s || "").toString().toLowerCase().replace(/[֑-ׇ]/g, "").trim(); }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function search(q, cred) {
    q = norm(q);
    return window.REGISTRY.filter(function (r) {
      if (cred && r.credential !== cred) return false;
      var hay = norm([r.name_he, r.name_en, r.number, r.city_he, r.city_en, r.credential].join(" "));
      return q.split(/\s+/).every(function (part) { return hay.indexOf(part) !== -1; });
    });
  }

  function renderRows(rows) {
    if (!rows.length) { results.innerHTML = '<div class="empty-state">' + esc(T.none) + "</div>"; return; }
    var html = '<p class="muted">' + esc(T.count(rows.length)) + '</p><div class="table-wrap"><table><thead><tr>' +
      "<th>" + (lang === "en" ? "Name" : "שם") + "</th><th>" + T.credential + "</th><th>" + T.number + "</th><th>" +
      T.city + "</th><th>" + T.expires + "</th><th>" + T.status + "</th></tr></thead><tbody>";
    rows.forEach(function (r) {
      html += "<tr><td><strong>" + esc(lang === "en" ? r.name_en : r.name_he) + "</strong></td>" +
        '<td><span class="ltr">' + esc(r.credential) + (r.endorsements && r.endorsements.length ? " + " + esc(r.endorsements.join(", ")) : "") + "</span></td>" +
        '<td><span class="ltr">' + esc(r.number) + "</span></td>" +
        "<td>" + esc(lang === "en" ? r.city_en : r.city_he) + "</td>" +
        '<td><span class="ltr">' + esc(r.expires) + "</span></td>" +
        '<td><span class="status ' + esc(r.status) + '">' + esc(T[r.status]) + "</span></td></tr>";
    });
    results.innerHTML = html + "</tbody></table></div>";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = form.querySelector("[name=q]").value;
    var cred = form.querySelector("[name=credential]").value;
    if (norm(q).length < 2 && !cred) { results.innerHTML = '<div class="empty-state">' + esc(T.prompt) + "</div>"; return; }
    renderRows(search(q, cred));
  });

  // Support links like verify.html?q=12345 (used by the homepage quick-verify box)
  var params = new URLSearchParams(location.search);
  if (params.get("q")) {
    form.querySelector("[name=q]").value = params.get("q");
    renderRows(search(params.get("q"), ""));
  }
})();
