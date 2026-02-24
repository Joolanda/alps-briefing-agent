
---

# 🌄 **Alps Briefing Agent**  
*A one‑day multi‑domain AI agent for weather, avalanche safety, and mountain planning.*

## 🧭 Overview
The **Alps Briefing Agent** was built as a one‑day assignment for the *AI Project Management* cohort.  
The original brief asked for a simple “Free Weather Advisor” agent that could answer:

> *“Do I need an umbrella in Berlin tomorrow?”*

This project goes far beyond that.  
It delivers a **multi‑domain, production‑ready AI agent** that integrates:

- **Weather forecasting** (Open‑Meteo)  
- **Avalanche danger analysis** (SLF v4 GeoJSON API)  
- **Geocoding** (Open‑Meteo geocoding)  
- **Conversational reasoning**  
- **A clean Streamlit UI**  

All within a single day.

---

## ⭐ Why this project stands out
This project exceeds the requirements of the “Free Weather Advisor” assignment by implementing a multi‑domain agent capable of weather forecasting, avalanche danger analysis, geocoding, and conversational reasoning. Instead of a minimal single‑tool demo, it delivers a cleanly architected, production‑ready agent with real‑world APIs and robust parsing logic.

### Highlights
- **Multi‑domain intelligence**  
  Weather forecasts, avalanche bulletins, and geocoding combined into one coherent agent.

- **Robust natural‑language parsing**  
  Extracts place names and temporal expressions from free‑form questions.

- **Modular architecture**  
  Clear separation between `services/`, `logic/`, and `ui/`.

- **Real‑world API handling**  
  Including SLF’s new v4 GeoJSON avalanche bulletin (complex, multi‑feature structure).

- **User‑friendly interface**  
  Streamlit front‑end for interactive exploration.

---

## 🧩 Architecture

```
alps_briefing_agent/
│
├── services/
│   ├── weather_open_meteo.py      # Weather API integration
│   ├── geocoding.py               # Location → lat/lon
│   └── avalanche_slf.py           # SLF v4 GeoJSON integration
│
├── logic/
│   ├── weather_advice.py          # Umbrella logic
│   └── avalanche_gear.py          # Avalanche gear logic
│
├── ui/
│   └── streamlit_app.py           # Streamlit interface
│
└── README.md
```

---

## 🌦️ Features

### **1. Weather Advisor**
Ask:
> *“Do I need an umbrella in Berlin tomorrow?”*

The agent:
- parses the question  
- extracts location + date  
- calls Open‑Meteo  
- returns a conversational recommendation  

---

### **2. Avalanche Gear Advisor**
Ask:
> *“Do I need avalanche gear in Andermatt tomorrow?”*

The agent:
- parses the question  
- maps Andermatt → SLF region CH‑2223  
- fetches the SLF v4 GeoJSON bulletin  
- finds the correct region across all features  
- extracts danger levels  
- gives a safety‑first recommendation  

---

## ⚠️ Safety Note
This project is an educational demo. Avalanche risk assessment is serious and conditions can change quickly. Always consult the official SLF bulletin and make conservative decisions when traveling in avalanche terrain.

---

### **3. Streamlit UI**
A clean interface to test both advisors interactively.

---

## 🚀 Running the project

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Streamlit
```bash
streamlit run streamlit_app.py
```

---

## 🧪 Example questions

- *“Do I need an umbrella in Munich today.”*  
- *“Do I need avalanche gear in Andermatt tomorrow.”*  
- *“What’s the weather like in Zermatt.”*  

---

## 🛠️ Tech Stack

- **Python 3.11**  
- **Streamlit**  
- **Requests**  
- **Open‑Meteo Weather API**  
- **Open‑Meteo Geocoding API**  
- **SLF Avalanche Bulletin v4 GeoJSON**  

---

## 📌 Notes on SLF v4 Integration
SLF’s new API uses a **FeatureCollection** with multiple features, each containing multiple regions.  
This project includes a robust region‑search function that scans all features to find the correct region ID.

---

## 🏔️ Future Extensions

- Multi‑day avalanche forecasts  
- Map visualizations of SLF polygons  
- Ski touring route suggestions  
- Weather + avalanche combined risk scoring  

---

## 🙌 Credits
Built by **Joolanda** as part of the *AI Project Management Cohort* — a one‑day challenge to design, build, and ship a working AI agent.

---
