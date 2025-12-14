from datetime import datetime

from input_validation import (
    input_nonempty,
    input_priority,
    input_date,
    input_int,
    is_valid_date,
) # Importiert die Funktionen zur Prüfung der Eingaben
from hilfsfunktionen import (
    PRIO_LOW,
    PRIO_MED,
    PRIO_HIGH,
    STATUS_OPEN,
    STATUS_DONE,
    DATE_FMT,
) # Importiert vordefinierte Werte und Formate

# Aufgaben-Funktionen
def add_task(todos, next_id_fn, make_task_fn):
    print("\n--- Aufgabe hinzufügen ---")
    desc = input_nonempty("Beschreibung: ")
    prio = input_priority(PRIO_MED)
    due = input_date(allow_empty=True)
    tid = next_id_fn(todos) # Holt die nächste freie ID für die neue Aufgabe
    todos.append(make_task_fn(tid, desc, prio, due)) # Erstellt die Aufgabe und fügt sie zur Liste hinzu
    print(f"Aufgabe #{tid} hinzugefügt.")

# Sucht Aufgabe mit bestimmter ID (lineare Suche).
def find_task_by_id(todos, tid):
    for t in todos:
        if t["id"] == tid: # Vergleicht die ID der aktuellen Aufgabe mit der gesuchten ID
            return t
    return None

# Bearbeitet eine bestehende Aufgabe.
def edit_task(todos):
    print("\n--- Aufgabe bearbeiten ---")
    tid = input_int("ID der Aufgabe: ") # Fragt nach ID, muss also eine Zahl sein
    t = find_task_by_id(todos, tid)
    if t is None:
        print("Keine Aufgabe mit dieser ID gefunden.")
        return

    print("Leerlassen, um Feld unverändert zu lassen.")
    new_desc = input(f"Neue Beschreibung [{t['description']}]: ").strip()
    if new_desc != "":
        t["description"] = new_desc # Aktualisiert Beschreibung, wenn nicht leer

    new_prio = input(
        f"Neue Priorität [{PRIO_LOW}/{PRIO_MED}/{PRIO_HIGH}] (Enter=unverändert): "
    ).strip().lower()
    if new_prio != "":
        if new_prio in (PRIO_LOW, PRIO_MED, PRIO_HIGH):
            t["priority"] = new_prio # Aktualisiert Priorität, wenn gültig
        else:
            print("Ungültige Priorität – unverändert belassen.")

    new_due_raw = input(
        "Neues Fälligkeitsdatum (YYYY-MM-DD, leer=unverändert, '-'=entfernen): "
    ).strip()
    if new_due_raw == "-":
        t["due_date"] = None # Setzt Datum auf None (Datum entfernen)
    elif new_due_raw != "":
        if is_valid_date(new_due_raw):
            t["due_date"] = new_due_raw # Aktualisiert Datum, wenn Format korrekt
        else:
            print("Ungültiges Datum – unverändert belassen.")

    print("Aufgabe aktualisiert.")

# Initialisiert Beispiel-Aufgaben.
def toggle_status(todos):
    print("\n--- Status umschalten (open/done) ---")
    tid = input_int("ID der Aufgabe: ")
    t = find_task_by_id(todos, tid)
    if t is None:
        print("Keine Aufgabe mit dieser ID gefunden.")
        return
    if t["status"] == STATUS_OPEN: # Wenn Status offen ist, dann auf erledigt setzten
        t["status"] = STATUS_DONE
    else:
        t["status"] = STATUS_OPEN #Ansonsten auf offen setzten
    print(f"Status geändert zu '{t['status']}'.")

# Löscht eine Aufgabe.
def delete_task(todos):
    print("\n--- Aufgabe löschen ---")
    tid = input_int("ID der Aufgabe: ")
    new_list = []
    deleted = False
    for t in todos:
        if t["id"] == tid:
            deleted = True # Aufgabe gefunden, wird gelöscht
        else:
            new_list.append(t) # Behält alle Aufgaben ausser der zu löschenden
    if deleted:
        todos[:] = new_list  # Aktualisiert die Original-Liste (in-place)
        print("Aufgabe gelöscht.")
    else:
        print("Keine Aufgabe mit dieser ID gefunden.")

 # Sortierschlüssel
def sort_key_due_then_priority(task):
    # Sortierregel 1: Fälligkeitsdatum
    if task["due_date"] is None:
        due_tuple = (datetime.max.date(),) # Kein Datum? Kommt ans Ende der Liste
    else:
        due_tuple = (datetime.strptime(task["due_date"], DATE_FMT).date(),) # Datumstext in ein vergleichbares Datumsobjekt umwandeln
    # Sortierregel 2: Priorität (Mapping von Text auf Zahl, 0 = höchste Prio)
    if task["priority"] == PRIO_HIGH:
        pr = 0 
    elif task["priority"] == PRIO_MED:
        pr = 1
    else:
        pr = 2
    return due_tuple + (pr, task["id"]) # Tupel wird sequenziell sortiert (Datum, dann Prio, dann ID)

# Listet Aufgaben mit optionalen Filtern und Sortierung.
def list_tasks(todos, search=None, status=None, priority=None, sort_by_due=True):
    result = []
    for t in todos:
        ok = True
        # Filter 1: Textsuche in der Beschreibung (case-insensitive)
        if search is not None and search != "":
            if search.lower() not in t["description"].lower():
                ok = False
        # Filter 2: Status
        if ok and status is not None and status != "":
            if t["status"] != status:
                ok = False
        # Filter 3: Priorität
        if ok and priority is not None and priority != "":
            if t["priority"] != priority:
                ok = False
        if ok:
            result.append(t) # Aufgabe hat alle Filter bestanden
    if sort_by_due:
        # Sortiert die gefilterte Liste mit dem Sortierschlüssel von oben
        result = sorted(result, key=sort_key_due_then_priority)
    return result

# Gibt eine Liste von Aufgaben formatiert aus.
def print_tasks(tasks):
    if len(tasks) == 0:
        print("Keine Aufgaben gefunden.")
        return
    print("-" * 78)
    # Formatiert die Kopfzeile mit festen Breiten (z.B. ID 4 Zeichen, Beschreibung 40 Zeichen)
    print(f"{'ID':<4} {'Beschreibung':<40} {'Prio':<7} {'Fällig':<12} {'Status':<6}")
    print("-" * 78)
    for t in tasks:
        # Wenn 'due_date' None ist, wird ein "-" angezeigt
        due = t["due_date"] if t["due_date"] is not None else "-"
        desc = t["description"][:40] # Schneidet die Beschreibung nach 40 Zeichen ab
        print(f"{t['id']:<4} {desc:<40} {t['priority']:<7} {due:<12} {t['status']:<6}") # Gibt die formatierte Zeile aus
    print("-" * 78)
