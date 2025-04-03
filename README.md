<p align="center">
  <img src="public/logo_flowtube.png" alt="FlowTube Logo" width="600">
</p>

**FlowTube** é um aplicativo web que cria um feed personalizado de vídeos do YouTube com base nos seus canais favoritos e palavras-chave de interesse.

> Desenvolvido por [Am I Artificial Intelligence](https://ami.digital) | [GitHub](https://github.com/amiartint/flowtube)
>
> Inspirado no projeto [YourTubes](https://github.com/jgravelle/YourTubes) de JGravelle.

## Funcionalidades

### Interface Moderna e Intuitiva
- **Gerenciamento de Canais**: Interface com abas para adicionar e remover canais com nomes amigáveis
- **Sistema de Paginação**: Navegação fácil entre conjuntos de vídeos
- **Design Responsivo**: Adapta-se a diferentes tamanhos de tela

### Conteúdo Personalizado
- **Feed Personalizado**: Agregue vídeos de múltiplos canais do YouTube em um único feed
- **Filtragem por Palavras-chave**: Filtre vídeos com base em palavras-chave específicas
- **Ordenação por Data**: Vídeos organizados por data de publicação (mais recentes primeiro)

### Experiência de Visualização
- **Reprodução Integrada**: Assista aos vídeos diretamente na aplicação em um player responsivo
- **Histórico de Visualização**: Identificação de vídeos já assistidos com indicador visual
- **Controles Personalizados**: Fácil navegação entre vídeos e player

### Personalização e Persistência
- **Configuração Persistente**: Suas preferências são salvas entre sessões
- **Internacionalização**: Interface disponível em português e inglês
- **Ajuste de Quantidade**: Controle o número de vídeos exibidos por canal

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Chave de API do YouTube (obtenha em [Google Cloud Console](https://console.cloud.google.com/))

### Passos para Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/amiartint/flowtube.git
   cd flowtube
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   
   # No Windows
   venv\Scripts\activate
   
   # No macOS/Linux
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure sua chave de API:
   - Copie o arquivo `.env.example` para `.env`
   - Edite o arquivo `.env` e adicione sua chave de API do YouTube:
     ```
     YOUTUBE_API_KEY=sua_chave_api_aqui
     ```

## Uso

1. Inicie o aplicativo:
   ```bash
   streamlit run main.py
   ```

2. Acesse o aplicativo no navegador (geralmente em http://localhost:8501)

3. Configure seus canais:
   - Na aba "Adicionar Canal" da barra lateral, insira a URL do canal do YouTube
   - Opcionalmente, adicione um nome amigável para o canal
   - Clique em "Adicionar Canal"
   - Gerencie seus canais na aba "Gerenciar Canais"

4. Configure palavras-chave e preferências:
   - Adicione palavras-chave para filtrar vídeos (uma por linha)
   - Ajuste o número máximo de vídeos por canal usando o controle deslizante
   - Clique em "Salvar Configuração" para aplicar as mudanças

5. Navegue pelo seu feed personalizado:
   - Os vídeos são exibidos em uma grade organizada por data de publicação
   - Use os controles de paginação para navegar entre conjuntos de vídeos
   - Vídeos já assistidos são marcados com um indicador azul
   - Clique em "Reproduzir Vídeo" para assistir diretamente na aplicação
   - Use o botão "Atualizar Vídeos" para buscar novos conteúdos

6. Personalize o idioma:
   - Selecione entre português e inglês no seletor de idioma na barra lateral

## Estrutura do Projeto

```
FlowTube/
│
├── data/                  # Diretório para dados do usuário
│   └── config.json        # Arquivo de configuração
│
├── translations/          # Diretório para arquivos de tradução
│   ├── en.json            # Traduções em inglês
│   └── pt.json            # Traduções em português
│
├── utils/                 # Diretório para módulos utilitários
│   ├── __init__.py        # Arquivo para marcar como pacote Python
│   └── i18n.py            # Sistema de internacionalização
│
├── main.py                # Aplicativo principal
├── requirements.txt       # Dependências do projeto
├── .env                   # Variáveis de ambiente (não incluído no repositório)
├── .env.example           # Exemplo de variáveis de ambiente
├── README.md              # Este arquivo
└── LICENSE                # Arquivo de licença
```

## Como Funciona

1. **Gerenciamento de Canais**: O aplicativo permite adicionar e remover canais do YouTube usando uma interface com abas, armazenando tanto a URL quanto um nome amigável para cada canal.

2. **Obtenção de Dados**: O aplicativo usa a API do YouTube para buscar os vídeos mais recentes dos canais configurados.

3. **Filtragem**: Os vídeos são filtrados com base nas palavras-chave fornecidas (se houver).

4. **Ordenação e Paginação**: Os vídeos são ordenados por data de publicação (mais recentes primeiro) e organizados em páginas para facilitar a navegação.

5. **Reprodução**: Os vídeos podem ser assistidos diretamente na aplicação através de um player responsivo, e o sistema mantém um histórico dos vídeos já assistidos.

6. **Cache**: Os resultados são armazenados em cache por 24 horas para melhorar o desempenho e reduzir chamadas à API.

7. **Internacionalização**: A interface do usuário é traduzida dinamicamente com base no idioma selecionado (português ou inglês).

## Limitações da API

- A API do YouTube tem cotas diárias de uso. Se você estiver acompanhando muitos canais ou atualizando com muita frequência, pode atingir esses limites.
- O aplicativo usa apenas a chave de API para autenticação, o que limita algumas funcionalidades.

## Personalização

### Adicionando Novos Idiomas

O sistema de internacionalização do FlowTube é baseado em arquivos JSON. Para adicionar um novo idioma:

1. Crie um novo arquivo JSON na pasta `translations/` com o código do idioma como nome (ex: `de.json` para alemão)
2. Copie o conteúdo de um arquivo existente (como `en.json`) e traduza os valores
3. Atualize o arquivo `utils/i18n.py` para incluir o novo idioma na lista de idiomas suportados

### Melhorias Futuras

Algumas melhorias planejadas para as próximas versões:

#### Interface e Experiência do Usuário
- **Tema Escuro/Claro**: Opção para alternar entre modos de visualização
- **Suporte para mais idiomas**: Expansão do sistema de internacionalização
- **Visualização de Estatísticas**: Gráficos e dados sobre os canais seguidos

#### Funcionalidades Avançadas
- **Categorização de Vídeos**: Organização por temas ou tags personalizadas
- **Exportação de Listas**: Compartilhamento de coleções de vídeos
- **Lista "Assistir Mais Tarde"**: Marcação de vídeos para visualização futura

#### Melhorias Técnicas
- **Autenticação OAuth**: Acesso a recursos adicionais da API do YouTube
- **Carregamento Assíncrono**: Melhor responsividade da interface
- **Sistema de Notificações**: Alertas sobre novos vídeos dos canais favoritos

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Agradecimentos

- [Streamlit](https://streamlit.io/) por fornecer uma excelente framework para aplicativos web em Python
- [Google YouTube API](https://developers.google.com/youtube/v3) por fornecer acesso aos dados do YouTube
- [JGravelle](https://github.com/jgravelle) pelo projeto original [YourTubes](https://github.com/jgravelle/YourTubes) que serviu de inspiração

---

<p align="center">
  <img src="public/logo_ami.png" alt="Am I Artificial Intelligence Logo" width="200">
  <br>
  <b>Am I Artificial Intelligence</b>
  <br>
  <a href="https://ami.digital">https://ami.digital</a> | <a href="mailto:ai@ami.digital">ai@ami.digital</a>
  <br>
  &copy; 2025 Am I Artificial Intelligence. Todos os direitos reservados.
</p>
