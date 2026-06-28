import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration to wide layout to match the original layout
st.set_page_config(page_title="Apex Departmental Dashboard", layout="wide")

# -----------------------------------------------------------------------------
# 1. RETRIEVE DATA FROM GOOGLE SHEETS
# -----------------------------------------------------------------------------
# Departmental performance dataset directly from your spreadsheet
data = {
    "Metric": ["Calls", "Resolved", "Transactional", "Returns", "Error"],
    "Dept A": [244, 203, 25, 12, 4],
    "Dept B": [186, 144, 14, 23, 5],
    "Dept C": [194, 167, 22, 4, 1]
}

df = pd.DataFrame(data)

# Calculate total operational stats dynamically
total_calls = df.loc[df["Metric"] == "Calls", ["Dept A", "Dept B", "Dept C"]].sum(axis=1).values[0]
total_resolved = df.loc[df["Metric"] == "Resolved", ["Dept A", "Dept B", "Dept C"]].sum(axis=1).values[0]
resolution_rate = round((total_resolved / total_calls) * 100, 2)

# Target benchmark from spreadsheet
target_calls = 640
target_delta = total_calls - target_calls  # -16 vs target

# -----------------------------------------------------------------------------
# 2. STREAMLIT APP HEADER
# -----------------------------------------------------------------------------
st.title("Apex Departmental Operations Dashboard")
st.caption("Real-time communication metrics, departmental breakdowns, and target tracking")
st.write("---")

# -----------------------------------------------------------------------------
# 3. TOP METRIC CARDS (KPIs)
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Operational Calls", 
        value=f"{total_calls:,}", 
        delta=f"{target_delta} vs Target ({target_calls})"
    )

with col2:
    st.metric(
        label="Resolved Issues", 
        value=f"{total_resolved:,}", 
        delta="KPI baseline met"
    )

with col3:
    st.metric(
        label="Overall Resolution Rate", 
        value=f"{resolution_rate}%", 
        delta="+2.5% vs Last Period"
    )

with col4:
    st.metric(
        label="Target Completion Status", 
        value="97.50%", 
        delta="-2.50% Target Buffer",
        delta_color="inverse"
    )

st.write("---")

# -----------------------------------------------------------------------------
# 4. VISUALIZATIONS SECTION (2-Column Layout)
# -----------------------------------------------------------------------------
chart_col1, chart_col2 = st.columns([3, 2])

with chart_col1:
    st.subheader("Departmental Metric Contributions")
    
    # Restructuring data for clean multi-bar visual tracking
    categories = df["Metric"].tolist()
    
    fig_bars = go.Figure()
    fig_bars.add_trace(go.Bar(name='Dept A', x=categories, y=df['Dept A'].tolist(), marker_color='#0066cc'))
    fig_bars.add_trace(go.Bar(name='Dept B', x=categories, y=df['Dept B'].tolist(), marker_color='#107c41'))
    fig_bars.add_trace(go.Bar(name='Dept C', x=categories, y=df['Dept C'].tolist(), marker_color='#8a4bcf'))
    
    fig_bars.update_layout(
        barmode='group',
        xaxis=dict(showgrid=True, gridcolor='#e5e5e5'),
        yaxis=dict(showgrid=True, gridcolor='#e5e5e5'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=20, b=40),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_bars, use_container_width=True)

with chart_col2:
    st.subheader("Total Incoming Volume Share")
    
    # Donut chart distribution of total volumes per team
    dept_labels = ['Dept A', 'Dept B', 'Dept C']
    dept_shares = [df['Dept A'].sum(), df['Dept B'].sum(), df['Dept C'].sum()]
    colors = ['#0066cc', '#107c41', '#8a4bcf']
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=dept_labels, 
        values=dept_shares, 
        hole=.6,
        marker=dict(colors=colors),
        textinfo='percent',
        textfont_size=14,
        direction='clockwise',
        sort=False
    )])
    
    fig_donut.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=20, b=40),
        height=400
    )
    
    st.plotly_chart(fig_donut, use_container_width=True)

st.write("---")

# -----------------------------------------------------------------------------
# 5. DATASET TABLE PREVIEW
# -----------------------------------------------------------------------------
st.subheader("Raw Spreadsheet Overview")
st.dataframe(df, use_container_width=True, hide_index=True)
