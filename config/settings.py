"""
Configuración del sistema de blog de afiliados
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Configuración Amazon Afiliados
AMAZON_PARTNER_TAG = os.getenv('AMAZON_PARTNER_TAG', 'techblog20209-21')
AMAZON_REGION = os.getenv('AMAZON_REGION', 'es')
AMAZON_MARKETPLACE = os.getenv('AMAZON_MARKETPLACE', 'www.amazon.es')

# Configuración Blogger (obsoleto - ahora usamos GitHub Pages)
BLOGGER_BLOG_ID = os.getenv('BLOGGER_BLOG_ID', '1234567890123456789')

# Configuración API Keys (para cuando tengas PA-API)
AMAZON_ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY', '')
AMAZON_SECRET_KEY = os.getenv('AMAZON_SECRET_KEY', '')

# Configuración OpenAI (para generación de contenido)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/database/tracker.db')

# Configuración de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', f'{BASE_DIR}/logs/bot.log')

# Configuración del scheduler
SCHEDULER_ENABLED = os.getenv('SCHEDULER_ENABLED', 'True').lower() == 'true'
SCHEDULER_INTERVAL = int(os.getenv('SCHEDULER_INTERVAL', '3600'))  # 1 hora en segundos

# Configuración de generación de contenido
MAX_ARTICLES_PER_DAY = int(os.getenv('MAX_ARTICLES_PER_DAY', '3'))
MIN_WORDS_PER_ARTICLE = int(os.getenv('MIN_WORDS_PER_ARTICLE', '1000'))

# Configuración SEO
TARGET_KEYWORDS = os.getenv('TARGET_KEYWORDS', 'tecnología,gadgets,laptops,smartphones').split(',')

# Configuración de redes sociales
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME', '')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD', '')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '')

PINTEREST_TOKEN = os.getenv('PINTEREST_TOKEN', '')
MASTODON_TOKEN = os.getenv('MASTODON_TOKEN', '')

# Configuración del blog
BLOG_NAME = os.getenv('BLOG_NAME', 'TechBlog')
BLOG_DESCRIPTION = os.getenv('BLOG_DESCRIPTION', 'Blog de tecnología con reviews y guías de productos')
BLOG_AUTHOR = os.getenv('BLOG_AUTHOR', 'TechBlog Team')

# Configuración de archivos
POSTS_DIR = BASE_DIR / 'blog-afiliados' / 'posts'
TEMPLATES_DIR = BASE_DIR / 'blog-afiliados' / 'templates'
ASSETS_DIR = BASE_DIR / 'blog-afiliados' / 'assets'

# Configuración de monetización
AFFILIATE_ENABLED = os.getenv('AFFILIATE_ENABLED', 'True').lower() == 'true'
AFFILIATE_DISCLOSURE = os.getenv('AFFILIATE_DISCLOSURE', 'True').lower() == 'true'

# Configuración de URLs
GITHUB_PAGES_URL = os.getenv('GITHUB_PAGES_URL', 'https://marioarpe.github.io/techblog-2026/')
BASE_URL = os.getenv('BASE_URL', GITHUB_PAGES_URL)
