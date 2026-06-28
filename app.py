import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# Set page configuration to wide layout
st.set_page_config(page_title="Call Centre Performance Dashboard", layout="wide")

# -----------------------------------------------------------------------------
# 1. LOAD & COMPUTE PERFORMANCE DATA
# -----------------------------------------------------------------------------
# Departmental performance matrix
dept_csv = """Metric,Dept A,Dept B,Dept C
Calls,244,186,194
Resolved,203,144,167
Transactional,25,14,22
Returns,12,23,4
Error,4,5,1"""

df_dept = pd.read_csv(StringIO(dept_csv))

# Time Series Data (June 1st to June 28th)
ts_csv = """Date,Total calls
01/06/2026,636\n02/06/2026,647\n03/06/2026,623\n04/06/2026,625\n05/06/2026,640
06/06/2026,596\n07/06/2026,552\n08/06/2026,604\n09/06/2026,590\n10/06/2026,615
11/06/2026,643\n12/06/2026,552\n13/06/2026,600\n14/06/2026,595\n15/06/2026,584
16/06/2026,571\n17/06/2026,625\n18/06/2026,570\n19/06/2026,586\n20/06/2026,615
21/06/2026,568\n22/06/2026,631\n23/06/2026,643\n24/06/2026,585\n25/06/2026,566
26/06/2026,647\n27/06/2026,594\n28/06/2026,624"""

df_ts = pd.read_csv(StringIO(ts_csv))
df_ts['Date'] = pd.to_datetime(df_ts['Date'], format='%d/%m/%Y')
df_ts['DayNumber'] = df_ts['Date'].dt.day

# Metrics Calculations
total_calls_day = df_dept.loc[df_dept['Metric'] == 'Calls', ['Dept A', 'Dept B', 'Dept C']].sum(axis=1).values[0]
total_resolved_day = df_dept.loc[df_dept['Metric'] == 'Resolved', ['Dept A', 'Dept B', 'Dept C']].sum(axis=1).values[0]
unresolved_issues = total_calls_day - total_resolved_day 

# Pie chart totals for underlying categories
total_transactional = df_dept.loc[df_dept['Metric'] == 'Transactional', ['Dept A', 'Dept B', 'Dept C']].sum(axis=1).values[0]
total_returns = df_dept.loc[df_dept['Metric'] == 'Returns', ['Dept A', 'Dept B', 'Dept C']].sum(axis=1).values[0]
total_errors = df_dept.loc[df_dept['Metric'] == 'Error', ['Dept A', 'Dept B', 'Dept C']].sum(axis=1).values[0]

# Style and Configuration Defaults
target_baseline = 640
bold_dark_font = dict(family="Arial, sans-serif", size=13, color="#111111")
bold_dark_title_font = dict(family="Arial, sans-serif", size=15, color="#111111")

# -----------------------------------------------------------------------------
# 2. HEADER
# -----------------------------------------------------------------------------
st.title("Call Centre Performance Dashboard")
st.caption("Operational layout tracking performance and issue categories | June 2026")
st.write("---")

# -----------------------------------------------------------------------------
# 3. TOP OPERATIONAL METRIC CARDS
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Volume (Current Day)", 
        value=f"{total_calls_day}", 
        delta=f"{total_calls_day - target_baseline} vs Target"
    )

with col2:
    st.metric(
        label="Resolved Issues", 
        value=f"{total_resolved_day}", 
        delta="Active baseline tracking"
    )

with col3:
    st.metric(
        label="Unresolved Issues", 
        value=f"{unresolved_issues}", 
        delta="Requires operational action",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="Target Achievement Status", 
        value="97.50%", 
        delta="-2.50% Below Benchmark Value",
        delta_color="inverse"
    )

st.write("---")

# -----------------------------------------------------------------------------
# 4. SINGLE ROW INTEGRATED LAYOUT: [2 Quarters | 1 Quarter | 1 Quarter]
# -----------------------------------------------------------------------------
layout_col1, layout_col2, layout_col3 = st.columns([2, 1, 1])

# --- QUARTERS 1 & 2: Time Series Chart ---
with layout_col1:
    st.subheader("Daily Incoming Call Trends")
    
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(
        x=df_ts['DayNumber'], y=df_ts['Total calls'],
        mode='lines+markers', name='Daily Total Calls',
        line=dict(color='#0066cc', width=2.5), marker=dict(size=6)
    ))
    fig_ts.add_trace(go.Scatter(
        x=df_ts['DayNumber'], y=[target_baseline] * len(df_ts),
        mode='lines', name=f'Daily Target Threshold ({target_baseline})',
        line=dict(color='#e74c3c', width=2, dash='dash')
    ))
    
    fig_ts.update_layout(
        xaxis=dict(
            title=dict(text="<b>Day of Month (June 2026)</b>", font=bold_dark_title_font),
            tickmode="linear", tick0=1, dtick=2, showgrid=True,
            gridcolor='#e5e5e5', tickfont=bold_dark_font
        ),
        yaxis=dict(
            title=dict(text="<b>Number of Calls</b>", font=bold_dark_title_font),
            showgrid=True, gridcolor='#e5e5e5', range=[530, 665], tickfont=bold_dark_font
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=bold_dark_font),
        margin=dict(l=60, r=20, t=10, b=50), height=380,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_ts, use_container_width=True)

# --- QUARTER 3: Category Breakdown Pie Chart ---
with layout_col2:
    st.subheader("Monthly Category Totals")
    
    pie_labels = ["Transactional", "Returns", "Error"]
    pie_values = [total_transactional, total_returns, total_errors]
    pie_colors = ['#0066cc', '#107c41', '#8a4bcf']
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=pie_labels, 
        values=pie_values, 
        hole=.5,
        marker=dict(colors=pie_colors),
        textinfo='value+percent',
        textfont=dict(family="Arial, sans-serif", size=11),
        direction='clockwise',
        sort=False
    )])
    
    fig_pie.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5, font=bold_dark_font),
        margin=dict(l=10, r=10, t=40, b=40),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- QUARTER 4: Departmental Bar Chart ---
with layout_col3:
    st.subheader("Calls Processed by Dept")
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=["Dept A", "Dept B", "Dept C"],
        y=[244, 186, 194],
        marker_color=['#0066cc', '#107c41', '#8a4bcf'],
        text=[244, 186, 194], textposition='auto',
        textfont=dict(family="Arial, sans-serif", size=12, color="#ffffff")
    ))
    
    fig_bar.update_layout(
        xaxis=dict(title=dict(text="<b>Department</b>", font=bold_dark_title_font), showgrid=False, tickfont=bold_dark_font),
        yaxis=dict(title=dict(text="<b>Calls Volume</b>", font=bold_dark_title_font), showgrid=True, gridcolor='#e5e5e5', tickfont=bold_dark_font),
        margin=dict(l=50, r=20, t=40, b=50), height=350,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_bar, use_container_width=True)
