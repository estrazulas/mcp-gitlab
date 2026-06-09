# Prompt para gerar relatório de issues

Use o MCP `gitlab-issues` para montar um relatório das issues do GitLab com estas regras:

- Use os projetos, milestone, labels e assignee que o usuário fornecer
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
Projeto: grupo/meu-projeto

Desenvolvimento
- Desenvolvimento - Título da issue
  grupo/meu-projeto/-/issues/99

Projeto: grupo/outro-projeto

Especificação
- Especificação - Título da issue
  grupo/outro-projeto/-/issues/17

Desenvolvimento
- Desenvolvimento - Título da issue
  grupo/outro-projeto/-/issues/99
```

Regras finais:

- O texto da linha da issue deve começar com `Especificação -` ou `Desenvolvimento -`
- Mantenha o título original da issue após o prefixo
- Preserve a ordem por projeto e por tipo
- Não adicione explicações fora da lista final
