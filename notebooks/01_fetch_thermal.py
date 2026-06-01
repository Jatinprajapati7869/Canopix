# %% [markdown]
# # Week 1: Fetch Thermal Satellite Data
# 
# **Goal:** Get a heatmap of surface temperatures for one neighborhood.
# 
# By the end of this notebook, you'll have a colorful map showing where
# the ground is hottest. That's your first deliverable. Let's go.

# %% Step 1: Install everything (run this ONCE, then comment it out)
# Uncomment the line below and run it if you haven't installed yet:

# !pip install earthengine-api geemap geopandas osmnx pybdshadow pvlib rasterio numpy folium pandas matplotlib

# %% Step 2: Import and authenticate with Google Earth Engine
import ee


# First time only: this opens a browser window to log in.
# After that, it remembers you.
ee.Authenticate()

# Replace 'your-project-id' with your Google Cloud project ID.
# Don't have one? Go to https://console.cloud.google.com/ and create one (free).
# Then enable the Earth Engine API for that project.
ee.Initialize(project='canopix')  # <-- CHANGE THIS

print("✅ Connected to Google Earth Engine!")

# %% Step 3: Pick your study area
# 
# Go to https://bboxfinder.com/ and draw a rectangle around a neighborhood.
# Copy the 4 numbers (west, south, east, north) and paste them below.
#
# Example below: Central Delhi (Connaught Place area)
# Change this to YOUR city / neighborhood.

WEST = 77.88
SOUTH = 21.91
EAST = 77.92
NORTH = 21.93
CITY_NAME = "Amla, Madhya Pradesh"  # just for labels

bbox = ee.Geometry.Rectangle([WEST, SOUTH, EAST, NORTH])
print(f"✅ Study area set: {CITY_NAME} ({WEST}, {SOUTH}) to ({EAST}, {NORTH})")

# %% Step 4: Fetch Landsat 9 surface temperature
#
# We're grabbing summer data (April-June for India, June-August for US)
# and taking the median to reduce cloud noise.

# Adjust these months for YOUR region's hottest season
START_DATE = '2024-04-01'
END_DATE = '2024-06-30'

def apply_scale_factors(image):
    """Convert Landsat Level-2 raw values to actual temperatures (Celsius)."""
    thermal = image.select('ST_B10').multiply(0.00341802).add(149.0).subtract(273.15)
    return thermal.rename('LST_Celsius')

# Load Landsat 9, filter, and compute median surface temperature
landsat = (ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")
           .filterBounds(bbox)
           .filterDate(START_DATE, END_DATE)
           .filter(ee.Filter.lt('CLOUD_COVER', 20))  # only clear images
           .map(apply_scale_factors)
           .median()
           .clip(bbox))

print(f"✅ Landsat 9 data loaded for {START_DATE} to {END_DATE}")

# %% Step 5: Visualize the heatmap!
import geemap
import os
import webbrowser

Map = geemap.Map()
Map.centerObject(bbox, 15)

# Add the temperature layer
vis_params = {
    'min': 25,
    'max': 55,
    'palette': ['#313695', '#4575b4', '#74add1', '#abd9e9', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
}
Map.addLayer(landsat, vis_params, f'Surface Temperature °C — {CITY_NAME}')

# Add the study area boundary
Map.addLayer(bbox, {'color': 'white'}, 'Study Area')

Map.addLayerControl()

# Save to HTML and open in browser (avoids VS Code widget bugs)
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'week1_heatmap.html')
Map.to_html(output_path)
print(f"✅ Map saved to: {output_path}")
print("Opening in browser...")
webbrowser.open(output_path)

# %% Step 6: Print some stats
#
# Let's see the actual temperature range in our area.

stats = landsat.reduceRegion(
    reducer=ee.Reducer.minMax().combine(ee.Reducer.mean(), sharedInputs=True),
    geometry=bbox,
    scale=30,  # Landsat resolution = 30m per pixel
    maxPixels=1e9
)

stats_dict = stats.getInfo()
print(f"\n🌡️  Temperature Stats for {CITY_NAME}:")
print(f"   Min:  {stats_dict.get('LST_Celsius_min', 'N/A'):.1f} °C")
print(f"   Max:  {stats_dict.get('LST_Celsius_max', 'N/A'):.1f} °C")
print(f"   Mean: {stats_dict.get('LST_Celsius_mean', 'N/A'):.1f} °C")

# %% [markdown]
# ## ✅ Week 1 Done!
# 
# You should see:
# - A colorful heatmap showing hot spots (red) and cool spots (blue)
# - Temperature stats printed above
# - Hot spots = parking lots, asphalt roads, rooftops
# - Cool spots = parks, water bodies, tree-covered areas
# 
# **Screenshot this map.** It's your first demo image.
# 
# **Next step:** Week 2 — we'll add buildings and calculate their shadows.
# Open `02_building_shadows.py` when you're ready.
