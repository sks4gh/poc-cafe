from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import string

app = Flask(__name__)

# Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017/"  # Change if using MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["cafe_db"]

# Collections
cafe_info_collection = db["cafe_info"]
menu_collection = db["menu"]
reservations_collection = db["reservations"]
orders_collection = db["orders"]
feedback_collection = db["feedback"]

def generate_unique_id(prefix):
    """Generate a unique 6-character ID (e.g., ORD123, RES456)."""
    return f"{prefix}{''.join(random.choices(string.digits, k=6))}"

### 📍 Café Information API
@app.route('/info', methods=['GET'])
def get_cafe_info():
    """Returns café details (location, hours, events, history)."""
    info = cafe_info_collection.find_one({}, {"_id": 0})
    return jsonify(info or {})

### 📜 Menu API
@app.route('/menu', methods=['GET'])
def get_menu():
    """Fetch the café menu."""
    menu = list(menu_collection.find({}, {"_id": 0}))
    return jsonify(menu)

@app.route('/menu', methods=['POST'])
def add_menu_item():
    """Add a new menu item."""
    data = request.json
    if not all(key in data for key in ["item", "price", "allergens"]):
        return jsonify({"error": "Missing fields"}), 400

    menu_collection.insert_one(data)
    return jsonify({"message": "✅ Menu item added!"})

@app.route('/menu/<item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    """Delete a menu item by ID."""
    result = menu_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return jsonify({"message": "✅ Menu item deleted!"})
    return jsonify({"error": "Item not found"}), 404

### 📅 Reservations API
@app.route('/reservations', methods=['GET'])
def get_reservations():
    """Fetch all reservations."""
    reservations = list(reservations_collection.find({}, {"_id": 0}))
    return jsonify(reservations)

@app.route('/reserve', methods=['POST'])
def make_reservation():
    """Create a reservation with an auto-generated reservation number."""
    data = request.json
    if not all(key in data for key in ["name", "date", "time", "guests"]):
        return jsonify({"error": "Missing fields"}), 400

    reservation_number = generate_unique_id("RES")
    reservation = {
        "reservation_number": reservation_number,
        "name": data["name"],
        "date": data["date"],
        "time": data["time"],
        "guests": data["guests"],
        "special_requests": data.get("special_requests", "")
    }
    
    reservations_collection.insert_one(reservation)
    return jsonify({"message": "✅ Reservation confirmed!", "reservation_number": reservation_number})

@app.route('/reservation/<reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    """Cancel a reservation by ID."""
    result = reservations_collection.delete_one({"_id": ObjectId(reservation_id)})
    if result.deleted_count:
        return jsonify({"message": "✅ Reservation canceled!"})
    return jsonify({"error": "Reservation not found"}), 404

### 🛒 Orders API
@app.route('/orders', methods=['GET'])
def get_orders():
    """Fetch all orders."""
    orders = list(orders_collection.find({}, {"_id": 0}))
    return jsonify(orders)

@app.route('/order', methods=['POST'])
def place_order():
    """Place an order with an auto-generated order number."""
    data = request.json
    if "name" not in data or "item" not in data:
        return jsonify({"error": "Missing name or item"}), 400

    order_number = generate_unique_id("ORD")
    order = {"order_number": order_number, "name": data["name"], "item": data["item"], "status": "Pending"}
    orders_collection.insert_one(order)
    return jsonify({"message": "✅ Order placed!", "order_number": order_number})

@app.route('/order/<order_id>', methods=['PUT'])
def update_order_status(order_id):
    """Update the status of an order."""
    data = request.json
    new_status = data.get("status")
    if not new_status:
        return jsonify({"error": "Missing status field"}), 400

    result = orders_collection.update_one(
        {"_id": ObjectId(order_id)}, {"$set": {"status": new_status}}
    )

    if result.matched_count:
        return jsonify({"message": "✅ Order status updated!"})
    return jsonify({"error": "Order not found"}), 404

### 💬 Feedback API
@app.route('/feedback', methods=['GET'])
def get_feedback():
    """Fetch customer feedback."""
    feedback = list(feedback_collection.find({}, {"_id": 0}))
    return jsonify(feedback)

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit customer feedback."""
    data = request.json
    if not all(key in data for key in ["name", "rating", "comments"]):
        return jsonify({"error": "Missing fields"}), 400

    feedback_collection.insert_one(data)
    return jsonify({"message": "✅ Feedback submitted!"})

if __name__ == '__main__':
    app.run(debug=True)
