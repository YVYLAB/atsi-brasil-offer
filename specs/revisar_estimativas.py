"""Aplica a revisão técnica inicial. Não constitui aprovação comercial."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Cada linha descreve trabalho específico. Horas são esforço, não tempo decorrido.
review = {
    "F01": [
        ("Workshops com responsáveis, objetivos, públicos e plataformas", 12),
        ("Mapear jornadas e requisitos funcionais por módulo do catálogo", 20),
        ("Definir requisitos não funcionais, privacidade e restrições", 12),
        ("Organizar épicos, prioridades, dependências e exclusões", 12),
        ("Revisar specs e critérios de aceite das features contratáveis", 24),
        ("Decompor tarefas, revisar estimativas e registrar premissas", 16),
        ("Consolidar pendências e conduzir revisão de aprovação", 8),
    ],
    "F02": [
        ("Definir arquitetura da informação e fluxos essenciais", 16),
        ("Desenhar wireframes mobile e painel administrativo", 24),
        ("Produzir telas de referência e estados de erro/vazio", 24),
        ("Modelar domínio, diagrama de classes e relacionamentos", 16),
        ("Definir arquitetura, contratos e fronteiras dos serviços", 16),
        ("Desenhar autorização, segurança e fluxo de dados pessoais", 12),
        ("Revisar acessibilidade e decisões com ATSI/YvyLab", 12),
    ],
    "F03": [
        ("Inicializar Expo/TypeScript e configuração por ambiente", 8),
        ("Estruturar navegação, deep links e rotas protegidas", 12),
        ("Implementar tokens, componentes e layouts reutilizáveis", 16),
        ("Preparar cliente de API, erros globais e estado de sessão", 8),
        ("Validar shell em Android/iOS e acessibilidade básica", 12),
    ],
    "F04": [
        ("Inicializar Next.js, configuração e layout administrativo", 8),
        ("Integrar sessão administrativa e papéis", 8),
        ("Proteger rotas e centralizar autorização no servidor", 8),
        ("Testar matriz de acesso e navegação administrativa", 8),
    ],
    "F05": [
        ("Preparar ambientes, segredos e configuração de serviços", 8),
        ("Configurar migrações e acesso ao banco/API", 8),
        ("Estabelecer políticas RLS e isolamento inicial", 8),
        ("Configurar storage, permissões e upload comum", 8),
        ("Preparar recuperação, observabilidade e documentação operacional", 8),
        ("Validar isolamento dos ambientes e segurança da fundação", 8),
    ],
    "F06": [
        ("Configurar assinatura e credenciais Android/iOS", 10),
        ("Automatizar verificações e builds no CI", 10),
        ("Distribuir builds internos e validar instalação", 10),
        ("Preparar metadados, privacidade e submissões", 12),
        ("Executar submissão inicial e documentar publicação", 10),
    ],
    "F07": [
        ("Preparar plano integrado, massa de dados e ambientes de homologação", 10),
        ("Executar jornadas ponta a ponta da base e vídeo escolhido", 16),
        ("Revisar autorização e exposição de dados entre usuários", 10),
        ("Revisar acessibilidade e dispositivos representativos", 10),
        ("Executar ciclo de regressão após correções integradas", 12),
        ("Consolidar aceite, pendências e transferência operacional", 6),
    ],
    "B01": [
        ("Definir contrato de destaques e disponibilidade dos cursos", 4),
        ("Consultar e paginar destaques publicados com autorização", 6),
        ("Construir mural, capas e navegação ao catálogo", 10),
        ("Tratar carregamento, vazio, imagem ausente e falha de rede", 4),
        ("Testar publicação, acesso e navegação Android/iOS", 8),
    ],
    "B02": [
        ("Configurar login e validação de credenciais no provedor", 6),
        ("Implementar sessão, renovação, expiração e logout", 8),
        ("Implementar recuperação e deep link de redefinição", 8),
        ("Construir telas, erros e proteção contra enumeração", 8),
        ("Testar sessão expirada, recuperação e isolamento de usuários", 10),
    ],
    "B03": [
        ("Configurar domínio, DNS e autenticação do remetente", 4),
        ("Integrar envio transacional com credenciais protegidas", 6),
        ("Preparar modelos e links seguros de recuperação", 4),
        ("Tratar falha, limites e rastreabilidade sem expor dados", 4),
        ("Validar entrega e documentar configuração operacional", 6),
    ],
    "B04": [
        ("Modelar perfil privado e políticas de leitura/alteração", 6),
        ("Implementar foto com tipo, tamanho e autorização", 8),
        ("Implementar alteração de nome e e-mail com verificação", 8),
        ("Integrar gestão de senha e reautenticação necessária", 6),
        ("Construir telas e testar privacidade, falhas e validações", 12),
    ],
    "B05": [
        ("Definir versão do texto, registro e revogação do consentimento", 4),
        ("Persistir escolha com identificação e data", 4),
        ("Implementar controle no perfil e feedback de atualização", 4),
        ("Testar revogação, acesso e evidência da escolha", 4),
    ],
    "B06": [
        ("Modelar cursos, módulos, aulas e ordem de publicação", 12),
        ("Implementar consultas, paginação e acesso básico autorizado", 14),
        ("Construir catálogo e página de detalhes", 16),
        ("Construir navegação módulo/aula e integração do player escolhido", 12),
        ("Tratar conteúdo indisponível e falhas de carregamento", 6),
        ("Testar ordenação, publicação e fluxos mobile", 12),
    ],
    "B07": [
        ("Definir regras de conclusão e retomada por estratégia de vídeo", 6),
        ("Implementar progresso idempotente por usuário e aula", 10),
        ("Calcular conclusão do curso e atualizar visualização", 8),
        ("Tratar reconexão e alterações no catálogo", 6),
        ("Testar isolamento, repetição de eventos e retomada", 10),
    ],
    "B08": [
        ("Definir permissões e estados de publicação", 8),
        ("Implementar CRUD de cursos, módulos e aulas", 18),
        ("Construir listagens, formulários e ordenação", 20),
        ("Integrar capas e destaques do mural", 8),
        ("Tratar validações, exclusão e referências em uso", 8),
        ("Testar autorização e ciclo completo de publicação", 14),
    ],
    "A01": [
        ("Definir política TOTP, reautenticação e recuperação", 6),
        ("Integrar inscrição, confirmação e remoção do fator", 8),
        ("Implementar desafio MFA no acesso e sessões", 8),
        ("Construir telas e orientações de recuperação segura", 6),
        ("Testar perda do fator, sessão e tentativas inválidas", 10),
    ],
    "A02": [
        ("Configurar OAuth Google e redirecionamentos por plataforma", 4),
        ("Integrar fluxo nativo/web e retorno ao app", 6),
        ("Tratar vínculo, e-mail coincidente e cancelamento", 6),
        ("Testar Android/iOS e contas de homologação", 8),
    ],
    "A03": [
        ("Definir tenant e configurar aplicação Microsoft", 6),
        ("Integrar OAuth e redirecionamento Android/iOS", 8),
        ("Tratar vínculo de identidade, cancelamento e consentimento", 6),
        ("Testar contas permitidas, restrições e falhas", 8),
    ],
    "M01": [
        ("Definir dados do destaque e destino externo/interno", 2),
        ("Implementar configuração no painel reutilizando a base", 4),
        ("Renderizar card, capa e navegação", 4),
        ("Testar publicação, links e capa ausente", 4),
    ],
    "M02": [
        ("Definir data, local e destino do destaque sem exigir gestão de eventos", 3),
        ("Implementar configuração do card no painel", 4),
        ("Exibir destaque e navegação no mural", 4),
        ("Testar datas, destino e disponibilidade", 3),
    ],
    "M03": [
        ("Definir vigência, destino e regras de exibição do banner", 4),
        ("Implementar cadastro e programação no painel", 6),
        ("Exibir banner conforme vigência e tratar links", 4),
        ("Testar limites de data e fallback de imagem", 4),
    ],
    "C01": [
        ("Validar compatibilidade do caso de uso com políticas do YouTube", 4),
        ("Validar URL/ID e integrar player oficial", 6),
        ("Tratar orientação, navegação e eventos permitidos", 6),
        ("Implementar estados de vídeo indisponível e falha de rede", 4),
        ("Testar incorporação em Android/iOS sem contornar o player", 8),
    ],
    "C02": [
        ("Definir ingestão e autorização do vídeo privado", 8),
        ("Implementar upload e associação no painel", 14),
        ("Processar estados e callbacks de preparação do vídeo", 10),
        ("Gerar autorização/token e verificar direito de acesso", 12),
        ("Integrar player, retomada e estados de falha", 14),
        ("Testar expiração, acesso indevido e rede em Android/iOS", 18),
        ("Documentar limites de proteção e consumo operacional", 4),
    ],
    "C03": [
        ("Implementar capacidade online equivalente a C02 sem dupla cobrança", 80),
        ("Validar viabilidade do download no Expo e políticas de uso", 12),
        ("Implementar fila, pausa, retomada e cancelamento de downloads", 24),
        ("Gerenciar arquivos, espaço local e remoção por usuário", 16),
        ("Definir e implementar expiração e revogação possível", 18),
        ("Implementar reprodução local e retomada offline", 16),
        ("Sincronizar progresso com resolução de eventos repetidos", 14),
        ("Testar rede interrompida, pouco espaço, logout e Android/iOS", 28),
    ],
    "C04": [
        ("Definir elegibilidade, identificação e dados do certificado", 6),
        ("Gerar PDF a partir de modelo aprovado", 10),
        ("Implementar código e consulta pública mínima de verificação", 8),
        ("Integrar emissão idempotente, armazenamento e download", 8),
        ("Testar acesso, conclusão e repetição de emissão", 10),
    ],
    "C05": [
        ("Modelar perguntas, alternativas, tentativas e política de aprovação", 8),
        ("Implementar autoria e edição no painel", 14),
        ("Construir execução e envio das respostas no app", 12),
        ("Corrigir no servidor e persistir resultado com segurança", 10),
        ("Testar reenvios, tentativas e proteção do gabarito", 12),
    ],
    "C06": [
        ("Definir fontes autorizadas, formato e política de geração", 8),
        ("Preparar ingestão textual e limites de conteúdo", 10),
        ("Integrar provedor com saída estruturada validada", 12),
        ("Construir revisão, edição e publicação humana no quiz", 12),
        ("Implementar limites de uso, erros e registro de consumo operacional", 8),
        ("Testar respostas inválidas, segurança e qualidade amostral", 14),
    ],
    "C07": [
        ("Definir fontes, privacidade, retenção e limites do assistente", 12),
        ("Implementar ingestão, segmentação e indexação autorizada", 24),
        ("Implementar busca com autorização por curso/usuário", 20),
        ("Integrar resposta com referências e recusa fora do contexto", 20),
        ("Construir conversa e estados de envio no app", 16),
        ("Aplicar limites, tratamento de falha e rastreabilidade", 12),
        ("Avaliar vazamento entre cursos, injeção de instruções e qualidade", 24),
        ("Documentar reindexação, atualização e operação", 8),
    ],
    "C08": [
        ("Modelar comentários, respostas e permissões", 6),
        ("Implementar envio, edição e remoção autorizada", 10),
        ("Construir listagem paginada e respostas no app", 10),
        ("Adicionar moderação administrativa básica", 8),
        ("Testar abuso básico, acesso e exclusão", 10),
    ],
    "C09": [
        ("Definir elegibilidade, nota e política de edição", 4),
        ("Persistir avaliação por usuário/curso com autorização", 6),
        ("Construir formulário e confirmação no app", 6),
        ("Testar repetição, edição e acesso", 8),
    ],
    "E01": [
        ("Modelar metadados, arquivos e acesso básico", 6),
        ("Implementar cadastro, capas e upload no painel", 12),
        ("Construir biblioteca com pesquisa e paginação", 10),
        ("Implementar abertura e download autorizado do arquivo", 10),
        ("Testar tipos, tamanho, links expirados e dispositivos", 12),
    ],
    "N01": [
        ("Configurar credenciais push e permissões Android/iOS", 8),
        ("Registrar e renovar tokens por dispositivo/usuário", 8),
        ("Implementar envio administrativo e recibos de falha", 10),
        ("Integrar recebimento, navegação e preferência de usuário", 8),
        ("Testar app aberto, fechado, token inválido e logout", 12),
    ],
    "N02": [
        ("Definir segmentos suportados e regras de elegibilidade", 6),
        ("Implementar seleção de público e prévia de quantidade", 8),
        ("Construir configuração e revisão da campanha", 8),
        ("Enviar em lotes evitando duplicação por campanha", 8),
        ("Testar segmentação, permissões e falhas parciais", 10),
    ],
    "N03": [
        ("Definir gatilhos, agenda, fuso e regras dos fluxos", 8),
        ("Implementar processamento agendado e estado do fluxo", 14),
        ("Adicionar idempotência, retentativa e cancelamento", 12),
        ("Construir configuração administrativa e histórico", 12),
        ("Testar reprocessamento, falhas e limites do serviço", 14),
    ],
    "G01": [
        ("Modelar grupos, categorias e links oficiais", 2),
        ("Implementar cadastro e publicação no painel", 4),
        ("Construir diretório e abertura do convite", 4),
        ("Testar links inválidos, privacidade e navegação", 4),
    ],
    "G03": [
        ("Modelar grupos, membros, publicações e visibilidade", 10),
        ("Implementar associação e autorização por grupo", 12),
        ("Construir feed paginado, publicação e mídia", 20),
        ("Implementar administração e moderação básica", 16),
        ("Tratar exclusão, denúncia e conteúdo indisponível", 8),
        ("Testar isolamento, mídia e fluxos de participação", 16),
    ],
    "G04": [
        ("Definir privacidade, retenção e regras de contato", 10),
        ("Modelar conversas, participantes e mensagens", 12),
        ("Implementar entrega em tempo real e paginação de histórico", 22),
        ("Construir conversas, estados de envio e reconexão", 20),
        ("Implementar bloqueio, denúncias e tratamento administrativo", 16),
        ("Testar ordenação, mensagens duplicadas e acesso indevido", 20),
        ("Avaliar limites de conexões e documentar operação", 8),
    ],
    "G05": [
        ("Definir campos públicos e consentimento opt-in", 6),
        ("Separar dados privados e públicos com políticas de acesso", 10),
        ("Construir edição e prévia do perfil público", 10),
        ("Implementar revogação e efeitos na visibilidade", 8),
        ("Testar privacidade, imagens e exposição indevida", 10),
    ],
    "G06": [
        ("Definir campos pesquisáveis e regras de descoberta", 4),
        ("Implementar índices, consulta e paginação autorizada", 8),
        ("Construir pesquisa, resultados e navegação ao perfil", 8),
        ("Testar opt-out, enumeração básica e desempenho inicial", 12),
    ],
    "EV01": [
        ("Modelar eventos, lotação, inscrições e estados", 12),
        ("Implementar administração de evento e lista de participantes", 20),
        ("Construir detalhes e inscrição no app", 16),
        ("Garantir vagas com transação e evitar inscrição duplicada", 16),
        ("Implementar cancelamento e regras de disponibilidade", 12),
        ("Testar concorrência de vagas, permissões e datas", 20),
    ],
    "EV02": [
        ("Definir identificador não previsível e validade da inscrição", 4),
        ("Gerar e associar QR ao registro sem expor dados pessoais", 6),
        ("Construir exibição e estados da inscrição", 6),
        ("Testar cancelamento, repetição e leitura de QR", 10),
    ],
    "EV03": [
        ("Definir template e regras de destinatários", 4),
        ("Integrar convite com serviço compartilhado B03", 6),
        ("Implementar estado de envio e reenvio controlado", 6),
        ("Testar falhas, limites e links do convite", 8),
    ],
    "EV04": [
        ("Definir papéis e regras de check-in online", 6),
        ("Integrar câmera, permissões e leitor no app", 10),
        ("Validar inscrição e registrar entrada atomicamente", 12),
        ("Construir feedback de sucesso, erro e duplicidade", 10),
        ("Implementar consulta administrativa de presenças", 8),
        ("Testar reutilização, evento incorreto e rede/dispositivos", 16),
    ],
    "P01": [
        ("Selecionar estratégia web e revisar fronteira com regras de lojas", 10),
        ("Modelar pedidos, estados e referências de pagamento", 12),
        ("Integrar criação de cobrança e checkout do provedor", 16),
        ("Validar assinatura de webhooks e tratar idempotência", 16),
        ("Implementar conciliação e fluxo básico de estorno", 12),
        ("Testar sandbox, eventos fora de ordem e falhas", 20),
    ],
    "P02": [
        ("Definir ciclo, cancelamento e estratégia por canal", 12),
        ("Integrar criação e atualização da assinatura no provedor", 18),
        ("Implementar renovação, falha e carência definidas no escopo", 18),
        ("Construir telas de plano, estado e cancelamento", 16),
        ("Sincronizar direitos de acesso com eventos recorrentes", 14),
        ("Testar cancelamento, renovação e eventos fora de ordem", 22),
    ],
    "P03": [
        ("Definir oferta e elegibilidade de compra por canal", 6),
        ("Integrar pedido e associação de comprador/curso", 10),
        ("Liberar e revogar direitos com base no pagamento", 12),
        ("Construir oferta, confirmação e estado da compra", 10),
        ("Testar compra repetida, falha, estorno e autorização", 16),
    ],
    "P04": [
        ("Definir reserva de vaga e expiração do pedido", 8),
        ("Integrar pedido e inscrição sem ultrapassar lotação", 14),
        ("Confirmar ou liberar vaga conforme pagamento", 12),
        ("Construir compra, confirmação e cancelamento", 10),
        ("Testar concorrência, expiração e estorno", 16),
    ],
    "P05": [
        ("Definir regras de perfil, compra e assinatura", 10),
        ("Modelar direitos e precedência das regras", 12),
        ("Aplicar autorização no backend de catálogo e aulas", 14),
        ("Integrar autorização de vídeo privado quando aplicável", 10),
        ("Exibir bloqueios e instruções de acesso no app", 10),
        ("Testar expiração, revogação e acesso por URL direta", 20),
    ],
    "P06": [
        ("Definir elegibilidade, convite e regras de inscrição", 6),
        ("Implementar autorização no backend do evento", 10),
        ("Integrar restrições no app e painel", 10),
        ("Testar convidados, pagamento, revogação e acesso direto", 16),
    ],
    "P07": [
        ("Definir elegibilidade de biblioteca e download", 6),
        ("Aplicar autorização de metadados e arquivo", 10),
        ("Integrar estados bloqueados e links temporários", 8),
        ("Testar expiração, revogação e compartilhamento de URL", 12),
    ],
    "L01": [
        ("Definir eventos auditáveis, retenção e dados excluídos do log", 8),
        ("Implementar gravação protegida de ator, data e alteração", 14),
        ("Integrar ações administrativas contratadas ao mecanismo", 12),
        ("Construir consulta com filtros e controle de acesso", 10),
        ("Testar integridade, exposição de dados e retenção", 12),
    ],
    "R01": [
        ("Definir o que conta como visualização e fonte do evento", 6),
        ("Instrumentar captura sem duplicar eventos de navegação", 10),
        ("Agregar dados por curso, aula e período", 8),
        ("Construir filtros e visualização administrativa", 8),
        ("Testar contagem, privacidade e desempenho inicial", 12),
    ],
    "R02": [
        ("Definir conclusão e campos do relatório", 4),
        ("Consultar e agregar progresso com autorização", 8),
        ("Construir filtros e exportação de conclusões", 8),
        ("Testar períodos, filtros e consistência com B07", 8),
    ],
    "R03": [
        ("Definir agregação, amostra e exibição de opiniões", 4),
        ("Implementar consultas sobre avaliações C09", 6),
        ("Construir indicadores e filtros administrativos", 8),
        ("Testar amostra vazia, atualização e privacidade", 8),
    ],
    "R04": [
        ("Definir evento qualificante e janelas DAU/MAU", 8),
        ("Instrumentar captura com deduplicação por usuário", 10),
        ("Implementar agregações e tratamento de fuso", 10),
        ("Construir painel e filtros por período", 8),
        ("Testar múltiplos dispositivos e consistência dos indicadores", 12),
    ],
    "R05": [
        ("Definir online, intervalo de heartbeat e tolerância", 8),
        ("Implementar presença e expiração de conexões", 18),
        ("Deduplicar sessões e dispositivos por usuário", 12),
        ("Construir indicador administrativo e atualização", 12),
        ("Testar desconexão, reconexão e limites de concorrência", 22),
        ("Documentar limitações de precisão e custos de presença", 6),
    ],
    "GM01": [
        ("Definir eventos elegíveis e restrições das plataformas de vídeo", 8),
        ("Modelar extrato e regras de pontuação", 10),
        ("Implementar concessão idempotente e reversão definida", 14),
        ("Construir configuração administrativa básica", 10),
        ("Integrar consulta de saldo e atividades", 8),
        ("Testar repetição, exploração básica e alterações de conteúdo", 14),
    ],
    "GM02": [
        ("Definir regra de presença elegível e reversão", 4),
        ("Integrar check-in confirmado ao extrato de pontos", 8),
        ("Exibir confirmação da pontuação no evento", 4),
        ("Testar duplicidade e cancelamento de presença", 10),
    ],
    "GM03": [
        ("Definir períodos, desempate e consentimento público", 6),
        ("Implementar agregação e consulta paginada", 10),
        ("Construir ranking e estados de ausência de dados", 10),
        ("Aplicar opt-out e restringir dados expostos", 6),
        ("Testar empate, períodos e acesso público", 10),
    ],
    "GM04": [
        ("Definir posição exibida e integração com privacidade", 4),
        ("Consultar saldo e posição usando motor e ranking existentes", 6),
        ("Construir componente de pontuação no perfil", 4),
        ("Testar ausência de posição e consistência do saldo", 8),
    ],
}

acceptance = {
    "F01": "Cada feature planejada está ligada a um épico, a critérios de aceite e a tarefas; decisões não resolvidas têm responsável e não são tratadas como aprovadas.",
    "F02": "Fluxos essenciais têm telas e estados associados; o diagrama explicita entidades e relações, e decisões de autorização correspondem às jornadas.",
    "F03": "O shell abre em Android/iOS, preserva navegação e mostra estados globais de erro sem acesso a rotas protegidas por sessão inválida.",
    "F04": "Uma conta sem papel administrativo é recusada tanto pela rota quanto pela operação de servidor.",
    "F05": "Migrações reproduzem o ambiente e políticas impedem leitura ou alteração de registros de outro usuário.",
    "F06": "Builds assinados são instalados nos ambientes de teste; submissões e pendências das lojas são registradas sem garantir aprovação.",
    "F07": "Os fluxos integrados contratados têm evidência de execução, problemas classificados e aceite ou pendência explícita dos responsáveis.",
    "B01": "Somente cursos publicados e elegíveis aparecem; destaque navega ao curso correto, e vitrines M01–M03 não são embutidas como entrega gratuita de B01.",
    "B02": "Sessão expirada não permite operação protegida; link de recuperação inválido ou expirado é rejeitado, sem revelar se um e-mail existe.",
    "B03": "Mensagem transacional usa remetente autenticado e link correto; falha de envio é observável sem registrar segredos.",
    "B04": "Usuário altera somente o próprio perfil; e-mail novo exige verificação e arquivo inválido não é aceito como foto.",
    "B05": "Aceite e revogação persistem com versão e data; a escolha pode ser consultada sem implicar disparos de campanha.",
    "B06": "A ordem curso/módulo/aula é consistente com o painel; conteúdo não publicado não é exposto por consulta direta.",
    "B07": "Repetir um evento de conclusão não duplica progresso e a conclusão pertence exclusivamente ao usuário autenticado.",
    "B08": "Publicar uma aula válida a disponibiliza na ordem correta; usuário sem permissão não consegue publicar por chamada direta.",
    "A01": "Desafio TOTP válido concede o nível de sessão esperado; código inválido é rejeitado e remoção exige autenticação adequada.",
    "A02": "Cancelamento do OAuth retorna ao app sem sessão indevida; vínculo de identidade não toma outra conta.",
    "A03": "Conta fora do tenant permitido é recusada quando houver restrição; redirecionamento retorna ao app correto.",
    "M01": "Publicar destaque abre o destino configurado; o card não concede biblioteca E01 nem direito de download.",
    "M02": "Destaque mostra data e destino corretos sem presumir inscrição EV01.",
    "M03": "Banner só aparece durante sua vigência no fuso definido e não implementa checkout ou motor de cupons.",
    "C01": "Player oficial reproduz vídeo permitido e trata vídeo indisponível; não existe download, remoção de marca nem promessa de proteção privada.",
    "C02": "Vídeo em processamento não é oferecido como pronto; token expirado ou usuário sem direito não obtém autorização válida de reprodução.",
    "C03": "Download interrompido pode ser retomado sem arquivo corrompido; logout e expiração obedecem à política possível, e reprodução offline não é prometida como DRM inviolável.",
    "C04": "Só aluno elegível recebe certificado; nova solicitação não duplica a emissão e código de verificação corresponde ao documento.",
    "C05": "Servidor corrige tentativa sem confiar na nota enviada pelo app; política de limite e repetição é respeitada.",
    "C06": "Saída inválida do modelo não vira quiz publicado; toda sugestão exige revisão humana antes de entrar em C05.",
    "C07": "Consulta não recupera material de curso não autorizado; resposta apresenta referência disponível e ausência de base é sinalizada.",
    "C08": "Só autor ou moderador autorizado altera/remove comentário; paginação não perde nem duplica respostas.",
    "C09": "Há no máximo uma avaliação vigente por aluno/curso conforme regra aprovada, com nota dentro da escala.",
    "E01": "Arquivo e capa inválidos são recusados; consulta e download seguem a autorização base, sem implementar P07 implicitamente.",
    "N01": "Token inválido é tratado; tocar em notificação abre destino permitido, sem acesso de usuário anterior após logout.",
    "N02": "Prévia e envio usam a mesma definição de público; reprocessar campanha não duplica envio no mecanismo contratado.",
    "N03": "Reexecutar job não repete ação já concluída; cancelar fluxo impede novos disparos pendentes conforme estado.",
    "G01": "Convite abre apenas o link oficial configurado; nenhum disparo ou participação automática é efetuado.",
    "G03": "Usuário sem vínculo não consulta publicação privada; conteúdo moderado deixa de aparecer conforme política.",
    "G04": "Não participante não lê conversa e bloqueio impede novos contatos conforme regra; reconexão mantém ordem e evita duplicação lógica.",
    "G05": "Sem opt-in não existe exposição pública; revogação remove o perfil dos caminhos públicos e da busca.",
    "G06": "Pesquisa retorna apenas perfis publicáveis e respeita opt-out e paginação.",
    "EV01": "Duas inscrições concorrentes não excedem vagas e uma mesma pessoa não gera duplicação indevida.",
    "EV02": "QR identifica inscrição não previsível sem expor dados pessoais; inscrição cancelada não é tratada como válida.",
    "EV03": "Convite tem destinatário e evento corretos; reenvio e falha são registrados usando B03 compartilhado.",
    "EV04": "QR de outro evento é recusado e segundo check-in não duplica presença; rede ausente mostra falha, não confirmação fictícia.",
    "P01": "Webhook sem assinatura válida não altera pedido; repetição e evento fora de ordem não geram efeitos duplicados.",
    "P02": "Cancelamento e renovação refletem estado do provedor e política de acesso; aprovação de estratégia por canal precede implementação.",
    "P03": "Somente pagamento confirmado concede o direito correto; estorno segue política aprovada e não libera outro curso.",
    "P04": "Pagamento e expiração de reserva mantêm vagas consistentes; cobrança sem confirmação não representa ingresso válido.",
    "P05": "Acesso direto à aula e ao vídeo verifica direito no servidor; revogação e expiração não dependem apenas da interface.",
    "P06": "Convite ou elegibilidade é validado antes da inscrição protegida, inclusive em chamada direta.",
    "P07": "URL de arquivo só é emitida para usuário elegível e expira conforme política; não se promete revogação de arquivo já baixado.",
    "L01": "Registro contém ator, momento e operação, sem senha ou token; acesso ao histórico exige permissão e usuário comum não o altera.",
    "R01": "Contagem segue definição de visualização e não soma navegação repetida como eventos distintos sem critério.",
    "R02": "Conclusões exportadas correspondem ao progresso B07, aos filtros e ao período exibido.",
    "R03": "Indicadores correspondem às avaliações C09 e distinguem ausência de avaliação de nota zero.",
    "R04": "Mesmo usuário em vários dispositivos conta uma vez na janela definida, com limites de dia/mês no fuso aprovado.",
    "R05": "Conexão expirada deixa de contar após tolerância definida; sessões simultâneas do mesmo usuário seguem a regra de deduplicação.",
    "GM01": "Evento repetido concede pontos uma vez; regras não recompensam assistir ao player YouTube em desacordo com políticas.",
    "GM02": "Somente check-in confirmado concede pontos, uma vez por usuário/evento.",
    "GM03": "Empates seguem regra aprovada, período filtra corretamente e usuário sem consentimento não é exposto.",
    "GM04": "Saldo e posição correspondem a GM01/GM03; perfil sem ranking apresenta estado explícito, não posição inventada.",
}


def enrich_acceptance():
    for code, criterion in acceptance.items():
        path, = ROOT.glob(f"{code}-*.md")
        text = path.read_text()
        if "## Cenário mínimo específico de aceite" not in text:
            text += f"\n## Cenário mínimo específico de aceite\n{criterion}\n"
        path.write_text(text)


def apply():
    if any("## Revisão técnica de esforço" in path.read_text()
           for path in ROOT.glob("[A-Z]*-*.md")):
        raise SystemExit("Revisão já aplicada. Edite as specs diretamente e execute gerar_catalogo.py; não sobrescrever revisões.")
    changes = []
    for code, tasks in review.items():
        path, = ROOT.glob(f"{code}-*.md")
        text = path.read_text()
        old_match = re.search(r"\| \*\*Total\*\* \| \*\*(\d+)(?: h)?\*\*", text)
        old = int(old_match.group(1))
        new = sum(hours for _, hours in tasks)
        if new < old:
            raise ValueError(f"{code}: redução não autorizada")
        table = ("## Tarefas para validação\n"
                 "| ID | Tarefa e entrega verificável | Horas propostas | Status |\n"
                 "|---|---|---:|---|\n")
        table += "\n".join(
            f"| {code}-T{i:02} | {task} | {hours} | Revisão técnica preliminar |"
            for i, (task, hours) in enumerate(tasks, 1))
        table += f"\n| **Total** | | **{new} h** | **Aprovação pendente** |\n"
        text = re.sub(r"## Tarefas para validação\n.*?(?=\n## |\Z)", table, text, flags=re.S)
        # Preserve o histórico e os demais campos do usuário, mas explicite o total vigente.
        text = re.sub(r"\n## Revisão técnica de esforço.*", "", text, flags=re.S)
        text += f"""

## Revisão técnica de esforço — 16/11/2026
Estimativa provável revisada: **{new} h**. Estimativa anterior: {old} h.
As horas da tabela acima substituem a distribuição inicial e são esforço de uma
pessoa, não prazo contratual. A ampliação cobre fluxos, autorização, falhas e
testes específicos que não estavam explicitados no rascunho.
As referências históricas no texto e no catálogo de origem não são o total vigente.
As tarefas estão sujeitas a revisão e aprovação; não foram executadas.

### Critérios de aceite transversais
- Entrega específica descrita em cada tarefa demonstrada em ambiente de homologação.
- Caminho principal e estados de vazio, erro e ausência de permissão verificados
  quando aplicáveis à interface e à integração.
- Regras de acesso aplicadas no servidor, não apenas ocultadas na interface.
- Testes da tarefa documentados e verificáveis; critérios funcionais específicos
  de negócio devem ser aprovados durante F01.
- Dependências, credenciais e decisões pendentes registradas antes de implementar.

### Limites da estimativa
Premissa: React Native/Expo Android e iOS, painel Next.js e backend Supabase;
uma implementação de referência e um ciclo de revisão por entrega. Recursos
do provedor e viabilidade técnica devem ser confirmados antes de compromisso.
Mudanças de escopo, integrações extras, migração de legado, tradução, DRM avançado,
funcionamento offline além do descrito e múltiplos gateways não estão implícitos.
Testes locais pertencem às features; F07 cobre integração, não repetição integral
dos mesmos testes. F01/F02 cobrem planejamento geral; tarefas de detalhamento
das features tratam decisões técnicas específicas e não repetem a descoberta.
Sem contingência percentual automática e sem custos de fornecedores incluídos.
"""
        path.write_text(text)
        changes.append((code, old, new))
    return changes


if __name__ == "__main__":
    for code, old, new in apply():
        print(f"{code}: {old} -> {new} h")
    enrich_acceptance()
