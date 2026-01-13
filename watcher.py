"""
This module implements a file watcher that monitors a specified folder for changes to an Excel file.
It uses the watchdog library to detect file system events and processes the Excel file after a configurable delay
to ensure the file is not being modified during the save operation.
"""

import os
import threading
import time
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from config import WATCH_FOLDER, EXCEL_FILE, DELAY_MINUTES
from excel_processor import process_excel
from logger import log

timer = None

class ExcelEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        global timer

        print("\n=== EVENT TETIKLENDI ===", flush=True)
        print(f"event.event_type: {event.event_type}", flush=True)
        print(f"event.src_path: {event.src_path}", flush=True)
        log(f"🟡 Event alındı: {event.event_type} - {event.src_path}")

        if event.is_directory:
            print("➡ Dizin olayı, atlandı.", flush=True)
            log("➡ Dizin olayı, atlandı.")
            return

        filename = os.path.basename(event.src_path)
        print(f"📄 Dosya adı: {filename}", flush=True)
        log(f"📄 Dosya adı: {filename}")

        # geçici excel
        if filename.startswith("~$"):
            print("⚠ Geçici Excel dosyası → işlem yok.", flush=True)
            log("⚠ Geçici Excel dosyası → işlem yok.")
            return

        # gerçek excel dosyası
        if filename == EXCEL_FILE:
            print(f"📥 GERÇEK Excel değişti: {filename}", flush=True)
            log(f"📥 GERÇEK Excel değişti: {filename}")

            # eski timer varsa iptal et
            if timer:
                print("🛑 Timer iptal edildi", flush=True)
                log("🛑 Timer iptal edildi")
                timer.cancel()

            # işlenecek gerçek yol
            real_path = os.path.join(WATCH_FOLDER, EXCEL_FILE)
            print(f"📌 İşlenecek dosya: {real_path}", flush=True)
            log(f"📌 İşlenecek dosya: {real_path}")

            # TIMER BAŞLAT (daemon=False)
            print(f"⏳ Timer başlıyor ({DELAY_MINUTES} dakika)...", flush=True)
            log(f"⏳ Timer başlıyor ({DELAY_MINUTES} dakika)...")

            timer = threading.Timer(DELAY_MINUTES * 60, safe_process, [real_path])
            timer.daemon = False     # 🔥 ÇÖZÜM
            timer.start()

            print("⏳ Kullanıcı kaydetme işlemini bitirsin diye bekleniyor.", flush=True)
            log("⏳ Kullanıcı kaydetme işlemini bitirsin diye bekleniyor.")
        else:
            print("➡ İlgisiz dosya, geçildi.", flush=True)
            log("➡ İlgisiz dosya, geçildi.")

def safe_process(path):
    print("🚀 Timer tetiklendi → safe_process CALLED", flush=True)
    log("🚀 Timer tetiklendi → safe_process çalışıyor")
    try:
        process_excel(path)
    except Exception as e:
        print(f"❌ process_excel TIMER hatası: {e}", flush=True)
        log(f"❌ process_excel TIMER hatası: {e}")

def start_watcher():
    print("🚀 start_watcher() çağrıldı", flush=True)
    log("📡 Excel watcher başlatıldı...")

    print(f"👁 İzlenen klasör: {WATCH_FOLDER}", flush=True)
    print(f"👁 İzlenen Excel:  {EXCEL_FILE}", flush=True)

    event_handler = ExcelEventHandler()
    observer = PollingObserver()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)

    print("▶ Observer başlatılıyor...", flush=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Observer durduruluyor...", flush=True)
        observer.stop()

    observer.join()
    print("🔚 Observer kapandı.", flush=True)
