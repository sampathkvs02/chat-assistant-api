from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "company.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employees (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Department TEXT NOT NULL,
        Salary INTEGER NOT NULL,
        Hire_Date TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Departments (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL UNIQUE,
        Manager TEXT NOT NULL
    )
    """)

    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM Employees")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO Employees (ID, Name, Department, Salary, Hire_Date)
        VALUES (?, ?, ?, ?, ?)
        """, [
            (1, "Alice", "Sales", 50000, "2021-01-15"),
            (2, "Bob", "Engineering", 70000, "2020-06-10"),
            (3, "Charlie", "Marketing", 60000, "2022-03-20")
        ])

    cursor.execute("SELECT COUNT(*) FROM Departments")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO Departments (ID, Name, Manager)
        VALUES (?, ?, ?)
        """, [
            (1, "Sales", "Alice"),
            (2, "Engineering", "Bob"),
            (3, "Marketing", "Charlie")
        ])
    conn.commit()
    conn.close()

initialize_database()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return (result[0] if result else None) if one else result

@app.route('/')
def home():
    return jsonify({"message": "Chat Assistant API is running!"}), 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get("query", "").strip().lower()
    departments = ["Sales", "Engineering", "Marketing"]
    department = next((dept for dept in departments if dept.lower() in query), None)
    
    if department:
        result = query_db("SELECT Manager FROM Departments WHERE Name = ?", (department,), one=True)
        response = f"The manager of {department} is {result[0]}" if result else f"No manager found for {department}."
    else:
        response = "Sorry, I didn't understand the department in your query."
    return jsonify({"response": response})

@app.route('/managers', methods=['GET'])
def list_managers():
    results = query_db("SELECT Name, Manager FROM Departments")
    return jsonify({row[0]: row[1] for row in results})

@app.route('/managers/add', methods=['POST'])
def add_manager():
    data = request.json
    department = data.get("department")
    manager = data.get("manager")
    
    if not department or not manager:
        return jsonify({"error": "Provide 'department' and 'manager'."}), 400
    
    existing = query_db("SELECT Name FROM Departments WHERE Name = ?", (department,), one=True)
    if existing:
        return jsonify({"error": f"Department '{department}' already exists."}), 409
    
    query_db("INSERT INTO Departments (Name, Manager) VALUES (?, ?)", (department, manager))
    return jsonify({"message": f"Added {manager} as manager of {department}."}), 200

@app.route('/managers/update', methods=['PUT'])
def update_manager():
    data = request.json
    department = data.get("department")
    manager = data.get("manager")
    
    if not department or not manager:
        return jsonify({"error": "Provide 'department' and 'manager'."}), 400
    
    existing = query_db("SELECT Name FROM Departments WHERE Name = ?", (department,), one=True)
    if not existing:
        return jsonify({"error": f"Department '{department}' not found."}), 404
    
    query_db("UPDATE Departments SET Manager = ? WHERE Name = ?", (manager, department))
    return jsonify({"message": f"Updated {department} manager to {manager}."}), 200

@app.route('/managers/delete', methods=['DELETE'])
def delete_manager():
    department = request.json.get("department")
    
    if not department:
        return jsonify({"error": "Provide 'department'."}), 400
    
    existing = query_db("SELECT Name FROM Departments WHERE Name = ?", (department,), one=True)
    if not existing:
        return jsonify({"error": f"Department '{department}' not found."}), 404
    
    query_db("DELETE FROM Departments WHERE Name = ?", (department,))
    return jsonify({"message": f"Deleted manager of {department}."}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              