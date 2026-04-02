# Prompt para gerar relatório de issues

Use o MCP `gitlab-issues` para montar um relatório de issues trabalhadas com estas regras:

- Projetos: `dsi/ingresso` e `dsi/ingresso-ifc`
- Milestone: `03/26`
- Assignee: `daniel.estrazulas`
- Considere `state=all` para trazer issues abertas e fechadas
- Não consulte novamente se os dados já foram obtidos
- Não inclua cabeçalho, introdução ou resumo adicional
- Não mostre URL completa; use apenas o formato `projeto/-/issues/nrissue`
- Separe o resultado por projeto
- Dentro de cada projeto, separe as issues em dois grupos:
  - `Especificação` quando a issue tiver a label `Requisitos`
  - `Desenvolvimento` quando não tiver a label `Requisitos`
- Se um projeto não tiver issues de um dos tipos, não exiba esse grupo

Formato esperado de saída:

```markdown
Projeto: dsi/ingresso

Desenvolvimento
- Desenvolvimento - Título da issue
  dsi/ingresso/-/issues/99

Projeto: dsi/ingresso-ifc

Especificação
- Especificação - Título da issue
  dsi/ingresso-ifc/-/issues/17

Desenvolvimento
- Desenvolvimento - Título da issue
  dsi/ingresso-ifc/-/issues/99
```

Regras finais:

- O texto da linha da issue deve começar com `Especificação -` ou `Desenvolvimento -`
- Mantenha o título original da issue após o prefixo
- Preserve a ordem por projeto e por tipo
- Não adicione explicações fora da lista final