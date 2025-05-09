import streamlit as st

st.title("HSP Coating Compatibility Calculator")

st.markdown("""
Enter the Hansen Solubility Parameters (HSP) for the **resin** and the **solvent**.
We'll calculate the Ra value to see if they're compatible.
""")

# Sample database of materials
materials = {
    "Resins": {
        "Epoxy Resin": (17.0, 10.0, 8.0),
        "Acrylic Resin": (16.2, 9.4, 6.8),
        "Polyurethane": (18.1, 5.3, 7.5),
    },
    "Solvents": {
        "Toluene": (18.0, 1.4, 2.0),
        "Ethanol": (15.8, 8.8, 19.4),
        "Acetone": (15.5, 10.4, 7.0),
    }
}

st.subheader("Choose a Resin")
resin_choice = st.selectbox("Resin", list(materials["Resins"].keys()))
resin_dd, resin_dp, resin_dh = materials["Resins"][resin_choice]

st.subheader("Choose a Solvent")
solvent_choice = st.selectbox("Solvent", list(materials["Solvents"].keys()))
solvent_dd, solvent_dp, solvent_dh = materials["Solvents"][solvent_choice]


# Calculate Ra
def calculate_ra(dd1, dp1, dh1, dd2, dp2, dh2):
    return ((4 * (dd1 - dd2)**2) + ((dp1 - dp2)**2) + ((dh1 - dh2)**2))**0.5

if st.button("Calculate Compatibility"):
    ra = calculate_ra(resin_dd, resin_dp, resin_dh, solvent_dd, solvent_dp, solvent_dh)
    st.write(f"**Ra = {ra:.2f}**")

    if ra <= 4:
        st.success("🟢 Highly Compatible")
    elif ra <= 7:
        st.warning("🟡 Borderline Compatibility")
    else:
        st.error("🔴 Incompatible")

import matplotlib.pyplot as plt

# Plot the points in Hansen space (δD vs δP)
fig, ax = plt.subplots()
ax.scatter(resin_dd, resin_dp, color='blue', label='Resin', s=100)
ax.scatter(solvent_dd, solvent_dp, color='green', label='Solvent', s=100)

# Draw Ra as a line between points
ax.plot([resin_dd, solvent_dd], [resin_dp, solvent_dp], 'k--', linewidth=1)

# Axis labels and styling
ax.set_xlabel("δD (Dispersion)")
ax.set_ylabel("δP (Polar)")
ax.set_title("Hansen Space: δD vs δP")
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)




