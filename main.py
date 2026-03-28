#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main script para ejecutar la automatización completa de TechBlogOfertas
"""

import asyncio
import logging

from modules.social_media_automation import SocialMediaAutomation
from modules.automation_scheduler import AutomationScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_once():
    automation = SocialMediaAutomation()
    summary = asyncio.run(automation.process_all_new_products())

    logger.info('--- RESUMEN EJECUCIÓN ÚNICA ---')
    logger.info('Total: %s', summary['total'])
    logger.info('Exitosos: %s', summary['successful'])
    logger.info('Fallidos: %s', summary['failed'])


def run_scheduler():
    scheduler = AutomationScheduler()
    scheduler.schedule_tasks(check_interval=300)
    scheduler.start()

    try:
        logger.info('Scheduler iniciado. Presiona Ctrl+C para terminar.')
        while True:
            asyncio.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        logger.info('Scheduler detenido por usuario')


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--scheduler':
        run_scheduler()
    else:
        run_once()
