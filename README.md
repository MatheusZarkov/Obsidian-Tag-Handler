Aqui está a documentação atualizada para incluir ambos os scripts:

---

# Gerenciador de Tags para Obsidian - Documentação Completa

## Descrição Geral
Esta coleção de scripts Python foi desenvolvida para gerenciar automaticamente tags YAML em arquivos Markdown do Obsidian. Inclui funcionalidades para adicionar tags baseadas na estrutura de pastas e remover tags específicas conforme necessário.

## Scripts Disponíveis

### 1. **Tag_Handler_Obsidian.py** - Gerenciador Principal de Tags
Script principal que adiciona e atualiza tags baseadas na estrutura de pastas com tags aninhadas.

### 2. **Remove_Folder_Tags.py** - Removedor de Tags de Pastas
Script utilitário que remove apenas tags que correspondem a nomes de pastas existentes.

---

## Funcionalidades por Script

### Tag_Handler_Obsidian.py
1. **Tags Aninhadas Automáticas**
   - Cria tags com caminho completo das pastas (ex: `Sora/AI/Prompts/imagens`)
   - Atualiza automaticamente quando arquivos são movidos
   - Remove tags de localização antigas

2. **Preservação Inteligente**
   - Mantém todas as tags personalizadas existentes
   - Preserva outras propriedades YAML (título, autor, etc.)
   - Detecta e substitui apenas tags de caminho

3. **Processamento Completo**
   - Processa todos os níveis de pasta (não limitado a 2)
   - Execução automática sem confirmação
   - Relatório detalhado de alterações

### Remove_Folder_Tags.py
1. **Remoção Seletiva**
   - Remove apenas tags que coincidem com nomes de pastas
   - Preserva tags personalizadas que não são nomes de pastas
   - Solicita confirmação antes da execução

2. **Processamento Seguro**
   - Identifica automaticamente todas as pastas
   - Remove tags correspondentes de forma seletiva
   - Mantém outras propriedades YAML intactas

---

## Como Usar

### Instalação
1. Salve ambos os scripts na pasta raiz das suas notas do Obsidian
2. Certifique-se de ter Python 3 e a biblioteca `pyyaml` instalada

### Execução

**Para adicionar/atualizar tags aninhadas:**
```bash
python Tag_Handler_Obsidian.py
```

**Para remover tags de pastas específicas:**
```bash
python Remove_Folder_Tags.py
```

---

## Exemplos de Uso

### Exemplo 1: Tags Aninhadas (Tag_Handler_Obsidian.py)
**Estrutura de Pastas:**
```
📁 Pasta_Raiz
 ├── 📁 Sora
 │    └── 📁 AI
 │         └── 📁 Prompts
 │              └── 📄 imagens.md
 └── 📁 Trabalho
      └── 📁 Projetos
           └── 📄 cliente1.md
```

**Resultado para `Sora/AI/Prompts/imagens.md`:**
```yaml
---
tags:
  - Sora/AI/Prompts
  - importante  # tag personalizada preservada
---
```

### Exemplo 2: Remoção Seletiva (Remove_Folder_Tags.py)
**Antes** (com pastas: Sora, AI, Trabalho):
```yaml
---
tags:
  - Sora
  - importante
  - AI
  - revisão
---
```

**Depois:**
```yaml
---
tags:
  - importante
  - revisão
---
```

### Exemplo 3: Movimentação de Arquivo
**Arquivo movido de** `Sora/AI/arquivo.md` **para** `Trabalho/Projetos/arquivo.md`:

**Antes:**
```yaml
---
tags:
  - Sora/AI
  - importante
---
```

**Depois:**
```yaml
---
tags:
  - Trabalho/Projetos
  - importante
---
```

---

## Fluxo de Trabalho Recomendado

### Cenário 1: Limpeza Inicial
1. Execute `Remove_Folder_Tags.py` para remover tags antigas de pastas
2. Execute `Tag_Handler_Obsidian.py` para adicionar tags aninhadas atualizadas

### Cenário 2: Manutenção Regular
- Execute apenas `Tag_Handler_Obsidian.py` periodicamente
- O script detecta e corrige automaticamente tags desatualizadas

### Cenário 3: Reorganização de Pastas
1. Reorganize suas pastas conforme necessário
2. Execute `Tag_Handler_Obsidian.py`
3. Tags serão automaticamente atualizadas para refletir nova estrutura

---

## Detalhamento Técnico

### Tag_Handler_Obsidian.py
- **Detecção de Tags de Caminho**: Identifica tags que representam estrutura de pastas
- **Substituição Inteligente**: Remove apenas tags de caminho antigas
- **Geração de Tags Aninhadas**: Usa "/" como separador para estrutura completa
- **Processamento em Tempo Real**: Atualiza baseado na localização atual do arquivo

### Remove_Folder_Tags.py
- **Mapeamento de Pastas**: Escaneia toda estrutura de diretórios
- **Comparação Exata**: Remove tags que coincidem exatamente com nomes de pastas
- **Preservação de Contexto**: Mantém tags que não representam pastas

---

## Configurações e Personalizações

### Modificações Comuns

**Para ignorar pastas específicas:**
```python
# Adicione na lista de exclusões
if item_name in ['.obsidian', 'Templates', 'Archive']:
    continue
```

**Para alterar formato de tags:**
```python
# Altere o separador de "/" para outro caractere
nested_tag = '-'.join(clean_parts)  # Ex: Sora-AI-Prompts
```

---

## Limitações e Considerações

### Tag_Handler_Obsidian.py
- Executa automaticamente sem confirmação
- Substitui espaços por underscores nos nomes de pastas
- Processa recursivamente todos os subdiretórios

### Remove_Folder_Tags.py
- Solicita confirmação antes da execução
- Remove apenas correspondências exatas
- Operação irreversível

---

## Troubleshooting

### Problemas Comuns
1. **"Error parsing YAML"**: Verifique formatação do frontmatter
2. **Tags não atualizadas**: Certifique-se que o arquivo está na localização correta
3. **Permissões negadas**: Execute com permissões adequadas de escrita

### Recomendações de Segurança
- Faça backup antes de executar os scripts
- Teste em uma pasta pequena primeiro
- Verifique os relatórios após execução

---

## Requisitos Técnicos
- Python 3.x
- Biblioteca pyyaml (`pip install pyyaml`)
- Permissões de leitura/escrita nos arquivos
- Estrutura de pastas organizada

---
