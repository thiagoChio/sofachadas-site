"""
FONTE ÚNICA dos dados da empresa e do rastreamento.
Nada disso fica escrito dentro do HTML: o build.py lê daqui.
Trocou telefone, endereço ou pixel? Mude aqui e rode `python build.py`.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Empresa:
    nome: str = "Só Fachadas MT"
    nome_curto: str = "Só Fachadas"
    subtitulo: str = "Comunicação Visual"
    whatsapp_e164: str = "5565993464848"        # só dígitos, com 55 + DDD
    telefone_exibicao: str = "(65) 99346-4848"
    email: str = "sofachadas.contato@hotmail.com"
    endereco: str = "Av. Canadá, 800 - Santa Rosa"
    cep: str = "78040-050"
    cidade: str = "Cuiabá"
    estado: str = "MT"
    instagram_user: str = "sofachadasmt"
    facebook_url: str = "https://www.facebook.com/sofachadasmt"
    google_avaliacao_url: str = "https://g.page/r/CYYnq_kGoN-vEBM/review"
    cnpj: str = "37.347.738/0001-30"
    ano_inicio: int = 2020
    horario: str = "Seg a sex, 7h às 17h"       # CONFIRMAR com o Ju
    site_url: str = "https://thiagochio.github.io/sofachadas/"

    @property
    def whatsapp_url(self) -> str:
        return f"https://wa.me/{self.whatsapp_e164}"

    @property
    def instagram_url(self) -> str:
        return f"https://www.instagram.com/{self.instagram_user}/"


@dataclass(frozen=True)
class Tracking:
    # Deixe vazio enquanto não houver conta de anúncio. Quando tiver, cole os IDs aqui.
    meta_pixel_id: str = ""            # ex.: "123456789012345"
    google_ads_id: str = ""            # ex.: "AW-123456789"
    google_ads_label: str = ""         # ex.: "AbCdEfGhIjKlMn"


EMPRESA = Empresa()
TRACKING = Tracking()
