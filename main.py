import streamlit as st
import googleapiclient.discovery
import googleapiclient.errors
import os
import json
from datetime import datetime, timedelta
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import base64
import pickle

# Configurar a página para melhor desempenho - deve ser o primeiro comando Streamlit
st.set_page_config(
    page_title="FlowTube",
    page_icon="public/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar o sistema de traduções baseado em JSON
try:
    from utils.i18n import get_text, code_to_name, supported_languages, get_available_languages
    print("Sistema de traduções JSON carregado com sucesso!")
    print(f"Idiomas suportados: {len(supported_languages)}")
except Exception as e:
    print(f"Erro ao carregar traduções: {e}")
    # Fallback para funções básicas de tradução caso ocorra erro
    supported_languages = ['en', 'pt']
    code_to_name = {
        'en': 'English',
        'pt': 'Português'
    }
    
    def get_text(key, lang='en'):
        return key
        
    def get_available_languages():
        return [("English", "en"), ("Português", "pt")]

# Carregar variáveis de ambiente
load_dotenv()

# Configurar cliente da API do YouTube
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Função para carregar a configuração
def load_config():
    # Caminho para o arquivo de configuração
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    config_file_path = os.path.join(config_dir, 'config.json')
    
    # Configuração padrão
    default_config = {
        "channels": [],
        "keywords": [],
        "channel_ids": {},  # Armazenar IDs de canais
        "max_results": 5,   # Número padrão de vídeos por canal
        "language": "pt",   # Idioma padrão
        "channel_info": {}  # Informações adicionais dos canais
    }
    
    # Garantir que o diretório existe
    os.makedirs(config_dir, exist_ok=True)
    
    try:
        # Verificar se o arquivo existe e não está vazio
        if os.path.exists(config_file_path) and os.path.getsize(config_file_path) > 0:
            with open(config_file_path, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                
                # Garantir que todos os campos necessários existam
                if 'channel_ids' not in config:
                    config['channel_ids'] = {}
                if 'max_results' not in config:
                    config['max_results'] = 5
                if 'channel_info' not in config:
                    config['channel_info'] = {}
                if 'language' not in config:
                    config['language'] = 'pt'
                
                return config
        else:
            # Criar arquivo de configuração padrão se não existir
            with open(config_file_path, 'w', encoding='utf-8') as config_file:
                json.dump(default_config, config_file, ensure_ascii=False, indent=4)
            return default_config
    except Exception as e:
        # Em caso de erro, usar configuração padrão
        st.error(f"Erro ao carregar configuração: {e}")
        
        # Tentar fazer backup do arquivo corrompido
        if os.path.exists(config_file_path):
            try:
                backup_path = f"{config_file_path}.bak"
                os.rename(config_file_path, backup_path)
                st.warning(f"Arquivo de configuração corrompido. Backup criado em {backup_path}")
            except:
                pass
        
        # Criar novo arquivo de configuração
        with open(config_file_path, 'w', encoding='utf-8') as config_file:
            json.dump(default_config, config_file, ensure_ascii=False, indent=4)
        
        return default_config

config = load_config()

# Função para salvar a configuração
def save_config():
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    config_file_path = os.path.join(config_dir, 'config.json')
    
    # Garantir que o diretório existe
    os.makedirs(config_dir, exist_ok=True)
    
    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)

# Inicializar cliente da API do YouTube
@st.cache_resource
def get_youtube_client():
    try:
        return googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, 
            developerKey=os.getenv('YOUTUBE_API_KEY'),
            cache_discovery=False
        )
    except Exception as e:
        st.error(f"Erro ao inicializar cliente da API do YouTube: {e}")
        return None

# Obter cliente da API
youtube = get_youtube_client()

# Função para obter ID do canal a partir da URL
def get_channel_id(channel_url):
    # Verificar se o ID já está em cache
    if channel_url in config['channel_ids']:
        return config['channel_ids'][channel_url]

    try:
        if '/channel/' in channel_url:
            # Extrair ID do canal da URL
            channel_id = channel_url.split('/channel/')[1].split('/')[0]
        elif '/user/' in channel_url or '/c/' in channel_url or '@' in channel_url:
            # Extrair nome de usuário da URL
            if '/user/' in channel_url:
                username = channel_url.split('/user/')[1].split('/')[0]
            elif '/c/' in channel_url:
                username = channel_url.split('/c/')[1].split('/')[0]
            else:
                username = channel_url.split('/')[-1]
            
            if username.startswith('@'):
                username = username[1:]  # Remover '@' se presente
            
            # Buscar ID do canal pelo nome de usuário
            request = youtube.search().list(
                part="snippet",
                type="channel",
                q=username,
                maxResults=1
            )
            response = request.execute()
            
            if response['items']:
                channel_id = response['items'][0]['snippet']['channelId']
            else:
                st.error(f"{get_text('error_channel_id', st.session_state.lang)} {channel_url}")
                return None
        else:
            st.error(f"{get_text('invalid_url', st.session_state.lang)} {channel_url}")
            return None

        # Armazenar ID do canal em cache
        config['channel_ids'][channel_url] = channel_id
        save_config()
        return channel_id
    except Exception as e:
        st.error(f"{get_text('error_occurred', st.session_state.lang)} {e}")
        return None

# Função para buscar os vídeos mais recentes de um canal
def fetch_latest_videos(channel_id, max_results=10):
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=max_results
        )
        response = request.execute()
        return response['items']
    except googleapiclient.errors.HttpError as e:
        st.error(f"{get_text('error_occurred', st.session_state.lang)} {e}")
        return []
    except Exception as e:
        st.error(f"{get_text('error_occurred', st.session_state.lang)} {e}")
        return []

# Função para filtrar conteúdo relevante
def filter_relevant_content(videos, keywords):
    return [video for video in videos if any(keyword.lower() in video['snippet']['title'].lower() or 
                                             keyword.lower() in video['snippet']['description'].lower() 
                                             for keyword in keywords)]

# Cache de vídeos
@st.cache_data(ttl=86400)  # Cache por 24 horas
def get_cached_videos(channels, max_results=5, keywords=None):
    all_videos = []
    
    for channel in channels:
        channel_id = get_channel_id(channel)
        if channel_id:
            videos = fetch_latest_videos(channel_id, max_results)
            all_videos.extend(videos)
        else:
            st.warning(get_text('skipping_channel', st.session_state.lang).format(channel))
    
    # Filtrar por palavras-chave se fornecidas
    if keywords and len(keywords) > 0:
        all_videos = filter_relevant_content(all_videos, keywords)
    
    # Ordenar por data de publicação (mais recente primeiro)
    all_videos.sort(key=lambda x: x['snippet']['publishedAt'], reverse=True)
    
    return all_videos

# Aplicativo Streamlit
def main():
    # Inicializar variáveis de estado para o player de vídeo e paginação
    if 'show_video' not in st.session_state:
        st.session_state.show_video = False
        st.session_state.current_video_id = None
        st.session_state.current_video_title = None
        st.session_state.watched_videos = set()
        st.session_state.page = 0
    
    # Inicializar estrutura de channel_info se não existir no config
    if 'channel_info' not in config:
        config['channel_info'] = []
    
    # Inicializar idioma na sessão se não estiver definido
    if 'lang' not in st.session_state:
        st.session_state.lang = config.get('language', 'pt')
    
    # Título da página com apenas a logomarca centralizada
    st.image("public/flowtube.png", width=300)
    
    # Linha horizontal para separar o título do conteúdo
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Barra lateral
    st.sidebar.title(get_text('settings', st.session_state.lang))
    
    # Seletor de idioma
    languages = get_available_languages()
    language_names = [lang[0] for lang in languages]
    language_codes = [lang[1] for lang in languages]
    
    # Obter o índice do idioma atual
    current_lang_index = language_codes.index(st.session_state.lang) if st.session_state.lang in language_codes else 0
    
    # Criar o seletor de idioma
    selected_lang_name = st.sidebar.selectbox(
        get_text('language', st.session_state.lang),
        language_names,
        index=current_lang_index
    )
    
    # Atualizar o idioma se alterado
    selected_lang_code = language_codes[language_names.index(selected_lang_name)]
    if selected_lang_code != st.session_state.lang:
        st.session_state.lang = selected_lang_code
        config['language'] = selected_lang_code
        save_config()
        st.rerun()
    
    # Abas para gerenciamento de canais
    channel_tab1, channel_tab2 = st.sidebar.tabs([get_text('add_channel', st.session_state.lang), get_text('manage_channels', st.session_state.lang)])
    
    with channel_tab1:
        # Formulário para adicionar canal
        with st.form("add_channel_form"):
            new_channel = st.text_input(get_text('channel_url', st.session_state.lang))
            channel_name = st.text_input(get_text('channel_name', st.session_state.lang), help=get_text('channel_name_help', st.session_state.lang))
            
            submitted = st.form_submit_button(get_text('add_channel', st.session_state.lang))
            
            if submitted and new_channel:
                # Verificar se o canal é válido
                channel_id = get_channel_id(new_channel)
                
                if channel_id:
                    # Se o nome do canal não for fornecido, tentar obter da API
                    if not channel_name:
                        try:
                            request = youtube.channels().list(
                                part="snippet",
                                id=channel_id
                            )
                            response = request.execute()
                            if response['items']:
                                channel_name = response['items'][0]['snippet']['title']
                            else:
                                channel_name = new_channel
                        except Exception as e:
                            st.error(f"{get_text('error_occurred', st.session_state.lang)} {str(e)}")
                            channel_name = new_channel
                    
                    # Adicionar canal com nome amigável
                    if new_channel not in [c['url'] for c in config.get('channel_info', [])]:
                        config['channel_info'].append({
                            'url': new_channel,
                            'name': channel_name,
                            'id': channel_id
                        })
                        config['channels'] = [c['url'] for c in config['channel_info']]
                        save_config()
                        st.success(f"{get_text('channel_added', st.session_state.lang)} '{channel_name}'!")
                        st.rerun()
                else:
                    st.error(get_text('invalid_channel', st.session_state.lang))
    
    with channel_tab2:
        if not config.get('channel_info', []):
            st.info(get_text('no_channels', st.session_state.lang))
        else:
            # Exibir lista de canais com opção de remoção
            for i, channel in enumerate(config['channel_info']):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.write(f"**{channel.get('name', channel['url'])}**")
                    st.caption(channel['url'])
                with col2:
                    if st.button(get_text('remove', st.session_state.lang), key=f"remove_{i}"):
                        config['channel_info'].pop(i)
                        config['channels'] = [c['url'] for c in config['channel_info']]
                        save_config()
                        st.success(get_text('channel_removed', st.session_state.lang))
                        st.rerun()
                st.divider()
    
    # Palavras-chave
    st.sidebar.subheader(get_text('keywords', st.session_state.lang))
    keywords_text = st.sidebar.text_area(
        get_text('enter_keywords', st.session_state.lang),
        "\n".join(config['keywords']),
        height=100,
        help=get_text('keywords_help', st.session_state.lang)
    )
    keywords = [k.strip() for k in keywords_text.split("\n") if k.strip()]
    
    # Número de vídeos por canal
    max_results = st.sidebar.slider(
        get_text('videos_per_channel', st.session_state.lang),
        min_value=1,
        max_value=50,
        value=config.get('max_results', 5),
        help=get_text('videos_per_channel_help', st.session_state.lang)
    )
    
    # Botão para salvar configuração
    if st.sidebar.button(get_text('save_config', st.session_state.lang)):
        config['keywords'] = keywords
        config['max_results'] = max_results
        save_config()
        st.sidebar.success(get_text('config_saved', st.session_state.lang))
    
    # Adicionar espaço para empurrar o rodapé para baixo
    for _ in range(5):
        st.sidebar.text("")
    
    # Rodapé com créditos
    st.sidebar.markdown("---")
    st.sidebar.markdown(get_text('inspired_by', st.session_state.lang), unsafe_allow_html=True)
    
    # Conteúdo principal
    col_refresh, col_modal = st.columns([5, 1])
    with col_refresh:
        if st.button(get_text('refresh_videos', st.session_state.lang)):
            st.cache_data.clear()
            st.rerun()
    
    # Exibir player de vídeo se um vídeo estiver selecionado
    if st.session_state.show_video:
        # Adicionar CSS para o player de vídeo responsivo
        st.markdown("""
        <style>
        .video-container {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            max-width: 100%;
        }
        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        .video-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .video-title {
            font-weight: bold;
            font-size: 1.2em;
            margin-right: 10px;
            flex-grow: 1;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Cabeçalho do vídeo com título e botões
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"<div class='video-title'>{st.session_state.current_video_title}</div>", unsafe_allow_html=True)
        with col2:
            if st.button(f"✖️ {get_text('close_video', st.session_state.lang)}"):
                st.session_state.show_video = False
                st.rerun()
        
        # Player de vídeo responsivo
        st.markdown(f"""
        <div class="video-container">
            <iframe 
            src="https://www.youtube.com/embed/{st.session_state.current_video_id}?autoplay=1" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
            </iframe>
        </div>
        """, unsafe_allow_html=True)
        
        # Linha divisora
        st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Exibir vídeos se houver canais configurados
    channels = [c['url'] for c in config.get('channel_info', [])] if config.get('channel_info') else config.get('channels', [])
    
    if channels:
        videos = get_cached_videos(channels, max_results, keywords)
        
        if not videos:
            st.info(get_text('no_videos', st.session_state.lang))
        else:
            st.subheader(f"{get_text('found_videos', st.session_state.lang)}: {len(videos)}")
            
            # Configuração de paginação
            videos_per_page = 6  # 2 linhas de 3 vídeos
            total_pages = max(1, (len(videos) + videos_per_page - 1) // videos_per_page)
            
            # Garantir que a página atual é válida
            if st.session_state.page >= total_pages:
                st.session_state.page = 0
            
            # Calcular índices de início e fim para a página atual
            start_idx = st.session_state.page * videos_per_page
            end_idx = min(start_idx + videos_per_page, len(videos))
            
            # Exibir vídeos da página atual
            current_videos = videos[start_idx:end_idx]
            
            # Exibir grade de vídeos (2 linhas de 3 vídeos)
            for i in range(0, len(current_videos), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_videos):
                        video = current_videos[i + j]
                        with cols[j]:
                            # Obter miniatura
                            thumbnail_url = video['snippet']['thumbnails']['high']['url']
                            response = requests.get(thumbnail_url)
                            img = Image.open(BytesIO(response.content))
                            st.image(img, use_container_width=True)
                            
                            # Título e canal do vídeo
                            st.markdown(f"**{video['snippet']['title']}**")
                            st.write(f"{video['snippet']['channelTitle']}")
                            st.write(f"{get_text('published', st.session_state.lang)}: {video['snippet']['publishedAt'][:10]}")
                            
                            # Verificar se o vídeo já foi assistido
                            video_id = video['id']['videoId']
                            video_title = video['snippet']['title']
                            watched = video_id in st.session_state.watched_videos
                            
                            # Botão de reprodução com indicador de assistido
                            video_number = start_idx + i + j + 1
                            button_text = f"{get_text('play_video', st.session_state.lang)} {video_number}"
                            if watched:
                                button_text = f"🔵 {get_text('watched_indicator', st.session_state.lang)}: {button_text}"
                            
                            if st.button(button_text, key=f"play_{video_id}"):
                                st.session_state.show_video = True
                                st.session_state.current_video_id = video_id
                                st.session_state.current_video_title = video_title
                                st.session_state.watched_videos.add(video_id)
                                st.rerun()
            
            # Controles de paginação
            if total_pages > 1:
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    if st.session_state.page > 0:
                        if st.button(f"◀ {get_text('previous', st.session_state.lang)}"):
                            st.session_state.page -= 1
                            st.rerun()
                
                with col2:
                    st.markdown(f"<div style='text-align: center'>{get_text('page', st.session_state.lang)} {st.session_state.page + 1} / {total_pages}</div>", unsafe_allow_html=True)
                
                with col3:
                    if st.session_state.page < total_pages - 1:
                        if st.button(f"{get_text('next', st.session_state.lang)} ▶"):
                            st.session_state.page += 1
                            st.rerun()
    else:
        st.info(get_text('add_channels_prompt', st.session_state.lang))

if __name__ == "__main__":
    main()
