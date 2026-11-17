"""Põe (ou repõe) a loja dos goblins no index.html: CSS, scripts e a seção "Take your goblin home".
Pode rodar quantas vezes quiser (troca o bloco entre os marcadores <!-- SHOP --> e <!-- /SHOP -->).
Rodar depois do gerar_horda.py se algum dia o index.html for refeito do zero.  Uso: python instalar_loja.py"""
import os, re
B = os.path.dirname(os.path.abspath(__file__))
V = "20261117"
SEC = '''<!-- SHOP (instalar_loja.py) -->
<section class="sec shop" id="shop">
  <h2 class="h"><span>&#9733;</span> Take your goblin home</h2>
  <p class="lead">Your goblin is free and it stays free. If you want it on your phone, here are two extras made from your own goblin, with your @ on it.</p>
  <img class="shop-banner" src="assets/shop/banner.webp" alt="A phone wallpaper and a round profile picture made from a goblin, next to a line of goblins from the horde" width="1440" height="810" loading="lazy">
  <div class="offers">
    <article class="offer hd">
      <div class="ofig"><img src="assets/shop/wallpaper.webp" alt="Sample phone wallpaper: a goblin with the name @yourname under it" width="300" height="533" loading="lazy"><img class="ava" src="assets/shop/avatar.webp" alt="Sample round profile picture with @yourname" width="240" height="240" loading="lazy"></div>
      <h3>Your Goblin HD <b>$3</b></h3>
      <ul><li>Phone wallpaper, 1080 x 1920</li><li>Profile picture, 1080 x 1080</li><li>Your goblin as a clean PNG, no background</li><li>Your @ on it, big and glowing</li></ul>
    </article>
    <article class="offer an">
      <div class="ofig"><img src="assets/shop/animated.webp" alt="Sample animated goblin loop: the goblin breathes, embers rise and the name glows" width="300" height="533" loading="lazy"></div>
      <h3>Animated Goblin <b>$7</b></h3>
      <ul><li>A short loop of your goblin for your story</li><li>It breathes, embers rise, your @ glows</li><li>MP4 in story size and square size</li><li>Includes everything in the HD pack</li></ul>
    </article>
  </div>
  <ol class="steps">
    <li>Find your @ in the horde above.</li>
    <li>Tap the button on your card. We copy your @ for you.</li>
    <li>Pay on Ko-fi and paste your @ when it asks.</li>
    <li>We send your files by email within 24 hours.</li>
  </ol>
  <p class="shop-soon" data-shop-soon>The shop opens soon. Find your goblin now, the buttons show up on your card.</p>
  <div class="shop-cta"><a class="btn" href="#horde">Find my goblin first <i aria-hidden="true">&#9654;</i></a></div>
  <p class="note">Only goblins that are already drawn. Goblins based on someone else's character stay free and are not for sale. Wrong goblin or a typo in your @? Send us a DM within 7 days and we fix it or refund you.</p>
</section>
<!-- /SHOP -->
'''

p = os.path.join(B, "index.html")
h = open(p, encoding="utf-8").read()
h = re.sub(r"<!-- SHOP \(instalar_loja\.py\) -->.*?<!-- /SHOP -->\n\n?", "", h, flags=re.S)
assert "<!-- 4. PAINS -->" in h, "marcador <!-- 4. PAINS --> sumiu do index.html"
h = h.replace("<!-- 4. PAINS -->", SEC + "\n<!-- 4. PAINS -->", 1)
h = re.sub(r'\s*<link rel="stylesheet" href="shop\.css[^"]*">', "", h)
h = h.replace('<link rel="stylesheet" href="style.css">', f'<link rel="stylesheet" href="style.css">\n<link rel="stylesheet" href="shop.css?v={V}">', 1)
h = re.sub(r'<script src="(config|shop)\.js[^"]*"></script>\n?', "", h)
h = re.sub(r'(<script src="app\.js[^"]*"></script>\n)', lambda m: m.group(1) + f'<script src="config.js?v={V}"></script>\n<script src="shop.js?v={V}"></script>\n', h, count=1)
assert 'shop.js' in h and 'shop.css' in h and 'id="shop"' in h
open(p, "w", encoding="utf-8").write(h)
print("loja instalada no index.html")
