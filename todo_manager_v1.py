# python3
# Todo-Manager Projekt von Joel Fehr & Matthias Heiniger 

import csv # CSV-Import/Export damit über CSV-Dateien gespeichert werden kann
from datetime import datetime, timedelta # Import für Datum & Zeit damit mit Python 3.7 funktioniert

from hilfsfunktionen import (
    CSV_FIELDS,
    DATE_FMT,
    PRIO_LOW,
    PRIO_MED,
    PRIO_HIGH,
    STATUS_OPEN,
    STATUS_DONE,
    file_exists,
    backup_copy_file,
)
from input_validation import (
    input_nonempty,
    input_priority,
    input_date,
    input_int,
)
from reset import reset_storage
from task_menu import (
    add_task,
    edit_task,
    toggle_status,
    delete_task,
    list_tasks,
    print_tasks,
)

# Speicherpfade
STORE_FILENAME = "todo.csv"
STORE_PATH = STORE_FILENAME 

# Menü-Konstanten
MENU_EXIT = "0"
MENU_SHOW = "1"
MENU_ADD = "2"
MENU_EDIT = "3"
MENU_TOGGLE = "4"
MENU_DELETE = "5"
MENU_FILTER_SORT = "6"
MENU_RESET = "7"


# CSV-Load
def _normalize_for_csv(task: dict) -> dict:  # konvertiert id zu str
    return {
        "id": str(task["id"]),
        "description": task["description"],
        "priority": task["priority"],
        "due_date": task["due_date"] or "",
        "status": task["status"],
        "created_at": task["created_at"],
    }


def _parse_from_csv(row: dict) -> dict:  # Wandelt CSV-Strings zurück in unser Dict inkl. Typen.
    return {
        "id": int(row.get("id", "0") or "0"), 
        "description": row.get("description", ""),
        "priority": row.get("priority", PRIO_MED),
        "due_date": row.get("due_date") or None,
        "status": row.get("status", STATUS_OPEN),
        "created_at": row.get("created_at")
        or datetime.now().strftime("%Y-%m-%d %H.%M.%S"),
    }


def load_todos(path: str) -> list[dict]: # Lädt To-Dos aus CSV, oder initialisiert mit Seed-Daten.
    print(f"[Speicherort] {path}")
    if not file_exists(path):
        todos = seed_tasks()
        save_todos(path, todos)
        return todos

    try:
        with open(path, "r", encoding="utf-8", newline="") as f: 
            reader = csv.DictReader(f) # Liest CSV-Datei als Dicts
            if reader.fieldnames is None or any( # fehlende Spalten -> Backup + Neu
                h not in reader.fieldnames for h in CSV_FIELDS
            ):
                backup_copy_file(path)
                todos = seed_tasks()
                save_todos(path, todos)
                return todos
            rows = list(reader)
        todos = [_parse_from_csv(r) for r in rows] 
        if len(todos) == 0:
            todos = seed_tasks()
            save_todos(path, todos)
        return todos
    except Exception as e:
        print("CSV konnte nicht gelesen werden = Backup + Neuinitialisierung.")
        print("   Details:", e)
        backup_copy_file(path)
        todos = seed_tasks()
        save_todos(path, todos)
        return todos


def save_todos(path: str, todos: list[dict]) -> None:
    payload = [_normalize_for_csv(t) for t in todos]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in payload:
            w.writerow(r)
    print(f"[gespeichert] {path}  (Anzahl: {len(todos)})")


# Seed & Datenmodell
def seed_tasks() -> list[dict]:  # Erzeugt 3 Beispiel-Aufgaben (erste Ausführung).
    today = datetime.now().date()
    return [
        make_task(
            1,
            "README der Aufgabe lesen",
            PRIO_HIGH,
            (today + timedelta(days=2)).strftime(DATE_FMT),
        ),
        make_task(
            2,
            "Funktionen add/edit/delete implementieren",
            PRIO_MED,
            (today + timedelta(days=5)).strftime(DATE_FMT),
        ),
        make_task(
            3,
            "Tests & Doku schreiben",
            PRIO_LOW,
            (today + timedelta(days=7)).strftime(DATE_FMT),
        ),
    ]


def make_task( # Erstellt ein To-Do Dict.
    tid: int,
    description: str,
    priority: str,
    due_date: str | None,
    status: str = STATUS_OPEN,
) -> dict:
    return {
        "id": int(tid),
        "description": description,
        "priority": priority,
        "due_date": due_date,  # YYYY-MM-DD oder None
        "status": status,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def next_id(todos: list[dict]) -> int:
    max_id = 0
    for t in todos:
        if t["id"] > max_id:
            max_id = t["id"]
    return max_id + 1


def submenu_filters(todos: list[dict]) -> None: # Submenü für Filtern & Sortieren
    print("\n--- Filtern & Sortieren ---")
    search = input("Textsuche in Beschreibung (optional): ").strip()
    status = input(
        f"Status [{STATUS_OPEN}/{STATUS_DONE}] (leer = alle): "
    ).strip().lower()
    if not (status == "" or status == STATUS_OPEN or status == STATUS_DONE):
        print("Ungültiger Status – ignoriere Status-Filter.")
        status = ""
    prio = input(
        f"Priorität [{PRIO_LOW}/{PRIO_MED}/{PRIO_HIGH}] (leer = alle): "
    ).strip().lower()
    if not (prio == "" or prio == PRIO_LOW or prio == PRIO_MED or prio == PRIO_HIGH):
        print("Ungültige Priorität – ignoriere Prioritäts-Filter.")
        prio = ""
    sort_choice = input("Nach Fälligkeitsdatum sortieren? (JA/Nein): ").strip().lower()
    sort_by_due = sort_choice == "ja"

    filtered = list_tasks( # Wendet Filter & Sortierung an gemäss Eingaben
        todos,
        search=search,
        status=status or None,
        priority=prio or None,
        sort_by_due=sort_by_due,
    )
    print_tasks(filtered)


# Menü Anzeige
def show_menu() -> None:
    print(
        """
================= To-Do Manager (CSV) =================
1) Aufgaben anzeigen
2) Aufgabe hinzufügen
3) Aufgabe bearbeiten
4) Aufgabe als erledigt/unerledigt markieren
5) Aufgabe löschen
6) Filtern/Sortieren
7) Speicher zurücksetzen (Backup + Neu)
0) Beenden
"""
    )

# Main-Einstiegspunkt
def main() -> None:
    name = input("Wie heisst du? ").strip() or "Benutzer"
    todos = load_todos(STORE_PATH)

    print(
        f"\nHallo {name}! Hier sind deine aktuellen To-Dos:\n"
    )  
    print_tasks(list_tasks(todos, sort_by_due=True))

# Hauptmenü-Schleife
    choice = ""
    while choice != MENU_EXIT:
        show_menu()
        choice = input("Auswahl: ").strip()

        if choice == MENU_SHOW:
            print_tasks(list_tasks(todos, sort_by_due=True))
        elif choice == MENU_ADD:
            add_task(todos, next_id, make_task)
            save_todos(STORE_PATH, todos)
        elif choice == MENU_EDIT:
            edit_task(todos)
            save_todos(STORE_PATH, todos)
        elif choice == MENU_TOGGLE:
            toggle_status(todos)
            save_todos(STORE_PATH, todos)
        elif choice == MENU_DELETE:
            delete_task(todos)
            save_todos(STORE_PATH, todos)
        elif choice == MENU_FILTER_SORT:
            submenu_filters(todos)
        elif choice == MENU_RESET:
            reset_storage(STORE_PATH, seed_tasks, save_todos)
            # nach Reset neu laden
            todos[:] = load_todos(STORE_PATH)
        elif choice == MENU_EXIT:
            print("Bis bald!")
        else:
            print("Ungültige Auswahl. Bitte 0–7 eingeben.")

# Programmstart
if __name__ == "__main__":  
    try:
        main()
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer.")
