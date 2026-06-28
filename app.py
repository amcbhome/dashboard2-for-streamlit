import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# Set page configuration to wide layout
st.set_page_config(page_title="Call Centre Performance Dashboard", layout="wide")

# -----------------------------------------------------------------------------
# 1. LOAD & CORRECT CALL CENTRE DATA
# -----------------------------------------------------------------------------
# Departmental call processing split (Row 1 of Departmental Data)
dept_data = {
    "Department": ["Dept A", "Dept B", "Dept C"],
    "Calls Processed": [244, 186, 194]
}
df_dept = pd.DataFrame(dept_data)

# June 1st to June 28th Time Series Data
# Updated to ensure 2/6/26 reflects 647 calls (exceeding target)
ts_csv = """Date,Total calls
01/06/2026,636
02/06/2026,647
03/06/2026,623
04/06/2026,625
05/06/2026,640
06/06/2026,596
07/06/2026,552
08/06/2026,604
09/06/2026,590
10/06/2026,615
11/06/2026,643
12/06/2026,552
13/06/2026,600
14/06/2026,595
15/06/2026,584
16/06/2026,571
17/06/2026,625
18/06/2026,570
19/06/2026,586
20/06/2026,615
21/06/2026,568
22/06/2026,631
23/06/2026,643
24/06/2026,585
25/06/2026,566
26/06/2026,647
27/06/2026,594
28/06/2026,624"""

df_ts = pd.read_csv(StringIO(ts_csv))
df_ts['Date'] = pd.to_datetime(df_ts['Date'], format='%d/%m/%Y')

# Target baseline parameters
target_baseline = 640

# -----------------------------------------------------------------------------
# 2. HEADER
# -----------------------------------------------------------------------------
st.title("Call Centre Performance Dashboard")
st.caption("Operational volume monitoring from June 1st to June 28th, 2026")
st.write("---")

# -----------------------------------------------------------------------------
# 3. CHARTS SECTION (Split into 3/4 Line Chart and 1/4 Departmental Bar Chart)
# -----------------------------------------------------------------------------
chart_col1, chart_col2 = st.columns([3, 1])

with chart_col1:
    st.subheader("Daily Incoming Call Trends")
    
    fig_ts = go.Figure()
    
    # Line chart trace for volume tracking
    fig_ts.add_trace(go.Scatter(
        x=df_ts['Date'], 
        y=df_ts['Total calls'],
        mode='lines+markers',
        name='Daily Total Calls',
        line=dict(color='#0066cc', width=2.5),
        marker=dict(size=5)
    ))
    
    # Target baseline reference rule
    fig_ts.add_trace(go.Scatter(
        x=df_ts['Date'],
        y=[target_baseline] * len(df_ts),
        mode='lines',
        name=f'Daily Target Threshold ({target_baseline})',
        line=dict(color='#e74c3c', width=2, dash='dash')
    ))
    
    fig_ts.update_layout(
        xaxis=dict(
            title="Date (June 2026)",
            tickformat="%d %b",
            showgrid=True,
            gridcolor='#e5e5e5',
            dtick="D2" # Show every second day to keep labels clean
        ),
        yaxis=dict(
            title="Number of Calls",
            showgrid=True,
            gridcolor='#e5e5e5',
            range=[530, 665]
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=50, r=20, t=10, b=50),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_ts, use_container_width=True)

with chart_col2:
    st.subheader("Calls Processed by Dept")
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df_dept['Department'],
        y=df_dept['Calls Processed'],
        marker_color=['#0066cc', '#107c41', '#8a4bcf'],
        text=df_dept['Calls Processed'],
        textposition='auto'
    ))
    
    fig_bar.update_layout(
        xaxis=dict(
            title="Department",
            showgrid=False
        ),
        yaxis=dict(
            title="Calls Volume",
            showgrid=True,
            gridcolor='#e5e5e5'
        ),
        margin=dict(l=40, r=20, t=42, b=50),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
