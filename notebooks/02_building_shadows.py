# %%
import osmnx as ox
# %%
import pandas as pd
# %%
WEST = 77.88
SOUTH = 21.91
EAST = 77.92
NORTH = 21.93
CITY_NAME = "Amla, Madhya Pradesh"
box=(NORTH,SOUTH,EAST,WEST)
print(f'Set for {box}')
try:
    building=ox.features_from_bbox(bbox=box,tags={"building":True})
    if "height" not in building.columns:
        building["height"]=10.0
    else:
        building["height"]=pd.to_numeric(building["height"], errors='coerce').fillna(10.0)
    print(f" Successfully downloaded {len(building)} building.")
except Exception as e:
    print(f"Error: {e}")

# %%
