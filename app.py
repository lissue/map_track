import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, to_hex


def generate_hex_colors(values):
    # Remove NaN values for normalization
    valid_values = np.array([val for val in values if not np.isnan(val)])
    hex_colors = "#000000"
    if len(valid_values) > 0:
        # Create a normalization function
        norm = Normalize(vmin=valid_values.min(), vmax=valid_values.max())
        # Create a colormap
        cmap = plt.get_cmap("inferno")
        # Generate hex colors for each value
        hex_colors = []
        for val in values:
            if np.isnan(val):
                hex_colors.append("#000000")  # Assign black for NaN values
            else:
                color = cmap(norm(val))
                hex_colors.append(to_hex(color))
    return hex_colors


if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    lat_degrees = st.number_input("Lat Degrees", value=38, step=1)
with col2:
    lat_minutes = st.number_input("Lat Minutes", value=24, step=1)
with col3:
    lat_seconds = st.number_input("Lat Seconds", value=39.7, step=0.1)
with col4:
    lon_degrees = st.number_input("Lon Degrees", value=80, step=1)
with col5:
    lon_minutes = st.number_input("Lon Minutes", value=00, step=1)
with col6:
    lon_seconds = st.number_input("Lon Seconds", value=16.8, step=0.1)
with col7:
    if st.button("Update"):
        lat = lat_degrees + lat_minutes / 60 + lat_seconds / 3600
        lon = -(lon_degrees + lon_minutes / 60 + lat_seconds / 3600)
        elapsed_t = np.nan
        t = datetime.now()
        if not st.session_state.data.empty:
            last_t = st.session_state.data.timestamp.values[-1]
            print(last_t)
            elapsed_t = t - pd.to_datetime(last_t)
            elapsed_t = elapsed_t.total_seconds() / 60

        st.session_state.data = pd.concat(
            [
                st.session_state.data,
                pd.DataFrame(
                    {
                        "lat": [lat],
                        "lon": [lon],
                        "timestamp": [t],
                        "elapsed_minutes": [elapsed_t],
                    }
                ),
            ]
        )
        st.session_state.data[
            "cumulative_elapsed_minutes"
        ] = st.session_state.data.elapsed_minutes.cumsum()
        st.session_state.data["color"] = generate_hex_colors(
            st.session_state.data.cumulative_elapsed_minutes.values
        )


st.map(st.session_state.data, color="color", size=1)
st.dataframe(st.session_state.data, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    if "__streamlitmagic__" not in locals():
        import streamlit.web.bootstrap

        streamlit.web.bootstrap.run(__file__, False, [], {})
