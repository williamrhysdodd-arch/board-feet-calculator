import streamlit as st

st.title("Board Feet Cost Calculator")
st.write("Calculate the cost of lumber based on board feet.")

st.header("Board Dimensions")

col1, col2, col3 = st.columns(3)

with col1:
    thickness = st.number_input("Thickness (inches)", min_value=0.0, value=1.0, step=0.25)

with col2:
    width = st.number_input("Width (inches)", min_value=0.0, value=6.0, step=0.5)

with col3:
    length_in = st.number_input("Length (inches)", min_value=0.0, value=96.0, step=0.5)

quantity = st.number_input("Quantity (number of boards)", min_value=1, value=1, step=1)

st.header("Pricing")
price_per_bf = st.number_input("Price per board foot ($)", min_value=0.0, value=5.00, step=0.25)

# Board foot formula: (thickness in inches x width in inches x length in feet) / 12
length_ft = length_in / 12
board_feet_per_board = (thickness * width * length_ft) / 12
total_board_feet = board_feet_per_board * quantity
total_cost = total_board_feet * price_per_bf

st.header("Results")

col1, col2, col3 = st.columns(3)
col1.metric("Board Feet (per board)", f"{board_feet_per_board:.2f}")
col2.metric("Total Board Feet", f"{total_board_feet:.2f}")
col3.metric("Total Cost", f"${total_cost:.2f}")

st.caption("Formula: (Thickness × Width × Length) / 12 = Board Feet")
