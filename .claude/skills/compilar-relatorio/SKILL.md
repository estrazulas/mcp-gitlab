---
name: compilar-relatorio
description: Compila relatório final combinando plano de trabalho (issues GitLab) e descrição de chamados, salvando em gen/DDMMAAAA/
metadata:
  type: skill
  source: /home/estrazulas/git/mcp_test/mcp-gitlab
---

# Skill: Compilar Relatório

Quando invocado com `/compilar-relatorio`, siga **rigorosamente** os passos abaixo para compilar o relatório final a partir de duas skills existentes (`/plano-trabalho` e `/descrever-chamados`) e salvar o resultado na pasta `gen/`.

## Fluxo de Execução

### 1. Coletar informações do período

O usuário pode informar o período inline no prompt ao invocar `/compilar-relatorio`. Exemplos:

- `/compilar-relatorio 01/06/2026-30/06/2026`
- `/compilar-relatorio 01/06/2026 a 30/06/2026`
- `/compilar-relatorio periodo:01/06/2026 ate 30/06/2026`
- `/compilar-relatorio 10/05/2026-15/05/2026 label:"Minha Label" projeto:grupo/meu-projeto`

**Regras de extração inline:**

| Padrão no texto | Extrair |
|---|---|
| `DD/MM/AAAA-DD/MM/AAAA` (datas separadas por hífen) | data inicial e data final |
| `DD/MM/AAAA` seguido de ` a ` ou ` ate ` ou ` até ` seguido de `DD/MM/AAAA` | data inicial e data final |
| `periodo:` ou `período:` seguido de `DD/MM/AAAA` ... `DD/MM/AAAA` | data inicial e data final |

Se o período não foi informado inline, pergunte ao usuário em duas etapas:

**Pergunta 1 — Data inicial:**
"Qual a **data inicial** do período? (formato: DD/MM/AAAA)"

Aguarde a resposta.

**Pergunta 2 — Data final:**
"Qual a **data final** do período? (formato: DD/MM/AAAA)"

Aguarde a resposta.

> Se ambos já foram informados inline, não pergunte — prossiga direto.

**Valide as datas:** confirme se são datas válidas (dia 01-31, mês 01-12, ano 4 dígitos). Se inválidas, peça para corrigir.

### 2. Definir o nome do diretório

O diretório de saída será `gen/DDMMAAAA/` onde `DDMMAAAA` é a **data inicial** no formato DDMMAAAA (sem barras).

Exemplo: período `01/06/2026 - 30/06/2026` → diretório `gen/01062026/`

### 3. Coletar filtros para o plano de trabalho

Pergunte ao usuário que filtros deseja usar para buscar as issues no GitLab. Os mesmos filtros do `/plano-trabalho`:

**Pergunta 3 — Label/Tag:**
"Qual label/tag deseja filtrar nas issues? (ex: back-end, front-end, urgencia, melhoria, bug, ou deixe vazio para trazer todas)"

Aguarde a resposta.

**Pergunta 4 — Projetos:**
"Quais projetos? Informe o nome ou parte do nome (ex: meu-projeto, grupo/projeto). Pode informar múltiplos separados por vírgula. Deixe vazio para trazer de todos os projetos."

Aguarde a resposta.

**Pergunta 5 — Situação:**
"Qual situação das issues? (aberta, fechada, todas)"

Aguarde a resposta.

**Pergunta 6 — Milestone:**
"Qual milestone deseja filtrar? Informe o nome ou deixe vazio para trazer todas."

Aguarde a resposta.

> **Simplificação:** se o usuário informou filtros inline (ex: `label:"Minha Label" projeto:grupo/meu-projeto situacao:abertas milestone:06/26`), pule as perguntas correspondentes e já use esses valores. Os identificadores seguem o mesmo padrão do `/plano-trabalho`:
> - `label:` — Label/Tag
> - `projeto:` ou `projetos:` — Nome do(s) projeto(s)
> - `situacao:` ou `situação:` — Situação
> - `milestone:` — Milestone

### 4. Executar a skill plano-trabalho

Invoque a skill `/plano-trabalho` usando a ferramenta `Skill` com os filtros coletados.

**Importante:** ao invocar o `/plano-trabalho`, forneça **todos os filtros inline** já no prompt para evitar que a skill pergunte novamente. Exemplo:

> Skill tool: skill="plano-trabalho", args="label:Minha Label projeto:grupo/meu-projeto situacao:fechadas milestone:06/26"

Aguarde o resultado completo da skill (a lista de issues formatada).

> Se a skill retornar erro (ex: MCP indisponível), informe o erro ao usuário e pergunte se deseja continuar com o relatório apenas com chamados, ou cancelar.

### 5. Coletar o texto dos chamados

Peça ao usuário para copiar e colar o texto dos chamados atendidos no período (ex: do GLPI, relatório, planilha).

Mensagem: "Cole aqui o texto com os chamados que atendeu no período (copie e cole o resultado do sistema de chamados)."

Aguarde o usuário colar o texto.

### 6. Executar a skill descrever-chamados

Invoque a skill `/descrever-chamados` usando a ferramenta `Skill`. A skill solicitará o texto dos chamados — forneça o texto que o usuário colou no passo anterior.

Aguarde o resultado completo da skill (a lista de chamados formatada).

> Se a skill retornar erro, informe o erro ao usuário e pergunte se deseja continuar com o relatório apenas com issues, ou cancelar.

### 7. Compilar o relatório final

Monte o relatório final em Markdown com a seguinte estrutura:

```markdown
# Plano de Trabalho do Período {data_inicial} - {data_final}

**Data de geração:** {data_atual}

---

## 1. Issues do GitLab

{resultado completo da skill plano-trabalho}

---

## 2. Chamados Atendidos

{resultado completo da skill descrever-chamados}

---

## 3. Resumo Consolidado

### Issues
- **Total de issues no período:** {total}
- **Por tipo:** {detalhamento}

### Chamados
- **Total de chamados no período:** {total_chamados}
- **Suporte técnico:** {qtd_tecnico}
- **Suporte negocial:** {qtd_negocial}

---

*Relatório gerado automaticamente em {data_atual} via /compilar-relatorio*
```

**Regras para compilação:**

- O **resultado do plano-trabalho** no passo 1 deve incluir **desde o cabeçalho** (`# Plano de Trabalho - Issues do GitLab`) **até o final** (resumo quantitativo). Copie o conteúdo completo retornado pela skill e insira como uma seção aninhada (já está dentro de "## 1. Issues do GitLab").

- O **resultado dos chamados** no passo 2 também deve incluir o conteúdo completo retornado pela skill (desde a lista até o resumo com totais).

- Extraia do resultado de cada skill os números para preencher o Resumo Consolidado (total de issues, totais por tipo, total de chamados, divisão técnico/negocial). Se alguma skill não tiver sido executada com sucesso, indique "Não disponível" no consolidado.

### 8. Salvar o arquivo

Salve o relatório em:

```
gen/{DDMMAAAA}/plano-de-trabalho-{periodo}.md
```

Onde:
- `{DDMMAAAA}` é a data inicial no formato DDMMAAAA (ex: `01062026`)
- `{periodo}` é uma versão simplificada do período para o nome do arquivo (ex: `01-06-a-30-06-2026`)

Use a ferramenta `Write` para criar o arquivo.

> Crie o diretório `gen/{DDMMAAAA}/` se ele não existir (use `mkdir -p` via Bash).

### 9. Confirmar ao usuário

Após salvar, informe ao usuário:

"✅ Relatório salvo em `gen/{DDMMAAAA}/plano-de-trabalho-{periodo}.md`

**Resumo:**
- Período: {data_inicial} a {data_final}
- Issues encontradas: {total_issues}
- Chamados registrados: {total_chamados}"

## Regras importantes

- **SEMPRE** colha o período e os filtros primeiro, antes de executar as skills.
- **NUNCA** invente informações de chamados ou issues. Use apenas os resultados reais das skills.
- Se uma skill falhar, **informe o erro** ao usuário e **pergunte se deseja continuar** com o que já foi gerado.
- O formato do diretório é **sempre** `gen/DDMMAAAA/` (data inicial, sem barras, 8 dígitos).
- O título do relatório usa o período completo formatado (dd/mm/aaaa - dd/mm/aaaa).
- Se o diretório `gen/{DDMMAAAA}/` já existir, sobrescreva o arquivo (o usuário será informado).
