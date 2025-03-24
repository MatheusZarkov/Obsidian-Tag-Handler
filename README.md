## Descrição Geral
Este script Python foi desenvolvido para gerenciar automaticamente tags YAML em arquivos Markdown do Obsidian, baseando-se na estrutura de pastas onde os arquivos estão localizados.

## Funcionalidades Principais
1. **Gerenciamento Automático de Tags**
   - Adiciona tags baseadas nos dois primeiros níveis de pastas
   - Preserva tags personalizadas existentes
   - Remove apenas tags relacionadas a pastas quando arquivos são movidos

2. **Processamento Inteligente**
   - Ignora a pasta `.obsidian` e seu conteúdo
   - Processa apenas arquivos Markdown (.md)
   - Mantém formatação original dos arquivos
   - Evita linhas em branco extras após o frontmatter YAML

3. **Relatório de Alterações**
   - Mostra quais arquivos foram modificados
   - Lista tags adicionadas e removidas
   - Fornece um resumo final com total de arquivos processados

## Como Usar

1. **Instalação**
   - Salve o script como `Tag_Handler_Obsidian.py`
   - Coloque o arquivo na pasta raiz onde estão suas notas do Obsidian

2. **Execução**
   - Execute o script usando Python 3
   - Comando: `python Tag_Handler_Obsidian.py`

3. **Exemplo de Estrutura de Pastas Suportada**
```
📁 Pasta_Raiz (onde está o script)
 ├── 📁 Pessoal
 │    ├── 📁 Médico
 │    │    └── 📄 consulta.md
 │    └── 📁 Financeiro
 │         └── 📄 orcamento.md
 └── 📁 Trabalho
      └── 📁 Projetos
           └── 📄 projeto1.md
```

## Exemplos de Uso

### Exemplo 1: Arquivo Novo
**Localização**: `Pessoal/Médico/consulta.md`
**Resultado**:
```yaml
---
tags:
  - Pessoal
  - Médico
---
```

### Exemplo 2: Arquivo com Tags Existentes
**Antes** (`Pessoal/Médico/consulta.md`):
```yaml
---
tags:
  - Remédios
  - Pessoal
  - Médico
---
```

**Depois de Mover para** `Pessoal/arquivo.md`:
```yaml
---
tags:
  - Remédios
  - Pessoal
---
```

## Detalhamento Técnico do Funcionamento

1. **Identificação de Tags de Pasta**
   - Escaneia a estrutura de diretórios
   - Identifica todos os nomes de pastas possíveis
   - Converte espaços em underscores nos nomes das tags

2. **Processamento de Arquivos**
   - Lê o conteúdo do arquivo
   - Identifica frontmatter YAML existente
   - Preserva tags personalizadas
   - Atualiza tags baseadas na localização atual

3. **Gerenciamento de Conteúdo**
   - Mantém formatação original
   - Evita duplicação de tags
   - Remove espaços em branco desnecessários

4. **Sistema de Relatório**
   - Registra alterações por arquivo
   - Mostra tags adicionadas/removidas
   - Fornece estatísticas de processamento

## Limitações e Observações
- Processa apenas os dois primeiros níveis de pastas
- Funciona apenas com arquivos Markdown
- Requer Python 3
- Necessita da biblioteca `pyyaml`

## Recomendações de Uso
1. Faça backup antes de executar o script
2. Verifique os relatórios após a execução
3. Use nomes de pasta sem caracteres especiais
4. Mantenha o script na pasta raiz das suas notas

## Mensagens de Erro Comuns
- "Error reading file": Problema ao ler o arquivo
- "Error parsing YAML": Frontmatter YAML mal formatado
- "Error writing to file": Problema ao salvar alterações

## Requisitos Técnicos
- Python 3.x
- Biblioteca pyyaml
- Sistema de arquivos com permissões de leitura/escrita

## Suporte
Este script é de código aberto e pode ser modificado conforme necessário para atender requisitos específicos.
