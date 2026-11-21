"""
TransitIQ: Public Transit Operations & Analytics Platform
Minimalist Monochrome Black & White Theme (Linear / Vercel Aesthetic)
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
    page_title="TransitIQ",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimalist Monochrome Black & White Theme (Clean, Precision Engineered)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');
    
    /* Typography: Explicitly avoid generic 'span' and 'div' to protect icon ligatures */
    html, body, p, h1, h2, h3, h4, h5, h6, label, div[data-testid="stMarkdownContainer"] p {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    /* Protect Material Symbols icons from font override */
    .material-symbols-rounded,
    .material-symbols-outlined,
    [data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapseButton"] span,
    header span,
    button span {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
        font-weight: normal !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* Clean Streamlit Header Clutter (Removes Deploy button & broken theme switcher menu) */
    .stAppDeployButton {
        display: none !important;
    }
    #MainMenu {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Backgrounds */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid #1a1a1a !important;
    }
    
    /* Global Container Spacing */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 95% !important;
    }

    /* Minimalist Navigation in Sidebar (SaaS Button Aesthetic) */
    div[data-testid="stRadio"] [role="radiogroup"] {
        gap: 4px !important;
    }
    /* Hide ONLY the radio circle (ex50key4) and native radio input - NEVER touch the text */
    .ex50key4,
    div[data-testid="stRadio"] [data-testid="stRadioOption"] .ex50key4,
    div[data-testid="stRadio"] [data-testid="stRadioOption"] > div > div:first-child,
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        opacity: 0 !important;
    }

    /* Style the navigation buttons cleanly */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] [data-testid="stRadioOption"] {
        background: #111115 !important;
        border: 1px solid #222227 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin-bottom: 4px !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        width: 100% !important;
        display: block !important;
    }
    div[data-testid="stRadio"] label:hover,
    div[data-testid="stRadio"] [data-testid="stRadioOption"]:hover {
        background: #18181f !important;
        border-color: #3f3f46 !important;
    }

    /* Selected Active Page (Bold White Pill) */
    div[data-testid="stRadio"] label:has(input:checked),
    div[data-testid="stRadio"] [data-testid="stRadioOption"]:has(input:checked),
    div[data-testid="stRadio"] [data-testid="stRadioOption"][aria-checked="true"] {
        background: #ffffff !important;
        border: 1px solid #ffffff !important;
    }

    /* Ensure Navigation Labels are ALWAYS 100% visible with crisp typography */
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"],
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p,
    div[data-testid="stRadio"] label p {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        color: #a1a1aa !important;
        margin: 0 !important;
        letter-spacing: -0.01em !important;
    }

    div[data-testid="stRadio"] label:has(input:checked) [data-testid="stMarkdownContainer"] p,
    div[data-testid="stRadio"] [data-testid="stRadioOption"]:has(input:checked) [data-testid="stMarkdownContainer"] p,
    div[data-testid="stRadio"] [data-testid="stRadioOption"][aria-checked="true"] [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* Minimal Header */
    .header-box {
        border-bottom: 1px solid #1a1a1a;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #ffffff;
        margin: 0;
    }
    .header-subtitle {
        font-size: 0.82rem;
        color: #71717a;
        margin-top: 0.2rem;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: #0d0d12 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 1rem 1.2rem !important;
        box-shadow: 0 4px 14px -2px rgba(0, 0, 0, 0.3) !important;
    }
    div[data-testid="stMetric"]:hover {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 0.72rem !important;
        color: #8b8b96 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }
    div[data-testid="stMetricValue"] div {
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
    }

    /* Form Inputs & Selectboxes */
    label[data-testid="stWidgetLabel"] p {
        font-size: 0.74rem !important;
        font-weight: 600 !important;
        color: #8b8b96 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        margin-bottom: 6px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #121217 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        min-height: 44px !important;
        padding: 2px 8px !important;
        transition: all 0.15s ease !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(255, 255, 255, 0.25) !important;
        background-color: #16161c !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 1px #ffffff !important;
    }

    /* Minimal High-End Buttons */
    div.stButton > button {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.4rem !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        letter-spacing: -0.01em !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 4px 14px rgba(255, 255, 255, 0.12) !important;
    }
    div.stButton > button:hover {
        background: #e4e4e7 !important;
        border-color: #e4e4e7 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.22) !important;
    }
    div.stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Custom Container Framing */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        background-color: #0d0d12 !important;
        box-shadow: 0 4px 24px -2px rgba(0, 0, 0, 0.4) !important;
        padding: 0.6rem !important;
    }

    /* Badges */
    .mono-badge {
        display: inline-block;
        padding: 3px 9px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background: #14141a;
        color: #d4d4d8;
        font-size: 0.7rem;
        font-weight: 600;
        border-radius: 4px;
        letter-spacing: 0.04em;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #ffffff !important;
    }
    .stProgress > div > div > div {
        background-color: #22222a !important;
        border-radius: 4px !important;
    }
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
NAV_PAGES = [
    "Operations Dashboard",
    "Ticketing Operations",
    "Transit Corridors",
    "Passenger Demand",
    "Fleet Management",
    "Database & Architecture"
]

if "nav_radio_selection" not in st.session_state:
    st.session_state["nav_radio_selection"] = "Operations Dashboard"

with st.sidebar:
    st.markdown("""
        <div style="padding: 0.6rem 0.2rem 1rem 0.2rem; border-bottom: 1px solid #1f1f23; margin-bottom: 0.8rem;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 26px; height: 26px; background: #ffffff; color: #000000; font-weight: 900; font-size: 11px; border-radius: 4px; display: flex; align-items: center; justify-content: center;">TQ</div>
                <div>
                    <div style="font-size: 0.9rem; font-weight: 700; letter-spacing: 0.08em; color: #ffffff;">TRANSITIQ</div>
                    <div style="font-size: 0.7rem; color: #71717a;">Operations &amp; Analytics</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        NAV_PAGES,
        key="nav_radio_selection",
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(f"""
        <div style="font-size: 0.72rem; color: #71717a; line-height: 1.6;">
            <div><b>System Engine:</b> {DB_DIALECT.upper()}</div>
            <div><b>Architecture:</b> 3NF Relational Model</div>
            <div><b>Workload:</b> OLTP / OLAP Dual-Mode</div>
            <div><b>Standard:</b> Microsoft DP-900</div>
        </div>
    """, unsafe_allow_html=True)

# Top Header with dynamic breadcrumb & quick back-to-dashboard button
col_head1, col_head2 = st.columns([8, 4])
with col_head1:
    st.markdown(f"""
        <div class="header-box">
            <h1 class="header-title">TransitIQ: {menu}</h1>
            <div class="header-subtitle">Metropolitan Public Transit Network Operations, Capacity Monitoring & Data Analytics</div>
        </div>
    """, unsafe_allow_html=True)
with col_head2:
    if menu != "Operations Dashboard":
        if st.button("Go to Operations Dashboard", use_container_width=True):
            st.session_state["nav_radio_selection"] = "Operations Dashboard"
            st.rerun()
    else:
        st.markdown("""
            <div style="text-align: right; padding-top: 0.5rem;">
                <span class="mono-badge">SYSTEM OPERATIONAL &bull; 160 TRIPS</span>
            </div>
        """, unsafe_allow_html=True)

# Helper Function: Generate Clean Monochrome Transit Network Vector Map
def render_monochrome_network_map():
    segments = execute_query("""
        SELECT 
            rs.route_id,
            r.route_code,
            r.route_name,
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

    # Route Line Shading in Minimalist Grayscale Tones
    route_styles = {
        "M-RED": ("#ffffff", 3.0),
        "M-BLUE": ("#d4d4d8", 2.5),
        "BRT-101": ("#a1a1aa", 2.0),
        "BRT-102": ("#71717a", 2.0),
        "EXP-500": ("#e4e4e7", 2.0),
        "CR-10": ("#52525b", 1.8)
    }

    routes_grouped = {}
    for seg in segments:
        code = seg["route_code"]
        if code not in routes_grouped:
            routes_grouped[code] = {"name": seg["route_name"], "lats": [], "lons": []}
        routes_grouped[code]["lats"].append(seg["latitude"])
        routes_grouped[code]["lons"].append(seg["longitude"])

    for code, data in routes_grouped.items():
        color, width = route_styles.get(code, ("#71717a", 2.0))
        fig.add_trace(go.Scatter(
            x=data["lons"],
            y=data["lats"],
            mode="lines",
            name=f"{code} {data['name']}",
            line=dict(color=color, width=width),
            hoverinfo="name"
        ))

    # Station Markers
    fig.add_trace(go.Scatter(
        x=stop_stats["longitude"],
        y=stop_stats["latitude"],
        mode="markers+text",
        name="Stations",
        text=stop_stats["stop_name"],
        textposition="top center",
        textfont=dict(color="#ffffff", size=9),
        marker=dict(
            size=stop_stats["total_footfall"].apply(lambda x: min(16, max(6, x / 15))),
            color="#ffffff",
            line=dict(width=1, color="#000000")
        ),
        hovertemplate="<b>%{text}</b><br>Footfall: %{customdata[0]}<br>Boardings: %{customdata[1]}<br>Alightings: %{customdata[2]}<extra></extra>",
        customdata=stop_stats[["total_footfall", "total_boardings", "total_alightings"]].values
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#09090b",
        plot_bgcolor="#09090b",
        margin=dict(l=15, r=15, t=15, b=15),
        height=360,
        xaxis=dict(title="Longitude (°E)", showgrid=True, gridcolor="#1a1a1a", zeroline=False, color="#71717a"),
        yaxis=dict(title="Latitude (°N)", showgrid=True, gridcolor="#1a1a1a", zeroline=False, color="#71717a"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9, color="#a1a1aa"))
    )
    return fig

# ==============================================================================
# 1. OPERATIONS DASHBOARD (MAIN OVERVIEW)
# ==============================================================================
if menu in ["Operations Dashboard", "Overview"]:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Active Corridors", f"{kpis.get('active_routes', 6)} Lines")
    with c2:
        st.metric("On-Time Performance", f"{kpis.get('on_time_performance_pct', 94.0)}%")
    with c3:
        st.metric("Total Ridership", f"{kpis.get('total_passengers', 2200):,}")
    with c4:
        st.metric("Total Fare Revenue", f"₹{kpis.get('total_revenue', 0.0):,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    col_map, col_chart = st.columns([6, 5])
    with col_map:
        with st.container(border=True):
            st.markdown("##### Transit Network Topology")
            st.caption("Active route alignments and station hubs sized by passenger footfall")
            st.plotly_chart(render_monochrome_network_map(), use_container_width=True)

    with col_chart:
        with st.container(border=True):
            st.markdown("##### Route Commercial Performance")
            st.caption("Total revenue generated across individual transit corridors")
            route_df = get_route_performance_df()
            
            fig_rev = px.bar(
                route_df,
                x="total_revenue",
                y="route_name",
                orientation="h",
                color="total_revenue",
                color_continuous_scale=["#3f3f46", "#71717a", "#d4d4d8", "#ffffff"],
                template="plotly_dark",
                height=360
            )
            fig_rev.update_layout(
                paper_bgcolor="#09090b",
                plot_bgcolor="#09090b",
                xaxis=dict(title="Revenue (₹)", showgrid=True, gridcolor="#1a1a1a"),
                yaxis=dict(title="", showgrid=False),
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_rev, use_container_width=True)

    # Route Table
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("##### Fleet Corridors Summary")
        st.dataframe(
            route_df[["route_code", "route_name", "route_type", "distance_km", "total_trips", "completed_trips", "on_time_percentage", "total_passengers", "total_revenue"]].rename(columns={
                "route_code": "Code",
                "route_name": "Corridor Name",
                "route_type": "Mode",
                "distance_km": "Distance (km)",
                "total_trips": "Trips",
                "completed_trips": "Completed",
                "on_time_percentage": "On-Time %",
                "total_passengers": "Passengers",
                "total_revenue": "Revenue (₹)"
            }),
            use_container_width=True,
            hide_index=True
        )

# ==============================================================================
# 2. TICKETING OPERATIONS (HIGH-END MINIMAL TERMINAL)
# ==============================================================================
elif menu == "Ticketing Operations":
    bookable = TransitService.get_bookable_trips()
    
    if not bookable:
        st.warning("No active trips scheduled. Please re-seed data in the Database section.")
    else:
        def format_trip_label(t):
            dep_raw = str(t['scheduled_departure'])
            time_str = dep_raw.split(' ')[1][:5] if ' ' in dep_raw else dep_raw[:5]
            return f"{t['route_name']} • {time_str} ({t['vehicle_code']})"

        trip_map = {format_trip_label(t): t for t in bookable}

        col_form, col_summary = st.columns([1, 1], gap="large")

        with col_form:
            with st.container(border=True):
                st.markdown("""
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.2rem; padding-bottom: 0.8rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <div>
                            <div style="font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em; color: #8b8b96; text-transform: uppercase;">Ticketing Terminal</div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-top: 2px;">Issue Passenger Ticket</div>
                        </div>
                        <span class="mono-badge">ACID PROTOCOL</span>
                    </div>
                """, unsafe_allow_html=True)

                selected_trip_label = st.selectbox("Scheduled Transit Service", list(trip_map.keys()))
                trip_data = trip_map[selected_trip_label]
                trip_stops = TransitService.get_stops_for_trip(trip_data["trip_id"])

                orig_opts = {s['stop_name']: s['stop_id'] for s in trip_stops[:-1]}
                dest_opts = {s['stop_name']: s['stop_id'] for s in trip_stops[1:]}

                c_orig, c_dest = st.columns(2, gap="medium")
                with c_orig:
                    sel_orig_name = st.selectbox("Origin Station", list(orig_opts.keys()))
                    sel_orig_id = orig_opts[sel_orig_name]

                with c_dest:
                    sel_dest_name = st.selectbox("Destination Station", list(dest_opts.keys()))
                    sel_dest_id = dest_opts[sel_dest_name]

                passenger_map = {
                    "Standard Adult": "Standard Adult",
                    "Student (50% Off)": "Student",
                    "Senior Citizen (60% Off)": "Senior Citizen",
                    "Commuter Pass (30% Off)": "Commuter Passholder"
                }

                payment_map = {
                    "Transit Smartcard (NFC)": "Transit Smartcard",
                    "Mobile UPI / QR": "Mobile QR / UPI",
                    "Contactless EMV": "Contactless EMV",
                    "Cash Station Counter": "Ticket Counter"
                }

                c_cat, c_pay = st.columns(2, gap="medium")
                with c_cat:
                    passenger_cat_label = st.selectbox(
                        "Passenger Category",
                        list(passenger_map.keys())
                    )
                    cat_clean = passenger_map[passenger_cat_label]

                with c_pay:
                    pay_method_label = st.selectbox(
                        "Payment Channel",
                        list(payment_map.keys())
                    )
                    pay_method = payment_map[pay_method_label]

                st.markdown("<br>", unsafe_allow_html=True)
                book_clicked = st.button("Confirm and Issue Ticket →", use_container_width=True)

        # Dynamic Pre-Booking Calculation
        base_fare = trip_data["base_fare"]
        discount_map = {"Standard Adult": 1.0, "Student": 0.50, "Senior Citizen": 0.40, "Commuter Passholder": 0.70}
        discount_rate = discount_map.get(cat_clean, 1.0)
        final_fare = round(base_fare * discount_rate, 2)
        discount_amt = round(base_fare - final_fare, 2)
        occupancy_pct = min(100.0, round((trip_data["booked_passengers"] / trip_data["capacity"]) * 100, 1))

        with col_summary:
            with st.container(border=True):
                st.markdown("""
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.2rem; padding-bottom: 0.8rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <div>
                            <div style="font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em; color: #8b8b96; text-transform: uppercase;">Real-Time Fare &amp; Inventory</div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-top: 2px;">Pre-Booking Verification</div>
                        </div>
                        <span class="mono-badge">LIVE CALCULATION</span>
                    </div>
                """, unsafe_allow_html=True)

                m1, m2 = st.columns(2, gap="medium")
                with m1:
                    st.metric("Base Corridor Fare", f"₹{base_fare:.2f}")
                with m2:
                    st.metric("Concession Discount", f"-₹{discount_amt:.2f}")

                st.markdown("<br>", unsafe_allow_html=True)
                st.metric("Total Payable Amount", f"₹{final_fare:.2f}")

                st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 1rem 0;'>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="font-size: 0.82rem; color: #d4d4d8; line-height: 1.8;">
                        <div><span style="color: #8b8b96;">Transit Corridor:</span> <b>{trip_data['route_name']}</b></div>
                        <div><span style="color: #8b8b96;">Vehicle Unit:</span> <b>{trip_data['vehicle_code']}</b> ({trip_data['capacity']} seat capacity)</div>
                        <div><span style="color: #8b8b96;">Occupancy Load:</span> <b>{trip_data['booked_passengers']} / {trip_data['capacity']} booked ({occupancy_pct}%)</b></div>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(occupancy_pct / 100.0)

        # Transaction Execution & Verified Boarding Pass Card
        if book_clicked:
            res = TransitService.book_ticket(
                trip_id=trip_data["trip_id"],
                origin_stop_id=sel_orig_id,
                destination_stop_id=sel_dest_id,
                passenger_type=cat_clean,
                payment_method=pay_method
            )

            if res["success"]:
                st.markdown("<br>", unsafe_allow_html=True)
                st.success("Transaction committed successfully to relational database under ACID protocol.")
                
                with st.container(border=True):
                    st.markdown(f"""
                        <div style="background: #08080a; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 1.4rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(255,255,255,0.15); padding-bottom: 0.9rem; margin-bottom: 1rem;">
                                <div>
                                    <div style="font-size: 0.85rem; font-weight: 800; letter-spacing: 0.12em; color: #ffffff;">TRANSITIQ BOARDING PASS</div>
                                    <div style="font-size: 0.68rem; color: #8b8b96;">METROPOLITAN TRANSIT AUTHORITY &bull; VERIFIED FARE RECEIPT</div>
                                </div>
                                <span style="background: #ffffff; color: #000000; font-size: 0.7rem; font-weight: 800; padding: 4px 10px; border-radius: 4px; font-family: monospace;">CONFIRMED</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
                                <div>
                                    <div style="font-size: 0.68rem; color: #8b8b96; text-transform: uppercase; letter-spacing: 0.05em;">Origin Station</div>
                                    <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 2px;">{sel_orig_name}</div>
                                </div>
                                <div style="font-size: 1.3rem; color: #8b8b96;">&rarr;</div>
                                <div style="text-align: right;">
                                    <div style="font-size: 0.68rem; color: #8b8b96; text-transform: uppercase; letter-spacing: 0.05em;">Destination Station</div>
                                    <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 2px;">{sel_dest_name}</div>
                                </div>
                            </div>
                            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; font-size: 0.78rem; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 1rem; margin-bottom: 1rem;">
                                <div>
                                    <div style="color: #8b8b96; font-size: 0.68rem; text-transform: uppercase;">Ticket Ref</div>
                                    <div style="color: #ffffff; font-family: monospace; font-weight: 700; margin-top: 2px;">{res['ticket_reference']}</div>
                                </div>
                                <div>
                                    <div style="color: #8b8b96; font-size: 0.68rem; text-transform: uppercase;">Category</div>
                                    <div style="color: #ffffff; font-weight: 600; margin-top: 2px;">{res['passenger_type']}</div>
                                </div>
                                <div>
                                    <div style="color: #8b8b96; font-size: 0.68rem; text-transform: uppercase;">Service Run</div>
                                    <div style="color: #ffffff; font-family: monospace; margin-top: 2px;">{trip_data['trip_code']}</div>
                                </div>
                                <div>
                                    <div style="color: #8b8b96; font-size: 0.68rem; text-transform: uppercase;">Payment</div>
                                    <div style="color: #ffffff; margin-top: 2px;">{res['payment_method']}</div>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px dashed rgba(255,255,255,0.15); padding-top: 1rem;">
                                <div>
                                    <div style="font-size: 0.68rem; color: #8b8b96; text-transform: uppercase; letter-spacing: 0.05em;">Total Fare Paid</div>
                                    <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff;">₹{res['fare_paid']:.2f}</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-family: monospace; font-size: 0.75rem; color: #52525b; letter-spacing: 3px;">|||| | ||| || |||| | ||</div>
                                    <div style="font-size: 0.62rem; color: #71717a; margin-top: 3px;">ATOMIC INVENTORY DEDUCTED</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(f"Transaction Rejected: {res['message']}")

# ==============================================================================
# 3. TRANSIT CORRIDORS
# ==============================================================================
elif menu == "Transit Corridors":
    with st.container(border=True):
        st.markdown("##### Transit Corridor Alignment & Station Sequence")
        st.caption("Sequential station alignments, inter-station distances, and travel times")

        routes = execute_query("SELECT route_id, route_code, route_name, route_type, distance_km, base_fare FROM routes ORDER BY route_id")
        route_choices = {f"{r['route_code']} - {r['route_name']} ({r['route_type']})": r for r in routes}
        
        selected_name = st.selectbox("Select Corridor", list(route_choices.keys()))
        sel_route = route_choices[selected_name]

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Mode of Transit", sel_route["route_type"])
        with c2:
            st.metric("Corridor Distance", f"{sel_route['distance_km']} km")
        with c3:
            st.metric("Base Adult Fare", f"₹{sel_route['base_fare']:.2f}")
        with c4:
            st.metric("Operational Status", "Active Service")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### Station Sequence")

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

        df_seg = pd.DataFrame(segments)
        df_seg["Accessibility"] = df_seg["wheelchair_accessible"].apply(lambda x: "Elevator & Tactile" if x else "Standard Stairs")
        st.dataframe(
            df_seg[["stop_sequence", "stop_name", "zone_id", "distance_from_start_km", "est_travel_time_min", "Accessibility"]].rename(columns={
                "stop_sequence": "Sequence",
                "stop_name": "Station Hub",
                "zone_id": "Fare Zone",
                "distance_from_start_km": "Distance from Start (km)",
                "est_travel_time_min": "Travel Time (min)"
            }),
            use_container_width=True,
            hide_index=True
        )

# ==============================================================================
# 4. PASSENGER DEMAND
# ==============================================================================
elif menu == "Passenger Demand":
    hourly_df = get_hourly_ridership_df()
    payment_df = get_payment_breakdown()

    col_rush, col_pie = st.columns([7, 4])
    with col_rush:
        with st.container(border=True):
            st.markdown("##### Hourly Passenger Volume (24-Hour Cycle)")
            st.caption("Crowding distribution across morning (08:00–10:00) and evening (17:00–19:00) peaks")
            
            fig_rush = px.area(
                hourly_df,
                x="hour_of_day",
                y="passenger_count",
                color="route_type",
                labels={"hour_of_day": "Hour of Day", "passenger_count": "Boardings"},
                color_discrete_sequence=["#ffffff", "#a1a1aa", "#71717a", "#52525b"],
                template="plotly_dark",
                height=340
            )
            fig_rush.update_layout(
                paper_bgcolor="#09090b",
                plot_bgcolor="#09090b",
                xaxis=dict(showgrid=True, gridcolor="#1a1a1a"),
                yaxis=dict(showgrid=True, gridcolor="#1a1a1a")
            )
            st.plotly_chart(fig_rush, use_container_width=True)

    with col_pie:
        with st.container(border=True):
            st.markdown("##### Payment Channels")
            st.caption("Distribution across ticketing methods")
            pay_totals = payment_df.groupby("payment_method")["transaction_count"].sum().reset_index()
            fig_pay = px.pie(
                pay_totals,
                names="payment_method",
                values="transaction_count",
                hole=0.45,
                template="plotly_dark",
                color_discrete_sequence=["#ffffff", "#d4d4d8", "#a1a1aa", "#52525b"],
                height=340
            )
            fig_pay.update_layout(paper_bgcolor="#09090b", plot_bgcolor="#09090b")
            fig_pay.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pay, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_demo, col_busiest = st.columns(2)
    with col_demo:
        with st.container(border=True):
            st.markdown("##### Passenger Demographic Classifications")
            demo_totals = payment_df.groupby("passenger_type")["transaction_count"].sum().reset_index()
            fig_demo = px.bar(
                demo_totals,
                x="passenger_type",
                y="transaction_count",
                template="plotly_dark",
                color_discrete_sequence=["#ffffff"],
                height=260
            )
            fig_demo.update_layout(paper_bgcolor="#09090b", plot_bgcolor="#09090b", xaxis_title="", yaxis_title="Tickets")
            st.plotly_chart(fig_demo, use_container_width=True)

    with col_busiest:
        with st.container(border=True):
            st.markdown("##### Top 5 Busiest Station Hubs")
            stop_df = get_stop_demand_df().head(5)
            fig_stops = px.bar(
                stop_df,
                x="stop_name",
                y="total_footfall",
                template="plotly_dark",
                color_discrete_sequence=["#d4d4d8"],
                height=260
            )
            fig_stops.update_layout(paper_bgcolor="#09090b", plot_bgcolor="#09090b", xaxis_title="", yaxis_title="Footfall")
            st.plotly_chart(fig_stops, use_container_width=True)

# ==============================================================================
# 5. FLEET MANAGEMENT
# ==============================================================================
elif menu == "Fleet Management":
    fleet_df = get_fleet_utilization_df()
    delay_df = get_delay_monitoring_df()

    col_f1, col_f2 = st.columns([6, 5])
    with col_f1:
        with st.container(border=True):
            st.markdown("##### Fleet Clean Propulsion Share")
            fig_fuel = px.pie(
                fleet_df,
                names="fuel_propulsion",
                hole=0.45,
                template="plotly_dark",
                color_discrete_sequence=["#ffffff", "#d4d4d8", "#a1a1aa", "#52525b"],
                height=300
            )
            fig_fuel.update_layout(paper_bgcolor="#09090b", plot_bgcolor="#09090b")
            st.plotly_chart(fig_fuel, use_container_width=True)

    with col_f2:
        with st.container(border=True):
            st.markdown("##### Schedule Punctuality Distribution")
            delay_counts = delay_df["delay_category"].value_counts().reset_index()
            delay_counts.columns = ["Category", "Trips"]
            fig_del = px.bar(
                delay_counts,
                x="Category",
                y="Trips",
                template="plotly_dark",
                color_discrete_sequence=["#ffffff"],
                height=300
            )
            fig_del.update_layout(paper_bgcolor="#09090b", plot_bgcolor="#09090b", xaxis_title="", yaxis_title="Trips")
            st.plotly_chart(fig_del, use_container_width=True)

    # Dispatch Controller
    with st.container(border=True):
        st.markdown("##### Operational Dispatch State Machine")
        st.caption("Update active operational states and record schedule deviations")
        
        trips_list = execute_query("""
            SELECT trip_id, trip_code, route_id, trip_status, scheduled_departure, delay_minutes 
            FROM trips 
            ORDER BY scheduled_departure DESC 
            LIMIT 20
        """)
        trip_opts = {
            f"{t['trip_code']} | Current Status: {t['trip_status']} (Delay: {t['delay_minutes']}m)": t
            for t in trips_list
        }
        
        sel_t_label = st.selectbox("Active Service Run", list(trip_opts.keys()))
        sel_t = trip_opts[sel_t_label]

        c_stat, c_del, c_btn = st.columns([4, 4, 3])
        with c_stat:
            new_stat = st.selectbox("Target State", ["Scheduled", "In-Transit", "Completed", "Delayed", "Cancelled"])
        with c_del:
            new_delay = st.slider("Recorded Delay (Minutes)", -5, 60, sel_t["delay_minutes"])
        with c_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Update Dispatch Record", use_container_width=True):
                d_res = TransitService.update_trip_status(sel_t["trip_id"], new_stat, new_delay)
                if d_res["success"]:
                    st.success(d_res["message"])
                else:
                    st.error(d_res["message"])

# ==============================================================================
# 6. DATABASE & ARCHITECTURE
# ==============================================================================
elif menu == "Database & Architecture":
    with st.container(border=True):
        st.markdown("##### DP-900 Relational Modeling & Technical Lab")
        st.caption("Interactive SQL query execution, Third Normal Form normalization proofs, and data quality governance")

        tab_sql, tab_erd, tab_audit = st.tabs(["SQL Query Console", "Relational Architecture (3NF)", "Data Governance & Cloud Export"])

        with tab_sql:
            st.markdown("##### Interactive SQL Execution")
            st.caption("Execute benchmark analytical queries against the database and evaluate query latency")
            
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
            
            chosen_sample = st.selectbox("Benchmark Query Selection", list(sample_queries.keys()))
            sql_input = st.text_area("SQL Command Buffer", value=sample_queries[chosen_sample].strip(), height=150)
            
            if st.button("Execute Query", use_container_width=True):
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
            st.markdown("##### Third Normal Form (3NF) Normalization Architecture")
            st.write("""
            - **First Normal Form (1NF):** Scalar atomic attribute domains; no composite arrays or repeating groups.
            - **Second Normal Form (2NF):** Full functional dependency on primary keys. Many-to-many relationship between routes and stops decoupled into `route_segments`.
            - **Third Normal Form (3NF):** Elimination of transitive functional dependencies ($X \\rightarrow Y, Y \\rightarrow Z$). Station infrastructure isolated in `stops`, vehicle properties isolated in `vehicles`.
            - Refer to `documentation/ERD_DIAGRAM.md` for mathematical normalization proofs.
            """)

        with tab_audit:
            st.markdown("##### Automated Data Governance & Cloud Staging")
            audit = run_data_quality_audit()
            
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Data Quality Score", f"{audit['quality_score']}%")
            with m2:
                st.metric("Integrity Checks Passed", f"{audit['passed_checks']} / {audit['total_checks']}")

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
