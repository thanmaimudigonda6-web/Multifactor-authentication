import streamlit as st

st.set_page_config(page_title="Expense Tracker", layout="wide")

# Add background image with CSS
def add_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1579621970563-fbf46d27c7d5?w=1200&h=800&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .main {
            background-color: rgba(255, 255, 255, 0.92);
            border-radius: 15px;
            padding: 20px;
        }
        .block-container {
            background-color: rgba(255, 255, 255, 0.92);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image()

st.title("💰 Personal Expense Tracker")
# ---------------- SESSION STATE ---------------- #
if "expenses" not in st.session_state:
    st.session_state.expenses = []
# ---------------- LAYOUT ---------------- #
col1, col2 = st.columns(2)
# ---------------- FORM ---------------- #
with col1:
    st.subheader("➕ Add Expense")
    with st.form("expense_form"):
        title = st.text_input("Expense Title")
        amount = st.number_input("Amount", min_value=0)
        category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills"])
        add = st.form_submit_button("Add Expense")
        if add:
            st.session_state.expenses.append({
                "title": title,
                "amount": amount,
                "category": category
            })
            st.success("Expense Added!")
# ---------------- DISPLAY ---------------- #
with col2:
    st.subheader("📊 Expense Summary")
    if st.session_state.expenses:
        total = sum(item["amount"] for item in st.session_state.expenses)
        st.write(f"💵 Total Expense: {total}")
        # Interactivity: Toggle
        show_details = st.toggle("Show Detailed Expenses")
        if show_details:
            for item in st.session_state.expenses:
                st.write(f"{item['title']} - ₹{item['amount']} ({item['category']})")
        # Interactivity: Filter
        category_filter = st.selectbox("Filter by Category",
                                      ["All", "Food", "Travel", "Shopping", "Bills"])
        if category_filter != "All":
            filtered = [e for e in st.session_state.expenses if e["category"] == category_filter]
            st.write("Filtered Results:")
            for item in filtered:
                st.write(f"{item['title']} - ₹{item['amount']}")
    else:
        st.warning("No expenses added yet!")