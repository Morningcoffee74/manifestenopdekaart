# 🚀 SNELSTART - Deploy in 10 minuten

## Stap 1: Download & Uitpakken
1. Download `overheidskaart-app.zip`
2. Dubbelklik op het bestand om uit te pakken
3. Je krijgt een map met alle bestanden

## Stap 2: GitHub Repository
1. Ga naar **github.com** en log in met je account
2. Klik rechtsboven op **+** → **New repository**
3. Vul in:
   - Repository name: `ManifestenOpDeKaart` (of je eigen naam)
   - Zet op **Private** ✓
4. Klik **Create repository**

## Stap 3: Upload Bestanden
1. Je ziet nu een lege repository pagina
2. Klik midden op de pagina op **"uploading an existing file"**
3. Sleep ALLE bestanden uit de uitgepakte map naar GitHub:
   - app.py
   - requirements.txt
   - README.md
   - .gitignore
4. Scroll naar beneden en klik **"Commit changes"**

## Stap 4: Streamlit Cloud
1. Ga naar **share.streamlit.io**
2. Klik **"Sign in"** → **"Continue with GitHub"**
3. Geef Streamlit toegang
4. Klik **"New app"** (rechtsboven, blauwe knop)
5. Selecteer:
   - Repository: `Morningcoffee74/ManifestenOpDeKaart`
   - Branch: `main`
   - Main file: `app.py`
6. Klik **"Deploy!"**

## Stap 5: Klaar!
- Wacht 2-3 minuten
- Je krijgt een URL: `https://xxx.streamlit.app`
- Deel deze link met collega's
- Iedereen kan de app nu gebruiken!

## 🎉 Wat kun je nu testen?

### Tab 1: Kaart View
- Vink kaartlagen aan/uit (gemeenten, provincies, waterschappen)
- Klik in dropdown op een overheid
- Bekijk welke convenanten ze hebben

### Tab 2: Convenant View
- Vink convenanten aan
- Zie welke overheden meedoen (rood op kaart)
- Test meerdere convenanten tegelijk

## ❓ Problemen?

**App start niet?**
- Check of alle bestanden zijn geüpload
- Kijk in Streamlit Cloud logs

**Vragen?**
- Stuur me de link naar je app
- Vertel wat niet werkt
