"""
Conteúdo do site: serviços, MAPA DE FOTOS do portfólio, do hero e do sobre.
Para trocar uma foto, troque o arquivo aqui (o arquivo precisa existir em assets/img/).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Servico:
    slug: str
    titulo: str
    descricao: str
    icone: str  # nome do ícone SVG em build.py


SERVICOS = [
    Servico("acm", "Fachadas em ACM",
            "Revestimento em alumínio composto: acabamento limpo, resistente ao sol de Cuiabá e com cara de marca grande.",
            "fachada"),
    Servico("letras", "Letras caixa e LED",
            "Letras em ACM, aço ou acrílico, com iluminação frontal ou backlight. Sua marca aparece de dia e brilha à noite.",
            "letra"),
    Servico("totens", "Totens e sinalização",
            "Totens de entrada, placas e sinalização que guiam o cliente até a sua porta.",
            "totem"),
    Servico("estruturas", "Estruturas metálicas",
            "Estrutura própria para fachadas, painéis e coberturas, fabricada e montada pela nossa equipe.",
            "estrutura"),
    Servico("outdoor", "Mídia exterior e outdoor",
            "Painéis e outdoors para quem quer ser visto de longe, no trânsito e na estrada.",
            "outdoor"),
]


@dataclass(frozen=True)
class Categoria:
    slug: str
    nome: str


TODAS_CATEGORIAS = [
    Categoria("letras", "Letras caixa e LED"),
    Categoria("acm", "Fachadas em ACM"),
    Categoria("totens", "Totens"),
    Categoria("estruturas", "Estruturas metálicas"),
    Categoria("outdoor", "Outdoor"),
]


# ======================================================================
#  MAPA DE FOTOS — PORTFÓLIO
#  arquivo = nome em assets/img/ (sem .jpg). A miniatura é <arquivo>-mini.jpg
# ======================================================================
SELO_ILUSTRATIVO = False   # True = estampa "imagem ilustrativa" (só para fotos que não são obras reais)


@dataclass(frozen=True)
class Projeto:
    titulo: str
    legenda: str
    categoria: str
    arquivo: str


PROJETOS = [
    Projeto("Gasolini", "Letras caixa com LED backlight e fachada em ACM", "letras", "gasolini-fachada"),
    Projeto("Amaggi", "Letras caixa iluminadas em fachada corporativa", "letras", "amaggi-letra-caixa-led"),
    Projeto("Peacook", "Logo e letras caixa com backlight", "letras", "peacook-letra-caixa-backlight"),
    Projeto("Gasolini — detalhe", "Letreiro iluminado à noite", "letras", "gasolini-letreiro-led"),
    Projeto("FIT Purificadores", "Fachada completa em ACM azul com letras caixa", "acm", "fit-fachada-acm"),
    Projeto("Suprema Casa de Carne", "Painel em ACM com letras caixa", "acm", "suprema-fachada-acm"),
    Projeto("FIT Purificadores — montagem", "Instalação dos painéis de ACM", "acm", "fit-acm-detalhe"),
    Projeto("Clínica Rena Odontologia", "Totem em ACM com caixa luminosa", "totens", "rena-totem"),
    Projeto("Clínica Rena — vista da rua", "Totem de entrada e sinalização de serviços", "totens", "rena-totem-rua"),
]

_USADAS = {p.categoria for p in PROJETOS}
CATEGORIAS = [c for c in TODAS_CATEGORIAS if c.slug in _USADAS]


# ======================================================================
#  MAPA DE FOTOS — HERO e SOBRE
#  profundidade = quanto a camada se move no parallax (negativo = contra-movimento)
# ======================================================================
@dataclass(frozen=True)
class Imagem:
    arquivo: str
    alt: str
    profundidade: float


HERO_FUNDO = Imagem("gasolini-fachada-hero", "Fachada da Gasolini com letras caixa iluminadas em Cuiabá", 0.25)
HERO_CARTOES = [
    Imagem("amaggi-letra-caixa-led-mini", "Letras caixa iluminadas da Amaggi", 0.6),
    Imagem("peacook-letra-caixa-backlight-mini", "Letras caixa com backlight da Peacook", 0.45),
]

SOBRE = [
    Imagem("gasolini-instalacao", "Equipe instalando letras caixa com LED", 0.12),
    Imagem("suprema-instalacao", "Instalação de letras caixa em painel de ACM", -0.08),
    Imagem("fit-instalacao-acm", "Montagem de fachada em ACM", 0.2),
]
