import streamlit as st
import pandas as pd

#st.set_page_config(page_title="Bin Location Finder", page_icon="📦", layout="centered")

st.set_page_config(
    page_title="Bin Location Finder",
    page_icon="logo.png",
    layout="centered"
)

# ===== CENTERED LOGO =====
st.markdown(
    """
    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <img src="logo.png" width="120">
    </div>
    """,
    unsafe_allow_html=True
)

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
PART_COL = "Part"
BIN_COL = "Bin"

part_number = st.text_input("Enter Part Number", placeholder="e.g. 100011")

if part_number:
    # Case-insensitive partial match
    mask = df[PART_COL].astype(str).str.contains(part_number.strip(), case=False, na=False)
    result = df[mask]

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
    st.info("Type a part number above to search.")

#with st.expander("View all data"):
#    st.dataframe(df, use_container_width=True, hide_index=True)
