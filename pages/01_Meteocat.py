import streamlit as st

st.set_page_config(
    page_title="Meteocat Sesrovires",
    page_icon=":sun_behind_rain_cloud:"
)

st.title("Previsió Meteo")
st.components.v1.iframe("https://m.meteo.cat/?codi=082080", height=600, scrolling=True)

st.markdown("Previsió extreta de [meteo.cat](https://meteo.cat/)")

st.markdown("- Sant Esteve Sesrovires. [escriptori](https://www.meteo.cat/prediccio/municipal/082080), [mòbil](https://m.meteo.cat/?codi=082080)")
