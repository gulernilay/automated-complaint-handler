import pandas as pd
import numpy as np
from datetime import datetime, date

# Geçersiz değer listesi
INVALID_VALUES = ["", " ", "-", "NA", "N/A", "n/a", "null", "None", "nan", None]

# -------------------------
# NUMERIC SAFETY FUNCTIONS
# -------------------------

def to_int_safe(value):
    """Excel'den gelen değerleri güvenli şekilde integer'a çevirir."""
    if pd.isna(value) or str(value).strip() in INVALID_VALUES:
        return None

    try:
        return int(float(str(value).replace(",", ".").strip()))
    except:
        return None


# -------------------------
# STRING NORMALIZATION
# -------------------------

def to_str_safe(value):
    """Boşluk, NA, -, None gibi tüm hatalı değerleri temiz bir string'e çevirir."""
    if pd.isna(value):
        return None
    v = str(value).strip()
    if v in INVALID_VALUES:
        return None
    return v


# -------------------------
# DATE PARSER (TÜRK FORMAT)
# -------------------------

def to_date_safe(value):
    """Tüm tarih formatlarını doğru şekilde parse eder (%d.%m.%Y dahil)."""
    if pd.isna(value) or str(value).strip() in INVALID_VALUES:
        return None

    # eğer zaten datetime ise direkt dönüştür
    if isinstance(value, (datetime, date)):
        return value.date()

    v = str(value).strip()

    try:
        # 25.03.2023 formatı
        if "." in v:
            return datetime.strptime(v, "%d.%m.%Y").date()

        # ISO tarih
        return pd.to_datetime(v, errors="coerce", dayfirst=True).date()
    except:
        return None


# -------------------------
# SPECIAL CLEANERS
# -------------------------

def clean_production_error(value):
    """Üretim Hatalı kolonunu normalize eder."""
    v = to_str_safe(value)
    if not v:
        return None

    v = v.lower()

    if v in ["hayır", "yok", "na", "n/a", "-", ""]:
        return "Hayır"

    if "hatalı" in v:
        return "Üretim Hatalı"

    if "aynı parti" in v:
        return "Aynı Partiden Tekrar"

    return v.capitalize()


# -------------------------
# MAIN PREPROCESS FUNCTION
# -------------------------

def preprocess_dataframe(df):
    df = df.copy()

    # Kolon isimlerini normalize et
    df.columns = [col.strip() for col in df.columns]

    # Tüm geçersiz değerleri temizle
    df = df.replace(INVALID_VALUES, np.nan)

    # Kolon dönüştürücüleri
    converters = {
    "ID": to_int_safe,
    "Şikayet_Tarihi": to_date_safe,
    "Ay": to_int_safe,
    "Yıl": to_int_safe,
    "Şikayeti_Yapan_Müşteri_Adı": to_str_safe,
    "Ürün_Grubu": to_str_safe,
    "Ürün_İsmi": to_str_safe,
    "Ürün_Üretim_Yılı": to_str_safe,
    "Parti_No": to_str_safe,
    "STT_TETT": to_str_safe,
    "Şikayet_Konu_Grubu": to_str_safe,
    "Şikayet_Konusu": to_str_safe,
    "Şikayet_Çözümü": to_str_safe,
    "Şikayete_Dönüş_Tarihi": to_date_safe,
    "Döf_No": to_str_safe,
    "Şikateye_Dönüş_Süresi_Gün": to_int_safe,
    "Sonuç": to_str_safe,
    "Üretim_Hatalı": clean_production_error,
    }

    # Kolon kolon dönüştür
    for col, func in converters.items():
        if col in df.columns:
            df[col] = df[col].apply(func)

    # ----------------------------------------
    # 🔥 SQL tablo kolon sırasıyla birebir eşitleme
    # ----------------------------------------
    EXPECTED_ORDER = [
    "ID",
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
    "Üretim_Hatalı"
    ]

    df = df.reindex(columns=EXPECTED_ORDER)

    return df

