import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json
from folium import GeoJson, Marker, Icon
import branca.colormap as cm

# Page config
st.set_page_config(page_title="Manifesten op de Kaart", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_government' not in st.session_state:
    st.session_state.selected_government = None
if 'selected_covenants' not in st.session_state:
    st.session_state.selected_covenants = []

# Title
st.title("🗺️ Manifesten op de Kaart")
st.markdown("---")

# Load dummy data
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
    # In reality this would come from CSV/database
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
    """Load semi-government organizations (points on map)"""
    # These would be placed in "legend area" in North Sea
    semi_govs = [
        {"name": "Ministerie van IenW", "lat": 53.5, "lon": 3.5},
        {"name": "Ministerie van EZK", "lat": 53.7, "lon": 3.5},
        {"name": "Ministerie van BZK", "lat": 53.9, "lon": 3.5},
        {"name": "TenneT", "lat": 53.5, "lon": 4.0},
        {"name": "Gasunie", "lat": 53.7, "lon": 4.0},
        {"name": "ProRail", "lat": 53.9, "lon": 4.0},
    ]
    return semi_govs

# Load all data
covenants_list, government_covenants = load_covenant_data()
gemeenten_data, provincies_data, waterschappen_data = load_geo_data()
semi_govs = load_semi_governments()

# Create tabs
tab1, tab2 = st.tabs(["🗺️ Kaart View", "📋 Convenant View"])

# TAB 1: MAP VIEW
with tab1:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Kaart van Nederland")
        
        # Filters
        with st.expander("⚙️ Kaartlagen", expanded=True):
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            with filter_col1:
                show_gemeenten = st.checkbox("Gemeenten", value=True)
                show_provincies = st.checkbox("Provincies", value=False)
            with filter_col2:
                show_waterschappen = st.checkbox("Waterschappen", value=False)
                show_semi = st.checkbox("Semi-overheden", value=True)
            with filter_col3:
                search_query = st.text_input("🔍 Zoeken", placeholder="Zoek gemeente, provincie...")
        
        # Create map
        m = folium.Map(
            location=[52.3, 5.3],
            zoom_start=7,
            tiles="OpenStreetMap"
        )
        
        # Add layers based on filters
        if show_gemeenten:
            gemeente_layer = GeoJson(
                gemeenten_data,
                name="Gemeenten",
                style_function=lambda x: {
                    'fillColor': '#3388ff',
                    'color': '#2c5aa0',
                    'weight': 2,
                    'fillOpacity': 0.3
                },
                highlight_function=lambda x: {'weight': 4, 'fillOpacity': 0.6},
                tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Gemeente:'])
            )
            gemeente_layer.add_to(m)
        
        if show_provincies:
            provincie_layer = GeoJson(
                provincies_data,
                name="Provincies",
                style_function=lambda x: {
                    'fillColor': '#ff7800',
                    'color': '#cc6000',
                    'weight': 3,
                    'fillOpacity': 0.2
                },
                highlight_function=lambda x: {'weight': 5, 'fillOpacity': 0.5},
                tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Provincie:'])
            )
            provincie_layer.add_to(m)
        
        if show_waterschappen:
            waterschap_layer = GeoJson(
                waterschappen_data,
                name="Waterschappen",
                style_function=lambda x: {
                    'fillColor': '#00bfff',
                    'color': '#0099cc',
                    'weight': 2,
                    'fillOpacity': 0.3,
                    'dashArray': '5, 5'
                },
                highlight_function=lambda x: {'weight': 4, 'fillOpacity': 0.6},
                tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Waterschap:'])
            )
            waterschap_layer.add_to(m)
        
        if show_semi:
            for org in semi_govs:
                folium.Marker(
                    location=[org['lat'], org['lon']],
                    popup=org['name'],
                    tooltip=org['name'],
                    icon=folium.Icon(color='red', icon='building', prefix='fa')
                ).add_to(m)
        
        # Display map
        map_data = st_folium(m, width=900, height=600)
        
        # Handle click on map
        if map_data and map_data.get('last_object_clicked'):
            clicked = map_data['last_object_clicked']
            st.info(f"Je klikte op coördinaten: {clicked}")
    
    with col2:
        st.subheader("Details")
        
        # For demo, show details of Amsterdam if clicked
        selected = st.selectbox(
            "Selecteer overheid (demo):",
            [""] + list(government_covenants.keys())
        )
        
        if selected:
            st.markdown(f"### {selected}")
            st.markdown("---")
            
            st.markdown("#### 📜 Convenanten & Manifesten")
            
            if selected in government_covenants:
                signed = government_covenants[selected]
                
                for covenant in covenants_list:
                    if covenant in signed:
                        st.success(f"✓ {covenant}")
                    else:
                        st.error(f"✗ {covenant}")
            else:
                st.info("Geen convenanten gevonden")

# TAB 2: COVENANT VIEW
with tab2:
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Convenanten")
        st.markdown("Selecteer één of meerdere convenanten om te zien welke overheden deze hebben ondertekend.")
        
        selected_covenants = []
        for covenant in covenants_list:
            if st.checkbox(covenant, key=f"cov_{covenant}"):
                selected_covenants.append(covenant)
        
        if selected_covenants:
            st.success(f"{len(selected_covenants)} convenant(en) geselecteerd")
    
    with col2:
        st.subheader("Aangesloten overheden")
        
        if selected_covenants:
            # Find all governments that signed selected covenants
            matching_govs = set()
            for gov, signed_covenants in government_covenants.items():
                if any(cov in signed_covenants for cov in selected_covenants):
                    matching_govs.add(gov)
            
            # Create map with highlighted governments
            m2 = folium.Map(
                location=[52.3, 5.3],
                zoom_start=7,
                tiles="OpenStreetMap"
            )
            
            # Add gemeenten with conditional highlighting
            for feature in gemeenten_data['features']:
                gov_name = feature['properties']['name']
                is_highlighted = gov_name in matching_govs
                
                GeoJson(
                    feature,
                    style_function=lambda x, highlighted=is_highlighted: {
                        'fillColor': '#ff4444' if highlighted else '#cccccc',
                        'color': '#cc0000' if highlighted else '#999999',
                        'weight': 3 if highlighted else 1,
                        'fillOpacity': 0.6 if highlighted else 0.2
                    },
                    tooltip=folium.GeoJsonTooltip(
                        fields=['name'], 
                        aliases=['Gemeente:']
                    )
                ).add_to(m2)
            
            # Display map
            st_folium(m2, width=1000, height=600)
            
            # Show list of matching governments
            st.markdown("### Aangesloten overheden:")
            for gov in sorted(matching_govs):
                signed = government_covenants.get(gov, [])
                matching = [c for c in selected_covenants if c in signed]
                st.markdown(f"**{gov}** - {', '.join(matching)}")
        else:
            st.info("👈 Selecteer een of meerdere convenanten om aangesloten overheden te zien")

# Footer
st.markdown("---")
st.caption("Demo versie - Manifesten op de Kaart | Fase 0")
