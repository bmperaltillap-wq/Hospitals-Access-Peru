# 🏥 Hospitals Access Peru - Geospatial Analysis

Bianca Peraltilla - 2025-2

**Geospatial Analysis of Public Hospital Access in Peru**

A comprehensive analysis of public hospital accessibility across Peru using geospatial data science techniques, interactive visualizations, and a Streamlit dashboard.

## 📋 Project Overview

This project analyzes the distribution and accessibility of public hospitals across Peru using the official MINSA-IPRESS dataset. The analysis includes static maps, proximity analysis for specific regions, and interactive visualizations to understand healthcare accessibility patterns.

## 🎯 Data Processing and Filtering

### Hospital Filtering Criteria

The analysis focuses on **operational public hospitals** with the following filtering rules:

1. **Institution Filter**: Only public institutions
   - `GOBIERNO REGIONAL` (Regional Government)
   - `MINSA` (Ministry of Health)
   - `ESSALUD` (Social Health Insurance)

2. **Classification Filter**: Only hospital establishments
   - `HOSPITALES O CLINICAS DE ATENCION GENERAL` (General hospitals)
   - `HOSPITALES O CLINICAS DE ATENCION ESPECIALIZADA` (Specialized hospitals)

3. **Status Filter**: Only operational establishments
   - `Condición == 'EN FUNCIONAMIENTO'` (Currently functioning)

4. **Geographic Filter**: Valid coordinates within Peru boundaries
   - Latitude: -18.5° to 0°
   - Longitude: -81.5° to -68°
   - Non-null and non-zero coordinates

5. **Data Quality**: Remove records with missing critical information

### CRS Conversions and Coordinate Processing

**Important Note**: The original MINSA dataset has **coordinate labels swapped**:
- Column `ESTE` contains **latitude values** (should be NORTE)
- Column `NORTE` contains **longitude values** (should be ESTE)

**Processing Steps**:
```python
# Coordinate correction applied in notebook 01
df['latitud'] = df['ESTE']    # ESTE contains latitude
df['longitud'] = df['NORTE']  # NORTE contains longitude

# Create geometry with corrected coordinates
geometry = [Point(lon, lat) for lon, lat in zip(df['longitud'], df['latitud'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
```

**CRS Information**:
- **Source CRS**: EPSG:4326 (WGS84 Geographic)
- **Target CRS**: EPSG:4326 (maintained throughout analysis)
- **Reason**: All analysis performed in geographic coordinates for compatibility with web mapping

### Final Dataset

After filtering: **232 operational public hospitals** from an initial 20,819 health establishments.

**Distribution**:
- General hospitals: 180 (77.6%)
- Specialized hospitals: 52 (22.4%)
- Geographic coverage: 25 departments

## 🛠️ Installation and Setup

### Prerequisites

- Python 3.8+
- Conda or pip package manager
- Git

### Quick Start

```bash
# Clone repository
git clone https://github.com/bmperaltillap-wq/Hospitals-Access-Peru.git
cd Hospitals-Access-Peru

# Install dependencies
make install
# or manually: pip install -r requirements.txt

# Run all analysis
make all

# Launch dashboard
make dashboard
```

### Manual Setup

```bash
# Create virtual environment
conda create -n hospitals python=3.11
conda activate hospitals

# Install packages
pip install streamlit pandas geopandas plotly folium matplotlib seaborn

# Run notebooks in order
jupyter notebook notebooks/01_data_processing.ipynb
# ... continue with 02, 03, 04, 05

# Launch Streamlit dashboard
streamlit run app/app.py
```

## 📊 Analysis Components

### 1. Data Description (`01_data_processing.ipynb`)
- Load and explore MINSA-IPRESS dataset (20,819 establishments)
- Apply filtering criteria for public hospitals
- Process and validate geographic coordinates
- Export clean dataset for analysis

### 2. Static Maps (`02_static_maps.ipynb`) 
- Generate choropleth maps showing hospital distribution
- Create maps highlighting districts with zero hospitals
- Produce departmental analysis charts
- Export PNG maps for dashboard

### 3. Proximity Analysis (`03_proximity_analysis.ipynb`)
- Lima region: Urban context with high hospital density
- Loreto region: Amazonian context with geographic challenges
- 10km buffer analysis around hospitals
- Population center accessibility assessment

### 4. Interactive Maps (`04_interactive_maps.ipynb`)
- National hospital distribution with marker clusters
- Regional proximity maps with population centers
- Interactive choropleth with hospital density
- Export HTML maps for web embedding

### 5. Dashboard Development (`05_streamlit_app.ipynb`)
- Streamlit application development
- Three-tab interface: Data Description, Static Maps, Dynamic Maps
- Statistical analysis and visualization
- Deployment-ready code

## 🌐 Dashboard Features

The Streamlit dashboard provides:

### Tab 1: Data Description
- Unit of analysis explanation
- Data sources and filtering methodology
- Statistical distributions and charts
- Geographic coverage metrics

### Tab 2: Static Maps & Department Analysis
- Hospital distribution maps created with GeoPandas
- Districts with zero hospitals visualization
- Departmental summary statistics
- Bar charts of top departments

### Tab 3: Dynamic Maps
- Interactive Folium maps
- National choropleth with marker clusters
- Lima and Loreto proximity analysis
- Selectable map visualization

## 📈 Key Findings

- **Geographic concentration**: Lima has the highest number of hospitals (37)
- **Coverage gaps**: Multiple districts lack hospital access
- **Institutional distribution**: Regional governments operate 62% of public hospitals
- **Accessibility challenges**: Significant travel distances in Loreto region
- **Urban vs. rural**: Clear disparity in hospital density

## 🔗 Links

- **Repository**: https://github.com/bmperaltillap-wq/Hospitals-Access-Peru
- **Dashboard**: https://hospitals-access-peru.streamlit.app/ 

## 📄 Data Sources

1. **MINSA-IPRESS**: Ministry of Health health establishments registry
2. **INEI Population Centers**: National Institute of Statistics population data
3. **Districts Shapefile**: Administrative boundaries from course repository

## 🤝 Contributing

This is an academic project for geospatial analysis coursework. The methodology and code structure can be adapted for similar healthcare accessibility analyses.

## 📝 License

Academic project - data sources retain their original licenses.
