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

    def _build_caption(self, title: str, affiliate_link: str) -> str:
        return "🔥 {}\n💰 Mejor precio hoy\n👉 {}\n#tecnologia #gadgets #ofertas".format(title, affiliate_link)

    def publish_photo_with_text(self, image_path: str, title: str, affiliate_link: str) -> bool:
        caption = self._build_caption(title, affiliate_link)

        try:
            with open(image_path, 'rb') as photo:
                self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode='HTML'
                )
            logger.info('✅ Mensaje publicado en Telegram: %s', title)
            return True

        except TelegramError as e:
            logger.error('❌ Error publicando en Telegram: %s', e)
            return False
        except FileNotFoundError:
            logger.error('❌ Archivo no encontrado: %s', image_path)
            return False


def publish_product_to_telegram(image_path: str, title: str, affiliate_link: str) -> bool:
    publisher = TelegramPublisher()
    return publisher.publish_photo_with_text(image_path=image_path, title=title, affiliate_link=affiliate_link)


def publish_product_video_sync(video_path: str, product_name: str, price: str, affiliate_link: str) -> bool:
    publisher = TelegramPublisher()
    caption = publisher._build_caption(product_name, affiliate_link)
    return publisher.publish_photo(image_path=video_path, caption=caption)


if __name__ == '__main__':
    logger.info('🟢 Telegram Publisher - TechBlogOfertas')
    logger.info('Canal: %s', TELEGRAM_CHANNEL)

    sample_image = BASE_DIR / 'videos_generados' / 'test.jpg'
    if sample_image.exists():
        publish_product_to_telegram(str(sample_image), 'iPhone 15 Pro', 'https://www.amazon.es/s?k=iPhone+15+Pro')
    else:
        logger.warning('⚠️ No se encontró imagen de ejemplo en videos_generados/test.jpg')
