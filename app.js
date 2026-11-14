/* Agents Goblins page: counter, effects, lead capture (Supabase REST, INSERT only, same table as the Mestre do Claude blog). */
(function () {
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* follower counter from contador.json (honest: not real time) */
  var cnt = document.getElementById("cnt"), upd = document.getElementById("cnt-upd");
  fetch("contador.json?v=" + Date.now()).then(function (r) { return r.json(); }).then(function (d) {
    var n = parseInt(d.followers, 10); if (isNaN(n)) throw 0;
    var today = new Date().toISOString().slice(0, 10);
    upd.textContent = (d.updated === today || !d.updated) ? "updated today" : "updated " + d.updated;
    if (reduce || n === 0) { cnt.textContent = n.toLocaleString("en-US"); return; }
    var t0 = performance.now();
    (function tick(t) { var k = Math.min(1, (t - t0) / 1200); cnt.textContent = Math.round(n * k).toLocaleString("en-US"); if (k < 1) requestAnimationFrame(tick); })(t0);
  }).catch(function () { cnt.textContent = "—"; upd.textContent = ""; });

  /* embers */
  var em = document.querySelector(".embers");
  if (em && !reduce) for (var i = 0; i < 16; i++) {
    var s = document.createElement("i");
    s.style.left = Math.random() * 100 + "%"; s.style.animationDuration = (6 + Math.random() * 7) + "s"; s.style.animationDelay = (-Math.random() * 10) + "s";
    s.style.opacity = 0; em.appendChild(s);
  }

  /* parallax */
  var bg = document.getElementById("heroBg");
  if (bg && !reduce) addEventListener("scroll", function () { var y = Math.min(scrollY, 900); bg.style.transform = "translateY(" + (y * 0.25) + "px) scale(1.08)"; }, { passive: true });

  /* reveal on scroll */
  var els = document.querySelectorAll(".gob,.pain,.ep,.human-box,.note");
  els.forEach(function (e) { e.classList.add("rv"); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (a) { a.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("on"); io.unobserve(x.target); } }); }, { threshold: .12 });
    els.forEach(function (e) { io.observe(e); });
  } else els.forEach(function (e) { e.classList.add("on"); });

  /* copy buttons */
  document.querySelectorAll(".cp").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.parentNode.querySelector("pre").textContent;
      var ok = function () { b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy"; }, 1500); };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, ok); else ok();
    });
  });

  /* lead capture */
  var form = document.getElementById("form-lead"), brinde = document.getElementById("brinde"), caixa = document.getElementById("locked");
  if (!form) return;
  var slug = form.getAttribute("data-slug"), chave = "jga_lead_" + slug, aberto = Date.now();
  function liberar(scroll) { brinde.hidden = false; caixa.hidden = true; if (scroll) brinde.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); }
  var p = new URLSearchParams(location.search);
  try { if (localStorage.getItem(chave) === "1") { liberar(false); return; } } catch (e) {}
  if (p.get("preview") === "1" && (location.hostname === "localhost" || location.hostname === "127.0.0.1" || location.protocol === "file:")) { liberar(false); return; }

  var msg = document.getElementById("msg-erro");
  function erro(t) { msg.textContent = t || ""; }
  form.addEventListener("submit", function (ev) {
    ev.preventDefault(); erro("");
    var f = new FormData(form);
    if (f.get("site_url")) return;
    if (Date.now() - aberto < 3000) { erro("Hold on a second and hit the button again."); return; }
    var nome = (f.get("name") || "").trim();
    var email = (f.get("email") || "").trim().toLowerCase();
    var fone = (f.get("phone") || "").replace(/\D/g, "");
    if (nome.length < 2) { erro("Type your name."); return; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) { erro("Check your email address."); return; }
    if (fone.length < 10 || fone.length > 13) { erro("Check your phone: country code plus number, 10 to 13 digits. Example: +1 555 123 4567."); return; }
    if (!f.get("consent")) { erro("Tick the consent box to unlock the pack."); return; }
    var cfg = window.JGA_LEADS || {};
    if (!cfg.url || !cfg.anonKey) { erro("Sign-up is being fixed. The pack stays locked for now. Try again later."); return; }
    var botao = form.querySelector("button[type=submit]");
    var txt = botao.innerHTML; botao.disabled = true; botao.textContent = "Sending...";
    var corpo = { nome: nome, whatsapp: fone, email: email, post_slug: slug, mentoria: false, consentimento: true,
      origem: (p.get("utm_source") || document.referrer || "direct").slice(0, 120) };
    fetch(cfg.url.replace(/\/$/, "") + "/rest/v1/" + (cfg.tabela || "leads"), {
      method: "POST",
      headers: { "Content-Type": "application/json", "apikey": cfg.anonKey, "Authorization": "Bearer " + cfg.anonKey, "Prefer": "return=minimal" },
      body: JSON.stringify(corpo)
    }).then(function (r) {
      if (!r.ok && r.status !== 409) throw new Error("status " + r.status);   // 409 = already signed up for this pack: unlock anyway
      try { localStorage.setItem(chave, "1"); } catch (e) {}
      liberar(true);
    }).catch(function () {
      erro("We could not send your details. The pack is still locked. Try again in a moment.");
      botao.disabled = false; botao.innerHTML = txt;
    });
  });
})();
