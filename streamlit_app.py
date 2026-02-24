import streamlit as st

from alps_briefing.services.geocoding import geocode
from alps_briefing.services.weather import fetch_weather
from alps_briefing.services.avalanche_slf import fetch_slf_bulletin
from alps_briefing.services.avalanche_gear_qa import answer_avalanche_gear_question

st.title("Alps Briefing Agent (MVP)")

st.markdown("## Ask the agent")
q = st.chat_input('Ask: "Do I need avalanche gear in Andermatt tomorrow?"')
if q:
    try:
        out = answer_avalanche_gear_question(q)
        st.write(out["answer"])
        with st.expander("Debug"):
            st.json(out)
    except Exception as e:
        st.error(str(e))

st.markdown("---")

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