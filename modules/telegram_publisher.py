#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Telegram Publisher - Publica productos en canal de Telegram usando .env
"""

import os
import logging
from pathlib import Path
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / '.env')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL = os.getenv('TELEGRAM_CHANNEL', '@TechBlogOfertas')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError('TELEGRAM_BOT_TOKEN no configurado en .env')


class TelegramPublisher:
    def __init__(self):
        self.bot = Bot(TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHANNEL

    def _build_caption(self, title: str, price: str, link: str) -> str:
        return f"🔥 {title}\n🎧 Cancelación de ruido\n💰 {price}\n👉 {link}\n#gadgets #tecnologia #ofertas"

    async def publish_photo(self, image_path: str, caption: str) -> bool:
        try:
            with open(image_path, 'rb') as photo:
                await self.bot.send_photo(chat_id=self.chat_id, photo=photo, caption=caption)
            logger.info('✅ Imagen enviada a Telegram: %s', image_path)
            return True
        except TelegramError as e:
            logger.error('❌ Error enviando foto a Telegram: %s', e)
            return False
        except FileNotFoundError:
            logger.error('❌ Archivo no encontrado: %s', image_path)
            return False

    async def publish_video(self, video_path: str, caption: str) -> bool:
        try:
            with open(video_path, 'rb') as video:
                await self.bot.send_video(chat_id=self.chat_id, video=video, caption=caption)
            logger.info('✅ Video enviado a Telegram: %s', video_path)
            return True
        except TelegramError as e:
            logger.error('❌ Error enviando video a Telegram: %s', e)
            return False
        except FileNotFoundError:
            logger.error('❌ Archivo no encontrado: %s', video_path)
            return False


def publish_product_to_telegram(image_path: str, title: str, price: str, link: str) -> bool:
    publisher = TelegramPublisher()
    caption = publisher._build_caption(title, price, link)
    return publisher.publish_photo(image_path, caption)


def publish_product_video_sync(video_path: str, title: str, price: str, link: str) -> bool:
    publisher = TelegramPublisher()
    caption = publisher._build_caption(title, price, link)
    return asyncio.run(publisher.publish_video(video_path, caption))


if __name__ == '__main__':
    logger.info('🟢 Telegram Publisher - TechBlogOfertas')
    logger.info('Canal: %s', TELEGRAM_CHANNEL)

    sample_image = BASE_DIR / 'videos_generados' / 'test.jpg'
    if sample_image.exists():
        publish_product_to_telegram(str(sample_image), 'iPhone 15 Pro', 'https://www.amazon.es/s?k=iPhone+15+Pro')
    else:
        logger.warning('⚠️ No se encontró imagen de ejemplo en videos_generados/test.jpg')
