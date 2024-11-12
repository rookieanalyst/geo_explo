import pandas as pd
import numpy as np
import json

import pydeck as pdk
import streamlit as st

st.set_page_config(layout = 'wide')

st.markdown("<h1 style=color:teal>Pydeck trials</h1>", unsafe_allow_html = True)

## LineLayer
DATA_URL = {
    "AIRPORTS": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/line/airports.json",
    "FLIGHT_PATHS": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/line/heathrow-flights.json",  # noqa
}

INITIAL_VIEW_STATE = pdk.ViewState(latitude=47.65, longitude=7, zoom=4.5, max_zoom=16, pitch=50, bearing=0)

# RGBA value generated in Javascript by deck.gl's Javascript expression parser
GET_COLOR_JS = [
    "255 * (1 - (start[2] / 10000) * 2)",
    "128 * (start[2] / 10000)",
    "255 * (start[2] / 10000)",
    ]

scatterplot = pdk.Layer(
    "ScatterplotLayer",
    DATA_URL["AIRPORTS"],
    radius_scale=20,
    get_position="coordinates",
    get_fill_color=[255, 140, 0],
    get_radius=60,
    pickable=True,
)

line_layer = pdk.Layer(
    "LineLayer",
    DATA_URL["FLIGHT_PATHS"],
    get_source_position="start",
    get_target_position="end",
    get_color=GET_COLOR_JS,
    get_width=1,
    highlight_color=[255, 255, 0],
    picking_radius=100,
    auto_highlight=True,
    pickable=True,
)

layers = [scatterplot, line_layer]

r_line = pdk.Deck(layers=layers, initial_view_state=INITIAL_VIEW_STATE)

## TripsLayer

TRIPS_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf.trips.json"  # noqa

df = pd.read_json(TRIPS_LAYER_DATA)

df["coordinates"] = df["waypoints"].apply(lambda f: [item["coordinates"] for item in f])
df["timestamps"] = df["waypoints"].apply(lambda f: [item["timestamp"] - 1554772579000 for item in f])

df.drop(["waypoints"], axis=1, inplace=True)

layer = pdk.Layer(
    "TripsLayer",
    df,
    get_path="coordinates",
    get_timestamps="timestamps",
    get_color=[253, 128, 93],
    opacity=0.8,
    width_min_pixels=5,
    rounded=True,
    trail_length=600,
    current_time=500,
)

view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=11, bearing=0, pitch=45)

# Render
r_trips = pdk.Deck(layers=[layer], initial_view_state=view_state)

## PathLayer

DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-lines.json"
df = pd.read_json(DATA_URL)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


df["color"] = df["color"].apply(hex_to_rgb)


view_state = pdk.ViewState(latitude=37.782556, longitude=-122.3484867, zoom=10)

layer = pdk.Layer(
    type="PathLayer",
    data=df,
    pickable=True,
    get_color="color",
    width_scale=20,
    width_min_pixels=2,
    get_path="path",
    get_width=5,
)

r_path = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}"})

# GreatCircleLayer
GREAT_CIRCLE_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/flights.json"  # noqa

df = pd.read_json(GREAT_CIRCLE_LAYER_DATA)

# Use pandas to prepare data for tooltip
df["from_name"] = df["from"].apply(lambda f: f["name"])
df["to_name"] = df["to"].apply(lambda t: t["name"])

# Define a layer to display on a map
layer = pdk.Layer(
    "GreatCircleLayer",
    df,
    pickable=True,
    get_stroke_width=12,
    get_source_position="from.coordinates",
    get_target_position="to.coordinates",
    get_source_color=[64, 255, 0],
    get_target_color=[0, 128, 200],
    auto_highlight=True,
)

# Set the viewport location
view_state = pdk.ViewState(latitude=50, longitude=-40, zoom=1, bearing=0, pitch=0)

# Render
r_circle = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{from_name} to {to_name}"}, map_style = 'dark'
)
r_circle.picking_radius = 10


examples = st.columns(2)

with examples[0]:
    st.markdown("<h3 style=color:teal>LineLayer</h3>", unsafe_allow_html = True)
    st.pydeck_chart(r_line)

    st.markdown("<h3 style=color:teal>TripsLayer</h3>", unsafe_allow_html = True)    
    st.pydeck_chart(r_trips)

with examples[1]:
    st.markdown("<h3 style=color:teal>PathLayer</h3>", unsafe_allow_html = True)     
    st.pydeck_chart(r_path)
    
    st.markdown("<h3 style=color:teal>GreatCircleLayer</h3>", unsafe_allow_html = True)     
    st.pydeck_chart(r_circle)