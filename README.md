# Site Só Fachadas MT

Landing page da Só Fachadas MT (Cuiabá–MT): fachadas em ACM, letras caixa com LED, totens e estruturas metálicas.
Objetivo único: levar o visitante a pedir orçamento pelo WhatsApp.

Site estático (HTML + CSS + JS), gerado por um script Python. Roda grátis no GitHub Pages e aceita domínio próprio depois.

## Onde mudar cada coisa

| Quero mudar... | Arquivo |
| --- | --- |
| Telefone, WhatsApp, endereço, e-mail, redes, horário | `src/empresa.py` |
| IDs do Pixel da Meta e do Google Ads | `src/empresa.py` (classe `Tracking`) |
| Serviços, projetos do portfólio, fotos do hero e do "Sobre" | `src/dados.py` (MAPA DE FOTOS) |
| Cores, fontes, tamanhos, animações | `assets/css/cinema.css` |
| Interações (menu, filtro, lightbox, formulário) | `assets/js/cinema.js` |
| Fotos novas | coloque o original em `fotos_originais/` e rode `python scripts/processa_fotos.py` |

Depois de qualquer mudança: `python build.py` (gera a pasta `docs/`, que é o site publicado).

## Testar

```
pip install playwright pillow
python scripts/testa.py
```

Testa 5 tamanhos de tela (360, 390, 414, 768, 1440), movimento reduzido e sem JavaScript: console sem erros, sem
rolagem lateral, botão principal acima da dobra no celular, alvos de toque ≥ 44 px, filtros, lightbox (setas, teclado)
e o formulário abrindo o WhatsApp com nome, serviço e origem (UTM). Prints em `scripts/prints/`.

## Publicar no GitHub Pages (grátis)

1. No GitHub Desktop: **File → Add local repository** → esta pasta → **create a repository** →
   **Publish repository** com o nome `sofachadas` e **"Keep this code private" desmarcado**.
2. No site do GitHub, no repositório: **Settings → Pages → Build and deployment →
   Source: Deploy from a branch → Branch: `main` / pasta `/docs` → Save**.
3. Em 1–2 minutos o site fica no ar em `https://thiagochio.github.io/sofachadas-site/`.

## Domínio próprio (quando o Ju comprar)

1. Em `src/empresa.py`, troque `site_url` para `https://www.sofachadasmt.com.br/` e rode `python build.py`.
2. No GitHub: **Settings → Pages → Custom domain** → `www.sofachadasmt.com.br`.
3. No registro do domínio (Registro.br): crie um registro `CNAME` de `www` apontando para `thiagochio.github.io`.

## Pendências antes de anunciar

- [x] WhatsApp novo: (65) 99276-4410
- [x] Horário confirmado: seg a sex, 7h às 18h
- [ ] Colar os IDs do Pixel da Meta e do Google Ads quando as contas de anúncio existirem
- [x] Website e telefone atualizados no Perfil da Empresa no Google
- [ ] Pedir avaliações no Google (o site tem botão para isso; a ficha ainda tem zero)
