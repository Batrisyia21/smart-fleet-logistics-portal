import sqlite3
import pandas as pd
import streamlit as st

# ==========================================
# 1. DATABASE INGESTION & SETUP
# ==========================================
DB_NAME = "logistics_system.db"
CSV_FILE = "smart_logistics_dataset.csv"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_csv(CSV_FILE)

        # Impute missing delay reasons
        if 'Logistics_Delay_Reason' in df.columns:
            df['Logistics_Delay_Reason'] = df['Logistics_Delay_Reason'].fillna('None / On Time')

        # Array of 11 international land logistics hubs    
        GLOBAL_HUBS = [
            (3.1390, 101.6869),   # Kuala Lumpur
            (1.3521, 103.8198),   # Singapore
            (13.7563, 100.5018),  # Bangkok
            (35.6762, 139.6503),  # Tokyo
            (22.3193, 114.1694),  # Hong Kong
            (25.2048, 55.2708),   # Dubai
            (51.5074, -0.1278),   # London
            (48.8566, 2.3522),    # Paris
            (40.7128, -74.0060),  # New York
            (29.7604, -95.3698),  # Houston
            (-33.8688, 151.2093), # Sydney
        ]
        
        clean_lats = []
        clean_lons = []
        # iterate through dataset and compute localized city-centered offsets
        for idx, row in df.iterrows():
            hub = GLOBAL_HUBS[idx % len(GLOBAL_HUBS)]
            lat_offset = (abs(row['Latitude']) % 0.2) - 0.1
            lon_offset = (abs(row['Longitude']) % 0.2) - 0.1
            clean_lats.append(hub[0] + lat_offset)
            clean_lons.append(hub[1] + lon_offset)

        # Overwrite raw coordinates with normalized values    
        df['Latitude'] = clean_lats
        df['Longitude'] = clean_lons

        # Persist normalized DataFrame directly
        df.to_sql("fleet_shipments", conn, if_exists="replace", index=False)
    except Exception as e:
        st.error(f"Error loading CSV file into SQL: {e}")
    finally:
        conn.close()

init_db()

def run_query(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def execute_sql(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# ==========================================
# 2. STREAMLIT CONFIG & CUSTOM STYLING
# ==========================================
st.set_page_config(
    page_title="Smart Fleet & Logistics Portal",
    page_icon="🚚",
    layout="wide"
)

st.markdown("""
<style>
    /* Remove default Streamlit top padding */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Main Background */
    .stApp {
        background-color: #0b0c10;
        color: #ffffff;
    }

    /* Lowered Banner */
    .hero-banner {
        width: 100vw;
        height: 50vh !important; 
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        background: linear-gradient(rgba(11, 12, 16, 0.70), rgba(11, 12, 16, 0.70)), 
                    url('https://images.unsplash.com/photo-1519003722824-194d4455a60c?auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        border-bottom: 3px solid #ff7b00;
        margin-bottom: 20px;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .hero-title span {
        color: #ff7b00;
        font-weight: 900;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #e0e0e0;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Sidebar Base */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 2px solid #ff7b00 !important;
        padding-top: 10px;
    }

    /* Sidebar Logo Header Row */
    .sidebar-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding: 0 5px;
    }

    .sidebar-brand {
        font-size: 1.5rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    
    .sidebar-brand span {
        color: #ff7b00;
    }

    /* Collapse Arrow Button */
    .collapse-btn-wrapper div.stButton > button {
        background: transparent !important;
        color: #ff7b00 !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        width: auto !important;
        min-height: auto !important;
    }
    
    .collapse-btn-wrapper div.stButton > button:hover {
        color: #ffffff !important;
    }

    /* Orange Box + Black Font Centered Button */
    .create-btn-container div.stButton > button {
        background-color: #ff7b00 !important;
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 16px !important;
        width: 100% !important;
        box-shadow: 0px 4px 12px rgba(255, 123, 0, 0.25) !important;
        margin: 0 auto 15px auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }

    .create-btn-container div.stButton > button:hover {
        background-color: #e06c00 !important;
        color: #000000 !important;
        box-shadow: 0px 6px 16px rgba(255, 123, 0, 0.4) !important;
    }

    /* Hide standard Radio Circles */
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }

    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 6px !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        transition: background-color 0.2s ease, color 0.2s ease;
        margin: 0 !important;
        width: 100% !important;
        border: 1px solid transparent !important;
        cursor: pointer;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        color: #cccccc !important;
        font-weight: 600 !important;
        font-size: 0.98rem !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background-color: rgba(255, 123, 0, 0.1) !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label:hover p {
        color: #ff7b00 !important;
    }

    /* Active Selected Option Styling */
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: #12141a !important; 
        border: 1px solid #ff7b00 !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] p {
        color: #ff7b00 !important;
        font-weight: 700 !important;
    }

    /* Sidebar Selectbox Label */
    section[data-testid="stSidebar"] label {
        color: #ff7b00 !important;
        font-weight: 600 !important;
    }

    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background-color: #0d0f17 !important;
        border: 2px solid #ff7b00 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        box-shadow: 0px 4px 12px rgba(255, 123, 0, 0.15) !important;
        height: 110px !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    div[data-testid="stMetricLabel"] p {
        color: #ffffff !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        margin-bottom: 2px !important;
    }

    div[data-testid="stMetricValue"] div {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
    }

    hr {
        border-top: 2px solid #ff7b00 !important;
        margin: 15px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# HERO HEADER SECTION
# ------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">Smart <span>Fleet & Logistics</span> Optimization Portal</div>
    <div class="hero-subtitle">Powered by Python, SQLite, and Streamlit</div>
</div>
""", unsafe_allow_html=True)

if 'active_menu' not in st.session_state:
    st.session_state['active_menu'] = "📊 Performance Hub"

if 'show_menu_options' not in st.session_state:
    st.session_state['show_menu_options'] = True

# ------------------------------------------
# SIDEBAR CONTROL MENU
# ------------------------------------------
with st.sidebar:
    # 1. Header with Brand & Orange Collapse Arrow Button
    col_brand, col_arrow = st.columns([0.8, 0.2])
    
    with col_brand:
        st.markdown('<div class="sidebar-brand"><span>Smart</span> Fleet</div>', unsafe_allow_html=True)
        
    with col_arrow:
        st.markdown('<div class="collapse-btn-wrapper">', unsafe_allow_html=True)
        arrow_label = "⟨" if st.session_state['show_menu_options'] else "⟩"
        if st.button(arrow_label, key="toggle_menu"):
            st.session_state['show_menu_options'] = not st.session_state['show_menu_options']
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Centered Orange Button with Black Text
    st.markdown('<div class="create-btn-container">', unsafe_allow_html=True)
    if st.button("⊕ Create new entry", key="create_btn"):
        st.session_state['active_menu'] = "📝 Dispatch Control (CRUD)"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 3. Collapsible Navigation Options
    if st.session_state['show_menu_options']:
        menu_options = [
            "📊 Performance Hub", 
            "📝 Dispatch Control (CRUD)", 
            "🗺️ GPS Tracker", 
            "📁 Records Database"
        ]
        
        selected_option = st.radio(
            "Navigation",
            menu_options,
            index=menu_options.index(st.session_state['active_menu']) if st.session_state['active_menu'] in menu_options else 0
        )
        
        st.session_state['active_menu'] = selected_option
        st.markdown("<hr>", unsafe_allow_html=True)

    # Asset Filter Dropdown
    all_assets = run_query("SELECT DISTINCT Asset_ID FROM fleet_shipments")['Asset_ID'].tolist()
    selected_asset = st.selectbox("Filter by Asset ID", ["All Assets"] + sorted(all_assets))

# Filter Base Data
if selected_asset == "All Assets":
    base_data = run_query("SELECT * FROM fleet_shipments")
else:
    base_data = run_query("SELECT * FROM fleet_shipments WHERE Asset_ID = ?", (selected_asset,))

# ------------------------------------------
# TAB 1: EXECUTIVE ANALYTICS DASHBOARD
# ------------------------------------------
if st.session_state['active_menu'] == "📊 Performance Hub":
    st.markdown(f"### Operational Overview ({selected_asset})")
    
    if not base_data.empty:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        total_shipments = len(base_data)
        delayed_shipments = len(base_data[base_data['Shipment_Status'] == 'Delayed'])
        avg_utilization = base_data['Asset_Utilization'].mean()
        avg_wait_time = base_data['Waiting_Time'].mean()
        
        kpi1.metric("Total Trips Logged", f"{total_shipments:,}")
        kpi2.metric("Delayed Shipments", f"{delayed_shipments:,}", delta=f"↑ {(delayed_shipments/total_shipments)*100:.1f}% Rate", delta_color="inverse")
        kpi3.metric("Avg Asset Utilization", f"{avg_utilization:.1f}%")
        kpi4.metric("Avg Waiting Time", f"{avg_wait_time:.1f} mins")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📦 Shipment Status Breakdown")
            status_counts = base_data['Shipment_Status'].value_counts()
            st.bar_chart(status_counts, horizontal=True)
            
        with col_right:
            st.subheader("⚠️ Primary Delay Factors")
            delay_counts = base_data['Logistics_Delay_Reason'].value_counts()
            st.bar_chart(delay_counts, horizontal=True)
            
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🚦 Traffic Conditions Impact")
        traffic_df = base_data.groupby(['Traffic_Status', 'Shipment_Status']).size().unstack(fill_value=0)
        st.bar_chart(traffic_df, horizontal=True)
    else:
        st.warning("No operational records found.")

# ------------------------------------------
# TAB 2: DISPATCH CONTROL (CRUD)
# ------------------------------------------
elif st.session_state['active_menu'] == "📝 Dispatch Control (CRUD)":
    st.header("Dispatch Management Console")
    st.caption("Perform Create & Update actions directly inside your SQL Database.")
    
    tab_create, tab_update = st.tabs(["➕ Register New Shipment Entry", "✏️ Update Shipment Status"])
    
    with tab_create:
        with st.form("new_shipment_form"):
            col1, col2, col3 = st.columns(3)
            timestamp = col1.text_input("Timestamp", value="2026-07-23 08:00:00")
            asset_id = col2.selectbox("Asset ID", sorted(all_assets))
            status = col3.selectbox("Shipment Status", ["In Transit", "Delivered", "Delayed"])
            
            lat = col1.number_input("Latitude", value=3.1390)
            lon = col2.number_input("Longitude", value=101.6869)
            traffic = col3.selectbox("Traffic Status", ["Clear", "Heavy", "Detour"])
            
            waiting = col1.number_input("Waiting Time (mins)", min_value=0, value=15)
            delay_reason = col2.selectbox("Delay Reason", ["None / On Time", "Weather", "Traffic", "Mechanical Failure"])
            utilization = col3.number_input("Asset Utilization (%)", min_value=0.0, max_value=100.0, value=85.0)
            
            submit_btn = st.form_submit_button("Submit Entry to SQLite Database")
            
            if submit_btn:
                insert_query = """
                INSERT INTO fleet_shipments 
                (Timestamp, Asset_ID, Latitude, Longitude, Shipment_Status, Traffic_Status, Waiting_Time, Logistics_Delay_Reason, Asset_Utilization)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                execute_sql(insert_query, (timestamp, asset_id, lat, lon, status, traffic, waiting, delay_reason, utilization))
                st.success(f"Successfully registered new trip for vehicle **{asset_id}** in SQL database!")

    with tab_update:
        st.subheader("Modify Existing Record")
        record_id = st.number_input("Enter Row Index (ROWID) to Update", min_value=1, value=1)
        
        with st.form("update_form"):
            col1, col2 = st.columns(2)
            new_status = col1.selectbox("New Shipment Status", ["Delivered", "In Transit", "Delayed"])
            new_traffic = col2.selectbox("Updated Traffic Status", ["Clear", "Heavy", "Detour"])
            update_btn = st.form_submit_button("Apply Update")
            
            if update_btn:
                update_query = "UPDATE fleet_shipments SET Shipment_Status = ?, Traffic_Status = ? WHERE rowid = ?"
                execute_sql(update_query, (new_status, new_traffic, record_id))
                st.success(f"Updated record #{record_id} status to '{new_status}' in SQL database!")

# ------------------------------------------
# TAB 3: GPS TRACKER
# ------------------------------------------
elif st.session_state['active_menu'] == "🗺️ GPS Tracker":
    st.header("Global Fleet Positioning (Land Logistics Hubs)")
    if not base_data.empty:
        map_df = base_data[['Latitude', 'Longitude']].dropna().rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
        st.map(map_df, zoom=1)
    else:
        st.info("No coordinates available to map.")

# ------------------------------------------
# TAB 4: DATABASE RECORDS VIEW
# ------------------------------------------
elif st.session_state['active_menu'] == "📁 Records Database":
    st.header("Live SQLite Database Records")
    st.write(f"Showing total **{len(base_data)}** rows from table `fleet_shipments`.")
    st.dataframe(base_data, use_container_width=True)