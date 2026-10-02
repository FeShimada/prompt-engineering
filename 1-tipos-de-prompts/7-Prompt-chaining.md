# Prompt Chaining

Divide uma tarefa em etapas sequenciais, onde a saída de uma é a entrada da próxima.

## Quando utilizar:

- Converter texto → traduzir → resumir.
- Gerar schema → endpoints → código em Go.
- Analisar logs em etapas: parsing → classificação → resposta.
- Criar fluxo de agente com passos definidos.
- Organizar raciocínio complexo em pipeline.

## Limitações:

- Mais latência por múltiplas etapas.
- Propaga erro de uma etapa para as seguintes.
- Aumenta custo de tokens.
- Depende de parsing correto.
- Complexidade de orquestração.
