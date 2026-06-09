---
name: descrever-chamados
description: Formata chamados atendidos no período a partir de texto copiado, classificando por tipo (suporte técnico ou negocial) e sistema
metadata:
  type: skill
  source: /home/estrazulas/git/mcp_test/mcp-gitlab
---

# Skill: Descrever Chamados

Quando invocado com `/descrever-chamados`, siga **rigorosamente** os passos abaixo para formatar e classificar os chamados atendidos no período.

## Fluxo de Execução

### 1. Solicitar o texto dos chamados

Peça ao usuário para **copiar e colar** o resultado dos chamados (ex: do sistema GLPI, relatório, planilha, etc.).

Mensagem padrão:
"Cole aqui o texto com os chamados que atendeu no período (copie e cole o resultado do sistema de chamados)."

### 2. Processar o texto colado

Analise o texto colado e **identifique cada chamado individualmente**. O formato esperado da entrada contém por linha/registro:

- Número do chamado (identificador numérico)
- Título/assunto (ex: "Não visualização de notas - Siggaa")
- Status (aberto, fechado, etc.)
- Responsável/atendente
- Datas (abertura, atualização, fechamento)
- Descrição/solicitação
- Solicitante

Extraia de **cada chamado**:
- **Número** do chamado
- **Título** — use como base para a descrição
- **Descrição** — use para entender o contexto (pode ajudar a inferir tipo e sistema)

### 3. Classificar cada chamado

Para **cada chamado**, determine:

#### a) Tipo (suporte tecnico ou negocial)

Analise o título e a descrição do chamado para inferir o tipo:

| Pista | Tipo |
|---|---|
| Dúvidas sobre uso, orientações, perguntas, "como fazer" | **negocial** |
| Solicitações de acesso, permissão, cadastro, liberação | **negocial** |
| Pedidos de revisão de acesso, ajuste de perfil | **negocial** |
| Erros, mensagens de erro, "não está funcionando" | **tecnico** |
| Comportamento inesperado, "não aparece", "sumiu", "não carrega" | **tecnico** |
| Problemas de visualização, falha no sistema, tela em branco | **tecnico** |
| "Não consigo", "parou de funcionar" (indicando erro/bug) | **tecnico** |

**Regra:** Se houver **dúvida** sobre o tipo de um chamado específico, **Pergunte ao usuário** antes de prosseguir. Exemplo: "O chamado XXXX — 'título do chamado' — seria suporte técnico ou negocial?"

#### b) Sistema

Tente inferir o sistema a partir do título e descrição. Use seu conhecimento genérico para classificar (ex: sistema acadêmico, portal, ERP, intranet, sistema de vendas, etc.).

**Regra:** Se **não for possível inferir** o sistema, pergunte ao usuário qual sistema está relacionado àquele chamado.

### 4. Formatar a saída

Para cada chamado, formate UMA linha no seguinte padrão:

```
- XXXX - descricao do chamado - tipo(suporte tecnico ou negocial) - sistema
```

Onde:
- **XXXX**: número do chamado (apenas os dígitos)
- **descricao do chamado**: utilizar preferencialmente o **título**, ajustado se necessário para ficar mais claro (pode encurtar ou complementar com base na descrição)
- **tipo**: "suporte tecnico" ou "suporte negocial" (exatamente como escrito, sem acentos)
- **sistema**: nome do sistema inferido (ex: portal, erp, academico, vendas, infraestrutura, etc.)

### 5. Apresentar o resultado final

Apresente ao usuário a lista completa formatada. Exemplo de saída esperada:

```
- 34142 - Não visualização de notas - suporte tecnico - academico
- 34383 - Acesso ao modulo de cadastro - suporte negocial - erp
- 34000 - Acesso ao servidor de arquivos - suporte negocial - infraestrutura
- 32201 - Perfil Administrador no sistema de vendas - suporte negocial - vendas
- 33421 - Erro ao gerar relatorio financeiro - suporte tecnico - erp
```

Após a lista, **resuma**:
- Total de chamados no período
- Quantos de suporte técnico
- Quantos de suporte negocial

### 6. Formato alternativo de entrada

Se o usuário colar em formato diferente do esperado (JSON, tabela, lista numerada), adapte-se — o importante é extrair corretamente número, título e descrição de cada chamado.

## Regras importantes

- **NUNCA** invente informações. Use apenas o que foi fornecido no texto colado.
- **SEMPRE** use o título como descrição principal.
- Se o título for muito genérico ("Chamado 1234", "Solicitação"), use a descrição para complementar.
- Se houver **dúvida** sobre o tipo ou sistema, **Pergunte** — não assuma.
- Os tipos devem ser escritos exatamente como: "suporte tecnico" e "suporte negocial" (sem acentos, tudo minúsculo).
- O sistema deve ser escrito em **minúsculo**.
