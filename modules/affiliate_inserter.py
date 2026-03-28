"""
Módulo para inserción de links de afiliado de Amazon
"""
import re
import requests
import hashlib
import hmac
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote
from datetime import datetime
import json
import time
from bs4 import BeautifulSoup

from config import settings

class AffiliateInserter:
    """Gestiona la inserción de links de afiliado de Amazon"""
    
    def __init__(self):
        """Inicializa el inseridor de afiliados"""
        self.logger = logging.getLogger(__name__)
        
        # Partner Tag configurado (desde settings)
        self.partner_tag = getattr(settings, 'AMAZON_PARTNER_TAG', 'techblog20209-21')

        # Configuración Amazon (tomada desde settings)
        marketplace = getattr(settings, 'AMAZON_MARKETPLACE', 'www.amazon.es')
        self.amazon_base_url = f"https://{marketplace}"
        
        # User-Agent para evitar bloqueos
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Product patterns para detectar menciones
        self.product_patterns = [
            r'\b(laptop|notebook|portátil)\b',
            r'\b(smartphone|móvil|celular)\b',
            r'\b(tablet|ipad)\b',
            r'\b(smartwatch|reloj inteligente)\b',
            r'\b(auriculares|cascos|headphones)\b',
            r'\b(cámara|camara|cámara digital)\b',
            r'\b(consola|playstation|xbox|nintendo)\b',
            r'\b(gadget|dispositivo)\b',
            r'\b(accesorio|periférico)\b',
            r'\b(mouse|ratón|teclado)\b'
        ]
        
        # Disclaimer legal
        self.disclaimer = '''
<div style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin: 20px 0;">
<p><small><strong>Disclosure:</strong> Como afiliado de Amazon, ganamos comisiones por compras calificadas realizadas a través de los links en este artículo. Los precios y disponibilidad son precisos al momento de la publicación, pero están sujetos a cambios.</small></p>
</div>
        '''
    
    def insert_affiliate_links(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inserta links de afiliado de Amazon en el contenido"""
        try:
            # Si la inserción de afiliados está deshabilitada, no hacemos nada
            if not getattr(settings, 'AFFILIATE_ENABLED', True):
                self.logger.info("Affiliate links disabled in settings; skipping insertion")
                return article_data

            content = article_data.get('content', '')
            main_keyword = article_data.get('main_keyword', '')
            
            self.logger.info(f"Insertando links de afiliado en: {article_data.get('title', '')}")
            
            # Detectar menciones de productos
            product_mentions = self._detect_product_mentions(content, main_keyword)
            
            if not product_mentions:
                self.logger.warning("No se detectaron menciones de productos")
                return article_data
            
            # Buscar productos en Amazon (modo manual sin PA-API)
            products_found = self._search_amazon_products_manual(product_mentions)
            
            # Insertar links de afiliado
            updated_content = content
            inserted_products = []
            
            for product in products_found:
                product_name = product['product_name']
                search_query = f"{product_name} {main_keyword}"
                
                # Crear link de búsqueda de Amazon con tag
                affiliate_url = f"{self.amazon_base_url}/s?k={quote(search_query)}&tag={self.partner_tag}"
                
                # Reemplazar menciones del producto con link de afiliado
                # Buscar diferentes formas en que se menciona el producto
                patterns_to_replace = [
                    rf'\b{re.escape(product_name)}\b',
                    rf'\b{re.escape(product_name)}s?\b',
                    rf'{re.escape(product_name)}',
                    rf'{re.escape(product_name)}s?'
                ]
                
                for pattern in patterns_to_replace:
                    updated_content = re.sub(
                        pattern,
                        f'[{product_name}]({affiliate_url})',
                        updated_content,
                        flags=re.IGNORECASE
                    )
                
                inserted_products.append({
                    'product_name': product_name,
                    'affiliate_url': affiliate_url,
                    'search_query': search_query,
                    'position': product['position'],
                    'context': product['context']
                })
                
                self.logger.info(f"✅ Link insertado: {product_name} -> {affiliate_url}")
            
            # Añadir disclaimer al final del artículo
            if inserted_products:
                updated_content += self.disclaimer
            
            # Actualizar artículo
            article_data['content'] = updated_content
            article_data['links_inserted'] = len(inserted_products)
            article_data['affiliate_products'] = inserted_products
            
            self.logger.info(f"Insertados {len(inserted_products)} links de afiliado")
            
            return article_data
            
        except Exception as e:
            self.logger.error(f"Error insertando links de afiliado: {str(e)}")
            return article_data
    
    def _detect_product_mentions(self, content: str, main_keyword: str) -> List[Dict]:
        """Detecta menciones de productos en el contenido"""
        try:
            mentions = []
            
            # Detectar usando patrones regex
            for pattern in self.product_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    # Obtener contexto alrededor de la mención
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = content[start:end].strip()
                    
                    mentions.append({
                        'product_type': match.group(),
                        'position': match.start(),
                        'context': context,
                        'keyword': main_keyword
                    })
            
            # Eliminar duplicados y limitar
            unique_mentions = []
            seen_positions = set()
            
            for mention in mentions:
                if mention['position'] not in seen_positions:
                    unique_mentions.append(mention)
                    seen_positions.add(mention['position'])
            
            return unique_mentions[:5]  # Limitar a 5 menciones
            
        except Exception as e:
            self.logger.error(f"Error detectando menciones: {str(e)}")
            return []
    
    def _search_amazon_products_manual(self, product_mentions: List[Dict]) -> List[Dict]:
        """Busca productos en Amazon usando web scraping manual"""
        products_found = []
        
        for mention in product_mentions:
            try:
                product_name = mention['product_type']
                search_query = f"{product_name} {mention['keyword']}"
                
                # Construir URL de búsqueda de Amazon
                search_url = f"{self.amazon_base_url}/s?k={quote(search_query)}"
                
                self.logger.info(f"🔍 Buscando en Amazon: {product_name}")
                
                # Realizar búsqueda web scraping
                response = requests.get(search_url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Buscar ASIN en los resultados
                    asin_match = self._extract_asin_from_page(soup)
                    
                    if asin_match:
                        affiliate_url = f"{self.amazon_base_url}/s?k={quote(search_query)}&tag={self.partner_tag}"
                        
                        products_found.append({
                            'product_name': product_name,
                            'asin': asin_match,
                            'affiliate_url': affiliate_url,
                            'search_query': search_query,
                            'position': mention['position'],
                            'context': mention['context']
                        })
                        
                        self.logger.info(f"✅ ASIN encontrado: {asin_match}")
                        time.sleep(2)  # Delay para evitar bloqueos
                    else:
                        self.logger.warning(f"⚠️ No se encontró ASIN para: {product_name}")
                else:
                    self.logger.error(f"❌ Error en búsqueda Amazon: {response.status_code}")
                    
            except Exception as e:
                self.logger.error(f"❌ Error buscando {mention['product_type']}: {str(e)}")
        
        return products_found
    
    def _extract_asin_from_page(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrae ASIN del HTML de resultados de Amazon"""
        try:
            # Buscar en diferentes lugares donde puede estar el ASIN
            asin_selectors = [
                '[data-asin]',
                '[data-asin-cy]',
                '[data-component-type="s-search-result"]',
                '.s-result-item',
                '[data-cel-widget]'
            ]
            
            for selector in asin_selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements[:3]:  # Primeros 3 resultados
                        # Intentar obtener ASIN de diferentes atributos
                        asin = (element.get('data-asin') or 
                                element.get('data-asin-cy') or
                                element.get('data-component-id'))
                        
                        if asin and len(asin) == 10:  # ASIN tiene 10 caracteres
                            return asin
                        
                        # Buscar ASIN en el href
                        link = element.find('a', href=True)
                        if link:
                            href = link.get('href', '')
                            asin_in_href = re.search(r'/dp/([A-Z0-9]{10})', href)
                            if asin_in_href:
                                return asin_in_href.group(1)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error extrayendo ASIN: {str(e)}")
            return None
