"""
Sistema de internacionalização para o YourTubes.
Este módulo carrega e gerencia as traduções para diferentes idiomas usando arquivos JSON.
"""

import os
import json
import streamlit as st

# Diretório onde estão os arquivos de tradução
TRANSLATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'translations')

# Mapeamento de nomes de idiomas para códigos - simplificado para apenas português e inglês
language_names = {
    "English": "en",
    "Português": "pt"
}

# Códigos de idioma para nomes
code_to_name = {v: k for k, v in language_names.items()}

# Inicializar variáveis
all_translations = {}
supported_languages = []

@st.cache_resource
def load_translations():
    """Carrega as traduções para português e inglês dos arquivos JSON.
    Usa o cache do Streamlit para evitar recargas desnecessárias."""
    translations = {}
    langs_supported = ['en', 'pt']
    
    # Carregar inglês como idioma base (fallback)
    english_file = os.path.join(TRANSLATIONS_DIR, 'en.json')
    if os.path.exists(english_file):
        with open(english_file, 'r', encoding='utf-8') as f:
            translations['en'] = json.load(f)
    else:
        print(f"Arquivo de tradução base não encontrado: {english_file}")
        return {}, []
    
    # Carregar português
    portuguese_file = os.path.join(TRANSLATIONS_DIR, 'pt.json')
    if os.path.exists(portuguese_file):
        try:
            with open(portuguese_file, 'r', encoding='utf-8') as f:
                translations['pt'] = json.load(f)
                print(f"Carregado arquivo de tradução: {portuguese_file}")
        except Exception as e:
            print(f"Erro ao carregar arquivo de tradução {portuguese_file}: {e}")
    
    print(f"Idiomas carregados: {len(translations)}")
    return translations, langs_supported

def get_text(key, lang='en'):
    """Retorna o texto traduzido para a chave e idioma especificados."""
    global all_translations, supported_languages
    
    # Se as traduções ainda não foram carregadas, carregue-as
    if not all_translations:
        all_translations, supported_languages = load_translations()
    
    # Se o idioma não for suportado, use o inglês
    if lang not in supported_languages:
        lang = 'en'
    
    # Se a chave existir no idioma solicitado, retorne-a
    if key in all_translations.get(lang, {}):
        return all_translations[lang][key]
    
    # Se não existir no idioma solicitado, tente em inglês
    if key in all_translations.get('en', {}):
        return all_translations['en'][key]
    
    # Se não existir em nenhum idioma, retorne a própria chave
    return key

# Carregar traduções usando o cache do Streamlit
all_translations, supported_languages = load_translations()

# Função para adicionar um novo idioma
def add_language(lang_code, translations_dict):
    """
    Adiciona um novo idioma ao sistema.
    
    Args:
        lang_code (str): Código do idioma (ex: 'de')
        translations_dict (dict): Dicionário com as traduções
        
    Returns:
        bool: True se o idioma foi adicionado com sucesso, False caso contrário
    """
    try:
        # Salvar as traduções em um arquivo JSON
        json_file = os.path.join(TRANSLATIONS_DIR, f"{lang_code}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(translations_dict, f, ensure_ascii=False, indent=4)
        
        # Adicionar ao dicionário de traduções em memória
        all_translations[lang_code] = translations_dict
        
        # Atualizar lista de idiomas suportados
        if lang_code not in supported_languages:
            supported_languages.append(lang_code)
            supported_languages.sort()
            if 'en' in supported_languages:
                supported_languages.remove('en')
                supported_languages.insert(0, 'en')
        
        return True
    except Exception as e:
        print(f"Erro ao adicionar idioma {lang_code}: {e}")
        return False

# Função para obter todos os idiomas disponíveis
def get_available_languages():
    """
    Retorna uma lista de tuplas (nome, código) dos idiomas disponíveis.
    
    Returns:
        list: Lista de tuplas (nome, código) dos idiomas disponíveis
    """
    # Retornar apenas português e inglês
    return [("English", "en"), ("Português", "pt")]
