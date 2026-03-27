"""
Script para regenerar artículos existentes con imágenes reales
"""
import os
import logging
from modules.content_generator import ContentGenerator

def regenerate_existing_articles():
    """Regenera artículos existentes con imágenes reales"""
    logger = logging.getLogger(__name__)
    
    # Directorio de posts
    posts_dir = "blog-afiliados/posts"
    
    # Inicializar generador
    generator = ContentGenerator()
    
    # Procesar cada archivo HTML existente
    for filename in os.listdir(posts_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(posts_dir, filename)
            
            try:
                # Extraer keyword del nombre del archivo
                keyword = filename.replace('.html', '').replace('-', ' ').title()
                
                logger.info(f"🔄 Regenerando: {filename}")
                
                # Generar nuevo contenido con imágenes reales
                article_data = generator.generate_article(keyword)
                
                if 'error' not in article_data:
                    # Leer contenido existente para preservar estructura
                    with open(filepath, 'r', encoding='utf-8') as f:
                        existing_content = f.read()
                    
                    # Reemplazar imágenes genéricas con imágenes reales
                    updated_content = existing_content.replace(
                        'https://picsum.photos/800/600?random=',
                        article_data['featured_image']
                    )
                    
                    # Guardar archivo actualizado
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    logger.info(f"✅ Actualizado: {filename}")
                else:
                    logger.error(f"❌ Error generando: {filename}")
                    
            except Exception as e:
                logger.error(f"❌ Error procesando {filename}: {str(e)}")

if __name__ == "__main__":
    regenerate_existing_articles()
