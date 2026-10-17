import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="EcoZ: IBM Z Carbon-Aware Scheduler", layout="wide")

st.title("⚡ EcoZ: Carbon-Aware Workload Scheduler for IBM Z")
st.caption("Optimizing Enterprise Batch Workloads with IBM Workload Manager (WLM) & Grid Telemetry")

# Load Mock Data
@st.cache_data
def load_data():
    jobs = pd.DataFrame({
        "Job_ID": ["JOB_01", "JOB_02", "JOB_03", "JOB_04", "JOB_05"],
        "Job_Name": ["Ledger Reconcile", "Payroll Batch", "Risk Scoring", "Audit Archive", "Model Retrain"],
        "Duration_Hours": [3, 2, 4, 2, 5],
        "Power_kW": [25, 40, 30, 15, 50],
        "Deadline_Hour": [24, 22, 24, 20, 24],
        "Default_Start": [19, 18, 20, 14, 17]
    })
    carbon = pd.DataFrame({
        "Hour": list(range(24)),
        "Carbon_gCO2_kWh": [210,195,180,175,180,200,240,290,310,280,220,180,160,150,165,190,230,320,380,410,430,390,310,250]
    })
    return jobs, carbon

jobs_df, carbon_df = load_data()

# Optimization Logic
def calculate_job_emissions(start_hour, duration, power, carbon_data):
    total_co2 = 0
    for h in range(start_hour, start_hour + duration):
        total_co2 += (power * carbon_data.loc[carbon_data['Hour'] == h, 'Carbon_gCO2_kWh'].values[0])
    return total_co2 / 1000.0  # kg CO2

def optimize_schedule(jobs, carbon):
    optimized_starts = []
    for _, row in jobs.iterrows():
        best_hour = row["Default_Start"]
        min_emissions = float("inf")
        # Can start from Hour 0 up to (Deadline - Duration)
        max_possible_start = int(row["Deadline_Hour"] - row["Duration_Hours"])
        
        for candidate in range(0, max_possible_start + 1):
            em = calculate_job_emissions(candidate, int(row["Duration_Hours"]), row["Power_kW"], carbon)
            if em < min_emissions:
                min_emissions = em
                best_hour = candidate
        optimized_starts.append(best_hour)
    
    jobs["EcoZ_Start"] = optimized_starts
    
    # Calculate totals
    default_co2 = sum([calculate_job_emissions(row["Default_Start"], int(row["Duration_Hours"]), row["Power_kW"], carbon) for _, row in jobs.iterrows()])
    optimized_co2 = sum([calculate_job_emissions(row["EcoZ_Start"], int(row["Duration_Hours"]), row["Power_kW"], carbon) for _, row in jobs.iterrows()])
    
    return jobs, default_co2, optimized_co2

jobs_res, default_total, opt_total = optimize_schedule(jobs_df.copy(), carbon_df)
pct_saved = ((default_total - opt_total) / default_total) * 100

# Top KPI Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Default Carbon Emitted", f"{default_total:.2f} kg CO₂")
col2.metric("EcoZ Carbon Emitted", f"{opt_total:.2f} kg CO₂", delta=f"-{pct_saved:.1f}%")
col3.metric("Total Emissions Avoided", f"{(default_total - opt_total):.2f} kg CO₂")
col4.metric("SLA / Deadline Violations", "0 Violations", delta="100% On-Time")

st.divider()

# Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Regional Grid Carbon Intensity (24h)")
    fig_grid = go.Figure()
    fig_grid.add_trace(go.Scatter(x=carbon_df["Hour"], y=carbon_df["Carbon_gCO2_kWh"], mode='lines+markers', line=dict(color='crimson', width=3)))
    fig_grid.update_layout(xaxis_title="Hour of Day (0-23)", yaxis_title="gCO₂ / kWh", height=350)
    st.plotly_chart(fig_grid, use_container_width=True)

with col_chart2:
    st.subheader("Workload Shift Comparison")
    st.dataframe(jobs_res[["Job_Name", "Duration_Hours", "Deadline_Hour", "Default_Start", "EcoZ_Start"]], use_container_width=True)
    st.caption("Notice how jobs shift from peak evening dirty hours (18:00-21:00) to midday solar windows (11:00-14:00) while still meeting deadlines.")
