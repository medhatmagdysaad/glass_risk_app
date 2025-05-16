import streamlit as st

# Title
st.title("Architectural Glass Risk Assessment Tool")

# Sidebar – User Inputs
st.sidebar.header("Select Glass Parameters")

glass_type = st.sidebar.selectbox("Glass Type / Configuration", [
    "Annealed (monolithic)",
    "Heat-strengthened (monolithic)",
    "Tempered (monolithic, unsoaked)",
    "Tempered (heat-soaked)",
    "Laminated Annealed",
    "Laminated Heat-Strengthened",
    "Laminated Tempered"
])

location = st.sidebar.selectbox("Location Type", [
    "Overhead", "Facade", "Balcony", "Low Level"
])

critical_use = st.sidebar.checkbox("Critical Use Area (risk to people)", value=True)

heat_exposure = st.sidebar.selectbox("Thermal Exposure", [
    "Partial shading + coated/tinted", "Even exposure", "Interior use"
])

# Backend rules: simplified example
risk_rules = {
    "Spontaneous Breakage": {
        "Tempered (monolithic, unsoaked)": {
            "risk": "Very High 🚩",
            "justification": "Unsoaked tempered glass carries risk of NiS inclusion breakage, especially in critical use.",
            "mitigation": "Use heat-soaked or laminated tempered glass in critical locations."
        },
        "Tempered (heat-soaked)": {
            "risk": "Low ✅",
            "justification": "Heat soak testing eliminates most panes at risk of NiS fracture.",
            "mitigation": "Verify heat soak certification from manufacturer."
        },
        "Laminated Tempered": {
            "risk": "High 🚩" if critical_use else "Medium ⚠️",
            "justification": "If tempered ply breaks, laminate may contain it. Still, NiS is a risk.",
            "mitigation": "Use double-laminated tempered or heat-soaked laminated panels for overhead/critical use."
        },
        "default": {
            "risk": "Low ✅",
            "justification": "Annealed and HS glass are not at risk of NiS-related spontaneous breakage.",
            "mitigation": "No special measures required for spontaneous breakage."
        }
    },
    "Post-Breakage Containment": {
        "Annealed (monolithic)": {
            "risk": "Very High 🚩",
            "justification": "Breaks into large shards with no retention.",
            "mitigation": "Use laminated or fully framed safety glazing."
        },
        "Tempered (monolithic, unsoaked)": {
            "risk": "Very High 🚩" if location == "Overhead" else "High 🚩",
            "justification": "Fractures into small granules that fall out of opening.",
            "mitigation": "Use laminated tempered glass for overhead or critical areas."
        },
        "Laminated Annealed": {
            "risk": "Low ✅",
            "justification": "Fragments retained by interlayer.",
            "mitigation": "Verify proper edge support and interlayer thickness."
        },
        "Laminated Tempered": {
            "risk": "Medium ⚠️",
            "justification": "Heavy cracked panels may sag if minimally supported.",
            "mitigation": "Use stiffer interlayer or retention systems for large overhead panes."
        },
        "default": {
            "risk": "Low ✅",
            "justification": "Adequate containment if laminated and well supported.",
            "mitigation": "Ensure glass is fully captured in frame."
        }
    },
    "Fragmentation Hazard": {
        "Annealed (monolithic)": {
            "risk": "Very High 🚩",
            "justification": "Breaks into large, sharp shards; dangerous on failure.",
            "mitigation": "Use tempered or laminated safety glazing in human impact zones."
        },
        "Tempered (monolithic, unsoaked)": {
            "risk": "Very High 🚩" if location == "Overhead" else "Medium ⚠️",
            "justification": "Breaks into many small granules that may fall uncontrolled.",
            "mitigation": "Use laminated tempered or protective screening below."
        },
        "Laminated Tempered": {
            "risk": "High 🚩" if location == "Overhead" else "Medium ⚠️",
            "justification": "May shed glass dust or small fragments if overhead; generally retained.",
            "mitigation": "Consider hybrid laminated-tempered-glass with stiff interlayer."
        },
        "default": {
            "risk": "Low ✅",
            "justification": "Glass type breaks safely or retains fragments.",
            "mitigation": "No special treatment needed beyond standard lamination."
        }
    }
}

# Display Risk Table
st.header("📊 Risk Assessment Summary")

for category, logic in risk_rules.items():
    config = logic.get(glass_type, logic["default"])
    st.subheader(f"🧱 {category}")
    st.markdown(f"**Risk Level:** {config['risk']}")
    with st.expander("Why this rating?"):
        st.markdown(f"**Justification:** {config['justification']}")
        st.markdown(f"**Mitigation Advice:** {config['mitigation']}")
