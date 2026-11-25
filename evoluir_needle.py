"""25/11: needle_ss_ttt reclamou 'Still not updated'. Troca a ficha #48 do site pelo goblin evoluído do ep. 10 (Light Bringer)."""
import os, re, runpy, sys
B = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(B, "..", "..", "producao", "C-video11", "goblins", "48e-needle_ss_ttt.png")
DST = os.path.join(B, "assets", "horda", "48e.webp")
src = open(os.path.join(B, "gerar_horda.py"), encoding="utf-8").read()
ns = {}
exec(src[src.index("def recorta_magenta"):src.index("def imagem")], {"__name__": "x"}, ns)
im = ns["recorta_magenta"](PNG)
im.save(DST, "WEBP", quality=90, method=6)
print("imagem:", DST, im.size)
DESC = "The Light Bringer: albino goblin in full flowing white robes with gold trim, holding glowing needles of light, a soft white halo behind him"
idx = os.path.join(B, "index.html")
h = open(idx, encoding="utf-8").read()
velho = re.search(r'<article class="hcard" data-h="needle_ss_ttt".*?</article>', h).group(0)
novo = ('<article class="hcard" data-h="needle_ss_ttt" data-q="@needle_ss_ttt light bringer ' + DESC.lower() + '">'
        '<div class="hn">#48</div><div class="hep">Evolved in ep. 10</div><div class="hi"><img src="assets/horda/48e.webp" alt="Goblin of @needle_ss_ttt: ' + DESC + '" loading="lazy" width="130" height="150"></div>'
        '<a class="hh" href="https://www.instagram.com/needle_ss_ttt/" target="_blank" rel="noopener">@needle_ss_ttt</a><p class="hs">LIGHT BRINGER</p><p class="hd">' + DESC + '</p></article>')
h = h.replace(velho, novo)
open(idx, "w", encoding="utf-8").write(h)
print("ficha #48 trocada:", h.count('assets/horda/48e.webp') == 1)
