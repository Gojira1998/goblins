/* Goblin shop: buttons on every horde card + the shop section. Lives apart from app.js because gerar_horda.py rewrites app.js and style.css. */
(function () {
  var S = window.GOBLIN_SHOP || {};
  var ready = function (u) { return typeof u === "string" && /^https:\/\//.test(u); };
  var block = (S.block || []).map(function (x) { return String(x).toLowerCase(); });
  var toast = document.createElement("div");
  toast.className = "shop-toast"; toast.setAttribute("role", "status"); toast.hidden = true;
  document.body.appendChild(toast);
  var timer;
  function say(t) { toast.textContent = t; toast.hidden = false; clearTimeout(timer); timer = setTimeout(function () { toast.hidden = true; }, 6000); }
  function copy(t) { try { if (navigator.clipboard) navigator.clipboard.writeText(t); } catch (e) {} }

  function button(url, label, cls, handle) {
    if (!ready(url)) {
      var s = document.createElement("span");
      s.className = "hbtn " + cls + " off"; s.textContent = label.replace(/\s*\(.*\)$/, "") + ": soon";
      s.title = "The shop opens soon"; return s;
    }
    var a = document.createElement("a");
    a.className = "hbtn " + cls; a.href = url; a.target = "_blank"; a.rel = "noopener"; a.textContent = label;
    a.addEventListener("click", function () {
      copy("@" + handle);
      say("We copied @" + handle + ". Paste it when Ko-fi asks for your @. Delivery within 24 hours.");
    });
    return a;
  }

  document.querySelectorAll("#hgrid .hcard").forEach(function (c) {
    var h = c.getAttribute("data-h");
    if (!h || c.classList.contains("wait") || block.indexOf(h) > -1 || c.querySelector(".hbuy")) return;
    var box = document.createElement("div"); box.className = "hbuy";
    box.appendChild(button(S.hd, "Get your HD goblin (" + (S.priceHd || "$3") + ")", "hd", h));
    box.appendChild(button(S.anim, "Animate my goblin (" + (S.priceAnim || "$7") + ")", "an", h));
    c.appendChild(box);
  });

  /* shop section: shows "Shop opens soon" until the Ko-fi links exist */
  var open = ready(S.hd) && ready(S.anim);
  document.querySelectorAll("[data-shop-soon]").forEach(function (e) { e.hidden = open; });
  document.querySelectorAll("[data-shop-open]").forEach(function (e) { e.hidden = !open; });
})();
