#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Automation Scheduler - Ejecuta la automatización en intervalos programados
"""

import logging
import schedule
import time
import threading
from datetime import datetime
from modules.social_media_automation import SocialMediaAutomation
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutomationScheduler:
    """Programa y ejecuta tareas de automatización"""
    
    def __init__(self):
        self.automation = SocialMediaAutomation()
        self.scheduler = schedule.Scheduler()
        self.running = False
        self.thread = None
    
    def schedule_tasks(
        self,
        check_interval: int = 300,
        watch_interval: int = 5
    ):
        """
        Programa las tareas
        
        Args:
            check_interval: Intervalo de chequeo en segundos (default: 5 minutos)
            watch_interval: Horas de repetición (default: diariamente cada 5 horas)
        """
        
        # Tarea 1: Chequear nuevos productos cada N segundos
        self.scheduler.every(check_interval).seconds.do(self._check_new_products)
        
        # Tarea 2: Limpiar temporales cada 24 horas
        self.scheduler.every().day.at("03:00").do(self._cleanup_temp_files)
        
        # Tarea 3: Generar reporte diario
        self.scheduler.every().day.at("08:00").do(self._daily_report)
        
        logger.info(f"✅ Tareas programadas")
        logger.info(f"   • Chequeo cada {check_interval}s")
        logger.info(f"   • Limpieza diaria a las 03:00")
        logger.info(f"   • Reporte diario a las 08:00")
    
    def _check_new_products(self):
        """Chequea productos nuevos (tarea programada)"""
        logger.info(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] Verificando nuevos artículos...")
        
        try:
            # Ejecutar en event loop asincrónico
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            summary = loop.run_until_complete(
                self.automation.process_all_new_products()
            )
            
            loop.close()
            
            if summary['total'] > 0:
                logger.info(f"✅ Procesados: {summary['successful']}")
                if summary['failed'] > 0:
                    logger.warning(f"⚠️ Fallidos: {summary['failed']}")
            else:
                logger.info("✅ No hay artículos nuevos")
                
        except Exception as e:
            logger.error(f"❌ Error en chequeo: {e}")
    
    def _cleanup_temp_files(self):
        """Limpia archivos temporales"""
        logger.info("🧹 Limpiando archivos temporales...")
        self.automation.video_generator.cleanup_temp_files()
    
    def _daily_report(self):
        """Genera reporte diario"""
        logger.info("📊 Generando reporte diario...")
        
        # Leer logs del día
        log_file = self.automation.log_dir / datetime.now().strftime('automation_%Y%m%d.log')
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            logger.info(f"📈 Eventos del día: {len(lines)}")
        else:
            logger.info("📈 Sin eventos hoy")
    
    def start(self):
        """Inicia el scheduler en background"""
        if self.running:
            logger.warning("⚠️ Scheduler ya está corriendo")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info(f"✅ Scheduler iniciado en background")
    
    def _run_scheduler(self):
        """Ejecuta el scheduler (corre en thread aparte)"""
        logger.info("🔄 Scheduler ejecutándose...")
        
        while self.running:
            try:
                self.scheduler.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"❌ Error en scheduler: {e}")
                time.sleep(5)
    
    def stop(self):
        """Detiene el scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("⏹️ Scheduler detenido")
    
    def show_schedule(self):
        """Muestra calendario de próximas ejecuciones"""
        print("\n" + "="*70)
        print("📅 PRÓXIMAS TAREAS PROGRAMADAS")
        print("="*70)
        
        if not self.scheduler.jobs:
            print("❌ No hay tareas programadas")
        else:
            for job in self.scheduler.jobs:
                print(f"\n⏱️  {job.job_func.__name__}")
                print(f"   Intervalo: {job.interval} {job.unit}")
                print(f"   Próxima ejecución: {job.next_run}")
        
        print("\n" + "="*70 + "\n")


# Comandos de utilidad
def run_scheduler_interactive():
    """Ejecuta scheduler en modo interactivo"""
    scheduler = AutomationScheduler()
    scheduler.schedule_tasks(check_interval=60)  # Chequear cada minuto en demo
    
    print("\n" + "="*70)
    print("🤖 AUTOMATION SCHEDULER")
    print("="*70)
    print("1. Iniciar scheduler")
    print("2. Ver próximas tareas")
    print("3. Ejecutar chequeo manual")
    print("4. Detener scheduler")
    print("5. Salir")
    print("="*70)
    
    scheduler.start()
    
    try:
        while True:
            choice = input("\n👉 Selecciona opción (1-5): ").strip()
            
            if choice == '1':
                if not scheduler.running:
                    scheduler.start()
                    print("✅ Scheduler iniciado")
                else:
                    print("⚠️ Scheduler ya está corriendo")
                    
            elif choice == '2':
                scheduler.show_schedule()
                
            elif choice == '3':
                print("🔄 Ejecutando chequeo manual...")
                scheduler._check_new_products()
                
            elif choice == '4':
                scheduler.stop()
                print("✅ Scheduler detenido")
                
            elif choice == '5':
                scheduler.stop()
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida")
                
    except KeyboardInterrupt:
        scheduler.stop()
        print("\n👋 Scheduler detenido")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--background':
        # Modo background
        logger.info("⚙️ Iniciando scheduler en background...")
        scheduler = AutomationScheduler()
        scheduler.schedule_tasks(check_interval=300)  # Chequear cada 5 minutos
        scheduler.start()
        
        logger.info("🔄 Scheduler corriendo en background")
        logger.info("Presiona Ctrl+C para detener\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            scheduler.stop()
            
    else:
        # Modo interactivo
        run_scheduler_interactive()
