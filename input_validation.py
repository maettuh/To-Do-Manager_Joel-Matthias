# input_validation.py

from datetime import datetime
from hilfsfunktionen import DATE_FMT, PRIO_LOW, PRIO_MED, PRIO_HIGH


# Input-Validierung

def input_nonempty(prompt: str) -> str: 
    text = input(prompt).strip() # .strip() entfernt Leerzeichen am Anfang/Ende
    while text == "": # Wiederholt die Frage, solange die Eingabe leer ist
        print("Eingabe darf nicht leer sein.")
        text = input(prompt).strip()
    return text


def input_priority(default: str = PRIO_MED) -> str:
    # .lower() macht die Eingabe klein (High -> high) für den Vergleich
    entry = input(
        f"Priorität [{PRIO_LOW}/{PRIO_MED}/{PRIO_HIGH}] (Enter='{default}'): "
    ).strip().lower()

    if entry == "":
        return default # Bei leere Eingabe (Enter) Standardwert nehmen
    # Solange die Eingabe keines der gültigen Wörter ist, weiterfragen
    while entry not in (PRIO_LOW, PRIO_MED, PRIO_HIGH):
        print("Ungültige Priorität.")
        entry = input(
            f"Priorität [{PRIO_LOW}/{PRIO_MED}/{PRIO_HIGH}] (Enter='{default}'): "
        ).strip().lower()

        if entry == "":
            return default 
    return entry


def is_valid_date(s: str) -> bool:
    try:
        datetime.strptime(s, DATE_FMT) # Versucht, den Text als Datum zu lesen
        return True # Datum ist gültig
    except Exception:
        return False # Fehler (z.B. falsches Format): Ungültig


def input_date(allow_empty: bool = True) -> str | None:
    raw = input("Fälligkeitsdatum (YYYY-MM-DD, leer = kein Datum): ").strip()

    if raw == "" and allow_empty:
        return None # Leere Eingabe ist okay, hat dann einfach kein Datum

    while not is_valid_date(raw): # Prüft mit der Funktion von oben, ob es passt
        print("Bitte Datum als YYYY-MM-DD eingeben (z. B. 2025-10-31).")
        raw = input(
            "Fälligkeitsdatum (YYYY-MM-DD, leer = kein Datum): "
        ).strip()

        if raw == "" and allow_empty:
            return None

    return raw


def input_int(prompt: str) -> int:
    raw = input(prompt).strip()
    while not raw.isdigit(): # Prüft, ob der String nur aus Zahlen besteht
        print("Bitte eine gültige ganze Zahl eingeben.") 
        raw = input(prompt).strip()
    return int(raw) # Wandelt den Text in eine Zahl um


