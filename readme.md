# Canopix - Urban Heat Island Tree Canopy Optimizer

A geospatial ML system that analyzes Landsat 9 thermal imagery and building shadow patterns to identify optimal locations for urban tree planting to reduce heat island effects.

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

## Overview

Canopix combines satellite thermal data with building shadow analysis to score potential tree planting sites by cooling efficiency. The system processes Google Earth Engine imagery and street network data to generate actionable recommendations for urban planners.

## Project Structure

```text
notebooks/
  01_fetch_thermal.py       # Landsat 9 thermal imagery acquisition via Earth Engine
  02_building_shadows.py    # Shadow analysis from building footprints
results/
  week1_heatmap.html        # Interactive heatmap visualization
```

## Tech Stack

- **Satellite Data**: Google Earth Engine, Landsat 9
- **Geospatial**: GeoPandas, OSMnx, pvlib
- **Analysis**: Python, NumPy, Pandas
- **Visualization**: Folium (interactive heatmaps)

## Getting Started

```bash
git clone https://github.com/Jatinprajapati7869/Canopix.git
cd Canopix
pip install -r requirements.txt
```

## Current Status

This project is in active development. The thermal data acquisition pipeline is complete. Building shadow analysis and site scoring are in progress.

## Documentation

See [tree_canopy_optimizer_guide.md](tree_canopy_optimizer_guide.md) for detailed methodology.

## License

MIT License. See [LICENSE](LICENSE) for details.