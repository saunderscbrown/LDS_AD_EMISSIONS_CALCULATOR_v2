import streamlit as st
from PIL import Image

# Load and display your logo
logo_path = "Wide_Ink_Palm_Dot (4).png"  # Ensure this file is in the same directory
logo = Image.open(logo_path)

st.set_page_config(page_title="Ad Campaign Emissions Calculator", layout="centered")

# Display logo and title
st.image(logo, width=300)
st.title("Ad Campaign Emissions Calculator")

# --- Calculator function ---
def calculate_ad_emissions(impressions, completed_views, duration, platform, carbon_intensity=0.384):
    base_view_emission_30s = 0.22
    view_emission_factor = base_view_emission_30s * (duration / 30)
    impression_emission_factor = 1.74

    platform_grid_factor = {
        'youtube': 0.36,
        'meta': 0.0,
        'default': 1.0
    }
    mix = platform_grid_factor.get(platform.lower(), 1.0)

    view_emissions_g = completed_views * view_emission_factor * mix
    non_viewed_impressions = impressions - completed_views
    impression_emissions_g = non_viewed_impressions * impression_emission_factor * mix

    total_emissions_kg = (view_emissions_g + impression_emissions_g) / 1000
    electricity_kwh = total_emissions_kg / carbon_intensity

    return round(total_emissions_kg, 4), round(electricity_kwh, 2)

# --- UI Form ---
with st.form("emissions_form"):
    impressions = st.number_input("Total impressions", min_value=0, value=1000000, step=1000)
    views = st.number_input("Completed views", min_value=0, value=800000, step=1000)
    duration = st.number_input("Ad duration (in seconds)", min_value=1, max_value=60, value=6)
    platform = st.selectbox("Platform", ["YouTube", "Meta (Facebook/Instagram)", "Other/Unknown"])
    carbon_intensity = st.number_input(
        "Carbon intensity (kg CO₂e per kWh)",
        min_value=0.0,
        value=0.384,
        step=0.00001,
        format="%.5f"
    )

    submitted = st.form_submit_button("Calculate")

    if submitted:
        platform_key = platform.lower().split()[0]
        emissions, kwh = calculate_ad_emissions(impressions, views, duration, platform_key, carbon_intensity)

        st.subheader("Results")
        st.write(f"**Total Emissions:** {emissions:.4f} kg CO₂e")
        st.write(f"**Electricity Equivalent:** {kwh} kWh")
