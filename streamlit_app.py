import streamlit as st

from alps_briefing.services.geocoding import geocode
from alps_briefing.services.weather import fetch_weather
from alps_briefing.services.avalanche_slf import fetch_slf_bulletin

st.title("Alps Briefing Agent (MVP)")

place = st.text_input("Location", "Zermatt")

if st.button("Generate briefing"):
    try:
        loc = geocode(place)
        st.subheader(loc["name"])
        st.write(f'Coordinates: {loc["lat"]:.4f}, {loc["lon"]:.4f}')

        st.markdown("### Weather (today)")
        st.json(fetch_weather(loc["lat"], loc["lon"]))

        st.markdown("### Avalanche bulletin (SLF)")
        st.json(fetch_slf_bulletin(lang="en"))

        st.caption("Disclaimer: Educational demo. Always rely on the official bulletin for decisions.")
    except Exception as e:
        st.error(str(e))