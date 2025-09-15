# Hospitals-Access-Peru
Análisis geoespacial del **acceso a hospitales públicos operativos** en Perú usando **Python, GeoPandas, Folium y Streamlit**.  
Trabajo para *Homework_2* (Data Science).

---

## 🎯 Objetivo
- Contar hospitales por **distrito** y **departamento**.
- Identificar **distritos con 0 hospitales**.
- Analizar **proximidad (10 km)** a hospitales en **Lima** y **Loreto**.
- Publicar **mapas estáticos**, **mapas interactivos** y un **dashboard** en Streamlit.

---

## 🧭 Datasets (fuentes)
- **MINSA – IPRESS**: establecimientos de salud (filtrar **hospitales operativos** con lat/long válida).
- **INEI – Centros Poblados**.
- **Shapefile distrital de Perú** (INEI/GeoPerú).
> Nota: Mantener CRS **EPSG:4326** (WGS84). Para buffers métricos de 10 km se puede proyectar a **EPSG:32718** y luego volver a 4326.

---

## ⚙️ Ejecución
```bash
pip install -r requirements.txt
streamlit run app/app.py
