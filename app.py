import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Bin Location Finder", page_icon="📦", layout="centered")

st.title("📦 Bin Location Finder")
st.write("Enter a Part Number to find its bin location.")

# ---------- Connect to Google Sheet ----------
# Replace the URL below with YOUR Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/11eP3HCgWvcl1XD5pAv5H1UbM9xX9sfR0/edit?usp=sharing&ouid=110452783196008988623&rtpof=true&sd=true"

@st.cache_data(ttl=60)  # refreshes every 60 seconds
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=SHEET_URL)
    # Clean column names (remove extra spaces)
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Could not load the Google Sheet. Check the URL and sharing settings.")
    st.stop()

# ---------- Search UI ----------
# Change these two lines to match YOUR exact column names
PART_COL = "Part No"          # ← change if different
BIN_COL = "Bin Location"      # ← change if different

part_number = st.text_input("Enter Part Number", placeholder="e.g. ABC-12345")

if part_number:
    # Case-insensitive exact or partial match
    mask = df[PART_COL].astype(str).str.contains(part_number.strip(), case=False, na=False)
    result = df[mask]

    if not result.empty:
        st.success(f"Found {len(result)} matching part(s)")
        # Show the important columns first
        display_cols = [PART_COL, BIN_COL] + [c for c in df.columns if c not in [PART_COL, BIN_COL]]
        st.dataframe(result[display_cols], use_container_width=True, hide_index=True)
    else:
        st.warning("No matching part number found.")
else:
    st.info("Type a part number above to search.")

# Optional: show full data (useful for checking)
with st.expander("View all data"):
    st.dataframe(df, use_container_width=True, hide_index=True)
