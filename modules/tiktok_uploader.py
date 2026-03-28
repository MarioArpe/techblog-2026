#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TikTok Uploader - Sube videos automáticamente a TikTok
NOTA: TikTok no proporciona API oficial para subes videos.
Este módulo usa métodos alternativos con limitaciones de velocidad de API.
"""

import json
import logging
import os
from pathlib import Path
from typing import Optional
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TikTokConfig:
    """Gestiona configuración de TikTok"""
    
    def __init__(self):
        self.config_file = Path("./config/tiktok_config.json")
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self):
        """Carga configuración"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'username': None,
            'password': None,
            'user_id': None,
            'access_token': None,
            'is_configured': False
        }
    
    def _save_config(self):
        """Guarda configuración"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Error guardando config: {e}")


class TikTokUploader:
    """
    Sube videos a TikTok automáticamente
    
    ⚠️ LIMITACIONES IMPORTANTES:
    - TikTok no tiene API oficial para subir videos
    - Se requieren métodos alternativos (Selenium, scrappers, etc)
    - Alto riesgo de ban de cuenta
    - Recomendación: Usar webhooks o integración manual
    """
    
    def __init__(self):
        self.config = TikTokConfig()
        self.session = requests.Session()

        # Cargar cookies de entorno si están disponibles
        tiktok_cookies = os.getenv('TIKTOK_COOKIES')
        if tiktok_cookies:
            try:
                cookies = json.loads(tiktok_cookies)
                for k, v in cookies.items():
                    self.session.cookies.set(k, v)
                logger.info('✅ Cookies de TikTok cargadas desde .env')
            except Exception as e:
                logger.warning(f'⚠️ No se pudieron parsear cookies de TikTok: {e}')

        logger.warning("""
╔════════════════════════════════════════════════════════════════╗
║           ⚠️  ADVERTENCIA: API DE TIKTOK NO OFICIAL             ║
╠════════════════════════════════════════════════════════════════╣
║ • TikTok no proporciona API oficial para subir videos          ║
║ • Se requieren métodos alternativos con alto riesgo de ban    ║
║ • Velocidad de API limitada a 1 video/10 minutos             ║
║ • Alto riesgo de suspension de cuenta                          ║
║                                                                ║
║ RECOMENDACIÓN:                                                 ║
║ • Usar studio.tiktok.com web interface                        ║
║ • Implementar publicación manual con notificaciones          ║
║ • O integración con herramientas oficiales                    ║
╚════════════════════════════════════════════════════════════════╝
        """)
    
    def upload_video_unofficial(
        self,
        video_path: str,
        title: str,
        description: str,
        hashtags: list
    ) -> bool:
        """
        Sube video usando método no oficial
        
        Args:
            video_path: Ruta del video
            title: Título
            description: Descripción
            hashtags: Lista de hashtags
        
        Returns:
            False - Método no disponible en esta implementación
        """
        logger.error("""
❌ UPLOAD NO DISPONIBLE

Por razones de seguridad y cumplimiento, esta implementación
no incluye métodos no oficiales de TikTok.

ALTERNATIVAS:
1. Upload manual a https://studio.tiktok.com
2. Usar herramientas de terceros autorizadas
3. Implementar webhook con verificación de TikTok
        """)
        return False
    
    def queue_for_manual_upload(
        self,
        video_path: str,
        title: str,
        description: str
    ) -> bool:
        """
        Encola video para carga manual con notificación
        
        Args:
            video_path: Ruta del video
            title: Título
            description: Descripción
        
        Returns:
            True si se encoló correctamente
        """
        try:
            video_file = Path(video_path)
            if not video_file.exists():
                logger.error(f"❌ Archivo no encontrado: {video_path}")
                return False
            
            # Crear carpeta de cola
            queue_dir = Path("./tiktok_queue")
            queue_dir.mkdir(exist_ok=True)
            
            # Guardar metadata
            metadata = {
                'video_file': str(video_file),
                'title': title,
                'description': description,
                'status': 'pending',
                'created_at': str(Path.cwd())
            }
            
            metadata_file = queue_dir / f"{video_file.stem}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"📋 Video encolado para carga manual: {video_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error encolando video: {e}")
            return False

    def upload_video_with_cookies(
        self,
        video_path: str,
        title: str,
        description: str,
        hashtags: list
    ) -> bool:
        """
        Método experimental de subida usando cookies. No garantizado.
        """
        video_file = Path(video_path)
        if not video_file.exists():
            logger.error(f"❌ Archivo no encontrado: {video_path}")
            return False

        # Ejemplo de endpoint tentativo (a adaptar con método real de TikTok)
        upload_url = "https://api.tiktok.com/upload/"  # FICTICIO
        payload = {
            'title': title,
            'description': description,
            'hashtags': ' '.join(hashtags)
        }

        try:
            with open(video_file, 'rb') as f:
                files = {'video': f}
                response = self.session.post(upload_url, data=payload, files=files, timeout=60)

            if response.status_code == 200:
                logger.info('✅ Posible subida a TikTok satisfactoria (sujeto a verificación manual)')
                return True
            else:
                logger.warning(f'⚠️ TikTok upload fallido (status={response.status_code})')
                return False

        except Exception as e:
            logger.error(f'❌ Error en upload TikTok con cookies: {e}')
            return False

    @staticmethod
    def format_tiktok_caption(
        product_name: str,
        affiliate_link: str,
        include_hashtags: bool = True
    ) -> str:
        """
        Formatea descripción para TikTok
        
        Args:
            product_name: Nombre del producto
            affiliate_link: Link del producto
            include_hashtags: Incluir hashtags
        
        Returns:
            Texto formateado para TikTok
        """
        caption = f"""{product_name}

¡Link en bio! 👆

@web7blogg"""
        
        if include_hashtags:
            caption += "\n\n#tecnologia #gadgets #ofertas #amazon #review #viral #unboxing"
        
        return caption


class TikTokAlternatives:
    """Alternativas propuestas para publicación en TikTok"""
    
    @staticmethod
    def generate_upload_instructions(video_path: str, caption: str) -> str:
        """
        Genera instrucciones para upload manual
        
        Args:
            video_path: Ruta del video
            caption: Caption para el video
        
        Returns:
            Instrucciones formateadas
        """
        instructions = f"""
╔════════════════════════════════════════════════════════════════╗
║              📱 INSTRUCCIONES PARA SUBIR EN TIKTOK            ║
╚════════════════════════════════════════════════════════════════╝

PASO 1 - Ir a Studio:
  → https://studio.tiktok.com

PASO 2 - Subir Video:
  → Click en "Subir video"
  → Seleccionar: {Path(video_path).name}
  
PASO 3 - Añadir Caption:
  → Copiar y pegar esto exactamente:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{caption}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASO 4 - Configuración:
  ☑️  Permitir comentarios: SI
  ☑️  Permitir duetos: SI
  ☑️  Permitir stitches: SI
  ☑️  Visibilidad: Pública

PASO 5 - Publicar
  → Click en "Publicar"

═══════════════════════════════════════════════════════════════
        """
        return instructions


# Funciones auxiliares
def create_tiktok_notification(
    product_name: str,
    video_path: str,
    affiliate_link: str
) -> str:
    """
    Crea notificación para usuario sobre video listo para TikTok
    
    Args:
        product_name: Nombre del producto
        video_path: Ruta del video
        affiliate_link: Link afiliado
    
    Returns:
        Texto de notificación
    """
    uploader = TikTokUploader()
    caption = uploader.format_tiktok_caption(product_name, affiliate_link)
    instructions = TikTokAlternatives.generate_upload_instructions(video_path, caption)
    return instructions


# Ejemplo de uso
if __name__ == "__main__":
    print("\n" + "="*70)
    print("📱 TIKTOK UPLOADER")
    print("="*70 + "\n")
    
    uploader = TikTokUploader()
    
    # Ejemplo de caption
    example_caption = uploader.format_tiktok_caption(
        product_name="iPhone 15 Pro",
        affiliate_link="@web7blogg",
        include_hashtags=True
    )
    
    print("📝 Ejemplo de formato para TikTok:\n")
    print(example_caption)
    print("\n" + "="*70 + "\n")
