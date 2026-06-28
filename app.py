import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# Set page configuration to wide layout for an operational dashboard feel
st.set_page_config(page_title="Call Centre Performance Dashboard", layout="wide")

# -----------------------------------------------------------------------------
# 1. LOAD & PROCESSING CALL CENTRE DATA
# -----------------------------------------------------------------------------
# Departmental overview data (for metrics calculations)
dept_csv = """Metric,Dept A,Dept B,Dept C
Calls,244,186,194
Resolved,203,144,167
Transactional,25,14,22
Returns,12,23,4
Error,4,5,1"""

df_dept = pd.read_csv(StringIO(dept_csv))

# Time Series Data for the main tracking graph
ts_csv = """Date,Total calls
1/6/26,608\n2/6/26,629\n3/6/26,585\n4/6/26,594\n5/6/26,632\n6/6/26,635\n7/6/26,553
8/6/26,550\n9/6/26,609\n10/6/26,638\n11/6/26,597\n12/6/26,583\n13/6/26,621\n14/6/26,554
15/6/26,608\n16/6/26,551\n17/6/26,634\n18/6/26,588\n19/6/26,603\n20/6/26,611\n21/6/26,584
22/6/26,622\n23/6/26,579\n24/6/26,594\n25/6/26,623\n26/6/26,630\n27/6/26,566\n28/6/26,624"""

df_ts = pd.read_csv(StringIO(ts_csv))
df_ts['Date'] = pd.to_datetime(df_ts['Date'], format='%d/%m/%y')

# Core Metric Computations
total_calls_june = df_ts['Total calls'].sum()
avg_daily_calls = round(df_ts['Total calls'].mean(), 1)

# Current Period Metrics (Using the last recorded day: 28/06/2026)
current_day_total = 624
target_baseline = 640
target_performance = "97.50%"
total_resolved_day = 203 + 144 + 167  # 514
resolution_rate_day = round((total_resolved_day / current_day_total) * 100, 1)

# -----------------------------------------------------------------------------
# 2. HEADER
# -----------------------------------------------------------------------------
st.title("Call Centre Operations & Performance Dashboard")
st.caption("Real-time operational volume tracking, service level metrics, and performance vs targets")
st.write("---")

# -----------------------------------------------------------------------------
# 3. TOP OPERATIONAL METRIC CARDS
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Monthly Calls (June)", 
        value=f"{total_calls_june:,}", 
        delta=f"Avg: {avg_daily_calls}/day"
    )

with col2:
    st.metric(
        label="Today's Call Volume", 
        value=f"{current_day_total}", 
        delta=f"{current_day_total - target_baseline} vs Target Baseline ({target_baseline})"
    )

with col3:
    st.metric(
        label="Today's Resolution Rate", 
        value=f"{resolution_rate_day}%", 
        delta=f"{total_resolved_day} Total Solved Cases"
    )

with col4:
    st.metric(
        label="Target Achievement Status", 
        value=target_performance, 
        delta="-2.50% Below Target Threshold",
        delta_color="inverse"
    )

st.write("---")

# -----------------------------------------------------------------------------
# 4. TIME SERIES TRACKING VISUALIZATION
# -----------------------------------------------------------------------------
st.subheader("Daily Incoming Call Trends vs. Target Benchmarks")

fig_ts = go.Figure()

# Add the daily incoming volumes line
fig_ts.add_trace(go.Scatter(
    x=df_ts['Date'], 
    y=df_ts['Total calls'],
    mode='lines+markers',
    name='Daily Total Calls',
    line=dict(color='#0066cc', width=2.5),
    marker=dict(size=6, symbol='circle')
))

# Add static daily benchmark baseline 
fig_ts.add_trace(go.Scatter(
    x=df_ts['Date'],
    y=[target_baseline] * len(df_ts),
    mode='lines',
    name='Daily Operational Target (640)',
    line=dict(color='#e74c3c', width=2, dash='dash')
))

fig_ts.update_layout(
    xaxis=dict(
        tickformat="%b %d",
        showgrid=True,
        gridcolor='#e5e5e5',
        title="Date"
    ),
    yaxis=dict(
        title="Call Volume Counts",
        showgrid=True,
        gridcolor='#e5e5e5',
        range=[500, 660] # Framed perfectly around your data boundaries
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(l=40, r=20, t=10, b=40),
    height=450,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig_ts, use_container_width=True)
