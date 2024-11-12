import pandas as pd
import numpy as np
import json

import pydeck as pdk
import streamlit as st

st.set_page_config(layout = 'wide')

st.markdown("<h1 style=color:teal>Pydeck trials</h1>", unsafe_allow_html = True)

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
    picking_radius=10,
    auto_highlight=True,
    pickable=True,
)

layers = [scatterplot, line_layer]

r = pdk.Deck(layers=layers, initial_view_state=INITIAL_VIEW_STATE)

st.components.v1.html(r, height = 500)