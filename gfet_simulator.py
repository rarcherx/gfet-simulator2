
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Liquid-Gated GFET Simulator")

# Sidebar inputs
st.sidebar.header("Simulation Parameters")

Vg_min = st.sidebar.slider("Gate Voltage Min (V)", -1.0, 0.0, -0.5)
Vg_max = st.sidebar.slider("Gate Voltage Max (V)", 0.0, 1.0, 0.5)
Vg_points = st.sidebar.slider("Number of Voltage Points", 10, 200, 100)

K_conc = st.sidebar.slider("Potassium Concentration [K⁺] (mM)", 0.1, 100.0, 10.0)
liquid_type = st.sidebar.selectbox("Liquid Type", ["Water (DI)", "PBS", "Saline"])
ionophore_conc = st.sidebar.slider("Ionophore Membrane Concentration (mol/L)", 0.0, 0.1, 0.01)

L = st.sidebar.number_input("Channel Length (μm)", 1.0, 100.0, 10.0)
W = st.sidebar.number_input("Channel Width (μm)", 1.0, 100.0, 10.0)
mobility = st.sidebar.number_input("Graphene Mobility (cm²/Vs)", 100.0, 10000.0, 2000.0)
temperature = st.sidebar.slider("Temperature (K)", 273, 373, 298)

# Constants
q = 1.6e-19  # Elementary charge (C)
k_B = 1.38e-23  # Boltzmann constant (J/K)
eps_0 = 8.85e-12  # Vacuum permittivity (F/m)

# Liquid dielectric properties
liquid_eps = {
    "Water (DI)": 78.5,
    "PBS": 70.0,
    "Saline": 65.0
}
eps_r = liquid_eps[liquid_type]

# Gate capacitance estimation
C_edl = eps_0 * eps_r / (1e-9)  # EDL thickness ~1nm
C_ionophore = eps_0 * 3.0 / (5e-9) * ionophore_conc * 1e3  # scaled by concentration
C_total = 1 / (1/C_edl + 1/C_ionophore)

# Gate voltage sweep
Vg = np.linspace(Vg_min, Vg_max, Vg_points)

# Drain current model (simplified)
W_m = W * 1e-6
L_m = L * 1e-6
mu = mobility * 1e-4  # cm²/Vs to m²/Vs
Id = mu * C_total * W_m / L_m * Vg**2

# Transconductance
gm = np.gradient(Id, Vg)

# Threshold voltage estimate
Vth = Vg[np.argmax(gm)]

# Display results
st.subheader("Drain Current vs Gate Voltage")
fig1, ax1 = plt.subplots()
ax1.plot(Vg, Id, label="I_d")
ax1.set_xlabel("Gate Voltage (V)")
ax1.set_ylabel("Drain Current (A)")
ax1.grid(True)
st.pyplot(fig1)

st.subheader("Transconductance vs Gate Voltage")
fig2, ax2 = plt.subplots()
ax2.plot(Vg, gm, label="g_m", color="orange")
ax2.set_xlabel("Gate Voltage (V)")
ax2.set_ylabel("Transconductance (S)")
ax2.grid(True)
st.pyplot(fig2)

st.subheader("Summary Metrics")
st.write(f"Estimated Threshold Voltage: {Vth:.3f} V")
st.write(f"Gate Capacitance: {C_total:.2e} F/m²")
st.write(f"Max Drain Current: {np.max(Id):.2e} A")
