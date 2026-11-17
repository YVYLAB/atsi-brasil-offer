# Assets do kit ATSI Brasil

- `atsi-agro-contornos.svg` e `atsi-agro-horizonte.svg`: SVGs decorativos locais criados para o configurador; **não são logos oficiais**.
- `atsi-logo-institucional.svg` e `atsi-logo-cabecalho.svg`: serão gerados aqui após executar `python3 scripts/baixar_logos_oficiais.py` a partir da raiz do ZIP **em um computador com internet**.
- O download dos logos originais não foi possível no ambiente em que este ZIP foi gerado. Consulte `branding-tsi-brasil.md` para links, paleta e instruções.

## Integração no configurador

Os dois logos foram posteriormente baixados com o script do pacote e validados
como SVG sem scripts nem referências externas ativas. O cabeçalho usa a variante
branca sobre azul-marinho, também aplicada aos mockups.

SHA-256 dos originais:
- Institucional: `e34c697166072682ccfda17ce8e27faba1a5252143f764164c8ff87b33e7c9a3`
- Cabeçalho: `f28ffc81ddebe17350fa86dc540cca7ae15adc0eedd2981400ed694d9c27ad59`

Montserrat variável obtida do repositório Google Fonts:
https://github.com/google/fonts/tree/main/ofl/montserrat
Arquivo local `montserrat-variable.ttf`; licença em `Montserrat-OFL.txt`.

Distribuir a pasta `branding/assets` junto ao HTML para manter logos e fonte
disponíveis offline. A autorização de uso da marca continua sujeita à ATSI.
