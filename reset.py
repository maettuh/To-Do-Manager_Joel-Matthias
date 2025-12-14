from hilfsfunktionen import file_exists, backup_copy_file


def reset_storage(store_path: str, seed_fn, save_fn) -> None: #Setzt den Speicher zurück, indem eine Sicherungskopie erstellt und der Speicher neu initialisiert wird.
    print("\n--- Speicher zurücksetzen ---")
    if file_exists(store_path):
        backup_copy_file(store_path)  # erstellt Kopie
    todos = seed_fn() # Lädt die Startdaten (die 3 Beispiele)
    save_fn(store_path, todos) # Überschreibt die Datei mit den neuen Daten
    print("Speicher neu initialisiert.")
