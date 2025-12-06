import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json
from folium import GeoJson, Marker, Icon
import branca.colormap as cm

# 1. Kleurdefinities
COLOR_LIGHT_GREEN = "#C9DBD4"
COLOR_LIGHT_GREY_F0 = "#F0F0F0" 
COLOR_LIGHT_GREY = "#E8E8E8"
COLOR_GREY = "#D1D1D1"
COLOR_DARK_GREEN = "#173C2E"
COLOR_GREEN = "#358A6A"
COLOR_WHITE = "#ffffff"
COLOR_TEXT_DARK = "#2d3748"
COLOR_TEXT_MUTED = "#718096"


# Page config
st.set_page_config(page_title="Manifesten op de Kaart", layout="wide", initial_sidebar_state="expanded")

# 2. Custom CSS - MAXIMALE COMPACTHEID, Selectbox Fix & Beter Kadreren

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Global Spacing - EXTREME COMPACTHEID */
    .main > div {{
        padding-top: 0.1rem !important; 
        padding-bottom: 0.1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }}
    
    .element-container, .stBlock {{
        margin-bottom: 0.1rem !important; /* Minimaal */
        padding: 0 !important;
    }}
    
    .row-widget {{
        margin-bottom: 0.1rem !important;
        padding: 0.1rem !important;
    }}

    /* Tekstgrootte - Compacter */
    p, span, div, label, .stMarkdown, .stCheckbox label, .stRadio label {{
        color: {COLOR_TEXT_DARK} !important;
        font-size: 0.8rem !important;
        line-height: 1.3 !important;
    }}
    
    /* H1 Title - Strak en gecentreerd */
    h1 {{
        color: {COLOR_DARK_GREEN} !important;
        font-size: 1.5rem !important; 
        margin-bottom: 0.3rem !important;
        padding: 0.4rem 0.8rem;
        background-color: {COLOR_LIGHT_GREY};
        border-left: 5px solid {COLOR_GREEN};
        border-radius: 4px;
    }}
    
    /* H2 Subheader - Kleinere, duidelijke kaders */
    h2 {{
        color: {COLOR_DARK_GREEN} !important;
        font-size: 1rem !important;
        margin-bottom: 0.2rem !important;
        padding: 0.3rem 0.5rem;
        background-color: {COLOR_LIGHT_GREEN};
        border-radius: 3px;
    }}
    
    /* Tabs - Zeer strak */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
        background-color: {COLOR_LIGHT_GREY_F0};
        padding: 3px;
        border-radius: 4px;
        margin-bottom: 0.3rem !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 28px;
        font-size: 0.8rem !important;
        padding: 0 10px;
    }}
    
    /* Expander - Maximaal compact */
    .streamlit-expanderHeader {{
        font-size: 0.8rem !important;
        padding: 0.3rem !important;
        background-color: {COLOR_LIGHT_GREEN};
        margin-bottom: 0.1rem !important;
    }}
    
    .streamlit-expanderContent {{
        padding: 0.3rem !important;
        border: 1px solid {COLOR_GREY};
        margin-bottom: 0.2rem !important;
    }}

    /* ALERT REPLACEMENT CLASSES (API FIX) */
    .covenant-status {{
        padding: 0.2rem 0.5rem;
        margin-bottom: 0.2rem;
        border-radius: 4px;
        font-weight: 500;
        color: {COLOR_DARK_GREEN};
        font-size: 0.8rem !important;
    }}
    
    .success-bg {{
        background-color: {COLOR_LIGHT_GREEN} !important;
        border-left: 3px solid {COLOR_GREEN};
    }}
    
    .error-bg {{
        background-color: {COLOR_LIGHT_GREY_F0} !important;
        border-left: 3px solid {COLOR_GREY};
    }}

    /* KOLOM KADERS (BETER TONEN) */
    [data-testid="column"] {{
        padding: 0.3rem !important;
        border: 1px solid {COLOR_GREY}; /* Duidelijker kader */
        border-radius: 4px;
        background-color: {COLOR_LIGHT_GREY_F0}; /* Lichtgrijze achtergrond */
        height: fit-content;
    }}
    
    [data-testid="column"]:first-child {{
        margin-right: 0.5rem; /* Ruimte tussen kolommen */
    }}

    /* SELECTBOX FIX (INPUT VELD) */
    [data-baseweb="select"] > div {{
        background-color: {COLOR_WHITE} !important;
        border: 1px solid {COLOR_GREY} !important;
        color: {COLOR_TEXT_DARK} !important;
        padding: 0.3rem 0.5rem !important; /* Compact */
        min-height: 28px;
    }}
    
    /* SELECTBOX FIX (DROPDOWN LIJST) */
    [data-baseweb="menu"] {{
        background-color: {COLOR_LIGHT_GREY_F0} !important;
        border: 1px solid {COLOR_GREY};
    }}
    
    [data-baseweb="menu"] li, [data-baseweb="menu"] li span {{
        color: {COLOR_TEXT_DARK} !important;
        font-size: 0.85rem !important;
    }}
    
    [data-baseweb="menu"] li:hover {{
        background-color: {COLOR_LIGHT_GREEN} !important;
    }}

</style>
""", unsafe_allow_html=True)

# Initialize session state (onveranderd)
if 'selected_government' not in st.session_state:
    st.session_state.selected_government = None
if 'selected_covenants' not in st.session_state:
    st.session_state.selected_covenants = []
if 'covenant_filter_mode' not in st.session_state:
    st.session_state.covenant_filter_mode = "OF"  # OF or EN

# Title - no emoji
st.title("Manifesten op de Kaart")

# 3. Load dummy data (onveranderd)

@st.cache_data
def load_covenant_data():
    """Load covenant and government linkage data"""
    covenants = [
        "Schoon en Emissieloos Bouwen",
        "MVOI ondertekend",
        "MVOI actieplan gereed",
        "SDG-gemeenten",
        "Schone Lucht Akkoord (SLA)",
        "Green Deal Biobased Bouwen",
        "Manifest Het Nieuwe Normaal (HNN)",
        "Nationaal Programma Circulaire Economie (NPCE)",
        "VNG-Programma Klimaatadaptatie"
    ]

    # Dummy data: which governments signed which covenants
    government_covenants = {
        "Amsterdam": ["MVOI ondertekend", "SDG-gemeenten", "SLA"],
        "Rotterdam": ["MVOI ondertekend", "Green Deal Biobased Bouwen", "NPCE"],
        "Utrecht": ["SDG-gemeenten", "SLA", "VNG-Programma Klimaatadaptatie"],
        "Den Haag": ["MVOI ondertekend", "SDG-gemeenten", "HNN"],
        "Eindhoven": ["Schoon en Emissieloos Bouwen", "NPCE"],
        "Groningen": ["SDG-gemeenten", "VNG-Programma Klimaatadaptatie"],
        "Noord-Holland": ["MVOI ondertekend", "SLA"],
        "Zuid-Holland": ["Green Deal Biobased Bouwen", "NPCE"],
        "Waterschap Amstel, Gooi en Vecht": ["SLA", "VNG-Programma Klimaatadaptatie"],
        "Waterschap Hollandse Delta": ["Green Deal Biobased Bouwen"],
    }

    return covenants, government_covenants

@st.cache_data
def load_geo_data():
    """Load geographical boundaries data - using simplified dummy data for demo"""

    # Simplified gemeente data (just a few for demo)
    gemeenten = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Amsterdam", "type": "gemeente"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [4.7, 52.3], [4.7, 52.4], [5.0, 52.4], [5.0, 52.3], [4.7, 52.3]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Rotterdam", "type": "gemeente"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [4.3, 51.85], [4.3, 51.95], [4.6, 51.95], [4.6, 51.85], [4.3, 51.85]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Utrecht", "type": "gemeente"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [5.0, 52.05], [5.0, 52.15], [5.2, 52.15], [5.2, 52.05], [5.0, 52.05]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Den Haag", "type": "gemeente"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [4.2, 52.0], [4.2, 52.1], [4.4, 52.1], [4.4, 52.0], [4.2, 52.0]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Eindhoven", "type": "gemeente"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [5.4, 51.4], [5.4, 51.5], [5.6, 51.5], [5.6, 51.4], [5.4, 51.4]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Groningen", "type": "gemeente"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [6.5, 53.2], [6.5, 53.3], [6.7, 53.3], [6.7, 53.2], [6.5, 53.2]
                    ]]
                }
            }
        ]
    }

    # Simplified provincie data
    provincies = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Noord-Holland", "type": "provincie"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [4.5, 52.2], [4.5, 52.9], [5.2, 52.9], [5.2, 52.2], [4.5, 52.2]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Zuid-Holland", "type": "provincie"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [4.0, 51.7], [4.0, 52.2], [4.8, 52.2], [4.8, 51.7], [4.0, 51.7]
                    ]]
                }
            }
        ]
    }

    # Simplified waterschap data
    waterschappen = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Waterschap Amstel, Gooi en Vecht", "type": "waterschap"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [4.8, 52.2], [4.8, 52.5], [5.3, 52.5], [5.3, 52.2], [4.8, 52.2]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Waterschap Hollandse Delta", "type": "waterschap"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [4.2, 51.7], [4.2, 52.0], [4.7, 52.0], [4.7, 51.7], [4.2, 51.7]
                    ]]
                }
            }
        ]
    }

    return gemeenten, provincies, waterschappen

@st.cache_data
def load_semi_governments():
    """Load semi-government organizations - ministries in North Sea, others at their actual locations"""
    # Ministries - placed in North Sea near Den Haag
    ministeries = [
        {"name": "Min. van Infrastructuur en Waterstaat", "lat": 52.3, "lon": 3.8, "type": "ministerie"},
        {"name": "Min. van Economische Zaken en Klimaat", "lat": 52.4, "lon": 3.7, "type": "ministerie"},
        {"name": "Min. van Binnenlandse Zaken", "lat": 52.2, "lon": 3.9, "type": "ministerie"},
        {"name": "Min. van Volkshuisvesting", "lat": 52.15, "lon": 3.85, "type": "ministerie"},
    ]

    # Semi-overheden - actual headquarter locations
    semi_overheden = [
        {"name": "TenneT", "lat": 51.9851, "lon": 5.8987, "type": "semi-overheid"},  # Arnhem
        {"name": "Gasunie", "lat": 53.2194, "lon": 6.5665, "type": "semi-overheid"},  # Groningen
        {"name": "ProRail", "lat": 52.0907, "lon": 5.1214, "type": "semi-overheid"},  # Utrecht
        {"name": "Schiphol Group", "lat": 52.3105, "lon": 4.7683, "type": "semi-overheid"},  # Schiphol
        {"name": "Havenbedrijf Rotterdam", "lat": 51.9225, "lon": 4.4792, "type": "semi-overheid"},  # Rotterdam
        {"name": "Port of Amsterdam", "lat": 52.4089, "lon": 4.8565, "type": "semi-overheid"},  # Amsterdam
    ]

    return ministeries, semi_overheden

# Load all data
covenants_list, government_covenants = load_covenant_data()
gemeenten_data, provincies_data, waterschappen_data = load_geo_data()
ministeries, semi_overheden = load_semi_governments()

# Create tabs - no emojis
tab1, tab2 = st.tabs(["🗺️ Kaart-weergave", "📄 Manifest-weergave"])

# 4. TAB 1: KAART-WEERGAVE

with tab1:
    # Kolomverhouding aangepast voor een bredere kaart
    col1, col2 = st.columns([2.5, 1.5]) 

    with col1:
        st.subheader("Kaart van Nederland")
        
        # Filters - meer ademruimte
        with st.expander("Kaartlagen", expanded=True):
            fcol1, fcol2, fcol3, fcol4 = st.columns(4)
            with fcol1:
                show_gemeenten = st.checkbox("Gemeenten", value=True)
            with fcol2:
                show_provincies = st.checkbox("Provincies", value=False)
            with fcol3:
                show_waterschappen = st.checkbox("Waterschappen", value=False)
            with fcol4:
                show_ministeries = st.checkbox("Ministeries", value=True)
                show_semi = st.checkbox("Semi-overheden", value=True)
        
        
        # Search box
        st.markdown('<div style="margin-top: -0.2rem;"></div>', unsafe_allow_html=True)
        search_query = st.text_input("🔍 Zoeken", placeholder="Zoek gemeente, provincie...", label_visibility="collapsed")
        st.markdown('<div style="margin-bottom: 0.1rem;"></div>', unsafe_allow_html=True)
        
        # Create map
        m = folium.Map(
            location=[52.2, 5.3],  # Centered on NL
            zoom_start=7,
            tiles="OpenStreetMap"
        )
        
        # Add layers based on filters
        if show_gemeenten:
            for feature in gemeenten_data['features']:
                gov_name = feature['properties']['name']
                
                # Highlight if search matches
                is_search_match = search_query and search_query.lower() in gov_name.lower()
                
                GeoJson(
                    feature,
                    name=gov_name,
                    style_function=lambda x, matched=is_search_match: {
                        'fillColor': COLOR_GREEN if matched else '#3388ff', # Groen bij match, standaard blauw
                        'color': COLOR_DARK_GREEN if matched else '#2c5aa0',
                        'weight': 4 if matched else 2,
                        'fillOpacity': 0.7 if matched else 0.3
                    },
                    highlight_function=lambda x: {'weight': 4, 'fillOpacity': 0.6},
                    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Gemeente:'])
                ).add_to(m)
                
                # Zoom to search result
                if is_search_match and search_query:
                    bounds = feature['geometry']['coordinates'][0]
                    m.fit_bounds([[b[1], b[0]] for b in bounds])
        
        if show_provincies:
            for feature in provincies_data['features']:
                GeoJson(
                    feature,
                    style_function=lambda x: {
                        'fillColor': '#ff7800',
                        'color': '#cc6000',
                        'weight': 3,
                        'fillOpacity': 0.2
                    },
                    highlight_function=lambda x: {'weight': 5, 'fillOpacity': 0.5},
                    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Provincie:'])
                ).add_to(m)
        
        if show_waterschappen:
            for feature in waterschappen_data['features']:
                GeoJson(
                    feature,
                    style_function=lambda x: {
                        'fillColor': '#00bfff',
                        'color': '#0099cc',
                        'weight': 2,
                        'fillOpacity': 0.3,
                        'dashArray': '5, 5'
                    },
                    highlight_function=lambda x: {'weight': 4, 'fillOpacity': 0.6},
                    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Waterschap:'])
                ).add_to(m)
        
        # Add ministeries (in sea)
        if show_ministeries:
            for org in ministeries:
                folium.Marker(
                    location=[org['lat'], org['lon']],
                    popup=org['name'],
                    tooltip=org['name'],
                    icon=folium.Icon(color='blue', icon='university', prefix='fa')
                ).add_to(m)
        
        # Add semi-overheden (at actual locations)
        if show_semi:
            for org in semi_overheden:
                folium.Marker(
                    location=[org['lat'], org['lon']],
                    popup=org['name'],
                    tooltip=org['name'],
                    icon=folium.Icon(color='red', icon='building', prefix='fa')
                ).add_to(m)
        
        
        # Display map - breder gemaakt voor betere oriëntatie
        st_folium(m, width=700, height=600, returned_objects=["last_object_clicked"])
        
        # Handle map clicks
        if map_data and map_data.get('last_object_clicked'):
            clicked = map_data['last_object_clicked']
            st.info(f"Klik gedetecteerd op: {clicked}")

    with col2:
        st.subheader("Details")
        
        # Dropdown to select government
        all_governments = list(government_covenants.keys())
        
        selected = st.selectbox(
            "Selecteer overheid:",
            [""] + all_governments,
            index=0,
            label_visibility="visible"
        )
        
        if selected:
            st.markdown(f"**{selected}**")
            
            if selected in government_covenants:
                signed = government_covenants[selected]
                
                # OPGELOST: st.success en st.error vervangen door custom markdown
                for covenant in covenants_list:
                    if covenant in signed:
                        # Succes: Groen
                        st.markdown(f'<div class="covenant-status success-bg">✅ {covenant}</div>', unsafe_allow_html=True)
                    else:
                        # Geen match: Neutraal/Error
                        st.markdown(f'<div class="covenant-status error-bg">❌ {covenant}</div>', unsafe_allow_html=True)
            else:
                st.info("Geen manifesten gevonden")
        else:
            st.info("👈 Selecteer een overheid om details te zien")

# 5. TAB 2: MANIFEST-WEERGAVE

with tab2:
    # Kolomverhouding aangepast voor een bredere kaart
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Manifesten")
        
        # EN/OF filter mode - meer ademruimte
        filter_mode = st.radio(
            "Filter:",
            options=["OF", "EN"],
            help="OF: minimaal één manifest. EN: alle manifesten.",
            horizontal=True
        )
        st.session_state.covenant_filter_mode = filter_mode
        
        # Manifest checkboxes
        selected_covenants = []
        for covenant in covenants_list:
            if st.checkbox(covenant, key=f"cov_{covenant}"):
                selected_covenants.append(covenant)
        
        if selected_covenants:
            # OPGELOST: st.success vervangen door custom markdown
            st.markdown(f'<div class="covenant-status success-bg">**{len(selected_covenants)}** manifest(en) geselecteerd</div>', unsafe_allow_html=True)
        else:
            st.info("Geen selectie")

    with col2:
        st.subheader("Aangesloten overheden")
        
        if selected_covenants:
            # Find all governments that match the filter
            matching_govs = set()
            
            if filter_mode == "OF":
                # OF logic: at least one covenant matches
                for gov, signed_covenants in government_covenants.items():
                    if any(cov in signed_covenants for cov in selected_covenants):
                        matching_govs.add(gov)
            else:
                # EN logic: all selected covenants must be signed
                for gov, signed_covenants in government_covenants.items():
                    if all(cov in signed_covenants for cov in selected_covenants):
                        matching_govs.add(gov)
            
            # Create map with ALL government layers highlighted - breder
            m2 = folium.Map(
                location=[52.2, 5.3],
                zoom_start=7,
                tiles="OpenStreetMap"
            )
            
            # Add gemeenten with highlighting (Kleurlogica aangepast, Python commentaar gebruikt)
            for feature in gemeenten_data['features']:
                gov_name = feature['properties']['name']
                is_highlighted = gov_name in matching_govs
                
                GeoJson(
                    feature,
                    style_function=lambda x, highlighted=is_highlighted: {
                        'fillColor': COLOR_GREEN if highlighted else '#dddddd', # Groen bij highlight
                        'color': COLOR_DARK_GREEN if highlighted else '#999999',
                        'weight': 3 if highlighted else 1,
                        'fillOpacity': 0.6 if highlighted else 0.2
                    },
                    tooltip=folium.GeoJsonTooltip(
                        fields=['name'], 
                        aliases=['Gemeente:']
                    )
                ).add_to(m2)
            
            # Add provincies with highlighting (Kleurlogica aangepast, Python commentaar gebruikt)
            for feature in provincies_data['features']:
                gov_name = feature['properties']['name']
                is_highlighted = gov_name in matching_govs
                
                GeoJson(
                    feature,
                    style_function=lambda x, highlighted=is_highlighted: {
                        'fillColor': COLOR_GREEN if highlighted else '#eeeeee', # Groen bij highlight
                        'color': COLOR_DARK_GREEN if highlighted else '#aaaaaa',
                        'weight': 4 if highlighted else 2,
                        'fillOpacity': 0.5 if highlighted else 0.15
                    },
                    tooltip=folium.GeoJsonTooltip(
                        fields=['name'], 
                        aliases=['Provincie:']
                    )
                ).add_to(m2)
            
            # Add waterschappen with highlighting (Kleurlogica aangepast, Python commentaar gebruikt)
            for feature in waterschappen_data['features']:
                gov_name = feature['properties']['name']
                is_highlighted = gov_name in matching_govs
                
                GeoJson(
                    feature,
                    style_function=lambda x, highlighted=is_highlighted: {
                        'fillColor': COLOR_GREEN if highlighted else '#f0f0f0', # Groen bij highlight
                        'color': COLOR_DARK_GREEN if highlighted else '#bbbbbb',
                        'weight': 3 if highlighted else 1,
                        'fillOpacity': 0.5 if highlighted else 0.15,
                        'dashArray': '5, 5'
                    },
                    tooltip=folium.GeoJsonTooltip(
                        fields=['name'], 
                        aliases=['Waterschap:']
                    )
                ).add_to(m2)
            
            # Display map - breder
            st_folium(m2, width=800, height=650)
            
            # Show list of matching governments
            if matching_govs:
                st.markdown(f"### Aangesloten overheden ({filter_mode}-filter):")
                for gov in sorted(matching_govs):
                    signed = government_covenants.get(gov, [])
                    matching = [c for c in selected_covenants if c in signed]
                    st.markdown(f"**{gov}** - {', '.join(matching)}")
            else:
                st.warning(f"Geen overheden voldoen aan {filter_mode}-filter met geselecteerde manifesten")
        else:
            st.info("👈 Selecteer een of meerdere manifesten om aangesloten overheden te zien")

# Footer - compact (onveranderd)
st.caption("Demo v0.4 | Manifesten op de Kaart")
