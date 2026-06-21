import streamlit as st

st.set_page_config(page_title="Board Feet Calculator", page_icon="🪵", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #A0522D !important;
        border-radius: 8px !important;
        padding: 6px !important;
    }
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapsedControl"] svg {
        width: 28px !important;
        height: 28px !important;
        color: white !important;
        fill: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🪵 Board Feet Cost Calculator")
st.caption("Know what your lumber's going to cost before you make a cut.")
st.info("👈 Add and edit your boards in the sidebar.")

# ---------------- Sidebar: inputs ----------------
with st.sidebar:
    st.header("🪵 Your Boards")
    st.write("Add a row for every board, even if they're all different sizes.")

    if "boards" not in st.session_state:
        st.session_state.boards = [{"id": 0}]
    if "next_id" not in st.session_state:
        st.session_state.next_id = 1

    for i, board in enumerate(st.session_state.boards):
        bid = board["id"]
        with st.container(border=True):
            header_col, remove_col = st.columns([5, 1])
            header_col.markdown(f"**Board {i + 1}**")
            if len(st.session_state.boards) > 1:
                if remove_col.button("🗑️", key=f"remove_{bid}"):
                    st.session_state.boards = [b for b in st.session_state.boards if b["id"] != bid]
                    st.rerun()

            st.number_input("Thickness (in)", min_value=0.0, value=1.0, step=0.25, key=f"thickness_{bid}")
            st.number_input("Width (in)", min_value=0.0, value=6.0, step=0.5, key=f"width_{bid}")
            st.number_input("Length (in)", min_value=0.0, value=96.0, step=0.5, key=f"length_{bid}")
            st.number_input("Quantity", min_value=1, value=1, step=1, key=f"qty_{bid}")
            st.number_input("Price / board foot ($)", min_value=0.0, value=5.00, step=0.25, key=f"price_{bid}")

    if st.button("➕ Add Another Board"):
        st.session_state.boards.append({"id": st.session_state.next_id})
        st.session_state.next_id += 1
        st.rerun()

# ---------------- Main area: results, pinned near top ----------------
st.divider()
st.subheader("📊 Results")

rows = []
grand_total_bf = 0.0
grand_total_cost = 0.0

for i, board in enumerate(st.session_state.boards):
    bid = board["id"]
    thickness = st.session_state[f"thickness_{bid}"]
    width = st.session_state[f"width_{bid}"]
    length_in = st.session_state[f"length_{bid}"]
    quantity = st.session_state[f"qty_{bid}"]
    price_per_bf = st.session_state[f"price_{bid}"]

    length_ft = length_in / 12
    bf_per_board = (thickness * width * length_ft) / 12
    total_bf = bf_per_board * quantity
    cost = total_bf * price_per_bf

    grand_total_bf += total_bf
    grand_total_cost += cost

    rows.append(
        {
            "Board": f"Board {i + 1}",
            "Dimensions": f'{thickness}" × {width}" × {length_in}"',
            "Qty": quantity,
            "Board Feet": round(total_bf, 2),
            "Cost": f"${cost:.2f}",
        }
    )

with st.container(border=True):
    col1, col2 = st.columns(2)
    col1.metric("Total Board Feet", f"{grand_total_bf:.2f}")
    col2.metric("Total Cost", f"${grand_total_cost:.2f}")

st.table(rows)

st.caption("Formula: (Thickness × Width × Length) / 12 = Board Feet")

st.divider()

with st.expander("📐 New to woodworking? What's a board foot?", expanded=False):
    st.markdown(
        """
        Lumber yards don't price hardwood by "the board" — they price it by **volume**,
        and a board foot is the unit they use to measure it.

        **One board foot = a piece of wood 12" long × 12" wide × 1" thick**
        (144 cubic inches of wood, however the actual board is shaped).

        So a thicker, wider, or longer board uses more wood — and costs more —
        even if it's technically still "one board." This calculator does that math
        for you: just enter each board's real thickness, width, and length in the
        sidebar, and it'll tell you exactly how many board feet you're buying and
        what it costs at your price per board foot.
        """
    )
