import sqlite3

# Connect to the database
conn = sqlite3.connect('hackaura.db')
cursor = conn.cursor()

# Check what's in the database
cursor.execute("SELECT id, assigned_service FROM call_records")
rows = cursor.fetchall()
print("Current data in database:")
for row in rows:
    print(f"ID: {row[0]}, Service: {row[1]}")

# Fix the enum values
updates = {
    'Fire Department': 'FIRE_DEPARTMENT',
    'Ambulance': 'AMBULANCE', 
    'Police': 'POLICE',
    'Multiple Services': 'MULTIPLE_SERVICES',
    'Crisis Response': 'CRISIS_RESPONSE'
}

for old_value, new_value in updates.items():
    cursor.execute("UPDATE call_records SET assigned_service = ? WHERE assigned_service = ?", (new_value, old_value))
    print(f"Updated {cursor.rowcount} records from '{old_value}' to '{new_value}'")

conn.commit()
conn.close()

print("Database enum values fixed!")
