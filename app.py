import streamlit as st
from smart_home_system import SmartHomeSystem

system = SmartHomeSystem()

st.title("🏠 Smart Home Dashboard")

# =========================
# Inputs
# =========================

hour = st.slider("Hour", 0, 23, 12)
day = st.slider("Day", 1, 7, 3)
ldr = st.slider("Light (LDR)", 0, 1000, 300)

pir_living = st.selectbox("PIR Living", [0, 1])
pir_bed = st.selectbox("PIR Bedroom", [0, 1])
pir_kitchen = st.selectbox("PIR Kitchen", [0, 1])
pir_bath = st.selectbox("PIR Bathroom", [0, 1])

temp_living = st.slider("Temp Living", 0, 50, 25)
temp_bed = st.slider("Temp Bedroom", 0, 50, 25)

gas_kitchen = st.slider("Gas Kitchen", 0, 500, 100)
gas_bath = st.slider("Gas Bathroom", 0, 500, 100)

flame = st.selectbox("Flame", [0, 1])

soil = st.slider("Soil Moisture", 0, 100, 50)
water = st.slider("Water Level", 0, 100, 70)

# =========================
# Prediction
# =========================

if st.button("Predict"):

    data = [
        hour,
        day,
        ldr,
        pir_living,
        pir_bed,
        pir_kitchen,
        pir_bath,
        temp_living,
        temp_bed,
        gas_kitchen,
        gas_bath,
        flame,
        soil,
        water
    ]

    result = system.predict(data)

    st.subheader("🏠 Smart Home Decisions")

    # Energy
    st.metric(
        "🔋 Energy Consumption",
        f"{result['Energy_kWh']:.2f} kWh"
    )

    st.divider()

    # Fire
    if result["Fire_Risk"] == 1:
        st.error("🚨 Fire Alert!")

    else:
        if flame == 1 and pir_kitchen == 1:
            st.success("🍳 Cooking Activity (Safe)")
        else:
            st.success("✅ No Fire Risk")

    # Irrigation
    if result["Irrigation"] == 1:
        st.warning("🌱 Irrigation Needed")
    else:
        st.success("🌱 Soil Moisture is Good")

    # Pool
    if result["Pool_Refill"] == 1:
        st.warning("🏊 Pool Refill Needed")
    else:
        st.success("🏊 Pool Water Level Normal")

    st.divider()

    st.write("Raw Model Output:")
    st.json(result)