Projekt: Aufgabenlisten-Manager (To-Do-List Manager)
Autoren: Joël Fehr und Matthias Heiniger
Datum: 14.12.2025

1. PROJEKTBESCHREIBUNG UND ZIELSETZUNG

Im Rahmen dieses Informatikprojekts wurde ein Aufgabenlisten-Manager entwickelt. Das Ziel war die Implementierung einer Software, die Aufgaben speichert, verwaltet, filtert und sortiert.

Die Wahl fiel auf dieses Thema aufgrund des hohen Praxisbezugs, insbesondere im Studium, wo ein solcher Manager hilft, den Überblick zu behalten. 
Zudem bot das Projekt die Möglichkeit, zentrale Konzepte von Python (Listen, Dictionaries, Dateioperationen) modular und erweiterbar umzusetzen.

Das messbare Ziel des Projektes war die Erstellung eines stabilen Programms, das folgende Kernkriterien erfüllt:
1. CRUD-Funktionalität: Aufgaben können hinzugefügt, bearbeitet, entfernt und als erledigt markiert werden.
2. Persistenz: Die Daten werden in einer Datei gespeichert und sind nach einem Programmneustart wieder verfügbar.
3. Filterung und Suche: Aufgaben lassen sich nach Beschreibung, Status oder Priorität filtern.
4. Sortierung: Eine Funktion zur Sortierung nach Fälligkeitsdatum/Priorität ist implementiert.
5. Initialisierung: Beim ersten Start werden automatisch drei Beispiel-Aufgaben generiert.

2. DEMO UND TUTORIAL

Für einen schnellen Einstieg und zur Demonstration der geforderten Funktionalitäten liegt ein Video bei.

Video-Datei: Video_ProgrammierProjekt_Python.mp4

Das Video demonstriert den kompletten Workflow:
- Öffnen des Projektordners.
- Starten der Anwendung.
- Erstellung, Filterung und Löschung von Aufgaben gemäss den Projektanforderungen.
- Zusätzlich Demonstration der Backup-Funktion beim Zurücksetzen der Datenbank.

3. INSTALLATION UND START

Voraussetzungen:
Für die Ausführung wird Python 3 benötigt. Das Projekt basiert auf Python-Standardbibliotheken, weshalb keine externen Pakete installiert werden müssen.

Ausführung:
Öffnen Sie das Terminal im Projektverzeichnis und führen Sie das Hauptskript aus:

python3 todo_manager_v1.py

4. PROJEKTSTRUKTUR
Das Projekt ist modular aufgebaut und besteht aus mehreren Dateien, um Übersichtlichkeit
und Wartbarkeit zu gewährleisten:

- todo_manager_v1.py
  Hauptdatei, Einstiegspunkt des Programms (Main Loop).

- menu.py
  Enthält die Menülogik und die Benutzerinteraktion.

- input_validation.py
  Prüft und validiert Benutzereingaben (z. B. Datum, Zahlen, Prioritäten).

- hilfsfunktionen.py
  Enthält Konstanten und wiederverwendbare Hilfsfunktionen.

- todo.csv
  CSV-Datei zur persistenten Speicherung aller Aufgaben.

5. FUNKTIONSÜBERSICHT

Das Programm wird über ein textbasiertes Menü (CLI = Command Line Interface) gesteuert und deckt die im Projektbeschrieb geforderten Funktionen ab:

Hauptfunktionen:
(1) Aufgaben anzeigen
Listet alle Aufgaben auf. Die Sortierung erfolgt primär nach Fälligkeitsdatum (Deadline), sekundär nach Priorität.

(2) Aufgabe hinzufügen
Erfasst eine neue Aufgabe mit Beschreibung, Priorität (niedrig, mittel, hoch) und Fälligkeitsdatum.

(3) Aufgabe bearbeiten
Ermöglicht die nachträgliche Änderung aller Attribute einer Aufgabe.

(4) Status umschalten
Markiert offene Aufgaben als erledigt und umgekehrt.

(5) Aufgabe löschen
Entfernt Aufgaben permanent aus der Liste.

(6) Filtern und Sortieren
Bietet eine Textsuche sowie Filter für Status und Priorität, um spezifische Aufgaben schnell zu finden.

(7) Speicher zurücksetzen
Setzt das System auf den Auslieferungszustand zurück. Dabei wird, wie in der Zielsetzung definiert, die Datenbank geleert und mit den drei initialen Beispiel-To-Dos neu befüllt. 
Zuvor wird automatisch eine Sicherheitskopie der alten Daten erstellt (txt.).

6. TECHNISCHE UMSETZUNG

Die Umsetzung erfolgte gemäss den Anforderungen der Aufgabenstellung in Python:

- Datenstruktur: Die Aufgaben werden zur Laufzeit als Liste von Dictionaries verwaltet.
- Speicherung: Die Persistenz wird durch CSV-Dateioperationen sichergestellt (todo.csv).
- Modularität: Der Code ist in logische Module unterteilt (Main, Menü, Validierung, Hilfsfunktionen), um die geforderte Erweiterbarkeit zu gewährleisten.
- Validierung: Eingaben wie Datum oder Priorität werden geprüft, um Programmabstürze zu verhindern.

7. BEISPIELHAFTER ABLAUF

(1.) Programmstart -> Automatisches Laden der gespeicherten Aufgaben (Beispiel Daten)
(2.) Auswahl "Aufgabe hinzufügen" = Eingabe 1
(3.) Eingabe:
   - Beschreibung: "Informatik Projekt abgeben"
   - Priorität: hoch
   - Fälligkeitsdatum: 2025-12-20
(4.) Aufgabe erscheint sortiert in der Aufgabenliste
(5.) Weitere Möglichkeiten mit der Eingabe 0-7

8. FAZIT
Mit dem Aufgabenlisten-Manager ist es gelungen, eine stabile und funktionale Anwendung zu erstellen, die den Anforderungen entspricht. 
Das Programm bietet eine solide Grundlage für die Organisation des Studienalltags und kann bei Bedarf modular erweitert werden.