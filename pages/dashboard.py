import sys
import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# Ensure we can import auth.py from the main folder
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))
import auth

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ELLI | Model Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- MEMORY PRESERVATION & GATEKEEPER ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

try:
    session = auth.supabase.auth.get_session()
    if session:
        st.session_state.logged_in = True
        st.session_state.user_email = session.user.email
except Exception:
    pass

if not st.session_state.logged_in:
    st.error("Please log in from the main interface to view this page.")
    st.page_link("webpage.py", label="Return to Login", icon="🔒")
    st.stop()


# --- SHARED UI LOGIC ---
components.html(
    """
    <script>
    const parentDoc = window.parent.document;
    if (!parentDoc.getElementById('elli-lottie-bg')) {
        const script = parentDoc.createElement('script');
        script.src = "https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js";
        parentDoc.head.appendChild(script);

        const container = parentDoc.createElement('div');
        container.id = 'elli-lottie-bg';
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100vw';
        container.style.height = '100vh';
        container.style.zIndex = '0';
        container.style.pointerEvents = 'none';
        container.style.opacity = '0.12';

        script.onload = () => {
            container.innerHTML = `
                <lottie-player src="https://lottie.host/80f7602e-13cb-4a11-8ec8-8cf81e3c8ca4/4xJ1t2T0B8.json" background="transparent" speed="0.6" style="width: 100%; height: 100%;" loop autoplay></lottie-player>
            `;
        };

        const stApp = parentDoc.querySelector('[data-testid="stAppViewContainer"]') || parentDoc.body;
        stApp.appendChild(container);
    }
    </script>
    """,
    height=0,
    width=0,
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
        :root { --ink:#181b1a; --panel:#202523; --mint:#1ee5aa; --gold:#ffcb05; --soft:#b9c0bc; }
        .stApp { background:radial-gradient(circle at 25% 12%, #2a3530 0, #181b1a 32rem); color:#f5f7f5; }
        [data-testid="stHeader"] { background:transparent; } #MainMenu, footer { visibility:hidden; }
        .block-container { max-width:1400px; padding:2rem 3.5rem 2rem; position: relative; z-index: 10; }
        
        .elli-brand { display:flex; align-items:flex-end; gap:0.8rem; margin:.2rem 0 1rem 0; }
        .elli-brand h1 { font:700 clamp(2.5rem,6vw,4rem)/.72 "Space Grotesk",sans-serif; letter-spacing:0; margin:0; color:#f2f4f2; }
        .elli-brand p { font:600 0.8rem/1.22 "Space Grotesk",sans-serif; color:#c5cbc7; margin:0 0 0.3rem 0; max-width:11rem; }
        
        .hero-section { padding:2.2rem; border:1px solid rgba(30,229,170,.2); border-radius:2rem; background:linear-gradient(135deg, rgba(32,37,35,.95), rgba(18,23,20,.95)); box-shadow:0 0 28px rgba(30,229,170,.08); margin-bottom: 2rem; margin-top: 1rem; }
        .hero-section h2 { font:700 clamp(2.4rem,4vw,3.2rem) "Space Grotesk",sans-serif; color:#f4f7f4; margin:0; }
        .hero-subtitle { font:600 1.05rem "DM Mono",monospace; letter-spacing:.12em; text-transform:uppercase; color:var(--mint); margin:.35rem 0 .85rem; }
        .hero-copy { max-width:860px; font:400 1.02rem/1.7 "Space Grotesk",sans-serif; color:#dfe5e1; margin:0; }
        
        /* Metric Styling */
        [data-testid="stMetricValue"] { font-family: "DM Mono", monospace !important; color: var(--gold) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Render Header & Navigation Menu ---
st.markdown(
    '''
    <div class="elli-brand">
        <h1>ELLI</h1>
        <p>Evolving<br>Large<br>Language<br>Intelligence</p>
    </div>
    ''', 
    unsafe_allow_html=True
)

nav_col1, nav_col2, nav_col3, _ = st.columns([1, 1, 1.2, 3])
with nav_col1:
    st.page_link("webpage.py", label="Chat", icon="💬")
with nav_col2:
    st.page_link("pages/landingpage.py", label="Home page", icon="🏠")
with nav_col3:
    st.page_link("pages/dashboard.py", label="Performance", icon="📊")

st.markdown(
    """
    <div class="hero-section">
        <p class="hero-copy">System Analytics</p>
        <h2>Dashboard</h2>
        <p class="hero-subtitle">Real-Time Metrics & Evaluation</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- DASHBOARD METRICS ---
st.markdown("### ⚡ Live Telemetry")
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="Inference Speed", value="112 t/s", delta="+12 t/s")
m2.metric(label="Avg Latency", value="0.7s", delta="-0.2s", delta_color="inverse")
m3.metric(label="Active Parameters", value="110M", delta="MoE Enabled", delta_color="off")
m4.metric(label="Memory Footprint", value="1.2 GB", delta="BF16 Quantized", delta_color="off")

st.markdown("---")

# --- CHARTS ---
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📉 Training Loss Convergence")
    st.caption("Simulated epoch training loss across the mixture of experts.")
    # Generate dummy data for a descending training curve
    epochs = np.arange(1, 101)
    loss = 2.5 * np.exp(-epochs / 20) + 0.5 + np.random.normal(0, 0.05, 100)
    loss_data = pd.DataFrame({"Epochs": epochs, "Loss": loss}).set_index("Epochs")
    st.line_chart(loss_data, color="#1ee5aa")

with col_right:
    st.markdown("### 🏆 Benchmark Comparisons")
    st.caption("Performance on standard NLP datasets (Zero-shot).")
    # Data comparing ELLI to a baseline
    benchmarks = pd.DataFrame({
        "Task": ["GSM8K", "HumanEval", "MMLU", "TruthfulQA"],
        "ELLI-300M": [42.1, 38.5, 45.2, 51.0],
        "Baseline": [35.2, 30.1, 40.4, 45.2],
    }).set_index("Task")
    st.bar_chart(benchmarks)

st.markdown("---")
st.markdown("### ⚙️ Hardware Utilization (Simulated)")
# Generate dummy area chart data for server loads
usage_data = pd.DataFrame(
    np.random.randn(20, 2) * 5 + [45, 60],
    columns=['CPU Usage (%)', 'RAM Usage (%)']
)
st.area_chart(usage_data, color=["#1ee5aa", "#ffcb05"])
