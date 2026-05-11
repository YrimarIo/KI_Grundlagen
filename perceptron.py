#!/usr/bin/env python3
"""
Beispiel 1: Einfaches Perzeptron

Dieses Skript zeigt das grundlegendste Bauelement eines neuronalen Netzes:
ein einzelnes Neuron (Perzeptron).

Was ist ein Perzeptron?
- Ein Perzeptron ist wie eine einfache Entscheidungs-Fabrik
- Es bekommt Eingaben (z.B. Sensorwerte) und gibt eine Entscheidung ab
- Analogie: Ein Türöffner mit 2 Schaltern - nur wenn BEIDE gedrückt sind, geht die Tür auf

Was dieses Skript zeigt:
- Wie ein Neuron Eingaben verarbeitet
- Was "Gewichte" und "Bias" bewirken
- Warum ein einzelnes Neuron nur einfache Probleme lösen kann (AND, OR)

Fuer Systemintegratoren:
Stellen Sie sich ein Perzeptron wie einen Regel-Engine vor:
  "WENN Sensor1=WERT1 UND Sensor2=WERT2 DANN Aktion"Ausgabe"

Die Gewichte bestimmen, wie stark jeder Sensor die Entscheidung beeinflusst.
Der Bias bestimmt die Schwelle - wie 'empfindlich' das Neuron ist.
"""

import numpy as np


def sigmoid(x):
    """
    Die Sigmoid-Aktivierungsfunktion.

    Was macht diese Funktion?
    - Wandelt jede beliebige Zahl in einen Wert zwischen 0 und 1 um
    - 0 = "Nein" / "Aus" / "Klasse 0"
    - 1 = "Ja" / "An" / "Klasse 1"
    - Werte nahe 0.5 = "unsicher"

    Warum ist das wichtig?
    - Ohne Sigmoid wuerden die Werte unbegrenzt wachsen
    - Sigmoid macht die Ausgabe interpretierbar (wie eine Wahrscheinlichkeit)

    Beispiele:
    - sigmoid(-10) = 0.0000 (fast immer "Nein")
    - sigmoid(0)   = 0.5000 (völlig unsicher)
    - sigmoid(10)  = 0.9999 (fast immer "Ja")

    Args:
        x: Eine Zahl oder ein Array von Zahlen

    Returns:
        Wert(e) zwischen 0 und 1
    """
    return 1 / (1 + np.exp(-x))


def perceptron_vorhersage(input_werte, gewichte, bias):
    """
    Berechnet die Ausgabe eines Perzeptrons fuer gegebene Eingaben.

    Wie funktioniert die Berechnung?
    1. Jeder Eingang bekommt ein Gewicht multipliziert (wie stark beeinflusst er?)
    2. Alle gewichteten Werte werden addiert
    3. Der Bias wird addiert (verschiebt die Entscheidungsschwelle)
    4. Sigmoid wandelt das Ergebnis in 0-1 um

    Mathematisch: output = sigmoid(input1*w1 + input2*w2 + ... + bias)

    Analogie fuer Systemintegratoren:
    Stellen Sie sich einen Alarm-System vor:
    - Eingang 1: Bewegungssensor (0 = ruhig, 1 = Bewegung)
    - Eingang 2: Fenstersensor (0 = geschlossen, 1 = geoeffnet)
    - Gewicht 1: 0.5 (Bewegung halb so wichtig)
    - Gewicht 2: 0.5 (Fenster halb so wichtig)
    - Bias: -0.7 (Schwelle: Alarm erst wenn SUMME > 0.7)

    Szenarien:
    - Kein Sensor aktiv: 0*0.5 + 0*0.5 - 0.7 = -0.7 -> sigmoid -> 0 (kein Alarm)
    - Fenster geoeffnet: 0*0.5 + 1*0.5 - 0.7 = -0.2 -> sigmoid -> 0.45 (kein Alarm)
    - BEIDE aktiv:     1*0.5 + 1*0.5 - 0.7 =  0.3 -> sigmoid -> 0.57 (Alarm!)

    Args:
        input_werte: Liste der Eingabewerte, z.B. [0, 1] fuer zwei Sensoren
        gewichte: Liste der Gewichte, z.B. [0.5, 0.5]
        bias: Der Bias-Wert (typischerweise negativ fuer eine Schwelle)

    Returns:
        Ein Wert zwischen 0 und 1:
        - Nahe 0: Das Neuron "stimmt nicht zu"
        - Nahe 1: Das Neuron "stimmt zu"
        - Nahe 0.5: Das Neuron ist "unsicher"
    """
    # Schritt 1: Gewichtete Summe berechnen
    # np.dot berechnet das Skalarprodukt: [x1,x2] dot [w1,w2] = x1*w1 + x2*w2
    gewichtete_summe = np.dot(input_werte, gewichte) + bias

    # Schritt 2: Durch Sigmoid in 0-1 wandeln
    ausgabe = sigmoid(gewichtete_summe)

    return ausgabe


def main():
    """
    Hauptfunktion: Demonstriert das Perzeptron mit AND- und OR-Logik.

    Warum AND und OR?
    - Das sind die einfachsten logischen Operationen
    - Ein einzelnes Perzeptron KANN AND und OR lösen
    - Ein einzelnes Perzeptron KANN XOR NICHT lösen (dafür braucht man mehrere Schichten)
    """
    print("=" * 50)
    print("Einfaches Perzeptron - Demo")
    print("=" * 50)

    # ========================================================================
    # BEISPIEL 1: AND-Logik
    # ========================================================================
    # AND bedeutet: Nur wenn BEIDE Eingaben 1 sind, ist das Ergebnis 1
    #
    # Wahrheitstabelle:
    # Eingabe 1 | Eingabe 2 | Ausgabe
    # ----------+-----------+--------
    #     0     |     0     |    0
    #     0     |     1     |    0
    #     1     |     0     |    0
    #     1     |     1     |    1

    print("\n--- AND-Logik ---")
    # Konfiguration fuer AND:
    # - Beide Eingaben gleich gewichtet (0.5)
    # - Bias von -0.7 bedeutet: SUMME muss > 0.7 sein fuer Ausgabe 1
    # - Nur wenn BEIDE Eingaben 1 sind: 1*0.5 + 1*0.5 = 1.0 > 0.7 -> Ausgabe 1
    gewichte_and = [0.5, 0.5]
    bias_and = -0.7

    # Alle moeglichen Eingabe-Kombinationen mit erwarteter Ausgabe
    test_faelle_and = [
        ([0, 0], 0),  # AND(0,0) = 0
        ([0, 1], 0),  # AND(0,1) = 0
        ([1, 0], 0),  # AND(1,0) = 0
        ([1, 1], 1),  # AND(1,1) = 1
    ]

    # Alle Testfaelle durchgehen und Ergebnisse anzeigen
    for eingang, erwartet in test_faelle_and:
        ergebnis = perceptron_vorhersage(eingang, gewichte_and, bias_and)
        # Wenn Ausgabe > 0.5, klassifizieren wir als "1", sonst "0"
        klassifiziert = 1 if ergebnis > 0.5 else 0
        # Prüfen ob Ergebnis korrekt
        status = "OK" if klassifiziert == erwartet else "FEHLER"
        print(f"AND{tuple(eingang)} = {ergebnis:.4f} -> {klassifiziert} [{status}]")

    # ========================================================================
    # BEISPIEL 2: OR-Logik
    # ========================================================================
    # OR bedeutet: Wenn MINDESTENS eine Eingabe 1 ist, ist das Ergebnis 1
    #
    # Wahrheitstabelle:
    # Eingabe 1 | Eingabe 2 | Ausgabe
    # ----------+-----------+--------
    #     0     |     0     |    0
    #     0     |     1     |    1
    #     1     |     0     |    1
    #     1     |     1     |    1

    print("\n--- OR-Logik ---")
    # Konfiguration fuer OR:
    # - Gleiche Gewichte wie AND
    # - Aber: Bias von -0.3 (niedrigere Schwelle)
    # - Nur wenn BEIDE Eingaben 0 sind: 0*0.5 + 0*0.5 = 0 < 0.3 -> Ausgabe 0
    gewichte_or = [0.5, 0.5]
    bias_or = -0.3

    test_faelle_or = [
        ([0, 0], 0),  # OR(0,0) = 0
        ([0, 1], 1),  # OR(0,1) = 1
        ([1, 0], 1),  # OR(1,0) = 1
        ([1, 1], 1),  # OR(1,1) = 1
    ]

    for eingang, erwartet in test_faelle_or:
        ergebnis = perceptron_vorhersage(eingang, gewichte_or, bias_or)
        klassifiziert = 1 if ergebnis > 0.5 else 0
        status = "OK" if klassifiziert == erwartet else "FEHLER"
        print(f"OR{tuple(eingang)} = {ergebnis:.4f} -> {klassifiziert} [{status}]")

    # ========================================================================
    # WICHTIGER HINWEIS: XOR
    # ========================================================================

    print("\n" + "=" * 50)
    print("Hinweis: XOR kann mit einem einzelnen Perzeptron")
    print("NICHT geloest werden!")
    print()
    print("XOR bedeutet: Ausgabe ist 1 wenn EXAKT EINE Eingabe 1 ist")
    print("XOR(0,0)=0, XOR(0,1)=1, XOR(1,0)=1, XOR(1,1)=0")
    print()
    print("Grund: XOR ist nicht linear trennbar - dafuer benoetigt man")
    print("ein neuronales Netz mit mehreren Schichten (siehe Beispiel 3)")
    print("=" * 50)


# Dieser Teil sorgt dafuer, dass main() nur ausgefuehrt wird,
# wenn das Skript direkt gestartet wird (nicht wenn es importiert wird)
if __name__ == "__main__":
    main()
