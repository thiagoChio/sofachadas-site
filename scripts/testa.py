"""
Testes do site com Playwright. Uso: python scripts/testa.py  (sobe um servidor local em docs/)
Gera prints em scripts/prints/ e falha (exit 1) se algo quebrar.
"""

import functools
import http.server
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
PRINTS = Path(__file__).resolve().parent / "prints"
PRINTS.mkdir(exist_ok=True)
PORTA = 8765
URL = f"http://127.0.0.1:{PORTA}/"
falhas = []


def ok(cond, msg):
    print(("  ok  " if cond else "  FALHA ") + msg)
    if not cond:
        falhas.append(msg)


def servidor():
    class Quieto(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    h = functools.partial(Quieto, directory=str(RAIZ / "docs"))
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    s = http.server.ThreadingHTTPServer(("127.0.0.1", PORTA), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def testa_viewport(b, w, h, nome, reduz=False, js=True):
    print(f"[{nome}] {w}x{h}{' reduced-motion' if reduz else ''}{' SEM JS' if not js else ''}")
    ctx = b.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce" if reduz else "no-preference",
                        java_script_enabled=js, has_touch=w < 800, is_mobile=w < 800)
    pg = ctx.new_page()
    erros = []
    pg.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: erros.append(str(e)))
    pg.route("**/fonts.g*/**", lambda r: r.abort())  # sem internet aqui: ignora fontes externas
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(1200)
    erros = [e for e in erros if "fonts.g" not in e and "net::ERR_FAILED" not in e]
    ok(not erros, f"sem erros no console {erros[:3]}")

    larg = pg.evaluate("document.documentElement.scrollWidth")
    ok(larg <= w, f"sem scroll horizontal (scrollWidth={larg})")

    cta = pg.locator(".hero-ctas .btn-gold").bounding_box()
    hero_h = pg.locator(".hero").bounding_box()["height"]
    if w <= 760:
        ok(cta["y"] + cta["height"] <= h, f"CTA do hero acima da dobra (termina em {cta['y'] + cta['height']:.0f}px)")
        ok(hero_h <= 980, f"hero <= 980px ({hero_h:.0f})")
        alvos = pg.evaluate("""[...document.querySelectorAll('a.btn,button,.filtro,.menu-toggle,.whats-float')]
            .filter(e=>e.offsetParent).map(e=>{const r=e.getBoundingClientRect();return [r.width,r.height,e.className]})
            .filter(([w,h])=>w<44||h<44)""")
        ok(not alvos, f"alvos de toque >= 44px {alvos[:3]}")
        fs = pg.evaluate("[...document.querySelectorAll('input,select,textarea')].map(e=>parseFloat(getComputedStyle(e).fontSize))")
        ok(min(fs) >= 16, f"inputs com fonte >= 16px {fs}")
    pg.screenshot(path=str(PRINTS / f"{nome}-topo.png"))
    for _ in range(40):  # rola a página para carregar fotos e disparar os reveals
        pg.mouse.wheel(0, 500)
        pg.wait_for_timeout(60)
    pg.wait_for_timeout(1200)
    pg.screenshot(path=str(PRINTS / f"{nome}-inteiro.png"), full_page=True)
    pg.evaluate("window.scrollTo(0,0)")

    if js:
        # todas as seções visíveis depois de pular por âncora
        pg.goto(URL + "#orcamento")
        pg.wait_for_timeout(900)
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(900)
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(900)
        invis = pg.evaluate("[...document.querySelectorAll('.reveal')].filter(e=>getComputedStyle(e).opacity<0.5).length")
        ok(invis == 0, f"nenhuma seção invisível após saltos ({invis})")

        if w <= 760:
            pg.click(".menu-toggle")
            pg.wait_for_timeout(400)
            pg.click(".main-nav a[href='#projetos']")
            pg.wait_for_timeout(900)
            ok(not pg.evaluate("document.documentElement.classList.contains('nav-aberto')"), "menu mobile abre, link clica e fecha")

        # filtros
        for f in pg.locator(".filtro").all():
            f.scroll_into_view_if_needed()
            f.click()
            pg.wait_for_timeout(150)
            n = pg.evaluate("[...document.querySelectorAll('.pf-item')].filter(e=>!e.hidden).length")
            ok(n > 0, f"filtro '{f.inner_text()}' mostra {n} projeto(s)")
        pg.locator(".filtro").first.click()

        # lightbox
        pg.locator(".pf-item").nth(1).click()
        pg.wait_for_timeout(300)
        ok(pg.locator(".lightbox.aberto").count() == 1, "lightbox abre")
        pos1 = pg.inner_text(".lb-pos")
        pg.click(".lb-prox")
        pos2 = pg.inner_text(".lb-pos")
        ok(pos1 != pos2 and pg.locator(".lightbox.aberto").count() == 1, f"seta avança sem fechar ({pos1} -> {pos2})")
        pg.screenshot(path=str(PRINTS / f"{nome}-lightbox.png"))
        pg.keyboard.press("ArrowLeft")
        ok(pg.inner_text(".lb-pos") == pos1, "tecla ← volta")
        pg.keyboard.press("Escape")
        ok(pg.locator(".lightbox.aberto").count() == 0, "Esc fecha")

        # formulário -> WhatsApp (com UTM)
        pg.goto(URL + "?utm_source=instagram&utm_medium=bio&utm_campaign=teste")
        pg.wait_for_timeout(500)
        pg.click("[data-servico='totens']")
        pg.wait_for_timeout(600)
        ok(pg.input_value("#servico") == "totens", "card de serviço pré-seleciona o orçamento")
        pg.click("#form-orcamento button[type=submit]")
        ok("Preencha" in pg.inner_text(".form-erro"), "valida formulário vazio")
        pg.fill("#nome", "Teste Silva")
        pg.fill("#telefone", "(65) 99999-0000")
        pg.fill("#mensagem", "Fachada de 6 m")
        destino = {}
        pg.route("https://wa.me/**", lambda r: (destino.setdefault("url", r.request.url), r.fulfill(body="ok")))
        pg.click("#form-orcamento button[type=submit]")
        pg.wait_for_timeout(800)
        u = destino.get("url", "")
        from urllib.parse import unquote
        ok(u.startswith("https://wa.me/5565992764410?text="), f"redireciona para o WhatsApp certo")
        ok("Teste Silva" in unquote(u) and "Totens" in unquote(u) and "instagram" in unquote(u),
           "mensagem traz nome, serviço e origem UTM")
    ctx.close()


def main():
    s = servidor()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, h, n in [(360, 740, "360"), (390, 844, "390"), (414, 896, "414"), (768, 1024, "768"), (1440, 900, "1440")]:
            testa_viewport(b, w, h, n)
        testa_viewport(b, 390, 844, "390-reduz", reduz=True)
        testa_viewport(b, 390, 844, "390-semjs", js=False)
        b.close()
    s.shutdown()
    print("\nFALHAS:" if falhas else "\nTUDO OK", *falhas, sep="\n - ")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
