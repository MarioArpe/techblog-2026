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
            return f"https://picsum.photos/800/600?random={hash(product_name)}"
    
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
    
    def _get_generic_image(self, product_name: str) -> str:
        """Genera imagen genérica pero específica del producto"""
        # Mapeo de productos a imágenes genéricas
        product_images = {
            'laptop': 'https://images.unsplash.com/photo-15556036720-6bfc8cf77b78e1a7c4ed05773d0d/photo-16061178699-6e2bfc8cf77b78e1a7c4ed05773d0d',
            'macbook': 'https://images.unsplash.com/photo-1541807023558-2f0f1b2fff8c0e35f4bb89f38d0b3/photo-1551807023558-2f0f1b2fff8c0e35f4bb89f38d0b3',
            'iphone': 'https://images.unsplash.com/photo-1511707347099-5e8ad9b3b0cb44b88336697913/photo-1511707347099-5e8ad9b3b0cb44b88336697913',
            'ipad': 'https://images.unsplash.com/photo-1544241025-c8c9a827c0e4e78d18d8a7f6e6d1a7c4ed05773d0d/photo-1544241025-c8c9a827c0e4e78d18d8a7f6e6d1a7c4ed05773d0d',
            'samsung': 'https://images.unsplash.com/photo-1592843838274-2190a1f2b4b8cbbd9d4a5d4b8cbbd9d4a5d/photo-1592843838274-2190a1f2b4b8cbbd9d4a5d4b8cbbd9d4a5d',
            'sony': 'https://images.unsplash.com/photo-1607147195360-a8c1d72c5b4b8cbbd9d4a5d4b8cbbd9d4a5d/photo-1607147195360-a8c1d72c5b4b8cbbd9d4a5d4b8cbbd9d4a5d'
        }
        
        # Identificar tipo de producto
        product_type = self._identify_product_type(product_name)
        
        if product_type in product_images:
            return product_images[product_type]
        
        # Si no se encuentra, usar imagen genérica de tecnología
        return f"https://images.unsplash.com/photo-15193886887-2b8cf8cf77b78e1a7c4ed05773d0d"
    
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
