import pytest
from main import pripojeni_db

def test_db_connection():
    """Testuje, zda se dokážeme připojit k databázi."""
    connection = pripojeni_db()
    assert connection is not None
    if connection:
        assert connection.is_connected()
        connection.close()

def test_vytvoreni_tabulky_existuje():
    """Testuje, zda v DB existuje tabulka ukoly."""
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE 'ukoly'")
    result = cursor.fetchone()
    assert result is not None  # Tabulka musí existovat
    conn.close()