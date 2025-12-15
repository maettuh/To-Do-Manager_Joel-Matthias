from datetime import datetime

# Konstanten & Format-Strings
CSV_FIELDS = ["id", "description", "priority", "due_date", "status", "created_at"]

DATE_FMT = "%Y-%m-%d"

PRIO_LOW = "low"
PRIO_MED = "medium"
PRIO_HIGH = "high"
VALID_PRIORITIES = (PRIO_LOW, PRIO_MED, PRIO_HIGH)

STATUS_OPEN = "open"
STATUS_DONE = "done"
VALID_STATUS = (STATUS_OPEN, STATUS_DONE)

# Dateien / Backup Funktionen
def file_exists(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8"):
            return True
    except FileNotFoundError:
        return False
    except Exception:  # andere Fehler bedeuten nicht zuverlässig 'nicht existent'
        return True

#Erstellt eine Backup-Kopie der Datei mit Zeitstempel
def backup_copy_file(src_path: str) -> str | None: 
    if not file_exists(src_path):
        return None
    try:
        with open(src_path, "rb") as fsrc:
            data = fsrc.read()
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{src_path}.bak-{ts}"
        with open(bak, "wb") as fdst: # Schreibt die Backup-Datei
            fdst.write(data)
        print(f"Datei gesichert als: {bak}")
        return bak
    except Exception as e: # Allgemeiner Fehler beim Backup
        print("Konnte Backup nicht erstellen:", e)
        return None
