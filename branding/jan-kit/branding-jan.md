# Branding de referência — JAN Implementos Agrícolas

> **Status:** guia de referência visual para abordagem comercial da YvyLab. Não é um brandbook oficial, e a paleta abaixo não foi divulgada pela JAN como manual cromático. Não transformar inferências em regras institucionais sem aprovação.

## 1. Empresa e posicionamento observável

- **Nome no site:** Jan Implementos Agrícolas / Implementos Agrícolas JAN S/A.
- **Origem/cidade:** Não-Me-Toque, Rio Grande do Sul, Brasil.
- **Atuação:** fabricação de implementos e máquinas agrícolas (distribuição, plantio, pulverização, preparo do solo, transporte de grãos e outras linhas).
- **Temas de conteúdo identificados no site:** assistência técnica, representantes, telemetria, produtos, notícias e formação de profissionais.
- **Frases presentes no site, para referência (sem apropriação comercial):** `Cultivamos Confiança` e, na telemetria, `Controle total. Produtividade máxima.`.
- **Cuidado com naming:** a JAN divulga iniciativa `+JAN`/`JAN Plus` para sua rede de revendas; não apresentar o nome como criação da YvyLab.

## 2. Linguagem visual observada

O recorte da página de contatos e as imagens públicas do site utilizam fundo claro/neutro, cartões brancos, títulos em azul-petróleo/cinza-antracite, links em laranja quente, linhas arredondadas e fotos de equipamentos e campo. A campanha `Presença` combina um tom azul-petróleo escuro, laranja e branco, com marca manuscrita sobre globo.

### Paleta de trabalho (aproximada)

| Token | Cor | Uso sugerido | Proveniência |
|---|---|---|---|
| `jan-ink` | `#2F3A3D` | textos/cabeçalhos | cor recorrente na captura da página de contato |
| `jan-deep` | `#24363F` | fundo escuro e gradientes | aproximação a partir do site/campanha |
| `jan-slate` | `#43545A` | bordas e elementos secundários | amostra da captura |
| `jan-orange` | `#FF8031` | links/CTAs e destaques | cor visível na captura, aproximada |
| `jan-surface` | `#F5F5F5` | fundo claro | amostra da captura |
| `jan-white` | `#FFFFFF` | cartões e textos em fundo escuro | amostra da captura |
| `jan-muted` | `#718088` | textos secundários | sugestão de contraste, não cor oficial |
| `jan-border` | `#DCE2E2` | divisórias e contornos | sugestão de UI, não cor oficial |

Para aplicações web com texto pequeno, verifique **WCAG AA**. Laranja claro em fundo branco pode não atingir contraste para texto comum; utilize tom mais escuro como `#A84600` para links pequenos, **somente como correção de acessibilidade da UI**, nunca alterando a cor da logo.

## 3. Assets originais publicamente identificados

| Arquivo da fonte | URL no domínio da JAN | Classificação |
|---|---|---|
| `logo-campanha-confianca-pt.svg` | https://www.jan.com.br/source/campanha/imagem/logo-campanha-confianca-pt.svg | Arte de campanha/rodapé; oficial no site, não necessariamente logo institucional mestre |
| `logo-presenca-pt.webp` | https://www.jan.com.br/source/campanha/imagem/logo-presenca-pt.webp | Arte da campanha Presença; não é o logo institucional isolado |

**Atenção:** o pacote não traz os bytes dos dois arquivos. Execute `scripts/baixar_assets_oficiais.py` em ambiente com acesso à internet e peça a versão oficial da assinatura institucional para produção.

## 4. Diretrizes de aplicação ao configurador comercial

- Apresentação deve ser **uma proposta personalizada para JAN**, identificada como demonstração desenvolvida pela **YvyLab**.
- Organizar em duas colunas: seções configuráveis à esquerda e mockup mobile à direita.
- Utilizar cores de referência com moderação: base escura azul-petróleo, acentos laranja, cards legíveis.
- Usar arte do site via imagem original, respeitando proporções; se indisponível, usar título tipográfico **`Proposta para JAN`**, não tentar reproduzir o símbolo.
- Destacar usos adequados à JAN: trilhas técnicas por modelo de máquina, treinamento de representantes, base de manuais/e-books, vídeos de operação/manutenção, eventos e certificações.
- Não inventar que a JAN já deseja ou contratou esses recursos: são oportunidades comerciais para validação.
- Diferenciar recursos gratuitos do pacote, opcionais e decisões exclusivas de entrega de vídeo.
- Preservar a estimativa e as dependências existentes do configurador; branding não altera cálculo de horas ou descontos.

## 5. Tipografia e layout

O site possui tipografia de aparência geométrica e forte nos títulos. Para um mockup, prefira `Inter`, `Arial` ou outra fonte já disponível, sem supor a família tipográfica oficial.

Sugestão de raio de UI: 12–18px em cartões, 24px em contêineres principais; espaçamento 8px; títulos com peso 700–800. Estes valores são **proposta da YvyLab**, não medidas da JAN.

## 6. Comunicação

Comunicar valor operacional: capacitação de concessionárias, técnicos de pós-venda, revendedores e clientes. O que se deseja demonstrar é uma plataforma de conhecimento **customizável com a marca da contratante**. Não registrar o nome `JAN+`, porque `JAN Plus` já aparece na comunicação existente da JAN.

## 7. Fontes

1. https://www.jan.com.br/contato — página de contatos e apresentação da interface.
2. https://www.jan.com.br/ — páginas de produtos, treinamento e comunicação institucional.
3. https://www.jan.com.br/telemetria — argumentos relacionados a tecnologia/produtividade.
4. https://www.jan.com.br/noticia/jan-inaugura-primeira-unidade-exclusiva-jan-plus-em-parceria-com-a-horizonte-maquinas — denominação `JAN Plus` em uso.
5. https://www.jan.com.br/noticia/primeira-revenda-com-novo-conceito-de-comunicacao-jan-e-inaugurada — ação `+JAN` em uso.

**Última conferência:** 17/11/2026. Recomenda-se reconfirmar assets e marcas antes de publicação.
