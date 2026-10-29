"""
Gera o site estático em docs/ (pasta que o GitHub Pages publica).

    python build.py

Dados da empresa: src/empresa.py   |   Conteúdo e MAPA DE FOTOS: src/dados.py
Visual: assets/css/cinema.css      |   Interações: assets/js/cinema.js
"""

import html
import json
import shutil
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from dados import (CATEGORIAS, HERO_CARTOES, HERO_FUNDO, PROJETOS,  # noqa: E402
                   SELO_ILUSTRATIVO, SERVICOS, SOBRE)
from empresa import EMPRESA as E, TRACKING as T  # noqa: E402

SAIDA = RAIZ / "docs"
VERSAO = date.today().strftime("%Y%m%d")
esc = html.escape

ICONES = {
    "fachada": '<path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-6h6v6M9 10h6"/>',
    "letra": '<path d="M4 20 10 4h4l6 16M7 13h10"/><path d="M2 20h20" opacity=".5"/>',
    "totem": '<rect x="8" y="2" width="8" height="14" rx="1"/><path d="M12 16v6M8 22h8M10 6h4M10 9h4"/>',
    "estrutura": '<path d="M3 21 12 3l9 18M6 15h12M8 11l8 10M16 11 8 21"/>',
    "outdoor": '<rect x="2" y="4" width="20" height="11" rx="1"/><path d="M7 15v6M17 15v6M5 21h4M15 21h4"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "zap": '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Z"/><path d="M8.5 7.5c.3 2.6 2.6 6.3 6.4 7.6l1.6-1.6-2.1-1.3-1 .9c-1.2-.5-2.6-1.9-3-3l.9-1-1.3-2.1Z"/>',
    "pin": '<path d="M12 22s7-6.3 7-12a7 7 0 0 0-14 0c0 5.7 7 12 7 12Z"/><circle cx="12" cy="10" r="2.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "insta": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "esq": '<path d="m15 18-6-6 6-6"/>',
    "dir": '<path d="m9 18 6-6-6-6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def ico(nome: str) -> str:
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONES[nome]}</svg>')


WHATS_SVG = ('<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 '
             '6.9L3 29l6.5-2c1.9 1 4.1 1.6 6.5 1.6 7.2 0 13-5.7 13-12.8S23.2 3 16 3Zm0 23.3c-2.1 0-4.1-.6-5.8-1.6l-.4-.2-3.9 1.2 '
             '1.2-3.8-.3-.4a10.4 10.4 0 0 1-1.7-5.7C5.1 10 10 5.3 16 5.3S26.9 10 26.9 15.8 22 26.3 16 26.3Zm6-7.8c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2'
             '-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.4'
             'c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.7s1.2 3.1 1.4 3.4c.2.2 2.4 3.6 5.7 5 .8.4 1.4.6 1.9.7.8.3 1.5.2 2.1.1.6-.1 '
             '1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4Z"/></svg>')


def whats_link(texto: str) -> str:
    from urllib.parse import quote
    return f"{E.whatsapp_url}?text={quote(texto)}"


MSG_PADRAO = "Olá! Vim pelo site da Só Fachadas e quero um orçamento."
anos = date.today().year - E.ano_inicio


def head() -> str:
    titulo = "Só Fachadas MT | Fachadas em ACM, Letras Caixa e Letreiros em Cuiabá – MT"
    desc = ("Fachadas em ACM, letras caixa com LED, totens e estruturas metálicas em Cuiabá e região. "
            "Projeto, fabricação e instalação. Peça seu orçamento pelo WhatsApp.")
    og_img = E.site_url + "assets/img/" + HERO_FUNDO.arquivo + ".jpg"
    ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": E.nome,
        "description": desc,
        "image": og_img,
        "logo": E.site_url + "assets/img/logo.jpg",
        "url": E.site_url,
        "telephone": "+" + E.whatsapp_e164,
        "email": E.email,
        "address": {"@type": "PostalAddress", "streetAddress": E.endereco, "addressLocality": E.cidade,
                    "addressRegion": E.estado, "postalCode": E.cep, "addressCountry": "BR"},
        "areaServed": [E.cidade, "Várzea Grande", "Mato Grosso"],
        "sameAs": [E.instagram_url, E.facebook_url],
        "foundingDate": str(E.ano_inicio),
    }
    cfg = {"whatsapp": E.whatsapp_e164}
    pixel = ""
    if T.meta_pixel_id:
        pixel += (f"<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};"
                  f"if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;"
                  f"s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
                  f"fbq('init','{T.meta_pixel_id}');fbq('track','PageView');</script>")
    if T.google_ads_id:
        pixel += (f'<script async src="https://www.googletagmanager.com/gtag/js?id={T.google_ads_id}"></script>'
                  f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{T.google_ads_id}');</script>")
    rastreio = f"""<script>
window.SF_CONFIG={json.dumps(cfg)};
/* UTM: script autocontido, roda antes de tudo para nao perder a origem */
(function(){{try{{var p=new URLSearchParams(location.search),u={{}};
["utm_source","utm_medium","utm_campaign","utm_content","utm_term","gclid","fbclid"].forEach(function(k){{if(p.get(k))u[k]=p.get(k)}});
window.__SF_UTM=u;if(Object.keys(u).length)sessionStorage.setItem("sf_utm",JSON.stringify(u));}}catch(e){{}}}})();
window.rastrearConversao=function(servico){{
  try{{if(window.fbq)fbq('track','Lead',{{content_name:servico}});}}catch(e){{}}
  try{{if(window.gtag&&{json.dumps(bool(T.google_ads_id and T.google_ads_label))})gtag('event','conversion',{{send_to:{json.dumps(T.google_ads_id + '/' + T.google_ads_label)}}});}}catch(e){{}}
}};
window.rastrearContato=function(){{try{{if(window.fbq)fbq('track','Contact');}}catch(e){{}}}};
</script>"""
    return f"""<!doctype html>
<html lang="pt-BR" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0a0a0b">
<link rel="canonical" href="{E.site_url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:url" content="{E.site_url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/logo-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap">
<link rel="preload" as="image" href="assets/img/{HERO_FUNDO.arquivo}.jpg">
<link rel="stylesheet" href="assets/css/cinema.css?v={VERSAO}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{rastreio}
{pixel}
</head>"""


def header() -> str:
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="logo" href="#topo" aria-label="{esc(E.nome)} — início"><img class="logo-sf" src="assets/img/logo-180.png" alt="" width="40" height="40"><span><b>SÓ <span class="gold-text">FACHADAS</span></b><small>{esc(E.subtitulo)}</small></span></a>
    <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu">{ico("menu")}</button>
    <nav class="main-nav" id="menu" aria-label="Principal">
      <a href="#servicos">Serviços</a>
      <a href="#projetos">Projetos</a>
      <a href="#sobre">Sobre</a>
      <a href="#orcamento">Orçamento</a>
      <a class="btn btn-gold" href="{whats_link(MSG_PADRAO)}" target="_blank" rel="noopener">{WHATS_SVG}WhatsApp</a>
    </nav>
  </div>
</header>"""


def hero() -> str:
    palavras = "Fachadas que fazem sua empresa ser vista.".split()
    titulo_hero = " ".join(
        f'<span class="w{" gold-text" if i == len(palavras) - 1 else ""}">{esc(p)}</span>' for i, p in enumerate(palavras))
    cartoes = "".join(
        f'<div class="hero-card" data-depth="{c.profundidade}"><img src="assets/img/{c.arquivo}.jpg" alt="{esc(c.alt)}" width="760" height="570"></div>'
        for c in HERO_CARTOES)
    return f"""<section class="hero" id="topo" aria-label="Apresentação">
  <div class="hero-bg" data-depth="{HERO_FUNDO.profundidade}"><img src="assets/img/{HERO_FUNDO.arquivo}.jpg" alt="{esc(HERO_FUNDO.alt)}" width="1920" height="1080" fetchpriority="high"></div>
  <div class="wrap hero-inner">
    <div>
      <p class="eyebrow">Comunicação visual em {esc(E.cidade)}–{esc(E.estado)}</p>
      <h1>{titulo_hero}</h1>
      <p class="hero-sub">Fachadas em ACM, letras caixa com LED, totens e estruturas metálicas. Do projeto à instalação, com equipe própria.</p>
      <div class="hero-ctas">
        <a class="btn btn-gold" href="{whats_link(MSG_PADRAO)}" target="_blank" rel="noopener">{WHATS_SVG}Pedir orçamento no WhatsApp</a>
        <a class="btn btn-ghost" href="#projetos">Ver projetos</a>
      </div>
      <div class="proof">
        <div><strong>{anos} anos</strong><span>no mercado</span></div>
        <div><strong>Equipe própria</strong><span>projeto à instalação</span></div>
        <div><strong>{esc(E.cidade)}</strong><span>e região</span></div>
      </div>
    </div>
    <div class="hero-cards" aria-hidden="true">{cartoes}</div>
  </div>
</section>"""


def servicos() -> str:
    cards = "".join(f"""<a class="card lightcard reveal" href="#orcamento" data-servico="{s.slug}">
        <span class="ico">{ico(s.icone)}</span><h3>{esc(s.titulo)}</h3><p>{esc(s.descricao)}</p><span class="mais">Pedir orçamento →</span></a>"""
                    for s in SERVICOS)
    return f"""<section class="section" id="servicos" aria-label="Serviços">
  <div class="wrap">
    <div class="section-head reveal"><p class="eyebrow">O que fazemos</p><h2>Sua marca, do tamanho que ela merece</h2>
      <p>Tudo que a fachada da sua empresa precisa, feito por quem fabrica e instala.</p></div>
    <div class="grid-servicos">{cards}</div>
  </div>
</section>"""


def portfolio() -> str:
    filtros = '<button class="filtro" type="button" data-filtro="todos" aria-pressed="true">Todos</button>' + "".join(
        f'<button class="filtro" type="button" data-filtro="{c.slug}" aria-pressed="false">{esc(c.nome)}</button>' for c in CATEGORIAS)
    selo = '<span class="selo">Imagem ilustrativa</span>' if SELO_ILUSTRATIVO else ""
    itens = "".join(f"""<a class="pf-item reveal" href="assets/img/{p.arquivo}.jpg" data-cat="{p.categoria}" data-titulo="{esc(p.titulo)}" data-legenda="{esc(p.legenda)}">
        <img src="assets/img/{p.arquivo}-mini.jpg" alt="{esc(p.titulo)}: {esc(p.legenda)}" loading="lazy" width="760" height="570">{selo}
        <span class="pf-cap"><strong>{esc(p.titulo)}</strong><span>{esc(p.legenda)}</span></span></a>""" for p in PROJETOS)
    return f"""<section class="section alt" id="projetos" aria-label="Projetos">
  <div class="wrap">
    <div class="section-head reveal"><p class="eyebrow">Obras entregues</p><h2>Projetos que já estão na rua</h2>
      <p>Algumas fachadas que fizemos em {esc(E.cidade)} e região. Toque para ampliar.</p></div>
    <div class="filtros" role="group" aria-label="Filtrar projetos">{filtros}</div>
    <div class="grid-pf">{itens}</div>
  </div>
</section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Foto do projeto" aria-hidden="true">
  <div class="lightbox-backdrop"></div>
  <button class="lb-btn lb-fechar" type="button" aria-label="Fechar">{ico("x")}</button>
  <button class="lb-btn lb-ant" type="button" aria-label="Foto anterior">{ico("esq")}</button>
  <button class="lb-btn lb-prox" type="button" aria-label="Próxima foto">{ico("dir")}</button>
  <figure class="lightbox-fig"><img src="" alt=""><figcaption><strong class="lb-tit"></strong><span class="lb-leg"></span></figcaption></figure>
  <span class="lb-pos" aria-live="polite"></span>
</div>"""


def sobre() -> str:
    fotos = "".join(f'<figure data-depth="{f.profundidade}"><img src="assets/img/{f.arquivo}-mini.jpg" alt="{esc(f.alt)}" loading="lazy" width="760" height="570"></figure>'
                    for f in SOBRE)
    itens = ["Visita técnica e medição no local", "Projeto visual antes de fabricar",
             "Fabricação própria em ACM e metal", "Instalação com equipe e equipamentos próprios"]
    lis = "".join(f"<li>{ico('check')}<span>{esc(t)}</span></li>" for t in itens)
    return f"""<section class="section" id="sobre" aria-label="Sobre a empresa">
  <div class="wrap sobre-grid">
    <div class="sobre-txt reveal">
      <p class="eyebrow">Quem somos</p>
      <h2>Feito por quem sobe no andaime</h2>
      <p style="margin-top:18px">A {esc(E.nome)} nasceu em {E.ano_inicio}, em {esc(E.cidade)}, para entregar fachadas com acabamento de marca grande para empresas de todos os tamanhos.</p>
      <p>Cuidamos de tudo: a ideia, o projeto, a fabricação e a instalação. Você fala com uma empresa só, do primeiro desenho até a luz acesa.</p>
      <ul class="lista-check">{lis}</ul>
    </div>
    <div class="sobre-fotos reveal">{fotos}</div>
  </div>
</section>
<section class="section alt" aria-label="Como funciona">
  <div class="wrap">
    <div class="section-head reveal"><p class="eyebrow">Como funciona</p><h2>Do primeiro contato à fachada pronta</h2></div>
    <div class="passos">
      <div class="passo reveal"><h3>Contato</h3><p>Você chama no WhatsApp e conta o que precisa.</p></div>
      <div class="passo reveal"><h3>Visita e projeto</h3><p>Medimos o local e mostramos como vai ficar.</p></div>
      <div class="passo reveal"><h3>Fabricação</h3><p>Produzimos as peças em ACM, metal e LED.</p></div>
      <div class="passo reveal"><h3>Instalação</h3><p>Nossa equipe instala e entrega pronto.</p></div>
    </div>
  </div>
</section>"""


def avaliacoes() -> str:
    return f"""<section class="section" aria-label="Avaliações">
  <div class="wrap">
    <div class="avaliacao reveal">
      <div><div class="estrelas" aria-hidden="true">★★★★★</div><h2>Já é nosso cliente?</h2>
        <p>Conte como foi a sua experiência no Google. Sua avaliação ajuda outras empresas de {esc(E.cidade)} a nos encontrar.</p></div>
      <a class="btn btn-ghost" href="{E.google_avaliacao_url}" target="_blank" rel="noopener">Avaliar no Google</a>
    </div>
  </div>
</section>"""


def orcamento() -> str:
    opcoes = "".join(f'<option value="{s.slug}">{esc(s.titulo)}</option>' for s in SERVICOS) + '<option value="outro">Outro / não sei ainda</option>'
    mapa = "https://www.google.com/maps/search/?api=1&query=" + "+".join(f"{E.nome} {E.endereco} {E.cidade}".split())
    return f"""<section class="section alt" id="orcamento" aria-label="Pedir orçamento">
  <div class="wrap orc-grid">
    <div class="orc-info reveal">
      <p class="eyebrow">Orçamento</p>
      <h2 style="font-size:clamp(34px,5vw,58px)">Vamos tirar sua fachada do papel?</h2>
      <p>Preencha em 30 segundos e a conversa já abre no WhatsApp com tudo explicado. Sem compromisso.</p>
      <ul class="contatos">
        <li>{ico("zap")}<a href="{whats_link(MSG_PADRAO)}" target="_blank" rel="noopener">{esc(E.telefone_exibicao)}</a></li>
        <li>{ico("pin")}<a href="{mapa}" target="_blank" rel="noopener">{esc(E.endereco)}, {esc(E.cidade)}–{esc(E.estado)}</a></li>
        <li>{ico("mail")}<a href="mailto:{E.email}">{esc(E.email)}</a></li>
        <li>{ico("clock")}<span>{esc(E.horario)}</span></li>
      </ul>
    </div>
    <form class="form reveal" id="form-orcamento" action="{E.whatsapp_url}" method="get" novalidate>
      <div class="campo"><label for="nome">Seu nome</label><input id="nome" name="nome" autocomplete="name" required></div>
      <div class="campo"><label for="telefone">WhatsApp com DDD</label><input id="telefone" name="telefone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(65) 9 0000-0000" required></div>
      <div class="campo"><label for="servico">Serviço</label>
        <select id="servico" name="servico" required><option value="">Escolha uma opção</option>{opcoes}</select></div>
      <div class="campo"><label for="mensagem">Conte um pouco (opcional)</label><textarea id="mensagem" name="mensagem" placeholder="Ex.: fachada de loja com 8 m de largura, quero letras iluminadas"></textarea></div>
      <p class="form-erro" role="alert"></p>
      <button class="btn btn-gold" type="submit">{WHATS_SVG}Enviar pelo WhatsApp</button>
      <p class="form-nota">Você será levado ao WhatsApp com a mensagem pronta.</p>
    </form>
  </div>
</section>"""


def footer() -> str:
    ano = date.today().year
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div><a class="logo" href="#topo"><b>SÓ <span class="gold-text">FACHADAS</span></b><small>{esc(E.subtitulo)}</small></a>
        <p style="margin-top:14px;max-width:36ch">Fachadas em ACM, letras caixa, totens e estruturas metálicas em {esc(E.cidade)} e região.</p></div>
      <div><h3>Contato</h3><ul>
        <li><a href="{whats_link(MSG_PADRAO)}" target="_blank" rel="noopener">WhatsApp {esc(E.telefone_exibicao)}</a></li>
        <li><a href="mailto:{E.email}">{esc(E.email)}</a></li>
        <li>{esc(E.endereco)}<br>{esc(E.cidade)}–{esc(E.estado)}, {esc(E.cep)}</li></ul></div>
      <div><h3>Redes</h3><ul>
        <li><a href="{E.instagram_url}" target="_blank" rel="noopener">Instagram @{esc(E.instagram_user)}</a></li>
        <li><a href="{E.facebook_url}" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="{E.google_avaliacao_url}" target="_blank" rel="noopener">Avaliar no Google</a></li></ul></div>
    </div>
    <p class="copy">© {ano} {esc(E.nome)} · CNPJ {esc(E.cnpj)}</p>
  </div>
</footer>
<a class="whats-float" href="{whats_link(MSG_PADRAO)}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">{WHATS_SVG}</a>"""


def main() -> None:
    # limpa docs/ mas preserva docs/correa/ (site da Correa Metalúrgica, gerado por correa_src/build.py)
    if SAIDA.exists():
        for item in SAIDA.iterdir():
            if item.name == "correa":
                continue
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    (SAIDA / "assets").mkdir(parents=True)
    for pasta in ("css", "js", "img"):
        shutil.copytree(RAIZ / "assets" / pasta, SAIDA / "assets" / pasta)
    corpo = "\n".join([header(), "<main>", hero(), servicos(), portfolio(), sobre(), avaliacoes(), orcamento(), "</main>", footer()])
    pagina = (head() + "\n<body>\n" + corpo +
              f'\n<script src="assets/js/cinema.js?v={VERSAO}" defer></script>\n</body>\n</html>\n')
    (SAIDA / "index.html").write_text(pagina, encoding="utf-8")
    (SAIDA / ".nojekyll").write_text("")
    (SAIDA / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {E.site_url}sitemap.xml\nSitemap: {E.site_url}correa/sitemap.xml\n")
    (SAIDA / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<url><loc>{E.site_url}</loc><lastmod>{date.today().isoformat()}</lastmod></url></urlset>\n")
    print(f"ok: {SAIDA / 'index.html'}  ({len(pagina) // 1024} KB)")


if __name__ == "__main__":
    main()
