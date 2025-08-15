
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("Liquid-Gated GFET Simulator")

# Sidebar inputs
st.sidebar.header("Simulation Parameters")
Vg_min = st.sidebar.slider("Gate Voltage Min (V)", -1.0, 0.0, -0.5)
Vg_max = st.sidebar.slider("Gate Voltage Max (V)", 0.0, 1.0, 0.5)
K_conc = st.sidebar.slider("Potassium Concentration [K⁺] (mM)", 0.1, 100.0, 10.0)
liquid_type = st.sidebar.selectbox("Liquid Type", ["Water", "PBS", "Saline"])
ionophore_conc = st.sidebar.slider("Ionophore Membrane Concentration (%)", 0.0, 10.0, 1.0)
L = st.sidebar.number_input("Channel Length (µm)", 1.0, 100.0, 10.0)
W = st.sidebar.number_input("Channel Width (µm)", 1.0, 100.0, 10.0)
mu = st.sidebar.number_input("Graphene Mobility (cm²/Vs)", 100.0, 10000.0, 2000.0)
T = st.sidebar.slider("Temperature (K)", 273, 373, 298)

# Constants
q = 1.6e-19
k_B = 1.38e-23
eps_0 = 8.85e-12
eps_r_dict = {"Water": 80, "PBS": 70, "Saline": 65}
eps_r = eps_r_dict[liquid_type]

# Capacitance model
def edl_capacitance(K_conc, eps_r):
    I = K_conc * 1e3  # mol/m³
    return np.sqrt(2 * eps_r * eps_0 * k_B * T * I)  # simplified model

def ionophore_effect(conc):
    return 1 + 0.1 * conc  # increases sensitivity

C_edl = edl_capacitance(K_conc, eps_r)
C_ion = ionophore_effect(ionophore_conc)
C_total = C_edl * C_ion

# Drain current model
def drain_current(Vg, Cg, mu, W, L):
    return mu * Cg * (W / L) * Vg**2

# Animation
st.subheader("Animated Gate Voltage Sweep")
fig, ax = plt.subplots()
Vg_range = np.linspace(Vg_min, Vg_max, 100)
Id = drain_current(Vg_range, C_total, mu * 1e-4, W * 1e-6, L * 1e-6)
line, = ax.plot([], [], lw=2)
ax.set_xlim(Vg_min, Vg_max)
ax.set_ylim(0, max(Id)*1.1)
ax.set_xlabel("Gate Voltage (V)")
ax.set_ylabel("Drain Current (A)")
ax.set_title("I–V Characteristics")

progress_bar = st.progress(0)
plot_placeholder = st.empty()

for i in range(1, len(Vg_range)+1):
    line.set_data(Vg_range[:i], Id[:i])
    fig.canvas.draw()
    plot_placeholder.pyplot(fig)
    progress_bar.progress(i / len(Vg_range))
    time.sleep(0.01)

# GFET schematic
st.subheader("GFET Schematic")
fig2, ax2 = plt.subplots(figsize=(6, 3))
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 5)
ax2.axis("off")
ax2.text(1, 4.5, "Gate Electrode", fontsize=10)
ax2.arrow(2, 4.2, 0, -1.5, head_width=0.2, head_length=0.2, fc='k', ec='k')
ax2.text(1, 2.5, "Electrolyte", fontsize=10)
ax2.add_patch(plt.Rectangle((3, 2), 4, 1, color='lightblue', alpha=0.5))
ax2.text(4.5, 2.5, "Ionophore Membrane", fontsize=8)
ax2.add_patch(plt.Rectangle((3, 1), 4, 0.5, color='orange', alpha=0.5))
ax2.text(4.5, 1.2, "Graphene Channel", fontsize=8)
ax2.plot([3, 7], [1, 1], color='black', lw=2)
ax2.text(2.8, 0.8, "Source", fontsize=8)
ax2.text(7.1, 0.8, "Drain", fontsize=8)
st.pyplot(fig2)
