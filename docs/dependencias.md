# Dependências automáticas

Selecionar um recurso inclui automaticamente os requisitos que ainda faltam.
Um popup explica o vínculo, lista cada inclusão com horas e valor e oferece o
botão **OK**. O investimento é atualizado junto com a configuração.

Regra acrescentada pelo usuário: **M01, E-books em destaque, exige E01, biblioteca
de e-books**. A vitrine e a biblioteca continuam sendo entregas distintas; o
esforço de uma não é incorporado outra vez à outra. Nos planos que já contêm
as duas, não há nova inclusão, popup ou cobrança duplicada.

Também são aplicados os vínculos existentes de quizzes com IA, push segmentado
e automações, perfis pesquisáveis, eventos/QR/check-in, pagamentos/acesso,
relatórios e pontuação. Requisitos obrigatórios já presentes não geram aviso.
Não são criados vínculos só por semelhança de nomes: por exemplo, uma vitrine
de evento pode continuar apontando para o destino externo conforme seu escopo.

## Inclusão e remoção

- Recurso necessário a outro selecionado fica marcado e bloqueado para remoção.
  O card informa quais escolhas dependem dele.
- O usuário pode retirar a escolha principal. Requisitos adicionados
  automaticamente saem quando não há mais nenhum recurso que os utilize.
- Escolhas feitas manualmente e recursos do preset não são retirados por essa
  limpeza, mesmo quando deixam de ser necessários a outro item.
- Requisitos compartilhados ficam enquanto houver qualquer uso.
- Trocar de preset reinicia a composição e o controle de inclusões automáticas.

`prerequisites` centraliza o grafo, `selectedDependents()` calcula os vínculos
ativos e `autoSelected` distingue inclusões automáticas de escolhas originais.
Os requisitos contam uma única vez nos totais e seguem as mesmas regras de
desconto dos demais itens. O PDF registra todos os itens efetivamente incluídos.

Teste: `python3 -m unittest discover -s tests -v`, incluindo os fluxos de
inclusão, bloqueio, popup, remoção de órfãos, requisitos compartilhados e
preservação de escolhas manuais.
