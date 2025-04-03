# Internacionalização do FlowTube

Este documento explica como o sistema de internacionalização (i18n) foi implementado no aplicativo FlowTube.

## Visão Geral

O FlowTube suporta múltiplos idiomas:
- Inglês (padrão)
- Português
- Espanhol
- Francês

O sistema está preparado para suportar até 40 idiomas diferentes, com a estrutura já implementada.

## Como Funciona

1. **Seleção de Idioma**: No canto superior direito da aplicação, há um seletor de idioma que permite aos usuários escolher sua preferência.

2. **Persistência**: A preferência de idioma é salva no arquivo `data/config.json` e mantida entre sessões.

3. **Traduções**: Todas as strings da interface estão em arquivos JSON separados no diretório `translations/` para fácil manutenção.

## Estrutura de Arquivos

```
FlowTube/
├── translations/          # Diretório para arquivos de tradução
│   ├── en.json            # Traduções em inglês
│   ├── es.json            # Traduções em espanhol
│   ├── fr.json            # Traduções em francês
│   └── pt.json            # Traduções em português
│
└── utils/                 # Diretório para módulos utilitários
    └── i18n.py            # Sistema de internacionalização
```

## Como Adicionar um Novo Idioma

Para adicionar suporte a um novo idioma:

1. Crie um novo arquivo JSON no diretório `translations/` com o código do idioma como nome (ex: `de.json` para alemão).

2. Copie a estrutura de um arquivo existente e traduza os valores, mantendo as mesmas chaves.

3. Exemplo de estrutura do arquivo JSON:
   ```json
   {
       "app_title": "YourTubes™",
       "app_subtitle": "Seu Feed Personalizado do YouTube™",
       "configuration": "Configuração",
       ...
   }
   ```

4. O sistema detectará automaticamente o novo idioma e o adicionará ao seletor de idiomas.

## Melhores Práticas

1. **Mantenha as chaves consistentes**: Use as mesmas chaves em todos os idiomas.

2. **Teste todos os idiomas**: Após adicionar ou modificar traduções, teste a aplicação em todos os idiomas suportados.

3. **Considere o espaço**: Algumas línguas podem precisar de mais espaço para o mesmo texto. Certifique-se de que o layout funciona bem em todos os idiomas.

4. **Formatação**: Mantenha os marcadores de formato (como `{}` para `.format()`) consistentes em todas as traduções.

5. **Codificação UTF-8**: Todos os arquivos JSON devem ser salvos com codificação UTF-8 para suportar caracteres especiais e não-latinos.

## Limitações Atuais

- Não há suporte para pluralização complexa
- As datas ainda são exibidas no formato ISO (AAAA-MM-DD)
- Não há suporte para idiomas com escrita da direita para a esquerda (RTL)

## Funcionamento Interno

O sistema de internacionalização é gerenciado pelo módulo `utils/i18n.py`, que:

1. Carrega dinamicamente todos os arquivos JSON do diretório `translations/`
2. Fornece a função `get_text(key, lang)` para obter textos traduzidos
3. Implementa fallback para inglês quando uma tradução não está disponível
4. Permite adicionar novos idiomas sem reiniciar a aplicação

---

Estas instruções devem ajudar a manter e expandir o sistema de internacionalização do FlowTube.
