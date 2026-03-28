#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Video Generator - Crea videos automáticos para promoción en redes sociales
Genera videos verticales (1080x1920) para TikTok y Telegram
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.VideoClip import ImageClip, TextClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
import requests
from typing import Optional, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoGenerator:
    """Generador de videos automáticos para redes sociales"""
    
    def __init__(self):
        self.output_dir = Path("./videos_generados")
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("./temp_video")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Dimensiones de video vertical (TikTok/Instagram Reels)
        self.width = 1080
        self.height = 1920
        self.fps = 30
        
    def download_product_image(self, image_url: str, product_name: str) -> Optional[str]:
        """Descarga imagen del producto desde URL"""
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                # Guardar imagen temporal
                image_path = self.temp_dir / f"{product_name.replace(' ', '_')}_product.jpg"
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"✅ Imagen descargada: {product_name}")
                return str(image_path)
        except Exception as e:
            logger.error(f"❌ Error descargando imagen: {e}")
        return None
    
    def create_background_frame(self, background_color: tuple = (20, 25, 45)) -> str:
        """Crea un fondo gradiente para el video"""
        img = Image.new('RGB', (self.width, self.height), background_color)
        
        # Crear gradiente desde arriba hacia abajo
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Gradiente azul a púrpura
        for y in range(self.height):
            ratio = y / self.height
            r = int(background_color[0] + (100 - background_color[0]) * ratio)
            g = int(background_color[1] + (60 - background_color[1]) * ratio)
            b = int(background_color[2] + (150 - background_color[2]) * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        bg_path = self.temp_dir / "background.png"
        img.save(bg_path)
        return str(bg_path)
    
    def create_product_frame(self, image_path: str, product_name: str) -> str:
        """Crea frame con imagen del producto"""
        try:
            # Cargar imagen del producto
            product_img = Image.open(image_path)
            
            # Redimensionar para que quepan en el frame vertical
            # Mantener aspecto, máximo 600x800
            product_img.thumbnail((600, 800), Image.Resampling.LANCZOS)
            
            # Crear lienzo
            frame = Image.new('RGB', (self.width, self.height), (15, 20, 40))
            
            # Pegar imagen en el centro-arriba
            x_offset = (self.width - product_img.width) // 2
            y_offset = 300  # Espacio desde arriba
            frame.paste(product_img, (x_offset, y_offset), 
                       product_img if product_img.mode == 'RGBA' else None)
            
            # Añadir sombra bajo el producto
            draw = ImageDraw.Draw(frame, 'RGBA')
            shadow_y = y_offset + product_img.height
            draw.ellipse(
                [x_offset - 50, shadow_y, x_offset + product_img.width + 50, shadow_y + 30],
                fill=(0, 0, 0, 50)
            )
            
            # Añadir título
            try:
                title_font = ImageFont.truetype(
                    "C:\\Windows\\Fonts\\arial.ttf", 
                    size=60
                )
                title_color = (255, 255, 255)
            except:
                title_font = ImageFont.load_default()
                title_color = (255, 255, 255)
            
            # Título centrado abajo
            lines = product_name.split()
            if len(product_name) > 20:
                # Partir en dos líneas
                mid = len(lines) // 2
                line1 = ' '.join(lines[:mid])
                line2 = ' '.join(lines[mid:])
                y_text = self.height - 250
                draw.text((self.width//2, y_text), line1, fill=title_color, 
                         font=title_font, anchor="mm")
                draw.text((self.width//2, y_text + 80), line2, fill=title_color, 
                         font=title_font, anchor="mm")
            else:
                draw.text((self.width//2, self.height - 200), product_name, 
                         fill=title_color, font=title_font, anchor="mm")
            
            frame_path = self.temp_dir / "frame_product.png"
            frame.save(frame_path)
            return str(frame_path)
            
        except Exception as e:
            logger.error(f"❌ Error creando frame del producto: {e}")
            return None
    
    def create_text_frame(self, title: str, subtitle: str, background_color=(20, 25, 45)) -> str:
        """Crea frame con texto"""
        frame = Image.new('RGB', (self.width, self.height), background_color)
        draw = ImageDraw.Draw(frame)
        
        try:
            title_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", size=80)
            subtitle_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", size=50)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Título principal
        draw.text((self.width//2, self.height//2 - 150), title, 
                 fill=(255, 215, 0), font=title_font, anchor="mm")
        
        # Subtítulo
        draw.text((self.width//2, self.height//2 + 100), subtitle, 
                 fill=(255, 255, 255), font=subtitle_font, anchor="mm")
        
        frame_path = self.temp_dir / f"frame_text_{subtitle}.png"
        frame.save(frame_path)
        return str(frame_path)
    
    def create_cta_frame(self, cta_text: str = "¡LINK EN BIO!") -> str:
        """Crea frame de call-to-action"""
        frame = Image.new('RGB', (self.width, self.height), (255, 107, 0))
        draw = ImageDraw.Draw(frame)
        
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", size=120)
        except:
            font = ImageFont.load_default()
        
        # Texto CTA
        draw.text((self.width//2, self.height//2), cta_text, 
                 fill=(255, 255, 255), font=font, anchor="mm")
        
        # Flecha
        try:
            arrow_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", size=150)
        except:
            arrow_font = font
        
        draw.text((self.width//2, self.height//2 + 250), "⬇️", 
                 fill=(255, 255, 255), font=arrow_font, anchor="mm")
        
        frame_path = self.temp_dir / "frame_cta.png"
        frame.save(frame_path)
        return str(frame_path)
    
    def generate_product_video(
        self, 
        product_name: str,
        product_image_url: str,
        price: str = "Mejor precio",
        affiliate_link: str = "@web7blogg",
        duration: float = 10.0
    ) -> Optional[str]:
        """
        Genera video completo del producto
        
        Args:
            product_name: Nombre del producto
            product_image_url: URL de la imagen del producto
            price: Precio con descuento
            affiliate_link: Link afiliado o username
            duration: Duración total del video en segundos
        
        Returns:
            Ruta del archivo de video generado
        """
        try:
            logger.info(f"🎬 Generando video para: {product_name}")
            
            # Descargar imagen
            image_path = self.download_product_image(product_image_url, product_name)
            if not image_path:
                logger.error("❌ No se pudo descargar la imagen")
                return None
            
            clips = []
            frame_duration = 2  # Segundos por frame
            
            # Frame 1: Fondo + Imagen del producto (4 segundos)
            try:
                product_frame = self.create_product_frame(image_path, product_name)
                if product_frame:
                    clip1 = ImageClip(product_frame).with_duration(4)
                    clips.append(clip1)
            except Exception as e:
                logger.warning(f"⚠️ Error en frame del producto: {e}")
            
            # Frame 2: Precio y beneficios (2 segundos)
            try:
                price_frame = self.create_text_frame(
                    title=price,
                    subtitle="💰 Mejor precio del mercado"
                )
                clip2 = ImageClip(price_frame).with_duration(2)
                clips.append(clip2)
            except Exception as e:
                logger.warning(f"⚠️ Error en frame de precio: {e}")
            
            # Frame 3: Beneficio (2 segundos)
            try:
                benefit_frame = self.create_text_frame(
                    title="✅ Garantizado",
                    subtitle="Envío rápido"
                )
                clip3 = ImageClip(benefit_frame).with_duration(2)
                clips.append(clip3)
            except Exception as e:
                logger.warning(f"⚠️ Error en frame de beneficio: {e}")
            
            # Frame 4: CTA (2 segundos)
            try:
                cta_frame = self.create_cta_frame()
                clip4 = ImageClip(cta_frame).with_duration(2)
                clips.append(clip4)
            except Exception as e:
                logger.warning(f"⚠️ Error en frame CTA: {e}")
            
            if not clips:
                logger.error("❌ No se crearon clips")
                return None
            
            # Concatenar clips
            final_video = concatenate_videoclips(clips)
            
            # Redimensionar al tamaño exacto requerido
            final_video = final_video.resize((self.width, self.height))
            
            # Guardar video
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"video_{product_name.replace(' ', '_')}_{timestamp}.mp4"
            
            logger.info(f"💾 Guardando video: {output_path}")
            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                verbose=False,
                logger=None
            )
            
            # Limpiar clips
            for clip in clips:
                clip.close()
            final_video.close()
            
            logger.info(f"✅ Video generado exitosamente: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Error generando video: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Limpia archivos temporales"""
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                self.temp_dir.mkdir(exist_ok=True)
            logger.info("🧹 Archivos temporales limpiados")
        except Exception as e:
            logger.warning(f"⚠️ Error limpiando temporales: {e}")


# Ejemplo de uso
if __name__ == "__main__":
    generator = VideoGenerator()
    
    # Ejemplo: generar video de iPhone 15 Pro
    video_path = generator.generate_product_video(
        product_name="iPhone 15 Pro",
        product_image_url="https://m.media-amazon.com/images/I/71YSVP6VzAL._AC_SY679_.jpg",
        price="€1,099",
        affiliate_link="amazon.es/iPhone15Pro",
        duration=10
    )
    
    if video_path:
        print(f"\n✅ Video generado: {video_path}\n")
    else:
        print(f"\n❌ Error generando video\n")
    
    # Limpiar temporales
    generator.cleanup_temp_files()
