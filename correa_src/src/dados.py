"""
Conteúdo do site da Correa Metalúrgica: serviços e MAPA DE FOTOS.
Para trocar uma foto, coloque o original em correa_src/fotos_originais/, rode
`python correa_src/scripts/processa_fotos.py` e ajuste o nome aqui.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Servico:
    slug: str
    titulo: str
    descricao: str
    icone: str  # nome do ícone SVG em build.py


SERVICOS = [
    Servico("coberturas", "Coberturas metálicas",
            "Coberturas com treliça e telha metálica para garagens, áreas de lazer, comércios e pátios.",
            "cobertura"),
    Servico("policarbonato", "Coberturas em policarbonato",
            "Estrutura metálica com policarbonato: protege da chuva e do sol sem perder a claridade.",
            "policarbonato"),
    Servico("portoes", "Portões e grades",
            "Portões de abrir ou de correr, grades e gradis sob medida, fabricados na nossa oficina.",
            "portao"),
    Servico("estruturas", "Estruturas e mezaninos",
            "Estruturas metálicas, mezaninos, escadas e passarelas calculadas para o uso do seu espaço.",
            "estrutura"),
    Servico("galpoes", "Galpões e barracões",
            "Estrutura completa para galpões e barracões, da fabricação à montagem no local.",
            "galpao"),
    Servico("serralheria", "Serralheria em geral",
            "Guarda-corpos, corrimãos, reforços, consertos e peças sob medida em aço.",
            "solda"),
]


@dataclass(frozen=True)
class Categoria:
    slug: str
    nome: str


TODAS_CATEGORIAS = [
    Categoria("coberturas", "Coberturas"),
    Categoria("portoes", "Portões e grades"),
    Categoria("estruturas", "Estruturas"),
]


# ======================================================================
#  MAPA DE FOTOS — PORTFÓLIO
#  arquivo = nome em assets/img/ (sem .jpg). A miniatura é <arquivo>-mini.jpg
# ======================================================================
SELO_ILUSTRATIVO = False


@dataclass(frozen=True)
class Projeto:
    titulo: str
    legenda: str
    categoria: str
    arquivo: str


PROJETOS = [
    Projeto("Cobertura com treliça", "Estrutura em treliça metálica com telha", "coberturas", "cobertura-trelica"),
    Projeto("Cobertura de pátio", "Cobertura metálica sobre a entrada e o pátio", "coberturas", "cobertura-frente"),
    Projeto("Cobertura em policarbonato", "Área de lazer coberta com estrutura metálica e policarbonato", "coberturas", "cobertura-policarbonato"),
    Projeto("Portão sob medida", "Portão em metalon com desenho diagonal, na fabricação", "portoes", "portao"),
    Projeto("Estrutura em fabricação", "Peças cortadas e soldadas na oficina", "estruturas", "estrutura-oficina"),
    Projeto("Montagem no local", "Solda de pilar metálico na obra", "estruturas", "solda-estrutura"),
]

_USADAS = {p.categoria for p in PROJETOS}
CATEGORIAS = [c for c in TODAS_CATEGORIAS if c.slug in _USADAS]


# ======================================================================
#  MAPA DE FOTOS — HERO e SOBRE
# ======================================================================
@dataclass(frozen=True)
class Imagem:
    arquivo: str
    alt: str
    profundidade: float


HERO_FUNDO = Imagem("cobertura-trelica-hero", "Cobertura metálica com treliça feita pela Correa Metalúrgica", 0.25)
HERO_CARTOES = [
    Imagem("cobertura-policarbonato-mini", "Cobertura em policarbonato com estrutura metálica", 0.6),
    Imagem("portao-mini", "Portão metálico sob medida na fabricação", 0.45),
]

SOBRE = [
    Imagem("solda-estrutura", "Soldador montando pilar metálico na obra", 0.12),
    Imagem("estrutura-oficina", "Estrutura metálica em fabricação na oficina", -0.08),
    Imagem("cobertura-frente", "Cobertura metálica pronta sobre a entrada", 0.2),
]
