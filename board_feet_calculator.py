import streamlit as st

st.set_page_config(page_title="Board Feet Calculator", page_icon="🪵", layout="wide")

# ---------------- Styling ----------------
# All the visual personality lives here: a craft-feeling display font,
# a wood-gradient hero banner, chunkier buttons, and metric "cards".
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Nunito+Sans:wght@400;600;700&display=swap');

    /* Body text */
    html, body, [class*="css"], .stMarkdown, .stButton, .stNumberInput {
        font-family: 'Nunito Sans', sans-serif;
    }
    /* Headings get the characterful display serif */
    h1, h2, h3, .hero-title {
        font-family: 'Fraunces', serif !important;
        letter-spacing: -0.5px;
    }

    /* Wood-gradient hero banner */
    .hero {
        background: linear-gradient(135deg, #6F4E37 0%, #A0522D 55%, #C19A6B 100%);
        border-radius: 18px;
        padding: 26px 32px;
        color: #FAF3E8;
        box-shadow: 0 8px 24px rgba(80, 50, 20, 0.25);
        position: relative;
        overflow: hidden;
        margin-bottom: 10px;
    }
    .hero::after {  /* faint wood-grain streaks across the banner */
        content: "";
        position: absolute; inset: 0;
        background-image: repeating-linear-gradient(
            100deg,
            rgba(255,255,255,0.06) 0px,
            rgba(255,255,255,0.06) 2px,
            transparent 2px,
            transparent 24px
        );
        pointer-events: none;
    }
    .hero-title { font-size: 2.6rem; font-weight: 700; margin: 0; color: #FFF8EF; }
    .hero-sub { font-size: 1.05rem; opacity: 0.92; margin-top: 6px; }

    /* Chunky, tactile buttons */
    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        border: 2px solid rgba(62,39,35,0.15);
        transition: transform 0.05s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(80,50,20,0.18);
    }

    /* Make the metrics look like cards */
    [data-testid="stMetric"] {
        background: #FFFDF9;
        border: 1px solid #E8D9C5;
        border-radius: 14px;
        padding: 14px 18px;
        box-shadow: 0 2px 8px rgba(120,90,60,0.08);
    }
    [data-testid="stMetricValue"] { color: #6F4E37; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🪵 Board Feet Cost Calculator</div>
        <div class="hero-sub">Know what your lumber's going to cost — before you make a cut.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

if "boards" not in st.session_state:
    st.session_state.boards = [{"id": 0}]
if "next_id" not in st.session_state:
    st.session_state.next_id = 1


def lumber_stack_svg(items):
    """Draw every board to scale as a little stack of 3D planks.

    `items` is a list of dicts with width/length/thickness (inches).
    All boards share one scale factor so their sizes are comparable.
    """
    if not items:
        return ""

    usable_w = 300                      # px the longest board may span
    left = 30                           # room for the board number on the left
    max_len = max((it["length"] for it in items), default=1) or 1
    scale = usable_w / max_len
    gap = 16
    y = 18
    parts = []

    for idx, it in enumerate(items):
        w_px = max(it["length"] * scale, 6)          # board length -> horizontal
        h_px = max(it["width"] * scale, 10)          # board width  -> vertical
        depth = min(max(it["thickness"] * scale * 3, 4), 16)  # thickness, slightly exaggerated
        x = left

        # top edge + right edge give it a chunky 3D look, then the grained face
        parts.append(
            f'<polygon points="{x},{y} {x + w_px},{y} {x + w_px + depth},{y - depth} {x + depth},{y - depth}" fill="#5C3A21"/>'
        )
        parts.append(
            f'<polygon points="{x + w_px},{y} {x + w_px + depth},{y - depth} '
            f'{x + w_px + depth},{y - depth + h_px} {x + w_px},{y + h_px}" fill="#7A4E2D"/>'
        )
        parts.append(f'<rect x="{x}" y="{y}" width="{w_px}" height="{h_px}" rx="2" fill="url(#wood)"/>')

        # a couple of grain lines across the face
        for g in range(1, 3):
            gy = y + h_px * g / 3
            parts.append(
                f'<line x1="{x + 4}" y1="{gy}" x2="{x + w_px - 4}" y2="{gy}" '
                f'stroke="#8B5A2B" stroke-opacity="0.35" stroke-width="1"/>'
            )

        # little numbered chip on the left, matching the table rows
        cy = y + h_px / 2
        parts.append(f'<circle cx="14" cy="{cy}" r="10" fill="#6F4E37"/>')
        parts.append(
            f'<text x="14" y="{cy + 4}" text-anchor="middle" font-family="Nunito Sans, sans-serif" '
            f'font-size="12" font-weight="700" fill="#FFF8EF">{idx + 1}</text>'
        )

        y += h_px + depth + gap

    view_w = left + usable_w + 18
    return (
        f'<svg width="{view_w}" height="{int(y) + 1}" viewBox="0 0 {view_w} {y}" '
        f'preserveAspectRatio="xMidYMid meet" style="display:block;" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<defs><linearGradient id="wood" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="#C9A66B"/><stop offset="100%" stop-color="#A0703C"/>'
        f'</linearGradient></defs>'
        + "".join(parts)
        + "</svg>"
    )

col_inputs, col_results = st.columns([3, 2])

# ---------------- Left column: board inputs ----------------
with col_inputs:
    st.subheader("🪵 Your Boards")

    if st.button("➕ Add Another Board", type="primary"):
        st.session_state.boards.append({"id": st.session_state.next_id})
        st.session_state.next_id += 1
        st.rerun()

    for i, board in enumerate(st.session_state.boards):
        bid = board["id"]
        with st.container(border=True):
            header_col, remove_col = st.columns([5, 1])
            header_col.markdown(f"**Board {i + 1}**")
            if len(st.session_state.boards) > 1:
                if remove_col.button("🗑️", key=f"remove_{bid}"):
                    st.session_state.boards = [b for b in st.session_state.boards if b["id"] != bid]
                    st.rerun()

            c1, c2, c3 = st.columns(3)
            with c1:
                st.number_input("Thickness (in)", min_value=0.0, value=1.0, step=0.25, key=f"thickness_{bid}")
            with c2:
                st.number_input("Width (in)", min_value=0.0, value=6.0, step=0.5, key=f"width_{bid}")
            with c3:
                st.number_input("Length (in)", min_value=0.0, value=96.0, step=0.5, key=f"length_{bid}")

            c4, c5 = st.columns(2)
            with c4:
                st.number_input("Quantity", min_value=1, value=1, step=1, key=f"qty_{bid}")
            with c5:
                st.number_input("Price / board foot ($)", min_value=0.0, value=5.00, step=0.25, key=f"price_{bid}")

# ---------------- Right column: results ----------------
with col_results:
    st.subheader("📊 Results")

    rows = []
    plank_shapes = []
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
        plank_shapes.append({"thickness": thickness, "width": width, "length": length_in})

    with st.container(border=True):
        st.metric("Total Board Feet", f"{grand_total_bf:.2f}")
        st.metric("Total Cost", f"${grand_total_cost:.2f}")

    st.markdown("**Your lumber, to scale**")
    st.markdown(lumber_stack_svg(plank_shapes), unsafe_allow_html=True)

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
        for you: just enter each board's real thickness, width, and length, and
        it'll tell you exactly how many board feet you're buying and what it costs
        at your price per board foot.
        """
    )
