# ATSI Brasil — Kit de Branding para OpenCode

Este pacote contém o arquivo solicitado `branding-tsi-brasil.md` (também com nome corrigido `branding-atsi-brasil.md`), tokens de cores e SVGs decorativos.

**Limitação importante:** neste ambiente, não foi possível baixar os bytes dos dois logotipos oficiais. Para não incluir logos falsos ou incompletos, o pacote traz as **URLs oficiais verificadas** e um script que baixa e valida os dois SVGs no computador com internet.

## Instalação

1. Extraia o ZIP na pasta do projeto do OpenCode.
2. Abra `branding-tsi-brasil.md` e aplique as instruções ao configurador mais recente.
3. Na raiz desta pasta, execute `python3 scripts/baixar_logos_oficiais.py`.
4. Após o download, confira `assets/atsi-logo-institucional.svg` e `assets/atsi-logo-cabecalho.svg` e copie os assets para o diretório público da aplicação.
5. Não substitua o catálogo atual de 54 features pelo HTML demonstrativo antigo.

Arquivos decorativos (`assets/atsi-agro-*.svg`) são originais deste kit, **não** são logotipos da ATSI.
