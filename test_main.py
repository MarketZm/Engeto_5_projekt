import pytest
from main import pripojeni_db

# POMOCNÁ FUNKCE: Vyčištění testovacích dat
def smaz_testovaci_ukol(nazev):
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ukoly WHERE nazev = %s", (nazev,))
    conn.commit()
    conn.close()

# --- TESTY PRO PŘIDÁNÍ ÚKOLU ---

def test_pridat_ukol_pozitivni():
    """Pozitivní test: Ověří, že se úkol korektně uloží do DB."""
    test_nazev = "Testovací úkol 123"
    test_popis = "Popis testu"
    
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (test_nazev, test_popis))
    conn.commit()
    
    # Ověření, že tam je
    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", (test_nazev,))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == test_nazev
    
    smaz_testovaci_ukol(test_nazev) # Úklid po testu
    conn.close()

def test_pridat_ukol_negativni():
    """Negativní test: Simulace chyby (např. chybějící název v SQL)."""
    conn = pripojeni_db()
    cursor = conn.cursor()
    # Pokus o vložení NULL do sloupce, který ho nepovoluje (nazev)
    with pytest.raises(Exception):
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (NULL, 'Popis')")
    conn.close()

# --- TESTY PRO AKTUALIZACI ---

def test_aktualizovat_ukol_pozitivni():
    """Pozitivní test: Změna stavu existujícího úkolu."""
    conn = pripojeni_db()
    cursor = conn.cursor()
    # Nejdřív vytvoříme dočasný úkol
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES ('UpdateTest', 'Popis')")
    test_id = cursor.lastrowid
    
    # Aktualizace na 'hotovo'
    cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", ('hotovo', test_id))
    conn.commit()
    
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (test_id,))
    assert cursor.fetchone()[0] == 'hotovo'
    
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (test_id,)) # Úklid
    conn.commit()
    conn.close()

def test_aktualizovat_ukol_negativni():
    """Negativní test: Pokus o aktualizaci neexistujícího ID."""
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE ukoly SET stav = 'hotovo' WHERE id = 999999")
    # V SQL UPDATE neexistujícího ID nevyhodí chybu, ale ovlivní 0 řádků
    assert cursor.rowcount == 0
    conn.close()

# --- TESTY PRO ODSTRANĚNÍ ---

def test_odstranit_ukol_pozitivni():
    """Pozitivní test: Úspěšné smazání úkolu."""
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES ('SmazatTest', 'Popis')")
    test_id = cursor.lastrowid
    
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (test_id,))
    conn.commit()
    
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (test_id,))
    assert cursor.fetchone() is None
    conn.close()

def test_odstranit_ukol_negativni():
    """Negativní test: Smazání neexistujícího ID."""
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ukoly WHERE id = 999999")
    assert cursor.rowcount == 0
    conn.close()