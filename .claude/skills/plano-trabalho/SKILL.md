---
name: plano-trabalho
description: Cria resumo de plano de trabalho a partir de issues do GitLab usando template padronizado
metadata:
  type: skill
  source: /home/estrazulas/git/mcp_test/mcp-gitlab
---

# Skill: Plano de Trabalho

Quando invocado com `/plano-trabalho`, siga **rigorosamente** os passos abaixo para criar um resumo de plano de trabalho a partir de issues do GitLab.

## Fluxo de Execução

### 1. Coletar informações do usuário

#### 1a. Verificar filtros informados inline

O usuário pode ter informado filtros diretamente no prompt ao invocar `/plano-trabalho`. Exemplos:

- `/plano-trabalho label:back-end projeto:grupo/meu-projeto`
- `/plano-trabalho label:bug,urgencia projeto:grupo/projeto-a,grupo/projeto-b situacao:fechadas milestone:06/26`
- `/plano-trabalho label:"Minha Label"`

Extraia os valores usando estes identificadores no texto (case insensitive):

| Identificador | Filtro |
|---|---|
| `label:` | Label/Tag (se múltiplos, separados por vírgula) |
| `projeto:` ou `projetos:` | Nome do(s) projeto(s) (separados por vírgula) |
| `situacao:` ou `situação:` | Situação (aberta, fechada, todas) |
| `milestone:` | Milestone |

Se um valor estiver entre aspas (`"..."`), use o conteúdo inteiro como um valor único (ex: `label:"Minha Label"` → label = "Minha Label").

#### 1b. Perguntar apenas o que não foi informado

Use os valores extraídos inline como filtros iniciais. Para cada filtro **não** informado no prompt, faça UMA pergunta por vez, aguardando a resposta antes de prosseguir:

**Pergunta 1 — Label/Tag (se não veio inline):**
"Qual label/tag deseja filtrar? (ex: back-end, front-end, urgencia, melhoria, bug, ou deixe vazio para trazer todas)"

Aguarde a resposta.

**Pergunta 2 — Projetos (se não veio inline):**
"Quais projetos? Informe o nome ou parte do nome (ex: meu-projeto, grupo/projeto). Pode informar múltiplos separados por vírgula. Deixe vazio para trazer de todos os projetos que você tem acesso."

Aguarde a resposta.

**Pergunta 3 — Situação (se não veio inline):**
"Qual situação das issues? (aberta, fechada, todas)"

Aguarde a resposta.

**Pergunta 4 — Milestone (se não veio inline):**
"Qual milestone deseja filtrar? Informe o nome ou deixe vazio para trazer todas as issues sem filtrar por milestone."

Aguarde a resposta.

> **Importante:** Se todos os filtros já tiverem sido informados inline, não faça nenhuma pergunta — prossiga direto para o passo 2.

### 2. Extrair usuário do .user

Leia o arquivo `.user` do projeto usando a ferramenta Read (não use outros meios). Extraia o valor da variável `GITLAB_USER` (formato: `GITLAB_USER = valor`).

> Se o arquivo `.user` não existir ou `GITLAB_USER` não estiver configurado, informe o erro ao usuário e peça para criar um arquivo `.user` baseado em `.user.example`.

### 3. Buscar projetos usando MCP

Use a ferramenta `list_projects` do MCP do GitLab para listar os projetos disponíveis.

- Se o usuário informou nomes de projetos, filtre os resultados comparando com o campo `name` ou `path_with_namespace` (case insensitive, contém).
- Se não informou, use todos os projetos retornados.
- Se nenhum projeto encontrado, informe e encerre.

> **IMPORTANTE:** Use **APENAS** as ferramentas MCP do GitLab (`list_projects` e `list_issues`). Não use GitHub, APIs externas ou outras ferramentas de busca.

### 4. Buscar issues usando MCP

Para cada projeto identificado, use a ferramenta `list_issues` do MCP do GitLab com os seguintes parâmetros:

- `project_id`: o `path_with_namespace` do projeto (ex: `grupo/meu-projeto`)
- `labels`: a label informada pelo usuário (se houver, separada por vírgulas se múltiplas)
- `state`: a situação informada (opened, closed, ou all)
- `milestone`: a milestone informada pelo usuário (se houver; se vazio, não enviar o parâmetro)
- Demais parâmetros opcionais não preenchidos

### 5. Classificar cada issue por tipo

Para cada issue retornada, determine o tipo analisando as `labels` do array:

| Condição | Tipo |
|---|---|
| A lista `labels` contém "requisitos" (case insensitive) | **Requisitos** |
| A lista `labels` contém "desempenho" (case insensitive) | **Desempenho** |
| Nenhuma das anteriores (labels vazias ou outros valores) | **Desenvolvimento** |

> Se uma issue tiver múltiplas labels conflitantes (ex: "requisitos" e "desempenho"), pergunte ao usuário qual considerar.

### 6. Montar o resumo no template

Para cada issue, formate no template abaixo:

```
#{iid} - {title}
Tipo: {Desenvolvimento|Requisitos|Desempenho}
Sistema: {path_with_namespace do projeto}
Url: {web_url da issue}

Resumo: {explicação do objetivo/propósito da issue}
```

**Regras para o Resumo:**

- **Leia todo o conteúdo do `description`** da issue (não apenas as primeiras linhas). O description pode conter histórias de usuário ("Como um..., eu quero..., para que..."), objetivos de negócio, critérios de aceitação, seções de "Objetivo" ou "User Story".

- A partir da leitura completa do description, **escreva uma explicação coesa em linguagem natural** que responda: **"O que esta issue visa alcançar? Qual é o seu propósito?"**

- **NÃO** cole o conteúdo do description verbatim — nem histórias de usuário no formato "Como um...", nem textos crus de "objetivo de usuário de negócio".

- O resumo deve ser uma **síntese explicativa**, como nos exemplos abaixo:

  **Exemplo (issue sobre impedir alteração de formulário):**
  > Define requisitos para impedir a alteração do formulário de ações afirmativas de uma oferta de curso quando já existirem inscrições vinculadas, garantindo a integridade dos dados das inscrições realizadas.

  **Exemplo (issue sobre questionário personalizado):**
  > Implementa a funcionalidade de questionário de inscrição personalizado por processo e oferta, permitindo selecionar formulários distintos para cada nível do cadastro.

- Mantenha o resumo conciso (máximo 3 linhas / ~250 caracteres).
- Se o `description` for vazio, vazio, None ou contiver apenas texto não informativo, use o próprio `title` da issue como resumo.

### 7. Apresentar o resultado

Apresente o resumo completo com:

1. Um cabeçalho: `# Plano de Trabalho - Issues do GitLab`
2. Os filtros utilizados (label, projetos, situação, milestone, usuário)
3. Uma linha em branco
4. As issues formatadas no template, separadas por uma linha em branco entre cada uma
5. Ao final, um resumo quantitativo:
   - Total de issues encontradas
   - Quantas de cada tipo (Desenvolvimento, Requisitos, Desempenho)
   - Quantas por projeto

### Exemplo do template (baseado na issue #98)

```
#98 - Relatório de Vendas - Dashboard
Tipo: Desenvolvimento
Sistema: grupo/meu-projeto
Url: grupo/meu-projeto/-/issues/98

Resumo: Cria dashboard para visualização de relatório de vendas com filtros por período, região e categoria de produto.
```

## Regras importantes

- **NUNCA** use APIs externas ou ferramentas que não sejam as MCP do GitLab (list_projects, list_issues).
- Só faça perguntas para os filtros que **não** foram informados inline no prompt.
- Se precisar perguntar, faça **UMA pergunta por vez**, aguardando a resposta antes de prosseguir.
- Se algo não estiver claro, **PERGUNTE** — não assuma nada.
- Se houver erro de conexão com o MCP, informe claramente ao usuário.
- Se o token estiver expirado (erro 401), informe ao usuário.
- Se a busca retornar 0 issues, informe "Nenhuma issue encontrada com os filtros informados."
