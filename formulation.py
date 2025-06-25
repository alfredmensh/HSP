import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

# --- Set up page configuration ---
st.set_page_config(page_title="FormChemie", layout="centered")

# --- Custom Orbitron Font and Glassy UI Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Orbitron', sans-serif;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        color: #0D1B2A;
    }

    .block-container {
        padding: 2rem 2rem 2rem 2rem;
        background-color: rgba(255,255,255,0.85);
        border-radius: 20px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.1);
    }

    h1, h2, h3 {
        color: #1A73E8;
    }

    </style>
""", unsafe_allow_html=True)

# --- Logo ---
logo = Image.open("formchem_logo.png")
st.image(logo, width=120)

# --- Sidebar Navigation ---
st.sidebar.title("🔬 FormChemie")
page = st.sidebar.radio("Navigate", ["🏠 Home", "🧪 Formulation Tool", "➕ Custom Solvent"])

# --- Sample Database ---
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

# --- Page: Home ---
if page == "🏠 Home":
    st.title("Welcome to FormChemie")
    st.markdown("""
    **FormChemie** is a modern web tool for formulators in the coating and resin industries.  
    We help chemists and engineers evaluate the **Hansen Solubility Parameters (HSP)**  
    and determine **solvent-resin compatibility** through visual maps and compatibility scores.

    🔍 _Check compatibility in seconds_  
    🎨 _Use advanced Hansen space visualizations_  
    ✏️ _Customize your own solvents or resins_  
    """)
    st.markdown("---")
    st.info("This is a student project created to demonstrate computational chemistry applications.")

# --- Page: Formulation Tool ---
elif page == "🧪 Formulation Tool":
    st.title("HSP Compatibility Calculator")
    resin_choice = st.selectbox("Choose a Resin", list(materials["Resins"].keys()))
    solvent_choice = st.selectbox("Choose a Solvent", list(materials["Solvents"].keys()))

    resin_dd, resin_dp, resin_dh = materials["Resins"][resin_choice]
    solvent_dd, solvent_dp, solvent_dh = materials["Solvents"][solvent_choice]

    def calculate_ra(dd1, dp1, dh1, dd2, dp2, dh2):
        return ((4*(dd1 - dd2)**2) + ((dp1 - dp2)**2) + ((dh1 - dh2)**2))**0.5

    if st.button("Calculate Compatibility"):
        ra = calculate_ra(resin_dd, resin_dp, resin_dh, solvent_dd, solvent_dp, solvent_dh)
        radius = st.slider("Adjust Compatibility Radius (Ra)", 2.0, 15.0, 7.0, step=0.1)

        st.write(f"**Ra = {ra:.2f}**")
        if ra <= radius:
            st.success(f"🟢 Compatible")
        elif ra <= radius + 2:
            st.warning(f"🟡 Borderline")
        else:
            st.error(f"🔴 Incompatible")

        # --- Visualize Hansen Space ---
        fig, ax = plt.subplots()
        ax.scatter(resin_dd, resin_dp, color='blue', label='Resin', s=120, marker='*')
        ax.scatter(solvent_dd, solvent_dp, color='green', label='Solvent', s=100)
        ax.plot([resin_dd, solvent_dd], [resin_dp, solvent_dp], 'k--')
        circle = plt.Circle((resin_dd, resin_dp), radius, color='blue', fill=False, linestyle='--')
        ax.add_patch(circle)

        ax.set_xlabel("δD")
        ax.set_ylabel("δP")
        ax.set_title("Hansen Space Visualization")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # --- Compatibility Table ---
        st.subheader("🧾 Solvent Compatibility Table")
        solvent_data = []
        for name, (s_dd, s_dp, s_dh) in materials["Solvents"].items():
            ra_val = calculate_ra(resin_dd, resin_dp, resin_dh, s_dd, s_dp, s_dh)
            match = "✓" if ra_val <= radius else "✗"
            solvent_data.append({
                "Solvent": name, "δD": s_dd, "δP": s_dp, "δH": s_dh,
                "Ra": round(ra_val, 2), "Match": match
            })
        df = pd.DataFrame(solvent_data)
        st.dataframe(df)

# --- Page: Custom Solvent ---
elif page == "➕ Custom Solvent":
    st.title("Add a Custom Solvent")
    name = st.text_input("Solvent Name")
    dd = st.number_input("δD", step=0.1, format="%.1f")
    dp = st.number_input("δP", step=0.1, format="%.1f")
    dh = st.number_input("δH", step=0.1, format="%.1f")

    if st.button("Add Solvent"):
        if name.strip() == "":
            st.warning("Please provide a solvent name.")
        else:
            materials["Solvents"][name] = (dd, dp, dh)
            st.success(f"Solvent '{name}' added.")
