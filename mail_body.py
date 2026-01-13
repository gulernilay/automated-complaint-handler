def generate_mail_body(row_dict):
    def fmt(value):
        return value if value not in [None, "", "nan"] else "-"

    return f"""
    <html>
    <body style="font-family:Arial; font-size:14px;">

        <h2 style="color:#d9534f;"> Yeni Müşteri Şikayet Kaydı Eklendi</h2>

        <p>Aşağıdaki bilgiler Müşteri Şikayetleri Exceline yeni eklenen şikayet kaydına aittir:</p>

        <hr>

        <p> <b>Şikayet Tarihi:</b> {fmt(row_dict.get('Şikayet_Tarihi'))}</p>
        <p> <b>Ay / Yıl:</b> {fmt(row_dict.get('Ay'))} / {fmt(row_dict.get('Yıl'))}</p>

        <p> <b>Müşteri / Mağaza:</b> {fmt(row_dict.get('Şikayeti_Yapan_Müşteri_Adı'))}</p>
        <p> <b>Ürün Grubu:</b> {fmt(row_dict.get('Ürün_Grubu'))}</p>
        <p> <b>Ürün İsmi:</b> {fmt(row_dict.get('Ürün_İsmi'))}</p>
        <p> <b>Üretim Yılı:</b> {fmt(row_dict.get('Ürün_Üretim_Yılı'))}</p>
        <p> <b>Parti No:</b> {fmt(row_dict.get('Parti_No'))}</p>
        <p> <b>STT / TETT:</b> {fmt(row_dict.get('STT_TETT'))}</p>

        <p> <b>Şikayet Konu Grubu:</b> {fmt(row_dict.get('Şikayet_Konu_Grubu'))}</p>
        <p> <b>Şikayet Detayı:</b><br>{fmt(row_dict.get('Şikayet_Konusu'))}</p>

        <p> <b>Çözüm / Yapılan İşlem:</b><br>{fmt(row_dict.get('Şikayet_Çözümü'))}</p>

        <p> <b>Müşteriye Dönüş Tarihi:</b> {fmt(row_dict.get('Şikayete_Dönüş_Tarihi'))}</p>
        <p> <b>Dönüş Süresi (Gün):</b> {fmt(row_dict.get('Şikayete_Dönüş_Süresi_Gün'))}</p>

        <p> <b>Sonuç:</b> {fmt(row_dict.get('Sonuç'))}</p>
        <p> <b>Üretim Hatalı:</b> {fmt(row_dict.get('Üretim_Hatalı'))}</p>

        <hr>

        <p>Bilginize sunarız.<br>
        <b>Chef Seasons – Şikayet Yönetim Sistemi</b></p>

    </body>
    </html>
    """
