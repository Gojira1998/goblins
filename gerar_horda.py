"""Gera a seção THE HORDE (ficha de cada goblin com @, imagem, esquadrão e episódio) dentro do index.html da página dos goblins,
com a busca por @ (campo no topo + campo na seção + link direto ?me=seu_arroba).

Uso:  py -3.11 gerar_horda.py
- Lê os episódios da lista EPISODIOS abaixo: producao/<pasta>/goblins/LISTA-goblins.json (+ grupos.json, se existir).
- Episódio novo = acrescentar uma linha em EPISODIOS (a pasta pode ainda nem existir; ela entra quando a lista aparecer).
- Imagem de cada ficha: assets/horda/NN.webp. Se não existir, o script cria a partir de <pasta>/assets/gob/NN.png (já recortado)
  ou recorta o fundo magenta de <pasta>/goblins/<arquivo> (precisa numpy e scipy: rodar com py -3.11).
  Goblin que ainda não foi desenhado entra com a ficha "being drawn" (a pessoa já acha o @ dela).
- Entrada com "evolui": true troca a imagem e a descrição de quem já tinha goblin (mantém o número antigo, marca "Evolved").
- Não publica nada. Publicar = bash ../publicar.sh c-goblins goblins (só com OK do João)."""
import json, html, re, os
B = os.path.dirname(os.path.abspath(__file__)); PROD = os.path.join(B, "..", "..", "producao")
EPISODIOS = [(3, "C-video3"), (4, "C-video4")]          # (número do episódio, pasta em producao/)
EP2 = ["@victor_automates", "@mcautomate", "@tajnyslipy", "@rinraroyl", "@anaar_net", "@stck.wrld"]   # os 6 do ep. 2 (estão na cena, sem ficha)
PAPEL = {1: "Squad leader", 2: "Big and strong", 11: "The Shadow, night watch chief", 12: "Night watch", 13: "Night watch", 14: "The lone goblin", 15: "Leads his own crew", 16: "Korg, red goblin warlord", 17: "The Manager"}
OFENSIVO = {"@rivertheretard": "RIVER"}                 # @ com palavra ofensiva: aparece com apelido, sem link

def limpa(s):
    s = re.sub(r"^(a|an|the)\s+", "", s.strip(), flags=re.I)
    s = re.sub(r"^[A-Z][\w.]*: ", "", s) if ":" in s[:22] else s
    s = re.sub(r"\b(?!(?:AI|RGB|LOW|CORTISOL)\b)([A-Z]{2,})\b", lambda m: m.group(1).lower(), s)   # caixa alta de prompt vira normal
    s = s.replace(" (the only text allowed)", "")
    return s[0].upper() + s[1:]

def recorta_magenta(path, alvo_h=300):
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mag = (r > 0.55) & (b > 0.55) & (g < 0.45) & (np.abs(r - b) < 0.35)
    lab, _ = ndimage.label(mag)
    borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(borda)) | ((r > 0.8) & (b > 0.8) & (g < 0.25))
    fg = ndimage.binary_opening(~bg, iterations=1)
    lab2, n = ndimage.label(fg)
    if n > 1:
        tam = ndimage.sum(fg, lab2, range(1, n + 1)); fg = np.isin(lab2, [i + 1 for i, s in enumerate(tam) if s > 400])
    bp = fg & ndimage.binary_dilation(~fg, iterations=2)
    rr = np.where(bp, np.minimum(r, g + 0.25), r); bb = np.where(bp, np.minimum(b, g + 0.25), b)
    rows = np.where(fg.any(1))[0]; cols = np.where(fg.any(0))[0]
    sl = (slice(rows.min(), rows.max() + 1), slice(cols.min(), cols.max() + 1))
    im = Image.fromarray((np.dstack([rr, g, bb, fg.astype(np.float32)])[sl] * 255).astype(np.uint8))
    s = alvo_h / im.height
    return im.resize((max(1, round(im.width * s)), alvo_h), Image.LANCZOS)

def imagem(n, pasta, arquivo):
    """Devolve o caminho relativo da webp (criando se der) ou None se o goblin ainda não foi desenhado."""
    dst = os.path.join(B, "assets", "horda", f"{n:02d}.webp")
    if os.path.exists(dst): return f"assets/horda/{n:02d}.webp"
    from PIL import Image
    cortado = os.path.join(PROD, pasta, "assets", "gob", f"{n:02d}.png")
    bruto = os.path.join(PROD, pasta, "goblins", arquivo)
    if os.path.exists(cortado): im = Image.open(cortado).convert("RGBA")
    elif os.path.exists(bruto): im = recorta_magenta(bruto)
    else: return None
    os.makedirs(os.path.dirname(dst), exist_ok=True); im.save(dst, "WEBP", quality=90, method=6)
    print("imagem nova:", os.path.basename(dst))
    return f"assets/horda/{n:02d}.webp"

# ---- junta os episódios
fichas, por_handle, ult_ep = [], {}, 3
for ep, pasta in EPISODIOS:
    lp = os.path.join(PROD, pasta, "goblins", "LISTA-goblins.json")
    if not os.path.exists(lp): continue
    ult_ep = ep
    L = json.load(open(lp, encoding="utf-8"))
    gp = os.path.join(PROD, pasta, "grupos.json"); squad = {}
    if os.path.exists(gp):
        for gr in json.load(open(gp, encoding="utf-8")).get("grupos", []):
            for x in gr["goblins"]: squad.setdefault(x["n"], gr["tarefa"])
    for x in L:
        h = x["handle"]; k = h.lower()
        img = imagem(x["n"], pasta, x["arquivo"])
        if k in por_handle:
            f = por_handle[k]
            if not x.get("evolui"): print("repetido, ignorado:", h); continue
            f.update(evol=ep, como=x["como"], papel=x.get("papel", f["papel"]))
            if img: f["img"] = img
            continue
        f = {"n": x["n"], "h": h, "ep": ep, "evol": None, "img": img, "como": x["como"],
             "sq": "THE LONE GOBLIN" if (ep == 3 and x["n"] == 14) else squad.get(x["n"], x.get("squad", "THE HORDE")),
             "papel": x.get("papel", PAPEL.get(x["n"], "") if ep == 3 else "")}
        por_handle[k] = f; fichas.append(f)

# mais novos primeiro (quem acabou de pedir acha o dele sem rolar), depois por número
fichas.sort(key=lambda f: (-(f["evol"] or f["ep"]), f["n"]))
total = len(fichas); prontos = sum(1 for f in fichas if f["img"]); novos = sum(1 for f in fichas if f["ep"] == ult_ep)

cards = []
for f in fichas:
    n, h = f["n"], f["h"]
    nome = OFENSIVO.get(h, h)
    link = "" if h in OFENSIVO else f' href="https://www.instagram.com/{h[1:]}/" target="_blank" rel="noopener"'
    tag = "a" if link else "span"
    cls = " lead" if (f["ep"] == 3 and n == 1) else " lone" if (f["ep"] == 3 and n == 14) else ""
    if f["ep"] == ult_ep or f["evol"] == ult_ep: cls += " new"
    selo = f'Evolved in ep. {f["evol"]}' if f["evol"] else f'Ep. {f["ep"]}'
    if f["img"]:
        hi = f'<img src="{f["img"]}" alt="{html.escape("Goblin of " + nome + ": " + f["como"])}" loading="lazy" width="130" height="150">'
    else:
        hi = '<span class="hwait">Being drawn.<br>Walks out next episode.</span>'
        cls += " wait"
    cards.append(
        f'<article class="hcard{cls}" data-h="{html.escape(h[1:].lower())}" data-q="{html.escape((nome + " " + f["sq"] + " " + f["como"]).lower())}">'
        f'<div class="hn">#{n:02d}</div><div class="hep">{selo}</div>'
        f'<div class="hi">{hi}</div>'
        f'<{tag} class="hh"{link}>{html.escape(nome)}</{tag}>'
        f'<p class="hs">{html.escape(f["sq"])}{(" · " + html.escape(f["papel"])) if f["papel"] else ""}</p>'
        f'<p class="hd">{html.escape(limpa(f["como"]))}</p></article>')

sec = f'''<!-- THE HORDE (gerado por gerar_horda.py) -->
<section class="sec" id="horde">
  <h2 class="h"><span>02</span> The horde</h2>
  <p class="lead">{total} of you asked to be a goblin, and every one gets a goblin dressed the way you asked. That many goblins don't fit in one video, so they all live here. Type your @ and find your card.</p>
  <label class="hsearch"><span>Find your @</span><input id="hq" type="search" placeholder="@yourname" autocomplete="off" autocapitalize="off" spellcheck="false"></label>
  <p class="hcount" id="hcount">{total} goblins · {novos} new in episode {ult_ep}</p>
  <p class="hnone" id="hnone" hidden></p>
  <div class="hgrid" id="hgrid">
{chr(10).join("    " + c for c in cards)}
  </div>
  <p class="note">Not a goblin yet? Comment the goblin you want to be on the latest episode and follow. You walk out of the next server.</p>
</section>
<!-- /THE HORDE -->
'''
css = '''
/* the horde (gerado por gerar_horda.py) */
.hsearch{display:flex;flex-direction:column;gap:6px;margin:18px 0 6px;font:600 14px var(--px);color:var(--lime)}
.hsearch input{font:500 16px 'Space Grotesk',sans-serif;padding:12px 14px;background:var(--bg2);color:var(--cream);border:2px solid #3a3150;border-radius:10px;outline:none;width:100%}
.hsearch input:focus{border-color:var(--fire)}
.hcount{font:600 13px var(--px);opacity:.7;margin:8px 0 14px}
.hnone{font-size:15px;line-height:1.5;background:var(--bg2);border-left:4px solid var(--fire);padding:12px 14px;margin:0 0 14px;border-radius:0 10px 10px 0}
.hgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media(min-width:560px){.hgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(min-width:760px){.hgrid{grid-template-columns:repeat(4,minmax(0,1fr))}}
.hcard{position:relative;background:var(--bg2);border:2px solid #2c2440;border-radius:12px;padding:10px 10px 12px;display:flex;flex-direction:column;gap:4px;min-width:0;scroll-margin-top:90px}
.hcard.lead{border-color:var(--fire)}.hcard.lone{border-color:#b3263a}
.hcard.new .hep{background:var(--fire);color:var(--ink)}
.hcard.hit{border-color:var(--lime);box-shadow:0 0 0 3px rgba(143,209,79,.35),0 18px 40px -18px rgba(143,209,79,.6)}
.hn{position:absolute;top:8px;left:10px;font:600 11px var(--px);color:var(--lime);opacity:.85}
.hep{position:absolute;top:6px;right:8px;font:700 10px/1 var(--px);padding:4px 6px;border-radius:6px;background:#2c2440;color:var(--cream)}
.hi{height:150px;display:flex;align-items:flex-end;justify-content:center;background:radial-gradient(ellipse at 50% 85%,rgba(56,224,200,.14),transparent 65%)}
.hi img{max-height:146px;max-width:100%;width:auto;image-rendering:pixelated}
.hwait{align-self:center;text-align:center;font:600 12px/1.4 var(--px);color:var(--cyan);opacity:.8;border:2px dashed #3a3150;border-radius:10px;padding:14px 8px}
.hh{font:700 14px/1.35 var(--px);color:var(--fire);text-decoration:none;overflow-wrap:anywhere;margin-top:4px}
a.hh:hover{text-decoration:underline}
.hs{font:600 11px/1.4 var(--px);color:var(--cyan)}
.hd{font-size:13px;line-height:1.4;opacity:.85}
.hcard[hidden]{display:none}
.findtop{display:flex;gap:8px;margin:14px 0 14px;max-width:460px;border:0;padding:0;background:none;box-shadow:none;border-radius:0}
.findtop input{flex:1;min-width:0;font:500 16px 'Space Grotesk',sans-serif;padding:13px 14px;border-radius:12px;border:2px solid #3a3150;background:rgba(18,13,28,.85);color:var(--cream);outline:none}
.findtop input:focus{border-color:var(--lime)}
.findtop button{font:700 15px/1 var(--px);padding:0 14px;white-space:nowrap;border:0;border-radius:12px;background:var(--lime);color:var(--ink);cursor:pointer;box-shadow:0 4px 0 #5d9a2c}
.findtop button:active{transform:translateY(4px);box-shadow:none}
'''
js = '''
/* the horde: busca por @ (gerado por gerar_horda.py) */
(function(){var q=document.getElementById('hq');if(!q)return;
var cs=[].slice.call(document.querySelectorAll('#hgrid .hcard')),out=document.getElementById('hcount'),none=document.getElementById('hnone'),base=out.textContent;
var EP2=__EP2__;
function norm(v){return (v||'').trim().toLowerCase().replace(/^@+/,'').replace(/^https?:\\/\\/(www\\.)?instagram\\.com\\//,'').replace(/[\\/?#].*$/,'');}
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
'''.replace("__EP2__", json.dumps([h[1:].lower() for h in EP2]))

h = open(os.path.join(B, "index.html"), encoding="utf-8").read()
h = re.sub(r"<!-- THE HORDE.*?<!-- /THE HORDE -->\n\n?", "", h, flags=re.S)
h = h.replace("<!-- 3. HUMAN BEHIND -->", sec + "\n<!-- 3. HUMAN BEHIND -->", 1)
assert 'id="horde"' in h
# campo "Find your goblin" no topo (hero): entra uma vez, fica entre os marcadores
topo = ('<!-- FIND TOP (gerado por gerar_horda.py) -->\n    <form class="findtop" id="findtop" role="search"><input type="search" placeholder="Type your @" '
        'aria-label="Your Instagram @" autocomplete="off" autocapitalize="off" spellcheck="false"><button type="submit">Find my goblin</button></form>\n    <!-- /FIND TOP -->\n')
h = re.sub(r"<!-- FIND TOP.*?<!-- /FIND TOP -->\n\s*", "", h, flags=re.S)
h = re.sub(r'(\s*)(<a class="btn" href="#join">)', lambda m: m.group(1) + topo + "    " + m.group(2), h, count=1)
assert 'id="findtop"' in h
open(os.path.join(B, "index.html"), "w", encoding="utf-8").write(h)
s = open(os.path.join(B, "style.css"), encoding="utf-8").read(); s = re.sub(r"\n/\* the horde \(gerado.*", "", s, flags=re.S) + css
open(os.path.join(B, "style.css"), "w", encoding="utf-8").write(s)
a = open(os.path.join(B, "app.js"), encoding="utf-8").read(); a = re.sub(r"\n/\* the horde: busca.*", "", a, flags=re.S) + js
open(os.path.join(B, "app.js"), "w", encoding="utf-8").write(a)
print("ok", total, "fichas,", prontos, "com imagem,", total - prontos, "sendo desenhadas,", novos, "novas no ep.", ult_ep)
