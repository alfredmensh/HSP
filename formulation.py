import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="FormChem", layout="wide")

# --- CUSTOM CSS FOR TESLA STYLE ---
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Helvetica', sans-serif;
            background-color: white;
            color: #111;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        h1, h2, h3 {
            font-weight: 600;
        }
        .css-18e3th9 {
            padding-top: 2rem;
        }
        .stButton>button {
            background-color: black;
            color: white;
            border-radius: 0px;
            font-weight: 500;
        }
        .stSlider > div {
            color: #111;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("🔬 FormChem")
page = st.sidebar.radio("Navigate to:", ["Home", "Compatibility Tool", "Customization"])

# --- LOGO ---
logo = Image.open("formchem_logo.png")
st.sidebar.image(logo, width=120)

# --- MATERIAL DATABASE ---
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

def calculate_ra(dd1, dp1, dh1, dd2, dp2, dh2):
    return ((4 * (dd1 - dd2)**2) + ((dp1 - dp2)**2) + ((dh1 - dh2)**2))**0.5

# --- HOME PAGE ---
if page == "Home":
    st.markdown("### 🌿 Welcome to")
    st.markdown("# **FormChem**")
    st.image("formchem_logo.png", width=150)
    st.markdown("""
    FormChem is a **digital formulation tool** powered by Hansen Solubility Parameters (HSP).
    
    🚀 **Features:**
    - Predict resin-solvent compatibility
    - Visualize interaction in HSP space
    - Customize your own solvent systems
    
    """)
    st.markdown("---")

# --- COMPATIBILITY TOOL PAGE ---
elif page == "Compatibility Tool":
    st.markdown("### 🧪 Resin–Solvent Compatibility")
    st.markdown("#### Select a resin and solvent to calculate compatibility (Ra) and visualize the result.")

    resin_choice = st.selectbox("Choose Resin", list(materials["Resins"].keys()))
    resin_dd, resin_dp, resin_dh = materials["Resins"][resin_choice]

    solvent_choice = st.selectbox("Choose Solvent", list(materials["Solvents"].keys()))
    solvent_dd, solvent_dp, solvent_dh = materials["Solvents"][solvent_choice]

    if st.button("Calculate Compatibility"):
        ra = calculate_ra(resin_dd, resin_dp, resin_dh, solvent_dd, solvent_dp, solvent_dh)
        radius = st.slider("Set Compatibility Radius", 2.0, 15.0, 7.0, step=0.1)

        st.markdown(f"**Ra = {ra:.2f}**")

        if ra <= radius:
            st.success(f"🟢 Compatible (Ra = {ra:.2f})")
        elif ra <= radius + 2:
            st.warning(f"🟡 Borderline (Ra = {ra:.2f})")
        else:
            st.error(f"🔴 Incompatible (Ra = {ra:.2f})")

        # Plot
        fig, ax = plt.subplots()
        ax.scatter(resin_dd, resin_dp, color='blue', s=150, marker='*', label='Resin')
        ax.scatter(solvent_dd, solvent_dp, color='green', s=100, label='Solvent')
        circle = plt.Circle((resin_dd, resin_dp), radius, color='blue', fill=False, linestyle='--')
        ax.add_patch(circle)
        ax.set_xlabel("δD (Dispersion)")
        ax.set_ylabel("δP (Polar)")
        ax.set_title("Hansen Space")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# --- CUSTOMIZATION PAGE ---
elif page == "Customization":
    st.markdown("### ➕ Add Your Own Solvent")
    st.markdown("Define solvent parameters to test compatibility against known resins.")

    resin_choice = st.selectbox("Resin for Comparison", list(materials["Resins"].keys()), key="custom_resin")
    resin_dd, resin_dp, resin_dh = materials["Resins"][resin_choice]

    radius = st.slider("Compatibility Radius", 2.0, 15.0, 7.0, step=0.1)

    new_name = st.text_input("Solvent Name")
    new_dd = st.number_input("δD", step=0.1, format="%.1f")
    new_dp = st.number_input("δP", step=0.1, format="%.1f")
    new_dh = st.number_input("δH", step=0.1, format="%.1f")

    if st.button("Add Solvent"):
        if new_name.strip() == "":
            st.warning("Please enter a valid name.")
        else:
            materials["Solvents"][new_name] = (new_dd, new_dp, new_dh)
            st.success(f"Added solvent: {new_name}")

    # Build table
    solvent_data = []
    for name, (s_dd, s_dp, s_dh) in materials["Solvents"].items():
        ra = calculate_ra(resin_dd, resin_dp, resin_dh, s_dd, s_dp, s_dh)
        if ra <= radius:
            match = "🟢 Compatible"
        elif ra <= radius + 2:
            match = "🟡 Borderline"
        else:
            match = "🔴 Incompatible"
        solvent_data.append({
            "Solvent": name,
            "δD": s_dd,
            "δP": s_dp,
            "δH": s_dh,
            "Ra": round(ra, 2),
            "Match": match
        })

    df = pd.DataFrame(solvent_data).sort_values("Ra")
    st.markdown("#### Solvent Compatibility Table")
    st.dataframe(df)
