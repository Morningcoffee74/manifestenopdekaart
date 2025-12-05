# 🗺️ Manifesten op de Kaart - Demo Versie

Een interactieve kaartapplicatie om convenanten en samenwerkingsverbanden van Nederlandse overheden te visualiseren.

## ✨ Functionaliteit (Fase 0 - Demo)

### Tab 1: Kaart View
- Interactieve kaart van Nederland
- Meerdere kaartlagen tegelijk zichtbaar:
  - Gemeenten
  - Provincies
  - Waterschappen
  - Semi-overheden (punten)
- Klik op gebied → zie convenanten in sidebar
- Zoekfunctie voor overheden

### Tab 2: Convenant View
- Selecteer één of meerdere convenanten
- Zie op kaart welke overheden deze hebben ondertekend
- Overheden worden rood gehighlight

## 📋 Convenanten (demo data)

- Schoon en Emissieloos Bouwen
- MVOI ondertekend
- MVOI actieplan gereed
- SDG-gemeenten
- Schone Lucht Akkoord (SLA)
- Green Deal Biobased Bouwen
- Manifest Het Nieuwe Normaal (HNN)
- Nationaal Programma Circulaire Economie (NPCE)
- VNG-Programma Klimaatadaptatie

## 🚀 Installatie & Gebruik

### Optie A: Lokaal draaien

1. **Python installeren** (versie 3.9 of hoger)
   ```bash
   python --version
   ```

2. **Dependencies installeren**
   ```bash
   pip install -r requirements.txt
   ```

3. **App starten**
   ```bash
   streamlit run app.py
   ```

4. **Browser openen**
   - Ga naar: http://localhost:8501

### Optie B: Deployen op Streamlit Cloud

1. **GitHub repository aanmaken**
   - Ga naar github.com
   - Klik "New repository"
   - Zet op **Private**
   - Upload alle bestanden

2. **Streamlit Cloud**
   - Ga naar share.streamlit.io
   - Log in met GitHub
   - Klik "New app"
   - Selecteer je repository
   - Main file: `app.py`
   - Klik "Deploy"

3. **Klaar!**
   - Na 2 minuten is app live
   - Deel de link met collega's

## 📁 Projectstructuur

```
manifesten-op-de-kaart/
├── app.py                  # Hoofdapplicatie
├── requirements.txt        # Python dependencies
├── README.md              # Deze file
└── data/                  # (Voor later: CSV bestanden, GeoJSON data)
```

## 🔄 Volgende stappen (Fase 1+)

- [ ] SQLite database toevoegen
- [ ] CSV import functionaliteit
- [ ] Login systeem voor bewerken
- [ ] Echte GeoJSON data (CBS, PDOK)
- [ ] Inkoopcombinaties toevoegen
- [ ] Export functionaliteit
- [ ] CRM uitbreidingen

## 📝 Notities

**Demo beperkingen:**
- Gebruikt vereenvoudigde kaartdata (6 gemeenten, 2 provincies, 2 waterschappen)
- Dummy convenanten data
- Geen database (alles in memory)
- Geen login systeem

**Voor productie nodig:**
- Volledige GeoJSON data downloaden van CBS/PDOK
- SQLite database opzetten
- CSV import bouwen
- Mac Mini of cloud hosting

## 🆘 Hulp nodig?

- Streamlit docs: https://docs.streamlit.io
- Folium docs: https://python-visualization.github.io/folium/

---

**Versie:** 0.1 (Demo)  
**Datum:** December 2024
