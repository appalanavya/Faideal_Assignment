import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Intelligent Order Prioritisation Engine",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS FOR PREMIUM 3D / GLASSMORPHISM UI ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
        color: #e94560;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(233, 69, 96, 0.3);
    }

    /* Titles and Text */
    h1, h2, h3 {
        color: #00d2ff !important;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
        font-family: 'Inter', sans-serif;
    }
    
    .stMarkdown p {
        color: #ffffff;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #e94560, #a21b3c);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #ff4d6d, #c9184a);
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.5);
    }

    /* Metric Containers */
    [data-testid="stMetricValue"] {
        color: #00d2ff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }

    /* Data Editor / Tables */
    .stDataEditor {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
    }

    /* Hide Streamlit Footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Input Fields & Caret */
    input, textarea, [data-baseweb="input"] {
        caret-color: #00d2ff !important;
        color: #ffffff !important;
    }
    
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
        border-radius: 8px !important;
    }

    /* Data Editor Customization */
    [data-testid="stDataEditor"] {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Animations */
    @keyframes glow {
        0% { box-shadow: 0 0 5px #00d2ff; }
        50% { box-shadow: 0 0 20px #00d2ff; }
        100% { box-shadow: 0 0 5px #00d2ff; }
    }
    
    .glow-effect {
        animation: glow 2s infinite alternate;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def get_sample_data():
    data = [
        {"order_id": 1, "retailer_id": "R1", "order_value": 500, "distance": 3, "order_time": "2026-03-25 09:00:00", "historical_order_frequency": 5, "avg_basket_size": 10, "warehouse_id": "W1"},
        {"order_id": 2, "retailer_id": "R2", "order_value": 200, "distance": 10, "order_time": "2026-03-25 10:30:00", "historical_order_frequency": 2, "avg_basket_size": 4, "warehouse_id": "W1"},
        {"order_id": 3, "retailer_id": "R1", "order_value": 800, "distance": 2, "order_time": "2026-03-25 08:45:00", "historical_order_frequency": 8, "avg_basket_size": 15, "warehouse_id": "W2"},
        {"order_id": 4, "retailer_id": "R3", "order_value": 150, "distance": 7, "order_time": "2026-03-25 11:00:00", "historical_order_frequency": 1, "avg_basket_size": 3, "warehouse_id": "W1"},
        {"order_id": 5, "retailer_id": "R2", "order_value": 650, "distance": 4, "order_time": "2026-03-25 09:30:00", "historical_order_frequency": 6, "avg_basket_size": 12, "warehouse_id": "W2"},
        {"order_id": 6, "retailer_id": "R4", "order_value": 300, "distance": 6, "order_time": "2026-03-25 10:15:00", "historical_order_frequency": 3, "avg_basket_size": 7, "warehouse_id": "W1"},
        {"order_id": 7, "retailer_id": "R1", "order_value": 900, "distance": 1, "order_time": "2026-03-25 08:30:00", "historical_order_frequency": 9, "avg_basket_size": 20, "warehouse_id": "W2"},
        {"order_id": 8, "retailer_id": "R3", "order_value": 400, "distance": 5, "order_time": "2026-03-25 09:45:00", "historical_order_frequency": 4, "avg_basket_size": 9, "warehouse_id": "W1"},
        {"order_id": 9, "retailer_id": "R2", "order_value": 700, "distance": 3, "order_time": "2026-03-25 08:50:00", "historical_order_frequency": 7, "avg_basket_size": 14, "warehouse_id": "W2"},
        {"order_id": 10, "retailer_id": "R4", "order_value": 250, "distance": 8, "order_time": "2026-03-25 10:00:00", "historical_order_frequency": 2, "avg_basket_size": 5, "warehouse_id": "W1"},
    ]
    return pd.DataFrame(data)

def calculate_scores(df, current_time_str):
    current_time = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S")
    
    # Pre-process times and values
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['waiting_time'] = (current_time - df['order_time']).dt.total_seconds() / 60.0 # minutes
    
    # Normalization helper (Min-Max)
    def normalize(series):
        if series.max() == series.min():
            return series * 0 
        return (series - series.min()) / (series.max() - series.min())

    # Scoring columns
    v_val = normalize(df['order_value'])
    v_freq = normalize(df['historical_order_frequency'])
    v_basket = normalize(df['avg_basket_size'])
    v_dist = normalize(df['distance'])
    v_wait = normalize(df['waiting_time'])
    
    # Formula: Score = (0.35 * order_value) + (0.25 * historical_order_frequency) + (0.15 * avg_basket_size) - (0.15 * distance) + (0.10 * waiting_time)
    df['score'] = (0.35 * v_val) + (0.25 * v_freq) + (0.15 * v_basket) - (0.15 * v_dist) + (0.10 * v_wait)
    
    # Rescale score to 0-100 for readability
    df['score'] = (normalize(df['score']) * 100).round(2)
    return df

def assign_decisions(df, capacity):
    # Sort by score descending
    df = df.sort_values(by='score', ascending=False).reset_index(drop=True)
    
    df['decision'] = "REJECT"
    
    fulfilled_count = 0
    retailer_fulfilled = {}
    max_per_retailer = max(1, int(0.3 * capacity))
    
    # 1. Assign FULFILL
    idx_to_skip = []
    for idx, row in df.iterrows():
        r_id = row['retailer_id']
        curr_r_count = retailer_fulfilled.get(r_id, 0)
        
        if fulfilled_count < capacity and curr_r_count < max_per_retailer:
            df.at[idx, 'decision'] = "FULFILL"
            fulfilled_count += 1
            retailer_fulfilled[r_id] = curr_r_count + 1
        else:
            idx_to_skip.append(idx)
            
    # 2. Assign DELAY (Next 30% of remaining orders)
    remaining_df = df.iloc[idx_to_skip]
    delay_count = int(0.3 * len(df))
    
    delay_indices = remaining_df.head(delay_count).index
    df.loc[delay_indices, 'decision'] = "DELAY"
    
    return df

# --- MAIN UI ---

def main():
    st.markdown("""
        <h1 style='text-align: center; color: #00d2ff; text-shadow: 0 0 20px rgba(0,210,255,0.7);'>
            🚛 Intelligent Order Prioritisation Engine 🤖
        </h1>
        <p style='text-align: center; font-size: 1.2rem; color: #ffffff; opacity: 0.8;'>
            Advanced Logistics Optimization & Real-time Prioritisation Dashboard
        </p>
    """, unsafe_allow_html=True)
    
    # Session State Initialization
    if 'manual_df' not in st.session_state:
        st.session_state.manual_df = get_sample_data()

    # --- INPUT LAYER ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Order Entry & Management")
        
        # Manual Input
        edited_df = st.data_editor(
            st.session_state.manual_df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "order_id": st.column_config.NumberColumn("Order ID", help="Unique identifier for the order"),
                "order_time": st.column_config.TextColumn("Order Time"),
            }
        )
        st.session_state.manual_df = edited_df
        
        # Dataset Upload
        uploaded_file = st.file_uploader("📂 Upload Order Dataset (CSV)", type="csv")
        if uploaded_file is not None:
            uploaded_df = pd.read_csv(uploaded_file)
            st.session_state.manual_df = pd.concat([st.session_state.manual_df, uploaded_df]).drop_duplicates(subset=['order_id']).reset_index(drop=True)
            st.success("CSV Data Merged Successfully!")
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("⚙️ Engine Controls")
        
        current_time_input = st.text_input("📍 Simulation Time", value="2026-03-25 11:30:00")
        capacity = st.slider("🚚 Delivery Capacity (Orders/Hr)", min_value=1, max_value=50, value=5)
        
        st.info(f"Retailer Fairness: Max {max(1, int(0.3*capacity))} orders/retailer")
        
        if st.button("🚀 Run Prioritisation Engine", use_container_width=True):
            st.session_state.run_engine = True
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PROCESSING LAYER ---
    if st.session_state.get('run_engine', False):
        final_df = calculate_scores(st.session_state.manual_df.copy(), current_time_input)
        final_df = assign_decisions(final_df, capacity)
        
        # --- DASHBOARD LAYER ---
        st.markdown("---")
        st.header("📊 Evaluation Results")
        
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📦 Total Orders", len(final_df))
        m2.metric("✅ Fulfilled", len(final_df[final_df['decision'] == 'FULFILL']))
        m3.metric("⏳ Delayed", len(final_df[final_df['decision'] == 'DELAY']))
        m4.metric("❌ Rejected", len(final_df[final_df['decision'] == 'REJECT']))
        
        # Visualizations
        v_col1, v_col2 = st.columns(2)
        
        with v_col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig_scores = px.bar(
                final_df.sort_values('score', ascending=True),
                x='score', y='order_id', color='decision',
                orientation='h',
                title="Order Priority Scores",
                color_discrete_map={'FULFILL': '#00ff87', 'DELAY': '#f9d423', 'REJECT': '#ff4b2b'},
                template="plotly_dark"
            )
            fig_scores.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_scores, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with v_col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig_pie = px.pie(
                final_df, names='decision',
                title="Decision Distribution",
                hole=.4,
                color='decision',
                color_discrete_map={'FULFILL': '#00ff87', 'DELAY': '#f9d423', 'REJECT': '#ff4b2b'},
                template="plotly_dark"
            )
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Detailed Results Table
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📑 Prioritised Order Queue")
        
        def color_rows(val):
            if val == 'FULFILL': color = '#00ff87'; bg = 'rgba(0, 255, 135, 0.1)'
            elif val == 'DELAY': color = '#f9d423'; bg = 'rgba(249, 212, 35, 0.1)'
            else: color = '#ff4b2b'; bg = 'rgba(255, 75, 43, 0.1)'
            return f'color: {color}; background-color: {bg}; font-weight: bold'

        styled_df = final_df.style.applymap(color_rows, subset=['decision'])
        st.dataframe(styled_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
