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
col1, col2, col3 = st.columns(3)
with col1:
    lat = st.number_input("Latitude")
with col2:
    lon = st.number_input("Longitude")
with col3:
    if st.button("Update"):
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


st.map(st.session_state.data, color="color")
st.dataframe(st.session_state.data, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    if "__streamlitmagic__" not in locals():
        import streamlit.web.bootstrap

        streamlit.web.bootstrap.run(__file__, False, [], {})
