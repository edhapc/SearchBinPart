import streamlit as st
import pandas as pd

#st.set_page_config(page_title="Bin Location Finder", page_icon="📦", layout="centered")
st.set_page_config(
    page_title="Bin Location Finder",
    page_icon="logo.png",
    layout="centered"
)

# ===== CENTERED LOGO =====
# More precise centering
col1, col2, col3 = st.columns([2.2, 1.2, 2.2])
with col2:
    st.image("logo.png", width=130)

# ===== CENTERED TITLE =====
st.markdown(
    "<h1 style='text-align: center; margin-top: 10px; margin-bottom: 5px;'>Bin Location Finder</h1>",
    unsafe_allow_html=True
)

# ===== CENTERED SUBTITLE =====
st.markdown(
    "<p style='text-align: center; color: #666; margin-bottom: 25px;'>Enter a Part Number to find its bin location.</p>",
    unsafe_allow_html=True
)

# ---------- Your Google Sheet (public CSV export) ----------
# This is the reliable way for public sheets
SHEET_ID = "11eP3HCgWvcl1XD5pAv5H1UbM9xX9sfR0"
GID = "908111469"   # from your URL

CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=60)  # refresh every 60 seconds
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()   # clean header names
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Could not load the Google Sheet. Make sure it is shared as 'Anyone with the link → Viewer'.")
    st.exception(e)
    st.stop()

# ---------- Search ----------
# ---------- Search with live suggestions ----------
PART_COL = "Part"
BIN_COL = "Bin"

# Get all unique part numbers
all_parts = df[PART_COL].astype(str).unique().tolist()

# Create a search box that shows matching suggestions
selected_part = st.selectbox(
    "Enter Part Number",
    options=[""] + sorted(all_parts),
    index=0,
    placeholder="Start typing a part number...",
    help="Type to filter the list"
)

if selected_part:
    result = df[df[PART_COL].astype(str) == selected_part]

    if not result.empty:
        st.success(f"Found {len(result)} matching part(s)")
        st.dataframe(
            result[[PART_COL, BIN_COL]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No matching part number found.")
else:
    st.info("Type or select a part number above to search.")
#with st.expander("View all data"):
#    st.dataframe(df, use_container_width=True, hide_index=True)
