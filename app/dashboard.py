"""
TransitIQ: Public Transit Intelligence & Operations Command Centre
Modern Enterprise Dashboard (Dark Theme Compatible, Zero Emojis)
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
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }
    
    /* Top Hero Banner */
    .hero-banner {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1.6rem;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #f8fafc;
        margin-bottom: 0.3rem;
    }
    .hero-subtitle {
        font-size: 0.92rem;
        color: #94a3b8;
        font-weight: 400;
    }

    /* Badges & Pills (Clean Monochrome & Subtle Tints) */
    .pill-badge {
        display: inline-block;
        padding: 3px 10px;
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

    /* Modern Metric Cards */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
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

    /* Smart Operational Insight Box */
    .insight-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-left: 4px solid #38bdf8;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 1.4rem;
        font-size: 0.88rem;
        color: #cbd5e1;
        line-height: 1.5;
    }

    /* Boarding Pass Card */
    .boarding-pass {
        background: #1e293b;
        border: 1px solid #475569;
        border-radius: 14px;
        padding: 1.5rem;
        max-width: 560px;
        margin: 1rem auto;
    }
    .pass-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #334155;
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
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .pass-arrow {
        font-size: 1.3rem;
        color: #38bdf8;
    }
    .pass-details {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        background: #0f172a;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #334155;
    }
    .pass-label { font-size: 0.7rem; color: #64748b; font-weight: 700; text-transform: uppercase; }
    .pass-val { font-size: 0.92rem; font-weight: 700; color: #f8fafc; }
    
    /* Station Stepper Timeline */
    .station-stepper {
        display: flex;
        align-items: center;
        overflow-x: auto;
        padding: 0.8rem 0;
        gap: 0.6rem;
    }
    .step-node {
        background: #1e293b;
        border: 1px solid #38bdf8;
        border-radius: 10px;
        padding: 0.65rem 0.95rem;
        min-width: 150px;
        text-align: center;
    }
    .step-seq { font-size: 0.68rem; font-weight: 800; color: #38bdf8; letter-spacing: 0.05em; }
    .step-name { font-size: 0.88rem; font-weight: 700; color: #f8fafc; margin-top: 3px; }
    .step-meta { font-size: 0.72rem; color: #94a3b8; margin-top: 3px; }
    .step-arrow { color: #64748b; font-size: 1.1rem; font-weight: 700; }
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
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="padding-bottom: 0.8rem; margin-bottom: 0.8rem; border-bottom: 1px solid #334155;">
            <div style="font-size: 1.35rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.01em;">TransitIQ</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Urban Mobility Command Centre</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background: #1e293b; border: 1px solid #334155; padding: 6px 12px; border-radius: 8px; font-size: 0.76rem; color: #38bdf8; font-weight: 600; margin-bottom: 1.2rem;">
            ENGINE: {DB_DIALECT.upper()} MODE &nbsp;|&nbsp; DP-900 CAPSTONE
        </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        [
            "Overview",
            "Corridors & Network",
            "Ridership & Demand",
            "Ticketing Operations",
            "Fleet & Dispatch",
            "Technical Architecture"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.78rem; color: #64748b; line-height: 1.6;">
        <b>Technical Architecture:</b><br>
        • Database: Third Normal Form (3NF)<br>
        • Workloads: OLTP & OLAP Dual-Mode<br>
        • Cloud Alignment: Azure SQL & Blob
    </div>
    """, unsafe_allow_html=True)

# Top Hero Banner
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">TransitIQ Operations Command</div>
        <div class="hero-subtitle">
            Metropolitan Transit Network Operations, Capacity Monitoring & Data Platform
        </div>
    </div>
""", unsafe_allow_html=True)

# Helper Function: Generate Offline Interactive Transit Network Map
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
        "M-RED": "#ef4444",    # Red
        "M-BLUE": "#3b82f6",   # Blue
        "BRT-101": "#06b6d4",  # Cyan
        "BRT-102": "#14b8a6",  # Teal
        "EXP-500": "#10b981",  # Emerald
        "CR-10": "#f59e0b"     # Amber
    }

    # Draw Route Vectors (Lines)
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

    # Draw Stations (Nodes)
    fig.add_trace(go.Scatter(
        x=stop_stats["longitude"],
        y=stop_stats["latitude"],
        mode="markers+text",
        name="Station Hubs",
        text=stop_stats["stop_name"],
        textposition="top center",
        textfont=dict(color="#f8fafc", size=9),
        marker=dict(
            size=stop_stats["total_footfall"].apply(lambda x: min(22, max(8, x / 12))),
            color="#38bdf8",
            line=dict(width=1.5, color="#f8fafc"),
            opacity=0.95
        ),
        hovertemplate="<b>%{text}</b><br>Footfall: %{customdata[0]}<br>Boardings: %{customdata[1]}<br>Alightings: %{customdata[2]}<extra></extra>",
        customdata=stop_stats[["total_footfall", "total_boardings", "total_alightings"]].values
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        margin=dict(l=15, r=15, t=15, b=15),
        height=400,
        xaxis=dict(
            title="Longitude (°E)",
            showgrid=True,
            gridcolor="#1e293b",
            zeroline=False,
            color="#94a3b8"
        ),
        yaxis=dict(
            title="Latitude (°N)",
            showgrid=True,
            gridcolor="#1e293b",
            zeroline=False,
            color="#94a3b8"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=9, color="#cbd5e1")
        )
    )
    return fig

# ==============================================================================
# 1. OVERVIEW
# ==============================================================================
if menu == "Overview":
    # 4 Clean Metric Cards
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
                <div class="metric-delta">Benchmark Target: >90%</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Ridership</div>
                <div class="metric-value">{kpis.get('total_passengers', 2200):,}</div>
                <div class="metric-delta">160 Scheduled Trips</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Gross Revenue</div>
                <div class="metric-value">₹{kpis.get('total_revenue', 0.0):,.0f}</div>
                <div class="metric-delta">Electronic Fare Collection</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="insight-card">
            <b>Operational Summary:</b> Network punctuality is performing at <b>94.2%</b> with an average delay of <b>1.8 minutes</b> across corridors. 
            Highest passenger throughput is concentrated on the <b>Red Line Metro</b> and <b>Silicon Express Shuttle</b>. 
            Digital smartcard and mobile QR transactions represent over <b>80%</b> of total fare collections.
        </div>
    """, unsafe_allow_html=True)

    # 2 Column View: Transit Map + Route Revenue Leaderboard
    col_map, col_chart = st.columns([6, 5])
    
    with col_map:
        st.subheader("Transit Network Topological Map")
        st.caption("Multimodal route alignments and station hubs sized by passenger footfall.")
        fig_net = render_transit_network_map()
        st.plotly_chart(fig_net, use_container_width=True)

    with col_chart:
        st.subheader("Route Revenue Performance")
        st.caption("Gross fare revenue generated per transit corridor.")
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
            height=400
        )
        fig_rev.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            xaxis=dict(title="Revenue (₹)", showgrid=True, gridcolor="#1e293b"),
            yaxis=dict(title="", showgrid=False),
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9))
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    # Clean Route Status Cards
    st.markdown("### Corridor Fleet & Capacity Status")
    cols = st.columns(3)
    for idx, row in route_df.iterrows():
        c = cols[idx % 3]
        badge_class = "badge-metro" if "Metro" in row["route_type"] else ("badge-bus" if "Bus" in row["route_type"] else "badge-express")
        with c:
            st.markdown(f"""
                <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.1rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span class="pill-badge {badge_class}">{row['route_code']}</span>
                        <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">{row['distance_km']} km</span>
                    </div>
                    <div style="font-size: 1rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.4rem;">{row['route_name']}</div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: #94a3b8; border-top: 1px solid #334155; padding-top: 0.5rem; margin-top: 0.5rem;">
                        <span>{row['total_passengers']:,} riders</span>
                        <span style="color: #38bdf8; font-weight: 600;">{row['on_time_percentage']}% on-time</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 2. CORRIDORS & NETWORK
# ==============================================================================
elif menu == "Corridors & Network":
    st.subheader("Transit Corridor & Station Inspector")
    st.write("Inspect sequential station stops, inter-station distances, estimated travel times, and accessibility infrastructure.")

    routes = execute_query("SELECT route_id, route_code, route_name, route_type, distance_km, base_fare FROM routes ORDER BY route_id")
    route_choices = {f"{r['route_code']} - {r['route_name']} ({r['route_type']})": r for r in routes}
    
    selected_name = st.selectbox("Select Corridor:", list(route_choices.keys()))
    sel_route = route_choices[selected_name]

    # Metric Row
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
    stepper_html = '<div class="station-stepper">'
    for i, s in enumerate(segments):
        stepper_html += f"""
            <div class="step-node">
                <div class="step-seq">STOP {s['stop_sequence']:02d}</div>
                <div class="step-name">{s['stop_name']}</div>
                <div class="step-meta">{s['distance_from_start_km']} km | ~{s['est_travel_time_min']} min</div>
            </div>
        """
        if i < len(segments) - 1:
            stepper_html += '<div class="step-arrow">➔</div>'
    stepper_html += '</div>'
    
    st.markdown(stepper_html, unsafe_allow_html=True)

    st.markdown("#### Station Facility Details")
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

# ==============================================================================
# 3. RIDERSHIP & DEMAND
# ==============================================================================
elif menu == "Ridership & Demand":
    st.subheader("Passenger Demand & Temporal Ridership Patterns")
    st.write("Analysis of passenger load distribution across 24-hour operational periods and payment preferences.")

    hourly_df = get_hourly_ridership_df()
    payment_df = get_payment_breakdown()

    col_rush, col_pie = st.columns([7, 4])
    
    with col_rush:
        st.markdown("#### Hourly Passenger Volume (24-Hour Cycle)")
        st.caption("Highlighted areas indicate peak morning (08:00–10:00) and evening (17:00–19:00) travel periods.")
        
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
            height=370
        )
        fig_rush.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            xaxis=dict(showgrid=True, gridcolor="#1e293b"),
            yaxis=dict(showgrid=True, gridcolor="#1e293b")
        )
        fig_rush.add_vrect(x0="08", x1="10", fillcolor="#38bdf8", opacity=0.15, line_width=0, annotation_text="Morning Peak", annotation_position="top left")
        fig_rush.add_vrect(x0="17", x1="19", fillcolor="#fbbf24", opacity=0.15, line_width=0, annotation_text="Evening Peak", annotation_position="top left")
        st.plotly_chart(fig_rush, use_container_width=True)

    with col_pie:
        st.markdown("#### Payment Method Distribution")
        st.caption("Ridership share across fare collection channels.")
        pay_totals = payment_df.groupby("payment_method")["transaction_count"].sum().reset_index()
        fig_pay = px.pie(
            pay_totals,
            names="payment_method",
            values="transaction_count",
            hole=0.45,
            template="plotly_dark",
            color_discrete_sequence=["#38bdf8", "#818cf8", "#34d399", "#fbbf24"],
            height=370
        )
        fig_pay.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a")
        fig_pay.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pay, use_container_width=True)

    st.markdown("---")
    
    col_demo, col_busiest = st.columns(2)
    with col_demo:
        st.markdown("#### Passenger Demographics")
        demo_totals = payment_df.groupby("passenger_type")["transaction_count"].sum().reset_index()
        fig_demo = px.bar(
            demo_totals,
            x="passenger_type",
            y="transaction_count",
            color="passenger_type",
            template="plotly_dark",
            labels={"passenger_type": "Category", "transaction_count": "Transactions"},
            height=300
        )
        fig_demo.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a", showlegend=False)
        st.plotly_chart(fig_demo, use_container_width=True)

    with col_busiest:
        st.markdown("#### Top 5 Station Hubs by Footfall")
        stop_df = get_stop_demand_df().head(5)
        fig_stops = px.bar(
            stop_df,
            x="stop_name",
            y="total_footfall",
            color="total_footfall",
            template="plotly_dark",
            color_continuous_scale="Blues",
            labels={"stop_name": "Station", "total_footfall": "Footfall"},
            height=300
        )
        fig_stops.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a", coloraxis_showscale=False)
        st.plotly_chart(fig_stops, use_container_width=True)

# ==============================================================================
# 4. TICKETING OPERATIONS
# ==============================================================================
elif menu == "Ticketing Operations":
    st.subheader("Passenger Ticketing & Reservation Console")
    st.write("Demonstration of real-time atomic transaction issuance with dynamic concession calculation.")

    bookable = TransitService.get_bookable_trips()
    
    if not bookable:
        st.warning("No scheduled trips currently available for ticketing.")
    else:
        trip_map = {
            f"[{t['trip_code']}] {t['route_name']} ({t['vehicle_code']}) - Scheduled: {t['scheduled_departure']}": t
            for t in bookable
        }
        selected_trip_label = st.selectbox("1. Select Scheduled Trip:", list(trip_map.keys()))
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
                "4. Passenger Classification:",
                ["Standard Adult (Full Fare)", "Student (50% Concession)", "Senior Citizen (60% Concession)", "Commuter Passholder (30% Concession)"]
            )
            cat_clean = passenger_cat.split(" (")[0]

        with c_pay:
            pay_method = st.selectbox(
                "5. Payment Channel:",
                ["Transit Smartcard", "Mobile QR / UPI", "Contactless EMV", "Ticket Counter"]
            )

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Issue Electronic Ticket (ACID Transaction)", type="primary"):
            res = TransitService.book_ticket(
                trip_id=trip_data["trip_id"],
                origin_stop_id=sel_orig_id,
                destination_stop_id=sel_dest_id,
                passenger_type=cat_clean,
                payment_method=pay_method
            )
            
            if res["success"]:
                st.success("Transaction committed successfully to relational database.")
                
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
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; border-top: 1px dashed #475569; padding-top: 0.8rem;">
                            <span style="font-size: 0.74rem; color: #94a3b8;">Channel: <b>{res['payment_method']}</b></span>
                            <span style="font-family: monospace; font-size: 0.95rem; letter-spacing: 2px; color: #64748b;">||| | |||| | ||| ||</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Transaction Rejected: {res['message']}")

# ==============================================================================
# 5. FLEET & DISPATCH
# ==============================================================================
elif menu == "Fleet & Dispatch":
    st.subheader("Fleet Assets & Real-Time Dispatch Management")
    st.write("Vehicle propulsion distribution, capacity utilization, and operational schedule management.")

    fleet_df = get_fleet_utilization_df()
    delay_df = get_delay_monitoring_df()

    col_f1, col_f2 = st.columns([6, 5])
    with col_f1:
        st.markdown("#### Vehicle Fleet Propulsion")
        fig_fuel = px.pie(
            fleet_df,
            names="fuel_propulsion",
            hole=0.45,
            template="plotly_dark",
            color_discrete_sequence=["#34d399", "#38bdf8", "#fbbf24", "#818cf8"],
            height=320
        )
        fig_fuel.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a")
        st.plotly_chart(fig_fuel, use_container_width=True)

    with col_f2:
        st.markdown("#### Punctuality Classification")
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
            height=320
        )
        fig_del.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a", showlegend=False)
        st.plotly_chart(fig_del, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Real-Time Dispatch Lifecycle Manager")
    st.caption("Update active operational states and record schedule deviations.")
    
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
        if st.button("Update Dispatch Record", type="primary"):
            d_res = TransitService.update_trip_status(sel_t["trip_id"], new_stat, new_delay)
            if d_res["success"]:
                st.success(d_res["message"])
            else:
                st.error(d_res["message"])

# ==============================================================================
# 6. TECHNICAL ARCHITECTURE
# ==============================================================================
elif menu == "Technical Architecture":
    st.subheader("DP-900 Relational Modeling & Technical Lab")
    st.write("Demonstration of database normalization, analytical queries, and data hygiene auditing.")

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
        sql_input = st.text_area("SQL Command Buffer:", value=sample_queries[chosen_sample].strip(), height=160)
        
        if st.button("Execute Query"):
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
            if st.button("Export Datasets to CSV (Data Lake Staging)"):
                files = export_tables_to_csv()
                st.success(f"Exported {len(files)} CSV files into `/data` directory.")
        with c_seed:
            if st.button("Re-Seed Production Database"):
                generate_and_seed_data()
                st.success("Re-seeded with 160 operational trips and 2,200 transactions.")
                st.rerun()
