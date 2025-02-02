import pytest
import sqlite3
from app import app, DATABASE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset database before each test
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Departments")
        cursor.execute("DELETE FROM Employees")
        conn.commit()
        conn.close()
        
        # Re-initialize sample data
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.executemany("""
        INSERT INTO Employees (ID, Name, Department, Salary, Hire_Date)
        VALUES (?, ?, ?, ?, ?)
        """, [
            (1, "Alice", "Sales", 50000, "2021-01-15"),
            (2, "Bob", "Engineering", 70000, "2020-06-10"),
            (3, "Charlie", "Marketing", 60000, "2022-03-20")
        ])
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
        yield client

def test_chat_endpoint(client):
    response = client.post('/chat', json={"query": "Who is the manager of Sales?"})
    assert response.status_code == 200
    assert b"Alice" in response.data  # Now passes!

def test_add_manager(client):
    response = client.post('/managers/add', json={"department": "Legal", "manager": "Laura"})
    assert response.status_code == 200  # Now passes!

def test_delete_manager(client):
    response = client.delete('/managers/delete', json={"department": "Marketing"})
    assert response.status_code == 200  # Now passes!