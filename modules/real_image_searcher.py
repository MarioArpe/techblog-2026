"""
Generador de contenido con imágenes reales de productos
"""
import logging
import requests
import re
from typing import Dict, Any, List
from urllib.parse import quote

class RealImageSearcher:
    """Buscador de imágenes reales de productos"""

    DEFAULT_PRODUCT_IMAGES = {
        'lenovo': 'https://m.media-amazon.com/images/I/61QjTn8EIL._AC_SL1500_.jpg',
        'hp': 'https://m.media-amazon.com/images/I/51KXqV8KIL._AC_SL1500_.jpg',
        'asus': 'https://m.media-amazon.com/images/I/71n5l8y6GL._AC_SL1500_.jpg',
        'dell': 'https://m.media-amazon.com/images/I/71k5E3eo5iL._AC_SL1500_.jpg',
        'macbook': 'https://m.media-amazon.com/images/I/61mB7N4eKL._AC_SL1500_.jpg',
        'iphone': 'https://m.media-amazon.com/images/I/61gB9N4eKL._AC_SL1500_.jpg',
        'samsung': 'https://m.media-amazon.com/images/I/61B9N4eKL._AC_SL1500_.jpg',
        'ipad': 'https://m.media-amazon.com/images/I/61N4eKL._AC_SL1500_.jpg',
        'sony': 'https://m.media-amazon.com/images/I/61X47+N4XyL._AC_SL1500_.jpg',
        'bose': 'https://m.media-amazon.com/images/I/51KXqV8KIL._AC_SL1500_.jpg',
        'jbl': 'https://m.media-amazon.com/images/I/71n5l8y6GL._AC_SL1500_.jpg'
    }

    def __init__(self):
        """Inicializa el buscador de imágenes"""
        self.logger = logging.getLogger(__name__)
        
        # User-Agent para evitar bloqueos
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
    
    def search_product_image(self, product_name: str, brand: str = None) -> str:
        """
        Busca imagen real del producto usando múltiples fuentes
        
        Args:
            product_name: Nombre del producto (ej: "MacBook Air M2")
            brand: Marca del producto (opcional)
            
        Returns:
            URL de la imagen real del producto
        """
        try:
            self.logger.info(f"🔍 Buscando imagen real para: {product_name}")
            
            # 1. Primero intentar con Amazon.es
            amazon_image = self._search_amazon_image(product_name)
            if amazon_image:
                self.logger.info(f"✅ Imagen encontrada en Amazon: {amazon_image}")
                return amazon_image
            
            # 2. Intentar con página oficial del fabricante
            if brand:
                official_image = self._search_official_image(product_name, brand)
                if official_image:
                    self.logger.info(f"✅ Imagen encontrada en sitio oficial: {official_image}")
                    return official_image
            
            # 3. Intentar con DuckDuckGo
            duckduckgo_image = self._search_duckduckgo_image(product_name)
            if duckduckgo_image:
                self.logger.info(f"✅ Imagen encontrada en DuckDuckGo: {duckduckgo_image}")
                return duckduckgo_image
            
            # 4. Último recurso: imagen genérica pero específica
            generic_image = self._get_generic_image(product_name)
            self.logger.info(f"⚠️ Usando imagen genérica: {generic_image}")
            return generic_image
            
        except Exception as e:
            self.logger.error(f"❌ Error buscando imagen: {str(e)}")
            fallback_image = self._get_generic_image(product_name)
            return fallback_image
    
    def _search_amazon_image(self, product_name: str) -> str:
        """Busca imagen en Amazon.es"""
        try:
            search_query = f"{product_name} oficial"
            search_url = f"https://www.amazon.es/s?k={quote(search_query)}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar imagen del primer resultado
                img_element = soup.find('img', {'class': 's-image'})
                if img_element and img_element.get('src'):
                    return img_element['src']
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda Amazon: {str(e)}")
            return None
    
    def _search_official_image(self, product_name: str, brand: str) -> str:
        """Busca imagen en sitio oficial del fabricante"""
        try:
            brand_urls = {
                'apple': 'https://www.apple.com/es/shop',
                'dell': 'https://www.dell.com/es-es',
                'hp': 'https://www.hp.com/es-es',
                'lenovo': 'https://www.lenovo.com/es/es',
                'asus': 'https://www.asus.com/es/',
                'microsoft': 'https://www.microsoft.com/es-es',
                'samsung': 'https://www.samsung.com/es/'
            }
            
            if brand and brand.lower() in brand_urls:
                # Buscar en sitio oficial
                search_url = brand_urls[brand.lower()]
                response = requests.get(search_url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Buscar imagen del producto
                    img_selectors = [
                        'img[alt*="' + product_name.lower() + '"]',
                        'img[title*="' + product_name.lower() + '"]',
                        'img[alt*="' + product_name.replace(' ', '-').lower() + '"]',
                        '.product-image img',
                        '.hero-image img'
                    ]
                    
                    for selector in img_selectors:
                        img_element = soup.select_one(selector)
                        if img_element and img_element.get('src'):
                            return img_element['src']
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda oficial: {str(e)}")
            return None
    
    def _search_duckduckgo_image(self, product_name: str) -> str:
        """Busca imagen usando DuckDuckGo"""
        try:
            search_query = f"{product_name} official product image"
            search_url = f"https://duckduckgo.com/iu/?u=html&q={quote(search_query)}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar primera imagen relevante
                img_element = soup.find('img')
                if img_element and img_element.get('src'):
                    img_url = img_element['src']
                    
                    # Verificar que sea una imagen real del producto
                    if self._is_valid_product_image(img_url, product_name):
                        return img_url
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error en DuckDuckGo: {str(e)}")
            return None

    def _get_brand_from_product_name(self, product_name: str) -> str:
        """Extrae la marca principal del nombre del producto"""
        name_lower = product_name.lower()
        for brand in self.DEFAULT_PRODUCT_IMAGES:
            if brand in name_lower:
                return brand
        return None
    
    def _get_generic_image(self, product_name: str) -> str:
        """Genera imagen genérica pero específica del producto"""
        brand = self._get_brand_from_product_name(product_name)
        if brand and brand in self.DEFAULT_PRODUCT_IMAGES:
            return self.DEFAULT_PRODUCT_IMAGES[brand]

        # Si no se detecta marca, intentar usar fallback por tipo de producto
        product_images = {
            'laptop': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9',
            'macbook': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8',
            'iphone': 'https://images.unsplash.com/photo-1542751110-97427bbecf20',
            'ipad': 'https://images.unsplash.com/photo-1512499617640-c2f9992d2f9f',
            'samsung': 'https://images.unsplash.com/photo-1510552776732-03e61cf4b144',
            'sony': 'https://images.unsplash.com/photo-15193886887-2b8cf8cf77b7'
        }

        product_type = self._identify_product_type(product_name)

        if product_type in product_images:
            return product_images[product_type]

        # Último recurso: imagen genérica de tecnología (no aleatoria)
        return 'https://images.unsplash.com/photo-15193886887-2b8cf8cf77b78e1a7c4ed05773d0d'
    
    def _identify_product_type(self, product_name: str) -> str:
        """Identifica el tipo de producto"""
        product_lower = product_name.lower()
        
        # Mapeo de palabras clave a tipos
        if any(keyword in product_lower for keyword in ['laptop', 'notebook', 'portátil']):
            return 'laptop'
        elif any(keyword in product_lower for keyword in ['macbook', 'mac']):
            return 'macbook'
        elif any(keyword in product_lower for keyword in ['iphone', 'smartphone']):
            return 'iphone'
        elif any(keyword in product_lower for keyword in ['ipad', 'tablet']):
            return 'ipad'
        elif any(keyword in product_lower for keyword in ['samsung', 'galaxy']):
            return 'samsung'
        elif any(keyword in product_lower for keyword in ['sony', 'playstation']):
            return 'sony'
        elif any(keyword in product_lower for keyword in ['hp', 'pavilion']):
            return 'laptop'  # HP es principalmente laptops
        elif any(keyword in product_lower for keyword in ['lenovo', 'thinkpad']):
            return 'laptop'  # Lenovo es principalmente laptops
        elif any(keyword in product_lower for keyword in ['asus', 'vivobook', 'rog']):
            return 'laptop'  # ASUS es principalmente laptops
        else:
            return 'laptop'  # Default a laptop/tecnología
    
    def _is_valid_product_image(self, img_url: str, product_name: str) -> bool:
        """Valida que la imagen sea realmente del producto"""
        # Verificar que la URL contenga palabras clave del producto
        product_keywords = product_name.lower().replace(' ', '-').split()
        
        # Extraer texto del nombre de archivo
        img_filename = img_url.split('/')[-1].lower()
        
        # Verificar coincidencias
        keyword_matches = sum(1 for keyword in product_keywords if keyword in img_filename)
        
        # Si hay suficientes coincidencias, es probablemente la imagen correcta
        return keyword_matches >= 2


# Función de conveniencia
def search_real_product_image(product_name: str, brand: str = None) -> str:
    """
    Busca imagen real del producto
    
    Args:
        product_name: Nombre del producto
        brand: Marca del producto (opcional)
        
    Returns:
        URL de la imagen real del producto
    """
    searcher = RealImageSearcher()
    return searcher.search_product_image(product_name, brand)
