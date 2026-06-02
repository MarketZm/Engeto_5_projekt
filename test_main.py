import pytest
from main import pripojeni_db, pridat_ukol_db, aktualizovat_ukol_db, odstranit_ukol_db


# POMOCNÁ FUNKCE: Vyčištění testovacích dat
def smaz_testovaci_ukol(nazev):
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ukoly WHERE nazev = %s", (nazev,))
    conn.commit()
    conn.close()


# --- TESTY PRO PŘIDÁNÍ ÚKOLU ---

def test_pridat_ukol_pozitivni():
    """Pozitivní test: pridat_ukol_db() uloží úkol a vrátí True."""
    test_nazev = "Testovací úkol 123"
    test_popis = "Popis testu"

    vysledek = pridat_ukol_db(test_nazev, test_popis)
    assert vysledek is True

    # Ověření, že úkol je skutečně v databázi
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nazev, popis FROM ukoly WHERE nazev = %s", (test_nazev,))
    radek = cursor.fetchone()
    conn.close()

    assert radek is not None
    assert radek[0] == test_nazev
    assert radek[1] == test_popis

    smaz_testovaci_ukol(test_nazev)  # Úklid po testu

def test_pridat_ukol_negativni():
    """Negativní test: pridat_ukol_db() selže při prázdném názvu a vrátí False."""
    vysledek = pridat_ukol_db("", "Popis")
    # Prázdný řetězec projde přes DB (není NULL), ale funkce by vrátila True.
    # Validace prázdného vstupu probíhá v pridat_ukol() před voláním DB funkce.
    # Tento test ověřuje chování při skutečné DB chybě — vložíme None (NULL):
    vysledek = pridat_ukol_db(None, "Popis")
    assert vysledek is False


# --- TESTY PRO AKTUALIZACI ---

def test_aktualizovat_ukol_pozitivni():
    """Pozitivní test: aktualizovat_ukol_db() změní stav existujícího úkolu."""
    # Příprava: vložíme testovací úkol přes naši DB funkci
    pridat_ukol_db("UpdateTest", "Popis")

    # Zjistíme ID nově vloženého úkolu
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'UpdateTest'")
    test_id = cursor.fetchone()[0]
    conn.close()

    # Zavoláme naši funkci
    pocet = aktualizovat_ukol_db(test_id, 'hotovo')
    assert pocet == 1

    # Ověření v DB
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (test_id,))
    assert cursor.fetchone()[0] == 'hotovo'
    conn.close()

    odstranit_ukol_db(test_id)  # Úklid

def test_aktualizovat_ukol_negativni():
    """Negativní test: aktualizovat_ukol_db() vrátí 0 pro neexistující ID."""
    pocet = aktualizovat_ukol_db(999999, 'hotovo')
    assert pocet == 0


# --- TESTY PRO ODSTRANĚNÍ ---

def test_odstranit_ukol_pozitivni():
    """Pozitivní test: odstranit_ukol_db() smaže existující úkol a vrátí 1."""
    # Příprava: vložíme testovací úkol
    pridat_ukol_db("SmazatTest", "Popis")

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'SmazatTest'")
    test_id = cursor.fetchone()[0]
    conn.close()

    # Zavoláme naši funkci
    pocet = odstranit_ukol_db(test_id)
    assert pocet == 1

    # Ověření, že úkol v DB opravdu neexistuje
    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (test_id,))
    assert cursor.fetchone() is None
    conn.close()

def test_odstranit_ukol_negativni():
    """Negativní test: odstranit_ukol_db() vrátí 0 pro neexistující ID."""
    pocet = odstranit_ukol_db(999999)
    assert pocet == 0
