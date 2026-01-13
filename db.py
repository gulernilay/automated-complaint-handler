import pyodbc
import hashlib
import json
from config import *
from logger import log


def get_connection():
    return pyodbc.connect(
        f"DRIVER={{{SQL_DRIVER}}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USERNAME};"
        f"PWD={SQL_PASSWORD};"
    )


def _clean_value(v):
    """numpy.nan, boş string vs. -> None çevirir"""
    import pandas as pd
    if isinstance(v, float) and pd.isna(v):
        return None
    if v in ["", " ", "-", "NA", "N/A", "null", "nan", None]:
        return None
    return v


def _build_row_hash(row_dict):
    """Satırın tamamına göre hash üretir. Tüm date objelerini string'e çevirir."""
    import datetime

    # Tüm değerleri temizle + date/datetime ise string yap
    clean_dict = {}
    for k, v in row_dict.items():
        v = _clean_value(v)

        # datetime.date veya datetime.datetime -> string
        if isinstance(v, (datetime.date, datetime.datetime)):
            v = v.strftime("%Y-%m-%d")

        clean_dict[k] = v

    raw_json = json.dumps(clean_dict, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw_json.encode("utf-8")).hexdigest()


def upsert_row(table, row_series):
    """
    ID'ye bakmaz.
    Satırın tam içeriğine göre RowHash üretir.
    Eğer RowHash zaten varsa -> 'no_change'
    Yoksa -> INSERT + 'insert'
    """
    import pandas as pd

    conn = get_connection()
    cursor = conn.cursor()

    # Excel satırını dict'e çevir + temizle
    rd = row_series.to_dict()
    row_clean = {k: _clean_value(v) for k, v in rd.items()}

    # 1) Satır hash'i üret
    row_hash = _build_row_hash(row_clean)

    # 2) Bu satır daha önce eklenmiş mi? (RowHash bazlı kontrol)
    cursor.execute(f"SELECT 1 FROM {table} WHERE RowHash = ?", row_hash)
    exists = cursor.fetchone()

    if exists:
        # Aynı satır zaten var -> hiçbir şey yapma
        cursor.close()
        conn.close()
        return "no_change", row_clean

    # 3) Yeni satır -> INSERT
    # SQL tablosundaki kolonlar (ID hariç; DB'de IDENTITY olması muhtemel)
    SQL_COLUMNS = [
        "Şikayet_Tarihi",
        "Ay",
        "Yıl",
        "Şikayeti_Yapan_Müşteri_Adı",
        "Ürün_Grubu",
        "Ürün_İsmi",
        "Ürün_Üretim_Yılı",
        "Parti_No",
        "STT_TETT",
        "Şikayet_Konu_Grubu",
        "Şikayet_Konusu",
        "Şikayet_Çözümü",
        "Şikayete_Dönüş_Tarihi",
        "Döf_No",
        "Şikayete_Dönüş_Süresi_Gün",
        "Sonuç",
        "Üretim_Hatalı",
    ]

    # RowHash'i de ekliyoruz
    insert_columns = SQL_COLUMNS + ["RowHash"]

    col_clause = ",".join(f"[{c}]" for c in insert_columns)
    placeholders = ",".join(["?"] * len(insert_columns))

    insert_values = [row_clean.get(col) for col in SQL_COLUMNS] + [row_hash]

    sql = f"INSERT INTO {table} ({col_clause}) VALUES ({placeholders})"

    cursor.execute(sql, insert_values)
    conn.commit()
    cursor.close()
    conn.close()

    # Mail body vs. için hash'i de döndürmek istersen:
    row_clean["RowHash"] = row_hash

    return "insert", row_clean
