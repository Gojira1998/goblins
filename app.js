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

  /* lead capture: one function per box (Goblin Prompt Pack = #form-lead, First Ticket = #form-ft). Same table, post_slug marks the box. */
  var p = new URLSearchParams(location.search);
  function captura(formId, caixaId, brindeId, msgId) {
    var form = document.getElementById(formId), brinde = document.getElementById(brindeId), caixa = document.getElementById(caixaId);
    if (!form || !brinde || !caixa) return;
    var slug = form.getAttribute("data-slug"), chave = "jga_lead_" + slug, aberto = Date.now();
    function liberar(scroll) { brinde.hidden = false; caixa.hidden = true; if (scroll) brinde.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); }
    try { if (localStorage.getItem(chave) === "1") { liberar(false); return; } } catch (e) {}
    if (p.get("preview") === "1" && (location.hostname === "localhost" || location.hostname === "127.0.0.1" || location.protocol === "file:")) { liberar(false); return; }

    var msg = document.getElementById(msgId);
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
      if (!f.get("consent")) { erro("Tick the consent box to unlock it."); return; }
      var cfg = window.JGA_LEADS || {};
      if (!cfg.url || !cfg.anonKey) { erro("Sign-up is being fixed. It stays locked for now. Try again later."); return; }
      var botao = form.querySelector("button[type=submit]");
      var txt = botao.innerHTML; botao.disabled = true; botao.textContent = "Sending...";
      var corpo = { nome: nome, whatsapp: fone, email: email, post_slug: slug, mentoria: false, consentimento: true,
        origem: (p.get("utm_source") || document.referrer || "direct").slice(0, 120) };
      fetch(cfg.url.replace(/\/$/, "") + "/rest/v1/" + (cfg.tabela || "leads"), {
        method: "POST",
        headers: { "Content-Type": "application/json", "apikey": cfg.anonKey, "Authorization": "Bearer " + cfg.anonKey, "Prefer": "return=minimal" },
        body: JSON.stringify(corpo)
      }).then(function (r) {
        if (!r.ok && r.status !== 409) throw new Error("status " + r.status);   // 409 = already signed up for this box: unlock anyway
        try { localStorage.setItem(chave, "1"); } catch (e) {}
        liberar(true);
      }).catch(function () {
        erro("We could not send your details. It is still locked. Try again in a moment.");
        botao.disabled = false; botao.innerHTML = txt;
      });
    });
  }
  captura("form-lead", "locked", "brinde", "msg-erro");
  captura("form-ft", "locked-ft", "brinde-ft", "msg-erro-ft");
  captura("form-t2", "locked-t2", "brinde-t2", "msg-erro-t2");
})();

/* the horde: busca por @ (gerado por gerar_horda.py) */
(function(){var q=document.getElementById('hq');if(!q)return;
var cs=[].slice.call(document.querySelectorAll('#hgrid .hcard')),out=document.getElementById('hcount'),none=document.getElementById('hnone'),base=out.textContent;
var EP2=["victor_automates", "mcautomate", "tajnyslipy", "rinraroyl", "anaar_net", "stck.wrld"];
function norm(v){return (v||'').trim().toLowerCase().replace(/^@+/,'').replace(/^https?:\/\/(www\.)?instagram\.com\//,'').replace(/[\/?#].*$/,'');}
function run(v,go){v=norm(v);var n=0,exact=null;
 cs.forEach(function(c){c.classList.remove('hit');var h=c.getAttribute('data-h');var ok=!v||h.indexOf(v)>-1||c.getAttribute('data-q').indexOf(v)>-1;if(v&&h===v)exact=c;c.hidden=!ok;if(ok)n++;});
 if(exact){cs.forEach(function(c){c.hidden=c!==exact;});n=1;exact.classList.add('hit');}
 out.textContent=v?(n+(n===1?' goblin':' goblins')):base;
 none.hidden=true;
 if(v&&!n){none.hidden=false;none.textContent=EP2.indexOf(v)>-1?('@'+v+', you walked out in episode 2 with the first six. Your card is coming. Comment the look you want on the latest episode.'):('No goblin for @'+v+' yet. Comment the goblin you want to be on the latest episode and follow. You walk out of the next server.');}
 if(go){var t=exact||document.getElementById('horde');setTimeout(function(){t.scrollIntoView({behavior:'smooth',block:exact?'center':'start'});},60);}
}
q.addEventListener('input',function(){run(q.value,false);});
var top=document.getElementById('findtop');
if(top)top.addEventListener('submit',function(e){e.preventDefault();var v=top.querySelector('input').value;q.value=v;run(v,true);try{history.replaceState(null,'','?me='+encodeURIComponent(norm(v))+'#horde');}catch(_){}});
var me=new URLSearchParams(location.search).get('me')||((location.hash.match(/^#@(.+)$/)||[])[1]);
if(me){me=decodeURIComponent(me);q.value='@'+norm(me);run(me,true);}
})();
