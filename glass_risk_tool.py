import streamlit as st

st.set_page_config(page_title="Glass Risk Assessment Tool", layout="centered")

st.title("🔍 Glass Risk Assessment Tool")

# --- Input Fields ---
location = st.selectbox("Location of Glass", ["Façade", "Roof", "Balustrade"])
height = st.number_input("Height from Floor (m)", min_value=0.0, step=0.1)
glass_type = st.selectbox("Glass Type", ["Annealed", "Toughened", "Heat Strengthened"])
laminated = st.radio("Laminated Safety Interlayer?", ["Yes", "No"])
framing = st.selectbox("Framing Type", ["Fully Framed"])
access_below = st.radio("Access Below Glass?", ["Yes", "No"])
thermal_exposure = st.radio("Thermal Exposure?", ["Yes", "No"])

# --- Logic ---
risk = "Check Inputs"

if location in ["Roof", "Balustrade"]:
    if glass_type == "Annealed":
        risk = "Very High"
    else:
        risk = "Low"

elif location == "Façade" and framing == "Fully Framed":
    if glass_type == "Annealed":
        if laminated == "No" and thermal_exposure == "No" and height <= 5 and access_below == "No":
            risk = "Medium"
        elif laminated == "No" and thermal_exposure == "No" and height > 5 and access_below == "No":
            risk = "High"
        elif laminated == "No" and thermal_exposure == "No" and height > 5 and access_below == "Yes":
            risk = "Very High"
        elif laminated == "No" and thermal_exposure == "Yes":
            risk = "Very High"
        elif laminated == "Yes" and thermal_exposure == "No":
            risk = "Medium"
        elif laminated == "Yes" and thermal_exposure == "Yes":
            risk = "Very High"

    elif glass_type == "Heat Strengthened":
        if laminated == "No" and thermal_exposure == "No" and height <= 5 and access_below == "No":
            risk = "Low"
        elif laminated == "No" and thermal_exposure == "No" and height > 5 and access_below == "No":
            risk = "High"
        elif laminated == "No" and thermal_exposure == "No" and height > 5 and access_below == "Yes":
            risk = "Very High"
        elif laminated == "No" and thermal_exposure == "Yes":
            risk = "Low"
        elif laminated == "Yes" and thermal_exposure == "Yes" and height > 5 and access_below == "Yes":
            risk = "Low"
        elif laminated == "Yes" and thermal_exposure == "No":
            risk = "Low"

    elif glass_type == "Toughened":
        if laminated == "No" and thermal_exposure == "No" and height <= 5 and access_below == "No":
            risk = "Medium"
        elif laminated == "No" and thermal_exposure == "No" and height > 5 and access_below == "No":
            risk = "High"
        elif laminated == "No" and thermal_exposure == "No" and height > 5 and access_below == "Yes":
            risk = "Very High"
        elif laminated == "No" and thermal_exposure == "Yes":
            risk = "Low"
        elif laminated == "Yes" and thermal_exposure == "Yes" and height > 5 and access_below == "Yes":
            risk = "Low"
        elif laminated == "Yes" and thermal_exposure == "No":
            risk = "Low"

# --- Output ---
st.markdown("### 🛡️ Risk Level:")
st.success(risk)
