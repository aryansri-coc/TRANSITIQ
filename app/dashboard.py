"""
TransitIQ: Public Transit Intelligence & Operations Command Centre
Ultra-Premium SaaS Enterprise UI (Dark Theme, Zero Emojis, Custom Nav Menu)
Microsoft DP-900 (Azure Data Fundamentals) Capstone Project
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="TransitIQ | Urban Mobility Operations",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-End Professional Enterprise Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Global Container Adjustments */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 96%;
    }

    /* Streamlit Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: #090d16 !important;
        border-right: 1px solid #1e293b !important;
    }

    /* Transform Native Radio Buttons into High-End Navigation Menu */
    div[data-testid="stRadio"] > div {
        gap: 6px;
    }
    div[data-testid="stRadio"] label {
        background: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 5px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: #1e293b !important;
        border-color: #38bdf8 !important;
        transform: translateX(3px) !important;
    }
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        margin: 0 !important;
    }
    /* Active Navigation State */
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%) !important;
        border-color: #38bdf8 !important;
        border-left: 4px solid #38bdf8 !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    /* Hide the default native radio circles */
    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    /* Top Hero Header */
    .hero-banner {
        background: linear-gradient(135deg, #090d16 0%, #0f172a 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.4rem 2rem;
        margin-bottom: 1.6rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
    }
    .hero-title {
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #f8fafc;
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        font-size: 0.88rem;
        color: #94a3b8;
    }

    /* Form & Console Card Container */
    .console-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.6rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.3rem;
        letter-spacing: -0.01em;
    }
    .card-subtitle {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 1.2rem;
    }

    /* Metric Cards */
    .metric-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        transition: border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #38bdf8;
    }
    .metric-label {
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #f8fafc;
        margin: 0.25rem 0;
    }
    .metric-delta {
        font-size: 0.78rem;
        color: #38bdf8;
        font-weight: 600;
    }

    /* Modern Styled Dropdown Labels */
    label[data-testid="stWidgetLabel"] p {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: #cbd5e1 !important;
        margin-bottom: 4px !important;
    }
    
    /* Streamlit Buttons Styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.4rem !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.45) !important;
    }

    /* Pill Badges */
    .pill-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-metro { background: #312e81; color: #a5b4fc; border: 1px solid #4338ca; }
    .badge-bus { background: #0c4a6e; color: #7dd3fc; border: 1px solid #0369a1; }
    .badge-express { background: #064e3b; color: #6ee7b7; border: 1px solid #047857; }
    .badge-commuter { background: #451a03; color: #fcd34d; border: 1px solid #b45309; }
    .badge-active { background: #064e3b; color: #6ee7b7; border: 1px solid #059669; }

    /* Live Ticket Pre-booking Card */
    .receipt-card {
        background: #090d16;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1rem;
    }
    .receipt-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #1e293b;
        font-size: 0.85rem;
    }
    .receipt-label { color: #94a3b8; font-weight: 500; }
    .receipt-value { color: #f8fafc; font-weight: 700; }
    
    /* Digital Boarding Pass */
    .boarding-pass {
        background: #0b1120;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.6rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    .pass-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
    }
    .pass-route {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1.2rem 0;
        text-align: center;
    }
    .pass-station {
        font-size: 1.2rem;
        font-weight: 800;
        color: #f8fafc;
    }
    .pass-arrow {
        font-size: 1.4rem;
        color: #38bdf8;
    }
    .pass-details {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        background: #060911;
        padding: 0.9rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #1e293b;
    }
    .pass-label { font-size: 0.7rem; color: #64748b; font-weight: 700; text-transform: uppercase; }
    .pass-val { font-size: 0.95rem; font-weight: 700; color: #f8fafc; }
</style>
""", unsafe_allow_html=True)

# Imports for data and services
from src.analytics.metrics_engine import (
    get_executive_kpis,
    get_route_performance_df,
    get_hourly_ridership_df,
    get_stop_demand_df,
    get_fleet_utilization_df,
    get_delay_monitoring_df,
    get_payment_breakdown
)
from src.services.transit_service import TransitService
from src.data.csv_ingestion import run_data_quality_audit, export_tables_to_csv
from src.data.seed_data import generate_and_seed_data
from src.db.connection import execute_query, DB_DIALECT

# Ensure initial data exists
try:
    kpis = get_executive_kpis()
except Exception:
    generate_and_seed_data()
    kpis = get_executive_kpis()

# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="padding: 0.5rem 0.2rem 1rem 0.2rem; border-bottom: 1px solid #1e293b; margin-bottom: 1.2rem;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; color: white;">
                    TQ
                </div>
                <div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">TransitIQ</div>
                    <div style="font-size: 0.74rem; color: #64748b; font-weight: 600;">Urban Mobility Command</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">
            Operations Consoles
        </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation Menu",
        [
            "Network Overview",
            "Ticketing Operations",
            "Corridors & Stops",
            "Passenger Demand",
            "Fleet & Dispatch",
            "Technical Lab"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 1rem; margin-top: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span style="width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block;"></span>
                <span style="font-size: 0.75rem; font-weight: 700; color: #10b981; text-transform: uppercase;">System Operational</span>
            </div>
            <div style="font-size: 0.78rem; color: #cbd5e1; font-weight: 600;">Engine: {DB_DIALECT.upper()} Mode</div>
            <div style="font-size: 0.72rem; color: #64748b; margin-top: 3px;">Microsoft DP-900 Relational Baseline</div>
        </div>
    """, unsafe_allow_html=True)

# Top Hero Header
st.markdown(f"""
    <div class="hero-banner">
        <div>
            <div class="hero-title">TransitIQ Operations Command</div>
            <div class="hero-subtitle">Metropolitan Transit Network Operations, Capacity Monitoring & Relational Data Platform</div>
        </div>
        <div style="text-align: right;">
            <span class="pill-badge badge-active">Live System</span>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">6 Lines • 16 Assets • 160 Trips</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Helper Function: Render Offline Interactive Transit Network Map
def render_transit_network_map():
    segments = execute_query("""
        SELECT 
            rs.route_id,
            r.route_code,
            r.route_name,
            r.route_type,
            rs.stop_sequence,
            s.stop_name,
            s.latitude,
            s.longitude
        FROM route_segments rs
        JOIN routes r ON rs.route_id = r.route_id
        JOIN stops s ON rs.stop_id = s.stop_id
        ORDER BY rs.route_id, rs.stop_sequence ASC
    """)
    stop_stats = get_stop_demand_df()

    fig = go.Figure()
    
    route_colors = {
        "M-RED": "#ef4444",
        "M-BLUE": "#3b82f6",
        "BRT-101": "#06b6d4",
        "BRT-102": "#14b8a6",
        "EXP-500": "#10b981",
        "CR-10": "#f59e0b"
    }

    routes_grouped = {}
    for seg in segments:
        code = seg["route_code"]
        if code not in routes_grouped:
            routes_grouped[code] = {"name": seg["route_name"], "lats": [], "lons": []}
        routes_grouped[code]["lats"].append(seg["latitude"])
        routes_grouped[code]["lons"].append(seg["longitude"])

    for code, data in routes_grouped.items():
        color = route_colors.get(code, "#94a3b8")
        fig.add_trace(go.Scatter(
            x=data["lons"],
            y=data["lats"],
            mode="lines",
            name=f"{code} - {data['name']}",
            line=dict(color=color, width=3.5),
            hoverinfo="name"
        ))

    fig.add_trace(go.Scatter(
        x=stop_stats["longitude"],
        y=stop_stats["latitude"],
        mode="markers+text",
        name="Station Hubs",
        text=stop_stats["stop_name"],
        textposition="top center",
        textfont=dict(color="#f8fafc", size=9),
        marker=dict(
            size=stop_stats["total_footfall"].apply(lambda x: min(20, max(8, x / 12))),
            color="#38bdf8",
            line=dict(width=1.5, color="#f8fafc"),
            opacity=0.95
        ),
        hovertemplate="<b>%{text}</b><br>Footfall: %{customdata[0]}<br>Boardings: %{customdata[1]}<br>Alightings: %{customdata[2]}<extra></extra>",
        customdata=stop_stats[["total_footfall", "total_boardings", "total_alightings"]].values
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#090d16",
        plot_bgcolor="#090d16",
        margin=dict(l=15, r=15, t=15, b=15),
        height=380,
        xaxis=dict(title="Longitude (°E)", showgrid=True, gridcolor="#1e293b", zeroline=False, color="#94a3b8"),
        yaxis=dict(title="Latitude (°N)", showgrid=True, gridcolor="#1e293b", zeroline=False, color="#94a3b8"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9, color="#cbd5e1"))
    )
    return fig

# ==============================================================================
# 1. NETWORK OVERVIEW
# ==============================================================================
if menu == "Network Overview":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Active Corridors</div>
                <div class="metric-value">{kpis.get('active_routes', 6)} Lines</div>
                <div class="metric-delta">Metro, BRT & Commuter</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">On-Time Performance</div>
                <div class="metric-value">{kpis.get('on_time_performance_pct', 94.0)}%</div>
                <div class="metric-delta">Target Benchmark: >90%</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Ridership</div>
                <div class="metric-value">{kpis.get('total_passengers', 2200):,}</div>
                <div class="metric-delta">Across 160 Scheduled Trips</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Gross Revenue</div>
                <div class="metric-value">₹{kpis.get('total_revenue', 0.0):,.0f}</div>
                <div class="metric-delta">Cashless Fare Collections</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_map, col_chart = st.columns([6, 5])
    with col_map:
        st.markdown("""
            <div class="console-card">
                <div class="card-title">Topological Transit Line Map</div>
                <div class="card-subtitle">Network alignment vector routes and station hubs sized by crowd footfall</div>
        """, unsafe_allow_html=True)
        st.plotly_chart(render_transit_network_map(), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart:
        st.markdown("""
            <div class="console-card">
                <div class="card-title">Corridor Revenue Leaderboard</div>
                <div class="card-subtitle">Gross fare collection across active transit lines</div>
        """, unsafe_allow_html=True)
        route_df = get_route_performance_df()
        fig_rev = px.bar(
            route_df,
            x="total_revenue",
            y="route_name",
            orientation="h",
            color="route_type",
            color_discrete_map={
                "Metro Rail": "#818cf8",
                "Rapid Bus": "#38bdf8",
                "Express Shuttle": "#34d399",
                "Commuter Train": "#fbbf24"
            },
            template="plotly_dark",
            height=380
        )
        fig_rev.update_layout(
            paper_bgcolor="#090d16",
            plot_bgcolor="#090d16",
            xaxis=dict(title="Revenue (₹)", showgrid=True, gridcolor="#1e293b"),
            yaxis=dict(title="", showgrid=False),
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9))
        )
        st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Clean Corridor Cards
    st.markdown("### Corridor Fleet & Operational Readiness")
    cols = st.columns(3)
    for idx, row in route_df.iterrows():
        c = cols[idx % 3]
        badge_class = "badge-metro" if "Metro" in row["route_type"] else ("badge-bus" if "Bus" in row["route_type"] else "badge-express")
        with c:
            st.markdown(f"""
                <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 1.1rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span class="pill-badge {badge_class}">{row['route_code']}</span>
                        <span style="font-size: 0.78rem; color: #94a3b8; font-weight: 600;">{row['distance_km']} km</span>
                    </div>
                    <div style="font-size: 0.98rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.4rem;">{row['route_name']}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; border-top: 1px solid #1e293b; padding-top: 0.5rem; margin-top: 0.5rem;">
                        <span>{row['total_passengers']:,} riders</span>
                        <span style="color: #38bdf8; font-weight: 600;">{row['on_time_percentage']}% on-time</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 2. TICKETING OPERATIONS (HIGH-END REDESIGNED KIOSK)
# ==============================================================================
elif menu == "Ticketing Operations":
    bookable = TransitService.get_bookable_trips()
    
    if not bookable:
        st.warning("No scheduled trips currently available for ticketing.")
    else:
        trip_map = {
            f"[{t['trip_code']}] {t['route_name']} ({t['vehicle_code']}) - Dep: {t['scheduled_departure']}": t
            for t in bookable
        }

        col_form, col_preview = st.columns([6, 4])

        with col_form:
            st.markdown("""
                <div class="console-card">
                    <div class="card-title">Ticketing & Reservation Terminal</div>
                    <div class="card-subtitle">ACID Transaction Engine • Concession Discount Calculation • Immediate Inventory Commit</div>
            """, unsafe_allow_html=True)

            selected_trip_label = st.selectbox("1. Active Transit Trip & Scheduled Departure:", list(trip_map.keys()))
            trip_data = trip_map[selected_trip_label]
            trip_stops = TransitService.get_stops_for_trip(trip_data["trip_id"])

            c_orig, c_dest = st.columns(2)
            with c_orig:
                orig_opts = {f"{s['stop_sequence']:02d}. {s['stop_name']}": s['stop_id'] for s in trip_stops[:-1]}
                sel_orig_label = st.selectbox("2. Boarding Station (Origin):", list(orig_opts.keys()))
                sel_orig_id = orig_opts[sel_orig_label]

            with c_dest:
                dest_opts = {f"{s['stop_sequence']:02d}. {s['stop_name']}": s['stop_id'] for s in trip_stops[1:]}
                sel_dest_label = st.selectbox("3. Alighting Station (Destination):", list(dest_opts.keys()))
                sel_dest_id = dest_opts[sel_dest_label]

            c_pass, c_pay = st.columns(2)
            with c_pass:
                passenger_cat = st.selectbox(
                    "4. Passenger Classification & Concession:",
                    ["Standard Adult (Full Fare)", "Student (50% Concession)", "Senior Citizen (60% Concession)", "Commuter Passholder (30% Concession)"]
                )
                cat_clean = passenger_cat.split(" (")[0]

            with c_pay:
                pay_method = st.selectbox(
                    "5. Payment Channel:",
                    ["Transit Smartcard", "Mobile QR / UPI", "Contactless EMV", "Ticket Counter"]
                )

            st.markdown("<br>", unsafe_allow_html=True)
            book_clicked = st.button("Confirm & Issue Electronic Ticket", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Dynamic Pre-Booking Receipt Calculation
        base_fare = trip_data["base_fare"]
        discount_map = {"Standard Adult": 1.0, "Student": 0.50, "Senior Citizen": 0.40, "Commuter Passholder": 0.70}
        discount_rate = discount_map.get(cat_clean, 1.0)
        final_fare = round(base_fare * discount_rate, 2)
        discount_amt = round(base_fare - final_fare, 2)
        occupancy_pct = min(100.0, round((trip_data["booked_passengers"] / trip_data["capacity"]) * 100, 1))

        with col_preview:
            st.markdown("""
                <div class="console-card">
                    <div class="card-title">Fare & Inventory Summary</div>
                    <div class="card-subtitle">Real-time capacity tracking & fare computation</div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="receipt-card">
                    <div class="receipt-row">
                        <span class="receipt-label">Route Line</span>
                        <span class="receipt-value">{trip_data['route_name']}</span>
                    </div>
                    <div class="receipt-row">
                        <span class="receipt-label">Vehicle Assigned</span>
                        <span class="receipt-value">{trip_data['vehicle_code']}</span>
                    </div>
                    <div class="receipt-row">
                        <span class="receipt-label">Trip Code</span>
                        <span class="receipt-value">{trip_data['trip_code']}</span>
                    </div>
                    <div class="receipt-row">
                        <span class="receipt-label">Seat Availability</span>
                        <span class="receipt-value">{trip_data['booked_passengers']} / {trip_data['capacity']} booked ({occupancy_pct}%)</span>
                    </div>
                    <div class="receipt-row">
                        <span class="receipt-label">Base Adult Fare</span>
                        <span class="receipt-value">₹{base_fare:.2f}</span>
                    </div>
                    <div class="receipt-row">
                        <span class="receipt-label">Concession Discount</span>
                        <span class="receipt-value" style="color: #38bdf8;">-₹{discount_amt:.2f}</span>
                    </div>
                    <div class="receipt-row" style="border-bottom: none; padding-top: 0.8rem;">
                        <span style="font-size: 1rem; font-weight: 700; color: #f8fafc;">Total Payable</span>
                        <span style="font-size: 1.35rem; font-weight: 800; color: #34d399;">₹{final_fare:.2f}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Capacity Progress Bar
            st.caption("Vehicle Capacity Utilization")
            st.progress(occupancy_pct / 100.0)

            st.markdown("</div>", unsafe_allow_html=True)

        # Handle Booking Submission
        if book_clicked:
            res = TransitService.book_ticket(
                trip_id=trip_data["trip_id"],
                origin_stop_id=sel_orig_id,
                destination_stop_id=sel_dest_id,
                passenger_type=cat_clean,
                payment_method=pay_method
            )
            
            if res["success"]:
                st.success("Transaction committed successfully to relational database under ACID protocol.")
                orig_name = sel_orig_label.split(". ")[1]
                dest_name = sel_dest_label.split(". ")[1]
                
                st.markdown(f"""
                    <div class="boarding-pass">
                        <div class="pass-header">
                            <div>
                                <span style="font-size: 1.15rem; font-weight: 800; color: #38bdf8;">TRANSITIQ BOARDING PASS</span><br>
                                <span style="font-size: 0.74rem; color: #94a3b8;">METROPOLITAN TRANSIT AUTHORITY</span>
                            </div>
                            <div style="text-align: right;">
                                <span class="pill-badge badge-active">CONFIRMED</span>
                            </div>
                        </div>
                        
                        <div class="pass-route">
                            <div>
                                <div class="pass-label">ORIGIN</div>
                                <div class="pass-station">{orig_name}</div>
                            </div>
                            <div class="pass-arrow">➔</div>
                            <div>
                                <div class="pass-label">DESTINATION</div>
                                <div class="pass-station">{dest_name}</div>
                            </div>
                        </div>
                        
                        <div class="pass-details">
                            <div>
                                <div class="pass-label">Ticket Ref</div>
                                <div class="pass-val">{res['ticket_reference']}</div>
                            </div>
                            <div>
                                <div class="pass-label">Category</div>
                                <div class="pass-val">{res['passenger_type']}</div>
                            </div>
                            <div>
                                <div class="pass-label">Fare Paid</div>
                                <div class="pass-val" style="color: #34d399;">₹{res['fare_paid']:.2f}</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; border-top: 1px dashed #334155; padding-top: 0.8rem;">
                            <span style="font-size: 0.74rem; color: #94a3b8;">Channel: <b>{res['payment_method']}</b></span>
                            <span style="font-family: monospace; font-size: 0.95rem; letter-spacing: 2px; color: #64748b;">||| | |||| | ||| ||</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Transaction Rejected: {res['message']}")

# ==============================================================================
# 3. CORRIDORS & STOPS
# ==============================================================================
elif menu == "Corridors & Stops":
    st.markdown("""
        <div class="console-card">
            <div class="card-title">Transit Corridor Alignment & Station Inspector</div>
            <div class="card-subtitle">Sequential station alignments, inter-station distances, estimated travel times, and accessibility infrastructure</div>
    """, unsafe_allow_html=True)

    routes = execute_query("SELECT route_id, route_code, route_name, route_type, distance_km, base_fare FROM routes ORDER BY route_id")
    route_choices = {f"{r['route_code']} - {r['route_name']} ({r['route_type']})": r for r in routes}
    
    selected_name = st.selectbox("Select Corridor:", list(route_choices.keys()))
    sel_route = route_choices[selected_name]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Mode of Transit", sel_route["route_type"])
    with c2:
        st.metric("Corridor Length", f"{sel_route['distance_km']} km")
    with c3:
        st.metric("Base Fare", f"₹{sel_route['base_fare']:.2f}")
    with c4:
        st.metric("Operational Status", "Active Service")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Sequential Station Alignment (Stop by Stop)")

    segments = execute_query("""
        SELECT 
            rs.stop_sequence,
            s.stop_name,
            s.stop_code,
            s.zone_id,
            s.wheelchair_accessible,
            rs.distance_from_start_km,
            rs.est_travel_time_min
        FROM route_segments rs
        JOIN stops s ON rs.stop_id = s.stop_id
        WHERE rs.route_id = :rid
        ORDER BY rs.stop_sequence ASC
    """, {"rid": sel_route["route_id"]})

    # Visual Stepper
    stepper_html = '<div class="station-stepper" style="display: flex; overflow-x: auto; gap: 8px; padding: 12px 0;">'
    for i, s in enumerate(segments):
        stepper_html += f"""
            <div style="background: #090d16; border: 1px solid #1e293b; border-radius: 10px; padding: 10px 14px; min-width: 150px; text-align: center;">
                <div style="font-size: 0.68rem; font-weight: 800; color: #38bdf8;">STOP {s['stop_sequence']:02d}</div>
                <div style="font-size: 0.88rem; font-weight: 700; color: #f8fafc; margin-top: 3px;">{s['stop_name']}</div>
                <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 3px;">{s['distance_from_start_km']} km | ~{s['est_travel_time_min']} min</div>
            </div>
        """
        if i < len(segments) - 1:
            stepper_html += '<div style="color: #64748b; font-size: 1.1rem; font-weight: 700; display: flex; align-items: center;">➔</div>'
    stepper_html += '</div>'
    st.markdown(stepper_html, unsafe_allow_html=True)

    df_seg = pd.DataFrame(segments)
    df_seg["Accessibility"] = df_seg["wheelchair_accessible"].apply(lambda x: "Elevator & Tactile Paving" if x else "Standard Stairs")
    st.dataframe(
        df_seg[["stop_sequence", "stop_name", "zone_id", "distance_from_start_km", "est_travel_time_min", "Accessibility"]].rename(columns={
            "stop_sequence": "Seq",
            "stop_name": "Station Name",
            "zone_id": "Fare Zone",
            "distance_from_start_km": "Distance (km)",
            "est_travel_time_min": "Travel Time (min)"
        }),
        use_container_width=True,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 4. PASSENGER DEMAND
# ==============================================================================
elif menu == "Passenger Demand":
    hourly_df = get_hourly_ridership_df()
    payment_df = get_payment_breakdown()

    col_rush, col_pie = st.columns([7, 4])
    
    with col_rush:
        st.markdown("""
            <div class="console-card">
                <div class="card-title">Hourly Passenger Volume (24-Hour Operational Cycle)</div>
                <div class="card-subtitle">Shaded regions highlight peak morning (08:00–10:00) and evening (17:00–19:00) crowding</div>
        """, unsafe_allow_html=True)
        fig_rush = px.area(
            hourly_df,
            x="hour_of_day",
            y="passenger_count",
            color="route_type",
            labels={"hour_of_day": "Hour of Day", "passenger_count": "Boardings"},
            color_discrete_map={
                "Metro Rail": "#818cf8",
                "Rapid Bus": "#38bdf8",
                "Express Shuttle": "#34d399",
                "Commuter Train": "#fbbf24"
            },
            template="plotly_dark",
            height=360
        )
        fig_rush.update_layout(
            paper_bgcolor="#090d16",
            plot_bgcolor="#090d16",
            xaxis=dict(showgrid=True, gridcolor="#1e293b"),
            yaxis=dict(showgrid=True, gridcolor="#1e293b")
        )
        fig_rush.add_vrect(x0="08", x1="10", fillcolor="#38bdf8", opacity=0.15, line_width=0, annotation_text="Morning Peak", annotation_position="top left")
        fig_rush.add_vrect(x0="17", x1="19", fillcolor="#fbbf24", opacity=0.15, line_width=0, annotation_text="Evening Peak", annotation_position="top left")
        st.plotly_chart(fig_rush, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_pie:
        st.markdown("""
            <div class="console-card">
                <div class="card-title">Fare Collection Channels</div>
                <div class="card-subtitle">Ridership share across ticketing methods</div>
        """, unsafe_allow_html=True)
        pay_totals = payment_df.groupby("payment_method")["transaction_count"].sum().reset_index()
        fig_pay = px.pie(
            pay_totals,
            names="payment_method",
            values="transaction_count",
            hole=0.45,
            template="plotly_dark",
            color_discrete_sequence=["#38bdf8", "#818cf8", "#34d399", "#fbbf24"],
            height=360
        )
        fig_pay.update_layout(paper_bgcolor="#090d16", plot_bgcolor="#090d16")
        fig_pay.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pay, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    col_demo, col_busiest = st.columns(2)
    with col_demo:
        st.markdown("""
            <div class="console-card">
                <div class="card-title">Passenger Demographics</div>
                <div class="card-subtitle">Volume of tickets issued across concession classifications</div>
        """, unsafe_allow_html=True)
        demo_totals = payment_df.groupby("passenger_type")["transaction_count"].sum().reset_index()
        fig_demo = px.bar(
            demo_totals,
            x="passenger_type",
            y="transaction_count",
            color="passenger_type",
            template="plotly_dark",
            labels={"passenger_type": "Category", "transaction_count": "Transactions"},
            height=280
        )
        fig_demo.update_layout(paper_bgcolor="#090d16", plot_bgcolor="#090d16", showlegend=False)
        st.plotly_chart(fig_demo, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_busiest:
        st.markdown("""
            <div class="console-card">
                <div class="card-title">Top 5 Station Hubs by Footfall</div>
                <div class="card-subtitle">Highest passenger boarding and transfer hubs</div>
        """, unsafe_allow_html=True)
        stop_df = get_stop_demand_df().head(5)
        fig_stops = px.bar(
            stop_df,
            x="stop_name",
            y="total_footfall",
            color="total_footfall",
            template="plotly_dark",
            color_continuous_scale="Blues",
            labels={"stop_name": "Station", "total_footfall": "Footfall"},
            height=280
        )
        fig_stops.update_layout(paper_bgcolor="#090d16", plot_bgcolor="#090d16", coloraxis_showscale=False)
        st.plotly_chart(fig_stops, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 5. FLEET & DISPATCH
# ==============================================================================
elif menu == "Fleet & Dispatch":
    fleet_df = get_fleet_utilization_df()
    delay_df = get_delay_monitoring_df()

    col_f1, col_f2 = st.columns([6, 5])
    with col_f1:
        st.markdown("""
            <div class="console-card">
                <div class="card-title">Vehicle Fleet Propulsion</div>
                <div class="card-subtitle">Share of clean energy rolling stock across lines</div>
        """, unsafe_allow_html=True)
        fig_fuel = px.pie(
            fleet_df,
            names="fuel_propulsion",
            hole=0.45,
            template="plotly_dark",
            color_discrete_sequence=["#34d399", "#38bdf8", "#fbbf24", "#818cf8"],
            height=300
        )
        fig_fuel.update_layout(paper_bgcolor="#090d16", plot_bgcolor="#090d16")
        st.plotly_chart(fig_fuel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
            <div class="console-card">
                <div class="card-title">Punctuality Classification</div>
                <div class="card-subtitle">Schedule variance distribution across completed trips</div>
        """, unsafe_allow_html=True)
        delay_counts = delay_df["delay_category"].value_counts().reset_index()
        delay_counts.columns = ["Category", "Trips"]
        fig_del = px.bar(
            delay_counts,
            x="Category",
            y="Trips",
            color="Category",
            template="plotly_dark",
            color_discrete_map={
                "Early / On-Time": "#34d399",
                "Acceptable (1-5m)": "#38bdf8",
                "Moderate Delay (6-15m)": "#fbbf24",
                "Severe Delay (>15m)": "#ef4444",
                "Cancelled": "#64748b"
            },
            height=300
        )
        fig_del.update_layout(paper_bgcolor="#090d16", plot_bgcolor="#090d16", showlegend=False)
        st.plotly_chart(fig_del, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="console-card">
            <div class="card-title">Real-Time Dispatch Lifecycle Manager</div>
            <div class="card-subtitle">Update operational trip lifecycle states and record schedule deviations</div>
    """, unsafe_allow_html=True)
    
    trips_list = execute_query("""
        SELECT trip_id, trip_code, route_id, trip_status, scheduled_departure, delay_minutes 
        FROM trips 
        ORDER BY scheduled_departure DESC 
        LIMIT 20
    """)
    trip_opts = {
        f"[{t['trip_code']}] Current Status: {t['trip_status']} (Delay: {t['delay_minutes']}m)": t
        for t in trips_list
    }
    
    sel_t_label = st.selectbox("Select Scheduled Trip:", list(trip_opts.keys()))
    sel_t = trip_opts[sel_t_label]

    c_stat, c_del, c_btn = st.columns([4, 4, 3])
    with c_stat:
        new_stat = st.selectbox("Target State:", ["Scheduled", "In-Transit", "Completed", "Delayed", "Cancelled"])
    with c_del:
        new_delay = st.slider("Recorded Delay (Minutes):", -5, 60, sel_t["delay_minutes"])
    with c_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Update Dispatch Record", type="primary", use_container_width=True):
            d_res = TransitService.update_trip_status(sel_t["trip_id"], new_stat, new_delay)
            if d_res["success"]:
                st.success(d_res["message"])
            else:
                st.error(d_res["message"])
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 6. TECHNICAL LAB
# ==============================================================================
elif menu == "Technical Lab":
    st.markdown("""
        <div class="console-card">
            <div class="card-title">DP-900 Relational Modeling & Technical Lab</div>
            <div class="card-subtitle">Interactive SQL query execution, Third Normal Form normalization proofs, and data quality governance</div>
    """, unsafe_allow_html=True)

    tab_sql, tab_erd, tab_audit = st.tabs(["SQL Query Console", "Relational Architecture (3NF)", "Data Governance & Cloud Export"])

    with tab_sql:
        st.markdown("#### Interactive SQL Execution Console")
        st.write("Execute benchmark analytical queries against the database and view execution latency.")
        
        sample_queries = {
            "Route Commercial Efficiency with Revenue per Km (CTE)": """
                WITH RouteTripStats AS (
                    SELECT r.route_id, r.route_code, r.route_name, r.distance_km,
                           COUNT(DISTINCT t.trip_id) AS trips_count
                    FROM routes r JOIN trips t ON r.route_id = t.route_id
                    WHERE t.trip_status = 'Completed'
                    GROUP BY r.route_id
                )
                SELECT s.route_code, s.route_name, s.distance_km, s.trips_count,
                       COUNT(pf.transaction_id) AS total_passengers,
                       ROUND(SUM(pf.fare_paid), 2) AS total_revenue,
                       ROUND(SUM(pf.fare_paid) / NULLIF(s.distance_km * s.trips_count, 0), 2) AS rev_per_km
                FROM RouteTripStats s
                JOIN trips t ON s.route_id = t.route_id
                JOIN passenger_fares pf ON t.trip_id = pf.trip_id
                GROUP BY s.route_code, s.route_name, s.distance_km, s.trips_count
                ORDER BY total_revenue DESC LIMIT 5;
            """,
            "Cumulative Intra-Day Revenue Progression (Window Function)": """
                SELECT 
                    DATE(boarding_timestamp) AS travel_date,
                    strftime('%H', boarding_timestamp) AS hour,
                    COUNT(*) AS riders,
                    ROUND(SUM(fare_paid), 2) AS hourly_revenue,
                    ROUND(SUM(SUM(fare_paid)) OVER (
                        PARTITION BY DATE(boarding_timestamp) 
                        ORDER BY strftime('%H', boarding_timestamp)
                    ), 2) AS cumulative_revenue
                FROM passenger_fares
                WHERE transaction_status = 'Success'
                GROUP BY travel_date, hour
                ORDER BY travel_date DESC, hour ASC
                LIMIT 12;
            """
        }
        
        chosen_sample = st.selectbox("Benchmark Query Selection:", list(sample_queries.keys()))
        sql_input = st.text_area("SQL Command Buffer:", value=sample_queries[chosen_sample].strip(), height=150)
        
        if st.button("Execute Query", type="primary"):
            t_start = datetime.now()
            try:
                res_rows = execute_query(sql_input)
                elapsed_ms = (datetime.now() - t_start).total_seconds() * 1000
                st.success(f"Execution completed in {elapsed_ms:.2f} ms ({len(res_rows)} rows returned).")
                if res_rows:
                    st.dataframe(pd.DataFrame(res_rows), use_container_width=True)
            except Exception as e:
                st.error(f"SQL Execution Error: {str(e)}")

    with tab_erd:
        st.markdown("#### Third Normal Form (3NF) Normalization Model")
        st.markdown("""
        - **First Normal Form (1NF):** Scalar atomic attribute domains; no composite arrays or repeating groups.
        - **Second Normal Form (2NF):** Full functional dependency on primary keys. Many-to-many relationship between routes and stops decoupled into `route_segments`.
        - **Third Normal Form (3NF):** Elimination of transitive functional dependencies ($X \\rightarrow Y, Y \\rightarrow Z$). Station infrastructure isolated in `stops`, vehicle properties isolated in `vehicles`.
        - Refer to **[documentation/ERD_DIAGRAM.md](file:///c:/Users/ARYAN/Desktop/DPAS/documentation/ERD_DIAGRAM.md)** for mathematical normalization proofs.
        """)

    with tab_audit:
        st.markdown("#### Automated Data Governance & Cloud Staging")
        audit = run_data_quality_audit()
        
        col_s1, col_s2 = st.columns([3, 7])
        with col_s1:
            st.metric("Data Quality Score", f"{audit['quality_score']}%", delta="100% Target")
        with col_s2:
            st.write(f"Passed **{audit['passed_checks']} of {audit['total_checks']}** validation checks (zero orphan records, zero negative fares).")
        
        st.markdown("---")
        c_exp, c_seed = st.columns(2)
        with c_exp:
            if st.button("Export Datasets to CSV (Data Lake Staging)", use_container_width=True):
                files = export_tables_to_csv()
                st.success(f"Exported {len(files)} CSV files into `/data` directory.")
        with c_seed:
            if st.button("Re-Seed Production Database", use_container_width=True):
                generate_and_seed_data()
                st.success("Re-seeded with 160 operational trips and 2,200 transactions.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
