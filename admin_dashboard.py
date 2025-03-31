import streamlit as st
import requests

# API Base URL
API_URL = "http://127.0.0.1:5000"

st.title("☕ Café Admin Dashboard")

# Sidebar Navigation
section = st.sidebar.radio("📌 Choose a Section", ["Café Info", "Reservations", "Orders", "Menu Management", "Customer Feedback"])

# 📍 Café Information
if section == "Café Info":
    st.subheader("📍 Café Information")
    info_response = requests.get(f"{API_URL}/info")
    if info_response.status_code == 200:
        info = info_response.json()
        st.write(f"📍 **Location:** {info['location']}")
        st.write(f"🕒 **Hours:** {info['hours']}")
        st.write(f"📞 **Contact:** {info['contact']}")
        st.write(f"🎤 **Events:** {', '.join(info['events'])}")
        st.write(f"📖 **History:** {info['history']}")
    else:
        st.error("⚠️ Could not fetch café info.")

# 📅 Reservations Section
elif section == "Reservations":
    st.subheader("📅 Reservations")
    reservations_response = requests.get(f"{API_URL}/reservations")
    if reservations_response.status_code == 200:
        reservations = reservations_response.json()
        for res in reservations:
            st.write(f"👤 {res['name']} - 📅 {res['date']} at {res['time']} - {res['guests']} guests")
    else:
        st.error("⚠️ Could not fetch reservations.")

# 📜 Orders Section
elif section == "Orders":
    st.subheader("📜 Order History")
    orders_response = requests.get(f"{API_URL}/orders")
    if orders_response.status_code == 200:
        orders = orders_response.json()
        for order in orders:
            st.write(f"🛒 **{order['name']}** ordered **{order['item']}** - Status: *{order['status']}*")
    else:
        st.error("⚠️ Could not fetch orders.")

# 🍽️ Menu Management
elif section == "Menu Management":
    st.subheader("🍽️ Add a Menu Item")
    item_name = st.text_input("Item Name")
    price = st.number_input("Price ($)", min_value=0.0, format="%.2f")
    allergens = st.text_input("Allergens (if any)")

    if st.button("✅ Add to Menu"):
        menu_data = {"item": item_name, "price": price, "allergens": allergens}
        response = requests.post(f"{API_URL}/menu", json=menu_data)
        if response.status_code == 200:
            st.success("🎉 Menu item added successfully!")
        else:
            st.error("⚠️ Error adding menu item.")

# 💬 Customer Feedback
elif section == "Customer Feedback":
    st.subheader("💬 Customer Feedback")
    feedback_response = requests.get(f"{API_URL}/feedback")
    if feedback_response.status_code == 200:
        feedback_list = feedback_response.json()
        for fb in feedback_list:
            st.write(f"⭐ {fb['rating']}/5 - {fb['name']} says: {fb['comments']}")
    else:
        st.error("⚠️ Could not fetch feedback.")
