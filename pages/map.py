import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt
import mpld3

from PIL import Image
from matplotlib.patches import Patch, Circle

edge_color = "#30011E"
background_color = "#fafafa"

sns.set_style({
    "font.family": "serif",
    "figure.facecolor": background_color,
    "axes.facecolor": background_color,
})

counties = gpd.read_file("./assets/cb_2018_us_county_500k/")
counties = counties[~counties.STATEFP.isin(["72", "69", "60", "66", "78"])]
counties = counties.set_index("GEOID")

states = gpd.read_file("./assets/cb_2018_us_state_500k/")
states = states[~states.STATEFP.isin(["72", "69", "60", "66", "78"])]

ax = counties.plot(edgecolor=edge_color + "55", color="None", figsize=(20, 20))
states.plot(ax=ax, edgecolor=edge_color, color="None", linewidth=1)

plt.axis("off")


counties = counties.to_crs("ESRI:102003")
states = states.to_crs("ESRI:102003")

def translate_geometries(df, x, y, scale, rotate):
    df.loc[:, "geometry"] = df.geometry.translate(yoff=y, xoff=x)
    center = df.dissolve().centroid.iloc[0]
    df.loc[:, "geometry"] = df.geometry.scale(xfact=scale, yfact=scale, origin=center)
    df.loc[:, "geometry"] = df.geometry.rotate(rotate, origin=center)
    return df

def adjust_maps(df):
    df_main_land = df[~df.STATEFP.isin(["02", "15"])]  
    df_alaska = df[df.STATEFP == "02"]  
    df_hawaii = df[df.STATEFP == "15"]  

    df_alaska = translate_geometries(df_alaska, 1100000, -5500000, 0.5, 45)  
    df_hawaii = translate_geometries(df_hawaii, 5500000, -2200000, 0.8, 30)  

    return pd.concat([df_main_land, df_alaska, df_hawaii])

counties = adjust_maps(counties)
states = adjust_maps(states)

ax = counties.plot(edgecolor=edge_color + "55", color="None", figsize=(20, 20))
states.plot(ax=ax, edgecolor=edge_color, color="None", linewidth=1)


fig, ax = plt.subplots(figsize=(20, 20))
counties.plot(ax=ax, edgecolor=edge_color + "55", color="None")
states.plot(ax=ax, edgecolor=edge_color, color="None", linewidth=1)

plt.axis("off")
fig.savefig('us_map.png')
plt.show()

