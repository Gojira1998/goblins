"""Gera a seção THE HORDE (ficha de cada goblin com @, imagem e esquadrão) dentro do index.html da página dos goblins.
Uso: python gerar_horda.py   (lê producao/C-video3/goblins/LISTA-goblins.json e grupos.json; imagens em assets/horda/NN.webp)"""
import json, html, re, os
B = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(B, "..", "..", "producao", "C-video3")
L = json.load(open(os.path.join(P, "goblins", "LISTA-goblins.json"), encoding="utf-8"))
G = json.load(open(os.path.join(P, "grupos.json"), encoding="utf-8"))["grupos"]
squad = {}
for gr in G:
    for x in gr["goblins"]: squad.setdefault(x["n"], gr["tarefa"])
PAPEL = {1: "Squad leader", 2: "Big and strong", 11: "The Shadow, night watch chief", 12: "Night watch", 13: "Night watch", 14: "The lone goblin", 15: "Leads his own crew", 16: "Korg, red goblin warlord", 17: "The Manager"}
OFENSIVO = {"@rivertheretard": "RIVER"}

def limpa(s):
    s = re.sub(r"^(a|an|the)\s+", "", s.strip(), flags=re.I)
    s = re.sub(r"^[A-Z][\w.]*: ", "", s) if ":" in s[:22] else s
    return s[0].upper() + s[1:]

cards = []
for x in L:
    n, h = x["n"], x["handle"]
    nome = OFENSIVO.get(h, h)
    link = "" if h in OFENSIVO else f' href="https://www.instagram.com/{h[1:]}/" target="_blank" rel="noopener"'
    tag = "a" if link else "span"
    sq = "THE LONE GOBLIN" if n == 14 else squad.get(n, "THE HORDE")
    papel = PAPEL.get(n, "")
    cls = " lead" if n == 1 else " lone" if n == 14 else ""
    cards.append(
        f'<article class="hcard{cls}" data-q="{html.escape((nome + " " + sq + " " + x["como"]).lower())}">'
        f'<div class="hn">#{n:02d}</div>'
        f'<div class="hi"><img src="assets/horda/{n:02d}.webp" alt="{html.escape("Goblin of " + nome + ": " + x["como"])}" loading="lazy" width="130" height="150"></div>'
        f'<{tag} class="hh"{link}>{html.escape(nome)}</{tag}>'
        f'<p class="hs">{html.escape(sq)}{(" · " + html.escape(papel)) if papel else ""}</p>'
        f'<p class="hd">{html.escape(limpa(x["como"]))}</p></article>')

sec = f'''<!-- THE HORDE (gerado por gerar_horda.py) -->
<section class="sec" id="horde">
  <h2 class="h"><span>02</span> The horde</h2>
  <p class="lead">83 of you asked to be a goblin. In episode 3 the old server flooded and every one of you walked out, dressed the way you asked. Find your card.</p>
  <label class="hsearch"><span>Find your @</span><input id="hq" type="search" placeholder="type your @ or a squad" autocomplete="off"></label>
  <p class="hcount" id="hcount">{len(cards)} goblins</p>
  <div class="hgrid" id="hgrid">
{chr(10).join("    " + c for c in cards)}
  </div>
  <p class="note">Not a goblin yet? Comment the goblin you want to be on the latest episode and follow. You walk out of the next server.</p>
</section>
<!-- /THE HORDE -->
'''
css = '''
/* the horde (gerado por gerar_horda.py) */
.hsearch{display:flex;flex-direction:column;gap:6px;margin:18px 0 6px;font:400 9px var(--px);color:var(--lime)}
.hsearch input{font:500 16px 'Space Grotesk',sans-serif;padding:12px 14px;background:var(--bg2);color:var(--cream);border:3px solid var(--ink);box-shadow:4px 4px 0 var(--moss);outline:none}
.hsearch input:focus{border-color:var(--fire)}
.hcount{font:400 9px var(--px);opacity:.7;margin:8px 0 14px}
.hgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media(min-width:560px){.hgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(min-width:760px){.hgrid{grid-template-columns:repeat(4,minmax(0,1fr))}}
.hcard{position:relative;background:var(--bg2);border:3px solid var(--ink);box-shadow:4px 4px 0 var(--moss);padding:10px 10px 12px;display:flex;flex-direction:column;gap:4px;min-width:0}
.hcard.lead{box-shadow:4px 4px 0 var(--fire)}.hcard.lone{box-shadow:4px 4px 0 #b3263a}
.hn{position:absolute;top:6px;left:8px;font:400 8px var(--px);color:var(--lime);opacity:.8}
.hi{height:150px;display:flex;align-items:flex-end;justify-content:center;background:radial-gradient(ellipse at 50% 85%,rgba(56,224,200,.14),transparent 65%)}
.hi img{max-height:146px;width:auto;image-rendering:pixelated}
.hh{font:400 9px/1.5 var(--px);color:var(--fire);text-decoration:none;overflow-wrap:anywhere;margin-top:4px}
a.hh:hover{text-decoration:underline}
.hs{font:400 7px/1.5 var(--px);color:var(--cyan)}
.hd{font-size:12px;line-height:1.4;opacity:.85}
.hcard[hidden]{display:none}
'''
js = '''
/* the horde: busca (gerado por gerar_horda.py) */
(function(){var q=document.getElementById('hq');if(!q)return;var cs=[].slice.call(document.querySelectorAll('#hgrid .hcard')),out=document.getElementById('hcount');
q.addEventListener('input',function(){var v=q.value.trim().toLowerCase().replace(/^@/,''),n=0;cs.forEach(function(c){var ok=!v||c.getAttribute('data-q').indexOf(v)>-1;c.hidden=!ok;if(ok)n++;});out.textContent=n+(n===1?' goblin':' goblins');});})();
'''
h = open(os.path.join(B, "index.html"), encoding="utf-8").read()
h = re.sub(r"<!-- THE HORDE.*?<!-- /THE HORDE -->\n", "", h, flags=re.S)
h = h.replace("<!-- 3. HUMAN BEHIND -->", sec + "\n<!-- 3. HUMAN BEHIND -->", 1)
assert 'id="horde"' in h
open(os.path.join(B, "index.html"), "w", encoding="utf-8").write(h)
s = open(os.path.join(B, "style.css"), encoding="utf-8").read(); s = re.sub(r"\n/\* the horde \(gerado.*", "", s, flags=re.S) + css
open(os.path.join(B, "style.css"), "w", encoding="utf-8").write(s)
a = open(os.path.join(B, "app.js"), encoding="utf-8").read(); a = re.sub(r"\n/\* the horde: busca.*", "", a, flags=re.S) + js
open(os.path.join(B, "app.js"), "w", encoding="utf-8").write(a)
print("ok", len(cards), "fichas")
