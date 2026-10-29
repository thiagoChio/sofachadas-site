"""
FONTE ÚNICA dos dados da Correa Metalúrgica e do rastreamento.
Trocou telefone, endereço ou pixel? Mude aqui e rode `python correa_src/build.py`.
Campos vazios ("") não aparecem no site.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Empresa:
    nome: str = "Correa Metalúrgica"
    subtitulo: str = "Metalúrgica e estruturas metálicas"
    whatsapp_e164: str = "5565992764410"        # só dígitos, com 55 + DDD
    telefone_exibicao: str = "(65) 99276-4410"
    email: str = "correametalurgica.cuiaba@gmail.com"
    endereco: str = "Av. Canadá, 800 - Santa Rosa"
    cep: str = "78040-050"
    cidade: str = "Cuiabá"
    estado: str = "MT"
    instagram_user: str = ""                     # ex.: "correametalurgica" (sem @)
    facebook_url: str = ""
    google_avaliacao_url: str = ""               # link de avaliação do Perfil do Google, depois da verificação
    cnpj: str = ""
    horario: str = "Seg a sex, 7h às 18h"
    site_url: str = "https://thiagochio.github.io/sofachadas-site/correa/"

    @property
    def whatsapp_url(self) -> str:
        return f"https://wa.me/{self.whatsapp_e164}"

    @property
    def instagram_url(self) -> str:
        return f"https://www.instagram.com/{self.instagram_user}/" if self.instagram_user else ""


@dataclass(frozen=True)
class Tracking:
    # Deixe vazio enquanto não houver conta de anúncio. Quando tiver, cole os IDs aqui.
    meta_pixel_id: str = ""
    google_ads_id: str = ""
    google_ads_label: str = ""


EMPRESA = Empresa()
TRACKING = Tracking()
