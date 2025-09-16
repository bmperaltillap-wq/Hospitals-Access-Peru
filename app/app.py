
import os
from pathlib import Path
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# ----- Rutas robustas -----
APP_DIR  = Path(__file__).resolve().parent      # .../app
ROOT_DIR = APP_DIR.parent                       # .../Hospitals-Access-Peru
DATA_DIR = ROOT_DIR / "data"                    # .../data

def f(rel_path: str) -> str:
    """
    Convierte 'data/archivo.ext' o 'archivo.ext' a ruta absoluta segura.
    Si viene sin prefijo, lo busca en /data.
    """
    p = Path(rel_path)
    if not p.is_absolute():
        p = (ROOT_DIR / rel_path) if rel_path.startswith("data") else (DATA_DIR / rel_path)
    return str(p.resolve())

# Configuración de página
st.set_page_config(
    page_title="Hospitals Access Peru",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Carga todos los datos necesarios usando rutas robustas."""
    try:
        hospitales = gpd.read_file(f("data/hospitales_procesados.geojson"))
        try:
            distritos = gpd.read_file(f("data/distritos_con_hospitales.geojson"))
        except Exception:
            distritos = None
        try:
            stats_dept = pd.read_csv(f("data/estadisticas_departamentales.csv"))
        except Exception:
            stats_dept = None
        return hospitales, distritos, stats_dept
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None

def main():
    """Función principal del dashboard"""
    st.title("🏥 Hospitals Access Peru")
    st.markdown("**Geospatial Analysis of Public Hospital Access**")

    # Cargar datos
    hospitales, distritos, stats_dept = load_data()
    if hospitales is None:
        st.error("❌ No se pudieron cargar los datos. Verifica archivos en la carpeta /data")
        try:
            st.caption("Contenido de /data detectado:")
            st.code("\\n".join(sorted(p.name for p in Path(f('data')).glob('*'))))
        except Exception:
            pass
        return

    # Tabs según requerimientos
    tab1, tab2, tab3 = st.tabs([
        "🗂️ Data Description", 
        "🗺️ Static Maps & Department Analysis", 
        "🌍 Dynamic Maps"
    ])

    with tab1:
        show_data_description(hospitales)

    with tab2:
        show_static_maps_department_analysis(hospitales, stats_dept)

    with tab3:
        show_dynamic_maps()

def show_data_description(hospitales):
    """Tab 1: Data Description"""
    st.header("📋 Data Description")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎯 Unit of Analysis")
        st.markdown("""
**Operational public hospitals in Peru**

This analysis focuses exclusively on:
- Public hospitals that are currently operational
- Hospitals with valid geographical coordinates (lat/long)
- Establishments classified as hospitals (not health centers)
""")

        st.subheader("📊 Data Sources")
        sources_data = {
            "Dataset": ["MINSA - IPRESS", "Population Centers", "Districts Shapefile"],
            "Source": ["Ministry of Health", "INEI", "Course Repository"],
            "Description": [
                "Operational subset of health establishments",
                "Population centers for proximity analysis", 
                "District boundaries for spatial analysis"
            ],
            "Records": [f"{len(hospitales)} hospitals", "—", "1,873 districts"]
        }
        st.dataframe(pd.DataFrame(sources_data), use_container_width=True, hide_index=True)

        st.subheader("🔧 Filtering Rules")
        st.markdown("""
**Only operational hospitals with valid lat/long:**
1. **Institution filter**: Only public institutions (GOBIERNO REGIONAL, MINSA, ESSALUD)
2. **Status filter**: Only establishments with "EN FUNCIONAMIENTO" condition
3. **Type filter**: Only "HOSPITALES O CLINICAS" classification
4. **Geographic filter**: Valid coordinates within Peru boundaries
5. **Data quality**: Remove records with missing or invalid coordinates
""")

    with col2:
        st.subheader("📈 Key Statistics")
        st.metric("Total Hospitals Analyzed", f"{len(hospitales)}")
        st.metric("Departments Covered", f"{hospitales['Departamento'].nunique()}")
        st.metric("Geographic Coverage", "National")

        st.subheader("🏛️ By Institution")
        inst_counts = hospitales['Institución'].value_counts()
        for inst, count in inst_counts.items():
            percentage = (count / len(hospitales)) * 100
            st.write(f"• {inst}: {count} ({percentage:.1f}%)")

        fig_pie = px.pie(
            values=inst_counts.values,
            names=inst_counts.index,
            title="Institution Distribution"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

def show_static_maps_department_analysis(hospitales, stats_dept):
    """Tab 2: Static Maps & Department Analysis"""
    st.header("🗺️ Static Maps & Department Analysis")
    st.subheader("Static Maps Created with GeoPandas")

    # Mapas estáticos embebidos (usando rutas robustas)
    map_files = [
        ("Hospital Distribution",          f("data/mapa_distribucion_general.png")),
        ("Districts with Zero Hospitals",  f("data/mapa_distritos_sin_hospitales.png")),
        ("Hospital Concentration",         f("data/mapa_concentracion_distritos.png")), 
        ("Top 10 Districts",               f("data/mapa_top10_distritos.png")),
    ]

    for i in range(0, len(map_files), 2):
        cols = st.columns(2)
        for j, (title, file_path) in enumerate(map_files[i:i+2]):
            with cols[j]:
                st.write(f"**{title}**")
                if os.path.exists(file_path):
                    st.image(file_path, use_container_width=True)
                else:
                    st.error(f"Static map not found:\n{file_path}")
                    try:
                        st.caption("Contenido de /data:")
                        st.code("\\n".join(sorted(p.name for p in Path(f('data')).glob('*'))))
                    except Exception:
                        pass
                    st.info("Run Notebook 2 to generate static maps")

    st.subheader("📊 Department Analysis")
    dept_counts = hospitales['Departamento'].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Department Summary Table**")
        dept_summary = pd.DataFrame({
            'Department': dept_counts.index,
            'Hospitals': dept_counts.values,
            'Percentage': (dept_counts.values / dept_counts.sum() * 100).round(1)
        })
        st.dataframe(dept_summary, use_container_width=True, hide_index=True)

    with col2:
        st.write("**Bar Chart - Top Departments**")
        top_10_dept = dept_counts.head(10)
        fig_bar = px.bar(
            x=top_10_dept.values,
            y=top_10_dept.index,
            orientation='h',
            title="Top 10 Departments by Hospital Count",
            labels={'x': 'Number of Hospitals', 'y': 'Department'}
        )
        fig_bar.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

def show_dynamic_maps():
    """Tab 3: Dynamic Maps"""
    st.header("🌍 Dynamic Maps")
    st.subheader("🗺️ Interactive Map Selection")

    map_option = st.selectbox(
        "Select a dynamic map to visualize:",
        ["National Choropleth + Markers", "Lima Proximity Analysis", "Loreto Proximity Analysis"]
    )

    # Mapear opciones a archivos (rutas robustas)
    map_files = {
        "National Choropleth + Markers": f("data/mapa_nacional_hospitales.html"),
        "Lima Proximity Analysis":       f("data/mapa_lima_proximidad.html"),
        "Loreto Proximity Analysis":     f("data/mapa_loreto_proximidad.html"),
    }

    map_descriptions = {
        "National Choropleth + Markers": """
**National Folium choropleth + markers:**
- Choropleth map showing hospital density by district
- Interactive marker cluster with all hospital points
- Popup information for each hospital
""",
        "Lima Proximity Analysis": """
**Folium proximity map for Lima:**
- Urban context with high hospital density
- 10 km buffer analysis around selected population center
- Hospitals inside the radius
""",
        "Loreto Proximity Analysis": """
**Folium proximity map for Loreto:**
- Amazonian context with geographic dispersion
- 10 km buffer analysis around selected population center
- Hospitals inside the radius
"""
    }

    st.markdown(map_descriptions[map_option])
    map_file = map_files[map_option]

    if os.path.exists(map_file):
        with open(map_file, 'r', encoding='utf-8') as fhtml:
            html = fhtml.read()
        st.components.v1.html(html, height=600)
    else:
        st.error(f"Dynamic map not found:\n{map_file}")
        try:
            st.caption("Contenido de /data:")
            st.code("\\n".join(sorted(p.name for p in Path(f('data')).glob('*'))))
        except Exception:
            pass
        st.info("Run Notebook 4 to generate interactive maps")

if __name__ == "__main__":
    main()
