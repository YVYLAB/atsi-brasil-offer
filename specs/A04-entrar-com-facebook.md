# A04 — Entrar com Facebook

**Status:** estimativa inicial para o configurador: **32 h / R$ 6.400**.
Proposta de esforço para uma integração oficial Android/iOS/web e um ciclo de
homologação. Não corresponde a login já implementado nem a medição histórica.

## Descrição e funcionamento

Entrar com uma conta Facebook e vincular a identidade à conta ATSI+, com
consentimento e permissões necessárias ao acesso.

## Escopo e exclusões

Login oficial para alunos Android/iOS/web e retorno à plataforma. Configuração
do aplicativo Meta, integração com o serviço de identidade escolhido em arquitetura
e tratamento das identidades existentes. Não inclui leitura de publicações,
contatos ou grupos, publicação em redes sociais ou envio de mensagens.

## Tarefas para validação

| ID | Tarefa e entrega verificável | Horas propostas | Status |
|---|---|---:|---|
| A04-T01 | Configurar app Meta, plataformas, callbacks e URLs de privacidade e exclusão de dados | 4 | Revisão técnica preliminar |
| A04-T02 | Integrar login oficial Android/iOS e retorno à plataforma | 8 | Revisão técnica preliminar |
| A04-T03 | Integrar login web, redirecionamentos e proteção do estado da autenticação | 6 | Revisão técnica preliminar |
| A04-T04 | Validar tokens e tratar vínculo de identidade, e-mail ausente e conta existente | 6 | Revisão técnica preliminar |
| A04-T05 | Testar Android/iOS/web, cancelamento, recusa de permissão e sessão expirada | 8 | Revisão técnica preliminar |
| **Total** | | **32 h** | **Estimativa inicial** |

## Dependências e riscos

Depende do login de base B02 e da fundação de identidade. Credenciais, domínio,
permissões, modo de publicação e políticas vigentes da Meta devem ser confirmados
na arquitetura. Avaliar o fluxo oficial disponível em cada plataforma, inclusive
eventuais diferenças de tokens no iOS. Não presumir SDK ou fornecedor já escolhido.

O Facebook pode não disponibilizar um e-mail utilizável. Prever a coleta e
verificação necessárias dentro da conta ATSI+, sem bloquear indevidamente a
jornada nem unir contas apenas por coincidência de e-mail. Vinculação exige
comprovação da conta já existente. Segredos do provedor permanecem no servidor.

Revisão ou aprovação externa da Meta pode introduzir esperas não contadas como
horas de implementação. A plataforma não deve prometer aprovação por terceiros.

## Cenário mínimo específico de aceite

O aluno entra com Facebook e retorna com sessão válida em Android, iOS e web.
Cancelamento, recusa de permissão e token inválido retornam a uma tela de acesso
clara, sem criar sessão indevida. E-mail ausente tem jornada definida; a
vinculação de identidade não permite acessar a conta de outra pessoa.

## Custos e composição comercial

Implantação: **R$ 6.400**, conforme 32 h e referência comercial de R$ 200/h.
Operação usa o serviço de identidade escolhido para a plataforma, com suas
cotas e condições; não duplica a infraestrutura de autenticação compartilhada.

Opcional independente, fora de Essencial, Plus e Premium. Pode receber o desconto
dos opcionais adicionais quando a configuração atende às regras da campanha.
Não muda os valores padrão dos planos nem o curso administrativo de cortesia.
