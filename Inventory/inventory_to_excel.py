import csv
import os

# File name for our "database"
FILE_NAME = "inventory_data.csv"

# Initial Data (used if the file doesn't exist yet)
# Expanded Inventory Data for a Tech Store
default_inventory = [
    {"Item": "Laptop", "Qty": 10, "Threshold": 3, "Price": 55000},
    {"Item": "Mouse", "Qty": 2, "Threshold": 5, "Price": 800},
    {"Item": "Keyboard", "Qty": 15, "Threshold": 5, "Price": 1200},
    {"Item": "Monitor", "Qty": 4, "Threshold": 2, "Price": 12000},
    {"Item": "Hard Drive", "Qty": 8, "Threshold": 4, "Price": 4500},
    {"Item": "USB Cable", "Qty": 20, "Threshold": 10, "Price": 350},
    {"Item": "Webcam", "Qty": 3, "Threshold": 5, "Price": 3200},
    {"Item": "Headphones", "Qty": 12, "Threshold": 4, "Price": 2500},
    {"Item": "Router", "Qty": 5, "Threshold": 2, "Price": 1800},
    {"Item": "RAM Stick", "Qty": 1, "Threshold": 3, "Price": 4000}
]

def save_to_csv(data):
    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Item", "Qty", "Threshold", "Price"])
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Data synced to {FILE_NAME}")

def load_from_csv():
    if not os.path.exists(FILE_NAME):
        return default_inventory
    
    with open(FILE_NAME, mode='r') as file:
        return list(csv.DictReader(file))

def run_inventory():
    inventory = load_from_csv()
    print("--- 🏢 Excel-Linked Inventory Manager ---")
    
    # Logic: Alert for items below threshold
    for row in inventory:
        qty = int(row['Qty'])
        thresh = int(row['Threshold'])
        status = "⚠️ LOW" if qty <= thresh else "✅ OK"
        print(f"{row['Item']:<12} | Stock: {qty:<3} | Status: {status}")

    # Save it back (simulating an update)
    save_to_csv(inventory)

run_inventory()