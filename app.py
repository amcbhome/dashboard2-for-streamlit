import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration to wide layout to match the original layout
st.set_page_config(page_title="Apex Executive SaaS Dashboard", layout="wide")

# -----------------------------------------------------------------------------
# 1. METRICS DATA (Matching the Dashboard Reference Images)
# -----------------------------------------------------------------------------
mrr_val = 285339
dau_val = 19781
churn_rate = 6.53
conv_rate = 2.82

# -----------------------------------------------------------------------------
# 2. HEADER
# -----------------------------------------------------------------------------
st.title("Apex Executive SaaS Dashboard")
st.caption("Real-time operations, customer distribution, and historical health index")
st.write("---")

# -----------------------------------------------------------------------------
# 3. TOP METRIC CARDS (KPIs)
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Monthly Recurring Revenue (MRR)", 
        value=f"£{mrr_val:,}", 
        delta="+17.74% vs Period Start"
    )

with col2:
    st.metric(
        label="Daily Active Users (DAU)", 
        value=f"{dau_val:,}", 
        delta="+0.32% vs Period Start"
    )

with col3:
    st.metric(
        label="Customer Churn Rate", 
        value=f"{churn_rate}%", 
        delta="-0.41% vs Last Quarter",
        delta_color="inverse" # Displays green for a reduction in churn
    )

with col4:
    st.metric(
        label="Average Conversion Rate", 
        value=f"{conv_rate}%", 
        delta="+0.12% Target Buffer"
    )

st.write("---")

# -----------------------------------------------------------------------------
# 4. CHARTS SECTION (2-Column Layout)
# -----------------------------------------------------------------------------
chart_col1, chart_col2 = st.columns([3, 2])

with chart_col1:
    st.subheader("Financial Growth Track (MRR & ARR)")
    
    # Set the time-series progression timeframe seen in the dashboard screenshots
    dates = pd.date_range(start="2026-04-05", end="2026-06-28", freq="W")
    
    # Scale lines linearly to match visual trends
    mrr_line = [285339] * len(dates)
    arr_line = [2900000 + (i * 38000) for i in range(len(dates))]
    
    fig_growth = go.Figure()
    
    # Solid blue line for MRR
    fig_growth.add_trace(go.Scatter(
        x=dates, y=mrr_line,
        mode='lines',
        name='MRR',
        line=dict(color='#0066cc', width=3)
    ))
    
    # Dashed green line for ARR
    fig_growth.add_trace(go.Scatter(
        x=dates, y=arr_line,
        mode='lines',
        name='Annual Run Rate (ARR Proj.)',
        line=dict(color='#107c41', width=2, dash='dash')
    ))
    
    fig_growth.update_layout(
        xaxis=dict(
            tickformat="%b %d\n%Y",
            showgrid=True,
            gridcolor='#e5e5e5'
        ),
        yaxis=dict(
            tickformat="£,", 
            range=[0, 3500000],
            showgrid=True, 
            gridcolor='#e5e5e5'
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=20, t=20, b=40),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_growth, use_container_width=True)

with chart_col2:
    st.subheader("Subscription Tiers")
    
    # Proportions exactly matching the donut charts across the reference files
    labels = ['Starter', 'Growth', 'Enterprise']
    values = [49.7, 36.3, 14.1]
    colors = ['#0066cc', '#107c41', '#8a4bcf'] # Blue, Green, Purple palette matching
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.6,
        marker=dict(colors=colors),
        textinfo='percent',
        textfont_size=14,
        direction='clockwise',
        sort=False
    )])
    
    fig_pie.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=20, b=40),
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
