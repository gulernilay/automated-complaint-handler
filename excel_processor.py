import pandas as pd
from config import TARGET_TABLE
from db import upsert_row
from logger import log, init_logger   # ⬅️ BURAYI GÜNCELLE
from mailer import send_mail
from mail_body import generate_mail_body
import time
from preprocess import preprocess_dataframe


def process_excel(path):
    # 🔹 Her Excel işlemi için yeni log dosyası
    init_logger(path)
    print(f"📂 Excel işleme başlıyor: {path}")
    log(f"📂 Excel işleme başlıyor: {path}")

    # Excel dosyası kilitliyse birkaç kez dene
    for i in range(5):
        try:
            df = pd.read_excel(path, engine="openpyxl", header=2)
            df = preprocess_dataframe(df)
            log(f"📄 Excel'den okunan satır sayısı: {len(df)} (ilk 2 satır atlandı)")
            print(f"📄 Excel'den okunan satır sayısı: {len(df)} (ilk 2 satır atlandı)")
            break
        except Exception as e:
            log(f"🔒 Dosya kilitli, {i+1}. deneme... Hata: {e}")
            print(f"🔒 Dosya kilitli, {i+1}. deneme... Hata: {e}")
            time.sleep(2)
    else:
        log("❌ Dosya sürekli kilitli kaldı, işlem iptal edildi.")
        print("❌ Dosya sürekli kilitli kaldı, işlem iptal edildi.")
        return

    try:
        inserted_rows = []

        for _, row in df.iterrows():
            result, row_dict = upsert_row(TARGET_TABLE, row)

            if result == "insert":
                inserted_rows.append(row_dict)

        log(f"Toplam satır işlendi: {len(df)}")
        log(f"Yeni eklenen şikayet sayısı: {len(inserted_rows)}")
        print(f"Toplam satır işlendi: {len(df)}")
        print(f"Yeni eklenen şikayet sayısı: {len(inserted_rows)}")

        if not inserted_rows:
            log("📭 Yeni şikayet eklenmedi, mail gönderilmeyecek.")
            print("📭 Yeni şikayet eklenmedi, mail gönderilmeyecek.")
            return

        for r in inserted_rows:
            mail_subject = "Müşteri Şikayetleri Exceline Yeni Bir Şikayet Eklendi"
            mail_body = generate_mail_body(r)
            send_mail(mail_subject, mail_body)

    except Exception as e:
        log(f"❌ SQL hata: {str(e)}")
        print(f"❌ SQL hata: {str(e)}")