#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Social Media Automation - Orquestador central de automatización
Integra: video generator → telegram publisher → tiktok notifier
"""

import logging
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

from modules.video_generator import VideoGenerator
from modules.telegram_publisher import publish_product_video_sync, TelegramPublisher
from modules.tiktok_uploader import TikTokUploader, create_tiktok_notification
from modules.content_watcher import ContentWatcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocialMediaAutomation:
    """Orqestablece la automatización completa de redes sociales"""
    
    def __init__(self):
        self.video_generator = VideoGenerator()
        self.telegram_publisher = TelegramPublisher()
        self.tiktok_uploader = TikTokUploader()
        self.content_watcher = ContentWatcher()
        
        self.log_dir = Path("./automation_logs")
        self.log_dir.mkdir(exist_ok=True)
    
    def _log_automation(self, status: str, product: str, details: Dict):
        """Registra evento de automatización"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'status': status,
                'product': product,
                'details': details
            }
            
            log_file = self.log_dir / f"automation_{datetime.now().strftime('%Y%m%d')}.log"
            with open(log_file, 'a') as f:
                import json
                f.write(json.dumps(log_entry) + '\n')
            
        except Exception as e:
            logger.warning(f"⚠️ Error registrando log: {e}")
    
    async def process_new_product(self, post_data: Dict) -> Dict:
        """
        Procesa un nuevo producto: genera video → publica en redes
        
        Args:
            post_data: Datos del nuevo artículo
        
        Returns:
            Diccionario con resultados de publicación
        """
        results = {
            'product': post_data['product_name'],
            'video_generated': False,
            'telegram_published': False,
            'tiktok_queued': False,
            'errors': []
        }
        
        try:
            logger.info(f"\n🚀 Iniciando automatización para: {post_data['product_name']}")
            
            # PASO 1: Generar video
            logger.info("1️⃣ Generando video...")
            video_path = self.video_generator.generate_product_video(
                product_name=post_data['product_name'],
                product_image_url=post_data['image_url'],
                price=post_data['price'],
                affiliate_link=post_data['affiliate_link']
            )
            
            if not video_path:
                results['errors'].append("Falló generación de video")
                self._log_automation('FAILED', post_data['product_name'], results)
                return results
            
            results['video_generated'] = True
            logger.info(f"✅ Video generado: {Path(video_path).name}")
            
            # PASO 2: Publicar en Telegram
            if self.telegram_publisher.is_ready():
                logger.info("2️⃣ Publicando en Telegram...")
                
                telegram_result = publish_product_video_sync(
                    video_path=video_path,
                    product_name=post_data['product_name'],
                    price=post_data['price'],
                    affiliate_link=post_data['affiliate_link']
                )
                
                if telegram_result:
                    results['telegram_published'] = True
                    logger.info("✅ Publicado en Telegram")
                else:
                    results['errors'].append("Falló publicación en Telegram")
                    logger.warning("⚠️ Error publicando en Telegram")
            else:
                logger.warning("⚠️ Telegram no configurado")
            
            # PASO 3: Notificar para TikTok (upload manual)
            logger.info("3️⃣ Preparando para TikTok...")
            
            tiktok_result = self.tiktok_uploader.queue_for_manual_upload(
                video_path=video_path,
                title=post_data['product_name'],
                description=post_data['description']
            )
            
            if tiktok_result:
                results['tiktok_queued'] = True
                logger.info("✅ Video encolado para TikTok")
                
                # Generar instrucciones de upload manual
                instructions = create_tiktok_notification(
                    product_name=post_data['product_name'],
                    video_path=video_path,
                    affiliate_link=post_data['affiliate_link']
                )
                
                # Mostrar instrucciones
                print(instructions)
            else:
                results['errors'].append("Falló encolamiento en TikTok")
            
            # Registrar éxito
            self._log_automation('SUCCESS', post_data['product_name'], results)
            logger.info(f"🎉 Automatización completada para: {post_data['product_name']}\n")
            
        except Exception as e:
            results['errors'].append(str(e))
            self._log_automation('ERROR', post_data['product_name'], results)
            logger.error(f"❌ Error en automatización: {e}")
        
        finally:
            # Limpiar temporales
            self.video_generator.cleanup_temp_files()
        
        return results
    
    def display_summary(self, results: Dict):
        """Muestra resumen de resultados"""
        print("\n" + "="*70)
        print("📊 RESUMEN DE AUTOMATIZACIÓN")
        print("="*70)
        print(f"Producto: {results['product']}")
        print(f"Video generado: {'✅ SÍ' if results['video_generated'] else '❌ NO'}")
        print(f"Telegram publicado: {'✅ SÍ' if results['telegram_published'] else '⚠️ NO'}")
        print(f"TikTok encolado: {'✅ SÍ' if results['tiktok_queued'] else '⚠️ NO'}")
        
        if results['errors']:
            print(f"\nErrores:")
            for error in results['errors']:
                print(f"  • {error}")
        
        print("="*70 + "\n")
    
    async def process_all_new_products(self) -> Dict:
        """
        Procesa todos los nuevos productos detectados
        
        Returns:
            Resumen de todas las publicaciones
        """
        new_posts = self.content_watcher.get_new_posts()
        
        if not new_posts:
            logger.info("✅ No hay artículos nuevos para procesar")
            return {'total': 0, 'successful': 0, 'failed': 0}
        
        summary = {
            'total': len(new_posts),
            'successful': 0,
            'failed': 0,
            'results': []
        }
        
        for post in new_posts:
            result = await self.process_new_product(post)
            summary['results'].append(result)
            
            if not result['errors']:
                summary['successful'] += 1
            else:
                summary['failed'] += 1
            
            # Marcar como procesado
            self.content_watcher.mark_as_processed(post['filename'])
        
        return summary


def display_automation_menu():
    """Muestra menú de opciones"""
    print("\n" + "="*70)
    print("🤖 AUTOMATIZACIÓN DE REDES SOCIALES")
    print("="*70)
    print("1. Procesar nuevos artículos")
    print("2. Verificar artículos nuevos")
    print("3. Configurar Telegram")
    print("4. Ver logs de automatización")
    print("5. Salir")
    print("="*70)


async def main():
    """Función principal"""
    automation = SocialMediaAutomation()
    
    while True:
        display_automation_menu()
        choice = input("\n👉 Selecciona opción (1-5): ").strip()
        
        if choice == '1':
            # Procesar nuevos
            logger.info("🔄 Detectando nuevos artículos...")
            summary = await automation.process_all_new_products()
            
            print("\n" + "="*70)
            print("📊 RESUMEN FINAL")
            print("="*70)
            print(f"Total procesados: {summary['total']}")
            print(f"Éxitosos: {summary['successful']} ✅")
            print(f"Fallidos: {summary['failed']} ❌")
            print("="*70 + "\n")
            
        elif choice == '2':
            # Verificar nuevos
            new_posts = automation.content_watcher.get_new_posts()
            automation.content_watcher.display_new_posts(new_posts)
            
        elif choice == '3':
            # Configurar Telegram
            from modules.telegram_setup import interactive_setup
            interactive_setup()
            
        elif choice == '4':
            # Ver logs
            log_file = automation.log_dir / f"automation_{datetime.now().strftime('%Y%m%d')}.log"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    print("\n" + f.read())
            else:
                print("❌ No hay logs disponibles")
            
        elif choice == '5':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        # Modo automático: procesar sin menú
        logger.info("⚙️ Modo automático activado")
        automation = SocialMediaAutomation()
        asyncio.run(automation.process_all_new_products())
    else:
        # Modo interactivo
        asyncio.run(main())
