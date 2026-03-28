"""
Generador de contenido para el blog de afiliados
"""
import logging
import random
from typing import Dict, Any, List
from datetime import datetime

from modules.keyword_researcher import KeywordResearcher
from modules.real_image_searcher import search_real_product_image


class ContentGenerator:
    """Generador de contenido optimizado para SEO"""
    
    def __init__(self):
        """Inicializa el generador de contenido"""
        self.logger = logging.getLogger(__name__)
        
        # Templates de contenido
        self.templates = {
            'laptop': self._get_laptop_template(),
            'smartphone': self._get_smartphone_template(),
            'tablet': self._get_tablet_template(),
            'gadget': self._get_gadget_template()
        }
    
    def generate_article(self, main_keyword: str, secondary_keywords: List[str] = None) -> Dict[str, Any]:
        """
        Genera un artículo completo basado en el keyword principal
        
        Args:
            main_keyword: Keyword principal
            secondary_keywords: Keywords secundarios
            
        Returns:
            Dict con el contenido generado
        """
        try:
            self.logger.info(f"📝 Generando artículo para: {main_keyword}")
            
            # Identificar tipo de contenido
            content_type = self._identify_content_type(main_keyword)
            
            # Obtener imagen destacada real del producto
            featured_image = self._get_featured_image(main_keyword)

            # Productos principales según tipo (para imágenes de cada producto)
            product_names = self._get_product_list(main_keyword, content_type)
            product_images = {name: self._get_product_image(name) for name in product_names}

            # Generar contenido basado en el tipo
            if content_type in self.templates:
                content = self.templates[content_type].format(
                    main_keyword=main_keyword,
                    featured_image=featured_image,
                    secondary_keywords=secondary_keywords or [],
                    product1_name=product_names[0] if len(product_names) > 0 else main_keyword,
                    product2_name=product_names[1] if len(product_names) > 1 else '',
                    product3_name=product_names[2] if len(product_names) > 2 else '',
                    product1_image=product_images.get(product_names[0], featured_image) if len(product_names) > 0 else featured_image,
                    product2_image=product_images.get(product_names[1], featured_image) if len(product_names) > 1 else featured_image,
                    product3_image=product_images.get(product_names[2], featured_image) if len(product_names) > 2 else featured_image
                )
            else:
                content = self._generate_generic_content(main_keyword, secondary_keywords)
            
            # Extraer información del artículo
            article_data = {
                'title': self._generate_title(main_keyword),
                'content': content,
                'main_keyword': main_keyword,
                'secondary_keywords': secondary_keywords,
                'content_type': content_type,
                'featured_image': featured_image,
                'generated_at': datetime.now().isoformat(),
                'word_count': len(content.split())
            }
            
            self.logger.info(f"✅ Artículo generado: {article_data['title']}")
            return article_data
            
        except Exception as e:
            self.logger.error(f"❌ Error generando artículo: {str(e)}")
            return {
                'error': str(e),
                'title': f'Error generando {main_keyword}',
                'content': '',
                'main_keyword': main_keyword
            }
    
    def _identify_content_type(self, keyword: str) -> str:
        """Identifica el tipo de contenido basado en el keyword"""
        keyword_lower = keyword.lower()
        
        if any(k in keyword_lower for k in ['laptop', 'portátil', 'notebook']):
            return 'laptop'
        elif any(k in keyword_lower for k in ['smartphone', 'móvil', 'celular']):
            return 'smartphone'
        elif any(k in keyword_lower for k in ['tablet', 'ipad']):
            return 'tablet'
        elif any(k in keyword_lower for k in ['gadget', 'dispositivo']):
            return 'gadget'
        else:
            return 'generic'
    
    def _generate_title(self, keyword: str) -> str:
        """Genera título viral"""
        viral_prefixes = [
            "🔥 Los 10 Mejores", "💰 Guía Completa", "📱 Top Ranking",
            "⚡ Comparativa 2026", "🎯 Análisis Experto"
        ]
        
        viral_suffixes = [
            " del 2026", " - Reviews Honestos", " - Guía Definitiva",
            " - Compra Inteligente", " - Precios Actualizados"
        ]
        
        prefix = random.choice(viral_prefixes)
        suffix = random.choice(viral_suffixes)
        
        return f"{prefix} {keyword.title()}{suffix}"
    
    def _get_product_list(self, main_keyword: str, content_type: str) -> List[str]:
        """Devuelve lista de productos específicos según el contenido"""
        if content_type == 'laptop':
            return [
                main_keyword,
                'HP Pavilion Aero 13',
                'ASUS VivoBook 15'
            ]
        elif content_type == 'smartphone':
            return [
                'iPhone 15 Pro',
                'Samsung Galaxy S24',
                'Google Pixel 8'
            ]
        elif content_type == 'tablet':
            return [
                'iPad Pro 12.9',
                'Samsung Galaxy Tab S9',
                'Surface Pro 9'
            ]
        elif content_type == 'gadget':
            return [
                'Sony WH-1000XM5',
                'Bose QuietComfort 45',
                'JBL Flip 6'
            ]
        else:
            # Fallback: usar solo main_keyword y dos genéricos
            return [main_keyword, 'Lenovo IdeaPad Slim 3', 'iPhone 15 Pro']

    def _get_product_image(self, product_name: str) -> str:
        """Busca URL de imagen real para un producto"""
        image_url = search_real_product_image(product_name)
        if image_url:
            return image_url
        # fallback a una imagen genérica construida añadiendo keyword
        return f"https://images.unsplash.com/photo-15193886887-2b8cf8cf77b78e1a7c4ed05773d0d"

    def _get_featured_image(self, keyword: str) -> str:
        """Obtiene imagen destacada real del producto"""
        # Buscar imagen real del producto
        content_type = self._identify_content_type(keyword)
        
        if content_type in ['laptop', 'smartphone', 'tablet']:
            # Extraer nombre del producto para búsqueda
            product_name = self._extract_product_name(keyword)
            if product_name:
                return search_real_product_image(product_name)
        
        # Si no se encuentra imagen específica, usar la búsqueda general de producto (no aleatoria)
        return search_real_product_image(keyword)
    
    def _extract_product_name(self, keyword: str) -> str:
        """Extrae nombre específico del producto del keyword"""
        # Mapeo de keywords a nombres de productos específicos
        product_mapping = {
            'laptop': {
                'lenovo': 'Lenovo IdeaPad Slim 3',
                'hp': 'HP Pavilion Aero 13',
                'asus': 'ASUS VivoBook 15',
                'dell': 'Dell XPS 13',
                'macbook': 'MacBook Air M2'
            },
            'smartphone': {
                'iphone': 'iPhone 15 Pro',
                'samsung': 'Samsung Galaxy S24',
                'xiaomi': 'Xiaomi 14 Pro',
                'google': 'Google Pixel 8'
            },
            'tablet': {
                'ipad': 'iPad Pro 12.9',
                'samsung': 'Samsung Galaxy Tab S9',
                'microsoft': 'Surface Pro 9'
            },
            'gadget': {
                'sony': 'Sony WH-1000XM5',
                'bose': 'Bose QuietComfort 45',
                'jbl': 'JBL Flip 6'
            }
        }
        
        keyword_lower = keyword.lower()
        
        # Buscar en el mapeo
        for _, products in product_mapping.items():
            for brand, name in products.items():
                if brand.lower() in keyword_lower:
                    return name
    
    def _get_laptop_template(self) -> str:
        """Template para artículos de laptops"""
        return """
# {main_keyword}

## 🏆 Top 3 Laptops de 2026: Calidad-Precio

Hemos analizado durante semanas los mejores portátiles del mercado. Aquí te presentamos nuestra selección top 3 con imágenes reales y especificaciones detalladas.

### 🥇 1. {product1_name} - TOP VENTAS

<div style="text-align: center; margin: 30px 0;">
<img src="{product1_image}" alt="{product1_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Pantalla**: 14" FHD (1920x1080) IPS anti-glare
- **Procesador**: Intel Core i5 de 10ª generación
- **Memoria**: 8GB DDR4 RAM + 512GB SSD
- **Gráficos**: Intel Iris Xe
- **Batería**: Hasta 12 horas de uso mixto
- **Peso**: 1.4 kg
- **Sistema**: Windows 11 Home

**Ideal para**: Estudiantes y profesionales que buscan portabilidad sin sacrificar rendimiento.

### 🥈 2. {product2_name} - MEJOR PRECIO

<div style="text-align: center; margin: 30px 0;">
<img src="{product2_image}" alt="{product2_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Pantalla**: 13.3" FHD (1920x1080) BrightView micro-edge
- **Procesador**: Intel Core i7 de 12ª generación
- **Memoria**: 16GB DDR4 RAM + 512GB SSD
- **Gráficos**: Intel Iris Xe
- **Batería**: Hasta 10.5 horas de uso mixto
- **Peso**: 1.3 kg
- **Sistema**: Windows 11 Home

**Ideal para**: Profesionales que viajan frecuentemente y necesitan máxima potencia en formato compacto.

### 🥉 3. {product3_name} - MEJOR RELACIÓN

<div style="text-align: center; margin: 30px 0;">
<img src="{product3_image}" alt="{product3_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Pantalla**: 15.6" FHD (1920x1080) LED anti-glare
- **Procesador**: AMD Ryzen 5
- **Memoria**: 8GB DDR4 RAM + 512GB SSD
- **Gráficos**: AMD Radeon Graphics
- **Batería**: Hasta 8 horas de uso mixto
- **Peso**: 1.8 kg
- **Sistema**: Windows 11 Home

**Ideal para**: Usuarios que necesitan pantalla grande para trabajo, estudiantes que prefieren laptops de escritorio, y personas con presupuesto limitado.

## 📊 Tabla Comparativa

| Característica | {main_keyword} | HP Pavilion Aero 13 | ASUS VivoBook 15 |
|--------------|----------------|--------------------|--------------------|
| Pantalla | 14" FHD | 13.3" FHD | 15.6" FHD |
| Procesador | Intel i5-1335U | Intel i7-1255U | AMD Ryzen 5 |
| Memoria RAM | 8GB DDR4 | 16GB DDR4 | 8GB DDR4 |
| Almacenamiento | 512GB SSD | 512GB SSD | 512GB SSD |
| Batería | 12 horas | 10.5 horas | 8 horas |
| Peso | 1.4 kg | 1.3 kg | 1.8 kg |
| Ideal para | Estudiantes | Profesionales | Uso diario |
| Precio | €599-€699 | €749-€849 | €699-€799 |

## 🤔 Preguntas Frecuentes (FAQ)

### **¿Cuál es el mejor portátil para estudiantes?**
El **{main_keyword}** es ideal para estudiantes gracias a su excelente relación calidad-precio, portabilidad y batería de 12 horas. Ofrece el mejor balance entre rendimiento y costo.

### **¿Vale la pena gastar más en un portátil de gama alta?**
Depende de tus necesidades. Si eres profesional que requiere máxima potencia, el **HP Pavilion Aero 13** justifica la inversión adicional. Para uso general, el **{main_keyword}** ofrece el mejor valor.

### **¿Qué procesador es mejor: Intel o AMD?**
Para uso general y ofimática, **Intel** ofrece mejor compatibilidad con software profesional. Sin embargo, **AMD** brinda mejor rendimiento gráfico integrado para tareas multimedia.

## 🎯 Conclusión

Después de semanas de análisis intensivo, estos son los mejores portátiles de 2026 que ofrecen el mejor balance entre precio, rendimiento y durabilidad. Desde el compacto **{main_keyword}** hasta el potente **HP Pavilion Aero 13**, hay opciones perfectas para cada presupuesto y necesidad.

⏰ <strong>¡OFERTAS POR TIEMPO LIMITADO!</strong> Los precios actuales son los mejores del año. No esperes más y aprovecha estas increíbles ofertas antes de que terminen.

<div style="margin-top: 3rem;">
    <a href="https://www.amazon.es/s?k={main_keyword}+2026&tag=techblog20209-21" class="final-cta" target="_blank">
        🛒 VER TODAS LAS OFERTAS EN AMAZON
    </a>
</div>

<p style="margin-top: 2rem; opacity: 0.8;">
    ¿Qué portátil te parece más interesante? Déjanos tu comentario abajo y comparte esta guía con quienes estén buscando su próxima computadora.
</p>
        """
    
    def _get_smartphone_template(self) -> str:
        """Template para artículos de smartphones"""
        return """
# {main_keyword}

## 📱 Top 3 Smartphones de 2026

Análisis completo de los mejores smartphones del mercado con imágenes reales y especificaciones técnicas.

### 🥇 1. {product1_name} - PREMIUM

<div style="text-align: center; margin: 30px 0;">
<img src="{product1_image}" alt="{product1_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Pantalla**: 6.1" Super Retina XDR
- **Procesador**: Apple A17 Pro
- **Memoria**: 8GB RAM
- **Almacenamiento**: 256GB/512GB/1TB
- **Cámaras**: 48MP + 12MP Ultra Wide
- **Batería**: Hasta 29 horas de reproducción de video

### 🥈 2. {product2_name} - MEJOR ANDROID

<div style="text-align: center; margin: 30px 0;">
<img src="{product2_image}" alt="{product2_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Pantalla**: 6.2" Dynamic AMOLED 2X
- **Procesador**: Snapdragon 8 Gen 3
- **Memoria**: 8GB RAM
- **Almacenamiento**: 256GB/512GB
- **Cámaras**: 50MP + 10MP
- **Batería**: Hasta 36 horas

### 🥉 3. {product3_name} - MEJOR PRECIO

<div style="text-align: center; margin: 30px 0;">
<img src="{product3_image}" alt="{product3_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Pantalla**: 6.3" OLED
- **Procesador**: Google Tensor G3
- **Memoria**: 8GB RAM
- **Almacenamiento**: 128GB/256GB
- **Cámaras**: 50MP + 12MP
- **Batería**: Hasta 24 horas

## 📊 Tabla Comparativa

| Característica | iPhone 15 Pro | Samsung Galaxy S24 | Google Pixel 8 |
|--------------|----------------|-------------------|----------------|
| Pantalla | 6.1" Super Retina | 6.2" Dynamic AMOLED | 6.3" OLED |
| Procesador | Apple A17 Pro | Snapdragon 8 Gen 3 | Google Tensor G3 |
| Memoria RAM | 8GB | 8GB | 8GB |
| Almacenamiento | 256GB/512GB/1TB | 256GB/512GB | 128GB/256GB |
| Cámaras | 48MP + 12MP | 50MP + 10MP | 50MP + 12MP |
| Batería | 29 horas video | 36 horas | 24 horas |
| Precio | €1199+ | €899+ | €699+ |

## 🤔 Preguntas Frecuentes

### **¿Cuál es el mejor smartphone para fotografía?**
El **iPhone 15 Pro** es superior para fotografía gracias a su sistema de cámaras triple, procesamiento A17 y pantalla Super Retina XDR.

### **¿Vale la pena gastar más en un iPhone?**
Si eres profesional creativo, el **iPhone 15 Pro** justifica la inversión por su ecosistema y rendimiento fotográfico.

### **¿Qué procesador es mejor: Apple o Qualcomm?**
Para ecosistema cerrado, **Apple** ofrece mejor optimización. Sin embargo, **Qualcomm** brinda mejor rendimiento en Android con mayor libertad de personalización.

## 🎯 Conclusión

El mercado de smartphones de 2026 ofrece opciones excelentes para cada presupuesto y necesidad. Desde el premium **iPhone 15 Pro** hasta el accesible **Google Pixel 8**, hay elección perfecta para cada usuario.

⏰ <strong>¡OFERTAS POR TIEMPO LIMITADO!</strong> Las mejores ofertas del año están disponibles.

<div style="margin-top: 3rem;">
    <a href="https://www.amazon.es/s?k={main_keyword}+2026&tag=techblog20209-21" class="final-cta" target="_blank">
        🛒 VER TODAS LAS OFERTAS EN AMAZON
    </a>
</div>
        """
    
    def _get_tablet_template(self) -> str:
        """Template para artículos de tablets"""
        return """
# {main_keyword}

## 📱 Top 3 Tablets de 2026

Guía completa de las mejores tablets con imágenes reales y análisis detallado.

### 🥇 1. {product1_name} - PREMIUM

<div style="text-align: center; margin: 30px 0;">
<img src="{product1_image}" alt="{product1_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Pantalla**: 12.9" Super Retina XDR
- **Procesador**: Apple M4
- **Memoria**: 8GB/16GB/1TB/2TB
- **Cámaras**: 12MP + 8MP
- **Batería**: Hasta 10 horas

### 🥈 2. {product2_name} - VERSATIL

<div style="text-align: center; margin: 30px 0;">
<img src="{product2_image}" alt="{product2_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Pantalla**: 11" Dynamic AMOLED 2X
- **Procesador**: Snapdragon 8 Gen 3
- **Memoria**: 8GB/12GB/256GB/512GB/1TB
- **Cámaras**: 13MP + 8MP
- **Batería**: Hasta 20 horas

### 🥉 3. {product3_name} - MEJOR PARA TRABAJO

<div style="text-align: center; margin: 30px 0;">
<img src="{product3_image}" alt="{product3_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Pantalla**: 13" PixelSense Flow
- **Procesador**: Intel Core Ultra 9
- **Memoria**: 16GB/32GB/1TB
- **Cámaras**: 10MP + 5MP
- **Batería**: Hasta 15 horas

## 📊 Tabla Comparativa

| Característica | iPad Pro 12.9 | Samsung Galaxy Tab S9 | Surface Pro 9 |
|--------------|----------------|-------------------|----------------|
| Pantalla | 12.9" Super Retina | 11" Dynamic AMOLED | 13" PixelSense |
| Procesador | Apple M4 | Snapdragon 8 Gen 3 | Intel Core Ultra 9 |
| Memoria RAM | 8GB/16GB/1TB/2TB | 8GB/12GB/256GB/512GB/1TB | 16GB/32GB/1TB |
| Cámaras | 12MP + 8MP | 13MP + 8MP | 10MP + 5MP |
| Batería | 10 horas | 20 horas | 15 horas |
| Ideal para | Creativos | Entretenimiento | Productividad |

## 🤔 Preguntas Frecuentes

### **¿Cuál es la mejor tablet para creatividad?**
El **iPad Pro 12.9** es superior para creatividad gracias a su pantalla Super Retina XDR, procesamiento M4 y ecosistema optimizado.

### **¿Vale la pena gastar más en una tablet?**
Depende de tu uso profesional. Si eres diseñador o artista, el **iPad Pro 12.9** justifica la inversión. Para uso general, el **Samsung Galaxy Tab S9** ofrece excelente valor.

### **¿Qué procesador es mejor: Apple o Intel?**
Para creatividad profesional, **Apple** ofrece mejor optimización de software. Sin embargo, **Intel** brinda mayor compatibilidad con programas de trabajo tradicionales.

## 🎯 Conclusión

La elección de tablet depende del uso principal. Para creatividad, el **iPad Pro 12.9** es incomparable. Para trabajo, el **Surface Pro 9** ofrece la mejor productividad.

⏰ <strong>¡OFERTAS POR TIEMPO LIMITADO!</strong> Las mejores ofertas del año están disponibles.

<div style="margin-top: 3rem;">
    <a href="https://www.amazon.es/s?k={main_keyword}+2026&tag=techblog20209-21" class="final-cta" target="_blank">
        🛒 VER TODAS LAS OFERTAS EN AMAZON
    </a>
</div>
        """
    
    def _get_gadget_template(self) -> str:
        """Template para artículos de gadgets"""
        return """
# {main_keyword}

## 🔥 Top 5 Gadgets Tecnológicos de 2026

Descubre los gadgets más innovadores del año con análisis expertos y recomendaciones.

### 🥇 1. {product1_name} - MEJORES AURICULARES

<div style="text-align: center; margin: 30px 0;">
<img src="{product1_image}" alt="{product1_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Cancelación de Ruido**: 30dB
- **Calidad Audio**: Hi-Res Audio
- **Batería**: 40 horas
- **Conectividad**: Bluetooth 5.3, NFC, USB-C

### 🥈 2. {product2_name} - MEJOR CALIDAD-PRECIO

<div style="text-align: center; margin: 30px 0;">
<img src="{product2_image}" alt="{product2_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Calidad Audio**: TriPort
- **Batería**: 24 horas
- **Conectividad**: Bluetooth 5.1, AUX, USB-C

### 🥉 3. {product3_name} - MEJOR PORTÁTILES

<div style="text-align: center; margin: 30px 0;">
<img src="{product3_image}" alt="{product3_name}" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
</div>

**Características principales:**
- **Calidad Audio**: JBL Signature Sound
- **Batería**: 12 horas
- **Diseño**: Plegable, resistente al agua

## 🎯 Conclusión

Los auriculares inalámbricos de 2026 ofrecen tecnología impresionante. Desde la cancelación de ruido profesional de **Sony** hasta la portabilidad de **JBL**, hay opción perfecta para cada necesidad y presupuesto.

⏰ <strong>¡OFERTAS POR TIEMPO LIMITADO!</strong> Las mejores ofertas del año están disponibles.

<div style="margin-top: 3rem;">
    <a href="https://www.amazon.es/s?k={main_keyword}+2026&tag=techblog20209-21" class="final-cta" target="_blank">
        🛒 VER TODAS LAS OFERTAS EN AMAZON
    </a>
</div>
        """
    
    def _generate_generic_content(self, main_keyword: str, secondary_keywords: List[str]) -> str:
        """Genera contenido genérico"""
        return f"""
# {main_keyword}

## 📖 Guía Completa

Descubre todo lo que necesitas saber sobre {main_keyword} en nuestra guía completa y actualizada.

### ¿Qué es {main_keyword}?
{main_keyword} es [descripción genérica del concepto]...

### Características Principales
- Característica 1: Descripción detallada
- Característica 2: Beneficios principales
- Característica 3: Usos recomendados

### ¿Cómo Elegir el Mejor {main_keyword}?
Guía paso a paso para tomar la decisión correcta...

### Conclusión
{main_keyword} ofrece excelente valor y rendimiento para [tipo de usuario]...

⏰ <strong>¡OFERTAS POR TIEMPO LIMITADO!</strong> Las mejores ofertas del año están disponibles.

<div style="margin-top: 3rem;">
    <a href="https://www.amazon.es/s?k={main_keyword}+2026&tag=techblog20209-21" class="final-cta" target="_blank">
        🛒 VER TODAS LAS OFERTAS EN AMAZON
    </a>
</div>
        """
