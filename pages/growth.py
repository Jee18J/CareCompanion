import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Child Growth Chart", layout="wide")

# Dummy percentile curves (simplified WHO-like format)
def get_weight_for_age_curves(gender):
    months = np.arange(0, 25)  # 0 to 24 months
    base = 3.2 if gender == "Male" else 3.0
    return {
        "months": months,
        "3rd": base + 0.3 * months,
        "15th": base + 0.35 * months,
        "50th": base + 0.42 * months,
        "85th": base + 0.49 * months,
        "97th": base + 0.55 * months,
    }

def get_height_for_age_curves(gender):
    months = np.arange(0, 25)
    base = 49.9 if gender == "Male" else 49.1
    return {
        "months": months,
        "3rd": base + 0.7 * months,
        "15th": base + 0.75 * months,
        "50th": base + 0.8 * months,
        "85th": base + 0.85 * months,
        "97th": base + 0.9 * months,
    }

def get_weight_for_height_curves(gender):
    heights = np.arange(45, 100)
    base = 2.5 if gender == "Male" else 2.3
    return {
        "heights": heights,
        "3rd": base + 0.1 * (heights - 45),
        "15th": base + 0.13 * (heights - 45),
        "50th": base + 0.15 * (heights - 45),
        "85th": base + 0.18 * (heights - 45),
        "97th": base + 0.20 * (heights - 45),
    }

# --- UI Section ---
st.title("👶 Child Growth Chart Visualizer")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age (months)", min_value=0, max_value=24, step=1)
with col2:
    weight = st.number_input("Weight (kg)", min_value=2.0, max_value=20.0, step=0.1)
    height = st.number_input("Height (cm)", min_value=45.0, max_value=100.0, step=0.1)

show = st.button("Plot Growth Charts")

if show:
    color = "blue" if gender == "Male" else "deeppink"

    # --- Weight for Age ---
    data = get_weight_for_age_curves(gender)
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    for key in ['3rd', '15th', '50th', '85th', '97th']:
        ax1.plot(data["months"], data[key], label=f"{key} percentile", linestyle='--' if key != "50th" else '-', color='gray' if key != "50th" else 'orange')
    ax1.scatter(age, weight, color=color, label="Your child", zorder=5)
    ax1.set_title("Weight-for-Age")
    ax1.set_xlabel("Age (months)")
    ax1.set_ylabel("Weight (kg)")
    ax1.legend()
    ax1.grid(True)

    # --- Height for Age ---
    data = get_height_for_age_curves(gender)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    for key in ['3rd', '15th', '50th', '85th', '97th']:
        ax2.plot(data["months"], data[key], label=f"{key} percentile", linestyle='--' if key != "50th" else '-', color='gray' if key != "50th" else 'orange')
    ax2.scatter(age, height, color=color, label="Your child", zorder=5)
    ax2.set_title("Height-for-Age")
    ax2.set_xlabel("Age (months)")
    ax2.set_ylabel("Height (cm)")
    ax2.legend()
    ax2.grid(True)

    # --- Weight for Height ---
    data = get_weight_for_height_curves(gender)
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    for key in ['3rd', '15th', '50th', '85th', '97th']:
        ax3.plot(data["heights"], data[key], label=f"{key} percentile", linestyle='--' if key != "50th" else '-', color='gray' if key != "50th" else 'orange')
    ax3.scatter(height, weight, color=color, label="Your child", zorder=5)
    ax3.set_title("Weight-for-Height")
    ax3.set_xlabel("Height (cm)")
    ax3.set_ylabel("Weight (kg)")
    ax3.legend()
    ax3.grid(True)

    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)
