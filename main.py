import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    """Vytvoří připojení k MySQL databázi."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MarZem9957',  # SEM NAPIŠ SVÉ HESLO
            database='task_manager_db'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Chyba při připojení k MySQL: {e}")
        return None

def vytvoreni_tabulky():
    """Vytvoří tabulku 'ukoly', pokud ještě neexistuje."""
    conn = pripojeni_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('nezahájeno', 'hotovo', 'probíhá') DEFAULT 'nezahájeno',
                datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(query)
            conn.commit()
            print("Tabulka 'ukoly' je připravena.")
        except Error as e:
            print(f"Chyba při vytváření tabulky: {e}")
        finally:
            cursor.close()
            conn.close()


# --- PŘIDÁNÍ ÚKOLU ---

def pridat_ukol_db(nazev, popis):
    """Uloží nový úkol do databáze. Vrátí True při úspěchu, False při chybě."""
    conn = pripojeni_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
            cursor.execute(query, (nazev, popis))
            conn.commit()
            return True
        except Error as e:
            print(f"Chyba při přidávání úkolu: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def pridat_ukol():
    nazev = input("Zadejte název úkolu: ").strip()
    popis = input("Zadejte popis úkolu: ").strip()

    if not nazev or not popis:
        print("Chyba: Název i popis musí být vyplněny!")
        return

    if pridat_ukol_db(nazev, popis):
        print(f"Úkol '{nazev}' byl úspěšně přidán.")


# --- ZOBRAZENÍ ÚKOLŮ ---

def zobrazit_ukoly_db(stav=None):
    """Načte úkoly z DB. Pokud je zadán stav, filtruje podle něj."""
    conn = pripojeni_db()
    if conn:
        try:
            cursor = conn.cursor()
            if stav:
                cursor.execute("SELECT * FROM ukoly WHERE stav = %s", (stav,))
            else:
                cursor.execute("SELECT * FROM ukoly")
            return cursor.fetchall()
        except Error as e:
            print(f"Chyba při načítání úkolů: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def zobrazit_ukoly():
    print("\n--- ZOBRAZENÍ ÚKOLŮ ---")
    print("1. Zobrazit všechny úkoly")
    print("2. Filtrovat podle stavu (nezahájeno, probíhá, hotovo)")

    volba = input("Vyberte možnost (1-2): ")

    if volba == '1':
        vysledky = zobrazit_ukoly_db()
    elif volba == '2':
        stav = input("Zadejte stav pro filtr: ")
        vysledky = zobrazit_ukoly_db(stav)
    else:
        print("Neplatná volba.")
        return

    if not vysledky:
        print("Nenalezeny žádné úkoly.")
    else:
        print("-" * 50)
        for radek in vysledky:
            print(f"ID: {radek[0]} | Název: {radek[1]}")
            print(f"Stav: {radek[3]}")
            print(f"Popis: {radek[2]}")
            print("-" * 50)


# --- AKTUALIZACE ÚKOLU ---

def aktualizovat_ukol_db(id_ukolu, novy_stav):
    """Aktualizuje stav úkolu v DB. Vrátí počet ovlivněných řádků."""
    conn = pripojeni_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE ukoly SET stav = %s WHERE id = %s"
            cursor.execute(query, (novy_stav, id_ukolu))
            conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Chyba při aktualizaci: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()
    return 0

def aktualizovat_ukol():
    try:
        id_ukolu = int(input("Zadejte ID úkolu, který chcete aktualizovat: "))
        novy_stav = input("Zadejte nový stav (nezahájeno/probíhá/hotovo): ")

        pocet = aktualizovat_ukol_db(id_ukolu, novy_stav)
        if pocet > 0:
            print(f"Úkol s ID {id_ukolu} byl aktualizován.")
        else:
            print(f"Úkol s ID {id_ukolu} nebyl nalezen.")
    except ValueError:
        print("Chyba: ID musí být číslo!")


# --- ODSTRANĚNÍ ÚKOLU ---

def odstranit_ukol_db(id_ukolu):
    """Smaže úkol z DB podle ID. Vrátí počet ovlivněných řádků."""
    conn = pripojeni_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM ukoly WHERE id = %s"
            cursor.execute(query, (id_ukolu,))
            conn.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Chyba při odstraňování: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()
    return 0

def odstranit_ukol():
    try:
        id_ukolu = int(input("Zadejte ID úkolu, který chcete odstranit: "))

        pocet = odstranit_ukol_db(id_ukolu)
        if pocet > 0:
            print(f"Úkol s ID {id_ukolu} byl úspěšně odstraněn.")
        else:
            print(f"Úkol s ID {id_ukolu} nebyl nalezen.")
    except ValueError:
        print("Chyba: ID musí být číslo!")


def hlavni_menu():
    while True:
        print("\n--- HLAVNÍ MENU ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        volba = input("Vyberte možnost (1-5): ")

        if volba == '1':
            pridat_ukol()
        elif volba == '2':
            zobrazit_ukoly()
        elif volba == '3':
            aktualizovat_ukol()
        elif volba == '4':
            odstranit_ukol()
        elif volba == '5':
            print("Ukončuji program. Na shledanou!")
            break
        else:
            print("Neplatná volba, zkuste to znovu.")


if __name__ == "__main__":
    vytvoreni_tabulky()
    hlavni_menu()
