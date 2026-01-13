import logging
import os
from datetime import datetime
from config import LOG_FILE  # .env'de tanımlı (ör: C:\logs\musteri_sikayet.log)

_current_log_file = None


def init_logger(excel_path: str | None = None):
    """
    Her Excel işleminde ayrı bir log dosyası açar.
    LOG_FILE'in klasörünü baz alır.
    Ör: LOG_FILE = C:\\logs\\musteri_sikayet.log ise -> C:\\logs klasörünü kullanır.
    """
    global _current_log_file

    # LOG_FILE'den klasör çıkar
    if LOG_FILE:
        base_dir = os.path.dirname(LOG_FILE)
        if not base_dir:
            base_dir = "logs"
    else:
        base_dir = "logs"

    os.makedirs(base_dir, exist_ok=True)

    # Excel adına göre anlamlı bir log ismi üret
    if excel_path:
        excel_name = os.path.splitext(os.path.basename(excel_path))[0]
    else:
        excel_name = "excel"

    log_name = f"log_{excel_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    full_path = os.path.join(base_dir, log_name)

    # basicConfig'i yeniden kur (force=True ile önceki ayarları sıfırla)
    logging.basicConfig(
        filename=full_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
    )

    _current_log_file = full_path
    print(f"[LOGGER] Aktif log dosyası: {full_path}")


def log(msg):
    logging.info(msg)
    print(msg)