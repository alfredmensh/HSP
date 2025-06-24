import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

logo = Image.open("formchem_logo.png")
st.image(logo, width=120)


st.title("HSP Compatibility Calculator")
st.markdown("Bereken de Ra-waarde om compatibiliteit tussen resin en solvent te beoordelen.")

# --- Sample database ---
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

# --- Functie voor Ra ---
def calculate_ra(dd1, dp1, dh1, dd2, dp2, dh2):
    return ((4 * (dd1 - dd2)**2) + ((dp1 - dp2)**2) + ((dh1 - dh2)**2))**0.5

# --- User inputs ---
resin_choice = st.selectbox("🔹 Kies een Resin", list(materials["Resins"].keys()))
resin_dd, resin_dp, resin_dh = materials["Resins"][resin_choice]

solvent_choice = st.selectbox("🔹 Kies een Solvent", list(materials["Solvents"].keys()))
solvent_dd, solvent_dp, solvent_dh = materials["Solvents"][solvent_choice]

# --- Compatibility calculation ---
if st.button("▶️ Calculate Compatibility"):
    ra = calculate_ra(resin_dd, resin_dp, resin_dh, solvent_dd, solvent_dp, solvent_dh)
    st.write(f"**Ra = {ra:.2f}**")

    # Compatibility threshold
    radius = st.slider("Stel compatibiliteitsgrens (Ra)", 2.0, 15.0, 7.0, step=0.1)

    if ra <= radius:
        st.success(f"🟢 Compatible (Ra = {ra:.2f} ≤ {radius})")
    elif ra <= radius + 2:
        st.warning(f"🟡 Borderline (Ra = {ra:.2f})")
    else:
        st.error(f"🔴 Incompatible (Ra = {ra:.2f} > {radius + 2})")

    # --- Visualisatie plot ---
    fig, ax = plt.subplots()
    ax.scatter(resin_dd, resin_dp, color='blue', marker='*', s=150, label='Resin')

    for name, (s_dd, s_dp, s_dh) in materials["Solvents"].items():
        s_ra = calculate_ra(resin_dd, resin_dp, resin_dh, s_dd, s_dp, s_dh)
        if s_ra <= radius:
            color = 'green'
        elif s_ra <= radius + 2:
            color = 'orange'
        else:
            color = 'red'
        ax.scatter(s_dd, s_dp, color=color, s=80)
        ax.text(s_dd + 0.1, s_dp + 0.1, name, fontsize=8)

    circle = plt.Circle((resin_dd, resin_dp), radius, color='blue', fill=False, linestyle='--', linewidth=1.5)
    ax.add_patch(circle)
    ax.set_xlabel("δD")
    ax.set_ylabel("δP")
    ax.set_title("Hansen Space Compatibility")
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')
    st.pyplot(fig)

    # --- Compatibiliteitstabel ---
    st.subheader("🧾 Solvent Compatibility Table")
    solvent_data = []

    for name, (s_dd, s_dp, s_dh) in materials["Solvents"].items():
        s_ra = calculate_ra(resin_dd, resin_dp, resin_dh, s_dd, s_dp, s_dh)
        if s_ra <= radius:
            status = "🟢 Compatible"
        elif s_ra <= radius + 2:
            status = "🟡 Borderline"
        else:
            status = "🔴 Incompatible"
        solvent_data.append({
            "Solvent": name,
            "δD": s_dd,
            "δP": s_dp,
            "δH": s_dh,
            "Ra": round(s_ra, 2),
            "Match": status
        })

    df = pd.DataFrame(solvent_data)
    df = df.sort_values("Ra")
    st.dataframe(df)

# --- Nieuw solvent toevoegen ---
st.subheader("➕ Add a Custom Solvent")
new_name = st.text_input("Naam")
new_dd = st.number_input("δD", step=0.1, format="%.1f")
new_dp = st.number_input("δP", step=0.1, format="%.1f")
new_dh = st.number_input("δH", step=0.1, format="%.1f")

if st.button("Add Solvent"):
    if new_name.strip() == "":
        st.warning("Please enter a solvent name.")
    else:
        # Voeg toe aan solvent dictionary
        materials["Solvents"][new_name] = (new_dd, new_dp, new_dh)
        st.success(f"Custom solvent '{new_name}' added!")

        # 🧠 Bereken direct compatibiliteit met geselecteerde resin
        if resin_dd is not None and resin_dp is not None and resin_dh is not None:
            ra = calculate_ra(resin_dd, resin_dp, resin_dh, new_dd, new_dp, new_dh)

            if ra <= radius:
                st.success(f"🟢 '{new_name}' is Compatible (Ra = {ra:.2f} ≤ {radius})")
            elif ra <= radius + 2:
                st.warning(f"🟡 '{new_name}' is Borderline (Ra = {ra:.2f})")
            else:
                st.error(f"🔴 '{new_name}' is Incompatible (Ra = {ra:.2f} > {radius + 2})")
