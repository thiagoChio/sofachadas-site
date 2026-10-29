"""
Processa as fotos reais das obras (roda offline, não em produção).

Para cada foto:
  1. aplica o RECORTE em frações (x0, y0, x1, y1) para tirar molduras/barras de marketing;
  2. gera a versão grande (lightbox/hero) e a miniatura (grade do portfólio), já otimizadas.

Uso:  python scripts/processa_fotos.py
Saída: assets/img/
"""

from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "fotos_originais"
DESTINO = RAIZ / "assets" / "img"

# ======================================================================
#  RECORTES  —  (x0, y0, x1, y1) em fração da imagem original.
#  (0, 0, 1, 1) = foto inteira. Use para remover molduras de marketing.
# ======================================================================
RECORTES = {
    "cobertura-frente": (0.0, 0.10, 1.0, 0.60),
    "cobertura-policarbonato": (0.0, 0.0, 1.0, 0.62),
    "amaggi-letra-caixa-led": (0.0, 0.166, 1.0, 0.834),   # tira barras preta/logo
    "peacook-letra-caixa-backlight": (0.0, 0.125, 1.0, 0.83),
}

GRANDE = 1600      # lado maior da versão grande
MINI = 760         # lado maior da miniatura
PROPORCAO_MINI = 4 / 3

# fotos usadas como fundo do hero ganham uma versão larga 16:9
HERO_LARGO = {"cobertura-trelica", "portao"}


def corta_proporcao(im: Image.Image, proporcao: float) -> Image.Image:
    w, h = im.size
    if w / h > proporcao:
        nw = int(h * proporcao)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w / proporcao)
    y = (h - nh) // 2
    return im.crop((0, y, w, y + nh))


def salva(im: Image.Image, caminho: Path, lado: int, qualidade: int = 78) -> None:
    im = im.copy()
    im.thumbnail((lado, lado), Image.LANCZOS)
    im.save(caminho, "JPEG", quality=qualidade, optimize=True, progressive=True)


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    for foto in sorted(p for p in ORIGEM.glob("*.jpg") if not p.name.startswith("_")):
        nome = foto.stem
        im = ImageOps.exif_transpose(Image.open(foto).convert("RGB"))
        x0, y0, x1, y1 = RECORTES.get(nome, (0, 0, 1, 1))
        w, h = im.size
        im = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))

        salva(im, DESTINO / f"{nome}.jpg", GRANDE)
        salva(corta_proporcao(im, PROPORCAO_MINI), DESTINO / f"{nome}-mini.jpg", MINI, 74)
        if nome in HERO_LARGO:
            salva(corta_proporcao(im, 16 / 9), DESTINO / f"{nome}-hero.jpg", 1920, 74)
        print("ok", nome)


if __name__ == "__main__":
    main()
