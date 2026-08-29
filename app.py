import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Bin Location Finder",
    page_icon="logo.png",
    layout="centered"
)

# ====================== LOGIN ======================
def check_login(username, password):
    try:
        usernames = st.secrets["credentials"]["usernames"]
        passwords = st.secrets["credentials"]["passwords"]
        if username in usernames:
            idx = usernames.index(username)
            return passwords[idx] == password
    except:
        return False
    return False

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>Login</h2>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if check_login(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect username or password")
    st.stop()

# ====================== AFTER LOGIN ======================

# Logout button
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ===== CENTERED LOGO =====
col1, col2, col3 = st.columns([2.2, 1.2, 2.2])
with col2:
    st.image("logo.png", width=130)

# ===== CENTERED TITLE =====
st.markdown(
    "<h1 style='text-align: center; margin-top: 10px; margin-bottom: 5px;'>Bin Location Finder</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: #666; margin-bottom: 25px;'>Enter a Part Number to find its bin location.</p>",
    unsafe_allow_html=True
)

# ---------- Google Sheet ----------
SHEET_ID = "11eP3HCgWvcl1XD5pAv5H1UbM9xX9sfR0"
GID = "908111469"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Could not load the Google Sheet.")
    st.stop()

# ---------- Shed Detection ----------
def get_shed(bin_code):
    if pd.isna(bin_code):
        return None
    code = str(bin_code).strip().upper()

    shed4 = ["DA", "DB", "DC", "DD", "DE", "DF", "DG", "DH", "DI", "DJ", "DK", "DM", "DO", "DT", "DN", "QB-04"]
    if any(code.startswith(p) for p in shed4):
        return 4

    shed3 = ["CA", "CB", "CC", "CD", "CE", "CF", "CG", "CH", "CI", "CJ", "CK", "QB-03"]
    if any(code.startswith(p) for p in shed3):
        return 3

    shed2 = ["BA", "BB", "BC", "BF", "BG", "BH", "BI", "BJ", "BK", "BL", "QB-02", "CNC"]
    if any(code.startswith(p) for p in shed2):
        return 2

    shed1 = ["AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AN", "AO", "ST"]
    if any(code.startswith(p) for p in shed1):
        return 1

    return None

# ---------- Search ----------
PART_COL = "Part"
BIN_COL = "Bin"

all_parts = sorted(df[PART_COL].astype(str).unique().tolist())

selected_part = st.selectbox(
    "Enter Part Number",
    options=[""] + all_parts,
    index=0,
    placeholder="Start typing a part number..."
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

        first_bin = result[BIN_COL].iloc[0]
        shed = get_shed(first_bin)

        if shed:
            st.markdown(f"### 📍 This part is located in **Shed {shed}**")

            pdf_file = f"Shed {shed}.pdf"
            try:
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label=f"📄 Download / View Shed {shed} Map (PDF)",
                        data=f,
                        file_name=pdf_file,
                        mime="application/pdf",
                        type="primary"
                    )
            except FileNotFoundError:
                st.warning(f"Map file **{pdf_file}** not found.")
        else:
            st.info("Could not detect the shed for this bin.")
    else:
        st.warning("No matching part number found.")
else:
    st.info("Type or select a part number above to search.")
