# Hospitals Access Peru - Complete Project Pipeline

# Install dependencies
install:
	pip install -r requirements.txt

# Run complete analysis pipeline
all: data static-maps proximity interactive app dashboard

# Process hospital data (Notebook 1)
data:
	jupyter nbconvert --execute notebooks/01_data_processing.ipynb

# Generate static maps (Notebook 2)  
static-maps:
	jupyter nbconvert --execute notebooks/02_static_maps.ipynb

# Run proximity analysis (Notebook 3)
proximity:
	jupyter nbconvert --execute notebooks/03_proximity_analysis.ipynb

# Create interactive maps (Notebook 4)
interactive:
	jupyter nbconvert --execute notebooks/04_interactive_maps.ipynb

# Develop Streamlit app (Notebook 5)
app:
	jupyter nbconvert --execute notebooks/05_streamlit_app.ipynb

# Launch Streamlit dashboard
dashboard:
	streamlit run app/app.py
