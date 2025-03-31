import streamlit as st
import requests

# API Base URL
API_URL = "http://127.0.0.1:5000"

# 🎉 Header
st.title("☕ Boutique Café Virtual Concierge")

# 📍 Café Information
st.sidebar.header("📍 About the Café")
info_response = requests.get(f"{API_URL}/info")
if info_response.status_code == 200:
    info = info_response.json()
    st.sidebar.write(f"📌 **Location:** {info['location']}")
    st.sidebar.write(f"🕒 **Hours:** {info['hours']}")
    st.sidebar.write(f"📞 **Contact:** {info['contact']}")
    st.sidebar.write("🎶 **Upcoming Events:**")
    for event in info.get("events", []):
        st.sidebar.write(f"🔹 {event}")
    st.sidebar.write(f"📖 **Our Story:** {info['history']}")
else:
    st.sidebar.error("⚠️ Could not load café info.")

# 📜 Menu
st.subheader("📋 Menu")
menu_response = requests.get(f"{API_URL}/menu")
if menu_response.status_code == 200:
    menu = menu_response.json()
    for item in menu:
        st.write(f"**{item['item']}** - ${item['price']:.2f} | ⚠️ *{item['allergens']}*")
else:
    st.error("⚠️ Error fetching menu!")

# 📅 Reservations
st.subheader("📅 Make a Reservation")
name = st.text_input("Your Name")
date = st.date_input("Select Date")
time = st.time_input("Select Time")
guests = st.number_input("Number of Guests", min_value=1, max_value=10, step=1)
special_requests = st.text_area("Special Requests (e.g., dietary restrictions)")

if st.button("✅ Confirm Reservation"):
    reservation_data = {
        "name": name, "date": str(date), "time": str(time),
        "guests": guests, "special_requests": special_requests
    }
    response = requests.post(f"{API_URL}/reserve", json=reservation_data)
    if response.status_code == 200:
        st.success("🎉 Reservation Confirmed!")
    else:
        st.error("⚠️ Error making reservation.")

# 📦 View Reservations
st.subheader("📦 Your Reservations")
if st.button("🔄 Refresh Reservations"):
    reservations_response = requests.get(f"{API_URL}/reservations")
    if reservations_response.status_code == 200:
        reservations = reservations_response.json()
        for res in reservations:
            st.write(f"👤 {res['name']} - {res['date']} at {res['time']} for {res['guests']} guests")
    else:
        st.error("⚠️ Error fetching reservations!")
