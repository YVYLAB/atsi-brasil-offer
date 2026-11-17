# Plataformas incluídas desde o Essencial

Decisão de produto confirmada em 17/11/2026: **o Essencial inclui aplicativos
Android e iOS e versão web para alunos**, além do painel administrativo web.
Plus e Premium mantêm essas plataformas; diferenciam-se pelas funcionalidades
contratadas, não pela inclusão de uma plataforma.

## Escopo

- **Android e iOS:** aplicativos para os alunos. Uma implementação
  multiplataforma pode ser adotada; não há exigência de dois projetos nativos.
- **Web para alunos:** acesso pelo navegador, com layout responsivo e as
  jornadas das funcionalidades contratadas. Não se resume ao painel de gestão.
- **Painel administrativo web:** acesso separado para gestão, com papéis
  e permissões, conforme F04/B08 e demais funcionalidades contratadas.
- O HTML do configurador e seus mockups continuam sendo apresentação comercial,
  não uma implementação dessas aplicações.

## Detalhamento e aceite

F01/F02 devem detalhar as jornadas Android/iOS/web, navegadores suportados,
responsividade, acessibilidade, sessão, recuperação de acesso e diferenças
entre plataformas. F03 deve preparar também a experiência web dos alunos;
F04 continua sendo exclusivamente a fundação administrativa.

O aceite da base deve demonstrar, nas três plataformas, login/recuperação,
perfil e consentimento, mural, catálogo, reprodução pelo método contratado e
progresso. Publicação de conteúdo deve refletir nos acessos autorizados.
Validar autorização no servidor e estados de erro, vazio e sessão expirada.

Recursos dependentes do dispositivo ou canal, como push, downloads offline
e pagamentos, exigem matriz de compatibilidade específica nas respectivas
specs. Incluir web não promete automaticamente offline no navegador, PWA
instalável ou equivalência de APIs nativas. Submissão às lojas, contas e
eventuais taxas seguem validação própria; aprovação por terceiros não é garantida.

## Estimativas: revisão pendente

As tarefas revisadas em 16/11/2026 explicitavam Android/iOS e painel
administrativo web, mas não decompunham a versão web dos alunos. Não considerar
que a estimativa de mobile já cobre automaticamente essa entrega.

Revisar o impacto em F01/F02/F03, ambientes/pipelines (F05/F06), homologação
(F07), interfaces e integrações das features. Decompor adaptação/reuso,
responsividade e testes de navegador, evitando duplicar backend e regras
compartilhadas. A tecnologia web será definida na arquitetura.

**Nenhuma hora, valor ou prazo foi recalculado nesta atualização.** Fundação
de 522 h e referências dos presets foram preservadas: Essencial 890 h,
Plus 1.150 h e Premium 1.946 h. Esses números permanecem preliminares;
o impacto da web para alunos está pendente de revisão técnica e comercial.
Não há estimativa adicional aprovada nem implementação do aplicativo.
