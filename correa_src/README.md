# Site Correa Metalúrgica

Mesmo motor do site da Só Fachadas, com as cores da logo (azul-marinho e dourado).
Publicado em https://thiagochio.github.io/sofachadas-site/correa/ (pasta `docs/correa/`).

| Quero mudar... | Arquivo |
| --- | --- |
| Telefone, e-mail, endereço, Instagram, CNPJ, link de avaliação | `correa_src/src/empresa.py` (campo vazio não aparece) |
| Serviços e fotos | `correa_src/src/dados.py` |
| Cores e fontes | `correa_src/assets/css/cinema.css` |
| Fotos novas | original em `correa_src/fotos_originais/` + `python correa_src/scripts/processa_fotos.py` |

Depois de mudar: `python correa_src/build.py`. Testes: `python correa_src/scripts/testa.py`.
O build da Só Fachadas (`python build.py`) preserva a pasta `docs/correa/`.
