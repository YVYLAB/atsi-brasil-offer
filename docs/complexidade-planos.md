# Complexidade dos planos

A apresentação comercial distingue os presets por **complexidade relativa
entre os planos**:

- Essencial: **Baixa**.
- Plus: **Média**.
- Premium: **Alta**.

Essa classificação substitui a média arredondada no indicador dos presets.
Não é uma avaliação absoluta de risco: um aplicativo Android/iOS/web com
autenticação e cursos continua exigindo engenharia e validação mesmo no Essencial.
Não se alteram as notas técnicas de cada feature na escala de 1–5.

Ao personalizar o escopo, o indicador passa explicitamente para **Complexidade
média** e usa a média aritmética das notas das funcionalidades selecionadas,
sem a fundação, com os rótulos técnicos existentes. Não herda a classificação
relativa do plano de origem e não promete um nível global de risco.

`scopeComplexity()` no `home.html` centraliza o indicador e o critério nos dados
de proposta. Cards dos presets e resumo informam o caráter relativo da
classificação. Horas, preços, prazos e regras promocionais não mudam.
