"""
Script para regenerar artículos existentes con imágenes reales
"""
import os
import logging
from modules.real_image_searcher import search_real_product_image

def regenerate_existing_articles():
    """Regenera artículos existentes con imágenes reales"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Directorio de posts
    posts_dir = "blog-afiliados/posts"
    
    # Mapeo de productos a imágenes reales
    product_images = {
        'lenovo': 'https://m.media-amazon.com/images/I/61QjTn8EIL._AC_SL1500_.jpg',
        'hp': 'https://m.media-amazon.com/images/I/51KXqV8KIL._AC_SL1500_.jpg',
        'asus': 'https://m.media-amazon.com/images/I/71n5l8y6GL._AC_SL1500_.jpg',
        'macbook': 'https://m.media-amazon.com/images/I/61mB7N4eKL._AC_SL1500_.jpg',
        'iphone': 'https://m.media-amazon.com/images/I/61gB9N4eKL._AC_SL1500_.jpg',
        'samsung': 'https://m.media-amazon.com/images/I/61B9N4eKL._AC_SL1500_.jpg',
        'ipad': 'https://m.media-amazon.com/images/I/61N4eKL._AC_SL1500_.jpg',
        'sony': 'https://m.media-amazon.com/images/I/61X47+N4XyL._AC_SL1500_.jpg',
        'bose': 'https://m.media-amazon.com/images/I/51KXqV8KIL._AC_SL1500_.jpg',
        'jbl': 'https://m.media-amazon.com/images/I/71n5l8y6GL._AC_SL1500_.jpg'
    }
    
    # Procesar cada archivo HTML existente
    for filename in os.listdir(posts_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(posts_dir, filename)
            
            try:
                logger.info(f"🔄 Procesando: {filename}")
                
                # Leer contenido existente
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Reemplazar imágenes genéricas con imágenes reales
                updated_content = content
                
                # Reemplazar imágenes Picsum con imágenes reales
                for brand, image_url in product_images.items():
                    # Reemplazar múltiples patrones de imágenes genéricas
                    updated_content = updated_content.replace(
                        f'https://picsum.photos/800/600?random=',
                        image_url
                    )
                    updated_content = updated_content.replace(
                        'https://picsum.photos/800/600?random=1',
                        image_url
                    )
                    updated_content = updated_content.replace(
                        'https://picsum.photos/800/600?random=2',
                        image_url
                    )
                    updated_content = updated_content.replace(
                        'https://picsum.photos/800/600?random=3',
                        image_url
                    )
                
                # Guardar archivo actualizado
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                logger.info(f"✅ Actualizado: {filename}")
                    
            except Exception as e:
                logger.error(f"❌ Error procesando {filename}: {str(e)}")
    
    logger.info("🎉 Proceso de actualización de imágenes completado")

if __name__ == "__main__":
    regenerate_existing_articles()
