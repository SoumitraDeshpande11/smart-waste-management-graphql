from database import get_connection, init_db
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "waste_management.db")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

init_db()
conn = get_connection()
cursor = conn.cursor()

cursor.executemany(
    "INSERT INTO zones (name, area_code) VALUES (?, ?)",
    [
        ("Downtown", "DT-001"),
        ("Suburb East", "SE-002"),
        ("Industrial Park", "IP-003"),
        ("Residential North", "RN-004"),
    ],
)

cursor.executemany(
    "INSERT INTO vehicles (registration_number, capacity, status) VALUES (?, ?, ?)",
    [
        ("WM-1001", 5000.0, "available"),
        ("WM-1002", 8000.0, "available"),
        ("WM-1003", 3000.0, "maintenance"),
        ("WM-1004", 6000.0, "available"),
    ],
)

cursor.executemany(
    "INSERT INTO drivers (name, phone) VALUES (?, ?)",
    [
        ("Rajesh Kumar", "9876543210"),
        ("Amit Sharma", "9876543211"),
        ("Priya Patel", "9876543212"),
    ],
)

cursor.executemany(
    "INSERT INTO complaints (zone_id, description) VALUES (?, ?)",
    [
        (1, "Garbage not collected for 3 days"),
        (2, "Overflowing bins near park entrance"),
        (3, "Hazardous waste dumped near factory"),
    ],
)

conn.commit()
conn.close()

print("Database seeded successfully!")
print("  - 4 Zones")
print("  - 4 Vehicles")
print("  - 3 Drivers")
print("  - 3 Complaints")
