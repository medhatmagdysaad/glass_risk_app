import streamlit as st

# Title and introduction
st.title("Glass Risk Assessment Tool")
st.header("Input Configuration")

# User inputs for IGU configuration
outer_type = st.selectbox("Outer glass type:", ["Annealed", "Toughened (Tempered)", "Heat Strengthened"])
inner_type = st.selectbox("Inner glass type:", ["Annealed", "Toughened (Tempered)", "Heat Strengthened", "Laminated"])
any_lam = st.radio("Is any lite laminated?", ("No", "Yes"))
coating = st.radio("Glass coating (e.g. Low-E, tinted)?", ("No", "Yes"))
shading = st.radio("Partial shading present?", ("No", "Yes"))
framing = st.selectbox("Framing support type:", ["Fully Framed", "Point Supported", "Partially Supported"])
height = st.number_input("Glass height from floor (m):", min_value=0.0, value=0.0, step=0.1)
pedestrian = st.radio("Presence of pedestrian access below?", ("No", "Yes"))

# Determine if any toughened (tempered) glass is present (for heat soak testing)
tempered_present = ("Toughened" in outer_type) or ("Toughened" in inner_type) or ("Tempered" in outer_type) or ("Tempered" in inner_type)
if tempered_present:
    heat_soak = st.radio("Heat soak tested (if tempered glass)?", ("Yes", "No"))
else:
    heat_soak = "N/A"  # Not applicable if no tempered glass

# Risk assessment calculations (based on standards and best practices)
# Convert yes/no inputs to booleans for easier logic
laminated_present = (any_lam == "Yes")
coating_present = (coating == "Yes")
shading_present = (shading == "Yes")
ped_below = (pedestrian == "Yes")
heat_soak_done = (heat_soak == "Yes")

# Simplify glass type identification
outer_is_annealed = outer_type.startswith("Annealed")
outer_is_toughened = ("Toughened" in outer_type or "Tempered" in outer_type)
outer_is_heat_strengthened = outer_type.startswith("Heat Strengthened")
inner_is_annealed = inner_type.startswith("Annealed")
inner_is_toughened = ("Toughened" in inner_type or "Tempered" in inner_type)
inner_is_heat_strengthened = inner_type.startswith("Heat Strengthened")
inner_is_laminated = inner_type.startswith("Laminated")

# Determine if outer lite is laminated (based on any_lam flag and inner selection)
outer_is_laminated = laminated_present and not inner_is_laminated

# 1. Thermal Stress Risk
# Annealed glass with coatings and partial shading has high thermal break risk (use heat-strengthened/tempered to mitigate).
if outer_is_annealed:
    if coating_present and shading_present:
        thermal_risk = "High"
        thermal_reason = "Outer lite is annealed with coating and partial shading (high thermal stress risk)."
    elif coating_present or shading_present:
        thermal_risk = "Medium"
        thermal_reason = "Outer lite is annealed with {} (elevated thermal stress risk).".format("coating" if coating_present else "partial shading")
    else:
        thermal_risk = "Low"
        thermal_reason = "Outer lite is annealed with no coatings or shading (thermal stress risk is low)."
elif outer_is_heat_strengthened:
    if coating_present and shading_present:
        thermal_risk = "Medium"
        thermal_reason = "Outer lite is heat-strengthened with coating and shading (moderate thermal stress risk)."
    else:
        thermal_risk = "Low"
        thermal_reason = "Outer lite is heat-strengthened (lower thermal stress risk)."
elif outer_is_toughened:
    thermal_risk = "Low"
    thermal_reason = "Outer lite is fully tempered (toughened), which is very resistant to thermal stress."
else:
    thermal_risk = "Low"
    thermal_reason = "Thermal stress risk is low."

# 2. Wind/Impact Resistance Risk
# Consider structural support (framing) and need for safety glass at accessible locations (per building codes).
if framing == "Fully Framed":
    if outer_is_annealed:
        struct_risk = "Medium"
        struct_reason = "Outer glass is annealed (weaker than tempered for wind loads)."
    elif outer_is_heat_strengthened:
        struct_risk = "Low"
        struct_reason = "Outer glass is heat-strengthened (moderate strength for wind loads)."
    else:  # toughened
        struct_risk = "Low"
        struct_reason = "Outer glass is fully tempered (high strength for wind/impact)."
elif framing == "Partially Supported":
    if outer_is_annealed:
        struct_risk = "High"
        struct_reason = "Annealed glass with partially supported edges has high risk under wind load."
    elif outer_is_heat_strengthened:
        struct_risk = "Medium"
        struct_reason = "Heat-strengthened glass with partial support has moderate risk under wind load."
    else:  # toughened
        struct_risk = "Low"
        struct_reason = "Toughened glass with partial edge support provides adequate strength for wind loads."
elif framing == "Point Supported":
    if outer_is_toughened:
        struct_risk = "Low"
        struct_reason = "Toughened glass is used with point supports (adequate strength)."
    else:
        struct_risk = "High"
        struct_reason = "Point-supported glass is not fully tempered (high risk of failure under load)."
else:
    struct_risk = "Low"
    struct_reason = ""

# Human impact risk for low-level glazing (if bottom of glass < ~1m from floor, safety glass required by standards).
impact_risk = "Low"
impact_reason = ""
if height < 1.0:
    safe_inner = (inner_is_toughened or inner_is_laminated)
    safe_outer = (outer_is_toughened or outer_is_laminated)
    if not safe_inner or not safe_outer:
        impact_risk = "High"
        side = "interior" if not safe_inner else "exterior"
        impact_reason = "Glazing is accessible at low height and the {} lite is not safety glass.".format(side)
    else:
        impact_risk = "Low"
        impact_reason = "Glazing at low level uses safety glass on both sides."

# Combined wind/impact risk is the higher of structural and impact risk
risk_scale = {"Low": 0, "Medium": 1, "High": 2}
combined_level = max(risk_scale.get(struct_risk, 0), risk_scale.get(impact_risk, 0))
if combined_level == 2:
    wind_impact_risk = "High"
elif combined_level == 1:
    wind_impact_risk = "Medium"
else:
    wind_impact_risk = "Low"

# Main reason for wind/impact risk output
if wind_impact_risk == "High":
    if impact_risk == "High":
        wind_impact_reason = "Glazing in a critical location is not safety glass, posing a high impact injury risk."
    else:
        wind_impact_reason = "Glass configuration is inadequate for its support type, giving high breakage risk under wind/impact."
elif wind_impact_risk == "Medium":
    wind_impact_reason = struct_reason if struct_reason and struct_risk == "Medium" else impact_reason
    if not wind_impact_reason:
        wind_impact_reason = "Moderate wind/impact risk."
else:
    wind_impact_reason = "Glass configuration meets strength and safety requirements (low wind/impact risk)."

# 3. Spontaneous Breakage Risk (Nickel Sulfide in tempered glass)
if outer_is_toughened or inner_is_toughened:
    if not heat_soak_done:
        # Not heat-soak tested (EN 14179 recommends heat soaking tempered glass to reduce NiS risk)
        if outer_is_toughened and ped_below:
            spontaneous_risk = "High"
            spontaneous_reason = "Toughened glass is not heat soak tested; risk of spontaneous breakage (NiS) and falling glass."
        else:
            spontaneous_risk = "Medium"
            spontaneous_reason = "Toughened glass is not heat soak tested; some risk of spontaneous breakage exists."
    else:
        spontaneous_risk = "Low"
        spontaneous_reason = "Toughened glass is heat soak tested, minimizing risk of spontaneous breakage."
else:
    spontaneous_risk = "Low"
    spontaneous_reason = "No fully tempered glass present, so spontaneous breakage risk is negligible."

# 4. Fragmentation Hazard
# Falling glass fragment size vs. injury risk (CWCT: use laminated or small-particle tempered glass above public areas).
if ped_below:
    if outer_is_laminated:
        frag_risk = "Low"
        frag_reason = "Outer pane is laminated, so broken glass will adhere to the interlayer (minimal falling fragment hazard)."
    elif outer_is_toughened:
        if height > 13.0:
            frag_risk = "High"
            frag_reason = "Outer pane is tempered glass – although it breaks into small pieces, from this height falling fragments pose significant hazard."
        else:
            frag_risk = "Medium"
            frag_reason = "Outer pane is tempered glass – it breaks into small fragments, reducing injury risk compared to large shards."
    else:
        frag_risk = "High"
        frag_reason = "Outer pane will break into large sharp fragments, posing a high hazard to pedestrians below."
else:
    frag_risk = "Low"
    frag_reason = "No pedestrian access below, so falling fragment hazard is low."

# 5. Post-breakage Containment Risk
# After breakage, will glass remain in opening? (Use laminated glass or full framing to retain broken pieces.)
if laminated_present:
    contain_risk = "Low"
    if inner_is_laminated:
        contain_reason = "Laminated inner pane will retain glass fragments if broken, preventing fallout."
    else:
        contain_reason = "Laminated outer pane will remain intact upon breakage, preventing glass fallout."
else:
    if framing == "Fully Framed":
        if outer_is_toughened:
            contain_risk = "High"
            contain_reason = "No lamination and outer pane is tempered – broken pieces would not be held by the frame."
        else:
            contain_risk = "Medium"
            contain_reason = "No lamination – frame may hold some broken glass, but there is risk of pieces falling."
    else:
        contain_risk = "High"
        if framing == "Point Supported":
            contain_reason = "No lamination and point supports provide virtually no retention; broken glass will fall out."
        else:
            contain_reason = "No lamination and only partial support – high risk of broken glass falling from the opening."

# Overall Risk level (highest among individual risks)
risk_levels = [thermal_risk, wind_impact_risk, spontaneous_risk, frag_risk, contain_risk]
if "High" in risk_levels:
    overall_risk = "High"
elif "Medium" in risk_levels:
    overall_risk = "Medium"
else:
    overall_risk = "Low"

# Display results
st.header("Risk Assessment Results")
# Overall risk with highlighted color
if overall_risk == "High":
    st.error(f"Overall Risk Level: {overall_risk}")
elif overall_risk == "Medium":
    st.warning(f"Overall Risk Level: {overall_risk}")
else:
    st.success(f"Overall Risk Level: {overall_risk}")

# Detailed breakdown for each risk category
def format_risk(category, level, reason):
    color = {"High": "red", "Medium": "orange", "Low": "green"}[level]
    return f"**{category}:** <span style='color:{color};font-weight:bold'>{level}</span> — {reason}"

st.markdown(format_risk("Thermal Stress Risk", thermal_risk, thermal_reason), unsafe_allow_html=True)
st.markdown(format_risk("Wind/Impact Resistance Risk", wind_impact_risk, wind_impact_reason), unsafe_allow_html=True)
st.markdown(format_risk("Spontaneous Breakage Risk", spontaneous_risk, spontaneous_reason), unsafe_allow_html=True)
st.markdown(format_risk("Fragmentation Hazard", frag_risk, frag_reason), unsafe_allow_html=True)
st.markdown(format_risk("Post-breakage Containment Risk", contain_risk, contain_reason), unsafe_allow_html=True)
