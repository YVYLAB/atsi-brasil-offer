# JAN — Kit visual de referência para proposta da YvyLab

**Data da revisão:** 17/11/2026.  **Natureza:** material de trabalho para uma demonstração comercial, **não é um manual de marca aprovado pela JAN**.

## O que está neste pacote

- `branding-jan.md`: guia com identidade observada no site da JAN e recomendações de aplicação.
- `tokens/jan-theme.css` e `tokens/jan-theme.json`: tokens editáveis e **aproximados**, amostrados da captura da página de contatos e complementados com sugestões de contraste.
- `referencias/fontes-oficiais.json`: endereços **verificados** de dois assets publicados no domínio oficial.
- `scripts/baixar_assets_oficiais.py`: baixa os dois assets originais em `logos/originais/` **ao executar em ambiente com internet**.
- `referencias/preview-online.html`: visualização dos assets hospedados pela JAN, exige internet.
- `assets/decor/*.svg`: dois SVGs **originais da YvyLab**, geométricos para fundo, **não são logos da JAN**.
- `PROMPT_OPENCODE.md`: instruções de aplicação da identidade numa demonstração para a JAN, sem modificar regras e preços do configurador.

## Situação dos logotipos

**Os arquivos oficiais de logo não foram obtidos como bytes neste ambiente:** downloads HTTPS ao domínio da JAN falharam. Não incluímos reconstruções artificiais ou logos inventados. Os links oficiais estão identificados e o script de download está pronto. Os arquivos institucionais/campanha publicados na web **não substituem um arquivo-mestre de marca validado pela JAN**.

Em um terminal com internet, na raiz desta pasta:

```bash
python3 scripts/baixar_assets_oficiais.py
```

O script salva os arquivos originais e seus hashes SHA-256; a seguir, confira visualmente as imagens e solicite à JAN a versão institucional autorizada caso a aplicação seja destinada a produção.

## Uso responsável

- Usar este kit em **mockup, estudo ou proposta de apresentação** da YvyLab.
- Não afirmar parceria, aprovação ou contratação da JAN.
- Não alterar nem distorcer a arte oficial; preserve proporção e área de proteção.
- Para publicar uma plataforma com marca JAN, obter permissão e os arquivos oficiais com a equipe de comunicação.
- Não utilizar a marca `JAN Plus` ou `+JAN` como nome de uma nova solução sem alinhamento, pois esses termos já aparecem em ações comerciais da própria JAN.

**Site-base:** https://www.jan.com.br/contato
