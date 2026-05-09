-- Vytvoření databáze (pokud ještě neexistuje)
CREATE DATABASE IF NOT EXISTS task_manager_db;
USE task_manager_db;

-- Vytvoření tabulky 'ukoly' podle zadání
CREATE TABLE IF NOT EXISTS ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- automatické ID
    nazev VARCHAR(255) NOT NULL,             -- název (povinný)
    popis TEXT NOT NULL,                     -- popis (povinný)
    stav ENUM('nezahájeno', 'hotovo', 'probíhá') DEFAULT 'nezahájeno', -- stav
    datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- datum vytvoření
);
SELECT * FROM ukoly;