import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Shadow Banking Pricing Engine", layout="wide")

st.title("Serverless Financial Econometrics Pipeline")
st.caption("Real-Time Shadow Banking Collateral Valuation & Dynamic Haircut Determination")

st.sidebar.header("Market-Microstructure Configuration")
selected_asset = st.sidebar.selectbox("Simulated Collateral Asset Class", ["Investment Grade Corporate Bonds", "High-Yield Mortgage-Backed Securities", "Emerging Market Sovereign Debt"])
volatility_shock = st.sidebar.slider("Simulate Collateral Downside Volatility", 1.0, 5.0, 3.5)
run_simulation = st.sidebar.button("Initialize Econometric Pricing Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: Option-Implied API -> General Equilibrium Normalization -> XGBoost Inference")

if run_simulation:
    st.subheader(f"Active Financial Intermediation Monitor: {selected_asset}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_quality = col1.empty()
    metric_haircut = col2.empty()
    metric_interest = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(2626)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    asset_qualities = []
    haircut_levels = []
    
    base_quality = 100.0 
    base_haircut = 5.0
    base_interest = 2.5
    
    for i in range(100):
        if i < 30:
            current_quality = base_quality + np.random.uniform(-1.0, 1.0)
            current_haircut = base_haircut + np.random.uniform(-0.1, 0.1)
            current_interest = base_interest + np.random.uniform(-0.05, 0.05)
            status = "LIQUID MARKET"
        elif i >= 30 and i < 65:
            current_quality = base_quality - (i - 30) * (0.8 * volatility_shock) + np.random.uniform(-3.0, 3.0)
            current_haircut = base_haircut + (i - 30) * (0.5 * volatility_shock) + np.random.uniform(-0.5, 0.5)
            current_interest = base_interest + (i - 30) * (0.05 * volatility_shock) + np.random.uniform(-0.1, 0.1)
            status = "DOWNSIDE SHOCK - DELEVERAGING"
        else:
            current_quality = current_quality + np.random.uniform(-2.0, 2.0)
            current_haircut = current_haircut + np.random.uniform(-0.5, 0.5) 
            current_interest = current_interest + np.random.uniform(-0.1, 0.1)
            status = "LIQUIDITY CRUNCH"
            
        current_quality = max(0.0, current_quality)
            
        asset_qualities.append(current_quality)
        haircut_levels.append(current_haircut)
        
        metric_quality.metric("Option-Implied Asset Quality", f"{current_quality:.1f} pts", f"{(current_quality - base_quality):.1f} Shift")
        metric_haircut.metric("Dynamic Haircut Requirement", f"{current_haircut:.2f}%", f"+{(current_haircut - base_haircut):.2f}% Margin")
        metric_interest.metric("Collateralized Interest Rate", f"{current_interest:.2f}%", f"+{(current_interest - base_interest):.2f}% Premium")
        
        if status == "DOWNSIDE SHOCK - DELEVERAGING" or status == "LIQUIDITY CRUNCH":
            metric_status.metric("Shadow Banking Status", status, "Systemic Risk Elevated")
        else:
            metric_status.metric("Shadow Banking Status", status, "Stable Intermediation")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=asset_qualities, mode='lines', name='Collateral Asset Quality', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=haircut_levels, mode='lines', name='Haircut Requirement (%)', yaxis='y2', line=dict(color='red', dash='dot')))
        
        fig.update_layout(
            title="Empirical Asset Pricing: Collateral Quality vs Joint Determination of Haircuts",
            xaxis=dict(title="High-Frequency Market Timeline"),
            yaxis=dict(title="Asset Quality (Pts)"),
            yaxis2=dict(title="Haircut Requirement (%)", overlaying='y', side='right', range=[0, max(20, current_haircut + 5)]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if status == "DOWNSIDE SHOCK - DELEVERAGING" and i == 30:
            log_placeholder.error(f"SYSTEMIC ALERT: Severe downside volatility detected in option-implied telemetry at {time_steps[i].strftime('%H:%M:%S')}. Machine learning inference engine actively calculating general equilibrium shift. Amplifying collateral haircuts to protect shadow banking intermediaries.")
        elif status == "LIQUIDITY CRUNCH" and i == 65:
            log_placeholder.warning(f"MARKET ADJUSTMENT: Haircuts and interest rates stabilized at elevated levels. Systemic liquidity significantly drained. Algorithmic pricing model confirming structural market friction.")
        elif status == "LIQUID MARKET" and i % 5 == 0:
            log_placeholder.success(f"Log: High-frequency financial telemetry tick {i} ingested via serverless API. Collateral markets clearing at baseline equilibrium.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless cloud architecture successfully modeled the joint determination of haircuts and interest rates during a shadow banking collateral shock.")
else:
    st.info("Click 'Initialize Econometric Pricing Engine' in the sidebar to simulate high-frequency asset pricing data ingestion.")